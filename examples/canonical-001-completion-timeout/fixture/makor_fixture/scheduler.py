from __future__ import annotations

from dataclasses import dataclass

from .clock import FakeClock
from .stores import ArtifactStore
from .telemetry import Telemetry


@dataclass
class JobState:
    status: str
    submitted_at: float
    deadline: float
    completed_at: float | None = None
    source: str | None = None


class Scheduler:
    def __init__(
        self,
        clock: FakeClock,
        telemetry: Telemetry,
        artifacts: ArtifactStore,
        *,
        lease_timeout: float,
        reconciliation_interval: float,
    ) -> None:
        self.clock = clock
        self.telemetry = telemetry
        self.artifacts = artifacts
        self.lease_timeout = float(lease_timeout)
        self.reconciliation_interval = float(reconciliation_interval)
        self._last_reconciliation = clock.now
        self.jobs: dict[str, JobState] = {}

    def submit(self, job_id: str) -> None:
        self.jobs[job_id] = JobState(
            status="RUNNING",
            submitted_at=self.clock.now,
            deadline=self.clock.now + self.lease_timeout,
        )
        self.telemetry.emit(
            "scheduler",
            "job_submitted",
            job_id=job_id,
            deadline=round(self.jobs[job_id].deadline, 6),
        )

    def complete(self, job_id: str, *, source: str = "completion") -> None:
        state = self.jobs[job_id]
        if state.status == "COMPLETED":
            self.telemetry.emit(
                "scheduler",
                "completion_duplicate_ignored",
                job_id=job_id,
                source=source,
            )
            return
        state.status = "COMPLETED"
        state.completed_at = self.clock.now
        state.source = source
        self.telemetry.emit(
            "scheduler",
            "job_completed",
            job_id=job_id,
            source=source,
        )

    def maintenance(self) -> None:
        if self.clock.now - self._last_reconciliation >= self.reconciliation_interval:
            self._reconcile()
            self._last_reconciliation = self.clock.now

        for job_id, state in self.jobs.items():
            if state.status == "RUNNING" and self.clock.now >= state.deadline:
                state.status = "TIMED_OUT"
                self.telemetry.emit(
                    "scheduler",
                    "lease_expired",
                    job_id=job_id,
                    age_ms=round((self.clock.now - state.submitted_at) * 1000),
                )

    def _reconcile(self) -> None:
        for job_id, state in self.jobs.items():
            if state.status == "RUNNING" and self.artifacts.has(job_id):
                self.complete(job_id, source="reconciliation")
                self.telemetry.emit(
                    "scheduler",
                    "reconciliation_recovered",
                    job_id=job_id,
                )

    def status(self, job_id: str) -> str:
        return self.jobs[job_id].status
