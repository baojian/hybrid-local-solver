# Research Notes

## Hybrid Local Solver

Working hypotheses, proof ideas, and experimental observations should be recorded here.

Important topics:

- Catalyst acceleration;
- AESP;
- LocSOR;
- hybrid switching rules;
- complexity bounds.

## 2026-08-12: rigorous AESP--LOCSOR synthesis

Recorded as a standalone note in
`manuscript/notes/hybrid_aesp_locsor/`. The note reconstructs the project
conversation in a common PageRank normalization and separates source results,
new proofs, conditional statements, empirical observations, corrections, and
open claims.

Closed statements:

- after any finite valid AESP handoff, local SOR with fixed
  `0 < omega < 2` terminates under the final degree-normalized gradient
  certificate;
- with the proof-safe tail `omega = 1`, an objective-gap handoff
  `f(x_J)-f* <= alpha^(3/2) * eps / (1+alpha)` gives tail work
  `O(1/(sqrt(alpha) * eps))`;
- the weighted-gradient-mass handoff
  `||D^(1/2) grad f(x_J)||_1 = O(alpha^(3/2))` gives the same tail order and
  bounds every tail active-set volume;
- the complete hybrid has a trajectory-dependent bound
  `O~(Lambda_J/sqrt(alpha)) + O(1/(sqrt(alpha) * eps))`.

Corrections and open item:

- the universal signed weighted-`l1` monotone SOR range is
  `0 < omega < 1+alpha`, not all of `(0,2)`; objective descent still holds on
  `(0,2)`;
- the graph-uniform target total work follows if the early AESP locality
  factor satisfies `Lambda_J = O(1/eps)`;
- that early-locality statement is not proved for every graph. The note gives
  a support-envelope lemma and an explicit no-percolation condition under
  which it does hold, and explains why the 2026 RPPR/FISTA support results do
  not transfer automatically to unregularized AESP.

The note is intentionally not input by the active manuscript while the
repository-wide residual convention remains open.

### Publication gate

Keep `manuscript/notes/hybrid_aesp_locsor/` as a rigorous standalone research
note; do not promote its graph-uniform end-to-end complexity claim into the
active paper until one of the following is established:

1. the central early-AESP locality lemma
   \[
   \Lambda_J
   := \max_{1\leq t\leq J}
      \frac{\overline{\operatorname{vol}}(S_t)}{\gamma_t}
   = O(1/\epsilon),
   \]
   with a graph-independent hidden constant; or
2. a correct weaker structural condition or alternative burn-in work argument
   that is sufficient for the paper's stated theorem.

Until this gate is closed, paper-facing statements may use the proved
trajectory-dependent theorem and explicitly conditional confinement
corollaries, but must continue to label the universal
`O~(1/(sqrt(alpha) * epsilon))` work bound as open.

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
- The lower-bound checker enforces the theorem regime
  `0 < eps_appr <= 1/16`; out-of-regime values are rejected rather than
  reported as theorem checks. The figure generator validates the complete
  `(alpha, eps_appr, ordering)` grid before plotting actual or scaled work.
- The relation between `eps_appr` and the RPPR sparsity parameter `rho` is
  deliberately not asserted. Both bound support volume, and settling it is a
  prerequisite for a fair APPR-versus-RPPR work comparison.
