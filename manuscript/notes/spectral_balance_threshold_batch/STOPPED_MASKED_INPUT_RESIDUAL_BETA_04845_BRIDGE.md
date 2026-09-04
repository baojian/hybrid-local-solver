# Exact beta-0.4845 stopped-input-cone bridge cell

Date: 2026-09-04

This unregistered note freezes a Fraction-exact bridge beyond the beta-0.484
small-root cell.  Starting from `BETA_0484_EDGES`, add `(3,6)`, and take

```text
s = 1/672,
d_source rho = 313/20000,
beta = 969/2000,
relative_width = 1/1000.
```

The resulting 27-vertex, 64-edge graph is simple, connected, undirected, and
unit weighted.  Its canonical point-source zero-start trace first fails at
phase 25, product 8, vertex 15 after 31 completed products.  The input batch
is empty, and

```text
xi_15 / W = -6.087995493483611...e-10 < 0.
```

Its exact same-chronology cell is

```text
[0.481398830294878..., 0.4845459054785884...).
```

The lower endpoint occurs at phase 24, product 1, row 9.  The upper endpoint
is failure-phase product 7, clock row 25; product 3, clock row 26, is slightly
higher at `0.4846255603238848...`.  Consequently this cell overlaps the
previous atlas endpoint `0.4841421563464968...` and extends the continuous
cover to `0.4845459054785884...`.  It does not by itself bridge to the known
beta-0.485 cell, whose lower endpoint is `0.4848047623241312...`.

Run:

```bash
uv run python \
  manuscript/notes/spectral_balance_threshold_batch/stopped_masked_input_residual_beta_04845_bridge_exact.py
```
