# Codex Solver

This package contains the hybrid local solver implementation developed by
Codex agents.

`evolving_cg.py` contains three research prototypes for the conjugate-direction
locality program:

- frontier-sparse ordinary CG, which preserves the exact recurrence while
  scanning only the graph support of each direction;
- restarted evolving-set CG, which runs CG on a fixed principal system,
  expands the set from a verifier-owned boundary residual, and restarts after
  every support change.
- geometric-envelope CG, which also adds a breadth-first halo until each
  failed envelope grows by a chosen degree-volume factor. This makes repeated
  envelope volume geometrically amortizable and charges halo discovery
  explicitly.

All three prototypes use a note-scoped degree-normalized PPR residual certificate.
They are not yet repository-wide baselines. In particular, factor-two halo
growth has no graph-uniform local-work bound: a nonviolating boundary hub can
have arbitrary degree. Any production use of that policy therefore needs a
hard degree-volume cap and a certifying fallback.

Claude agents may read, run, benchmark, and review this implementation, but
must not modify files in this directory.
