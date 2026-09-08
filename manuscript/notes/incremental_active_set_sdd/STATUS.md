# Direction status: incremental_active_set_sdd

## Third campaign: lower-bound audit and 600 additional active minutes

The user requested another ten active hours after checking whether existing
lower bounds support the conjecture's scale. This campaign began on
8 September 2026 at 02:44:03 UTC; both prior campaigns are excluded.
Use [the current campaign status](OVERNIGHT_20260908_STATUS.md) and
`OVERNIGHT_20260908_WORK_LOG.json` for continuation and actual active time.

**Source / Proved here:** the literature review supports worst-case
inverse-accuracy optimality, with the existing problem-definition star
result imported explicitly. Corollary `cor:op3-uniform-output-lower-bound`
makes its constant uniform for lazy alpha in `(0,1/3]`. This is not a
proof of the conjectured upper bound. The new seed-only gate reduces the
sufficient threshold to `eps_appr*d_v >= (1-alpha)/2` with one degree query.

**Refuted:** the instancewise reading of the mass-over-degree divided by
epsilon lower bound. A cycle family has that expression exponential in k
and a deterministic local original-ACL computation costing O(k^3), including
linear-search maps. This does not refute any existential worst-graph bound.
See `sec:op3-lower-bound-quantifiers` and
[the source transfer map](LOWER_BOUND_LITERATURE_AUDIT_20260908.md).

**Measured:** the exact audit passes 44 independent star-system solves,
132 exact seed-only threshold cases, 231 uniform-alpha output cases,
1,096 original degree-gate inputs and 36 local cycle runs. The latter
check 1,764 original residual rows; at k=128 the algorithm emits 255
coordinates and records 3,812,842 charged units without reading ambient n.
Source and backend hashes are in `LOWER_BOUND_QUANTIFIERS_AUDIT.json`.

**Open / next:** general OP3 and potential-driven local discovery. The
weighted constructor and capped supplied recurrence are now proved below
as drafts awaiting independent review. Continue the additional campaign;
this first literature checkpoint does not complete the ten-hour request.
The formal dependency is now `problem_definitions`, specifically its
Proposition 5 star formula/output argument. Other directions remain
context/provenance only. The 127-page note builds without final warnings;
65 own scripts and three registry tests pass. Broad checks retain only the
recorded baseline failures, with all five baseline hashes unchanged.
See `OVERNIGHT_20260908_BLOCK1_AUDIT.json`.

## Third campaign, block 19: batched exact twin quotients

**Proved here, awaiting independent review:** Complete eligible batches
can be partitioned into true original twin classes using only their paid
full rows. A symmetric quotient is factored once, and saved class-to-group
coefficients reconstruct every physical coordinate in one reverse replay.
The fully charged adaptive bound is O((1+V+t*(t+f)^2)*log(2+V)); t counts
consumed classes and f counts maximum frontier groups, with f<=2^t-1.
Under an unsupplied k-type promise, total work/allocation improves to
O((1+V+(1+k)^3)*log(2+V)), with O(1+V+(1+k)^2) live words. This gives
both original ACL and, separately, exact physical/dyadic canonical RPPR
structural bounds. Read `thm:op3-batch-type-quotient`.

**Proved here / Refuted rule:** Induced-batch twin grouping loses a nonzero
Schur contrast on a five-vertex path. The implemented dense quotient
factorization has a cubic binary-tree cost even when inverse alpha is
logarithmic in inverse accuracy. These are representation-specific limits,
not general OP3 lower bounds. Read `prop:op3-batch-type-limits`.

**Measured:** 7,728 original ACL outputs, 7,298 exact obstacles, 88,759
final residual rows, 40,641 prefixes, 37,149 reverse coordinates and
27,098 historical group sums. Mixed types, tiny signed gates, tiny alpha,
arbitrary signed labels, fixed-type multiplicity growth and private huge
hubs pass. Six separately labeled binary-tree prefixes are nonterminal;
they check 246 independently lifted coordinates. The R=6 quotient has
order 64 and uses 41,664 off-diagonal factor inner products. See
`BATCH_TYPE_QUOTIENT_AUDIT.json`.

**Open / next:** Preserve sparse quotient structure instead of producing
a dense quotient factor; first audit weighted tree quotients and the
physical seed's within-class contrast. General OP3 remains Open. Formal
dependencies remain `["problem_definitions"]`. All 90 own scripts and three
registry tests pass. The 187-page note builds without final warnings; proof
pages 180-183 were visually reviewed. The same baseline failures and five
source hashes remain; reproduction stops at its test prerequisite. See
`OVERNIGHT_20260908_BLOCK19_AUDIT.json`. Resume
`TWIN_QUOTIENT_TREE_PROBE_20260908.md`.

## Third campaign, block 18: exact obstacles and dyadic canonical output

**Proved here, awaiting independent review:** The grouped backend can use
strict positive obstacle gates, with finite termination controlled by
support volume rather than a minimum positive gate. Penalties rho>=1/2
need only the seed degree. Under the unsupplied k-type promise, exact
physical RPPR work/allocation is O((1+V)(1+k)^2 log(2+V)), V<1/rho,
without target-alpha arithmetic dependence. Read `thm:op3-exact-group-obstacle`.

**Proved here:** Direct bisection emits dyadic canonical coordinates with
objective gap at most eps_obj, using O((1+V)log(2+1/eps_obj)) extra work
and no graph access or square-root primitive. Total PageRank mass bounds
all coordinate errors together. Each emitted value uses only
O(1+log(2+1/eps_obj)) bits, but no internal pivot bit bound is claimed.
This is a separate RPPR objective statement, not rounded ACL correctness.
Read `thm:op3-rational-canonical-materialization` and
`cor:op3-canonical-rppr-neighborhood-types`.

**Measured:** 17,065 independently solved exact obstacles, 98,783 original
KKT rows, 51,195 dyadic canonical outputs and independent rational objective
enclosures, plus 43,845 root/precision certificates. Exact zero gates,
signed gate offsets through 2^-1024, tiny alpha, mixed type blow-ups and
private huge hubs pass. The default grouped ACL backend remains unchanged.
See `EXACT_GROUP_OBSTACLE_AUDIT.json`.

