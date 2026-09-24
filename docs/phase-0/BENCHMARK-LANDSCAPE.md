# Benchmark Landscape

This document maps the closest evaluation efforts to the proposed benchmark and defines the gap the project should occupy.

| Project | Starting information | Primary target | Produces repair? | Trajectory central? | Main gap relative to this project |
|---|---|---|---:|---:|---|
| SWE-bench | Explicit GitHub issue + repo | Resolve stated issue | Yes | No | Problem is substantially specified before diagnosis begins |
| SWE-Doctor | Explicit issue + repo | Reproduce, diagnose, patch | Yes | Partly | Diagnosis is grounded, but the target behavior is still issue-described |
| Fault-localization benchmarks | Bug report / failure context | Rank faulty files/lines | Usually no | No | Localization is not full causal diagnosis or repair verification |
| OpenRCA | Query + telemetry | Identify root-cause elements | Usually no | Limited | AIOps/telemetry RCA rather than repository-scale causal debugging |
| RCAEval | Microservice telemetry | Failure diagnosis | Usually no | Limited | Focused on microservices/AIOps telemetry |
| Edge Delta RootCauseBench | Incident telemetry + change context | Identify culprit commit | Remediation label | No | Commit attribution rather than discovering source-level causal mechanism and validating repair |
| APEX-SWE Observability | Production-like symptom + logs/dashboard/chat + repo | Diagnose and remediate | Yes | Some qualitative analysis | Closest overlap; does not make diagnostic trajectory, competing hypotheses, and counterfactual root-cause verification the benchmark's central scoring object |
| CodeClash | High-level goal | Self-directed iterative software improvement | Yes | Yes | Goal-oriented building/optimization rather than causal fault diagnosis |
| SWE-smith | Synthetic/reconstructed SWE tasks | Generate training/eval tasks | N/A | N/A | Infrastructure opportunity, not direct conceptual overlap |
| SWE-ReX | Sandboxed runtime | Execute agent work | N/A | N/A | Infrastructure opportunity, not direct conceptual overlap |

## Gap statement

The benchmark should occupy the space between issue-resolution benchmarks and observability/RCA benchmarks.

The task is not:

- "Fix the bug described in this issue."
- "Which file contains the fault?"
- "Which deployment caused the incident?"
- "Given telemetry, identify the failing service."
- "Improve this system toward a high-level goal."

The task is:

> **Here is a weak, downstream observation from a complex software system. Determine what is actually wrong, prove why, repair the causal defect, and show that the repair generalizes beyond the original manifestation.**

## Why APEX-SWE does not make this redundant

APEX-SWE Observability is the strongest prior-art challenge to novelty and should be treated as a design constraint rather than ignored.

Its key strengths:
- production-style debugging rather than explicit failing tests,
- telemetry and unstructured operational context,
- real repository grounding,
- patch-based remediation,
- evidence that epistemic discipline correlates with success.

The proposed benchmark must go further in dimensions that APEX-SWE does not make primary leaderboard objects:

### 1. Prompt ambiguity is intentional and graded

A case should be rejected if the prompt localizes the relevant subsystem too strongly.

### 2. Competing hypotheses are part of case design

Every accepted case should document multiple initially plausible causal vectors and the evidence that discriminates between them.

### 3. Investigation quality is scored

The benchmark should record whether the agent:
- formed reasonable hypotheses,
- gathered discriminating evidence,
- revised beliefs after contrary evidence,
- reproduced the failure,
- avoided unsupported certainty,
- and minimized destructive or irrelevant actions.

### 4. Causal explanations are testable

The agent should submit a machine-readable diagnosis connecting:
- observed symptom,
- causal mechanism,
- relevant state transition or interaction,
- evidence,
- and expected effect of the intervention.

### 5. Counterfactual variants test understanding

The evaluator should alter conditions while preserving the root cause. A valid causal repair should continue to work.

### 6. Diagnosis and intervention are separable metrics

A model can:
- diagnose correctly but patch incorrectly,
- patch successfully by luck without correct diagnosis,
- or partially mitigate the symptom without removing the cause.

The benchmark should preserve these distinctions.

## Evaluation axes to carry into Phase 1

At minimum, Phase 1 should specify separate metrics for:

1. root-cause identification,
2. causal-chain correctness,
3. failure reproduction,
4. hypothesis quality,
5. information gain / diagnostic efficiency,
6. evidence grounding,
7. belief revision,
8. intervention minimality,
9. functional repair correctness,
10. counterfactual robustness,
11. regression avoidance,
12. scope discipline,
13. appropriate abstention/escalation,
14. cost, time, and tool-use efficiency.

## Design hazards identified in recon

### Synthetic-puzzle smell
Hand-written bugs can leak the intended answer through unnatural implementation choices.

### Hidden-information masquerading as difficulty
A case is invalid if no reasonable engineer could determine the cause from available evidence.

### Single-path diagnosis
If one command or one log line reveals the answer, the case measures retrieval rather than causal investigation.

### Grader overfitting
A single visible symptom encourages patches that suppress the manifestation without fixing the cause.

### Trajectory gaming
A model could emit polished hypotheses after finding the answer. Scoring should rely on timestamped actions/evidence, not only a post-hoc narrative.

### Cost bias
Models with huge token/tool budgets may brute-force the repository. Efficiency metrics should exist, but must not dominate causal correctness.

### Data contamination
Cases derived directly from public incidents risk memorized fixes. Transformations and held-out/private or newly constructed cases will be needed for serious leaderboard use.

### Harness confounding
Model comparisons become noisy if each system receives a different tool environment. The canonical benchmark should define a standard harness profile while allowing secondary bring-your-own-agent tracks.
