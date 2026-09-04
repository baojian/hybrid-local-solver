# Exact four-leaf finite witness, zero-root limit, and continuity lift

Date: 2026-09-04

This note records a stronger `s -> 0` limit on the graph

```text
BETA_04865_BRANCH_BOUNDARY_EDGES
  + {(4,27),(15,28),(2,29),(13,30)}.
```

It is a connected simple unit graph with 31 vertices and 68 edges.  The
source is vertex `0`.  Fix

```text
d_source rho = 7053/500000,
relative_width = 1/1000,
beta = 2437/5000.
```

## Finite positive-root certificate

At retained root `s=1/1048576` and representative `beta=39/80`, the complete
Fraction-exact positive-root chronology fails at phase 24, product 8, at leaf
`28`, with empty input batch.  Its exact chronology cell is

```text
[0.4868820271518755...,0.48767016032436117...).
```

This is a direct finite positive-`alpha` certificate.  Its exact normalized
failure residual is strictly negative, although only
`-5.7004602573...e-19`; the robust scaled limit below explains the sign and
the stable branch mechanism.  The finite wrapper is
`stopped_masked_input_residual_beta_04877_four_leaf_exact.py`.

## Audited zero-root limit

The Fraction-exact scaled zero-root trace has chronology cell

```text
[0.48688202715538775..., 0.4876701546689488...).
```

Its first failure is phase 24, product 8, at leaf `28`, with empty input
batch and active face

```text
{0,...,19,22,23,24,25,26,27,28,29,30}.
```

The raw scaled input residual is exactly negative.  Its size relative to the
failure-phase width is

```text
-2.9873300452...e-6 < 0.
```

Unlike the nearly equioscillating two-leaf construction, the upper endpoint
here is product 3, row `26`.  Product 7, row `25`, is larger by
`0.0005565245230...`.  Decreasing the source threshold further is unsafe:
the strict failure residual is already the smallest nonzero active-input
margin and approaches its sign boundary.

## Complete equality audit

There are no maximum-row ties, stop ties, zero exterior-input tests, zero
closure-admission tests, or zero pre-push residuals.  The important strict
margins are

```text
normalized failure residual       2.9873300452...e-6
exterior/closure test              1.4022429778...e-5
non-tied lower-clamp gap           6.2711103367...e-6
post-closure active residual       6.2711103367...e-6
pre-push residual                  8.6970812638...e-6
unique-maximum gap                 3.7971744679...e-8
stop-decision gap                  2.7015466894...e-4
```

The exact equality ledger contains 40 grouped events.  They are four copies
of ten structurally forced closure groups, involving 17 coordinates per
event type:

| event | vertices |
|---|---|
| post phase 1 | `30` |
| post phase 2 | `18` |
| post phase 3 | `27,29` |
| post phase 4 | `5,8,14` |
| post phase 5 | `7,24` |
| post phase 6 | `15` |
| post phase 9 | `10,28` |
| post phase 14 | `26` |
| post phase 15 | `19,22,23` |
| post phase 19 | `25` |

For each group the four types are its post-closure zero residual, then at
product 1 of the next phase its inherited zero active-input residual, zero
raw velocity, and lower-clamp tie.  The closure push cancels the vertex's
own diagonal residual, while no vertex pushed in the same or a later batch
is its neighbor.  The next-phase equalities follow from stationary scaled
load and the phase velocity reset.  The exact wrapper checks every batch,
missing-neighbor condition, and equality event; no tie is unclassified.

## Continuity consequence

For every fixed

```text
0.48688202715538775... < beta < 0.4876701546689488...,
```

the zero-root run lifts to a canonical counterexample at all sufficiently
small positive retained roots `s`.  All admission, push, maximum-row, and
stop comparisons are strict.  If a forced active-input zero becomes negative
under perturbation, failure occurs earlier.  Otherwise it stays on the same
face, and the positive-part velocity and lower-clamp maps are continuous at
their forced ties.  Finite induction therefore reaches either an earlier
failure or the strict phase-24 failure above.

The small root `s=s(beta)`, and thus

```text
alpha = s(beta)^2/(2-s(beta)^2),
```

may depend on `beta`.  The upper endpoint is excluded.  Since the preceding
two-leaf finite and limiting cells overlap the displayed lower endpoint,
this family extends the continuous refuted interval, but it does not reach
`1/2`.

Run the machine-readable certificate with

```bash
uv run python \
  manuscript/notes/spectral_balance_threshold_batch/stopped_masked_input_residual_beta_04877_four_leaf_zero_root_limit_audit_exact.py
```
