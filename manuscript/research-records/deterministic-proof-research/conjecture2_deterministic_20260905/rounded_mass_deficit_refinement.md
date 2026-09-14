# Mass-deficit work bound for the actual default rounded algorithm

This strengthening of the already proved implementation bound has passed
two independent audits, recorded in `rounded_mass_deficit_complexity_audit.md`
and `rounded_mass_deficit_independent_audit.md`. It changes no algorithm,
schedule, grid, reporter, checkpoint, or repair. It is now included in the
theorem appendix.

The existing exact-trajectory argument retained the known correction mass
`eta=1-w^T bar` and obtained work proportional to `eta/r`. The rounded
analysis replaced `eta` by one for convenience. For the actual complete
wrappers, their already chosen grid is fine enough to retain this factor.

## Stage hypotheses and the lower bound on eta

Consider a nontrivial stage `0<alpha<1`, `0<r<1/d_seed`. The baseline
satisfies `0<=bar<=x*_r`, `s=b-Q bar>=0`, and `s<=4alpha r w`.
The projection uses its exact mass cap

    eta = 1-w^T bar = (w^T s)/alpha.

Write `eta_*(q)=1-w^T x*_q`. The canonical KKT slack and source identity
give

    vol(supp x*_q) <= eta_*(q)/q.

The seed coordinate of `x*_r` is positive: otherwise its Stieltjes row has
`(Qx*_r)_seed<=0`, contradicting the positive right side
`b_seed-alpha r w_seed>0` of the supersolution inequality. Thus

    eta >= eta_*(r) >= r*d_seed >= r.                 (1)

Also `supp bar` is a subset of `supp x*_r`, so its volume is at most
`eta/r`. The analytical core `C=supp x*_(r/2)` has volume at most
`2eta/r`, exactly as in the exact source-mass proof.

## Retaining source mass in the perturbed response

The perturbed comparison lemma gives `B_k<=a^k B_0+Gamma` and does not
require replacing the exact source mass `m_s=alpha eta` by `alpha`.
With the same analytical `t=Q^{-1}s`, the unchanged estimates are

    B_0 <=3lambda*m_s,
    A(t)=lambda*m_s,
    ||s-Qxi*||^2 <=lambda*m_s,
    lambda=alpha*r.

Since the nonnegative mass penalty and mirror term can be dropped,

    ||Qxi_k-s||^2 <=8lambda*m_s+2Gamma.

Adding the optimal source residual with the same two-square inequality
therefore yields

    ||Q(xi_k-xi*)||^2
       <=18alpha^2*r*eta+4Gamma.                      (2)

The conservative perturbation constants remain valid because every state
has mass at most eta<=1. No error bound needs to be rederived with a
smaller coefficient.

## The existing default grid already has the required precision

Every complete wrapper uses

    tau=alpha*delta^2/8,  delta<=alpha*r/2,
    h<=theta*tau/256,    Gamma<=29h/theta.

Consequently

    Gamma <=29tau/256
          <=29alpha^3*r^2/8192
          <=alpha^2*r*eta,                            (3)

where the last step uses (1) and `29alpha/8192<1`. This is an additional
property of the default grids, not an instruction to choose a finer grid.
It need not hold for arbitrary independently supplied corrector tolerances
or grids. The other existing condition `nu=theta*kappa_r<=lambda/4`
is unchanged.

## Selected-work inequality

For any executed prefix of K steps, the existing perturbed flow proof now
has

    B_core=K*vol(C)<=2eta*K/r,
    H2<=K*(18alpha^2*r*eta+4Gamma)<=22alpha^2*r*eta*K.

Writing Y=D_out+B_core, the identical absorption/Young calculation gives

    sum_k vol(supp z_(k+1))
      <=Y<=16H2/lambda^2+4B_core<=360eta*K/r.          (4)

This bounds the actual stored kinetic supports, including all grid-induced
support changes. It does not assume a support margin or compare the rounded
trajectory coordinatewise with an exact trajectory.

Baseline volume is at most eta/r; source records are O(eta/r), using
eta/r>=1. Exposed history, retained records, direct exception transitions,
terminal materialization and repair therefore inherit the same factor.
The existing rebase and balanced-tree logarithms remain paid. A candidate
at iteration k has volume at most `eta*(1+360k)/r`, so geometric cached
checkpoints add `O(eta*(K_actual+1)*log(N+2)/r)` operations.

## Summation over continuation

The already proved rounded maximum repair gives

    eta_*(r) <= eta_new <=(1+alpha)*eta_*(r).

The function eta_* is concave, nondecreasing, and zero at zero, so
`eta_*(R)/R<=eta_*(rho)/rho` when `R>=rho`. With consecutive regularizations
`r_prev in [r,2r]`,

    eta/r <=4eta_*(rho)/rho.                          (5)

The initial zero baseline obeys the same estimate by taking
`r_prev=1/d_seed`, where eta_*=1. There are only O(L) stages. Using the
same L and B as `integer_source_complexity_corollary.md`, a conservative
per-stage word bound is `O((eta/r)*T*L^3)`, with T=O(1/sqrt(alpha)).
Thus the complete rounded implementation satisfies both its old bound and

    O(eta_*(rho)*L^4/(rho*sqrt(alpha)))               (6)

arithmetic/word operations. Its adjacency inspections satisfy both the
old bound and

    O(eta_*(rho)*L^2/(rho*sqrt(alpha))).              (7)

Equivalently its work is

    O~(eta_*(rho)/(rho*sqrt(alpha))).                 (8)

The powers of L in (6)-(7) deliberately pay the extra stage-count logarithm;
no constant-factor sum for mass-weighted stages is assumed. The same B-bit
envelope and conservative B^3 arithmetic multiplier remain valid because
the algorithm and grids have not changed. All zero/direct branches retain
their separately stated costs.

The final reported mass deficit brackets eta_*(rho) within factor
1+alpha, so the refinement concerns a quantity that can also be estimated
from the actual returned vector. The algorithm never queries the optimum
or uses eta_* to select a step.
