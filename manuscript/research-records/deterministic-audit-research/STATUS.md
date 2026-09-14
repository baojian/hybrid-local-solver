# Research handoff — deterministic OP2

**Read CURRENT.md first for the current live state. This file retains the
chronological research history and contains superseded running-job entries.**

Last substantive update: 2026-09-05 08:04 UTC.
Status: **Reported proof passed this session's first independent mathematical
audit; further verification active; minimum ten-hour work not yet fulfilled.**

The objective and constraints in README.md remain authoritative. Research
started at 01:41:57 UTC; the requested minimum window ends at 11:41:57 UTC.
No repository files have been edited, and no randomized operation has been
used in any proposed solver or test. At 05:08 UTC another task requested
coordination. Only pre-existing repository pointers and known primitive
obstructions were sent; this session's new explorations remain private.

## Latest direction: mass-preserving score repair

**08:04 audit/refinement update:** independent exact lemma checks passed
576 stage cases / 18,432 iterations and 16,100 projection-sector cases.
Results and proof review are in `notes/independent-proof-audit.md`.
The first-read hashes are recorded there. A later snapshot in
`results/proof-snapshot-after-first-audit/` has different hashes because the
owning task continued editing; its note explicitly distinguishes it from
the first-read version.

A private copied package `pruned_rppr/` adds fixed **final** degree pruning
and an optional source-derived box. `PROVENANCE.json` records the source
package and hashes. The original package is unedited. The restricted proof
uses `M=Q_AA` and changes the second linear energy term to
`lambda (M w)^T xi`, because `M w>=alpha w` rather than equality. All original
degrees and scanned incidences are retained. The full-objective audit
completed 72 cases / 17,652 iterations / 216 stages, all exact checks passed.
See `notes/fixed-degree-pruning.md`. Sessions 50308, 64975, and 42205 are
complete; there are currently no intended live old-direction experiments.

Two further practical ideas are being developed, not yet implemented:
(i) shrink the permanent degree cutoff to `(1-mass(baseline))/rho` at stage
boundaries; it is safe because the monotone baseline lies below the final
optimum. Never use restricted source mass/alpha for that cutoff.
(ii) first explore the seed's component in the fixed degree-pruned graph
under a total original-degree budget `1/rho`. Query degree before deciding
to scan a row. If the component is fully exposed within budget, solve its
known constrained quadratic directly; otherwise fall back to continuation.
This costs at most `O(1/rho)` initial work. Retain original degrees and count
excluded neighbor replies. A singleton component has an immediate exact
diagonal solution. For a larger completed component, a possible direct
dyadic accelerated solver can use the known lower spectral bound
`beta=alpha+(1-alpha)/2 * min_i(outside_degree_i/d_i)`, choose dyadic theta
with theta^2<=beta, and project onto density box `U=1/d_seed` and mass<=1.
Both contain the optimum. With exact raw products and downward density
rounding h in auxiliary/primal states, the ordinary-energy perturbation
bound is `E_next<=a E+5h`. Taking `h<=theta epsilon/16`, a block horizon with
`a^K<=epsilon/2`, gives gap below epsilon with only bounded rational state.
These details require a complete derivation and implementation audit before
they are promoted to a theorem or delivered as software.

**Important 07:43 change:** another task reported a complete canonical
deterministic OP2 proof. This session read its full main TeX and practical
appendix and independently checked the mathematical argument and local
ledger. No gap was found in the first pass. The proof belongs to task
**Prove conjecture 2 deterministically**, at
`research/conjecture2_deterministic_20260905/deterministic_conjecture2.tex`.
See `notes/independent-proof-audit.md` for hashes and the detailed review.
It uses continuation, a diffuse residual source, a box/cap projection,
and a second residual energy. It does not prove the rate of this session's
separate mass-preserving repair candidate, which remains open.

No private exploration was disclosed. The three remaining old-direction
campaigns (PIDs 83639, 84604, 90138; sessions 34983, 44053, 95801) were
intentionally stopped with SIGINT at about 07:43 to redirect effort toward
the proof audit. Their finite logs and checkpoints remain preserved; a
stale checkpoint marked running is not evidence of an active process.
The goal remains active because the requested duration and independent
implementation verification are unfinished. At 07:43 the goal tool reported
20,029 seconds of accumulated work; do not substitute the six-hour elapsed
wall clock for ten hours of actual work.

