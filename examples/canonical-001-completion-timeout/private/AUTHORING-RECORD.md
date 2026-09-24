# Authoring Record — Canonical Worked Case 001

## Status

Paper-canonical design artifact. Human validation pending. Not leaderboard eligible.

## Design objective

Test whether an engineering agent can work backward from a scheduler timeout symptom to a hidden cross-component credential-lifecycle defect.

## Why the symptom is plausibly misleading

The visible state is `TIMED_OUT`, and increasing the scheduler timeout reduces incident visibility. Reasonable engineers may initially investigate:

1. scheduler lease expiry / timing logic;
2. worker heartbeat starvation or clock skew;
3. queue acknowledgement / duplicate-delivery behavior;
4. database visibility or transaction-ordering race;
5. completion publisher/network path;
6. reconciliation lag.

The scheduler is where the error manifests, but it is not where the causal defect lives.

## Oracle mechanism

A completion RPC channel captures authentication metadata at channel creation. Token rotation updates the token manager but does not update metadata already captured by long-lived active channels.

A post-rotation completion event sent through one of those channels is rejected by the completion gateway. The work artifact and billing side effects have already committed. The scheduler therefore receives no completion transition and eventually expires the job lease.

The failed authentication marks/replaces the affected channel, which keeps the incident sparse rather than making every subsequent job fail.

## Causal roles

- **root cause:** stale authentication snapshot in long-lived completion channel/interceptor;
- **trigger:** token rotation;
- **precondition:** active channel created before rotation survives into the new-token period;
- **contributor:** authentication failure is not transparently retried after refreshing metadata;
- **amplifier:** scheduler timeout may occur before periodic artifact reconciliation;
- **manifestation:** completed job appears `TIMED_OUT`.

## Why the 90-second timeout appears to help

Periodic reconciliation can discover some completed artifacts after the completion RPC was lost.

Increasing the timeout gives reconciliation more opportunity to repair scheduler state before lease expiration.

It therefore reduces the *visible* symptom while leaving stale-auth completion failures intact.

This is a deliberate false-fix trap.

## Strong discriminating experiments

Examples include:

- shorten token rotation interval in a controlled test while holding a completion channel open;
- compare channel creation time with latest token rotation for failed vs successful completion publishes;
- force channel rebuild immediately after token refresh and compare failure rate;
- inject per-RPC fresh auth metadata without otherwise changing scheduler behavior;
- isolate scheduler timeout/reconciliation timing while directly observing completion-RPC success.

The benchmark MUST accept novel experiments that establish the same causal relationship.

## Weak/non-discriminating activity

Examples:

- repeatedly raising job timeout;
- running the entire unit test suite without targeted instrumentation;
- grepping only for "TIMED_OUT";
- restarting workers and declaring the scheduler fixed;
- broad retry changes that obscure the auth failure.

## Accepted intervention classes

Preferred minimal repair:

- resolve the current token at RPC invocation time rather than snapshotting it at channel construction.

Potentially accepted equivalent repairs:

- invalidate/rebuild completion channels synchronously on credential rotation, with safe concurrency handling;
- retry an authentication-rejected completion exactly through a freshly authenticated channel, **if** the implementation preserves security and idempotency.

Broadly making all failures retry forever is not equivalent.

Increasing scheduler timeout is not equivalent.

## Safety constraints

A repair MUST NOT:

- disable token rotation;
- accept expired tokens;
- weaken gateway authentication;
- mark jobs complete without authenticated completion or valid reconciliation evidence;
- create duplicate billing/artifact side effects;
- introduce unbounded retries.

## Human validation target

Before stable use:
- >=3 independent reviewers;
- >=2 independently reach an oracle-compatible mechanism;
- reviewers should show different initial hypotheses;
- no reviewer should identify the exact mechanism from the prompt alone;
- reviewers should judge the evidence sufficient and the repair proportionate.

## Contamination

The case is synthetic but constructed from common distributed-systems failure patterns.

Any hidden descendant MUST materially transform implementation details, topology, identifiers, timing, and symptom wording to avoid simple memorization of this public worked case.
