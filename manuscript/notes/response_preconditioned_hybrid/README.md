# response_preconditioned_hybrid

This standalone note defines a common active-set interface for the project's
iterative and persistent-response solver lines. It does not claim that a mixed
method is universally optimal. Instead, it proves the generic block-response,
dual-local orthogonal-correction, boundary-interval, uniform-leverage,
response-energy-packing, monotone boundary-variation, geometric-rebuild, and
probe-before-rebuild lemmas and states a conditional
composition theorem whose two endpoints are the local iterative product scale
and an output-sensitive incremental SDD/Schur solver.

The proposed method stores a response representation for a settled anchor,
uses a frontier buffer for newly admitted vertices, performs aggregate
preconditioned repair, and materializes the old-face correction only at final
output. The unresolved graph-uniform ingredient is certified finite-band
boundary reporting on nonequitable cyclic cores; no uncharged boundary scan or
future-support oracle is hidden in the interface.

The no-restart numerical half is now closed conditionally on charged response
application. For every support expansion, the whole lifted Schur-frontier
space is energy-orthogonal to all earlier lifted frontier spaces. Consequently
arbitrary certified frontier-solve errors add exactly in quadrature, and the
settled face never needs to be optimized again. This does not hide the dense
lift: all applications of the old-face response remain in the explicit
`U_lift` charge.

Successive exact corrections on nested faces are `Q`-orthogonal. Their primal
vectors can be dense, but applying `Q` annihilates the whole old face and
leaves a dual signature only on the new batch and current boundary. This is
the precise surviving locality of an orthogonal evolving-set method. The
missing implementation must produce or query that dual signature from an
implicit response without materializing the dense primal correction.

Eliminating the settled face gives an exact positive dual-transfer operator
from the current batch demand to all exterior demand increases. This rewrites
support discovery as monotone threshold reporting for implicit nonnegative
Schur transfers; it is a narrower target than maintaining every primal
coordinate after every expansion. Schur associativity additionally proves
that any consecutive interval of light transfers may be replaced by one exact
aggregate transfer without changing its endpoint, exterior demands, or the
operator seen by future events. The remaining cost is representation and
crossing discovery, not trajectory correctness.

The boundary-variation ledger proves that every still-inactive normalized
demand is monotone and that all such motion has total degree-weighted mass at
most `(1-alpha)/2`. Thus exact keys cross a fixed threshold only once. The
remaining difficulty is to route an implicit dense Schur increment to all
crossing keys; publishing additive `alpha*tau` scalar updates merely recovers
the classical `1/(alpha*tau)` accounting.

A source-aware leverage theorem now exploits the fact that a nested correction
is generated on the newly admitted batch `B`. The squared exterior leverages
sum to at most `|B|`, yielding an a priori degree-volume bound on ambiguous
finite-band intervals without materializing the dense correction. A matched
edge construction shows why the older source-oblivious energy interval is not
enough: it can mark every boundary row ambiguous after a one-row change and
force quadratic refresh. A rank-sensitive locator lemma proves that a
bounded-arity hierarchy with constant-factor aggregate leverage-mass queries
finds all potentially ambiguous rows with probe count controlled by `|B|`,
the correction energy, and hierarchy depth---not by boundary size. The
remaining data-structural target is a local squared-response range-add that
implements those group traces on nonequitable cyclic cores.

The source-aware mass has now been identified exactly with a simpler object.
For a batch elimination `A -> A union B`, the squared leverage at an exterior
vertex is the decrease of that vertex's diagonal in the terminal Schur
complement. These diagonal losses telescope to at most `(1-alpha)/2` for each
still-exterior label, independently of the number of earlier batches. Group
masses are therefore weighted aggregate Schur-diagonal losses. The hierarchy
needs only a certified one-sided estimate with additive error proportional to
its current pruning threshold; multiplicative accuracy on tiny groups is not
required.

The diagonal-loss ledger and the orthogonal correction-energy ledger combine
multiplicatively. Over any epoch in which an exterior label remains asleep,
its normalized response uncertainty is at most the square root of the
accumulated diagonal loss times the accumulated correction energy. Summing
over disjoint wake-up epochs gives a second Cauchy--Schwarz telescope. For a
unit seed, the total correction energy is at most `alpha`; since the total
diagonal loss of label `v` is at most `(1-alpha)/(2*d_v)`, wake-ups at margin
`Theta(alpha*tau)` occur at most
`O(1/(tau*sqrt(alpha*d_v)))` times per label. This is a proved response-side
`1/sqrt(alpha)` mechanism, not a global running-time theorem: summing over all
live labels can still be too expensive, and maintaining the diagonal-loss
ledger is precisely the unresolved operation.

