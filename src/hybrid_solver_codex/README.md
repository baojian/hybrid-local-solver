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

`response_hybrid.py` is the exact algebraic reference for the response--
iterative roadmap. It maintains a dense principal inverse on a settled anchor,
uses warm-started CG on the anchor Schur complement for a light frontier, and
absorbs the frontier when degree volume grows geometrically. The backend
probes every new frontier once before a rebuild, allowing an easy heavy batch
to certify without being factorized. Its diagnostic frontier-lift operation
also realizes the exact old-face response and verifies that arbitrary nested
Schur-frontier errors are mutually energy-orthogonal. Its normalized lift
constructs an energy-orthonormal basis for each frontier, allowing the
append-only multi-event response-sketch identities in the accompanying note
to be checked directly. The tests also verify the two-sided group estimator
and its exact transposed harmonic measurement identity. The backend
materializes the full matrix and records global boundary reads and dense
arithmetic explicitly. It validates bordered updates and switching invariants;
it is not the sought output-sensitive SDD implementation.

`tests/test_response_theory_identities.py` is the numerical theorem harness
for the response track. It checks the grounded-Laplacian and Schur congruence,
source leverage as exact Schur-diagonal loss, invariance under
degree-preserving exterior rewiring, the transposed fixed-anchor harmonic
sketch, and the two-ledger square-root response bound. These are dense
small-graph identities and do not constitute a complexity experiment.

Claude agents may read, run, benchmark, and review this implementation, but
must not modify files in this directory.
