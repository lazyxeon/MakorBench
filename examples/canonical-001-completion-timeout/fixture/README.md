# Case 001 executable development fixture

This is the public executable fixture for `makor-dev-001-completion-timeout`.

It is intentionally a **development case**, not a hidden leaderboard case. The paper oracle is public elsewhere in this repository.

## Run

From the repository root:

```bash
# Agent-visible smoke test
python -m unittest discover \
  -s examples/canonical-001-completion-timeout/fixture/tests \
  -p "test_*.py"

# Maintainer verifier/counterfactual tests
python -m unittest discover \
  -s examples/canonical-001-completion-timeout/private/tests \
  -p "test_*.py"
```

Generate a sample incident evidence bundle:

```bash
python examples/canonical-001-completion-timeout/fixture/generate_evidence.py
```

## Design

The fixture simulates:

- scheduler leases and timeout state;
- periodic artifact reconciliation;
- worker artifact + billing side effects;
- rotating worker service credentials;
- pooled long-lived completion channels;
- authenticated completion delivery;
- deterministic telemetry.

The pre-fix implementation intentionally contains the Case 001 causal defect described by the public oracle.

The reference solution and oracle/counterfactual tests live under the case-level `private/` tree and MUST NOT be mounted into an evaluated agent environment.

A future hidden descendant must also transform this public case rather than reuse its published causal mechanism verbatim.
