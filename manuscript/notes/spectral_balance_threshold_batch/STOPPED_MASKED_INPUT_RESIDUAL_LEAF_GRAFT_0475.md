# Stopped masked input residual: an exact beta=.475 leaf-graft cell

Date: 2026-09-04

This is an unregistered companion result.  It records a one-leaf extension
of the exact `beta=0.473` graph and does not alter the shared beta-cell atlas.

## Verdict

**Proved here.**  Add one pendant leaf to failure-side vertex `14` of the
27-vertex graph exported as `BETA_0473_EDGES`.  With rationally retimed
`rho`, the canonical zero-start chronology violates `MaskedInputResidual`
for every

```text
0.4724806924545223... <= beta < 0.4761532081683130....
```

Thus `beta=19/40=0.475` is refuted.  This cell overlaps the previously exact
cell ending at `0.4735482533062691...` and therefore extends its contiguous
coverage to `0.4761532081683130...` once independently replayed.

## Exact instance

Use `BETA_0473_EDGES` and add only

```text
(14,27).
```

The resulting graph has 28 vertices and 51 edges.  It is finite, simple,
connected, undirected, unit-weight, and still has source `0` of degree two.
Take

```text
s = 1/224,
alpha = 1/100351,
d_source rho = 79/4000,
rho = 79/8000,
relative terminal width = 1/1000,
beta = 19/40.
```

Run the canonical pre-gradient input admission, simultaneous active diagonal
push, maximal exact-positive append-and-push closure, and fixed-beta stop from
the zero lower state.

## Exact failure

At one-based phase 22, product 8 is about to run after 28 completed products.
The input batch is empty and the new leaf `27`, which is already active, has

```text
xi_27 / phase_old_width = -4.3859936161093515...e-9 < 0.
```

The predecessor ratio is

```text
0.4772934261992556... > 19/40,
```

so the failing product is required.  The completed failure-phase products
have the relay

```text
product:  1          2          3          4          5          6          7
ratio:    .4827578   .4804856   .4761532   .4801533   .4862220   .4846453   .4772934
max row:  26         26         26         25         25         25         25
```

Thus the existing clock branch keeps the phase alive; the added leaf is the
remote failure row rather than the maximum-width row.

The leaf is not released just before failure.  The exact history publishes it
in the append closure of phase 4, product 1, together with rows
`{4,5,10,27}`.  It is then active-pushed in the first product of every phase
5--21 and in all seven completed products of phase 22.  At the failed input
it has positive retained velocity, `current_27>previous_27`.

Because row `27` is a nonsource degree-one leaf with sole neighbor `14`, its
exact failed input residual in random-walk degree coordinates is the scalar
identity

```text
xi_27 = h_27 - b q_27 + c q_14,
b=(1+3 alpha)/2,     c=(1-alpha)/2,
q=current+theta(current-previous).
```

The verifier asserts this identity as a rational equality.  Numerically at
the failure,

```text
q_14 = 1.1530443614643556...e-6,
q_27 = 9.562180953169972...e-7,
h_27 = -9.839632513526544...e-8.
```

Thus the old port forcing is eventually overtaken by the leaf's extrapolated
diagonal term.  The graft separates the maximum-width clock from the failing
row, but it does so through accumulated momentum on an early-published leaf,
not through a one-product fresh-leaf trigger.

## Exact chronology cell

The largest stopped-product ratio is attained at phase 21, product 1 and is
`0.4724806924545223...`.  The smallest continued-product ratio is attained
at phase 22, product 3 and is `0.4761532081683130...`.  The full chronology
is therefore identical on the half-open interval in the verdict.  The lower
endpoint is included because stopping uses `<=`; the upper endpoint is
excluded because continuation is strict.

## Verification

Run:

```bash
uv run python manuscript/notes/spectral_balance_threshold_batch/\
stopped_masked_input_residual_leaf_graft_0475_exact.py
```

The exported constants are `LEAF_0475_VERTICES`, `LEAF_0475_EDGES`,
`LEAF_0475_ROOT`, `LEAF_0475_RHO_SCALE`,
`LEAF_0475_RELATIVE_WIDTH`, and `LEAF_0475_STOP_BETA`.  The wrapper validates
the graph and uses `fractions.Fraction` for every state and branch.  It
asserts the failure, the relay rows, endpoint-attaining products, and exact
equality between its independently reconstructed cell and the tracer's cell.

## Structural reading and boundary

The leaf graft does two different jobs cleanly: the old clock branch controls
all seven continuation widths, while an early-activated leaf later develops
the negative extrapolated input residual.  This avoids asking one gadget to
both keep the phase alive and fail the cone.

The calculation is still a finite cell, not a family tending to `1/2`.  Its
failure sign is small, so every higher-beta extension must be independently
replayed exactly; numerical continuity alone is not a certificate.
