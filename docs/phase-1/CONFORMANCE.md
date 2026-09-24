# MakorBench v0.1 Implementer Conformance Checklist

This checklist operationalizes `SPEC.md` for independent implementations.

An implementation claiming **Canonical Track compatibility** should be able to answer **yes** to every REQUIRED item below.

## Task ingestion

- [ ] Validates the public task manifest against `schemas/task-manifest.schema.json`.
- [ ] Presents only the designated initial symptom prompt at run start.
- [ ] Mounts the specified repository/source snapshot.
- [ ] Uses the pinned environment image or an equivalently verified immutable snapshot.
- [ ] Enforces the declared network policy.
- [ ] Enforces the declared wall-time/resource budget.

## Privacy boundary

- [ ] Private oracle material is never mounted into the agent environment.
- [ ] Hidden regression tests are inaccessible to the agent.
- [ ] Hidden counterfactual variants are inaccessible to the agent.
- [ ] Reference interventions are inaccessible to the agent.
- [ ] Public run artifacts do not leak hidden-case oracle content.

## Agent interaction

- [ ] Records model identity/version when available.
- [ ] Records reasoning-effort setting when configurable.
- [ ] Records agent scaffold and version.
- [ ] Records harness and version.
- [ ] Captures observable tool calls and environment outputs.
- [ ] Does not require hidden chain-of-thought.

## Required outputs

- [ ] Captures final repository diff or explicit no-change outcome.
- [ ] Validates `diagnosis.json` against `schemas/diagnosis.schema.json`.
- [ ] Validates `verification.json` against `schemas/verification.schema.json`.
- [ ] Archives an observable diagnostic trajectory.
- [ ] Records cost/token/time metadata when available.

## Evaluation

- [ ] Applies hidden functional/regression checks.
- [ ] Applies the task's hidden counterfactual variants.
- [ ] Distinguishes infrastructure failure from agent failure.
- [ ] Uses a documented retry policy for infrastructure failures.
- [ ] Preserves diagnosis and intervention results as separable components.
- [ ] Does not reduce canonical reporting to a single binary pass/fail.

## Stable-release task admission

For every task included in a stable canonical release:

- [ ] Oracle causal mechanism is documented.
- [ ] Material causal roles and causal chain are documented.
- [ ] Accepted reproduction/evidence route exists.
- [ ] At least one valid intervention class exists.
- [ ] Oracle intervention passes all hidden counterfactual variants.
- [ ] Multiple plausible initial hypothesis classes are documented.
- [ ] At least three independent qualified human reviewers evaluated the case.
- [ ] At least two reviewers independently reached an oracle-compatible diagnosis, except designated abstention cases.
- [ ] Trivial shortcut baselines were tested.
- [ ] Contamination/provenance record exists.
- [ ] Randomness and failure-rate envelope are characterized when applicable.

## Comparable result declaration

A published result should explicitly declare whether it is:

- **Canonical** — reference scaffold/profile and canonical network policy;
- **Open-World** — public network/precedent retrieval permitted;
- **Diagnosis-Only** — no intervention required;
- **Intervention-Only** — oracle-quality diagnosis supplied;
- **BYOA** — non-canonical scaffold; reported separately.

If any REQUIRED Canonical condition is not met, the result should not be represented as directly comparable to the Canonical leaderboard.