**07:33 update:** the corrected main repair census completed 6,491 cases
with no experimental-horizon failures; the port probe completed 1,098
cases, with a numerical maximum port/coarse-dissipation ratio about 13,209.
The dense actual-graph beam completed 14,642 cases, with maximum substantial
repair energy debit -0.0173441 in its normalized convention. No positive
zero-start energy violation was certified. The resumed PLC tree beam also
completed, adding 26,617 cases; its final worst signed-debit ratio was about
0.75844. These are finite deterministic searches, not rate theorems.

The 96-case stable APC residual probe completed. The largest observed mean
positive residual divided by alpha rose from about 2.72 at alpha=.01 to
426.61 at alpha=1e-8, while the corresponding normalized mean actual row
volume remained below one in those worst-residual examples. Inactive
positive-score cancellation in the exact volume identity is substantial;
raw negative score or residual mass is a much coarser sufficient condition.

Three campaigns remain active at 07:33: PLC atlas session 34983 (363,800
additional cases), corrected repair forked session 44053 (6,863 cases,
1,848 with substantial repair), and corrected repair atlas session 95801
(62,189 cases). Completed.json takes precedence over stale checkpoints.

`notes/chebyshev-signed-mass.md` proves an exact finite-unit-tree obstruction
to a uniform l1 norm assumption in ChebyPush. Recent sparsified-Cholesky and
network-flow paper checks have not supplied a deterministic polylog-overhead
solver or a proved local accelerated obstacle algorithm.

A current unproved idea is to compare against the obstacle optimum with
the same total mass as the current auxiliary state, equivalently the
minimizer over a mass-constrained feasible set. This may separate the
nonexpansive repair on fixed-mass fibers from scalar mass progress. No
moving-comparator potential or convergence theorem is established.

**06:28–07:00 additions:** the repair note now gives an exact quadratic
energy identity retaining five dissipation terms, verified with exact
rational arithmetic on both the old prescribed-state path witness and a
new 426-vertex canonical zero-start unit-tree witness. At its 56th step the
repair port exceeds the old coarse coupling dissipation by a factor above
3,016, while the actual energy contracts. Thus that coarse absorption
shortcut is exactly false. A second exact witness (100-ary depth-4 tree,
alpha=1e-6, rho=1/400000000) disproves the suggestion that repairs only occur
after a total-mass overshoot. Neither witness refutes the algorithm's rate.

The original APC residual-mass sufficient condition and safe-convex-set
interface are written in `notes/residual-mass-and-safe-convex-set.md`.
The deterministic scaling probe is session **21536**, result
`results/averaged-residual-mass-probe.jsonl`; its first short launch had an
index error and was restarted after correction. Initial corrected results
show that raw positive residual mass can be much larger than alpha while
the actual volume ledger remains small. Do not infer a polylog bound from
those finite observations.

New finite searches:
- `results/mass-repair-port-probe/`, session **61564**, started 06:19:43 UTC;
  max port/coarse-dissipation ratio exceeded 9,993 by 06:40 (numerical).
- `results/mass-repair-dense-graph-beam/`, session **2000**, started about
  06:52; deterministic single-edge additions/removals, 24–32 vertex dense
  and sparse starting graphs, alpha in {1/256,1/1024,1/4096}. The older
  `mass-repair-graph-beam` session 78189 was intentionally stopped after
  over 4,000 cases with no substantial repairs; its initial graph families
  did not stress the intended mechanism. This was not an algorithm failure.

The stable implicit-tree replay is complete, including stable quadratic-gap
upper bounds below the solver's cached certificates. Sessions 55760, 58070,
85351 and the short exact-undershoot run are complete. No need to poll them.

At 06:32 the other task requested only proof status. The reply said that no
complete deterministic OP2 theorem is claimed and that convergence remains
open; no route, private formulas, experiments, or files were disclosed.

