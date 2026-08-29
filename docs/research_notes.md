# Research notes

This file is the current project-level map of exploratory results, blockers,
and promotion gates. It is not a chronological lab notebook. Detailed proof
state belongs in each note's `STATUS.md`; accepted historical handoffs are
preserved in the immutable
[`research-round archive`](../manuscript/notes/_shared/coordination/rounds/).
The machine-readable note map is
[`registry.toml`](../manuscript/notes/registry.toml).

Last synchronized: 2026-08-29, after the point-source envelope, dynamic
event-interface, and proper-face ground/reporter audit.

## Fixed end-to-end target

The primary audit target is an exact-real algorithm on a finite simple
undirected unweighted graph with no isolated vertices and adjacency-list
access. Its canonical source is one vertex, `s=e_v`. Let

```text
x0     = Q^-1 b,
pi     = D^1/2 x0,
pi_hat = D^1/2 x_hat.
```

The algorithm must return sparse `x_hat` with

```text
max_i |pi_hat_i-pi_i| / d_i <= eps_ppr,
```

one complete terminal certificate, and one terminal return. The charged work
includes seed input, discovery, every repeated row read, inner update,
correction/rekey, response operation, certificate query, materialization,
state read/write, and output write. The desired point-source bound is

```text
O_tilde(1/(sqrt(alpha) eps_ppr)).
```

The shared problem definition continues to allow a general sparse
distribution. By linearity, a proved point-source PPR solver gives the
general-seed corollary

```text
nnz(s) + O_tilde((sum_v sqrt(s_v))^2/(sqrt(alpha) eps_ppr)).
```

This is not the formerly requested additive `nnz(s)` bound: for a uniform
`k`-point source the extra factor is `k`. RPPR obstacle solutions are
nonlinear in `s`, so their point-source runs cannot be superposed before the
final unregularized PPR approximation is formed. Claims that use connected
support, rooted exploration, or the support-radius bound are therefore
point-source claims.

The current verdict is a qualified breakthrough.  Point-source rootedness
closes the full online cactus class and removes multi-source merge
bookkeeping.  On arbitrary proper faces, a canonical positive ground
conjugacy, accelerated finite ground publication, admission replay, and
conductance-certified rank-one response split now close a second structural
branch at the target square-root scale.  Exact rank-one responses reduce its
dynamic reporter to lazy planar extreme queries.  The universal graph theorem
is still open because sparse high-gap pivots can leave genuine gray rows and
variable two-port blocks still require an amortized transformed-meld/event
locator.
In the unweighted model the remaining high-mode row radius has now been
compressed further: it is at most one common response constant times
`sqrt(s_v)`, where `s_v` is the same scalar ground coupling already carried
by the lazy planar reporter.  Thus no row-specific high-dimensional dual
state remains in this branch.  The unresolved loss is genuinely the scalar
gray band near zero, not maintenance of the full response vector.
At a fixed snapshot, even that affine-plus-square-root band reduces to
planar extreme queries: dyadic bins in `s_v` and the Young majorant for
`sqrt(s_v)` give affine lower and upper scores with less than 1.02
multiplicative inflation.  The unresolved online question is now whether
many simultaneous bin crossings can be reported or charged without a dense
refresh.
That online loss is not a bookkeeping artifact.  A second exact `K8`
high-gap witness has two retained exterior rows with identical old
`(s_v,g_v)` states, yet the same sparse pivot gives them opposite signed
high-mode corrections.  Therefore the planar two-state record cannot
deterministically advance a nonzero gray band; an implementation must retain
attachment geometry, an interval, or a stronger response oracle.
The exact-rank-one trace is now an end-to-end structural theorem, not merely a
reporter lemma.  Its Schur pivot, admitted obstacle value, and ground-update
value are computable from `(s_v,g_v)` and one global ground mass; active
coordinates use the same lazy triangular transform and are materialized once.
Candidate and incidence counts are output-linear, so discovery costs
`O_tilde(vol(S*))` and the final safe Chebyshev solve gives
`O_tilde(vol(S*)/sqrt(alpha))`.  Complete-graph point-source traces realize
this theorem exactly.
The exact hypothesis is completely characterized in the unweighted model:
the new vertex must be adjacent to every current face vertex and those old
vertices must share one ambient degree; then
`gamma=(1-alpha)/(2*alpha*d)`.  Thus an entire exact-rank-one trace is
necessarily an equal-degree clique-prefix type branch.  This explains both
why the theorem is nonvacuous and why it does not settle general sparse
graphs.

