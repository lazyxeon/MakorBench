from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from makor_fixture import FixtureConfig, FixtureSystem


def build_incident() -> FixtureSystem:
    system = FixtureSystem(
        FixtureConfig(
            lease_timeout=45,
            reconciliation_interval=60,
            pool_size=1,
        )
    )

    system.submit_and_run("warmup-001")
    system.advance(6 * 60 * 60)
    system.rotate_token()

    system.submit_and_run("incident-8f2a")
    system.advance(50)

    system.submit_and_run("recovery-002")
    return system


def write_bundle(system: FixtureSystem) -> Path:
    output = HERE / "generated"
    output.mkdir(exist_ok=True)

    (output / "logs.jsonl").write_text(system.telemetry.jsonl())

    metrics = {
        "lease_expired_count": len(system.telemetry.matching(service="scheduler", event="lease_expired")),
        "completion_rejected_count": len(system.telemetry.matching(service="completion_gateway", event="completion_rejected")),
        "completion_accepted_count": len(system.telemetry.matching(service="completion_gateway", event="completion_accepted")),
        "token_rotated_count": len(system.telemetry.matching(service="identity", event="token_rotated")),
        "reconciliation_recovered_count": len(system.telemetry.matching(service="scheduler", event="reconciliation_recovered")),
        "job_status": {job_id: state.status for job_id, state in system.scheduler.jobs.items()},
    }
    (output / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")

    traces = {}
    for event in system.telemetry.events:
        job_id = event.get("job_id")
        if job_id is not None:
            traces.setdefault(job_id, []).append(event)
    (output / "traces.json").write_text(json.dumps(traces, indent=2, sort_keys=True) + "\n")

    return output


if __name__ == "__main__":
    system = build_incident()
    path = write_bundle(system)
    print(f"wrote evidence to {path}")
