# Exact zero-root limit and forced-zero lifting audit

Date: 2026-09-04

This note audits the removable `s -> 0` limit on the 64-edge
`BETA_04865_BRANCH_BOUNDARY_EDGES` graph.  Use the constant analytic source
threshold

```text
d_source rho = 756368559/50000000000,
relative_width = 1/1000.
```

At `beta=48657/100000`, the Fraction-exact scaled limit trace has cell

```text
[0.48649576806397526..., 0.48658126877289976...).
```

It first fails at phase 25, product 8, vertex 14.  The input batch is empty,
the active face is

```text
{0,...,19,22,23,24,25,26},
```

and the scaled active input residual is

```text
-1.7517090946215215...e-6 < 0.
```

The upper endpoint is product 3, row 26.  Product 7, row 25 is strictly
larger by `5.9198099742...e-11`; this is a strict exact comparison, not a
floating tie.

## Complete comparison audit

There are no maximum-row ties, stop ties, zero exterior input tests, zero
closure-admission tests, or zero pre-push residuals.  The smallest exact
strict margins, rendered in decimal only for readability, are

```text
active nonzero input residual     1.4448592932...e-6
exterior input test               9.1475367519...e-5
raw nonzero velocity              1.6540752445...e-5
pre-push residual                 5.2981178523...e-6
closure test                      4.2202241789...e-5
unique-maximum gap                4.2681682094...e-8
stop-decision gap                 1.1268772900...e-5
```

The trace contains exactly 39 zero comparisons.  They are three copies of
the same 13 structurally forced zeros:

| event | vertices |
|---|---|
| post phase 4 | `5,8,15` |
| post phase 5 | `7,24` |
| post phase 6 | `11` |
| post phase 7 | `9` |
| post phase 9 | `10` |
| post phase 15 | `19,22,23` |
| post phase 16 | `26` |
| post phase 20 | `25` |

For every listed vertex, its closure diagonal push cancels its own residual
exactly, and no vertex pushed in the same or a later closure batch is its
neighbor.  Its post-closure residual is therefore structurally zero.  At the
first product of the next phase the scaled limit load is unchanged and the
phase velocity is reset, so the same coordinate has zero active input
residual and zero raw velocity.  These give `13+13+13=39` zeros.  The exact
audit checks the closure batches and the missing-neighbor condition for every
one of them; there are no other zeros.

## Lifting lemma for this trace

Fix any

```text
0.48649576806397526... < beta < 0.48658126877289976....
```

Then the zero-root trace lifts to a counterexample for all sufficiently small
positive `s` (and hence for a rational choice such as `s=1/m`).  The argument
is a finite induction through the 32 attempted products.

The required smallness threshold depends on the chosen `beta`, through its
distance from the two limiting cell endpoints.  Equivalently, the positive
instance parameter `alpha=s^2/(2-s^2)` may depend on `beta`; this is not one
fixed positive-root witness covering the entire interval at once.

All exterior admissions, positive-residual pushes, closure batches, maximum
rows, and stop decisions are strict at `s=0`, so those choices persist by
continuity.  The only zero input tests are on coordinates already in the
active face.  If one becomes negative after perturbation, the positive-root
run is already a counterexample at an earlier product.  Otherwise it does
not change the face, and the gradient/clamp update remains continuous because
`max(t,0)` is continuous at `t=0`.  The inherited zero raw velocities are
handled by the same observation.  Thus either an earlier failure occurs or
the finite positive-root state stays close to the limit state through phase
25, product 8.  In the latter case the limiting scaled failure margin
`-1.7517...e-6` makes the same active residual strictly negative.

This is the forced-zero, piecewise-continuous corollary of the finite-prefix
small-root lemma.  It does not require choosing a fixed analytic arm at the
zero velocity ties.  Therefore the zero-root computation is sufficient here:
there is no unresolved non-forced zero or tied branch comparison.

Combining this fixed-topology family with the finite exact beta-cell atlas
below the displayed lower endpoint refutes every fixed

```text
0 < beta < 0.48658126877289976....
```

The endpoint itself is not included by this strict-continuity argument.

Run the machine-readable exact audit with

```bash
uv run python \
  manuscript/notes/spectral_balance_threshold_batch/stopped_masked_input_residual_beta_04858_zero_root_limit_audit_exact.py
```
