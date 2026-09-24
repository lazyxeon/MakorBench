# Licensed under the Apache License, Version 2.0.
"""Reference MakorBench v0.1 score aggregation.

This module intentionally implements only arithmetic and score ceilings.
Semantic component grading is defined by SCORING.md and GRADING-PROTOCOL.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Components:
    diagnosis: float
    investigation: float
    intervention: float
    verification_judgment: float

    def validate(self) -> None:
        bounds = {
            "diagnosis": (self.diagnosis, 35.0),
            "investigation": (self.investigation, 25.0),
            "intervention": (self.intervention, 30.0),
            "verification_judgment": (self.verification_judgment, 10.0),
        }
        for name, (value, maximum) in bounds.items():
            if not 0.0 <= value <= maximum:
                raise ValueError(f"{name} must be within [0, {maximum}], got {value}")

    @property
    def raw_total(self) -> float:
        self.validate()
        return (
            self.diagnosis
            + self.investigation
            + self.intervention
            + self.verification_judgment
        )


@dataclass(frozen=True)
class CeilingInputs:
    causal_mechanism_score_d1: float
    reproduction_score_g1: float
    evidence_grounding_score_d4: float
    counterfactual_score_i2: float
    critical_regression: bool = False
    benchmark_tampering: bool = False

    def validate(self) -> None:
        checks = {
            "causal_mechanism_score_d1": (self.causal_mechanism_score_d1, 15.0),
            "reproduction_score_g1": (self.reproduction_score_g1, 10.0),
            "evidence_grounding_score_d4": (self.evidence_grounding_score_d4, 5.0),
            "counterfactual_score_i2": (self.counterfactual_score_i2, 10.0),
        }
        for name, (value, maximum) in checks.items():
            if not 0.0 <= value <= maximum:
                raise ValueError(f"{name} must be within [0, {maximum}], got {value}")


@dataclass(frozen=True)
class AppliedCeiling:
    rule: str
    cap: float


@dataclass(frozen=True)
class ScoreResult:
    raw_score: float
    makor_score: float
    ceilings: tuple[AppliedCeiling, ...]
    disqualified: bool = False


def _ceilings(inputs: CeilingInputs) -> Iterable[AppliedCeiling]:
    if inputs.causal_mechanism_score_d1 < 8.0:
        yield AppliedCeiling("wrong-cause", 65.0)
    if inputs.reproduction_score_g1 == 0.0 and inputs.evidence_grounding_score_d4 <= 1.0:
        yield AppliedCeiling("no-causal-evidence", 60.0)
    if inputs.counterfactual_score_i2 == 0.0:
        yield AppliedCeiling("counterfactual-failure", 70.0)
    if inputs.critical_regression:
        yield AppliedCeiling("critical-regression", 50.0)


def compute_makor_score(components: Components, inputs: CeilingInputs) -> ScoreResult:
    """Compute v0.1 draft MakorScore from already-graded components."""
    components.validate()
    inputs.validate()

    raw = components.raw_total

    if inputs.benchmark_tampering:
        return ScoreResult(
            raw_score=raw,
            makor_score=0.0,
            ceilings=(AppliedCeiling("benchmark-tampering", 0.0),),
            disqualified=True,
        )

    ceilings = tuple(_ceilings(inputs))
    cap = min((item.cap for item in ceilings), default=100.0)
    return ScoreResult(
        raw_score=raw,
        makor_score=min(raw, cap),
        ceilings=ceilings,
        disqualified=False,
    )
