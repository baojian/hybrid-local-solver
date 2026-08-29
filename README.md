# Hybrid Local Solver

This is a numerical optimization repository.

`hybrid-local-solver` develops and evaluates accelerated local solvers for
large-scale graph optimization problems. The initial focus is local PageRank:
obtaining an accurate solution near a seed set while avoiding work over the
entire graph whenever locality permits. The canonical scope statement is
[`docs/project-scope.md`](docs/project-scope.md).

The project is in an early research stage. Algorithmic definitions, complexity
claims, and experimental conclusions should be treated as work in progress
until they are documented, tested, and reflected in the accompanying paper.

## Research direction

The central goal is to understand when acceleration, local iterative updates,
and persistent graph response can be combined without losing the computational
advantages of locality. The project studies connections among:

- **Catalyst acceleration**, as an outer acceleration framework for iterative
  optimization methods;
- **AESP**, as a reference point for accelerated local graph solving;
- **LocSOR**, which uses localized successive over-relaxation updates;
- **incremental SDD and Schur response**, which reuse restricted-system state
  instead of solving or materializing every active prefix from scratch;
- **local PageRank**, as the primary graph problem and a setting in which work
  can be measured through local iterations and edge operations.

The intended hybrid method will investigate switching or coupling rules among
accelerated iterations, efficient local updates, and persistent response state.
Relevant questions include convergence, preservation of locality, boundary
certification, practical stopping criteria, and dependence on the
teleportation parameter `alpha` and target accuracy `epsilon`. The current
family map and proof priorities are maintained in
[`docs/solver-family-roadmap.md`](docs/solver-family-roadmap.md); it explicitly
labels the response--iterative architecture as a research hypothesis rather
than a universal optimality theorem.

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
| [`experiments/`](experiments/) | Runnable experiments, parameter sweeps, and registered research-note proof audits. |
| [`results/`](results/) | Structured experiment records and provenance; transient raw runs remain ignored. |
| [`tests/`](tests/) | Automated checks for graph loading, solver interfaces, and experiment entry points. |
| [`docs/`](docs/) | Authoritative research context, mathematical conventions, decisions, and literature notes. |
| [`manuscript/`](manuscript/) | Active LaTeX paper, independently buildable research notes, shared notation, and read-only archives. |
| [`papers/`](papers/) | Source PDFs managed with Git LFS; annotations belong in `docs/literature/`. |
| [`tools/`](tools/) | Machine-checkable repository coordination and maintenance commands. |

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

Agent-family ownership, optional concurrent branch/worktree isolation,
handoffs, and default context selection are defined in
[`docs/coordination/`](docs/coordination/). Routine single-agent work uses the
current branch directly. Run `make agent-audit` to validate the active
assignment ledger and provider-owned path declarations.

## Research context and paper library

A new collaborator should begin with the
[`docs/agent-onboarding/`](docs/agent-onboarding/) package. It gives a
self-contained formal problem contract, the verified current research state,
and the contribution workflow while routing every claim back to its
authoritative source.

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
make agent-audit
make test
make lint
```

Build the manuscript with:

```bash
make paper
```

Build all standalone research notes with:

```bash
make notes
```

Audit or inspect the machine-readable research-note registry with:

```bash
make note-audit
make note-report
make note-targets
make note-graph
```

Run the representative or complete registered proof-audit suite with:

```bash
make research-audit-fast
make research-audit
```

Run the dense response--iterative reference comparison with:

```bash
make response-hybrid
```

This diagnostic validates Schur updates and switching while reporting dense
response arithmetic and global boundary reads separately; it is not a claimed
local-time implementation.

Run the complete reproducibility workflow with:

```bash
make reproduce
```

This default workflow is offline-friendly: it runs the automated checks, a
deterministic synthetic APPR theorem smoke test, figure generation, and the
manuscript build. The smoke result is written under `results/raw/` with its Git
commit and dirty-worktree status.

Normal solver and sweep execution does not retrieve graph files. Prepare a
chosen data directory explicitly, then pass that same directory to the long
real-graph sweeps:

```bash
make fetch-graphs DATA_DIR=/absolute/path/to/graphs
make full-experiments DATA_DIR=/absolute/path/to/graphs
```

See [`docs/data-acquisition.md`](docs/data-acquisition.md) and
[`experiments/README.md`](experiments/README.md) for selective retrieval,
individual sweep commands, and structured outputs.
