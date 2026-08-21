# propagate_settle_framework

This standalone note extracts a common theoretical framework from the
measured `two_rung_sor`, `rlsor_terminal_exact_rung`, and
`frontier_adaptive_ladder` methods.

The central proved fact is an absorption law for exact settlement.  Once the
outside coordinates and the settled region are fixed, an exact restricted
solve erases every over-relaxation, ordering, and signed-packet decision made
inside the region.  For nested regions, smaller settlements are absorbed by
the larger one.  Thus the settled trajectory is determined only by the
sequence of discovered regions; over-relaxation can help only through region
discovery or its work cost.

The note also proves an exact defect identity for an inexact delivery phase
and a trajectory-sensitive work theorem.  The relevant structural quantity is
the settled-volume revisit factor

`R_set = sum_k cvol(U_k) / cvol(U_K)`,

where `cvol(U) = sum_{u in U} (1 + d_u)` charges one active-coordinate word
and its adjacency scan (and is within a factor two of degree volume). It is
not the raw number of batches. Exact RPPR boundary expansion therefore costs
`O((w + 1)^2 R_set / rho)` under supplied width-`w` orderings.  The desired
product scale follows from the strictly weaker target
`R_set = O_tilde(1 / sqrt(alpha))`, even when the number of small early
batches is larger.  This quantity is the theoretical analogue of the adaptive
frontier solver's measured work-per-touched-support ratio.

The note now proves that a log-free graph-uniform revisit bound is false for
the literal exact boundary gate.  A four-vertex tailed triangle has two
activation batches in the same root-distance shell.  A width-two tailed fan
extends this to any prescribed number `L` of singleton batches, all among
distance-one vertices, and forces `R_set > (L + 1) / 5`.  With a quantitative
choice of the fan size, this gives the intrinsic lower bound
`R_set = Omega_alpha(log(1 / rho))`.  Thus constant elimination width and
constant support radius do not remove the dynamic-range logarithm.

The polylogarithmic revisit target remains open in thick, large biconnected
cores and is consistent with the fan obstruction.  The alternative is to
retain incremental Schur state, as the path, tree, cycle, and bounded-block
algorithms in `delayed_reflection_ladder` already do.

The note now makes that alternative exact.  Cumulative settled volume equals
a charge-weighted activation age: each vertex is charged once for every fresh
settlement after it enters.  A lazy block-Schur update stores the correction
to old coordinates and updates remaining violation demands through one signed
Schur block-column.  On the same tailed fan that forces a logarithmic fresh
revisit, a two-coordinate separator reproduces the identical first $L$
batches and exact restricted solution in $O(m+L)$ work, versus
$\Omega(mL)$ for fresh settlement.  Thus the lower bound isolates a
state-maintenance cost rather than an information-theoretic discovery
barrier.

This fan mechanism now has several rigorous structural generalizations.

- A charged online activation-aligned presentation with live frontal size
  `zeta` and at most `nu` exact signatures reproduces every gate batch in
  `O((1 + zeta^2 + nu zeta) cvol(S) + T_sep)` work.  The note explicitly
  charges separator discovery and states the exact metadata/access model.
- A kinetic threshold theorem removes the `nu` term when distinct demands
  cross zero in a stable scalar order.  It gives an exact
  `O(cvol(S) log(2 + R))` online solver on rooted spiders even if all `R`
  frontier responses differ.
- A certified low-rank response tree replaces exact row equality by interval
  certificates and refines only clusters whose KKT sign is ambiguous.

The flat structural condition cannot be removed graph-uniformly.  A proved
constant-degree expander family has full RPPR support but forces
`zeta, nu = Omega(n)` in every activation-aligned presentation.  This is a
framework obstruction, not a lower bound against all algorithms.

Two representation-specific cyclic obstructions sharpen that conclusion.
Original-basis multifrontal or Cholesky hierarchies that explicitly store
their exact fronts require `Omega(n^2)` entries on bounded-degree expanders.
On sparse cyclic Stieltjes systems, arbitrarily light singleton cascades make
every remaining boundary demand change, so an eager exact-demand array also
requires `Omega(n^2)` updates.  Neither result rules out compressed, lazy, or
matrix-free state.  Positively, a stable exposed block--cut presentation with
block size `b` supports an exact response-generated solver whose route cost is
quadratic in `b`; polylogarithmic blocks reach the product scale when the
presentation itself can be maintained within that budget.  The companion
`delayed_reflection_ladder` note now removes this metadata assumption for
bounded blocks.  Activating zero-valued vertices preserves all consumed
response prefixes, so online block mergers rebuild only future iterator state
and retain the same product scale under ordinary adjacency access.

