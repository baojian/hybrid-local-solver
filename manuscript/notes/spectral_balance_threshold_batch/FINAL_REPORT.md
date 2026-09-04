# Deterministic spectral balance: final decision report

Date: 2026-08-31; updated 2026-09-01.  This report summarizes the audited working note; proofs,
counterexamples, and executable certificates are in `README.md`, `CLAIMS.md`,
`STATUS.md`, and `VERIFICATION.md`.

**Superseding update (2026-09-04).**  This report's later statements that
`StoppedMaskedInputResidual` is the sole unproved premise are historical.
The literal point-source zero-start statement is strictly refuted, with a
continuous exact beta-cell cover through
`0.4897917473484638...`.  A separate `ExactBoxLC` route proves the outer
accelerated oracle-call theorem, and positive-barrier cap-min rounding makes
an objective-accurate obstacle point exactly safe, but no audited theorem
supplies that point in deterministic support-linear work.  Thus the general
deterministic `O_tilde(M/sqrt(alpha))` result remains open for the narrower
oracle/persistent-response reason stated in `DETERMINISTIC_HALO_INTEGRATION.md`.

## Decision

The directed-random-walk paper can derandomize each *supplied-face* solve, but
it does not by itself remove the small `o(1)` factor or amortize the changing
faces.  Sharper current-face eigenvalues improve favorable instances, but a
fresh Chebyshev/CG solve on every face cannot meet the general target.  The
canonical ballasted broom keeps
`lambda_min(Q_UU)=Theta(alpha)` for `Theta(1/sqrt(alpha))` large faces, and an
endpoint path forces the same fresh-polynomial failure despite a one-edge
frontier.

A genuine optimizable theorem does exist after shifting the *obstacle prox*,
not merely retuning a fresh face solve.  With `sigma=tau^2`, a complete
shifted obstacle closure gives

```text
O_tilde(A/tau + B tau/mu_*),
```

where `mu_*=lambda_min(Q_(S*,S*))>=alpha`; in the graph-uniform case this is
`O_tilde(A/tau+B tau/alpha)`.  Here `A` charges fast filtering/response
production and `B` charges the persistent slow/reporting ledger; neither is a
free oracle parameter.  The clipped optimizer is
`tau=sqrt(A mu_*/B)` when it lies in `[sqrt(mu_*),1]`, with interior value
`2 sqrt(A B/mu_*)` up to logarithms.  For `A=B=M`, this is
`tau=sqrt(mu_*)` and work `O_tilde(M/sqrt(mu_*))`.

This yields unconditional deterministic no-small-`o(1)` algorithms on paths,
trees, supplied constant-treewidth graphs, and feedback-edge-rank `k`
instances with an explicit additive `k^omega_mat` core term (in particular,
the target bound when `k^omega_mat=O_tilde(M)`).  For general sparse graphs it
is a conditional theorem: the precise missing operation is a persistent,
support-local changing-principal response producer.  The weakest audited
capped form is
`AmortizedLowerShiftedApply(tau)`; `ShiftedProxClosure(tau)` and
`CenterLift(tau)` are stronger sufficient interfaces.

The 2026-09-01 continuation found a second, more concrete route that avoids
assuming a general dynamic inverse.  At the retained shift `sigma=alpha`, a
projected-NAG proximal phase with certified lower retraction, one active
diagonal residual push, and maximal safe positive append has an exact charged
ledger `W_charged<=2W_core+M`.  If its pushed lower envelope dominates the
same-time unpushed omniscient envelope, ordinary fixed-face acceleration
proves the missing quarter-bracket phase and hence the full target.  This
`PushedDomainDominance` statement survives all current tests, but is not yet
proved.  Two exact local flux identities now isolate its remaining
reachable-history obligations; generic monotonicity shortcuts are strictly
false even on two-coordinate retained systems.

## 1. Concrete map from the directed-random-walk paper

