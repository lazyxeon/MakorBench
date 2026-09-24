# Canonical Worked Case 001 — Completion Timeout

**Case ID:** `makor-dev-001-completion-timeout`  
**Status:** paper-canonical design case; not leaderboard eligible  
**Purpose:** exercise the MakorBench v0.1 task, oracle, trajectory, counterfactual, and scoring contracts before building an executable fixture.

## Case thesis

The operator sees a scheduling symptom:

> a small number of jobs are marked `TIMED_OUT` even though their output artifacts exist and downstream billing records indicate successful completion.

The actual causal defect is **not in the scheduler**.

A long-lived worker completion channel snapshots authentication metadata when the channel is created. The worker's token manager later rotates credentials, but active channels continue publishing completion events with the stale token. The first affected publish fails; the work product has already committed, so the job appears to have succeeded everywhere except the scheduler's completion state.

The case is designed so a competent engineer can discover this through evidence and controlled experiments without being told which subsystem is at fault.

## Why this is a MakorBench case

It includes:

- a vague downstream symptom;
- multiple genuine initial hypotheses;
- a root cause outside the obvious surface subsystem;
- a designed reproduction path;
- a minimal repair class;
- hidden counterfactual variants;
- realistic logs/metrics/traces/code evidence;
- an oracle causal chain;
- explicit false-fix traps;
- a scoring walkthrough.

## Public worked-case warning

This directory intentionally contains the oracle because it is a **worked example for benchmark designers**.

It MUST NOT be used as a hidden leaderboard task.

The eventual executable version should either:
- be treated as a public development case; or
- be structurally transformed into a new hidden case with a different implementation and symptom surface.

## Directory

- `prompt.md` — what the evaluated agent sees initially
- `task.json` — paper task manifest
- `EVIDENCE-MAP.md` — proposed agent-visible evidence surfaces
- `SCORING-WALKTHROUGH.md` — examples of strong and weak trajectories
- `IMPLEMENTATION-PLAN.md` — how to turn the paper case into an executable fixture
- `private/oracle.json` — exposed here only because this is a worked example
- `private/AUTHORING-RECORD.md`
- `private/COUNTERFACTUALS.md`
- `private/HUMAN-WALKTHROUGH.md`

## Intended causal roles

| Role | Case element |
|---|---|
| Root cause | completion channel auth interceptor snapshots token state at channel creation |
| Trigger | service-token rotation |
| Precondition | a long-lived active completion channel survives across rotation |
| Contributor | `UNAUTHENTICATED` completion failure is not transparently retried with refreshed credentials |
| Amplifier | scheduler lease may expire before periodic reconciliation notices the completed artifact |
| Manifestation | scheduler/UI reports `TIMED_OUT` although artifact and billing side effects exist |

The distinction between these roles is intentional. Raising the scheduler timeout can reduce visible incidents without repairing the root cause.