The local neighbor-oracle implementation completed three finite-tree replays
with enormous ambient sizes (up to about 10^40 vertices), querying only
85–255 vertex degrees. All neighbor calls and cumulative volume were checked.
The binary depth-100 case needed 2,048 iterations and 348,282 adjacency
entries; no global graph array was used. These finite numerical checks
support the implementation ledger, not the missing accelerated-rate theorem.
A stable quadratic-gap external audit now replaces subtraction of nearly
equal objective values in that experiment.

As of 06:14, the corrected forked energy census had 4,135 cases, including
1,115 with substantial repairs, with no non-roundoff positive energy debit.
The corrected atlas had 22,357 cases and no experimental-horizon failures.
The PLC atlas resumed census had 175,081 additional cases. Running job IDs
and absolute result paths below remain unchanged.

**Numerical correction at 05:29 UTC:** dense h must be formed directly,
without cancelling the regularization load. The older extreme-cell H
statistics and repair censuses are marked with numerical-audit notices and
are being replayed. An exact invariant `H<=q mass(x)/(2s)` now checks each
dense step. Exact lemmas and the directly maintained local reporter are
unaffected. The corrected jobs are:

- `results/mass-repair-stable-campaign/`, session 1696;
- `results/mass-repair-stable-energy/`, session 66532;
- `results/mass-repair-stable-forked/`, session 44053.

Their output paths are absolute. The old mass-repair campaign, atlas, and
forked jobs were stopped with SIGINT, preserving all prior logs. The stable
atlas replay has also started; do not count the old raw H values as evidence.

The corrected stable-energy census completed 2,008 cases in 706.50 seconds,
with no detected positive debit above the stated energy cutoff. The separate
24,408-prescribed-state scalar-mass-reserve coefficient grid found no feasible
tested coefficient choice, even for contraction constant 0.1. This rejects
only that finite grid and is not a zero-start counterexample. Its result is
`results/mass-repair-reserve-grid.json`.

The corrected small-graph atlas replay is running in
`results/mass-repair-stable-atlas/`, session 95801, started 05:44:27 UTC.
The score-repair note now gives the full algebraic energy proof and the
constant-step-size extension. A 24,408-state grid at each eta in
`{1,1/2,1/4,1/10,1/100}` still refuted the usual one-step potential on
prescribed states; no zero-start failure is asserted. Results are in
`results/mass-repair-step-size-states.jsonl`.

Accounting qualification: the arbitrary-T `O_tilde(T/rho)` implementation
theorem is in the exact-real model with no global rebases. The floating-point
reporter explicitly charges rebases; their count is polylogarithmic if an
accelerated horizon is proved, but that cannot yet be assumed for arbitrary T.

`notes/mass-preserving-score-repair.md` records a fourth candidate. Repair the
averaged score h to a nonnegative vector with its original signed mass
`B=(1-s)Z+s`, then apply the usual `s rho` soft threshold. The rigorous volume
identity gives cumulative auxiliary row volume at most `T/rho`. Its only
fixed point is the required regularized optimum; its repair map preserves
order and is nonexpansive in weighted l1. Accelerated convergence is OPEN.

The old one-step potential is false for arbitrary feasible states. An exact
rational 128-vertex path witness is saved in
`results/mass-repair-exact-state-witness.json`; this is a prescribed state,
not a canonical zero-start iterate. The correct energy inequality includes
the signed term `alpha ell (X_star-Z_next)`. That term can be positive on
zero-start leaf-seeded stars; it cannot simply be discarded.

`local_mass_repair.py` reuses the checked deterministic AVL score recurrence
and cached certificate with a changed weighted threshold. Its audit passed
822 graph/parameter cases, 131,520 steps, and 822 rebases, checking the actual
volume bound and zero extra adjacency calls for certification. Maximum
optimum-scaled discrepancy was about `5.11e-14`. The explicit iteration cap
is labeled experimental, and the code does not claim a root-time theorem.

New live campaigns:

- `results/mass-repair-campaign/`, session 75104, started 04:54:53 UTC:
  equitable barbells, then radial trees, clique families, and alternating
  suns. Original vertex volumes and output counts are charged. Over 2,200
  bottleneck cases had no experimental root-horizon failure at 05:01 UTC.
- `results/mass-repair-atlas/`, session 32084, started around 05:03 UTC:
  every connected graph through seven vertices, every seed, deterministic
  alpha grid and both sides of numerical homotopy thresholds. Seeds are
  permuted to index zero for the dense audit's horizon convention.