The universal hybrid proof is now reduced to one precise response step.
Exact Schur algebra is used until `zeta = ceil(alpha^(-1/4))`, which costs at
most `O(cvol(S) / sqrt(alpha))`.  A per-event shock-only repair bound is
proved false: a tiny singleton shock can require a linear next-batch output,
and full-sweep AG/Chebyshev/CG still need one old-face pass as the shock tends
to zero.  However, the note now proves that all numerical repairs in an epoch
can be deferred to one final accelerated solve.  With an independently
maintained exact response certificate, heavy shocks bound the number of such
repairs.  Arbitrary rooted trees meet the intended product bound through a
different exact response-generated trace, without claiming that trace equals
the literal boundary gate.  Within the exact-gate hybrid route, the remaining
universal claim is light-shock response maintenance on nonequitable cyclic
cores, with every old-face read and response query explicitly charged.

For approximate output, the note proves a strictly weaker reduction.  If
every exact boundary demand is certified to additive normalized error
`alpha * tau_gate / 4`, admitting only estimates above the corresponding
finite threshold remains support-safe and terminates with degree-normalized
solution error at most `tau_gate`.  One final accelerated solve adds
`tau_sol`, while RPPR regularization contributes `rho`.  Thus a certified
finite-band response oracle would give
`O_tilde(1 / (epsilon * sqrt(alpha)))` work by taking all three errors as
`epsilon / 3`.  Establishing that band-response oracle on general cyclic
cores is now the weakest sufficient unresolved theorem; exact zero-sign
maintenance is no longer necessary for this approximate target.

The response certificate is now weakened further.  Uniform point estimates
are unnecessary: certified lower endpoints suffice for admission, certified
upper endpoints suffice for termination, and only intervals intersecting the
transition band must be refined.  For any nested exact-face expansion, the
full exterior demand change has squared Euclidean norm at most twice the
objective shock.  Therefore boundary degree volume moving by normalized
margin `theta` is at most `2 * shock / theta^2`, with telescoping shock over
disjoint epochs.  The remaining cyclic problem is an output-sensitive
heavy-change reporter for these energy-packed crossings, not a full boundary
refresh.

The existing notched-double-sun structural epoch is now ruled out as an RPPR
trajectory witness.  At every active face `U` containing the anchor and
satisfying `W intersect U = empty`, each unadmitted frontier petal `f_i` and
matching report leaf `w_i` have identical shifted load, degree, face row, and
exact normalized demand.  The canonical all-violations gate therefore admits
them together.  A single seed can break at most one pair, so no parameters
produce linearly many distinct petal admissions while maintaining
`W intersect U = empty`; a positive report-leaf seed already violates that
condition.  For one simultaneous uniform point-estimate call at the same
face, both labels are forced above the robust band and neither is selected
below it.  This does not constrain arbitrary asynchronous interval
refinement.  The structural pruning threshold
`tau_fb = ((1 - alpha) / 2)^5` is not the KKT demand tolerance
`eta = alpha * tau`.  The audit preserves the fully charged prefix and gives
separate eleven-coordinate vectors for fresh row validation and reuse of
already charged stored records; mathematical co-admission alone forces no
particular scan, materialization, or intermediate output.  This retires the
graph only as a canonical RPPR trace witness.  It does not weaken its
representation audit or refute a reporter on an asymmetric legal cyclic
family.

