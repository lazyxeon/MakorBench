# MakorBench Specification

**Version:** 0.1-draft  
**Status:** Phase 1 normative RFC  
**Repository name:** pending rename from `RootCauseBench` to `MakorBench`

> **Makor** (מָקוֹר) means *source* or *origin*. MakorBench evaluates whether an AI engineering agent can move from an observed symptom to the source of failure.

---

## 1. Purpose

MakorBench evaluates **causal software diagnosis**.

A MakorBench task begins with an observed symptom that is incomplete, downstream, and compatible with multiple plausible causes. The agent must investigate a realistic software system, determine the causal defect, reproduce or otherwise establish the failure mechanism, implement a proportionate repair, and verify that the repair resolves the underlying cause rather than only the original manifestation.

The canonical task flow is:

```text
observed symptom
    ↓
competing hypotheses
    ↓
evidence gathering
    ↓
hypothesis discrimination
    ↓
failure reproduction / causal confirmation
    ↓
root-cause diagnosis
    ↓
minimal intervention
    ↓
verification
    ↓
hidden counterfactual evaluation
```

MakorBench is explicitly designed to test **problem discovery before problem solving**.

---

## 2. Design thesis

Issue-resolution benchmarks largely ask whether an agent can solve a problem after the problem has already been described.

MakorBench asks whether the agent can determine **what is actually wrong**.

The benchmark SHOULD be designed such that aggressive optimization against it improves transferable engineering behavior:

> If a model is benchmaxxed for MakorBench, it should become better at diagnosing real systems, not merely better at recognizing MakorBench artifacts.

---

## 3. Normative language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** are to be interpreted as normative requirements.

A task that violates a MUST-level case requirement is not a valid canonical MakorBench task.

---

## 4. Scope

### 4.1 In scope

MakorBench is intended to measure:

- causal debugging in realistic repositories;
- diagnosis from weak or misleading symptoms;
- hypothesis formation and revision;
- evidence-seeking behavior;
- runtime and code-level investigation;
- root-cause localization;
- failure reproduction;
- causal-chain explanation;
- proportionate repair;
- verification and regression testing;
- counterfactual robustness;
- scope discipline;
- uncertainty management;
- appropriate escalation or abstention when evidence is insufficient.

### 4.2 Out of scope

MakorBench is not primarily intended to measure:

- isolated code completion;
- implementation from a fully specified ticket;
- trivia about programming languages;
- pure static fault localization;
- telemetry-only service attribution;
- exploit development;
- open-ended product building;
- competitive programming;
- style or prose quality;
- broad repository refactoring absent a causal diagnosis task.

MakorBench MAY contain tasks involving any of those skills when they arise naturally inside a causal investigation, but they are not the benchmark's central object.

---

## 5. Terminology

### 5.1 Observed symptom

The initial externally visible behavior supplied to the agent.

Examples:

- intermittent latency;
- a stale UI state;
- a worker apparently completing while an upstream system reports timeout;
- rare duplicate processing;
- a crash that appears correlated with an unrelated deployment;
- an authorization failure that only appears after a long-lived session;
- a resource leak exposed only under a specific workload.

The observed symptom is **not** the root-cause statement.

### 5.2 Root cause

The defect, interaction, state transition, or causal mechanism whose removal prevents the target failure across the benchmark's valid counterfactual conditions.

A line of code is not necessarily a root cause. A valid diagnosis may require describing an interaction among components, configuration, state, ordering, workload, or timing.

### 5.3 Causal chain

The sequence linking the root cause to the observed symptom.

A causal chain SHOULD identify intermediate state changes or interactions when they are necessary to explain why the symptom occurs.

### 5.4 Hypothesis

A candidate causal explanation that is plausible given evidence available at a particular point in the investigation.

### 5.5 Discriminating evidence

Evidence that meaningfully changes the relative plausibility of competing hypotheses.

### 5.6 Reproduction

A controlled procedure or instrumented observation that demonstrates the target failure or a sufficiently specific causal mechanism.

