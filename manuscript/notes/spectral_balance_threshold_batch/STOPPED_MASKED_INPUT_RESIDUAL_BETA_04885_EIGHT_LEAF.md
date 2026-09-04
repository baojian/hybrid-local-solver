# Exact eight-leaf relay and zero-root lift

Date: 2026-09-04

Starting from the six-leaf graph, add the pair

```text
{(1,33),(23,34)}.
```

The resulting graph has 35 vertices and 72 unit edges and remains simple and
connected with source `0`.

## Finite positive-root relay

Fix `s=1/4096` and `relative_width=1/1000`.  Three Fraction-exact source
thresholds give a finite relay:

| `d_source rho` | representative `beta` | exact chronology cell (decimal rendering) |
|---|---:|---|
| `1363/100000` | `0.4882` | `[0.48806839433893695...,0.4884019576618608...)` |
| `109/8000` | `0.4884` | `[0.48824932214123595...,0.4885632177154518...)` |
| `13621/1000000` | `0.4885` | `[0.4883929965053578...,0.48868006133662073...)` |

The cells overlap sequentially, and the first overlaps the robust six-leaf
finite cell.  Every row first fails at phase 26, product 8, vertex `28`, with
empty input batch.  Their normalized residuals are respectively
`-7.5895...e-11`, `-6.6028...e-11`, and `-5.8194...e-11`.  Thus this is a
fully finite positive-`alpha` relay, not a limiting computation.

## Audited zero-root limit

The same topology has a three-row exact zero-root relay:

| `d_source rho` | representative `beta` | exact limiting cell (decimal rendering) |
|---|---:|---|
| `1363/100000` | `0.4882` | `[0.4880686430540822...,0.4884011060182894...)` |
| `109/8000` | `0.4884` | `[0.48824956947231757...,0.4885623702605307...)` |
| `544839/40000000` | `0.4885` | `[0.4883941377364695...,0.488691166865773...)` |

These cells also overlap sequentially, and the first overlaps the six-leaf
limit.  All have the same failure tuple and empty batch.  Their normalized
limiting residuals are at most `-0.00237`.  The first two upper endpoints are
product 3, row `26`.  In the optimized last row, product 7, row `25`, is the
open endpoint and product 3 is strictly larger by `1.8269944258...e-8`.

The full comparison audit finds 44 grouped closure/inherited events from 11
closure groups, involving 17 coordinates per event type.  Each group is
certified by diagonal cancellation, absence of same-or-later pushed
neighbors, stationary scaled load, and the next-phase velocity reset.  The
only additional equalities are three maximum ties between twin leaves `27`
and `31` at product 1 of phases 23 through 25.  Both have neighbor set `{4}`,
so the equality is forced by a source-preserving graph automorphism for every
retained root.

There is no other maximum tie, stop tie, zero exterior-input test, zero
closure test, or zero pre-push residual.  In particular,

```text
minimum maximum-to-next gap        1.7689292366...e-8
minimum stop-decision gap          1.0586226353...e-4
```

are exactly positive.  The twin tie changes no state: only the scalar maximum
value enters the stop rule.

Therefore, for every fixed beta strictly between the first lower endpoint and
the combined upper endpoint, one relay row gives a strict limiting chronology
and all sufficiently small positive retained roots yield either an earlier
active input failure or the same strict phase-26 failure.  As before,
`s=s(beta)` and hence `alpha` may depend on beta.  The combined upper endpoint
`0.488691166865773...` is excluded, and no claim reaches `1/2`.

Machine-readable verifiers:

```text
stopped_masked_input_residual_beta_04882_eight_leaf_exact.py
stopped_masked_input_residual_beta_04885_eight_leaf_zero_root_limit_audit_exact.py
```