For every exposed face `U`, degree coordinates give

```text
H_UU = a D_U - b A_U,
a=(1+alpha)/2,  b=(1-alpha)/2.
```

This is SDDM and can be represented as a grounded undirected Laplacian: use
internal edge weight `b` and add a ground edge of weight `alpha d_i` at row
`i`.  Consequently the
deterministic almost-linear directed-Laplacian machinery applies to a
*materialized fixed face*.  The map is:

| Our operation | Fixed-system operation in the paper | What transfers |
| --- | --- | --- |
| Solve `Q_UU x=c_U` | Solve grounded `H_UU y=D_U^(1/2)c_U` | Deterministic supplied-face energy approximation |
| Certify a numerical candidate | Sparse residual product on `U` | Our residual/retraction adapter makes a safe lower subsolution |
| Find the next active batch | Exterior signs of `c-Qz` | Not supplied by the paper |
| Reuse state after `U` grows | Dynamic principal inverse/Schur response | Not supplied by the paper |
| Charge only `vol(S*)` | No ambient preprocessing or old-face replay | Not supplied by the paper |

On a symmetric input the directed skew component vanishes, so the paper's
partial-symmetrization parameter is not our desired spectral cutoff.  Literal
composition therefore gives approximately

```text
O_tilde(M^(1+o(1))/sqrt(alpha)),
```

not `O_tilde(M/sqrt(alpha))`.  It is a valid deterministic replacement for
the randomized face solver when the small `o(1)` is acceptable.

## 2. What a narrower formed-face spectrum really buys

The exact face gap is

```text
mu_U = alpha + (1-alpha) delta_U/2,
```

where `delta_U` is the killed/Dirichlet normalized-Laplacian gap.  Therefore
the user's intuition is correct on well-exposed faces: certified
`mu_U>>alpha` accelerates both Chebyshev/CG and the batch-depth estimate.

It is not graph-uniform.  Every face has diagonal
`a=(1+alpha)/2`, hence `lambda_max(Q_UU)>=a>=1/2`.  If `mu_U=Theta(alpha)`,
the full condition number is still `Theta(1/alpha)`; degree/Jacobi scaling
only rescales both endpoints.  The exact fresh-face ledger is

```text
sum_j vol(U_j) sqrt(lambda_max(Q_Uj)/mu_Uj).
```

The ballasted broom makes this `Omega(M/alpha)`.  Thus an adaptive eigenvalue
certificate is useful as a portfolio branch, but cannot be the missing
general proof.

There is nevertheless a closed high-gap branch: if the final certified gap
is at least `sqrt(alpha)`, the product of
`O_tilde(1/sqrt(mu_*))` faces and
`O_tilde(M/sqrt(mu_*))` fresh work per face is
`O_tilde(M/mu_*)=O_tilde(M/sqrt(alpha))`.  Descending safe guesses plus the
existing residual certificate find this branch without knowing the gap in
advance.

The later accelerated phase also improves, not only the face solve.  For any
certified `alpha<=mu<=lambda_min(Q_UU)`, the audited companion metric

```text
F_mu = (1+mu)Q - Q^2 - mu a I
```

is Stieltjes/lattice compatible, contracts a held tuned-NAG step by
`1-sqrt(mu)`, and retains the exact negative cut-square term when the face
grows.  Decreasing dyadic gap estimates can be transported nonexpansively
after rescaling the physical state.  This closes gap-adaptive state transport;
it does not by itself turn the additive event bank into a publication-time
bound.

## 3. The valid balance and deterministic algorithms

Define the global obstacle resolvent

```text
T_sigma(x) = argmin_(z>=0) { Phi(z) + (sigma/2)||z-x||_2^2 }.
```

For every monotone lower subsolution,

```text
x <= T_sigma(x) <= x*,
||T_sigma(x)-x*||_2 <= sigma/(mu_*+sigma) ||x-x*||_2.
```

