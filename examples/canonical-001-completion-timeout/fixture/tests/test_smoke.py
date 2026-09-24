from __future__ import annotations

import sys
import unittest
from pathlib import Path

FIXTURE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIXTURE))

from makor_fixture import FixtureSystem


class PublicSmokeTests(unittest.TestCase):
    def test_healthy_job_completes(self):
        system = FixtureSystem()
        system.submit_and_run("smoke")
        self.assertTrue(system.artifacts.has("smoke"))
        self.assertEqual(system.billing.count("smoke"), 1)
        self.assertEqual(system.scheduler.status("smoke"), "COMPLETED")


if __name__ == "__main__":
    unittest.main()
