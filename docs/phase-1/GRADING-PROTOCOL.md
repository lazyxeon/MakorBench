# MakorBench Grading Protocol

**Version:** 0.1-draft  
**Status:** Phase 1 normative companion to `SCORING.md`

## 1. Purpose

This document defines how a canonical MakorBench run is transformed into auditable score components.

The protocol separates:

1. deterministic execution outcomes;
2. oracle-backed causal semantics;
3. observable trajectory analysis;
4. human adjudication for ambiguous grader cases.

No single model-as-judge output is sufficient for the complete benchmark score.

## 2. Grading order

Canonical grading SHOULD run in this order:

1. validate run artifacts and schemas;
2. detect infrastructure failure;
3. detect benchmark tampering;
4. execute original hidden functional tests;
5. execute hidden regression tests;
6. execute hidden counterfactual variants;
7. derive trajectory facts;
8. grade diagnosis against oracle causal claim units;
9. grade investigation rubric;
10. grade intervention proportionality;
11. grade verification/judgment;
12. apply score ceilings;
13. produce `score-report.json`.

The ordering prevents semantic graders from influencing deterministic outcomes.

## 3. Artifact validation

A run is gradable only if required artifacts are syntactically valid:

- final repository state or explicit no-change marker;
- `diagnosis.json`;
- `verification.json`;
- trajectory log;
- run metadata.

Malformed semantic artifacts MAY receive zero on affected semantic components while preserving deterministic functional outcomes, unless the release declares malformed required output a full-run failure.

The release policy MUST be documented.

## 4. Deterministic layer

The deterministic layer computes:

- Functional Resolution;
- Counterfactual Resolution Rate;
- Regression Preservation Rate;
- benchmark-tampering status;
- persistent diff;
- resource usage when directly measurable.

These values SHOULD be generated without an LLM judge.

## 5. Causal semantic layer

### 5.1 Oracle preparation

Before model evaluation, each stable task SHOULD define causal claim units.

Each claim unit includes:

- ID;
- weight;
- oracle claim;
- optional accepted equivalent formulations.

Weights are authored before the evaluated model output is seen.

### 5.2 Matching

The diagnosis grader assesses whether the submitted diagnosis:

- entails the oracle claim;
- partially captures it;
- contradicts it;
- omits it.

A recommended ordinal match scale is:

- **1.0** — materially equivalent;
- **0.5** — partially correct but missing a material qualifier;
- **0.0** — absent or incorrect.

A release MAY use finer resolution after calibration.

### 5.3 Judge independence

For stable hidden evaluation:

- the evaluated model MUST NOT grade itself;
- one uncalibrated LLM judge MUST NOT be the sole authority for high-impact diagnosis scores;
- at least two independent grading passes SHOULD be used for causal semantic scoring;
- disagreement beyond a configured threshold SHOULD trigger human adjudication or a third calibrated judge.

Judge prompts, versions, temperature/settings, and rubric version MUST be recorded.

### 5.4 Blindness

Semantic graders SHOULD receive only information required to compare the submitted claim against the oracle claim.

They SHOULD NOT receive the model's identity.

## 6. Evidence-grounding layer

Material diagnosis claims SHOULD reference trajectory event IDs.

The grounding grader verifies:

1. cited event exists;
2. event was agent-visible;
3. evidence is relevant to the claim;
4. evidence does not materially contradict the claim;
5. evidence timing relative to persistent intervention.

A semantically correct diagnosis with fabricated evidence references receives reduced D4/G3 credit.

## 7. Persistent intervention reconstruction

The grader SHOULD reconstruct the first persistent intervention when intermediate filesystem states are available.

Recommended procedure:

1. compute final diff;
2. inspect file-write/edit events;
3. identify the earliest edit whose content survives materially into the final diff;
4. ignore fully reverted diagnostic instrumentation;
5. record the corresponding trajectory sequence number.

When reconstruction is unreliable, mark the boundary confidence and avoid over-precise G3 scoring.

A benchmark MUST NOT pretend to know edit intent when the observable record cannot support it.

## 8. Investigation rubric

G1–G4 are graded using task-specific oracle annotations plus canonical anchors.

### 8.1 Reproduction

Prefer deterministic evidence:

- reproduction test outcome;
- trace condition;
- instrumentation assertion;
- stress threshold;
- controlled simulation.

### 8.2 Discriminating experiments

Task authors SHOULD annotate examples of evidence that would distinguish major hypothesis classes.

The grader rewards information value, not stylistic resemblance to the oracle walkthrough.

A novel experiment can receive full credit when it provides equivalent or stronger discrimination.

### 8.3 Epistemic update

G4 may be supported by:

- explicit hypothesis checkpoints;
- changed investigative behavior after contrary evidence;
- abandoning a failed intervention;
- targeted follow-up experiment after an unexpected result.

Lack of verbose narration MUST NOT reduce G4 by itself.

## 9. Proportionality grading

I4 is semantic and may require repository context.

The grader asks:

- Are persistent changes causally justified?
- Is there a narrower repair with equivalent correctness that a competent engineer would clearly prefer?
- Did the agent modify unrelated areas?
- Did it weaken safety, validation, or security?
- Did it turn a local failure into a broad architectural rewrite without necessity?

Diff size alone is not the metric.

Task authors MAY define known unacceptable workaround classes.

## 10. Verification grading

V1 uses both:

- `verification.json`;
- observed post-intervention trajectory events.

Claims of testing that do not appear in the trajectory receive no execution credit.

The grader distinguishes:

- causal re-test;
- regression test;
- generic test-suite run;
- unsupported claim that the change is correct.

## 11. Score ceiling order

Apply ceilings after raw component scoring.

If several ceilings apply, use the **lowest cap**.

Benchmark tampering overrides all ceilings and sets score to zero.

The score report MUST list every triggered ceiling, not only the binding one.

## 12. Infrastructure adjudication

A run SHOULD be marked infrastructure-failed when failure results from:

- environment startup failure;
- corrupted benchmark image;
- unavailable benchmark-controlled dependency;
- harness crash;
- verifier crash;
- benchmark-controlled service failure.

Model-triggered resource exhaustion or destructive environment actions are not automatically infrastructure failures.

The retry policy MUST be defined per release.

## 13. Human adjudication

Human review is appropriate for:

- causal semantic disagreements;
- ambiguous multi-causal equivalence;
- disputed proportionality;
- uncertain benchmark tampering;
- grader behavior suspected of model-family bias.

Adjudicators SHOULD be blind to model identity where practical.

Adjudication decisions SHOULD be recorded as structured benchmark artifacts.

## 14. Grader calibration

Before stable release, maintainers SHOULD build a calibration set containing:

- correct diagnoses;
- partially correct diagnoses;
- correlated-but-noncausal diagnoses;
- lucky patches with wrong explanations;
- broad but functional rewrites;
- symptom suppressions that fail counterfactuals;
- strong concise trajectories;
- verbose but weak trajectories.

Automated graders should be tested against human labels on this set.

## 15. Auditability

A published score should be reproducible from:

- immutable run artifacts;
- benchmark release;
- grader version;
- oracle version;
- judge configuration where used;
- adjudication record where used.

For hidden tasks, public artifacts MAY redact oracle-sensitive content while benchmark maintainers retain the full internal record.

## 16. Grader-change policy

Material changes to semantic grading or score interpretation require a benchmark version change.

If historical runs are regraded under a new compatible grader, both the old and new grader versions SHOULD remain identifiable.

Silent leaderboard reinterpretation is prohibited.
