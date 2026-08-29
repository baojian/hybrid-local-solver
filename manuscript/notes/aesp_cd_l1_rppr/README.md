# AESP-CD RPPR note

This standalone note develops a composite AESP outer loop with local proximal
coordinate descent for the shared regularized PageRank model. The proof source
is `main.tex` and its included sections; [`STATUS.md`](STATUS.md) is the
current claim ledger and handoff.

The oracle-free end-to-end contract is the canonical point-source problem
`s=e_v`.  The shared definitions remain general.  Linearity extends a proved
point-source PPR solver to a sparse distribution with work
`nnz(s)+O_tilde((sum_v sqrt(s_v))^2/(sqrt(alpha)*eps_ppr))`; it does not give
the formerly requested additive `nnz(s)` bound.  RPPR obstacle solutions do
not superpose.  Point-source lower publications are, however, automatically
rooted and connected, so no multi-source component-merge reporter is needed.
The contract is not recursively closed: on a three-vertex path, the exact
root-only point-source solve already leaves two positive residual sources.
Thus coarse-to-fine bootstrapping needs a joint nonnegative-residual reporter
or pays the linear-superposition allocation factor.

There is now a sharp external regime split.  The August 2026 active-set
algorithm of [Wei and Yang](https://arxiv.org/abs/2608.16339) computes a
point-source ACL `eps_ppr` approximation in `O_tilde(1/eps_ppr^2)` work.
It therefore already meets this note's target whenever
`eps_ppr >= sqrt(alpha)`.  The unresolved point-source range is only
`eps_ppr < sqrt(alpha)`, or `rho < sqrt(alpha)/2` under the standard
`rho=eps_kkt=eps_ppr/2` reduction.  Their method supplies safe finite
boundary certificates by repeatedly solving and scanning the current active
SDD system; the radius-one finite-gap fan in this note proves that this
particular repeated-full-solve implementation can still require
`Omega(1/eps_ppr^2)` work.  The remaining opportunity is dynamic reuse of
those one-sided residual certificates in the small-accuracy regime.

Classical APPR already separates envelope size from discovery work more
sharply than the ordinary-PPR superlevel screen below.  Its terminal support
contains `S*(rho)` and is itself contained in
`S*((1-alpha)rho/2)`, so for `alpha<1/2` it is a valid envelope of volume
below `4/rho`; for a point source it also has
`O_tilde(1/sqrt(alpha))` radius.  Yet APPR has tight worst-case work
`Theta(1/(alpha*rho))`.  Hence an output-sized envelope exists and can be
found locally; the unresolved issue is exactly accelerated construction or
dynamic reuse of that envelope, not an output-volume theorem.
The tight APPR star already has envelope volume `Theta(1/rho)` and radius at
most one while spending `Omega(vol(E)/alpha)` work, so this distinction is
not caused by distant output or a loose volume estimate.
Indeed, if the APPR support is supplied as an oracle, accelerated proximal
gradient on that fixed envelope gives semantic PPR for a general sparse
source in
`nnz(s)+O_tilde(1/(sqrt(alpha)*eps_ppr))` work without a strict support
margin.  Even the envelope radius extends to distance from a general source
set.  The point-source hypothesis instead turns that multi-root geometry
into one connected rooted discovery trace.  The gap between this oracle
theorem and the desired algorithm is therefore only the accelerated
envelope-construction interface.
For multiple sources, the same geometry is multi-rooted.  If the scaled
point-source RPPR supports have disjoint closed neighborhoods, their exact
solutions decompose at thresholds `rho/s_v`, their volumes sum to at most
`1/rho`, and the additive sparse-source target is recovered.  Shared
inactive rows are precisely what break this decomposition and force component
mergers.
The finite route-output locator reduction itself also extends to a sparse
source with only the additive source-read cost: source rows begin as explicit
candidate records, joint merge rows use thresholds
`alpha*(rho*d_v-s_v)`, and the same response-radius/event charge applies.
Across the whole trace, all source and graph-frontier candidate records total
at most `nnz(s)+2*vol(S*)`; candidate enumeration itself is not the gap.
Ordinary PPR also screens the support for every source distribution, but the
sharp guaranteed volume remains only `Theta(1/(alpha*rho))`, so this linear
screen does not supply the accelerated envelope.
Its exact pivot increments remain energy-orthogonal for every source
distribution, with total energy at most `alpha/2` and total degree-weighted
variation at most one.  On the final support they give an exact inverse
factorization, reducing the missing primitive to an online thresholded
inverse-Cholesky-column reporter for an initially unknown principal matrix.
Thus solving the remaining locator interface would recover the original
additive sparse-source target, not just its point-source restriction.
The fixed-envelope terminal composition does not identify the final positive
face and therefore also avoids the proper-face constant-vector/Perron
identity needed by the separate momentum-window route.

Three superficially stronger point-source results do not close that hard
range after their hidden scope is restored.  The ICDT 2024
degree-normalized SSPPR method treats teleportation as a constant and uses
global preprocessing; its variable-`alpha` work is still
`O_tilde(1/(alpha eps_ppr))`.  ChebyPush has Chebyshev degree
`K=O_tilde(1/sqrt(alpha))`, but its safe local theorem costs
`O(K^2/eps_ppr)` under a stability assumption; that assumption is not
graph-universal, since on a cubic high-girth ball
`||T_k(P)||_1 >= (4/3)^(k-1)`.  A 2026 single-source estimation lower bound
does certify the unavoidable `Omega(1/eps_ppr)` output scale, but assumes
constant teleportation and therefore does not rule out the desired
variable-`alpha` acceleration.  The 2026 FISTA locality
bound has the desired accelerated core term only under confinement and adds
`sqrt(vol(B))/(rho alpha^(3/2))` boundary work.  Thus none supplies the
missing graph-universal one-sided reporter.

Finite accuracy does remove one previously apparent obstruction.  With
`rho=eps_kkt`, round each monotone active coordinate down on a constant-ratio
geometric grid whose floor is `Theta(alpha eps_kkt)`.  If a rounded boundary
sum exceeds its load baseline, the true key is positive and the row is a
safe admission; otherwise the rounding tail is already at most the allowed
`alpha eps_kkt d_v` KKT error.  Hence no unknown strict key margin is needed,
and every coordinate has only logarithmically many relevant levels.  The
unclosed interface is now specifically an online source of those level
crossings from compressed dynamic Schur state, not exact breakpoint order.
This interface has an exact random-walk form.  Admitting a row \(w\) raises
the old restricted solution by \(\Delta_w h^{S,w}\), where
\(h^{S,w}_i\) is the killed PageRank walk's probability of reaching \(w\)
before another exterior row or killing.  Thus the reporter need only emit
the coordinates whose killed-harmonic increment crosses their next finite
level.  By reversibility, the degree-weighted hitting column is also the
expected occupation distribution of a killed excursion from the pivot;
this identifies the missing query as a dynamic degree-normalized
significant-entry problem.  The persistent original-frontier universe itself has at most
`2*vol(S*)` rows and all of its active incidences are exposed in
`vol(S*)` work.  Candidate enumeration is therefore closed; compressed
killed-harmonic level notification is the remaining general-graph primitive.
The nested exact pivot increments also form an energy-orthogonal response
basis, with total energy at most `alpha/d_source` and a coordinatewise
Bessel/leverage ledger.  This removes arbitrary directional repetition from
the missing interface, but an algorithm must still construct or sketch each
dense harmonic response without paying for the whole current face.
Chebyshev locality gives each such response a deterministic tail
`sqrt(d_i/d_w) h_i <= (2/alpha) lambda_alpha^(dist(i,w)-1)`.  Therefore a
finite-level crossing can occur only within
`O_tilde(1/sqrt(alpha))` distance of its pivot, despite the killed walk's
`Theta(1/alpha)` mean horizon.  This identifies the right information radius,
but not yet the work: those neighborhoods can have huge volume and can
overlap.
Approximate response values are not an additional barrier: a computable
degree-weighted response residual gives simultaneous rigorous intervals for
every response coordinate, and a summable residual schedule is absorbed by
the finite KKT band at only logarithmic accuracy cost.  A certified
dual-residual energy bound improves the explicit coordinate loss from
`1/alpha` to `1/sqrt(alpha)`.  This dual energy is exactly twice the response
quadratic's objective gap, so a certified lower objective bound makes it
observable; the plain residual norm is retained as the simpler solve-free
sufficient test.  What remains is
output-sensitive coordinate location, not exact response arithmetic.

Consequently the remaining general-graph theorem now has a minimal explicit
interface.  If a dynamic locator charges only once per crossed finite level,
plus the graph distance from its pivot to that crossing (including all state
maintenance and empty-output queries), then the event count and hitting-radius
theorems immediately give `O_tilde(vol(S*)/sqrt(alpha))` discovery work.  This
is stronger than a named-coordinate dynamic inverse: existing dynamic spectral
solvers do not by themselves enumerate all one-sided level events.  Thus the
single-source simplification has produced a genuine reduction, but not yet an
implementation of the last reporter.

A second exact comparison rules out a tempting shortcut.  If `y0` is
ordinary point-source PPR, then every RPPR support coordinate satisfies
`y0_i > alpha*rho/p`, so its `alpha*rho` superlevel is a valid containing
envelope of volume below `p/(alpha*rho)`.  A root--candidate--large-clique
family makes the ratio `y0_i/rho` tend to `alpha/p`; hence no universal
`rho*sqrt(alpha)` screening threshold exists.  Ordinary-PPR thresholding
alone cannot discover the desired accelerated-size envelope.

The note proves the local KKT-mass and relative-oracle interfaces, safe lower
centers and retraction, fixed-envelope locality, finite residual identities,
several exact trajectory calibrations, and an unconditional accelerated result
on the a-posteriori high-Dirichlet class. It also records sharp failures of
raw correction counting, Euclidean-only collateral packing, black-box
shadowing, and the simplest unsplit lagged energy bank.
The finite-inner comparison is now sharp at the root-potential level:
`sqrt(Phi_(t+1)) <= sqrt((1-q) gamma_t Phi_t) + sqrt(kappa_A) xi_t`.
This removes the artificial `xi_t <= 1` restriction and improves the
conditional absolute polish from a `theta` scale to a `sqrt(theta)` scale;
it does not prove the missing net packing inequality.
On the exact settled optimal face, a new cross-normalized error/velocity bank
contracts by `1-q` on every correction-free stage and by a constant after a
`Theta(1/q)` post-full window. It passes the previous K2 low-mode STOP; its
unpaid term is now the explicit correction forcing in a `Q_A^(-1)` norm. A
reachable complete-graph family proves that no graph-uniform constant can pay
that forcing from net high-band decrease alone: the required ratio is
`>(N-1)/23`. The surviving exact fixed-face interface is instead a
contract-or-spend window: after `Theta(1/q)` stages the bank contracts by a
constant unless it spends a telescoping low Euclidean endpoint drop.
A fully rational-interval `P24` trajectory additionally proves that paying
the low forcing by net high-band drop plus `6/5` times the starting low bank
still fails; its certified required coefficient is greater than
`1.206959416`. This narrows the viable interface to the unsplit endpoint
spend or an adaptive event allowance.
An alternative Moreau-Hessian bank has a correction-event forcing metric with
condition number below `4(1+q^2)`.  For an explicit nested-face epoch protocol
that expands only at boundaries and restarts momentum at the unchanged primal
point, it gives a geometric root-potential ledger: face-optimum gains and
correction masses are injected once and earlier events are automatically
discounted.  This is not yet an event-packing theorem for the automatic
per-stage admission trajectory.
Keeping the correction cross term gives a sharper signed increment `Xi_t`.
Only `[Xi_t]_+` enters the refined epoch ledger, and its fixed-face sum has a
telescoping Stieltjes payment without the former geometric `1/q` loss. A
reachable `P3` event proves that `Xi_t` can nevertheless be positive and can
increase the bank, while the reachable `K8` family makes the telescoping
payment asymptotically tight.  An exact settled `S5` trajectory has adjacent
positive partial/full events and grows the bank across the pair, so even a
mandatory one-step quiet gap is false.  On the positive side, every graph
family with a proved clipped-master inequality has a mean-free Moreau bank
that contracts by a factor at most `3/8` in `ceil(log(2)/q)` exact fixed-face stages,
independently of event density.  The remaining pulse obstruction is therefore
concentrated in the constant low mode.  This high-bank estimate now has a
finite-inner root perturbation with a discounted residual budget.  For the
low mode there is an exact dichotomy: mean overshoot contracts its Moreau bank
by `1-q` in one step, while every non-overshoot correction is forced by the
infinity norm of the mean-free trial residual.  Combining the master high
root with the exact forced mean recurrence gives a two-scale epoch potential:
a quiet `ceil(2/q)` same-point-restart epoch contracts it below `0.407`, and
an epoch whose observable weighted mean deficit is at most one quarter still
contracts by `3/4`.  A sharper arbitrary-history low-root gate halves the
two-scale potential on every accepted `ceil(2/q)` window, and it retains an
explicit finite-inner residual allowance.  Independently, an observable
pure-prox alignment warmup reduces the high/mean residual ratio by
`(1+q)^(-J)`; once its computable threshold is crossed, the entire exact
global-momentum tail is permanently correction-free.  This gives a genuine
fixed-full-face accelerated route with `O(1/q)` warmup up to logarithms,
without lower eigendata.  A reachable `K_N` family proves that high-to-low
transfer cannot be paid by a graph-uniform high-bank coefficient: even after
a `1/q` rescaling the required coefficient is greater than `(N-1)/15`.
Thus a local, infinity-norm, or volume-sensitive payment for the weighted
mean deficit is still needed.
On a fixed certified face, the inner-work obstruction is now removed:
Chebyshev semi-iteration may use signed scratch vectors, after which a
Stieltjes retraction and coordinatewise maximum with the old safe checkpoint
publish a monotone lower certificate. A small shift therefore costs
`O_tilde(vol(A)/sqrt(lambda_lower))`, and a certified final RPPR face can be
solved directly in `O_tilde(1/(rho*sqrt(alpha)))` work. Requiring every
scratch residual to remain nonnegative provably loses this acceleration, and
fixed-rank low-mode deflation is blocked by arbitrarily high multiplicity
near-ground clusters. The remaining end-to-end issue is face discovery,
certification, and replay rather than the terminal linear solve.
That boundary is now sharper. Full-graph Chebyshev scratch can carry constant
`l2` mass on an exponentially large regular-tree frontier at degree
`Theta(1/sqrt(alpha))`, so unrestricted signed scratch is not automatically
local even when the final obstacle support is one vertex. Conversely, if
every restricted face exposes a margin-certified boundary batch of volume at
least `gamma*vol(A)`, safe restricted solves and scans geometrically sum to
`O_tilde(vol(S*)/(gamma*sqrt(alpha)))`. Endpoint paths give the matching
structural STOP: a boundary-only protocol may expose one vertex per batch and
pay quadratic cumulative face volume. Across an explicit same-point face
replay, the sharp graph-uniform Moreau root-shock coefficient is `2` (energy
coefficient `4`), so the existing root convolution has optimal scale.
The singleton path STOP is not informational.  An append-only scalar
`LDL^T` message evaluates each new boundary key in constant time and performs
only one terminal back substitution, giving output-linear discovery work.
The block Schur identity shows what must replace this message on a general
graph: an implicit dynamic response applying the old inverse to every new
coupling block and refreshing affected boundary queries.  Fixed-rank Krylov
recycling does not suffice for arbitrary new coupling directions.
On forests this interface can be realized by top-tree Schur summaries:
each link, active/pinned toggle, or named KKT query changes only logarithmically
many two-port quadratic messages.  A supplied width-`w` junction tree gives
the analogous `O((w+1)^3 log B)` update.  This is not yet an end-to-end
frontier oracle: the number `Q` of named pinned-coordinate queries remains an
explicit charge and can be quadratic under repeated full-frontier rescans.
For a stable fixed separator of dimension one or two, a kinetic threshold
heap or planar extreme-point reporter closes this query term in near-linear
work; the general fixed-dimensional statement is an explicit dynamic
extreme-point interface. Balanced forest messages also have a certified
finite-precision implementation under a nonzero KKT gap. Exact rational
messages do not have polylogarithmic bit size in general: a constant-condition
tridiagonal family already produces endpoint fractions with linearly many
bits.
For one positive root load on a promised tree, the query interface closes
completely: scalar child responses propagate the next exact activation
threshold to the root, so every emitted singleton has a currently positive
boundary key and the first failed root comparison is the global obstacle KKT
certificate.  The same exact-real argument extends to single-source
unicyclic graphs by paying for explicit scans of the unique cycle, whose
length is bounded by the support radius.  The total literal-admission work is
`O_tilde((1+vol(S*))/sqrt(alpha))`, hence
`O_tilde(1/(rho*sqrt(alpha)))` for RPPR.  Independent rational audits cover
negative internal intercepts, competing branches, threshold ties, and exact
zero.  Persistent transfer products and static dormant-run hulls further
close cactus traces having only polylogarithmically many productive descendant
sites per cycle, even when arbitrarily many immutable live thresholds remain.
Epoch rebuilding removes that hypothesis with the unconditional
instance-sensitive block charge
`O_tilde(L_B + J_B*min{p_B+1,sqrt(L_B)})`, strictly improving a full block scan but not
yet reaching the radius--volume target on every cactus; it does reach that
target whenever every root route has
`sum_B min{p_B+1,sqrt(L_B)}=O_tilde(R*)`.  The
bounded-productive result includes chains of arbitrarily long cycles.
More strongly, a two-hysteretic online heavy--light decomposition removes the
final-support oracle for every single-root cactus: every current light edge
shrinks subtree size by at least a `2/3` factor, each node changes heavy child
only logarithmically often, and conservative whole-path rebuilds have total
`O_tilde(vol(S*)*R*)` work.  Thus the smallest still-open structural reporter
is now a genuinely variable-port series--parallel block, rather than an
unbounded cactus chain.  A three-vertex two-source
example shows why running
independent single-root copies does not handle component mergers.
A small-`rho` connected-prefix realization lemma makes the square-root
separation reachable by a legal RPPR singleton trace; it stops the literal
flat rebuild-and-scan interface, not multilevel reporting or another legal
batch order.  A matching static-cluster interface proposition makes this
boundary explicit: without bulk affine pullback or hull meld, an adversarial
`Theta(sqrt(L))`-event phase costs `Omega(L)` even though this is not an
algorithmic lower bound.
Even the exact Schur objective decrease cannot pay a fixed amount per
admission: an exact two-vertex RPPR family has a strict admission whose gain
tends quadratically to zero.  Thus gain-only charging needs an explicit
relative margin or a different potential.  With a declared batch-density
gate, the repair is exact: `||g_W||^2 >= 2 eta L work(W)` makes the Schur gain
at least `eta work(W)`, so accepted batch costs telescope.
The earlier offline construction supplied the final closed block tree, its
weighted heavy--light decomposition, and balanced series--parallel parses.
The hysteretic theorem makes this online by allowing changed paths to be
discarded and rebuilt, charging each structural atom to a comparable route
node and at most logarithmically many heavy switches there.  Persistent
cut/concatenate and bulk pullback/meld would improve this radius-paid rebuild
to polylogarithmic maintenance, but is no longer needed for the cactus product
bound.  It remains the missing interface for general variable-port
series--parallel blocks.
A separate quantitative result reduces uniformly separated RPPR boundary
keys to monotone coordinate-level events.  This is soft-linear only when the
level-event source is itself charged; ordinary point-query Schur messages do
not reveal those crossings automatically.  An exact RPPR P4 witness rules
out fixed factor-two bins.
For the remaining series--parallel interface, fixed-mark Schur updates and
named cycle responses are logarithmic.  A conditional reduction isolates the
missing object as a persistent affine hull supporting bulk pullback and meld.
The pullback alone is structured: nonnegative two-port Schur maps act on
normalized row slopes by an order-preserving/reversing Möbius map, so one
child hull can keep a lazy projective view.  These views compose as fixed
$3\times3$ homogeneous matrices, so an entire series chain remains
constant-size.  The unresolved operation is the
meld and strict argmax across differently transformed, arbitrarily
interleaving child hulls.
If every sibling pair instead has disjoint pulled-back slope intervals, one
bridge tangent gives a logarithmic persistent meld; this is a clean
structural GO, but not a general reporter.
The condition is observable from the two lazy endpoint images at every
changed meld, so the fast branch can be guarded online and abandoned safely
when the intervals overlap.
Separately, exact all-positive batching cannot be charged just to support
radius.  An explicit point-source fan family has every graph vertex at radius
one but needs at least $m/2-1$ nonempty simultaneous batches on $m$ path
vertices; an eight-vertex exact instance additionally realizes five strict
singleton batches.  Thus the point-source restriction removes component
mergers, not serial boundary activation around one root.
This obstruction is exact-support-specific: on the fan family, the
root-only restricted point already has normalized KKT residual below
$\rho$.  It therefore stops immediately under the matched finite choice
$\varepsilon_{\rm kkt}\geq\rho$ used in the PPR reduction.  Exact batch
counts must not be reused as finite-accuracy lower bounds.
The escape is not uniform over fan parameters.  A second exact family with
$\alpha=1/4$ and
$\rho=\varepsilon_{\rm kkt}=1/(10m)$ passes the finite-significance test at
exactly the next two path vertices for $m/2$ rounds.  Consequently, the
strategy that independently solves and scans the whole current face per
round really costs $\Omega(m^2)=\Omega(1/\varepsilon^2)$ even at the matched
finite target.  Dynamic reuse is essential; finite accuracy alone does not
close the product-scale theorem.
Nor can the nonlinear obstacle be replaced by one ordinary-PPR sweep: an
exact point-source path has an active RPPR coordinate where the corresponding
unconstrained shifted PPR coordinate is strictly negative.
Parametric point-source homotopy gives a sharper algebraic interface: after
one admission, every surviving critical threshold is a nonnegative weighted
average of its old value and the admitted maximum.  The thresholds therefore
move monotonically, but a six-vertex exact trace reverses two candidates'
priority order.  A plain lazy heap is insufficient; the remaining reporter
must support nonuniform rank-one mixtures.
The same homotopy slope canonically normalizes every connected proper face.
If `h_A=H_A^(-1) alpha d_A` and `W_A=diag(d_i/h_i)`, then
`0<h_A<=1`, `H_A h_A=alpha W_A h_A`, and
`alpha W_A<=H_A<=W_A`.  Thus the exact positive generalized ground state is
known without an eigensolve; the elimination record already recovers it.
This supplies Perron data for a separately proved `W_A`-geometric
correction-free tail, but it does not automatically transplant the original
constant-direction clipping master to the new mass matrix.
There is nevertheless an exact controller conjugacy.  With
`R_A=diag(h_A)`, the operator
`bar Q_A=R_A^(-1) W_A^(-1) H_A R_A` is self-adjoint in
`bar D_A=diag(d_i h_i)`, has spectrum in `[alpha,1]`, and satisfies
`bar Q_A 1=alpha 1`.  A `W_A`-shift and the safe cap
`[u-Delta h_A]_+` become the ordinary identity shift and common constant cap
after the change of variables.  Thus the fixed-face full-face algebra
transfers exactly to a modified proper-face controller; high-gap and master
sign certificates remain separate hypotheses.
The high gap now has an explicit graph certificate: with
`q=sqrt(alpha/(1-alpha))`, weighted ground conductance
`Phi_h>=sqrt(2alpha/q)=Theta(alpha^(1/4))` implies every transformed high
resolvent mode is at most `1-q`.  This is only a sufficient Cheeger
condition; it does not establish the independent clipped-master sign.
It nevertheless closes the alternative fixed-face alignment route: after an
observable pure-prox warmup and same-point restart, all later `h_A`-caps are
zero and the exact proper-face tail costs only
`O_tilde(alpha^(-1/2))` resolvent applications.  Thus this positive theorem
does not pass through the unresolved mixed-clipping master inequality.
The certificate is nonvacuous: for `q<=1/256`, a proper `K_m` face with one
exterior leaf and `m>=ceil(1/alpha)` has `Phi_h>=27/256`.
The ground coordinate `h_i` is exactly the probability of teleporting before
leaving the face.  If every vertex leaks at most an `eta` fraction of its
edges, then `min h>=alpha/(alpha+((1-alpha)/2)eta)`, giving a direct
ordinary-conductance or Poincare certificate without first diagonalizing the
face.  When `eta=O(alpha)`, the sufficient scales are respectively
`Theta(alpha^(1/4))` and `Theta(sqrt(alpha))`.  This spectral check is also
finite: a positive approximate ground vector with local one-sided relative
residual `eps_h` multiplicatively sandwiches the exact ground vector and
loses only the factor `1-eps_h` in the computed conductance/Poincare lower
bound.  Exact ground coordinates are therefore not required merely to
certify the tail hypothesis.
Keeping the complete exterior Schur complement turns that identity into an
exact ratio-pivot homotopy algorithm: every support coordinate enters once,
and the target support is certified when the largest remaining ratio falls
below $\rho$.  Its discovery work is
$\widetilde O(\vol(S^\star)+\sum_w(1+\delta_w)^2)$, where $\delta_w$ is the
actual Schur-fill degree at pivot $w$.  Bounded homotopy width therefore gives
a genuine product-scale point-source solver after the final-face Chebyshev
step.  Explicit fill can still be quadratic (already at a high-degree root),
so this is a new structural GO rather than the universal theorem.
Linear pivot-path length for K-matrix LCPs is classical
([Foniok--Fukuda--Gärtner--Lüthi](https://arxiv.org/abs/0807.1249)); the
new role here is the point-source $\rho$-ratio parameterization, sparse-fill
ledger, and finite-error contract, not the number of exact pivots alone.
At a single requested $\rho$, this simplifies further: maintain only the
scalar restricted residual $g_v=A_v-\rho B_v$, pivot any certified-positive
row, and stop when all certified upper residuals meet the normalized KKT
tolerance.  Point-source locality makes this row discovery complete because
every nonroot row not yet adjacent to the support still has strictly negative
load.  Thus the weakest missing universal interface is now a dynamic
one-sided residual reporter; separate ratio vectors are needed only for the
full $\rho$-homotopy.
In degree-unscaled coordinates the same point-source obstacle is exactly a
killed divisible-sandpile odometer: a legal push sends the fraction
`(1-alpha)/(1+alpha)` of its removed residual to its neighbors and dissipates
the rest.  The obstacle vector is the coordinatewise least stabilizer, so
every fair full-toppling order converges to it.  This explains the rooted
Abelian growth structure, but also calibrates its limitation: residual-cone
local topplings still have only the classical
`O(1/(alpha*eps_kkt))` work certificate.  The Schur residual pivot is an
exact block toppling; acceleration must come from representing those block
responses economically.
The total positive exterior residual mass is also nonincreasing and starts
below $\alpha$.  In fact each pivot removes at least
$\alpha/p$ times its admitted residual from this mass, so the sum of all
block-pivot residual injections over any legal order is at most
$(1-\alpha)/2$.  Hence at any one time at most
$1/\varepsilon_{\rm kkt}$ rows can exceed the finite KKT threshold.  This
does not yet bound lifetime rekeys, but it is a genuine finite-accuracy
sparsity invariant absent from exact support recovery.
Every Schur multiplier is also exactly the first-exit distribution of the
PageRank walk killed at rate (2\alpha/(1+\alpha)) and traced through the
current active face.  This samples one dense fill column implicitly, but a
literal walk still has (O(1/\alpha)) expected length.  The missing
acceleration is therefore a one-sided threshold reporter for these harmonic
transports, not merely an ordinary random-walk sampler.
A separate forward-push/Monte-Carlo audit reaches the same boundary.  After
pushing to normalized residual threshold `theta`, reversibility bounds every
degree-normalized residual correction by `theta`, so an `O(1)` endpoint
oracle would attain the target after balancing
`theta=eps_ppr/sqrt(alpha)`.  Literal endpoints cost
`Theta(1/alpha)` walk steps each; charging them moves the optimum back to
`O_tilde(1/(alpha*eps_ppr))`.  This rules out only the literal push--walk
implementation, not randomized shortcut preprocessing or a compressed
endpoint oracle.
The same homotopy has a margin-free approximate stopping rule:
$\alpha d_v\leq B_v\leq(1+\alpha)d_v/2$, so an additive upper error
$\eta$ on the largest remaining critical ratio costs at most
$(1+\alpha)\eta/2$ in the normalized KKT diagnostic.  Exact support and
exact breakpoint separation are therefore unnecessary at the requested
finite accuracy.
A certified interval version makes the remaining approximation contract
explicit: rowwise pair radii of order $\alpha\eta d_v$ suffice for additive
ratio accuracy $\eta$, and the reporter may safely pivot, stop, or refine a
gray row.  A two-by-two exact witness shows why a generic two-sided spectral
Schur approximation is not already such a certificate: an
$\varepsilon$-spectral perturbation can replace a positive updated breakpoint
by zero.  Approximate elimination therefore still needs a rowwise one-sided
error conversion; this is the present general-graph bridge.
This distinction matters when importing near-linear
[approximate Gaussian elimination](https://arxiv.org/abs/1605.02353),
[spectral vertex sparsifiers](https://arxiv.org/abs/1506.08204), or their
[dynamic variants](https://arxiv.org/abs/1906.10530): those papers certify
spectral/energy behavior, while the ratio-pivot stop needs simultaneous
one-sided row intervals.  Whether those tools can be augmented to supply the
intervals at local cost is now the precise open interface.
An exact RPPR theta core proves that one direction-free scalar threshold is
insufficient, while a weighted fan has a quadratic-size explicit obstacle
response table; neither statement is an algorithmic lower bound.
The closest dynamic-data-structure results do not currently supply that
combined interface.  [Top trees](https://arxiv.org/abs/cs/0310065) give
logarithmic structural updates once a composable cluster summary is provided,
and [dynamic treewidth](https://arxiv.org/abs/2504.02790) maintains a bounded-
width decomposition and declared dynamic-programming state.  The
[dynamic planar convex hull](https://arxiv.org/abs/1902.11169) supports
insert/delete and extreme-point queries in one global coordinate frame, while
[dynamic hulls for simple paths](https://doi.org/10.4230/LIPIcs.SoCG.2024.24)
add restricted deque/concatenate structure.  Their stated operation sets do
not yield arbitrary hierarchical affine pullback together with persistent
hull meld/split and strict labeled argmax.  Thus these papers validate the
neighboring ingredients, but using them here still requires a new reduction
or a stronger reporter theorem.
A supplied balanced series--parallel parse nevertheless has an unconditional
exact fallback that avoids meld entirely.  Snapshot static hulls at all
canonical clusters, mark the root paths of changed home leaves dirty, query
the maximal clean sibling cover, and rebuild after `sqrt(N)` distinct
touches.  This costs `O_tilde(N+J sqrt(N))`; it meets the product budget when
the charged block radius is at least `sqrt(N)`.  The remaining variable-port
gap is precisely to remove that square-root loss (or charge it) while also
paying online parse discovery and inactive halo.
If only `p` distinct home leaves ever change, the same online scheme sharpens
to `O_tilde(N+J min(p+1,sqrt(N)))`, so repeated mutations through a small
productive interface are also product-scale when `p+1<=R*`.
The overlap is genuinely unbounded for an explicitly merged chain: a
weighted SP fan has even/odd child envelopes whose facets alternate, and one
bulk child translation removes or reinserts linearly many parent facets.
Thus constant-bridge repair cannot improve the epoch bound; a successful
improvement must keep the transform/meld lazy or use a different reporter.
[Kinetic/dynamic hulls](https://doi.org/10.1016/j.comgeo.2006.01.002) also
allow points with declared bounded-complexity trajectories and individual
flight-plan changes.  A Schur update, however, changes the pulled-back
trajectory of an entire dormant cluster at once; treating it as one flight-
plan update per row reproduces the very materialization charge at issue.
Speculative coordinate-envelope doubling gives a second conditional route:
its solves geometrically sum to
`O_tilde(vol(U_final)/sqrt(lambda_floor))`, but `U_final` includes inactive
halo and need not be controlled by `vol(S*)`.  A margin-free clip-or-pay
retraction now converts feasible accelerated projected-gradient scratch into
an order-safe obstacle subsolution in the required
`O_tilde(vol(U)/sqrt(alpha))` work.  It charges each unsafe coordinate either
to its small primal value or to its residual, so strict complementarity is no
longer needed for this fixed-envelope primitive.  Strict margins remain useful
only when the exact active face itself must be identified.  High-degree
inactive decoys and dynamic boundary reporting still remain.
The RPPR support cap nevertheless gives a universal retained-volume result:
by keeping at most `1/rho` inactive halo volume in addition to the true active
support, an exact dynamic obstacle protocol never retains more than `2/rho`
volume. This is a partial affirmative answer, not an accelerated solver: all
serial updates and frontier reports remain charged to the explicit quantity
`W_DS(2/rho)`. A subcubic exact audit shows that naive factor-two speculation
can already explore `26/9` times the final support volume. Once discovery has
certified the final positive face, carrying no momentum through admissions
and restarting only once gives the q-free bridge
`C_rst <= 4(F(z)-F(x*))`.  On a general proper final face this composes
directly with the safe Chebyshev terminal solve.  The master/mean accepted
windows and alignment tail require their additional constant-mode, spectral,
and face-stability certificates; the bridge does not manufacture them.
The common-cap truncation ledger is also joint: correction and surviving
momentum `Q`-energies share one copy of the telescoping energy drop.

The primary live target is the output-sensitive online one-sided event
locator, beginning with variable two-port series--parallel blocks; a secondary
route is to pack failed proper-face windows and finite changing-face replays.
No graph-uniform exact accelerated solver or unconditional
`O_tilde(1/(rho*sqrt(alpha)))` end-to-end theorem is claimed. In particular:

- the abstract ledger witness is not an RPPR instance or an exact-proximal
  trajectory;
- the finite P4/P7 traces prove no infinite periodicity and no finite-inner
  work theorem;
- the fixed-P4 theorem refutes a horizon-uniform inflation bound while its
  primal error still converges geometrically, so it is not a net-exponent
  counterexample;
- the retraction discontinuity is a STOP for black-box shadowing, not a
  counterexample to direct finite-sequence packing or a graph-uniform solver
  theorem;
- entry-dominated stages and persistent-row energy now have explicit charges,
  but converting the event-level low-progress spend into a changing-face
  accelerated net exponent remains open.

An exact settled `P96` trajectory also shows why the new gate cannot be
replaced by a raw half-contraction assertion: its total Moreau bank retains
more than `0.54` after exactly `1/q` transitions, with the low component
retaining more than `2/3`.

Build the note from the repository root with:

```bash
make -C manuscript/notes/aesp_cd_l1_rppr
```

Run all twenty-seven exact audits with:

```bash
uv run python -m experiments.proof_audits.runner \
  --tier full --note aesp_cd_l1_rppr
```

Their durable IDs are:

- `aesp_cd_l1_rppr.safeguarded_outer_ledger` (Round 022 provenance);
- `aesp_cd_l1_rppr.fixed_operator_p4_tail` (Round 023);
- `aesp_cd_l1_rppr.retraction_and_fixed_face` (Round 024);
- `aesp_cd_l1_rppr.boundary_shielding_filter` (Round 025);
- `aesp_cd_l1_rppr.persistent_q_energy` (Round 026);
- `aesp_cd_l1_rppr.weighted_reserve_boundary` (Round 027);
- `aesp_cd_l1_rppr.windowed_cross_normalized` (Round 028);
- `aesp_cd_l1_rppr.p24_low_start_stop` (Round 029);
- `aesp_cd_l1_rppr.signed_event_stop` (Round 030);
- `aesp_cd_l1_rppr.adjacent_signed_event_stop` (Round 031).
- `aesp_cd_l1_rppr.p96_full_face_window_stop` (Round 032).
- `aesp_cd_l1_rppr.safe_chebyshev_face` (Round 034).
- `aesp_cd_l1_rppr.singleton_face_batches_stop` (Round 035).
- `aesp_cd_l1_rppr.s5_face_shock_sharp` (Round 036).
- `aesp_cd_l1_rppr.rppr_speculative_decoy` (Round 037).
- `aesp_cd_l1_rppr.dynamic_schur_forest` (Round 038).
- `aesp_cd_l1_rppr.bounded_degree_speculative_stop` (Round 039).
- `aesp_cd_l1_rppr.tree_singleton_threshold` (Round 040).
- `aesp_cd_l1_rppr.separated_level_reporter` (Round 041).
- `aesp_cd_l1_rppr.variable_two_port_stops` (Round 042).
- `aesp_cd_l1_rppr.radius_batch_stop` (Round 043).
- `aesp_cd_l1_rppr.obstacle_clip_retraction` (Round 044).
- `aesp_cd_l1_rppr.accelerated_support_spill` (Round 045).
- `aesp_cd_l1_rppr.point_source_scope` (Round 046).
- `aesp_cd_l1_rppr.fan_linear_batches` (Round 047).
- `aesp_cd_l1_rppr.point_source_homotopy` (Round 048).
- `aesp_cd_l1_rppr.point_source_ratio_pivot` (Round 049).

The full tier includes the optional P7 corroborating trace. These audits check
the scoped exact identities and source guardrails; they do not promote the
open graph-uniform theorem.
