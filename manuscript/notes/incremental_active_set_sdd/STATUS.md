# Direction status: incremental_active_set_sdd

## Second night, block 8: generic proximal tolerance and canonical ranges

**General OP3 remains Open.** `thm:op3-generic-relative-proximal` proves
the universal inner relative tolerance `1/(33*2^30*kappa^3)` for a supplied
zero-start accelerated invocation. One energy-seminorm induction controls
every model error and contracts the gap by 32, without using the unknown
gap, a positive gap floor, absolute coefficient scale or coordinate bounds
to set the tolerance. The zero-gap case is included. Residual translation
in `cor:op3-generic-residual-restart` permits arbitrary feasible restarts
and signed lower domains. These are **Proved here** drafts awaiting review.

`prop:op3-vwf-canonical-input-gap` proves finite attainment exactly when
the total final slope is nonnegative on a connected supplied graph. A paid
common terminal-ray shift bounds the minimum coordinate without increasing
either the original or normalized proximal objective. With A=sum|f_i'(0)|,
B0=max(U,max(-L_i)) and K=(n-1)/c_min, the initial gap is at most
`A*B0+K*A^2/2`. `cor:op3-generic-canonical-ranges` then bounds every
canonical accelerated coordinate from these input quantities, including
zero total final slope. This does not control all recursively generated
edge or curvature coefficients.

**Source:** CPW Algorithm 9 / Theorem 8.3 supply only the convergence
inequality, and Claim 8.19 identifies the normalized model. The tolerance
and canonicalization arguments are note-local. Every supplied graph scan,
piece copy, vector, failed call and oracle cost remains charged. Dense
exact proximal candidates are validators; the audit's edge budget is an
interface ledger, not a measured fast sparse oracle.

**Measured:** `GENERIC_PROXIMAL_GEOMETRY_AUDIT.json` passes 112 complete
trajectories and 3,584 step certificates in 25.121 seconds. It covers 80
signed-domain runs, 11 zero-gap runs, four zero-total-tail runs, five
infeasible centers, 1,184 negative feasible iterates, 64 oracle shifts by
2^512, and exact trajectory equality under energy scales 2^-80, 1, 2^80.
Earlier full audits and immutable backend hashes are preserved.

**Next falsifiable target:** corrected Lift with exact function constants,
persistent derivative-integral curves, and a valid supplied forest pass.
Resume from the new first section of `CAPPED_INNER_ORACLE_PROBE.md`.
General recursive inner work, numerical propagation, local discovery and
cumulative supplied-graph costs remain **Open**. Formal note dependencies
remain empty; source imports and context are identified in the proof.
Verification is recorded in `OVERNIGHT_20260907_BLOCK8_AUDIT.json` and
`VERIFICATION.md`. The campaign continues until 480 new actual active minutes.


## Historical second-night block 7: explicit proximal accuracy and certified restarts

**General OP3 remains Open.** `thm:op3-explicit-capped-proximal-budget`
proves a parameter-explicit relative oracle tolerance for a supplied original
capped diffusion problem. Earlier feasible iterates bound the next accelerated
center; the normalized oracle guarantee then supplies its absolute model
error; the source convergence inequality bounds the next feasible iterate.
This induction avoids a circular numerical-range assumption. It applies
from any feasible nonpositive-energy starting point with a known gap floor.

`cor:op3-capped-certified-restart-driver` obtains that floor from every
failed original gap certificate, runs the same original capped objective,
boxes the output and restarts. Each run contracts gap by at least 32.
The implemented original certificate stops the driver and certifies its ACL
output. All sparse construction, failed guards, graph scans, new vectors,
boxing and inner-oracle work are retained in the bound. The new results
are **Proved here**, drafts awaiting independent review, conditional on
the explicitly stated inner relative-oracle contracts.

**Source:** CPW Algorithm 9 and Theorem 8.3 supply the accelerated
convergence inequality; their normalized proximal instance is Claim 8.19.
PDF pp. 44 and 50–52 were visually checked. This imports convergence
analysis, not a fast constrained numerical backend or preconditioner builder.

**Measured:** 414 accelerated trajectories with 11,152 complete model and
sublevel checks, including 43 infeasible centers, 36 standalone center
checks, 32 reference optimum coordinates beyond the cap and 30 negative
individual proximal tail slopes. The driver audit passes 277 original cases,
696 guard sandwiches, 419 failed guards with known positive gap floors and
277 original ACL certificates. It checks 142 nonzero restarts and 13,824
inner model contracts. Of these drivers, 135 need multiple runs; the three
cases with eps_appr=2^-30 require four, four and five runs. Dense exact
KKT-piece solves and perturbation searches are validator work. The full
driver audit took 1,393.777 seconds; large exact rationals are recorded
compactly with explicit binary hashes and bit lengths.

**Next falsifiable target:** `CAPPED_INNER_ORACLE_PROBE.md`. A sharper
energy-norm induction suggests the generic relative tolerance
`1/(33*2^30*kappa^3)` for a zero-start source invocation, independent of
unknown absolute energy scale. This is still a **Conditional probe** to
formalize and audit, including zero gap and signed lower domains. A
canonical common-shift normalization may then bound generic coordinates.
The probe also records the checked sign correction in the source Lift
constant, a forest-elimination range induction, and a possible persistent
derivative-curve implementation with exact integral aggregates.

Unknown-support discovery, recursive inner-oracle work and cumulative
supplied-graph costs remain open. Current checks are in
`OVERNIGHT_20260907_BLOCK7_AUDIT.json` and `VERIFICATION.md`. The 103-page
note builds without final warnings. New proof pages 98–101 and changed end
pages 102–103 were visually reviewed. All 48 direction scripts pass focused
lint/format and three registry tests pass. The same baseline failures and
five unchanged file hashes remain. The 480-new-active-minute campaign
continues in its actual-time ledger.

## Historical second-night block 6: global signed compression and original sublevels