A minimal asymmetric repair also fails, for a different exact reason.
For even `n >= 4`, take an anchor cycle, attach a degree-one source petal
`f_i` and a report vertex `w_i` at every anchor, and pair the reports by a
perfect matching.  The graph is simple, unweighted, has maximum degree four,
and its anchor--report cut has rank `n`; source and report rows are no longer
twins.  Nevertheless, for every `alpha in (0,1)` and `rho > 0`, any exact
canonical face `U` with `W intersect U = empty` whose next batch `B` also has
`B intersect W = empty` can add a source petal only at the single seed anchor.
Report quietness gives
`x_ui <= 4 alpha rho / vartheta`, while a positive petal demand gives
`x_ui > 2 alpha rho / vartheta`, with
`vartheta = (1-alpha)/2`; the nonseed anchor equation is incompatible with
that band and the identical bounds on its two cycle neighbors.  A
positive-load `F` seed is the sole initial exception, every nonpositive seed
load gives the zero optimum, and a positive `W` seed violates report exclusion
immediately.  Thus every report-free canonical prefix has at most one `F`
coordinate, despite the full-rank raw cut.  This is a KKT-legality
obstruction, not a reporter lower bound or a finite-precision result.  Its
trace audit retains the fully charged prefix and separates all eleven work,
memory, materialization, and output coordinates.  The next candidate must
attenuate reports through active stems or another bounded-degree threshold
gadget; direct degree lifting is now retired.

The smallest active-relay repair is now retired as a relay-first witness too.
On the even active-relay matched sun, every anchor has a degree-one source
petal `f_i` and a two-edge
report stem `u_i-r_i-w_i`, while `W` retains its perfect matching.  The graph
is simple and unweighted with degrees `4,1,2,2`, maximum degree four, and
full-rank raw anchor--relay and relay--report cuts.  Nevertheless, at any
canonical face with `W` still unadmitted, an unadmitted nonseed pair satisfies

`e_f = -alpha rho + (vartheta/2) x_u`,

`e_r = -alpha rho sqrt(2) + (vartheta/sqrt(8)) x_u`.

Thus a positive relay demand requires
`x_u > 4 alpha rho/vartheta`, which makes the petal demand strictly larger
than `alpha rho`.  Every nonseed relay is therefore preceded or co-admitted by
its petal in every canonical all-violations batch, including batches of
arbitrary size.
A report-free face containing all relays already contains all petals except
possibly the one paired with a positive relay seed, so at most one petal can
enter afterward.  Positive anchor and petal seeds have no exception; a
positive relay seed gives the sole possible exception; a positive report seed
violates report exclusion initially; and every nonpositive seed load gives the
zero optimum.  The four positive-start ranges are respectively `rho<1/4`,
`rho<1`, `rho<1/2`, and `rho<1/2` for anchor, petal, relay, and report seeds.
Hence the desired active-relay phase cannot contain
`Theta(n)` later distinct petal admissions.  The proposition does not rule out
some different trace made of paired petal--relay batches; it proves that such a
trace cannot supply the prescribed common preloaded-relay phase.  This is an
exact KKT chronology obstruction, not reporter algebra or a response-rank/work
lower bound.  Under a noncanonical policy that may choose an arbitrary subset
of positive violations, the petal is only proved simultaneously eligible and
could be deferred.

The exact thresholds above are separate from `eta = alpha tau` and from the
structural pruning threshold `tau_fb = vartheta^5`.  The trace audit retains
the fully charged eleven-coordinate prefix.  Since this graph has
`cvol(V)=13n`, fresh validation of all local threshold implications costs
`(Theta(n),1,0,0,Theta(n),0,0,0,O(1),0,0)` beyond that prefix; if all gadget
rows were already retained and charged, the incremental vector is
`(0,0,0,0,Theta(n),0,0,0,O(1),0,0)`.  Numerical face solves, response
queries, state, recovery/materialization, and required emitted labels remain
separate representation-dependent charges.  The result is exact-real-cell
only and has no word/bit, finite-precision, or numerical-stability conclusion.

The literal degree-three repair has now been tested and also stops before
reporter algebra.  Put the petals on their own cycle while retaining the
anchor cycle, edges `u_i-f_i`, stems `u_i-r_i-w_i`, and the perfect matching
on `W`.  This simple unweighted graph has degrees `(A,F,R,W)=(4,3,2,2)`,
`cvol(V)=15n`, and full-rank raw `A-F`, `A-R`, and `R-W` cut blocks.  The local
threshold reversal is genuine: when a petal and its two cycle neighbors are
inactive, a nonseed relay crosses at
`x_u > 4 alpha rho/vartheta`, while the petal waits until
`x_u > 6 alpha rho/vartheta`.

