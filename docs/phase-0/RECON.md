# Phase 0 Reconnaissance

Status: complete enough to enter specification design, with one naming decision still open.

## Mission

Determine whether the proposed benchmark measures a genuinely under-covered capability, identify the closest prior work, define the benchmark's non-negotiable differentiators, and establish a concrete path to a research-grade RFC without prematurely building expensive infrastructure.

## Core research question

Can an AI engineering agent infer the true causal defect in a large software system from an ambiguous, downstream, and potentially misleading symptom, then reproduce the failure, perform discriminating investigation, implement a minimal repair, and verify that the repair resolves the underlying cause rather than merely suppressing the observed symptom?

The benchmark should test **problem discovery before problem solving**.

## Primary finding

The proposed capability is not equivalent to existing issue-resolution, fault-localization, observability, or telemetry RCA benchmarks.

The nearest work covers important pieces of the problem:

- SWE-bench starts from an explicit GitHub issue and asks for a patch.
- SWE-Doctor emphasizes reproduction and runtime-grounded diagnosis, but still begins from an issue report that states the target behavior.
- fault-localization work measures where the bug is, often using issue context, rather than whether the agent can infer the hidden causal chain from a weak symptom.
- OpenRCA and RCAEval focus on root-cause analysis from production telemetry.
- Edge Delta's RootCauseBench asks which recent commit caused a production incident from telemetry and change context.
- APEX-SWE Observability asks agents to diagnose and remediate production failures using logs, dashboards, chat context, and source code.
- CodeClash removes task-level instructions and evaluates goal-oriented software engineering, but does not center causal debugging from an under-specified symptom.

The proposed benchmark's distinct axis is:

> **Ambiguous symptom -> competing hypotheses -> evidence gathering -> causal diagnosis -> reproduction -> minimal intervention -> counterfactual verification.**

## Critical naming collision

An active public project already exists at:

- https://github.com/edgedelta/root-cause-bench

It is also named **RootCauseBench** and was created for AI root-cause analysis of production incidents. The overlap is close enough to create citation, search, and identity confusion even though the proposed benchmark differs materially in scope.

Recommendation: resolve the public name before Phase 1 is finalized. Keep this repository as the working location for now, but treat `RootCauseBench` as a working title.

A preliminary exact-name search found no obvious collision for **CausalDebugBench**. This is not trademark or legal clearance, only a project-name reconnaissance result.

## Non-negotiable differentiators

A qualifying benchmark design should satisfy all of the following:

1. **Symptom-first prompt**
   - The agent receives an observed behavior, not a localized bug report.
   - The prompt should not identify the responsible file, subsystem, function, or causal mechanism.

2. **Genuine diagnostic ambiguity**
   - At least several competing hypotheses must be reasonable at the start.
   - Difficulty must come from causal ambiguity, not missing information or artificial obscurity.

3. **Downstream or misleading symptom**
   - The observed failure should often occur away from the causal defect.
   - Correlation with a subsystem should not automatically imply causal origin.

4. **Full-system investigation**
   - The agent can inspect the repository and ordinary engineering evidence.
   - Depending on the case: logs, traces, metrics, configuration, tests, git history, runtime instrumentation, tickets, or maintenance notes.

5. **Trajectory matters**
   - Evaluation must preserve the agent's diagnostic actions.
   - A lucky patch and a disciplined causal investigation should not be considered equivalent.

6. **Reproduction before confidence**
   - Strong credit requires demonstrating the failure mechanism or producing evidence that discriminates among plausible causes.

7. **Minimal intervention**
   - Patches that broadly rewrite a system until tests pass should be penalized.
   - The benchmark should reward repairs proportional to the demonstrated root cause.

8. **Counterfactual verification**
   - Hidden variants should alter timing, workload, topology, inputs, concurrency, or another causal parameter.
   - Symptom-specific hacks should fail these variants; cause-level repairs should survive.

9. **Epistemic discipline**
   - The agent should distinguish observed facts, hypotheses, and confidence.
   - Unsupported certainty should be penalized.

