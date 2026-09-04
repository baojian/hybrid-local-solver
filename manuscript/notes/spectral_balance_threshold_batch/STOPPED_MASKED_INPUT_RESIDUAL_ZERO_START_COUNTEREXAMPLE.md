# Stopped masked input residual: an exact canonical zero-start counterexample

Date: 2026-09-04

This is an unregistered companion result.  It tests the literal retained-prox
chronology from the prescribed zero lower state, with a single point source,
and with every mechanism in `StoppedMaskedInputResidual` enabled.

## Verdict

**The claim with the quarter-width inner stopping rule is false.**  A
Fraction-exact trace on a 16-vertex finite simple connected undirected
unit-weight graph reaches a strictly negative masked input residual.  The
failure occurs in the actual outer chronology, rather than in a supplied
inner state, and the trace uses all three intended mechanisms:

```text
pre-gradient input-residual frontier admission
+ one active diagonal residual push per product
+ immediate diagonal pushes to maximal exterior append closure.
```

This result has a precise boundary.  The product before the failure has
inner-width ratio `0.2583894607814098...`, only slightly above `1/4`.
The complete stopping chronology, however, is unchanged only on the exact
half-open beta cell

```text
[0.24963797244535363..., 0.25193067122814977...).
```

The lower endpoint is the largest ratio at a product where an earlier phase
stopped; the upper endpoint is the smallest ratio at a product which had to
continue.  Therefore this example refutes every beta in that cell, including
`1/4`, but makes no claim outside it.  A separate Fraction-exact 24-vertex
witness refutes a cell containing `beta=1/3`; see
`STOPPED_MASKED_INPUT_RESIDUAL_ONE_THIRD_COUNTEREXAMPLE.md`.

## Exact instance

Let the vertex set be `V={0,...,15}`, the source be `0`, and let the unit-edge
set be

```text
E = {
  (0,1), (0,10), (1,2), (2,3), (3,4), (4,5), (5,6),
  (7,12), (8,9), (9,10), (9,11), (10,15), (11,12),
  (12,13), (12,14), (13,14), (14,15)
}.
```

The source degree is two.  Take

```text
s = 1/224,
alpha = s^2/(2-s^2) = 1/100351,
d_source rho = 481/8000,
rho = 481/16000,
relative terminal width = 1/1000.
```

Run the canonical retained-shift outer loop from the zero lower state, with
shift `sigma=alpha`.  Every publication decision is the exact strict test
`residual>0`; zero is neither admitted nor pushed.

After 47 completed gradient products, at one-based outer phase 20, the tenth
product in that phase is about to run.  Its input batch is empty and its
gradient face is

```text
{0,1,2,3,4,5,6,8,9,10,11,12,14,15}.
```

The preceding exact inner-width ratio is

```text
inner_width / phase_old_width
  = 0.2583894607814098... > 1/4,
```

so the literal quarter rule must execute this product.  Before doing so, the
masked input residual at the already active vertex `11` is strictly negative.
In random-walk degree coordinates,

```text
xi_11 = -8.939445218207715...e-12 < 0,
xi_11 / phase_old_width = -1.533358898199047...e-8 < 0.
```

The exact verifier prints the full rational numerators and denominators.
Since normalized symmetric coordinates differ by multiplication by the
positive factor `sqrt(d_11)=sqrt(2)`, the sign failure is identical there.

## Why this is a canonical counterexample

The verifier constructs the point-source load and executes the entire outer
loop from zero.  At each shifted phase it resets the NAG momentum as
prescribed.  At each inner product it then performs, in order:

1. every exact-positive input-residual frontier admission;
2. the masked input-cone check and one gradient product;
3. the certified uniform lower retraction and momentum clamp;
4. one simultaneous exact-positive active residual push;
5. every exact-positive exterior append, with its immediate diagonal push,
   until closure; and
6. the exact inner stopping comparison.

All state values, residuals, outer updates, and branch comparisons use
`fractions.Fraction`.  Hence the negative residual and the strict preceding
`>1/4` comparison are exact statements, not floating-point or publication-
floor artifacts.  The graph validator also checks simplicity,
connectedness, and absence of isolated vertices.

Run:

```bash
.venv/bin/python manuscript/notes/spectral_balance_threshold_batch/stopped_masked_input_residual_zero_start_counterexample_exact.py
```

The dedicated wrapper asserts the graph, rational parameters, total product
count, failure phase/product/vertex, input batch, face, negative sign, and the
strict pre-failure quarter inequality.  It also reports the exact beta cell
on which all earlier stop/nonstop decisions, hence the whole failing
chronology, remain identical.  It calls the general exact tracer
`retained_prox_input_cone_trace_exact.py`, which contains the full chronology.

## Consequence and remaining proof target

The current quarter-stopped `Conditional InputConeFrontierNAG` route cannot
be used as stated, even after exploiting the complete single-source
zero-start ancestry and both kinds of chronological push.  This does not
rule out the overall deterministic local solver, nor the same route with an
earlier fixed stop.

The sharpened question is whether *some* universal `beta<1/2` forces the
chronological shield before any negative input residual can form.  The
present 16-vertex graph is stopped before its failing product at `beta=1/3`,
but separate exact traces refute cells containing both the one-third and
two-fifths rules.  Since beta changes the phase endpoints, isolated witnesses
cannot be ordered monotonically by their predecessor ratios; uncovered beta
cells remain genuine possibilities.