**Open / next:** A paid compositional or low-rank threshold reporter beyond
a globally bounded type promise. The grouped binary-tree cubic obstruction
still applies to its matrix/order. General OP3 remains Open and formal
dependencies remain `["problem_definitions"]`. All 89 own scripts and three
registry tests pass. The 183-page note builds without final warnings; pages
177-179 were visually reviewed. Broad checks retain the unchanged baseline
failures and five matching hashes; reproduction stops at its test prerequisite.
See `OVERNIGHT_20260908_BLOCK18_AUDIT.json`. The next concrete target is
`BATCH_TYPE_QUOTIENT_PROBE_20260908.md`.

## Third campaign, block 17: a tight type-bound result and a branching limit

**Source / Proved here, awaiting independent review:** Lampis's uncolored
neighborhood-type definition gives a structural promise, not free global
preprocessing. The local producer itself neither receives k nor the type
partition. A type's remaining members are discovered together and never
split across completed-state groups, proving at most k such groups and
2k+1 transient groups. Thus `thm:op3-local-neighborhood-types` gives
`O((1+V)(1+k)^2*log(2+V))` work/allocation with V<2/eps_appr, independent
of target alpha and ambient size in the exact-real word model.

**Proved here:** A two-center star with near and remote leaf banks has at
most four global types and arbitrarily large ambient volume. Every original
ACL output has Omega(1/eps_appr) mandatory near leaves for alpha in (0,1/3].
This matches the structural upper bound's accuracy power up to logarithms;
it does not resolve arbitrary-graph OP3.

**Proved here / Refuted rule:** `thm:op3-grouped-binary-cubic` forces the
implemented first-eligible-group order to use Omega(eps_appr^-3) shared
matrix updates on a finite binary tree. Here alpha=1/(96R-1) and
eps_appr=1/(32*2^R), so inverse alpha is only logarithmic in inverse accuracy.
A rational Green subsolution and explicit Dirichlet torsion prove the
positive gates. This is a representation/order obstruction; existing fast
tree algorithms are unaffected.

**Measured:** The type audit passes 20,826 original outputs on 349 quotient
blow-ups, 71,050 count checks and 194,276 unsplit/discovery checks, plus nine
private four-type double-star outputs. The branching audit passes 1,024
symbolic certificates, 156 radial faces, 234 Green/torsion systems and six
actual capped prefixes. The latter are nonterminal and are not ACL outputs.
They contain 246 total pivots, with independently verified lifted coordinates.
At R=6 the producer reaches volume 380 using 91,519 shared matrix updates,
including 79,552 on the last level. See both new audit JSON files.

**Open / next:** Exact-obstacle gates under the same type promise, followed
by useful low-rank or compositional compression that avoids the demonstrated
branching growth. General OP3 remains Open. Formal dependencies remain
`["problem_definitions"]`; source type definitions are attributed explicitly.
The 181-page note builds without final warnings; new proof pages 173-176
were visually reviewed. All 88 own scripts and three registry tests pass.
Broad checks retain only recorded baseline failures and all five source
hashes match. Reproduction stops at the failed test prerequisite. See
`OVERNIGHT_20260908_BLOCK17_AUDIT.json` and resume
`EXACT_GROUP_OBSTACLE_PROBE_20260908.md`.

## Third campaign, block 16: shared frontier groups and reverse aggregates

**Proved here, awaiting independent review:** The implemented grouped
producer uses original adjacency into the admitted set to refine frontier
response groups, while keeping every original degree. Degree heaps find
eligible members; row entries pay for all membership moves. Shared Schur
updates cost the square of the transient group count, and reverse split
merges reconstruct all coordinates without expanding historical groups.
Its total work/allocated words are
`O((1+V+sum_i(b_i+1)^2)*log(2+V))`, with V<2/eps_appr and no target-alpha
arithmetic dependence. Live state is O((1+V)^2). Read
`thm:op3-frontier-response-groups`.

**Proved here:** On a star with m leaves and a sufficiently long path tail,
all alpha in (0,1/3] give at most two transient groups and O(m log m)
local work at eps_appr=1/(4m). This repairs the explicit clique expansion
in that example; trees were already covered by earlier fast algorithms.

**Measured:** 7,311 original ACL outputs, 49,915 final residual rows,
12,986 prefix states, 5,700 independently verified reverse coordinates
and membership aggregates, 594 splits and 655 old-member moves. Exact
ties, huge private hubs, unequal original degrees, arbitrary signed labels
and alpha through 2^-1024 pass. The m=64 star case has 66 shared matrix
updates and 66,793 charged units versus 45,760 fill updates and 17,313,546
units in the explicit reference. These counters are not timing speedups.
See `FRONTIER_GROUPS_AUDIT.json`.

**Open / next:** Establish a structural neighborhood-type bound and test
a binary-tree obstruction to this specific first-eligible-group order.
Read `FRONTIER_GROUP_STRUCTURE_PROBE_20260908.md`. The group bound is
not universally small; general OP3 remains Open. Formal dependencies are
still `["problem_definitions"]`. The 177-page note builds without final
warnings; new proof pages 171-173 were visually reviewed. All 86 own
scripts and three registry tests pass. Broad checks retain the recorded
baseline failures, with all five source hashes unchanged. Reproduction
stops at the failed test prerequisite. See
`OVERNIGHT_20260908_BLOCK16_AUDIT.json`.

## Third campaign, block 15: implemented exact frontier and explicit fill cost

**Proved here, awaiting independent review:** `thm:op3-exact-frontier`
returns original ACL output with residual at most 3eps_appr*d/4 and
original support volume below 2/eps_appr. Each admitted row and each
known degree is read once. The exact Schur state uses deterministic AVL
maps and intrusive incidence lists; one reverse pass reconstructs the
potentials. Total work and allocated words are
`O((1+V+sum_i(p_i+1)^2)*log(2+V))`, live state is O((1+V)^2), and the
arithmetic bound has no alpha dependence. No dense inverse or repeated
face solve is part of the producer.

**Proved here / Refuted rule:** A star with a long tail forces at least
binomial(m,3) explicit fill-pair updates at admitted volume Theta(m), even
when the ambient volume exceeds 4/eps_appr. This refutes a linear fill
bound for this representation; it does not obstruct implicit rank-one
cliques, existing tree algorithms, or the OP3 target.

