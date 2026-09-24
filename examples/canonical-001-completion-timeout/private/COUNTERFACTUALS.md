# Hidden Counterfactual Design

These variants are public here only because this is a worked example.

The eventual executable development case should keep them private from the evaluated agent during a run.

## CF-1 — Rotation jitter

Change:
- token lifetime and refresh timing are randomized within a bounded range;
- worker/process IDs and channel IDs are randomized.

Invariant:
- active channels still snapshot auth before rotation.

Purpose:
- defeats hard-coded assumptions about a six-hour boundary;
- validates that the repair follows credential state rather than clock constants.

Expected:
- per-RPC fresh-auth or safe channel-invalidation repair passes;
- timeout tuning and hard-coded refresh timing fail.

## CF-2 — Reconciliation disabled

Change:
- periodic artifact reconciliation is delayed beyond the scheduler timeout.

Invariant:
- stale channel auth remains the cause of lost completion events.

Purpose:
- removes the mitigating path that made a 90-second timeout appear helpful.

Expected:
- correct auth repair passes;
- timeout-only mitigation fails more clearly.

## CF-3 — Different concurrency / channel reuse

Change:
- reduce worker concurrency and channel-pool size;
- ensure at least one channel remains active across rotation.

Invariant:
- a pre-rotation channel remains in use after token refresh.

Purpose:
- checks that the repair is not accidentally tied to the original pool cardinality.

Expected:
- causal repair passes;
- fixes that merely churn a specific pool slot fail.

## CF-4 — Alternate gateway latency

Change:
- introduce modest non-auth completion-gateway latency and unrelated transient `UNAVAILABLE` responses.

Invariant:
- auth rejection remains distinct from ordinary transport failures.

Purpose:
- checks that broad retry changes do not merely mask all delivery errors.

Expected:
- correct auth lifecycle repair plus existing transient retry behavior passes;
- indiscriminate retry-forever behavior fails safety/resource checks.

## Counterfactual acceptance rule

The root mechanism is invariant across all variants:

> completion requests can be emitted with credentials older than the token manager's current state because auth metadata was captured at long-lived channel construction.

The exact visible symptom frequency is allowed to vary.
