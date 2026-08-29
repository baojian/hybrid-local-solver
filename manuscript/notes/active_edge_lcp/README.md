# active_edge_lcp

This standalone note develops the obstacle/LCP route to OP2 in the canonical
RPPR normalization.  It proves that exact negative-slack pivots from zero are
nested, coordinatewise increasing, and support-safe for the PageRank
Stieltjes matrix.  It also proves the supplied-support CG bound and a local
minimum-norm KKT objective certificate.

The numerical sign interface is now margin-free.  If an approximate solve on
a reachable face has residual norm `delta`, a boundary key below
`-delta/alpha` is provably negative for the exact face.  If no key crosses that
known threshold and the residual is reduced to the explicit objective-derived
target in Theorem `thm:threshold-dichotomy`, orthant projection already meets
`eps_obj`.  The primitive never needs to resolve every arbitrarily small
complementarity sign.

An overlapping-threshold corollary makes this robust to certified numerical
intervals of a predetermined width.  Exact face changes also obey a global
energy/slack-motion telescope bounded by `alpha`; this is useful potential,
but it does not pay for explicit updates caused by a dense correction.

The end-to-end theorem is deliberately conditional.  The missing result is a
margin-free active-edge continuation primitive that amortizes changing-face
linear algebra and complete known-threshold boundary reporting within
`O_tilde(vol(S*) sqrt(kappa(Q)))`, including discovery, repeated scans,
updates, state traffic, materialization, certification, and output.  Terminal
support volume alone is insufficient: exact path faces can be every nested
prefix, giving quadratic cumulative scan volume.

On promised endpoint-seeded paths, that changing-face issue is closed in the
exact-real model: an append-only scalar `LDL^T` recurrence tests the next
boundary in constant arithmetic per admitted vertex and materializes the
answer once, for total `O(vol(S*))` work.  This structural theorem shows why
the repeated-prefix example is a warning about state reuse rather than a path
lower bound.

The projected-CG route has an exact four-vertex obstruction.  Starting from
an exact old face, ordinary CG stays feasible and energy-decreasing but
overshoots one optimum coordinate at iteration three.  Orthant projection is
inactive, so projected CG follows the same trajectory.  Run the rational
audit with:

```bash
python3 verify_counterexample.py
python3 verify_threshold_dichotomy.py
python3 verify_path_ldl.py
```

The checked outputs are stored beside the scripts.  Build the note with:

```bash
make
```

The full primary-source map is `docs/literature/lcp-solvers.md`.