The point-source restriction is a genuine simplification, but it does not by
itself close dynamic support discovery.  A proved fan family has every graph
vertex adjacent to the source while the exact rule that solves the current
face and admits every positive exterior key still takes a linear number of
nonempty batches.  Thus radius controls route length, not the number of
response changes or restricted-face rebuilds around one root.
The analogous randomized shortcut has now been audited as well.  Forward
push to normalized residual threshold `theta`, followed by residual-endpoint
sampling, has variance only `theta`; with an `O(1)` PageRank-endpoint oracle,
balancing at `theta=eps_ppr/sqrt(alpha)` would attain exactly the target
`O_tilde(1/(sqrt(alpha)*eps_ppr))`.  A literal terminated walk, however, has
expected length `Theta(1/alpha)`.  Charging those graph moves changes the
balance back to `O_tilde(1/(alpha*eps_ppr))`.  Thus randomization identifies
the same missing accelerated endpoint/response primitive rather than
removing it; this is an accounting result for the standard push--sample
implementation, not a lower bound against shortcut data structures.  The
estimator is additionally a randomized semantic guarantee, not the primary
deterministic terminal residual certificate.
The canonical all-positive Schur batch does have a clean universal fallback:
its total positive exterior-key mass contracts by at least
`1-alpha/p`, where `p=(1+alpha)/2`.  This gives an
`O(alpha^-1 log(1/eps))` batch bound, but not square-root acceleration; an
exact point-source path family has one-batch mass ratio
`(1-alpha^2)/(1+6alpha+alpha^2)=1-Theta(alpha)`.
The RPPR support is also not merely the positive connected component of the
ordinary shifted PPR vector: a three-vertex exact point-source instance has a
strictly active obstacle coordinate whose unconstrained shifted coordinate is
negative.  Any successful reduction must retain nonlinear obstacle/Schur
information.

The classical APPR support sandwich makes the surviving gap especially
precise.  At threshold `rho`, every terminal APPR support contains
`S*(rho)` and is contained in `S*((1-alpha)rho/2)`.  Hence for
`alpha<1/2` it is a certified containing envelope of volume below `4/rho`,
and the point-source radius lemma puts the same envelope within
`O_tilde(1/sqrt(alpha))` hops of the root,
although classical APPR takes tightly `Theta(1/(alpha*rho))` work to build
it.  If this envelope is supplied, accelerated proximal gradient on the
fixed envelope reaches semantic PPR error `eps_ppr` for a general sparse
source in
`nnz(s)+O_tilde(1/(sqrt(alpha)*eps_ppr))` work, without an exact-support
margin.  The square-root radius itself extends to distance from a general
source set; point-source structure makes the construction a single rooted
trace, rather than a collection of components that can merge.  It is not
needed for the terminal oracle solve.
If the scaled point-source RPPR supports have pairwise disjoint closed
neighborhoods, they also decompose exactly at thresholds `rho/s_v`; their
volumes sum to at most `1/rho`, so the additive sparse-source target follows.
The remaining multi-source obstruction is therefore shared boundary rows and
component merging, not the source weights themselves.
The finite route-output locator reduction also extends verbatim after
initializing the sparse source rows: its boundary threshold becomes
`alpha*(rho*d_v-s_v)`, and its total work gains only `nnz(s)`.  Consequently
the unresolved locator, if implemented at the stated output-sensitive rate,
would recover the original additive sparse-source target rather than merely
the point-source specialization.
The complete persistent source-plus-frontier candidate universe has size at
most `nnz(s)+2vol(S*)`, so the difficulty is updating old-coordinate
responses rather than finding or storing candidate row identifiers.
The ordinary-PPR superlevel screen also extends to every source distribution,
but its sharp threshold is `alpha*rho` and hence its volume guarantee is only
`Theta(1/(alpha*rho))`; it does not construct the accelerated envelope.
The principal-pivot response increments are also source-independent:
they are pairwise energy-orthogonal, have total energy at most `alpha/2`,
and total degree-weighted variation at most one.  The point source only
sharpens the energy constant to `alpha/(2d_o)`.
Restricted to the terminal support, the normalized pivot columns sum exactly
to the principal inverse.  The remaining locator is therefore an online,
thresholded inverse-Cholesky-column reporter whose principal matrix is not
known in advance.
The subsequent fixed-envelope proximal solve never needs to identify the
final positive face, so it also bypasses the proper-face
`Q_A 1 != alpha 1` obstruction in the separate momentum-window analysis.
The ordering-independent APPR star already has envelope radius at most one
and volume `Theta(1/rho)` while spending `Omega(vol(E)/alpha)` work, so the
gap is repeated state processing rather than distant or oversized output.
The universal point-source problem is therefore exactly accelerated
construction or dynamic reuse of an output-sized envelope, not an
output-volume existence question.