Taking `sigma=tau^2` needs
`O_tilde(1+tau^2/mu_*)` outer calls.  If one entire no-miss shifted active-set
closure costs `O_tilde(A/tau)`, multiplication gives the promised balance.
The deterministic residual/retraction adapter makes finite signed
Chebyshev/CG outputs safe, so numerical certification is closed.

Closed end-to-end classes are:

- endpoint paths: retained tridiagonal transfer gives exact linear work;
- trees: scalar Schur messages implement every shifted closure and give
  `O_tilde(M/tau+M tau/alpha)`;
- supplied constant treewidth: bounded-width elimination gives the same bound
  up to width factors;
- feedback-edge rank `k`: tree Green queries plus a `k x k` Woodbury core,
  solved by pivot-free recursive block inversion, give
  `O_tilde((M+k^omega_mat)/sqrt(alpha))` exact ordered-field operations for
  the certified capped output.  Here `omega_mat` is any admissible exact
  matrix-multiplication exponent.  Degree coordinates remove radicals.  This
  does not claim bit complexity, floating-point stability, that the last
  capped face equals the full exact support, or an improvement to the separate
  chronological `Mk^2+k^3` maintenance bound.

For arbitrary graphs the response update after adding a block `B` contains
the dense old-face lift

```text
-(Q_UU+tau^2 I)^(-1) Q_UB g_B.
```

Padded old CG directions remain mutually conjugate, but their orthogonality
against the new residual is broken by `P^T Q_UB g_B`.  A complete repair is
exactly the dense Schur lift.  Warm restart plus retraction therefore cannot
be charged only by the new coordinates; the endpoint-path regression and the
ballasted broom make this failure explicit.

No Green-leverage oracle is needed to terminate a capped prox.  If the
maintained lower correction `d>=0` has active residual
`e_U=r_U-(Q_UU+tau^2 I)d_U>=0` and a complete current boundary scan has
nonpositive exterior scores, then `(-e_U,0)` is a subgradient of the full
shifted obstacle objective.  If `d_prox*` is its exact minimizer, strong
convexity gives

```text
F(d)-F(d_prox*) <= ||e_U||_2^2/[2(alpha+tau^2)],
||d-d_prox*||_2 <= ||e_U||_2/(alpha+tau^2).
```

This pays every hidden cascade globally.  The scan is support-local in the
canonical point-source problem: the source is seeded, and a nonneighbor of
the current support has the known negative floor score.  Thus the remaining
producer is needed only when the boundary is currently quiet but the active
residual is too large for the requested objective cap.

For exact restricted-center or zero-margin support certification, a weaker
rowwise Green fact remains useful.  Put `C_v=-Q_vU>=0`; then

```text
0 <= C_v(Q_UU+tau^2 I)^(-1)e
   <= sqrt((a+tau^2)/(alpha+tau^2)) ||e||_2.
```

Every visibly positive current-score batch can be appended at correction
zero, preserving all old scores, and the appended sources over one nested
prox call have the global square bank
`sum_B||g_B||_2^2<=(1+tau^2)alpha`.  A norm-trigger buy count follows only in
reset-and-zero-append epochs; it is not a contraction theorem for arbitrary
intervening updates.

The remaining general theorem is now sharply isolated:

> Maintain a certified-lower accelerated shifted solve through all visible
> zero-appends.  Repeatedly rescan, append every positive current score, and
> reduce `||e||` until the global subgradient cap is met, with all response
> updates and rescans totaling `O_tilde(M/tau)` work and no old-volume replay.

The resulting deterministic skeleton is concrete:

```text
sigma <- tau^2;  x <- certified lower starting point
repeat outer prox calls until the manuscript objective cap:
    U <- supp(x) plus the seeded source;  d <- 0;  e <- r_U
    repeat:
        scan every edge leaving U
        append every row with current score > 0, setting its d-coordinate to 0
        if all current exterior scores <= 0 and
           ||e||^2 <= 2(alpha+sigma) epsilon_prox: commit x <- x+d; break
        perform a certified-lower accelerated shifted residual-reduction step
```