### 5.7 Intervention

The code, configuration, test, or other permitted change intended to remove the root cause.

### 5.8 Counterfactual variant

A hidden evaluation condition that changes incidental properties of the case while preserving the same underlying causal defect.

### 5.9 Diagnostic trajectory

The ordered record of agent actions, evidence observations, hypothesis updates, experiments, code changes, and verification steps during a run.

---

## 6. Core task contract

Every canonical MakorBench task MUST provide the agent with:

1. a repository or software system environment;
2. an observed symptom description;
3. sufficient obtainable evidence to diagnose the root cause;
4. standard engineering tools appropriate to the environment;
5. a finite execution budget;
6. no direct disclosure of the hidden root cause.

Every canonical task MUST contain, hidden from the agent:

1. an oracle root-cause description;
2. an oracle causal chain;
3. one or more accepted reproduction strategies or equivalent causal evidence criteria;
4. an oracle repair or repair equivalence criteria;
5. regression tests;
6. counterfactual evaluation conditions;
7. documented plausible alternative hypotheses;
8. task-validity evidence from human review;
9. shortcut and trivial-baseline checks.

---

## 7. Initial symptom requirements

### 7.1 Symptom-first

The initial prompt MUST describe what was observed, not what the benchmark author already knows.

It MUST NOT directly identify:

- the faulty file;
- the faulty function;
- the root-cause subsystem;
- the exact causal mechanism;
- the reference fix;
- the hidden test that fails;
- the commit that introduced the defect, unless commit attribution is itself incidental evidence rather than the answer.

### 7.2 Diagnostic ambiguity

A canonical task MUST admit at least **three defensible initial causal hypotheses** under blinded human review.

These hypotheses MUST differ meaningfully in causal mechanism or responsible subsystem. Cosmetic variants of the same theory do not count.

Example of acceptable diversity:

- connection-pool state corruption;
- DNS or network retry behavior;
- token refresh / credential lifecycle;
- scheduler starvation.

Example of unacceptable diversity:

- off-by-one in function A;
- off-by-one in function B;
- off-by-one in function C.

### 7.3 Truthful ambiguity

The prompt MAY be incomplete, noisy, or based on an operator's imperfect observation.

It MUST NOT contain knowingly false factual claims solely to trick the agent.

A report such as “restarting the worker seems to help” is valid when that correlation is genuinely present, even if restart is not causally fundamental.

### 7.4 Causal distance

For medium and hard cases, the symptom SHOULD be downstream from the defect.

A benchmark dominated by failures that occur exactly at the faulty line is insufficiently diagnostic.

---

## 8. Evidence model

### 8.1 Obtainable evidence

The environment MAY expose:

- source code;
- tests;
- runtime logs;
- traces;
- metrics;
- configuration;
- build artifacts;
- dependency metadata;
- commit history;
- issue history;
- local documentation;
- profiler output;
- database snapshots;
- packet captures;
- crash dumps;
- local service APIs;
- simulated external services;
- historical maintenance or incident records.

The case author MUST document which evidence surfaces are relevant, irrelevant, or potentially misleading.

### 8.2 No omniscience

The agent SHOULD receive the same categories of evidence a competent engineer could realistically obtain in the modeled environment.

The benchmark MUST NOT make a case difficult by withholding evidence that is necessary in principle to distinguish the true cause from alternatives.

### 8.3 No answer leakage

No agent-visible artifact SHOULD state the hidden causal answer in substantially equivalent form.

If a historical commit, issue, or document contains the exact answer, the case author MUST either:

- transform or remove the leakage;
- make retrieval of the artifact an explicit and legitimate intended behavior;
- or reject the case.

### 8.4 Network access

The **Canonical Track MUST run without unrestricted public internet access**.

Rationale:

- prevents retrieval of upstream fixes or benchmark discussions;
- limits contamination shortcuts;
- improves reproducibility;
- ensures that evidence gathering occurs within the task environment.