**General OP3 remains Open.** `thm:op3-global-vwf-compression` now
implements a scalar compression valid on the entire VWF domain. Tiny
signed breakpoints distribute their curvature between zero and a fixed
nearby breakpoint; a controlled constant shift makes the approximation
one-sided. The final derivative is unchanged. Dyadic compression then
satisfies `F >= F_hat >= 2*F(x/2)-2*xi`, with `xi<=C*tau^2/8` and
O(k+1+log(R/tau)) charged word work. This removes dependence on the
smallest split and on an evaluation radius for this operation. It still
needs a largest-split and curvature/error bound, and tiny curvature weights
may remain. It is not a proof of the source's all-number assumption.

`cor:op3-global-vwf-energy-embedding` gives the exact one-call graph
scaling and additive budget. `lem:op3-original-capped-coercivity` bounds
original feasible sublevels by `lambda*sum(x)-1/(2*bar_alpha)`.
`prop:op3-seed-only-shortcut` returns a certified original ACL output with
one degree query and no adjacency reads when diffusion is weak enough;
remaining cases have `gamma>eps_appr`. These are **Proved here**, drafts
awaiting independent review, with their limited scopes stated in the note.

**Measured:** 1,212 global compressions with 23,000 complete polynomial
overlay intervals, 87,152 finite-interval inequalities, 4,848 infinite-ray
inequalities and exact preservation of every final derivative. Signed splits
reach 2^-2048. The weaker bounded baseline has 1,206 functions and 18,616
full intervals. The original coercivity/shortcut audit checks 1,644 graph
cases, 7,716 complete vertex bounds and three implicit stars with up to
10^30 leaves. Reference graph matrices and optima remain validators.

**Source / context:** CPW's signed geometric argument, Lemma 7.7 and the
proof of Lemma 6.4, was visually checked on PDF pp. 37–39. The new global
regularization and perspective proof are local drafts, not source imports.
The actual normalized proximal instance in Claim 8.19 was reread; absolute
proximal tolerances remain a concrete next target.

**Next falsifiable target:** `GLOBAL_VWF_RECURSION_PROBE.md`. Prove a
single elimination-pass upper-breakpoint bound and a parameter-explicit
absolute-error policy for one original-capped accelerated invocation.
Then trace shifted residual instances and the full recursion/error budget.
Unknown-support graph discovery and cumulative supplied-graph work remain
open even if the numerical source interface is repaired.

Current checks: `OVERNIGHT_20260907_BLOCK6_AUDIT.json` and `VERIFICATION.md`.
The 101-page note builds without final warnings; new pages 94–98 and the
changed end pages 99–101 were visually reviewed. All 46 direction scripts
pass focused lint/format and three registry tests pass. Required project
checks retain the same baseline failures, with all five baseline hashes
unchanged. The eight new active hours remain in progress in the actual-time
ledger.

## Historical second-night block 5: computable certificates and source-objective mapping

**General OP3 remains Open.** `thm:op3-local-gap-certificate` implements
an original-accuracy certificate using only positive candidate rows and
neighbor degree queries. Its deterministic work is
O((1+volume)*log(2+volume)), including failed certificates and false-positive
rows. A separable quadratic model gives a computable upper bound on the
unknown objective gap, with a matching smoothness-factor upper bound;
an explicit source tolerance guarantees acceptance. Candidate production
and cumulative support-volume work remain separate open questions.

`lem:op3-capped-grounding-vwf` repairs the source objective mapping:
CPW's VWF definition requires a linear final tail, so an unmodified positive
quadratic is outside that class. A two-piece capped penalty has the same
optimum, and boxing transfers any relative objective guarantee back.
`prop:op3-positive-face-range-loss` gives an exponentially small exact
Schur coupling on a fully positive physical hub-path face with alpha=1/3
and eps_appr=1/(24n). This refutes unqualified coefficient-range inheritance,
not the source algorithm or OP3. `lem:op3-grounded-edge-pruning` then bounds
energy and coordinate error from removing small total edge weight, including
boxed approximate candidates. Exact support can change. All four results
and the gap-sandwich lemma are **Proved here**, drafts awaiting review.

**Measured:** 16,506 independent gap and graph-access checks across 1,233
original cases, including 12,807 accepted and 3,699 charged failed
certificates; all 11,574 candidates meeting the sufficient source accuracy
pass. Four implicit stars with up to 10^30 leaves read one leaf row only.
The range/pruning audit checks 550 supplied cases, two designed support
changes, 2,576 boxed approximate candidates, 45,870 capped-VWF inequalities
and hub paths through 257 physical vertices. Exact full matrices and
candidate generation remain validator work, distinct from the certificate.

**Source / context:** CPW Definition 3.2 was checked visually in PDF p. 14;
Fact 7.2 and the scalar compression proof still use a bounded breakpoint
range. New source-objective mapping and pruning do not discharge that
recursive obligation. No fast constrained solver is imported.

**Next falsifiable target:** `BOUNDED_VWF_COMPRESSION_PROBE.md`. Test
snapping small signed split points to zero while retaining curvature,
combine its additive error with the source's geometric compression, and
prove bounds on all required fields and cumulative error. The known
original potential box does not bound every accelerated or shifted query.
Local graph construction remains open even if the supplied solver is repaired.

Current checks: `OVERNIGHT_20260907_BLOCK5_AUDIT.json` and `VERIFICATION.md`.
The 97-page note builds without final warnings; pages 3 and 90–97 were
visually reviewed. All 43 direction scripts pass focused lint/format and
three registry tests pass. Required whole-project checks retain the same
unrelated baseline failures. The eight additional active hours remain in
progress in the separate actual-time ledger.

## Historical second-night block 4: residual-paid updates and diffusion accuracy

**General OP3 remains Open.** The new generic result is an accuracy
conversion, not a local solver. `lem:op3-diffusion-energy-scale` gives a
known negative objective scale for the nontrivial ACL case.
`thm:op3-diffusion-accuracy-bridge` proves that a feasible relative-energy
approximation with `eta=bar_alpha^2*(eps_appr/8)^2`, followed by downward
clipping, satisfies every original ACL residual inequality and retains
only true obstacle-support coordinates. These are **Proved here** drafts
awaiting independent review. Producing and certifying that candidate with
local total work remains open.

