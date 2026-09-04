# Exact beta-0.4865 branch-boundary cell

Date: 2026-09-04

This unregistered note freezes an exact chronology cell obtained by moving
rho just across a limiting outer-stop boundary.  Starting from the 64-edge
clock-rewire graph, replace `(1,11)` by `(1,4)` and take

```text
s = 1/4096,
d_source rho = 1891197/125000000,
beta = 304/625,
relative_width = 1/1000.
```

The 27-vertex graph remains simple, connected, undirected, and unit weighted.
Its canonical point-source zero-start trace first fails at phase 25, product
8, vertex 14, with an empty input batch and

```text
xi_14 / W = -9.506036905615688...e-11 < 0.
```

The exact same-chronology cell is

```text
[0.48639969150013823...,0.48650854880991756...).
```

It overlaps the previous endpoint `0.48646664846402143...`.  The upper
endpoint is failure-phase product 3, clock row 26; product 7 is much looser at
`0.48664161157750385...`.  Thus the active constraint is not local
product-3/product-7 equioscillation: rho is pinned just above a prior-phase
stop boundary.  At `s=0` that boundary is near `0.0151295754303`; the exact
limit cell at the chosen side renders approximately as
`[0.4863999752...,0.4865073135...)`.  These limit values are diagnostic only;
the atlas row uses the positive rational root above.

Run:

```bash
uv run python \
  manuscript/notes/spectral_balance_threshold_batch/stopped_masked_input_residual_beta_04865_branch_boundary_exact.py
```
