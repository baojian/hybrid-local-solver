# Stopped masked input residual: an exact delayed-path beta cell

Date: 2026-09-04

This is an unregistered companion result.  It modifies the 24-vertex
two-fifths witness by one two-edge pendant path and certifies a complete
half-open interval of stopping thresholds.  It does not update any shared
integration or controller-owned summary.

## Verdict

**Proved here.**  The canonical zero-start `one-push-maximal` chronology
violates `MaskedInputResidual` for every fixed stopping threshold in the exact
execution-tree cell

```text
0.4175772135237306... <= beta < 0.4356241290316428....
```

In particular, `beta=87/200=0.435` is refuted.  The first negative active
input residual is reached after a predecessor-width ratio

```text
0.4485767345201572... > 87/200.
```

Therefore the failing product is executed.  This result is a finite exact
counterexample, not yet a family approaching `1/2`.

## Exact graph and parameters

Use vertices `0,...,25` and source `0`.  Start with the 24-vertex graph in
`STOPPED_MASKED_INPUT_RESIDUAL_TWO_FIFTHS_COUNTEREXAMPLE.md`, then attach the
two-edge pendant path

```text
2--24--25.
```

Equivalently, the complete 46-edge set is

```text
E = {
  (0,1), (0,12), (1,2), (1,6), (1,11), (2,3), (2,4),
  (2,5), (2,8), (2,10), (2,11), (2,24), (3,4), (3,5),
  (4,5), (4,6), (4,8), (5,6), (5,9), (6,7), (7,8),
  (8,9), (8,10), (9,10), (10,11), (12,13), (13,14),
  (13,17), (13,18), (14,15), (15,16), (15,17), (15,20),
  (16,17), (16,20), (17,18), (18,19), (18,20), (18,22),
  (18,23), (19,20), (20,21), (20,23), (21,22), (22,23),
  (24,25)
}.
```

This graph is finite, simple, connected, undirected, unit-weight, and has
source degree two.  Take

```text
s = 1/224,
alpha = s^2/(2-s^2) = 1/100351,
d_source rho = 173/8000,
rho = 173/16000,
relative terminal width = 1/1000.
```

Run the exact pre-gradient input-frontier admission, one simultaneous active
diagonal push, maximal append-and-immediate-push closure, and the fixed-beta
width stop from the prescribed zero lower state.

## Exact failure

At one-based outer phase 16, product 7 is about to run after 21 completed
products.  The input batch is empty, the failure row is the already active
vertex `16`, and the active face is

```text
{0,1,2,...,18,24,25}.
```

In random-walk degree coordinates,

```text
xi_16 / phase_old_width
  = -3.6861938539586764...e-8 < 0,

preceding_inner_width / phase_old_width
  = 0.4485767345201572... > 87/200.
```

Positive diagonal similarity preserves the negative sign in symmetric
normalized coordinates.

The two new path rows act as a genuine delayed clock.  During the failure
phase the maximum residual ratios are

```text
product:  1          2          3          4          5          6
ratio:    .4485396   .4411513   .4356241   .4443590   .4511357   .4485767
max row:  7          7          9          25         25         25
```

Thus the old clock branch carries products 1--3 and the fresh endpoint
`25` carries products 4--6.  This is the desired clock/failure separation on
one finite canonical graph, although it covers only a bounded beta interval.

## Why this proves an interval, not only one beta

The exact tracer intersects every strict continuation comparison and every
weak stopping comparison along the run.  For this execution its cell is

```text
[beta_lower,beta_upper)
 = [0.4175772135237306..., 0.4356241290316428...).
```

The lower endpoint is the phase-15 first-product stopping ratio and is
included because stopping uses `inner_width <= beta old_width`.  The upper
endpoint is the phase-16 product-3 continuation ratio and is excluded because
that product continues only for strict `beta` below the ratio.  Every
admission, push, clamp, stop, and continuation decision is therefore
identical throughout the half-open cell.  The same phase-16 product-7 strict
negative residual is reached for every beta in it.

## Exact verification

Run:

```bash
uv run python manuscript/notes/spectral_balance_threshold_batch/\
stopped_masked_input_residual_delayed_path_counterexample_exact.py
```

The wrapper validates the graph and uses `fractions.Fraction` for every state,
branch comparison, residual sign, ratio, and beta-cell endpoint.  It asserts
that the tracer's exact cell equals the interval obtained from the phase-15
and phase-16 decisive products; decimal values above are display-only.

## Honest boundary

This two-edge path rigorously shows how a fresh delayed row can take over the
maximum-width clock immediately before a remote failure.  It closes no
universal family: its cell ends at `0.435624...`.  A separate exact witness
currently reaches a higher cell, while the remaining route to refuting every
fixed `beta<1/2` still requires either chained synchronized releases or a
parametric construction whose decisive continuation ratios tend to `1/2`.
