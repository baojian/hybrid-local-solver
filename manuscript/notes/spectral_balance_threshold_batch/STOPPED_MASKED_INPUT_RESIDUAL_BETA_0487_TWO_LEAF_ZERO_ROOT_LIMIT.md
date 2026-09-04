# Exact two-leaf zero-root limit and continuity lift

Date: 2026-09-04

This note audits the removable `s -> 0` limit on the 29-vertex, 66-edge
two-leaf graph

```text
BETA_04865_BRANCH_BOUNDARY_EDGES + {(4,27),(15,28)}.
```

The source is vertex `0`, all edges are unit weight, and the graph is simple
and connected.  Fix

```text
d_source rho = 14701198001/1000000000000,
relative_width = 1/1000.
```

At `beta=487/1000`, the Fraction-exact scaled limit trace has chronology cell

```text
[0.48618996153896166..., 0.4870260368530394...).
```

The first failure is phase 24, product 8, at the new leaf `28`.  The input
batch is empty, the active face is

```text
{0,...,19,22,23,24,25,26,27,28},
```

and the scaled active input residual is

```text
-6.8973748801...e-6 < 0.
```

The open upper endpoint is attained at product 7 by row `25`.  Product 3,
row `26`, is strictly larger by `2.2683023148...e-11`; the exact verifier
checks this sign as a rational inequality.

## Complete equality audit

There is no maximum-row tie, stop tie, zero exterior-input test, zero
closure-admission test, or zero pre-push residual.  The smallest strict
margins, shown as decimals only for readability, are

```text
active nonzero input residual     4.3359304618...e-7
exterior input test               4.0416699650...e-5
raw nonzero velocity              4.2056537958...e-5
non-tied lower-clamp gap          4.2056537958...e-5
pre-push residual                 6.3193526369...e-6
closure test                      1.6248352047...e-5
post-closure active residual      6.6192302612...e-6
unique-maximum gap                6.9243677549...e-8
stop-decision gap                 2.6036853039...e-5
```

The exact tracer returns 36 grouped equality events.  They are four copies
of the following nine groups, containing 16 coordinates in total:

| event | vertices |
|---|---|
| post phase 3 | `27` |
| post phase 4 | `5,8,14` |
| post phase 5 | `7,15,24` |
| post phase 6 | `11` |
| post phase 7 | `9` |
| post phase 9 | `10,28` |
| post phase 14 | `19,22,23` |
| post phase 16 | `26` |
| post phase 19 | `25` |

For each group the four event types are: a post-closure zero residual, the
same coordinate's active-input zero at product 1 of the next phase, its zero
raw velocity, and the resulting tie between the stored lower value and the
following iterate in the lower clamp.  Thus there are `16` coordinate
occurrences of each type, or `64` scalar equalities.

Every post-closure zero is structurally forced.  Its diagonal closure push
cancels its own residual, and no vertex pushed in the same or a later closure
batch is its neighbor.  At the next phase the limiting load is stationary
and velocity has reset to zero, which forces the three inherited equalities.
The verifier checks the exact closure batches, missing-neighbor condition,
and complete equality-event list; there is no unclassified tie.

## Continuity lift

Fix a threshold strictly inside the limiting cell:

```text
0.48618996153896166... < beta < 0.4870260368530394....
```

Then this zero-root trace lifts to a counterexample for all sufficiently
small positive retained roots `s`.  The proof is a finite induction through
the 31 attempted products.  All exterior admissions, positive-residual
pushes, closure batches, maximum rows, and stop decisions are strict at
`s=0`, so these choices persist by continuity.

At a structurally forced active-input zero, a negative perturbation already
gives an earlier counterexample.  Otherwise the coordinate remains on the
same active face.  The raw-velocity positive part and lower clamp are
continuous even when their two arguments tie.  Consequently either failure
occurs earlier, or the positive-root states converge through phase 24,
product 8 to the limiting state.  In the second case the strict scaled
failure margin above preserves the negative residual at leaf `28`.

The required small positive value `s=s(beta)` depends on the fixed threshold,
and hence so may

```text
alpha = s(beta)^2/(2-s(beta)^2).
```

This is not a single positive `alpha` witness for the whole interval.  The
upper endpoint is also excluded: the lifting argument needs strict distance
from the limiting stop boundary.

The independently verified finite positive-root two-leaf cell already ends
at `0.4870256869778903...`.  The audited limit family supplies only the
additional open sliver up to `0.4870260368530394...`, while making the
fixed-topology asymptotic mechanism rigorous.

Run the machine-readable audit with

```bash
uv run python \
  manuscript/notes/spectral_balance_threshold_batch/stopped_masked_input_residual_beta_0487_two_leaf_zero_root_limit_audit_exact.py
```
