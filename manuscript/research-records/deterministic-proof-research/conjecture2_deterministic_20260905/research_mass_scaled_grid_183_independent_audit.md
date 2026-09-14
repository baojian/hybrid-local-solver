# Independent exact validation of the mass-scaled-grid research prototype

**All 183 fixed manifest cases passed.** This is a new full integration check of
`mass_scaled_grid_rppr.solve_rppr_mass_scaled_grid`. It makes no claim that this
prototype is packaged or selected as the default. Neither fast nor adaptive was
rerun, and no numerical module, existing test, or package file was changed.

The tested prototype SHA-256 is
`3b8cfa4a8f0161101147573007e5ac4cbabb4c64e348ec702f90d977a37d7d8f`, matching the
requested source. All recorded prototype/core/dependency hashes agree before and
after the run. The canonical 183-case manifest is unchanged, with hash
`e02485273de4bc1b615530518ac9db60ae5d7beee0140e0e787f6f4320ed0434`.

## Independent validation interface

For the 181 explicitly represented cases, the existing independent
`tests.test_solver.validate_case` receives a wrapper returning the prototype's
unchanged inner `SolverResult`. Thus its exhaustive KKT optimum, exact original
objective, repaired source, fixed-halving schedule, sparse safety, and ordinary
external-oracle ledger checks remain in force. The two huge stars use an exact
analytic seed-only optimum with all omitted leaf KKT conditions checked.

A separate strict oracle proxy checks local discovery and actual degree/entry
counts. Observational subclasses count steps, capture returned actual stage
candidates, and inspect initialization after retargeting; they do not change
the rounded numerical operations. Each stage's candidate is independently
compared with the exact optimum, so the restored certificate is checked against
the actual original-objective error as well as against its own scalar fields.

For every one of the **520 stages**, the additional checks establish:

- `eta` equals both the factory hint and the assembled exact source-mass cap;
  `source_mass=alpha*eta`, and `eta>=r`. The preceding repaired baseline is
  represented exactly on both the declared preceding grid and the selected
  current grid.
- The actual weighted floor is `Gamma=29*eta*h/theta < tau/8`, with
  `h<=theta*tau/(256*eta)` and `Gamma<=eta*alpha^2*r`. All terminal repair grid
  constraints hold. No unit-mass precision bound is incorrectly imposed on
  this new variant.
- Before any step, the actual tolerance, zero-step certificate, current block
  power, accepted-checkpoint state, and next-checkpoint index are correct. The
  original, half-block, and binomial horizons are independently reconstructed
  for the **actual** tolerance, including minimality and their ordering.
- Retargeting work is included in the accumulated ordinary schedule counters
  exactly as claimed; its displayed diagnostic subsets are not added twice.
- The baseline/source-volume and stronger `eta<=4*eta_*(r)` bounds hold, as does
  cumulative kinetic volume `<=360*eta*K/r`. The original fixed halving rule is
  used throughout.
- Checkpoint cache misses are zero, geometric aggregate volume is paid, and all
  created checker containers are reclaimed. The exact returned candidate and
  repaired output satisfy their respective objective certificates.

The factory observers compare actual oracle counters before scalar hint
computation with counters on entry to the new corrector construction. All 520
comparisons agree: hint computation itself introduces no graph request. Final
factory release also introduces no graph request. The extra cached degree
lookups, conversions, integer updates, and retained-reference releases remain
separate additive scalar-work metrics.

## Recorded outcomes

| Quantity | Count |
|---|---:|
| Complete solver cases | 183 |
| Completed stages | 520 |
| Correction iterations | 12,068 |
| Actual oracle adjacency entries | 2,760 |
| Actual oracle degree replies | 2,156 |
| Factory cached scalar degree lookups | 713 |
| Factory reference releases | 520 |
| Checkpoints | 1,508 |
| Accepted / rejected checkpoints | 420 / 1,088 |
| Checker containers created / reclaimed | 9,048 / 9,048 |
| Checkpoint cached adjacency entries | 9,405 |

All **183** final outputs pass both the exact optimum/objective comparison and a
separately calculated exact original-objective subgradient certificate. All eight
large-label/reversed-row cases agree with their own unrenamed prototype case in
final output and every repaired stage. No equality with a different backend's
trajectory or output is assumed.

On saved records, 48 stages have a grid coarser than the ordinary unit-mass grid
for the **same incoming baseline**, with maximum factor four. This comparison
recomputes only the scalar grid rule and does not run another solver. Forty-nine
actual binomial horizons are strictly longer than their relaxed initialization
horizons, so the restored-tolerance path is materially exercised. The largest
observed `Gamma/(tau/8)` is exactly `29/32`, still strictly below one.

Both analytic stars, with `10^6` and `2^100` leaves, make six seed-row requests and
read six actual graph entries, with thirteen degree replies each. No hub row is
queried. Seven cases use direct branches. This manifest has **no zero-iteration
stage**; this integration report therefore does not claim new numerical coverage
of that branch. The separate per-prefix/zero-stage audit is a distinct artifact.

No guard was reached. The fixed guards were 250,000 iterations, 10,000,000 actual
oracle entries and degree replies each, 120 seconds per case, and 1,800 seconds
total. Completed records were atomically saved after each case, with partial
observations and incomplete status available on failure. Every full case was run
once; all subsequent processing was read-only summarization of saved outcomes.

## Reproducibility files

- `validate_mass_scaled_grid_prototype_independent.py`: independent validator,
  SHA-256 `6dd9f09a56a0bf113bbf5773cbef7f2e7af3585c6b8cd5e5f69704451207e197`.
- `research_mass_scaled_grid_183_validation.json`: complete manifest, results,
  stages, candidates, exact comparisons, mass hints, extra work ledgers, runtime,
  guards, and before/after source hashes; SHA-256
  `4e31680a52b2d5aed6a5b0407a5559b363140eb1291d8aedae59a06360dd8ffe`.
- `research_mass_scaled_grid_183_validation_summary.json`: compact exact counts
  and diagnostic ratios.
- `research_mass_scaled_grid_183_validation.log`: sequential completion log.

No implementation defect was found. These exact tests supplement the proof and
the separate per-prefix audit; they do not establish comparative runtime or
ordinary floating-point correctness.