A task MAY provide a curated local knowledge base, documentation mirror, package mirror, or incident archive when precedent retrieval is part of the intended engineering task.

A separate **Open-World Track MAY allow network access**, but results MUST NOT be mixed with Canonical Track results.

---

## 9. Agent environment

### 9.1 Canonical environment

The canonical environment SHOULD provide:

- a POSIX shell;
- repository access;
- language/toolchain dependencies required by the project;
- test runners;
- ordinary text/code search;
- process inspection;
- logging and instrumentation tools relevant to the case;
- version control;
- writable working tree.

Additional tools MAY be task-specific.

### 9.2 Standardization

Canonical leaderboard runs MUST report the **model-agent-harness combination**, not only the model name.

Agent scaffolds can materially affect performance. MakorBench MUST NOT imply that scores from materially different harnesses are model-only measurements.

### 9.3 Canonical Track

A release SHOULD define one reference harness profile for direct leaderboard comparison.

The profile MUST specify:

- shell/tool interface;
- context handling;
- timeout;
- maximum turns or interaction policy;
- network policy;
- model reasoning setting when configurable;
- filesystem permissions;
- available services;
- retry policy;
- parallelism policy.

### 9.4 Bring-Your-Own-Agent Track

MakorBench MAY support a secondary BYOA track.

BYOA results MUST report the full scaffold and MUST be separated from Canonical Track rankings.

---

## 10. Required agent deliverables

At the end of a run, the agent MUST produce:

1. a repository diff or explicit no-change decision;
2. a machine-readable diagnosis artifact;
3. a machine-readable verification artifact.

### 10.1 Diagnosis artifact

The canonical schema is conceptually:

```json
{
  "symptom_summary": "...",
  "root_cause": {
    "mechanism": "...",
    "locations": ["..."],
    "causal_chain": ["...", "..."],
    "confidence": 0.0
  },
  "reproduction": {
    "status": "reproduced | strongly_evidenced | not_reproduced",
    "procedure": ["..."],
    "observations": ["..."]
  },
  "alternatives": [
    {
      "hypothesis": "...",
      "status": "rejected | weakened | unresolved",
      "evidence": ["..."]
    }
  ],
  "intervention": {
    "summary": "...",
    "expected_causal_effect": "..."
  },
  "residual_uncertainty": ["..."],
  "adjacent_findings": ["..."]
}
```

The final machine-readable artifact does **not** replace trajectory capture. It records the final state of the agent's diagnosis.

### 10.2 Verification artifact

The agent MUST report:

- what tests or experiments it executed;
- whether the original symptom was re-tested;
- what regressions it checked;
- what causal prediction it expected the repair to satisfy;
- unresolved risks.

### 10.3 Adjacent findings

Agents MAY report genuine additional defects discovered during investigation.

The benchmark SHOULD distinguish:

- useful adjacent findings;
- irrelevant scope expansion;
- unnecessary modifications.

Discovering additional defects MUST NOT justify modifying unrelated systems without causal or safety rationale.

---

## 11. Diagnostic trajectory capture

The benchmark harness MUST preserve an ordered diagnostic trajectory sufficient for later scoring and analysis.

At minimum it MUST record:

- agent messages;
- tool invocations;
- shell commands;
- file reads and edits when technically available;
- test and experiment execution;
- outputs returned to the agent;
- timestamps or monotonic event ordering;
- token/compute usage when available;
- final artifacts.

The harness SHOULD support an optional structured event channel through which agents can declare:

- current hypotheses;
- confidence changes;
- planned discriminating tests;
- evidence interpreted as supporting or refuting a hypothesis.

However, canonical correctness MUST NOT depend on a model voluntarily producing polished chain-of-thought. The benchmark MUST be evaluable from observable actions, explicit concise diagnostic artifacts, and environment state.

---

## 12. Reproduction requirements

### 12.1 Reproduction is preferred

A successful diagnosis SHOULD include failure reproduction whenever reproduction is reasonably possible.

### 12.2 Equivalent causal evidence