There is also an exact route from that operation to spectral graph machinery.
After scaling by `D^(1/2)`, the PageRank matrix becomes the grounded Laplacian
`((1-alpha)/2)*(D-A) + alpha*D`: original graph edges have conductance
`(1-alpha)/2`, and every vertex has a ground edge of conductance `alpha*d_v`.
Schur complements, diagonal losses, and normalized exterior responses respect
this congruence. The dynamic spectral-vertex-sparsifier and electrical-flow
locator of van den Brand et al. therefore supplies a concrete construction
blueprint. Its published preprocessing, update, and query costs are global in
the ambient graph and do not prove the desired local bound; the new target is
to make its terminal/locator epochs exposure-charged and schedule them by the
two-ledger product rule.

At the information level, the ambient graph is no longer an obstacle. For a
current face, its response rows and diagonal losses depend only on the face's
internal edges, the cut incidences exposed by scanning its rows, and one degree
query per distinct boundary label. Edges wholly in the exterior do not enter
the formulas. The complete static locator record therefore has size linear in
charged exposed volume. A Chebyshev inverse-square-root sketch now constructs
simultaneous one-sided estimates of every exposed boundary diagonal loss in
`O_tilde(cvol(S) / sqrt(alpha))` work. Geometrically spaced full checkpoints
therefore have the same final-volume product cost. What remains open is the
incremental update/query cost between rebuilds, not acquisition of the
unexposed graph or a full checkpoint scan.

A fixed-anchor sketch identity further connects the two solver arms. For any
linear measurement matrix on normalized exterior dual demands, precompute its
transposed harmonic extensions through the anchor. An exact frontier solution
then updates the complete exterior sketch from frontier-incidence scans and
the touched rows of those stored extensions. Its known frontier source is
subtracted explicitly. No dense old-face correction or boundary scan appears.
This makes CountSketch, sparse-recovery, and hierarchy measurements concrete
backend candidates, while leaving the number of measurements, anchor solves,
stored-row reads, and within-epoch updates fully charged.

A two-sided Gaussian lemma now makes the measurement count explicit. Source
probes on the normalized frontier and target probes supported on a reached
hierarchy node estimate that node's complete leverage mass through
polylogarithmically many scalar transposed harmonic measurements. Combined
with leverage packing, only output-sensitive nodes are tested; neither the
dense exterior response nor an all-leaf squared update is formed.

A coded bucket theorem now removes the remaining per-node target-row count.
For one fixed event, a signed hash-and-bit bank shared by the whole packed
query contains every potentially ambiguous row at normalized margin `m` and
certified correction-energy radius `E` with high probability; exact validation
removes false candidates. Both its target dimension and its candidate list are
`O_tilde(1 + |F| E^2 / m^2)`, exactly the ambiguity-packing scale and not the
ambient boundary size. The bank is compatible with the transposed harmonic
identity and can be defined on global vertex identifiers before the current
boundary is known. Exact validation now removes the adaptive-target obstacle:
a first-failure coupling permits one hash/sign bank per doubling capacity to
be reused throughout the epoch. Across all capacities, the number of distinct
target rows is controlled by the largest realized packed query, rather than
the sum of all per-event dimensions. Fresh Gaussian source probes retain a
summable whole-trace failure budget. The harmonic product also has exact
target and source orientations. An online rent-or-buy rule at each capacity
uses at most twice the smaller of its target-row count and cumulative source
width in anchor right-hand sides, with no future-trace advice. The rental
branch streams the implicit coded bank through one anchor-cut scan; the
purchase branch stores target extensions. Target-bank construction, every
source-side cut scan, every later stored-row read/application, source preparation,
measurement/decoder workspace, boundary-membership maintenance, and exact
candidate validation remain explicit charges. The open
primitive is therefore an aggregate bound for the repeated cut scans or
stored-response applications, not the measurement dimension, adaptive
randomness, anchor-right-hand-side count, or output-sensitive reporting.

The packed query now extends from one common margin to a whole checkpoint
segment with heterogeneous slacks. Divide each far boundary row by its own
initial distance to the gate, while keeping the width-`m` transition band
explicit. If the segment admits total batch size `b` and accumulates exact
orthogonal correction energy `mathcal E`, every far label that crosses the
gate is contained in one heavy-row query. Both its target dimension and the
degree volume of true far crossings are
`O_tilde(1 + b*mathcal E/m^2)`. For the literal realized gate, the single
vector of accumulated demand change divided by checkpoint slack is enough:
its scalar bucket measurements update causally, so neither Gaussian sources
nor source history are needed. If direction-independent row energies are
required, a Gaussian map reduces all concatenated batch sources to logarithmic
width, and the decoder retains only append-only squared bucket norms. This
closes heterogeneous-slack packing, realized source dimension, and fixed-bank
source-history state. Round 020 identifies the first exact boundary of that
state: after a genuine checkpoint-slack reweight, retained squared bucket
norms alone need not determine the refreshed decoder. Installing or applying
the slack-weighted harmonic rows, enlarging bank capacity, a paid replay or
richer-state policy for changed checkpoint weights, transition-band
maintenance, and exact validation remain unresolved in aggregate.