The bounded two-star admission probe has a useful positive conclusion:
`prop:op3-harmonic-union-stream` charges genuine changed-response events
against the original residual mass of remaining twins. J supplied union
updates stream at most `2*J+2*H_J/lambda` events. This prices the union
operation with available input curves; it does not price their construction
or give a complete local module solver. A naive cumulative obstruction
from this family therefore fails for the measured mechanism.

**Measured:** the union audit passes 96 legal original-degree trajectories,
6,712 positive core admissions, 2,047 twin residual budgets and 216,453
complete affine-piece identities. The accuracy audit passes 1,233 original
graph cases and 11,574 candidate-to-ACL certificates, with 3,291 clipped
false-positive coordinates. Full curve builds and candidate generation
are separately identified reference work. Saved records are
`MODULE_ADMISSION_COST_AUDIT.json` and `DIFFUSION_ACCURACY_BRIDGE_AUDIT.json`.

**Source / context:** the original p-norm flow theorem retains degree and
Dirichlet-curvature factors. A unit-weight path exactly refutes a proposed
minimum-edge-weight curvature bound, under both L and 2L conventions;
it does not refute an unspecified source parameter or prove an OP3 lower
bound. Chen–Peng–Wang still requires local-construction and intermediate
numerical-range arguments. Primary page pointers and metadata are
synchronized in `docs/literature/`; no new fast solver is imported.

**Next falsifiable targets:** `DIFFUSION_SOURCE_CERTIFICATE_PROBE.md`:
trace intermediate tolerance requirements, seek a computable certificate,
and charge local construction and cumulative supplied-face work. Use the
completed audits rather than repeating them. Further special graph classes
are not the main next block.

Current checks: `OVERNIGHT_20260907_BLOCK4_AUDIT.json` and `VERIFICATION.md`.
The 93-page note builds without final warnings; pages 3 and 87–93 were
visually checked. All 41 direction scripts pass focused lint/format and
three registry tests pass. Required whole-project checks retain the same
unrelated baseline failures, whose five files have unchanged hashes.
The new eight-hour campaign remains ACTIVE in its actual-time ledger.

## Historical second-night block 3: strict reporting and known-child removal

**General OP3 remains Open.** Two missing algebraic interfaces are now
implemented and **Proved here**, as drafts awaiting independent review.
`thm:op3-module-reporter` gives a constant-work strict due/quiet query on
fixed supplied responses. Updating a positive core target or recovering a
coordinate costs O((1+d_i)*log(2+N)); original degree pays for the cotree
path. Arbitrary common fields and target increases or decreases are allowed.
Dense indexed heaps retain no stale history. This does not update a graph.

`lem:op3-module-summand-removal` removes a known convex zero-left summand
in O((1+k_child)*log(2+k_total)) exact-real word work and allocated words,
streaming only that child. Signed suffix shears are locally certified;
zero jumps are deleted with persistent AVL deletion. The original curves
remain intact. `cor:op3-module-child-extraction` applies this in the correct
union/join field, retaining original diagonal degrees.

**Measured:** the reporter passes 1,716 original graph executions,
121,344 independent original-matrix queries, 30,336 strict equality checks,
9,540 degree/depth certificates and 15,102 old-version checks. Seventeen
structural diagnostics include 512-core combs, cliques, stars and root
unions, plus a singleton. Removal passes 2,000 seeded synthetic sequences,
2,231 supplied child extractions, 179,816 complete affine-piece identities
and 165,113 AVL node checks. Counts describe overlapping tests and are not
numbers of distinct graphs. Exact records are `MODULE_VALUE_REPORTER_AUDIT.json`
and `MODULE_CURVE_REMOVAL_AUDIT.json`; no floating-point claim is inferred.

**Source / context:** the Shamir–Sharan cograph structure theorem was
checked in its author PDF and synchronized in `docs/literature/`. It
supports degree-paid structural updates, but does not update obstacle
responses. No source is imported into the new fixed-response or removal
proofs, and the formal note dependency array remains empty.

**Next falsifiable target:** `MODULE_ADMISSION_COST_PROBE.md`. Test genuine
changed-curve work at union nodes under legal positive admissions. Its
possible residual-mass charge may prevent a naive repeated-rebuild
counterexample; the association between event complexity and paid residual
is still open. Then return to the arbitrary-graph sparse coarse certificate
and constrained-diffusion directions. The triangle-to-paw witness still
refutes keeping all old induced-active modules intact.

Current checks: `OVERNIGHT_20260907_BLOCK3_AUDIT.json` and `VERIFICATION.md`.
The 88-page note builds without final warnings and the new proof pages
were visually reviewed. All 39 direction scripts pass focused lint/format;
registry tests pass. Repository-wide checks retain the same unrelated
notation/inventory/lint failures. No active-manuscript/shared-ledger
promotion occurred. The eight-hour campaign remains ACTIVE in its separate
actual-time ledger; prior-night time is excluded.

## Historical second-night block 2: persistent recursive responses

**General OP3 remains Open.** The new supplied-decomposition result is
`thm:op3-persistent-modules`: complete recursive union/join core responses
and final core recovery in **O(N*log^2(2+N)) exact-real word work and
allocated words**, including all retained old versions. This is **Proved
here**, a draft awaiting independent review. The input includes a reduced
decomposition, original degrees and private-leaf counts; local discovery
is not included. The earlier explicit implementation has the weaker
O((N+m_core)*log(2+N)) bound, with its distinct-edge charge retained.

The persistent implementation reuses the existing immutable affine AVL
primitives and adds zero-left-ray merging and legal positive/negative join
shears. It passes 1,716 original graph cases, 50,268 retained affine-piece
matches, 22,530 saved curve versions and 100,500 coordinate recoveries,
alongside 50,250 independent whole-interval original certificates. Eighteen
comb/clique/star diagnostics reach 512 core vertices. Counts overlap and
are executions/versions, not additional distinct input graphs.

Read `RECURSIVE_MODULE_RESPONSE_PROBE.md` and the authoritative proof
`sections/op3_recursive_modules.tex`. Next resume
`MODULE_REPORTER_AND_UPDATE_PROBE.md`: audit the degree-paid depth bound
and exact fixed-module event reporter, then changing module membership.
The saved triangle-to-paw example gives a legal positive admission that
breaks an old induced-active module, so keeping every old module intact is
not a valid general update interface. Curve replacement remains a separate
cost even if graph recognition is cheap.

