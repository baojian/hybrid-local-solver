# Independent audit of the rounded mass-deficit refinement

Inspected `rounded_mass_deficit_refinement.md` against the already proved
rounded two-energy, selected-flow, exact source-cap, repair, and local
implementation statements. No algorithm, code, or TeX was changed.

**Finding: the strengthening is valid for the stated default complete
rounded wrappers.** Their existing grid suffices. The conservative L^4
word and L^2 adjacency bounds correctly pay an additional stage-count
logarithm. The statement should retain its explicit qualification that
arbitrary standalone corrector tolerances/grids are not covered.

## 1. Positive mass deficit and the analytical core

At a nontrivial stage `r*d_seed<1`, the seed must be positive in x*_r.
Otherwise its Stieltjes row would give `(Qx*)_seed<=0`, whereas the KKT
supersolution requires it to be at least
`alpha*(1-r*d_seed)/sqrt(d_seed)>0`. The nonnegative optimal source has
weighted mass `alpha*eta_*(r)` and equals `alpha*r*w_i` on positive
support. Therefore

    eta >= eta_*(r) >= r*vol(supp x*_r) >= r*d_seed >= r.

This proof includes the important lower bound `eta/r>=1`; it is not an
assumed lower bound on a potentially tiny mass quantity. Baseline order
gives `vol(supp bar)<=eta/r`. Since `bar<=x*_(r/2)`, the half-parameter core
has `vol(C)<=2eta/r`. The same outside KKT margin remains valid.

## 2. Retained source mass and the existing error budget

Let `m_s=alpha*eta`, `lambda=alpha*r`. The perturbed auxiliary energy gives
`B_k<=a^k B_0+Gamma`, while `B_0<=3lambda*m_s` and `A(t)=lambda*m_s`.
Dropping the nonnegative mirror and mass terms yields

    ||Qxi_k-s||^2 <=8lambda*m_s+2Gamma.

This does not require B_0 or B_k to be nonnegative: the upper bound
`a^k B_0<=3lambda*m_s` is valid in either case. For the optimal residual
`q=s-Qxi*`, positivity, `q<=lambda*w`, and `w^Tq<=m_s` give
`||q||^2<=lambda*m_s`. The two-square inequality therefore proves

    ||Q(xi_k-xi*)||^2 <=18alpha^2*r*eta+4Gamma.

The earlier conservative perturbation lemma remains applicable because all
actual and analytical states have mass at most eta<=1. A new eta-scaled
perturbation lemma is unnecessary.

For the unchanged complete-wrapper budgets,

    Gamma <=29h/theta <=29tau/256
          <=29alpha^3*r^2/8192
          <=(29alpha/8192)*alpha^2*r*eta
          <alpha^2*r*eta.

The last inequality uses eta>=r. Final accuracy-driven refinement only
decreases delta, tau, h, and hence this upper bound. The existing raw-error
condition `nu<=lambda/4` is unaffected.

## 3. The exact constant in the stored support bound

Retain `Bcore<=2eta*K/r` and set `Y=Dout+Bcore`. With
`H2<=22alpha^2*r*eta*K`, the perturbed selected inequality is

    (lambda/2)Dout <=sqrt(Y*H2)+nu*Y.

For nu<=lambda/4, this implies

    Y <=(4/lambda)sqrt(Y*H2)+2Bcore
      <=Y/2+8H2/lambda^2+2Bcore,
    Y <=16H2/lambda^2+4Bcore <=360eta*K/r.

The constants are exactly 16*22+4*2=360. This applies to stored positive
kinetic outputs, including rounding-induced faces. It does not rely on
coordinatewise comparison with an exact trajectory or a positive support
margin. For K=0 the sum is zero; initialization is accounted for separately
below.

## 4. Every implementation charge inherits the factor

Put `M=eta/r>=1`. At a stage prefix K, a convenient explicit bound is

    W_K <=360M*K,
    N <=1+2vol(supp bar)+W_K <=363M*(K+1).