Exact source whitening is no longer hidden: a Chebyshev
polynomial of any constant-factor spectral frontier prepares all Gaussian
sources once in `O_tilde(T_mv / sqrt(alpha))` work and preserves every group
mass within an explicit constant. In the exact backend, one frontier
matrix-vector product uses one charged anchor-response application.

There is now a second, monotone source construction that is closer to the
delayed-push mechanism. A positive geometric quadrature approximates the
frontier inverse square root by logarithmically many shifted Stieltjes
resolvents. The sum of their shifted work masses is at most
`1 / sqrt(alpha)`, and residual coordinate settlement across the whole ladder
has the same accelerated alpha dependence in the Schur-coordinate model.
Every shifted resolvent is exactly a sparse face solve with extra diagonal
killing only on the frontier. Any unfinished solve is an exact nonnegative
anchor debt; settling that debt later produces precisely the corresponding
shifted Schur residual. Thus target harmonic rows are not algebraically
necessary. What remains is to amortize the sparse propagation and delayed
anchor settlements in graph work on a high-rank core.

That last transfer cannot be made literally row by row. On the one-edge graph,
the first shifted-resolvent rung is a two-coordinate sparse system. One exact
Schur-coordinate settlement finishes it, but exact sparse coordinate pushes
are forced to alternate and need `Omega(1 / alpha)` row touches even to reduce
the rung residual by a fixed factor. The delayed-debt identity therefore
removes the algebraic target-row requirement but does not itself remove the
repeated-work factor. A block response, elimination, accelerated transport,
or dynamically sparsified substitute is genuinely necessary. This is an
algorithm-specific obstruction to literal exact pushes, not a lower bound for
all sparse or response implementations.

The fixed-face aggregation problem is closed in a deliberately frozen model:
`(A,F)`, the exposed cut, and the shifted ladder remain fixed while additive
nonnegative fragments arrive. The scalar theorem charges every fragment
coordinate in `C_frag`; `r` nonnegative columns cost the sum of their `r`
Chebyshev runs, and signed columns are split into positive and negative streams
with no pre-certificate cancellation credit. In exact-real arithmetic a
signed Chebyshev semi-iteration flushes one scalar aggregate in
`O_tilde(cvol(T) / sqrt(alpha) + C_frag)` work. The note gives complete
eleven-coordinate vectors for one fixed-face flush and a geometric sequence of
flushes, including adjacency and interaction rounds, coefficient/control
work, recurrence and cut-response applications, retained debt, workspace,
materialization, validation, and emission.

The energy certificate implies a simultaneous mathematical interval for every
exterior response, but this quantifier does not itself implement
`BoundaryBounds`. The named `AllBoundaryFlush` realization explicitly scans
the cut, materializes and classifies every current boundary interval, and pays
for every emitted record; it is a complete checkpoint, not an output-sensitive
partial reporter. Signed interior iterates never control support admission.
On the one-edge example the flush uses `O(1 / sqrt(alpha))` complete two-row
sweeps, consistent with the literal exact-push `Omega(1 / alpha)` individual-
row obstruction. Geometrically growing fixed-decision faces retain the
final-volume product bound only with the stated column and fragment charges.

Round 013 isolates the first frozen high-rank representation STOP after that
GO. On the fixed notched-double-sun face containing all cyclic/chord anchors
and all source petals, the first shifted rung has an exact dense response to
every report leaf. For each fixed size and sufficiently near-one `alpha`, its
matching entry is `Theta(vartheta^2)` while every off-match is
`O_n(vartheta^3)`, where `vartheta=(1-alpha)/2`. Gate
`g=vartheta^(5/2)` and band `m=g/2` therefore emit exactly one new delta label
per unit petal fragment and keep all other unreported labels outside the band.
The named `EagerExactSlack` policy nevertheless rewrites every separately
addressed exact unreported-label slack after every light event. It pays
`Theta(p n^2)` response/control/materialization work for `Theta(r n)`
delta/certificate output, with `p=r` for nonnegative columns and `p=2r` for
signed-split certification; its full vector is
`eq:notched-sun-eager-eleven-vector`. This is an exact-real fixed-face
representation/query obstruction only. The fragment trace is not an RPPR
chronology, and the proposition does not refute implicit cyclic transfer,
packed coded queries, scale truncation, on-demand validation, or an
output-sensitive partial flush.

