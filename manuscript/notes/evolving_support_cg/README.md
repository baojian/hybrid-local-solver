# evolving_support_cg

This standalone note studies whether conjugate gradients can be represented
as a locally evolving set process for the shared symmetric PageRank system.
It proves finite graph propagation and a trajectory-dependent edge-work bound
for exact ordinary CG, gives a three-coordinate obstruction to thresholding a
live CG direction, and proves the boundary and monotonicity properties of
exact principal-subsystem solves for the PageRank M-matrix.

The accompanying implementation compares two designs. Exact frontier-sparse
CG is promising and is algebraically identical to ordinary CG. Restarting a
principal-system solve after every one-hop boundary expansion is correct but
is empirically refuted as a standalone strategy on paths and long spiders due
to repeated-prefix work. A factor-two geometric-envelope variant now gives a
proved logarithmic restart bound and geometrically amortized revisit work in
terms of the terminal explored volume. A high-degree decoy theorem now proves
that this terminal volume is unbounded as a function of `alpha` and
`eps_ppr`: one nonviolating halo vertex can have arbitrary degree. In
contrast, exact violation-only expansion has terminal volume at most
`d_source + (1 + alpha) / (2 * alpha * eps_ppr)`. This closes the proof
program as a rigorous tradeoff. Any geometric implementation needs a hard
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
