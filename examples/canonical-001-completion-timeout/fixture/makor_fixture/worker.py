from __future__ import annotations

from .completion import CompletionClient, PublishResult
from .stores import ArtifactStore, BillingLedger
from .telemetry import Telemetry


class Worker:
    def __init__(
        self,
        *,
        artifacts: ArtifactStore,
        billing: BillingLedger,
        completion: CompletionClient,
        telemetry: Telemetry,
    ) -> None:
        self.artifacts = artifacts
        self.billing = billing
        self.completion = completion
        self.telemetry = telemetry

    def execute(self, job_id: str, payload: str = "rendered") -> PublishResult:
        self.telemetry.emit("worker", "render_complete", job_id=job_id)
        self.artifacts.put(job_id, payload)
        self.billing.record_completion(job_id)
        return self.completion.publish(job_id)
