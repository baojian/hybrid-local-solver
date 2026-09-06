# Verification record

Investigation start: **2026-09-06 02:49:49 UTC**.
Requested minimum completion time: **2026-09-06 08:49:49 UTC**.
Final review time: **2026-09-06 09:06:34 UTC**.
Elapsed investigation: **6 hours, 16 minutes, 45 seconds**.
All 35 recorded runs are complete; 29 have verified saved source snapshots.
Elapsed investigation time is distinct from the CPU or wall time of any
individual audit. The user requested at least six hours.

## What the evidence means

The TeX proofs establish the asymptotic statements. The computations below
check identities, invariants, implementation equivalence, finite examples
and specific handoff interfaces. They do not constitute formal verification
of an infinite-family theorem. No practical speedup over a benchmarked
solver is claimed.

All graph models use original degrees and canonical simple unit graphs.
Dense exact optima and equitable radial representations are offline
verification instruments, not uncharged local-algorithm primitives.
Python dictionaries and heaps implement audit states; the deterministic
worst-case data-structure bounds in the note use balanced trees.
The coordinate-tail checks execute the stated mathematical trajectory with
dense verification residuals and offline invariant checks. Their incidence
counters check the degree ledger. They are not a production implementation
whose every executed verification operation has local cost.

## Principal completed runs

Raw run names below are stems under
`results/raw/two_stage_revisited_20260906/`. Parameters, SHA-256 hashes,
source-snapshot checks and reproduction commands are in `COVERAGE.json`.
Counts from overlapping runs must not be added as disjoint coverage.

| Run | Coverage | Main assertions |
| --- | ---: | --- |
| `orthant_smoke` | 64 cases, 1,536 exact steps | Two energies, cooling bank, moving flow and work |
| `orthant_nonsquare` | 548 cases, 94,530 exact steps | Four non-dyadic-square alpha choices and dyadic theta selection |
| `orthant_atlas_full` | 27,120 cases, 2,461,140 exact steps | Every seed on all 995 connected atlas representatives with 2–7 vertices; four alpha values |
| `sparse_state_extended` | 1,618 graph cases + 12 implicit stars | Dense/sparse state and key equality, output and row ledger |
| `sparse_state_endpoints` | 64 graph cases + 12 endpoints + 12 stars | Zero and alpha=1 branches; inactive high-degree hubs |
| `directed_rounding_extended` | 4,872 graph cases + 4 stars | Actual directed records, rounding, energies, grids, ties, pruning and work |
| `directed_rounding_nonsquare` | 1,114 graph cases + 4 stars | Four alpha values that are not dyadic squares; complete rounded-state and pruning checks |
| `objective_residual_kkt` | 780 cases | Independent RPPR objective, KKT and optional positive-residual targets |
| `sparse_sources_smoke` | 324 graph cases + 4 stars | Additive input work, original source weights, semantic and ACL output |
| `general_source_objective_extended` | 10,228 cases | Original-source objective restored on the approximate envelope |
| `general_source_certificates` | 652 cases | Additional maximum-principle, KKT and residual assertions |
| `relative_tail` | 256 cases + 2 cycle witnesses | Relative RPPR deficit and exact/rounded reserved GS |
| `excess_tail` | 256 cases | Observable excess budget; 128 prefixes above RPPR; all exceed the older objective budget |
| `coarse_face_handoff_extended` | 36 cases; 19 nonempty tails | Certified face-relative randomized-prefix interface and GS |
| `coarse_face_excess_handoff` | 36 cases; 27 nonempty tails | Optional earlier residual-excess gate on the same face contract |
| `deterministic_signed_handoff` | 256 actual runs | Conservative coarse prefix and signed delivery; all small-graph tails empty |
| `deterministic_signed_early` | 256 actual runs; 248 nonempty tails | Optional early residual gate |
| `deterministic_signed_extended` | 1,096 actual runs; 1,025 nonempty tails | Expanded early gate; 1,083 early handoffs; 12 additional external signed-tail witnesses |
| `deterministic_signed_order` | 256 actual runs + 12 signed-tail witnesses | Final clipping lies below RPPR at eps_ppr/3 and has nonnegative residual |
| `deterministic_signed_final` | 256 actual runs + 12 signed-tail witnesses + 14 endpoints | Strengthened order/residual assertions and the corrected alpha=1/zero branches |
| `deterministic_signed_composite` | Same scopes plus 4 signed composite-gap witnesses | Negative-coordinate supplied states qualify without lower retraction; no AESP-prefix implementation claimed |
| `deterministic_signed_nonsquare` | 512 actual runs; 438 nonempty tails, plus the same 30 external/endpoint checks | Four alpha values that are not dyadic squares; exact and separately rounded handoffs |
| `aesp_exact_shift_instability` | 3 exact finite trees and a rational frequency certificate | Ideal exact-inner AESP residual-mass obstruction; excludes thresholded inner-policy conclusions |
| `aesp_exact_shift_excess` | The same 3 finite trees | Additional exact excess check: the largest mass witness already has zero excess at reserve 2^-16 |
| `aesp_exact_shift_realization` | The same 3 large trees plus 3 materialized small graphs | Independent dense shifted solves match the level-polynomial trajectory through six stages |
| `ramp_four_counterexample` | One exact finite certificate | 512-vertex lollipop exceeds a 4r tracking bound |
| `radial_ramp_counterexamples` | Four exact finite certificates | Decrease, PPR overshoot, negative residual and tracking above 10^15 |
| `radial_tracking_search` | 81 finite trajectories | Integer tracking certificates below floating-point resolution |
| `radial_tracking_deeper` | Four deeper finite trajectories | Largest certified finite ratio above 9×10^75 |
| `front_limit_uniformity` | 12 finite trees, through 65,000 steps | Energy-certified kinetic positivity and exact integer sign checks |
| `front_limit_probe`, `front_limit_extended` | 28 finite/limit comparisons | Exact transfer gain and high-precision diagnostics of the graph limit |
| `front_limit_growth` | Seven limit-only profiles | Numerical cascade growth, checked at 80 and 100 digits |
| `ramp_probe_extended`, `quotient_ramp_extended` | 2,080 and 735 floating cases | Falsification searches; not the rigorous counterexample certificates |

