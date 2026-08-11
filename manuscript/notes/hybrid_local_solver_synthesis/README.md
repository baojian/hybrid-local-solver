# Hybrid local solver: full rigorous synthesis

This directory contains a standalone, modular LaTeX synthesis of the research
conversation about locally evolving set methods, AESP, the proposed
AESP-to-LocSOR hybrid, the corrected SOR analysis, the connection to the 2026
`l1`-regularized PageRank paper, the experimental program, and the
Terminal-Bench Science task design.

It complements the narrower proof note in
`manuscript/notes/hybrid_aesp_locsor/`. It is deliberately **not included in
`manuscript/main.tex` by default**. The repository-wide PageRank residual
convention remains open, and several of the strongest end-to-end complexity
statements remain conditional. The note therefore labels every claim as
source-derived, proved in the note, conditional, empirical, or open. Sections
can be migrated into the active manuscript after the corresponding conventions
and proof obligations are resolved.

Build with:

```bash
make -C manuscript/notes/hybrid_local_solver_synthesis
```

The main source is `hybrid_local_solver_synthesis.tex`; individual sections are
under `sections/` to facilitate selective incorporation into the active paper.
