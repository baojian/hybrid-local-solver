# Input-frontier-only NAG: an exact canonical zero-start obstruction

Date: 2026-09-04

This is an unregistered companion result.  It concerns the weakened retained-
prox chronology that uses pre-gradient input-residual frontier admission and
the certified lower retraction, but omits both the once-per-product active
residual push and the immediate diagonal pushes used during exterior append
closure.

## Verdict

**Proved here.**  Pre-gradient input-residual admission by itself does not
preserve `MaskedInputResidual`, even on a canonical point-source trajectory
starting from zero.  There is a Fraction-exact counterexample on a 20-vertex
unit path with one chord.

This does **not** refute the current central `StoppedMaskedInputResidual`
claim, whose algorithm has all three mechanisms enabled:

```text
input-residual frontier admission
+ one active diagonal residual push per product
+ immediate diagonal pushes to exterior append closure.
```

Instead, the counterexample proves that the latter two pushes cannot be
dropped as inessential implementation details.  Any proof of the central
claim may use their extra chronological flux.

## Exact instance

Let the source be endpoint `0` and let

```text
V={0,...,19},
E={{i,i+1}: 0<=i<19} union {{14,18}},
s=1/224,
alpha=s^2/(2-s^2)=1/100351,
rho=1067/40000.
```

The graph is finite, simple, connected, undirected, unit-weight, and the seed
is the single point mass `e_0`.  Run the exact two-certificate outer loop from
zero with retained shift `sigma=alpha`, relative terminal width `1/1000`, and
the literal quarter inner stopping rule.  Within each shifted phase, run the
input-frontier-only recurrence described above.

At zero-based outer phase `18`, the fourth inner product is reached with

```text
certified face = {0,1,...,15,18}.
```

At the preceding product the exact inner-width ratio is

```text
inner_width / old_width = 0.3210703410080295... > 1/4,
```

so the fourth product must be executed.  Its masked input residual at vertex
`18` is strictly negative.  In random-walk degree coordinates,

```text
xi_18 / old_width = -2.6434071053066468...e-8 < 0.
```

The symmetric normalized-coordinate residual is multiplied by
`sqrt(d_18)=sqrt(3)`, giving the corresponding diagnostic ratio
`-4.578561036...e-8`.  A dense replay also keeps the same chronology for the
tested publication floors from `0` through `1e-10`; this floating-point
crosscheck is supplementary, not part of the exact proof.

## Why the computation is exact

The verifier works in random-walk degree coordinates, related to symmetric
coordinates by the positive diagonal map `x=D^(1/2)u`.  Coordinate signs and
all admission comparisons are therefore unchanged.  After division by the
shifted smoothness constant, the shifted operator is

```text
A = a I - delta P,
a     = (1+s^2)/2,
delta = (1-s^2)/2,
```

where `(Pu)_i` is the exact rational average over the unit neighbors of `i`.
Because `s`, `rho`, degrees, and every initial value are rational, every NAG
step, lower retraction, admission comparison, outer width update, and quarter
stopping comparison is performed by `fractions.Fraction`.  The verifier
asserts the failure phase, product, vertex, face, and the strict pre-failure
quarter inequality before printing the exact numerator and denominator.

Run:

```bash
.venv/bin/python manuscript/notes/spectral_balance_threshold_batch/input_frontier_only_zero_start_obstruction_exact.py
```

## Consequence for the proof program

The earlier arbitrary-state flux obstructions left open whether zero-start
point-source ancestry alone prevented failure.  This example closes that
question negatively for the input-frontier-only variant: canonical ancestry
is not enough.  The remaining plausible invariant must explicitly exploit
the active push and append-push terms in the full chronological decomposition.

