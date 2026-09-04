# Stopped masked input residual: an exact beta=.48 cell

Date: 2026-09-04

This is an unregistered companion result.  It concerns only the canonical
zero-start, one-push-maximal retained-prox chronology.

## Verdict

**Proved here.**  There is a finite simple connected undirected unit graph on
27 vertices for which `MaskedInputResidual` fails for every

```text
0.47690551924253965... <= beta < 0.4812222006674521....
```

In particular, `beta=12/25=0.48` is refuted.  The lower endpoint lies below
the independently exact preceding cover through `0.4784561594666679...`, so
the cells overlap and extend the continuous counterexample interval through
the upper endpoint above.  This is a finite cell, not a proof for all
`beta<1/2`.

## Exact instance and chronology

The graph, source, and all 59 unit edges are exported as `BETA_048_EDGES` in
`stopped_masked_input_residual_beta_048_counterexample_exact.py`.  Its source
is vertex `0`, with the same two source edges `(0,1)` and `(0,12)` used in the
earlier two-lobe witnesses.  Take

```text
s = 1/224,
alpha = 1/100351,
d_source rho = 171/10000,
rho = 171/20000,
relative terminal width = 1/1000,
beta = 12/25.
```

The exact run stops once per phase through phase 21.  In phase 22, the first
seven products continue and product 8 has the first negative active input
residual.  The input batch is empty, the failing row is `15`, and

```text
xi_15 / phase_old_width = -9.297704068113206...e-9 < 0.
```

The active face at failure is

```text
{0,1,...,18,24,25,26}.
```

The completed products in the failure phase have the exact two-clock relay

```text
product:  1          2          3          4          5          6          7
ratio:    .4874557   .4849087   .4813478   .4847608   .4891352   .4875039   .4812222
max row:  26         26         26         25         25         25         25
```

Thus the one-edge clock at row `26` covers the first three products and the
two-edge clock ending at row `25` covers the final four.  The exact bottleneck
is product 7, and it remains strictly above `0.48`, so product 8 cannot be
skipped.

## Chronology cell

The largest ratio at a stopped product is attained at phase 21, product 1:

```text
0.47690551924253965....
```

The smallest ratio at a continued product is attained at phase 22, product 7:

```text
0.4812222006674521....
```

Since the stopping comparison is weak, the first endpoint is included; since
continuation is strict, the second is excluded.  The verifier reconstructs
both extrema from every stop decision in the full trace and checks equality
with the tracer's independently accumulated chronology cell.

## Verification and boundary

Run:

```bash
uv run python manuscript/notes/spectral_balance_threshold_batch/\
stopped_masked_input_residual_beta_048_counterexample_exact.py
```

The wrapper uses `fractions.Fraction` for every state, admission, push, and
stopping comparison.  It validates simplicity and connectivity, checks the
failure location and empty input batch, reconstructs the cell, and verifies
the complete maximum-row relay.

This witness refutes the proposed fixed-threshold repair at `beta=.48`; it
does not yet settle the remaining interval from its exact upper endpoint to
`1/2`.  A full negative theorem still needs either overlapping cells through
every larger beta or a parametric clock-synchronization construction.