**Measured:** 7,305 original ACL outputs, 44,149 final residual rows,
12,986 prefix Schur/map/queue checks, 6,349 implemented pivots, 60,747
fill updates and 12,900 load publications. Exact threshold ties, signed
large labels, small alpha through 2^-1024, and three private huge hubs
are included. Independent dense calculations are validators only.
See `FRONTIER_EXACT_AUDIT.json`.

**Open / next:** Compress fill while paying for transformed-load threshold
reporting, or use controlled refinement in the original equations.
The cubic reference does not improve the known quadratic source rate.
General OP3 remains Open. Formal dependencies remain
`["problem_definitions"]`. The 175-page note builds without final warnings;
new proof pages 168-170 were visually reviewed. All 85 own scripts and
three registry tests pass. Broad checks retain only the recorded baseline
failures, with all five source hashes unchanged. Reproduction stops at
its failed test prerequisite. See `OVERNIGHT_20260908_BLOCK15_AUDIT.json`
and resume `FRONTIER_GROUP_COMPRESSION_PROBE_20260908.md`.

## Third campaign, block 14: a penalty reserve still misses support

**Proved here, awaiting independent review:** A finite complete binary tree
at fixed alpha=1/3 admits an original significant-coordinate subsolution.
Increasing only right-edge conductances gives M<=M_hat<=(3/2)M while
preserving original row sums and M-matrix signs. A two-step finite-subtree
grounding bound shows that the all-left potential decays faster. Its
perturbed obstacle at penalty lambda/C omits the significant vertex whenever
`C*(289/300)^R <=51/403`. This includes every fixed or polylogarithmic
penalty reserve eventually. True degree-one leaves and root grounding are
included; no infinite-tree limit is assumed.

**Measured:** 257 exact symbolic dyadic-reserve and large-volume certificates,
seven polynomial-reserve witnesses, five independent finite-tree Green
solves on 243 total vertices, ten left-transfer bounds, and five original
radial obstacle quotients with 129 KKT/subsolution rows. Enormous trees are
symbolic proof objects and are not described as executed local solves.
See `SPECTRAL_LOAD_RESERVE_OBSTRUCTION_AUDIT.json`.

**Scope:** This is a support-rule obstruction, not a computational lower
bound or a restriction on accurate original-residual refinement. The
original fixed-alpha problem and trees already have fast local algorithms.
General OP3 remains Open. Formal dependencies remain
`["problem_definitions"]`.

**Open / next:** Implement the exact paid live-frontier elimination baseline
in `FRONTIER_IMPLEMENTATION_PROBE_20260908.md`. Its honest cost should
expose the fill-pair and load-reporting work, with one-time original rows
and one final reconstruction; no new nearly linear general claim is made.
Checkpoint verification: the 172-page note builds without final warnings;
new proof pages 166-168 were visually reviewed. All 84 own scripts and three
registry tests pass. Broad checks retain the recorded baseline failures,
with all five hashes unchanged; reproduction stops at its test prerequisite.
See `OVERNIGHT_20260908_BLOCK14_AUDIT.json`.

## Third campaign, block 13: sharp spectral support stability

**Proved here, awaiting independent review:** Under a relative spectral
sandwich, nonpositive off-diagonal entries and nonnegative row sums,
same-load obstacle minimizers satisfy
`||u-u_hat||_infty <12 eta/eps_appr` on the large-component branch.
Their union has original volume at most 4/eps_appr, so it is proper.
A path-to-zero energy bound controls the Dirichlet inverse without target
alpha. Thus eta<=eps_appr^2/192 preserves all significant coordinates.

A weighted path changes edge conductances while keeping original-degree
load and row sums. At relative error asymptotic to 4 eps_appr^2, its
obstacle omits a coordinate above 3 eps_appr/16 in the original positive-
target obstacle. The accuracy power two is sharp for this direct
matrix-replacement rule. A separate star shows that an abstract positive
definite spectral approximation need not have the M-matrix signs, and
its inactive residual can be negative despite exact KKT.

**Measured:** 28,335 exact same-load pairs, 16,365 union Dirichlet diagonals,
9,444 safe containments, 132 weighted paths through N=4096, 135,748
original-degree load rows, three independent dense endpoint obstructions
and 12 sign counterexamples. All solves in this audit are explicit proof
validators; perturbed residuals are not relabelled original ACL output.

**Source / scope:** Kyng--Sachdeva arXiv:1605.02353v1 was checked in its
primary PDF and the literature index, topic note and local bibliography
were synchronized. No source primitive is imported into a new local-work
theorem. These obstructions do not apply to proved accurate refinement
using a spectral preconditioner. General OP3 remains Open.

**Open / next:** Check `LOAD_RESERVE_SPECTRAL_PROBE_20260908.md`.
It proposes a finite bounded-degree tree obstruction to using a coarser
matrix with any fixed reduction of the obstacle penalty. This is another
specific support rule, not a computational lower bound; trees already
have fast local algorithms. Formal dependencies remain
`["problem_definitions"]`.

Checkpoint verification: the 170-page note builds without final warnings;
new proof pages 164-166 and the new source's central pages were visually
reviewed. All 83 own scripts and three registry tests pass. Broad checks
retain the recorded baseline failures, with all five hashes unchanged;
reproduction stops at its test prerequisite.
See `OVERNIGHT_20260908_BLOCK13_AUDIT.json`.

## Third campaign, block 12: sharp comparison-parameter obstruction

**Proved here, awaiting independent review:** On an explicit path family,
a conservative coordinate of value eps_appr/4 disappears from a valid
accuracy-eps_appr/2 ACL output at bar_a asymptotic to 16 eps_appr^4.
The exact positive-target obstacle also omits it, including at all larger
bar_a. The existing safe comparison uses eps_appr^4/128. Consequently the
fourth power is sharp for the arbitrary-output support-extraction rule;
the uniform potential-sensitivity factor eps_appr^-3 is sharp as well.
This constrains this reduction and does not imply an OP3 work lower bound
or rule out a producer deliberately emitting additional envelope labels.

**Measured:** 135 path cases through N=4096, 193,071 conservative and
193,071 positive-target original residual rows, 270 exact prefix Dirichlet
solves, six independent dense Dirichlet validators and 15 small whole-graph
obstacle validators. The safe parameter retains the endpoint, while the
larger comparison parameters omit it. Exact examples and hashes are in
`CONSERVATIVE_PARAMETER_OBSTRUCTION_AUDIT.json`.