The scan, zero append, residual/retraction certificate, subgradient stop, and
outer contraction are proved.  On paths, trees, supplied bounded width, and
the stated low-cycle rebuild regime, the last line has an implemented
deterministic realization.  On a general sparse graph, amortizing that last
line and its rescans by `O_tilde(M/tau)` is exactly the remaining conjectural
interface—not an omitted call to a free SDD solver.

For the stronger `CenterLift` route, the positive inverse-square-root group
probe and canonical first-crossing/conservation ledger already pay the
reporting side by `O_tilde(M tau/alpha)`.  In the capped loop above, rescans
are charged directly in `AmortizedLowerShiftedApply`.  Either way, Gaussian
trace probes are no longer the core obstacle.

## 4. Retained-prox continuation: exact gains and exact stops

Set `sigma=alpha` in every obstacle proximal call.  The retained exact/inexact
bracket and two-certificate invariant imply that an inner shifted bracket of
one quarter reduces the outer width by a constant factor, with only
`O(log(alpha/eps_obj))` phases.  The missing producer is therefore the narrow
statement

```text
QuarterBracketMaskedNAG:
  continue one projected estimate-sequence recurrence through all safe
  growing-face events and reduce the shifted bracket by four in
  O_tilde(1/sqrt(alpha)) core products.
```

A fixed-final-face omniscient shadow initially appeared to prove this.  It
does not.  The stored 30-vertex simple connected unit graph `lag30`, at
`alpha=1/10000,rho=17/2000`, has an exact `Q(sqrt(20002))` phase-8/product-86
one-product-lag lower deficit

```text
0.0002892921587903060918853871424203...
```

in degree coordinates; lower, primal, and next-extrapolate lag comparisons
all fail in normalized arithmetic.  The same phase still ends in `1.6405`
root-time, so this refutes only pointwise `OneStepDomainDominance`, not the
aggregate quarter-bracket bound.

There is a certified linear repair.  For Stieltjes `B`, lower state `u`, and
residual `r=h-Bu`, adding `r_i/B_ii` simultaneously on any visible
positive-residual batch preserves the lower certificate.  The block solve
`B_WW^-1 r_W` has the same algebraic property but is not free.  The concrete
enhanced recurrence uses only the diagonal version: one active push after
every retraction plus maximal positive-append closure.  Its exact work ledger
is

```text
W_push<=W_core,       W_append<=M,
W_charged<=2W_core+M.
```

Thus no randomization, dense solve, or hidden subpolynomial factor remains in
the repair layer.  If

```text
PushedDomainDominance:
  lower_pushed_masked(t) >= lower_unpushed_omniscient(t)
```

holds along the prescribed source chronology, fixed-face NAG proves
`QuarterBracketMaskedNAG` and the target.  It has zero observed deficit on
the lag4/lag30 graphs, structured families, 1500 random graphs, all 26,704
connected labelled six-vertex graphs at one parameter pair, and a 17,472-run
grid over every connected labelled five-vertex graph, four `alpha` values,
and six source-threshold fractions.  Long paths retain many missing
omniscient coordinates after closure, so not all evidence is immediate
full-face discovery.  The largest observed phase remains below `1.68`
root-time.  These are floating-point finite tests, not a theorem.

There is also a roundoff-free audit.  In degree coordinates, rational root
`s` gives rational `alpha=s^2/(2-s^2)` and an entirely Fraction-exact
recurrence.  All 4,368 histories from the 728 connected labelled five-vertex
graphs, three thresholds, and `alpha in {1/7,1/199}` pass; the smaller-alpha
histories use as many as 152 products.  This exactly checks the pushed,
pre-push, momentum, boundary, and exterior-state inequalities on those finite
families.  Two additional four-vertex small-root grids bring the exact total
to 4,596 histories and reach 1,003 products.  A focused five-vertex rerun has
strict relevant one-step and masked raw-residual margins.  This still does
not establish arbitrary-graph preservation.