Round 014 gives the matching narrow GO on that exact calibration trace.
`NotchedSunScaleDelta` first validates the complete frozen
cycle–chord–petal–report template, cut, ladder, event order, and stream mode.
For the explicit near-one range
`0 < vartheta <= 1 / (1296 n^2)`, a nonnegative Neumann expansion has kernel
norm at most three. Its length-one matching term is already above
`g = vartheta^(5/2)`, while the uniform tail over every still-unreported label
is at most `g/2`. The reporter therefore retains only the template and label
map, ladder, event counter, and stream metadata. It checks every incoming
fragment, then emits `w_k` and one universal future-safe certificate per
logical column without forming a response column or slack cell. Its complete
vector is `eq:notched-sun-scale-delta-eleven-vector`; total work is linear in
`n + J + p + C_frag + r n`, with `p=r` and `C_frag=rn` for nonnegative
columns or `p=2r` and `C_frag=2rn` for the separately checked signed
`2-minus-1` streams. This is a fixed-template, fixed-order, exact-real,
scale-aware partial reporter—not a dynamic reporter for arbitrary fragments
or a PPR/RPPR chronology. It demonstrates constructively why the
`EagerExactSlack` STOP cannot be broadened to this template-aware
representation.

Round 015 relaxes exactly that reporter's prescribed common event order.
`NotchedSunPermutationDelta` accepts any online-verified permutation of the
same unit petal events. At each interaction it checks that every stream names
the same valid, previously unseen petal with the required amplitude, marks one
seen-label entry, emits the paired report label, and certifies the unreported
complement using the same prefix-length Neumann tail. The matching lower bound
and off-matching upper bound are pointwise and hence independent of the
permutation. The complete vector
`eq:notched-sun-permutation-eleven-vector` remains
`(Theta(n),2,n,Theta(n+J+p),Theta(C_frag+rn+n),0,0,Theta(n+J+p),O(1),0,Theta(rn))`.
Thus `p=r`, `C_frag=rn` for nonnegative columns and `p=2r`, `C_frag=2rn`
for separately read signed `2-minus-1` streams. The seen set is absorbed in
linear template memory, and there is still no response application,
future-label scan, slack cell, or numerical materialization. This changes no
other axis: the face, cut, ladder, label pairing, amplitudes, fixed `n`,
near-one scale, exact-real model, and common cross-stream schedule remain
promised. Repeats, different per-column orders, batches, arbitrary fragments,
RPPR chronology, fixed-alpha uniformity, and finite precision remain outside
scope.

Round 016 relaxes exactly the no-repetition clause while retaining complete
petal coverage. `NotchedSunMultiplicityDelta` preprocesses positive exact
multiplicities `mu_i`, accepts any online-verified common permutation of that
multiset, and atomically rejects bad labels, amplitudes, exhausted counts, or
events beyond `L = sum_i mu_i`. The total length `L` is authoritative for
interaction and fragment charges; the exact last-unseen horizon
`H = L - min_i mu_i` is authoritative for the nonvacuous tail certificate.
Solving the scalar Neumann inequality without a relaxed constant gives

`vartheta <= 1 / (sqrt(81 H^2 + 3) + 9 H)^2`,

equivalently `18 H sqrt(vartheta) + 3 vartheta <= 1`. At a label's first
occurrence the matching response crosses and one delta is emitted; on a
repeat the label is already reported, no delta is emitted, and every unseen
label remains below `g-m`. One counter per label replaces the seen bit but
retains linear persistent state and stores no response or slack coordinate.
The complete vector `eq:notched-sun-multiplicity-eleven-vector` is
`(Theta(n),2,L,Theta(n+J+p),Theta(C_frag+rL+n),0,0,Theta(n+J+p),O(1),0,Theta(rL))`,
with `C_frag=pL=rL` for `p=r` nonnegative streams and `C_frag=pL=2rL` for
`p=2r` separately checked signed streams. The scale is sharp only for the
displayed uniform template Neumann envelope, not a generic scalar-potential
or reporter lower bound. Unbounded repetitions, arbitrary fragments or
amplitudes, batches, per-column orders, RPPR chronology, fixed-alpha
uniformity as `L` grows, and finite precision remain outside scope.

Round 017 relaxes the unit-logical-amplitude clause to one finite positive
exact-real occurrence schedule shared by every logical column and physical
stream. For label `i`, declared prefix masses `A_(i,k)` are compared with the
response-mass capacity

