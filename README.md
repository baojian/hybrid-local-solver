# Hybrid Local Solver

`hybrid-local-solver` is a research codebase for developing and evaluating
accelerated local solvers for large-scale graph optimization problems. The
initial focus is local PageRank: obtaining an accurate solution near a seed
set while avoiding work over the entire graph whenever locality permits.

The project is in an early research stage. Algorithmic definitions, complexity
claims, and experimental conclusions should be treated as work in progress
until they are documented, tested, and reflected in the accompanying paper.

## Research direction

The central goal is to understand when acceleration and local iterative
updates can be combined without losing the computational advantages of
locality. The project studies connections among:

- **Catalyst acceleration**, as an outer acceleration framework for iterative
  optimization methods;
- **AESP**, as a reference point for accelerated local graph solving;
- **LocSOR**, which uses localized successive over-relaxation updates;
- **local PageRank**, as the primary graph problem and a setting in which work
  can be measured through local iterations and edge operations.

The intended hybrid method will investigate switching or coupling rules
between accelerated outer iterations and efficient local inner solves.
Relevant questions include convergence, preservation of locality, practical
stopping criteria, and dependence on the teleportation parameter
`alpha` and target accuracy `epsilon`.

## Publication targets

This repository supports venue-neutral manuscript development, with possible
submissions to the *Journal of Machine Learning Research* (JMLR) and the
*International Conference on Machine Learning* (ICML). Shared manuscript
sources live in [`manuscript/`](manuscript/), while complete previous-paper
projects are preserved separately under `manuscript/archive/`. Venue-specific
formatting can be isolated in the manuscript workspace as submission targets
are prepared. Mathematical conventions and evolving research decisions are
recorded in [`docs/`](docs/).

## Repository structure

| Path | Purpose |
| --- | --- |
| [`src/`](src/) | Reusable graph loading, solver implementations, and shared baselines. |
| [`experiments/`](experiments/) | Runnable experiment and parameter-sweep entry points built on `src/`. |
| [`results/`](results/) | Structured experiment records and provenance; transient raw runs remain ignored. |
| [`tests/`](tests/) | Automated checks for graph loading, solver interfaces, and experiment entry points. |
| [`docs/`](docs/) | Authoritative research context, mathematical conventions, decisions, and literature notes. |
| [`manuscript/`](manuscript/) | Active LaTeX paper sources plus read-only archives of previous paper projects. |
| [`papers/`](papers/) | Source PDFs managed with Git LFS; annotations belong in `docs/literature/`. |

Keep reusable computational logic in `src/`; experiment scripts should
orchestrate that logic, and tests should verify its stable interfaces. When
research definitions change, keep `docs/`, the implementation, tests, and
manuscript consistent.

## Reproducibility

Every reported experiment should record:

- graph dataset;
- teleportation parameter `alpha`;
- target accuracy `epsilon`;
- random seed;
- stopping criterion;
- solver parameters;
- Git commit hash;
- dirty-worktree status.

Complexity comparisons should report outer acceleration iterations, local
inner iterations, and edge operations. Figures must be generated
programmatically from experiment outputs and must not be edited manually.
Residual definitions, normalization, and stopping criteria must remain
consistent across theory, implementation, and experiments.

See [`docs/research_protocol.md`](docs/research_protocol.md) and
[`docs/mathematical-conventions.md`](docs/mathematical-conventions.md) for the
project-wide protocol and conventions.

## Research context and paper library

Start with [`docs/research-context.md`](docs/research-context.md) for the
current problem statement, intended contributions, open definitions, and
documentation map. Curated notes and page-level pointers live in
[`docs/literature/`](docs/literature/).

Source PDFs may be added to [`papers/`](papers/), which is configured for Git
LFS. See [`papers/README.md`](papers/README.md) before adding a paper; adding an
unannotated collection of PDFs is intentionally discouraged.

## Development setup

The project requires Python 3.14 and uses
[`uv`](https://docs.astral.sh/uv/) for dependency management:

```bash
uv sync
```

Run the standard checks with:

```bash
make test
make lint
```

Build the manuscript with:

```bash
make paper
```

Run the complete reproducibility workflow with:

```bash
make reproduce
```

This default workflow is offline-friendly: it runs the automated checks, a
deterministic synthetic APPR theorem smoke test, figure generation, and the
manuscript build. The smoke result is written under `results/raw/` with its Git
commit and dirty-worktree status.

The real-graph parameter sweeps may download datasets and run for a long time,
so they are kept behind an explicit command:

```bash
make full-experiments
```

See [`experiments/README.md`](experiments/README.md) for the individual sweep
commands and their structured outputs.