The lower comparison reduces exactly to a local inequality.  For pre-push
masked lower `u`, omniscient lower `w`, `delta=w-u`, and
`C=diag(B)-B>=0`,

```text
B_ii delta_i <= [h-Bu]_i^+
        iff (C delta)_i <= (h-Bw)_i       on delta_i>0.
```

The left side is sufficient for the diagonal push/append to dominate `w`.
This `ShadowResidualCover` says neighboring shadow-deficit flux must be paid
by the omniscient certificate's residual slack; an independent set of
positive-deficit vertices suffices.

All enhanced tests in fact satisfy the stronger pre-push inequality `u>=w`,
exactly on the rational exhaustive families and to roundoff elsewhere.  A
proof of this lead invariant would remove shadow residual cover entirely, but
generic retraction isotonicity is strictly false, so it still requires the
paired accelerated/push chronology.

After the synchronized first product, the tests satisfy the stronger temporal
statement that the preceding pushed masked lower dominates the *next*
omniscient envelope.  First-product repair plus this `PushedOneStepLead`
directly implies pushed-domain dominance and is now the most compact single
conjecture.  The exact Jacobi-cap counterexample shows that its proof must use
the accumulated accelerated masked state, not merely isotonicity of one push.
Exact four-vertex histories also show that the corresponding one-step
auxiliary and extrapolate orders are false even while lower/current lead is
strict.  Thus this compact route must address the retracted envelope directly,
not shift the full-state induction by one product.

The synchronized phase base is in fact proved.  If `r_A>=0` is the old active
residual, the first masked current `ell_A+r_A/L` has residual
`R_AA r_A>=0`, so it is not shaved; omniscient shaving can only lower common
rows.  A positive omniscient exterior lower is at most `r_i/L`, while masked
closure appends at least `r_i/B_ii>=r_i/L`.  Thus first-product pushed
dominance is unconditional.  The narrow temporal route now has exactly one
open premise: `PushedOneStepLead`.  Proving it would close the full target.

The first temporal instance is also proved on a common face:
`U_1-c_2^o=s(1-s)Rr/[B_ii(1+s)]>=0`.  But this identity cannot simply be
iterated.  A Fraction-exact 12-vertex point-source example at
`alpha=1/124999` reverses the third-product lead by `0.120502...` if the full
zero face is supplied for free; the violating product is the first
quarter-residual stopping product and masked shaving is still absent.
Starting from the minimal source face and executing the prescribed positive
append cascade reaches the same full face after one product but retains
strict lead `0.0039679`.  Thus admission values and first-entry chronology,
not point-source load, fixed-face algebra, or no-shave alone, are essential.

Canonical lower states exclude that stop: exact-positive closure maintains
`face=supp(lower)`, and shifted certification implies the original
certificate `Q lower<=load`.  Every positive non-source lower coordinate
therefore has a strictly larger neighbor, so every positive lower superlevel
is source-rooted and connected.  This is a proved structural invariant, but
a quantitative admission-edge charge is still missing.

The exact remaining inequality can now be stated as a residual shield.  For
preceding pushed lower `U`, next omniscient input `q`, post-push residual
`r_U`, and omniscient shave `theta`, the new-candidate gap is
`R(U-q)-r_U/L+theta`.  Hence the single conjecture is equivalent to
`L R(U-q)+Ltheta>=r_U` on candidate-growth rows.  The right side decomposes
into incoming active-push flux plus one-time admission flux, suggesting a
source-arborescence charge for the latter and the momentum cone for the
former.  That combined payment is the remaining proof, not an established
inequality.

