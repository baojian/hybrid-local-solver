# Acceleration versus Locality in Regularized PageRank

This directory contains a standalone LaTeX research note reconstructed from
the hybrid-local-solver discussions through August 2026.  It is deliberately
separate from the active manuscript.

The note records the complete proof history rather than only the final
conclusion:

- the accelerated-warmup plus monotone-local-tail proposal;
- the over-regularization handoff and local tail bound;
- the matched generalized-Bregman activation tax and its exact obstruction;
- order-safe Euclidean proximal centers;
- the cumulative active-volume/deactivation-flux identity;
- the proposed flux conjecture and the rooted-tree stress test that invalidates
  it as a usable graph-uniform locality hypothesis;
- a rigorous product lower bound for persistent-support one-hop methods; and
- the remaining safeguarded/restarted research directions.

Every central statement is tagged as a source result, a proved statement, a
conditional theorem, a computational observation, a refuted route, or an open
problem.  The RPPR residual and accuracy quantities are note-scoped because
the repository-wide residual convention is still open.

Build independently with:

```bash
make -C manuscript/notes/hybrid_local_solver_complete_note
```

The generated PDF is intentionally ignored and the note is not input by
`manuscript/main.tex`.

