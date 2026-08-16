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
to repeated-prefix work. The remaining algorithmic target is a guarded
hybrid that invokes restricted CG only after a local method has discovered a
stable envelope.

Build from this directory with:

```bash
make
```

Reproduce the synthetic exploration with:

```bash
uv run python -m experiments.explore_evolving_cg
```