The debt itself is now exactly time-directed.  If the active push is batch
zero and append batches are numbered by admission, then the final residual is
`r_i=sum_{t(j)>=t(i)}C_ij p_j`; row `i`'s own diagonal update cancels every
earlier contribution.  Append flux is therefore globally one-time, while
only active--active flux recurs.  This makes “source-arborescence credit plus
momentum credit” a precise prospective proof decomposition, although their
dominating inequality remains open.

Substitution removes even that residual variable.  If `V` is pre-push,
`U=V+p` is post-closure, and `gamma=L-B_ii`, then exactly
`LR(U-q)-r_U=gamma(U-q)+C(V-q)+early_admission_flux`; all same/later batch
terms cancel.  Adding `Ltheta` is equivalent to the desired lead on a growing
omniscient-envelope row.  Thus the final sign theorem has four explicit
credits—diagonal gap, neighbor pre-push gap, positive earlier-admission flux,
and shave—and no hidden debt.  Its canonical nonnegativity is still open.

One extra post-append cleanup push gives the strongest current algorithmic
candidate.  After a second closure its exact shield is
`gamma(U^(2)-q)+C(U^(1)-q)+early_credit+Ltheta`: only two successive lower
levels remain.  Cleanup scans charge forward to the next enlarged core face,
apart from at most `M` per logarithmically many outer phases, so the target
ledger is unchanged asymptotically.  It repairs the exact supplied-face stop
with margin `0.083327...`, improves lag30 lead by about 100x, and passes a
10,000 arbitrary fixed-face histories through their first quarter-residual
crossing (minimum `5.78e-9`).  A generic product-seven reversal appears only
after its phase should have stopped at product one, so the correct candidate
is `StoppedPostAppendTwoLevelLead`.  It is not yet a theorem: on the exact
four-vertex star at `alpha=1/199`, the omniscient envelope exceeds two static
Jacobi pushes by `0.0004853298...`, so the stopped paired sign still requires
a canonical two-level proof.
Together with the proved first-product repair and cleanup work ledger, proving
this stopped sign would close `QuarterBracketMaskedNAG` and the full target;
it is a second single-premise route, with a larger constant but a cleaner
two-level state.

All canonical tests also lie in a smaller `MaskedInputResidual` cone:
`h-Bq>=0` before the masked gradient.  Conditional on it, masked shaving is
identically zero, pre-push lower equals the raw current, and every push/clamp
resets `current=lower`; the state reduces to a residual and nonnegative
auxiliary gap.  This is exact on the focused small-graph audits and survives
adversarial searches to roundoff, but generic fixed-face histories violate it.
The supplied-face lead stop occurs without shaving, so preservation of this
cone would simplify rather than finish the two-level causal proof.

A final synthesis makes the input cone substantially more useful than that
temporal comparison suggests.  Before each gradient product, materialize
every exterior row with positive residual at `q`.  Conditional on
`h_A-B_AAq_A>=0`, inverse positivity gives
`q_A<=B_AA^-1h_A<=x_A^*`; therefore an exterior positive-residual row cannot
lie outside the exact prox support.  After this one-hop closure all ignored
exterior gradients are nonnegative.  Dropping them preserves the global
strong-convexity lower model, while the active smooth step supplies the usual
descent model.  Standard strongly-convex NAG consequently contracts

```text
E=f(x)-f(x^*)+alpha||z-x^*||_2^2
```

by `1-s`, `s=sqrt(2alpha/(1+alpha))`.  Certified positive pushes and joining
the physical primal/estimate states with the lower certificate cannot
increase this potential by the Stieltjes lattice and Euclidean projection
lemmas; zero-state safe admissions do not change it.  Thus

```text
StoppedMaskedInputResidual + input-residual frontier admission
  => QuarterBracketMaskedNAG
  => O_tilde(M/sqrt(alpha)).
```

