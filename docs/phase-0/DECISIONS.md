# Phase 0 Decision Log

## D-0001 — Specification first

**Decision:** do not begin by building a full benchmark harness.

**Rationale:** the expensive and differentiating part of this project is case quality, causal scoring, and evaluation methodology. Existing execution infrastructure can likely be reused.

**Status:** accepted.

---

## D-0002 — Trajectory is a first-class evaluation object

**Decision:** the benchmark must preserve and score diagnostic behavior, not only the final patch.

**Rationale:** two agents can produce the same successful patch through radically different processes. Root-cause competence requires evidence gathering, hypothesis discrimination, reproduction, and verification.

**Status:** accepted in principle; exact scoring remains Phase 1 work.

---

## D-0003 — Counterfactual verification is required

**Decision:** a benchmark case should include hidden evaluation variants whenever feasible.

**Rationale:** this is the main defense against symptom suppression and patch-to-the-test behavior. The root cause should remain invariant while incidental manifestations change.

**Status:** accepted in principle.

---

## D-0004 — Public name unresolved

**Decision:** treat `RootCauseBench` as a working title only.

**Rationale:** Edge Delta already maintains a public benchmark with the same name at https://github.com/edgedelta/root-cause-bench.

**Candidate:** `CausalDebugBench` is a strong preliminary alternative because it describes the intended differentiator and an initial exact-name search did not surface an obvious existing benchmark.

**Status:** open. No repository rename should occur until explicitly decided.

---

## D-0005 — APEX-SWE Observability is required prior art

**Decision:** the eventual RFC must directly compare itself with APEX-SWE Observability.

**Rationale:** APEX-SWE already evaluates production debugging without explicit failing unit tests and requires diagnosis plus remediation. Novelty claims that ignore it would be weak.

**Status:** accepted.

---

## D-0006 — Case difficulty must come from ambiguity, not deprivation

**Decision:** cases must contain enough obtainable evidence to diagnose the root cause.

**Rationale:** an impossible or underspecified mystery is not a hard engineering problem. The intended challenge is choosing and executing the right investigation among multiple plausible explanations.

**Status:** accepted.
