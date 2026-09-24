# MakorBench Task Bundle Contract

**Status:** Phase 1 normative companion to `SPEC.md`  
**Schema dialect:** JSON Schema Draft 2020-12

This document defines the minimum separation between agent-visible task material and benchmark-private oracle material.

## 1. Design goal

A MakorBench implementation should be portable across execution harnesses without changing the causal task.

The benchmark therefore separates:

1. **task semantics** — prompt, environment snapshot, evidence surfaces, resource policy;
2. **agent scaffold** — how a model interacts with the environment;
3. **private evaluation state** — oracle diagnosis, counterfactual variants, graders, reference interventions.

The scaffold may vary by track. The semantic task and private oracle must remain fixed for a comparable run.

## 2. Recommended bundle layout

```text
tasks/<task-id>/
├── task.json                  # public manifest; validates against task-manifest.schema.json
├── prompt.md                  # only initial symptom/report supplied at run start
├── environment/               # build recipe or immutable environment reference
│   ├── README.md
│   └── ...
├── fixtures/                  # agent-visible local evidence, when required
│   └── ...
└── private/                   # MUST NOT enter the agent-visible environment
    ├── oracle.json            # validates against oracle.schema.json
    ├── graders/
    ├── counterfactuals/
    ├── regression-tests/
    ├── authoring-record.md
    └── human-validation/
```

A concrete implementation MAY package the same logical objects differently, but MUST preserve the visibility boundary.

## 3. Public manifest

`task.json` MUST validate against `schemas/task-manifest.schema.json`.

The manifest pins:

- task ID;
- benchmark version;
- prompt path;
- repository/source snapshot;
- execution image digest;
- resource budget;
- network policy;
- track;
- architecture/seed where relevant.

A stable release MUST NOT rely only on mutable container tags, moving branches, or floating package versions.

## 4. Initial prompt

`prompt.md` is the only natural-language problem statement automatically presented at task start.

It MUST:

- state an observed symptom in operator/user language;
- avoid naming the causal subsystem unless that would realistically be known;
- avoid giving a failing test name whose semantic content localizes the defect;
- avoid reference-fix language;
- avoid benchmark-author commentary about intended difficulty.

Additional information may become available only through normal agent investigation of the environment.

## 5. Private oracle

`private/oracle.json` MUST validate against `schemas/oracle.schema.json`.

It records at least:

- oracle causal mechanism;
- causal roles;
- material causal chain;
- accepted reproduction/evidence routes;
- accepted intervention classes;
- plausible alternative hypotheses;
- counterfactual variants;
- provenance;
- known shortcuts.

The oracle is benchmark-maintainer material. It MUST NOT be mounted into the agent environment, included in model context, or exposed through public dev artifacts for hidden leaderboard cases.

## 6. Counterfactual boundary

Counterfactual variants belong to the **private verifier**, not the interactive task environment.

A variant should preserve the same causal mechanism while modifying incidental conditions. Examples include:

- randomized process IDs;
- different request ordering;
- shifted timing windows;
- changed concurrency;
- alternate but equivalent topology;
- different cache warmness;
- different dataset values;
- different resource ceilings within the causal regime.

The reference intervention MUST pass every release counterfactual.

## 7. Run outputs

A canonical run produces at least:

```text
runs/<run-id>/
├── patch.diff                 # or explicit no-change marker
├── diagnosis.json             # diagnosis.schema.json
├── verification.json          # verification.schema.json
├── trajectory.jsonl           # harness-defined observable event log
├── run-metadata.json          # model/scaffold/harness/resource information
└── grader-results.json        # generated after private evaluation
```

Private oracle data MUST NOT be copied into public run artifacts for hidden cases.

## 8. Trajectory boundary

`trajectory.jsonl` records observable interaction events such as:

- assistant/user-visible agent messages;
- tool calls;
- shell commands;
- environment outputs;
- file edits;
- test invocations;
- structured hypothesis checkpoints when the scaffold supports them.

MakorBench does **not** require, collect, or grade hidden chain-of-thought. Evaluation must be possible from observable actions, explicit artifacts, and resulting environment state.

## 9. Comparable-run invariant

Two results are directly comparable only when they share:

- benchmark release;
- task version;
- track;
- semantic environment snapshot;
- verifier version;
- canonical scaffold profile, when reported on the Canonical leaderboard.

Bring-your-own-agent results may use different scaffolds but must be reported separately.

## 10. Schema evolution

All machine-readable artifacts carry a schema version.

Backward-incompatible changes require:

- a new schema version;
- release notes;
- migration guidance where practical;
- no silent reinterpretation of historical leaderboard artifacts.