`kappa_i = d_(u_i) (1 + c_eta) sqrt(vartheta)`.

Its first certified index `k_i*` is the first prefix strictly above that
capacity; it may be larger than one. The pre-crossing gap
`gamma_i = kappa_i - A_(i,k_i*-1)`, event horizon
`H_i = L - mu_i + k_i* - 1`, and full interleaving mass horizon
`F_i = A - A_i + A_(i,k_i*-1)` distinguish unseen, seen-but-unreported, and
already-reported labels. With

`lambda_i = vartheta^2 / (d_(u_i) (1 + c_eta))`,
`epsilon = 9 vartheta^3 / (1 - 3 vartheta)`, and
`m_A = min_i(lambda_i gamma_i - epsilon F_i) > 0`,

`NotchedSunAmplitudeDelta` certifies every unreported label below `g-m_A` and
emits `w_i` exactly when occurrence `k_i*` arrives. Thus the certified crossing
is the first exact strict crossing even when earlier positive occurrences were
too small. The reporter stores one common prefix schedule, crossing indices,
and counters but no response or slack coordinate. Its complete vector
`eq:notched-sun-amplitude-eleven-vector` is
`(Theta(n),2,L,Theta(n+J+p+L),Theta(C_frag+rL+L+n),0,0,Theta(n+J+p+L),O(1),0,Theta(rL))`.
Here `C_frag=rL` and total absolute supplied coefficient mass is `r A` for
`p=r` nonnegative streams; `C_frag=2rL` and absolute mass is `3r A` for the
separately checked signed `2-minus-1` streams. Every fixed finite positive
schedule passes at a sufficiently near-one scale. Failure of the displayed
margin rejects only this scalar certificate, not every reporter. Undeclared
or unbounded mass, arbitrary signed logical amplitudes, per-column schedules,
batches, arbitrary fragment support, RPPR chronology, fixed-alpha uniformity,
and finite precision remain outside scope.

Round 018 relaxes exactly the common logical-column schedule. Each column
`q` declares its own positive schedules `a_(q,i,k)`, lengths `L_q`, and
logical mass `A_q`; the accepted stream may arbitrarily interleave one event
from any column. The structural capacity is still

`kappa_(q,i) = d_(u_i) (1 + c_eta) sqrt(vartheta)`,

but its crossing index, pre-crossing gap, local mass horizon, and margin are
column-specific. In particular,

`F_(q,i) = A_q - A_(q,i) + A_(q,i,k*_(q,i)-1)` and
`m_q = min_i(lambda_i gamma_(q,i) - epsilon F_(q,i)) > 0`.

The global asynchronous event horizon is
`H^(async)_(q,i) = L_Sigma - mu_(q,i) + k*_(q,i) - 1`, whereas unrelated
columns never enter `F_(q,i)` because they do not change response column `q`.
`NotchedSunColumnAmplitudeDelta` therefore emits one updated universal
certificate only for the affected column; certificates for all other columns
remain unchanged. It emits exactly `r n` deltas over the epoch. With
`L_Sigma = sum_q L_q >= r n`, its full vector
`eq:notched-sun-columnwise-amplitude-eleven-vector` simplifies to
`(Theta(n),2,L_Sigma,Theta(n+J+p+L_Sigma),Theta(C_frag+L_Sigma),0,0,Theta(n+J+p+L_Sigma),O(1),0,Theta(L_Sigma))`.
Here `C_frag=L_Sigma` and absolute physical mass is `A_Sigma` for the
nonnegative interface; `C_frag=2L_Sigma` and absolute mass is `3A_Sigma` for
the atomically paired signed `2-minus-1` interface. The reporter stores all
declared schedules and `r n` counters but no response or slack coordinate.
It still excludes undeclared or unbounded mass, arbitrary signed logical
amplitudes, signed pairs split across interactions, simultaneous batches,
arbitrary fragment support, RPPR chronology, fixed-alpha uniformity, and
finite precision. A failed per-column margin rejects only this scalar
certificate. The cross-direction lesson is conditional: global latency can
be separated from local certificate mass only when unrelated events provably
leave that state block unchanged.

Round 019 removes exactly the one-logical-event interaction restriction.
`NotchedSunBatchAmplitudeDelta` accepts any finite sequence of nonempty
simultaneous batches whose tagged records are the next consecutive declared
occurrences in each touched column--label cell. A batch may mix columns,
labels, and several occurrences of one cell. The reporter stages the entire
batch, verifies every tag, amplitude, cap, stream identity, and atomic signed
`2-minus-1` pair before committing, and rejects a duplicate, replay, gap,
split pair, or mismatch without changing persistent state. At a batch
boundary it emits exactly the cells satisfying