Global exact balance exhausts that window.  At any `W`-free canonical face
containing all relays whose next canonical all-violations batch is also
`W`-free, write `t=((1+alpha)/2)/vartheta`,
`p_i=vartheta*x_ui/(alpha*rho)`, and
`q_i=vartheta*x_ri/(alpha*rho*sqrt(2))`.  Report quietness gives `q_i<=2`,
and each nonseed relay equation gives `4<p_i<=4+8t`.  If a nonseed anchor's
petal were still inactive, its anchor equation would force

`p_(i-1)+p_(i+1) = 8 + 4(t-1/(8t))p_i + 2/t > 8+16t`,

while the two neighboring report-quiet relay equations give the opposite
upper bound `p_(i-1)+p_(i+1)<=8+16t`.  A relay seed obeys the same anchor cap.
Thus the common face already contains every petal except possibly the one
paired with an anchor or relay seed.  A positive petal seed leaves no
exception; a positive report seed violates the epoch; and nonpositive seed
load gives zero.  The positive-start ranges are respectively `rho<1/4`,
`rho<1/3`, `rho<1/2`, and `rho<1/2` for `A,F,R,W` seeds.  Hence no
single-seed report-free canonical chronology activates all relays before
`Theta(n)` later distinct petal admissions, even though the isolated
thresholds are reversed.  An arbitrary positive-subset policy is outside the
claim.

The full exact-cell audit is at
`rem:petal-cycle-relay-trace-ledger`.  Beyond the complete paid prefix, fresh
streamed validation costs
`(Theta(n),1,0,0,Theta(n),0,0,0,O(1),0,0)` in the shared eleven-coordinate
order; validation from already paid retained rows costs
`(0,0,0,0,Theta(n),0,0,0,O(1),0,0)`.  Numerical face work, response state,
materialization, and required emissions remain separate.  This proves no
reporter or response-rank/work lower bound and has no word/bit,
finite-precision, or stability consequence.  Since no legal long epoch
exists, the raw full-rank cuts do not establish genuinely changing response
directions along an RPPR trace.  This motivates the independent-backbone
legality test below; every candidate still needs explicit seed-orbit and
canonical all-violations audits before reporter analysis.

The literal independent-backbone test now stops too.  For even `n >= 4`, let
`B={b_i}` and `A={u_i}` be cycles and add sitewise edges `b_i-u_i`,
`b_i-r_i`, `u_i-f_i`, and `r_i-w_i`, with a perfect matching on `W`.  The
degrees are `(B,A,R,F,W)=(4,4,2,1,2)`, `cvol(V)=18n`, and all four sitewise
cut blocks have rank `n`.  Nevertheless, for every seed on `B`, every
`alpha in (0,1)`, and every `rho>0`, a canonical all-violations prefix is
petal-free as long as its faces and next batches are report-free.  With
`t=((1+alpha)/2)/vartheta`, normalized anchor value `s_i`, and normalized
relay value `q_i`, report quietness gives `q_i<=2`; at a maximum active
anchor `M`, the two exact active equations give

`t(M-q_i) = (s_(i-1)+s_(i+1))/4 - 1 <= (M-2)/2`.

Thus `M>2` is impossible, exactly ruling out a positive petal demand.  The
same bound shows that a newly violating anchor's relay is either already
active or, when both vertices are inactive, has positive demand and is
co-admitted in the same all-violations batch.  Thus the relay is active no
later than its anchor and the induction persists.  Hence the first petal
batch, if any, already contains a report.

The anchor-seed escape is now followed to completion rather than inferred
from its first batch.  In the exact counterrange
`0<rho<(1-alpha)/8`, put `lambda=1/(2rho)` and
`t=(1+alpha)/(1-alpha)`, so `lambda>2(t+1)`.  The first batch contains `f_0`
and may also contain the tied triple `{b_0,u_-1,u_1}`.  If that triple is
not initially positive, it either enters as the entire next batch when
`lambda>8t+2-3/(2t)`, or the trace stops.  Thus every continuing trace reaches
the same launch face `{u_0,f_0,b_0,u_-1,u_1}`.  If the common launch value is
`z=2(2 lambda t-16t^2-4t+3)/(t(16t^2-7))`, the exact next-batch thresholds
are `z>2` for `{f_-1,f_1}`, `z>4` for `{b_-1,b_1,r_0}`, and `z>8` for
`{u_-2,u_2}`; all satisfied groups are added simultaneously.