The scoped primary-source check in `docs/literature/lcp-solvers.md` covers
related persistent curve primitives and dynamic min-cost-flow thresholds.
Those flow guarantees have different certificates and explicit
subpolynomial overhead, so no direct OP3 import is asserted. The literature
index is synchronized; no source PDF or new cross-note proof edge was added.
The note registry still has `depends_on=[]` and no active-manuscript/shared-
ledger promotion occurred.

Current checks are in `OVERNIGHT_20260907_BLOCK2_AUDIT.json` and the latest
`VERIFICATION.md` entry. The same-task heartbeat remains ACTIVE for the
480-minute second-night campaign; see its separate actual-time ledger.

## Historical second-night block 1: local multipartite solver

**General OP3 remains Open.** The user requested 480 additional active
research minutes on 7 September. The current campaign is tracked in
`OVERNIGHT_20260907_STATUS.md` and `OVERNIGHT_20260907_WORK_LOG.json`;
none of the completed first-night 601.407 minutes count toward it.

**Proved here**, draft awaiting independent review:
`thm:op3-canonical-multipartite` gives a complete original-degree/adjacency
solver for promised complete multipartite cores with unequal private leaves,
for every physical seed. No partition, core size or minimum core degree is
supplied. Work is `O(1+cvol(U)*log(2+cvol(U)))`, space is `O(1+cvol(U))`,
in exact-real words. Separately, this yields ACL `O_tilde(1/eps_appr)` at
lambda=eps_appr/2 and exact RPPR `O_tilde(1/rho)` at lambda=rho. It has
no imported fast SDD or dynamic-tree primitive and no bit-cost claim.

**Measured:** the actual narrow engine passes 3,640 full original obstacle
comparisons and 16 implicit certificates. Its canonical/any-seed extension
passes 4,840 explicit comparisons and 56 implicit certificates, with all
scanned rows positive, exact gate ties and independently audited restricted
solutions. The two audits overlap in graph coverage; their counts are not
claims of distinct graph instances. See `LOCAL_MULTIPARTITE_PROBE.md` and
`sections/op3_local_multipartite.tex` for the mechanism and scope.

**Next falsifiable target:** `RECURSIVE_MODULE_RESPONSE_PROBE.md` derives
candidate union/join response transformations and a distinct-core-edge
charge for intermediate copying. Audit both before claiming a work theorem. The
partition-discovery theorem does not extend automatically to recursive
modules. Revisit generic sparse coarse response/certification and primary
sources after this bounded probe; reducing the repeated rank-dependent
coarse writes remains the arbitrary-graph blocker.

**Formal dependencies:** existing note registry `depends_on=[]`; all new
proof imports are within this direction. **Context/provenance:** the saved
multipartite probe and earlier clique result; no shared-ledger or active-
manuscript promotion. The first-night synthesis below is preserved as
history. Current verification is recorded in `VERIFICATION.md` and
`OVERNIGHT_20260907_BLOCK1_AUDIT.json`.

## Historical first-night final block (14)

**General OP3 remains Open.** The current decision document is
[OP3_MORNING_DECISIONS_20260907.md](OP3_MORNING_DECISIONS_20260907.md).
All positive results below are **Proved here** as drafts awaiting independent
review; no active-manuscript or shared-ledger promotion has occurred.

The sparse certified coarse construction replaces the dense inverse and
proves expected ACL work `E[W]=O_tilde((1+E[r])/eps_appr)`; a fixed containing
obstacle-support rank bound `R` gives `O_tilde((1+R)/eps_appr)`.
See `thm:op3-certified-linear-rank` and
`CERTIFIED_COARSE_PUBLICATION_AUDIT.json` (67,856 original ACL executions).
Online top-tree balancing and the fast sparse SDD solver remain explicit
**Source** imports. Exact reference substitutions audit application logic,
not those sources' fast performance. The construction may stop early and
has no exact RPPR or OP2 consequence.

A separate fully implemented scalar sweep solves promised clique cores
with arbitrary unequal private leaves and a core seed in local
`O(cvol(U)*log(2+cvol(U)))` exact-real word work. It has 1,464 explicit
original obstacle comparisons and six implicit original-equation checks;
see `thm:op3-local-clique-pendants` and `LOCAL_CLIQUE_PENDANT_PROBE.md`.
It handles the dense family that forces cubic complete-vector writes under
the fixed absolute-budget refresh policy. Sparse residual epochs and a
geometric-supersolution counterexample identify representation-specific
failures, not universal OP3 lower bounds.

The recommended next bounded target is **Conditional / Open**:
`MULTIPARTITE_CORE_PROBE.md`. Its supplied-part scalar algebra is implemented
and audited (261 original obstacle comparisons); local part discovery and
incremental event maintenance still need a complete construction. General
OP3 additionally requires avoiding repeated rank-dependent coarse writes,
all-component searches and cycle-triggered reconstruction.


## Historical block 13 checkpoint

The following checkpoint records the earlier state. Its certified-solve next
probe is completed by block 14 above; subsequent old probes and statuses
are retained as development history.

**Proved here, awaiting independent review:** `thm:op3-coarse-publication-acl`
uses the component reporters as a geometric-value producer and removes the
revealed-cycle-rank q term. Its ACL-only exact-word work is
`O_tilde((1+r^2)/eps_appr)`, where r is the cycle rank inside the actually
reached positive support. It pays for cached incidence redelivery, failed
producer searches, geometrically grown parent buffers, source callbacks,
cycle rebuilds and current inverse updates. Publications leave the inverse
unchanged. Old whole port-value snapshots are released; immutable application
records are included in the space bound. The online top-tree balancing
algorithm remains an explicit **Source** import.

**Measured:** `COARSE_PUBLICATION_AUDIT.json` passes 54,240 atlas executions,
twenty larger explicit cases, five implicit private-star cases and twenty-four
shared-pair-star cases. It checks 217,135 independent admission faces and
inverse certificates, 3,221,573 due-row signs, 1,379,835 original boundary
bounds and 500,887 publication-only inverse invariance checks. There are 542
terminal points strictly before the exact obstacle optimum; all satisfy ACL.
The largest implicit example has 4,240,252,449 vertices but reads only 33
active rows (1,056 original incidences); its support rank is zero and its
revealed rank is 496. It makes 33 publications and 1,056 cached deliveries,
with zero exceptional-candidate gate scans, versus 5,456 old direct checks.
This algorithm is not an exact-RPPR algorithm and gives no OP2 conclusion.

