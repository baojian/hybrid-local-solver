# Stopped masked input residual: an exact two-fifths-stop counterexample

Date: 2026-09-04

This is an unregistered companion result.  It strengthens the canonical
zero-start obstruction to the fixed stop
`inner_width <= (2/5) old_width`.

## Verdict

**The two-fifths stop does not preserve `MaskedInputResidual`.**  A
Fraction-exact trace on a 24-vertex finite simple connected undirected
unit-weight graph reaches a strictly negative active input residual after a
predecessor with

```text
inner_width / phase_old_width
  = 0.4151107187959626... > 2/5.
```

Thus the failing product is required even by the earlier two-fifths stop.
The full run is the prescribed point-source, zero-start outer chronology with
all three input-frontier, active-push, and maximal append-push mechanisms.
The identical strict trace holds for every beta in the exact chronology cell

```text
[0.38928607214283667..., 0.41511071879596256...).
```

This witness does not address `beta=9/20` or any beta outside that cell.

## Exact instance

The instance is the same 24-vertex graph used by the one-third witness.  Let
`V={0,...,23}`, source `v=0`, and

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
beta = 2/5.
```

At one-based outer phase 14, the seventh product in the phase is about to run,
after 19 completed products.  Its input batch is empty, its failure vertex is
the already active vertex `16`, and its face is

```text
{0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18}.
```

The exact degree-coordinate residual satisfies

```text
xi_16 / phase_old_width = -4.846557184187879...e-9 < 0,
```

while the exact preceding width ratio is
`0.4151107187959626... > 2/5`.  Positive diagonal similarity preserves the
failure sign in symmetric normalized coordinates.

## Exact verification

Run:

```bash
.venv/bin/python manuscript/notes/spectral_balance_threshold_batch/stopped_masked_input_residual_two_fifths_counterexample_exact.py
```

The dedicated wrapper first invokes the graph validator, then runs the full
chronology with `fractions.Fraction` for every value and branch comparison.
It asserts the rational parameters, first failure phase/product/vertex, face,
negative sign, and strict pre-failure `>2/5` inequality.  The general tracer
uses exact-positive publication decisions: a zero residual is neither
admitted nor pushed.  It also reports the exact half-open beta cell on which
every preceding stop/nonstop decision is unchanged.

## Consequence

The sequence of exact witnesses at beta `1/4`, `1/3`, and `2/5` shows that a
moderate adjustment of the stopping constant does not restore the proposed
coordinatewise cone.  A separate exact atlas now overlaps this cell with
lower and higher histories to cover every `0<beta<0.4620157444...`; see
`STOPPED_MASKED_INPUT_RESIDUAL_BETA_CELL_ATLAS.md`.  Thresholds from that
endpoint to `1/2` remain open.  The examples do not by themselves refute a
different invariant or a modified update rule.