The later exact face audit in
`prop:double-cycle-anchor-seed-obstruction` does not assume those launch ties
persist.  It proves that `{f_-1,f_1,b_-1,b_1,r_0}` is active or co-positive
before `{u_-2,u_2}`.  Before `f_+/-2` or the first report, the only optional
local groups are `b_+/-2` and `r_+/-1`.  Solving all four faces at the petal
threshold `s_2=2` gives a strictly positive report margin `q_0-2`, with
positive `dq_0/ds_2`; a second exact table excludes deeper relays before that
report.  For `n=6`, the antipodal `b_3=b_-3` and `u_3=u_-3` see both
`+/-2` neighbors and have thresholds `p_2>4` and `s_2>4`; the same second
table and the already-proved `s_2>2 => q_0>2` implication exclude both before
a report.  For even `n>=8`, the one-neighbor frontier thresholds are instead
`p_2>8` and `s_2>8`.  Therefore `f_+/-2` can enter only in a batch that also
contains `w_0`, unless a report entered earlier.  Every strictly report-free prefix
contains at most `f_0,f_-1,f_1`.  This constant-three obstruction retires the
anchor-seed counterrange as a long cyclic witness.

The remaining relay-seed orbit is now exhaustive as well.  For every site
`j`, put

`rho_W = 1/(2(2t+1))` and `rho_B = 1/(2(4t+1))`,

so `0<rho_B<rho_W<1/2`.  If `rho>=1/2`, every shifted load is nonpositive and
zero is the unique optimum.  If `rho<1/2`, the initialized face is exactly
`{r_j}` and its normalized coordinate is
`q_j=(1/(2rho)-1)/t`.  Its only boundary demands are
`e(w_j)/(alpha rho sqrt(2))=-1+q_j/2` and
`e(b_j)/(alpha rho)=-2+q_j/2`.  Hence the complete first-batch split is

- empty at `rho_W<=rho<1/2`;
- exactly `{w_j}` at `rho_B<=rho<rho_W`; and
- exactly `{w_j,b_j}` at `0<rho<rho_B`.

At `rho=rho_W`, the zero report demand is inactive; at `rho=rho_B`, the
zero backbone demand is inactive while the report demand is positive.  The
calculation is local to `j`, so it covers every rotation and both parity
classes of the fixed report matching.  Thus every relay-seeded trace that
propagates reports in its first batch, before any petal.  Together with the
backbone- and anchor-seed propositions, this retires this double-cycle graph
family for the prescribed long report-free later-petal witness.  It does not
retire all cyclic witnesses, arbitrary positive-subset batching, or any
post-report trace.

The full exact-cell audit is at
`rem:double-cycle-feed-trace-ledger`.  Beyond the complete paid prefix, fresh
streamed validation costs
`(Theta(n),1,0,0,Theta(n),0,0,0,O(1),0,0)` in the shared eleven-coordinate
order; validation from already paid retained rows costs
`(0,0,0,0,Theta(n),0,0,0,O(1),0,0)`.  The prefix still pays every face solve,
old-row read, response query, state write, materialization, and required
emission.  For the fixed anchor seed, write `P_firstW` for the complete paid
prefix through the first report or termination.  Its additional local proof
audit costs `(O(1),1,0,0,O(1),0,0,0,O(1),0,0)` with fresh rows and
`(0,0,0,0,O(1),0,0,0,O(1),0,0)` with already paid retained rows.  An
all-rotation audit restores the corresponding `Theta(n)` scan/control terms.
For a fixed relay seed, `P_firstW^relay` likewise pays the complete prefix
through the first report, singleton termination, or absent initialization.
Only its constant-radius proof audit is incremental: fresh rows cost
`(O(1),1,0,0,O(1),0,0,0,O(1),0,0)` and already paid retained rows cost
`(0,0,0,0,O(1),0,0,0,O(1),0,0)`.  Auditing all relay rotations restores the
same linear scan/control terms.  No vector hides prefix work, and no reporter
or response work is charged to an incremental proof audit.  This is a
canonical exact-real chronology STOP, not a reporter or response-rank/work
lower bound, and it has no finite-precision or stability consequence.  It
rules out only the prescribed report-free petal/attachment trace with
changing directions and makes no claim after `W` enters.  The next candidate
must use a different coupling or bounded-degree feed before reporter analysis.

Build from this directory with:

```bash
make
```
