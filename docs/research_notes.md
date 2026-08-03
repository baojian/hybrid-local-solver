# Research Notes

## Hybrid Local Solver

Working hypotheses, proof ideas, and experimental observations should be recorded here.

Important topics:

- Catalyst acceleration;
- AESP;
- LocSOR;
- hybrid switching rules;
- complexity bounds.

## 2026-08-02: APPR worst-case work is `Theta(1/(alpha * eps))`

Recorded in `manuscript/sections/appr_lower_bound.tex`. The classical ACL
upper bound `O(1/(alpha * eps))` is worst-case tight, witnessed by the
center-seeded star `K_{1,m}` with `m = floor(1/(8 * eps_appr))`, for every
legal active-vertex ordering. This fixes the baseline that the hybrid solver
must beat and identifies the two obstructions to attack:

1. the `1/alpha` factor, from settling only an `alpha`-fraction of pushed
   residual per push;
2. the `1/eps_appr` factor, from repeatedly rescanning a
   `Theta(1/eps_appr)`-degree vertex.

Any hybrid or accelerated method claiming a better worst-case bound must break
at least one of these; a `sqrt(alpha)`-type acceleration attacks (1) only.

Implementation status and open items:

- `src/baselines/appr.py` now provides a controlled reference implementation
  with exact degree-weighted work accounting and four legal active-vertex
  orderings. `tests/test_appr_lower_bound.py` makes the star a regression test
  and cross-checks FIFO output against the Numba kernel after repairing its
  missing self-reactivation queue step. The reproducible diagnostic entry
  point is `uv run python -m experiments.check_appr_lower_bound`; it records
  graph, `alpha`, `eps_appr`, source, random seed, stopping rule, ordering, and
  code version. Its path and long-spider rows are explicitly not theorem
  checks.
- Whether a path or long spider is tight in the coupled regime
  `L = Theta(1/eps)` with `alpha * L^2 = O(1)` is left open; the star needs no
  such coupling.
- The relation between `eps_appr` and the RPPR sparsity parameter `rho` is
  deliberately not asserted. Both bound support volume, and settling it is a
  prerequisite for a fair APPR-versus-RPPR work comparison.
