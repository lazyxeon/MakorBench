from __future__ import annotations

import sys
import unittest
from pathlib import Path

FIXTURE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIXTURE))

from makor_fixture import FixtureConfig, FixtureSystem
from makor_fixture.completion import UNAUTHENTICATED
from makor_fixture.reference_solution import CurrentCredentialChannel


class FixtureBehaviorTests(unittest.TestCase):
    def make_incident(self, *, fixed: bool = False, timeout: float = 45, reconciliation: float = 60):
        channel_type = CurrentCredentialChannel if fixed else None
        kwargs = {}
        if channel_type is not None:
            kwargs["channel_type"] = channel_type

        system = FixtureSystem(
            FixtureConfig(
                lease_timeout=timeout,
                reconciliation_interval=reconciliation,
                pool_size=1,
            ),
            **kwargs,
        )
        system.submit_and_run("warmup")
        self.assertEqual(system.scheduler.status("warmup"), "COMPLETED")

        system.advance(6 * 60 * 60)
        system.rotate_token()
        system.submit_and_run("target")
        return system

    def test_oracle_reproduction_times_out_completed_work(self):
        system = self.make_incident()

        self.assertTrue(system.artifacts.has("target"))
        self.assertEqual(system.billing.count("target"), 1)
        self.assertEqual(system.scheduler.status("target"), "RUNNING")

        failures = system.telemetry.matching(service="worker", event="completion_delivery_failed")
        self.assertEqual(len(failures), 1)
        self.assertEqual(failures[0]["status"], UNAUTHENTICATED)

        system.advance(50)
        self.assertEqual(system.scheduler.status("target"), "TIMED_OUT")

    def test_next_channel_uses_current_credential(self):
        system = self.make_incident()

        system.submit_and_run("next")
        self.assertEqual(system.scheduler.status("next"), "COMPLETED")
        self.assertEqual(system.billing.count("next"), 1)

    def test_worker_restart_temporarily_suppresses_symptom(self):
        system = FixtureSystem(FixtureConfig(pool_size=1))
        system.submit_and_run("warmup")
        system.advance(6 * 60 * 60)
        system.rotate_token()
        system.restart_worker()

        system.submit_and_run("after-restart")
        self.assertEqual(system.scheduler.status("after-restart"), "COMPLETED")

    def test_longer_timeout_can_mask_failure_via_reconciliation(self):
        system = self.make_incident(timeout=90, reconciliation=60)
        self.assertEqual(system.scheduler.status("target"), "RUNNING")

        system.advance(61)
        self.assertEqual(system.scheduler.status("target"), "COMPLETED")
        self.assertEqual(system.scheduler.jobs["target"].source, "reconciliation")

        failures = system.telemetry.matching(service="worker", event="completion_delivery_failed")
        self.assertEqual(len(failures), 1)

    def test_reference_repair_survives_rotation(self):
        system = self.make_incident(fixed=True)
        self.assertEqual(system.scheduler.status("target"), "COMPLETED")

        failures = system.telemetry.matching(service="worker", event="completion_delivery_failed")
        self.assertEqual(failures, [])

    def test_reference_repair_preserves_authentication(self):
        system = FixtureSystem(channel_type=CurrentCredentialChannel)
        system.scheduler.submit("invalid-auth")

        result = system.gateway.publish(
            "invalid-auth",
            "not-a-valid-token",
            channel_id="manual",
            channel_age=0,
        )
        self.assertFalse(result.delivered)
        self.assertEqual(result.status, UNAUTHENTICATED)
        self.assertEqual(system.scheduler.status("invalid-auth"), "RUNNING")

    def test_billing_is_idempotent(self):
        system = FixtureSystem(channel_type=CurrentCredentialChannel)
        system.scheduler.submit("dup")
        system.worker.execute("dup")
        system.worker.execute("dup")
        self.assertEqual(system.billing.count("dup"), 1)
        self.assertEqual(system.scheduler.status("dup"), "COMPLETED")


if __name__ == "__main__":
    unittest.main()
