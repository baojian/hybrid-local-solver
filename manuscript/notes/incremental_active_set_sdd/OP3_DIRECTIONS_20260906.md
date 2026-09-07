# OP3: directions after the OP2 results

## Latest geometric-publication result (block 13)

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


**Overnight update:** the initial recommendation below now has a concrete
growing-core realization. `BRANCH_CORE_FLUX_PROBE.md` gives scalar physical
flux events, 27,120 exact comparisons, and the explicit remaining
`O_tilde((1+r^2)/eps_appr)` core cost. The general conjecture remains Open.
`LIVE_CORE_PEELING_PROBE.md` then replaces r by maximum live-core size,
passes 54,240 comparisons, and supplies a canonical tree family showing
why that maximum need not be polylogarithmic. The current next experiment
is `ORDERED_PATH_CLUSTER_PROBE.md`. The completed root-threshold probe
supplies an exact ancestor-group formula, but source-valid witnesses reject
stale global order for exact stopping and, under a separate legal policy,
for ACL stopping. Adjacent path-cluster slope separation is the next
constructive primitive to prove and implement.

Exploration date: 6 September 2026. Mathematical authority for the new
reduction is `main.tex`, Section `sec:op3-geometric-events`. The new claims
are **Proved here** proof drafts awaiting independent review. **OP3 remains
Open.** This report recommends a research direction, not manuscript promotion.

My recommendation is to pursue **persistent response with geometric value
events** first, with **local constrained elimination** as the main alternative.
Keep teleportation continuation as a limited diagnostic probe. Do not begin
by trying to maintain every exact intermediate solution or reproduce every
Wei--Yang admission.

## 1. The question we are actually trying to answer

The third item in `problem_definitions/main.tex` asks for a local algorithm
with fully charged work

\[
\widetilde O(1/\varepsilon_{\rm appr}),
\]

including only polylogarithmic dependence on inverse teleportation. The
canonical graph is simple, connected, undirected and unweighted; the source
is one vertex; adjacency scans, repeated operations, state maintenance,
certificate evaluation and output are all charged. Randomization is allowed
by the stated high-probability OP3 formulation.

Using the manuscript's lazy parameter, the output must have the witness

\[
\widehat{\boldsymbol\pi}
=\operatorname{PPR}_{\alpha}(\boldsymbol e_v-\boldsymbol r),
\qquad \widehat{\boldsymbol\pi}\geq0,
\qquad 0\leq r_i\leq\varepsilon_{\rm appr}d_i.
\]

This implies semantic degree-normalized error at most
`eps_appr`: apply the nonnegative PPR map to `0<=r<=eps_appr*d`, and use
`PPR_alpha(d)=d`. The converse does not hold in general. The new manuscript
already supplies an explicit ACL-compatible OP2 corollary, so there is now a
valid comparison in the same accuracy namespace:

| Available bound | What it buys | What OP3 would remove |
|---|---|---|
| New deterministic and randomized methods: `O_tilde(1/(eps_appr sqrt(alpha)))` | Sparse ACL output; the active paper's `cor:acl-compatible-output` provides the conversion | The polynomial inverse-teleportation factor |
| Wei--Yang: `O_tilde(1/eps_appr^2)` | Sparse ACL output with logarithmic inverse-teleportation dependence | A repeated-support factor |
| Desired OP3 bound: `O_tilde(1/eps_appr)` | Both dependences simultaneously | Neither improvement follows just by taking the better existing bound |

For comparisons of work, distinguish the new algorithms' expected/Las Vegas
variants from a high-probability time guarantee. Comparing the displayed
envelopes alone is not a new high-probability portfolio theorem. Ignoring
logarithms, their crossover is `eps_appr ~ sqrt(alpha)`.