- `results/mass-repair-energy-probe/`, session 6391, started around 05:08 UTC:
  stable quadratic-gap calculation, stopping before energy drops below
  `1e-12 E_initial`, to test the one-step estimate without cancellation of
  nearly equal objective values. This is a numerical falsification audit;
  any strict violation requires higher-precision or exact replay.
  **Completed:** 2,008 cases in 482.51 seconds, no detected positive energy
  debit above the `1e-12 E_initial` cutoff.
- `results/mass-repair-forked-probe/`, session 84716, started around 05:19 UTC:
  unequal paths, branching trees, and dense arms attached to one seed, to
  test interaction between transient modes. Stable gap calculation and
  substantial-repair counters distinguish real repairs from roundoff.

The repair note now includes a proved fixed-auxiliary-support interval
bound: `E_(k0+r)<=q^r(E_k0+s X_star U_outside r/(2 vol(S)))`. Its proof uses
geometric decay of primal history outside S and `ell vol(A)<=H`. The missing
step is amortization over support changes; this conditional bound does not
complete OP2.

At 05:21 UTC, the original PLC atlas and tree-beam jobs were found to have
stopped around 05:06 with FileNotFoundError on relative checkpoint paths.
Their saved case logs remain available. They were resumed with absolute
output paths at about 05:23 UTC:

- `results/plc-atlas-resumed/`, session 34983, skips through the last saved
  tuple `(atlas=600,m=8,seed=2,rho_index=4,mass_cap=False)`.
- `results/plc-adversarial-trees-resumed/`, session 60855, reconstructs the
  alpha=1e-6 beam using cached scores and evaluates only missing cases.

Do not treat the old running checkpoints as active-process evidence. These
were storage-path failures, not mathematical failures. Future jobs should
resolve output paths before starting.

The earlier averaged equitable campaign has completed 3,248 cases, with
maximum observed `rho sqrt(alpha) W_z` about 44.90. Its completed.json is
authoritative over its stale running checkpoint. A separate 72-case alpha
scaling audit finished in `results/averaged-alpha-scaling.jsonl`; raw negative
score mass can grow while actual row work stays small, so bounding raw H
alone may be too coarse. The original PLC atlas and tree beam still run.

Two additional primary-paper audits are recorded in
`notes/positivity-literature-audit.md`. Neither the LIM positivity claims nor
Cheng-Shen's mass-preserving time-discretization stability result supplies
the missing general accelerated optimization theorem.

## Established in this working directory

1. A-CODER has a dimension-independent singleton cyclic smoothness constant
   on canonical RPPR matrices. Its exact-support route is nevertheless
   refuted by a certified dyadic-interval replay on a 255-vertex binary tree.
   See `notes/cyclic-dual-averaging.md` and the exact interval witness JSON.
2. Positive linear coupling with ordinary primal PG and postprojected
   auxiliary state has an accelerated potential and a local PG certificate.
   Its exact volume ledger isolates the signed mass debit `D-s P`. A weaker
   bound `W<=2T/rho+2E_0/(alpha^2 rho^2)` is proved, but does not meet OP2.
3. A distinct averaged variant projects the auxiliary gradient step and sets
   `x^+=(1-s)x+s z^+`. Its moving-domain comparator proves the same root-rate
   potential. Its score has common scalar decay plus sparse local updates.
   An AVL-based weighted threshold reporter and a cached stopping-certificate
   identity give fully charged `O_tilde(T+W_z)` work. Bounding W_z is open.
4. Both positive-coupling variants fail exact-support containment already on
   a single unit edge: `alpha=1/100`, `rho=1/2`, seed 0. The exact optimum is
   `(1/101,0)` with inactive slack `1/10100`, while the third primal iterate
   is `(461/40000,61/40000)`. The mass cap is inactive through these steps.
   This is an algorithm-specific support witness, not a work lower bound.

## Checked implementations

- `local_positive_coupling.py`: only local degree/neighbor access, sorted
  contribution merges, explicit state/projection/output ledger. All 1,233
  small-graph comparisons passed; maximum relative iterate difference
  approximately `2.24e-13`.
