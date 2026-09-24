# MakorBench Scoring Examples

These examples are illustrative. They are not canonical benchmark tasks.

## Example A — Correct diagnosis, disciplined repair

The agent:
- reproduces an intermittent timeout;
- determines that stale credentials remain attached to pooled connections;
- rules out DNS and scheduler starvation with targeted experiments;
- patches pool invalidation;
- re-tests the failure;
- passes all counterfactuals and regressions.

Illustrative score:

| Component | Score |
|---|---:|
| Diagnosis | 35/35 |
| Investigation | 24/25 |
| Intervention | 30/30 |
| Verification/Judgment | 10/10 |
| **MakorScore** | **99** |

This is the intended high-score behavior.

## Example B — Lucky patch, wrong explanation

The agent broadly modifies connection retry logic. Hidden tests pass and the change happens to invalidate stale connections as a side effect, but the final diagnosis blames DNS timeout configuration.

Illustrative score:

| Component | Score |
|---|---:|
| Diagnosis | 5/35 |
| Investigation | 5/25 |
| Intervention | 27/30 |
| Verification/Judgment | 4/10 |
| Raw total | 41 |
| Wrong-cause ceiling | 65 |
| **MakorScore** | **41** |

A functional patch is recognized, but it does not masquerade as root-cause competence.

## Example C — Correct cause, failed implementation

The agent correctly identifies the stale-credential pool mechanism, reproduces it, and rules out strong alternatives. Its patch introduces a concurrency bug and fails regressions.

Illustrative score:

| Component | Score |
|---|---:|
| Diagnosis | 34/35 |
| Investigation | 24/25 |
| Intervention | 10/30 |
| Verification/Judgment | 6/10 |
| **MakorScore** | **74** |

This run demonstrates strong diagnosis but weak implementation.

## Example D — Symptom suppression

The agent raises the timeout from 5 seconds to 30 seconds. The original visible symptom disappears in the base test, but stale pooled connections still exist and hidden counterfactuals fail.

Illustrative score:

| Component | Score |
|---|---:|
| Diagnosis | 10/35 |
| Investigation | 6/25 |
| Intervention | 10/30 |
| Verification/Judgment | 3/10 |
| Raw total | 29 |
| Counterfactual ceiling | 70 |
| **MakorScore** | **29** |

The hidden variants expose that the root cause was not removed.

## Example E — Patch first, explain later

The agent immediately searches for credential code, makes a correct repair by intuition, then runs excellent experiments proving the mechanism after the patch.

It can still earn strong diagnosis and intervention credit. It loses pre-intervention evidence credit because the process does not demonstrate that the causal proof drove the intervention.

Illustrative score:

| Component | Score |
|---|---:|
| Diagnosis | 34/35 |
| Investigation | 17/25 |
| Intervention | 30/30 |
| Verification/Judgment | 9/10 |
| **MakorScore** | **90** |

MakorBench does not forbid intuition. It simply distinguishes validated diagnosis-before-repair from post-hoc confirmation.

## Example F — Verbose hypothesis theater

The agent repeatedly narrates ten hypotheses but runs almost no discriminating experiments. It eventually patches the correct line after broad search.

Hypothesis count provides no automatic credit.

Illustrative score:

| Component | Score |
|---|---:|
| Diagnosis | 25/35 |
| Investigation | 8/25 |
| Intervention | 25/30 |
| Verification/Judgment | 5/10 |
| **MakorScore** | **63** |

Verbose uncertainty is not the same as productive investigation.

## Example G — Useful adjacent defect

While diagnosing the target race, the agent notices a genuine unrelated unsafe temporary-file permission. It records it in `adjacent_findings` but does not modify it.

This can earn full adjacent-finding discipline credit.

If the agent rewrites the unrelated file-permission subsystem and creates new regressions, scope/proportionality credit falls.

## Example H — Multi-causal failure

The failure requires:
- a missing invalidation hook (**root cause**),
- a credential rotation event (**trigger**),
- a long-lived pooled connection (**precondition**),
- an unusually high retry timeout (**amplifier**).

A diagnosis that says only "the retry timeout is too high" identifies an amplifier, not the root cause.

The oracle and diagnosis schemas are designed to preserve this distinction.

## Example I — Correct abstention

A designated abstention case provides evidence consistent with two causes that cannot be distinguished with available instrumentation, and automatic repair would be unsafe.

A strong agent:
- states both remaining causes;
- names the missing discriminating measurement;
- avoids speculative code changes;
- escalates.

On a normal solvable task, generic refusal would not receive equivalent credit.
