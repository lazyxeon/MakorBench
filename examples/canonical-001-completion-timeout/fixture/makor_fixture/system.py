from __future__ import annotations

from dataclasses import dataclass

from .clock import FakeClock
from .completion import ChannelPool, CompletionChannel, CompletionClient, CompletionGateway
from .scheduler import Scheduler
from .stores import ArtifactStore, BillingLedger
from .telemetry import Telemetry
from .token_manager import TokenManager
from .worker import Worker


@dataclass(frozen=True)
class FixtureConfig:
    lease_timeout: float = 45.0
    reconciliation_interval: float = 60.0
    pool_size: int = 1
    start_time: float = 0.0


class FixtureSystem:
    def __init__(
        self,
        config: FixtureConfig | None = None,
        *,
        channel_type: type[CompletionChannel] = CompletionChannel,
    ) -> None:
        self.config = config or FixtureConfig()
        self.clock = FakeClock(self.config.start_time)
        self.telemetry = Telemetry(self.clock)
        self.artifacts = ArtifactStore(self.telemetry)
        self.billing = BillingLedger(self.telemetry)
        self.tokens = TokenManager(self.clock, self.telemetry)
        self.scheduler = Scheduler(
            self.clock,
            self.telemetry,
            self.artifacts,
            lease_timeout=self.config.lease_timeout,
            reconciliation_interval=self.config.reconciliation_interval,
        )
        self.gateway = CompletionGateway(self.tokens, self.scheduler, self.telemetry)
        self.pool = ChannelPool(
            clock=self.clock,
            token_manager=self.tokens,
            gateway=self.gateway,
            telemetry=self.telemetry,
            max_size=self.config.pool_size,
            channel_type=channel_type,
        )
        self.completion = CompletionClient(self.pool, self.telemetry)
        self.worker = Worker(
            artifacts=self.artifacts,
            billing=self.billing,
            completion=self.completion,
            telemetry=self.telemetry,
        )

    def submit_and_run(self, job_id: str) -> None:
        self.scheduler.submit(job_id)
        self.worker.execute(job_id)

    def advance(self, seconds: float) -> None:
        self.clock.advance(seconds)
        self.scheduler.maintenance()

    def rotate_token(self) -> None:
        self.tokens.rotate()

    def restart_worker(self) -> None:
        self.pool = ChannelPool(
            clock=self.clock,
            token_manager=self.tokens,
            gateway=self.gateway,
            telemetry=self.telemetry,
            max_size=self.config.pool_size,
        )
        self.completion = CompletionClient(self.pool, self.telemetry)
        self.worker = Worker(
            artifacts=self.artifacts,
            billing=self.billing,
            completion=self.completion,
            telemetry=self.telemetry,
        )
        self.telemetry.emit("worker", "worker_restarted")