Two tempting external shortcuts are now ruled to the correct scope.  The
2026 single-source estimation lower bound forces the `Omega(1/eps)` output
scale but assumes constant teleportation, so it does not preclude the
variable-`alpha` square-root target.  Conversely, ChebyPush's local work
analysis assumes a graph-universal `l1` stability constant that fails already
on cubic high-girth balls: the distance-`k` frontier gives
`||T_k(P)||_1 >= (4/3)^(k-1)`.  Thus neither result settles the hard
small-`alpha` regime.

On promised cactus graphs the point-source rootedness now gives a complete
online structural breakthrough.  Maintain current subtree structural volume
and change a heavy child only when a competitor exceeds it by a factor of
two.  Every light edge then shrinks volume by a `2/3` factor, every node
changes heavy child only logarithmically often, and rebuilding the few
affected chain-cactus paths can be charged to comparable atom--route pairs.
Together with the exact per-path epoch reporter, this yields

```text
O_tilde((1+R*) (1+vol(S*)))
```

without knowing the final support or final HLD.  For point-source RPPR this
is `O_tilde((1+vol(S*))/sqrt(alpha))`.  The smallest structural class still
open is therefore a genuinely variable two-port series--parallel block; the
previous unbounded-productive cactus chain is no longer an open case.
On a supplied balanced parse of such a block, static canonical-hull epochs
already give an exact oracle-free fallback in
`O_tilde(N+J sqrt(N))` work.  It is product-scale when the charged block
radius is at least `sqrt(N)`; shallow variable-port blocks still require a
true bulk-pullback/meld reporter or a new charge for this square-root loss.
With only `p` distinct changed home leaves, the same online epoch sharpens to
`O_tilde(N+J min(p+1,sqrt(N)))`, covering repeated updates through a small
productive interface.
An exact weighted-fan construction shows that a single bulk translation of
one child can remove or reinsert linearly many alternating parent-envelope
facets.  Hence constant-many bridge repairs do not remove the loss; the
missing operation really is a lazy transformed meld (or a different global
event representation).

A point-source rho-homotopy still reveals useful extra structure.  On a fixed
face every boundary key is affine in rho, and after admitting one vertex each
surviving critical rho becomes a nonnegative weighted average of its previous
value and the admitted maximum.  This monotone mixing is exact, but the
weights differ by boundary row: a six-vertex rational instance reverses two
candidates' order.  Homotopy therefore replaces the fully arbitrary rekey
problem by dynamic maxima under row-dependent rank-one mixtures, not by an
ordinary lazy heap.