**Open / next:** The spectral-envelope probe proposes a weighted-path
obstruction at relative spectral error of order eps_appr^2 and a matching
sufficient stability bound under M-matrix and nonnegative-row-sum
assumptions. Both require proof and audit. A newly checked approximate
Cholesky source motivates the transfer question; no new source theorem
is imported at this checkpoint. Formal note dependencies remain
`["problem_definitions"]`.

Checkpoint verification: the 168-page note builds without final warnings;
new proof pages 162-163 were visually reviewed. All 82 own scripts and three
registry tests pass. Broad checks retain the recorded baseline failures,
with all five hashes unchanged; reproduction stops at its test prerequisite.
See `OVERNIGHT_20260908_BLOCK12_AUDIT.json`.

## Third campaign, block 11: conservative-envelope equivalence

**Proved here, awaiting independent review:** The capped AVL component gate
either materializes the whole original graph of volume at most B or gives
a distinct-degree witness that its volume exceeds B. Full started rows,
including a partially consumed last row, have degree sum at most B.
Work and cumulative allocation are O((1+B) log(2+B)); a huge new degree
is rejected before its row buffer is allocated or read.

With B=4/eps_appr, the supplied theorem handles complete small graphs in
the desired work. On larger graphs the conservative obstacle is unique
and proper. A Dirichlet torsion comparison shows that at
bar_a=eps_appr^4/128, every conservative coordinate above eps_appr/8
remains positive. This gives an equivalence between fast significant
conservative-envelope discovery and the capped algorithmic ACL target
with original support volume O(1/eps_appr). The forward reduction removes
target alpha even from logarithms. Neither producer is proved to exist;
literal exact nested-system reuse is a further requirement.

A center with inverse-accuracy many leaves and an arbitrarily long tail
forces those leaves in both original ACL output and conservative envelopes.
The small-component gate therefore does not remove the output lower bound.

**Measured:** The gate passes 4,086 outcomes, including private paths and
hubs of size 2^1024. The reduction passes 7,299 original target certificates,
1,902 conservative comparisons and actual weak-producer envelopes, and
1,237 torsion systems. Reverse tests use the implemented cubic producer;
forward supplied solves are explicitly dense validators. No fast finder
is inferred from these tests. Large-ambient leaf inequalities pass at
1,021 accuracies and 3,063 positive-target parameter cases.

**Open / next:** Prove or refute the explicit fourth-power parameter
obstruction in `CONSERVATIVE_PARAMETER_OBSTRUCTION_PROBE_20260908.md`.
It concerns support containment under an arbitrary ACL output, not an OP3
work lower bound. Formal dependencies remain `["problem_definitions"]`.

Checkpoint verification: the 166-page note builds without final warnings;
new proof pages were visually reviewed. All 81 own scripts and three
registry tests pass. Broad checks retain the recorded baseline failures,
with all five hashes unchanged; reproduction stops at its test prerequisite.
See `OVERNIGHT_20260908_BLOCK11_AUDIT.json`.

## Third campaign, block 10: conservative discovery and first closure

**Proved here, awaiting independent review:** The stopped conservative
gap push needs no globally stabilizing obstacle. Unit superlevel flux
controls each edge difference; proper support bounds the maximum by its
cardinality. The last push first making support full also obeys a bounded
maximum, and the process stops immediately there. Its monotone-value
budget gives fewer than 8/eps_appr^3 degree-weighted updates.

For bar_alpha<=eps_appr^2/4, a proper conservative output transfers upward
to the target parameter using its active residual margin. Larger parameters
use native damped pushes. Equality of maintained positive/discovered counts
detects the whole graph without ambient n; a paid in-place LDL^T solve
then gives exact original target PageRank. Total work and allocation are
O(eps_appr^-3), original row volume is below 2/eps_appr, and all original
rows/degrees are cached once. Live graph state is linear in inverse accuracy;
the optional dense matrix uses quadratic space. This remains a weaker
reference, not the conjectured reuse rate or a floating-point theorem.

**Measured:** 2,065 original target certificates, 3,223 exact prefixes,
985 conservative superlevel identities and 29 implemented exact closed
solves; 1,158 pushes, 2,061 degree-weighted updates and three private
huge-hub cases. Alpha extends to 2^-1024. The two-vertex case uses two
pushes and one exact solve instead of the old reference's 1,744 pushes.
Internal tolerances differ; both certify the same target accuracy.

**Open / next:** Investigate the explicit conservative-envelope equivalence
probe. A capped whole-component exploration may handle small ambient
graphs in the desired work, leaving a well-posed proper conservative
obstacle. The torsion comparison and two algorithmic reductions need
proof and charged implementation checks before being claimed. Formal
dependencies remain `["problem_definitions"]`; neither the OP2 note nor
the bounded-treewidth comparisons were imported into this result.

Checkpoint verification: the 161-page note builds without final warnings;
new proof pages were visually reviewed. All 79 own scripts and three
registry tests pass. Broad checks retain the recorded baseline failures,
with all five hashes unchanged; reproduction stops at its test prerequisite.
See `OVERNIGHT_20260908_BLOCK10_AUDIT.json`.

## Third campaign, block 9: a paid native reference and sandpile mapping

**Proved here, awaiting independent review:** `thm:op3-native-gap-push`
gives native work O(1/(bar_a*e)+e^-2) with original support volume below
2/e. Its sorted pointer array charges insertions, stable cached records
avoid repeated lookups, and its intrusive queue needs no allocation per
push. Only newly positive rows are read, once each. The arithmetic floor
composition gives a deterministic local O(eps_appr^-3) reference with no
target-alpha or ambient-size dependence. Live graph state is O(1/eps_appr);
total allocation is conservatively bounded by work, not by Python memory
measurements. This weak result does not improve the nearly quadratic
Wei–Yang source rate or prove OP3.

**Measured:** 826 complete original ACL outputs; 3,848 exact intermediate
invariant checks; 3,022 pushes and 3,773 degree-weighted updates. Three
private hubs through degree 2^1024 are queried only for degree. The
two-vertex stress case requires 1,744 pushes, exposing a removable
full-support constant-mode cost. Source/backend hashes are recorded in
`NATIVE_GAP_PUSH_AUDIT.json`.

