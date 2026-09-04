# Exact twelve-leaf finite witness and zero-root audit

Date: 2026-09-04

Starting from the ten-leaf graph, add the pair

```text
{(1,37),(19,38)}.
```

The resulting graph is simple and connected, with 39 vertices, 76 unit
edges, and source `0`.

## Finite positive-root certificate

At

```text
s = 1/4096,
d_source rho = 6549/500000,
relative_width = 1/1000,
beta = 12217/25000,
```

the complete Fraction-exact canonical chronology first fails at phase 27,
product 8, vertex `28`, with empty input batch.  Its exact beta cell is

```text
[0.4886718252465223..., 0.4888994588075898...).
```

The lower endpoint is attained at phase 26, product 1, by leaf `27`; the
open upper endpoint is attained at phase 27, product 3, by row `26`.  The
normalized negative input residual is `-6.4622535274...e-11`.  This direct
positive-`alpha` cell overlaps the final finite eight-leaf relay cell, so the
finite construction covers continuously through every beta strictly below
`0.4888994588075898...`.

## Audited zero-root limit

At the same source threshold, the Fraction-exact scaled `s=0` trace has cell

```text
[0.4886720900294752..., 0.48889876186669784...).
```

It has the same failure tuple and empty batch.  Its failure is robust after
normalization by the failure-phase width:

```text
-0.0025719893827... < 0.
```

Product 3, row `26`, gives the open upper endpoint; product 7, row `25`, is
strictly larger by `0.0001867688753...`.

A source-threshold retiming on the same graph,

```text
d_source rho = 26191/2000000,
beta = 4889/10000,
```

has the exactly audited limiting cell

```text
[0.4887692904770463...,0.48898613288770115...).
```

It overlaps both the original twelve-leaf cell and the next paired-leaf
relay.  The failure tuple and every equality class are unchanged, while the
normalized negative residual remains `-0.0023936328511...`.  Solving the
fixed-branch product-3/product-7 equioscillation gives the exact (large)
rational source threshold

```text
0.013095460978126071...
```

and limiting endpoint `0.48898749344945247...`.  This optimum is useful as a
branch audit, but the displayed small rational is retained as the robust
machine-readable relay.

The complete comparison audit finds 44 grouped closure/inherited equality
events, involving 22 forced coordinates per event type.  The only other
equalities are structural maximum ties:

```text
leaves {33,37}:     product 1 of phases 22--23,
leaves {27,31,35}: product 1 of phases 24--27.
```

Each listed group consists of twin leaves with the same unique neighbor, so
permuting the tied vertices is a source-preserving graph automorphism.  The
algorithm uses only their common maximum value, and the tie cannot change
the state.  There are no other maximum ties, stop ties, zero exterior-input
tests, zero closure tests, or zero pre-push residuals.  Representative exact
strict margins are

```text
active nonzero input residual     1.2713490735...e-6
pre-push residual                 5.5862814044...e-6
maximum-to-next-distinct gap      1.1719250947...e-7
stop-decision gap                 7.9099705248...e-6
```

Consequently the usual finite-prefix continuity lift is rigorous for every
fixed beta in the interior of the limiting cell.  Here the stronger endpoint
nevertheless comes from the explicit finite-root witness above.  The upper
endpoint is excluded, and no claim reaches `1/2`.

Machine-readable verifiers:

```text
stopped_masked_input_residual_beta_04890_twelve_leaf_exact.py
stopped_masked_input_residual_beta_04890_twelve_leaf_zero_root_limit_audit_exact.py
stopped_masked_input_residual_beta_04899_twelve_leaf_zero_root_retimed_exact.py
```