The same slope response removes a different proper-face obstruction.  Put
`h_A=H_A^-1 alpha d_A` and `W_A=diag(d_i/h_i)`.  Exact Stieltjes comparison
gives `0<h_A<=1`, while Perron--Frobenius gives
`alpha W_A <= H_A <= W_A` and `H_A h_A=alpha W_A h_A`.  Every connected
proper face therefore has a canonical known ground state at eigenvalue
`alpha`; the homotopy elimination record already recovers it.  This is
usable by a separately certified no-correction Perron tail, but it does not
by itself transplant the original constant-direction clipping master to the
new mass matrix.
In fact a modified controller is exactly conjugate to the normalized
full-face primitive: with `R=diag(h)`, the operator
`R^-1 W^-1 H R` has constant ground vector, while a `W`-shift and `h`-cap
become the identity shift and constant cap.  This transfers the algebraic
fixed-face interfaces without an eigensolve; it does not supply the separate
high-gap or master-sign certificates those interfaces assume.
The conjugate has a more concrete form:
`diag(d_i h_i)*(Qbar-alpha I)` is exactly the weighted graph Laplacian on
the active induced graph with conductance
`((1-alpha)/2)*h_i*h_j` on edge `ij`.  Thus the extra proper-face high-gap
assumption is precisely a weighted conductance/Poincare assumption.  In
particular, if `q=sqrt(alpha/(1-alpha))`, the explicit Cheeger certificate
`Phi_h >= sqrt(2*alpha/q)=Theta(alpha^(1/4))` implies the required
resolvent high gap.  It does not imply the separate clipped-master sign
condition.  Crucially, the sign condition is unnecessary for the alternative
observable-alignment route: pure prox aligns the transformed residual, a
same-point restart then makes every later `h_A`-cap vanish, and the fixed-face
tail uses only `O_tilde(1/sqrt(alpha))` exact resolvent applications.  A
proper clique with one exterior leaf and size at least `1/alpha` gives an
explicit infinite nonvacuous family satisfying the certificate.  More
generally, if every face vertex has exterior-degree fraction at most `eta`,
then the killed-walk interpretation gives
`min h >= alpha/(alpha+((1-alpha)/2)eta)` and converts ordinary induced-face
conductance or Poincare gap directly into the ground geometry.  With
`eta=O(alpha)`, ordinary conductance `Theta(alpha^(1/4))` or ordinary
Poincare gap `Theta(sqrt(alpha))` is sufficient.  Exact ground data are not
needed even for this certification: any positive `h_tilde` with one-sided
residual `0 <= alpha*d-H*h_tilde <= eps_h*alpha*d` satisfies
`h_tilde <= h <= h_tilde/(1-eps_h)`, so its computed conductance and
Poincare gap, multiplied by `1-eps_h`, are rigorous lower certificates.  A
connected point-source support has one ground mode; disconnected multi-source
faces have one ground mode per component and require componentwise handling.
The same certified high gap also yields a rank-one inverse approximation:
for every face right-hand side, the exact response is its explicit ground
multiple plus a high-mode remainder of norm at most
`q/(alpha*(1+q))` times the centered right-hand side.  For pivot responses
this updates every boundary record through one common scalar and leaves a
simultaneous gray-band certificate.  Its sharper row radius uses the weighted
dual norm `sqrt(sum_i H_vi^2*h_i/d_i)`, rather than summing all coordinate
error radii; this can be much smaller on a wide boundary row.  Rows whose
approximate keys lie outside that interval are classified together.
It closes reporter work when every such band fits inside finite KKT hysteresis;
concentrated loads can still leave a large gray set, so this is a
conductance-certified shortcut rather than a universal event locator.
This interface is fully finite: if a positive approximate ground vector has
the one-sided residual certificate above, its relative sandwich controls both
the ground rank-one coefficient and the high-mode norm.  Explicit coordinate
radii then depend only on the approximate ground vector, its residual error,
and the transformed right-hand side; applying a retained nonnegative coupling
row gives the observable KKT interval directly.
There is also a completely local way to produce the required one-sided
ground certificate.  Truncating the killed-walk Neumann series after `K`
terms gives an exact nonnegative residual bounded by
`((1-alpha)/(1+alpha))^K * alpha*d`.  This removes the logical eigensolver
oracle, but costs `O(vol(A)/alpha * log(1/eps_h))`; obtaining the same
one-sided enclosure in accelerated work is nevertheless possible.  Run
ordinary signed Chebyshev scratch on the normalized face, then apply the safe
Stieltjes max-retraction over the explicit positive checkpoint
`2*alpha/(1+alpha)*sqrt(d)`.  The published residual is nonnegative on every
coordinate, and driving the raw residual below its explicit norm target gives
the relative upper residual certificate in
`O_tilde(vol(A)/sqrt(alpha))` work.  Thus the ground preprocessing loss is
closed; obtaining or verifying the conductance/Poincare lower bound remains a
separate structural condition.
Nested admissions do not require paying that ground solve repeatedly.  For
`B=A union {w}`, the new ground vector is an exact block update by the same
nonnegative pivot-response column `H_A^-1(-H_Aw)` already used by support
discovery.  A one-sided approximate ground and a one-sided approximate
response satisfy an exact residual replay identity: the old residual becomes
`r_h+t*r_u` and the new row residual is zero.  Hence finite response budgets
add across the trace, while exact ground geometry updates for free once the
pivot response has been charged.
Finite sparse pivot responses need no full-face guard.  Their right-hand side
is nonnegative; at every zero coordinate of the safe Stieltjes publication,
the off-diagonal signs make the residual nonnegative automatically.  The
published response can therefore stay sparse while certifying every row.
The same normalized raw-residual target as for the ground solve produces this
response certificate in `O_tilde(vol(A)/sqrt(alpha))` work for one pivot.
Paying that from scratch after every admission would recreate the known
quadratic face-by-face ledger; this closes response safety, not dynamic
response amortization.
There is now an exact low-rank reporter reduction behind the favorable
high-gap case.  Store for each persistent row only its ground coupling `s_v`
and obstacle key `g_v`.  A rank-one admission applies the same invertible
triangular 2-by-2 map to every nonneighbor row; newly adjacent rows are exactly
the ones found by scanning the admitted adjacency list.  A cumulative lazy
matrix turns current-key maximization into a dynamic planar extreme-point
query, giving soft-linear exact reporting when the response is truly rank one.
For conductance-certified approximate rank one, the weighted dual error bands
propagate through the same nonnegative maps; only rows whose accumulated bands
overlap the KKT threshold require fallback.
This branch is nonvacuous even before approximation: on every nested prefix of
an unweighted complete graph, both the ground vector and every exterior pivot
response are constant, with the exact identity
`u=(1-alpha)/(2*alpha*(n-1))*h`.  Hence the gray band is zero and the planar
lazy reporter applies literally.
The zero-band conclusion does not follow from high gap alone.  An exact
`K8` face with two exterior leaves has all seven high generalized eigenvalues
above the required threshold at `alpha=1/17,q=1/4`, yet a leaf pivot has
retained coordinate deviation `-281/20320` from its ground rank-one term.
Thus conductance controls a finite interval but concentrated pivot loads can
still force genuine gray rows.

