# MakorBench Scoring Model

**Version:** 0.1-draft  
**Status:** Phase 1 normative scoring RFC  
**Depends on:** `SPEC.md`

## 1. Objective

MakorBench must distinguish between:

- an agent that correctly identifies the causal mechanism;
- an agent that produces a working patch by luck or broad search;
- an agent that explains the cause correctly but cannot repair it;
- an agent that suppresses the visible symptom without removing the cause;
- an agent that diagnoses and repairs the cause through disciplined investigation;
- an agent that reaches the right answer only after destructive or irrelevant scope expansion.

The benchmark therefore reports **multiple component scores** and a bounded aggregate **MakorScore**.

A single binary resolved/unresolved result is insufficient.

## 2. Scoring principles

### 2.1 Outcome evidence is strongest when deterministic

Functional repair, regression preservation, and counterfactual robustness SHOULD be graded by executable hidden tests or other deterministic verifiers whenever feasible.

### 2.2 Causal diagnosis must be graded against an explicit oracle

Task authors MUST define the material causal mechanism, causal roles, causal chain, and accepted equivalence classes before model evaluation.

A grader MUST NOT infer the benchmark's intended answer from the model response.

### 2.3 Investigation quality is graded from observable behavior

MakorBench does not require hidden chain-of-thought.

Process grading uses:

- tool calls;
- environment observations;
- experiments;
- test results;
- file inspection and edits;
- structured hypothesis checkpoints when voluntarily emitted;
- final diagnosis evidence references;
- ordering of evidence relative to persistent intervention.

### 2.4 Correctness dominates efficiency

A slower correct causal investigation is more valuable than a fast incorrect one.

Efficiency is reported separately and contributes only a small optional tie-break metric. It MUST NOT dominate the primary score.

### 2.5 No reward for unsupported narrative

A polished final explanation receives limited credit when its claims are not grounded in evidence actually observed during the run.

## 3. Headline metrics

Every canonical result MUST report:

1. **MakorScore** — aggregate 0–100 score;
2. **Diagnosis Score (D)** — 0–35;
3. **Investigation Score (G)** — 0–25;
4. **Intervention Score (I)** — 0–30;
5. **Verification & Judgment Score (V)** — 0–10;
6. **Functional Resolution** — pass/fail;
7. **Counterfactual Resolution Rate** — 0–100%;
8. **Regression Preservation Rate** — 0–100%;
9. **Diagnostic Cost Profile** — time, tokens, tool calls, experiments, cost when available.

The component scores MUST remain visible even when MakorScore is used for ranking.

## 4. Aggregate score

The draft MakorScore is:

```text
MakorScore = D + G + I + V
```

with a maximum of 100.

The additive structure is intentionally interpretable. It is combined with **score ceilings** for severe failure modes so that one dimension cannot fully compensate for another.

The weights are a v0.1 research choice and MUST be calibrated against pilot cases before a stable 1.0 release.

## 5. Diagnosis Score — 35 points

### D1. Causal mechanism correctness — 15 points

Measures whether the final diagnosis identifies the oracle-compatible causal mechanism or causal set.

Suggested anchors:

- **15** — correct minimal causal mechanism/set with no material contradiction;
- **12** — substantially correct with a minor omission that does not change the repair logic;
- **8** — identifies the right subsystem and partial mechanism but misses a material causal dependency;
- **4** — identifies a correlated contributor or manifestation rather than the root mechanism;
- **0** — materially incorrect cause.

For multi-causal tasks, full credit requires the material causal roles required by the oracle.

### D2. Causal-chain correctness — 10 points

Measures whether the diagnosis correctly connects cause to observed symptom through material intermediate state transitions/interactions.

- **10** — complete material chain;
- **7** — mostly correct chain with one non-critical gap;
- **4** — plausible but incomplete link from cause to manifestation;
- **0** — no valid causal chain or materially false chain.

### D3. Alternative-hypothesis discrimination — 5 points

Measures whether strong plausible alternatives were explicitly eliminated or appropriately left unresolved.