`c_(q,i)^- < k*_(q,i) <= c_(q,i)^+`

and one universal remaining-label certificate per affected column. The same
column-local mass horizon remains valid because simultaneous positive
increments commute and every other-label mass was already included in
`F_(q,i)`; other-column mass still changes a disjoint response block. This is
an exact first crossing only at atomic batch boundaries---there is
deliberately no hidden order or subevent certificate inside a simultaneous
batch.

For `B` accepted batches, `L_Sigma` logical records, affected-column count
`S_Sigma`, and maximum batch size `b_max`, the complete vector
`eq:notched-sun-batch-eleven-vector` is

`(Theta(n),2,B,Theta(n+J+p+L_Sigma),Theta(C_frag+L_Sigma),0,0,Theta(n+J+p+L_Sigma),O(b_max),0,Theta(S_Sigma+rn))`.

The physical ledgers stay distinct: nonnegative mode has
`(p,C_frag,absolute mass)=(r,L_Sigma,A_Sigma)`, while atomically paired signed
mode has `(2r,2L_Sigma,3A_Sigma)`. The theorem keeps the fixed template,
face, cut, ladder, pairing, fixed `n`, complete finite declared positive
schedules, per-column margin, and exact-real arithmetic. It does not cover
undeclared or unbounded mass, arbitrary signed logical amplitudes, split
signed pairs, cross-column coupled response, arbitrary fragment support, RPPR
chronology, fixed-alpha uniformity, or finite precision. A failed margin is
still only rejection by this scalar reporter.

Round 020 leaves that frozen separated-batch line and changes actual
checkpoint slack weights in a reused packed bucket. Proposition
`prop:three-label-norm-only-reweight-obstruction` fixes one hash repetition,
one bucket, labels `00,01,10`, and realized positive signs. The scalar source
histories `(-4,1,1)` and `(-2,-1,-1)` have the identical complete retained
norm state `(A_1,C_1,A_2,C_2)=(1,9,1,9)` under unit weights. After the genuine
inverse-slack refresh `(1,1,1)->(1,3,2)`, the first bit test is `9>4` for the
first history and `9<16` for the second. A two-source nonnegative variant has
common old state `(1,5,1,5)` and flips as `9>8` versus `9<10`. Therefore the
named `NormOnlyWeightRefresh` state cannot accept every such refresh without
old-source information. Three colliding labels are minimal: with at most two,
a separating bit gives the individual row norms, and any grouped old norm
supplies the only missing inner product.

The exact no-replay policy stages and validates the version/capacity header
and three new weights, then rejects without persistent mutation. Its full
vector is

`(0,0,1,0,Theta(1),0,0,Theta(1),Theta(1),0,1)`.

The explicit accepted `ReplayThreeWeightRefresh` comparator reads the six old
response cells of the nonnegative witness, writes four two-cell reweighted
measurements and four updated norms, and emits one decoder record. Its full
vector is

`(0,0,1,0,Theta(1),0,6,Theta(1),Theta(1),12,1)`.

If those cells were not retained, rebuilding them must instead add the actual
source-side anchor-cut scan and response application, plus any newly exposed
adjacency. This is a one-bucket exact-real named-state STOP, not a lower bound
against richer Gram state, source replay, cut rebuilding, collision-free
banks, another decoder, or another support-safe trace. It proves no RPPR/KKT
chronology, terminal solver, finite-precision, word, or bit result.

The remaining online question is not resolved by sleeping. For every fixed
path length, a family-dependent sufficiently small positive `rho_n` makes the
ambient-degree, endpoint-seeded canonical all-violations trace admit one new
vertex at a time, while successive charged-volume ratios tend to one. No
positive lower bound on `rho_n` uniform in the path length is asserted. The
note cites the fully charged append-only path `LDL^T` response and records its
full vector, so this is a scheduling obstruction rather than a path work lower
bound. The literal gate still needs an output-sensitive partial flush after
some light events, or a separately proved alternative safe response trace.

The target side is also closed under a precise structural parameter. If the
normalized anchor--boundary cut has rank `s`, one bank of `s` harmonic basis
vectors answers every hierarchy measurement from the touched anchor rows. A
linear-volume comb tree shows this cannot be a universal shortcut: its cut
rank is full, its harmonic bank is dense, and every lower-rank approximation
has energy-operator error at least `(1-alpha)/(2*sqrt(3))`, hence constant in
the comb length for fixed `alpha < 1`. The remaining target is therefore
online scheduling or partial application of the positive debt ladder, or
on-demand sparsification giving the same work, on high-rank nonequitable
cores—not a generic low-rank factorization. A complete fixed-face aggregate
flush is already exposure-charged at the product scale.

