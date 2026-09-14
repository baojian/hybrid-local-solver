# Proof-to-implementation map

Use this beside the [complete proof][pdf] and [reading guide][guide].
Proof references below are stable TeX labels: search the indicated label in
the [main file][main], [first appendix][appendix1], or [second appendix][appendix2].
Code links name the current standalone package methods, not research prototypes.
All links are relative to the final review-bundle root.

## 1. Start at the actual default route

[The public initializer][public] binds both `solve` and `solve_fast` to
`_fast.solve_rppr_fast`. That function calls
`_integer.solve_rppr_integer(..., corrector_class=FastDyadicCorrector)`.
The outer wrapper owns the fixed halving schedule, terminal repair, and result.
The cooperative class order is

    Fast → Combined → EarlyStop → Binomial → SourceEnergy → Direct → Integer.

Thus the executed numerical `step` passes through the early-bound invalidation
and binomial-power update wrappers to **`DirectExceptionIntegerCorrector.step`**.
`run` is `EarlyStopSourceEnergyCorrector.run`. The direct step implements the
same rounded recurrence as `IntegerDyadicCorrector.step`, with fewer intermediate
tree transitions. Reading only the latter misses the default dispatch.

The main theorem is an exact-real result. The package implements its separately
proved rational-input, bounded-dyadic extension: correction cap
`eta=1-mass(baseline)`, stage tolerance `tau=alpha*delta**2/8`, and exact terminal
PG followed by clipping, grid rounding, and a monotone maximum. The main
exact-real clipping proof instead uses `alpha**3*delta**2/2`.

## 2. Follow one stage

| Mathematical obligation | Package location | What to check |
|---|---|---|
| Safe baseline and diffuse source: `eq:baseline`, `eq:t`; cap `app:eta` | [Integer][integer] `IntegerDyadicCorrector.__init__` | Exact source from seed, baseline and its boundary; source range, mass identity, cached degrees, and dyadic baseline representation. No optimum is supplied. |
| Ordinary acceleration: `eq:iteration`, `lem:comparison` | [Direct][direct] `DirectExceptionIntegerCorrector.step`; [Integer][integer] `step` for the original transition | Mirror projection, scalar decay, selected primal increments, exact kinetic-neighbor sums. There is no inner original-objective line search or cleanup. |
| Two-energy justification: `lem:sector`, `eq:aux`, `eq:response`; rounded `app:two-energy` | The same step, source/box/cap initialization, and reporter | These are **analytical invariants**, not computed energies. Neither `x*`, `Q^(-1)s`, nor the comparison support appears as an algorithmic input. |
| Exact clipped projection: `eq:key`, `app:weighted-key`, `app:closed-tail` | [Reporter][reporter] `IntegerClippedReporter.project_counts`, `_threshold`, `_scaled_mass`; `IntegerMomentAVL.tail_moments`, `rank_record`, `at_least` | Two disjoint trees, four translated breakpoint sequences, exact affine root, and closed-tail emission at projected density **at least h**. Sub-grid positives are never enumerated and scanned. |
| Valid keys between queries: appendix `app:encoding` | [Direct][direct] `_finish_direct_transition`; [Reporter][reporter] `_set`; [Integer][integer] `_base`, `_install_exceptions` | Remove using the registry's old numerical key; refresh retired, new and touched records. No query occurs during transition. Rebase rebuilds exposed keys. |
| Stored error interface: `app:error-model`, `app:dyadic-update`, `app:scalar-rebase`, `app:rounding-constants`, `app:raw-rounding` | [Direct][direct] `step`; [Integer][integer] `_rebase` | Integer floors are downward. Scatter actual ordinary primal changes; rebase `X` and `L` independently **without adjacency scattering**. Keep kinetic/baseline sums exact. |
| Stage stopping: `app:initial-bound`, `app:binomial-block`, `app:checkpoints` | [Source][source] `SourceEnergyDyadicCorrector.__init__`; [Binomial][binomial] `dyadic_block_bound`, `objective_gap_bound`; [Early][early] `run`, `_checkpoint`, `CacheOnlyOracle` | Upward source-square statistic; actual target tolerance; fixed fallback horizon; cached-only independent checks. A zero-step stage returns its initial-energy bound. |
| Safe repaired output: `app:pg-repair`, `app:final-budgets`, `app:max-repair` | [Integer][integer] `output`, `_terminal_repair`, `solve_rppr_integer` | Materialize the actual candidate, compute an exact PG scan, clip before scanning newly positive PG neighbors, round, then take the old-baseline maximum. Approximate `L` is not the terminal gradient. |

**State dictionary.** Code `H=1/h`, `S/H=sigma`; `X`, `L`, `z`, `M` and
`baseline` store integer counts. The physical correction density is
`S*X[i]/H**2`, kinetic density is `z[i]/H`, `L[i]/H` approximates the sum
of neighboring `X/H`, and `M[i]/H` is the exact neighboring kinetic sum.
Full output density is `(H*baseline[i]+S*X[i])/H**2`.
Output triples `(vertex, density, degree)` represent
`x_i=density*sqrt(degree)` exactly.

## 3. Locate every local-work charge

The main derivation is `eq:selected` → `eq:work`; its rounded counterparts
are `app:perturbed-flow`, `app:rounded-work`, `app:rounded-mass-work`.
Explicit operation/bit bounds are in `app:explicit-complexity`.
The code records structural counters; it does not numerically evaluate the
unknown analytical support bound.