The retained cache volume and the full candidate volume are at most
`M+W_K`. Fixed source records number O(1+vol(supp bar))=O(M). Thus baseline
input, source construction, degree/neighbor exposure, old/new exception
refreshes, support scatters, candidate materialization, and terminal PG
and repair all receive the same factor. A newly exposed degree remains
only a word reply; its adjacency is never charged as free, nor scanned
implicitly by this refinement.

Scalar rebases still number O(1+theta*K) and scan O(N) old/current
records, with the usual tree logarithm. Direct exception replacement has
the same old/new support-record charges as before. The terminal candidate
scan and any source scan in the next stage are each paid in their own
stage. Reclamation of old state is paid by its historical size.

At geometric checkpoint times, candidate volume is at most M*(1+360k).
The sum of times is less than twice the actual stopping iteration; all
checker maps, cached rows, exact scalar accumulation, and discarded
candidates therefore add O(M*(K+1)*log(N+2)) work and O(M*(K+1)) temporary
records. An accepted candidate does not remove the separately charged
terminal PG scan.

A full conservative stage ledger is consequently

    O(L + K*log^2(N+2)
        + M*(K+1)*(1+theta*K)*log(N+2)).

The fixed terms and root queries are absorbed because M>=1. At K=0 this
still pays source setup, metadata, materialization, terminal repair, and
reclamation. It does not charge those tasks to a nonexistent kinetic sum.
With K<=T*L and log(N+2)=O(L), the ledger is O(M*T*L^3); adjacency
inspections are O(M*T*L). These are the precise stage bounds used below.

## 5. Rounded repair, initial stage, and continuation sum

The existing rounded terminal repair and safe maximum give support
containment, density error at most 2delta, and delta<=alpha*r/2. Hence

    eta_*(r)<=eta_new
       <=eta_*(r)+2delta*vol(supp x*_r)
       <=(1+alpha)*eta_*(r).

This statement is valid for an accepted checkpoint, a fallback endpoint,
and a zero-step stage: all provide the same actual objective-gap premise
for that repair. No new source or stopping oracle is needed.

Least-supersolution comparison proves coordinatewise convexity of x*_q.
Therefore eta_* is concave, nondecreasing, and eta_*(0)=0. For R>=rho,
`eta_*(R)/R<=eta_*(rho)/rho`. If a stage at r follows repair at
`R in [r,2r]`, its fixed input cap satisfies

    eta/r <=2(1+alpha)*eta_*(R)/R <=4eta_*(rho)/rho.

The first stage starts from zero at the analytical preceding parameter
`R=1/d_seed`, where x*_R=0 and eta_*(R)=1. Thus it satisfies the same bound
without assuming a computed prior optimum.

There are O(L) stages. Summing the per-stage bounds above gives

    O(eta_*(rho)*T*L^4/rho) arithmetic/word operations,
    O(eta_*(rho)*T*L^2/rho) adjacency inspections,
    T=O(1/sqrt(alpha)).

These conclusions use the stage-count factor explicitly, not an unproved
geometric bound on the mass-weighted stage sum. The former, stronger
explicit logarithmic bounds without eta_* also remain true for the same
algorithm; one may report both.

## 6. Encoding and branch scope

The algorithm and all grids are unchanged, so the prior
`B=O(b_par+b_graph+L)` bit envelope remains valid. It can also be recovered
from the refined record bound by using eta<=1. Exact parameter operations,
binomial powers, H-squared candidate certificates, root degree sums, and
rounded terminal calculations do not acquire a new denominator involving
the unknown optimum or eta_*. The conservative B^3 multiplier per
arithmetic operation therefore applies unchanged. All comparisons and
arithmetic remain deterministic.

The displayed asymptotic refinement concerns the nontrivial stage regime.
The zero-output and alpha=1 direct branches retain their stated O(1) word
and conservative O(B^3) bit costs. The returned mass deficit is an exact
quantity for the actual output and brackets eta_*(rho) within factor
1+alpha, but eta_* is never used to choose the schedule, grid, or step.

No further numerical test is needed to justify this algebraic strengthening:
it is a retained-constant analysis of the same already tested trajectory.
The existing worked three-vertex example also supplies concrete nonunit
caps and final mass deficits, without being used as a premise here.
