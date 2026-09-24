# MakorBench Schemas

The Phase 1 specification uses **JSON Schema Draft 2020-12** for machine-readable contracts.

- `task-manifest.schema.json` — public task/run manifest
- `oracle.schema.json` — private benchmark-maintainer ground truth
- `diagnosis.schema.json` — agent's final causal diagnosis
- `verification.schema.json` — agent's final verification report
- `trajectory-event.schema.json` — canonical observable event envelope
- `score-report.schema.json` — canonical per-run score report

These schemas are v0.1 research-draft contracts and may change before MakorBench 1.0.

The specification deliberately separates the private oracle from agent-visible artifacts to prevent accidental answer leakage and to support hidden counterfactual verification.

Issue #3 extends the v0.1 contract with trajectory evidence references and optional causal claim units for auditable semantic scoring.
