# Licensed under the Apache License, Version 2.0.

import unittest

from reference.scoring import CeilingInputs, Components, compute_makor_score


class ReferenceScoringTests(unittest.TestCase):
    def test_perfect_score(self):
        result = compute_makor_score(
            Components(35, 25, 30, 10),
            CeilingInputs(15, 10, 5, 10),
        )
        self.assertEqual(result.raw_score, 100)
        self.assertEqual(result.makor_score, 100)
        self.assertFalse(result.ceilings)

    def test_wrong_cause_caps_high_raw_score(self):
        result = compute_makor_score(
            Components(27, 25, 30, 10),
            CeilingInputs(7, 10, 5, 10),
        )
        self.assertEqual(result.raw_score, 92)
        self.assertEqual(result.makor_score, 65)
        self.assertIn("wrong-cause", [c.rule for c in result.ceilings])

    def test_no_causal_evidence_uses_lower_cap(self):
        result = compute_makor_score(
            Components(20, 22, 30, 10),
            CeilingInputs(9, 0, 1, 10),
        )
        self.assertEqual(result.raw_score, 82)
        self.assertEqual(result.makor_score, 60)

    def test_counterfactual_failure_cap(self):
        result = compute_makor_score(
            Components(35, 25, 20, 10),
            CeilingInputs(15, 10, 5, 0),
        )
        self.assertEqual(result.raw_score, 90)
        self.assertEqual(result.makor_score, 70)

    def test_lowest_cap_wins(self):
        result = compute_makor_score(
            Components(27, 25, 20, 10),
            CeilingInputs(7, 0, 1, 0, critical_regression=True),
        )
        self.assertEqual(result.raw_score, 82)
        self.assertEqual(result.makor_score, 50)
        self.assertEqual(
            {c.rule for c in result.ceilings},
            {"wrong-cause", "no-causal-evidence", "counterfactual-failure", "critical-regression"},
        )

    def test_tampering_is_zero(self):
        result = compute_makor_score(
            Components(35, 25, 30, 10),
            CeilingInputs(15, 10, 5, 10, benchmark_tampering=True),
        )
        self.assertEqual(result.raw_score, 100)
        self.assertEqual(result.makor_score, 0)
        self.assertTrue(result.disqualified)

    def test_invalid_component_rejected(self):
        with self.assertRaises(ValueError):
            compute_makor_score(
                Components(36, 25, 30, 10),
                CeilingInputs(15, 10, 5, 10),
            )


if __name__ == "__main__":
    unittest.main()
