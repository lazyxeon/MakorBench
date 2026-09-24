# Phase 1 Open Questions

This document records unresolved specification questions. It is intentionally separate from the normative contract so design uncertainty remains visible.

## OQ-01 — Structured hypothesis declarations

Should agents be required to emit explicit hypothesis updates during the run?

**Benefit:** makes belief revision measurable.

**Risk:** changes agent behavior and may reward performative narration rather than better diagnosis.

Current leaning: make structured declarations optional in the base protocol and rely primarily on observable actions plus concise checkpoints emitted by compatible harnesses.

## OQ-02 — Canonical harness

Candidates include:

- SWE-ReX-based reference environment;
- Harbor / Terminal-Bench task packaging;
- a thin wrapper compatible with multiple coding agents.

The benchmark should reuse infrastructure and avoid becoming an agent framework.

## OQ-03 — Internet policy

Current spec sets no unrestricted internet for the Canonical Track and permits an Open-World Track.

Need to define whether package registries and documentation mirrors are:
- blocked,
- locally mirrored,
- or task-specific.

## OQ-04 — Required counterfactual count

v0.1 requires >=1 for production-grade canonical tasks and recommends >=2.

Need empirical pilot data before setting the v1.0 minimum.

## OQ-05 — Adjacent finding credit

A model may discover real defects outside the reported symptom.

Need to reward useful engineering vigilance without encouraging uncontrolled scope expansion.

Possible approach:
- no primary root-cause credit;
- separate audited adjacent-finding metric;
- intervention penalty if unrelated findings are modified without justification.

## OQ-06 — Information efficiency

Raw tool-call count is not directly comparable across scaffolds.

Potential measures:
- environment actions until causal localization;
- number of expensive experiments;
- normalized wall time;
- fraction of actions that materially discriminate hypotheses;
- oracle-annotated information gain.

This is likely a research metric rather than a hard gate in v0.1.

## OQ-07 — Diagnosis without patch

Some cases may justify escalation or abstention rather than an automated intervention.

Need a principled mechanism for cases where:
- the evidence supports a cause;
- the repair carries unacceptable uncertainty;
- or human approval is realistically required.

## OQ-08 — Human validator qualification

Potential minimum:
- experienced contributor/maintainer in the relevant stack; or
- professional software engineer with demonstrated debugging experience; or
- benchmark maintainer approved through calibration tasks.

Formalize only after pilot cases reveal inter-rater variance.

## OQ-09 — Difficulty model

A vector is preferable to a single difficulty label.

Need to determine whether dimensions can be objectively measured or only author/reviewer rated.

## OQ-10 — Counterfactual generation

Need to decide how much can be generated mechanically versus requiring human-designed variants.

Mechanically generated mutations risk producing invalid or unrealistic conditions. Human variants are expensive but more defensible.
