# Independent audit of the diffuse-source continuation argument

This records an independent check of the fresh current-task
`dyadic_q_metric_stability.md`, `squared_response_work_reduction.md`, and
root's approximate-baseline repair. All statements below are deterministic.
The previous manuscript-source restriction remains unchanged.

## 1. General diffuse-source constant

Let a baseline `bar` satisfy

    0<=bar<=x*_rho,
    0<=s=b-Qbar<=C*lambda*w,
    lambda=alpha*rho, C>=1.

Then `m=w^T s=alpha*(1-w^T bar)<=alpha`. The analytical vector
`t=Q^-1 s` satisfies

    0<=t<=C*rho*w,   w^T t=m/alpha<=1.

For the actual Euclidean projection onto

    B={0<=z<=C*rho*w, w^T z<=1},

the single-comparator inequality

    <p-t,Q(raw-p)> >= 0

holds exactly. Lower normals see `Qp-s<=0`; upper normals see
`Qp-s>=Q(C rho w)-s>=0`; an active mass normal sees
`w^T(Qp-s)=alpha-m>=0`. This does not assume that arbitrary Euclidean
projections are nonexpansive in the Q norm.

The auxiliary quadratic

    F(xi)=||Qxi-s||²/2+alpha*lambda*w^T xi

has Q-gradient `Qxi-s+lambda*w`, exactly the gradient used by the original
corrector. Its Q-metric Hessian is Q, with spectrum in [alpha,1]. The
standard two-sequence accelerated comparison calculation works with the
nonoptimal t: it needs strong convexity at t and the displayed sector
inequality, not stationarity of t. Hence

    E_(k+1)<=a E_k,
    E_k=F(xi_k)-F(t)+alpha/2 ||z_k-t||_Q²,
    a=1-sqrt(alpha).

The potentially negative sign of E causes no difficulty. Since

    ||s||²<=C lambda m,
    alpha*t^T s/2<=C lambda m/2,
    F(t)=lambda m,

we have `E_0<=(C-1)lambda m` and therefore `F(xi_k)<=C lambda m`.
For the true correction `xi*=x*_rho-bar`, define
`q=s-Qxi*=b-Qx*_rho`. Obstacle KKT and Stieltjes signs give
`0<=q<=lambda*w`, and `w^T q<=m`. Consequently

    ||Q(xi_k-xi*)||²
      <=2||Qxi_k-s||²+2||q||²
      <=(4C+2)lambda m
      <=(4C+2)alpha²rho.

The independently checked selected-response work reduction then gives

    sum_(k<K) vol(supp z_(k+1)) <= (32C+20)K/rho.

For C=4 these constants are 18 and 148.

For ordinary accelerated convergence, `xi*` is the actual correction
optimum: its slack is the RPPR slack, and a positive correction coordinate
has a positive final RPPR coordinate. Thus complementary slackness applies.
Also `xi*<=t<=C rho w` and `w^T xi*<=1`, so the usual Euclidean initial
energy is at most `C alpha rho`. A known iteration count based on this
bound avoids any objective-gap oracle.

## 2. The approximate-baseline repair

Suppose `tilde>=0` approximates the OLD regularization `r`, with

    J_r(tilde)-J_r(x*_r) <= tau,
    tau=alpha^5*r²/8.

Strong convexity gives the Euclidean error bound

    ||tilde-x*_r||_2<=eta=alpha²*r/2.

Let `delta=eta/alpha=alpha*r/2` and set

    bar_i=max(tilde_i-delta*w_i,0).

Because all graph degrees are at least one,

    |tilde_i-x*_(r,i)|<=eta*w_i,
    |[Q(tilde-x*_r)]_i|<=eta*w_i.

The second inequality uses `||Q||_2<=1`. Since `delta>=eta`,
`bar<=x*_r`. Furthermore

    0<=x*_r-bar<=(delta+eta)w<=alpha*r*w.

At a positive repaired coordinate, write
`bar=tilde-delta*w+v`, where `v>=0` and `v_i=0` there.
Stieltjes signs imply `(Qv)_i<=0`, so

    (Qbar)_i <= (Qtilde)_i-alpha*delta*w_i
              <= (Qx*_r)_i <= b_i.

At a zero repaired coordinate, `(Qbar)_i<=0<=b_i` directly.
Thus `s=b-Qbar>=0` everywhere. The absolute row sum of the
normalization `D^(-1/2) Q D^(1/2)` is exactly
`q0+c=1`; hence

    |Q(x*_r-bar)| <= alpha*r*w.

Old KKT gives `0<=b-Qx*_r<=alpha*r*w`, and therefore

    0<=s<=2alpha*r*w.

For a next threshold `rho` with `r/2<=rho<=r`, this becomes
`s<=4alpha*rho*w`, the C=4 source condition above. The repaired support
is contained in the old exact support, so its degree volume is at most
`1/r`. Producing the repair requires scanning the materialized approximate
output once, which is already bounded by cumulative emitted kinetic
support and the stored old baseline. No unknown exact support is queried.

## 3. Endpoint and implementation checks to retain in the full theorem

- Start from the exactly zero solution at `r0=1/d_seed`; its next-stage
  source b satisfies the diffuse bound directly. Thresholds between the
  final two dyadic levels are covered by the ratio `r/rho<=2`.
- Handle alpha=1 directly; this avoids formulas dividing by `1-alpha`.
- Intermediate stages use the repair tolerance above. The final stage
  can target the requested epsilon without another repair.
- The constrained set contains the true correction and the analytical t,
  although total baseline-plus-mirror mass need not be one. Only the
  correction's own mass cap is required.
- The upper box must be included in the actual projection reporter and its
  arithmetic accounting. A generic cap-only implementation is insufficient.
- Finite-precision bit cost is a separate issue from the algebraic operation
  model; if the main conjecture uses exact arithmetic operations, the proof
  should state that model explicitly instead of silently claiming a
  floating implementation certificate.

## 4. Completed small-graph diagnostic check

All 771 connected labeled simple graphs on 2--5 vertices were enumerated.
Seed-preserving relabelings reduce these to 73 representatives without
changing the quantities tested. For alpha=1/64 and 1/1024, six rational
threshold choices, and lazy or ordinary projected Nesterov, 1,488
nontrivial runs were checked. Both dyadic obstacle solutions were solved
exactly with Fractions in degree coordinates; trajectories used floating
arithmetic for 16/sqrt(alpha) steps.

No Q-error peak exceeded its initial value. The maximum normalized squared
Q sum was 1.2306; the maximum
`sqrt(alpha)*sum||L0 error||²/(alpha²rho)` was 0.22013. These observations
are supporting diagnostics only. The diffuse-source comparison proof above
is independent of them.
