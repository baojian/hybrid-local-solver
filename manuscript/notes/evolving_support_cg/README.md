# evolving_support_cg

This standalone note studies whether conjugate gradients can be represented
as a locally evolving set process for the shared symmetric PageRank system.
It proves finite graph propagation and a trajectory-dependent edge-work bound
for exact ordinary CG, gives a three-coordinate obstruction to thresholding a
live CG direction, and proves the boundary and monotonicity properties of
exact principal-subsystem solves for the PageRank M-matrix.

The endpoint path now gives an exact calibration of the promising baseline.
For the endpoint seed on unweighted `P_n`, with ambient path degrees,
`alpha_n = n^(-2)`, and `eps_ppr = 1/10`, ordinary exact CG from zero has a
positive singleton residual at the next frontier after every `k < n` steps,
but its live direction is nonzero on the full visited prefix. The actual
degree-normalized residual certificate first holds at `K = n`. Consequently,
a literal implementation that repeatedly scans the genuinely supported rows
uses `Theta(n^2) = Theta(nu_n / sqrt(alpha_n))` work, where
`nu_n = vol(P_n)`. The theorem includes all eleven resource coordinates. It
is specific to this exact-CG trajectory and explicit sparse realization; it
does not lower-bound arbitrary supported polynomials, implicit/rational
response routes, prefetching adaptivity, or finite-precision implementations.

The accompanying implementation compares two designs. Exact frontier-sparse
CG is promising and is algebraically identical to ordinary CG. Restarting a
principal-system solve after every one-hop boundary expansion is correct but
is empirically refuted as a standalone strategy on paths and long spiders due
to repeated-prefix work. A factor-two geometric-envelope variant now gives a
proved logarithmic restart bound and geometrically amortized revisit work in
terms of the terminal explored volume. A high-degree decoy theorem now proves
that this terminal volume is unbounded as a function of `alpha` and
`eps_ppr`: one nonviolating halo vertex can have arbitrary degree. In
contrast, for a point seed and exact principal-subsystem solves, exact
violation-only expansion has terminal volume at most
`d_source + (1 + alpha) / (2 * alpha * eps_ppr)`. This closes that restart
tradeoff rigorously. Any geometric implementation needs a hard
volume/degree guard and a certifying fallback.

Build from this directory with:

```bash
make
```

Reproduce the synthetic exploration with:

```bash
uv run python -m experiments.explore_evolving_cg
uv run python -m experiments.explore_geometric_envelope_obstruction
```
