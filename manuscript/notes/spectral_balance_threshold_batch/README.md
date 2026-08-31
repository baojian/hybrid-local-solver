# Spectral balance for deterministic threshold-batch RPPR

Working note, started 2026-08-31.  This note asks whether the random
supplied-face solves in the threshold-batch RPPR theorem can be replaced by a
deterministic Chebyshev/CG construction without changing the target
`O_tilde(vol(S*) / sqrt(alpha))` work.  The specific target is a genuine
cutoff tradeoff, ideally

```text
T(beta) = O_tilde(M / beta + M beta / alpha),
```

whose optimum is attained at `beta = sqrt(alpha)`.  Here
`M = vol(S*)`.  A parameterized promise theorem is not confused with such an
unconditional tradeoff: the spectral parameter must either be certified or
have a second branch that pays when the promise fails.

## Scope and project-convention map

This is an unregistered working companion to the registered
`active_edge_lcp`, `incremental_active_set_sdd`, and
`response_preconditioned_hybrid` directions; it does not replace their
`main.tex` proof authorities or the active manuscript.  The graph is the
project's canonical finite, simple, connected, unit-weight undirected graph,
the source is the point mass at `v`, and

```text
Q = alpha I + (1-alpha) L_norm/2,
S* = supp(x_rho*),                 M = vol(S*).
```

Plain `Q`, `x`, and `D` in this note denote the manuscript's bold matrix,
vector, and degree matrix.  The target is the Stage-I RPPR objective-gap
namespace `eps_obj`; no statement here is automatically a terminal
`eps_ppr` theorem without the manuscript's separate bias and certification
conversion.  Likewise, the residual/retraction formulas below are scoped to
this note's exact obstacle coordinates and do not resolve or rename the
repository-wide residual convention.

Work is charged in the exact-real adjacency-list model: reading a row costs
its ambient degree, every repeated active/boundary scan, sparse product,
response application, materialization, validation, and emitted output is
counted.  A supplied face, hierarchy, factor, response bank, or spectral
certificate is never free unless the statement explicitly makes it a
premise.  Deterministic finite-precision and bit complexity remain open.

Claim classes use the repository meanings **Source**, **Proved here**,
**Conditional**, **Measured**, **Open**, and **Refuted**.  Descriptive tags in
the long audit table refine one of these six classes; they are not additional
evidence levels.

For the concise answer to the three research questions, see
`FINAL_REPORT.md`.  `CLAIMS.md` is the compact theorem/counterexample ledger,
`STATUS.md` contains the exhaustive claim-by-claim audit, and
`VERIFICATION.md` records the exact scope of every executable check.

The exact checks relevant to the final decision boundary are
`path_gap_certificate_exact.py`, `gap_adaptive_fmu_exact.py`,
`adaptive_square_function_exact.py`, `moving_face_smoothing_exact.py`,
`green_bracket_exact.py`, `green_lift_exact.py`,
`projected_green_overshoot_exact.py`, `exact_delayed_clock.md` with its
`exact_delayed_clock.py` verifier, and
`cycle_rank_response_verify.py`.  The larger numerical regression suite is
`witnesses.py`; the two-mask chronology experiments are kept separately in
`two_mask_experiments.py`.

## Current verdict

The extended audit was worthwhile, but its outcome is deliberately split.
It produced a genuine certified-gap moving-state theorem and a new
end-to-end feedback-edge-rank class with no small `o(1)` factor.  It did not
produce an unconditional general-graph `O_tilde(M/sqrt(alpha))` algorithm.
For general graphs the exact remaining object is a persistent shifted
response/publication clock, not another fixed-face eigenvalue estimate.

1. A Dirichlet-adaptive strengthening of the existing batch-depth theorem is
   valid.  It improves both the number of faces and deterministic inner
   solves.
   A second, a-posteriori version uses the *current* face eigenvalue and does
   not require a promise on the final support; it pays only an extra
   `1/alpha` prefactor inside the logarithm.
2. Racing deterministic almost-linear solving against ordinary CG gives a
   useful, rigorous parameterized theorem and can absorb the deterministic
   solver's subpolynomial overhead on high-Dirichlet instances.
3. Neither result yet supplies a term decreasing with the cutoff.  A small
   Dirichlet eigenvalue by itself does not imply that the explored face is a
   good PPR envelope, because the low eigenvector can be localized far from
   the source and the live frontier.
4. The strongest algebraic route for removing repeated face solves is the
   already-proved orthogonal lifted-frontier decomposition in
   `response_preconditioned_hybrid`.  Frontier solve errors add in energy and
   the new blocks are disjoint; after the companion canonical reporting
   ledger is imported, the remaining cost is applying the dense old-face
   responses (`CenterLift`).
5. A genuine `1/tau + tau/alpha` balance does arise in that response
   problem.  It comes from splitting the product of Schur-diagonal loss and
   orthogonal correction energy, rather than from tuning the face condition
   number.  The deterministic positive group probe and canonical
   conservation close candidate/no-miss reporting *given charged response
   summaries*; turning the balance into graph work still needs a persistent
   deterministic producer of those summaries.
6. A deterministic lower-envelope retraction now supplies the required
   support-safety interface for any finite CG/Chebyshev face solve.  It fully
   repairs the oscillatory-residual certification gap with only logarithmic
   extra accuracy.  It does not amortize Krylov work across nested faces.
7. A source-effective spectral cutoff is stronger than the smallest face
   eigenvalue.  A bounded Chebyshev filter can try a cutoff `beta` safely and
   an exact residual check certifies success; low eigenvalues invisible to
   the current right-hand side do not cost iterations.  This is a proved
   instance-adaptive face theorem, but no graph-uniform cross-face sum is yet
   known.
8. On trees, moving-response reuse can be implemented exactly by scalar
   piecewise-affine Schur messages.  This gives an unconditional deterministic
   special-graph solver with no `M^o(1)` factor: work
   `O(log(1+Delta) sum_u |T_u|)`, and an endpoint path has the sharper
   output-sensitive one-pass bound `O(vol(S*))`.  Its quadratic worst case on
   deep branching trees is why it is evidence for, not a solution of, the
   general response interface.  A new projective derivative-segment data
   structure improves the *supplied-tree/envelope* bound to
   `O(n log^2 n)` arithmetic; turning unread boundary subtrees into lazy
   activation promises without inspecting outside `S*` remains a separate
   online lemma if one insists on an exact output-local one-shot obstacle
   solve.  That stronger lemma is not needed for the target bound: the
   shifted-prox/threshold construction below now gives an unconditional
   `O_tilde(M/tau+M tau/alpha)` tree algorithm, and the same conclusion for
   supplied constant-treewidth faces.
9. A separate end-to-end theorem is already closed for bounded-width chordal
   faces.  Fresh exact `LDL^T` costs `O(w^2|U|+vol(U))` per face, so the
   original threshold depth gives
   `O_tilde(((w^2|S*|)+M)/sqrt(alpha))`.  Constant-width chordal graphs and
   supplied constant-treewidth decompositions therefore remove `M^o(1)`.
10. The ballasted broom proves that replacing `[alpha,1]` by each measured
    current-face spectrum and restarting CG/Chebyshev still costs
    `Omega(M/alpha)`.  The face diagonal is constant, so a low lower endpoint
    cannot be paired with a comparably low upper endpoint by Jacobi scaling.
11. The canonical transform `z=y+rho 1` makes every fixed-face right-hand side
    nonnegative and cut-supported.  It yields a valid source-effective cutoff
    and the positive-resolvent ledgers `1/tau` and `tau/alpha`.  The moving cut
    has total signed `l1` variation at most `M`, and padding new transformed
    coordinates by `rho` cancels every old-row RHS change exactly; the sole
    residual is the positive frontier excess.  This closes input accounting,
    not its dense inverse response.  Broom, comb, and one-edge witnesses
    respectively stop fresh cutoff, free explicit DtN tables, and literal row
    settlement.
12. Farfan--Ghadiri--Yang's entrywise SDDM threshold-decay solver is a close
    fixed-matrix analogue of active discovery.  It is randomized, retains
    `2^(O(sqrt(log n)))` cover overlap, and needs global ambient preprocessing;
    it improves fixed-face certification but not the local deterministic
    moving-face bound.
13. A direct CG/backend hybrid really does produce
    `M/beta+chi M beta/alpha` for `beta>=sqrt(alpha)` when the fallback solves
    a face in `chi M` work.  Its optimizer leaves the valid interval when
    `chi>1`, so parameter tuning cannot absorb a deterministic `M^o(1)`
    fallback; constant-overhead bounded-width elimination can.
14. The strongest new general design is conductance-based.  A hypothetical
    nested local `tau`-expander hierarchy gives intra-cluster Chebyshev work
    `M/tau` and only `M tau` coarse edges, hence the exact desired low ledger
    `M tau/alpha`.  Deterministic insertion-local hierarchy maintenance and
    persistent coarse Schur response are both still open; this is marked as a
    conjectural implementation, not an algorithm theorem.
15. The canonical problem is exactly a fixed-obstacle Stieltjes LCP.  Its
    `rho`-homotopy has nested support and at most `|S*|+1` affine pieces, but
    advancing a piece applies the same dense Dirichlet-to-Neumann response;
    a linear pivot count is not a local-work theorem.
16. Cut support does improve a *fixed-face source numerator*: the cut part
    has an exact `(lambda-alpha)` spectral factor, and both cut size and a
    minimax scalar shift give certified favorable-instance cutoffs.  The
    seed/frontier component of the ballasted broom remains visible at the
    required tolerance, so no graph-uniform fresh-face improvement follows.
17. An ordinary *one-shot inverse split* by a scalar shift cannot create the
    desired low-tail rent term.  Once the shift is large enough to improve
    Chebyshev beyond the `1/sqrt(alpha)` scale, a two-vertex SDDM leaves a
    constant fraction of its full `1/alpha` slow response in the unshifted
    tail.  Thus `M tau/alpha` cannot be inferred from `sum d_out` or the
    scalar inverse identity alone.
18. A rigorous rank--port specialization does give
    `O_tilde(M+A/tau+B tau/alpha)`, optimized at
    `tau=sqrt(A alpha/B)`, provided a charged persistent response bank and a
    weighted port-packing certificate are supplied.  Paths and brooms have
    scalar response rank; the comb has full rank.  This is a valid special
    theorem and a precise missing interface, not an unconditional algorithm.
19. Reinterpreting the shift as a **global obstacle proximal step** gives the
    cleanest exact balance found so far.  With `sigma=tau^2`, the obstacle
    resolvent contracts by `sigma/(alpha+sigma)` and takes
    `O_tilde(1+tau^2/alpha)` outer calls.  Therefore a single
    `ShiftedProxClosure(tau)` costing `O_tilde(M/tau)` per call gives exactly
    `O_tilde(M/tau+M tau/alpha)`.  A generalized zero-threshold block-Cholesky
    depth lemma makes this unconditional on every tree and on supplied
    constant-treewidth faces: a shifted prox needs only
    `O_tilde(1/sqrt(alpha+tau^2))` exact nested faces, each structural face
    solve and boundary scan is linear.  Paths retain the sharper incremental
    interval implementation.  On a general graph the closure still requires
    the open no-miss persistent shifted response producer; it is a sharper
    formulation of `CenterLift`, not a proof that this producer is free.
20. The same proximal proof answers the formed-subgraph spectral question
    more strongly than a per-face CG substitution.  If
    `mu_*=lambda_min(Q_(S*,S*))`, every lower iterate and proximal output is
    supported inside `S*`; the resolvent contracts by
    `sigma/(mu_*+sigma)`, and its nested-face depth is
    `O_tilde(1/sqrt(mu_*+sigma))`.  Structural implementations therefore cost
    `O_tilde(A/tau+A tau/mu_*)`, optimized at `tau=sqrt(mu_*)`.  A descending
    guess-and-certify schedule obtains `O_tilde(A/sqrt(mu_*))` without knowing
    `mu_*` in advance.  This is unconditional for the tree/bounded-width,
    low-cycle, and charged dynamic-fill branches; on general graphs it still
    depends on `ShiftedProxClosure`.
21. Chronological block Cholesky gives an observable no-`o(1)` generalization
    of bounded width.  If `F_chol` is the largest retained factor and
    `R_chol` the total elimination-tree closure reached by admissions, the
    exact bound is
    `O_tilde(R_chol+(F_chol+M)/tau+(F_chol+M)tau/mu_*)`.  This closes meshes
    and other localized-fill instances but can be quadratic on expanders or
    adversarial admission orders.
22. The imported two-mask NAG algebra closes correctness, deadlock, state
    transport, held contraction, and all high-frequency pending outputs.  A
    PageRank-specific strengthening proves
    `C^TC<=(A-alpha I)(I-A)`.  Splitting at
    `A-alpha I=tau^2` gives the literal fast coefficient `1/tau` and leaves
    only a floor band with exterior norm at most `tau`; at
    `tau=sqrt(alpha)` this band is merely `[alpha,2alpha]`.  Positive
    truncation yields the proved batch output bound
    `s_B^T(C_Be)_+<=tau sqrt(b cut(U,B))||e||`.
23. The exact follow-up audit rejects the hoped-for final conversion.  Repeated
    activation pulses invalidate the run-wide `O(alpha^2)` burst-start cap,
    although batch-cut Cauchy still pays total output mass.  Absolute output
    cannot count full products without dividing by the publication margin,
    and that restores a forbidden `1/theta`.  Zero-jump interpolation is exact
    for a singleton, but canonical batches cross asynchronously; a simple
    unit graph produces `D` distinct first-step crossing times in one maximal
    batch from the standard zero state.  The precise remaining interface is
    therefore structural: prove a threshold-free `ProjectiveBatchCrossing`
    clock theorem, or maintain the simultaneous inverse response
    (`CenterLift`).  Log determinant cannot pay fixed-face waiting, and AMPS
    closes only the explicit small-fill branch.
24. A different estimate-sequence representation permits an exact
    `dual-dominance projection`: project both the primal and auxiliary
    physical NAG states above the historical subsolution.  Its standard
    potential never increases, every published batch is immediately
    scratch-ready, and the combined expansion debt telescopes to at most
    `alpha||x^*||^2/2<=alpha/2`.  A bounded additive bank still does not
    control the times at which canonical publications arrive, so the
    projective dwell clause remains explicit.
25. The killed-walk Perron survival identity closes the *serial* spatial
    clock.  A source-free chamber with
    `lambda_W<=alpha+tau^2`, under shift `tau^2`, attenuates its positive
    Green maximum by at most `tau^2/(alpha+tau^2)`.  Thus a significant
    serial chain has only
    `O_tilde(1+tau^2/alpha)` layers.  On a supplied bounded-overlap laminar
    hierarchy with mean-zero gap `Omega(tau^2)` and retained responses, each
    layer costs `O_tilde(M/tau)`, proving the desired
    `O_tilde(M/tau+M tau/alpha)` conditional theorem.
26. Perron leakage also proves that a significant disjoint slow chamber buys
    volume `Omega(gamma/tau^2)`.  It cannot be summed over arbitrary
    overlaps: all length-`k` sliding intervals in a `2k` path have tight
    gap/leakage volume `Theta(k)` but total counted volume `Theta(k^2)`.
    Multiple ports are harmless for the one positive Perron mode, but may
    excite signed low mean-zero modes; recursively selecting a deterministic
    laminar hierarchy and transporting its response online is exactly the
    remaining `SourceClockNoReuse/NestedExpanderLift` interface.
27. The stopped-output algebra is now closed on the full spectrum.  Bottom-
    band NAG multipliers first give bounded total variation on a fixed face.
    More strongly, the Stieltjes companion metric
    `F0=acI-c^2S^2` contracts on held steps, is Fejer under the dual lattice
    projection, and loses exactly `||(-Q_BU)w||^2` under principal growth.
    It proves a global `O(alpha)` bank for the physical and velocity cut
    outputs without a band split.  A single monotone reservoir absorbs held
    dissipation, face events, and publications.  What remains is no longer a
    velocity/rotation defect: it is the scale-relative chronology lemma that
    turns this square bank into a count of held products.  The
    dual-projected implementation keeps `iterations*sqrt(alpha)` below
    `20.54` in the structured/random audit, but this remains empirical
    evidence for that final occupancy bridge.
28. A positive Poisson/square-root flow gives an ideal deterministic shared
    clock: `dot d=A^-1/2(g-Ad)` is monotone, root-time convergent, and ordered
    under principal-domain growth for every nonnegative packet.  It is not a
    sparse implementation.  A new lower bound shows any universal
    entrywise-positive walk polynomial approximating `A^-1/2` to fixed small
    relative error has degree `Omega(1/alpha)`.  Root-time positivity must
    therefore use shifted inverse/rational response or graph-specific
    elimination--the same persistent `CenterLift` object in a sharper form.
29. The constant-free `F0` reservoir does not admit a uniform relative
    contraction.  A reachable canonical two-vertex checkpoint has zero
    unopened residual but future Schur energy `Theta(1/alpha)` times its
    active error energy.  The exact repaired inequality is spectral:
    `G<=||b_+||^2/alpha+e^T(A-alpha I)(I-A)e/alpha`.  The witness lies at
    eigenvalue about `1/2` and is paid by the fast branch; after the cutoff,
    only the floor-window projective clock remains.
30. The known stationary vector gives a new observable landscape
    `V_U(i)=alpha+((1-alpha)/2)d_out,U(i)/d_i`.  Its exact ground-state
    identity localizes every mode below `alpha+tau^2` to monotone wells with
    `d_out/d=O(alpha+tau^2)` and buys independent low rank by well volume.
    It yields the closed boundary-exposed special theorem
    `O_tilde(M/(alpha+phi_trace))`, reaching the target when
    `phi_trace=Omega(sqrt(alpha))`.  With a persistent no-replay
    `LandscapeSchurClosure`, it gives the genuine conditional balance
    `A_fast/tau+B_land tau/alpha`; producing the condensed component frames
    through well merges is the remaining general-graph operation.
31. The new `F0` Lyapunov is intrinsically critical-clock, not a hidden
    proof of the whole parameter curve.  For
    `alpha=epsilon^4,tau=epsilon`, three scalar modes rule out every natural
    diagonal metric `pQ direct_sum(kI+gamma F0)`: floor stability forces
    `k=O(epsilon)`, the intermediate mode forces
    `gamma=Omega(1/epsilon)`, and the mid-spectrum mode forbids that value.
    This rules out retuning by scalar weights alone.  It does not rule out
    changing the metric operator.  The certified-gap metric `F_mu` below adds
    the missing distance-one term and gives a valid root `sqrt(mu)` whenever
    `mu<=lambda_min(Q_U)`.  A free cutoff unrelated to a certified face gap
    still belongs to shifted prox or landscape/hierarchy.
32. The earlier shared-clock simulation had a narrower scope than first
    suggested, and its immediate-event failure is now exact.  At
    `alpha=1/1000,rho=1/100000`, the complete projected-NAG/retraction trace
    on a canonical 34-vertex simple-unit graph lies in `Q(sqrt(10))` and has
    publication times `[0,1,2,3,4,38]`.  Every exterior residual is strictly
    nonpositive at products 5 through 37 (the largest is exactly represented
    with value `-2e-8`), while the last batch is strictly positive.  The
    active lower-subsolution and early-stop inequalities are also exact, and
    an exact rational full solve proves `S*=V`.  Thus
    scratch dominance closes only post-publication admission; it does not
    imply publication in the next product.  The longest gap is
    `1.075/sqrt(alpha)`.  The separate `alpha=10^-4` floating-point run has
    scaled gap `0.40`, so neither trace refutes a shared root-scale clock or
    the target runtime.  The exact result is a theorem about this named
    recurrence, not a lower bound for every deterministic algorithm.
33. Exact fixed-face observability Gramians prove
    `sum_t||Cq_t||^2<=J0/(2sqrt(alpha))` and
    `sum_t||q_(t+1)-q_t||_Q^2<=6J0`; the first root factor is sharp on simple
    unit graphs.  They do not splice through face growth using the polynomial
    `F0` bank.  The remaining-variation Gramian contains a resolvent shifted
    by `Theta(sqrt(alpha))`; on unit `P_3` its old block jumps strictly while
    `Ch=Cw=Cq=0`.  The resulting two-layer route has a natural Chebyshev/
    correlation scale `alpha^-1/4` and reproduces the algebraic balance
    `M/tau+M tau/alpha`, but only under the still-open
    `QuarterScaleResponseEpoch(tau)` no-reuse producer.
34. A certified formed-face gap can now accelerate the *moving* companion
    clock without corrupting its event bank.  For
    `alpha<=mu<=lambda_min(Q_U)`, the new Stieltjes metric
    `F_mu=(1+mu)Q-Q^2-mu aI` contracts by `1-sqrt(mu)`, is lattice Fejer, and
    loses exactly `||Cw||^2` at fixed-`mu` face growth.  Certified gaps are
    used nonincreasingly.  Before an expansion whose new certificate is
    `nu<=mu`, rescale the physical auxiliary error from `sqrt(mu)` to
    `sqrt(nu)`; an exact scalar inequality makes this switch nonexpansive.
    The center, gate, and recenter debts then sum to `O_tilde(alpha)` over all
    dyadic levels.  This closes gap-adaptive state transport, not the final
    publication-occupancy theorem or response-summary implementation.
35. A path-Poincare certificate is computable by one boundary-rooted BFS and
    subtree-load pass.  It is a safe lower gap, but on the canonical
    ballasted broom its exact congestion is
    `j^2+(2N+2)j+3N+1`; for `Theta(alpha^-1/2)` consecutive faces both the
    certificate and true gap stay within `1.03alpha`.  Likewise, a fixed-face
    dyadic race obtains the optimal certified-face cost without knowing the
    gap.  These results close parameter selection, not nested replay:
    restarting either solver on the broom still costs `M/alpha`.
36. A raw point-source Green bracket cannot supply the missing replay bank.
    Exact finite simple-unit trees give a negative critical-NAG coordinate
    and a hard lift `1.126299...` times the complete monotone source-reservoir
    increment.  A high-private-degree path family strengthens the ratio to
    `Omega(1.22745543^t/t)`.  This rules out every universal constant payment
    for raw, unstopped NAG.  It does not rule out threshold-stopped or
    maximal-batch chronology because the construction does not force that
    expansion to be a canonical first-crossing event.
37. Coordinate clipping does not restore such a bracket.  On a finite
    simple-unit tree, fixed-face projected NAG has a positive coordinate
    `26.5766...` times its exact Green coordinate.  Canonical
    `rho=epsilon_obj=10^-30` makes both values publication-significant and
    gives `S*=V`.  This is a fixed principal-face witness, not a proof that
    the face/time occurs in the exact maximal-batch chronology.
38. The certified-gap metric also has a sharp fixed-face square function:
    every fixed exterior cut obeys
    `sum||Cq_t||^2<=((3+sqrt(5))/(8sqrt(mu)))J_mu`.  Unit `P4` shows why this
    does not splice into a moving-face tail: the old cut, expansion cut, and
    first two outputs can all vanish, while a later persistent exterior
    output is strictly positive.  This closes gap-adaptive fixed-face
    observability, not `PublicationSharedClock`.
39. A tree-plus-feedback-edge factorization gives a broader end-to-end
    deterministic class.  Pair Green queries form the dense `k x k`
    Woodbury core without materializing `k` full columns, so one exact face
    costs `O_tilde(vol(U)+k^omega_mat)` exact ordered-field operations, where
    `omega_mat` is any fixed admissible matrix-multiplication exponent.  Over only the capped
    `J=O_tilde(alpha^-1/2)` maximal faces this is
    `O_tilde((M+k^omega_mat)/sqrt(alpha))`; it returns the certified approximate
    output and does not assert `U_J=S*` or exact unrestricted termination.
40. Capped shifted-prox termination needs no Green leverage.  If the current
    lower correction has active residual `e>=0` and every current exterior
    score is nonpositive, then `(-e,0)` is a full obstacle subgradient and the
    entire hidden cascade has objective value at most
    `||e||^2/[2(alpha+sigma)]`.  Visible batches still zero-append and share
    source-square mass at most `(1+sigma)alpha`; a norm-buy count requires
    reset-and-zero-append epochs.  The remaining general task is persistent
    accelerated reduction of `e`, with rescans, in `O_tilde(M/tau)` total
    work.  Green leverage remains relevant only to exact restricted-center or
    zero-margin support certification.

The investigation is continuing.  Statements below are separated into
proved claims, candidate bounds, and stops.

## 1. Exact face eigenvalue

Write

```text
Q = alpha I + ((1-alpha)/2) L_norm
```

and, for a proper face `U`, define its Dirichlet normalized-Laplacian gap

```text
delta_U = lambda_min((L_norm)_UU).
```

Because the principal matrix retains ambient degrees,

```text
mu_U := lambda_min(Q_UU)
      = alpha + ((1-alpha)/2) delta_U.
```

For nested faces `U subseteq S*`, interlacing gives `mu_U >= mu_*`, where

```text
mu_* := lambda_min(Q_{S*S*}).
```

The current face eigenvalue is therefore an upper bound on the unknown final
one.  It is not a safe look-ahead certificate.

The upper endpoint can also be measured, but it cannot yield a polynomial
improvement on a low-gap face.  Put

```text
Lambda_U=lambda_max(Q_UU).
```

Every diagonal entry of `Q_UU` is

```text
a=(1+alpha)/2,
```

and hence

```text
a <= Lambda_U <= 1,
kappa_U=Lambda_U/mu_U >= a/mu_U.             (trace obstruction)
```

The lower bound follows already from
`trace(Q_UU)/|U|=a`.  Thus a formed face may improve the upper endpoint from
one to roughly one half, but not to `Theta(alpha)`.  Whenever
`mu_U=Theta(alpha)`, its full spectral condition number is necessarily
`Theta(1/alpha)` up to constants.  Any larger gain must come from a raised
lower endpoint, source invisibility of the low modes, eigenvalue clustering,
or cross-face state reuse---not from replacing the interval `[alpha,1]` by a
uniformly narrow interval around `alpha`.

For completeness, the exact a-posteriori CG ledger along the reached faces
is

```text
T_CG=O_tilde(sum_j vol(U_j) sqrt(Lambda_j/mu_j))
    <=O_tilde(M sum_j sqrt(Lambda_j/mu_j)).    (path-spectrum ledger)
```

This is a useful measured parameter: if its last sum is
`O_tilde(1/sqrt(alpha))`, deterministic CG already has the target cost.  But
the ballasted broom has `mu_j=Theta(alpha)`, `Lambda_j>=a`, and
`Theta(1/sqrt(alpha))` faces, so the sum is `Theta(1/alpha)`.  The trace
obstruction shows that estimating `Lambda_j` more accurately cannot repair
that example.

## 2. Proved Dirichlet-adaptive depth theorem

Let `mu_bar` be any certified lower bound satisfying

```text
alpha <= mu_bar <= mu_*.
```

In the block-Cholesky proof, replace

```text
||C^{-1}|| <= 1/sqrt(alpha)
```

by the exact bound

```text
||C^{-1}|| = 1/sqrt(mu_*) <= 1/sqrt(mu_bar).
```

Every subsequent comparison remains valid.  In particular, for

```text
q_mu = (sqrt(2/mu_bar)-1)/(sqrt(2/mu_bar)+1),
```

the threshold-batch face gap satisfies

```text
gap(U_J) <= 8 q_mu^(2J) + theta^2/(mu_bar rho).
```

The seed term does not acquire an adverse factor because its initial load is
at most `alpha <= mu_bar`.  Choosing

```text
theta = (1/8) sqrt(mu_bar rho eps_obj)
```

gives

```text
J = O_tilde(1/sqrt(mu_bar)).
```

The same replacement is valid in the empty-batch KKT estimate and in the
projection estimate, since every error vector is supported on `S*` or on a
principal subface whose smallest eigenvalue is at least `mu_bar`.

### 2.1 Proved a-posteriori depth from the current face

The current eigenvalue `mu_J=lambda_min(Q_UJ,UJ)` is an upper, not a lower,
bound on the unknown final eigenvalue.  Nevertheless it gives a valid
a-posteriori stopping certificate.  For every included face,

```text
gap(U_J)
 <= (8/alpha) q(mu_J)^(2J) + theta^2/(alpha rho),

q(mu) = (sqrt(2/mu)-1)/(sqrt(2/mu)+1).
```

This statement uses no spectral promise beyond the matrix actually exposed.
Here is the proof.  In the full block order from the threshold-depth theorem,
let `C_hat` be the lower block-bidiagonal Cholesky truncation and split the
dominating solution into its seed-forced and threshold-forced parts.  The
threshold part has the existing norm bound `theta^2/(alpha rho)`.

For the seed part, restrict `C_hat` to its prefix through block `J`.  The same
inverse-order argument used in the main proof gives

```text
||(C_hat_prefix)^(-1)||_2 <= 1/sqrt(mu_J),
||C_hat_prefix||_2 <= sqrt(2).
```

Let `A_J=C_hat_prefix C_hat_prefix^T`.  It is block tridiagonal with spectrum
in `[mu_J,2]`.  A degree-`J-1` inverse polynomial applied to the block-zero
source cannot reach block `J`; subsequent multiplication by
`C_hat_prefix^T` still has zero block `J`.  The usual Chebyshev inverse error
therefore proves

```text
||(seed solution)_J||_2
 <= 2 sqrt(2) (alpha/mu_J) q(mu_J)^J
 <= 2 sqrt(2) q(mu_J)^J.
```

Below the cut, the block-bidiagonal recurrence is homogeneous.  Its entire
tail is the inverse of the lower-right triangular block applied to the one
coupling from block `J`.  The coupling norm is at most one by the Cholesky row
map.  The lower-right inverse is a submatrix of the nonnegative full inverse,
so its norm is at most `1/sqrt(alpha)`.  Hence

```text
||seed tail beyond J||_2
 <= 2 sqrt(2/alpha) q(mu_J)^J.
```

Squaring this bound and combining it with the threshold part exactly as in
the original proof yields the displayed theorem.

If a charged certificate supplies a lower bound on the current-face minimum
eigenvalue, a stopping rule can stop as soon as

```text
(8/alpha) q(mu_J)^(2J) <= target seed gap.
```

Up to logarithms, this asks for `J sqrt(mu_J)>=1`.  If the current gaps stay
above a declared cutoff `beta` until this fires, the number of faces is
`O_tilde(1/sqrt(beta))` and deterministic CG on those faces costs
`O_tilde(M/beta)`.  If a two-sided certified estimate proves that the current
gap crosses below `beta` first, the algorithm can detect that event.  With
only a lower certificate, failure to prove `mu_J>=beta` merely triggers a
conservative switch; it is not evidence that `mu_J<beta`.  This closes the mathematical high-gap side of the desired
rent-or-buy split a-posteriori; making it an algorithm also requires charging
the lower-eigenvalue certificate.  The low-gap continuation is still the missing
`O_tilde(M beta/alpha)` side.

That certificate is not free in general.  Ordinary CG/Lanczos Ritz values
approach the smallest eigenvalue from above, whereas safety needs a lower
bound proving `Q_UU>=beta I`.  Cheap valid examples are a Gershgorin bound
from the exposed rows, a supplied structural Dirichlet/conductance bound, or
an `LDL^T`/inertia certificate on a bounded-width face.  A general sparse
inertia factorization can create fill and must be charged.  Consequently the
formula below is always a valid retrospective execution ledger, and becomes
an online branch only when such a certificate is included in its stated
cost.

One fully local executable certificate is the normalized Gershgorin bound

```text
mu_G(U)=max{alpha,
  min_(i in U)[
    (1+alpha)/2
    -((1-alpha)/2) sum_(j in N(i) intersect U)1/sqrt(d_i d_j)
  ]}.
```

Scanning the already exposed active rows computes `mu_G(U)` in `O(vol(U))`
work and proves `mu_U>=mu_G(U)`.  It can therefore be substituted for `beta`
in the online high-gap branch with no asymptotic extra cost.  It may be very
loose (and is essentially useless on the broom), so it is an implementable
favorable-instance theorem rather than a replacement for the missing low-gap
branch.

The stationary-vector ground-state identity proved later supplies a second,
often cleaner certificate:

```text
mu_U>=mu_land(U)
     :=alpha+((1-alpha)/2)
       min_(i in U) d_out,U(i)/d_i.               (landscape gap)
```

It is also computed in one exposed-row scan and is a genuine lower spectral
bound, not a Ritz estimate.  It can replace `mu_G` in every high-gap race.
If even one deep interior vertex has `d_out,U(i)=0`, the bound falls back to
`alpha`, so it does not evade the ballasted-broom stop.  Its stronger use is
not the minimum but the low-well decomposition: after removing vertices
with `d_out/d=O(alpha+tau^2)`, the complementary principal block has a
certified `Omega(alpha+tau^2)` gap.  That refinement and its remaining
Schur-transport condition are stated in the landscape section below.

As an immediate unconditional corollary, suppose the actual threshold trace
obeys the observable boundary-exposure promise

```text
phi_trace=min_(reached U) min_(i in U) d_out,U(i)/d_i.
```

Then every reached face has the common certified gap

```text
mu_bar=alpha+((1-alpha)/2)phi_trace.
```

The Dirichlet-adaptive threshold depth is
`O_tilde(1/sqrt(mu_bar))`, and deterministic Chebyshev/CG solves one face in
`O_tilde(M/sqrt(mu_bar))`.  Hence fresh deterministic formed-face solves
already give the executable end-to-end bound

```text
T_exposed=O_tilde(M/mu_bar)
         =O_tilde(M/(alpha+phi_trace)).        (boundary-exposed theorem)
```

In particular, `phi_trace=Omega(sqrt(alpha))` reaches
`O_tilde(M/sqrt(alpha))` without a deterministic SDD backend or any
subpolynomial factor.  The promise is checked online by row counts.  It is a
real special-instance theorem, not a general solution: a single fully
interior reached vertex makes `phi_trace=0`, as on the ballasted broom.

There is a completely measurable two-parameter refinement which is useful on
instances having only a short low-gap suffix.  Face interlacing makes
`mu_j=lambda_min(Q_(U_j,U_j))` nonincreasing.  For a declared cutoff `beta`,
let

```text
ell_beta = number of reached faces at or after the first mu_j<beta.
```

Before that crossing, the a-posteriori stopping rule permits only
`O_tilde(1/sqrt(beta))` faces, each costing
`O_tilde(M/sqrt(beta))` by CG.  On every later face, race fresh CG against the
deterministic almost-linear solver.  This gives the proved execution ledger

```text
T(beta,ell_beta)
 <=O_tilde(
      M/beta
      +M ell_beta min{M^o(1),1/sqrt(alpha)}
    ).                                      (low-suffix ledger)
```

The analysis may minimize this expression over the gaps of the realized
trace.  An algorithm may do so only over cutoffs for which it has obtained a
charged lower certificate; no final-support eigenvalue is assumed.  The
ledger improves the generic bound when the low-gap suffix is short.  It is
**not** the desired balance: no spectral
argument bounds `ell_beta` by `beta/alpha`, and the broom has
`ell_beta=Theta(1/sqrt(alpha))` for every `beta` larger than a constant
multiple of `alpha`.  Thus introducing the observed eigenvalue as a parameter
is valid, but optimizing it alone cannot manufacture the missing buy term.

### 2.2 Ballasted-broom stop for fresh current-face solves

The current-face theorem is useful only when the observed gap actually rises.
There is a canonical single-source tree on which it does not, even though the
exact active trace continues for `Theta(1/sqrt(alpha))` large faces.

Assume `0<alpha<=1/256`.  Let the seed `o` have

```text
N=ceil(10/alpha)
```

leaf neighbors and one additional path
`o-v_1-v_2-...-v_m`, where
`m>=L+1` and `L=floor(1/(8sqrt(alpha)))`.  Put

```text
D=d_o=N+1,                 rho=1/(4D).
```

For the canonical RPPR load, the first exact positive-residual batch contains
all `N` leaves and `v_1`.  After that, at least the next `L` batches are the
singletons `v_2,...,v_(L+1)`.  Every post-first face `U_j` has

```text
vol(U_j)=Theta(1/rho),
alpha <= mu_j=lambda_min(Q_(U_j,U_j)) <= 1.025 alpha.
```

Here is a proof of the nontrivial singleton claim.  Work in degree
coordinates with

```text
H=aD-bA,       a=(1+alpha)/2,       b=(1-alpha)/2.
```

The seed right-hand side is `3alpha/4`, while a nonseed vertex of degree `d`
has right-hand side `-alpha rho d`.  On the seed-only face,

```text
y_o=3alpha/(4aD),
g_leaf=alpha/(4D)(3b/a-1)>0,
g_v1  =alpha/(4D)(3b/a-2)>0.
```

Thus the claimed first batch is exact for `alpha<1/5`.  Eliminate the leaves
from every later face.  The remaining root equation is

```text
A_0 y_0-b y_1=h,
A_0=(D alpha+b^2)/a <=21,
h=alpha/4(3-(N/D)(b/a)) >=alpha/2.
```

On a face ending at `v_j`, split the path solution as `y=p-m`.  The positive
part `p` has root forcing `h` and zero path forcing.  The nonnegative part
`m` has zero root forcing and path forcing `2alpha rho`.  Set

```text
kappa=arcosh(a/b)=2 atanh(sqrt(alpha)).
```

The homogeneous Green formula gives

```text
p_j
 = h sinh(kappa)
   /(A_0 sinh((j+1)kappa)-b sinh(j kappa))
 >= (h/A_0) sinh(kappa)/sinh((j+1)kappa).
```

For `j<=L`, `(j+1)kappa<=0.38`.  The elementary inequality
`sinh(nx)<=n sinh(x) cosh(nx)` therefore yields

```text
p_j >= alpha/(46(j+1)).
```

The negative part has an even simpler endpoint bound.  Put
`Delta_i=m_i-m_(i-1)` and use the fictitious Dirichlet value `m_(j+1)=0`.
The root Robin equation gives `Delta_1>=0`, while each path row gives

```text
b(Delta_i-Delta_(i+1))+2alpha m_i=2alpha rho.
```

Summing implies

```text
m_j<=2alpha rho j/b.
```

Since `rho<=alpha/40`, `b>0.498`, and
`alpha(j+1)^2<=9/256`, the positive bound is strictly larger than
`2alpha rho(j+1)/b`.  Hence

```text
y_j>2alpha rho/b,
g_(v_(j+1))=b y_j-2alpha rho>0.
```

The path is the only remaining boundary edge, so every one of these batches
is a singleton.  Finally, the test vector `sqrt(d)` on `U_j` is constant in
normalized coordinates on every internal edge and pays exactly the one cut
edge.  Therefore

```text
mu_j<=alpha+b/vol(U_j)
    <=alpha+alpha/40
    =1.025alpha,
```

while `Q>=alpha I` gives the lower bound.  Also
`vol(U_j)=2N+1+2j>=1/(4rho)`, and
`L=Omega(1/sqrt(alpha))`.  Consequently

```text
sum_(j=1)^L vol(U_j)/sqrt(mu_j)
 = Omega(1/(rho alpha)).
```

This is a rigorous route stop: exact or certified estimation of the current
face eigenvalue, followed by a fresh Chebyshev schedule or a fresh full-face
inverse-square-root probe charged by `vol(U_j)/sqrt(mu_j)`, cannot prove the
target on this family.  It is **not** a lower bound for every deterministic
algorithm.  The graph is a tree, and a retained Schur recurrence or tree
elimination can reuse the path response in linear work.  The separation says
precisely that moving-face response reuse, rather than a sharper current-gap
estimate, is necessary.

There is a complementary *Krylov-locality* sharpening which does not merely
insert the condition number into an upper-bound formula.  Take an endpoint
path of length

```text
n=Theta(1/sqrt(alpha))
```

and let `y^0=H^-1 alpha e_v` be its unregularized degree-coordinate
response.  Choose

```text
rho=1/2 min_i y_i^0.
```

Then the regularized solution has full support and

```text
y*=y^0-rho 1>=rho 1,       z*=y*+rho 1=y^0.
```

The first identity uses `H^-1 alpha d=1`.  For this path length the standard
hyperbolic solution of the tridiagonal recurrence has bounded endpoint
ratio and `min_i y_i^0=Theta(sqrt(alpha))`; equivalently this follows from
the recurrence together with `d^T y^0=1`.

Every proper reachable face is a prefix, and its only exterior neighbor is
the next path vertex.  Since the final support is the whole path, the safe
pivot theorem implies that this sole boundary vertex must be live; hence the
exact face chain has singleton expansions.  On a prefix `U_j`, the
cut-supported transformed load is supported only at its two endpoints:

```text
H_Uj z^Uj=alpha e_v+rho b e_(last)              (up to endpoint weight).
```

Starting from zero, every vector in the `k`th Krylov space is supported
within distance `k-1` of those endpoints, because multiplication by the
path matrix moves support by at most one edge.  If `k<j/2`, a middle
coordinate of the Krylov candidate is zero whereas `z_i^Uj>=rho`.  Thus no
fresh CG, MINRES, or Chebyshev polynomial of that degree can achieve
coordinate error below `rho/2` (and the manuscript's lower-envelope
tolerance is smaller on this family).  For the `Theta(n)` prefixes with
`j>=n/2`, every fresh solve therefore needs `Omega(n)` sparse matvecs, each
costing `Theta(n)`.  The cumulative fresh-Krylov work is

```text
Omega(n^3)=Omega(M/alpha),
```

while the target is `Theta(M/sqrt(alpha))=Theta(n^2)`.  The cut has one edge
throughout.  This is an actual lower bound for zero-start/fresh polynomial
Krylov on the concrete cut-supported right-hand sides, not just a pessimistic
spectral schedule.  It still does not lower-bound warm state carrying a
nonlocal response: the one-pass path Schur recurrence below attains linear
work and is exactly the missing kind of state reuse.

### 2.3 Positive special case: exact tree-response reuse

The preceding qualification is constructive.  Root a finite tree at the
single seed `o`.  For a nonroot vertex `u` with parent `p`, let `T_u` be its
descendant subtree and condition on the parent value `t>=0`.  If
`beta_pu=-Q_pu>0`, define the exact response

```text
mu_u(t)=beta_pu z_u(t),
```

where `z(t)` minimizes the restricted nonnegative quadratic on `T_u` with
the added load `beta_pu t e_u`.  Stieltjes comparison and scalar Schur
elimination give all of the following.

1. `z(t)` is continuous and coordinatewise nondecreasing; its supports are
   nested.
2. It is zero exactly until the explicit threshold
   `t=alpha rho sqrt(d_u)/beta_pu`.
3. `mu_u(t)` is continuous, nondecreasing, and piecewise affine with at most
   `|T_u|+1` pieces.  On a fixed active subtree `A`, its slope is
   `beta_pu^2 (Q_AA^(-1))_uu`.
4. At the root, the unique solution is the zero of

```text
Q_oo t-c_o-sum_{u child of o} mu_u(t)=0;
```

   every affine-piece slope is the positive root Schur complement and is at
   least `alpha`.

The proof is entirely deterministic.  Bottom-up multiway merging of child
breakpoint lists, followed by one top-down evaluation, gives the exact RPPR
solution in

```text
O(log(1+Delta) sum_{u != o}|T_u|)
```

arithmetic and the same response storage.  Since
`sum_u |T_u|<=n h` for rooted height `h`, this is near-linear on bounded- or
logarithmic-height trees and has no dependence on `1/sqrt(alpha)`.  On the
finite ballasted broom with path length `Theta(1/sqrt(alpha))`, the `N`
ballast leaves contribute `N` and the path contributes only
`O(1/alpha)`; because `N=Theta(1/alpha)`, the exact work is `O(n)`.  Thus the
broom strictly separates fresh Krylov restarts from retained response
messages.

There is an even sharper endpoint-path algorithm.  Forward elimination
maintains only the pivot and transformed demand

```text
delta_i=a_i-beta_i^2/delta_(i-1),
eta_i=c_i+beta_i eta_(i-1)/delta_(i-1).
```

The first `eta_i<=0` is exactly the final KKT boundary; back substitution on
the preceding prefix returns the exact solution.  It reads every discovered
edge once and costs `O(1+vol(S*))`.  This is a genuine deterministic removal
of the small-`o(1)` factor for a nontrivial special class.

The general tree message theorem is not yet the desired graph theorem.  A
deep tree can have `sum_u|T_u|=Theta(n^2)`, and on a graph with cycles the
separator message is a matrix-valued piecewise quadratic object rather than
a scalar list.  The comb obstruction says that its exact boundary rank can
already be linear.  What the tree theorem proves is that the missing DtN
operation is not intrinsically expensive on the broom: it becomes expensive
only when one discards the causal elimination state or when separators cease
to be scalar.

### 2.4 Projective segment compression on a supplied tree

The explicit `sum_u|T_u|` construction is not the best static tree bound.
There is a lazy projective representation that avoids applying the parent
Schur transform separately to every descendant breakpoint.

For a conditional response `mu(t)`, store its nondecreasing derivative as
finite segments of slope `s` and horizontal length `ell`, followed by one
terminal ray.  Convexity follows either from Stieltjes comparison or by
viewing `mu` as the derivative of the convex conjugate of the subtree value
function.  Suppose the child responses at `u` sum to `m(x)`, the local
diagonal (including any proximal shift) is `a`, the local right-hand side is
`r`, and the parent edge has magnitude `w=-Q_up>0`.  On a positive piece,

```text
a x-r-m(x)=w t,                 mu_u(t)=w x.
```

Hence a segment of `m` transforms exactly as

```text
s'   =w^2/(a-s),
ell' =(a-s)ell/w.                         (tree Schur segment map)
```

All denominators are positive because they are scalar Schur pivots.  This
map belongs to a closed lazy-tag family.  Let a tag `(M,kappa)`, with

```text
M=[[A,B],[C,D]],
```

act by

```text
s'   =(A s+B)/(C s+D),
ell' =kappa(C s+D)ell.
```

If a balanced sequence node stores only

```text
L=sum ell,             P=sum s ell,
```

then the whole subtree is updated in constant arithmetic:

```text
[P';L']=kappa M [P;L].                    (projective moments)
```

Tags compose as `(M_2 M_1,kappa_2 kappa_1)`.  The parent Schur map is the
single tag

```text
M_u=[[0,w^2],[-1,a]],        kappa_u=1/w.
```

This is why the apparently prefix-dependent slope conversion does not force
a scan of the list.

The other needed operation is also closed.  To sum a smaller child response
into a larger derivative sequence, add the child's initial slope globally;
then, at every child breakpoint, insert its positive slope jump and add that
jump to the suffix.  A suffix slope addition by `Delta` is the projective tag

```text
M_Delta=[[1,Delta],[0,1]],       kappa=1.
```

An implicit balanced search tree supports coordinate split, breakpoint
insertion, suffix tagging, concatenation, and prefix search using `(L,P)`.
The node activation/truncation is one prefix search: with
`F(x)=a x-r-m(x)`, a segment contributes

```text
Delta F=a L-P.
```

If `F(0)<0`, discard the unique prefix ending at `F=0`; if `F(0)>=0`, prepend
the zero-response interval of length `F(0)/w`.  A vertex creates at most one
new breakpoint, and discarded prefixes never return.

Choose the largest child sequence as the merge base and insert every smaller
sequence.  Each surviving breakpoint moves into a container at least twice
as large, so it moves `O(log n)` times.  Each balanced-tree operation costs
`O(log n)`.  This proves the following arithmetic theorem.

```text
Given a supplied n-vertex tree (or a supplied n-vertex tree envelope),
the exact Stieltjes obstacle solution and its active set can be computed in
O(n log^2 n) arithmetic and O(n) live segment storage.
```

After locating the root crossing, the active breakpoint labels determine the
active subtree; a final ordinary tree elimination/back substitution recovers
all values in linear work.  A reversible split log is an equivalent recovery
method.  Splay/dynamic-finger merging may remove one logarithm, exactly as in
the sandpile data structure, but that sharpening is not needed here.

This theorem is **supplied-tree**, not yet support-local.  Reading the whole
ambient tree can be much larger than `S*`.  A local implementation would
represent each unread boundary child only by its first activation threshold,
then expand its adjacency list when a demand-driven root prefix search first
crosses that promise.  Causality says the newly revealed response modifies
only the unprocessed suffix, so the same projective algebra is compatible
with such a generator.  What is still missing is a proved meld/split schedule
showing that online promise refinements retain the `O(M log^2 M)` movement
bound.  This `LazyTreePromise` lemma is a precise tree version of no-miss
`ShiftedProxClosure`; the static projective theorem must not be cited as if it
already proved local discovery.

## 3. Proved deterministic solver race

Let `f(M)=M^{o(1)}` denote the overhead of a deterministic almost-linear
Laplacian/SDD solver on an `O(M)`-nonzero face.  A face can instead be solved
by deterministic Chebyshev or CG in

```text
O_tilde(M/sqrt(mu_bar))
```

work.  Racing the two methods on every face and using the adaptive depth gives

```text
T_det(mu_bar)
  = O_tilde(
      (M/sqrt(mu_bar)) min{f(M), 1/sqrt(mu_bar)}
    ).
```

One final Stage-II face solve costs only

```text
O_tilde(M min{f(M),1/sqrt(mu_U)}),
```

and is dominated by the Stage-I bound.  Thus the target
`O_tilde(M/sqrt(alpha))` follows in either of the regimes

```text
mu_bar >= sqrt(alpha)                  (CG branch),
mu_bar >= alpha f(M)^2                 (almost-linear branch).
```

The second condition is the first genuine way in which spectral improvement
can pay for the `M^{o(1)}` deterministic overhead.  It is conditional on a
certified final-face lower bound.

Section 2.1 removes that final-support promise at the cost of an additional
logarithm.  If the a-posteriori rule stops at face `J` with current gap
`mu_J`, every earlier principal face has gap at least `mu_J`.  Racing the two
solvers on those faces gives the same power-law bound

```text
O_tilde(
  (M/sqrt(mu_J)) min{f(M),1/sqrt(mu_J)}
),
```

where the soft notation now also hides `log(1/alpha)`.  Thus the two displayed
high-gap regimes can be recognized from the formed face; no prediction of
`mu_*` is needed.  The final-gap promise theorem remains sharper by avoiding
the extra logarithmic prefactor and is useful when a structural envelope is
known in advance.

### 3.1 A known deterministic small-support branch

There is a second parameterized improvement which is independent of the
Dirichlet gap.  Let

```text
s=|S*|,       M=vol(S*),       M_in=nnz(Q_(S*,S*))<=M.
```

The conjugate-direction algorithm of Martinez-Rubio--Wirth--Pokutta
discovers the orthant and solves it exactly in

```text
O(s^3+s M)
```

time and `O(s^2)` space.  Their approximate recycled-CG variant has the
bound

```text
O_tilde(s M_in min{s,1/sqrt(alpha)}+s M).
```

These are not output-linear in general, but they remove the deterministic
SDD subpolynomial factor on genuinely small supports.  In particular,
`M>=s` implies

```text
s<=alpha^(-1/4)
  => s M<=M/sqrt(alpha),
     s^3<=M/sqrt(alpha).
```

Thus the exact conjugate-direction branch already meets the desired target
throughout the cardinality regime `s<=alpha^(-1/4)`, without a spectral
promise and without randomness.  More generally the best presently proved
deterministic portfolio is, up to accuracy logarithms,

```text
min{
  M/alpha,                              fresh-face Chebyshev,
  M^(1+o(1))/sqrt(alpha),               deterministic SDD per batch,
  s^3+s M,                              exact conjugate directions,
  s M_in min{s,1/sqrt(alpha)}+s M       recycled-CG active set
}.
```

The first two entries are the threshold-batch routes analyzed here; the last
two use their source paper's own active-set sequence.  This portfolio is a
real improvement for small `s`, but it does not give the requested
graph-uniform `M/sqrt(alpha)` theorem because `s` can be as large as `M`.

### 3.2 End-to-end deterministic theorem on bounded-width chordal faces

There is also a structural class on which the requested derandomization is
already complete.  Suppose every reachable induced face has a chordal
completion with an exposed perfect-elimination order of width at most `w`.
This holds without preprocessing when the input graph is chordal with maximum
clique size `w+1`: every induced subgraph is chordal and maximum-cardinality
search finds and verifies a perfect-elimination order from its exposed rows.
Trees are the case `w=1`.  The same conclusion holds for a bounded-treewidth
graph if a compatible width-`w` decomposition/order is supplied or maintained
within the stated local cost.

On each threshold-batch face `U`, deterministically:

1. construct/restrict the width-`w` elimination order;
2. factor the degree-coordinate Stieltjes matrix
   `H_UU=aD_U-bA_UU` exactly as `L D L^T`;
3. solve the current face by two triangular substitutions;
4. scan the exposed rows, admit the exact threshold batch, and repeat.

A width-`w` factor has `O(w|U|)` nonzeros.  Its numeric factorization costs
`O(w^2|U|)`, triangular solution costs `O(w|U|)`, and order construction plus
the fully charged boundary scan costs `O(vol(U))`.  No approximate residual,
randomized chain, or cross-face warm start is required.  Exact Stieltjes
support safety and the existing depth theorem apply unchanged.  Since there
are `O_tilde(1/sqrt(alpha))` faces and every reachable face is contained in
`S*`, the complete work is

```text
O_tilde(
  ((w^2 |S*|)+M)/sqrt(alpha)
)
 <=O_tilde((w^2+1)M/sqrt(alpha)).             (bounded-width theorem)
```

The bound includes refactorizing every face from scratch, all row and
boundary scans, order construction, solution materialization, and output.
Therefore constant-width chordal graphs give an unconditional deterministic
removal of the small-`o(1)` factor for the original algorithm, not merely a
solver subroutine.  The theorem does not extend by replacing treewidth with
degeneracy: sparse graphs can have large elimination fill.  For unbounded
`w`, the factor `w^2` is the explicit price of the dense separator response.
The display is an arithmetic-operation theorem, matching the manuscript's
real-RAM work model.  If all input weights are rational and exact bit
complexity is required, fraction growth must either be included or the
triangular solves must be performed to the certified residual tolerance and
passed through the lower-envelope adapter; that adds accuracy/weight-length
logarithms, not a new width or `alpha` power.

## 4. Cutoff beta: what a valid balance would require

If `beta <= mu_*` is certified, the current proved bound is

```text
T_high(beta)
  = O_tilde(
      (M/sqrt(beta)) min{f(M),1/sqrt(beta)}
    ).
```

For plain CG this is `O_tilde(M/beta)`.  Choosing `beta=sqrt(alpha)`
recovers the target only on instances satisfying the promise.  The parameter
cannot be optimized freely: choosing `beta > mu_*` invalidates both the batch
depth and the residual-to-energy certificates.

An unconditional square-root balance needs a second algorithm invoked when
`mu_* < beta`.  The ideal missing statement is

```text
T_low(beta) = O_tilde(M beta/alpha).
```

Then `T_high(beta)+T_low(beta)` is minimized at `beta=sqrt(alpha)`.  No such
low-gap theorem has yet been proved.

There is a useful exact audit of the most direct hybrid interpretation of
this formula.  Suppose a deterministic backend solves and certifies one face
in

```text
O_tilde(chi vol(U))
```

work, where `chi>=1` is its overhead over a sparse linear pass.  Use CG on
the high-gap prefix and switch permanently to this backend at the first face
whose certified gap falls below `beta`.  Interlacing makes the high-gap faces
a prefix.  The a-posteriori depth theorem gives at most
`O_tilde(1/sqrt(beta))` such faces, each costing
`O_tilde(M/sqrt(beta))`, while the entire remaining suffix contains at most
`O_tilde(1/sqrt(alpha))` faces.  Therefore the fully charged hybrid ledger is

```text
T_hybrid(beta)
 <= O_tilde(M/beta + chi M/sqrt(alpha)).       (exact hybrid ledger)
```

For `beta>=sqrt(alpha)`, the second term can be weakened to the desired
shape,

```text
T_hybrid(beta)
 <= O_tilde(M/beta + chi M beta/alpha).        (hybrid balance)
```

This is a genuine executable balance whenever the gap test has a charged
lower certificate.  It also explains exactly when tuning helps.  The formal
minimizer of the last display is `sqrt(alpha/chi)`.  For every nonconstant
overhead `chi>1` it lies below the range `beta>=sqrt(alpha)` in which the
low-suffix conversion is valid, so the best valid endpoint is
`beta=sqrt(alpha)` and the cost remains

```text
O_tilde((1+chi)M/sqrt(alpha)).
```

Thus setting `chi=f(M)=M^o(1)` for the deterministic almost-linear SDD
backend cannot tune away its subpolynomial factor.  Setting `chi=O(1)` does
meet the target; this is exactly what the bounded-width `LDL^T` theorem
provides.  The ballasted broom makes the suffix count tight at the crossover:
it has `Theta(1/sqrt(alpha))` low-gap singleton faces.  Therefore a better
general result needs either a constant-overhead deterministic low-gap face
solver or cross-face response reuse; an eigenvalue cutoff alone cannot
manufacture the missing `chi=O(1)` backend.

### 4.1 Proved source-effective cutoff (no eigenvalue promise)

The minimum eigenvalue is more pessimistic than necessary for a particular
face correction.  Let `A=Q_UU`, let `g` be the normalized right-hand side
remaining from the current lower subsolution, and fix any
`alpha<=beta<1`.  Define

```text
x_beta(lambda) = (1+beta-2 lambda)/(1-beta),
q_k,beta(lambda)
  = T_k(x_beta(lambda))/T_k(x_beta(0)).
```

Then `q_k,beta(0)=1`.  On `[0,beta]`, it lies between zero and one; on
`[beta,1]`,

```text
|q_k,beta(lambda)|
 <= 1/T_k((1+beta)/(1-beta))
 <= 2 exp(-2 k sqrt(beta)).
```

The last inequality uses
`arcosh((1+beta)/(1-beta))=2 atanh(sqrt(beta))>=2sqrt(beta)`.
Because `q(0)=1`,

```text
p_(k-1)(lambda)=(1-q_k,beta(lambda))/lambda
```

is a polynomial.  The deterministic candidate `y=p_(k-1)(A)g` has residual
`r=q_k,beta(A)g`.  If `P_<beta` denotes the spectral projector of `A`, then

```text
||r||_2^2
 <= ||P_<beta g||_2^2
    + 4 exp(-4 k sqrt(beta)) ||g||_2^2.
```

Thus, whenever the current right-hand side has low-spectrum mass at most
`eta/2`, degree

```text
k = O((1/sqrt(beta)) log(||g||/eta))
```

meets residual tolerance `eta`.  Crucially, the polynomial is bounded on the
whole possible spectrum `[alpha,1]`; this is not an invalid Chebyshev solve
run with a guessed lower eigenvalue.  The implementation computes the actual
residual after the attempt.  If it passes, Section 5.7 retracts and certifies
it.  If it fails, decrease `beta` dyadically.  The degrees form a geometric
sum, and `beta=alpha` always succeeds, so the adaptive face cost is

```text
O_tilde(vol(U)/sqrt(beta_eff)),
```

where `beta_eff` is the largest attempted cutoff whose checked residual
passes.  No spectral projector or prior estimate of `beta_eff` is required.

This answers part of the spectral question affirmatively: a formed face can
be cheap even when its smallest eigenvalue is close to `alpha`, if the active
correction is nearly orthogonal to its low modes.  It is also a safer
parameter than using the current `mu_U` as a prediction of the unknown final
gap.

The limitation is summation.  Applying the theorem independently to nested
faces gives

```text
sum_j O_tilde(vol(U_j)/sqrt(beta_eff,j)).
```

Neither interlacing nor correction-energy orthogonality bounds this sum by
`M/sqrt(alpha)`: the old rows can be revisited in every term.  A failure at
cutoff `beta` does certify source-visible low mass, and for an exact
orthogonal frontier correction of energy `E_j` it implies

```text
E_j >= ||P_<beta g_j||_2^2/beta.
```

Summing over the exact orthogonal corrections and using
`sum_j E_j<=alpha` gives the sharper global source ledger

```text
sum_j ||P_<beta g_j||_2^2 <= alpha beta.       (low-band source ledger)
```

The canonical positive-source conservation identity of Section 5.6.1 gives
a second, incomparable bound.  In degree coordinates the correction load
`r_j` is nonnegative and the normalized load is `g_j=D^-1/2 r_j`; hence

```text
||P_<beta g_j||_2 <= ||g_j||_2 <= ||r_j||_1.
```

There are `O_tilde(1/sqrt(alpha))` reached batches and each canonical batch
has total excess load at most `alpha`.  Therefore

```text
sum_j ||P_<beta g_j||_2 <= O_tilde(sqrt(alpha)).
                                                    (low-band L1 ledger)
```

Consequently the number of faces whose low-band residual alone exceeds an
absolute tolerance `eta` is at most

```text
min{alpha beta/eta^2, O_tilde(sqrt(alpha)/eta)}.
```

This is a real cross-face gain: it counts failed source-cutoff attempts
without multiplying by the number of old-face eigenmodes.

It still does not close the target at the manuscript tolerance
`eta^2=Theta(alpha rho eps_obj)`.  The count becomes only

```text
min{
  O(beta/(rho eps_obj)),
  O_tilde(1/sqrt(rho eps_obj))
},
```

and a failed attempt may already have read the whole current face.  Neither
this count nor the energy identity assigns those repeated old-row reads to
disjoint volume.  Aggregating the low-band pieces before materialization
would avoid the replay, but implementing that aggregation and emitting its
group summaries is exactly `CenterLift/AggregateLift`; discovering the
intervening batches from already-emitted summaries is
`BoundaryReportGivenLift`.
Thus the low-band source ledger is proved and should be used in any future
balance proof, while treating it as `M beta/alpha` graph work would conflate
energy with row access.

There is a further implementation caveat.  The two displays concern the
*exact* frontier load obtained by padding the exact previous face solution.
If the previous face is only approximate, its known residual is carried into
the enlarged face and can itself have low-band mass.  Re-solving it away at
every transition restores the restart tax; retaining it is precisely the
delayed numerical-debt stream handled conditionally by `AggregateLift`.
Therefore the source ledgers may count exact low-mode events inside that
primitive, but they do not by themselves justify a fresh-filter algorithm
with only that many fallbacks.

## 5. Candidate mechanisms under audit

### 5.1 Shifted face solves

Replace `Q` by `Q+sigma I` to raise the smallest eigenvalue.  The shifted
obstacle solution is a coordinatewise lower solution, hence support-safe, but
it can omit true active coordinates.  Its original-objective bias satisfies

```text
F(x_sigma)-F(x*) <= (sigma/2) ||x*||_2^2 <= sigma/2.
```

The standard objective-to-semantic conversion therefore requires
`sigma = O(alpha eps^2)`.  A large spectral shift such as
`sigma=sqrt(alpha)` is not accuracy-safe.  Homotopy or iterative refinement
must supply a new amortization; the shift alone is not the desired balance.

Both assertions have direct proofs.  If `x_sigma-x*` had a positive part on
an index set `I`, subtracting the two complementarity systems would give
`(Q(x_sigma-x*))_I<0`; the Stieltjes signs instead imply this vector dominates
`Q_II (x_sigma-x*)_I^+`, contradicting positive definiteness.  Hence
`x_sigma<=x*`.  Optimality of `x_sigma` for
`F(x)+(sigma/2)||x||^2` gives the displayed bias, and the unit-source energy
bound gives `||x*||^2<=1`.

### 5.2 Polynomial spectral splitting and deflation

Chebyshev can approximate `1/x` on `[beta,1]` in
`O_tilde(1/sqrt(beta))` degree.  The remainder is the spectral subspace below
`beta`.  A fixed-rank deflation is not graph-uniform: connected Stieltjes
families can have arbitrarily many eigenvalues in `[alpha,O(alpha)]`.  A
valid theorem must charge an adaptive low-spectrum dimension, separator
rank, or source-visible spectral mass; `lambda_min` alone is insufficient.

The ballasted broom gives a quantitative rank stop even for a *constant*
post-deflation gap.  Take `r=Theta(1/sqrt(alpha))` consecutive internal path
vertices, all of ambient degree two.  Their principal normalized block is
tridiagonal with diagonal `a` and off-diagonal `-b/2`, hence has eigenvalues

```text
nu_k=a-b cos(k pi/(r+1)),       k=1,...,r.
```

For every fixed `gamma in (0,a)`, a constant fraction of these values is at
most `gamma` once `alpha` is small.  Principal-submatrix interlacing implies
that the full broom face also has `Omega(r)=Omega(1/sqrt(alpha))`
eigenvalues below `gamma`.  Finally, if a deflation space has dimension less
than that count, its orthogonal complement intersects the corresponding low
eigenspace nontrivially; the min--max principle then leaves a Rayleigh
quotient below `gamma`.  Therefore *any* deflation that raises the complement
gap to a constant on this family needs rank
`Omega(1/sqrt(alpha))`, independent of how its vectors are constructed.
This rules out a graph-uniform constant/polylog-rank reference basis as a way
to make every broom face a linear-time CG solve.

### 5.3 Shifted preconditioning

The obvious degree/Jacobi scaling cannot improve the face condition number.
In degree coordinates `H=aD-bA`, its diagonal is exactly `aD`; therefore

```text
(aD_U)^(-1/2) H_U (aD_U)^(-1/2)=Q_UU/a.
```

Both spectral endpoints are divided by the same scalar.  In particular, the
ballasted-broom lower endpoint remains `Theta(alpha)` and its upper endpoint
remains `Theta(1)`.  Any successful preconditioner must encode off-diagonal
Green-function/Schur information; degree scaling alone is not a hidden way to
narrow the formed-subgraph spectrum.

Using `Q+beta I` as a preconditioner for `Q` produces outer condition number

```text
kappa_out <= ((alpha+beta)/(alpha(1+beta))).
```

Solving each preconditioner application by Chebyshev has condition number
`(1+beta)/(alpha+beta)`.  The two square roots cancel exactly:

```text
sqrt((1+beta)/(alpha+beta))
  sqrt((alpha+beta)/(alpha(1+beta))) = 1/sqrt(alpha).
```

Thus the work is

```text
O_tilde(M/sqrt(alpha)),
```

independent of `beta`, for one fixed face.  This recovers the familiar CG
bound but does not remove the number of face rebuilds.  With accelerated
outer iteration the cutoff disappears rather than producing a tunable gain.

There is, however, an exact way to expose the requested tradeoff before
outer acceleration cancels it.  Parameterize the shift as `sigma=beta^2`
with `sqrt(alpha)<=beta<=1`, and use

```text
P_beta = Q + beta^2 I.
```

A constant-relative-accuracy Chebyshev application of `P_beta^-1` costs

```text
O_tilde(M/beta).
```

Preconditioned Richardson for `Q` has contraction governed by
`alpha/(alpha+beta^2)` and therefore needs
`O_tilde(1+beta^2/alpha)` applications.  Its fully multiplied fixed-face
work is

```text
T_fixed(beta)
 = O_tilde(M/beta + M beta/alpha).
```

The optimum is exactly `beta=sqrt(alpha)`, giving
`O_tilde(M/sqrt(alpha))`.  Outer PCG replaces `beta^2/alpha` by
`beta/sqrt(alpha)` and makes the two square roots cancel, as in the preceding
calculation.  Thus this balance is real but is not a faster fixed-face
solver; it is a two-scale decomposition of the standard Chebyshev rate.

Its importance is architectural.  If all disjoint Schur-frontier blocks
admitted over the run supported shifted applications whose *total* base
volume was `M`, then the same calculation would give the desired end-to-end

```text
O_tilde(M/beta + M beta/alpha).
```

The numerical part therefore exists.  What is missing is a charged
implementation of a frontier Schur product: applying

```text
K_B y = H_BB y - H_BU H_UU^(-1) H_UB y
```

requires exactly the old-face inverse response.  If that operation scans or
solves on `U` for every new block or Richardson step, the disjoint-volume
premise is false and the restart tax returns.  This identifies a concrete
missing lemma rather than an unexplained optimization parameter:

```text
sum over all frontier shifted/Schur applications of charged work
  = O_tilde(M/beta).
```

Together with the lower-envelope publication theorem, that lemma would turn
the fixed-operator balance into the requested deterministic algorithm.

The one-sided probe results sharpen the missing lemma but do not prove it.
For each disjoint frontier block, the inverse-square-root response can be
split at the same scale `beta`: the lower integral tail is majorized by
`beta K_B^{-1}`, while all shifts in the upper tail are at least `beta^2`.
Under the same total-base-volume premise, this exposes the same two formal
ledgers:

```text
upper shifted tail:       O_tilde(M/beta),
low inverse/repair tail:  O_tilde(M beta/alpha).
```

The first uses Chebyshev on matrices grounded by at least `beta^2`; the
second is the positive Richardson/low-tail debt.  The displayed costs are
conditional on charging the Schur applications to disjoint frontier volume,
not a new proof of that charge.  With `g=1_B`, the resulting probe is an
entrywise group upper oracle, so no Gaussian source selection is left in this
decomposition.

To obtain an actual algorithm one still needs the following single primitive.

```text
PositiveFrontierRentOrBuy(beta):
  for adaptive nested faces and disjoint frontiers B_j,
  apply or query every shifted Schur response and low-tail debt needed by
  the correction and the one-sided group probes;
  expose no unsafe adjacency rows;
  publish certified group upper bounds and exactly validate reached leaves;
  charge all old-face reads, response applications, cut scans, and delayed
  defects in total
      O_tilde(M/beta + M beta/alpha).
```

Three independent tests show why every clause is necessary.  The ballasted
broom refutes fresh full-face scans even with exact current eigenvalues; the
one-edge shifted-debt example refutes literal sparse coordinate settlement;
and the three-coordinate CG example refutes zero-padding without the Schur
lift.  None is a lower bound against the stated primitive, but together they
leave no hidden ``ordinary CG'' implementation.  Proving this primitive, or
restricting the graph so that it follows from elimination/separators, is the
remaining end-to-end task.

#### Block-extension preconditioning: a proved trigger, not a producer

There is a clean way to test whether an old-face preconditioner remains
spectrally useful after one batch.  Write the shifted enlarged face as

```text
A_T=[A_U  E; E^T  F],       C=A_U^(-1/2) E F^(-1/2).
```

With the *exact* old inverse and the raw new block, block-diagonal
preconditioning gives

```text
diag(A_U,F)^(-1/2) A_T diag(A_U,F)^(-1/2)
       =[I C; C^T I].
```

Consequently, if `s=||C||_2<1`, its condition number is exactly

```text
kappa_ext=(1+s)/(1-s).                              (extension condition)
```

The corresponding Schur complement is

```text
S=F-E^T A_U^(-1)E=F^(1/2)(I-C^T C)F^(1/2).
```

Thus a batch with `s<=gamma<1` can reuse an already-applicable old inverse
with only a constant conditioning loss.  This is a rigorous low-coupling
``rent'' rule.  It remains true up to the usual multiplicative factor if
`A_U` is replaced by a spectral preconditioner.

The natural high-coupling rebuild potential also telescopes.  For nested
blocks `B_j`, let `F_j` and `C_j` denote the raw diagonal block and normalized
coupling at its admission.  Block determinants give the exact identity

```text
Psi_J := sum_(j<=J) -log det(I-C_j^T C_j)
       = log( det(A_0) prod_j det(F_j) / det(A_J) ).  (log-det ledger)
```

If every shifted face has spectrum in `[mu,L]` and the final dimension is
`N`, then

```text
sum_j ||C_j||_F^2 <= Psi_J <= N log(L/mu),
# {j: ||C_j||_2>=gamma}
  <= N log(L/mu)/[-log(1-gamma^2)].                  (coupling packing)
```

The first inequality uses `-log(1-x)>=x`; the second uses determinant
bounds.  Hence `Psi` is a valid deterministic checkpoint/rebuild trigger.

It is **not** the missing `M/beta` work ledger.  Applying the supposedly
reused block preconditioner already requires `A_U^(-1)` on each new right
hand side, while forming the exact extension requires the response matrix

```text
R_B=A_U^(-1)E.
```

Neither operation is paid by `Psi`.  Even when every `||C_j||_2` is bounded
by a fixed constant, singleton admissions can produce one new dense,
linearly independent response column per batch.  A full response bank then
has rank `Theta(|S*|)`; on paths and trees elimination compresses it, but a
generic sparse graph has no such supplied representation.  Re-solving each
column by Chebyshev costs `O_tilde(vol(U)/sqrt(mu))`, restoring the restart
tax.  Therefore the block lemma localizes the remaining theorem precisely:

```text
maintain/apply the old inverse or its Schur responses under low-coupling
extensions in total O_tilde(M/beta), rather than merely prove that the
extended operator is well preconditioned relative to that unavailable
inverse.
```

This distinction also prevents a circular proof: an exact old inverse is an
excellent extension preconditioner, but treating its application as unit
cost assumes `CenterLift` itself.

The log-determinant trigger can be compared sharply with the two remaining
proper-face ledgers.  For a frontier vector `y`, put `u=F^(1/2)y`.  Its old
face lift and Schur energies are exactly

```text
E_lift = ||C u||_2^2,
E_S    = u^T(I-C^T C)u.
```

On a low-coupling batch, `||C||<=gamma<1`, hence

```text
E_lift <= [gamma^2/(1-gamma^2)] E_S.          (light lift ledger)
```

Because exact nested frontier corrections are energy-orthogonal, this
inequality sums without replay.  It is genuinely useful for the new light
increment ledger: once an aggregate response vector is available, its total
low-coupling energy is paid by the correction energy.  It does **not** build
that vector or give a directional lower certificate for an unseen row.

Two exact families show that log determinant cannot fill those gaps.

1.  On the two-vertex PageRank block
    `A=[a -b;-b a]`, `a=(1+alpha)/2`, `b=(1-alpha)/2`, admission of the
    second coordinate has `C=-b/a`.  Therefore

    ```text
    Psi=-log(1-C^2)=Theta(log(1/alpha)),
    E_lift/E_S=C^2/(1-C^2)=Theta(1/alpha).
    ```

    Thus no polylogarithmic multiple of `Psi` pays a severe Green dwell or
    the scale `1/alpha` response amplification.  More basically, a long
    severe interval on a fixed face has positive occupancy but zero new
    log-determinant increment.  A link from severe occupancy to `Psi` would
    need an additional controller lemma forcing a quantitatively coupled
    face expansion; it is false from operator geometry alone.

2.  Let `J=ceil(1/tau^2)`, start with `J` old scalar coordinates, and admit
    `J` scalar partners whose independent Stieltjes blocks are
    `[1 -tau;-tau 1]`.  Every normalized coupling is `tau`, so

    ```text
    sum_j -log(1-tau^2)=Theta(1),
    rank [A_(U_(j-1))^(-1)E_j : j=1,...,J]=J=Theta(1/tau^2).
    ```

    The final condition number is only `(1+tau)/(1-tau)`.  Arbitrarily weak
    Stieltjes links make the example connected without changing the
    separation.  Hence a constant trace/log-det budget may hide exactly the
    `Omega(1/tau^2)` independent light directions seen in the canonical
    nested-Krylov construction.  Log determinant can pack *squared response
    mass* but cannot pay response rank, materialize an aggregate Green probe,
    or validate that a reported direction is aligned with the actual source.

The resulting audit is therefore asymmetric: the light energy estimate is
a valid component that should be retained, while both `severe occupancy <=
logdet` and `light response rank <= logdet` are false.  The still-missing
lemma is precisely an output-sensitive aggregate Green probe plus a
directional lower validation, or a different scale-relative/projective
payment for severe occupancy.

The newer two-history proper-face algebra narrows this statement further.
Take as an imported, independently checked interface the identities

```text
J_h=(1+tau)s_W^T b_h
```

at expansion times, the first-crossing velocity ledger, and whole-burst
telescoping for the held-face defect `Delta=M_prev-M`.  These facts cancel
the cut/rank-two contribution on the scalar slow mode and charge every
expansion source through Green amplification only once.  After those
cancellations, the only uncharged term has the form

```text
O_sev = alpha sum_(h severe) W_h M_h.          (severe occupancy)
```

The log-determinant potential is still incapable of paying this last term.
It changes only when the principal face expands, whereas a severe interval
may remain on one fixed face for arbitrarily many held updates.  Thus even a
perfect bound on the total expansion potential says nothing about its
occupancy.  The two-vertex block above gives the scale separation on the
same fixed operator: its slow Green amplification is `Theta(1/alpha)` while
the entire available determinant loss is only `Theta(log(1/alpha))`.

The binding dichotomy does suggest the right *kind* of missing statement,
but does not yet prove it.  A sufficient scale-relative lemma would be an
inequality of the schematic form

```text
alpha sum_(h in I severe) W_h M_h
 <= C [ P_a-P_b
        + sum_(h in I) E_h^(mean-zero)
        + q^2 W_a Delta_a ],                  (projective dwell)
```

for every maximal held interval `I=[a,b]`, where `P` is a nonnegative
projective potential for the scalar coefficient (for example a clipped
logarithmic ratio) and `E^(mean-zero)` is already paid by orthogonality.
The known row-binding alternative only says that one binding event either
contracts the scalar coefficient or creates mean-zero energy.  It does not
show that every unit of `W_h M_h` causes such an event; a held interval can
have occupancy without a new bind.  Consequently `(projective dwell)` is a
genuine missing lemma, not a relabeling of the existing dichotomy.

For the light branch the conclusion is complementary.  Log determinant
does pay the aggregate lift *energy* once the aggregate Green response has
been materialized.  The independent `1/tau^2`-block family shows that it
cannot pay for constructing those directions one by one.  Positivity lets a
single summed probe dominate all of them after their sources are known, but
causality prevents simply postponing that solve: an unseen first crossing
may be needed to create the next source.  Therefore the exact remaining
light interface is

```text
AggregateGreenFirstCrossing(tau):
  maintain one-sided group upper summaries for the causal sum of all light
  responses, and at a reported leaf produce a source-aligned lower witness,
  in total O_tilde(M/tau) work.
```

The existing positive group oracle supplies the mathematical upper bound;
the residual/retraction adapter validates a lower witness once a candidate
coordinate is evaluated.  What remains open is their persistent production
without replaying old-face edges.  This is now strictly narrower than a
generic dynamic inverse.

There is a sharper PageRank-specific coupling inequality which materially
shrinks the low-frequency part of that interface.  Let `A=Q_UU` and
`C=-Q_BU`, where `B` is any subset of the exterior boundary.  The full
normalized PageRank operator satisfies

```text
alpha I <= Q <= I,
Q^2 <= (1+alpha)Q-alpha I.
```

The `UU` block of `Q^2` is
`A^2+Q_(U,V\U)Q_(V\U,U)`.  Since `C^TC` is only part of the second summand,
taking the `UU` principal block proves

```text
C^T C <= (A-alpha I)(I-A).                  (floor-aware coupling)
```

This strictly strengthens `C^TC<=A-A^2` and vanishes on a genuine
`alpha`-eigenvector, as it must: a global floor mode has no exterior cut.
It is invariant under the proximal shift.  Indeed
`Q_sigma=Q+sigma I` has spectral interval
`[alpha+sigma,1+sigma]`, the exterior block is unchanged, and the same
argument gives

```text
C^T C
 <=(A_sigma-(alpha+sigma)I)((1+sigma)I-A_sigma)
 =(A-alpha I)(I-A).
```

Thus the floor-window split can be used inside `ShiftedProxClosure` without
paying for the shift a second time.
For `tau>0`, let

```text
P_lo=1_[alpha,alpha+tau^2](A),
P_hi=I-P_lo.
```

Functional calculus then gives the exact split

```text
||C P_lo||_2 <= tau,
P_hi C^T C P_hi <= tau^(-2) P_hi A^2 P_hi.  (floor-window split)
```

The second inequality plugs directly into the proved NAG potential, whose
first term is `||Ah||^2/2`: every pending output above the floor window costs
the desired `1/tau` fast factor.  At the target `tau=sqrt(alpha)`, the
previously unresolved spectral interval `[alpha,sqrt(alpha))` collapses to
the much narrower `[alpha,2alpha]`, and its operator coupling to the exterior
is at most `sqrt(alpha)`.  This is the first spectral split in the audit that
literally has the two coefficients needed for

```text
M/tau + M tau/alpha.
```

It is not yet the end-to-end activation theorem.  `P_lo` is a signed spectral
projector, and an `l2` operator bound does not by itself give a one-sided,
degree-weighted candidate-volume bound.  The abstract rank-one fan-out

```text
C=(tau/sqrt(k)) 1_k u^T
```

has `||C||=tau` but `||Ch||_1=tau sqrt(k)|u^Th|`; star fan-outs approximate
this behavior.  Thus converting `(floor-window split)` to an `l1` scan would
reintroduce a square-root boundary-size loss.  The squared-mass group oracle
can use the `l2` statement, but still needs a causal positive upper summary
and a source-aligned leaf validation.  The remaining narrow lemma is

```text
FloorBandActivation(tau):
  for P_[alpha,alpha+tau^2](A), charge all one-sided first crossings and
  exact leaf validations by O_tilde(M tau/alpha), without materializing the
  signed projector or scanning every fan-out after each face change.
```

If the new two-mask first-crossing/conservation ledger proves this lemma,
the NAG high-window inequality supplies `M/tau`, and the requested balance
is unconditional.  Without it, neither determinant nor AMPS fills the gap:
log determinant is unchanged throughout a held interval, while AMPS can
only *buy* the exact floor-band response at the already-stated
`R_chol+F_chol` fill-reach cost.  Spectral smallness alone gives no bound on
that topological fill.

The PageRank stationary vector gives a stronger **one-sided weighted** bound
than the raw fan-out example permits.  Put `L_U=A-alpha I` and let
`s_U=sqrt(d_U)`, `s_W=sqrt(d_W)`.  The global identity `Qs=alpha s` gives

```text
L_U s_U=C^T s_W,
s_U^T L_U s_U=b cut(U).                      (stationary cut identity)
```

For an arbitrary signed vector `e`, positivity of `C` implies
`(Ce)_+<=C e_+` coordinatewise.  Moreover `L_U` is a grounded graph
Laplacian, so its Dirichlet form is Markovian:

```text
(e_+)^T L_U e_+ <= e^T L_U e.
```

Consequently, if `e=P_lo h`, then

```text
s_W^T(Ce)_+
 <=s_U^T L_U e_+
 <=sqrt(s_U^T L_U s_U) sqrt(e^T L_U e)
 <=tau sqrt(b cut(U)) ||e||_2.               (one-sided floor flux)
```

This localizes to the actual pending batch.  For `B subset W`, let
`d_B(i)` be the weight from `i in U` into `B` and put

```text
K_B=b diag(d_B(i)/d_i).
```

Then `C_B^T s_B=K_Bs_U`, `0<=K_B<=L_U`, and the same proof gives

```text
s_B^T(C_Be)_+
 <=tau sqrt(b cut(U,B)) ||e||_2.             (batch floor flux)
```

This is strictly better for cumulative accounting.  Once `B` is admitted,
its `U--B` edges become internal; across disjoint first-crossing batches,

```text
sum_B cut(U_before_B,B)<=M.
```

Thus the square-root cut factors in the activation-scale ledger can be
combined by Cauchy against a one-time edge budget rather than charged to the
entire face cut on every held interval.

Unlike a normwise projector estimate, this controls exactly the positive
part of the exterior deficit and survives arbitrary spectral signs.  It is
therefore a plausible bridge to the new two-mask first-crossing ledger.
For the canonical right-hand side, the initial operator-weighted NAG energy
is at the `alpha^2` scale; if the proved expansion potential also yields the
run-wide invariant `||P_lo h||_2=O(1)`, `(one-sided floor flux)` charges the
near-floor pending mass by `O(tau sqrt(cut(U)))` per held time.  A
whole-burst/cut Cauchy ledger of total scale `M` would then give the desired
`O_tilde(M tau/alpha)` slow term.

The last implication is deliberately marked conditional.  It requires two
checks in the exact two-mask notation:

1. the activation/candidate weight must match `s_W^T(Ce)_+` (or dominate it
   without a degree loss); and
2. `L+(1+alpha)G` must control the low-window Euclidean norm across every
   mask expansion, not merely `||Ae||` on a held face.

If either check fails, the fan-out conversion or the `1/alpha` norm loss
returns.  Thus `(one-sided floor flux)` is a proved algebraic lemma and a
specific route to `CertifiedActivationRate`, not yet a claimed cumulative
rate theorem.

The strict held-step NAG contraction turns those two checks into an almost
mechanical conditional rate theorem.  The operator-weighted potential obeys

```text
L_t >=(1/2)||A h_t||_2^2 >=(alpha^2/2)||h_t||_2^2.
```

For the floor-window component `e_t=P_lo h_t`, `(one-sided floor flux)` gives

```text
s_W^T(Ce_t)_+
 <=(tau/alpha) sqrt(2b cut(U) L_t).           (pending from potential)
```

During one held interval beginning at `a`, the supplied NAG Lyapunov theorem
has `L_(a+k)<=(1-s)^k L_a`, with `s=sqrt(alpha)`.  Since
`1-sqrt(1-s)>=s/2`, summing the last display yields

```text
sum_(k held) s_W^T(Ce_(a+k))_+
 <=O((tau/(alpha s)) sqrt(cut(U)L_a)).        (held floor output)
```

Therefore, under the concrete run-wide invariant

```text
L_a=O(alpha^2) at every burst start,             (canonical energy cap)
```

one interval costs only `O((tau/s)sqrt(cut(U)))`.  With at most
`J=O_tilde(1/s)` threshold faces, `cut(U)<=M`, and `M>=1`, even the crude sum

```text
sum_intervals O((tau/s)sqrt(cut(U)))
 <=O_tilde(M tau/s^2)
 = O_tilde(M tau/alpha)                (conditional floor-output rate)
```

has exactly the desired slow scale for *cumulative weighted pending output*.
A sharper cut/burst Cauchy ledger can only improve it.  This is not yet the
same as a bound on the number of held iterations.  If the safely published
row that keeps interval `a` alive has weighted margin `m_a`, then every held
step must satisfy `m_a<=s_W^T(Ce_t)_+` only after the already-closed high
window is removed.  The exact rate consequence is

```text
N_a^lo
 <=O((tau/(alpha s m_a)) sqrt(cut(U_a)L_a)),

sum_a N_a^lo=O_tilde(1/s)
 if
 sum_a sqrt(cut(U_a)L_a)/m_a=O_tilde(alpha/tau).
                                             (activation-scale ledger)
```

Thus the canonical energy cap alone closes the output ledger but can be too
weak after division by a very small publication margin.  The light-floor,
first-crossing, or whole-burst theorem must prove `(activation-scale
ledger)` in its own normalization.  This is the exact scale-relative clause
which cannot be replaced by log determinant.

A minimal abstract sequence proves that this qualification is necessary.
For `a=1,...,J`, set

```text
m_a=2^(-a),       cut_a=1,       L_a=m_a^2.
```

Then `sum_a L_a<1`, so every absolute energy/light-floor budget is excellent,
but

```text
sum_a sqrt(cut_a L_a)/m_a=J.
```

Thus neither summable expansion energy, a uniform burst cap, nor an
expansion-only log-determinant potential implies the activation-scale
ledger.  A proof must use the causal relation between successive margins and
velocities supplied by the two-history/first-crossing dynamics.  This is a
counterexample to a *potential-only proof template*, not a lower bound for
the PageRank two-mask algorithm; the displayed sequence has not been claimed
to be realizable by a canonical graph.

This isolates a very small final audit against the two-mask proof.  If its
combined potential `L+(1+alpha)G` is nonnegative and globally bounded at the
canonical `alpha^2` scale after accounting for all light-floor events, then
`(canonical energy cap)` follows immediately.  If its definition of pending
activation work is directly the cumulative weighted positive deficit,
`(conditional floor-output rate)` closes it.  If the charged object is the
number of held iterations, its margin-normalized ledger must imply
`(activation-scale ledger)`.  Only then is `FloorBandActivation(tau)` proved
and the high/low split closes `M/tau+M tau/alpha`.  Until these
notation-level implications are checked, the displayed statements remain
conditional rather than an end-to-end claim.

The same cutoff has an exact interpretation in the accelerated recurrence,
not merely in the boundary inequality.  For `tau>=sqrt(alpha)`, put

```text
s_tau=sqrt(alpha+tau^2),
beta_tau=(1-s_tau)/(1+s_tau).
```

With unit gradient step, one eigenmode `lambda` of NAG obeys

```text
r^2-(1+beta_tau)(1-lambda)r
   +beta_tau(1-lambda)=0.                    (damped roots)
```

Its discriminant changes sign exactly at
`lambda=s_tau^2=alpha+tau^2`.  Above that point the roots are complex and

```text
|r|=sqrt(beta_tau(1-lambda))<=sqrt(beta_tau)
    <=exp(-Theta(s_tau)),
```

so the fast time is `O(1/s_tau)=O(1/tau)`.  Below the breakpoint the larger
root is

```text
r_+(lambda)
 =[1-lambda+sqrt((1-lambda)(s_tau^2-lambda))]/(1+s_tau)
 <=1-lambda/(4s_tau).
```

The floor mode therefore has slow time
`O(s_tau/alpha)=O(tau/alpha)`.  This proves that the two terms in the desired
tradeoff are the underdamped and overdamped time scales of one tunable
deterministic recurrence.  At `tau=sqrt(alpha)`, its breakpoint is exactly
`2alpha`, matching the floor-aware boundary window above.

Running `(damped roots)` over every edge for the entire slow time would cost
`M tau/alpha` and gives no additive improvement by itself.  The role of
`(batch floor flux)` is to confine that overdamped output to the charged
frontier/cut ledger, while the full face is scanned only on the
`O(1/tau)` fast scale.  This is the precise algorithmic meaning of
`M/tau+M tau/alpha`; it is not obtained by simply retuning full-face CG.

The corresponding algorithm is nevertheless concrete and requires no
eigenvector computation.  The cutoff is used only in the proof:

```text
TwoMaskNAG(theta):
  K <- {seed}                         # support-safe published lower mask
  U <- {seed}                         # signed scratch mask
  initialize persistent NAG state (x,v) on U and lower subsolution ell=0
  repeat:
    retract the current signed state through the residual-safe adapter
    ell <- ell join retracted(x)
    publish into K every lower-certified score above theta/2

    while some published batch B subset K\U has r_B(x)>=0:
      zero-pad B into U
      transport (x,v) and charge the exact expansion potential

    if QuietKKT_theta(ell): return ell
    take one held NAG step on Q_U and update exposed boundary residuals
```

The imported two-mask lemmas establish support safety, correctness of
zero-padding, absence of deadlock, the exact held contraction, and the
expansion jump formula.  Every step is deterministic; a sparse held update
and its boundary bookkeeping cost at most the final exposed volume `M`.
No line calls an SDD solver, constructs `P_lo`, or assumes the final support.

For analysis only, split the pending error at
`A-alpha I=tau^2`.  The high part is paid by the proved NAG
operator-weighted potential and `(floor-window split)`.  The low part is
paid by `(batch floor flux)` provided the margin-normalized
`(activation-scale ledger)` follows from the light-floor/first-crossing
account.  Under that one remaining hypothesis the implementation above has

```text
T_TwoMask(tau)=O_tilde(M/tau+M tau/alpha),
T_TwoMask(sqrt(alpha))=O_tilde(M/sqrt(alpha)).
```

This is the most specialized deterministic design obtained in the audit:
all its numerical, safety, and high-frequency components are proved, and
its sole unproved line is a scalar cumulative activation inequality.  It is
strictly stronger than a conditional `CenterLift` oracle, but must not be
called an end-to-end theorem until that inequality is checked in the exact
two-mask normalization.

The exact two-mask audit now decides the two conditional checks above.

First, `(canonical energy cap)` is **not** preserved by the available event
ledger.  One activation pulse contributes at most `O(alpha^2)`, but there may
be `J=O_tilde(1/s)` pulses, so the run-wide scale can be

```text
sum_j g_j^2=O_tilde(alpha^2/s)=O_tilde(alpha^(3/2)).
```

This does not destroy the cumulative *output-mass* estimate.  Using the
batch-specific cuts, `sum_j cut(U_j,B_j)<=M`, Cauchy still gives at
`tau=s=sqrt(alpha)`

```text
sum held weighted floor output
 <=O_tilde(sqrt(M)/sqrt(alpha))
 <=O_tilde(M/sqrt(alpha)).
```

It does invalidate the stronger claim that every burst begins at
`L=O(alpha^2)`.

Second, output mass cannot be converted to the number of full products
without a relative/projective argument.  For any scalar pending mode, scale
its forcing, safe margin, and output by `epsilon`.  Its sign-crossing time is
unchanged, whereas `sum_t |output_t|` is multiplied by `epsilon`.  Therefore
no inequality of the form

```text
number of held products <= constant * absolute pending flux
```

can hold uniformly.  Dividing by the certified margin is valid but introduces
`1/theta`; the target theorem permits only logarithmic accuracy dependence.
The geometric sequence `m_a=2^-a,L_a=m_a^2` shows that summable light energy
does not repair this scale loss.

There is an exact singleton repair: interpolate one NAG step to the first
time a coordinate has residual zero.  Adding that coordinate then has zero
Lyapunov jump.  Batches do not cross synchronously, however; this already
occurs on the canonical simple unit-weight `P_4`.  Processing the coordinates
one at a time can replay the face, while repairing the whole batch to a
simultaneous zero-jump state requires

```text
d_T=Q_TT^(-1)[0;r_B],       T=U union B,
```

up to the exact state-coordinate convention.  This is precisely the batch
`CenterLift` response, not a free interpolation.

The zero-jump statement is an exact algebraic identity, not merely a norm
bound.  Let `d=x^T-x^U` be the change of exact face center, let `h` be the
old centered state padded by zero, and let the stored velocity be supported
on `U`.  With `A=Q_UU` and `r=r_B(x)`, one has

```text
Q_TT(h-d)=[Ah;-r].
```

For `e=Q_TT^-1[0;r]`, therefore,

```text
Q_TT(h-d+e)=[Ah;0].
```

Adding `e` to both physical histories leaves their velocity unchanged.  In
the sharp discrete Lyapunov, the `||Qh||^2` term, the velocity--`Qh` cross
term, and the velocity energy are consequently identical before and after
the batch event.  This proves exact zero jump for the simultaneous repair.
It also makes the computational obstruction explicit: forming even this
single right-hand-side correction applies the enlarged inverse to the whole
positive boundary residual and is generally dense on the old face.

The singleton case itself is an unconditional no-`o(1)` theorem.  Assume
that every maximal threshold batch contains one coordinate, or more
generally that all coordinates in a batch have the same affine first-cross
parameter.  On a proposed NAG step, if the pending residual changes sign,
interpolate the two-component state to that parameter, zero-pad the batch,
and continue on the enlarged face.  Convexity of the sharp quadratic
Lyapunov gives

```text
L(Y(t))<=(1-t)L(Y)+tL(TY)<=(1-t sqrt(alpha))L(Y),
```

and the exact expansion identity adds `||r_B(Y(t))||^2/2=0`.  Hence all
complete held products have one global `O_tilde(1/sqrt(alpha))` contraction
budget; face changes never restart it.  Fractional product-bearing events
need not have a lower-bounded interpolation length, but their number is the
maximal-batch depth `O_tilde(1/sqrt(alpha))`.  Every product and boundary
scan touches at most the final exposed volume `M`, while publication goes
through the closed lower-envelope adapter.  Therefore

```text
T_singleton-cross=O_tilde(M/sqrt(alpha)).       (closed special theorem)
```

This result holds on arbitrary graphs under the chronology promise.  The
promise cannot be removed by serializing a general batch, as the family
below shows.

There is also an exact observable generalization.  Let `E_cross` be the
number of zero-residual interpolation events actually performed when a
batch is serialized.  Event jumps remain zero regardless of their timing,
so the same proof gives

```text
T_serial-cross=O_tilde(M[alpha^(-1/2)+E_cross]).
```

If every maximal batch contains at most `k` rows, then
`E_cross<=k J=O_tilde(k/sqrt(alpha))` and the work is
`O_tilde(kM/sqrt(alpha))`.  This makes small-batch serialization a valid
deterministic branch and supplies a measurable crossing-multiplicity
parameter.  It is not a graph-uniform improvement because `k` can be the
entire exposed frontier; the next construction realizes that possibility
already in the first step.

The asynchrony is present even at the standard zero initialization, and it
can have arbitrarily many distinct crossing groups inside one maximal
batch.  Let a unit-weight seed `o` have neighbors `u_1,...,u_D`; attach
`d-1` private leaves to `u_d`, so `deg(o)=D` and `deg(u_d)=d`.  Put

```text
a=(1+alpha)/2,       b=(1-alpha)/2,
rho=b/(4D^2).
```

On the seed-only normalized face, the zero-initialized first unit-gradient
step is

```text
x_o^(1)=alpha(1-rho D)/sqrt(D).
```

Along its affine interpolation, the exterior residual at `u_d` is

```text
r_d(t)=-alpha rho sqrt(d)
       +t [b/sqrt(Dd)] x_o^(1).
```

Its unique first-crossing parameter is therefore

```text
t_d=rho D d/[b(1-rho D)]
   =d/[4D(1-b/(4D))].                         (canonical async times)
```

All `t_d` lie strictly in `(0,1)` and are pairwise distinct.  At the full
endpoint their normalized positive residuals satisfy

```text
sqrt(d) r_d(1)
 =alpha[b(1-rho D)/D-rho d]
 >=alpha[b(1-rho D)/D-b/(4D)]>0.
```

Thus one sufficiently small threshold publishes all `D` rows as one
maximal batch, yet zero-jump singleton interpolation creates `D` separate
events.  This is a canonical, connected, simple-unit, actually reached
state, rather than an arbitrary Stieltjes state.  It proves that the known
maximal-batch depth theorem cannot pay serial interpolation.  It is still
not an end-to-end runtime lower bound: accepting the whole batch's
residual-square impulse is another legitimate algorithmic choice, and the
example's seed face is a high-gap scalar face rather than the unresolved
floor window.

The remaining alternative is therefore structural, not a notation check:

```text
ProjectiveBatchCrossing(tau):
  either prove that all asynchronous first crossings can be processed in
  O_tilde(1/tau) full products with no division by their absolute margins,
  or compute/persist the simultaneous batch lift in charged
  O_tilde(M/tau) total work.
```

Log determinant cannot prove the first clause because it is unchanged while
a fixed face waits.  AMPS implements the second clause only under the
explicit `R_chol,F_chol` fill-reach bound.  Hence the floor-aware inequalities
substantially narrow and correctly scale the low-frequency output, but do
**not** by themselves close deterministic general-graph work.

There is also a sharp recurrence-level reason that merely narrowing the
spectral window further cannot prove the first clause.  Fix any
`lambda<alpha+tau^2` and let `0<r_-<r_+<1` be the two real roots of
`(damped roots)` at that eigenvalue.  For arbitrary distinct integers
`t_1,...,t_N`, the scalar sequences

```text
g_i(t)=epsilon_i [r_+^t-(r_+/r_-)^(t_i) r_-^t]
```

all satisfy the *same* second-order recurrence and cross zero exactly at
their prescribed times `t_i`.  Choosing

```text
epsilon_i=2^(-i)(r_-/r_+)^(t_i)
```

keeps the two initial states, and hence every homogeneous quadratic energy
of those states, summable independently of `N` and of the largest crossing
time.  Multiplying all `epsilon_i` by a common number makes the absolute
flux arbitrarily small without changing any `t_i`.

This construction uses a diagonal direct sum of identical floor modes.  It
is therefore an **operator-level stop**, not a canonical connected-graph
lower bound: the PageRank seed, monotone publication history, and Stieltjes
coupling may forbid some of its initial states.  What it proves is exactly
what a successful argument must use.  Neither the width of
`[alpha,alpha+tau^2]`, held-step contraction, nor a quadratic energy bound
can synchronize asynchronous first crossings or bound their count.  A
proof of `ProjectiveBatchCrossing(tau)` must exploit the causal restriction
on the two histories produced by the canonical algorithm, or it must buy
the missing inverse response.

The canonical restriction can itself be stated as one minimal missing
lemma.  Let `A=Q_UU`, `C=-Q_BU>=0`, let `x^U` be the exact old-face center,
and write

```text
h=x-x^U,             g=r_B(x^U)>0,
z=c_U-Ax=-Ah.
```

Then the signed pending residual is exactly

```text
r_B(x)=g+Ch=g-CA^-1 z.                         (pending observable)
```

Thus even if a degree-mass clock is a single positive Green response, the
pending cut observes one additional inverse.  The standard inequalities

```text
C^TC<=A-A^2<=A,
L(h,v)>=(1/2)h^TA^2h>=(alpha/2)h^TAh
```

show that a frozen published gate `g_i>=theta/2` activates within

```text
O(alpha^-1/2 log(L_start/(alpha theta^2)))
```

held products.  This is the sharp conclusion of a uniform gate and held
contraction, but summing it over the known
`O_tilde(alpha^-1/2)` maximal batches gives only `O_tilde(1/alpha)`.

The single-source sign pattern explains why this per-batch multiplication
may be avoidable.  In the chronological block-Cholesky coordinates of the
final support, the first block contains the unique positive seed load;
every later block load is a distributed publication-floor term.  The
existing threshold proof bounds the floor response energy by

```text
O(theta^2/(alpha rho)).                         (floor tail)
```

Consequently the exact missing statement is narrower than an arbitrary
Stieltjes activation theorem:

```text
CanonicalSingleSourceProjectiveNoRestart(tau):
  all waiting intervals caused by the seed-driven low-band response share
  O_tilde(1/tau+tau/alpha) projective clocks in total; any remaining low-band
  response is dominated by (floor tail) and may be left in the certified
  terminal objective error.
```

At `tau=sqrt(alpha)` this is an `O_tilde(1/sqrt(alpha))` statement.  It must
also transport the seed observable across face expansions; the unmatched
profile change is the same dense `CenterLift` term.  Abstract low-frequency
Stieltjes blocks with a fresh positive load at every stage violate the
conclusion and realize `Theta(1/alpha)` waiting, but they are not canonical:
non-source raw PageRank loads are negative.  No canonical simple-unit
counterexample and no proof of the displayed no-restart lemma is currently
known.  This cleanly separates the remaining mathematical conjecture from
the already-refuted absolute-flux proof.

The numerical evidence favors, but does not prove, this canonical
no-restart statement.  The reproducible dense floating-point simulator in
`two_mask_experiments.py` maintains the lower publication mask, a delayed
signed scratch mask, persistent NAG histories, and admits a frozen batch only
when its scratch residual is nonnegative.  On a four-clique plus 128-vertex
tail, the runs

```text
alpha       events       iterations*sqrt(alpha)       maximum batch wait
1e-2          40                  13.80                         1
1e-3         118                  17.14                         1
1e-4         128                  14.83                         1
```

stay on a single root-scale clock despite a growing number of events.  A
16-layer alternating-width graph similarly stays between `15.5` and `15.7`.
An additional sweep of 1,200 random connected simple graphs with 5--44
vertices, `alpha` between `1e-4` and about `0.45`, and logarithmically varied
`rho` found maximum frozen-batch wait one under this implementation.  This
measures only the delay from an already *published* batch to scratch
admission.  It is not a bound on the held interval before the next
publication.

A later adversarial search found a canonical simple connected unit graph on
34 vertices which makes that distinction strict.  For `alpha=10^-3` and
`rho=10^-5/d_source`, ProjectedEstimateNAG publishes at

```text
[0,1,2,3,4,38].
```

Every batch is scratch-ready at publication, but the final
inter-publication gap is 34 products.  Thus “all batches wait at most one”
must not be used as evidence for one-step publication.  On the same graph at
`alpha=10^-4`, the event times are `[0,1,2,3,43,44]`; the longest gap times
`sqrt(alpha)` is `0.40`, versus `1.075` at `10^-3`.

The `alpha=10^-3` trace is no longer merely numerical evidence.
`exact_delayed_clock.py` conjugates `x=D^(1/2)y` and evaluates the entire
recurrence in `Q(sqrt(10))`, including the common retraction, both lattice
projections, the historical lower maximum, and every publication sign.  It
certifies the exact batches at products `0,1,2,3,4,38`; all 33 intervening
scans have nonpositive exterior residual, with largest value `-2e-8`, and
the minimum residual in the final batch is about `7.555e-5`.  Hence this is
a strict counterexample to the immediate-publication lemma for the named
recurrence.  The verifier additionally proves that the graph is simple and
connected with 69 edges, `rho vol(V)=0.00138`, every published vector remains
an active lower subsolution, and no quiet scan can trigger the manuscript's
active-residual early stop: the smallest squared norm/tolerance ratio is
`4.09312681762e11`.  Exact rational elimination gives a strictly positive
full solution, hence `S*=V`; the delay is not an artifact of an irrelevant
vertex outside the target support.  It is still not a lower bound for the
target runtime or for other algorithms.  The `alpha=10^-4` trace and the
bounded-root-gap pattern remain floating-point evidence only.  The graph is
a permanent numerical regression in `delayed_publication_graph` and an exact
regression in `exact_delayed_clock.py`.

The simulator also reveals a simpler sufficient invariant.  In every
reported run, the historical lower envelope obeyed `ell<=x` at each
publication scan.  Since `C_B>=0`, this immediately gives

```text
r_B(x)=r_B(ell)+C_B(x-ell)>=r_B(ell)>0.
```

More generally only the projected dominance
`C_B(x-ell)>=0` is needed.  Under this invariant no certified batch has a
held *post-publication* waiting interval: it can enter the scratch mask in
the scan which publishes it.  It says nothing about products spent before
the lower envelope makes the next publication; the 34-vertex witness has
the invariant and still has a 34-product inter-publication gap.  Thus

```text
ScratchDominance: C_B(x-ell)>=0 at every publication
```

closes scratch admission but is not an alternative closure of
`CanonicalSingleSourceProjectiveNoRestart`.  A separate publication-dwell
clock is still necessary.

It cannot be enforced for free by replacing both histories with their join
with `ell`.  A bounded three-coordinate counterexample already exists on the
simple unit path `P_3`.  With

```text
alpha=1.6402418651905565e-5,
x^* =(0.57714942, 0.71292356, 0.59825843),
ell =(0.09098101, 0.02539009, 0.11210235),
x   =(0.04021504, 0.12062264, 0.62105751),
```

and `Q=((1+alpha)/2)I-((1-alpha)/2)D^-1/2 A D^-1/2`, one has

```text
min Q(x^*-ell) = 6.22e-6 >0,
```

so `ell` is a strict lower subsolution.  Put `x'=x join ell` and take zero
velocity.  Direct evaluation gives

```text
(1/2)||Q(x-x^*)||^2 +(alpha/2)||x-x^*||_Q^2 =0.03266476,
(1/2)||Q(x'-x^*)||^2+(alpha/2)||x'-x^*||_Q^2=0.03370166.
```

The accelerated Lyapunov rises by about `3.17%`, even though the ordinary
`Q`-energy falls.  The obstruction is the positive distance-two coupling in
`Q^2`; Stieltjes truncation does not extend to the operator-squared term.
This is a state-level PageRank counterexample, not a claim that the state is
reached by canonical zero initialization.  It proves that a dominance repair
must be charged or dynamically derived; a generic lattice projection cannot
establish the missing invariant.

There is, however, a different estimate-sequence state in which dominance
*can* be enforced without increasing the held-face potential.  Put

```text
a=(1-sqrt(alpha))/sqrt(alpha),
Phi_U(h,v)=(1/2)h^TQ_Uh+(alpha/2)||h+a v||_2^2.
```

This is the standard unweighted NAG quadratic and it contracts by
`1-sqrt(alpha)` on a held face.  Store the primal physical state
`x=x^U+h` and the auxiliary physical state
`w=x^U+h+a v`.  Given a lower subsolution `ell<=x^U`, replace them by

```text
x' =x join ell,          w'=w join ell,
h'=x'-x^U,               z'=w'-x^U,
v'=(z'-h')/a.                                      (dual dominance projection)
```

This projection never raises `Phi_U`.  To see it, let
`k=x^U-ell>=0`, so `Q_Uk>=0`, and put `q=h+k=x-ell`.  Then

```text
h'=q_+-k.
```

The Markov property of a grounded graph form gives
`q_+^TQ_Uq_+<=q^TQ_Uq`, while
`q_+-q=(-q)_+>=0` and `Q_Uk>=0`.  Hence

```text
(h')^TQ_Uh'<=h^TQ_Uh.
```

For the auxiliary term, `z=h+a v` is replaced coordinatewise by
`z'=max(z,-k)` with `-k<=0`, so `||z'||_2<=||z||_2`.  This proves the
claim.  In particular the projected primal always dominates `ell`, and
every batch published from `ell` is scratch-ready immediately.

The price appears at face expansion, but it has an exact cumulative bound.
For `T=U union B`, let `d=x^T-x^U>=0`; zero extension changes both centered
states from `h,z` to `h-d,z-d`.  Old-face orthogonality gives

```text
Delta Phi
 =(1/2)||d||_Q^2 +(alpha/2)||d||_2^2-alpha z^Td.
```

Let `G_U=F(x^U)-F(x^*)`, so
`G_U-G_T=||d||_Q^2/2`.  Since the auxiliary projection guarantees
`z>=-k`, and `Q>=alpha I`, the combined potential satisfies

```text
Delta(Phi+2G)
 <=alpha k^T d.                                     (projected event debt)
```

Across the nested exact centers, `k=x^U-ell<=x^U` and

```text
sum_U (x^U)^T d
 <=(1/2)||x^*||_2^2.
```

The canonical solution is coordinatewise dominated by the ordinary
point-source PageRank response
`p=alpha Q^-1 e_v/sqrt(d_v)`, whose Euclidean norm is at most
`1/sqrt(d_v)<=1`.  Consequently

```text
sum_events [Delta(Phi+2G)]_+ <=alpha/2.             (total event bank)
```

This closes projection safety, immediate scratch admission, and the total
expansion debt for a new **ProjectedEstimateNAG** candidate.  It still does
not by itself bound elapsed products: a contraction with additive impulses
of bounded total mass can receive those impulses at widely separated late
times.  To finish, one must prove that canonical publications cannot realize
such adversarial timing--equivalently, a projective dwell/no-restart lemma
for the lower-envelope update.  The candidate replaces the pending-output
observability problem by this narrower event-timing statement; it does not
silently claim that a total additive bank is a clock bound.

The new candidate is implemented separately in
`run_projected_estimate_nag`.  Dense exact centers are used only to audit the
proved inequalities, never by the recurrence.  On the four-clique plus
128-vertex tail it gives

```text
alpha       events       iterations*sqrt(alpha)
1e-2          40                  13.40
1e-3         118                  17.11
1e-4         128                  14.72
```

Every batch was scratch-ready at publication.  On 300 additional random
connected graphs with the earlier parameter ranges, all runs terminated,
the largest scaled iteration count was `20.54`, the largest measured
projection-potential ratio was `1+1.3e-10`, and every audited event satisfied
the projected event-debt inequality.  These are regression checks, not an
output-local theorem: the code scans dense ambient rows and the missing
projective dwell/square-function statement is a worst-case timing claim.

There is now a sharper fixed-face result for that clock.  On one held face,
restrict a homogeneous packet to the bottom band
`spectrum(A) subset [alpha,C alpha]` and write its NAG extrapolate as

```text
q_t=f_t(A)h_0+g_t(A)(sqrt(alpha) z_0).
```

The two fundamental multipliers have uniformly bounded total variation:

```text
sum_t sup_lambda |Delta f_t(lambda)|=O_C(1),
sum_t sup_lambda sqrt(lambda)|Delta g_t(lambda)|=O_C(1).
```

Together with `C_ext^T C_ext<=A-A^2<=A`, this proves that arbitrary
disjoint future row sets, inspected at arbitrary stopping times, share one
bottom-packet bank,

```text
sum_t ||C_(B_t)q_t||_2^2
 <=O_C(||h_0||_A^2+alpha||z_0||_2^2).          (fixed-face stopped bank)
```

Thus a fixed slow packet does **not** pay a fresh root burn-in per future
row.  Under nested faces the same conclusion remains true even with rotating
eigenspaces as long as the physical two-history state stays quantitatively
bottom.  Zero extension can violate that condition only through the new cut
output

```text
||Q_T E h||_2^2=||Q_Uh||_2^2+||(-Q_BU)h||_2^2.
```

The physical-position contributions have the global canonical bank
`sum_events||(-Q_BU)h||^2=O(alpha)`.  The companion velocity cut output can
also be closed, without a spectral split, by changing its metric.  Write

```text
Q=aI-cS,   a=(1+alpha)/2,   c=(1-alpha)/2,   S>=0,
F0=acI-c^2S^2=(1+alpha)Q-Q^2-alpha a I,
J_Q(h,w)=h^TQh+||w||^2+w^TF0w,
w=sqrt(alpha)(z-x^U).
```

At a `Q`-eigenvalue `lambda`, `F0` has eigenvalue
`f0(lambda)=ac-(a-lambda)^2`.  Hence `0<F0<=Q`.  An exact scalar
Sylvester calculation for the estimate-state update

```text
M_lambda=(1/(1+sqrt(alpha)))
 [[1-lambda,     1-lambda],
  [alpha-lambda,1-lambda]]
```

gives

```text
M_lambda^T diag(lambda,1+f0(lambda)) M_lambda
 <=(1-sqrt(alpha))diag(lambda,1+f0(lambda))       (held F0 LMI)
```

throughout `lambda in [alpha,1]`.  This was checked symbolically, not only
on a grid: after substituting
`lambda=alpha+(1-alpha)y`, all Bernstein coefficients of the two diagonal
minors and determinant are nonnegative on `(sqrt(alpha),y) in [0,1]^2`.
The exact reproduction is `f0_lmi_exact.py` in this directory.

The metric is compatible with the actual lattice projection.  Both `Q` and
`I+F0` are Stieltjes, and for every lower subsolution `ell`, with
`e=x^U-ell`,

```text
(I+F0)Q^-1
 =(1-alpha a)Q^-1+(1+alpha)I-Q >=0 entrywise.
```

Thus `(I+F0)e>=0`; the Stieltjes lower-box lemma shows that projecting the
physical auxiliary point `z` to `z join ell` cannot increase its
`I+F0` distance from `x^U`.  The ordinary Markov truncation gives the same
statement for the `Q` part of `h`.  This repairs exactly the failure of the
earlier `Q-Q^2` potential: the removed `alpha cS` term was the
sign-indefinite lattice obstruction.

The face-growth identity is equally sharp.  Let `T=U dotunion B`,
`C=-Q_BU=cS_BU`, `d=x^T-E x^U`, and `Q_Td=E_Bg`.  Zero extension gives

```text
(Ew)^T F0_T(Ew)=w^T F0_Uw-||Cw||^2,
d^T F0_T Ew=g^TCw-alpha a d^TEw.
```

Recentring `h'=Eh-d`, `w'=Ew-sqrt(alpha)d` therefore yields the exact
event formula

```text
Delta J
 =||d||_Q^2
  -2alpha(1-alpha a)(z-x^U)^Td+alpha||d||^2
  -||Cw||^2-2sqrt(alpha)g^TCw+alpha d^TF0_Td.
```

Since the projected estimate point has `z>=ell`, `d>=0`, and `F0<=Q`,
Young's inequality implies

```text
Delta J
 <=-(1/2)||Cw||^2
   +(2+alpha)||d||_Q^2
   +2alpha e^Td+2alpha||g||^2.
```

The three positive terms have the already closed center, projected-event,
and gate telescopes, each `O(alpha)`.  Held contraction, lattice Fejer
monotonicity, and the exact cut drop consequently prove

```text
sum_events ||Cw||^2=O(J_initial+alpha).
```

Together with the physical-position bank and
`q=(h+w)/(1+sqrt(alpha))`, this gives the full signed stopped-event bank

```text
sum_events ||Cq||^2=O(J_initial+alpha).       (full-spectrum cut bank)
```

This is stronger than the earlier proposed two-band/`RootForceBank`
reduction and removes its remaining velocity offspring.  It is important
not to call it the complete `PublicationSharedClock`.  A square-summable
sequence of event outputs can still consist of many small pulses separated
by root-length held intervals.  What remains is a chronology/occupancy
lemma assigning every such long interval, without reuse, either to a
threshold-sized portion of this bank or to a serial killed-walk chamber
whose attenuation/volume is spent once.  Thus the discrete algebraic
shock bank is now closed; the general-graph product-count bridge is not.

#### Exact fixed-face square functions and the quarter-scale response

The fixed-face chronology can be sharpened beyond the event bank.  Put
`s=sqrt(alpha)` and, on one held face `A`, use companion coordinates

```text
q_t=(h_t+w_t)/(1+s),
[h_(t+1);w_(t+1)]
 =(1/(1+s))[[I-A,I-A],[alpha I-A,I-A]][h_t;w_t].
```

For a fixed exterior coupling `C`, the floor-aware inequality

```text
C^TC<=(A-alpha I)(I-A)
```

and the exact scalar observability Gramians give

```text
sum_(t>=0)||Cq_t||^2
 <=J_0/(2sqrt(alpha)),                            (fixed-cut square function)

sum_(t>=0)||q_(t+1)-q_t||_A^2
 <=6J_0.                                         (full quadratic variation)
```

Here `J_0=h_0^TAh_0+||w_0||^2+w_0^TF0(A)w_0`.  These are exact proved
inequalities, not grid observations.  Solving the scalar Lyapunov equations,
substituting `lambda=s^2+(1-s^2)y`, and converting the cleared numerators to
the tensor Bernstein basis gives nonnegative coefficients for both diagonal
bounds.  The first `1/s` factor is sharp up to a constant on simple connected
unit graphs: a nearly regular core with ten private leaves realizes a mode
`lambda=(6+o(1))alpha` and a proportional cut square.

The second estimate does not splice through face growth using only `F0`.
The exact Gramian for *remaining* quadratic variation has an `h-h` entry
whose partial fractions include the hard resolvent

```text
R_U=[2s I+(1-s)Q_U]^-1
    =(1/(1-s))[Q_U+2s/(1-s) I]^-1.               (hard variation response)
```

For `T=U dotunion B`, writing

```text
Abar=2sI+(1-s)Q_U,       Cbar=(1-s)(-Q_BU),
Sigmabar=Dbar-Cbar Abar^-1 Cbar^T,
```

block inversion gives the positive domain-growth lift

```text
(R_T)_UU-R_U
 =Abar^-1 Cbar^T Sigmabar^-1 Cbar Abar^-1.        (remaining-variation lift)
```

It can be invisible to the current zero-order `Cq/Cw/F0` cut bank.  On the
simple unit path `P_3`, take `U={1,2}`, add `B={3}`, and choose `h=e_1,w=0`.
The cut row is supported only at vertex 2, so

```text
Ch=Cw=Cq=0,
```

while irreducibility of `Abar` makes

```text
h^T[(R_T)_UU-R_U]h>0.
```

The uniformly conditioned second resolvent in the same Gramian has a
strictly positive lift as well.  Hence the exact remaining-variation
potential jumps although the current `F0` event outputs vanish.  No finite
constant can prove

```text
Delta(remaining variation)<=K||Cq||^2
```

on all principal expansions.  This is a strict matrix witness, not a loose
norm loss.  It explains why replacing the rational Gramian by the local
upper bound `6J` and restarting it per face reuses an old packet.

Writing one non-restarted recurrence relative to the fixed final solution
does not remove this future-propagator debt.  If `P_t` is the active mask and
`e_t=x_t-x*`, the raw masked recurrence is exactly

```text
e_(t+1)=P_t(I-Q)[(1+beta)e_t-beta e_(t-1)]-(I-P_t)x*.
```

It has no instantaneous stored-state jump when the mask grows, but the
inactive forcing `-Q_UO x_O^*` is not threshold-bounded.  On the canonical
unit edge, one may have an exactly quiet published exterior residual while
the active-row inactive forcing tends to `1/8` as `alpha->0`.

There is also a canonical event version of the future-propagator stop.  On
unit `P3`, set `U={1,2}`, add vertex 3, and choose
`rho=rho_0-epsilon`, where
`rho_0=(1-alpha)^2/[4(1+alpha)]`.  The new row is genuinely positive, but its
exact center-increment energy is

```text
4alpha(1+alpha)epsilon^2/(alpha^2+6alpha+1) ->0.
```

For the legal lattice state `h=kappa e_1,w=0`, every instantaneous
`Ch,Cw,Cq` term vanishes, whereas the shifted-resolvent old-block lift is a
fixed positive multiple of `kappa^2`.  Hence no uniform inequality can pay
the exact future tail by the local cut squares plus center-increment energy.
The state satisfies the publication and lattice invariants, but its
reachability from the prescribed zero initialization at that exact event is
not proved.  This is a proof-template obstruction, not a canonical runtime
lower bound.  The missing statement is precisely a stopped
`MaskedDuhamelOccupancy`/persistent shifted-response assignment.  The exact
`P2/P3` identities are included in `moving_face_smoothing_exact.py`.

The obstruction also reveals a concrete intermediate scale.  The shift in
the hard response is `Theta(s)=Theta(sqrt(alpha))`.  Its condition number is
`Theta(1/s)`, so deterministic Chebyshev applies it in

```text
O_tilde(1/sqrt(s))=O_tilde(alpha^-1/4)
```

products for fixed relative accuracy.  On a path its Green kernel has
correlation length `Theta(alpha^-1/4)`; on a general graph the corresponding
walk-metric truncation radius is `O_tilde(alpha^-1/4)`, but the volume of that
ball need not be local or output-sensitive.  At the critical cutoff the desired
root time `alpha^-1/2` is therefore the product of two quarter scales: at
most `alpha^-1/4` significant response epochs, each costing
`M alpha^-1/4`, would meet the target.

The hard pencil is itself exactly another PageRank operator.  Normalizing
`K=2sI+(1-s)Q` by `1+s` gives

```text
K/(1+s)=((1+mu_hard)/2)I-((1-mu_hard)/2)S,
mu_hard=s(2-s)=Theta(s).
```

Hence one fixed nonnegative shifted load has threshold depth and Chebyshev
degree `O_tilde(alpha^-1/4)`.  The word *fixed* is essential.  On a unit
path, inject `N=Theta(1/s)` fresh positive coordinate loads of amplitude
`eta=s^(3/2)`.  Their total square mass is
`N eta^2=Theta(s^2)=Theta(alpha)`, while every load exceeds the largest
global error-compatible threshold `Theta(s^2)`.  Thus the square banks allow
`Theta(alpha^-1/2)` individually significant fresh loads; shifted depth
proves a memory length, not an `alpha^-1/4` epoch count.  This sequence is a
strict arbitrary-load obstruction, not by itself a canonical point-source
chronology.

Even a genuine point source does not yield a universal positive Green
bracket for the raw accelerated state.  At `alpha=1/16384`, critical
zero-start NAG on an explicit 20,478-vertex finite simple unit tree has, at
time 29 and distance seven,

```text
x_29(u)=-0.004090196485...<0,
(Q^-1 e_v)_u>14alpha,       |x_29(u)|>67alpha.
```

Therefore neither `0<=x_t<=2Q^-1e_v` nor
`|Q^-1e_v-x_t|<=Q^-1e_v` holds entrywise.  The failed bracket would have
made every positive hard lift telescope into the monotone source reservoir

```text
Rsrc_U=e_v^TQ_U^-1 K_U^-1 Q_U^-1e_v,
```

and would thereby have supplied the desired monotone payment.

This is not a below-threshold artifact.  On the same finite tree choose the
literal canonical parameters `rho=epsilon_obj=10^-30`.  Then

```text
vartheta=9.765625e-34,       rho vol(S*)=4.0954e-26,
x_rho^*(u)>3.2e-8,           |x_29(c_rho)_u|>1.4e-7,
S*=V.
```

The last claim follows from a shortest-walk lower bound at every vertex, all
of which lie within distance 18 of the source.  Thus threshold significance
and the support-volume contract do not repair the raw pointwise bracket.

In fact no universal pointwise constant survives on arbitrary principal
faces contained in a valid support.  At the singular limit of the critical
inverse polynomial, evaluation at `z=i` shows that its positive and negative
spatial coefficients both grow exponentially.  Fixing one such coefficient,
then taking a sufficiently high-degree regular tree isolates it at the
corresponding distance, while the exact Green entry stays asymptotic to a
constant times `d^-r`.  Continuity moves the example to some `alpha>0`; a
finite causal ellipsoid plus one degree-completing shell realizes it as a
simple unit graph.  Finally choosing `rho` and `epsilon_obj` sufficiently
small gives `S*=V`, `rho vol(S*)<=1`, and keeps both compared coordinates
above `vartheta`.  Thus for every fixed `C` there are threshold-significant
principal-face examples with either a negative coordinate or positive
overshoot beyond `C Q_U^-1f`.  The construction does not prove that this face
and time occur in the exact canonical threshold chronology.

That domination is false directly as well.  A 39-vertex simple unit
tree has an exact principal expansion for which the time-13 hard lift is
`1.126299...` times the complete source-reservoir increment.  More strongly,
high-private-degree path families make

```text
sup h_t^T[(K_T^-1)_UU-K_U^-1]h_t
    /(Rsrc_T-Rsrc_U)=infinity.
```

More quantitatively, at fixed `alpha=.01` the exterior-pole calculation gives

```text
rho kappa=101(10+sqrt(19))/1309=1.107905877...,
hard lift / reservoir increment
 =Omega((rho kappa)^(2t)/t)
 =Omega(1.22745543^t/t).
```

The unbounded ratio is realized by finite graphs after taking a finite
private degree.  It also rules out a proof bank containing only past/current
raw cut squares on the same future row: those squares grow only linearly in
`t` while the hard response above grows exponentially relative to the static
endpoint scale.  It refutes unrestricted raw-state/source-reservoir payment,
not a stopped low-band theorem with explicit threshold/floor debt,
future-tail reservation, or attenuation; the leaf expansion need not occur
at that time in the canonical maximal-batch trace.  Exact finite checks are
in `green_bracket_exact.py` and `green_lift_exact.py`.

Projection removes that negative coordinate but still does not give an
upper Green bracket.  With `alpha=10^-6`, exact coordinatewise-projected NAG
on a 6,142-coordinate principal face of a finite 12,286-vertex simple unit
tree has

```text
x_39(u)=4.989725986...e-5,
(Q_U^-1e_v)_u=1.877487188...e-6,
x_39(u)/(Q_U^-1e_v)_u=26.576618025... .
```

For canonical `rho=epsilon_obj=10^-30`, both the projected coordinate and
exact face solution exceed `vartheta=1.25e-34` by more than twenty orders of
magnitude, `rho vol(S*)=2.457e-26`, and a global shortest-walk certificate
again gives `S*=V`.  Hence clipping alone cannot prove
`x_t<=C Q_U^-1f` even with `C=20` on significant coordinates.  This is a
fixed principal-face/time counterexample.  It does not show that the same
face and state occur in the canonical maximal-batch chronology, nor does it
refute a stopped low-frequency bracket augmented by an `F_mu` debt.  The
exact reproduction is `projected_green_overshoot_exact.py`.

This factorization extends to a free cutoff through the shifted-obstacle
construction and recovers the requested balance algebra exactly.  Normalize
one `tau^2`-shifted prox operator; its spectral floor and critical root are

```text
s_tau=sqrt(alpha+tau^2)=Theta(tau),   tau>=sqrt(alpha),
r_tau=Theta(1/sqrt(tau)),
```

up to harmless `1+tau^2` rescaling.  One prox needs `O_tilde(1/tau)` held
products, hence `O_tilde(1/sqrt(tau))` response windows of length/radius
`r_tau`.  The outer resolvent contraction needs
`O_tilde(1+tau^2/alpha)` prox calls.  Therefore

```text
N_epoch=O_tilde((1+tau^2/alpha)/sqrt(tau))
       =O_tilde(tau^(3/2)/alpha),
cost per shifted response=O_tilde(M/sqrt(tau)),
total response
 =O_tilde(M/tau+M tau/alpha).
```

Equivalently, multiplying the total slow duration `Theta(tau/alpha)` by
the reciprocal window length and by the response cost gives the second
term `M tau/alpha`; the initial prox gives the first `M/tau` term.  Thus a
two-level shifted-response implementation would give

```text
O_tilde(M/tau+M tau/alpha).                      (quarter-scale epoch balance)
```

There is an equivalent exact fixed-face preconditioner calculation.  Put

```text
A_sigma=(Q+tau^2 I)/(1+tau^2),
s_tau=sqrt((alpha+tau^2)/(1+tau^2)),
gamma_tau=tau^2+2s_tau(1+tau^2)/(1-s_tau)=Theta(tau).
```

Using `P=Q+gamma_tau I` to precondition `H=Q+tau^2 I` gives
`kappa(P)=Theta(1/tau)` and `kappa(P^-1 H)=Theta(1/tau)`.  Thus a supplied
fixed face needs `O_tilde(tau^-1/2)` preconditioned iterations, each using a
`P` solve of `O_tilde(M tau^-1/2)` work, for `O_tilde(M/tau)` total.  The
proximal contraction count then gives the displayed balance without any
informal window argument.

This fixed-face/ideal-clock arithmetic is proved; the moving-face epoch
count is conditional.  Dividing an ideal shared running time by a response
length does not itself prove that face growth avoids restart.  Define the
remaining producer precisely as follows.

```text
QuarterScaleResponseEpoch(tau):
  persist the shifted harmonic state
    [Q_U+gamma_tau I]^-1
  through every safe face event in a window of radius
    O_tilde(tau^-1/2);
  perform no recursive off-support work beyond immediate quiet-KKT
    boundary inspection charged to the final output volume;
  charge all overlapping response balls so that only
    O_tilde(tau^(3/2)/alpha) significant epochs occur;
  spend O_tilde(vol(U_epoch)/sqrt(tau)) per epoch.
```

For one fixed zero-extended packet `b`, the PSD domain increments of the
shifted inverse do telescope:

```text
sum_j b^T(R_(j+1)-R_j)b
 =b^T(R_final-R_initial)b<=||b||^2/gamma_tau.
```

The missing case is a changing signed packet: NAG evolution, recentering,
and new batch sources introduce noncommuting directions, so the displayed
fixed-packet identity cannot be summed directly.

The `P_3` witness proves that the current zero-order `Cq/Cw/F0` cut bank does
not implement this producer.  It does not rule out a higher-order or delayed
statistic: on `P_3`, `CQh` is nonzero.  A length-`L` path gives the properly
scoped extension, since `CQ^k h=0` for every `k<L-1` while the resolvent lift
is positive; `L=Theta(tau^-1/2)` is path-sharp.  Precomputing an ordinary
graph-radius ball is also unsafe.  In the canonical seed--hub--`N`-leaf tree,
take `rho=2/(N+1)`.  The exact obstacle support is just the degree-one seed:
after solving that singleton, the hub residual times `sqrt(N+1)/alpha` is

```text
-2+(c/a)(1-2/(N+1))<0,
```

and every leaf residual is `-alpha rho`.  Hence `M=1`, whereas traversing the
ordinary radius-two ball touches `N+1` edges.  What is needed is an output-sensitive
shifted-response ball or an equivalent stopped-time/Agmon packing with no
reuse.  At `tau=sqrt(alpha)` this is exactly the proposed
`alpha^-1/4`-by-`alpha^-1/4` route.  It is a sharper formulation of
`CenterLift/FreshBottomLaminarization`, not yet an unconditional algorithm.
Moreover, the naive tuned `F0` metric is refuted below, so a full proof must
either transport the rational Gramian itself or supply a new
lattice-compatible multi-step potential.

The accounting can be consolidated further into one monotone reservoir.
Let

```text
G_U=(1/2)||x^*-x^U||_Q^2,
c_G=2(2+3alpha),
e=x^U-ell,
Omega=J_Q(h,w)+c_G G_U
      +alpha(||x^*||^2-||e||^2)+alpha||x^*-ell||^2.
```

Every term is nonnegative because `0<=e<=x^*`.  At an event,
`e^+=Ee+d`, the two static Euclidean terms contribute
`-2alpha e^Td-alpha||d||^2`, and `G` drops by
`||d||_Q^2/2`.  With `||g||^2<=||d||_Q^2`, the preceding event inequality
then gives

```text
Delta_event Omega
 <=-(1/2)||Cw||^2-alpha||d||^2.
```

At a publication `ell^+=ell+p`, the two static Euclidean changes sum to
`-2alpha(x^*-x^U)^Tp<=0`, while the accompanying lattice lifts are Fejer
for `J_Q`.  On a held product the static terms do not change and the full-
spectrum LMI gives

```text
Omega_t-Omega_(t+1)>=sqrt(alpha) J_Q(h_t,w_t).
```

The apparently extraneous constant can be removed.  The dynamic reservoir

```text
Omega_dyn=Omega-alpha||x^*||^2
 =J_Q+c_GG_U
  +alpha(||x^*-ell||^2-||x^U-ell||^2)
```

is still nonnegative, since `x^*>=x^U>=ell` coordinatewise, and it has
exactly the same event, publication, and held differences.  Unlike `Omega`,
it vanishes at the final exact state.  The canonical initialization has
`Omega_dyn,0=O(alpha)`.  Thus expansions do
not restart an energy clock even implicitly: held steps, admissions, and
publications all draw from one reservoir.  This still yields only an
additive estimate `sum_t J_t=O(sqrt(alpha))`.  Since `J_Q` can be arbitrarily
small compared with the unexposed future-face part of `Omega_dyn`, additive
dissipation alone permits a sequence of decreasing pulses separated by
fresh root-length intervals.  A completed clock theorem must use the
single-source/threshold chronology to rule out or spatially charge precisely
that sequence; no further quadratic-event potential is missing.

There is a tempting relative strengthening of this reservoir, and it has an
exact sharp obstruction.  Partition the final support into the current face
and its future part,

```text
Q=[[A,-C^T],[-C,D]],       S=D-CA^-1C^T.
```

Let `ell` be the current lower publication, `e=x^U-ell`, and let
`b=f_O+C ell` be its unopened residual.  If `x_O` is the future block of the
final solution, then

```text
g=b+Ce=Sx_O,       G=(1/2)x_O^TSx_O.
```

It is false that the cross drift can be bounded by a constant multiple of
`e^TAe`.  A strict canonical witness is the two-vertex unit edge.  Put

```text
a=(1+alpha)/2, c=(1-alpha)/2,
Q=[[a,-c],[-c,a]],  source=1,  rho=c/2,
U={1},   ell=alpha/2.
```

The canonical load is `f=(alpha(1-rho),-alpha rho)`.  The one-face center,
future Schur complement, and exact future coordinate are

```text
x^U=alpha(1-rho)/a,
e=x^U-ell=alpha/(2a),
b=-alpha rho+c ell=0,
S=a-c^2/a=alpha/a,
x_O=c-rho=c/2.
```

Both final coordinates are positive, and `ell` is a valid nonnegative face
subsolution.  It is not an artificial unreachable checkpoint: on the
seed-only face, the first unit-gradient step goes from `0` to
`f_1=alpha(1-rho)`, and `ell` is its affine point at
`t=1/[2(1-rho)]`; the exterior residual is exactly zero there.
Nevertheless

```text
G=(1/2)Sx_O^2=alpha c^2/(8a),
e^TAe=alpha^2/(4a),
G/(e^TAe)=c^2/(2alpha)=Theta(1/alpha).       (relative-drift witness)
```

Thus neither the extra Euclidean terms in the constant-free `Omega_dyn` nor an unweighted
`G<=O(e^TAe)` argument produces relative contraction.  This witness does
not refute spectral rent-or-buy: its current face has eigenvalue `a>=1/2`,
so the gate drift is a fast constant-time mode despite the large energy
amplification.

The correct general replacement exposes exactly that spectral distinction.
Since `Q>=alpha I`, its Schur complement satisfies `S>=alpha I`.  Also the
PageRank floor-aware coupling inequality gives

```text
C^TC<=(A-alpha I)(I-A).
```

Because `e,C>=0` and only the positive part of `b` can increase `g`,

```text
G <=(1/(2alpha))||b_++Ce||^2
  <=(1/alpha)||b_+||^2
    +(1/alpha)e^T(A-alpha I)(I-A)e.          (relative spectral drift)
```

If every unopened normalized residual is at most `theta`, the first term is
at most the usual `theta^2/(alpha rho)` floor.  Splitting at
`A-alpha I=tau^2` shows why the two-vertex amplification is harmless: its
error lies in the fast part, while on the floor window the amplification is
bounded by `tau^2/alpha`.  More explicitly, up to a harmless factor two for
the two projected pieces,

```text
G <=theta^2/(alpha rho)
   +(tau^2/alpha)||P_lo e||^2
   +(1/alpha)e_hi^T(A-alpha I)(I-A)e_hi.
```

The high term is compatible with the already proved `M/tau` accelerated
branch.  The low term is precisely where a scale-relative clock is still
needed: an absolute energy bound on `P_lo e` cannot count amplitude-
independent crossing latency.  Thus rent-or-buy repairs the canonical
two-point counterexample, but the general proof still requires
`RelativeFloorClock(tau)`, assigning the low-window drift without a
`1/theta` division.  This is a sharper missing lemma, not an assertion that
the full balance has now been proved.

There is also a fully local landscape parameter for the low window.  It is
more directly observable than the generic inverse landscape because the
global stationary vector is known.  Put `s_i=sqrt(d_i)` and, for a current face
`U`,

```text
V_U(i)=(Q_Us_U)_i/s_i
      =alpha+c d_out,U(i)/d_i,
c=(1-alpha)/2.
```

For every vector `f` supported on `U`, direct edge expansion gives the exact
ground-state identity

```text
f^TQ_Uf
 =sum_(i in U) V_U(i) f_i^2
  +c sum_({i,j} in E(U))
       (f_i/sqrt(d_i)-f_j/sqrt(d_j))^2.       (local landscape)
```

Thus no solve or eigenvector is needed to evaluate the potential.  If
`L_U(Lambda)` is the spectral subspace below `Lambda`, define

```text
H_U(K,Lambda)={i: V_U(i)<=K Lambda},       K>1.
```

For every `f in L_U(Lambda)`,

```text
||f_(U\H)||^2 <=(1/K)||f||^2.              (well localization)
```

Restriction to `H` is consequently injective on the low subspace.  For any
orthonormal low family `phi_1,...,phi_r`,

```text
(1-1/K)r
 <=sum_m ||(phi_m)_H||^2<=|H|,
```

so independent fresh low directions buy well vertices with no degree or
port-rank loss.  At the desired cutoff `Lambda=alpha+tau^2`, every well
vertex has

```text
d_out,U(i)/d_i=O_K(alpha+tau^2),
```

while the complementary principal region has gap at least `K Lambda` by
the same identity and is a valid `O(1/tau)` Chebyshev region.

This landscape is monotone under face growth: `d_out,U(i)` only decreases,
so `H_U(K,Lambda)` only expands, and its connected components grow and
merge but never split.  The raw degree volume of vertices entering the well
is therefore at most `M`.  This supplies a concrete, observable candidate
for the coefficient `B` in

```text
O_tilde(M/tau+B_land(tau) tau/alpha).
```

The structural merge forest is itself executable in `O_tilde(M)` total
work for every fixed cutoff.  Maintain `d_out,U(i)` counters on exposed
vertices; an edge changes exactly once from exterior to internal when its
second endpoint is admitted.  When a vertex first satisfies
`V_U(i)<=K Lambda`, insert it into a union-find structure and join its
already-well neighbors.  Every vertex enters once, every incident row is
scanned only a constant number of times, and components only merge.  Thus
there is no randomized expander-decomposition or eigenvalue-oracle cost
hidden in locating these coarse wells.

The formula is an end-to-end theorem only if a persistent component-frame
implementation processes each well entry/merge without replay, so that
`B_land=O_tilde(M)`.  The landscape theorem itself does not provide that
implementation.  A sharp low eigenvector can be a symmetric superposition
over many disconnected wells, and when wells merge their condensed Schur
operator can rotate densely.  The `F0` cut bank pays the rotation energy,
but a Bessel-stable multi-component frame transport (or smooth-filter/IMS
replacement) is still needed to count chronology and materialization work.
Thus `V_U` turns “the explored eigenvalue might be larger” into a precise
local rent-or-buy parameter, while retaining the exact `NestedExpanderLift`
obstruction rather than hiding it in an eigenvalue oracle.

In oracle form the resulting balance is completely concrete.  Define
`LandscapeSchurClosure(tau)` to maintain the monotone well components and
their condensed interface so that

1. all complement filtering/elimination over the run costs
   `O_tilde(A_fast/tau)`; and
2. all low-well Schur products, first-crossing reports, and merge-frame
   transports over one unit of slow time cost `O_tilde(B_land)`, with no
   rereading of a component at every descendant face.

The high complement has certified gap `Omega(alpha+tau^2)`, while the
remaining tuned floor clock has length `O_tilde(tau/alpha)`.  Therefore

```text
T_land(tau)
 =O_tilde(A_fast/tau+B_land tau/alpha).       (conditional landscape balance)
```

For certified `A_fast,B_land` independent of the chosen cutoff over its
admissible range, the optimizer is

```text
tau_*=sqrt(A_fast alpha/B_land),
T_land(tau_*)=O_tilde(2sqrt(A_fast B_land/alpha)),
```

clipped to `sqrt(alpha)<=tau<=1`.  Explicitly, for any nonnegative `A,B`,

```text
min_(sqrt(alpha)<=tau<=1) {A/tau+B tau/alpha}
 = (A+B)/sqrt(alpha),             A<=B,
 = 2sqrt(AB/alpha),               B<=A<=B/alpha,
 = A+B/alpha,                     A>=B/alpha.
```

This piecewise form matters when the two charged ledgers are not both `M`:
blindly quoting the stationary point can select an inadmissible cutoff.  With a no-replay closure,
`A_fast,B_land=O_tilde(M)` and the target `O_tilde(M/sqrt(alpha))` follows.
The first clause is ordinary deterministic Chebyshev on a certified fast
region; the second clause is exactly the still-unproved persistent Schur/
component-frame operation.  The well/merge structure feeding it is already
maintained in `O_tilde(M)` deterministic local work.  This is a genuine optimizable theorem
*conditional on a named producer*, not a bound obtained by treating its
dense output as free.

The cutoff need not be guessed in advance.  Let

```text
tau_k=2^k sqrt(alpha),       sqrt(alpha)<=tau_k<=1,
Lambda_k=alpha+tau_k^2.
```

There are `K=O(log(1/alpha))` scales.  Maintain the preceding counters and
union--find forest independently at every scale.  An admitted edge changes
one exterior-degree counter at each scale, and a vertex enters each scale's
well at most once.  Hence all dyadic structural forests together cost
`O_tilde(M)` work and space.  This is an actual simultaneous maintenance
theorem; the tilde hides only the `K` factor.

Suppose in addition that `LandscapeSchurClosure(tau_k)` is a correct,
interruptible certified implementation at every scale and touches only the
eventual support.  Give one work quantum in round-robin order to every live
scale and return the first result passing the common quiet-KKT certificate.
If scale `k` would finish after `T_k` of its own operations, the race finishes
after at most `K min_k T_k` aggregate operations.  Consequently the
parameter-free conditional bound is

```text
O_tilde(min_k {A_fast(k)/tau_k+B_land(k) tau_k/alpha}).
                                                        (dyadic landscape race)
```

When `A_fast,B_land` are scale-independent, a dyadic point lies within a
factor two of `sqrt(A_fast alpha/B_land)`, so the race is within a constant
factor (besides logarithms) of the continuous optimum.  Thus parameter
selection is not the remaining obstruction: response production is.  The
round-robin premise is important.  Running every scale to completion and
summing their bounds can pay `M/alpha` at the largest scale.

The forest also must not be confused with the required response frame.  A
single connected landscape well can contain arbitrarily many low modes.
Take `r` disjoint unweighted cliques of size `L` and join one distinguished
vertex of each clique to one common hub.  On the full face `d_out=0`, so
`V_U=alpha` everywhere and the well graph has one connected component.  Let
`W=L(L-1)+1` be a clique's degree volume.  The `r`-dimensional trial space
whose vectors satisfy

```text
f_i=t_j sqrt(d_i) on clique j,       f_hub=0
```

has, by the exact landscape identity,

```text
f^TQf/||f||^2<=alpha+c/W.
```

Min--max therefore gives `lambda_r(Q)<=alpha+c/W`.  Taking
`W>=c/tau^2` puts at least `r` eigenvalues below `alpha+tau^2` although the
well forest has only one component.  Thus retaining one Perron scalar per
connected well is rigorously false; a Bessel-stable frame or an implicit
coarse operator is necessary.

The smallest moving-face algebra shows exactly which extra state is absent.
If an old block `A` gains one new coordinate coupled by row `C`, block
inversion contains

```text
A^-1 C^T (D-CA^-1C^T)^-1 C A^-1.             (merge correction)
```

Even when `C` has one nonzero, `A^-1C^T` is generally dense.  On a
degree-two path, put `A=tridiag(-gamma,a,-gamma)` with
`a=(1+alpha)/2`, `gamma=(1-alpha)/4`, and attach the new endpoint at the
last old coordinate.  If `cosh(kappa)=a/(2gamma)`, then, after the coupling
normalization,

```text
(A^-1 gamma e_n)_i=sinh(i kappa)/sinh((n+1)kappa),
kappa=Theta(sqrt(alpha)).
```

Every old coordinate changes and the response has critical propagation
length `Theta(1/sqrt(alpha))`.  Union--find stores none of this vector.  A
path can represent it by a constant-size transfer recurrence, so the example
is not a lower bound against all algorithms; it is a strict witness that the
structural well forest alone does not implement `LandscapeSchurClosure`.

The same floor-aware factor also gives a direction-uniform chamber return
theorem.  For a source-free chamber `W` coupled to any collection of ports
by `C=-Q_(W,Gamma)>=0`, the `WW` block of `I-N^2>=0`, where `N` is the
global normalized adjacency, gives

```text
CC^T<=(Q_W-alpha I)(I-Q_W).                    (boundary trace)
```

Douglas factorization therefore implies, for every scalar spectral function
`r`,

```text
||C^T r(Q_W) C||
 <=max_(lambda in spec(Q_W))
      |(lambda-alpha)(1-lambda)r(lambda)|.
```

In particular,

```text
0<=C^TQ_W^-1C<=(1-sqrt(alpha))^2 I.           (full round trip)
```

For the bottom band `lambda<=C0 alpha<=sqrt(alpha)`, the sharper multiplier
is at most

```text
(1-1/C0)(1-C0 alpha)<1.                       (bottom round trip)
```

These inequalities are multi-port and rank-free; products of literal
bottom-chamber return maps contract even when their eigenvectors rotate and
the maps do not commute.  They rule out “many port directions” as a local
counterexample.  They do not by themselves compose through the evolving
interface: Schur elimination inserts an interface inverse with norm as
large as `1/alpha` between returns.  A near-isometric normalized return then
represents continuation of one extended global low mode, which the
persistent state should share, but proving that chronology is exactly the
component-frame transport clause above.  The `F0` ledger pays every explicit
moving-cut offspring; the landscape/round-trip facts still need the
relative occupancy assignment to turn that payment into products.

This `F0` construction is a local **metric**, not a sparse approximation to
the positive fractional generator.  It certifies a signed NAG trajectory;
it does not make that trajectory monotone.  For example, with
`alpha=10^-2`, a scalar mode `lambda=1/2`, unit positive load, and zero
history, the NAG iterates begin

```text
1, 1.90909, 2.32645, 2.33396, 2.17005, 2.01797, ...,
```

around the exact value `2`.  The negative increments after the overshoot
are exactly what the Poisson flow forbids.  Lattice projection protects a
certified lower envelope but does not turn the signed transfer polynomial
into a completely monotone function or give principal-domain order.
Consequently `F0` avoids a dense response in the *output accounting*; it
does not implement `A^-1/2`.  Any implementation that insists on the
Poisson flow's entrywise monotonicity must still use positive shifted
resolvents (or graph-specific elimination), and therefore still encounters
`CenterLift` under nested growth.

The implementation audit now evaluates this companion metric directly.
On 80 additional random connected graphs, all projected runs terminated and
all batches were immediately scratch-ready.  The largest normalized held
LMI ratio was `0.9999105`, the largest lattice-projection ratio was
`1+4e-16`, and every event upper bound had nonnegative numerical slack.
Weighted random trees with five decades of edge variation raised the
observed constant (`iterations*sqrt(alpha)`) to about `22.52` but did not
make it grow as `alpha` decreased: on the worst sampled tree the values for
`alpha=10^-2,3*10^-3,10^-3,3*10^-4,10^-4` were respectively
`24.00,23.33,22.52,21.43,20.37`.  These are regression tests for the exact
algebra and useful counterexample searches, not a proof of the chronology
lemma.

The held LMI is tied to the critical momentum `sqrt(alpha)` and must not be
silently advertised as a tunable-`tau` Lyapunov.  A naive substitution makes
this false even in one scalar mode.  Set `tau=alpha^(1/4)`, use momentum
root `delta=sqrt(alpha+tau^2)`, keep the same `F0` metric, and start the floor
mode `lambda=alpha` from `(h,w)=(1,0)`, with the natural
`w=delta(z-x^U)` scaling.  One step has

```text
h^+=(1-alpha)/(1+delta),
w^+=tau^2/(1+delta),
J^+/J
 =[(1-alpha)^2+(1+alpha c)tau^4/alpha]/(1+delta)^2
 ->2 as alpha->0.
```

For `alpha=10^-4` the ratio is `1.65127>1`.  Thus the critical `F0`
theorem closes the desired `tau=sqrt(alpha)` shock algebra, but the full
parameterized tradeoff must still come from shifted prox/hierarchy or from
a new tunable metric with its event and lattice properties proved afresh.
This failure extends to the entire natural diagonal Stieltjes family.  Let
`alpha=epsilon^4`, `tau=epsilon`, `epsilon<=10^-2`, and consider

```text
p h^TQh+w^T(kI+gamma F0)w,       p,k,gamma>=0,
```

with the tuned companion root
`delta=sqrt(alpha+tau^2)`.  Divide the metric by `p` (the case `p=0` is
degenerate) and write `m(lambda)=k+gamma f0(lambda)`.  Nonexpansion of each
individual input column gives three necessary inequalities.

* At `lambda=alpha`, the input `(h,w)=(1,0)` gives exactly

  ```text
  m(alpha)
   <=(1+delta)^2-(1-epsilon^4)^2<=2.1 epsilon,
  ```

  so `k<=2.1 epsilon`.
* At `lambda=epsilon`, the input `(0,1)` gives

  ```text
  m(epsilon)
   >=epsilon(1-epsilon)^2/
      [(1+delta)^2-(1-epsilon)^2]>=0.24.
  ```

  Since `f0(epsilon)<=epsilon`, this forces
  `gamma>=0.21/epsilon`.
* At `lambda=a=(1+alpha)/2`, the first input column requires
  `m(a)<=1.6`, whereas `f0(a)=ac` and the preceding lower bound gives
  `m(a)>=gamma ac>5`.

This contradiction proves that no metric in the displayed diagonal family
is even one-step nonexpansive for the tunable recurrence.  A successful
tunable version needs cross-history terms, a multi-step potential, or a
different operator; each option must re-establish Stieltjes lattice
compatibility and the exact principal-growth cut drop.  The result is a
scoped obstruction, not a proof that no richer tunable Lyapunov exists.

#### Certified-gap adaptive companion metric

A different operator does in fact close the natural formed-face gap route.
Suppose the current face has a certified bound

```text
alpha<=mu<=lambda_min(Q_U),       t=sqrt(mu),
```

and tune the NAG companion to root `t`.  Define

```text
F_mu=(1+mu)Q-Q^2-mu aI
    =acI-c(mu-alpha)S-c^2S^2,
J_mu(h,w)=h^TQh+||w||^2+w^TF_mu w,
w=sqrt(mu)(z-x^U).
```

This metric is not in the refuted family above: the new
`-c(mu-alpha)S` distance-one term changes the operator, rather than merely
reweighting `F0`.  On every scalar mode `lambda in [mu,1]`,

```text
f_mu(lambda)=(1+mu)lambda-lambda^2-mu a,
M_(lambda,mu)^T diag(lambda,1+f_mu(lambda)) M_(lambda,mu)
 <=(1-sqrt(mu))diag(lambda,1+f_mu(lambda)).
                                                        (adaptive held LMI)
```

The exact tensor-Bernstein certificate substitutes
`mu=t^2`, `alpha=z t^2`, and `lambda=t^2+(1-t^2)y`.  The two diagonal minors
have degrees `(8,4,1)` and least positive coefficients `1/56,1/8`; the
determinant has degree `(15,6,2)` and least positive coefficient `1/3003`.
The reproduction is `gap_adaptive_fmu_exact.py`.

All sign and event properties survive.  Concavity of `f_mu` gives
`0<F_mu<=Q` on a certified face.  Its expansion above is Stieltjes, and

```text
(I+F_mu)Q^-1
 =(1-mu a)Q^-1+(1+mu)I-Q>=0 entrywise,
```

so the same lower-box lattice projection is Fejer.  For a fixed `mu` and a
principal extension with `C=-Q_BU`,

```text
(Ew)^TF_(mu,T)(Ew)=w^TF_(mu,U)w-||Cw||^2.       (adaptive cut drop)
```

The parameter can decrease without a restart debt.  If
`alpha<=nu<=mu`, keep the physical auxiliary error `z-x^U` and rescale
`w` by `sqrt(nu/mu)`.  For every `lambda in [alpha,1]`,

```text
1+f_mu(lambda)-(nu/mu)(1+f_nu(lambda))
 =(mu-nu)/mu [1+lambda-lambda^2+(mu+nu)(lambda-a)]>=0.
                                                        (free gap decrease)
```

For `lambda>=a` positivity is immediate.  For `lambda<=a`, use
`mu+nu<=2` to lower-bound the bracket by
`3lambda-lambda^2-alpha>=2alpha-alpha^2`.  Thus one may first lower the root
to a certificate valid on the impending larger face and then recenter at
that new root; no unsafe over-tuned step is taken.

The ordering is necessary, not cosmetic.  On the simple unit triangle,
take the old two-vertex face and its exact gap `mu=a-c/2`, then add the third
vertex, whose full-face gap is `alpha`.  Recentring while retaining the stale
`mu` gives an exact companion jump satisfying

```text
lim_(alpha->0) alpha Delta J_stale/(x^TQx)=7/32.
```

Thus stale-gap expansion can amplify the source energy by
`Theta(1/alpha)`.  The implemented schedule first computes the new safe
certificate, lowers the physical root for free on the old face, and only
then expands.

The variable-gap event ledger is also exact.  Let `nu` be the new valid
certificate, `e=x^U-ell`, `d=x^T-Ex^U>=0`, `Q_Td=E_Bg`, and after the free
rescaling put `w=sqrt(nu)(z-x^U)`.  Direct expansion gives

```text
Delta J_nu
 =||d||_Q^2-2nu(1-nu a)(z-x^U)^Td+nu||d||^2
  -||Cw||^2-2sqrt(nu)g^TCw+nu d^TF_(nu,T)d,
```

and hence

```text
Delta J_nu
 <=-(1/2)||Cw||^2+(2+nu)||d||_Q^2
   +2nu e^Td+2nu||g||^2.                         (adaptive event bank)
```

Here `F_nu<=Q_T`, `Q_T>=nu I`, and
`||g||^2<=||d||_Q^2`.  The positive terms are genuinely summable.  Exact
center increments are energy-orthogonal, so
`sum||d||_Q^2<=x*^TQx*<=alpha`, and the same bound pays the gates.  Within
one dyadic `nu` level, `e<=x^U` implies

```text
2e^Td<=||x^T||^2-||x^U||^2,
nu||x^T||^2<=x^TQ_Tx^T<=alpha.
```

There are only `O(log(1/alpha))` nonincreasing levels.  Therefore every
positive event debt and the full velocity-cut bank remain
`O_tilde(alpha)`, while held steps contract at the current certified rate
`1-sqrt(nu)`.

The same metric yields a sharp certified-gap fixed-face square function.
Let `A` be held, put `s=sqrt(mu)`, and let
`q_t=(h_t+w_t)/(1+s)` be the tuned NAG extrapolate.  For any fixed exterior
row block `C`, the PageRank principal-block identity gives

```text
C^TC<=(A-alpha I)(I-A).
```

Solving the exact two-by-two scalar observability Lyapunov equation and
comparing it with the `J_mu` metric gives

```text
sum_(t>=0)||Cq_t||^2
 <=[(3+sqrt(5))/(8sqrt(mu))] J_mu(h_0,w_0).
                                                        (adaptive square function)
```

The constant `(3+sqrt(5))/8` is sharp for this uniform scalar comparison:
as `mu->0`, `alpha/mu->0`, and `lambda=mu`, the normalized Gramian tends to
`[[1/2,1/4],[1/4,1/4]]`.  Its top eigenvalue is exactly that constant.  The
exact tensor-Bernstein certificates for both principal minors and the
determinant are reproduced by `adaptive_square_function_exact.py`.

This theorem is fixed-face/fixed-exterior.  It does not splice its exact
future tail through face growth.  On the unit path `P4`, take old face
`U={1,2}`, add `B={3}`, keep `W={4}` exterior, and initialize
`h=e_1,w=0`.  The old persistent cut is zero, and the expansion interface
satisfies

```text
C_BU h=C_BU w=C_BU q_0=0,
C_WT q_0=C_WT q_1=0.
```

Nevertheless zero-extended tuned NAG gives

```text
(q_2)_3=sqrt(2)c^2/(1+sqrt(mu))^3,
C_WT q_2=c^3/(1+sqrt(mu))^3>0.
```

Thus the exact remaining exterior-observability potential jumps while every
instantaneous interface term above vanishes.  The coarse `J_mu` dissipation
and the event bank still bound total square output, but restarting a future-
tail bound at each face can repurchase the same packet.  This is an exact
`PublicationSharedClock` obstruction, not a contradiction to the fixed-face
square function.

The purely numerical startup/re-equilibration cost of visiting dyadic roots
is geometrically dominated by the last certificate:

```text
sum_(visited levels k) 1/sqrt(mu_k)
 =O(1/sqrt(mu_final)).
```

This statement prices root changes; it must not be confused with a proof
that the next publication occurs after one such equilibration window.

This makes dyadic unknown-gap transport executable whenever a charged lower
certificate is available.  More generally, Collatz--Wielandt gives, for any
strictly positive exposed vector `v`,

```text
mu_hat(U,v)=max{alpha,min_(i in U)(Q_Uv)_i/v_i}
           <=lambda_min(Q_U).
```

Taking `v=1` is the exposed-row Gershgorin certificate; taking
`v_i=sqrt(d_i)` gives exactly
`min_i[alpha+c d_out,U(i)/d_i]`.  The latter is local, incrementally
maintainable, and nonincreasing under face growth.  Better positive vectors
can strengthen the certificate, but constructing a near-Perron `v` through
nested faces is itself a positive inverse/power-response problem; it must be
charged and can be slow when several low modes nearly coincide.  Ordinary
Lanczos Ritz values remain unsafe upper estimates.  The theorem improves the later moving-state clock on favorable
formed faces and removes the earlier metric/restart obstruction.  It does
not by itself convert the square bank into a scale-relative publication
occupancy bound, and at `nu=alpha` it reduces to the still-open critical
general-graph chronology problem.

A second safe certificate makes the geometry explicit.  Choose for each
`i in U` a path `P_i` to an exterior zero, including its final boundary
edge, and set

```text
Gamma(P)=max_e sum_(i:e in P_i) d_i |P_i|.
```

Writing `x_i=sqrt(d_i)u_i`, path Cauchy--Schwarz and the exact grounded
Dirichlet identity give

```text
||x||^2<=Gamma(P) x^T(I-S_U)x,
mu_path(U)=alpha+(1-alpha)/(2Gamma(P))
          <=lambda_min(Q_U).                     (path certificate)
```

There is no lost factor two.  A boundary-rooted multi-source BFS forest and
one subtree-load accumulation evaluate a valid `Gamma(P)` in `O(vol(U))`
work.  This can be stronger or weaker than the pointwise landscape bound,
but it does not supply response reuse.  On the canonical ballasted broom,
after the ballast batch and `j` handle vertices are active, the unique
boundary routing has the exact congestion

```text
Gamma_j=j^2+(2N+2)j+3N+1,       N=ceil(10/alpha).
```

For `Theta(alpha^-1/2)` consecutive singleton faces,
`mu_path(U_j)<=1.01alpha` and the true gap is at most `1.03alpha`.
Recomputing all BFS certificates costs only `O(M/sqrt(alpha))`, but one
fresh relaxation per face still costs `Omega(M/alpha)`.  Charging increases
of `Gamma_j` does not help: nearly all of
`Gamma_j-Gamma_(j-1)=2N+2j+1` is the same old ballast volume acquiring one
extra path edge.  Thus a path certificate closes safe parameter selection,
not `PublicationSharedClock`.

For one fixed supplied face, even certification can be avoided by a dyadic
race.  Run roots `mu_k=2^-k` down to `alpha`, quarantine every over-tuned
lane, and accept only a deterministic full residual/KKT pass.  The first
valid level satisfies `mu_k in (lambda_min(Q_U)/2,lambda_min(Q_U)]`; all
earlier scheduled budgets form a geometric prefix, giving

```text
O_tilde(vol(U)/sqrt(lambda_min(Q_U)))             (fixed-face race)
```

without treating a Ritz value as a lower bound.  A false high guess can also
be retracted to a safe lower subsolution, but its signed history cannot be
retained under `F_mu`.  Repeating this race on nested faces is exactly the
fresh-face ledger refuted by the broom, so it is not a moving-face theorem.

The adaptive implementation is a regression option in
`run_projected_estimate_nag`.  On the delayed 34-vertex witness it starts at
the safe dyadic singleton gaps `0.256` (`alpha=10^-3`) and `0.4096`
(`alpha=10^-4`), drops to `alpha` at the first expansion, and changes the
publication times from `[0,1,2,3,4,38]` to `[0,1,2,3,4,5]` in the first run
and from `[0,1,2,3,43,44]` to `[0,1,2,3,4,5]` in the second.  Every exact
held, projection, and event inequality retained nonnegative numerical slack.
The total iterations fall only from `528` to `490` and from `1613` to `1568`,
because the cheap certificate immediately becomes `alpha` and the terminal
fixed-face accuracy tail is unchanged.  This is useful evidence that the
free switch is implemented correctly, not evidence that the landscape
certificate tracks the true gap or closes the general clock.  A further 200
random connected-graph runs all terminated; the largest normalized held
ratio was `0.9999071`, the largest projection ratio was
`1+2.3e-16`, and at most four dyadic certificate levels were visited.
At `alpha=3e-5` on the delayed witness, the fixed clock publishes at
`[0,1,2,3,52,53]` while the adaptive clock publishes at `[0,1,2,3,4,5]`;
the total normalized iterations change only from `16.02` to `15.73`.  This
again separates a real early-face acceleration from the still-unproved
global shared-clock conclusion.

#### Positive square-root flow: an ideal clock and a locality barrier

For a fixed Stieltjes face `A` and one nonnegative expansion packet `g`, the
continuous flow

```text
dot d=A^(-1/2)(g-Ad),       d(0)=0
```

has the exact solution

```text
d(t)=A^-1(I-exp(-t sqrt(A)))g,
g-Ad(t)=exp(-t sqrt(A))g.
```

Both `x^-1/2` and `exp(-t sqrt(x))` are completely monotone.  Their
resolvent/heat-subordination formulas and the Stieltjes signs therefore give

```text
d(t)>=0,        dot d(t)>=0,        g-Ad(t)>=0,
||d(infinity)-d(t)||_A
 <=exp(-t sqrt(alpha))||d(infinity)||_A.       (positive root clock)
```

It is exactly the nonoscillatory accelerated clock desired by publication.
It also respects principal growth.  For `U subset T`, `s>=0`, and `g_U>=0`,
Schur complement positivity gives

```text
E(A_U+sI)^-1g_U <=(A_T+sI)^-1E g_U.
```

Integrating against `s^-1/2/pi` yields the same inequality for
`A^-1/2`.  At a face expansion, the embedded old state has nonnegative old
residual and new residual `-A_BUd_U>=0`, so every old packet continues
monotonically without a sign reset.  This proves that a positive ideal
`PublicationSharedClock` exists at the operator level.

The dual-dominance projection above is **not** an implementation of this
flow.  NAG has a signed polynomial transfer on the high band; projecting its
two physical states is nonlinear and preserves a Lyapunov/lower-envelope
order, but it does not make the packet transfer completely monotone, linear,
or domain-monotone.  The later `F0` construction does give a valid discrete
full-spectrum stopped-cut surrogate and closes the cut-source/velocity
offspring in square energy.  What it still does not inherit from the Poisson
flow is a coordinatewise ordered, scale-relative clock: the signed NAG
trajectory may overshoot, and its square bank does not count arbitrarily
small threshold crossings.  The dense fractional inverse is therefore no
longer needed for the offspring *ledger*, but remains the only closed route
here to literal positive domain-monotone evolution.

There is a simple degree lower bound showing why a purely local positive
polynomial cannot fill this gap.  Suppose

```text
p_k(P)=sum_(j=0)^k c_j P^j
```

is entrywise nonnegative for every symmetric nonnegative substochastic
`P`.  Applying it to a path scaled by an arbitrarily small edge weight and
looking at its two endpoints forces `c_j>=0` for every `j`.  Let
`A=aI-bP`, take scalar `P=1` and `P=1-alpha`, and, for
`alpha<=1/2`, suppose `p_k` has relative error at most `1/25` for
`A^-1/2` on both scalars.  Positivity of the coefficients gives

```text
p_k(1-alpha)/p_k(1)>=(1-alpha)^k,
```

whereas the target ratio is

```text
(a-b)^1/2/(a-b(1-alpha))^1/2=1/sqrt(1+b),
```

a constant bounded away from one even after the `1/25` approximation
factors.  Hence

```text
k=Omega(1/alpha).                              (positive fractional barrier)
```

So the root-time `A^-1/2` action cannot be obtained from a universal
entrywise-positive sparse walk polynomial.  Positive rational quadrature
evades the polynomial barrier, but every term is a shifted inverse
`(A+sI)^-1`; multi-shift Krylov shares their recurrence on one fixed face,
while nested-face reuse is precisely `CenterLift`.  A graph-specific tree or
hierarchical factor can also evade the barrier, which is why trees and
bounded-fill classes remain positive special cases.  On general graphs the
Poisson route is therefore a clean equivalent formulation of the missing
persistent dense response, not a free derandomization.

The Perron survival identity gives a genuine spatial version of the missing
shared clock.  Work in degree coordinates on a connected source-free
chamber `W`.  Let `P_W` be the substochastic random-walk restriction, let
`r_W` be its Perron root, and write

```text
Q_W=aI-bP_W,
a=(1+alpha)/2,        b=(1-alpha)/2,
theta=b/a,
lambda_W=a-b r_W=alpha+b(1-r_W).
```

Normalize the positive Perron vector `phi` so that its maximum is one and
let `m` be a maximizing row.  Since `1>=phi`,

```text
Pr_m(tau_W>t)=(P_W^t 1)_m
              >=(P_W^t phi)_m=r_W^t.
```

The exact survival generating-function identity then gives

```text
E_m[theta^tau_W]
 =1-(1-theta) sum_(t>=0) theta^t Pr_m(tau_W>t)
 <=theta(1-r_W)/(1-theta r_W)
 =(lambda_W-alpha)/lambda_W.                 (Perron attenuation)
```

If `u` is a nonnegative `theta`-harmonic single-source Green response in
`W`, with its source outside the chamber, optional stopping yields

```text
u_m<=((lambda_W-alpha)/lambda_W) max_(boundary W)u.
```

This statement is independent of the number of boundary ports: it uses only
their maximum value.  In particular, if `lambda_W<=C alpha`, every serial
source-free slow chamber loses a constant factor.  The amplitude range used
here has an exact canonical justification, rather than a complementarity
margin assumption.  On the final support `S`, in degree coordinates put

```text
p=alpha H_SS^-1 e_v,          q=alpha rho H_SS^-1 d_S,
y*=p-q>0,                     H=aD-bA.
```

Inverse positivity and the diagonal Schur-complement identity imply, for
every `i in S`,

```text
q_i>=alpha rho d_i(H_SS^-1)_(ii)
   >=alpha rho d_i/H_ii=alpha rho/a,
p_i>q_i.
```

The maximum principle places `max_S p` at the seed, and the seed equation
gives `p_v<=1/d_v<=1`.  Thus every final-support coordinate lies on a
positive point-source Green profile with

```text
alpha rho/a < p_i <=1.                         (canonical Green range)
```

Consequently only `O(log(1/(alpha rho)))` constant-attenuation chambers can
occur on a significant serial ancestry chain.  Notice that this is a lower
bound on the *unregularized source response* `p`, not on `y_i^*` itself;
the latter can approach zero without strict complementarity.

The identity is even better aligned with the shifted-prox balance.  For
`Q_W+sigma I`, replace `theta` by `theta_sigma=b/(a+sigma)` to obtain

```text
E_m[theta_sigma^tau_W]
 <=(lambda_W-alpha)/(lambda_W+sigma).
```

With `sigma=tau^2` and `lambda_W<=alpha+tau^2`, this is at most

```text
q_tau=tau^2/(alpha+tau^2).
```

Hence the number of significant serial chamber layers is bounded by

```text
log(1/(alpha rho))/log(1+alpha/tau^2)
 <=(1+tau^2/alpha) log(1/(alpha rho)).        (serial chamber depth)
```

A supplied laminar chamber hierarchy now gives a closed conditional
balance.  Assume that, at every hierarchy node, the reflected mean-zero
subspace has gap `Omega(tau^2)`, its one remaining coarse direction is the
positive Perron mode above, parallel children partition the node up to
polylogarithmic overlap, every significant child can be assigned to a
source-to-target ancestry to which the boundary-maximum attenuation applies,
and response states are retained rather than rebuilt.  All mean-zero work at
one layer costs `O_tilde(M/tau)` by Chebyshev, while
`(serial chamber depth)` bounds the number of significant coarse layers.
Therefore

```text
T_LaminarPerronLift(tau)
 =O_tilde((M/tau)(1+tau^2/alpha))
 =O_tilde(M/tau+M tau/alpha).                 (supplied hierarchy theorem)
```

This is the precise way the survival lemma strengthens the earlier
conductance proposal: it proves the serial low-mode clock, rather than only
postulating that an expander hierarchy has few coarse steps.

The positivity qualification is essential.  The argument applies directly
to the exact Green profile, monotone Schur increments, and shifted-obstacle
prox responses.  It does not apply to a signed NAG error or momentum state:
optional stopping controls a nonnegative harmonic function, whereas a
mean-zero accelerated transient can change sign and can cross the same
one-sided gate asynchronously.  Connecting this spatial theorem to raw NAG
would require a separate positive-envelope or projective-state bridge.  The
lower-envelope/retraction interface supplies safe output once a positive
response is produced, but it does not create that bridge for free.

There is also a parallel-volume identity.  Summing the Perron equation in
the reversible degree measure cancels internal edges and gives

```text
sum_(i in W,j outside W) w_ij phi_i
 =(1-r_W) sum_(i in W)d_i phi_i
 =((lambda_W-alpha)/b) sum_W d_i phi_i.       (Perron leakage)
```

If a chamber receives entrance Perron leakage at least `gamma max(phi)`,
then

```text
vol(W)>=gamma b/(lambda_W-alpha).
```

For `lambda_W-alpha<=tau^2`, a disjoint parallel family therefore buys
volume `Omega(gamma/tau^2)` per significant chamber.  At one laminar level
these volumes sum to `M`, while all chambers at that level evolve in
parallel under the same products.

The word *laminar* is essential.  Leakage volume cannot be summed over
arbitrary overlapping slow chambers.  On the interior of a unit path, take
all sliding intervals of length `k`.  Each has

```text
r_W=cos(pi/(k+1)),
lambda_W-alpha=Theta(1/k^2),
max(phi)=1,
cut leakage=Theta(1/k),
vol(W)=Theta(k),
```

so the volume lower bound is tight.  A path of length `2k` contains
`Theta(k)` such intervals; their total counted volume is `Theta(k^2)` even
though the graph volume is only `Theta(k)`.  Taking
`k=Theta(1/sqrt(alpha))` makes every interval an `O(alpha)`-gap chamber.
Thus no argument may charge adaptively chosen overlapping chambers directly
to `(Perron leakage)`.

This also locates the multi-port gap.  A fixed chamber's Perron component is
safe under arbitrarily many ports, but asynchronous ports can excite signed
mean-zero combinations or raise the boundary maximum at different times.
If the reflected chamber has only one low mode, those combinations are fast;
otherwise the chamber must be cut recursively.  What remains unproved for a
general online face sequence is a deterministic bounded-overlap laminar
selection plus persistent response transport.  Equivalently, one must show
that the canonical chronology cannot reuse the same overlapping slow volume
as many fresh projective clocks.  This is exactly
`SourceClockNoReuse/NestedExpanderLift`, not a missing scalar inequality in
the survival proof.

For clarity, the fixed-chamber multi-port statement is a spectral theorem.
Normalize the Perron vector `phi` in Euclidean coordinates and suppose

```text
lambda_1(Q_W)<=alpha+tau^2,
lambda_2(Q_W)>=alpha+c_0 tau^2.
```

For any nonnegative aggregate port load `g`,

```text
(Q_W+tau^2 I)^-1 g
 =phi [phi^Tg/(lambda_1+tau^2)]
  +(Q_W+tau^2 I)^-1(I-phi phi^T)g.            (port split)
```

The first term depends on all ports through one positive scalar.  Along a
monotone sequence of positive port increments that scalar is monotone, so it
starts only one coarse clock.  The second term has operator norm at most
`1/(alpha+(1+c_0)tau^2)` and is approximated by a degree
`O_tilde(1/tau)` polynomial.  Thus port count does not enter the slow rank
when the chamber has one low mode.  If `lambda_2` is also low, `(port split)`
exhibits the exact reason to recurse: distinct ports can address different
low directions.  A supplied reflected expander hierarchy supplies this
one-low-mode promise; constructing and updating it locally remains the
producer problem.

The parallel/overlap issue can be exposed as an optimizable observable
parameter rather than hidden in `O_tilde`.  For a fixed `tau`, suppose the
online chamber epochs can be assigned to a rooted hierarchy forest such
that

```text
A_H = total root-chamber volume,
B_H = maximum, over positive hierarchy depths, of the total chamber volume
      at that depth, counting overlap and repeated epochs with multiplicity.
```

Assume the one-low-mode and persistent-response clauses above.  The root
fast pass costs `O_tilde(A_H/tau)`.  Perron attenuation permits only
`O_tilde(tau^2/alpha)` further significant depths, each of total volume at
most `B_H`, so

```text
T_H(tau)=O_tilde(A_H/tau+B_H tau/alpha).       (hierarchy ledger)
```

When the certificates and ledgers remain valid over the candidate range,
the formal optimizer is

```text
tau_*=sqrt(A_H alpha/B_H),
T_H(tau_*)=O_tilde(2 sqrt(A_H B_H/alpha)),
```

clipped to the allowed spectral interval.  A laminar partition has
`A_H,B_H=O_tilde(M)` and recovers `tau=sqrt(alpha)`.  Repeated sliding path
intervals have `B_H=Theta(kM)` if treated as separate epochs, exactly
recording the invalid overlap charge.  Thus `B_H` is the concrete parameter
which an online selector must keep small; the desired balance is no longer
obtained by silently assuming that all low chambers are disjoint.

There is nevertheless a nontrivial numerical-rank fact for the moving
inverse-square-root probe.  Compare one enlarged shifted face with the direct
sum of the old face and its raw new block:

```text
A_0=A_U direct_sum F,
A_1=[A_U E;E^T F]=A_0+D,       rank(D)<=2|B|.
```

The low-rank matrix-function update theorem of Shmueli--Drineas--Avron
applied to `Delta=A_1^(-1/2)-A_0^(-1/2)` gives, in blocks of size
`k=rank(D)`,

```text
sigma_(j+k l)(Delta)
 <=4 exp[-Theta(l/log(kappa_hat))] sigma_j(Delta).
```

Thus one batch has inverse-square-root correction rank

```text
r_epsilon=O(|B| log(kappa_hat) log(1/epsilon)).       (sqrt-update rank)
```

This avoids the pinning reduction and is a genuine reason to test a
low-rank moving deterministic probe in practice.  It does not contradict the
`Theta(1/tau^2)` light-direction witness: many individually low-rank updates
can accumulate independent directions.

The published construction is not the missing work theorem.  Its stated
Riccati cost is

```text
O((T_(A^1/2)+T_(A^-1/2)) r_epsilon^2+n r_epsilon^4),
```

and it assumes the ability to apply the *old* square root and inverse square
root.  In our recursion that application is the old-face response problem.
Storing every dense correction factor makes an application cost grow with
the whole prefix rank; repeatedly constructing later factors can then pay a
quadratic history sum.  The approximation is also two-sided in operator
norm, so the group reporter must use the already-proved additive `l2` error
guard rather than claim entrywise domination.  Consequently this result
supports the following precise conditional implementation target:

```text
LowRankSqrtUpdate(tau): construct, recompress, and apply all chronological
inverse-square-root corrections, including certified l2 error, in total
O_tilde(M/tau).
```

If that target is achieved, it directly produces the aggregate deterministic
Green probe.  The decay theorem proves small per-update numerical rank, but
not the online construction/recompression bound.

#### Canonical cut-supported transform

The point-source right-hand side has one further exact reformulation.  If
`y^U` is the degree-coordinate face solution and

```text
z^U=y^U+rho 1_U,
```

then, because

```text
H_U 1_U=alpha d_U+b d_out,U,
```

we have

```text
H_U z^U=alpha e_v+rho b d_out,U.              (cut source)
```

Thus every fixed face has a nonnegative right-hand side supported only at the
seed and the *interior endpoints* of its current cut.  This is useful: a
low-gap continuation should be parameterized not only by `mu_U`, but also by
the cost of transporting these cut sources through the old-face
Dirichlet-to-Neumann map.  It also makes the resolvent split above especially
natural.  At scalar eigenvalue `lambda>=alpha`, splitting the positive
fractional integral at a free scale `tau` gives

```text
integral_tau^infinity dt/(lambda+t^2) <= 1/tau,
integral_0^tau       dt/(lambda+t^2) <= tau/alpha.
```

If high-shift cut responses can be rented at total base cost `M` and the low
tail can be bought/aggregated through one persistent response representation,
these are exactly the formal ledgers `M/tau` and `M tau/alpha`.

The moving cut has a useful exact total-variation ledger.  Embed every
`d_out,U_j` in the final support `S*`, with zero coordinates outside `U_j`,
and include the change from the empty face.  Along a nested chain,

```text
sum_j ||d_out,U_(j+1)-d_out,U_j||_1 <= vol(S*)=M.   (cut variation)
```

Indeed, an edge whose two endpoints eventually enter contributes `+1` when
its first endpoint enters and `-1` when its second endpoint enters, unless
both enter in the same batch; a final boundary edge contributes only the
first event.  Summing absolute changes therefore charges each internal edge
at most twice and each final boundary edge once.  The same proof works for
weighted graphs with conductance in place of edge count.  Consequently the
degree-coordinate transformed right-hand sides have signed variation

```text
rho b sum_j ||Delta d_out,U_j||_1 <= rho b M <= b,
```

apart from the single seed mass `alpha`.  This is strictly stronger than
summing the *sizes* of all intermediate cuts, which can count a persistent
edge in every face.

There is also an exact cancellation that explains what this variation ledger
does and does not buy.  Let `T=U union B`, assume the seed is already in `U`,
and initialize the expanded transformed vector by

```text
zbar_T=(z^U, rho 1_B).
```

Writing

```text
e_B^U=b D_B^-1 A_BU y^U-alpha rho 1_B
```

for the original degree-normalized boundary excess, direct block
multiplication gives

```text
(alpha e_v+rho b d_out,T)-H_T zbar_T
    = (0_U, D_B e_B^U).                         (padding cancellation)
```

On the old rows, deleting the `U--B` cut load is exactly cancelled by padding
the new `z` coordinates with `rho`.  All remaining forcing is supported on
the newly admitted block and is precisely the already-certified active
excess.  Thus, when `e_B^U>=0`, the correction is the positive frontier lift

```text
z^T-zbar_T=H_T^-1 (0,D_B e_B^U)>=0.
```

This closes the *source-update* side of the canonical transform: changing
cut loads do not require replaying old rows merely to restore their
equations.  It does not close `CenterLift`.  Computing the displayed inverse
action on old coordinates is exactly the dense Schur/Dirichlet-to-Neumann
response.  The canonical conservation identity below charges the total
frontier input mass, and `(cut variation)` charges the transformed cut input,
but neither ledger prices the graph work needed to materialize their
responses.

There is a useful algorithmic corollary which should be applied before any
spectral refinement.  If `ell_U` is a current subsolution and an exposed
boundary row has positive residual, that vertex is support-safe.  After
admitting any such batch and padding the new coordinates by zero,
`(ell_U,0_B)` is still a subsolution: old inequalities are unchanged, and
the new inequalities are exactly the positive boundary-residual tests.
Therefore an implementation may repeatedly

```text
admit every currently certified positive boundary row,
initialize it at zero, and continue local monotone settlements
```

until this avalanche stagnates, without invoking an SDD/Krylov solve.  Every
new adjacency row is still exposed only once and is charged to `M`.  Only a
stagnant face, whose current lower envelope has no positive boundary
residual, needs `CenterLift`/spectral refinement.  This can collapse an entire
endpoint path after one seed update, but it is not a bound on the number of
stagnations: the ballasted broom can be parameterized so that the next path
row becomes positive only after the current face response increases, giving
`Theta(1/sqrt(alpha))` genuine refinement points.  The free avalanche is thus
a mandatory preprocessing step and a practical improvement, not a
replacement for moving-response reuse.

In particular, small total input variation cannot justify literal monotone
row propagation.  On the two-row SDDM block

```text
[[a,-b],[-b,a]],       b/a=(1-alpha)/(1+alpha),
```

alternately settling the only positive residual contracts it by only
`(b/a)^2=1-Theta(alpha)` per pair of row touches.  Scaling the initial source
makes its total positive `l1` mass arbitrarily below `1/2` without changing
the required `Omega(1/alpha)` touches for a constant relative reduction.
An exact scalar Schur solve, of course, is constant work.  Hence the new
variation theorem eliminates one possible accounting loss but also sharpens
the missing lemma: the frontier inverse action must be *aggregated*, not
implemented as source-proportional coordinate settlement.

#### Global obstacle form and the parametric-path stop

The shift has an exact global interpretation which is stronger than the
face identity above.  In degree coordinates the original obstacle problem is

```text
min_(y>=0)  1/2 y^T H y-alpha e_v^T y+alpha rho d^T y.
```

Substitute `z=y+rho 1` and use `H1=alpha d`.  All terms linear in `z`
coming from `rho` cancel, leaving, up to a constant independent of `z`,

```text
min_(z>=rho 1) 1/2 z^T H z-alpha e_v^T z.       (fixed obstacle)
```

Consequently the global KKT system is

```text
z>=rho 1,   Hz>=alpha e_v,
(z_i-rho)(Hz-alpha e_v)_i=0  for every i.       (obstacle KKT)
```

Thus `z*` is the unique least-energy `H`-superharmonic majorant of the
constant obstacle.  On a face `U`, setting the exterior value to `rho`
gives exactly

```text
H_UU z_U=alpha e_v+rho b d_out,U;
```

the cut-supported equation is precisely a Dirichlet discretization of the
global obstacle, not an algebraic coincidence.  Notice also that clipping
the unconstrained Green response coordinatewise at `rho` is not a solution:
across an active--contact edge the clipping changes the harmonic equation.

This exposes a second deterministic route, but also its exact cost.  Regard
`rho` as a decreasing homotopy parameter.  On an interval where the active
set is `U`, the unshifted solution is affine:

```text
y_U(rho)=alpha H_UU^-1(e_v-rho d_U),
d y_U/d rho=-alpha H_UU^-1 d_U<0.               (path direction)
```

Inverse positivity and the comparison principle imply that, as `rho`
decreases, coordinates can enter the support but cannot leave it.  Hence the
canonical nonnegative `l1` path has at most `|S*|+1` affine pieces (simultaneous
entries only reduce this count).  This specializes the linear-breakpoint
phenomenon known for nonnegative Stieltjes quadratic regularization.  It is a
real structural improvement over a generic active-set QP: no exponential
pivot sequence is possible here.

It is not the desired local running-time theorem.  Advancing one breakpoint
requires the direction `H_UU^-1 d_U`; inserting a block `B` requires

```text
-H_UU^-1 H_UB,
```

and updating all inactive breakpoint keys is the corresponding
Dirichlet-to-Neumann action.  Condensed-inverse or rank-one pivot formulas
make this algebra explicit but make the response dense on a general graph.
Tracing all `|S*|` homotopy pieces is also potentially worse than the
`O_tilde(1/sqrt(alpha))` threshold-batch faces already proved in the
manuscript.  The homotopy becomes an output-linear algorithm on paths/trees
only because their response admits the retained scalar/subtree state proved
below; on a general graph it is another formulation of `CenterLift`.

This distinction also settles what the cut budget can safely buy.  The
variation bound pays for *describing* every change to the Dirichlet data, and
the padding identity pays for restoring all old equations without rereading
their rows.  It does not pay for applying the inverse.  Spectrally, a load
`g` can have

```text
g^T Q_UU^-1 g <= ||g||_2^2/alpha,
```

and the broom's one-edge cut is aligned with a Perron mode of eigenvalue
`(1+o(1))alpha`, making the `1/alpha` amplification essentially sharp.  The
comb independently prevents a universal constant-rank explicit response
table.  Neither graph refutes an implicit separator hierarchy, but together
they rule out the inference

```text
small cut variation  =>  cheap materialized response.
```

A homotopy implementation would therefore need the following charged
primitive, which is equivalent in substance to the earlier rent-or-buy
interface rather than a way around it:

```text
ObstacleHomotopyLift:
  maintain H_UU^-1 d_U, all new-column Schur responses, and the relevant
  inactive breakpoint/boundary keys under nested insertions;
  touch only support-safe exposed rows; and charge all dense response work
  to O_tilde(M/sqrt(alpha)) (or to the tau-split ledgers).
```

The value of the obstacle reformulation is that it narrows future searches
to this primitive and makes parametric Stieltjes-QP and sandpile algorithms
directly comparable.  It does not make a Dirichlet-to-Neumann query free.

There is an exact spectral interpretation of the cut source.  Let
`s_U=sqrt(d_U)` and scale the right-hand side back to normalized coordinates.
Since

```text
Q_UU s_U=alpha s_U+b D_U^(-1/2)d_out,U,
```

the transformed load is

```text
g_z
 =D_U^(-1/2)(alpha e_v+rho b d_out,U)
 =(alpha/sqrt(d_v))e_v+rho(Q_UU-alpha I)s_U.     (cut spectrum)
```

Thus the cut part is automatically multiplied by `lambda-alpha` on a
`Q_UU` eigenvector of eigenvalue `lambda`; the seed part is not.  For the
spectral projector `P_<beta` and `rho vol(U)<=1`, this gives the checked
graph-uniform bound

```text
||P_<beta g_z||_2
 <= alpha/sqrt(d_v)+rho(beta-alpha)||s_U||_2
 <= alpha/sqrt(d_v)+(beta-alpha)sqrt(rho).       (cut low band)
```

Combined with the residual-filter theorem, `(cut low band)` gives a genuine
source-effective cutoff whenever the accepted residual tolerance exceeds its
right side.  At the manuscript's certified face tolerance
`eta=Theta(alpha sqrt(rho eps_obj))`, however, even the first term is usually
too large.  On the ballasted broom `d_v=Theta(1/rho)`, it is exactly
`Theta(alpha sqrt(rho))`, a constant factor above the requested tolerance for
constant `eps_obj`.  Hence the formula identifies a useful favorable regime
but does not produce a graph-uniform low-gap branch at the required accuracy.

More explicitly, if `eta>2alpha/sqrt(d_v)`, set

```text
beta_cut=min{1,
  alpha+(eta/2-alpha/sqrt(d_v))/sqrt(rho)}.
```

Then `(cut low band)` is at most `eta/2` at `beta_cut`.  The bounded residual
filter of Section 4.1 therefore solves this transformed face in

```text
O_tilde(vol(U)/sqrt(beta_cut))
```

deterministic work, with the actual residual checked afterward.  If the
displayed inequality on `eta` fails, this corollary makes no improvement and
the safe fallback is `beta=alpha`.  This is a concrete cut/seed parameter,
not an eigenvalue estimate.  Like every fresh-face bound, its sum over nested
faces still requires the response-reuse primitive.

The literal cut size gives a second, incomparable fixed-face estimate.  With
`cut(U)=sum_{i in U} d_out,U(i)`, one has

```text
||D_U^(-1/2)d_out,U||_2^2
  =sum_i d_out,U(i)^2/d_i <= cut(U).
```

Consequently the positive `gamma=1` transform satisfies

```text
||P_<beta g_z||_2
 <= alpha/sqrt(d_v)
    +min{rho b sqrt(cut(U)),
         rho(beta-alpha)sqrt(vol(U))}.             (cut/low-band minimum)
```

This is the precise sense in which a small cut can reduce the *source
numerator*.  It still does not price the application of the old-face Green
function to that source: `cut(U)=1` is compatible with a dense response over
the whole old face.

The cut factor also gives a sharper response-energy identity.  Write

```text
g_cut=rho b D_U^(-1/2)d_out,U
     =rho(Q_UU-alpha I)s_U.
```

Functional calculus and `(lambda-alpha)^2/lambda<=lambda-alpha` imply

```text
g_cut^T Q_UU^-1 g_cut
 <=rho^2 s_U^T(Q_UU-alpha I)s_U
 =rho^2 b cut(U).                              (cut response energy)
```

Likewise, below a spectral cutoff `beta`,

```text
||P_<beta Q_UU^(-1/2)g_cut||_2
 <=min{rho sqrt(b cut(U)),
        sqrt(rho)(beta-alpha)/sqrt(beta)}.
```

Thus a small cut can reduce both the residual numerator and the energy of a
*static pure-cut* response.  It still changes only logarithms in an ordinary
worst-case CG convergence bound, and it does not apply to the incremental
right-hand side after a face expansion: padding cancellation turns that
increment into the frontier load `(0,D_B e_B^U)`, which need not contain the
factor `Q-alpha I`.  This is the exact point at which a fixed-face cut-aware
improvement stops short of a cross-face `CenterLift` theorem.

There is also a genuine optimizable scalar family.  For `gamma>=0`, put

```text
z_gamma=y+gamma rho 1_U.
```

Its normalized face load is exactly

```text
g_gamma
 =alpha e_v/sqrt(d_v)+rho(gamma Q_UU-alpha I)s_U.  (scalar-shift family)
```

For an eigenvalue interval `[alpha,beta]`, the minimax choice and value are

```text
gamma_beta=2alpha/(alpha+beta),
min_gamma max_{lambda in [alpha,beta]} |gamma lambda-alpha|
  =alpha(beta-alpha)/(alpha+beta).
```

Indeed the optimum equioscillates at the two endpoints.  Hence

```text
||P_<beta g_gamma_beta||_2
 <=alpha/sqrt(d_v)
   +rho alpha(beta-alpha)/(alpha+beta) sqrt(vol(U))
 <=alpha/sqrt(d_v)+alpha sqrt(rho).                (balanced source)
```

This is a valid parameter balance for a deterministic Chebyshev/CG
*fixed-face* solve.  It is stronger than `gamma=1` when `beta` is much larger
than `alpha`, and the residual can be checked through the lower-envelope
adapter.  It is not yet the requested runtime balance.  First,
`gamma_beta<1` for `beta>alpha`, and in degree coordinates

```text
H_U z_gamma
 =alpha e_v-(1-gamma)alpha rho d_U
   +gamma rho b d_out,U;
```

the interior forcing is signed.  Thus the one-sided positive response and
monotone-debt arguments no longer apply.  Second, at the manuscript tolerance
`eta=Theta(alpha sqrt(rho eps_obj))`, the last display is still too large by
a constant factor uniformly for `eps_obj<=1`; the seed term cannot be removed
by this graph-independent scalar estimate.  Third, changing faces changes
both `s_U` and the cut term, so even favorable per-face degrees still need a
cross-face response ledger.

The broom regression makes the second point quantitative rather than merely
using the triangle inequality.  At `alpha=10^-3` and low cutoff `20alpha`,
the positive cut source has low-band mass `45.4` times the unit-accuracy face
tolerance.  The minimax scalar reduces this to `24.8`, while even the oracle
least-squares scalar for the *actual* low eigenspace leaves a factor `22.6`.
At `alpha=10^-5` the same three ratios are `45.3`, `24.8`, and `22.6`.
Computing the oracle scalar also presupposes the low projector, so it is only
a diagnostic.  Thus a scalar shift is a useful favorable-instance parameter,
but the one-cut broom still blocks a graph-uniform cutoff at the certified
accuracy.

#### A scalar shift cannot finance the low branch from cut mass

There is a separate, exact stop for the tempting shifted-refinement
implementation.  For any `sigma>0`, the ordinary inverse has the identity

```text
Q^-1=(Q+sigma I)^-1+sigma Q^-1(Q+sigma I)^-1.   (shift split)
```

The first term is the rented, better-conditioned solve; the second is the
positive low-tail correction.  On an eigenvector of eigenvalue `lambda`, the
fraction of the exact response left in the tail is

```text
sigma/(lambda+sigma).                            (tail fraction)
```

Meanwhile the condition number of the rented system is at least, up to the
constant upper endpoint,

```text
kappa_sigma=(1+sigma)/(alpha+sigma).
```

To make its Chebyshev degree `O(1/tau)` for `tau>=sqrt(alpha)`, one needs
`alpha+sigma=Omega(tau^2)`.  Therefore, on a mode
`lambda<=c alpha`, every nontrivial choice `tau^2=Omega(alpha)` leaves a
constant fraction of the full slow response in the buy term.  If instead
`sigma=o(alpha)`, the first term still needs
`Omega(1/sqrt(alpha))` iterations.  There is no scalar-shift interval in
which the high solve is accelerated and the low response simultaneously
acquires a factor `tau`.

This is realized by the smallest possible cut/frontier example:

```text
Q=[[a,-b],[-b,a]],
a=(1+alpha)/2,  b=(1-alpha)/2,
g=e_2.
```

Its eigenvalues are exactly `alpha` and one, the slow eigenvector is
`(1,1)/sqrt(2)`, and `g` is a single newly admitted frontier coordinate with
nonzero slow projection.  Taking `sigma=alpha` improves the shifted condition
number by a factor two but leaves exactly half of the `1/alpha` slow response
in the tail.  Alternating positive row settlements contract by only
`(b/a)^2=1-Theta(alpha)`, so materializing that tail by the literal monotone
implementation costs `Omega(1/alpha)` row touches, independently of the
amplitude of `g`.  Exact two-row Schur elimination is constant work, which is
why this is a lower bound on the proposed *shift plus row-settlement*
realization, not on all algorithms.

The same conclusion can be stated as a positive mass inequality.  If
`h>=0`, put

```text
x_sigma=(Q_UU+sigma I)^-1 h,
w_sigma=sigma Q_UU^-1 x_sigma.
```

Using `Q_UU sqrt(d_U)>=alpha sqrt(d_U)` and inverse positivity gives

```text
sqrt(d_U)^T x_sigma
  <=sqrt(d_U)^T h/(alpha+sigma),
sqrt(d_U)^T w_sigma
  <=sigma sqrt(d_U)^T h/[alpha(alpha+sigma)].
```

This is a valid source-mass bound, but when `sigma>=alpha` its multiplier is
`Theta(1/alpha)`, not `O(tau/alpha)` at `tau=sqrt(alpha)`.  The canonical
conservation theorem may sum `sqrt(d)^T h` across batches and the closed
boundary reporter may exploit that sum; neither inequality applies the
dense old-face response.  A true `B tau/alpha` term must therefore come from
an additional structural statement such as weighted port packing,
orthogonal response-energy packing, or a persistent separator hierarchy.
The comb shows that cut cardinality alone cannot supply constant response
rank, while the broom shows that a one-edge cut alone cannot remove the slow
mode.  Neither refutes the open implicit `CenterLift` primitive.

Three cautions prevent `(cut source)` from being mistaken for the missing
algorithm.

1. When a face grows, `d_out,U` loses the old cut incidences and gains the new
   ones.  The *right-hand-side update* in the `z` formulation is therefore
   signed, even though `z^T-z^U=y^T-y^U>=0`.  It is not a monotone stream of
   independent cut loads.
2. The seed term remains source-visible in the low eigenspace.  On the
   ballasted broom, the cut has one edge and
   `lambda_min(Q_UU)=(1+o(1))alpha`; the positive Perron mode has constant
   normalized root coordinate.  Hence the projection of
   `alpha e_v/sqrt(d_v)` onto this mode is
   `Theta(alpha/sqrt(d_v))`, at the same scale as the certified face residual
   tolerance (and the cut term has the same sign on that mode).  Replacing
   the full right-hand side by `(cut source)` therefore does not justify a
   cutoff above `Theta(alpha)` for a fresh solve.  The reduced symmetric
   regression in `witnesses.py` records this source-alignment ratio.
3. Applying a cut source to all relevant boundary labels *is* the
   Dirichlet-to-Neumann response operation.  On the comb tree, a path anchor
   with one exposed leaf per anchor vertex has cut-response rank equal to the
   anchor size and every exact harmonic column is dense.  This rules out a
   universal constant-rank bank or free explicit response table (not an
   implicit tree recurrence).  At the opposite extreme, literal nonnegative
   row settlement is also insufficient: already the first shifted rung on a
   single edge alternates residual between its two rows and needs
   `Omega(1/alpha)` row touches for a constant reduction, although the exact
   scalar Schur solve takes one operation.  An aggregate Chebyshev sweep
   restores `O(1/sqrt(alpha))` only on a fixed face.

Accordingly, cut size or `sum d_out` is a useful *source* parameter but not a
standalone work parameter.  A valid positive theorem must additionally name
the implementation cost of its changing Dirichlet-to-Neumann map---for
example separator width, treewidth, cut rank plus a charged application
scheme, or the `PositiveFrontierRentOrBuy` contract.  The ballasted broom does
not refute such an implicit tree implementation; the one-edge and comb tests
only refute the two specific realizations just described.

#### Global shifted obstacle prox: an exact rent--buy identity

The scalar-shift stop above concerns one inverse decomposition followed by a
literal settlement of its tail.  It does **not** rule out repeatedly applying
the shifted *obstacle resolvent*.  That global interpretation gives a cleaner
and fully rigorous form of the requested balance.

Let

```text
Phi(x)=1/2 x^T Qx-c^T x+I_{x>=0}(x)
```

and, for `sigma>0`, define

```text
T_sigma(x)=argmin_(z>=0) {Phi(z)+(sigma/2)||z-x||_2^2}.
```

Call `x` a lower subsolution if `0<=x<=x*` and
`r_i=(c-Qx)_i>=0` wherever `x_i>0`.  The Stieltjes obstacle map is isotone in
its right-hand side.  Since `T_sigma(x*)=x*`, and since `x` itself is a
subsolution of the shifted LCP with matrix `Q+sigma I` and right-hand side
`c+sigma x`, comparison gives

```text
x<=T_sigma(x)<=x*.                              (prox monotonicity)
```

There is also an exact global contraction, including all face changes inside
the prox call.  If `z=T_sigma(x)`, optimality gives

```text
sigma(x-z) in partial Phi(z),       0 in partial Phi(x*).
```

Strong monotonicity of `partial Phi` and Cauchy--Schwarz imply

```text
||z-x*||_2 <= [sigma/(alpha+sigma)] ||x-x*||_2. (prox contraction)
```

Thus, with `sigma=tau^2`, a prescribed energy/objective accuracy takes

```text
J=O_tilde(1+tau^2/alpha)
```

global prox calls.  This is the source of the buy factor; it is not an
assumed low-tail mass estimate.

The active-set form is especially revealing.  Put `d=z-x` and
`r=c-Qx`.  On the final prox support `U`,

```text
(Q_UU+sigma I)d_U=r_U,
r_j-Q_jU d_U<=0                       for j outside U.
```

Start on the support of `x` and solve the first equation on an intermediate
face `U`.  If a boundary batch `B` has shifted violation

```text
g_B=r_B-Q_BU d_U>0,
```

then on `T=U dot-union B` the exact updated correction is

```text
d_T=[d_U;0]+(Q_TT+sigma I)^-1[0;g_B]>=[d_U;0].
                                                        (positive prox lift)
```

Consequently every inner expansion is safe and monotone.  When all exterior
violations are quiet, the result is the global `T_sigma(x)`, not a biased
fixed-face surrogate.  Its new unshifted residual equals `sigma d_U>=0` on
the positive support and is nonpositive outside, so the committed point is
again a lower subsolution for the next outer call.

The existing lower-envelope publication adapter applies without a new proof.
In degree coordinates the shifted face operator is

```text
H_UU+sigma D_U,
```

and

```text
(H_UU+sigma D_U)1 >=(alpha+sigma)d_U.
```

Thus, if a signed CG/Chebyshev candidate has normalized residual at most
`eta_sigma`, subtracting `eta_sigma/(alpha+sigma) 1` and joining with the
historical subsolution gives a certified lower shifted correction.  With the
same boundary ratio

```text
R_U=max_(j in boundary U) d_U(j)/sqrt(d_j),
```

the choice

```text
eta_sigma=(alpha+sigma) theta/[16 max{1,R_U}]
```

preserves the earlier `theta/16` normalized boundary-leakage bound, safe
score threshold, and quiet KKT logic.  Hence Chebyshev, CG, direct tree
Schur, and rent--buy candidates all publish through the already-closed
residual/retraction interface.  This repairs numerical semantics; it does
not charge repeated face reads inside one closure.

This proves the following exact primitive theorem.

```text
ShiftedProxClosure(tau):
  starting from a lower subsolution, compute T_(tau^2)(x), including every
  no-miss positive face expansion, in O_tilde(vol(U_out)/tau) work.

If ShiftedProxClosure(tau) is available, total work is
  O_tilde((1+tau^2/alpha) M/tau)
  =O_tilde(M/tau+M tau/alpha).                 (prox rent--buy theorem)
```

The optimizer is `tau=sqrt(alpha)`.  Unlike the fixed-face Richardson
calculation, this theorem already includes the outer active-set semantics;
unlike the one-shot shift split, its low branch is paid by the contraction of
the global strongly monotone obstacle operator.  The only conditional line is
the stated work bound for a whole closure.

The words "whole closure" are essential.  Repeating

```text
solve the current shifted face; add its positive boundary; restart
```

does not satisfy the primitive.  On an endpoint path the exact boundary has
only the next path vertex, so a prox point whose support contains `k` new
vertices forces `k` nested inner faces.  Fresh Chebyshev on each such face
recreates the path restart ledger even though there are only a constant
number of *outer* prox calls at `sigma=alpha`.  The regression at
`alpha=10^-3`, 48 vertices, and `sigma=alpha` reaches 45 vertices in the first
prox through 44 singleton inner expansions; all 47 possible expansions over
the entire run occur only once, while 27 outer calls achieve relative error
`5.6e-9`.  Its observed Euclidean contraction is `0.5000002` versus the exact
bound `1/2`, and the prox KKT error is below `6e-18`.  Incremental path Schur
state processes those expansions once; restarted shifted CG does not.

A certified lower approximation is also sufficient, but it makes the
remaining response requirement explicit.  If `z=T_sigma(x)` and an oracle
returns `x<=z_tilde<=z` with

```text
||z-z_tilde||_2
 <=[alpha/(2(alpha+sigma))] ||x-x*||_2,
```

then its contraction factor is at most
`1-alpha/(2(alpha+sigma))`.  For a shifted lower solve with nonnegative debt

```text
e=r_U-(Q_UU+sigma I)d_tilde_U>=0,
```

the missing correction is exactly `A_U^-1e`, where
`A_U=Q_UU+sigma I`.  A full entrywise Green summary is **not** needed for
capped termination.  For exact restricted-center certification, put
`C_v=-Q_vU>=0`.  Positivity of the principal shifted Schur complement and
Cauchy--Schwarz in the `A_U` metric give

```text
0<=C_v A_U^-1 e
  <=sqrt(a+sigma)||e||_(A_U^-1)
  <=sqrt((a+sigma)/(alpha+sigma))||e||_2,       (scalar debt envelope)
a=(1+alpha)/2.
```

Thus any approximate exterior score below the negative of this computable
radius is rigorously quiet for the exact completion on the current face.  If
every row passes this test, that exact restricted completion is globally
quiet, while
`||A_U^-1e||_(A_U)^2<=||e||_2^2/(alpha+sigma)` certifies its solve error.
This leverage statement is useful for exact restricted-center or zero-margin
support certification.  It is not needed to terminate the capped objective.

Indeed, suppose merely that the current lower correction `d>=0` is supported
on `U`, has `e_U=r_U-A_Ud_U>=0`, and every **current** exterior score
`s_v=r_v-A_vU d_U` is nonpositive.  For the full shifted obstacle objective

```text
F(d)=1/2 d^T A d-r^T d+I_(d>=0),    A=Q+sigma I,
```

let `d_prox*` denote the exact global prox correction.  The smooth gradient
is `-e_U` on `U` and `-s_v>=0` outside.  At an exterior zero coordinate the
orthant normal cone is `(-infinity,0]`; choosing normal component `s_v`
cancels the exterior gradient.  Hence

```text
(-e_U,0) in partial F(d),
F(d)-F(d_prox*) <= ||e_U||_2^2/[2(alpha+sigma)],
||d-d_prox*||_2 <= ||e_U||_2/(alpha+sigma).   (global capped stop)
```

The first inequality follows by minimizing the strong-convexity lower model;
the distance bound follows from strong monotonicity.  It includes every row
which would become positive after solving the old debt and every descendant
cascade.  In canonical point-source RPPR the full exterior premise is local:
the source is seeded, and a nonneighbor of `U` has no coupling and the known
strictly negative floor score `-alpha rho sqrt(d_v)`.  Scanning all incident
edges of `U` therefore checks every potentially positive exterior row.

Visible positive batches have a fully local persistent append.  If
`g_tilde_B=r_B-Q_BU d_tilde_U>0`, append `B` with correction zero.  Then

```text
d_tilde_T=[d_tilde_U;0],
e_T=[e_U;g_tilde_B]>=0,
||e_T||_2^2=||e_U||_2^2+||g_tilde_B||_2^2,
```

and every old exterior score is unchanged.  Only the newly incident rows
must be exposed.  Comparing with the exact mutually `A`-orthogonal expansion
packets gives the global bank

```text
sum_B ||g_tilde_B||_2^2 <=(1+sigma)alpha.       (visible-source square bank)
```

This removes full Green-debt maintenance from capped termination.  The square
bank is over one nested prox call.  Its checkpoint count
`1+(1+sigma)alpha/beta^2` is valid only for epochs which reset `e=0` (or below
a fixed fraction of `beta`) and then perform only zero-appends until the next
trigger; nonnegativity alone does not make an intervening residual-changing
rent step an `l2` contraction.

The remaining general interface can therefore be weakened to
`AmortizedLowerShiftedApply(tau)`: maintain a certified-lower accelerated
shifted solve through visible zero-appends; rescan, append every positive
current score, and reduce `||e||` until the global capped stop holds, with all
response work and rescans totaling `O_tilde(M/tau)`.  Exact zero-margin
support discovery still needs an exact solve or interval refinement.  No
general-graph implementation of this weaker producer is currently proved.

There is a sharp reason that ordinary projected gradient does not implement
the primitive at the advertised price.  With
`L>=lambda_max(Q+sigma I)`, its map

```text
G(z)=[(I-(Q+sigma I)/L)z+(c+sigma x)/L]_+
```

is isotone because `I-(Q+sigma I)/L` is entrywise nonnegative.  Starting at a
lower subsolution, it is therefore perfectly support-safe.  But on the slow
mode its contraction is only

```text
1-(alpha+sigma)/L.
```

For `sigma=tau^2>=alpha`, constant progress takes `Omega(1/tau^2)` sweeps,
not `O(1/tau)`.  The shifted version of the positive-walk barrier gives the
same conclusion for every universal nonnegative polynomial settlement.  A
valid `ShiftedProxClosure(tau)` must consequently use signed square-root
acceleration together with a certified lower envelope/delayed response, or a
structural direct elimination.  Merely observing that projected gradient is
monotone would yield `M/tau^2`, destroying the desired balance.

The primitive closes unconditionally on a path.  Every prox support is an
interval containing the old support: a disjoint positive component would
have only the negative nonseed baseline as its right-hand side, contradicting
inverse positivity.  On an interval, the shifted equations are tridiagonal.
Affine `3 x 3` transfer matrices (equivalently two one-sided continued-fraction
Schur states around the seed) compose associatively.  Appending an endpoint
updates the relevant product and both endpoint violations in constant
arithmetic; one final backward sweep materializes the correction.  Therefore
one exact prox closure costs `O(vol(U_out))`, and all outer calls cost

```text
O_tilde(M(1+tau^2/alpha))
 <=O_tilde(M/tau+M tau/alpha),       0<tau<=1.  (path theorem)
```

Taking the unshifted limit recovers the earlier one-pass path obstacle solve.
On a general tree, scalar Schur factors along a changed root--leaf path are
Möbius maps and can likewise be composed by a top tree.  What is not yet
proved is exact no-miss reporting for all quiet side children whose affine
thresholds change under each positive Green update; scanning those children
after every leaf addition is quadratic on a comb.  Thus the new prox theorem
does not give an output-linear *exact one-shot* tree closure for free.
The target approximate solve nevertheless closes on trees by retaining
threshold batches, as follows.

### 5.3.1 Arbitrary-source chain depth and the tree rent--buy theorem

The block-Cholesky depth argument is not intrinsically a point-source
argument.  The point source in the manuscript removes a condition-number
factor from the constant, but an arbitrary initial block only places that
factor inside a logarithm.

Let `A` be any Stieltjes matrix with

```text
mu I <= A <= L I.
```

For a load `r`, let `d*` solve the obstacle problem
`min_(d>=0) (1/2)d^T A d-r^T d`.  Start with a block `B_0` containing every
coordinate with initially positive load, solve exactly on the current face,
and thereafter admit **all** positive exterior residuals as the next batch.
Extend the resulting nested sequence to `S=supp(d*)`.  If `d^(J)` is the
exact face solution after `J` later blocks and

```text
q=(sqrt(2L/mu)-1)/(sqrt(2L/mu)+1),
```

then

```text
||d*-d^(J)||_A
 <= (4L/mu) q^J ||d*||_A.              (arbitrary-source depth)
```

Here is the proof, including the constant that matters for the outer
composition.  Use the block-respecting factorization
`A_SS=C C^T` and write the positive pivot vectors as `z_k`.  The exact
completion-of-squares identity is

```text
||d*-d^(J)||_A^2=sum_(k>J)||z_k||^2.
```

Retain only the diagonal and first block subdiagonal of `C`, calling the
result `C_hat`.  The Stieltjes inverse order and the block-row map give

```text
||C_hat^-1||<=1/sqrt(mu),       ||C_hat||<=sqrt(2L).
```

Because every still-future coordinate had nonpositive residual before the
preceding all-positive batch, causality gives

```text
C_hat z <= [g_0;0;...;0].
```

The degree-`J-1` Chebyshev approximation to the inverse of
`C_hat C_hat^T`, whose spectrum is in `[mu,2L]`, cannot reach beyond block
`J-1`.  Therefore

```text
||P_(>J) z||
 <= (2 sqrt(2L)/mu) q^J ||g_0||.
```

Finally `g_0` is a restriction of `r_S=A_SS d*`, and
`A^2<=L A`, so `||g_0||^2<=L||d*||_A^2`.  Squaring proves the displayed
claim with slack.  Notice that no support size, complementarity margin, or
single-source sign remains in the bound.  If initially positive coordinates
are exposed only on the current graph boundary, including all of them in
`B_0` is safe: zero padding preserves the lower subsolution and a nonboundary
nonseed row still has negative canonical load.

Apply this lemma to one proximal correction.  Let

```text
A=Q+sigma I,       mu=alpha+sigma,       L<=1+sigma<=2,
r=c-Qx,            d*=T_sigma(x)-x.
```

For a lower subsolution, every exact nested-face correction obeys
`0<=d^(J)<=d*`, so the committed point stays between `x` and `x*`.  Choose

```text
epsilon_in=alpha/(2 sqrt(L mu)).
```

After

```text
J=O(sqrt(L/mu) log(L/(alpha mu)))
```

all-positive batches, the arbitrary-source depth lemma gives
`||d^(J)-d*||_A<=epsilon_in||d*||_A`.  Coordinatewise monotonicity implies
`||d*||_2<=||x-x*||_2`, hence

```text
||x+d^(J)-x*||_2
 <=[1-alpha/(2(alpha+sigma))] ||x-x*||_2.   (inexact prox contraction)
```

Thus `O_tilde(1+sigma/alpha)` inexact outer calls suffice, exactly as for the
exact prox up to a factor two in the contraction deficit.

On an ambient tree, every reached face is a connected subtree and an exact
face solve, all boundary residuals, and its certificate cost
`O(vol(U))` by leaf elimination.  With `sigma=tau^2`, one prox call therefore
costs

```text
O_tilde(M/sqrt(alpha+tau^2)) <= O_tilde(M/tau),
```

and the whole deterministic algorithm costs

```text
O_tilde(
  M(1+tau^2/alpha)/sqrt(alpha+tau^2)
 )
 <= O_tilde(M/tau+M tau/alpha),             0<tau<=1.
                                                        (tree balance theorem)
```

At `tau=sqrt(alpha)` this is `O_tilde(M/sqrt(alpha))` with no
subpolynomial solver factor.  More generally, if every reached face comes
with a width-`w` chordal elimination order, replace `M` by
`M_w=M+w^2|S*|`; supplied constant treewidth gives the same requested bound.

The global `alpha` in this theorem can in fact be replaced by the final
formed-face gap

```text
mu_* = lambda_min(Q_(S*,S*)).
```

This improvement applies to both layers, not just to a fresh face solve.
If `0<=x<=x*` and `y=T_sigma(x)`, isotonicity gives
`x<=y<=x*`, so both `y-x*` and `x-x*` are supported on `S*`.  The optimality
conditions for `y` and `x*`, monotonicity of the orthant normal cone, and
`Q_(S*,S*)>=mu_* I` give

```text
(mu_*+sigma)||y-x*||_2^2
 <= sigma <x-x*,y-x*>,
||T_sigma(x)-x*||_2
 <=[sigma/(mu_*+sigma)]||x-x*||_2.          (formed-face prox contraction)
```

Every correction face is a principal submatrix of `S*`, so the arbitrary-
source depth lemma simultaneously improves from `alpha+sigma` to
`mu_*+sigma`.  With `L<=1+sigma`, choose

```text
epsilon_in=mu_*/(2 sqrt(L(mu_*+sigma))).
```

Then the committed nested-face correction obeys

```text
||x+d^(J)-x*||_2
 <=[1-mu_*/(2(mu_*+sigma))]||x-x*||_2,
J=O_tilde(1/sqrt(mu_*+sigma)).
```

Hence any implementation whose structural cost is `A` per exact face has

```text
O_tilde(
 A(1+tau^2/mu_*)/sqrt(mu_*+tau^2)
)
 <= O_tilde(A/tau+A tau/mu_*).               (formed-face balance)
```

Taking `tau=sqrt(mu_*)` gives `O_tilde(A/sqrt(mu_*))`, which can be
polynomially smaller than `A/sqrt(alpha)` on a well-grounded final support.
If the response-production and repeated-outer ledgers have different charged
coefficients, the same proof gives the literal user-requested form

```text
T(tau)=R+A/tau+B tau/mu_*,
tau_opt=sqrt(A mu_*/B),
T(tau_opt)=R+2 sqrt(A B/mu_*),
```

with `tau_opt` clipped to the algorithm's allowed interval.  This optimization
is substantive only when `A` and `B` are independently proved work ledgers;
renaming the same uncharged dense response in two ways does not qualify.

No advance eigenvalue certificate is required for the structural algorithms.
Try `gamma=1,1/2,1/4,...`, set `sigma=tau^2=gamma`, and run the number of
inner/outer steps justified under the hypothesis `mu_*>=gamma`.  Every failed
phase still commits a monotone lower point, so it is safe.  Apply the existing
computable residual/quiet-KKT certificate; on failure halve `gamma`.  Once
`gamma<=mu_*`, the preceding proof guarantees acceptance.  Since

```text
sum_(gamma>=Theta(mu_*)) 1/sqrt(gamma)=O(1/sqrt(mu_*)),
```

the trials cost only an additional logarithmic accuracy/certification factor.
This is an a-posteriori algorithmic adaptation, not the unsafe practice of
treating the current face eigenvalue (an upper bound on `mu_*`) as a lower
certificate.  It upgrades the tree, supplied bounded-width, low-cycle, and
dynamic-fill-reach branches below.  For a hypothetical general-graph
`ShiftedProxClosure`, it likewise replaces the conditional outer ledger
`M tau/alpha` by `M tau/mu_*`; implementing that closure remains open.

Concretely, the certified structural algorithm is:

```text
GapAdaptiveShiftedProx(theta):
  x <- 0                                      # certified lower subsolution
  for gamma = 1, 1/2, 1/4, ..., alpha:
    sigma <- gamma; tau <- sqrt(gamma)
    repeat O_tilde(1) outer calls:
      r <- c-Qx
      start with supp(x) and every positive row of r
      repeat O_tilde(1/sqrt(gamma)) nested batches:
        solve the shifted current face exactly (or use certified retraction)
        admit every positive exterior residual
      commit the resulting lower correction to x
    if QuietKKT_theta(x): return x
```

The loop never needs to evaluate `mu_*`.  At the final fallback
`gamma=alpha` its premise is automatic.  On a structural face class the
per-phase bound is `O_tilde(A/sqrt(gamma))`; with fresh CG it is
`O_tilde(M/gamma)`, as quantified below.

There is also a sharper low-cycle specialization.  In normalized
coordinates, choose a spanning tree `F` of a connected reached face and
write

```text
Q_U=B_U+c Z_U Z_U^T,
B_U=alpha I+c D_U^-1/2(L_F+D_(out,U))D_U^-1/2,
```

where the columns of `Z_U` are
`D_U^-1/2(e_i-e_j)` for the `k_U` non-tree internal edges and
`c=(1-alpha)/2`.  The off-diagonal graph of `B_U` is a grounded tree and
`B_U>=alpha I`.  Its two directed cavity messages per edge give a pair Green
query after an LCA/path-product preprocessing.  Explicitly, if `uv` is a
tree edge and the source `p` lies on the `u` side, then

```text
(B_U^-1)_(v,p)/(B_U^-1)_(u,p)=-b_(uv)/D_(v->u)>0,
D_(v->u)=b_(vv)-sum_(r~v,r!=u)b_(vr)^2/D_(r->v).
```

The diagonal Green entries follow by including every neighbor in the same
cavity formula.  Therefore all entries of

```text
W_U=c^-1 I+Z_U^T B_U^-1 Z_U
```

cost only `O_tilde(k_U^2)` after one linear tree factorization.  Define
`omega_mat` to be any fixed admissible exponent for exact matrix
multiplication over the ordered input field.  Recursive block inversion of
the SPD core costs `O(k_U^omega_mat)`: every leading block and recursive Schur
complement is SPD, so no pivot search or square root is needed.  In degree
coordinates the update is `H_U=Bbar_U+c C_U C_U^T`, where `C_U` is the
ordinary feedback-edge incidence matrix; all apparent degree radicals cancel.
After the core solve, use a *single* final tree solve with sparse load
`b-Z_Uy`; materializing the `k_U` full Green columns is unnecessary.  One
exact restricted center and its complete boundary-key scan consequently cost

```text
O_tilde(vol(U)+k_U^omega_mat).                 (cycle-rank face solve)
```

The live state is `O(vol(U)+k_U^2+S_MM(k_U))`, with `S_MM` the chosen
multiplication routine's workspace (quadratic for standard recursive
schedules).  These are exact ordered-field arithmetic/comparison bounds;
they do not imply bit complexity or floating-point stability.  If `omega`
denotes only the infimum exponent, write `k^(omega+o(1))` or
`O(k^(omega+epsilon))`, not silently `O_tilde(k^omega)`.

Let `U_0,...,U_J` be only the canonical maximal threshold faces required up
to the manuscript's certified objective-floor/capping stop, and suppose
they lie in a charged reference support of volume `M` and cyclomatic number
`k`.  Rebuilding the tree/core and scanning all boundary incidences at every
batch is support-local and gives

```text
O_tilde(J(M+k^omega_mat))
 =O_tilde((M+k^omega_mat)/sqrt(alpha)).        (cycle-rank theorem)
```

The equality uses the independent capped threshold-depth theorem.  It does
**not** claim that face `J` equals the unrestricted exact support.  This
removes the small `o(1)` factor whenever
`k^omega_mat=O_tilde(M)`, strictly beyond constant feedback-edge rank.  If the
depth theorem has a common certified final-face lower bound `mu_bar`, the same
argument replaces the last display by
`O_tilde((M+k^omega_mat)/sqrt(mu_bar))`; no eigenvalue is needed to execute the
exact faces.  A shifted face has the identical decomposition after replacing
`alpha` by `alpha+sigma`, so the earlier formed-face prox curve also remains
valid with structural coefficient `M+k^omega_mat`.

This is sharper than merely observing `treewidth<=k+1`: a generic supplied
width factorization charges about `k^2|U|` on each face, whereas the cycle
decomposition confines every non-tree dense operation to the `k x k` core
and materializes the full solution only in the final tree substitution.

For a supplied legal singleton trace, an online discovery tree plus rank-one
updates of the dense cycle core maintains an *implicit exact center* in
`O_tilde(Mk^2+k^3)` total work.  That statement alone is not a no-miss
reporter: a quiet exterior vertex can have many attachments to the reached
tree without contributing an internal cycle.  A one-shot fast inverse of the
final core also does not output all intermediate exact centers, so the
fast-multiplication theorem does not improve that chronological bound.  The
rebuild-per-maximal-batch theorem avoids the reporter gap by scanning all
boundary incidences, already within its `M/sqrt(alpha)` term.  Exact
decomposition checks are in `cycle_rank_response_verify.py`.

This proof permits a fresh structural face elimination at each of the
`O_tilde(1/sqrt(mu))` batches.  The already-verified dynamic heavy-path
backend can retain the factorization instead: for arbitrary local loads its
two-scalar Schur state becomes the homogeneous affine transfer

```text
[A_i]   [a_i  0  -w_(i+1)^2] [A_(i+1)]
[B_i] = [h_i w_(i+1)  0     ] [B_(i+1)],
[C_i]   [1    0       0     ] [C_(i+1)]

delta_i=A_i/C_i,             eta_i=B_i/C_i.
```

A light child contributes `-w^2/delta` to the parent diagonal and
`+w eta/delta` to its load.  Ordered `3 x 3` products therefore extend the
proved HSEG-LDL heavy-path potential without changing its structural
`O(M log^2 M)` admission charge.  This is a useful implementation
improvement, not needed to obtain the asymptotic theorem because repeated
boundary scans already cost `O_tilde(M/sqrt(mu))`.

There is a broader output-sensitive direct branch which makes dynamic fill
explicit.  Order vertices by their actual admission time and let

```text
A_j=Q_(U_j,U_j)+sigma I=L_j L_j^T,
F_chol=max_j nnz(L_j).
```

For a batch `B_j` of size `b_j`, write

```text
A_j=[A_(j-1) E_j; E_j^T G_j],
W_j=L_(j-1)^(-1)E_j,
S_j=G_j-W_j^T W_j.
```

Then old factors are retained *exactly* and

```text
L_j=[L_(j-1) 0; W_j^T chol(S_j)].
```

Let `rho_j` be the number of old-factor nonzeros in the elimination-tree
closure reached from the nonzeros of `E_j`.  Partial triangular substitution
and the small Gram/Schur factorization cost at most

```text
R_j=O(b_j^2 rho_j+b_j^3),
R_chol=sum over all admissions R_j.                 (dynamic fill reach)
```

This is the same sparse-closure quantity exploited by the AMPS augmented
principal-update method; here it follows directly from chronological block
Cholesky.  It is observable during the run and does not assume that a dense
response is free.

The factors depend on the shifted operator but not on the right-hand side,
so they persist across all outer proximal calls.  One exact face solve costs
`O(F_chol)`, and one complete boundary scan costs `O(M)`.  Combining the
arbitrary-source batch-depth lemma with the inexact-prox contraction gives
the unconditional *instance-parameterized* bound

```text
O_tilde(
  R_chol+(F_chol+M)(1+tau^2/mu_*)/sqrt(mu_*+tau^2)
)
 <= O_tilde(
  R_chol+(F_chol+M)/tau+(F_chol+M)tau/mu_*
),                                                       (fill-reach balance)
```

for `sigma=tau^2` and `sqrt(alpha)<=tau<=1`.  At
`tau=sqrt(mu_*)`, every instance satisfying

```text
F_chol=O_tilde(M),       R_chol=O_tilde(M/sqrt(mu_*))
```

removes the small-`o(1)` factor.  This strictly extends a bounded-width
promise when the actual chronological closure is small, and it is useful for
power-grid/mesh-like instances with localized fill.  It is not a general
sparse-graph theorem: expanders or adversarial admission orders may have
`F_chol=Theta(|S*|^2)` and equally large closure work.  Reordering after each
face may reduce static fill but destroys the displayed retained-prefix
factorization unless its update cost is charged separately.

Fresh Chebyshev/CG does **not** obtain the same result on a general graph.
Put `nu=mu_*+sigma`.  One shifted face solve costs
`O_tilde(M/sqrt(nu))`, there are `O_tilde(1/sqrt(nu))` faces per prox, and
there are `O_tilde(nu/mu_*)` prox calls.  The factors cancel exactly:

```text
T_fresh(sigma)
 =O_tilde((M/sqrt(nu))(1/sqrt(nu))(nu/mu_*))
 =O_tilde(M/mu_*),                              (fresh-face cancellation)
```

independent of the shift.  This is still useful: on **every** graph,
`mu_*>=sqrt(alpha)` implies `T_fresh<=O_tilde(M/sqrt(alpha))`, and the
descending guess/KKT schedule recognizes that regime without a prior
certificate.  It also proves that Chebyshev/CG exploits a genuinely narrower
final formed-face spectrum as far as fresh solves possibly can.  But when
`mu_*=Theta(alpha)`, as on the ballasted broom, it returns `M/alpha`; tuning
`sigma` or the current-face eigenvalue cannot create a missing square root.
The tree theorem works because structural elimination makes one face linear;
the general low-gap theorem still needs persistent Krylov/Schur reuse across
those inner faces.  Exact output-linear tree no-miss reporting would improve
the special theorem further, but its `LazyTreePromise` interface is not
required for the displayed balance.

### 5.4 Low Dirichlet gap as an envelope certificate

A low `delta_U` asserts existence of a slowly escaping vector in `U`; it does
not assert that the PPR/RPPR source is aligned with that vector or that the
current boundary demand is small.  A connected face may contain a weakly
attached whisker creating the low mode while the source drives an unrelated
unexplored branch.  Any low-gap completion theorem needs at least a
source-alignment or boundary-flux quantity in addition to `delta_U`.

The executable witness `witnesses.py` makes both failures concrete.  A
`K_m` face with a path attached opposite the seed has
`delta_U=Theta(m^{-2})`, yet the first omitted path vertex has strictly
positive exact boundary residual and a tail of length `Theta(1/sqrt(alpha))`
can remain active.  A chain of `k` weakly linked cliques has `Theta(k)`
eigenvalues below `sqrt(alpha)` for suitable cluster size, so a
graph-independent fixed-rank low-mode correction cannot cover the bad
spectrum.

These examples do not depend on numerical coincidence.  For the first one,
let `U=K_m` and give one distinguished clique vertex a single edge to an
outside path.  The distinguished ambient degree is `m` and every other
clique degree is `m-1`.  Symmetry reduces the Perron eigenvalue `lambda` of
the killed normalized adjacency on `U` to

```text
lambda^2 - ((m-2)/(m-1)) lambda - 1/m = 0.
```

Since the polynomial at one is `1/(m(m-1))` and its derivative between the
root and one is bounded above and below by positive constants, its root
satisfies `1-lambda=Theta(m^-2)`.  Hence
`delta_U=Theta(m^-2)`.  At `rho=0`, the face inverse is strictly positive and
the omitted neighbor has residual

```text
-Q_leaf,U x_U > 0.
```

Strict positivity persists for all sufficiently small positive `rho`.  On
the full finite clique--path graph, the inverse is again strictly positive,
so the whole chosen tail remains active for a sufficiently small positive
`rho`.  Thus neither low `delta_U` nor positivity/reachability of the face
certifies completion.

For the second example, take `k` cliques of size `m` and join consecutive
cliques by one edge.  The `k`-dimensional subspace whose degree-normalized
coordinates are constant on each clique pays energy only on the `k-1`
joining edges, while its squared norm is `Theta(m^2)` times the squared norm
of the `k` constants.  The min--max principle therefore gives

```text
lambda_k(L_norm) = O(m^-2),
```

and `Q` has at least `k` eigenvalues in
`[alpha, alpha+O(m^-2)]`.  Taking `m` large makes all `k` modes lie below any
declared `beta>alpha`.  The low spectral subspace has no graph-independent
rank bound.

### 5.5 No-restart lifted-frontier corrections

For nested batches `B_j`, exact Schur-frontier corrections lift to mutually
`Q`-orthogonal subspaces.  Approximating each frontier solve therefore gives
the exact Pythagorean error identity

```text
||z_tilde-z||_Q^2
  = sum_j ||y_tilde_j-y_j||_{K_j}^2.
```

Since the batches are disjoint, frontier-local Chebyshev/CG work sums to

```text
O_tilde(M/sqrt(alpha))
```

without restarting on the old face.  This is currently the closest algebraic
route to the requested deterministic bound.  Its unresolved charge is the
dense lift `Q_SS^{-1}Q_ST y` and the corresponding boundary-threshold
reporter.  A cutoff should be applied to response representation or event
heaviness, not merely to `lambda_min(Q_UU)`.

### 5.6 A genuine optimizable two-ledger cutoff

For one exterior coordinate or one fixed boundary-hierarchy node, partition
the nested corrections into epochs.  Let

```text
A_r = Schur-diagonal/source-leverage loss accumulated in epoch r,
E_r = Q-energy of the orthogonal corrections accumulated in epoch r.
```

The exact response interval is

```text
|demand change in epoch r| <= sqrt(A_r E_r).
```

Across disjoint epochs, the two ledgers telescope:

```text
sum_r A_r <= D,          sum_r E_r <= E,
```

where the normalized Schur-loss budget is `D=O(1)` for a fixed node and the
unit-source RPPR energy budget is `E<=alpha`.

In the usual point-source specialization `rho=eps_kkt`, let the finite KKT
margin be `m=c alpha rho`.  (For a different accuracy namespace, replace
`rho` below by its normalized KKT tolerance.)  Wake an epoch only when
`sqrt(A_r E_r)>=m`.  For any freely chosen cutoff `tau>0`, every wake-up
satisfies at least one of

```text
A_r >= m/tau,            E_r >= m tau.
```

Charging the first class to `D` and the second to `E` proves the exact
heavy/light count

```text
N(tau) <= D tau/m + E/(m tau)
       = O(tau/(alpha rho) + 1/(rho tau)).
```

This is the requested optimizable form.  It is minimized at

```text
tau = sqrt(alpha),       N = O(1/(rho sqrt(alpha))).
```

Equivalently, it is Young's inequality applied before the two telescopes are
discarded separately.  The two classes have an algorithmic interpretation:

1. leverage-heavy epochs justify rebuilding or refining structural response
   information;
2. energy-heavy epochs justify flushing an accumulated frontier correction
   with Chebyshev/CG.

This lemma is unconditional algebra, but it is not yet an end-to-end running
time theorem.  A naive implementation can still scan every exterior label or
the entire old face on every wake-up.  The needed implementation must locate
all heavy hierarchy nodes output-sensitively and apply the dense old-face
lift without materializing it after every batch.

There are two distinct summations here and they must not be conflated.  For a
fixed exterior vertex, or for a fixed hierarchy node that remains exterior,
the Schur-diagonal ledger telescopes.  At a fixed hierarchy level, the group
losses of disjoint nodes also pack.  But the same correction-energy epoch is
shared by every node.  Summing the displayed per-node wake-up count over all
nodes would therefore reuse `E_r` many times.  A global theorem needs a
search rule that visits only nodes whose *joint* leverage--energy product is
large, plus a way to obtain the relevant group loss without first visiting
the node.  The algebraic wake-up lemma does not supply that data structure.

A synchronized scheduler gives the strongest presently justified global
count.  Fix one partition level, let

```text
R = sum_j |B_j|,          E = sum_j ||Delta_j||_Q^2,
```

and use a common response margin `m`.  Declare an individual correction
energy-heavy when its energy exceeds `m tau`; there are at most

```text
E/(m tau)
```

such corrections.  Greedily pack all remaining corrections into common
epochs of energy at most `2 m tau`.  If a hierarchy node is ambiguous in one
such epoch, its group leverage loss is at least `m/(2 tau)`.  At a fixed
level the nodes are disjoint, and every batch's group losses sum to at most
`|B_j|`.  Charging each batch loss to its unique common epoch therefore gives

```text
number of ambiguous light-epoch nodes = O(R tau/m).
```

Thus the nonduplicating, levelwise balance is

```text
O(R tau/m + E/(m tau)).
```

This is rigorous, but it also exposes why the current packing theorem is
insufficient.  With `E<=alpha`, `R<=|S*|`, and the semantic RPPR margin
`m=Theta(alpha rho)`, optimizing this expression gives

```text
O(sqrt(R alpha)/(alpha rho)),
```

which can be worse than `M/sqrt(alpha)` by a support-size factor.  Moreover,
the count assumes the group masses can be queried without scanning the
groups.  A successful proof needs a stronger *source-weighted work* ledger
than rank alone, or it must compute/localize the actual boundary response
vector.  The latter is exactly the dense response primitive we started with.

### 5.6.1 Canonical single-source `L1` conservation (proved)

For the canonical point source, there is an exact source-weighted ledger that
is sharper than the generic energy bound for the *actual* batches.  Work in
degree coordinates with

```text
H=aD-bA,       a=(1+alpha)/2,       b=(1-alpha)/2.
```

Let `v` be the seed and let the exact solution on a reachable face `U`
satisfy

```text
H_U y^U = alpha e_v-alpha rho d_U.
```

Define its active mass and its weighted cut value by

```text
M(U)       = sum_(i in U) d_i y_i^U,
cut_U(y^U)= sum_(i in U) d_out,U(i) y_i^U.
```

Multiplying the face equation by the all-ones row gives the exact identity

```text
rho vol(U)+M(U)+(b/alpha) cut_U(y^U)=1.                 (L1-face)
```

Indeed, `1^T A_UU y=sum_i(d_i-d_out,U(i))y_i`, while
`a-b=alpha`.  Thus this is a conservation law, not an inequality produced by
Cauchy--Schwarz.

For an exterior vertex define the degree-normalized signal

```text
s_j^U=(b/d_j) sum_(i in U intersect N(j)) y_i^U.
```

The total exterior signal is consequently

```text
S(U):=sum_(j notin U) d_j s_j^U
     =b cut_U(y^U)
     =alpha(1-rho vol(U)-M(U))
     <=alpha(1-rho vol(U)).                              (L1-boundary)
```

Now let a positive-residual batch `B` be admitted, put `T=U union B` and
`W=V\T`, and define

```text
e_b^U=s_b^U-alpha rho,
I(U,B)=sum_(w in W) d_w(s_w^T-s_w^U).
```

Padding `y^U` by zero is a subsolution on `T`, because every admitted row has
positive residual.  Inverse positivity therefore gives `y^T>=y^U` on the
old coordinates and `I(U,B)>=0`.  Decomposing `S(U)-S(T)` into the signal
absorbed by `B` and the signal newly sent to the persistent exterior proves
the exact batch identity

```text
I(U,B)+alpha(M(T)-M(U))
  =sum_(b in B) d_b e_b^U.                               (L1-batch)
```

The right side is exactly the total positive degree-scaled residual that
caused this batch, not a surrogate leverage or rank quantity.  In particular,

```text
0 <= sum_(b in B) d_b e_b^U <= S(U) <= alpha.
```

For a threshold-depth trace of
`J=O_tilde(1/sqrt(alpha))` exact batches, the total actual batch-excess budget
is therefore

```text
sum_phases sum_(b in B) d_b e_b^U = O_tilde(sqrt(alpha)).
```

If an alternative reporter emits a vertex only after *degree-normalized*
excess at least `m=Theta(alpha rho)`, this gives the conditional
output-volume bound

```text
O_tilde(sqrt(alpha)/m)=O_tilde(1/(rho sqrt(alpha))).
```

This supplies the missing source numerator of the rank-only scheduler for the
canonical single source: actual positive events have the right total mass.
It does **not** by itself bound the volume of the manuscript's original
batch.  That algorithm thresholds the normalized-coordinate residual
`sqrt(d_b)e_b` at `vartheta`, not `e_b` at a common degree-normalized margin;
the conservation law then controls `sum sqrt(d_b)` rather than
`sum d_b`.  The global support bound still controls the latter, but not via
this identity alone.  Combined with the positive group upper oracle and the
companion first-crossing scheduler, it closes
`BoundaryReportGivenLift`: once certified additive response summaries are
supplied, all no-miss candidate visits and exact leaf validations have the
right total charge.

What remains is to *produce* the increments `s^T-s^U` and their group
summaries without scanning the old face or all of `W`.  A literal positive
Neumann/push propagation pays the expected killed-walk lifetime
`Theta(1/alpha)`; fixed-face Chebyshev pays `Theta(1/sqrt(alpha))` but does not
reuse the response across moving faces.  Thus the remaining lemma can now be
stated more narrowly: implement `CenterLift` so that it emits those summaries
with work proportional, up to polylogarithms and the desired rent-or-buy
terms, to the conserved excess rather than to killed-walk dwell time or
replayed face volume.

There is a precise reason the last sentence cannot follow from `L1-batch`
alone.  Consider any stable time-invariant linear streaming realization of a
scalar inverse `1/lambda`, and let `h_0,h_1,...` be its impulse-response
coefficients.  Exact steady-state response to a constant source requires

```text
sum_(t>=0) h_t=1/lambda,
```

so necessarily

```text
sum_(t>=0) |h_t| >= 1/lambda.                 (streaming L1 gain)
```

Equivalently, for any linear update decomposition that installs a positive
source increment of mass `m` and charges the time-integrated absolute
response/messages, the scalar slow mode alone can cost `m/lambda`.  At
`lambda=alpha` this is the killed-walk `1/alpha` scale.  Optimal heavy-ball
or a restarted polynomial reduces the *settling time* for one fixed source
to `O(1/sqrt(lambda))`; it does not change the DC inverse gain.  Signed
cancellation can make a normwise final approximation fast, but an argument
which takes absolute values at every delayed impulse loses that cancellation
and falls back to `(streaming L1 gain)`.

This is a scoped accounting barrier, not an oracle lower bound: an exact
Schur update may install the final scalar response in one operation, and a
fixed-face Chebyshev sweep charges edges rather than response magnitude.  It
does prove that the conserved total positive message mass, by itself, cannot
be multiplied by an asserted `1/sqrt(alpha)` propagation factor.  A valid
streaming acceleration proof has to add orthogonal energy cancellation,
first-crossing threshold accounting, or a compressed persistent response
state.  Those are exactly the unclosed `CenterLift` clauses.

#### A positive-walk barrier (proved, scoped)

The loss from literal positive propagation is not just an artifact of the
coordinate schedule.  In degree coordinates write

```text
H_U=aD_U(I-gamma P_U),
P_U=D_U^-1 A_UU,
gamma=b/a=(1-alpha)/(1+alpha).
```

Consider a universal degree-`k` walk filter

```text
p_k(P)=sum_(t=0)^k c_t P^t,       c_t>=0,
```

which must be a coordinatewise lower inverse for every nonnegative
substochastic face transition `P` and every `g>=0`:

```text
0<=p_k(P)g<=(I-gamma P)^-1 g.                  (universal lower walk)
```

Then necessarily

```text
0<=c_t<=gamma^t       for every t<=k.
```

To see this within undirected graph faces, use a length-`t` weighted path
whose ambient degrees are padded by ground/exterior ballast so that every
internal transition has weight `epsilon`.  At the opposite endpoint,
`P^s e_0` vanishes for `s<t`, its unique shortest-walk term at `s=t` is
`epsilon^t`, and every longer contribution is `O(epsilon^(t+2))`.  Divide
the endpoint inequality in `(universal lower walk)` by `epsilon^t` and let
`epsilon` tend to zero.  This gives `c_t<=gamma^t`; nonnegativity is part of
the safe positive-walk model.

Now apply the same universal coefficients to a full regular component, for
which `P1=1`.  On the Perron source the relative missing response is at
least

```text
1-(1-gamma)p_k(1)
 >=1-(1-gamma)sum_(t=0)^k gamma^t
 =gamma^(k+1).
```

Therefore relative error `delta` requires

```text
k >= log(1/delta)/(-log gamma)-1
  =Omega((1/alpha) log(1/delta)).              (positive barrier)
```

This lower bound is deliberately scoped.  Coefficients tailored to a known
small spectrum, a separator Schur solve, or a signed Chebyshev polynomial
are outside the model.  Its relevance is architectural: positivity gives
immediate support-safe monotonicity but pays the killed-walk `1/alpha`
lifetime; the `1/sqrt(alpha)` acceleration uses cancellation.  The proved
residual/retraction adapter makes a *completed* signed face solve safe, but
when its signed Krylov state is carried to a larger face, the omitted
boundary rows create exactly the orthogonality/response defects priced in
Section 5.9.  A successful general algorithm must therefore combine signed
acceleration with a persistent certified response mechanism; it cannot be a
uniform positive walk filter alone.

#### Why a degree cutoff does not by itself implement CenterLift

One natural attempt is to run monotone coordinate settlement on low-degree
rows and buy a block/Chebyshev solve on high-degree rows.  The normalization
shows exactly what this does and does not prove.  Let

```text
h_i=(-D^(-1/2) grad F)_i-alpha rho
```

be the positive degree-normalized KKT excess, and update coordinate `i` only
when its manuscript-normalized score satisfies
`sqrt(d_i) h_i>=theta`.  The standard residual-mass potential starts at
`alpha`, and one update decreases it by

```text
alpha d_i h_i >= alpha theta sqrt(d_i).
```

If every rented row has `d_i<=Delta`, its total adjacency work is therefore

```text
sum_rent d_i <= sqrt(Delta)/theta.             (low-degree rent)
```

This is a valid deterministic favorable-instance term.  It is not paired
with a valid high-degree buy term.  Although the number of distinct
high-degree active vertices is at most `M/Delta`, exact conditional updates
of one such vertex can return residual through its neighbors and require the
same row again.  The center-seeded star forces `Omega(1/alpha)` center-row
updates for this coordinate scheme.  Charging only the first heavy-row scan
would therefore omit the response work.

To turn `(low-degree rent)` into a theorem one needs a one-shot
`HighDegreeCenterLift(Delta)` which, after a heavy row wakes, settles its
coupled old-face response at total cost proportional to its newly charged
volume and never requires an uncharged replay.  A fresh Chebyshev call does
this on one fixed block but may revisit the whole old face; literal monotone
push does not, but pays `1/alpha`.  Thus the degree split recovers the same
missing Schur-response primitive in a simpler guise.  Optimizing `Delta`
before proving the buy ledger would be spurious.

### 5.7 Deterministic lower-envelope adapter (proved)

Work in degree coordinates.  Put

```text
H_U = D_U^(1/2) Q_UU D_U^(1/2) = a D_U - b A_UU,
a=(1+alpha)/2,  b=(1-alpha)/2,
```

and let `y_U^*=H_U^{-1}f_U` be the exact reachable-face solution.  Suppose a
deterministic CG/Chebyshev call returns a signed vector `y` with

```text
||D_U^(-1/2)(f_U-H_U y)||_2 <= eta.
```

For every boundary vertex let `d_U(j)` be its number of neighbors in `U` and
define the locally computable exposure factor

```text
Gamma_U = max{1, max_(j in boundary(U)) d_U(j)/sqrt(d_j)}.
```

Choose

```text
eta = alpha theta/(16 Gamma_U),       t = eta/alpha.
```

Let `ell` be the previous nonnegative subsolution, padded by zero on a newly
admitted batch, and publish

```text
u = y-t 1,             z = ell max u       (coordinatewise maximum).
```

Then

```text
0 <= z <= y_U^*,       H_U z <= f_U,
0 <= y_U^*-z <= theta/(8 Gamma_U) 1.
```

The proof is short and one-sided.  If `e=f_U-H_Uy`, the residual hypothesis
gives `|e_i|<=eta sqrt(d_i)`.  Grounding gives

```text
H_U 1 >= alpha D_U 1 >= alpha D_U^(1/2) 1,
```

so `H_Uu<=f_U`: `u` is a subsolution.  The coordinatewise maximum of two
subsolutions of a Stieltjes system is again a subsolution, and inverse
positivity puts it below `y_U^*`.  Finally,

```text
||D_U^(1/2) H_U^(-1)e||_2
  = ||Q_UU^(-1)D_U^(-1/2)e||_2 <= eta/alpha,
```

which bounds every coordinate of `H_U^(-1)e` by `eta/alpha`; adding the
retraction `t` proves the displayed error.

In the original normalized coordinates, the exact-minus-published boundary
residual is

```text
(b/sqrt(d_j)) sum_(i in N(j) intersect U) (y_i^*-z_i)
  <= theta/16.
```

Consequently a published score above `theta/2` is a true exact positive
face residual and is support-safe.  A coordinate not published has exact
residual at most `theta/2+theta/16<theta`.  The threshold-batch depth proof
and the quiet-face KKT certificate therefore retain their constants (with
room to spare).  Padding `ell` after an admission is valid because every new
row was admitted with positive published residual; old rows are unchanged.

This theorem closes deterministic *finite-solve certification*.  The factor
`Gamma_U` affects CG/Chebyshev only inside a logarithm.  It does not close the
number of matrix-vector products spent again on old rows after the face
grows.

### 5.8 Why a single masked Chebyshev recurrence is not yet the solution

On a fixed supplied face, Chebyshev is deterministic and has the desired
`O_tilde(vol(U)/sqrt(mu_U))` work.  A tempting alternative is to keep one
Chebyshev recurrence while the face grows and mask every update to the
currently exposed coordinates.  This has two separate difficulties.

First, masking turns the homogeneous Chebyshev residual recurrence into a
forced second-order recurrence.  Existing LocalCH analysis writes the error
exactly in this form, but its accelerated bound assumes that a run-dependent
geometric mean of the masking-noise ratios stays below

```text
1 + c sqrt(alpha)/(1-sqrt(alpha)),       c < 2.
```

That is a useful conditional performance parameter, not a graph-uniform
bound.  If active sets may shrink, the same coordinate can contribute
masking noise repeatedly.  Requiring a monotone growing mask improves this:
each still-hidden coordinate has one delay interval, making the philosophy
closer to the one-time threshold charge in the batch-depth proof.  However,
Chebyshev's Green kernel for the forced recurrence carries time-dependent
weights; the existing block-Cholesky one-time charge does not directly bound
their sum.  A new stability lemma would still be required.

Second, Chebyshev iterates and residuals oscillate, so their raw positive
residuals are not support certificates.  Section 5.7 now resolves this issue:
at any requested checkpoint, solve to the declared residual tolerance and
publish only the retracted lower envelope.  Thus oscillation is no longer a
correctness obstruction.  What remains is a work obstruction.  Restarting
the certified call after each face costs the old-face matrix-vector products
again; continuing the masked recurrence produces the forced-recurrence noise
described above.  No current theorem charges that noise once per newly
admitted coordinate at accelerated scale.

Standard *unretracted* accelerated proximal gradient has an even clearer
locality failure.
On a star with the seed at a leaf, momentum can touch the high-degree center
although the exact regularized support is only the seed.  This incurs work
proportional to the ambient star degree.  Hence a global FISTA call cannot be
substituted for the local face solver while retaining an output-sensitive
bound.

### 5.9 Cross-face Krylov reuse: exact loss and the required repair

The lower-envelope adapter permits arbitrary signed scratch, but it does not
make a fixed-matrix Krylov history valid after a principal face is enlarged.
The smallest CG example is the three-vertex Stieltjes path

```text
H = [[ 2,-1, 0],
     [-1, 2,-1],
     [ 0,-1, 2]],              f=e_1.
```

CG on `U={1,2}` uses conjugate directions

```text
p_0=e_1,             p_1=(1/4,1/2),
```

and reaches `y_U^*=(2/3,1/3)`.  After padding this solution by zero and
admitting coordinate three, the enlarged residual is `(0,0,1/3)`.  Its
natural new direction is proportional to `e_3`, but

```text
p_1^T H e_3 = -1/2 != 0.
```

Thus simply retaining the ordinary short recurrence loses conjugacy.
Restarting is correct but repays old-face work.  Full orthogonalization
retains the history but can store and touch a growing dense basis.

The exact accounting is slightly more informative than the example.  Let
`P=[p_1,...,p_k]` be old search directions and let

```text
G=P^T H_UU P
```

be diagonal (or merely SPD for an augmented basis).  After padding by zero,
their mutual conjugacy is actually preserved:

```text
[P;0]^T H_TT [P;0]=G.
```

If the old face was solved exactly, the enlarged initial residual is
`r_0=[0;g_B]`, and it remains Euclidean-orthogonal to `[P;0]`.  The defect is
instead the conjugacy of the *new* direction:

```text
[P;0]^T H_TT r_0=P^T H_UB g_B.              (frontier defect)
```

The unique projection into the stored basis which repairs this defect is

```text
s_0=r_0-[P;0]G^(-1)P^T H_UB g_B.            (augmented-CG repair)
```

When `P` spans all of `R^U`, the identity
`P G^(-1)P^T=H_UU^(-1)` turns this formula into exactly the Schur-frontier
lift below.  With a truncated recycle space it is only the Galerkin
approximation to that lift; the component in the discarded old-face modes is
uncontrolled without a new approximation theorem.

For the canonical frontier loads, the *size* of this repair has a useful
deterministic ledger.  State it in normalized coordinates, so the matrix is
`Q<=I`.  Put

```text
c=P^T Q_UB g_B,
v=[P;0] G^-1 c.
```

The old-coordinate energy of the repair is

```text
||v||_Q^2=c^T G^-1 c
 <=g_B^T Q_BU Q_UU^-1 Q_UB g_B
 <=g_B^T Q_BB g_B
 <=||g_B||_2^2.                              (defect-energy bound)
```

The first inequality is Galerkin projection, the second is positivity of the
Schur complement, and the third uses `Q<=I`.  For a canonical positive batch,
`g_B=sqrt(D_B)e_B` and

```text
||g_B||_2 <= sum_(i in B) d_i e_i=:m_B.
```

The conservation ledger gives `m_B<=alpha` per reached batch and
`sum_B m_B=O_tilde(sqrt(alpha))`; hence

```text
sum_B ||v_B||_Q^2
 <=sum_B m_B^2
 <=alpha sum_B m_B
 =O_tilde(alpha^(3/2)).                        (cumulative defect size)
```

This answers one part of the cross-face accounting question: the new
coordinates do not create an unbounded amount of raw orthogonality defect.
It is not, by itself, a short-recurrence convergence theorem.  A CG direction
may be rescaled without changing its span, and a low-eigenvalue coefficient
can amplify a small residual direction by `1/alpha`.  The repair vectors from
different expansions are not known to be mutually energy-orthogonal either.
Thus dropping them requires a perturbation theorem in the *solution* norm at
the requested `rho`-dependent tolerance; applying them exactly still requires
the dense old-face combination.  The proved bound is a legitimate numerator
for a future rent-or-buy rule, not a proof that the buy operation is free.

This also exposes the cost that ordinary recycling language can hide.  For
each new block direction one must (i) compute all `k` frontier-defect inner
products, (ii) solve the `k`-dimensional Gram system, and (iii) form a dense
old-face combination of the stored directions.  If the basis is dense, the
last step touches `Theta(k|U|)` entries per block direction; storing it costs
the same order.  Keeping every old direction can therefore reproduce the
`M/alpha` ledger, while fixing `k` has no graph-uniform guarantee (weakly
coupled clique chains have arbitrarily many relevant low modes, and the comb
has full response rank).  A compressed structure capable of applying the
last display is not ``free recycling''; it is precisely an implementation of
the persistent Schur/DtN response sought in
`PositiveFrontierRentOrBuy`.

The exact one-block repair is the Schur-frontier lift

```text
L_U,B = [-H_UU^(-1) H_UB ; I_B].
```

Its columns are `H`-orthogonal to every old-face vector.  In the example the
new direction is `(1/3,2/3,1)`, not `e_3`.  This proves both sides of the
interface: old Krylov work can be preserved algebraically, and doing so
requires applying the old-face response `H_UU^(-1)H_UB`.  That is the dense
lift isolated in Section 5.5.  Any claimed no-restart CG theorem must either
implement this response at charged local cost or explicitly pay
reorthogonalization/restart work.

Chebyshev has no conjugacy state, but face expansion creates the analogous
loss.  Padded recurrence states were polynomials of `H_UU`; they are not the
states that the enlarged matrix would have produced, because earlier
matrix-vector products omitted propagation through `H_BU`.  Recomputing the
new residual inserts a forcing impulse into the second-order recurrence.
There are three valid options:

1. restart the polynomial and repay the old rows;
2. replay the missing polynomial tail through the new block;
3. prove a stability/amortization lemma for all such delayed forcing.

The missing lemma for option 3 must bound the accumulated forced-Chebyshev
response by a sum over newly admitted incidences or orthogonal frontier
energy, with no repeated old-face volume.  Existing LocalCH bounds this term
by a run-dependent masking-noise parameter; the threshold-batch Cholesky
proof charges delayed *coordinates* once but does not control the
time-weighted second-order forcing.  This is currently open, not an implicit
consequence of either theorem.

The subset-Chebyshev recurrence of ChebyPush gives a particularly clean
version of option 3, but its local work theorem assumes

```text
||T_k(P)||_1 = O(1)                         (all k),
```

for the random-walk operator `P`.  This is not graph-universal.  On the
infinite `d`-regular tree, start at the root `o`.  A vertex at exact distance
`k` can receive only the leading term `2^(k-1)P^k e_o` of `T_k(P)e_o`.
There are `d(d-1)^(k-1)` such vertices and each receives
`2^(k-1)/d^k`.  Therefore

```text
||T_k(P)e_o||_1 >= (2(d-1)/d)^(k-1),        d>=3,
```

which grows exponentially.  The radial calculation in `witnesses.py`
checks the complete norm as well as this outer-level lower bound.  Even under
the stated stability assumption, ChebyPush's local bound is
`O(K^2/eps)`; with the PPR truncation degree
`K=O_tilde(1/sqrt(alpha))`, this is `O_tilde(1/(alpha eps))`, not the
desired square-root work.  The paper is useful because it exposes and
compensates delayed defects explicitly, but it does not close our uniform
reuse lemma.

There is also direct path regression evidence against warm restart plus
retraction alone.  In a separate exact-arithmetic implementation, after
every face expansion the previous lower subsolution was padded, CG was
restarted, and a common adaptive Stieltjes retraction was applied.  On an
endpoint path with

```text
alpha=1e-3,       n=128,       rho=1e-5,
```

the support still grew essentially one vertex at a time, using about `2506`
CG iterations and a cumulative scanned-volume ledger of `4.2e5`.  This is an
empirical regression, not a class lower bound, but it agrees with the exact
three-coordinate mechanism: retaining the lower point is not the same as
retaining the inverse response or Krylov subspace.  Warm restart is therefore
removed from the unconditional candidate list.

A second regression rules out the equally tempting ``never restart''
shortcut.  On the same endpoint path, one optimal heavy-ball recurrence was
continued across every face expansion by zero-padding its signed current and
momentum states.  After every step, the exact common Stieltjes retraction was
joined with the historical lower subsolution, and only this certified lower
envelope controlled admission.  With

```text
alpha=1e-3,       n=128,       rho=1e-5,
gate=alpha*rho/16,
```

the run still made `127` singleton expansions.  It needed `5715` recurrence
steps, an average of `45` steps between expansions and at most `91`, with a
cumulative degree-volume ledger of about `8.14e5`.  The subsolution invariant
held to numerical precision.  This is again an empirical regression rather
than a lower bound, but it isolates the issue: retaining momentum and a safe
lower point does not restore the matrix-vector products omitted across past
boundary rows.  A successful continuing recurrence must account for those
delayed defects explicitly; zero-padding alone is removed from the
unconditional candidate list.

### 5.10 A conductance parameter gives the exact desired balance (candidate)

There is a more structural interpretation of the free parameter than a
formed-face eigenvalue.  Let `tau` be a *conductance* cutoff and imagine a
`tau`-expander decomposition of the finally relevant graph.  Up to logarithms,
such a decomposition has

```text
internal cluster conductance:  Omega(tau),
internal mean-zero gap:        Omega(tau^2),
inter-cluster edges:           O(M tau).
```

The first two lines make a deterministic Chebyshev treatment of all
within-cluster mean-zero modes cost `O_tilde(M/tau)`.  If the remaining
cluster-constant/coarse response could be represented only on the cut edges
and settled with the worst positive-resolvent dwell `1/alpha`, its work would
be

```text
O_tilde(|E_cut|/alpha)=O_tilde(M tau/alpha).
```

This recovers, for a mathematically natural graph parameter,

```text
T_exp(tau)=O_tilde(M/tau+M tau/alpha),
```

and `tau=sqrt(alpha)` gives the target.  Unlike changing the diagonal shift,
the two terms now correspond to different graph objects: rapidly mixing
intra-cluster modes versus the sparse inter-cluster skeleton.  The scalar
Cheeger/Poincare implications and this accounting calculation are valid.

The claim that only one genuinely slow direction remains per expanding
cluster has a precise static theorem.  Let `d_out,C` be the cut degree of a
cluster and give each cut edge back to its interior endpoint as a self-loop.
The resulting reflected normalized Laplacian is

```text
L_C^circ
 =D_C^-1/2(D_C-A_CC-diag(d_out,C))D_C^-1/2.
```

It has null vector `sqrt(d_C)`.  If the reflected cluster has conductance at
least `tau`, Cheeger's inequality gives

```text
lambda_2(L_C^circ)>=tau^2/2.
```

The actual Dirichlet block contains the nonnegative killing diagonal:

```text
L_C^D
 =D_C^-1/2(D_C-A_CC)D_C^-1/2
 =L_C^circ+diag(d_out,C/d_C) >= L_C^circ.
```

Therefore every vector orthogonal to `sqrt(d_C)` has Rayleigh quotient at
least `tau^2/2`.  By min--max, `L_C^D`, and hence

```text
Q_CC=alpha I+b L_C^D,
```

has at most one eigenvalue below `alpha+b tau^2/2`.  This proves the static
``one coarse mode per cluster'' statement; it is not an assumption about
the number of ports.

The canonical floor relaxation has an additional exact rank-two structure
which is useful for trying to stream that one coarse mode.  State it on any
proper face and put

```text
s_i=sqrt(d_i),
ell_i=b d_out(i)/sqrt(d_i),
h=Q_UU s=alpha s+ell,
H=s^T h=alpha vol(U)+b cut(U),
R=h s^T/H,
B=I-Q_UU.
```

Here `R^2=R`.  For the relaxed-floor change of basis
`A_xi=I+xi R`, direct multiplication gives the exact conjugacy

```text
A_xi B A_xi^-1
 =B+xi(RB-BR)A_xi^-1,                         (floor conjugacy)

RB-BR=(Q_UU ell s^T-h ell^T)/H.               (cut commutator)
```

The second identity uses `B=I-Q`, `s^TQ=h^T`, and
`Qh=alpha h+Qell`.  Thus all failure of the known constant direction to
commute with the proper-face propagation is a signed rank-two source born at
the cut; it is not an arbitrary dense operator perturbation.  Its numerator
is quantitatively cut controlled:

```text
||ell||_2^2 <= b^2 cut(U),       ||Qell||_2<=||ell||_2.
```

The oblique change of basis is also normwise safe at the target scale.  Since
`Q^2<=Q`,

```text
||h||_2^2<=H,
||R||_2<=1/sqrt(alpha),
||A_xi^-1||_2<=1+xi/sqrt(alpha),
```

and, writing `V=vol(U)` and `k=cut(U)`,

```text
||RB-BR||_2
 <= b sqrt(kV)/(alpha V+bk)+sqrt(b)
 <= (1/2)sqrt(b/alpha)+sqrt(b).
```

Consequently

```text
xi ||RB-BR||_2 ||A_xi^-1||_2=O(1)
```

for `xi=sqrt(alpha)`.  This rules out numerical instability of a single
coarse-mode floor conjugation as the explanation for the missing factor.

There is a matching binding dichotomy.  Decompose any clipped residual as

```text
r_g=F_g s+w_g,       w_g perpendicular to s,
```

and let `Z` be coordinates at which the floor binds, so `(r_g)_i=0`.
Then `(w_g)_i=-F_gs_i` on `Z`, and hence, for every `gamma in (0,1)`, either

```text
|F_g|<=gamma |F|,
```

or

```text
||w_g||_2^2>=gamma^2 F^2 sum_(i in Z)d_i.      (binding dichotomy)
```

Thus every binding episode either contracts the scalar slow coefficient or
creates a quantitatively chargeable mean-zero component.  Together with the
reflected-cluster gap, `(floor conjugacy)` and `(binding dichotomy)` give the
right local ingredients for a forced Chebyshev implementation of
`StreamMeanZero`.

They still do not prove its cumulative work.  As the face changes, the cut
vector `ell` changes; the succession of rank-two births can span the entire
terminal space.  The comb realizes exactly this full-rank causal prefix
response.  Applying one inverse response for each birth therefore recreates
the restart ledger even though every individual perturbation has rank two
and bounded norm.  What remains is a theorem that batches these births in
one persistent recurrence/checkpoint state and uses orthogonal mean-zero
energy or first-binding charges only once.  Treating the Dirichlet-to-Neumann
response of each new `ell` as free would assume `CenterLift` again.

There is also a deterministic source-aware **rent-or-cut** alternative on a
supplied reflected cluster.  Let `L_C^circ` be its reflected normalized
Laplacian, let `g` be a current mean-zero frontier load, and let `P_low` be
the spectral projector onto eigenvalues in `(0,tau^2)`.  Exactly one of the
following holds:

1. `||P_low g||<=eta`.  A bounded Chebyshev residual filter may discard this
   part and solves the visible complement in
   `O_tilde(vol(C)/tau)` work; the residual/retraction adapter checks the
   claimed `eta` afterward.
2. `w=P_low g` is nonzero.  It is orthogonal to `sqrt(d_C)` and satisfies

   ```text
   w^T L_C^circ w/||w||_2^2<tau^2.
   ```

   A Cheeger sweep therefore returns a cut of conductance at most
   `sqrt(2) tau`.

A finite polynomial implementation uses a constant-width transition band
around `tau^2`; if its low residual is large, the returned vector has
Rayleigh quotient `O(tau^2)`, and the cut is exactly validated.  Thus random
starting vectors are unnecessary for a low mode that is actually visible to
the current source.  Recursively cutting every source-visible failure also
has the right *structural* edge ledger: charging each `O(tau)` cut to the
smaller side yields `O_tilde(M tau)` total crossing edges.

This does not yet give the construction time `M/tau`.  A filter can scan the
whole current cluster before peeling a tiny side, and a later independent
frontier source can expose another previously invisible low direction.
Repeated unbalanced peels or the comb can therefore rescan the same large
side.  A complete implementation needs a local seeded cut routine charged to
the peeled side, or must retain the large-side Krylov/flow state after the
cut.  Saranurak--Wang's deterministic expander pruning demonstrates this
kind of reuse for deletions from a supplied expander, but it does not cover
our insertion-local unknown-support sequence or maintain the Schur response.
The rent-or-cut lemma hence explains how Chebyshev can *discover* the needed
hierarchy; `CenterLift` still has to make that discovery cumulative.

It still does not prove `M/tau` total work.  Successive frontier loads can
have arbitrarily many linearly independent components in the *fast*
mean-zero subspace---the clique with one tooth at every vertex is the
simplest example.  Each such component is cheap for a supplied fixed solve,
but solving it afresh rereads the cluster.  To use the one-mode theorem in
the nested algorithm one needs a separate streaming statement:

```text
StreamMeanZero(tau):
  accept all adaptive cut/frontier impulses in every reflected cluster;
  apply their components orthogonal to sqrt(d_C), including delayed
  boundary defects and exact threshold validation, in total
  O_tilde(M/tau), not once per impulse.
```

This is the high-frequency half of `NestedExpanderLift`; the one-coarse-mode
lemma only supplies its spectral premise.  It prevents the conductance
proposal from silently treating many easy right-hand sides as one solve.

There is a more honest response-rank version of this calculation which makes
clear when the displayed formula is actually additive.  For every cluster
`C`, let

```text
p_C = number of exposed boundary ports of C,
r_C = dimension of the span of all cut/frontier loads on C that the run
      must lift (after exact dependencies are removed).
```

Building a deterministic response bank for those directions by the
mean-zero cluster filters costs

```text
A/tau,       A:=sum_C r_C vol(C).
```

An explicit port-by-response representation contains at most
`sum_C p_C r_C` scalar couplings.  If the nested hierarchy and the actual
source sequence satisfy the *weighted port packing* certificate

```text
sum_C p_C r_C <= B tau,                         (port packing)
```

and this coarse representation is maintained persistently rather than
re-solved after every face, then literal positive low-tail settlement costs
at most `B tau/alpha`.  Under these stated bank-construction and persistence
premises the lower-envelope adapter therefore gives the genuine conditional
bound

```text
T_port(tau)=O_tilde(M+A/tau+B tau/alpha).       (rank--port balance)
```

This is exactly the requested optimizable algebra, without hiding a
Dirichlet-to-Neumann call.  Its unconstrained optimizer and value are

```text
tau_* = sqrt(A alpha/B),
T_port(tau_*)=O_tilde(M+2 sqrt(A B/alpha)),
```

clipped to the interval of scales for which the decomposition certificate
holds.  In the favorable uniform-rank regime `r_C<=r`, disjoint cluster
volume gives `A<=rM`; an expander cut bound plus weighted port packing gives
`B=O_tilde(rM)`.  Hence `tau=sqrt(alpha)` yields

```text
T_port=O_tilde(r M/sqrt(alpha)).
```

Constant response rank is therefore a rigorous special regime in which the
small-`o(1)` factor disappears.  The parameter cannot be deleted in general.
For the `k`-tooth comb, take the anchor path `C={u_1,...,u_k}` and attach one
frontier leaf `f_i` to each `u_i`.  In degree coordinates

```text
-H_CC^-1 H_CF=b H_CC^-1 diag(w_1,...,w_k).
```

All tooth weights are positive, so this matrix has rank `k`; irreducibility
of the path Stieltjes matrix makes every inverse column strictly positive
and hence dense.  Therefore `p_C=r_C=k=Theta(|C|)` exactly, not merely in a
numerical example.  Conversely, the broom/path has scalar ports and
`r_C=1`, explaining why a retained tree recurrence succeeds even though
every formed face has gap `Theta(alpha)`.  Thus `r_C` distinguishes the two
examples that a face eigenvalue or cut cardinality alone cannot.

The qualification in `(rank--port balance)` is substantive.  The one-sided
positive probe proved in Section 6.2 can report candidate groups without
building all `r_C` columns, but `CenterLift` must still apply the actual
frontier correction; candidate compression is not response compression.
Likewise, merely asserting `p_C=O(1)` after an arbitrary clustering is not
enough if discovering the cluster or refreshing its bank rereads old volume.
The theorem is executable only when `r_C`, the response bank, and the port
packing are certified and maintained within the displayed charges.

They are not yet an algorithm.  A sufficient precise interface would be:

```text
NestedExpanderLift(tau):
  under the one-time insertion of all edges exposed by nested safe faces,
  maintain a support-local expander hierarchy with O_tilde(M tau) total
  cross edges;
  charge all mean-zero cluster filtering in O_tilde(M/tau);
  maintain and query the induced coarse/Schur response, including numerical
  debt and boundary validation, in O_tilde(|E_cut|/alpha), without explicit
  dense fill.
```

This interface implies `PositiveFrontierRentOrBuy`, so the lower-envelope
wrapper would make it end-to-end deterministic.  It is more constructive
than treating a DtN oracle as primitive, but two clauses remain open.

First, the optimal static `O_tilde(M/tau)` expander decompositions with
`O_tilde(M tau)` cross edges used in modern graph algorithms are randomized
in their cleanest form.  Known deterministic dynamic expander hierarchies or
decremental decompositions retain subpolynomial overhead (and generally
global preprocessing).  A face chain exposes edges by insertions and must be
local to `S*`; rebuilding a static decomposition after every singleton face
is ruled out by the broom.  A naive deterministic recursive spectral cutter
can also rescan one large remainder after many small peel-offs, so Cheeger's
inequality alone does not prove the total construction work.

Second, a sparse inter-cluster edge set is not itself a sparse Schur
complement.  Eliminating the cluster mean-zero modes can couple all boundary
ports of a cluster and create dense fill.  A fixed-face iterative V-cycle can
avoid materializing that fill, but running it after every new frontier still
replays the old clusters.  Maintaining its state under adaptive sources is
again the moving-response problem.  The comb refutes a constant-rank explicit
port table, while its tree recurrence shows that an implicit hierarchical
representation can succeed; hence this is a missing implementation lemma,
not a lower bound against the hierarchy.

The regressions behave consistently with the candidate.  A long path is cut
into scalar-port clusters and admits a retained recurrence; a regular tree is
already a high-conductance cluster and is handled by the `M/tau` branch; a
ballasted broom separates a large easy ballast cluster from a scalar path
skeleton.  None refutes `NestedExpanderLift`.  What prevents promotion from
conjecture to theorem is precisely deterministic *nested/local maintenance*
and coarse-response persistence.  This is currently the most concrete new
general-graph design route to the requested balance.

## 6. Conditional balanced algorithm suggested by the cutoff

The following architecture is now the primary positive candidate.

1. Maintain a settled anchor face and collect new support-safe frontier
   batches without re-solving the old face.
2. Represent each new exact correction in its Schur-frontier coordinates.
   Orthogonality allows independent numerical error budgets and prevents a
   restart tax.
3. Accumulate light corrections until their energy ledger reaches
   `m tau`; flush their aggregate with deterministic Chebyshev/CG.
4. Accumulate response-leverage loss until it reaches `m/tau`; then refresh
   the affected boundary hierarchy or buy a reusable response orientation.
5. Use `tau=sqrt(alpha)` and validate every reported boundary coordinate
   exactly before admitting it.

The companion canonical-source argument now closes the reporting side in
the following deliberately separated form:

```text
BoundaryReportGivenLift:
  given additive certified group summaries for every emitted frontier
  correction, report every first threshold crossing, validate its leaf
  exactly, and charge all candidate/group work to
      O_tilde(M/sqrt(alpha)).
```

Its proof combines the exact canonical excess conservation with the
one-positive-probe group upper oracle below; it no longer needs Gaussian
trace sources.  Crucially, the phrase ``given summaries'' is not free.  The
remaining primitive is

```text
CenterLift = AggregateLift = O_tilde(M/sqrt(alpha)):
  produce and persist those old-face response/group-summary increments under
  all nested safe expansions, including delayed Krylov defects.
```

If this one primitive has the stated charge, the complete algorithm is
deterministic, support-safe, and has the target work.  Chebyshev/CG supplies
each numerical flush and the lower-envelope adapter supplies certification;
the unresolved issue is producing the dense response information without
replaying the old face.  Random Gaussian sketches are no longer the
derandomization bottleneck.

### 6.1 Deterministic trace-estimation stop

The existing output-sensitive group reporter obtains response-leverage
traces from Gaussian right-hand sides.  Chebyshev or CG can evaluate each
chosen right-hand side deterministically, but they do not derandomize the
choice of a small simultaneous trace basis.

There is an elementary black-box obstruction.  Let a deterministic algorithm
query an unknown PSD matrix `A` on fewer than `n` adaptively selected vectors.
Answer every query with zero.  At termination choose a unit vector `u`
orthogonal to the span of all queries.  The two matrices

```text
A_0 = 0,                 A_1 = u u^T
```

produce the same transcript, while their traces are zero and one.  Hence no
generic deterministic multiplicative trace estimator can replace the
Gaussian sketches with fewer than `n` matrix-vector queries.  This is a
black-box stop, not yet a graph-specific lower bound: a successful
deterministic reporter must exploit more of the grounded-Laplacian response
structure, use a different one-sided event representation, or pay an
explicit rank/separator parameter.

### 6.2 One positive face solve dominates every frontier leverage row

The preceding black-box stop does **not** apply once the Stieltjes signs are
used.  In fact, all Gaussian source probes on one fixed anchor/frontier pair
can be replaced by one deterministic positive right-hand side.

Let `V=A dotcup F dotcup W`, put `T=A dotcup F`, and define the usual lift and
frontier Schur complement

```text
U = [-Q_AA^{-1} Q_AF ; I_F],
K = Q_FF-Q_FA Q_AA^{-1}Q_AF.
```

The normalized exterior response matrix whose row norms are the
source-aware leverages is

```text
B = -D_W^{-1/2} Q_WT U K^{-1/2} >= 0.
```

Let `s_F=(sqrt(d_u))_(u in F)` and make the single positive face solve

```text
u = Q_TT^{-1} E_F s_F,
p = -D_W^{-1/2} Q_WT u.
```

Then, coordinatewise,

```text
p_v >= ||B_(v,:)||_2,
```

and its degree-weighted mass obeys

```text
sum_(v in W) d_v p_v <= vol(F).                 (positive-probe mass)
```

The degree-square-root source is not essential.  An even simpler choice is

```text
g_F=1_F,
u=Q_TT^{-1}E_F g_F.
```

Now `K^{-1/2}g_F>=1_F`, so the same row domination holds, while the mass
identity has source term
`sqrt(d_F)^T1_F<=vol(F)`.  All conclusions below therefore hold for this
all-ones right-hand side as well.

Here is the complete proof.  Schur complementation preserves the Stieltjes
property, so `K^{-1/2}` is entrywise nonnegative; this follows directly from
the positive resolvent integral for the fractional inverse.  Also `K<=I`:
the Schur variational formula is at most the trial value with zero anchor
coordinates, and `Q_FF<=I`.  Thus `K^{-1/2}>=I` in Loewner order.  Its
off-diagonal entries are nonnegative and its diagonal entries are at least
one.  Consequently

```text
t:=K^{-1/2}s_F >= s_F >= 1                 coordinatewise.
```

The block inverse identity gives

```text
Q_TT^{-1}E_F = U K^{-1},
p = B t.
```

Every row of `B` is nonnegative, hence

```text
p_v = B_(v,:) t >= ||B_(v,:)||_1 >= ||B_(v,:)||_2.
```

For the mass identity, extend `u` by zero off `T` and put `q=Qu`.  Then
`q_A=0`, `q_F=s_F`, and `q_W<=0`.  Since `Q sqrt(d)=alpha sqrt(d)`,

```text
sum_(v in W) d_v p_v
 = s_W^T(-q_W)
 = ||s_F||_2^2-alpha s_T^T u
 <= vol(F).
```

Therefore, for every leverage cutoff `lambda>0`,

```text
{v: ||B_(v,:)||_2^2 >= lambda}
  subseteq {v: p_v >= sqrt(lambda)},

vol{v: p_v >= sqrt(lambda)} <= vol(F)/sqrt(lambda).
```

This survives an inexact deterministic solve without a probabilistic
argument.  Let `u_tilde` have face-energy error at most `delta`, and form the
signed approximate exterior probe

```text
p_tilde=-D_W^{-1/2}Q_WT u_tilde.
```

Because `Q^2<=Q`, its normalized exterior error `e=p_tilde-p` satisfies

```text
sum_(v in W) d_v e_v^2
 = ||Q_WT(u_tilde-u)||_2^2
 <= ||u_tilde-u||_Q^2
 <= delta^2.
```

If `delta<=sqrt(lambda)/4`, every row with leverage at least `lambda` has
`p_tilde_v>=sqrt(lambda)/2`.  Conversely, every candidate at the latter
threshold either has `p_v>=sqrt(lambda)/4`, or
`|e_v|>=sqrt(lambda)/4`.  Markov's inequality in the displayed weighted
square norm gives the deterministic false-positive bound

```text
vol{v:p_tilde_v>=sqrt(lambda)/2}
 <= 4 vol(F)/sqrt(lambda) + 16 delta^2/lambda
 <= 4 vol(F)/sqrt(lambda)+1.
```

Thus ordinary residual-certified Chebyshev/CG is enough for a fixed-face
probe; neither exact arithmetic nor a coordinatewise monotone iteration is
needed for no-false-negative candidate production.

There is a complementary squared-mass version that is better suited to a
boundary hierarchy.  Return to the normalized response matrix

```text
B=-D_W^{-1/2}Q_WT U K^{-1/2}>=0
```

and use the Schur-whitened deterministic probe

```text
p=B 1_F.
```

For every hierarchy group `C`, its exact source-aware leverage mass has the
one-sided oracle

```text
Z(C):=sum_(v in C)||B_(v,:)||_2^2
    <=sum_(v in C)p_v^2=||p_C||_2^2.            (group upper oracle)
```

The upper bound can be loose, but its total mass has exactly the same rank
packing scale as the trace.  Put `u=U K^{-1/2}1_F`, extend it by zero, and let
`q=Qu`.
Since `Q^2<=Q` and the lift is an isometry,

```text
sum_(v in W)d_v p_v^2
 = ||q_W||_2^2
 <= ||Qu||_2^2
 <= ||u||_Q^2
 = |F|.
```

Consequently a bounded-arity hierarchy that retains a group only when
`||p_C||_2^2>=lambda` visits only
`O(|F|/lambda)` disjoint groups per level; exact leaf validation removes
all false positives.  This matches the packing count of the Gaussian trace
oracle even though it is not a constant-factor estimate of `Z(C)`.  The
distinction matters: on a star-like response row, the ratio
`p_v/||B_(v,:)||_2` can be `Theta(sqrt(|F|))`.

The group oracle is stable under deterministic approximation.  If
`||p_tilde-p||_2<=delta`, then

```text
U_hat(C):=(||p_tilde_C||_2+delta)^2
```

is a simultaneous upper bound for every group.  For
`delta<=sqrt(lambda)/2`, every retained group has
`||p_tilde_C||_2>=sqrt(lambda)/2`; disjointness and the global squared-mass
bound still give `O(|F|/lambda+1)` groups per level.  Thus no union bound,
random source, or multiplicative trace estimate is required.

This also determinizes the previously conditional low-cut-rank reporter on a
fixed epoch.  Suppose the normalized anchor--exterior cut has a supplied
rank-`r` factorization and the corresponding `r` harmonic columns
`Q_AA^-1 B` have been constructed at charged cost.  For any frontier vector
`y`, its exterior response can be written as

```text
direct sparse term b(y) - C^T t(y),        t(y) in R^r.
```

For every hierarchy group, the squared norm of this vector expands into the
three additive summaries `sum b^2`, `sum C b`, and `sum C C^T`.  Hence the
group value for the single positive whitened probe is evaluated exactly with
`O(r^2)` arithmetic per reached group, without target-side random sketches.
Chebyshev evaluation of the frontier inverse square root costs
`O_tilde(r vol(F)/sqrt(alpha))` sparse/harmonic work under the supplied bank.
The packing above bounds the reached groups by `O(|F|/lambda)` per level.

This is a complete deterministic **fixed-epoch, supplied-bank** reporter.
It becomes useful when `r=polylog(M)` and the bank is shared by many frontier
events.  It is not a general moving-face theorem: constructing the bank needs
`r` anchor responses, refreshing it must be charged, and the comb tree has
`r=Theta(|A|)` with dense independent harmonic columns.  The positive probe
removes the Gaussian dimension, not the cut rank or response-maintenance
cost.

The same probe also has the earlier degree-weighted `l1` mass control.  The
stationary identity followed by Cauchy--Schwarz and `K<=I` gives

```text
sum_v d_v p_v
 <= sqrt(d_F)^T K^(1/2)1_F
 <= sqrt(vol(F)|F|)
 <= vol(F).
```

For a complete fixed face `T`, the sparse-matvec version is

```text
p_T=-D_W^{-1/2}Q_WT Q_TT^{-1/2}1_T.
```

It dominates every conditional response row supported on `T` and has
weighted squared mass at most `|T|`.  Chebyshev or the positive-resolvent
ladder evaluates the inverse-square-root action using only `Q_TT` products in
`O_tilde(vol(T)/sqrt(alpha))` work.  Geometric checkpoints therefore have a
summable fixed-face cost.  As with the ordinary positive inverse probe, the
unresolved step is how to cover the online interval between checkpoints
without replaying the old face.

The ordinary inverse probe above remains useful when one wants a particularly
simple positive SDDM solve and an `l1` candidate list.  It should not replace
the whitened probe inside the group reporter: its squared mass can lose a
factor as large as `1/alpha`.  Conversely, the whitened result is a static or
causally append-only group-oracle theorem; materializing its exterior column
or all group sums is still charged and is exactly the open `CenterLift`
input to `BoundaryReportGivenLift`.

There is also an entrywise **upper** rational approximation, so a fixed-face
whitened oracle need not rely on the right-rectangle lower approximation from
the positive-resolvent note.  Let

```text
t_0=eta sqrt(alpha),
t_(j+1)=(1+eta)t_j,
T=t_J>=1/eta,
```

and define

```text
r_+(K)=(2/pi)[
  t_0 K^{-1}
  +sum_(j<J)(t_(j+1)-t_j)(K+t_j^2 I)^{-1}
  +((T^2+1)/T)(K+T^2 I)^{-1}
].
```

Then, entrywise and uniformly for every Stieltjes `K` with
`alpha I<=K<=I`,

```text
r_+(K) >= K^{-1/2},
```

while scalar functional calculus gives

```text
r_+(x) <= (1+O(eta))x^{-1/2},       x in [alpha,1],
```

and the total shifted work mass is `O(1/sqrt(alpha))`.

The proof is completely positive.  In the Stieltjes integral

```text
K^{-1/2}=(2/pi) integral_0^infinity (K+t^2I)^{-1} dt,
```

the lower tail is entrywise at most `t_0K^{-1}`, and left rectangles majorize
the decreasing resolvent on every middle interval.  For the upper tail write
`K=D-A`, with `A>=0` and `D<=I`.  Comparing every nonnegative Neumann-walk
term gives, for `t>=T`,

```text
(K+t^2I)^{-1}
 <= ((T^2+1)/t^2)(K+T^2I)^{-1}       entrywise.
```

Integration produces the last term of `r_+`.  The omitted/overcounted scalar
tails and the geometric rectangle distortion are `O(eta)` relative error;
the same integral comparison proves the work-mass bound.

Consequently

```text
p_+=-D_W^{-1/2}Q_WT U r_+(K)1_F
```

entrywise dominates the exact whitened probe, and its weighted squared mass
is `O(|F|)` because
`r_+(K)K r_+(K)<=(1+O(eta))^2I`.  With source `sqrt(d_F)`, the analogous
degree-weighted `l1` mass is `O(vol(F))`.  This closes a fixed-operator
one-sided oracle.  It does **not** make a literal partial sparse settlement
one-sided: unfinished shifted solves remain lower approximations.  Certified
linear-solve error or an exact resolvent application must still be included,
and moving-face response reuse remains open.

More operationally, let a normalized frontier correction have coefficient
vector `a`, energy `E=||a||_2^2`, and normalized exterior response `Ba`.
Every row capable of changing a boundary value by at least `m` is contained
in

```text
C(F,E,m):={v:p_v>=m/sqrt(E)},
vol(C(F,E,m)) <= vol(F) sqrt(E)/m.             (candidate ledger)
```

Exact validation of this deterministic superset removes false positives.  If
the frontier blocks are disjoint, their total volume is at most `M`, and
their orthogonal energies sum to `E_tot`, then even counting repeated
candidates with multiplicity gives

```text
sum_j vol(C(F_j,E_j,m))
 <= (sqrt(E_tot)/m) sum_j vol(F_j)
 <= M sqrt(E_tot)/m.                            (global candidates)
```

There are two different uses of this formula.  If `E_j` is the energy of the
*exact* correction, only `E_tot<=alpha` is available; the resulting
`M sqrt(alpha)/m` can still be too large when the semantic margin `m` is
small.  It must not be advertised as the target work bound by itself.  If
instead `E_j` is the freely allocated numerical-error energy of the
orthogonal lifted solves, choose

```text
E_tot <= m^2/alpha.
```

Then every noncandidate row has error below `m`, while the complete
candidate-validation volume is at most

```text
M/sqrt(alpha).
```

Tightening the aggregate energy tolerance to this value changes a
Chebyshev/CG solve only through a logarithm.  In this error-reporting role,
the probe is therefore sufficient for the candidate and validation part of
the balanced meta-theorem.  This is the first graph-specific deterministic
replacement for the Gaussian trace layer that removes the extra
frontier-rank factor.  It is also simpler than an inverse-square-root probe:
the source is just `s_F` and the operator is the ordinary current-face SDDM
inverse.

The theorem closes **candidate packing**, not yet response-summary production
time (`CenterLift`).
On one fixed face, deterministic Chebyshev/CG plus the lower-envelope adapter
computes a no-false-negative approximation to `p` and one cut scan lists the
candidates.  Along nested faces, recomputing `Q_TT^{-1}E_Fs_F` after every
small expansion can still pay the old-face volume repeatedly.  A fully
charged theorem needs either an aggregate positive-response flush, or a
rent-or-buy schedule that proves all these probe solves and cut scans total
`O_tilde(M/sqrt(alpha))`.  The endpoint-path warm-restart regression remains
a test of exactly this missing moving-face implementation.

There is a stronger causal cumulative form.  For nested faces, let `B_j` be
the new batch, `L_j` its exact lift, `K_j` its frontier Schur complement, and

```text
U_j=L_j K_j^{-1/2},
C_j=-D_W^{-1/2}Q_WV U_j >= 0
```

on any set `W` that is still exterior at the current time.  The columns of
the `U_j` are mutually `Q`-orthonormal.  Define

```text
Lambda_v^2 = sum_j ||C_j(v,:)||_2^2.
```

The direct inverse-square-root probe

```text
p_v^min = sum_j (C_j 1_(B_j))_v
```

satisfies `p_v^min>=Lambda_v`.  Indeed, all entries are nonnegative, so the
sum of the row `l1` norms dominates the Euclidean norm of the concatenated
row.  Its mass is at most the total batch volume.  For one batch,
`q=QU_j1_(B_j)` vanishes on the old face, equals `K_j^(1/2)1_(B_j)` on the
batch, and is nonpositive outside.  The stationary identity,
Cauchy--Schwarz, and `K_j<=I` give

```text
sum_(v still exterior) d_v (C_j1_(B_j))_v
 <= sqrt(vol(B_j)|B_j|)
 <= vol(B_j).
```

Keeping the batch columns separate gives the stronger squared group ledger
`sum_j sum_v d_v(C_j1_(B_j))_v^2<=sum_j|B_j|`; summing the positive columns
into one scalar probe trades that square ledger for the displayed causal
`l1` ledger.

Even the fractional source is unnecessary.  The ordinary positive solve may
use either `sqrt(d_(B_j))` or the simpler all-ones source.  With the latter,

```text
u_hat_j
 = Q_(S_(j+1),S_(j+1))^{-1} E_(B_j) 1_(B_j)
 = L_j K_j^{-1} 1_(B_j)
```

produces an exterior probe

```text
p_hat_j=C_j K_j^{-1/2}1_(B_j).
```

As in the fixed-pair proof, `K_j^{-1/2}1_(B_j)>=1`, so
`p_hat_j` also dominates the row norm of `C_j`; its weighted mass is at most
`sum_(u in B_j)sqrt(d_u)<=vol(B_j)` because the face right-hand side is
exactly `E_(B_j)1_(B_j)`.  Consequently the fully causal deterministic sum

```text
p_hat=sum_j p_hat_j
```

obeys

```text
p_hat_v >= Lambda_v,
sum_v d_v p_hat_v <= sum_j vol(B_j) <= M,
vol{v:Lambda_v^2>=lambda} <= M/sqrt(lambda).
```

No independence or oblivious trace is needed, so the statement remains true
when every later batch is chosen from earlier answers.  It also avoids
counting the same candidate separately for a single checkpoint query, or for
the first crossing of one fixed probe threshold.  It does **not** license
rerunning the complete hierarchy after every batch for free: a still-exterior
false candidate can be revisited as its slack and accumulated probe change.
Avoiding those repeated visits still requires the epoch/two-ledger scheduler.

At a geometric checkpoint one can compress all history further.  On the
current face `T`, the full probe

```text
u_T=Q_TT^{-1}1_T,
p_T=-D_W^{-1/2}Q_WT u_T
```

dominates the response leverage of every `Q`-orthonormal subspace supported
on `T`, hence in particular all earlier lifted-frontier spaces.  Its mass is
at most `vol(T)`.  Rebuilding this probe only after face volume doubles has
geometrically summable *base face volume*.  This does not by itself handle
the interval between rebuilds: a path can force many singleton admissions
while the face volume ratio remains arbitrarily close to one.  A complete
doubling scheme therefore still needs a rent branch that produces or safely
delays the new-batch probes at frontier-charged cost.  Stating the full probe
without that branch would repeat the already refuted ``sleep until doubling''
schedule.

### 6.3 Conditional end-to-end meta-theorem

The balance can be stated without hiding the missing step.  Suppose a
deterministic implementation maintains nested support-safe faces and has the
following charged producer; combine it with the now-closed companion
reporting ledger.

```text
CenterLift(tau):
  processes all energy-heavy epochs and all disjoint frontier systems,
  persists the old-face responses, and emits certified additive group
  summaries in total O_tilde(M/tau) work;

BoundaryReportGivenLift(tau):
  from those summaries, locates and exactly validates all first-crossing
  boundary events in
  total O_tilde(M tau/alpha) work.
```

Suppose also that numerical errors add in the proved orthogonal frontier
energy norm and that the final residual certificate is recomputed exactly on
the materialized support and boundary.  Then the total charged work is

```text
T(tau) = O_tilde(M/tau + M tau/alpha),
```

and `tau=sqrt(alpha)` gives `O_tilde(M/sqrt(alpha))`.  This is a genuine
conditional algorithmic theorem: it identifies a sufficient producer
contract, and Chebyshev/CG is adequate for its numerical flushes.  It is not
an unconditional theorem because no deterministic general-graph
implementation of `CenterLift` with the stated response-production charge is
currently known.  In particular, canonical conservation and the positive
probe prove the second line only after the summaries exist; they do not prove
the first line.

## 7. Exact mapping to deterministic random-walk solvers

For a face `U`, degree scaling gives the SDDM matrix

```text
H_U = D_U^(1/2) Q_UU D_U^(1/2)
    = ((1+alpha)/2) D_U - ((1-alpha)/2) A_UU.
```

It is exactly the grounded Laplacian of an augmented undirected graph.  Give
every internal edge conductance `(1-alpha)/2` and connect `u` to a ground
vertex with conductance

```text
g_u = alpha d_u + ((1-alpha)/2) d_out,U(u).
```

The diagonal is then the sum of internal and grounding conductances.  Thus
the deterministic Eulerian/Laplacian machinery of *Derandomizing Directed
Random Walks in Almost-Linear Time* applies to every supplied face (the
undirected graph is an Eulerian special case).  Partial symmetrization gives
no additional structural gain here because the face system is already
symmetric.

What the paper concretely supplies is a deterministic
`M^(1+o(1)) log(1/eta)` face solve.  Rebuilding that solver for the
`O_tilde(1/sqrt(mu_bar))` certified faces gives the race in Section 3.  Its
construction relies on subpolynomial-quality deterministic sparsification;
it does not provide a linear-or-polylog-overhead sparse-face primitive that
would erase the `M^o(1)` factor.  Nor does it report the next active boundary
set without evaluating the face response.  Consequently it improves the
random *linear algebra* call, but it does not solve the dynamic response
problem isolated above.

### 7.1 The paper's `beta` is not our spectral cutoff

The notation is potentially misleading.  In that paper, beta-partial
symmetrization replaces an Eulerian directed graph `G` by

```text
U^(beta)(G)=G+beta U(G),
L_(U^(beta)(G))=L_G+beta U(L_G).
```

Its purpose is to make a *directed* approximation robust enough for crude
sparsification; Richardson needs `O(beta)` applications to recover the
original directed solve.  On an undirected input, `U(G)=G`, so this operation
is simply

```text
L_(U^(beta)(G))=(1+beta)L_G.
```

It neither adds grounding nor changes the condition number.  In particular,
identifying that beta with a face cutoff cannot yield
`M/beta+M beta/alpha`: the first operation is a scalar rescaling on our
symmetric system, whereas the latter balance requires two genuinely
different work ledgers.

### 7.2 Where its `m^(o(1))` actually enters

The overhead is structural and global, rather than a consequence of failing
to notice the spectral floor `alpha`.

1. The deterministic expander decomposition quoted as Theorem 3.9 costs
   `m^(1+O(1/r)+o(1))(log m)^(O(r^2))`.  Choosing subpolynomial `r` is already
   an `m^(1+o(1))` construction.
2. The degree-preserving undirected sparsifier used inside global
   sparsification is itself constructed in `m^(1+o(1))` time (Lemma 4.10).
3. In the squaring framework, a block of
   `d=Theta((log n)^(1/3))` sparsified squarings has `n^(o(1))` fill.  Blocks
   are linked by global sparsification and the recursive solver has
   `n^(o(1))` branches.

A known `alpha` can shorten the number of squarings needed to reduce the
remaining condition number, and hence can improve hidden logarithms or avoid
some late recursion on a very well-conditioned instance.  It does **not**
turn the initial deterministic expander decomposition or degree-preserving
sparsifier into a linear-time construction.  On our already symmetric face,
the more relevant comparison is therefore the explicit race

```text
deterministic KMP-style solve:       M^(1+o(1)) polylog(1/eta),
deterministic Chebyshev/CG solve:    M/sqrt(mu_U) polylog(1/eta).
```

The ballasted broom in Section 2.2 then rules out summing the second line over
fresh nested faces, while the first line retains the subpolynomial factor and
has the same moving-face replay problem.  Nothing in the KMP squaring chains
provides a persistent Schur lift, delayed-boundary-defect account, or
output-sensitive active-set reporter.  Thus the paper is useful as a
deterministic *single supplied-system* fallback, but it supplies neither side
of the missing moving-face rent-or-buy interface.

The Perron analysis above makes the closest useful connection to KMP's
expander machinery precise.  If an expander hierarchy is already supplied,
its cluster gap certificate isolates one positive coarse mode; Perron
survival pays the serial coarse ancestry and Chebyshev pays the reflected
mean-zero modes, giving the conditional hierarchy ledger
`A_H/tau+B_H tau/alpha`.  KMP can therefore support the *static certificate*
side of this architecture.  Its full-graph `m^(1+o(1))` hierarchy/squaring
construction, however, does not select a support-local laminar family under
face growth and does not retain Green/Schur state when a boundary is
unpinned.  It consequently does not discharge either `B_H=O_tilde(M)` for
the online chronology or the persistent-response premise.  This distinction
is important: the new Perron lemma strengthens what one can prove **given**
the right hierarchy, rather than turning the KMP solver itself into the
requested active-set algorithm.

## 8. Certification problem

The parameterized depth theorem requires a lower bound on the final face,
not an eigenvalue estimate of the current face.  Safe sources include:

1. a known envelope `W superset S*` and a certified lower bound for `Q_WW`;
2. a structural promise on every reachable final support;
3. a Dirichlet conductance or Poincare lower certificate for such an
   envelope;
4. a new a-posteriori terminal certificate strong enough to validate a
   guessed spectral cap.

For Dirichlet conductance `phi_D`, Cheeger's inequality yields

```text
mu_* >= alpha + ((1-alpha)/4) phi_D(S*)^2.
```

Thus the CG branch is certified by conductance on the order of
`alpha^(1/4)`, while absorption of the deterministic overhead needs only
conductance on the order of `f(M) sqrt(alpha)`.

## 9. Follow-up literature audit

The closest follow-ups found so far give the following concrete comparison.

| Work | What transfers | Why it does not settle this target |
|---|---|---|
| Li--Vaughn, deterministic spectral sparsification (2026) | New deterministic sparsification via pessimistic estimators and polynomial inverse-square-root/exponential approximations. | Time `m^(1+o(1))+O_tilde_eps(n^2)`: useful for dense graphs, not a linear-overhead primitive on sparse local faces. |
| Marcussen--Pyne--Rubinfeld, catalytic-logspace spectral sparsification (August 2026) | Gives a deterministic pessimistic estimator for effective-resistance sampling and a near-optimal-size sparsifier in catalytic logspace.  It is the newest direct derandomization follow-up and its greedy potential is conceptually relevant to replacing Gaussian/edge sampling. | The theorem optimizes workspace, not running time: the final construction may brute-force over `2^B` strings with `B<=n^3`, and the simpler greedy version repeatedly evaluates a global trace-exponential/effective-resistance potential.  It starts from the full graph and produces only a spectral sparsifier, not an inverse response or solution coordinates.  It therefore does not improve KMP's time or the moving-face producer. |
| Wei--Yang, simple active-set PageRank (2026) | The same limiting-face SDD viewpoint; randomized `O_tilde(1/eps^2)` ACL PageRank and an RPPR active-set method. | Direct ACL work beats `1/(eps sqrt(alpha))` only in the coarse regime `eps` larger than about `sqrt(alpha)`.  Its RPPR theorem pays `O_tilde(|S*| vol(S*))`; deterministic substitution explicitly restores a `|S*|^o(1)` factor. |
| Huang et al., accelerated evolving sets (2025) | Only `O_tilde(1/sqrt(alpha))` shifted proximal systems; each inner system has constant condition after choosing a unit-scale shift. | Their `R` is a run-dependent ratio of initial scaled-gradient `l1` masses, not cut rank or a reusable Schur parameter, and the PPR bound is `O_tilde(min{m,R^2/eps^2}/sqrt(alpha))`.  For the variational/RPPR objective they explicitly leave effective localization of ISTA/coordinate descent open because momentum initializations lose the required nonnegativity. |
| Yang et al., ChebyPush (2024) | Explicit subset-Chebyshev recurrence and delayed-defect compensation. | Local theorem assumes bounded `||T_k(P)||_1`, refuted uniformly by regular trees; even conditionally the PPR local bound contains `K^2=O_tilde(1/alpha)`. |
| Zhou et al., LocalCH (2024) | A forced second-order recurrence for masked Chebyshev and practical local acceleration. | Accelerated work assumes a favorable run-dependent geometric mean of masking-noise ratios. |
| Fountoulakis--Martinez-Rubio, classical acceleration for RPPR (2026) | A deterministic FISTA analysis with over-regularization and an explicit no-percolation/confinement condition.  Under confinement it proves a core term `O_tilde(1/(rho sqrt(alpha)))`. | The additional transient-boundary term is `O(sqrt(vol(B))/(rho alpha^(3/2)))`; a seed-at-leaf star makes standard FISTA activate a degree-`m` center and incur `Omega(m)` work although the optimum has one vertex.  This is a structural conditional result, not a general response-reuse primitive. |
| Calder--Yezzi, PDE acceleration for obstacle problems (2018) | A damped-wave/heavy-ball discretization rigorously replaces the diffusive CFL scale by the square-root/wave scale and is numerically effective for penalized obstacle problems.  The paper explicitly observes that optimal damping depends on the first Dirichlet eigenvalue of the unknown free domain. | Its complexity counts full-grid sweeps (the same global order as CG for a linear problem); the obstacle experiments use a large finite penalty and supplied spatial domain.  It neither discovers only the final graph support nor persists responses across changing free domains.  It supports adaptive damping in a numerical backend, not the local `CenterLift` theorem. |
| Ang--De Sterck--Vavasis, MGProx / FastMGProx (2024) | Adaptive restriction zeros coarse variables at currently nonsmooth/active fine coordinates, proves a fixed-point property and descent of the coarse correction, and performs well empirically on an elastic obstacle problem.  It is a credible practical supplied-hierarchy backend and closely matches the idea of a support-aware coarse solve. | The proved strongly-convex rate is exactly the proximal-gradient fallback `(1-mu/L)^k`; FastMGProx proves the generic `O(1/k^2)` first-order rate.  The authors explicitly leave the observed multigrid speedup unexplained by a stronger rate.  Each experiment uses the full supplied mesh and coarse hierarchy, with no output-local discovery, changing-principal response, or work bound in `vol(S*)`.  It therefore supports the conditional `NestedExpanderLift` architecture but does not instantiate it. |
| Schmelzer--Stoll, Non-Negative Conjugate Gradients (July 2026) | Wraps matrix-free CG in a primal--dual principal-pivot loop for nonnegative quadratics.  Its inexact-decision lemma proves that a residual below the finite decision margin follows exactly the same active-set trajectory as exact solves; this independently validates our residual/certification layer.  Each fixed free-set solve retains the usual `O(sqrt(kappa))` CG rate. | The method explicitly restarts CG whenever a variable is dropped or re-admitted.  Its total count is `s O(sqrt(kappa))`, where `s` has only finite termination; the paper states that the `2^n` ceiling is not an efficiency estimate.  It scans a supplied variable set, its randomized Nystrom option is not deterministic, and the paper itself notes that factorized preconditioners generally do not restrict cheaply to changing free sets.  On our monotone Stieltjes specialization it is therefore a fresh-face method stopped by the ballasted broom, not response reuse. |
| Papadopoulos--Hintermueller, mesh-dependent PDAS iteration growth (August 2026) | Proves a sticky-active-set theorem for finite-element obstacle problems: an interior active degree of freedom cannot deactivate until the inactive boundary reaches it, so the method peels only layer by layer.  The experiments show nearly doubling iteration counts under refinement despite finite-dimensional local superlinear convergence. | This is a different PDE discretization and a shrinking/deactivation chronology, so it is not a lower bound for our monotone growing PageRank face.  It does rigorously show that local semismooth-Newton/identification theory alone gives no mesh-independent Stage-I active-set count; multilevel or persistent transport must be analyzed separately. |
| Martinez-Rubio--Wirth--Pokutta (2023) | Deterministic accelerated sparse optimization and conjugate-direction variants for positive-definite M-matrices. | Bounds retain support-size/repeated-subspace factors and do not give output-linear changing-face reuse. |
| Saranurak--Wang, expander decomposition/pruning (2019) | Their static theorem has exactly the formal balance ingredients: randomized `O_tilde(M/tau)` construction, clusters of conductance `tau`, and `O_tilde(M tau)` crossing edges.  Their expander-pruning theorem is deterministic and reuses local flow across a short sequence of edge deletions. | The static decomposition is randomized.  Deterministic pruning assumes the initial expander and handles deletions; reversing our insertion chain requires knowing the final support and reading it first.  Neither theorem maintains the coarse Schur/solution response, so even a supplied decomposition leaves `CenterLift` open. |
| Fleischmann--Li--Li, faster weak expander decompositions (2025) | Warm-starts both sides of every sparse cut simultaneously, removing one recursion-depth factor; the static construction uses `O(log^2 n)` cut-matching rounds and gives a true laminar partition/near-expander certificate.  This directly addresses the repeated-large-remainder *static construction* concern. | Its cut player samples a random direction, it is run on one fully supplied graph, and its output is a weak mixing/cut certificate rather than a Green or terminal-Schur state.  It can improve the certificate producer after the final support is known, but it neither discovers that support locally nor transports responses across face insertions. |
| Chuzhoy--Parter, fully dynamic low-diameter router decomposition (2026) | Deterministically maintains proper, edge-disjoint router clusters with bounded vertex overlap under adaptive insertions and deletions starting from an empty graph.  Proper internal routing is stronger than a purely ambient path certificate and is the newest plausible deterministic hierarchy producer for a growing explored graph. | The stated overlap, congestion, recourse, and update bounds are `n^(o(1))`/`n^(O(delta))`, with router parameters `k<=log(n)^(1/49)`; they do not become polylogarithmic.  The data structure preserves routing/spanner demands, not a grounded spectral approximation or the coarse Schur/Green state.  It can instantiate a subpolynomial-overhead structural hierarchy, but neither removes the forbidden small `o(1)` nor supplies `CenterLift`. |
| Zhao, fully dynamic directed spectral/cut sparsifiers (2025) | Gives polylogarithmic amortized edge-update time after near-linear preprocessing; for sufficiently large partial symmetrization it also gives a deterministic dynamic degree-preserving spectral approximation.  This is a genuine dynamic follow-up to the KMP partial-symmetrization framework. | The general high-accuracy spectral sparsifier is randomized/oblivious-adversary, while the deterministic partially symmetrized theorem requires a polylogarithmic symmetrization level.  More fundamentally, all variants preprocess the supplied ambient graph and maintain a two-sided sparsifier, not an output-local inverse, Perron coefficient, active-set separator, or persistent principal Schur response. |
| Gottesbueren--Parotsidis--Probst Gutenberg, practical expander decomposition (2024) | Implements and substantially accelerates the Saranurak--Wang construction while preserving its formal guarantees; this is the most relevant experimental backend for the proposed conductance branch. | It is a static full-input decomposition/engineering result.  It does not make the construction deterministic, insertion-local, or response-maintaining, so it improves a practical experiment rather than the `NestedExpanderLift` theorem. |
| Ruotolo--Vadhan, singular values versus expansion (2025) | Gives directed Cheeger and higher-order Cheeger analogues, strengthening the interpretation of how many slow directed modes an expander-like cluster may possess. | Our face matrices are already symmetric, where the needed reflected-cluster Cheeger statement is classical and proved above.  The paper supplies no nested active-set solver, Schur response, or no-miss reporter. |
| Goranci--Henzinger--Peng (2018); Durfee--Gao--Goranci--Peng (2019), dynamic approximate Schur complements / spectral vertex sparsifiers | They explicitly maintain terminal Schur information and, in the latter work, changes to a Laplacian demand with query access to solution coordinates.  This is the closest operator interface to the missing moving-face primitive. | The separable-graph guarantee costs about `sqrt(n)/eps^2` per update/query and assumes a global separator hierarchy.  The general-graph solver is randomized/expected-amortized, costs about `n^(11/12) eps^-5` per update/query, periodically rebuilds global structures, and returns two-sided energy approximation.  The separable-graph paper also gives OMv-conditional barriers for much faster arbitrary incremental/decremental effective-resistance queries.  Our canonical one-source nested sequence is narrower, but a purported arbitrary-demand `CenterLift` would be too strong. |
| Jiang--Peng--Weinstein, dynamic least-squares regression (2022) | Gives a randomized insertion-only data structure robust to adaptive row updates, with near-input update work plus an additive dense-dimensional term; it also identifies the exact Kalman/Woodbury `Theta(d^2)` response update as the natural unrestricted baseline.  This is a useful warning against silently upgrading `CenterLift` to an arbitrary-demand dynamic inverse. | Under OMv, fully dynamic constant-relative-error LSR and insertion-only inverse-polynomial-accuracy LSR require `d^(2-o(1))` amortized update time.  These are conditional lower bounds for unrestricted dense regression rows/labels, not for nested principal submatrices of a sparse Stieltjes graph with one canonical source.  The positive upper bound is randomized and contains an additive `epsilon^-4 d^5` term.  Hence this scopes the interface but does not rule out the source-local graph theorem sought here. |
| Yeung--Pothen--Halappanavar--Huang, AMPS principal-submatrix updates (2017) | Reuses one sparse `LDL^T` factor and proves that the update work is governed by the elimination-tree closure of the modified indices, rather than by the ambient dimension.  Its partial-substitution calculation directly motivates the proved `R_chol` dynamic-fill-reach branch above and is a practical implementation option when actual fill is localized. | It presupposes an already factored full supplied matrix and its final solution step can still cost `nnz(L)` per update; the paper reports experimental speedups, not an output-local worst-case theorem.  On arbitrary admission orders the closure or fill can be quadratic, and embedding all future coordinates by pinning destroys our locality. |
| Shmueli--Drineas--Avron, low-rank square-root updates (2023) | A rank-`k` SPD perturbation changes the inverse square root by a matrix whose singular values decay geometrically in blocks of size `k`; the resulting epsilon-rank is `O(k log(kappa_hat)log(1/epsilon))`.  Since appending a batch differs from `A_U direct_sum F` by rank at most `2|B|`, this supplies a rigorous per-batch compression theorem for the deterministic inverse-square-root probe. | Their Riccati construction costs `O((T_(A^1/2)+T_(A^-1/2))r^2+n r^4)` and assumes applications of the old square-root operators.  In the moving-face recursion that assumption is `CenterLift`; dense correction factors accumulate, online recompression is uncharged, and the guarantee is two-sided rather than entrywise.  It motivates `LowRankSqrtUpdate(tau)` but does not prove its `M/tau` work. |
| Gao--Kyng--Spielman, practical approximate elimination (2023) | A robust SDDM implementation based on approximate Cholesky and PCG; useful as an experimental fixed-face backend. | It samples fill while eliminating one supplied system; it is not a deterministic theorem amortizing nested principal systems or revealing unseen active rows. |
| Augmented/recycled CG literature (surveyed by Soodhalter--de Sturler--Kilmer, 2020) | Supplies the correct residual-projection framework for sequences of changing SPD systems and practical recycle-space truncation strategies. | On a growing principal face, the projection is exactly `[P;0]G^-1P^T H_UB`, becoming the dense Schur lift when the recycle space is complete.  Published convergence is in terms of recycle-subspace quality; it gives no source-local rule that bounds discarded frontier modes or the dense basis-application cost by `vol(S*)`. |
| Bolten--de Sturler--Hahn, recycling for evolving structures (2020); Burke--Frommer--Ramirez-Hidalgo--Soodhalter, recycling for matrix functions (2022) | The first explicitly transports approximate invariant spaces when the mesh and algebraic dimension change; the second gives augmented methods for matrix functions with changing matrices and unrelated right-hand sides.  They are the closest numerical templates for retaining CG/Chebyshev information across our nested faces. | Both take the transport/recycle space as supplied and assess its quality numerically or through projected convergence quantities.  They give no output-local construction or cumulative rank bound.  In our principal-extension algebra their transport step must recover the frontier defects `P^T H_UB`, while exact preservation requires the dense combination `[P;0]G^-1P^T H_UB`; this is the already-isolated `CenterLift`, not a cheaper theorem hidden in recycling terminology. |
| Kadeethum--Ballarin--Choi--Lee, online spectral deflation for state-constrained optimal control (2026, arXiv:2606.17971) | Directly studies repeated restricted SPD Schur systems under changing active sets.  It computes low modes of one full-domain reference, restricts them to each inactive set, and uses A-DEF2/Jacobi-CG with conditioning guards; this is a strong practical template for a supplied local envelope. | The active set is an input and outer-loop discovery is explicitly excluded.  Directional coherence after restriction is empirically diagnosed, not proved by interlacing.  Ambient eigenmodes require global preprocessing/storage, and no asymptotic local-work or rank bound is given.  Weak clique chains and long broom paths force the rank needed for a constant deflated gap to grow. |
| Gomez--He--Pang (2023), He--Han--Gomez--Cui--Pang (2024), parametric Stieltjes sparse-QP paths | For a nonnegative `l1`-regularized Stieltjes quadratic, the support path is monotone and has only linearly many breakpoints; parametric pivoting can trace it in a strongly polynomial number of steps.  This exactly matches the `rho`-homotopy of the global obstacle form above. | Their condensed matrix operations apply/update principal inverses and solve bounded-variable QPs.  The guarantee counts pivots, not adjacency work; generic implementations are low-order polynomial (`O(n^3)` in the related bounded Stieltjes-QP result, `O(n^2)` for tridiagonal structure).  The new-column operation is our dense Schur/DtN lift, and tracing `Theta(|S*|)` breakpoints can exceed the threshold-depth bound. |
| Chang--Chen--Munro--Peng--Shi--Zheng, sandpile prediction (2023) | Demonstrates the right kind of event compression on structured graphs: compute all firing counts in `O(n log n)` on trees and `O(n)` on paths, rather than simulating individual topplings.  Its least-action formulation is closely analogous to the least-superharmonic obstacle solution. | It is an integral Abelian sandpile, not the killed continuous quadratic obstacle.  Its general one-sink bound is `O(R m^2 log(nN))` iterations, not local or near-linear.  The tree data structure supports the existing tree/width branch but does not implement a general-graph `CenterLift`. |
| Vegh, separable convex quadratic flows (2012); van den Brand et al., deterministic min-cost flow (2023) | The grounded-flow dual places the obstacle in the family of network convex optimization/LCP problems.  These works show deterministic polynomial solvability and sophisticated response persistence for ordinary min-cost flow. | The exact general quadratic-flow theorem costs `O(m^4 log m)`.  The modern deterministic ordinary min-cost-flow theorem is `m^(1+o(1))`, assumes the full graph and integral linear costs, and gets its speed from subpolynomial dynamic graph machinery.  Neither supplies a support-local, no-`o(1)` quadratic diode-network solver. |
| Livne, NLF resistor-network convex-flow solver (2026) | Damped chord-Newton reduces a smooth undirected nonlinear flow equilibrium to only `2--4` weighted Laplacian solves in the reported experiments, with approximate Cholesky or LAMG+ as interchangeable linear backends.  This is a useful practical template for batching several smooth corrections on one supplied graph. | The paper explicitly labels its wall-clock `O(m)` behavior empirical, not proved.  It assumes a full undirected graph and smooth signed edge laws; directed variants are future work, and it does not implement nodal obstacle/box constraints, support-local discovery, or a growing-principal inverse.  Therefore it can replace the numerical backend in experiments but not `ShiftedProxClosure` or `CenterLift`. |
| Farfan--Ghadiri--Yang, entrywise SDDM solving (2025/2026) | For one invertible SDDM matrix and nonnegative right-hand side, computes an entrywise multiplicative approximation in `O_tilde(m 2^(O(sqrt(log n))))` bit operations.  Its threshold-decay framework is explicitly designed to recover large unknown coordinates by solving only a boundary-expanded subsystem. | The theorem is randomized with high probability: its inverse-distance cover samples random source sets and calls randomized normwise Laplacian solves.  The cover has `2^(O(sqrt(log n)))` overlap, so it retains the forbidden subpolynomial factor.  It is precomputed for one fixed matrix and shrinks a remaining index set; our faces grow and their cut-supported right-hand sides change sign between faces. |
| Zhao, fully dynamic directed spectral sparsifiers (2025/ICALP 2026) | Maintains directed spectral sparsifiers with polylogarithmic amortized edge-update time; one coarse partial-symmetrization layer has a deterministic dynamic patching construction. | The full explicit sparse guarantee is high-probability and starts with global ambient preprocessing.  The paper itself obtains a dynamic RCDD solve by running a *static* directed solver on the maintained sparsifier; it does not maintain inverse/Schur responses or solution coordinates.  On our undirected faces partial symmetrization is again only rescaling, and rebuilding/static-solving after each face retains the old factor. |
| Goranci--Kyng--Probst Gutenberg--Zhao--Zoecklein, online/stable sparsification (2026) | The online paper proves adaptive-stream leverage-score sampling with near-linear graph-stream processing; the stable-sparsifier paper partitions monotone edge updates into epochs using cumulative online leverage and changes its sparsifier only `O_tilde(n/epsilon)` times.  The stability fact `sum leverage=O(n log n)` is a useful checkpointing analogy for our response epochs. | Both final sparsifiers are randomized.  The cited deterministic online-BSS alternative uses a dense `d^2` state.  The stable oracle has `O_tilde_epsilon(n^2)` total update time and answers pair effective resistance/maxflow, not a solution vector.  Activating a principal vertex is an unpinning operation: boundary-to-ground edges become internal couplings, so it is not an insertion-only PSD row stream; a finite pinning reduction gives leverage near one per activated coordinate and requires the final ambient vertex set.  Even a maintained spectral sparsifier still needs a static solve and supplies no coordinatewise no-miss response. |
| Sachdeva--Thudi--Zhao (2024); Jambulapati--Sachdeva--Sidford--Tian--Zhao (2024), Eulerian sparsifier follow-ups | Improve the sparsity of directed Eulerian approximations; the latter gives a high-probability polylogarithmic-time Eulerian solver after randomized effective-resistance decomposition. | The faster construction/solver is randomized, while the deterministic construction is polynomial or `m^(1+delta)`/almost-linear.  Both solve one supplied operator.  They do not improve KMP into a deterministic `m polylog m` moving-principal-response data structure. |

There is an additional operator mismatch in the dynamic-terminal row which
is easy to miss.  If the active face is `U` and the unread exterior is `W`,
declaring `U` to be the terminal set of the ambient graph maintains

```text
SC(Q,U)=Q_UU-Q_UW Q_WW^-1 Q_WU,
```

not the Dirichlet operator `Q_UU` used by the obstacle face.  The difference
can be a factor `Theta(1/alpha)` already on one unit edge:

```text
Q=[[a,-c],[-c,a]],       a=(1+alpha)/2, c=(1-alpha)/2,
Q_{11}=a,                SC(Q,{1})=a-c^2/a=alpha/a.
```

Thus exact terminal-Schur maintenance would include paths through vertices
which the safe local algorithm has not admitted.  Pinning `W` to ground and
then taking the pinning conductance to infinity recovers `Q_UU`, but every
activation becomes a high-leverage *pin deletion*, as quantified below.
This is why the superficially matching `AddTerminal` operation is not itself
`CenterLift`.  It can become useful inside a supplied current face--for
example to eliminate a certified fast complement onto landscape wells--but
then the face insertion, deterministic/local initialization, and response
lifting costs remain exactly the open clauses.

The dynamic-expander follow-ups do not remove those clauses.  Current
polylogarithmic-update *expander* decompositions use randomized
initialization/cut certificates, while the deterministic weighted static
construction costs `m^(1+1/r) polylog(m)^(O(r))`; taking growing `r`
restores the same `m^(1+o(1))` factor.  Deterministic dynamic router
decomposition is now available, but its overlap/congestion/update guarantees
are themselves `n^(o(1))` and it preserves routability rather than Schur
response.  Decremental deterministic pruning can preserve an already
supplied expander, but our active graph is insertion-only and its final
support is unknown.  Reversing time requires first reading that final
support.  Even a hypothetical free dynamic decomposition would provide
only the clusters and crossing-edge ledger, not their moving coarse Schur
response, so it would close the structural half of `NestedExpanderLift` but
not the response half.

The router-to-spectrum translation is exact enough to rule out a hidden
better parameter.  Suppose an unweighted cluster routes every
degree-restricted demand with congestion at most `eta`.  For any cut with
`vol(S)<=vol(C\S)`, send `d_v` units out of each `v in S` and distribute the
same total over the other side without exceeding its vertex degrees.  Every
routing path crosses the cut, hence

```text
vol(S)<=eta |delta_C(S)|,       Phi(C)>=1/eta,
lambda_2(L_C)>=1/(2 eta^2).
```

Thus its deterministic mean-zero Chebyshev cost is `O_tilde(eta vol(C))`.
With the paper's `eta=n^(O(1/k))`, this is precisely an `n^(o(1))`
structural branch, not a polylogarithmic `M/tau` branch with freely chosen
`tau`.  This can still be absorbed when `1/sqrt(alpha)` is larger than the
subpolynomial overhead, just as for KMP, but it does not prove the requested
uniform no-small-`o(1)` result.  Moreover the argument produces only a gap;
it does not apply the cluster inverse to the chronological cut source.

The mismatch with monotone sparsifier streams has a sharp algebraic form.
Embed every future support coordinate in advance and pin every inactive
vertex to ground with conductance `Gamma`.  For an SPD final operator `A`, a
single pinned coordinate has matrix `A+Gamma e_v e_v^T`.  Its edge leverage
is exactly

```text
Gamma e_v^T(A+Gamma e_v e_v^T)^-1 e_v
 =Gamma a_v/(1+Gamma a_v),
a_v=e_v^T A^-1 e_v.
```

It tends to one as `Gamma` tends to infinity, which is precisely the limit
that enforces the principal-face condition `x_v=0`.  Hence every vertex
activation is a high-leverage deletion in this reduction; the stable-epoch
rule cannot group even a path's singleton activations.  Moreover the
reduction must allocate all of `S*` before local discovery.  This does not
lower-bound a response-aware tree or separator data structure, but it
rigorously rules out obtaining our moving-face theorem merely by feeding
principal activations to a monotone online sparsifier.

The direct citation census of KMP (arXiv/DOI records through 2026-08-31)
adds singular-value sparsification/expansion, practical expander engineering,
dynamic directed sparsification, Kemeny's-constant estimation, and
deterministic min-cost flow.  The technically relevant items are represented
in the rows above.  None maintains a growing principal inverse, an obstacle
prox closure, or coordinatewise boundary responses.  Thus the negative
follow-up conclusion is based on the actual citation family, not only on a
keyword search.

### 9.1 Entrywise SDDM threshold decay: close semantics, wrong cost model

The Farfan--Ghadiri--Yang theorem is unusually relevant because its output
guarantee is genuinely coordinatewise.  For integer SDDM `L`, nonnegative
`b`, and non-exponentially-small `epsilon`, it returns

```text
exp(-epsilon)(L^-1 b)_i <= xhat_i <= exp(epsilon)(L^-1 b)_i
```

simultaneously for every coordinate, with high probability, in

```text
O_tilde(m 2^(O(sqrt(log n))) log(U) log^2(U/(epsilon delta)))
```

bit operations.  Such a guarantee would make threshold comparisons robust
after inserting a constant slack: a coordinate above
`exp(epsilon) theta` cannot be missed, and a reported candidate can be
validated exactly before admission.  It can therefore replace the
*norm-to-coordinate certification* step of a fixed-face implementation.

It does not derandomize our algorithm.  The construction first defines a
distance from entries of `L^-1`, then builds a low-diameter cover by sampling
many independent source subsets `S` and approximately solving `Lx=1_S`.
The normwise solves are themselves probabilistic.  The resulting cover has
both diameter and overlap `2^(O(sqrt(log n)))`; its key amortization says each
vertex belongs to at most that many boundary-expanded systems.  Consequently
the paper moves the replay factor from all threshold stages into a
subpolynomial-overlap cover---precisely the factor the present target must
remove.

There is also a structural mismatch, with one useful monotonicity nuance.
Its global matrix `L` and its cover are fixed; threshold decay successively
*removes solved coordinates* and updates a nonnegative residual right-hand
side.  A cover built on the full ambient matrix can safely support its
principal subsystems: Dirichlet restriction only increases the paper's
inverse-probability distance.  Thus an ambient cover could in principle be
reused for all of our faces.  Constructing that cover, however, reads and
solves on the entire ambient graph in
`m 2^(O(sqrt(log n)))` work, so it destroys the required `M`-locality.

Building only on the currently explored face does not fix this.  Our exact
active-set chain successively *adds coordinates*; expansion increases Green
entries and can shrink inverse distance, so an old face's outer-separation
guarantee need not survive.  Under the canonical transform the face
right-hand side is nonnegative at any one time, but its increment when the
cut moves deletes old cut loads and adds new ones, hence is signed.  Moreover,
the paper's per-vertex `2^(O(sqrt(log n)))` participation proof uses the
geometric decay of one fixed solution and one decreasing unsolved set.  It
does not bound boundary-expanded sets for our sequence of changing cut
sources.  Rebuilding the cover per face is ruled out by the broom.

The paper therefore contributes two useful design clues, not an end-to-end
bound:

1. a boundary-expanded partial system is the right semantic object for
   finding large coordinates without solving the entire complement; and
2. entrywise multiplicative approximation is sufficient for no-miss
   thresholding with slack.

To transfer either clue deterministically, one would still need a persistent
inverse-distance cover or positive response hierarchy whose total overlap is
polylogarithmic across *growing principal faces*.  That is a reformulation of
`PositiveFrontierRentOrBuy`, not a proof of it.  In particular, feeding the
cut-supported right-hand side to the published partial solver silently
assumes the very face-dependent Dirichlet-to-Neumann response that must be
charged.

Zhao's dynamic directed-sparsifier follow-up is complementary but does not
fill this gap.  It can update a sparse spectral surrogate after individual
edge changes, and its adaptive partial-symmetrization layer contains a
deterministic star-patching construction.  The full near-linear-size dynamic
sparsifier still uses high-probability sampling/global decomposition, and the
solver application stated in that paper runs a static Eulerian solver on top
of the current sparsifier.  For a growing induced face, making each newly
internal edge an update can therefore make sparsifier maintenance cheap, but
the operation we need next remains

```text
apply the new principal inverse / Schur response to the moving source.
```

A spectral sparsifier does not store that vector.  Re-solving it after each
batch has the same restart ledger, while a dynamic solution query would be a
new theorem.  In addition, ambient initialization reads the whole graph and
violates locality when `M<<m`.  Thus this follow-up is useful evidence that
matrix *maintenance* and response *maintenance* must be kept distinct.

### 9.2 Online reference deflation: a useful conditional branch

Kadeethum--Ballarin--Choi--Lee (arXiv:2606.17971, June 2026) is the closest
new numerical follow-up to the cross-face Krylov question.  It studies a
sequence of restricted SPD Schur-complement systems created by changing
active sets.  Low eigenmodes of one full-domain reference operator are
computed offline, restricted and QR-orthogonalized on each current inactive
set, and used in A-DEF2 deflated Jacobi-CG.  Rayleigh--Ritz reselection, POD
enrichment, and coarse-Gram condition guards make this a credible practical
backend when a reusable reference domain is available.

Its exact transfer to our notation yields a clean promise theorem.  Let a
supplied reference basis have rank `r`, let `gamma_j^def` be a certified
lower eigenvalue of the projected/deflated complement on face `U_j`, and let
`C_ref` include constructing and exposing the relevant reference rows.  A
dense basis application costs `O(r|U_j|)` in addition to the sparse matrix
product.  The small Gram matrices can be updated along a nested principal
chain in `O(r^2 M)` total arithmetic once all basis rows are available.
Therefore A-DEF2/CG gives the fully explicit ledger

```text
T_def
 =O_tilde(
    C_ref+r^2 M
    +sum_j (vol(U_j)+r|U_j|)/sqrt(gamma_j^def)
  ).                                             (reference-deflation ledger)
```

In particular, if `r=polylog(M)`, `C_ref=O_tilde(M/sqrt(alpha))`, and every
reached restricted basis leaves a constant projected gap
`gamma_j^def=Omega(1)`, then the existing
`J=O_tilde(1/sqrt(alpha))` depth bound gives the desired deterministic target.
This is a meaningful favorable-instance branch, separate from bounded
treewidth.

The paper does not prove those promises.  It explicitly states that
interlacing controls eigenvalue *locations* but not directional coherence of
restricted reference eigenvectors; the usable cutoff rank is determined by
empirical principal-angle diagnostics.  Its experiments receive the active
set from an outer method and exclude active-set updates, KKT checks, and
outer-loop work.  The reference eigensolve and dense basis live on the full
ambient domain, which violates locality when `M<<m`.  Moreover, if the
certified projected gap is only `beta`, the last display still contains the
fresh-face factor `1/sqrt(beta)` on all `J` faces.  To make it constant, a
weakly coupled chain of `k` cliques needs rank `Omega(k)`, and a broom path of
length `Theta(1/sqrt(alpha))` has that many path frequencies below a constant
cutoff.  Hence no graph-uniform polylogarithmic-rank conclusion follows.

The practical recommendation is nevertheless concrete: on applications
with a natural local envelope and observed stable low-rank coherence, race a
small restricted reference basis against ordinary CG and the deterministic
SDD backend, while preserving the residual/retraction certificate.  This can
substantially improve running time, but its rank/coherence monitor is an
instance parameter rather than the missing unconditional theorem.

The three supplied active-identification papers fit after, rather than before,
this table.  Their exact interfaces are as follows.

| Supplied paper | Exact hypothesis and conclusion | RPPR translation and missing cost |
|---|---|---|
| Facchinei--Fischer--Kanzow, *On the Accurate Identification of Active Constraints* | The primal solution is a fixed isolated stationary point.  Given a primal--dual pair `(x,lambda)` in a sufficiently small neighborhood of its KKT set and an identification radius `r(x,lambda)` which tends to zero more slowly than distance to that set, Theorem 2.2 proves exact recovery of every active constraint by `g_i(x)<=r(x,lambda)`.  MFCQ makes the neighborhood uniform over the compact multiplier set (Theorem 2.3); identifying the strongly active subset uses SMFCQ/unique multipliers (Theorem 2.4). | This can certify an orthant once a near-KKT primal--dual pair and all tested slacks are already available.  It neither constructs that pair nor locates an unread graph constraint.  The identification radius is asymptotic and contains no adjacency-work or support-volume bound. |
| Lewis--Wright, *Identifying Activity* | For `h(c(x))`, Assumption 1 is the horizon-subdifferential transversality condition.  Theorem 2.2 starts with `x` near the critical point and a subgradient-graph pair satisfying small value, graph, and criticality residuals, and then certifies an actively sufficient graph piece.  Corollary 5.2 gives eventual manifold identification only when the multiplier is unique, lies in the relative interior, and convex `h` is partly smooth; the iterates and criticality residual must already converge. | For the nonnegative orthant this explains eventual face stabilization under a nondegeneracy/relative-interior margin.  It supplies no finite radius in graph-local work units, no way to discover a remote violated coordinate, and no bound for producing the convergent critical sequence. |
| Keskar et al., *A Second-Order Method for Convex l1-Regularized Optimization with Active Set Prediction* | The orthant-based adaptive method repeatedly predicts a face, approximately minimizes a smooth quadratic there (implemented with CG), corrects failed sign predictions, and globalizes against a full ISTA step.  The proved theorem assumes a continuously differentiable strongly convex smooth part with Lipschitz gradient and establishes global linear objective convergence of Algorithm 2. | It is a useful Stage-II implementation template, not a finite active-identification or output-sensitive theorem.  Its safeguard evaluates the ambient gradient/ISTA point, while its CG cost is stated in the chosen subspace dimension; neither operation is charged to the eventual local graph support. |

Consequently these papers can justify a final fixed-face phase, especially
under a strict inactive-multiplier or partial-smoothness margin.  They do not
find the graph boundary without evaluating its response, charge adjacency-list
work, or handle the deliberately margin-free threshold-depth theorem.  They
therefore do not replace Stage I or its SDD/response primitive.  In particular,
``eventual finite identification'' is not the same statement as an
`O_tilde(vol(S*))` boundary reporter: the former is conditional on a sequence
already converging in the ambient criticality norm, whereas producing and
checking that norm may itself read the whole graph.

No follow-up located through 2026-08-31 simultaneously supplies deterministic
sparse near-linear SDD solving, output-sensitive active-set reporting, and
the required local support guarantee.  Every candidate in the table is
checked against those three requirements rather than only against its
headline global solve time.

The Wei--Yang conclusion is especially diagnostic: it explicitly names
reuse between successive SDD solves on nested active sets as an open
direction.  Their suggested target is precisely to remove the extra active-set
iteration factor.  Their paper therefore confirms, rather than resolves, the
moving-face interface isolated here.  The Fountoulakis--Martinez-Rubio star
lower bound independently shows why simply replacing those restricted solves
by one global classical momentum trajectory is not a graph-uniform fix.

The parameter map in Wei--Yang can be made exact.  Their ACL theorem sets
the residue and activation margins to `lambda=kappa=epsilon/2`, reaches at
most `1/lambda=2/epsilon` active sets, and every face has
`O(1/lambda)` nonzeros.  Solving all of them from scratch gives

```text
T_WY,ACL=O_tilde(1/epsilon^2),
vol(output)<=2/epsilon.
```

Writing `M=Theta(1/epsilon)`, this is `O_tilde(M^2)`.  It beats the desired
spectral baseline `O_tilde(M/sqrt(alpha))` exactly in the coarse-output
regime `M=O(1/sqrt(alpha))`, equivalently `epsilon=Omega(sqrt(alpha))`.
This is a useful portfolio branch, not a solution in the hard regime of a
large localized output and small teleportation.

For the `l1`-regularized PageRank objective, their active sets stay inside
`S*`, but the theorem charges

```text
T_WY,RPPR=O_tilde(|S*| vol(S*)).
```

The randomness is only in the SDD calls.  Replacing them by the cited
deterministic almost-linear solver multiplies the ACL and RPPR bounds by
`(1/epsilon)^o(1)` and `|S*|^o(1)`, respectively.  Hence this newest direct
follow-up neither removes the small `o(1)` nor supplies cross-face reuse; its
own conclusion asks for an incremental or warm-started implementation to
move the ACL bound toward `O_tilde(1/epsilon)`.

Combining all proved branches gives a clean deterministic trichotomy.  Let
`mu_*=lambda_min(Q_(S*,S*))`, `s=|S*|`, `k` be the cyclomatic number of the
charged reference support, and let `R_chol,F_chol` be the observable
chronological fill-reach parameters defined above.  Up to accuracy logarithms
one may safely race

```text
T_portfolio = min {
  M/mu_*,
  M^(1+o(1))/sqrt(mu_*),
  R_chol+(F_chol+M)/sqrt(mu_*),
  (M+k^omega_mat)/sqrt(mu_*),
  s^3+sM
}.
```

The descending gap-guess plus quiet-KKT certificate makes the first and
third terms executable without knowing `mu_*`; the exact cycle-rank branch
does not need the gap to run.  Thus the requested
`O_tilde(M/sqrt(alpha))` bound is already deterministic with no small
`o(1)` under any one of

```text
(a) mu_*>=sqrt(alpha),
(b) R_chol=O_tilde(M/sqrt(alpha)) and
    F_chol=O_tilde(M sqrt(mu_*/alpha)),
(c) k^omega_mat=O_tilde(M sqrt(mu_*/alpha)),
(d) the stated bounded-width or small-support promise.
```

The cycle-rank term refers only to the capped certified approximate output,
not exact full-support termination.  The graph-uniform unresolved quadrant
is therefore

```text
mu_*<sqrt(alpha), high chronological response fill,
and no bounded structural support parameter.
```

In that quadrant, both current papers and the counterexamples say the same
thing: a new persistent response representation is required.  Sharper
formed-face eigenvalue estimation, fresh CG/Chebyshev, log-determinant
checkpointing, or a deterministic fixed-system SDD solver alone cannot do
it.

## 10. Remaining research targets

- Prove or refute `MaskedDuhamelOccupancy` for the *actual* canonical
  maximal-batch chronology; fixed-face square functions and local event
  charges alone are now known to be insufficient.
- Implement `QuarterScaleResponseEpoch(tau)` with output-sensitive shifted
  Green balls, or prove a canonical first-crossing family that defeats it.
- Turn the exact cycle-rank static theorem into a practical backend and test
  the crossover between batch rebuilds and the `Mk^2+k^3` persistent core.
- Seek a laminar response frame whose construction, not merely its supplied
  use, has the charged `A/tau+B tau/alpha` work.
