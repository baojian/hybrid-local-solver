# Manuscript workspace

This directory contains the active arXiv theory paper, *Accelerated Local
Algorithms for Personalized and Regularized PageRank*, and preserves the independent research
notes and archives that led to it.

## Active manuscript

The files at the root of `manuscript/` form the active paper:

```text
manuscript/
├── main.tex
├── appendix.tex
├── references.bib
├── sections/
├── tex/
│   └── shared/
│       ├── preamble.tex
│       ├── math_commands.tex
│       ├── research_commands.tex
│       ├── research_note_preamble.tex
│       ├── source_aligned_problem.tex
│       ├── notation.tex
│       ├── NOTATION.md
│       └── writing_commands.tex
└── dist/                  # generated PDF and arXiv source archive
```

`main.tex` contains document structure only. Shared package configuration and
notation live under `tex/shared/`. The active command set preserves the
author's recurring NeurIPS 2024 and 2025 writing conventions without importing
archived scientific claims or the unrelated machine-learning boilerplate in
those older command files:

- `math_commands.tex` defines the canonical `\v...` vector, `\m...` matrix,
  `\g...` calligraphic, and `\s...` blackboard-bold families, together with
  common graph operators and helpers such as `\mc`, `\norm`, and `\grad`, plus
  semantic accuracy macros such as `\epsappr`, `\epsobj`, and `\epsppr`;
- `source_aligned_problem.tex` is the one reusable graph, PageRank, RPPR,
  work-unit, and tolerance-namespace definition imported by the paper and all
  notes;
- `research_commands.tex` owns algorithm names and claim-status labels, while
  `research_note_preamble.tex` gives every standalone note the same shell;
- `notation.tex` is the registry of reserved and proof-scoped scientific
  symbols, written as includable LaTeX (`\input{tex/shared/notation}`);
  `NOTATION.md` records the layering and maintenance rules and points to it;
- `writing_commands.tex` contains figure-panel labels, reference wrappers,
  drafting colors, checkmarks, and pseudocode assignment symbols;
- `preamble.tex` owns package loading and theorem-environment setup.

The active paper presents both randomized and deterministic solutions of the
algorithmic OP2 running-time target in `notes/problem_definitions/`:

- deterministic regularization continuation, a two-metric accelerated proof,
  cumulative kinetic-volume charging, and a deterministic sparse reporter;
- randomized support-safe threshold batching, block-Cholesky/Chebyshev depth,
  and residual-certified nearly-linear SDD calls;
- a separate bounded-arithmetic point-source implementation with explicit
  encoding costs;
- semantic PPR and ACL residual guarantees, an optional set-only PPR handoff,
  and explicit multi-source input-cost extensions;
- source-checked comparisons, full proofs, and an AI-assistance disclosure.

The randomized proof comes from `notes/active_edge_lcp/`. The two
`deterministic_op2*_20260905` notes contain the development and independent
audit of the deterministic proof. `evolving_support_cg` is relevant context,
not the source of a complete randomized OP2 theorem. The active paper builds
without importing any of those archives. Earlier APPR, ISTA, and CF-Push
section files remain as supporting material but are not input by this paper.

Add reusable notation to these shared files rather than defining commands
inside individual sections. Structural tests enforce that boundary and prevent
the source-aligned problem from being redeclared. Archived macro files remain
read-only references and are never input by the active manuscript.

Build the active paper from the repository root with:

```bash
make paper
make -C manuscript arxiv
```

The second command writes `dist/arxiv-source.tar.gz` and
`dist/accelerated-local-rppr.pdf`. The archive contains only the active
transitive TeX dependencies, bibliography, generated `.bbl`, and a small
build README. See [`ARXIV_REVIEW.md`](ARXIV_REVIEW.md) for the proof/source
audit, baseline repository issues, independent-build check, and visual QA.
The 9 September revision makes both OP1 and OP2 prominent and expands the
source comparisons beyond the two closest 2026 papers. See
`ARXIV_REVIEW.md` and `../docs/literature/publication-review-20260909.md`.
The author can submit the archive; no external submission has been performed.

Project-wide mathematical definitions and research decisions belong in
`docs/`. Keep the active manuscript consistent with those documents, the
implementation, and the tests.

## Standalone research notes

Publication-oriented but not-yet-integrated derivations live under
`manuscript/notes/`. These notes may use a scoped normalization while a
repository-wide mathematical decision remains open, and they must label source
results, proved statements, conditional statements, empirical observations,
and open conjectures separately.

