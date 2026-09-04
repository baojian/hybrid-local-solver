# Stopped masked input residual: an exact triple-clock beta cell

Date: 2026-09-04

This is an unregistered companion result.  It extends the canonical
clock-grafting obstruction above `beta=0.46` without modifying any shared
integration file.

## Verdict

**Proved here.**  A 28-vertex finite simple connected undirected unit-weight
graph violates `MaskedInputResidual` throughout the exact chronology cell

```text
0.45836356321468646... <= beta < 0.46201574441162896....
```

In particular, `beta=23/50` is refuted.  This cell overlaps the preceding
double-clock cell, whose upper endpoint is `0.4589730192979452...`; together
they give a contiguous exact obstruction through `0.46201574441162896...`.

## Instance

Use the 24-vertex graph from
`STOPPED_MASKED_INPUT_RESIDUAL_TWO_FIFTHS_COUNTEREXAMPLE.md` and add

```text
2--24--25,     7--26,     2--27.
```

The first two grafts are the existing double clock.  The last leaf is the
new third graft.  The exact script exports the complete graph as
`TRIPLE_CLOCK_EDGES` and validates simplicity and connectedness.

Take

```text
s = 1/224,
alpha = 1/100351,
d_source rho = 21/1000,
rho = 21/2000,
relative terminal width = 1/1000,
beta = 23/50.
```

Run the canonical point-source zero-start chronology with pre-gradient input
admission, one simultaneous active diagonal push, maximal exact-positive
append-and-push closure, and the fixed-beta stopping test.

## Exact failure and clock relay

At one-based phase 19, product 8 is about to run after 25 completed products.
Its input batch is empty and the already active vertex `16` has

```text
xi_16 / phase_old_width = -3.165282566369072...e-8 < 0.
```

The preceding product has width ratio

```text
0.46663673977815245... > 23/50,
```

so the failing product is required.  Within the failure phase, the completed
products have

```text
product:  1          2          3          4          5          6          7
ratio:    .4759517   .4703437   .4620157   .4678245   .4776145   .4762617   .4666367
max row:  26         26         26         25         25         25         25
```

The single-leaf clock at row `26` carries products 1--3; the endpoint of the
two-edge clock at row `25` carries products 4--7.  The failure remains remote
at row `16`.

## Exact beta cell

The largest ratio among all stopped products is attained at phase 18,
product 1 and equals `0.45836356321468646...`.  The smallest ratio among all
continued products is attained at phase 19, product 3 and equals
`0.46201574441162896...`.  Since stopping uses a weak comparison and
continuation a strict one, the identical full chronology holds exactly on
the half-open interval stated above.  Every beta in that interval reaches the
same strict failure.

## Verification

Run:

```bash
uv run python manuscript/notes/spectral_balance_threshold_batch/\
stopped_masked_input_residual_triple_clock_counterexample_exact.py
```

Every arithmetic operation and branch comparison uses
`fractions.Fraction`.  The wrapper asserts the graph, parameters, failure,
clock rows, endpoint-attaining products, and equality between the independently
recomputed cell and the general tracer's exact cell field.

## Honest boundary

This is a finite cell, not a parametric limit.  It shows that a third local
graft can preserve the remote failure while moving the covered threshold
past `0.46`.  Refuting every fixed `beta<1/2` still requires further
synchronized clock cells or a family whose minimum continuation ratio tends
to `1/2`.
