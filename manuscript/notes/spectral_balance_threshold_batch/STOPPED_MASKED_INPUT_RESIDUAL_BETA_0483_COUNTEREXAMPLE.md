# Exact stopped-input-cone counterexample at beta 0.483

Date: 2026-09-04

This unregistered note freezes a canonical point-source, zero-start,
one-push-maximal counterexample for `beta=483/1000`.  It is a finite exact
certificate, not the still-missing parametric construction up to `1/2`.

The graph is the 62-edge beta-0.482 retimed graph with the single additional
edge `(8,11)`.  It is simple, connected, undirected, unit weighted, has 27
vertices, and uses

```text
s = 1/224,
alpha = 1/100351,
rho_scale = 633/40000,
relative_width = 1/1000.
```

The exact execution first fails at phase 23, product 8, vertex 15, after 29
completed products.  The input admission batch is empty and the active face
is `0,...,18,24,25,26`.  The normalized masked input residual is strictly
negative:

```text
xi_15 / W = -3.3837831899378006...e-8.
```

Its full same-chronology beta cell is

```text
[0.47865117954737074..., 0.4830073888985141...).
```

The lower endpoint is attained at phase 22, product 1.  The upper endpoint is
attained at failure-phase product 3 by clock vertex 26.  Failure-phase products
4--7 switch the maximum to clock vertex 25; product 7 has ratio
`0.48310614849913197...`, so product 3 is the strict bottleneck.  This exposes
the local retiming target: raise the product-3 row until it meets product 7.

Run the exact certificate with

```bash
uv run python \
  manuscript/notes/spectral_balance_threshold_batch/stopped_masked_input_residual_beta_0483_counterexample_exact.py
```
