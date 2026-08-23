# AESP-CD RPPR note

This standalone note proposes a composite AESP outer loop with local proximal
coordinate descent for the shared regularized PageRank model.  The weighted
KKT-mass decrease, diagnostic-to-solution-error conversion, and local
inner-oracle work bound are proved for arbitrary signed iterates.  The
contraction and error certificate are also stated for any separable
$\ell_1$-regularized Stieltjes quadratic with a positive supersolution.  The
note gives the resulting cumulative inner-work interface for a composite AESP
outer loop, with no sign restriction on its extrapolated centers.  The raw
absolute-gap interface is shown to be intrinsically too coarse at an
$\ell_1$ kink.  Using the relative Catalyst criterion, a proximal warm start,
and greedy coordinate selection gives $\widetilde O(V/\sqrt\alpha)$ total
work on any fixed certified envelope of degree volume $V$.  An optimal-support
oracle gives $V\leq1/\rho$ and the target
$\widetilde O(1/(\rho\sqrt\alpha))$ bound.  Without an oracle, the same local
heap implementation has a trajectory-dependent
$\widetilde O(V_{\max}^{\rm exp}/\sqrt\alpha)$ bound in terms of the maximum
actually explored stage volume.  This raw analysis initially leaves the task
of proving $V_{\max}^{\rm exp}=O(1/\rho)$ or enforcing that cap.
For a certified lower center, the cap is automatic: the shifted minimizer,
proximal warm start, and every greedy coordinate iterate stay between the
center and the RPPR optimum.  Thus each safe-centered proximal call is
oracle-free and costs $\widetilde O(1/\rho)$.  A local retraction converts any
signed finite-support trial point into such a lower certificate.  For the
resulting safeguarded recurrence, the
stage-start KKT masses telescope to at most $1-\alpha$, with no
$1/\alpha$ loss.  The note also derives the exact correction term in the
Nesterov potential and a Euclidean progress telescope for it.  A three-vertex
path refutes pointwise momentum nonexpansion, so the remaining proof obligation
is the sharper amortization that combines this defect formula with the
proximal-displacement collapse identity.  A multiplicative potential ledger
now reduces that obligation further to bounding cumulative log-inflation;
each correction inflates the classical potential by at most a factor two.  An
exact single-edge family with a singleton optimal support has a full
correction every other stage, and hence logarithmically many charged
correction/rekey calls for logarithmic terminal accuracy after only one
support discovery.  Every such correction has $\gamma_t<1$, however, so the
family has $\mathcal I_T=0$.  It refutes raw correction-count amortization,
not the still-open bound on harmful normalized inflation.  The note now
upper-bounds that positive part: every $\log\max\{1,\gamma_t\}$ is bounded by a
normalized collateral-clipping charge supported only on coordinates that the
common retraction clips while their extrapolates remain below the optimum.
The charge may be positive on a benign collateral round.  For $t\geq2$, its
clipping amplitude is written exactly through the proximal-displacement
collapse identity.  This is an a posteriori proof charge because it uses the
unknown optimum.  A second exact single-edge family, now with full optimal
support, has a harmful full collateral correction at stage two for which the
charge is asymptotic to $(44/9)q$ while the same-step Euclidean log-error
decrease is asymptotic to $(88/9)q^2$.  It rigorously refutes an
$\alpha$-independent packing of the collateral charge by monotone Euclidean
log-error, even over the first two stages; the same family rules out every
$o(1/q)$ coefficient, including polylogarithmic dependence on $1/\alpha$.
It does not refute packing by a different potential or the collapse history.
Round 022 sharpens the boundary: an exact self-similar scalar
sequence satisfies the current safe-chain, start-mass, correction-mass,
collapse, defect, and defective-contraction ledgers while accumulating
`Omega(1/q)` positive log-inflation over `Theta(1/q^2)` steps with only
constant potential progress.  This is a theorem about the insufficiency of
those abstract ledgers, not an RPPR instance or an exact-proximal trajectory;
it deliberately omits the fixed-operator active-row relation
`Q e_t = kappa_A s_t` and its coupled boundary complementarity.  Conversely,
an exact finite endpoint-seeded `P4` RPPR trace has iterate support equal to
the optimal support from stage 7 onward but continues to exhibit positive
inflation through stage 498.
An exact `P7` trace corroborates late inflation through stage 796.  These
finite traces refute one-for-one support-addition attribution and eventual
post-discovery disappearance only; by themselves they prove no infinite periodicity,
scaling obstruction, or finite-inner work theorem.

