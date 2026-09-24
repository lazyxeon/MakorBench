from __future__ import annotations

from dataclasses import dataclass, field

from .telemetry import Telemetry


@dataclass
class ArtifactStore:
    telemetry: Telemetry
    objects: dict[str, str] = field(default_factory=dict)

    def put(self, job_id: str, payload: str) -> None:
        self.objects[job_id] = payload
        self.telemetry.emit("artifact", "commit_ok", job_id=job_id)

    def has(self, job_id: str) -> bool:
        return job_id in self.objects


@dataclass
class BillingLedger:
    telemetry: Telemetry
    completed_jobs: set[str] = field(default_factory=set)

    def record_completion(self, job_id: str) -> None:
        before = len(self.completed_jobs)
        self.completed_jobs.add(job_id)
        self.telemetry.emit(
            "billing",
            "ledger_commit_ok",
            job_id=job_id,
            duplicate=(len(self.completed_jobs) == before),
        )

    def count(self, job_id: str) -> int:
        return 1 if job_id in self.completed_jobs else 0