Wei--Yang's Theorem 1.2 and concluding paragraph explicitly formulate the
reuse direction. I checked the primary PDF, including the paragraph on PDF
page 15. [Primary source](https://arxiv.org/pdf/2608.16339v1).

There are two legitimate success targets to distinguish:

1. **Literal reuse:** accelerate the source's particular sequence of nested
   faces and its intermediate gates.
2. **The complexity target:** return the same ACL output guarantee through a
   different, fully specified local discovery schedule.

The second leaves more room. The proposed geometric-event reduction takes
that room explicitly; it does not claim to reproduce the literal source trace.
No existing result reviewed here rules out the broader target. On a
center-seeded star with `m` leaves, lazy `alpha=1/3` gives leaf PageRank mass
`1/(3m)`. At `eps_appr=1/(6m)`, every valid ACL output must include all
leaves, since ACL implies semantic accuracy. Thus an elementary output lower
bound is `Omega(1/eps_appr)` on this family, consistent with the target.

## 2. What the existing notes contribute

The recent active manuscript and proof-owning notes take precedence over old
shared snapshots that still describe OP1 and OP2 as open. I did not revise
the root problem contract or promote an exploratory claim.

| Read in detail for this question | Reusable content | Boundary that matters now |
|---|---|---|
| `incremental_active_set_sdd` | Exact Schur corrections, energy telescope, linear path elimination, complete interface | Energy and warm starts do not pay for dense updates or boundary searches |
| `active_edge_lcp` and the active manuscript | Safe pivots, threshold-batch depth, certified supplied-face SDD calls, ACL output repair | A `1/sqrt(alpha)` bound on the number of fresh solves still misses OP3 |
| `deterministic_op2_20260905`, its independent companion, and current paper sections | Continuation, mass/box constraints, two energies and charged sparse updates | These solve the OP2 target; replacing a final linear solver does not remove the outer factor |
| `spectral_balance_threshold_batch`, especially its safe-box source audit | Supplied-face diffusion solver, positive repair, tree/width/cycle-rank backends; detailed failed spectral/recycling routes | A static inverse, a static obstacle solver and a persistent local discovery algorithm are distinct objects |
| `response_preconditioned_hybrid` and `delayed_reflection_ladder` | Finite-band response reporting, adaptive sketches, transport and refresh accounting | The remaining cost is producing or refreshing high-rank response state |
| `adaptive_revisit_control`, `propagate_settle_framework`, `signed_spider_generalization`, `two_rung_direct_theory` | Explicit compressed responses on paths, branches and cyclic attachments; legal-chronology tests | Symmetric or fixed-port gadgets can make a proposed hard example easy |
| `local_solver_oracle_hierarchy`, `evolving_support_cg`, `aspr23_bound_audit` | Failures of repeated materialization, fresh Krylov solves and overly broad lower-bound models | An obstruction to a named representation does not refute OP3 |
| `two_stage_revisited_20260906`, `two_stage_point_source_aesp_cd` | Certified handoff and completion; distinction between semantic and positive-residual outputs | Fast terminal completion still needs a paid discovery stage |

I also surveyed the other note status cards. The AESP, momentum, SOR,
clipped-potential, seed-return and experimental-ladder notes provide useful
negative controls, but their remaining questions target an accelerated
recurrence or a restricted solver class. They are not the most direct route
to eliminating *all* polynomial inverse-teleportation dependence. The
coverage record lists the files actually consulted; this is not a claim to
have line-by-line audited the entire notes directory.

## 3. A new reduction: pay for value changes, then isolate their discovery

Work in the source's degree coordinates with

\[
\bar\alpha=\frac{2\alpha}{1+\alpha},\quad
\gamma=1-\bar\alpha,\quad
\boldsymbol M=\boldsymbol D-\gamma\boldsymbol A,\quad
\lambda=\varepsilon_{\rm appr}/2.
\]

For a reached face `U`, let
`u^U_U=M_UU^{-1}(e_v-lambda*d)_U`, zero outside. Its actual degree-coordinate
RPPR point is `z^U=bar_alpha*u^U`. Safe admissions make `u^U` increase
coordinatewise, and conservation gives

\[
\lambda\operatorname{vol}(U)
+\bar\alpha\sum_{i\in U}d_i u_i^U
+\sum_{i\notin U}r_i^U=1.
\]

Therefore `vol(U)<=2/eps_appr` and `u_i^U<=1/(bar_alpha*d_i)`.

Maintain a lower published value `ell_i` for each active coordinate, with

\[
\ell_i\leq u_i^U\leq\tfrac54\ell_i+h,
\qquad h=\varepsilon_{\rm appr}/(16\gamma).
\]

Each positive publication starts at least at `h/2`; subsequent changes grow
by a factor at least `11/10`. An exact geometric floor is one option, but
the proof also gives an overlapping interval policy that needs no exact
threshold-equality decision or unknown complementarity margin.

The maintained exterior key is just
`L_j=gamma*sum_{i in U intersect N(j)} ell_i`. Each publication updates the
cached row once, charging its full degree. The important inequalities are

\[
L_j\leq r_j^U\leq\tfrac54L_j
+\tfrac1{16}\varepsilon_{\rm appr}d_j.
\]

Admit when `L_j>(11/20)*eps_appr*d_j`. Every admission is safe for RPPR at
`lambda=eps_appr/2`. When the producer has completed all required publications
and the dictionary is empty, exterior residuals are at most
`(3/4)*eps_appr*d_j`; active residuals equal `(1/2)*eps_appr*d_i`.

Each coordinate can generate only
`O(1+log_+(1/(alpha*eps_appr)))` publications. Consequently the total work
of receiving events, scanning their rows and maintaining the boundary keys
is

\[
\widetilde O\!\left(\operatorname{vol}(U_{\rm fin})
\left[1+\log_+\frac1{\alpha\varepsilon_{\rm appr}}\right]+1\right).
\]

One final certified SDD solve followed by downward clipping supplies the
ACL output in expected near-linear local work. Its required precision is
polynomial in the named parameters, contributing only logarithms. These
arguments are written as `thm:op3-geometric-recipient` and
`lem:op3-terminal-repair`.

**What has changed:** the old additive-quantization argument paid for an
inverse-teleportation number of tiny increments. Multiplicative changes plus
a small absolute floor give an alpha-independent polynomial work bound for
the recipient. This is an original proof draft from this exploration, not
an imported theorem or a verified solution of OP3.

**What has not been proved:** finding all coordinates that require a new
publication. A loop that checks every old coordinate at every face still
costs `sum_U vol(U)`. A heap does not solve this: its old keys may change
without being individually visited. Counting changes is not locating them.
All producer work, including failed searches and completeness certificates,
remains in a separate quantity `P`.

The sufficient missing lemma is now:

> Along this canonical monotone, finite-band trace, maintain an implicit
> response and produce the required geometric value publications, including
> certificates that no publication remains due, in total
> `P=O_tilde(vol(U_fin)+1)` charged local work.

The interface does not demand arbitrary loads, arbitrary dynamic inverse
queries, a supplied future graph, or exact intermediate vector output.
Those stronger interfaces should not be imposed unless a proposed mechanism
actually needs them.

## 4. The directions worth choosing between

### A. Persistent Schur responses with geometric publications - first choice

Retain a response hierarchy across admissions and ask it only for the
coordinate increases needed by Section 3. Use a finite overlap band for
all tests, and materialize the numerical answer once.

The first milestone should be an asymmetric cyclic family with a growing
number of attachments and surviving old boundary vertices. An asymmetric
ladder with extra chords or a chain of unequal cyclic modules is a better
test than another symmetric star. Trees and supplied bounded-width graphs
remain useful implementation controls, but a cheap *single* solve on these
classes is already known and is not the new result.

**First concrete task:** implement a retained factor/response state on the
chosen family. Meter (i) producing value intervals, (ii) locating due
publications, (iii) delivering row changes, and (iv) terminal completion
separately. Prove a bound on the first two; Section 3 already pays for the
third and fourth.

**Go criterion:** producer work bounded by new exposed volume plus actual
publications, with at most logarithmic overhead. **Stop criterion for that
implementation:** every small admission rebuilds a size-`V` response,
recomputes an unbounded-rank basis, or checks all old coordinates. A stop
does not refute the general direction.

### B. Local constrained elimination - main alternative, higher risk

The global nonnegative quadratic-diffusion algorithm of Chen--Peng--Wang
uses constrained vertex elimination, vertex weighting functions and j-tree
preconditioning. Its source theorem is randomized and near-linear in the
supplied graph. The paper itself leaves strongly local near-linear diffusion
open in Section 1.4. [Primary source, Theorem 1.1 and Sections 1.4, 2](https://arxiv.org/pdf/2105.14629v2).

For a supplied face the degree matrix has the exact decomposition

\[
\boldsymbol M_{UU}
=\gamma\boldsymbol L(\mathcal G[U])
+\operatorname{diag}(\bar\alpha d_i+\gamma d_{i,\bar U}).
\]

Thus the constrained face objective is algebraically in the generalized-
diffusion class, with a quadratic vertex term. Two algorithmic obligations
remain: localize construction to exposed volume, and audit parameter range.
Assumption 3.15 (PDF page 17) restricts all nonzero numbers encountered to
`[n^(-c),n^c]` for a universal constant; numerical stability is outside its
scope. Importing an unrestricted, only-polylogarithmic dependence on
`1/alpha` and `1/eps_appr` therefore needs an additional argument.
[Primary source, Assumption 3.15](https://arxiv.org/pdf/2105.14629v2).
This is a more relevant starting point than a generic convex-flow algorithm
with a subpolynomial running-time factor: OP3 allows randomness but its soft-O
notation does not hide `V^o(1)`.

A concrete related mechanism is **elimination on the live frontier**. After
eliminating admitted vertices, an effective pivot with diagonal `s_i`,
positive surplus `h_i`, and incident conductances `w_ij` updates a remaining
vertex's surplus by `w_ij*h_i/s_i` and creates Schur edges of weight
`w_ij*w_ik/s_i`. These are positive updates, so the frontier gates can be
maintained directly; old solution coordinates need not be written. Exact
fill can nevertheless be dense. Approximate elimination must prove both a
total fill-processing bound under the **source-driven admission order** and
finite-band correctness of the induced loads. A spectral approximation of
the matrix alone proves neither.

**First concrete task:** formalize a local elimination recursion that retains
unresolved boundary terms without reading their entire future components.
Test its true fill and changed-load work on the same asymmetric cyclic family.
Alternatively, localize one stage of the generalized-diffusion recursion,
with every preconditioner edge and vertex-function operation charged.

**Go criterion:** geometric rebuilding plus intervening work sums to
`O_tilde(1/eps_appr)`, and the actual original-graph ACL certificate survives.
**Stop criterion for an import:** the source theorem begins with the whole
graph, assumes a known final envelope, or requires a new complete solve for
each singleton admission. “Use a near-linear solver” is not the missing lemma.

This route may change the discovery schedule substantially. That is suitable
for the broader complexity target, but should be stated if literal source
reuse is the intended deliverable.

### C. Continuation in teleportation - useful probe, lower priority

Keep `lambda` fixed and set `t=bar_alpha/(1-bar_alpha)`. The obstacle

\[
\min_{\boldsymbol w\geq0}
\tfrac12\boldsymbol w^\top(\boldsymbol L+t\boldsymbol D)\boldsymbol w
-(\boldsymbol e_v-\lambda\boldsymbol d)^\top\boldsymbol w
\]

has a solution increasing coordinatewise as `t` decreases. Halving `t`
changes its matrix by only a factor two in Loewner order. This gives nested
supports and a natural preconditioner continuation.

But even a three-vertex path develops new support when `t` is halved:

\[
\lambda=1/5:\qquad
\boldsymbol w_{3/2}=(8/25,0,0),\qquad
\boldsymbol w_{3/4}=(96/205,4/205,0).
\]

So a constant spectral comparison does not give a coordinatewise factor
comparison, and does not supply a cheap constrained proximal step. The proof
and exact witness are in `subsec:op3-teleportation-probe`.

**First concrete task:** bound total newly exposed volume and retained-state
repair over one halving, with a measurable certificate. **Go criterion:** a
constant or logarithmic-cost local stage. **Stop criterion:** assuming that
the preconditioned obstacle projection is an ordinary SDD solve, or merely
replacing the old condition number by a new unknown inner oracle. I would
not make this the main route yet.

## 5. Approaches to deprioritize

- **Only warm-starting fresh solves.** It preserves numerical information but
  still pays for old matrix passes and output. The endpoint path already
  separates that representation from a retained response.
- **Trying to make the exact batch count logarithmic.** A path can admit
  only the next vertex per round. Its linear response algorithm succeeds by
  making those rounds cheap.
- **Additive rounding paid only by total PageRank mass.** The necessary
  boundary accuracy introduces the old inverse-teleportation factor. The
  new geometric proof changes this accounting, while leaving production open.
- **Energy telescoping as a work bound.** Many spatially broad corrections
  can have small total energy. A node touched is a cost even if its change
  is tiny.
- **Ambient dynamic inverse or sparsifier imports.** Their preprocessing,
  update models, output formats and accuracy dependences must be matched.
  A terminal Schur complement is not automatically the growing Dirichlet
  principal matrix.
- **A universal lower bound inferred from CG, SOR or a single reporter.**
  Those restrictions omit allowed elimination and persistent response.

## 6. Evidence produced in this exploration

The registered exact audit `incremental_active_set_sdd.geometric_value_events`
uses rational arithmetic. The extended run covered 19,416 executions across
142 connected graph representatives through six vertices, every seed, four
lazy alpha values, three ACL tolerances and both batch and singleton policies.
Another 24 executions used paths, asymmetric ladders, grids and barbells,
including `alpha=1/1000003`. All 19,440 executions passed the stated checks.

The checks include support safety, monotone exact responses, conservation,
the publication band, incremental keys, safe stopping and terminal clipping
under adverse numerical errors. There were 64,400 terminal perturbation
checks and 1,618 separate teleportation-halving checks. The runs include 44
batch admissions with no neighbor in the latest admitted batch: updating
only the newest rows would miss relevant old-boundary changes.

The dense reference's total visited volume was 200,515. Delivered event
volume was 150,441, including 69,625 on previously active coordinates. These
are separate diagnostic counters, not competing solver runtimes. The
reference used dense rational solves and scanned old coordinates to discover
events. Even a large measured separation would not prove a fast producer.

Reproduction command:

```text
uv run python experiments/proof_audits/incremental_active_set_sdd/geometric_value_events.py --max-n 6 --structured --output results/raw/op3_geometric_events_n6_structured.json
```

The durable audit summary records graph families, parameters, stopping rule,
source hash, base commit and dirty-worktree status. `VERIFICATION.md` records
build and repository-check outcomes. Numerical or exact finite audits support
the algebra but do not independently certify the asymptotic proof.

## 7. Proposed next decision

Choose **A as the main implementation/proof direction**, using the new
publication interface as its acceptance contract. Use **B as the alternative
mechanism** if retained linear-response updates repeatedly recreate dense
fill or full scans. Keep **C as a short probe** until a paid local halving
lemma exists.

The first deliverable should be a producer theorem or a precise obstruction
for one explicit retained representation on an asymmetric cyclic family.
Another fixed-face convergence theorem would leave the central OP3 question
unchanged. No larger agent campaign, topology migration or manuscript
promotion is needed to make that next choice.

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

**Resolved next target:** `UNICYCLE_TOP_TREE_PROBE.md` preserves the local unicyclic
continuation plan: one exceptional two-parent candidate, a charged point query,
one paid re-rooting at cycle closure, two fixed cycle ports and the corrected
root solve. A triangle witness proves that the uncorrected spanning-tree
response can be negative; retain signed affine responses. Arbitrary-graph
OP3 remains Open. No result has been promoted to the active manuscript.

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


## Latest local cycle-rank result

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
insertion parent. Its proposed r^2 improvement is not yet an end-to-end
algorithm or theorem. General OP3 remains Open, and every new proof draft
still awaits independent review.


## Latest maintained coarse inverse result

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