Round 023 supplies the missing infinite-tail theorem for the same fixed `P4`
objective.  An exact rational invariant cone proves that, from stage 44, the
fixed-support recurrence repeats the eleven-stage word
`F N N F N^6 P0`.  The second full correction is harmful once per word and
has a uniform positive log-inflation floor, so
`I_(44+11N) >= (315/33280) N` and `I_T=Theta(T)` on this one fixed RPPR
trajectory.  At the same time, the primal error contracts by at most `11/500`
per word and hence converges geometrically.  This refutes a horizon-uniform,
support-only, parameter-only, or transient-only inflation bound.  It does
not refute an allowance logarithmic in terminal accuracy, the frozen
polylogarithmic dependence on `epsilon^{-1}`, or a net bound of the form
`I_T <= (1-c)qT + polylog`; `q=1/8` is fixed, so there is no small-`q`
scaling obstruction.

The round also records the exact finite-inner residual interface.  A finite
lower-subsolution output adds an end residual to the active fixed-row
identity, the next start mass, and the following collapse.  The published C2
relative stop can leave this residual nonzero—even a scalar quadratic gives
residual size `Theta(sqrt(q))` relative to its displacement—so the exact-tail
cone cannot be imported into a finite-inner proof.  Requiring both C2 and an
absolute end-mass polish makes the finite shifted error at most `xi` with
only an additional logarithmic work factor.  Conditional on a net packing
theorem for the actual finite trajectory, the note gives computable outer
horizon and `xi`, proves the fresh terminal gate, and records the resulting
conditional cached-row resource vector.  The gate correctness, the
large-`alpha` zero-start fallback, and the cache mechanics are unconditional.
The overall input range remains `0<alpha<=1`: shifted acceleration is analyzed
for `alpha<1/2` (the frozen accelerated arm uses `alpha<1/4`), while the
unshifted fallback covers `1/4<=alpha<=1`; the accelerated rate-to-gate and
complete vector are not graph-uniformly unconditional.

Round 024 closes two narrower seams without closing that graph-uniform
target.  On `P2`, the support-indexed lower retraction is exactly
discontinuous when a zero trial coordinate enters the support; even inside
one fixed positive support its sharp local infinity-norm amplification is
`1+1/alpha`.  Thus an exact-to-finite proof that merely iterates an ambient
Lipschitz shadow bound would require exponentially small per-stage errors and
would lose the accelerated inner-work scale.  This is a STOP for that
black-box shadowing proof template, not a counterexample to direct finite
packing or to the solver.

The fixed operator also yields two positive results.  On a settled optimal
face, an exact full correction is always followed by a no-correction stage;
with a finite shifted solve, any adjacent correction is bounded solely by
the just-produced end residual and vanishes under absolute polish.  More
substantially, let
`theta_A=lambda_min(Q_A)/(kappa_A+lambda_min(Q_A))` on the unknown optimal
support.  If `theta_A>=c0*q` for an absolute `c0>0`, resolvent contraction
directly gives the terminal gate in `O_tilde(1/q)` stages and supplies the
cached eleven-resource vector with
`O_tilde(1/(rho*sqrt(alpha)))` work, without a log-inflation assumption.
This is an unconditional theorem on that a-posteriori promised structural
class, but the condition is not algorithmically certified and is not
graph-uniform.  The actual-finite net exponent remains open only for the
low-Dirichlet branch.

Round 025 removes support entry itself from that blocker.  On every newly
positive row, the exact first-retraction violation is zero; for a finite
shifted solve it is at most `beta_A` times the preceding end residual.  A
locally maintained absolute end-mass target therefore bounds all
entry-dominated positive log-inflation before the fresh gate by `4 delta q T`,
independently of how many coordinates enter, while retaining
`O_tilde(1/(rho q))` work.  More generally, relative to the residual-free
driver at the same realized states, a finite end residual can create only a
one-sided correction excess of size `O(xi/(alpha q))` in the momentum state;
this is a polynomial one-stage interface, not iterated ambient shadowing.

On a settled exact face after a full correction, the first following stage
has no correction, and the collapse driver two stages later is exactly
`Q_A (Q_A+kappa_A I)^(-2)
[beta_A(2+beta_A)Q_A-kappa_A I] e_t`.  Its scalar coefficient changes sign
only at
`lambda/kappa_A=(1+q)^2/((1-q)(3+q))`, so a single nonnegative low mode
cannot retrigger at that point.  Coordinatewise positive-part mixing of
several modes can still do so.  These results reduce the live low-Dirichlet
target to persistent-row partial corrections; they do not establish the
graph-uniform net exponent or the unconditional cached vector.

