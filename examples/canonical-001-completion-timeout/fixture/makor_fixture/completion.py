from __future__ import annotations

from dataclasses import dataclass

from .clock import FakeClock
from .scheduler import Scheduler
from .telemetry import Telemetry
from .token_manager import TokenManager


OK = 0
UNAUTHENTICATED = 16


@dataclass(frozen=True)
class PublishResult:
    delivered: bool
    status: int


class CompletionGateway:
    def __init__(
        self,
        token_manager: TokenManager,
        scheduler: Scheduler,
        telemetry: Telemetry,
    ) -> None:
        self.token_manager = token_manager
        self.scheduler = scheduler
        self.telemetry = telemetry

    def publish(self, job_id: str, token: str, *, channel_id: str, channel_age: float) -> PublishResult:
        if token != self.token_manager.current_token:
            self.telemetry.emit(
                "completion_gateway",
                "completion_rejected",
                job_id=job_id,
                status=UNAUTHENTICATED,
                channel_id=channel_id,
                channel_age=round(channel_age, 6),
            )
            return PublishResult(False, UNAUTHENTICATED)

        self.scheduler.complete(job_id, source="completion")
        self.telemetry.emit(
            "completion_gateway",
            "completion_accepted",
            job_id=job_id,
            status=OK,
            channel_id=channel_id,
        )
        return PublishResult(True, OK)


class CompletionChannel:
    def __init__(
        self,
        *,
        channel_id: str,
        clock: FakeClock,
        token_manager: TokenManager,
        gateway: CompletionGateway,
        telemetry: Telemetry,
    ) -> None:
        self.channel_id = channel_id
        self.clock = clock
        self.gateway = gateway
        self.telemetry = telemetry
        self.created_at = clock.now
        self._authorization = token_manager.current_token
        self.telemetry.emit(
            "worker",
            "completion_channel_created",
            channel_id=self.channel_id,
        )

    def publish(self, job_id: str) -> PublishResult:
        return self.gateway.publish(
            job_id,
            self._authorization,
            channel_id=self.channel_id,
            channel_age=self.clock.now - self.created_at,
        )


class ChannelPool:
    def __init__(
        self,
        *,
        clock: FakeClock,
        token_manager: TokenManager,
        gateway: CompletionGateway,
        telemetry: Telemetry,
        max_size: int = 1,
        channel_type: type[CompletionChannel] = CompletionChannel,
    ) -> None:
        if max_size < 1:
            raise ValueError("max_size must be >= 1")
        self.clock = clock
        self.token_manager = token_manager
        self.gateway = gateway
        self.telemetry = telemetry
        self.max_size = max_size
        self.channel_type = channel_type
        self._channels: list[CompletionChannel] = []
        self._cursor = 0
        self._next_id = 1

    def _new_channel(self) -> CompletionChannel:
        channel = self.channel_type(
            channel_id=f"ch{self._next_id:02d}",
            clock=self.clock,
            token_manager=self.token_manager,
            gateway=self.gateway,
            telemetry=self.telemetry,
        )
        self._next_id += 1
        self._channels.append(channel)
        return channel

    def get(self) -> CompletionChannel:
        if len(self._channels) < self.max_size:
            return self._new_channel()
        channel = self._channels[self._cursor % len(self._channels)]
        self._cursor = (self._cursor + 1) % max(1, len(self._channels))
        return channel

    def invalidate(self, channel: CompletionChannel) -> None:
        self._channels = [item for item in self._channels if item is not channel]
        self._cursor = 0
        self.telemetry.emit(
            "worker",
            "completion_channel_invalidated",
            channel_id=channel.channel_id,
        )


class CompletionClient:
    def __init__(self, pool: ChannelPool, telemetry: Telemetry) -> None:
        self.pool = pool
        self.telemetry = telemetry

    def publish(self, job_id: str) -> PublishResult:
        channel = self.pool.get()
        result = channel.publish(job_id)
        if result.status == UNAUTHENTICATED:
            self.pool.invalidate(channel)
        if not result.delivered:
            self.telemetry.emit(
                "worker",
                "completion_delivery_failed",
                job_id=job_id,
                status=result.status,
                retryable=False,
                channel_id=channel.channel_id,
            )
        return result
