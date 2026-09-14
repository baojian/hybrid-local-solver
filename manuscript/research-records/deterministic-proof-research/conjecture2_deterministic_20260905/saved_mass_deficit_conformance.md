# Exact conformance of saved runs to the rounded mass-deficit bound

**All recorded-stage checks passed.** This read-only audit made no solver
call and no graph-oracle call. It checked only existing complete answers,
using exact rational arithmetic. These tests supplement the proof in
`rounded_mass_deficit_refinement.md`; they do not establish its universal
or every-prefix claims.

| Saved artifact | Complete output records | Stage records | Stages with checkpoint metadata |
|---|---:|---:|---:|
| `final_combined_rppr_study.json` | 21 | 148 | 120 |
| `combined_certified_dyadic_study.json` | 24 | 120 | 60 |
| `direct_exception_transition_benchmark.json` | 12 | 72 | 72 |
| `worked_three_vertex_example.json` | 1 | 4 | 4 |
| **Total** | **58** | **344** | **256** |

The 256 stages record 749 checkpoints. Two output records and their twelve
stages are explicitly reused across the first two artifacts; their stored
source-file hashes, run indices, complete answers, and source-version maps
were reconciled exactly. Excluding that known reuse leaves 56 original
record occurrences and 332 stage occurrences. Timing repetitions remain in
these counts and are not presented as distinct graph instances. The four
artifacts contain respectively 14, 3, 3, and 1 case labels; some labels
refer to overlapping fixtures.

## Checks made at every complete stage

The cap was independently reconciled with the preceding saved repaired
output: `eta=1-sum_i d_i*bar_f_i`. The recorded baseline volume was likewise
checked against that preceding output. Each stage satisfies exactly

    eta >= r,
    vol(baseline) <= eta/r,
    source_mass = alpha*eta,
    source_records <=1+2vol(baseline) <=3eta/r,
    tau = alpha*delta^2/8 <=alpha^3*r^2/32,
    h <=theta*tau/256,
    Gamma_bound :=29h/theta <=alpha^2*r*eta,
    kinetic_volume <=360eta*K/r.

The dyadic momentum inequalities and the existing raw-error condition
`2h<=alpha*r/4` also pass. Repaired output masses and volumes agree with
their stage summaries. There are **no zero-step stages in this particular
saved-study subset**; the earlier proof and branch audits cover that case,
but it is not counted as tested here.

For checkpoint metadata, let J be the recorded count, S the recorded sum
of checkpoint iteration indices, and V their aggregate candidate volume.
Every applicable stage satisfies

    S <2K when J>0,
    V <=eta*(J+360S)/r,
    V =cached_adjacency_entries =checker_accumulation_updates.

All recorded cache-miss counts are zero, and every recorded temporary
checker container is reclaimed: both container totals equal 6J.

## Observed margins

The largest observed fractions of the corresponding new bounds were:

| Quantity divided by its refined bound | Largest fraction, approximately |
|---|---:|
| Baseline volume / `(eta/r)` | `0.802560604` |
| `(29h/theta)` / `(alpha^2*r*eta)` | `0.000442505` |
| Kinetic volume / `(360eta*K/r)` | `0.002582385` |
| Aggregate checkpoint volume / `(eta*(J+360S)/r)` | `0.000462535` |

Exact ratios and their case/stage identities are in
`saved_mass_deficit_conformance.json`. These observed margins do not justify
tightening any theorem constant.

## Provenance and limits

- Nineteen output records were produced under the recorded Python 3.12.14
  runtime, and 38 under Python 3.14.5. The two reused records retain their
  original 3.14.5 provenance rather than the enclosing study's 3.12.14
  metadata. The worked-example JSON does not record its runtime; none is
  retrospectively assigned. No timing values were compared or combined.
- All recorded source-file hashes match current source files except the
  worked example's package `__init__.py`. Its five recorded implementation
  module hashes still match. The current export file has additional named
  exports and still binds `solve_fast` to `_fast.solve_rppr_fast`. The saved
  run remains attributed to its recorded version; unrecorded dependencies
  are not claimed to have been version-checked.
- The direct-exception benchmark stores case names but omits explicit
  numerical input dictionaries. Its alpha was recovered from the recorded
  exact `source_mass/eta` and independently cross-checked by
  `8*tau/delta^2` at every stage. No graph parameters or missing trajectory
  values were invented.
- Saved stages contain endpoint cumulative kinetic volumes, not individual
  per-step volumes. Checkpoint metadata contains counts and aggregate sums,
  not each checkpoint's candidate volume. Accordingly this audit verifies
  endpoint and aggregate inequalities only; it does not reconstruct missing
  per-prefix data.
- `Gamma_bound` is the proved envelope `29h/theta`, not a measured actual
  rounding-error accumulation. The unknown optimum's mass deficit is not
  determined independently by these records, except in the worked example
  that already contains its exact optimum.

`audit_saved_mass_deficit_conformance.py` reproduces the checks using only
the standard library and saved JSON. Input files are hashed before and
after checking to confirm they remain unchanged. Original source, solver,
package, and manuscript files were not modified.