The whole group-query primitive is now closed whenever the normalized
anchor--boundary cut has small rank. Factor the cut as `B*C`, solve the anchor
only for the columns of `B`, and split each normalized exterior response into
a sparse direct vector minus a low-rank harmonic vector. Every hierarchy-node
squared norm is then an exact quadratic of three additive summaries. Only the
source Gaussian probes remain, and Chebyshev prepares them at the accelerated
frontier scale. Polylogarithmic cut rank therefore gives a complete packed
reporter after charged preprocessing. This
cannot be the universal argument: a comb tree consisting of an active path
with one exterior leaf per path vertex has linear cut rank, a dense full-rank
harmonic bank, and best rank-deficient energy error at least
`(1-alpha)/(2*sqrt(3))`, independent of its length for fixed `alpha < 1`.
The obstruction rules out universal low-rank materialization, not implicit
tree recurrences.

A concrete cyclic stress test now also closes one tempting loophole. In a
“notched double sun”—a cycle-plus-chord anchor with one frontier petal and one
exterior report leaf at every anchor vertex—the cut has full rank and the
natural partition is nonequitable. A prescribed structural face sequence has
a linear number of singleton additions inside one geometric epoch. Every exact
loss vector is dense for every `alpha in (0,1)`. For each fixed `n`, there is
an `alpha_n < 1` such that, for `alpha in (alpha_n,1)`, the
`Theta_gamma(n)` vectors in the prescribed fixed-`gamma` epoch are linearly
independent. As `alpha` tends to one, the matching loss is
`Theta((1-alpha)^4)` while every off-matching loss is
`O_n((1-alpha)^6)`. Thus squaring the response does not create an exact
polylogarithmic-dimensional fixed linear target tag. Literal all-leaf updates
and explicit harmonic-row materialization expose their full word charges.
This is deliberately not a finite-band lower bound: a scale-matched additive
oracle may ignore the smaller off-matching tail, and nonlinear, adaptive,
sparse-recovery, and cyclic separator representations remain viable. It is
also not yet an RPPR-trajectory counterexample: no load or KKT gate producing
the prescribed admission order is claimed.

That limitation is now calibrated constructively. For each fixed `n` and
additive-oracle parameter `beta`, there is an `alpha_bar_(n,beta) < 1` such
that `alpha > alpha_bar_(n,beta)` and finite-band threshold
`((1-alpha)/2)^5` keep only the report leaf matched to the admitted petal;
the sum of every off-matching tail lies inside the allowed additive band. An
explicit one-sided group oracle therefore follows one hierarchy path and
validates one leaf. This counts group queries and leaf validations; hierarchy
and membership-state maintenance and exact-validation arithmetic remain
separate charges. The family remains useful against exact fixed linear tags,
but it cannot support a lower bound at this separated scale only in the stated
fixed-`n`, near-one-`alpha` regime. No conclusion is proved for fixed `alpha`
as `n` grows or for another joint parameter regime or reporting scale.

The same trace now gives an explicitly charged adaptive-epoch implementation
audit. For each `n`, choose an `n`-dependent
`alpha_n^star > max(alpha_bar_(n,beta), 3/4)`; this is not a uniform
fixed-`alpha` assertion. At event `k`, after the anchor, singleton frontier,
margin, and capacity are fixed, draw a fresh independent Gaussian source block
and a fresh independent hash/sign target block. The schedule
`delta_k = delta / (k(k+1))` gives a simultaneous whole-epoch guarantee,
and all resulting source-probe and target-repetition logarithms are retained.
The coded bank finds the unique separated report leaf after current-boundary
and report-membership lookups and exact validation. However, the literal
implementation that explicitly
stores its fresh transposed harmonic table has `|A_k| * p_k` cells, where
`p_k = (L+1) B_k R_k` while the candidate cap is only `B_k R_k`. Across the
`Theta_gamma(n)` events, table writes alone are at least
`n (L+1) sum_k B_k R_k`, whereas charged volume plus all candidate caps is
`O_gamma(sum_k B_k R_k)`. The note separately charges source preparation,
right-hand-side construction and anchor solves, stored-row reads, direct
frontier/hash work, decoder and random-block work, peak workspace, the
report-membership dictionary, exact validation, adjacency exposure, and
output. This rules out only per-event fresh **explicit dense harmonic-table**
materialization. The certified adaptive-reuse theorem now removes the need to
rebuild the target layer per event: one bank per doubling capacity suffices.
The audit does not rule out implicit or batched construction of those reused
banks, compressed row access, dynamic terminal
sparsifiers, cyclic transfer states, or sparse recovery; nor does it turn the
prescribed structural trace into an RPPR trajectory or a reporter lower bound.