10. **Useful benchmaxxing**
    - The benchmark should be designed so that optimizing models against it improves transferable engineering diagnosis rather than only benchmark-specific pattern matching.

## Important overlap: APEX-SWE Observability

APEX-SWE is the closest major benchmark discovered during Phase 0.

Its Observability tasks already:
- omit failing unit tests from the prompt,
- expose production-style telemetry,
- require tracing a failure through a codebase,
- require a patch,
- and reward epistemic discipline.

The proposed benchmark therefore should not claim novelty merely from "debugging production-like failures without a failing test."

The stronger novelty target is:

- **deliberately weak or edge-case symptom reports,**
- **multiple intentionally preserved causal hypotheses,**
- **scored diagnostic trajectories,**
- **explicit hypothesis-discrimination behavior,**
- **root-cause explanations tied to evidence,**
- **hidden counterfactual variants,**
- **and separation of causal diagnosis quality from final patch correctness.**

## Candidate task archetypes

The specification should support several archetypes rather than one repeated bug shape:

- delayed-onset state corruption,
- stale cache or connection state,
- race conditions with misleading surface failures,
- resource lifetime bugs,
- authentication/authorization state drift,
- retry/fallback interactions,
- configuration and code interaction,
- cross-service causal defects,
- performance degradation caused by an apparently unrelated subsystem,
- test or monitoring artifacts that incorrectly suggest a cause,
- interacting individually-reasonable components whose combination creates failure,
- partial fixes that reduce symptom frequency but leave the root cause intact.

## Case-construction principle

Prefer transformed real incidents over hand-authored "puzzle bugs."

A strong case should:
1. begin from a real or realistic causal failure,
2. preserve the causal structure,
3. neutralize memorization cues,
4. preserve several defensible initial hypotheses,
5. expose only evidence an engineer could realistically obtain,
6. include a known reproducible causal chain,
7. include a known minimal repair,
8. include hidden counterfactual variants.

## Human validation concept

A case should not enter the benchmark solely because its author believes it is difficult.

Candidate acceptance should include blinded diagnosis by multiple experienced engineers.

A useful target pattern:
- reviewers disagree on the initial hypothesis,
- reviewers can eventually converge using available evidence,
- the root cause is reproducible,
- the case is not solved by a trivial grep or one obvious log line,
- and the reference repair survives counterfactual evaluation.

## Infrastructure implication

Do not build a bespoke agent runtime in the first implementation.

Existing infrastructure can plausibly cover much of execution:
- SWE-ReX for sandboxed shell environments,
- SWE-smith for repository/task environment construction,
- Harbor / Terminal-Bench style task packaging,
- or a thin custom layer over a standard coding-agent harness.

The intellectual contribution should be the **task protocol, case admissibility standard, trajectory schema, causal scoring, and counterfactual evaluation**, not a new shell wrapper.

## Phase 0 exit criteria

Phase 0 is considered complete when:

- [x] Existing repo inspected.
- [x] Closest benchmark families identified.
- [x] Major naming collision identified.
- [x] Distinguishing capability stated.
- [x] Initial case-admission principles stated.
- [x] Initial evaluation dimensions stated.
- [x] Reuse-vs-build infrastructure direction identified.
- [ ] Public benchmark name chosen.
- [ ] Phase 1 normative specification drafted.

## Primary references

- SWE-bench: https://github.com/SWE-bench/SWE-bench
- SWE-smith: https://github.com/SWE-bench/SWE-smith
- SWE-ReX: https://github.com/SWE-agent/SWE-ReX
- CodeClash: https://github.com/CodeClash-ai/CodeClash
- OpenRCA: https://github.com/microsoft/OpenRCA
- RCAEval: https://github.com/phamquiluan/RCAEval
- Existing RootCauseBench: https://github.com/edgedelta/root-cause-bench
- APEX-SWE: https://arxiv.org/abs/2601.08806
- SWE-Doctor: https://github.com/SWE-Doctor/SWE-Doctor
- LinuxFLBench: https://github.com/FudanSELab/LinuxFLBench
