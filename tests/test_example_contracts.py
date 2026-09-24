# Licensed under the Apache License, Version 2.0.

import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "examples" / "canonical-001-completion-timeout"
SCHEMAS = ROOT / "schemas"


class ExampleContractTests(unittest.TestCase):
    def _validate(self, instance_path: Path, schema_path: Path):
        instance = json.loads(instance_path.read_text())
        schema = json.loads(schema_path.read_text())
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(instance)

    def test_task_manifest(self):
        self._validate(
            CASE / "task.json",
            SCHEMAS / "task-manifest.schema.json",
        )

    def test_private_oracle(self):
        self._validate(
            CASE / "private" / "oracle.json",
            SCHEMAS / "oracle.schema.json",
        )

    def test_claim_unit_weights_sum_to_one(self):
        oracle = json.loads((CASE / "private" / "oracle.json").read_text())
        weights = [item["weight"] for item in oracle["causal_claim_units"]]
        self.assertAlmostEqual(sum(weights), 1.0, places=9)

    def test_case_is_marked_public_paper_case(self):
        task = json.loads((CASE / "task.json").read_text())
        oracle = json.loads((CASE / "private" / "oracle.json").read_text())
        self.assertEqual(task["benchmark_version"], "0.1-paper")
        self.assertTrue(oracle["provenance"]["public_worked_case"])
        self.assertEqual(oracle["human_validation"]["status"], "pending")


if __name__ == "__main__":
    unittest.main()