There is, however, an exact positive algorithm behind this identity.  If the
current exterior Schur complement is kept explicitly, admitting a largest
critical ratio is exactly one Stieltjes pivot; each support coordinate enters
once, and the first largest ratio below the target rho is the global KKT
certificate.  With delta_v denoting the realized Schur-fill degree at the
pivot, discovery costs

```text
O_tilde(vol(S*) + sum_v (1+delta_v)^2).
```

Thus bounded homotopy elimination width gives a genuine point-source
product-scale solver after the existing final-face Chebyshev step.  This is a
structural breakthrough, not yet a general-graph one: explicit fill can be
quadratic even when an implicit tree or separator reporter would be linear.
For finite accuracy, the homotopy does not require exact breakpoint
separation: every exterior affine-key slope lies between `alpha*d_v` and
`(1+alpha)*d_v/2`.  A certified additive upper error `eta` on the largest
remaining ratio therefore contributes at most `(1+alpha)*eta/2` to the
degree-normalized KKT diagnostic.  This is the correct interface for an
approximate or sparsified Schur implementation.

The finite reporter now has an alternative harmonic formulation.  Every
exact singleton pivot adds a killed hitting-probability column; these columns
are pairwise orthogonal in the principal Hessian energy, have a telescoping
total-energy budget, and can trigger only logarithmically many finite
coordinate levels.  Chebyshev decay confines each such level event to
`O_tilde(1/sqrt(alpha))` graph distance from its pivot.  Consequently a
dynamic locator charged once per emitted level plus its pivot-to-event route
would close discovery in `O_tilde(vol(S*)/sqrt(alpha))` work.  Ball scans do
not instantiate this interface because ball volume and repeated overlap are
uncontrolled; existing named-coordinate dynamic inverse structures likewise
do not enumerate all one-sided events.