| Charged operation | Responsible method and records |
|---|---|
| New degrees, first and repeated row entries | [Integer][integer] `_expose`, `_row`; `degree_replies`, `first_adjacency_entries`, `scanned_adjacency_entries`, with baseline/selected subcategories. No boundary row is recursively scanned. |
| Repeated kinetic work and sparse responses | [Direct][direct] `step`; `kinetic_volume`, `selected_adjacency_entries`, `sparse_record_updates`. Each selected appearance pays again. |
| Ordered lookup, root search and emissions | [Reporter][reporter] `ReporterMetrics` under `corrector_metrics["reporter"]`; point changes, comparisons, rank/tail/mass queries, tree visits and emissions. Vertex maps/sets use [AVL containers][avl], not expected-time hashing. |
| Fixed source and old/new exceptions | Initialization and `_install_exceptions`; direct transition metrics; source/exception refresh records and membership passes. Their cost is charged even when no new vertex is found. |
| Scalar rebases and retained history | [Integer][integer] `_rebase`; old/rounded/exposed record counters, `scalar_neighbor_rebase_records`; `rebase_adjacency_entries=0`. Rebuilding keys and disposing obsolete records remain paid. |
| Materialization, checkpoints and disposal | `output`; [Early][early] `_checkpoint`, `_metered_checker`, `CheckpointMetrics`. Cached graph reads and temporary checker/container reclamation are charged, including unsuccessful checks. |
| Terminal scan, rounding, merging and output | `_terminal_repair`; stage `projected_gradient_metrics`; outer continuation/repair metrics and `final_output_words`. Zero-step stages still pay setup and terminal work. |
| Schedule and precision setup | Grid halvings, bound doublings, source-statistic records, binomial setup/power counters; `integer_size_snapshot` is an optional separately charged diagnostic, not an automatic all-state scan. |

Read `result.metrics` together with each stage's `corrector_metrics`.
These are overlapping structural views, **not numbers to indiscriminately
sum**: baseline/selected entry counts classify scanned entries; per-stage PG
details are also aggregated in outer repair metrics; checkpoint materialization
details include work recorded by `output`. Source reads and later cached reads
are distinct charged operations. The default integer mode does not measure
every Python arithmetic temporary; the proved bit bound is separate.

`certify_output`, in [the certificate module][certificate], implements
`app:independent-gap` independently of the acceleration proof. A user-requested
call pays its own support scan. An inconclusive certificate does not contradict
a smaller proved convergence bound.

## 4. Optional routes and evidence boundaries

| Public option | Proof and implementation change | Additional ledger |
|---|---|---|
| `solve_with_singleton` | `app:singleton`; [Singleton][singleton] `solve_rppr_with_singleton_precheck`. Seed-row KKT test, equality accepted, optional degree cutoff; otherwise call the supplied fallback. | `trial_metrics` **plus** the untouched `fallback_result` ledgers. Trial reads are not silently cached into the fallback. |
| `solve_adaptive` | `app:adaptive`, `app:diffuse-deficit`; [Adaptive][adaptive] `source_maximum`, `solve_rppr_adaptive`. Recompute the repaired-source maximum; nonfinal decreases have factor 2–4, final clamp may be closer. | `adaptive_metrics` plus inner result ledgers. Source passes and repeated cached reads are paid; numerical core and terminal repair are unchanged. |
| `solve_mass_scaled_grid` | `app:mass-grid`; [Mass grid][massgrid] `MassScaledGridCorrector.__init__`, `MassCapHintFactory`, `solve_rppr_mass_scaled_grid`. Fixed outer schedule; floor `29*eta*h/theta`, exact baseline representation, and restored **actual tau** before stepping. | `mass_hint_metrics` plus inner ledgers. Displayed retargeting subsets are already included in ordinary schedule counters; do not add them twice. |

These options are not silently composed with each other and are not required
by the default theorem. Their output trajectories or practical costs may differ.
The named comparison backends in the [package README][readme] remain available;
`solve_reference` is a packaged reference backend, not the default integer core.

For code verification start with [public solver tests][tests],
[optional mass-grid tests][mass-tests], and the [fixed-manifest validation
instructions][validation]. The package's transcription manifests identify
permitted source relocations. Earlier research-only Fraction prototypes,
dense obstacle oracles, and symmetry-reduced experiments are evidence, not
runtime dependencies or alternative premises of this theorem. Finite tests
check implementations; the two-energy and selected-work lemmas establish
graph-uniform guarantees.

[pdf]: output/pdf/deterministic_conjecture2.pdf
[guide]: proof_reading_guide.md
[main]: deterministic_conjecture2.tex
[appendix1]: practical_refinements_appendix.tex
[appendix2]: practical_schedules_appendix.tex
[readme]: deliverables/deterministic-rppr/README.md
[public]: deliverables/deterministic-rppr/deterministic_rppr/__init__.py
[integer]: deliverables/deterministic-rppr/deterministic_rppr/_integer.py
[direct]: deliverables/deterministic-rppr/deterministic_rppr/_direct.py
[reporter]: deliverables/deterministic-rppr/deterministic_rppr/_integer_reporter.py
[source]: deliverables/deterministic-rppr/deterministic_rppr/_source_energy.py
[binomial]: deliverables/deterministic-rppr/deterministic_rppr/_binomial.py
[early]: deliverables/deterministic-rppr/deterministic_rppr/_early_stop.py
[certificate]: deliverables/deterministic-rppr/deterministic_rppr/_certificate.py
[avl]: deliverables/deterministic-rppr/deterministic_rppr/_avl.py
[singleton]: deliverables/deterministic-rppr/deterministic_rppr/_singleton.py
[adaptive]: deliverables/deterministic-rppr/deterministic_rppr/_adaptive.py
[massgrid]: deliverables/deterministic-rppr/deterministic_rppr/_mass_grid.py
[tests]: deliverables/deterministic-rppr/tests/test_solver.py
[mass-tests]: deliverables/deterministic-rppr/tests/test_mass_grid.py
[validation]: deliverables/deterministic-rppr/validation/README.md

