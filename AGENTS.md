# Agent Instructions

This repository is a research project targeting a JMLR submission.

## Scientific invariants

1. Do not change mathematical definitions without updating documentation and tests.
2. Residual conventions, normalization, and stopping criteria must remain consistent between theory and code.
3. Every experiment must record graph, alpha, epsilon, random seed, stopping rule, and code version.
4. Never manually edit generated figures.

## Required checks

Before finishing code changes:

```bash
make test
make lint
```

Before changing reported experimental results:

```bash
make reproduce
```