Response accuracy itself is now separated from event location: a
degree-weighted residual norm gives simultaneous certified intervals for all
coordinates of an approximate killed-harmonic response. Choosing summable
per-pivot residual budgets changes only logarithmic solve accuracy and fits
inside the finite KKT hysteresis.  A dual-energy residual certificate sharpens
the coordinate bound from an explicit `1/alpha` loss to `1/sqrt(alpha)`;
the same energy is exactly twice the response-quadratic objective gap, so any
certified lower objective bound makes the test observable.  The older
ordinary residual norm remains a solve-free sufficient bound.  The
open operation is therefore exhaustive
event-coordinate reporting, not exact response evaluation.

An RPPR route must state its regularization conversion, such as
`rho=tau=eps_ppr/2`, and its terminal certificate. Exact-real means algebraic
cell arithmetic, not exact-minimizer output or a floating-point/bit result.
For `alpha` bounded below by a constant, monotone coordinate descent remains
an allowed fallback. This is a target contract, not a proved theorem.

## AESP--LOCSOR promotion gate

Keep
[`hybrid_aesp_locsor`](../manuscript/notes/hybrid_aesp_locsor/)
as a standalone rigorous research note. Do not promote its graph-uniform
end-to-end complexity claim into the active manuscript until either:

1. the central early-AESP locality lemma

   \[
   \Lambda_J
   := \max_{1\leq t\leq J}
      \frac{\overline{\operatorname{vol}}(S_t)}{\gamma_t}
   = O(1/\epsilon)
   \]

   is proved with a graph-independent hidden constant; or
2. a correct weaker structural condition or alternative burn-in work argument
   sufficient for the stated manuscript theorem is proved.

Until then, the proved trajectory-dependent theorem and explicitly
conditional confinement corollaries may be developed, but the universal
`O_tilde(1/(sqrt(alpha)*epsilon))` work bound is open.

## Current proof fronts