The complementary energy-packing ledger proves that the squared exterior
demand change across any nested exact-face expansion is at most the primal
energy shock. Boundary degree volume moving by normalized margin `theta` is
therefore at most `2 * shock / theta^2`, telescoping over disjoint epochs.
Every scalar response leverage is also at most `sqrt((1-alpha)/2)`, so
energy-certified repairs yield normalized queried intervals without
coordinate-specific leverage estimation. The open primitive is now precisely
an output-sensitive heavy-change reporter for these monotone, energy-packed
crossings.

The group-trace oracle has also been reduced to a concrete randomized object.
A logarithmic batch of source-normalized Gaussian response sketches estimates
all fixed hierarchy-node leverage masses simultaneously; branch and bound may
then use those estimates adaptively. The static lemma alone suggests retaining
signed sketches, but the adaptive theorem below replaces that unsafe reuse by
fresh per-batch randomness and nonnegative mass accumulation.

Across an adaptive support trace, fresh sketches are drawn only after the
current batch is fixed and their nonnegative squared masses are accumulated.
Conditional concentration and a summable failure budget make every prefix
valid. Energy-normalized frontier bases are mutually orthogonal, and a newly
exposed boundary vertex has zero response to every earlier basis, so neither
old probes nor old faces are replayed. The remaining primitive is aggregate
implicit or batched application of the proved coded harmonic bank, a target-side
squared-response range-add, or a dynamic additive aggregate
Schur-diagonal-loss oracle. Spectral
Chebyshev whitening has already removed exact source solves and the random
source-conditioning assumption. The sketch route is a Monte Carlo
reduction; deterministic or Las Vegas certification of discarded groups
remains an additional obligation.

The exact diagnostic backend is
`src/hybrid_solver_codex/response_hybrid.py`, with the reproducible comparison
driver `experiments/explore_response_hybrid.py`. It separates adjacency scans,
global boundary reads, dense response arithmetic, Schur construction,
frontier iterations, materialization, and output writes. It is a correctness
and switching oracle, not an output-sensitive implementation.

Build from this directory with:

```bash
make
```

Reproduce the Round-012 aggregate-flush, one-edge scaling, and finite path
checks from the repository root with the recorded seed:

```bash
uv run python manuscript/notes/response_preconditioned_hybrid/check_round012.py \
  --seed 20260821 --trials 100
```

Reproduce the Round-013 frozen notched-sun response and delta-trace checks:

```bash
uv run python manuscript/notes/response_preconditioned_hybrid/check_round013.py \
  --seed 20260821 --trials 100 --max-n 24
```

Reproduce the Round-014 Neumann-tail certificate and template reporter checks:

```bash
uv run python manuscript/notes/response_preconditioned_hybrid/check_round014.py \
  --seed 20260821 --trials 100 --max-n 24
```

Reproduce the Round-015 verified-permutation reporter checks:

```bash
uv run python manuscript/notes/response_preconditioned_hybrid/check_round015.py \
  --seed 20260821 --trials 100 --max-n 24
```

Reproduce the Round-016 bounded-multiplicity reporter checks:

```bash
uv run python manuscript/notes/response_preconditioned_hybrid/check_round016.py \
  --seed 20260821 --trials 100 --max-n 24 --max-multiplicity 6
```

Reproduce the Round-017 positive-amplitude capacity and first-crossing checks:

```bash
uv run python manuscript/notes/response_preconditioned_hybrid/check_round017.py \
  --seed 20260821 --trials 100 --max-n 24 --max-multiplicity 6
```

Reproduce the Round-018 independent-column schedule, asynchronous
interleaving, and atomic-pairing checks:

```bash
uv run python manuscript/notes/response_preconditioned_hybrid/check_round018.py \
  --seed 20260821 --trials 100 --max-n 24 --max-multiplicity 6 \
  --max-columns 4
```

Reproduce the Round-019 simultaneous-batch, atomic-validation, endpoint-
crossing, and batch-ledger checks:

```bash
uv run python manuscript/notes/response_preconditioned_hybrid/check_round019.py \
  --seed 20260821 --trials 100 --max-n 24 --max-multiplicity 6 \
  --max-columns 4 --max-batch-size 16
```

Reproduce the Round-020 exact slack-reweighting collision, decoder flip,
nonnegative variant, and one/two-label minimality checks:

```bash
uv run python manuscript/notes/response_preconditioned_hybrid/check_round020.py \
  --seed 20260821 --trials 100
```

The Round-012--019 scripts are numerical proof audits. The Round-020 script
uses exact rational arithmetic. None is a finite-precision theorem or a
replacement for the LaTeX proofs.