This `InputConeFrontierNAG` route bypasses temporal dominance and the event
timing bank entirely.  The implication is correct, but the once-unproved
premise is now refuted at the literal quarter stop and throughout every fixed
`beta<0.4897917473484638...` by exact zero-start chronology cells.  The
input-frontier implementation has exact nonnegative residual on 842
four/five-vertex histories at `s=1/10`, reaches only `-1.36e-15` roundoff over 500
seeded random canonical runs, and has maximum stable measured potential ratio
`0.999197` over 200 further runs.  A 40-generation targeted input-cone
adversary and five-alpha crosscheck reach only `-9.1e-20` roundoff.  These
tests are not a proof, but this is now
the narrowest single-premise route to the full target.

The stopping guard on the alternative two-cleanup route is also exact.  A
rational 12-row fixed-face trace stops after product one with residual maximum
`0.163995...`, yet reverses product-three lead by `0.000122140052...` if
illegally continued.  By contrast, 1,710 exact binary-residual four-vertex
histories at three roots and 6,080 skew-profile histories at root `1/10` pass
through their prescribed stop.  Hence two pushes do not give an all-time
Jacobi cap; the viable conjecture is precisely the stop-guarded implication.

The acceleration history has a second exact local identity.  Put

```text
s=sqrt(2alpha/(1+alpha)),
R=I-B/(1+alpha)=((1-s^2)/2)I+K,       K>=0.
```

If `g,d,z` are masked-minus-omniscient gaps in extrapolate, current, and
auxiliary state on a common active row, then

```text
g_i^+=[s(1-s)z_i+2(Kg)_i]/(1+s).      (momentum-flux identity)
```

This explains why the auxiliary order can fail while extrapolate order
survives: neighboring extrapolate surplus pays the auxiliary lag.  Reachable
NAG clamping introduces no extra conjecture: its output extrapolate is the
maximum of three ordered quantities, so raw-current, raw-extrapolate, and
lower order survive the clamp.  The new-coordinate state gate also follows
exactly from the local boundary-flux premise `Cq^o<=Cu`; a positive
omniscient exterior current then forces a safe append large enough to dominate
both current and extrapolate.  A complete proof now needs the source
chronology to preserve only momentum flux, shadow residual cover, and this
boundary flux.

The distinction is important: an exact two-coordinate reachable-clamp state
keeps current/extrapolate order but changes a positive momentum-flux margin to
`-1/6`; even a legal diagonal push under a common retained-form Stieltjes load
leaves it at `-2/15`.  Thus clamping adds no separate *order* clause, yet the
canonical source history must re-establish `MomentumFlux` for the following
product.

Two exact stops show why reachability cannot be discarded:

- a scalar legal NAG state begins with masked domination of lower, current,
  and extrapolate but reverses next-extrapolate order by exactly `1/3` after
  a common gradient/retraction step;
- on the canonical unit-edge retained load at `alpha=1/10000,rho=1/1000`
  with a certified constant-shave old lower, ordered input currents make the
  pushed-retraction outputs reverse by about `0.0423` in both coordinates.

The currents in these two stops are not proved reachable from the prescribed
zero-start source run.  They do not refute `PushedDomainDominance`; they prove
that neither coordinate-order induction nor isotonicity of the repair map is
available as a generic theorem.  The strongest honest boundary is therefore:
the diagonal algorithm, certificate, outer recurrence, sparse-work ledger,
first-product repair, common-face second-product lead, and canonical source-
arborescence structure are closed.  The compact route has one remaining
statement, `PushedOneStepLead`, now explicitly scoped to the minimal-admission
source chronology.  The alternative local-cone route still has the three
reachable-history clauses above.  The post-append cleanup variant supplies a
second single-premise route, `StoppedPostAppendTwoLevelLead`, with a cleaner
two-level identity and stronger evidence but a larger constant.  None of the
three routes is yet a general-graph theorem.

