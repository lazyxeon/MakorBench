# MakorBench

Existing software-engineering benchmarks mostly ask whether a model can solve a known problem. This project asks whether the model can **discover what the problem actually is**.

The proposed benchmark evaluates causal software diagnosis from an ambiguous downstream symptom:

**symptom -> competing hypotheses -> evidence gathering -> reproduction -> root-cause diagnosis -> minimal repair -> counterfactual verification**

## Status

The project is currently in **Phase 0: reconnaissance and benchmark positioning**. No claim is made that a runnable benchmark exists yet.

Phase 0 artifacts:

- [Reconnaissance](docs/phase-0/RECON.md)
- [Benchmark landscape](docs/phase-0/BENCHMARK-LANDSCAPE.md)
- [Campaign plan](docs/phase-0/CAMPAIGN-PLAN.md)
- [Decision log](docs/phase-0/DECISIONS.md)

The next phase will produce a normative RFC covering task format, case-admission rules, diagnostic trajectory capture, scoring, counterfactual evaluation, and benchmark-gaming defenses.

## Thesis

Issue-resolution benchmarks test whether an agent can solve a problem that has already been identified.

This benchmark is intended to test whether an agent can determine **what is actually wrong** when the initial observation is incomplete, downstream, and compatible with multiple plausible causes.

A core design principle is that benchmark optimization should be useful:

> If frontier labs aggressively optimize against this benchmark, the resulting optimization pressure should improve transferable diagnostic engineering behavior.

## License

Apache License 2.0. See [LICENSE](LICENSE).