Credit is based on evidence, not the number of hypotheses named.

- **5** — major alternatives addressed with discriminating evidence;
- **3** — some major alternatives addressed;
- **1** — alternatives listed without meaningful discrimination;
- **0** — no meaningful handling of alternatives.

### D4. Evidence grounding — 5 points

Measures whether material causal claims are supported by agent-observed evidence.

The final diagnosis SHOULD cite observable trajectory event IDs.

- **5** — all material claims grounded in relevant observed evidence;
- **3** — mechanism grounded but some chain claims weakly supported;
- **1** — mostly assertion with sparse evidence;
- **0** — unsupported or contradicted by observed evidence.

## 6. Investigation Score — 25 points

Investigation scoring evaluates **how the agent established the diagnosis**, not private reasoning text.

### G1. Reproduction / causal confirmation — 10 points

- **10** — reproduces the failure or meets the task's strongest accepted causal-evidence criterion;
- **7** — strong causal evidence but incomplete reproduction;
- **4** — partial confirmation consistent with the cause;
- **0** — no meaningful causal confirmation.

A task may define equivalent evidence for failures that are unsafe or impractical to reproduce.

### G2. Discriminating experimentation — 6 points

Measures whether actions meaningfully distinguish competing hypotheses.

- **6** — multiple high-value discriminating tests or one decisive test;
- **4** — useful investigation with some low-information actions;
- **2** — mostly broad search with limited discrimination;
- **0** — no meaningful hypothesis discrimination.

### G3. Pre-intervention evidence quality — 5 points

Measures whether the agent gathered causal evidence **before committing the persistent repair**.

This is the primary defense against post-hoc rationalization.

- **5** — core causal evidence observed before the first persistent intervention;
- **3** — some causal evidence precedes the intervention, but key confirmation follows;
- **1** — repair substantially precedes diagnosis;
- **0** — final explanation is entirely post-hoc or unsupported.

The harness determines the **persistent intervention boundary** as the first edit that contributes materially to the final submitted patch, when this can be reconstructed. Diagnostic instrumentation that is fully reverted SHOULD NOT count as the intervention boundary.

### G4. Epistemic update discipline — 4 points

Measures observable responsiveness to evidence.

Credit can come from concise structured hypothesis checkpoints or from clear action changes after contrary evidence.

- **4** — investigation adapts appropriately as evidence changes;
- **2** — some evidence-driven adaptation;
- **0** — repeatedly ignores contradictory evidence or remains anchored without justification.

This component MUST NOT require hidden chain-of-thought.

## 7. Intervention Score — 30 points

### I1. Functional resolution — 10 points

Based on hidden functional tests for the original failure.

```text
10 × original_failure_tests_passed / original_failure_tests_total
```

Tasks with non-test verifiers MUST define an equivalent deterministic measure.

### I2. Counterfactual robustness — 10 points

Based on hidden variants that preserve the root causal mechanism while changing incidental conditions.

```text
10 × counterfactual_variants_passed / counterfactual_variants_total
```

A patch that suppresses only the originally observed manifestation should lose most or all of this credit.

### I3. Regression preservation — 5 points

```text
5 × protected_regressions_passed / protected_regressions_total
```

Critical safety/security regressions MAY trigger additional score ceilings.

### I4. Proportionality and scope discipline — 5 points

Measures whether the intervention is appropriately bounded.

- **5** — minimal/proportionate repair with no unjustified persistent changes;
- **3** — valid repair with modest unnecessary scope;
- **1** — broad rewrite or unrelated persistent modifications;
- **0** — destructive, benchmark-specific, or unjustifiably invasive intervention.

Diff size alone MUST NOT determine this score. Some genuine root causes require broad changes.

## 8. Verification & Judgment Score — 10 points

### V1. Post-fix causal verification — 5 points

Measures whether the agent verifies the causal prediction of its repair rather than merely running a generic test suite.

- **5** — re-tests the symptom/mechanism and validates the predicted causal effect;
- **3** — strong functional verification without direct causal confirmation;
- **1** — minimal smoke testing;
- **0** — no meaningful verification.

