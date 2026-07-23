# Hybrid Local Solver

Research repository for developing hybrid accelerated local optimization methods for large-scale graph problems.

The project studies provably efficient local solvers for PageRank-type problems by combining:

- accelerated outer frameworks (e.g., Catalyst-style acceleration);
- local evolving-set processes;
- relaxation-based local solvers such as LocSOR;
- adaptive hybrid switching strategies.

The final goal is a reproducible research artifact accompanying a submission to the **Journal of Machine Learning Research (JMLR)**.

## Repository structure

```
paper/        JMLR manuscript source
src/          Python implementation
experiments/  Reproducible experiments
results/      Generated outputs (ignored by git)
tests/        Unit tests
docs/         Mathematical conventions and research notes
```

## Development

Python environment is managed by `uv`:

```bash
uv sync
make test
make paper
```

## Reproducibility principles

Every reported experiment should record:

- graph dataset;
- teleportation parameter alpha;
- accuracy epsilon;
- random seed;
- stopping criterion;
- code version.

## Paper

The manuscript uses the official JMLR LaTeX style. The complete LaTeX source is maintained under `paper/` so that the paper can be compiled independently.