**Proved here / Measured:** `COARSE_SCHUR_DOWNDATE_PROBE.md` derives an
at-most-two-coordinate ordinary coarse Schur downdate and a determinant
budget spanning all permanent and temporary port changes. Its audit checks
6,472 actual source-driven traces and 11,668 sparse-update identities. The
budget alone is not a maintained-solve work theorem.

**Next Open target:** `CERTIFIED_COARSE_SDD_PROBE.md` specifies approximate
port bands certified by a sparse original coarse residual, downward terminal
repair, and a possible source-backed expected linear-rank ACL bound. That
composition is not yet implemented or proved as an end-to-end theorem.
General OP3 remains **Open**; no active-manuscript promotion has occurred.


Last reviewed: 2026-09-07

The new exploration is a proof draft, not independently reviewed.

State: proved-open

## Earlier maintained coarse inverse result

**Proved here, awaiting independent review:** `thm:op3-maintained-coarse-inverse`
completes the selected-Green transaction and improves active-cycle-rank
work to

`O(1 + V*((1+r)*L^4 + (1+r)^2 + q*L^2))`.

The ACL consequence is O_tilde((1+r^2+q)/eps_appr). Separately, the same
exact-obstacle algorithm gives O_tilde((1+r^2+q)/rho) exact RPPR work.
The graph, access and exact-real word model are unchanged. The proof pays
for every old-port promotion, old-version response query, temporary parent,
dense update, restriction copy, source rebuild, quiet gate and final output.
The finer trajectory ledger uses cycle-birth count b and retained count p:
O(1+V*((1+b)*L^4+(1+p)^2+q*L^2)). Only the current dense inverse is retained;
all historical application versions and their old port values are charged
within the stated r-based space bound.

**Measured:** `MAINTAINED_COARSE_INVERSE_AUDIT.json` passes 54,240 atlas
executions on all 995 connected graphs through seven vertices, every seed,
four parameter pairs and two policies; twenty larger explicit cases, five
implicit private-star cases and the exact triangle witness also pass.
There are 217,490 independent inverse certificates, checking 2,295,640
entries of J*K=I against original-matrix Schur elimination, 483,416 explicit
original-gate checks plus 859 implicit-case gates, and 198,003 historical
component rechecks. Atlas updates include 21,543 temporary-parent drops,
5,858 newly promoted Steiner junctions, up to five simultaneous old
promotions and six active parents. No coarse solve feeds an admission.
Reference hierarchy rebuilding and full validation remain separately
charged; the fast online balancing algorithm is an explicit Source import.

**Next Open target:** `COARSE_PUBLICATION_PROBE.md` proposes using the
component reporters as the previously missing geometric-publication producer.
It may remove repeated exceptional-gate scans and the q term for ACL work.
The proposal must replace tuple-copying parent lists, count cached-edge
redelivery and publication-only payload updates, and distinguish current
inverse storage from optional historical port-value snapshots. The final
point may stop before the exact obstacle optimum, so no exact-RPPR or OP2
consequence is asserted for that proposed variant. General OP3 remains Open.

## Earlier coarse-factorization variant

**Proved here, awaiting independent review:** `thm:op3-local-cycle-rank`
gives a local exact obstacle algorithm on arbitrary finite simple connected
unweighted graphs with explicit support parameters r and q. Here r is the
cycle rank inside the final positive support and q is the rank of the graph
revealed by its scanned incidences, excluding edges between inactive vertices.
For V=cvol(U) and L=log(2+V), the work is

`O(1 + V*((1+r)*L^4 + (1+r)^3 + q*L^2))`.

This gives O_tilde((1+r^3+q)/eps_appr) ACL and exact
O_tilde((1+r^3+q)/rho) RPPR. Shared-port copies, duplicate diagonal/load
corrections, exceptional gates, cycle-birth repartitioning, matrices, failed
checks and final output are paid. The online top-tree balancing remains an
explicit **Source** import. The implemented audit rebuilds its reference
hierarchies and separates those costs.

**Measured:** `LOCAL_CYCLE_RANK_CLUSTER_AUDIT.json` passes 54,240 executions
on all 995 connected atlas graphs through seven vertices, every seed, four
parameter pairs and two policies. Twenty larger explicit examples and five
finite implicit private-star examples also pass. They check 217,410 positive
faces, 168,368 independent coarse Schur systems and 483,413 original gates.
The atlas includes 33,074 admissions creating multiple cycles and 3,441 quiet
exceptional checks. The implicit graphs scan only 58/51/48/62/70 entries.

**Proved here / Measured:** `sec:op3-cluster-green` obtains selected
conditional inverse entries from stored scalar elimination records.
`CLUSTER_GREEN_QUERY_AUDIT.json` checks 29,408 affine/variance identities
and 123,844 covariance pairs against 2,664 independent conditional inverses.

**Next Open target:** `COARSE_INVERSE_UPDATE_PROBE.md` specifies a maintained
coarse inverse: ordinary rank-one updates, old-port promotion, one border
containing every active parent, and optional removal of the transient
insertion parent. This was the block-11 next target; the completed transaction and r^2 bound
are now recorded above. General OP3 remains Open, and every new proof draft
still awaits independent review.

## Earlier local unicyclic result

**Proved here, awaiting independent review:** `thm:op3-local-unicyclic`
extends the local exact obstacle/ACL construction to every finite simple
connected unweighted unicyclic graph, with an arbitrary physical seed and
unbounded tree attachments. Its exact-word work is
O(1+cvol(U) log^4(2+cvol(U))) and its space, including historical application
versions, is O(1+cvol(U) log^3(2+cvol(U))). This gives O_tilde(1/eps_appr)
ACL and exact O_tilde(1/rho) RPPR in the nonzero regime.

