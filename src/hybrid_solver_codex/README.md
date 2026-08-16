# Codex Solver

This package contains the hybrid local solver implementation developed by
Codex agents.

`evolving_cg.py` contains two research prototypes for the conjugate-direction
locality program:

- frontier-sparse ordinary CG, which preserves the exact recurrence while
  scanning only the graph support of each direction;
- restarted evolving-set CG, which runs CG on a fixed principal system,
  expands the set from a verifier-owned boundary residual, and restarts after
  every support change.

Both prototypes use a note-scoped degree-normalized PPR residual certificate.
They are not yet repository-wide baselines, and no graph-uniform local-work
claim is attached to them.

Claude agents may read, run, benchmark, and review this implementation, but
must not modify files in this directory.