Some failures are too stochastic, destructive, expensive, or environment-dependent for deterministic reproduction.

A task MAY define an alternative causal-evidence criterion, such as:

- instrumentation showing the faulty state transition;
- a deterministic unit-level extraction of the causal mechanism;
- a trace demonstrating the failure path;
- a controlled simulation;
- a statistical stress test with a predefined threshold.

### 12.3 Symptom suppression is insufficient

A change that makes the original symptom disappear but does not remove the hidden causal defect MUST NOT receive full repair credit.

---

## 13. Counterfactual evaluation

Counterfactual evaluation is a defining feature of MakorBench.

### 13.1 Requirement

Production-grade canonical tasks MUST include at least one hidden counterfactual variant. Mature tasks SHOULD include two or more.

### 13.2 Variant properties

A counterfactual variant SHOULD alter one or more incidental variables such as:

- timing;
- concurrency;
- workload;
- request ordering;
- topology;
- dataset composition;
- resource limits;
- cache state;
- process lifetime;
- input distribution;
- randomized identifiers;
- configuration values not causally fundamental to the defect.

The **root causal mechanism MUST remain invariant**.

### 13.3 Purpose

Counterfactual variants test whether the intervention removes the cause rather than overfitting the observed manifestation.

### 13.4 Hiddenness

Counterfactual variants MUST remain hidden during the run.

Authors SHOULD avoid exposing a fixed small family of obvious mutation patterns that agents could target directly.

---

## 14. Intervention requirements

### 14.1 Proportionality

A repair SHOULD be no broader than necessary to remove the demonstrated root cause and preserve intended behavior.

### 14.2 Regression safety

Canonical tasks MUST include hidden regression checks sufficient to reject common broad or destructive fixes.

### 14.3 Forbidden shortcut classes

A task grader SHOULD reject or strongly penalize interventions that:

- disable the affected feature without justification;
- suppress errors without correcting the cause;
- weaken authentication or authorization;
- skip or hard-code test outcomes;
- remove validations solely to avoid failure;
- blanket-retry indefinitely;
- change benchmark fixtures;
- alter the grader;
- bypass intended interfaces through benchmark-specific hacks.

Case-specific exceptions MAY exist when such behavior is genuinely the correct engineering repair, but the oracle MUST document why.

---

## 15. Case admissibility

A candidate task is canonical only if all required gates pass.

### 15.1 Causal ground truth

The author MUST be able to state:

- the root causal mechanism;
- the complete material causal chain;
- why plausible alternatives are not the root cause;
- the minimal valid intervention class.

### 15.2 Reproducibility

The environment MUST produce the target failure or accepted causal evidence at a rate sufficient for reliable evaluation.

### 15.3 Ambiguity validation

Blinded human reviewers MUST identify multiple reasonable initial hypotheses.

If reviewers immediately converge on the correct subsystem from the prompt alone, the task SHOULD be rejected or reworked.

### 15.4 Solvability

At least one qualified human reviewer MUST be able to diagnose the case using only agent-visible evidence and tools.

### 15.5 No hidden-information trap

If two causal hypotheses remain observationally indistinguishable under all available evidence, the task is invalid unless the accepted answer explicitly allows that uncertainty.

### 15.6 No trivial shortcut

Task authors MUST test simple baselines appropriate to the case, including where relevant:

- grep for symptom terms;
- most recently changed file;
- most recent commit;
- nearest stack-trace frame;
- first failing service;
- highest-error log component;
- broad test-run localization.

A canonical case SHOULD NOT be solvable reliably by a trivial heuristic.

### 15.7 Reference intervention

The author MUST provide at least one known valid intervention or a rigorous equivalence criterion.

### 15.8 Counterfactual validity

The oracle intervention MUST pass hidden counterfactual variants.

### 15.9 Review record

Each task MUST include a hidden case-authoring record documenting:

- source/provenance;
- causal mechanism;
- alternative hypotheses;
- expected diagnostic path(s);
- known shortcuts;
- human review results;
- transformation steps;
- contamination risk;
- grader rationale.

