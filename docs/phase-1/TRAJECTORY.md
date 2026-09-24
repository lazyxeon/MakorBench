# MakorBench Diagnostic Trajectory Contract

**Version:** 0.1-draft  
**Status:** Phase 1 normative companion to `SCORING.md`

## 1. Purpose

The diagnostic trajectory captures **observable engineering behavior** without requiring private chain-of-thought.

It exists to answer questions such as:

- What evidence did the agent actually inspect?
- What experiments did it run?
- What changed after contrary evidence?
- Did it establish causality before patching?
- Did it verify the repair?
- Did it wander, brute-force, or repeatedly retry ineffective actions?
- Did the final diagnosis cite evidence that was genuinely observed?

## 2. Non-goal: hidden reasoning capture

MakorBench MUST NOT require hidden chain-of-thought, scratchpad text, or provider-private reasoning tokens.

A model can score perfectly with concise visible communication if its observable investigation establishes the required evidence.

## 3. Event log

The canonical trajectory is an append-only JSONL stream.

Every event MUST include:

- `event_id` — unique within the run;
- `sequence` — monotonically increasing integer;
- `event_type`;
- `timestamp` when available;
- `source` — agent, harness, environment, grader, or user;
- `payload`.

The normative event schema is `schemas/trajectory-event.schema.json`.

## 4. Core event types

Canonical harnesses SHOULD map observable activity into the following types:

- `message`
- `tool_call`
- `tool_result`
- `file_read`
- `file_write`
- `command`
- `command_result`
- `test_run`
- `experiment`
- `observation`
- `hypothesis_checkpoint`
- `verification`
- `final_artifact`
- `infrastructure_event`

Provider-specific raw events MAY be preserved in addition.

## 5. Hypothesis checkpoints

Hypothesis checkpoints are OPTIONAL for agent compatibility.

When emitted, they SHOULD contain only concise externally reportable state:

- hypothesis label;
- confidence bucket or probability;
- supporting event IDs;
- contradicting event IDs;
- status: active, weakened, rejected, confirmed.

Agents MUST NOT be required to reveal private reasoning to populate these fields.

## 6. Evidence references

The final `diagnosis.json` SHOULD cite trajectory event IDs supporting material causal claims.

Evidence references enable the scorer to distinguish:

- observed evidence;
- unsupported assertion;
- evidence gathered before repair;
- evidence gathered only after successful repair;
- contradictory evidence ignored by the final narrative.

A reference to a nonexistent event is invalid.

## 7. Persistent intervention boundary

MakorBench defines the **persistent intervention boundary** as the earliest observable repository modification that materially contributes to the final submitted intervention.

When technically feasible, the harness SHOULD reconstruct this by comparing intermediate file states with the final diff.

Temporary instrumentation that is fully reverted before submission SHOULD NOT establish the boundary.

The boundary is used for investigation scoring, not to forbid early editing.

## 8. Derived trajectory facts

A scorer MAY derive deterministic facts including:

- event count;
- tool-call count;
- experiment count;
- unique files inspected;
- unique subsystems touched;
- tests before intervention;
- tests after intervention;
- time to first oracle-relevant evidence;
- evidence-before-intervention ratio;
- persistent edit count;
- reverted diagnostic edit count;
- repeated command loops;
- failed experiment recovery;
- final evidence citation coverage.

Derived facts SHOULD be cached in `grader-results.json` for auditability.

## 9. What is not automatically rewarded

The following MUST NOT receive positive process credit merely because they occur frequently:

- more tokens;
- more commands;
- more file reads;
- more hypotheses;
- more patches;
- more tool calls;
- longer explanations.

Volume is not competence.

## 10. Evidence-before-intervention metric

For oracle-relevant evidence items observed by the agent, the scorer MAY report:

```text
EBI = relevant_evidence_observed_before_boundary
      / relevant_evidence_observed_total
```

EBI is a diagnostic metric, not a complete score by itself.

Some efficient agents may make a small tentative repair early and then validate correctly. Human-calibrated G3 scoring remains authoritative in v0.1.

## 11. Experiment quality

A strong experiment changes the relative plausibility of competing causal hypotheses.

Case authors SHOULD annotate expected discriminating evidence in the private oracle.

Examples:

- changing token lifetime separates credential-lifecycle from network hypotheses;
- bypassing a cache separates stale-state from persistence hypotheses;
- forcing single-thread execution separates race-condition from deterministic logic hypotheses;
- restarting only one component distinguishes local state from distributed state.

Generic full test-suite execution is useful verification but often weak diagnostic discrimination.

## 12. Belief revision

MakorBench may credit belief revision without explicit probability narration.

Observable evidence includes:

- switching investigative subsystem after a hypothesis is contradicted;
- designing a new experiment in response to a failed prediction;
- abandoning an edit after it fails reproduction;
- explicitly marking a hypothesis rejected.

Repeatedly pursuing a contradicted path can reduce G4.

## 13. Trajectory privacy and publication

Public dev tasks SHOULD publish full trajectories when licensing permits.

Hidden leaderboard tasks SHOULD publish enough derived metrics for auditability without leaking private task content.

Raw trajectories containing secrets, proprietary logs, or hidden oracle material MUST be sanitized or withheld.

## 14. Harness adapters

Different agent frameworks expose different event formats.

A MakorBench harness adapter MUST:

1. preserve provider/framework raw logs when permitted;
2. translate comparable observable events into the canonical schema;
3. document lossy mappings;
4. never fabricate semantic hypothesis events that the agent did not emit;
5. version the adapter.

## 15. Trajectory integrity

The canonical event stream SHOULD be append-only and integrity-protected for stable leaderboard runs.

Recommended mechanisms include:

- sequential hashes;
- immutable artifact storage;
- run-level content hash;
- signed server-side metadata.

The benchmark need not require cryptographic signing for local development runs.

## 16. Grading boundary

Trajectory analysis may inform G2–G4, D4, and V1–V3.

Functional test outcomes remain independent of trajectory interpretation.

A model MUST NOT lose functional credit merely because its trajectory adapter is less expressive, provided the canonical required observable events are captured.

## 17. Research metrics

Non-ranking research metrics MAY include:

- hypothesis churn;
- branching factor;
- repeated-failure recovery;
- subsystem revisit rate;
- evidence-to-edit latency;
- experiment information yield;
- proportion of final causal claims supported by pre-intervention evidence;
- false-positive adjacent defect rate.

These SHOULD remain diagnostic until validated.
