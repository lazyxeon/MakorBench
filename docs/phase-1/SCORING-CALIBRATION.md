# MakorBench v0.1 Scoring Calibration — Initial Paper Exercise

**Status:** pre-pilot calibration  
**Purpose:** test whether the draft rubric orders deliberately different engineering behaviors in the intended direction.

These are hand-constructed trajectories, not benchmark claims.

## C1 — Evidence-led root-cause diagnosis

Behavior:
- begins from an ambiguous timeout symptom;
- forms credential lifecycle, networking, and scheduler hypotheses;
- uses a targeted lifetime experiment to separate the credential hypothesis;
- reproduces stale pooled-connection state;
- patches invalidation;
- re-tests the mechanism;
- passes all counterfactuals/regressions.

Score target: **95–100**.

Reason: this is the reference behavior MakorBench is intended to reward.

## C2 — Concise expert trajectory

Behavior:
- does not narrate hypotheses at length;
- inspects three high-information artifacts;
- runs one decisive experiment;
- correctly diagnoses the causal mechanism;
- applies minimal repair;
- verifies and passes hidden variants.

Score target: **93–100**.

Constraint tested: concise agents must not be penalized for lack of verbose reasoning.

Expected difference from C1: at most a few points depending on evidence coverage; no penalty merely for fewer messages/tool calls.

## C3 — Verbose hypothesis theater

Behavior:
- emits many hypotheses and lengthy explanations;
- performs broad grep/search;
- runs few discriminating experiments;
- eventually finds and fixes the cause;
- passes most functional tests.

Score target: **55–75**, depending on final diagnosis and counterfactual robustness.

Constraint tested: narration volume does not substitute for investigation quality.

Expected ordering: C1/C2 > C3.

## C4 — Lucky functional patch, wrong cause

Behavior:
- changes retry/pool code broadly;
- passes base and some hidden tests;
- final explanation blames DNS;
- little pre-intervention causal evidence.

Score target: **<=65** due to wrong-cause ceiling.

Constraint tested: successful patching does not masquerade as root-cause competence.

Expected ordering: C1/C2 > correct-diagnosis/failed-repair cases > C4 where applicable.

## C5 — Symptom suppression

Behavior:
- raises timeout threshold;
- visible symptom disappears;
- underlying stale state persists;
- counterfactual variants fail.

Score target: **well below 70**; counterfactual ceiling applies.

Constraint tested: hidden variants distinguish repair from symptom masking.

## C6 — Correct diagnosis, unsafe repair

Behavior:
- correctly proves the causal mechanism;
- implements a fix that weakens authentication or introduces a critical regression.

Score target: **<=50** when the task marks the protected invariant critical.

Constraint tested: diagnostic competence does not erase unsafe intervention.

## C7 — Patch-first, prove-after

Behavior:
- reaches the correct patch very early by strong intuition/pattern recognition;
- then performs rigorous causal reproduction and verification;
- passes counterfactuals.

Score target: **high but below evidence-led equivalent**, typically ~85–92.

Constraint tested: MakorBench does not punish intuition, but distinguishes evidence-led intervention from post-hoc confirmation.

## Initial ordering check

The draft rubric is intended to produce:

```text
C1 ≈ C2 > C7 > C3 > C4/C5 > C6 when critical safety is violated
```

Exact C3–C5 ordering depends on actual diagnosis and executable outcomes; no universal ordering is required.

## Ceiling arithmetic checks

The reference scorer tests:

- perfect 100-point run;
- wrong-cause cap = 65;
- no-causal-evidence cap = 60;
- counterfactual-failure cap = 70;
- critical-regression cap = 50;
- lowest applicable cap wins;
- benchmark tampering = 0;
- invalid component bounds are rejected.

## What this calibration does not establish

This exercise does **not** validate the human/semantic rubric.

Remaining empirical work:
- blind human scoring of the same trajectories;
- automated grader agreement against human labels;
- sensitivity to model-family writing style;
- sensitivity to concise vs verbose agent scaffolds;
- score distributions on real cases;
- whether the 35/25/30/10 weighting needs adjustment.

Those remain required before v1.0.