### V2. Residual uncertainty and escalation — 3 points

- **3** — accurately reports remaining uncertainty/risk and escalates when appropriate;
- **2** — generally calibrated with minor over/under-confidence;
- **0** — material unsupported certainty, concealed unresolved risk, or unjustified refusal.

### V3. Adjacent-finding discipline — 2 points

- **2** — genuine adjacent findings are reported separately and not modified without justification;
- **1** — minor scope confusion;
- **0** — unrelated findings drive unnecessary changes or distract from the target failure.

No points are awarded merely for finding extra defects.

## 9. Score ceilings and disqualifiers

Ceilings preserve the benchmark's causal objective.

### 9.1 Wrong-cause ceiling

If D1 < 8/15, **MakorScore is capped at 65**, even if the patch passes functional tests.

Rationale: a lucky or brute-force repair is useful evidence of implementation ability, but it is not strong root-cause diagnosis.

### 9.2 No-causal-evidence ceiling

If G1 = 0 and D4 <= 1, **MakorScore is capped at 60**.

### 9.3 Counterfactual failure ceiling

If I2 = 0, **MakorScore is capped at 70**.

### 9.4 Critical regression ceiling

A task MAY define critical protected invariants. Violating one caps MakorScore at **50** unless the benchmark oracle explicitly allows that tradeoff.

### 9.5 Benchmark tampering

Intentional modification of grader files, hidden fixtures, benchmark metadata, or verifier interfaces that are outside the permitted task surface yields **0** for the run.

### 9.6 Infrastructure failure

Infrastructure failure is **not** an agent score. Apply the benchmark retry policy.

## 10. Anti-post-hoc design

MakorBench MUST NOT score final prose alone as proof of good diagnosis.

The following rules apply:

1. material diagnosis evidence SHOULD cite trajectory event IDs;
2. evidence must have been available to the agent during the run;
3. the grader records whether evidence preceded or followed persistent intervention;
4. an explanation that first appears after a successful patch can earn diagnosis correctness but reduced investigation credit;
5. structured hypothesis declarations are useful but optional;
6. no hidden chain-of-thought is required.

This allows a concise agent to score well while preventing a model from receiving full process credit for reverse-engineering a story after accidental success.

## 11. Causal claim units

Each private task oracle SHOULD define **causal claim units** for semantic grading.

Example:

```json
[
  {
    "id": "C1",
    "weight": 0.30,
    "claim": "Expired credential state remains attached to pooled connection objects."
  },
  {
    "id": "C2",
    "weight": 0.25,
    "claim": "Credential rotation refreshes the global token but does not invalidate existing pooled connections."
  },
  {
    "id": "C3",
    "weight": 0.25,
    "claim": "The first request on a stale pooled connection times out before fallback creates a fresh connection."
  },
  {
    "id": "C4",
    "weight": 0.20,
    "claim": "Process restart clears the pool, explaining the observed temporary recovery."
  }
]
```

Claim units make semantic diagnosis grading auditable and reduce dependence on one exact wording.

Weights MUST sum to 1.0 within each scored causal component.

## 12. Semantic grading protocol

Deterministic grading is preferred, but causal language often requires semantic equivalence.

For stable leaderboard evaluation:

1. task authors define causal claim units before model evaluation;
2. deterministic/exact structural checks run first;
3. semantic matching is performed against claim units, not free-form benchmark intent;
4. a single model-as-judge MUST NOT be the sole authority for disputed high-impact scores;
5. judge identity/version and prompts MUST be versioned;
6. disagreements above a release-defined threshold SHOULD be adjudicated by a second independent judge or human reviewer;
7. benchmark maintainers SHOULD periodically audit judge agreement against human labels.

Hidden oracle text MUST NOT be exposed to the evaluated agent.

## 13. Trajectory scoring protocol

Trajectory scoring uses `trajectory.jsonl` and the schema defined in `schemas/trajectory-event.schema.json`.

Events have immutable sequence IDs.

