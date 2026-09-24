# Evidence Map

This document describes the **planned agent-visible evidence** for the executable version. It is not part of the initial prompt.

## System topology

```text
API
 │
 ▼
Scheduler ──► work queue ──► Worker
   ▲                         │
   │                         ├──► Artifact Store
   │                         ├──► Billing Ledger
   │                         └──► Completion Gateway ──► Scheduler state
   │
   └──────── periodic reconciliation ◄──────── Artifact metadata
```

A job can therefore produce its artifact and billing side effect before the scheduler receives its completion notification.

## Proposed repository areas

```text
services/
  scheduler/
    lease_manager.py
    reconciler.py
  worker/
    runner.py
    completion_client.py
    token_manager.py
    channel_pool.py
  completion_gateway/
    server.py
    auth.py
libs/
  rpc/
    retry_policy.py
tests/
  integration/
  worker/
```

The names above are descriptive enough to be realistic but should not expose the fault directly.

## Logs

The environment should include a noisy multi-service log corpus.

Relevant but non-conclusive observations:

- timed-out jobs show normal worker execution completion;
- artifact commit succeeds before scheduler timeout;
- completion publishing occasionally records a generic delivery failure;
- the error code can be traced to an authentication rejection, but the log MUST NOT say "stale token";
- token refresh logs occur elsewhere and at a different time scale;
- unrelated transient network warnings appear often enough to make networking plausible.

Example shape:

```text
worker job=8f2a render_complete duration_ms=11843
artifact job=8f2a commit_ok object=...
billing job=8f2a ledger_commit_ok
worker job=8f2a completion_delivery_failed status=16 retryable=false channel_id=ch07
scheduler job=8f2a lease_expired age_ms=45121
```

A strong agent must connect the status code and channel age to credential lifecycle rather than merely grep "timeout".

## Metrics

Available time series should include:

- worker CPU/memory;
- queue depth;
- database latency;
- scheduler lease-expiry count;
- completion-delivery failure count;
- channel age histogram;
- token refresh count;
- reconciliation completion count.

The designed signal:

- incidents cluster after token rotation;
- not every rotated worker fails;
- failures disproportionately involve channels created before the latest rotation;
- host resource metrics remain normal.

The correlation should be discoverable but not precomputed for the agent.

## Traces

A subset of jobs includes traces spanning:

- worker completion;
- artifact commit;
- completion RPC;
- scheduler state update.

Failed cases show completion RPC rejection before scheduler state transition.

Tracing coverage should be sampled so the agent must select useful incident IDs rather than receive a perfect trace for every failure.

## Source-code evidence

The causal defect should be represented approximately as:

```python
class AuthInterceptor:
    def __init__(self, token_manager):
        self._token = token_manager.current_token  # snapshot

    def metadata(self):
        return {"authorization": f"Bearer {self._token}"}
```

while token refresh correctly changes:

```python
token_manager.current_token = refreshed_token
```

The channel pool reuses the interceptor as long as an active channel remains healthy.

The retry policy treats ordinary transient transport failures as retryable but not authentication failures.

## Existing tests

Tests should prove:

- token manager itself refreshes successfully;
- new completion channels use the current token;
- completion RPC succeeds normally;
- scheduler reconciliation eventually sees completed artifacts.

The missing coverage is the interaction:

> **an already-active completion channel survives a token rotation and is used afterward.**

That omission is realistic because each subsystem's local tests pass.

## Historical context

The executable case MAY include neutral git history showing:
- a prior channel-pooling optimization;
- a later token-rotation change;
- unrelated scheduler timeout tuning.

Commit messages MUST NOT reveal the bug.

The failure should emerge from the interaction of individually reasonable changes rather than a commit named "break auth refresh."