**Source / Proved here:** LMPU's conservative sandpile least action and
FL's supplied odometer correction were checked in their primary PDFs.
The note gives an explicit affine mapping at gamma=1 and its own
finite-graph feasibility proof. Neither source supplies a charged local
OP3 running-time bound; positive teleportation is a killed variation.
The literature index, topic note and references are synchronized.

**Open / next:** Read `NATIVE_PRODUCER_REFINEMENT_PROBE_20260908.md`.
Detect full support during native work and replace its repeated constant
mode by one paid solve. Check the conservative proper-support energy
bound and whether a useful stronger correction contract emerges. The
existing OP2 theorem was read for comparison; it is not imported into a
new claim and formal dependencies remain `["problem_definitions"]`.

Checkpoint verification: the 159-page note builds without final warnings;
new proof pages were visually reviewed. All 78 own scripts and three
registry tests pass. Broad checks retain the recorded baseline failures,
with all five hashes unchanged; reproduction stops at its test prerequisite.
See `OVERNIGHT_20260908_BLOCK9_AUDIT.json`.

## Third campaign, block 8: arithmetic alpha transfer and supplied work

**Proved here, awaiting independent review:** A unit-source potential has
global oscillation at most `(n-1)/gamma`, including full support. With all
support rows materialized, adding one nonnegative constant shifts every
normalized target residual down to minimum zero. This replaces the former
full-component numerical fallback with O(B log B) arithmetic.

**Conditional:** The general floor wrapper still requires the native work
and original support-volume contract. It is not a near-linear finder.

**Proved here, awaiting independent review:** The supplied-envelope solver
now has work `(1+V) polylog(2+V+1/eps_appr+1/p)`, independent of target
alpha even in logarithms. It keeps lambda=eps_appr/2 and delta=eps_appr/8,
solves at `max(alpha, eps_appr^2/(32+eps_appr^2))`, reserves eps_appr/8
of residual tolerance, then applies the arithmetic transfer. Same-load
obstacle monotonicity preserves the promised target envelope. Exact-real
constant division is charged; no bit or floating-point claim is made.

**Measured:** The arithmetic wrapper passes 3,243 original certificates,
including 1,554 constant corrections and 608 proper-support transfers.
The supplied composition passes 4,950 target residual/support certificates,
1,650 same-load monotonicity checks and 1,758 numerical reference callbacks.
It includes 792 full-support constant shifts, alpha=2^-1024, and three
private huge-hub cases whose outside rows are never read. Numerical VWF
outputs remain explicit dense validators; preparation and correction are
implemented. The seed-gate interface was extended to reserve accuracy
without changing the original load; all three dependent short audits were
rerun to update their source/backend hashes.

**Next / Open:** General OP3 and native local production. The alternative
proper-envelope cap proof is no longer needed to obtain alpha-independent
supplied work. Investigate a paid monotone push with a volume contract,
its energy bound before full support, and the primary sandpile literature.
Checkpoint verification: 155-page note builds without final warnings; the
new proofs and final one-page abstract were visually reviewed. All 77 own
scripts and three registry tests pass. Broad checks retain the same three
test failures, two unrelated lint findings and two oversized sources; all
five baseline hashes match. Reproduction stops at its test prerequisite.
See `OVERNIGHT_20260908_BLOCK8_AUDIT.json`.

## Third campaign, block 7: supplied-envelope work and the small-alpha reduction

**Proved here, awaiting independent review:** The complete supplied-envelope
work theorem reads only original rows in the supplied set, preserves cut
grounding and has cost `(1+V) polylog(2+V+1/alpha+1/eps_appr+1/p)`.
The seed gate removes an extra inverse-(1-alpha) range term near alpha one.
Every positive superlevel of any nonnegative-residual potential is connected
to the seed. Proper support of k vertices gives maximum potential at most
`k/gamma`; full support has an explicit counterexample.

**Conditional:** A native ACL producer with original support-volume bound
B can run at `max(alpha, eps_appr/(4B+eps_appr))`. After a paid degree pass
and support closure check, proper support transfers with the same potential;
a whole-graph support of volume at most B invokes the completed supplied
solver at the target alpha. This yields an accuracy-squared floor when
B=O(1/eps_appr). A sparse word bound is not a volume contract.

**Refuted:** Raising to a floor of order accuracy and returning the same
native obstacle can violate the target residual on a proper-support path.
This is a substitution obstruction, not a general algorithmic lower bound.

**Measured:** 6,177 envelope preparations, 258 exact principal-matrix and
numerical compositions, and 1,806 numerical ranges pass. The alpha audit
checks 1,644 original ACL outputs, 7,545 strict-superlevel identities,
15,341 edge gradient bounds and 1,071 proper-support maxima. Its outputs
include 152 same-potential transfers and 259 full-component fallbacks.
Both wrappers reject huge-degree candidates before any row scan. Dense
numerical providers are validators; the native near-linear producer is
not implemented or proved. Source hashes are in the named audit JSONs.

**Next / Open:** General OP3. Continue the new campaign with a possible
proper-envelope range improvement and an explicit bounded-volume native
producer. See `PROPER_ENVELOPE_AND_NATIVE_PRODUCER_PROBE_20260908.md`.
Checkpoint verification: 151-page note builds without final warnings; new
pages 143-148 were visually reviewed. All 75 own scripts and three registry
tests pass. Broad checks retain the same three test failures, two unrelated
lint findings and two oversized sources; all five baseline hashes match.
Reproduction stops at its failed test prerequisite. See
`OVERNIGHT_20260908_BLOCK7_AUDIT.json`.

## Third campaign, block 6: complete capped supplied recurrence

**Proved here, awaiting independent review:**
`thm:op3-complete-supplied-recursion` gives a complete source-backed
supplied VWF solver with M0 polylogarithmic word work and total allocated
words, including every failed branch. Its absolute-accuracy corollary
uses the original boxing and ACL bridge. The corrected weighted
constructor is composed with the existing numerical range, compression,
forest and mixed-accuracy proofs. No polynomial weight ratio in the
current core size, minimum positive gap, or free failed call is assumed.
The old conditional recurrence remains a reusable contract statement.

