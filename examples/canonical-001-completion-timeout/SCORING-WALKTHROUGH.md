# Scoring Walkthrough — Canonical Worked Case 001

This document maps representative agent behaviors to the MakorBench v0.1 rubric.

## Oracle causal claim units

Recommended private claim units:

| ID | Weight | Claim |
|---|---:|---|
| C1 | 0.30 | long-lived completion channel/interceptor snapshots credential state at construction |
| C2 | 0.20 | token rotation updates the token manager without updating already-active channel auth metadata |
| C3 | 0.20 | post-rotation completion RPC can therefore be rejected while artifact/billing side effects have already committed |
| C4 | 0.15 | missing completion transition causes scheduler lease expiry / timeout manifestation |
| C5 | 0.15 | worker restart or channel recreation temporarily fixes the issue by rebuilding auth state |

Weights sum to 1.0.

## High-scoring trajectory

Agent:
- notices completed-work / timed-out-state contradiction;
- compares scheduler state with completion transport;
- correlates failures with channel age and token rotation;
- runs a controlled keep-channel-open rotation experiment;
- identifies stale auth snapshot;
- changes auth to resolve current token per RPC;
- validates auth security, idempotency, original symptom, and hidden variants.

Expected:
- D: 33–35
- G: 23–25
- I: 28–30
- V: 9–10
- MakorScore: 93–100

## Scheduler-timeout false fix

Agent:
- increases timeout to 180 seconds;
- base visible timeout frequency drops;
- never investigates completion transport.

Expected:
- low D/G;
- partial I1 possible in weak base scenario;
- I2 near zero under reconciliation-disabled counterfactual;
- counterfactual ceiling applies.

## Blanket retry false fix

Agent:
- retries every completion failure indefinitely.

Potential outcome:
- some auth failures disappear after eventual channel replacement;
- resource use and duplicate-delivery risk increase;
- root cause remains poorly understood.

Expected:
- limited diagnosis credit;
- proportionality/safety penalty;
- regression tests should reject unbounded retry or duplicate completion behavior.

## Correct patch by intuition, proof after

Agent:
- sees auth code quickly;
- changes interceptor to fetch current token;
- then performs excellent reproduction/verification.

Expected:
- strong D/I/V;
- reduced G3 pre-intervention evidence;
- still high overall score, but below equally correct evidence-led trajectory.

## Wrong correlated diagnosis

Agent:
- correctly notices auth failures but concludes "token refresh is sometimes failing";
- token-manager refresh itself is actually healthy.

Expected:
- partial D1/D2;
- evidence may contradict mechanism;
- patching token refresh cadence rather than channel snapshot should fail counterfactuals.

## Adjacent finding

Suppose the agent also notices that channel metrics lack a token-generation label.

Reporting that as an observability improvement is acceptable.

Reworking the entire metrics subsystem during the repair should reduce scope/proportionality credit unless necessary.