A final exact stop rules out a simpler attempted proof.  The positive-residual
Jacobi map is isotone, but on the canonical two-vertex unit edge at
`alpha=1/7,rho=1/10` the fourth omniscient envelope exceeds one Jacobi push
from its predecessor by exactly `(1/3200,1/3200)`.  One push therefore cannot
be treated as prepaying a complete accelerated envelope round; the paired
accelerated/push history is essential.
Likewise, the exact four-vertex star at `alpha=1/199` has the next envelope
above two Jacobi pushes by `0.0004853298...`; the cleanup candidate must use
its paired lower levels and stopping rule, not a static two-push cap.

## 5. Follow-up literature verdict

No audited follow-up currently supplies the missing deterministic,
support-local, nested-principal response primitive.

- [Kyng--Meierhans--Probst Gutenberg](https://arxiv.org/abs/2208.10959)
  gives the deterministic fixed-system backend, with a subpolynomial
  overhead.
- [Wei--Yang](https://arxiv.org/abs/2608.16339) is the closest matching local
  active-set PageRank algorithm, but its advertised bound is high-probability
  and it explicitly re-solves the nested SDD systems and scans their
  boundaries.
- [Fountoulakis--Martinez-Rubio](https://arxiv.org/abs/2602.21138) gives a
  useful accelerated/local optimization comparison, not persistent Schur
  response maintenance.
- [Chuzhoy--Parter](https://arxiv.org/abs/2601.20718),
  [Li--Vaughn](https://arxiv.org/abs/2608.13910), and
  [Farfan--Ghadiri--Yang](https://arxiv.org/abs/2511.16570) improve
  deterministic routing/sparsification or fixed SDDM access, but retain
  ambient or subpolynomial costs and do not maintain solution responses on an
  unknown growing support.
- [Kadeethum--Ballarin--Choi--Lee](https://arxiv.org/abs/2606.17971) is a
  promising practical restricted-eigenspace recycling method.  Its active
  sets and global reference modes are supplied, and the needed rank/coherence
  bound is empirical rather than graph-uniform.

The three supplied convex-optimization papers are useful for the final
identification/refinement stage and for designing practical active-set
heuristics.  Their hypotheses begin after a useful global gradient/face is
already available; they do not charge unread-boundary discovery or the dense
Dirichlet-to-Neumann response.  They therefore do not close the Stage-I local
work theorem.

## 6. Exact delayed-clock correction

The strengthened exact verifier proves, over `Q(sqrt(10))`, that one canonical
34-vertex simple connected unit graph at `alpha=1/1000`, `rho=1/100000` has
projected-NAG publication times

```text
0, 1, 2, 3, 4, 38.
```

All exterior residuals at products 5 through 37 are nonpositive, with largest
exact value `-2e-8`; every lower-subsolution inequality holds; every quiet
early-stop test fails by squared ratio at least `4.09312681762e11`; and an
exact rational full solve is positive, hence `S*=V`.  This refutes only the
immediate-next-product lemma for that recurrence.  It is compatible with a
shared `O(1/sqrt(alpha))` clock and is not an algorithmic lower bound.

## Bottom line

The extended directions were worthwhile: they found the right optimizable
parameterization, proved unconditional no-small-`o(1)` algorithms on several
nontrivial graph classes, derandomized fixed-face candidate selection, and
reduced the general problem to one weaker capped residual producer contract.
It did not prove an unconditional general-graph deterministic
`O_tilde(M/sqrt(alpha))` algorithm.  Further material is most valuable if it
addresses dynamic Schur responses, incremental principal inverse application,
or output-sensitive
obstacle multigrid, or prove/refute the three retained momentum/shadow/boundary-flux
history clauses.  The most focused alternative is now to prove or refute
`StoppedMaskedInputResidual` for the input-frontier one-push recurrence: all
other support-safety, estimate-potential, stopping, and sparse-work steps of
that conditional route are closed.  More generic active-set identification
papers are unlikely to resolve the remaining bottleneck.
