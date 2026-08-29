# active_edge_lcp

This standalone note develops the obstacle/LCP route to OP2 in the canonical
RPPR normalization.  It proves that exact negative-slack pivots from zero are
nested, coordinatewise increasing, and support-safe for the PageRank
Stieltjes matrix.  It also proves the supplied-support CG bound and a local
minimum-norm KKT objective certificate.

The end-to-end theorem is deliberately conditional.  The missing result is a
margin-free active-edge continuation primitive that amortizes changing-face
linear algebra and complete boundary-violation reporting within
`O_tilde(vol(S*) sqrt(kappa(Q)))`, including discovery, repeated scans,
updates, state traffic, materialization, certification, and output.  Terminal
support volume alone is insufficient: exact path faces can be every nested
prefix, giving quadratic cumulative scan volume.

The projected-CG route has an exact four-vertex obstruction.  Starting from
an exact old face, ordinary CG stays feasible and energy-decreasing but
overshoots one optimum coordinate at iteration three.  Orthant projection is
inactive, so projected CG follows the same trajectory.  Run the rational
audit with:

```bash
python3 verify_counterexample.py
```

The checked output is stored in `counterexample_output.txt`.  Build the note
with:

```bash
make
```

The full primary-source map is `docs/literature/lcp-solvers.md`.