The new ingredients are a charged named-coordinate query, the unique
exceptional two-parent candidate, one paid re-rooting at cycle closure, and
uniform-shift restoration at two fixed ports. Every unsuccessful gate check,
original graph query, payload change, historical allocation and final output
is included. The published height-bounded balancing algorithm remains an
explicit **Source** import; its fast online implementation is not supplied.

**Measured:** `CLUSTER_POINT_QUERY_AUDIT.json` checks 58,816 named coordinates.
`LOCAL_UNICYCLIC_CLUSTER_AUDIT.json` checks 3,888 atlas executions over all
78 tree/unicyclic graphs through seven vertices, plus sixteen larger explicit
attachment executions and four finite implicit private-star examples. There
are 16,371 independent face solves, 26,043 original gate checks, and 319
negative uncorrected spanning-tree faces. The implicit examples scan only
27, 51, 45 and 48 original entries. Reference hierarchy rebuilding and full
validation recovery are counted separately from the proposed online work.

**Next Open target:** `BOUNDED_CYCLE_RANK_PROBE.md` proposes partitioning the
active spanning tree into O(q) two-port components, glued by a small coarse
system, where q is the cycle rank of the locally revealed graph. Multiple
exceptional candidates and paid repartitioning must be audited before a new
theorem is stated. Arbitrary-graph OP3 remains Open; no manuscript promotion
or independent review has occurred.

## Earlier complete tree result

**Proved here, awaiting independent review:** `thm:op3-local-top-tree`
gives a deterministic exact obstacle/ACL algorithm on arbitrary trees with
O(cvol(U) log^4(2+cvol(U))) local exact-real word work and
O(cvol(U) log^3(2+cvol(U))) space, including every retained version.
Graph discovery, home-edge payloads, failed queries, all cluster operations
and final output are charged. The source balancing algorithm is imported;
the complete application callbacks are implemented and exactly audited.
This implies O_tilde(1/eps_appr) tree ACL work and exact O_tilde(1/rho)
tree RPPR work in the nonzero regime. It is not a numerical-stability claim.

**Measured:** `TOP_TREE_CALLBACK_AUDIT.json` checks 650 source-valid faces,
167,384 legal binary joins, 26,130 independent Schur oracles, 168,294 valid
summaries, 650 exposure transitions and 1,296 payload refreshes. Supplied
hierarchy enumeration is reference work, not the published online algorithm.

**Proved here / Measured:** a uniform shift C=1/bar_alpha makes every
cluster load negative while allowing the physical seed to be interior.
The geometric root may therefore differ from the seed. The exact shifted
reporter and one-cycle restoration identities are in
`sec:op3-shifted-tree-clusters`; 564 faces check 33,550 conditional identities
and 1,972 valid physical-seed-interior clusters. Two cycle witnesses pass.

**Resolved next target:** `UNICYCLE_TOP_TREE_PROBE.md` preserves the plan for local unicyclic
continuation: one exceptional two-parent candidate, a charged point query,
one paid re-rooting at cycle closure, two fixed cycle ports and the corrected
root solve. A triangle witness proves that the uncorrected spanning-tree
response can be negative; retain signed affine responses. Arbitrary-graph
OP3 remains Open. No result has been promoted to the active manuscript.

## Earlier threshold result

**Proved here, awaiting independent review:**
`lem:op3-root-resistance-transform` and `cor:op3-root-coordinate-update`
give exact ancestor-group affine threshold maps and harmonic/resistance
updates on canonical rooted trees. `ROOT_THRESHOLD_ORDER_PROBE.md` records
22,440 exact traces and 406,131 coordinate/Green checks.

**Refuted, representation-specific:** a stale minimum certifies exact
quietness, even under minimum-threshold admissions. Two nine-vertex
witnesses separate FIFO and minimum policies. A fifteen-vertex legal trace
also misses an original ACL violation by a factor about 1.06386. These are
not failures of the implemented physical-flux queues. The exact interval
search covers 13,179 minimum-policy sequences through eleven vertices;
a minimum-policy ACL guarantee remains Open beyond that finite evidence.

**Follow-up:** adjacent-path separation and the projective primitive are now
implemented and proof-drafted. The precise remaining top-tree import is
recorded in `ORDERED_PATH_CLUSTER_PROBE.md`.

## Latest constructive result

**Proved here, awaiting independent review:** `thm:op3-live-core-peeling`
in `sections/op3_live_core_peeling.tex` replaces the permanent branching
count by maximum simultaneous core size q. Removing a nonseed vertex of
current reduced degree at most two moves at most one grouped physical
flux. It gives `O_tilde((1+q^2)/eps_appr)` word work and `O(V+q^2)` storage,
including failed queue visits and inverse deletion. See
`LIVE_CORE_PEELING_PROBE.md`.

**Measured:** 54,240 exact comparisons, 50 larger/targeted cases, 15,476
inverse-entry checks and 8,497 physical-group checks pass. Groups of up to
64 original boundary incidences move without membership copies in the
solver. On the 127-vertex completed binary tree, LIFO reduces the peak core
from FIFO's 64 to 7 and inverse updates from 167,743 to 1,344.

**Refuted, representation-specific:** degree-two peeling plus LIFO always
has polylogarithmic live-core size. `prop:op3-live-core-interior-tree` forces
a full depth-h prefix while original leaves at height `3h+5` remain inactive.
No first peeling step is possible. The explicit inverse needs
`Omega((1/eps_appr)^(log_6 8))` writes for this family. Ten exact cases
include a 2,097,151-vertex implicit ambient tree with only 127 positive rows
and 674,751 inverse updates. This does not lower-bound OP3 or other solvers.

**Follow-up completed:** fixed-lambda root thresholds and their group maps
are now audited in `ROOT_THRESHOLD_ORDER_PROBE.md`; the next constructive
question is the ordered path-cluster probe above.

## Earlier growing-core backend