---

## 16. Human validation protocol

Before inclusion in a stable release, a task SHOULD be reviewed by at least three technically qualified reviewers who did not author the case.

Reviewers SHOULD independently record:

1. their initial hypotheses after reading only the prompt;
2. their investigation;
3. the evidence that changed their beliefs;
4. their final diagnosis;
5. whether the task felt fair;
6. whether any artifact leaked the answer;
7. whether the root cause was underdetermined;
8. whether the reference repair was proportionate.

A strong task typically produces:

- diverse initial hypotheses;
- eventual convergence on the same causal mechanism;
- meaningful evidence-driven belief revision.

Inter-rater results SHOULD be retained as benchmark metadata.

---

## 17. Difficulty dimensions

MakorBench SHOULD report difficulty as a vector rather than only a single label.

Candidate dimensions include:

- **causal distance** — number/complexity of intermediate steps from defect to symptom;
- **hypothesis breadth** — number and strength of plausible alternatives;
- **temporal difficulty** — delayed onset, intermittency, or long-lived state;
- **cross-component span** — number of subsystems involved;
- **observability quality** — noisiness or incompleteness of evidence;
- **interaction order** — whether the defect emerges only from component interaction;
- **reproduction difficulty** — effort required to reliably trigger the failure;
- **counterfactual diversity** — number and variety of hidden variants.

A later release MAY derive coarse labels such as easy/medium/hard from these dimensions, but the underlying vector SHOULD remain available.

---

## 18. Run protocol

A canonical run SHOULD follow this lifecycle:

1. instantiate clean environment;
2. verify task health with oracle prechecks;
3. start trajectory capture;
4. present symptom prompt;
5. allow agent investigation within the configured budget;
6. collect final repository state;
7. collect diagnosis artifact;
8. collect verification artifact;
9. run visible-state validation;
10. run hidden functional tests;
11. run hidden counterfactual tests;
12. compute scoring components;
13. archive trajectory and run metadata;
14. destroy or reset the environment.

Runs that fail because of benchmark infrastructure SHOULD be retried under the release's documented retry policy rather than silently counted as model failures.

---

## 19. Resource and budget reporting

Every canonical result MUST report, where available:

- wall-clock time;
- model tokens;
- tool calls;
- shell commands;
- number of file modifications;
- number of test/experiment executions;
- monetary cost;
- reasoning effort setting;
- maximum context size;
- agent scaffold version;
- harness version.

MakorBench SHOULD distinguish **correctness metrics** from **efficiency metrics**.

A model that reaches the correct diagnosis inefficiently should not be treated as equivalent to a model that never reaches it, but efficiency is a meaningful engineering property and should be reported.

---

## 20. Scoring interface

The normative numerical scoring model is defined separately in `SCORING.md`.

The specification requires that scoring preserve at least the following distinctions:

1. correct diagnosis + correct intervention;
2. correct diagnosis + incorrect intervention;
3. incorrect diagnosis + accidentally successful intervention;
4. symptom mitigation without root-cause removal;
5. correct root cause but weak/unsupported causal chain;
6. correct repair that fails counterfactual variants;
7. correct outcome produced by destructive scope expansion;
8. justified abstention when evidence is genuinely insufficient.

A single binary pass/fail number MUST NOT be the only canonical reported metric.

---

## 21. Contamination and memorization controls

### 21.1 Public incident risk

Cases directly copied from public bug reports or commits are contamination-prone.

Task authors SHOULD transform:

- identifiers;
- constants;
- topology;
- file structure where practical;
- symptom wording;
- timing;
- irrelevant implementation details;

while preserving the causal structure.

### 21.2 Hidden test set

A serious leaderboard SHOULD maintain a private or controlled test set.

Public dev cases SHOULD exist for harness development and research transparency.

### 21.3 Refresh policy

The benchmark SHOULD support periodic task refreshes or rolling hidden evaluation to reduce long-term saturation.

