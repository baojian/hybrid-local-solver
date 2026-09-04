# Exact six-leaf finite witness and zero-root lift

Date: 2026-09-04

Add three leaf pairs to the 27-vertex branch-boundary graph:

```text
{(4,27),(15,28),(2,29),(13,30),(4,31),(21,32)}.
```

The result is a connected simple unit graph with 33 vertices and 70 edges.
The source is vertex `0` and the relative target width is `1/1000`.

## Finite positive-root certificate

At

```text
s = 1/4096,
d_source rho = 6943/500000,
beta = 4881/10000,
```

the complete Fraction-exact canonical chronology fails at phase 25, product
8, vertex `28`, with empty input batch.  Its exact beta cell is

```text
[0.48729045390469944..., 0.48820216764353663...).
```

The normalized negative input residual is `-2.9403342983...e-11`.  This is a
direct positive-`alpha` certificate, not a limiting computation.

## Zero-root limit

At the same source threshold the Fraction-exact scaled `s=0` trace has cell

```text
[0.4872906952446029..., 0.4882140103628501...).
```

It has the same first failure tuple and empty batch.  The limiting residual
is robust after normalization by the failure-phase width:

```text
-0.0014375151572... < 0.
```

Product 7, row `25`, gives the open upper endpoint; product 3, row `26`, is
larger by `2.1086025566...e-6`.

## Equality classification

The zero-root trace has 40 grouped closure/inherited equalities.  They arise
from ten closure groups, containing 20 coordinates per event type.  Each
post-closure zero is certified by diagonal cancellation and absence of a
same-or-later pushed neighbor; the next phase inherits the active-input zero,
zero raw velocity, and lower-clamp tie.

There are also four maximum-row ties, at product 1 of phases 21 through 24,
between vertices `27` and `31`.  These two leaves have the identical neighbor
set `{4}`.  Swapping them is a source-preserving graph automorphism, so their
residual equality is structural for every retained root.  The maximum value
is all the algorithm uses, and its exact gap to the next distinct residual is
positive.  There are no other maximum ties, stop ties, zero exterior-input
tests, zero closure tests, or zero pre-push residuals.

The smallest exact comparison margins include

```text
active nonzero input residual     7.9350545773...e-7
pre-push residual                 1.8260779012...e-6
unique/next-distinct maximum gap  1.7143266836...e-8
stop-decision gap                 1.1401036285...e-4
```

Thus the twin-leaf maximum ties do not obstruct the finite-prefix continuity
argument.  For every fixed beta strictly inside the limiting cell, all
sufficiently small positive `s` either fail earlier at a perturbed active
zero or reach the strict phase-25 failure.  The choice `s=s(beta)`, hence
`alpha`, may depend on beta, and the upper endpoint is excluded.

Machine-readable verifiers:

```text
stopped_masked_input_residual_beta_04881_six_leaf_exact.py
stopped_masked_input_residual_beta_04882_six_leaf_zero_root_limit_audit_exact.py
```