**Proved here, awaiting independent review:**
`thm:op3-branch-core-flux` in `sections/op3_branch_core_flux.tex` handles
a growing retained branching core with scalar physical-flux queues. It
returns ACL output using `lambda=eps_appr/2`, with
`O(|U|r^2 + r vol(U) + vol(U) L log(2+vol(U)))` exact-real word work,
where `r` is the returned retained-core size and
`L=1+log_+(1/(bar_alpha eps_appr))`. Storage is `O(vol(U)+r^2)`.
All event searches are paid; polynomial costs remain in the dense inverse
and in scanning all retained queues. It reads precisely positive output rows, including on
arbitrary ambient graphs. See `BRANCH_CORE_FLUX_PROBE.md`.

**Measured:** 27,120 exact face/obstacle comparisons and 17 additional
residual diagnostics pass, including threshold equality, shared reports
from 16 retained vertices, and the prior Schur-cancellation examples.
On a 102,707-vertex shared-report graph, it scans 271 positive rows and
878 entries. Intermediate audits separately check 9,717 inverse entries,
4,345 physical fluxes and 3,253 shared gate sums.

**Proved here, representation-specific:**
`prop:op3-dense-core-binary-tree` forces cubic inverse writes for this
backend on balanced trees with full required support. Four exact cost
diagnostics through 127 vertices verify the accounting. This is an easy
family for other representations, not a lower bound for OP3.

## Earlier exact support theorem

**Proved here, awaiting independent review:**
`thm:op3-two-port-frontier` in `sections/op3_two_port_frontier.tex` gives
`O((1+vol(S)) log^4(2+vol(S)))` exact-real local work when the positive
support has at most one nonseed vertex of degree at least three. The solver
discovers the retained vertices itself, scans precisely positive-support
rows, and never explores an inactive attachment. A second nonseed branching
activation is detected as outside this class before its row is read.

**Measured:** 8,329 exact comparisons and nine larger KKT checks pass;
18,791 outside-class cases are correctly detected. A 66,162-vertex shared
report graph requires 98 row scans and 258 adjacency entries. The actual
planar reporter passes 5,136 extreme checks and 1,606 independent static-chain
checks. See `TWO_PORT_FRONTIER_PROBE.md` and the durable audit files.

**Refuted:** a constant-relative normalized Schur extreme query alone
certifies original ACL quietness. Three source-valid two-arm traces satisfy
the 1.1 approximate-return contract at every admission, yet allow a quiet
return with the other boundary residual above the requested tolerance.
See `SCHUR_RELATIVE_REPORTER_PROBE.md`; original-value geometric reporting
is not refuted by this different normalization.

**Open:** remove the polynomial cost of a growing retained branching core,
including finding due scalar thresholds without rewriting all retained
values. A hierarchy that eliminates its vertices still needs paid changes
of old boundary coordinates. The source 3D extreme-query contract is now
reconciled, but its backend is not implemented here. The earlier stable-port reporter and
rooted-spider results are explicitly identified as provenance; the new
structural work proof and AVL implementation are self-contained drafts.

## Overnight continuation

The user has authorized ten additional active research hours. Resume from
[`OVERNIGHT_STATUS.md`](OVERNIGHT_STATUS.md) and its work log. The first block
produced an affine-composition-tree mechanism for supplied tree responses.
The next block implemented its persistent AVL representation and proved the
supplied-tree `O(n log^2 n)` word-work bound as a draft; see
`TREE_AFFINE_PROBE.md` and `thm:op3-persistent-tree`. It also implemented a
fully local exact solver on cycles with unequal pendant-leaf counts and an
arbitrary seed, with `O_tilde(1/eps_appr)` ACL work on that promised family;
see `LOCAL_CYCLE_PROBE.md` and `cor:op3-local-cycle-acl`. All 1,152 tree and
5,265 cyclic exact comparisons pass. These claims await independent review.
An exact length-two-attachment witness refutes automatically freezing more
general attached trees. The third block handles delayed changes by retaining
a bounded region near each active end: `thm:op3-bounded-attachments` gives
`O_tilde(q^3/eps_appr)` work for a cycle seed and attachment size q, without
supplying q or the cycle ports. Its 1,909 exact comparisons and eight larger
KKT checks pass. The q dependence remains real for this implementation:
`INACTIVE_ATTACHMENT_AUDIT.json` shows full classification reading an
arbitrarily large inactive star while support volume stays three. A direct
initial gate check avoids that particular witness. This is a representation
obstruction, not a lower bound for local solvers. Local discovery and cyclic response maintenance at
the general OP3 scale remain open. Existing lazy tree iterators already
achieve the weaker product scale by paying for ancestor walks.

## Current OP3 exploration

The current direction comparison is
[`OP3_DIRECTIONS_20260906.md`](OP3_DIRECTIONS_20260906.md). The previous
contract and history below remain useful for the literal source interface.
The new finite-band interface intentionally allows a different safe trace.

- **Proved here, awaiting independent review:**
  `lem:op3-response-size`, `thm:op3-geometric-recipient`, and
  `lem:op3-terminal-repair` in `sections/op3_geometric_events.tex`.
  With `lambda=eps_appr/2`, geometric publications have total recipient work
  `O_tilde(V[1+log_+(1/(alpha eps_appr)))+1)`. Terminal completion is one
  expected near-linear certified SDD solve and a downward repair, returning
  the ACL witness with support volume at most `2/eps_appr`.
- **Proved here, awaiting independent review:** the rescaled obstacle optimum
  grows as teleportation decreases, but a three-vertex path acquires new
  support under a factor-two matrix change. There is no pointwise
  multiplicative warm-start bracket from spectral comparability alone.
- **Conditional:** an output-sensitive producer for the required geometric
  publications would resolve the broader OP3 complexity target. This does
  not reproduce the literal Wei--Yang gate or solve arbitrary dynamic
  inverse queries.
- **Measured:** 19,440 exact rational trace checks and 64,400 terminal
  perturbation checks passed. Dense reference solves supply the missing
  producer; these counts do not establish a fast implementation.
- **Open:** produce the value intervals, locate all due publications and
  certify quietness with total `O_tilde(V+1)` local work, including every
  unsuccessful search. Near-linear recipient work is not producer work.
- **Source alternative:** Chen--Peng--Wang's generalized diffusion algorithm
  supplies a randomized near-linear *global* constrained solver under a
  polynomial numerical-range assumption. Locality and parameter range both
  require new work; source pointers are in
  `docs/literature/lcp-solvers.md`.