[`notes/registry.toml`](notes/registry.toml) is the exhaustive machine-readable
inventory and [`notes/README.md`](notes/README.md) is the concise status index.
Every note has `main.tex`, `README.md`, `STATUS.md`, and a shared-rule
`Makefile`; large notes keep ordered proof units under `sections/body/`. All
registered notes can be built together with:

```bash
make notes
```

Each note imports the shared source-aligned model, then states only its
stronger assumptions and proof-scoped quantities. This shares mathematical
language without adopting a repository-wide PageRank residual or stopping
rule.

The AESP--LOCSOR synthesis is in:

```text
manuscript/notes/hybrid_aesp_locsor/
```

Build it independently with:

```bash
make -C manuscript/notes/hybrid_aesp_locsor
```

It is deliberately not input by `manuscript/main.tex`. Migrate material into
the active paper only after reconciling it with the residual convention,
existing CF-Push analysis, implementation, and tests.

The AESP--LocGD center-star lower bound is in:

```text
manuscript/notes/aesp_locgd_star_lower_bound/
```

Build it independently with:

```bash
make -C manuscript/notes/aesp_locgd_star_lower_bound
```

This note proves an unconditional
`Omega(1 / (sqrt(alpha) * epsilon))` active-volume lower bound for the literal
AESP-PPR outer loop with batched LocGD on a center-seeded star. It also records
the failed residual-cone route, the exact algorithmic scope, and the
`Omega(min(m, 1 / epsilon) / sqrt(alpha))` graph-budget refinement. It is not
a lower bound for arbitrary AESP inner maps or all hybrid local methods.

The volume-gated acceleration note is in:

```text
manuscript/notes/volume_gated_acceleration/
```

Build it independently with:

```bash
make -C manuscript/notes/volume_gated_acceleration
```

This note proves a graph-uniform `1 / rho` peak-volume invariant for an
RPPR-based safe support gate, derives exact spider-prefix conditioning, gives
a path counterexample to restart-on-every-expansion, and proves an amortized
restricted re-solving lemma. The final
`O_tilde(1 / (rho * sqrt(alpha)))` work bound remains conditional on a
one-sided expanding-subspace continuation lemma or an equivalent
newly-admitted-volume charge. The note is not input by the active manuscript.

## Imported source workspaces

Exact external LaTeX sources used to prepare agent-oriented reader editions
live locally under the Git-ignored `imports/` directory. Each workspace pins
an explicit source version, retains the downloaded archive and per-file
hashes, and separates immutable `source/extracted/` evidence from an editable
`reader/` copy. Do not commit imported archives, extracted sources, builds, or
page renders.

Use a provenance-pinned workflow to fetch, audit, compile, render, and migrate
imported sources. Do not copy their claims into the active manuscript without
following the repository-level literature and mathematical-convention
requirements.

## Archived manuscripts

Complete previous-paper projects live under `manuscript/archive/`:

- [`archive/arxiv-2026-classical-acceleration-rppr/`](archive/arxiv-2026-classical-acceleration-rppr/)
  contains the source-faithful arXiv v2 reader edition of *Complexity of
  Classical Acceleration for \(\ell_1\)-Regularized PageRank*.
- [`archive/colt-2023-accelerated-sparse-appr/`](archive/colt-2023-accelerated-sparse-appr/)
  contains the source-faithful arXiv v1 / COLT 2023 reader archive of
  *Accelerated and Sparse Algorithms for Approximate Personalized PageRank and
  Beyond*.
- [`archive/kdd-2023-appr-sor/`](archive/kdd-2023-appr-sor/) contains the
  standalone KDD 2023 APPR-SOR paper.
- [`archive/neurips-2024-locch/`](archive/neurips-2024-locch/) contains the
  standalone NeurIPS 2024 LocCH paper and reviewer response.
- [`archive/neurips-2025-aesp/`](archive/neurips-2025-aesp/) contains the
  standalone NeurIPS 2025 AESP paper and author response.

Archived projects are historical, read-only references. They are not included
in the root `make paper` or `make reproduce` targets. Before inspecting,
building, or explicitly changing an archive, read its own `README.md` and
`AGENTS.md`; preserve its internal structure and use its documented build
commands.

Do not automatically copy archived prose, claims, bibliography entries,
macros, or experimental results into the active manuscript. Verify any reused
material against the current project documentation and cited sources.