**Measured:** The generic cap/composition audit passes 12,374 transaction
prefixes, 39,807 requests, 252 adaptive conditional probability trees,
and 40 recursive mass/depth/call trees. It rejects huge allocations before
their payloads, charges released memory cumulatively, caps zero-size loops,
and gives four counterexamples to reusing one random seed under adaptive
calls. This audits resource semantics, not the full VWF algorithm.

**Source / implementation boundary:** The low-stretch tree and accelerated
convergence inequality remain explicit source imports. Earlier audits
implement the numerical, routing, resistance and sampling interfaces.
Neither the source tree algorithm nor the entire asymptotic recursion
is claimed as an implemented experiment.

**Verification:** 146-page note builds without final warnings; the final
cover and pages 140-143 were visually reviewed. All 73 own scripts and
three registry tests pass. Broad checks retain 231 passing tests and the
same three failures, two unrelated lint findings and two oversized AESP
sources. All five baseline hashes and the cap-audit source hash match.
Reproduction stops at its failed test prerequisite. See
`OVERNIGHT_20260908_BLOCK6_AUDIT.json`.

**Next / Open:** General OP3 remains Open. Make the significant-envelope
work reduction fully explicit, then test potential-driven local discovery
or a geometric boundary-event producer. The supplied numerical solver
obligation has been closed at the proof-draft level. Continue the
600-new-active-minute campaign; both earlier campaigns are excluded.

## Third campaign, block 5: resistance estimates and bounded core sparsification

**Proved here, awaiting independent review:** ordinary-solve resistance
sketches and a bounded core sparsifier. The new constructor gives
`G <= Q <= (10752W/j)G`, with O(j log(j/p)) core edges, from a supplied
tree. The checked arbitrary-positive-weight AN source yields quality
O(m L^2/j) and work O(m[L^6+log(weight_ratio)]). The source tree is
explicitly imported; its algorithm is not implemented by these audits.
All nonaborted cores are connected and have deterministic weight bounds,
even when their spectral estimate is wrong. Read
`sec:op3-ordinary-solve-resistances` and `sec:op3-bounded-core-sparsifier`.

**Measured:** 260 square-root brackets, 68 exact sign-moment identities,
1,556 nonlinear solver edge-error bounds, 676 actual cycle-backend sketch
groups and 225 additional dense nonlinear reference groups. The sampling
audit has 182 attempts: 155 returned graphs pass both exact PSD bounds,
while 27 report permitted capped-sampler aborts. Three complete
sketch-to-sampler runs use 450 resistance groups; nine forest/core
compositions pass. Extreme relative weights and all four explicit guard
failures are exercised. No probability theorem is inferred from frequencies.

**Verification:** 143-page note builds without final warnings; pages
134-140 visually reviewed. All 72 own scripts and three registry tests
pass. Broad checks retain 231 passing tests, the same three failures,
two unrelated lint findings and two oversized AESP sources. All five
baseline hashes match, as do the three current audit/backend hash sets.
Reproduction stops at its test prerequisite. See
`OVERNIGHT_20260908_BLOCK5_AUDIT.json`.

**Next / Open:** reconcile primitive-level work/allocation and call/depth
caps in the complete supplied recursion. Read
`SUPPLIED_RECURSION_CAP_PROBE_20260908.md`. The weighted constructor
hypothesis is now discharged on the tracked global numerical ranges;
the final capped recurrence composition remains to be written. General
OP3 and potential-driven local discovery remain Open. Continue the
600-new-minute campaign; neither earlier night counts toward it.

## Third campaign, block 4: paid random sampling and cycle solves

**Proved here, awaiting independent review:** a bounded fair-bit categorical
sampler, a heavy-path flow backend, and a supplied-tree cycle solve with
explicit energy-error and failure budgets. The checked arbitrary-weight
low-stretch-tree source gives O(m L^5) word work for logarithmic L. No
fixed symmetric solver operator, real-uniform sampler or bit-complexity
claim is assumed. Read `sec:op3-fair-bit-sampling` and
`sec:op3-weighted-cycle-solver`.

**Measured:** 140,860 exact terminal intervals, 209 exhaustive sampling
grids, 3,488 cycle energy identities, 3,456 heavy-path update/query/work
checks and nine prescribed-budget solves totaling 2,808 updates. Larger
trees have up to 512 vertices, arbitrary roots and weights 2^-80 to 2^80.

**Verification:** 137-page note builds without final warnings; new pages
130-134 visually reviewed. All 70 own scripts and three registry tests
pass. Broad checks retain only the same baseline failures; all five
baseline hashes match. Reproduction stops at its test prerequisite.
See `OVERNIGHT_20260908_BLOCK4_AUDIT.json`.

**Next / Open:** implement and prove ordinary-solve resistance sketches,
then capped core sparsification. Check all failure-branch resource and
weight bounds before promoting the full supplied recurrence. General OP3
and local discovery remain Open; the 600-new-minute campaign continues.

## Third campaign, block 3: charged weighted corridor routing

**Proved here, awaiting independent review:** a complete construction
from an arbitrary supplied spanning tree T. With total stretch W and
root budget j, it constructs `G <= Q <= (5376W/j)G` using at most j
roots. All tree distances, congestion, ownership, corridor cuts, local
part construction and core aggregation are charged. The proof uses the
correct common congestion offset and retains parts sharing one root.
Read `sec:op3-weighted-corridor-routing`.

**Measured:** 27,961 exact constructions, 55,706 PSD certificates,
33,404 common-offset corridors, 16,189 corrected cut-routing cases,
272,880 independent stretches and 134,700 congestion checks. The audit
records 56,091,347 charged construction units and passes every supplied
root/spanning tree in the small atlas grid, plus larger weighted and
parallel-edge cases through 512 vertices. Its full run took 69.054 seconds.

**Verification:** the 133-page note builds without final warnings and
pages 127-130 were visually reviewed. All 68 own scripts and three
registry tests pass. Broad checks retain only the same three failures
with 231 passing tests, two unrelated lint findings and two oversized
AESP sources. All five baseline hashes match; reproduction stops at its
failed test prerequisite. See `OVERNIGHT_20260908_BLOCK3_AUDIT.json`.

