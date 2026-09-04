# Stopped masked input residual: an exact one-third-stop counterexample

Date: 2026-09-04

This is an unregistered companion result.  It strengthens the canonical
zero-start counterexample from the literal quarter stop to the earlier
one-third inner stop.

## Verdict

**The fixed stop `inner_width <= old_width/3` does not preserve
`MaskedInputResidual`.**  A Fraction-exact trace on a 24-vertex finite simple
connected undirected unit-weight graph reaches a strictly negative active
input residual even though the preceding width ratio is

```text
0.3732141756300159... > 1/3.
```

Thus the failing product is required by the one-third rule.  The trace starts
from the prescribed zero lower state with a single point source, resets
momentum at every outer phase, and enables pre-gradient input admission, the
once-per-product active push, and maximal append-with-immediate-push closure.

The same graph and parameters, run under the altered outer chronology caused
by `beta=2/5`, also give an exact failure; see
`STOPPED_MASKED_INPUT_RESIDUAL_TWO_FIFTHS_COUNTEREXAMPLE.md`.  For the present
one-third history, the identical strict counterexample holds for every beta
in the exact chronology cell

```text
[0.3276043827054206..., 0.37321417563001585...).
```

Outside that cell the phase endpoints change and this trace makes no claim.

## Exact instance

Let `V={0,...,23}`, source `v=0`, and

```text
E = {
  (0,1), (0,12), (1,2), (1,6), (1,11), (2,3), (2,4),
  (2,5), (2,8), (2,10), (2,11), (3,4), (3,5), (4,5),
  (4,6), (4,8), (5,6), (5,9), (6,7), (7,8), (8,9),
  (8,10), (9,10), (10,11), (12,13), (13,14), (13,17),
  (13,18), (14,15), (15,16), (15,17), (15,20), (16,17),
  (16,20), (17,18), (18,19), (18,20), (18,22), (18,23),
  (19,20), (20,21), (20,23), (21,22), (22,23)
}.
```

The source has degree two.  Take

```text
s = 1/224,
alpha = s^2/(2-s^2) = 1/100351,
d_source rho = 173/8000,
rho = 173/16000,
relative terminal width = 1/1000,
beta = 1/3.
```

At one-based outer phase 13, the seventh product in the phase is about to run.
Exactly 18 products have already completed.  No new row enters in the input
batch, and the active face is

```text
{0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18}.
```

The preceding inner width satisfies the exact strict comparison

```text
inner_width / phase_old_width
  = 0.3732141756300159... > 1/3.
```

Nevertheless, the product input at the already active vertex `16` has

```text
xi_16 / phase_old_width = -9.274461320341061...e-8 < 0.
```

The dedicated verifier prints the full exact rational values.  The coordinate
system is the random-walk degree form; positive diagonal similarity to the
symmetric normalized form preserves every sign.

## Exact verification

Every state value and every control-flow comparison is evaluated by
`fractions.Fraction`.  The publication rule is the exact strict comparison
`residual>0`, with zero neither admitted nor pushed.  The verifier asserts
the graph, rational parameters, first failure phase/product/vertex, face,
negative sign, and the strict `>1/3` predecessor inequality.

Run:

```bash
.venv/bin/python manuscript/notes/spectral_balance_threshold_batch/stopped_masked_input_residual_one_third_counterexample_exact.py
```

The wrapper calls `retained_prox_input_cone_trace_exact.py`.  That general
tracer now accepts an exact optional `stop_beta` (default `1/4`), preserving
the prior quarter-stop behavior while permitting exact audits of proposed
earlier stops.  It also computes the exact half-open beta cell on which every
recorded stop/nonstop branch is unchanged.

## Consequence

Moving the stopping constant from `1/4` to `1/3` is not enough to rescue the
chronological input-cone invariant.  A proof along this route must either use
a still earlier stop, strengthen the update or admission rule, or replace
coordinatewise input-residual nonnegativity by a different invariant.  The
separate two-fifths counterexample and a later high-beta chronology cell push
the obstruction farther upward.  Since beta changes the outer history,
these cells cannot be ordered monotonically by a single predecessor ratio.
Uncovered intervals remain; whether counterexample cells can cover them and
approach `1/2` is now decisive.
