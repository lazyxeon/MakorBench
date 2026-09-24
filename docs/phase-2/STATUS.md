# Phase 2 Status

**Date:** 2026-09-24  
**Working project name:** MakorBench  
**Repository rename:** pending user action from RootCauseBench to MakorBench

## Integration state

The approved Phase 0 reconnaissance, Phase 1 task contract, and Phase 1 scoring/trajectory RFC have now been merged into `main`. External review gates remain open on Issues #2 and #3.

The repository validation workflow is therefore now present on the default branch, allowing downstream Phase 2 pull requests to execute real CI.

## Approved foundations

### Phase 0
Reconnaissance and benchmark positioning complete enough for campaign progression.

### Phase 1 — task contract
Maintainer-approved for progression.

Independent implementability review remains required before stable methodology claims.

### Phase 1 — trajectory/scoring
Maintainer-approved as the working v0.1 pilot model.

Current draft:
- Diagnosis: 35
- Investigation: 25
- Intervention: 30
- Verification/Judgment: 10
- efficiency reported separately

External human calibration and independent review remain required before v1.0.

## Phase 2 — Case 001 paper design

**Case:** `makor-dev-001-completion-timeout`

Paper-canonical design is complete.

Artifacts include:
- symptom-first prompt;
- evidence map;
- oracle;
- causal roles;
- four counterfactual designs;
- authoring record;
- human diagnostic walkthrough;
- scoring walkthrough;
- executable-fixture plan.

Task/oracle schema validation passed directly.

## Phase 2 — Case 001 executable fixture

Implementation exists on branch `phase-2-case-001-impl`.

Implemented:
- fake deterministic clock;
- scheduler leases;
- reconciliation;
- artifact store;
- idempotent billing ledger;
- rotating service credentials;
- completion gateway authentication;
- pooled long-lived completion channels;
- target stale-auth interaction;
- sparse post-rotation failure behavior;
- worker restart mitigation;
- timeout/reconciliation mitigation;
- private reference repair;
- public smoke test;
- private oracle/regression tests;
- three executable counterfactual families;
- evidence generator;
- CI wiring.

### Visibility boundary

Agent-visible development fixture:
- `examples/canonical-001-completion-timeout/fixture/`

Evaluator/private material:
- `examples/canonical-001-completion-timeout/private/`

The reference repair and oracle counterfactual tests have been removed from the agent-visible package.

### Validation state

Completed:
- paper task/oracle JSON Schema validation;
- causal claim-unit weight validation;
- behavioral dry-run of the intended core mechanism;
- behavioral dry-run of sparse 3-channel post-rotation failures.

Pending:
- exact repository test execution under GitHub Actions;
- generated evidence bundle inspection from the committed code;
- human diagnostic review;
- reference repair execution against all committed verifier tests.

GitHub CI is wired and is now eligible to execute because the validation workflow has been integrated into `main`.

## Next gates

1. integrate approved stack sufficiently for CI to execute;
2. run Case 001 public/private test suites;
3. inspect generated evidence for difficulty/leakage;
4. perform blinded human review;
5. tune Case 001 based on reviewer behavior;
6. then decide whether to build additional cases or a minimal canonical harness adapter.
