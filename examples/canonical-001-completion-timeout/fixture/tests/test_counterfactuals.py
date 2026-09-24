from __future__ import annotations

import sys
import unittest
from pathlib import Path

FIXTURE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIXTURE))

from makor_fixture import FixtureConfig, FixtureSystem
from makor_fixture.reference_solution import CurrentCredentialChannel


def prime_channels(system: FixtureSystem, count: int) -> None:
    for index in range(count):
        system.submit_and_run(f"warmup-{index}")


class CounterfactualTests(unittest.TestCase):
    def test_cf1_rotation_time_is_not_special(self):
        for rotation_time in (17, 91, 733):
            buggy = FixtureSystem(FixtureConfig(reconciliation_interval=10_000, pool_size=1))
            prime_channels(buggy, 1)
            buggy.advance(rotation_time)
            buggy.rotate_token()
            buggy.submit_and_run(f"buggy-{rotation_time}")
            buggy.advance(46)
            self.assertEqual(buggy.scheduler.status(f"buggy-{rotation_time}"), "TIMED_OUT")

            fixed = FixtureSystem(
                FixtureConfig(reconciliation_interval=10_000, pool_size=1),
                channel_type=CurrentCredentialChannel,
            )
            prime_channels(fixed, 1)
            fixed.advance(rotation_time)
            fixed.rotate_token()
            fixed.submit_and_run(f"fixed-{rotation_time}")
            fixed.advance(46)
            self.assertEqual(fixed.scheduler.status(f"fixed-{rotation_time}"), "COMPLETED")

    def test_cf2_timeout_only_mitigation_fails_when_reconciliation_is_late(self):
        buggy = FixtureSystem(
            FixtureConfig(
                lease_timeout=90,
                reconciliation_interval=120,
                pool_size=1,
            )
        )
        prime_channels(buggy, 1)
        buggy.rotate_token()
        buggy.submit_and_run("target")
        buggy.advance(91)
        self.assertEqual(buggy.scheduler.status("target"), "TIMED_OUT")

        fixed = FixtureSystem(
            FixtureConfig(
                lease_timeout=90,
                reconciliation_interval=120,
                pool_size=1,
            ),
            channel_type=CurrentCredentialChannel,
        )
        prime_channels(fixed, 1)
        fixed.rotate_token()
        fixed.submit_and_run("target")
        fixed.advance(91)
        self.assertEqual(fixed.scheduler.status("target"), "COMPLETED")

    def test_cf3_pool_cardinality_does_not_change_mechanism(self):
        buggy = FixtureSystem(
            FixtureConfig(
                reconciliation_interval=10_000,
                pool_size=3,
            )
        )
        prime_channels(buggy, 3)
        buggy.rotate_token()

        for index in range(3):
            job_id = f"stale-{index}"
            buggy.submit_and_run(job_id)
            buggy.advance(46)
            self.assertEqual(buggy.scheduler.status(job_id), "TIMED_OUT")

        fixed = FixtureSystem(
            FixtureConfig(
                reconciliation_interval=10_000,
                pool_size=3,
            ),
            channel_type=CurrentCredentialChannel,
        )
        prime_channels(fixed, 3)
        fixed.rotate_token()

        for index in range(3):
            job_id = f"fresh-{index}"
            fixed.submit_and_run(job_id)
            fixed.advance(46)
            self.assertEqual(fixed.scheduler.status(job_id), "COMPLETED")


if __name__ == "__main__":
    unittest.main()