Round 026 gives the persistent controller an exact actual-finite energy
ledger.  On a row active at consecutive stages, the previous and current end
residuals combine into `u_t=Q e_t`, so the collapse is exactly
`[beta_A u_(t-1)-(1+beta_A)u_t]_+` and is bounded by
`beta_A[Q d_t]_+`.  Over every window, both the sum of squared persistent
controller magnitudes and `alpha^2` times the sum of squared common caps on
persistent-dominated stages telescope into the decrease of
`<e_t,Q e_t>`.  Separately, the common correction
`r_t=D^(1/2) min{beta_A D^(-1/2)d_t,Delta_t 1}` and the surviving momentum
`p_t=beta_A d_t-r_t` each have at most `beta_A^2` times the `Q`-energy of
`d_t`; their windowed sums telescope through the same error energy.  These
are statements about the realized finite recurrence and do not erase either
end residual or require exact-to-finite shadowing.

The round also turns the earlier mixed-mode `K8` direction into a reachable
event.  One exact dense-seed instance has the all-time word
`N N P0 F N^infinity`: both the persistent partial correction and the full
correction have positive inflation before the fresh gate, but their total
inflation is below `2 log 2`.  It is therefore a real collateral pulse, not
an additive-resistant counterexample.  A rational small-`q` dense-seed
family sharpens the proof boundary: at its harmful persistent full stage,
the raw Euclidean defect is `>28q` after common scaling, while the same-stage
`Q`-energy drop is `<197q^4`.  Paying the raw defect directly from the new
unsplit window bank therefore costs
`Omega(q^(-3))=Omega(alpha^(-3/2))`.  This is a STOP for that raw conversion.
Even after the actual potential weight `mu_E=kappa_A q^2`, direct payment by
the same unsplit local `Q`-energy drop needs `Omega(q^(-1))`.  The family
does not refute a `q^(-1)`-weighted, spectrally split, or differently
normalized bank, an additive polylogarithmic term, the target net exponent,
or the solver.

Round 027 tests that remaining weighted route at its simplest exact form.
Adding the lagged Euclidean reserve
`((1-q)^2 mu_E/(2q))*||x*-x_(t-1)||_2^2` to the actual finite potential
absorbs every realized correction defect while retaining the finite
shifted-solve error.  Its graph-uniform comparison, however, gives only a
`1-Theta(q^2)` drift and therefore only `O(q^(-2))` stages.  This is a valid
finite-sequence reserve, not the missing accelerated theorem.

A sharper two-family boundary applies to the lagged unsplit bank
`Psi_t=Phi_t+(A/q)<e_(t-1),Qe_(t-1)>`.  Paying the reachable Round-026 `K8`
pulse directly forces
`A>14(1-q)kappa_A/197>=6929307/98509850`.  For every such coefficient, an
exact reachable uniform-seed `K2` trajectory has only
`O(q^2)` relative bank decrease on its stage-two persistent transition, so no
uniform one-step `1-cq` comparison is possible for this template.  The same
trajectory still decays globally at the accelerated exponential rate after
only an `O(log(q^(-1)))` startup normalization, so it is not a net-exponent
or additive-term counterexample.

The `K8` pulse remains compatible with a high-band bank: its exact
`mu_E`-weighted payment divided by the `q^(-1)` high-band energy drop tends
to `14641/32256`.  This is only a stress-family check.  In the general
fixed-face filter, the coordinatewise positive part does not commute with
the low/high projectors, and the low projector is not positivity preserving.
Thus no general spectral window or nonlinear transfer theorem is proved.

The live mathematical target is therefore narrower: use a `q^(-1)`-weighted,
spectrally split, windowed, nonlinear, or differently normalized persistent
low-Dirichlet Lyapunov to prove a net accelerated exponent for the actual
finite safeguarded sequence.  No graph-uniform exact accelerated solver or
graph-uniform unconditional end-to-end `O_tilde(1/(rho*sqrt(alpha)))`
theorem is claimed.

Build with:

```bash
make -C manuscript/notes/aesp_cd_l1_rppr
python3 manuscript/notes/aesp_cd_l1_rppr/check_round022.py
# Optional longer corroborating trace:
python3 manuscript/notes/aesp_cd_l1_rppr/check_round022.py --with-p7
python3 manuscript/notes/aesp_cd_l1_rppr/check_round023.py
python3 manuscript/notes/aesp_cd_l1_rppr/check_round024.py
python3 manuscript/notes/aesp_cd_l1_rppr/check_round025.py
python3 manuscript/notes/aesp_cd_l1_rppr/check_round026.py
python3 manuscript/notes/aesp_cd_l1_rppr/check_round027.py
```