- `local_averaged_coupling.py` and `deterministic_avl.py`: common score decay,
  sparse corrections, two AVL maps, weighted rank threshold, charged rebases,
  and accuracy checks at geometrically spaced iterations. The identity
  `p_i=[(1-s)u_i+s h_i-alpha rho]_+` computes the ordinary PG output without
  fresh adjacency scans. The audit passed 720 AVL insertion/deletion orders,
  822 graph/parameter cases, 131,520 recurrence steps, and 822 rebases; largest
  optimum-scaled discrepancy about `1.59e-13`. A second full audit confirmed
  the cached PG identity and zero extra neighbor inspections.
- All validation is deterministic. These floating-point checks do not supply
  a coefficient-bit stability theorem. The two support witnesses have exact
  rational/interval certificates independent of floating-point optima.

## Active computational campaigns

Read the small checkpoint files, not entire case logs. Sources and hashes are
snapshotted before each long run. A duration cap is not a claim of completed
research time; the programs stop if their unique enumeration finishes first.

- `results/plc-atlas-campaign/`: starts 02:31:12 UTC, up to 36,000 seconds;
  connected unlabeled graphs through seven vertices, every seed, deterministic
  alpha grid, both sides of exact-face numerical homotopy transitions, both
  auxiliary projections. Last observed over 197,000 cases; max prefix
  `rho average volume` 1.12. Process session 36171, OS PID 33141.
- `results/plc-adversarial-trees/`: starts about 03:14:30 UTC, up to 36,000
  seconds; deterministic beam search over integer branching sequences to
  challenge `signed debit <= C sqrt(alpha) log(2/rho)`. The displayed
  inequality is a **hypothesis**, not a theorem. Last observed 61,600 cases,
  worst ratio around 0.50. Process session 25133.
- `results/averaged-equitable-campaign/`: starts about 03:29:32 UTC, up to
  36,000 seconds; radial trees, clique chains/levels, and alternating suns,
  charging original vertex counts and degrees. Geometrically spaced accuracy
  checks match a realizable local stopping schedule. Last observed 2,700
  cases and maximum `rho sqrt(alpha) W_z` about 39.07. Process session 61282.

Completed separate censuses:

- `plc-radial-campaign.jsonl`: 6,604 cases; all computed certificates reached.
  Largest observed `rho sqrt(alpha) sum V` about 22.59 capped, 1497.60 uncapped.
  Some capped prefix averages exceeded 21, so per-iterate locality cannot be
  assumed from the small graph-atlas successes.
- `plc-equitable-campaign.jsonl`: completed the finite family list. On very
  ill-conditioned cell graphs, double-precision reference objective error
  becomes visible (e.g. apparent negative relative gaps around 1e-11). Treat
  small signed margins and objective comparisons there as numerical only;
  use higher precision for any adverse history promoted to a claim.

## Current proof targets and cautions

The postprojected candidate needs a bound on accumulated signed projection
debit. The averaged candidate needs a bound on cumulative auxiliary support
volume; its local threshold reporter is no longer an unimplemented oracle.
Mass capping alone proves neither assertion. Potential routes under thought
include a degree-weighted entropy/flux argument or an amortized charge for
outward transient waves. These remain ideas, not established estimates.

The averaged candidate can retain a slowly decaying primal history after its
auxiliary coordinate becomes zero. The sparse reporter avoids rescanning that
history, but this does not by itself control repeated auxiliary activations.
Dense cells with long holding times and branching-sequence searches are meant
to test exactly this issue.

The existing repository's randomized supplied-face SDD primitive is still
excluded. Recent deterministic spectral-sparsification searches, including
arXiv:2608.13910, do not provide a missing polylog-overhead general SDD solver.
Do not substitute an `M^o(1)` factor into a soft-O statement. Do not repeat
existing safe-box, scalar-retraction, projected-CG, or one-pass-peeling claims
without reading their exact failed interfaces in the source notes.

## Next independent checks

Inspect completed campaign summaries and high-precision replay candidates.
Derive a falsifiable whole-run bound, rather than another support-containment
claim. Keep all graph discovery, ordered-tree maintenance, retained state,
certificate checks, output, and any preprocessing in the final work ledger.
The task remains active beyond the minimum window until a valid deterministic
proof exists; no completion claim has been made.
