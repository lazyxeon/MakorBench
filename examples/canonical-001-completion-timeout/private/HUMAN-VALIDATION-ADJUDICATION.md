# Case 001 Human Validation Adjudication

This is maintainer-private guidance for evaluating blinded reviewer submissions.

## Oracle-compatible diagnosis

A response is oracle-compatible when it materially identifies:

1. a completion-channel/client authentication state that can outlive credential rotation;
2. post-rotation completion publication using stale credential state;
3. completion rejection preventing normal scheduler state transition;
4. work side effects having already committed, explaining the timeout/success contradiction.

The reviewer does **not** need to name the exact class/file used by the fixture.

## Partial diagnosis categories

### Correlated authentication diagnosis

Example:
> token refresh is flaky

This notices the auth surface but misses that refresh itself succeeds and the stale state lives in a long-lived channel.

### Manifestation diagnosis

Examples:
- scheduler timeout too short;
- reconciliation too slow.

These explain visible timing but not why completion delivery was lost.

### Contributor-only diagnosis

Example:
> UNAUTHENTICATED should be retried

Retry policy matters, but retry alone does not identify the stale credential snapshot.

## Prompt ambiguity analysis

Aggregate initial hypotheses by mechanism class rather than wording.

Desired outcome:
- multiple classes across reviewers;
- auth/completion may appear as one plausible class;
- exact stale-channel mechanism should not dominate prompt-only responses.

## Leakage audit

Any reviewer who discovers:
- `private/`;
- reference solution;
- oracle;
- counterfactual tests;
- public project issue/PR discussion

must be excluded from blinded diagnostic-rate calculation, though their leakage report remains useful.

## Acceptance recommendation

Recommend **validated** only when:
- >=3 valid blinded reviews;
- >=2 oracle-compatible diagnoses;
- evidence sufficiency is broadly positive;
- no material leak is found;
- disagreement does not show oracle underdetermination.

Otherwise recommend:
- revise and rerun;
- reject case;
- or classify as public tutorial only.