**Next falsifiable target:** build the producer on an asymmetric cyclic
family with growing attachments and surviving old boundary keys. Meter
response production and event location separately from delivery. A full
old-face scan at every small admission fails this implementation target.
The secondary route is local constrained elimination; teleportation
continuation is a lower-priority probe.

**Concrete overnight refinement:** bounded attached trees are now covered by
a complete proof draft. The two-retained-vertex construction now avoids
whole inactive attachments, including on a genuinely activating asymmetric
branch. A growing core now has a complete scalar physical-flux reporter,
with an explicit dense inverse cost. Next remove that response cost and
the full scan of retained queues, or maintain changing separator coordinates
with every transformation and failed certificate charged.
The stronger Chebyshev saturation comparison passes 6,155 exact polynomial
checks through q=9 but remains **Open** for arbitrary q; improving this factor
alone would not resolve the discovery gap. The supplied-tree ACT does not
itself give a growing-tree event dictionary or a bulk-transformed threshold
hull. The new planar primitive supports individual changes in stable
coordinates; it does not supply that stronger interface.

Formal registry dependencies remain unchanged: the new reduction uses its
own elementary arguments and the supplied-face SDD source. No new claim is
promoted into the shared results or active manuscript. The detailed checks,
coverage and elapsed research time are in `VERIFICATION.md` and
`EXPLORATION_COVERAGE.json`.

## Exact question and contract

- **Question:** Can the Wei--Yang growing-active-set method reuse exact old-face
  state without repeated materialization or global boundary refresh on arbitrary
  graphs?
- **Model:** Map the shared lazy system to Wei--Yang's degree form by `bar_alpha = 2 alpha/(1+alpha)`, `x = D^(1/2) z`, with `rho` unchanged. For `M = D-(1-bar_alpha)A`, residue `r(z)=s-bar_alpha^(-1)Mz`, and exact restricted state `z[U]`, admit `v` when `r(z[U])_v > (lambda+kappa)d_v` (`main.tex:98-152`).
- **Accuracy namespace:** With `lambda=kappa=epsilon/2`, the exact path gate returns a deterministic ACL `epsilon`-approximation. With `lambda=rho` and `kappa <= min(rho,xi/bar_alpha)`, it returns RPPR objective gap at most `bar_alpha kappa <= xi` and ACL error `rho+kappa` (`main.tex:417-455`). These are source/native namespaces, not the repository's final `eps_ppr` convention.
- **Access and charged work:** Charge one word per materialized coordinate, degree work for every adjacency scan, all updates and violation queries, and one final output. The path algorithm costs `O(cvol(U_J)+d_next)`; the general interface costs `O(I(U_K)+cvol(U_K))` (`main.tex:51-56,361-415,471-501`).
- **Intended result:** A high-probability arbitrary-graph `Violations`/`Expand`/`Finalize` data structure with total `O_tilde(cvol(S*)/sqrt(alpha) polylog(1/(rho xi delta)))`; the stronger output-linear bound remains open (`main.tex:541-555`).

## Claim ledger

- **Source:** Wei--Yang arXiv:2608.16339v1 gives ACL work `O_tilde(1/epsilon^2)` and RPPR work `O_tilde(|S*| vol(S*))`, and explicitly leaves incremental reuse open (`main.tex:154-182,591-597`).
- **Proved here:** Exact block-Schur correction and energy telescoping; the endpoint-path materialization barrier; append-only path `LDL^T` gates plus one reverse materialization; and preservation of the source ACL/RPPR guarantees on paths (`main.tex:184-276,280-455`).
- **Conditional:** Any interface satisfying the source-safe error margins and charging all update/query/output work removes the round factor, with total `O(I(U_K)+cvol(U_K))` (`main.tex:471-517`).
- **Measured:** None for the original exact-interface investigation. The
  September finite-band audit is recorded separately above.
- **Refuted:** An ordinary warm start followed by full active-matrix passes or full vector materialization does not remove repeated-prefix work; endpoint paths force quadratic writes in that representation (`main.tex:73-80,280-340`).
- **Open:** Graph-uniform implicit continuation on arbitrary cyclic graphs; energy telescoping alone does not pay for dense old-coordinate transport or repeated boundary-key refresh (`main.tex:519-560`).

## Central blocker

Support complete boundary-violation reporting under dense implicit Schur corrections without materializing the old solution or refreshing every boundary key. The next falsifiable target is `conj:aggregate`; every proposed oracle should first be tested on broad old-face transport and repeated boundary-key refresh (`main.tex:519-560,585-589`).

## Dependencies and reusable outputs

- Formal registry dependencies: none.
- Source/shared prerequisites: the shared PageRank/RPPR model and the
  Wei--Yang 2026 source.
- Supplies to: `response_preconditioned_hybrid` (block correction and implicit interface), `local_solver_oracle_hierarchy` (path representation separation), and the controller's persistent-response track.

## Resume here

- Start with `UNICYCLE_TOP_TREE_PROBE.md` and the completed tree/shift
  proofs in `sections/op3_local_top_trees.tex` and
  `sections/op3_shifted_tree_clusters.tex`.
- Implement a logarithmic point query and a locally discovering unicyclic
  state machine; audit actual source-driven prefixes and both sides of
  cycle closure. Keep the balancing-source import explicit.
- Stop/go test: all exceptional candidates, one-time re-rooting, two-port
  exposure, signed spanning-tree responses and original residual checks
  must be paid before stating a unicyclic theorem.

## Verification

- Source pointers checked: `README.md`; `main.tex`; the note's entry in `registry.toml`; and shared related-work/results/broadcast ledgers dated 2026-08-20.
- Focused build/checks run: New proof sections compile. The exact audits and
  focused Python checks pass. The latest broad test run has 231 passes and
  the same three pre-existing notation/size failures; broader lint has the
  same two unrelated findings. Full details are in `VERIFICATION.md`.
- Known gaps: `cvol` is now defined locally in the scope section, removing the
  dependence on `propagate_settle_framework` for the basic work unit. The short
  README still omits the alpha/variable mapping, native accuracy parameters,
  interface details, dependencies, and exact next lemma; this `STATUS.md`
  remains the operational resume card.