Final diagnosis evidence references SHOULD point to these IDs.

The scorer may derive:

- evidence-before-intervention ratio;
- number of distinct experiments;
- repeated failed-action loops;
- test/reproduction attempts;
- files/subsystems inspected;
- persistent vs reverted edits;
- hypothesis checkpoint revisions when present.

Raw activity volume is **not** itself a positive signal.

More commands do not mean better engineering.

## 14. Efficiency metrics

Efficiency SHOULD be reported separately.

Recommended fields:

- wall-clock time;
- model input/output/reasoning tokens;
- monetary cost;
- tool calls;
- shell commands;
- distinct files inspected;
- experiments executed;
- time/actions to first oracle-relevant evidence;
- time/actions to first correct causal localization;
- time/actions to stable repair.

A release MAY publish a secondary Pareto frontier or cost-normalized analysis.

Efficiency contributes **0 points** to v0.1 MakorScore.

This avoids rewarding shallow early guesses over disciplined diagnosis before enough calibration data exists.

## 15. Abstention and escalation cases

Some future tasks MAY intentionally be underdetermined or unsafe to auto-repair.

Such tasks MUST be explicitly marked in the hidden oracle.

For a designated abstention task, full credit may require:

- identifying what is known;
- identifying the unresolved causal alternatives;
- naming the evidence needed to resolve them;
- avoiding unjustified code changes;
- escalating appropriately.

Ordinary solvable tasks do not award full credit for generic refusal.

## 16. Track-specific scoring

### 16.1 Canonical combined track

Uses the full 100-point MakorScore.

### 16.2 Diagnosis-Only track

Reports D + G + diagnosis-relevant V components, normalized to 100.

No intervention score is inferred.

### 16.3 Intervention-Only track

Agent receives oracle-quality diagnosis.

Reports I + intervention-relevant V components, normalized to 100.

### 16.4 Open-World / BYOA

Uses the same component definitions when possible but MUST be ranked separately from the Canonical track.

## 17. Dataset aggregation

For a benchmark release, report:

- mean MakorScore;
- median MakorScore;
- bootstrap 95% confidence interval;
- component-score means;
- functional resolution rate;
- full counterfactual resolution rate;
- per-difficulty-vector breakdowns;
- per-causal-archetype breakdowns.

A stable leaderboard SHOULD use the **mean MakorScore** as the primary ordering only after pilot calibration confirms that task-level score distributions are not pathologically skewed.

Task-level scores MUST remain downloadable/auditable.

## 18. Repeated runs

Because agentic runs can be stochastic, stable evaluations SHOULD use multiple trials per task for nondeterministic systems.

Report at minimum:

- number of trials;
- mean and variance;
- pass@k or consistency metrics when relevant;
- exact sampling/reasoning settings.

Leaderboard maintainers SHOULD avoid mixing one-shot and repeated-run results as if directly equivalent.

## 19. Calibration requirements before v1.0

The 35/25/30/10 weighting and score ceilings are **provisional**.

Before a stable v1.0 release, maintainers SHOULD evaluate whether the scoring model:

1. ranks disciplined correct diagnosis above lucky patching;
2. ranks root-cause repair above symptom suppression;
3. does not excessively penalize concise but effective agents;
4. does not reward verbose hypothesis theater;
5. correlates reasonably with blinded human engineering judgment;
6. remains stable across causal archetypes;
7. does not collapse to functional test pass rate;
8. does not become dominated by subjective semantic grading.

If these criteria fail, weights SHOULD change before v1.0 rather than preserving backward compatibility with a poor research-preview metric.

## 20. Reference comparisons

MakorBench deliberately extends beyond result-only software evaluation.

Relevant design context includes:

- SWE-bench's executable patch resolution model;
- APEX-SWE's finding that epistemic reasoning and uncertainty reduction are associated with production-debugging success;
- trajectory-aware evaluation work showing process signals can improve characterization beyond pass/fail;
- tool-use benchmarks that separately report trajectory quality and final accuracy.

These references motivate process-aware scoring but do not dictate MakorBench's weights.
