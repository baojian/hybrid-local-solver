# Hybrid local solver: full rigorous synthesis

This directory contains a standalone, modular LaTeX synthesis of the research
conversation about locally evolving set methods, AESP, the proposed
AESP-to-LocSOR hybrid, the corrected SOR analysis, the connection to the 2026
`l1`-regularized PageRank paper, the earlier project draft on local ISTA and
Catalyst, the experimental program, and the Terminal-Bench Science task
design.

It complements the narrower proof note in
`manuscript/notes/hybrid_aesp_locsor/`. It is deliberately **not included in
`manuscript/main.tex` by default**. The repository-wide PageRank residual
convention remains open, and several of the strongest end-to-end complexity
statements remain conditional. The note therefore labels every claim as
source-derived, proved in the note, parameterized, conditional, empirical, or
open. Sections can be migrated into the active manuscript after the
corresponding conventions and proof obligations are resolved.

Build with:

```bash
make -C manuscript/notes/hybrid_local_solver_synthesis
```

The main source is `main.tex`; individual sections are under `sections/` to
facilitate selective incorporation into the active paper. The entry point
loads the shared manuscript notation and problem modules from
`manuscript/tex/shared/`.

New results beyond the initial synthesis include:

- a master handoff inequality for arbitrary finite Phase-I methods;
- a graph-structure-free but `R`-parameterized
  `O(R / (alpha^(3/4) * epsilon))` AESP-plus-LocSOR bound;
- a weighted contraction and residual-to-solution certificate for
  `l1`-regularized PageRank; and
- unconditional convergence of a finite composite Catalyst burn-in followed
  by momentum-free ISTA.

The graph-uniform `O_tilde(1 / (sqrt(alpha) * epsilon))` unregularized theorem
and the graph-independent `O_tilde(1 / (rho * sqrt(alpha)))` RPPR work theorem
remain explicit open proof obligations.
