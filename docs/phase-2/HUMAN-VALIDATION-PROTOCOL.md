# MakorBench Human Validation Protocol

**Version:** 0.1-draft  
**Applies to:** public development Case 001 initially, then candidate stable tasks

## 1. Purpose

Human validation tests whether a MakorBench case is:

- genuinely ambiguous at the start;
- solvable from available evidence;
- causally well-grounded;
- realistic enough to resemble engineering diagnosis;
- free of accidental oracle leakage;
- neither trivial nor underdetermined.

Human validation is a **case-quality gate**, not a human-vs-model competition.

## 2. Reviewer independence

A stable candidate case SHOULD be reviewed by at least three people who:

- did not author the case;
- have not read the private oracle;
- have not read the reference solution;
- have not participated in prior debugging discussion of the case;
- have enough software/debugging experience to use the provided environment.

Reviewers MAY know the general MakorBench methodology.

## 3. Blinding

Reviewers receive only the generated reviewer bundle.

The bundle MUST exclude:

- `private/`;
- reference solution;
- counterfactual definitions;
- hidden verifier tests;
- oracle causal claims;
- scoring walkthrough that reveals the mechanism.

Reviewers MAY receive:
- initial operator prompt;
- agent-visible source;
- public smoke tests;
- generated logs/metrics/traces;
- ordinary local documentation;
- review instructions.

## 4. Review sequence

### Stage A — prompt-only hypotheses

Before inspecting source or evidence files, reviewer records:

- 3–5 plausible causal hypotheses, when possible;
- confidence that any one hypothesis is already clearly dominant;
- whether the prompt appears to leak a specific subsystem.

This stage measures genuine starting ambiguity.

### Stage B — investigation

Reviewer may inspect the full reviewer bundle and use ordinary local engineering tools.

They should keep concise evidence notes, not private chain-of-thought.

Record:
- commands/tools used;
- decisive observations;
- experiments/reproductions;
- discarded hypotheses and the evidence that weakened them.

### Stage C — final diagnosis

Reviewer submits:
- causal mechanism;
- causal chain;
- reproduction/evidence;
- proposed minimal repair;
- residual uncertainty;
- whether they would deploy the repair without additional review.

### Stage D — case-quality survey

Reviewer rates:
- realism;
- fairness;
- evidence sufficiency;
- prompt localization/leakage;
- puzzle/artificiality;
- difficulty;
- confidence in diagnosis.

## 5. Acceptance targets

A candidate case passes initial human validation when:

1. at least 3 independent reviewers complete the protocol;
2. at least 2 independently reach an oracle-compatible causal mechanism;
3. initial hypotheses show meaningful diversity;
4. no majority identifies the exact mechanism from prompt-only information with high confidence;
5. reviewers who solve the case cite evidence available in the bundle;
6. no reviewer reports missing information necessary in principle to distinguish the cause;
7. no private/oracle leakage is found;
8. the case is not broadly judged to be an artificial puzzle.

## 6. Failure interpretations

### Too easy

Signals:
- reviewers converge on exact subsystem from prompt alone;
- one grep/search reliably exposes the answer;
- root cause is obvious from a suspicious identifier/comment;
- no competing hypothesis survives shallow inspection.

Action: reduce direct leakage or redesign causal structure. Do **not** merely delete necessary evidence.

### Too hard / underdetermined

Signals:
- capable reviewers cannot distinguish two mechanisms even after full investigation;
- required evidence is absent;
- reproduction depends on undocumented hidden state;
- oracle requires knowledge outside the visible environment.

Action: add evidence or redesign the case.

### Wrong kind of hard

Signals:
- excessive repository size with no causal complexity;
- answer hidden behind arbitrary obfuscation;
- unrealistic naming tricks;
- dependency/setup friction dominates diagnosis.

Action: remove incidental difficulty.

## 7. Qualification record

For research reporting, collect only the experience needed to contextualize the review, for example:

- years of professional or equivalent software experience;
- primary technical domains;
- debugging/operations experience;
- familiarity with the implementation language.

Avoid collecting unnecessary personal information.

## 8. Oracle comparison

After a reviewer submits their response, maintainers compare it against the private oracle.

Reviewers SHOULD NOT be shown the oracle before submission.

An oracle-compatible diagnosis need not use exact wording. It must identify the material causal mechanism/set and support a repair that addresses it.

## 9. Disagreement review

If reviewers materially disagree:

1. determine whether disagreement reflects legitimate alternative causality;
2. inspect whether the oracle is over-specific;
3. inspect whether evidence is insufficient;
4. inspect whether one reviewer used accidental leakage;
5. revise the case if the benchmark—not the reviewer—is the source of ambiguity.

MakorBench should prefer rejecting a weak case over forcing reviewer consensus.

## 10. Reporting

For a validated case, publish or retain:

- number of reviewers;
- qualification summary;
- prompt-only hypothesis diversity;
- oracle-compatible diagnosis rate;
- median/dispersion of completion time when available;
- case-quality ratings;
- leakage findings;
- changes made after review.

Do not publish identifying reviewer information without consent.
