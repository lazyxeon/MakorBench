# Issue #3 Research Notes — Scoring and Trajectory Evaluation

Phase 1 scoring is informed by the following adjacent evaluation work.

## SWE-bench

SWE-bench provides the key executable-outcome baseline: patches are applied in a container and tests determine whether the stated issue is resolved. MakorBench retains executable repair grading but does not reduce causal diagnosis to patch success.

- https://www.swebench.com/SWE-bench/guides/evaluation/

## APEX-SWE

APEX-SWE Observability evaluates production-style debugging with telemetry and unstructured context. Its analysis reports that stronger performance is associated with epistemic reasoning: distinguishing assumptions from verified facts and resolving uncertainty before acting.

- https://arxiv.org/abs/2601.08806

This supports MakorBench's explicit evidence-grounding and epistemic-update dimensions.

## Efficient SWE Agent Benchmarking via Trajectory-Aware Evaluation

PTA-IRT uses historical execution trajectories as privileged process information beyond pass/fail outcomes. It is not a direct MakorBench scoring recipe, but it supports the premise that trajectories contain useful discriminative information beyond final resolution.

- https://arxiv.org/abs/2609.01603

## TRAJECT-Bench

TRAJECT-Bench reports trajectory-level diagnostics for tool selection, argument correctness, and ordering in addition to final accuracy.

- https://arxiv.org/abs/2510.04550

MakorBench similarly separates final outcome from observable process quality, but focuses on causal software diagnosis rather than generic tool use.

## Design implication

MakorBench v0.1 uses:
- deterministic executable grading for repair outcomes;
- oracle-backed structured semantic grading for causal diagnosis;
- observable trajectory events for investigation quality;
- no requirement for hidden chain-of-thought;
- explicit score components rather than a single opaque judge verdict.