### 21.4 Provenance

Every task MUST retain private provenance metadata so maintainers can audit contamination risk.

---

## 22. Benchmark tracks

A mature release MAY expose several tracks.

### 22.1 Canonical Causal Diagnosis

- standard harness;
- no unrestricted internet;
- hidden test cases;
- fixed execution budget;
- primary research leaderboard.

### 22.2 Open-World Engineering

- network access allowed;
- precedent retrieval permitted;
- results reported separately;
- intended to test practical engineering effectiveness rather than contamination-resistant diagnosis.

### 22.3 Diagnosis-Only

- agent investigates and submits diagnosis but does not modify the repository;
- useful for isolating causal reasoning from implementation ability.

### 22.4 Intervention-Only

- agent receives an oracle-quality diagnosis and must implement/verify the repair;
- useful as a control condition.

The Diagnosis-Only and Intervention-Only tracks are particularly valuable for decomposing whether a system fails because it cannot identify the problem or cannot implement the solution.

---

## 23. Reporting requirements

A published MakorBench result MUST identify:

- benchmark release/version;
- track;
- model;
- model version/date when available;
- reasoning setting;
- agent scaffold;
- harness;
- environment version;
- number of repetitions;
- run failures/retries;
- all primary component metrics;
- aggregate metric if one is used;
- confidence intervals or uncertainty where appropriate;
- cost and wall time when available.

Leaderboard entries SHOULD link to sufficient run artifacts for independent auditing, subject to hidden-case confidentiality.

---

## 24. Versioning

MakorBench releases SHOULD use semantic benchmark versions.

Example:

- `0.x` — research preview; protocol may change;
- `1.0` — first stable methodology;
- `1.x` — backward-compatible task additions and clarifications;
- `2.0` — material methodology/scoring change.

Leaderboard scores from incompatible major versions MUST NOT be directly merged.

---

## 25. Non-goals for v0.1

The initial benchmark does not need to:

- cover every programming language;
- model every form of production observability;
- support hardware debugging;
- produce hundreds of tasks;
- establish a perfect universal engineering score;
- build a novel agent framework.

A small set of exceptionally strong cases is preferable to a large set of shallow ones.

---

## 26. Phase 1 unresolved items

The following are deliberately deferred or still open:

1. exact scoring weights and aggregate-score construction;
2. exact diagnostic event schema;
3. exact reference harness choice;
4. time/token/tool budgets;
5. minimum number of counterfactual variants for v1.0;
6. human-reviewer qualification standard;
7. whether structured hypothesis declarations are mandatory or optional;
8. how information-efficiency should be normalized across harnesses;
9. how to score genuine adjacent defect discovery;
10. how to score a correct diagnosis when the agent reasonably chooses not to patch.

These items are tracked separately so that the task contract can stabilize without prematurely locking a weak scoring scheme.

---

## 27. Relationship to adjacent benchmarks

MakorBench is complementary to, not a replacement for:

- **SWE-bench** — issue-to-patch resolution;
- **SWE-Doctor** — reproduction-grounded issue resolution;
- **APEX-SWE Observability** — production debugging using telemetry and unstructured context;
- **OpenRCA / RCAEval** — AIOps and telemetry-root-cause analysis;
- **CodeClash** — self-directed goal-oriented software development;
- **Terminal-Bench** — hard terminal-based agent work.

The intended differentiator is the combination of:

- deliberately under-specified downstream symptom;
- validated competing causal hypotheses;
- full repository-scale investigation;
- trajectory-aware evaluation;
- explicit causal-chain artifact;
- diagnosis/intervention decomposition;
- hidden counterfactual verification.

---

## 28. Minimal definition

A concise definition suitable for papers and handoff material:

> **MakorBench is a benchmark for evaluating whether autonomous software-engineering agents can diagnose the hidden causal source of an ambiguous downstream symptom, validate that diagnosis through evidence and reproduction, implement a minimal repair, and survive counterfactual tests that distinguish root-cause resolution from symptom suppression.**
