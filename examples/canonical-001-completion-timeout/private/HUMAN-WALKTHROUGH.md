# Human Oracle Walkthrough

This walkthrough demonstrates one disciplined path to the answer. It is not the only accepted investigation.

## 1. Start from contradiction

The key contradiction is:

- scheduler says the job timed out;
- artifact exists;
- billing indicates completion.

Therefore "job execution itself exceeded the timeout" is not sufficient to explain the state.

A competent investigator should separate:
1. execution success;
2. completion notification;
3. scheduler state transition.

## 2. Test the scheduler hypothesis

Inspect scheduler metrics and lease logic.

Findings:
- lease expiration behaves according to configured timeout;
- there is no broad scheduler stall;
- healthy jobs on the same scheduler update normally;
- longer timeout reduces visible incidents because reconciliation sometimes runs first.

Conclusion:
- scheduler timeout is likely a manifestation/amplifier, not the initiating defect.

## 3. Inspect completion path

For affected job IDs:

- worker completes work;
- artifact commit succeeds;
- billing commit succeeds;
- scheduler never receives normal completion transition;
- completion delivery records a failure.

This moves probability toward the worker-to-completion-gateway path.

## 4. Decode the transport failure

Inspect completion RPC result for several incidents.

The failure status corresponds to authentication rejection.

Do **not** stop at "authentication is broken." Ask why it is intermittent and uptime-dependent.

## 5. Compare credential lifecycle

Observe:
- worker token manager refreshes credentials successfully;
- incidents cluster after refresh;
- new channels created after refresh succeed;
- failing requests disproportionately use channels created before refresh.

This is strong discriminating evidence against generic networking.

## 6. Inspect channel/interceptor code

Find that authentication metadata is captured when the long-lived interceptor/channel is created.

Token manager refresh is independent.

Hypothesis:

> a channel can remain operational while carrying an auth snapshot older than the token manager's current credential.

## 7. Reproduce

Controlled experiment:

1. create completion channel;
2. publish successfully;
3. force/accelerate token rotation;
4. keep the channel alive;
5. publish again through the same channel.

Expected pre-fix result:
- second completion RPC rejected for auth;
- new channel succeeds.

This isolates the mechanism.

## 8. Repair

Preferred repair:
- obtain current token per RPC invocation, or otherwise guarantee channel auth is refreshed atomically with token rotation.

Avoid:
- disabling rotation;
- accepting expired credentials;
- blanket retries;
- scheduler timeout increase.

## 9. Verify

Verify:
- controlled pre-fix reproduction no longer fails;
- ordinary completion delivery still succeeds;
- auth rejection still occurs for genuinely invalid credentials;
- no duplicate completion/billing side effects;
- original integration scenario passes;
- counterfactual variants pass.

## 10. Final causal chain

```text
token rotates
  ↓
token manager holds new token
  ↓
long-lived channel still holds old auth snapshot
  ↓
post-rotation completion RPC uses stale credentials
  ↓
gateway rejects completion event
  ↓
artifact + billing remain committed
  ↓
scheduler receives no completion transition
  ↓
lease expires before/without reconciliation
  ↓
job is displayed as TIMED_OUT despite successful work
```

That chain explains every major observation, including why restart helps and why longer timeout only partially mitigates the symptom.
