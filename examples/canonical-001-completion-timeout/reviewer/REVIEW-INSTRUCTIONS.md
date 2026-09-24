# Case 001 Blinded Reviewer Instructions

You are evaluating the **quality of a debugging benchmark case**, not competing for a score.

## Rule 1 — do not seek outside answers

Please work only from this bundle.

Do not search the public repository, GitHub history, issue tracker, internet, or other copies of the case. The full public project contains oracle/reference material that would invalidate the review.

## Stage A — before inspecting source/evidence

Read `prompt.md` only.

Fill out the **Prompt-only section** of `review-response.md` before opening other files.

List the causal explanations you would reasonably consider at this point. Do not try to be exhaustive.

## Stage B — investigate

You may then inspect:

- `fixture/`
- `evidence/`

Use normal local tools and run code/tests as desired.

Record concise evidence and experiments. You are not being asked to provide private chain-of-thought.

## Stage C — diagnose and repair

In `review-response.md`, provide:

- your final root-cause mechanism;
- the causal chain from defect to symptom;
- reproduction or strongest causal evidence;
- the smallest repair you would make;
- residual uncertainty.

You may edit a working copy of the fixture if useful. Preserve your final diff separately.

## Stage D — case review

Complete the case-quality ratings.

Pay particular attention to:
- whether the prompt gives away the answer;
- whether evidence is sufficient;
- whether difficulty feels causal rather than artificial;
- whether you encountered any file that appeared to reveal hidden benchmark intent.

## Suggested time box

60–90 minutes is a useful target for this development case, but it is not a pass/fail requirement.

Record actual time spent.
