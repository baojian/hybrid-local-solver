# Exact beta-0.486 clock-side swap cell

Date: 2026-09-04

This unregistered note freezes a degree-preserving clock-side edge swap that
extends the exact beta-cell atlas.  On the 64-edge relay graph, replace
`(5,8)` by `(4,10)` and use

```text
s = 1/4096,
d_source rho = 7569821/500000000,
beta = 243/500,
relative_width = 1/1000.
```

The resulting 27-vertex graph is simple, connected, undirected, and unit
weighted.  Its canonical point-source zero-start execution first fails at
phase 25, product 8, vertex 14 after 31 completed products, with an empty
input batch and

```text
xi_14 / W = -1.522438418805046...e-10 < 0.
```

The Fraction-exact same-chronology cell is

```text
[0.48576853645024953..., 0.486397917190983...).
```

It overlaps the previous atlas endpoint `0.48613378881118563...`.  The upper
endpoint is failure-phase product 3, clock row 26; product 7 uses row 25 and
is `0.48639792464493786...`.  Their gap is below `7.46e-9`, so this rational
rho nearly equioscillates the two bottleneck rows while the swap raises the
whole relay.

Run:

```bash
uv run python \
  manuscript/notes/spectral_balance_threshold_batch/stopped_masked_input_residual_beta_0486_clock_swap_exact.py
```