| Direction | Established boundary | Next falsifiable target |
| --- | --- | --- |
| [`aesp_cd_l1_rppr`](../manuscript/notes/aesp_cd_l1_rppr/) | Safe centers, finite residual interfaces, persistent `Q`-energy banks, and high-Dirichlet acceleration are proved. The lagged Euclidean reserve has only `q^2` drift; the simplest unsplit weighted bank fails a stagewise `cq` contraction. | Prove a windowed, spectrally split, nonlinear, or differently normalized low-Dirichlet Lyapunov for the actual finite sequence. |
| [`hybrid_aesp_locsor`](../manuscript/notes/hybrid_aesp_locsor/) | Structured response handoffs and two nonsettled continuations are proved. A settled path makes the observable reset/drop ratio `Theta(1/alpha)`, without yielding a work lower bound. | Pay multiple actual nonsettled reset budgets with a nonadditive/logarithmic ledger, or prove a weaker structural burn-in theorem. |
| [`volume_gated_acceleration`](../manuscript/notes/volume_gated_acceleration/) | The support cap and exact finite path/nonpath causal ledgers are proved in scope. Restarted credit need not recover before the next admission. | Prove all-history solvency under an explicit structural condition or find debt surviving several admissions. |
| [`response_preconditioned_hybrid`](../manuscript/notes/response_preconditioned_hybrid/) | Fixed-face response packing and structured delta reporters are proved. One pivot repairs a three-label reweight collision; general explicit Gram state is quadratic. | Find sparse collision-sensitive state or a geometrically paid replay/rebuild theorem under repeated reweighting. |
| [`propagate_settle_framework`](../manuscript/notes/propagate_settle_framework/) | Several exact settlement/absorption rules are proved on named graph families; the latest double-cycle candidate is retired in its prescribed scope. | Find a different cyclic coupling or bounded-degree settlement gadget with seed chronology proved first. |
| [`local_solver_oracle_hierarchy`](../manuscript/notes/local_solver_oracle_hierarchy/) | Output/capacity bounds and resource separations are proved. Broad supported-prefix product lower bounds are defeated by constant-prefix or sparse-basis counteralgorithms. | Defeat both residual-slack spreading and delayed sparse-basis synthesis, or state a narrower justified model. |

All remaining direction targets, evidence classes, and formal dependencies are
kept in `registry.toml`; use `make note-targets` and `make note-graph` rather
than duplicating them here.

## Reusable conclusions

- The classical APPR upper bound `O(1/(alpha*eps_appr))` is worst-case tight
  on the center-seeded star in the theorem regime. The baseline implementation
  and ordering-independent regression remain in `src/baselines/`,
  `tests/test_appr_lower_bound.py`, and
  `experiments.check_appr_lower_bound`. Path/spider diagnostic rows are not
  theorem checks.
- Fixed RPPR regularization gives a support-volume cap, and safe lower centers
  make local proximal calls oracle-free on certified envelopes. This settles
  local call correctness, not expanding-face accelerated amortization.
- Persistent response state can eliminate repeated solves on paths and other
  structured families, but a graph-uniform output-sensitive boundary
  interface is still missing.
- Orthogonality and energy packing explain why mixed response/frontier methods
  are promising. Dense response application or boundary materialization must
  remain explicit in every claimed work bound.
- Several exact witnesses close tempting proof templates without establishing
  broad solver lower bounds. A STOP for a recurrence, representation, or
  scalar bank must retain that qualifier.

## Round-027 boundary

Round 027 proves an actual-finite lagged Euclidean reserve whose unconditional
comparison yields only `Theta(q^2)` drift. It also proves that direct payment
of the reachable K8 pulse forces a positive coefficient in the lagged unsplit
`q^-1 Q` bank, while a reachable persistent K2 stage then has only `O(q^2)`
relative decrease. The K2 trajectory nevertheless has accelerated global
decay after a logarithmic startup normalization, and the K8 high-band payment
ratio tends to `14641/32256`. Therefore the result stops one stagewise unsplit
template; it is not a net-rate obstruction, an additive-resistant
counterexample, or a solver theorem. Full equations and review provenance are
in [`Round 027`](../manuscript/notes/_shared/coordination/rounds/2026-08-23-round-027.md).

## Evidence and promotion discipline

- `main.tex` plus included section files are proof authority for a direction;
  `STATUS.md` records its current operational state.
- Exact and seeded numerical proof audits live in
  [`experiments/proof_audits/`](../experiments/proof_audits/) and are indexed
  by mechanism, with round number retained only as provenance.
- Numerical tables and graph searches remain measured scaffolding unless a
  theorem explicitly promotes them.
- Promote material to the active manuscript only after its dependencies are
  proved or the claim is narrowed to a correct conditional statement.
- Preserve refuted routes and corrections in the owning note and round record;
  do not keep copying their full history into this current-state file.