**Next / Open:** the core still needs sparsification, and tree selection
must use the checked arbitrary-weight source. The KOSZ 2013 cycle solver
provides a new source-backed route to the resistance estimator; its exact
expected-error lemmas were checked in the primary PDF. The next concrete
tasks are a bounded fair-bit sampler, a heavy-path cycle-update backend,
and ordinary-solve resistance sketches. Read
`RESISTANCE_ESTIMATOR_CONSTRUCTION_PROBE_20260908.md`. The full supplied
recurrence remains Conditional; general OP3 remains Open. Continue the
600 NEW active-minute campaign.

## Third campaign, block 2: rooted pieces and weighted ownership

**Proved here, awaiting independent review:** a star obstruction to CPW's
literal whole-component stretch lemma, a replacement spectral comparison
`G <= Q <= 21*kappa*G` using rooted pieces, and a linear-work weighted
tree decomposition with unique load ownership and at most two shared
boundaries per piece. The source correction does not refute CPW's final
spectral-constructor or diffusion theorem.

**Measured:** 19,854 exact weighted comparisons, 59,562 PSD certificates,
and 9,042 supplied-tree ownership cases. The latter validate 127,547
pieces and 1,483,000 intersections while recording 10,486,152 charged
construction units. Both audits include conductances or loads at 2^-80
and 2^80. Validator matrices, complete paths and pairwise comparisons
remain separate from charged construction. See the two new sections
`sec:op3-rooted-piece-comparison` and `sec:op3-weighted-tree-ownership`.

**Verification:** 130-page note builds without final warnings; pages
123-127 were visually reviewed. All 67 own scripts and three registry
tests pass. Required broad checks retain 231 passing tests, the same
three baseline failures, two unrelated lint findings and two oversized
AESP sources. The five baseline hashes are unchanged. Reproduction stops
at its failed test prerequisite. See `OVERNIGHT_20260908_BLOCK2_AUDIT.json`.

**Next / Open:** implement and prove the charged tree-path and corridor
routing step in `WEIGHTED_DECOMPOSITION_DESIGN_20260908.md`. Its
common-offset argument must cover edges that cross a piece with neither
endpoint owned there. The full supplied recurrence remains Conditional,
and general OP3 remains Open. Continue the ten NEW active hours.

## Historical second campaign completion

Completed **481.581 new active research minutes** across twelve blocks. The first night is excluded, as are 41.3 explicitly recorded unverified minutes and the gaps between active intervals. General OP3 remains Open. Read [the morning decision note](OP3_MORNING_DECISIONS_20260908.md).

## Second night, block 12: nested numerics and a sharper local target

**General OP3 remains Open.** Start with
[OP3_MORNING_DECISIONS_20260908.md](OP3_MORNING_DECISIONS_20260908.md).
The new significant-potential envelope theorem only requires a supplied set
containing `{i: u_i > eps_appr/8}`. Its restricted solution is within
`eps_appr/8` of the full obstacle; numerical approximation and clipping then
certify the original ACL residual. Finding this set in the target local work
remains Open. A separate explicit subsolution now proves an asymptotic
obstruction to FIFO BFS discovered-label envelopes on original degree-three
trees. This refutes the exploration rule, not general OP3.

**Proved here, awaiting independent review:** the envelope/ACL bridge,
spectral residual gap certificate, computable stopping rules, paid upward
rounding and confidence wrapper under its stated resistance-estimator
contract. The full supplied near-linear recurrence is a **Conditional**
theorem: the actual-positive-weight constructor/source extension remains
explicitly unreconciled. The previously proved numerical range lemmas do
not silently remove CPW's printed weight-ratio assumption.

**Measured:** Two genuinely nested accelerated levels pass 389,120 fixed
inner steps. On the same two physical profiles, certified stopping uses
6,525 steps plus 12,605 paid tree certificates. Its third signed profile
exercises positive compression errors and piece changes. All four saved
physical outputs pass the original ACL certificate. The envelope audit
passes 1,097 physical inputs, 19,925 supplied sets and 751,993 original
residual certificates. Three finite tree witnesses pass exact original
quotient KKT checks; 67 asymptotic-family instances validate 10,138 positive
subsolution rows. The spectral audits pass 1,440 mixed certificates,
240 exact-tree certificates and 180 weighted confidence cases, including
540 invalid-estimator aborts before any sampling.

All eight new audits have durable source/backend hashes. Dense minima,
supplied preconditioners and symmetry quotients remain identified validators.
No general fast constructor, hidden free graph access or bit-complexity
claim is inferred. The initial full-curve tree witness computation was
terminated without a result; a simpler exact positive-face tree validator
completed all three finite cases in 5.587 seconds.

**Verification:** The 124-page note builds without final warnings or
unresolved references; the new proof pages were visually reviewed. All
64 own scripts pass focused lint/format and three registry tests pass.
Required broad checks retain the same 231 passing tests and three baseline
failures, two unrelated lint findings and two oversized AESP sources.
All five baseline hashes are unchanged; reproduction stops at its test
prerequisite. See `OVERNIGHT_20260907_BLOCK12_AUDIT.json` and
`VERIFICATION.md`. Formal note dependencies remain empty.

**Next decision:** prioritize potential-driven local discovery or the
geometric boundary-event interface; separately close the weighted supplied
constructor contract. The morning note gives specific success criteria.

## Historical second-night block 11: spectral edge floors and recursive ranges

**General OP3 remains Open.** The new section
`sec:op3-recursive-vwf-ranges` proves a paid preconditioner edge-floor
wrapper, complete one-step range propagation and a simultaneous
logarithmic bound through a supplied mixed recursion. Deleting sufficiently
small preconditioner edges and doubling retained weights preserves spectral
order at twice the quality; every forest bridge survives. The original
objective is unchanged, so this uses no objective-error budget.

The range induction controls energy and graph weights first, then final
slopes/curvature, then domains and breakpoints. With depth D, size/quality
bound P and initial numerical bound Z, logarithmic ranges and compression
bins are O((D+1) log P+log Z). No minimum positive curvature drop, gap or
split separation is assumed. These are **Proved here** drafts. They are
not a statement that every encountered nonzero meets CPW Assumption 3.15.

**Measured:** The spectral audit passes 150 cases, 750 exact PSD
certificates, 5,598 cut certificates, 213 bridge checks and 21 threshold
ties. The range audit passes 108 proximal/forest steps and 432
residual/compressed-child steps, including 27 zero initial gaps, 121
negative individual model slopes and 135 positive compression errors.
Common energy scales and signed events at 2^-100 are included. Dense
minima, matrices and cuts are validators, not production costs.

