# Reference scoring implementation

This directory contains a deliberately small reference implementation of the **MakorBench v0.1 draft score aggregation**.

It does **not** grade causal semantics. It assumes the component/subcomponent rubric in `SCORING.md` has already produced numeric scores.

Its purpose is to make the aggregate arithmetic and ceiling behavior unambiguous.

Run:

```bash
python -m unittest tests.test_reference_scoring
```

The reference implementation is not yet a stable public API.
