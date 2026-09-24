# Campaign Plan

The project should proceed as a specification-first campaign. The goal is to make the idea rigorous enough that an established benchmark group can implement, adopt, or collaborate on it.

## Phase 0 — Reconnaissance and positioning

**Goal:** establish novelty, scope, prior art, constraints, and implementation leverage.

Artifacts:
- benchmark landscape,
- naming decision,
- initial design principles,
- campaign plan.

Gate:
- a one-paragraph benchmark definition that is clearly distinct from SWE-bench, APEX-SWE Observability, OpenRCA, and the existing Edge Delta RootCauseBench.

Status: **in progress; substantive recon complete, naming unresolved.**

## Phase 1 — Normative benchmark specification

**Goal:** write the benchmark as if an independent team had to implement it without asking the authors what was intended.

Planned artifacts:
- `SPEC.md`
- `SCORING.md`
- `CASE-AUTHORING.md`
- `TRAJECTORY-SCHEMA.md`
- `THREAT-MODEL.md`

Key decisions:
- exact agent inputs,
- allowed tools,
- required outputs,
- time/compute limits,
- root-cause schema,
- hypothesis/evidence event schema,
- scoring weights,
- abstention rules,
- counterfactual protocol,
- case admission/rejection rules.

Gate:
- two independent readers can derive the same implementation behavior from the spec.

## Phase 2 — Canonical worked cases

**Goal:** prove that the protocol is understandable and practically constructible.

Deliverables:
- one fully worked toy case for documentation,
- one realistic medium case,
- one difficult case with multiple credible hypotheses,
- oracle diagnosis,
- oracle minimal patch,
- counterfactual variants,
- human diagnostic walkthrough.

Gate:
- at least one strong coding agent can run end-to-end through the protocol,
- human reviewers agree the case is fair and genuinely diagnostic.

## Phase 3 — Pilot harness

**Goal:** implement only enough infrastructure to validate the evaluation concept.

Preferred strategy:
- reuse an existing sandbox/harness,
- avoid custom orchestration unless required,
- preserve complete agent trajectories,
- make scoring reproducible.

Candidate foundations:
- SWE-ReX,
- Harbor/Terminal-Bench task format,
- SWE-smith-derived repo environments.

Gate:
- repeatable execution across at least two model/agent stacks.

## Phase 4 — Small validated benchmark

**Goal:** 10–25 high-quality cases, not hundreds of weak ones.

Requirements:
- multiple repositories,
- multiple causal archetypes,
- blind human validation,
- contamination review,
- trivial-baseline suite,
- adversarial shortcut testing,
- inter-rater agreement reporting.

Gate:
- benchmark separates strong agents,
- rankings are stable enough to be meaningful,
- no dominant trivial heuristic.

## Phase 5 — External handoff / collaboration

**Goal:** put the benchmark in front of groups capable of scaling and maintaining it.

Likely audiences:
- SWE-bench / SWE-agent researchers,
- CodeClash authors,
- benchmark/evaluation teams working on production engineering,
- labs interested in agentic software engineering and causal diagnosis.

Handoff package:
- concise research pitch,
- complete RFC,
- worked cases,
- pilot results,
- explicit differentiation from prior art,
- list of open implementation questions.

## Research thesis

The benchmark should embody a simple distinction:

> **Issue-resolution benchmarks test whether an agent can solve a problem that has already been identified. This benchmark tests whether the agent can discover what the problem actually is.**

A second design thesis should constrain every scoring decision:

> **If frontier labs aggressively optimize against this benchmark, the resulting optimization pressure should improve transferable diagnostic engineering behavior.**