The P16 exact intermediate RPPR-gradient witness is reproduced by the
registered `unsafe_intermediate` audit and recorded in the focused runner log.

The expanded general-source objective run began before the later extra
maximum-principle/KKT assertions were added. The separate 652-case run checks
those additions. The conservative and first early deterministic runs began
before the external signed-tail witnesses were added; the expanded run and
final focused suite exercise them. These distinctions are preserved by the
saved source snapshots.

The final output-order review caught and corrected an alpha=1 endpoint:
the stronger RPPR order statement requires returning the regularized seed
value, rather than exact unregularized PPR. The last dedicated run includes
14 explicit endpoint checks. Earlier runs did not assert this stronger order.

The randomized face audit uses exact elimination to propose a dyadic answer
that must pass the imported theorem's residual test. It neither implements
nor times randomized SDD. External tail-only witnesses start from explicit
reference points; they are not claimed to be generated by the prefix.
Earlier handoff is not always cheaper: the optional randomized excess gate
can exchange fewer face solves for hundreds of thousands of coordinate
updates in this finite collection.

## Provenance qualifications

Later runs save the exact Python sources under a sibling `_source/` directory,
as well as their hashes, input parameters, UTC start, repository commit,
dirty-worktree flag and null random seed for deterministic audits.
The two floating graph-generation campaigns use seed `20260906+i` for
generated graph index `i`, as recorded by their graph IDs and source rules;
the solver trajectories themselves are deterministic.
`COVERAGE.json` verifies these saved hashes when a snapshot is present.
The early smoke/atlas/nonsquare and some interface outputs predate this
snapshot helper. Their recorded source hash or command log is retained;
an exact source snapshot is unavailable for those early runs. In particular,
the long atlas audit began before a formatting change to its script. Its
initial source fingerprint differs from the current file; do not pretend
the current file is that archived source. Later focused checks use the
current source. This is a provenance limitation, not an assertion of new
mathematical coverage.

The session started on dirty commit
`529be09beca95dadc87143cf4af90be46a6e08d2`. Another task committed the existing
manuscript changes as `7e1b4e77351b361e0c700ce3186c1534d2023f0e` during this
investigation. Those changes were preserved. This contribution changes only
the new dated note/audit directories and their five index/registry/runner
integration files. No active manuscript source, older note, baseline, or
provider implementation was changed.

## Repository checks

- `make agent-audit`: **passed**.
- Focused audit runner: **12 audits passed** (fast tier, 136.0 seconds in
  the final suite run). Later ideal-AESP excess/realization assertions and
  the additional alpha choices passed their separate runs recorded above.
- Focused Ruff check and format check: **passed**, 21 Python files including
  the shared runner.
- `make test`: **231 passed, 3 pre-existing failures**. The latest
  `make reproduce` reaches the same test gate and stops with those failures.
- `make lint`: **two pre-existing failures**; the command stops before its
  subsequent full-format gate. Do not report the repository-wide lint as green.
- Note inventory: the only failures are the same two pre-existing oversized
  source files. The new note's status, registry and dependency checks pass.
- TeX build: **36 pages**, no undefined references, warnings or overfull boxes.
- PDF: all 36 pages inspected for clipping, overlap, equations, page breaks
  and references, including re-rendering the changed pages after the earlier
  33-page review.

The existing test failures are
`test_known_semantic_aliases_do_not_regress` (the older AESP notation alias)
and two inventory tests for existing 1,237-line and 4,361-line note files.
The existing lint findings are an unused `pagerank_matrix` import in
`problem_definitions/verify_exact_batch_cholesky.py:14` and a lambda assignment
in `spectral_balance_threshold_batch/green_band_stress_exact.py:248`.
Their full logs are retained beside the raw results.

## Reproduction

From the repository root:

```sh
make -C manuscript/notes/two_stage_revisited_20260906
uv run python -m experiments.proof_audits.runner --note two_stage_revisited_20260906
uv run python -m experiments.proof_audits.two_stage_revisited_20260906.deterministic_signed_handoff --max-n 5 --early
uv run python -m experiments.proof_audits.two_stage_revisited_20260906.front_limit_uniformity --pairs 1,2,4,8
```

The full runner tier includes long exact and numerical campaigns; use the
individual commands in the coverage manifest to reproduce a specific claim.