**Source / next target:** CPW's constructor still explicitly assumes a
polynomial weight ratio. The underlying Abraham–Neiman arbitrary-weight
low-stretch-tree and Koutis–Levin–Peng fixed-precision sparsifier statements
were checked in their primary PDFs and recorded in the literature index
and topic note. Resume `SUPPLIED_GLOBAL_RECURSION_PROBE.md`: reconcile a
complete weighted constructor/confidence contract, formalize the full
supplied work recurrence, and run a genuinely nested accelerated audit.
These full-recursion claims remain **Conditional** here. Local discovery
and cumulative graph work remain **Open**.

The 117-page note builds without warnings or unresolved references;
pages 112–115 were visually reviewed. All 56 scripts pass focused
lint/format and three registry tests pass. Broad checks retain the same
baseline failures and five unchanged hashes; reproduction stops at the
test prerequisite. See `OVERNIGHT_20260907_BLOCK11_AUDIT.json` and
`VERIFICATION.md`. Formal note dependencies remain empty.


## Historical second-night block 10: mixed additive numerical recursion

**General OP3 remains Open.** The new section
`sec:op3-mixed-additive-oracles` proves compression embedding, guarded
relative refinement and accelerated accuracy while retaining an explicit
additive error. The recursive budget is
`eta_child=eta_parent/(2^34*kappa_parent)`. It needs no unknown negative
optimum or positive gap floor. These are **Proved here** drafts; recursive
preconditioner construction, graph ranges and fast work remain **Conditional**.

**Measured:** The dense forward-piece reference passes 747 exact minima,
2,830 bound quadratic solves and 192 independent tree comparisons. Mixed
acceleration passes 153 invocations and 4,896 complete step certificates,
including 640 nonzero errors at zero initial gap. The implemented persistent
forest/compression/refinement/recovery pipeline passes 61 cases and 942
coarse calls, including 188 positive compression-error checks, 570 nonzero
negative regularization shifts and 484 paid failed improvement guards.
Signed splits at 2^-100 and the actual kappa=4 recursive tolerance are
included. Dense coarse solves and dyadic candidate rounding are validator
work; no fast oracle or bit-complexity claim follows from their timing.

An initial reference run exceeded decimal serialization limits because
successive exact candidates developed large denominators. Upward dyadic
rounding with an exact energy guard repaired the reference policy; no
mathematical inequality had failed. All final source/backend hashes match.

**Next falsifiable target:** `COARSE_GRAPH_RANGE_PROBE.md` saves a spectral
preconditioner edge-floor wrapper and simultaneous energy/range induction.
They are unproved candidates at this checkpoint. Actual CPW construction
and shrink costs still need source verification. The 114-page note builds
without final warnings; pages 108–113 were visually reviewed. All 54
scripts pass focused lint/format and three registry tests pass. Required
broad checks retain the same baseline failures and five unchanged hashes.
See `OVERNIGHT_20260907_BLOCK10_AUDIT.json` and `VERIFICATION.md`.
Formal note dependencies remain empty; prior source imports are unchanged.


## Historical second-night block 9: persistent exact VWF forest elimination

**General OP3 remains Open.** `thm:op3-persistent-vwf-forest` implements
exact elimination on a supplied forest whose remaining edges join retained
roots. It stores immutable derivative curves with exact integral aggregates,
correct Lift constants and signed lower endpoints. It returns canonical
root functions, copied coarse edges and saved child responses for exact
conditional recovery. With W=sum(input split count+2), work is
O(m+W log^2(2+W)) and all newly allocated words are
O(m_root+W log^2(2+W)), including retained versions. Recovery costs
O(n log(2+W)) work and total allocation. These are **Proved here** drafts.

`lem:op3-correct-vwf-lift` proves the corrected negative constant term and
boundary formulas. `lem:op3-affine-derivative-integrals` proves the lazy
integral transform. `prop:op3-vwf-forest-ranges` bounds one exact pass's
splits, terminal slopes, curvature and values at zero. Individual terminal
slopes may be negative. `cor:op3-generic-proximal-terminal-mass` bounds
the positive tail mass supplied by an accelerated normalized model.

**Source / context:** CPW already gives fast degree-one VWF elimination
in Lemmas 6.1 and 6.6; this is an independently implemented and audited
representation of that approach, not a claim that elimination is new.
PDF pp. 30–34 were visually checked. Algorithm 6 eliminates before
compression. The note records the checked constant-sign correction on
pp. 40–42 and states an explicit saved-child recovery contract to avoid
the parent-descriptor ambiguity in Algorithm 7.

**Measured:** The explicit reference passes 3,000 scalar Lift cases,
16,997 full polynomial identities and 192 tree reconstructions in 4.390
seconds. The persistent audit passes 1,000 scalar operation/persistence
cases, 34,404 complete curve intervals, 5,941 saved versions and 9,081
general affine integral checks. It reconstructs 192 trees, certifies 15
retained-root field assignments, rejects three invalid graph shapes and
checks nine larger cases through 512 vertices. Every coordinate in the
larger outputs is positive. Canonical exports match exact coefficients.
The final full persistent audit took 54.119 seconds; old helper hashes remain
unchanged. Reference pieces and original KKT are validator work.

**Next falsifiable target:** `ADDITIVE_RECURSION_PROBE.md`. Formalize
and audit compression, refinement and acceleration with mixed relative
and additive guarantees, including zero gap. Then trace the actual recursive
preconditioner/graph scales and work. The new additive-budget schedule and
dense forward-piece coarse validator are **Conditional candidates**.
Fast recursive coarse work and unknown-support local discovery remain
**Open**. The 111-page note builds without final warnings; final pages 4
and 104–109 were visually reviewed. All 51 direction scripts pass focused
lint/format and three registry tests pass. Required broad checks retain the
same baseline failures and five unchanged hashes. Details are in
`OVERNIGHT_20260907_BLOCK9_AUDIT.json` and `VERIFICATION.md`.


## Historical second-night block 8: generic proximal tolerance and canonical ranges

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

- Formal registry dependencies: `problem_definitions`.
  The third campaign imports Proposition 5 in its proof-attempt supplement
  for the star formula and fixed-parameter sparse-output argument.
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
