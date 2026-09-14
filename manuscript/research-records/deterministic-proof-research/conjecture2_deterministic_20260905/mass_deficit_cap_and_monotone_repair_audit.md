# Audit: correction mass caps, monotone repair, and mass-deficit work

Status: independently checked mathematical refinement of the completed
deterministic exact-word algorithm. This note changes no implementation.
It uses only the authorized problem definition and the fresh proof
`deterministic_conjecture2_proof.md`. All statements below are deterministic.

## 1. Setup and the exact mass deficit

Use the notation of the main proof: `Qw=alpha*w`,
`alpha I <= Q <= I`, `Q` is Stieltjes, `w_i=sqrt(d_i)`, and
`w^T b=alpha`. At a stage with parameter `r`, write `lambda=alpha*r`.
The safe baseline satisfies

    0 <= xbar <= x*_r,
    s=b-Q*xbar >= 0,
    s <= 4*lambda*w.

Define

    m_s=w^T s,
    eta=m_s/alpha=1-w^T xbar.

This value is known exactly from the sparse baseline. Computing it does
not require summing an unknown boundary or inspecting the full graph.
In the nonzero regime `0<r<1/d_seed`, one has `eta>0`.

The analytical unregularized comparator `t=Q^(-1)s` satisfies

    0 <= t <= 4*r*w,
    w^T t=eta.

The true correction `e*=x*_r-xbar` satisfies `0<=e*<=t`. Therefore the
unit correction mass cap can be replaced by the smaller, known cap

    K_(r,eta)={z: 0<=z<=4*r*w, w^T z<=eta}.          (1)

All iterates remain in this convex set, so the full physical iterate
`xbar+xi` has mass at most one. Nothing is asserted about the unknown
comparator being computable.

## 2. The Q-normal sector survives, with equality at the mass face

Let `p` be the Euclidean projection of a raw vector onto (1), and let
`n=raw-p` be its normal. As in the main proof, lower-box normal terms in
`<Qp-s,n>` are nonnegative because `p_i=0` implies `(Qp)_i<=0<=s_i`.
Upper-box terms are nonnegative because `p_i=4*r*w_i` implies
`(Qp)_i>=4*lambda*w_i>=s_i`.

The remaining normal is `gamma*w`, with `gamma>=0`; if it is nonzero,
`w^T p=eta`. Its contribution is exactly

    gamma*(alpha*w^T p-m_s)
      = gamma*(alpha*eta-m_s)=0.

Consequently

    <p-t,Qn>=<Qp-s,n>>=0.                           (2)

Both accelerated energy arguments in the main proof thus apply unchanged.
In particular the auxiliary energy gives, for every iteration,

    ||Q(xi_k-e*)||_2^2 <= 18*lambda*m_s.             (3)

This is a statement about the actual nonlinear projected trajectory.
No metric nonexpansiveness between arbitrary projection inputs is used.

## 3. A sharper analytical core, without a support oracle

For any regularization `q>=0`, set

    qvec_q=b-Q*x*_q,
    eta_opt(q)=1-w^T x*_q.

The obstacle KKT conditions give

    0<=qvec_q<=alpha*q*w,
    qvec_(q,i)=alpha*q*w_i  when x*_(q,i)>0,
    w^T qvec_q=alpha*eta_opt(q).

It follows that

    vol(supp x*_q) <= eta_opt(q)/q                 (q>0).       (4)

At the current stage let `C=supp x*_(r/2)`. Since
`xbar<=x*_r<=x*_(r/2)`, its mass deficit is at most `eta`. Equation (4)
therefore gives

    vol(C) <= 2*eta/r.                              (5)

The usual outside-core gradient margin is unchanged:

    (Q*x*_r-b+lambda*w)_i >= lambda*w_i/2, i notin C. (6)

There is no need to replace the core by the correction support to obtain
(5). In fact the proposed correction core is the same set:

    supp(x*_(r/2)-xbar)=supp(x*_(r/2)).              (7)

Here is a direct check of the possible subtlety in (7). If an index in
the right-hand support had zero correction, then
`xbar_i=x*_(r/2,i)=x*_(r,i)>0`. At an equal coordinate of the ordered
vectors `x*_r<=x*_(r/2)`, nonpositive off-diagonals imply
`(Q*x*_r)_i >= (Q*x*_(r/2))_i`. Stationarity instead gives the first
quantity equal to `b_i-lambda*w_i` and the second to
`b_i-lambda*w_i/2`, a contradiction. The reverse inclusion is immediate.

More generally, for any `0<=q<=r`, the nonnegative vector
`e*_q=x*_q-xbar` solves the correction obstacle problem with fixed source
`s` and linear penalty `alpha*q*w`. Indeed its residual is exactly the
full optimizer's KKT residual, which is nonnegative and vanishes whenever
`e*_(q,i)>0`. Thus translating to a nonnegative correction introduces no
missing KKT condition, even if a correction coordinate vanishes over a
positive baseline coordinate.

## 4. The exact kinetic constant improves to 76

Retain the selected signed-flow argument from the main proof. For `K`
iterations, write

    D=sum_k vol(supp z_(k+1) outside C),
    B=K*vol(C),
    H2=sum_k ||D_degree^(-1/2) H_k||_2^2.

The symbol `D_degree` above is the degree matrix, not the scalar work `D`.
By (3), the flow formula, and `0<=Q-mu I<=Q`,

    H2 <= 18*lambda*m_s*K.

The selected support degree is at most `D+B`, and (6) yields

    lambda*D/2 <= sqrt((D+B)*H2).                   (8)

Set `Y=D+B`; the full kinetic volume is at most `Y`. Then

    Y <= B+2*sqrt(Y*H2)/lambda
      <= B+Y/2+2*H2/lambda^2,

where the second line is Young's inequality. Therefore

    sum_k vol(supp z_(k+1))
      <= Y <= 2*B+4*H2/lambda^2
      <= 4*eta*K/r+72*eta*K/r
      = 76*eta*K/r.                                (9)

This counts every appearance of every emitted kinetic vertex. It does
not merely bound the union of supports. The constant 76 applies to the
exact trajectory with the smaller cap; finite-precision trajectories
need their separate perturbation accounting.

## 5. The other local operations inherit the eta factor

Equation (4) at `q=r` and `xbar<=x*_r` give

    vol(supp xbar) <= vol(supp x*_r) <= eta/r.       (10)

The fixed source is supported on the baseline, its exposed neighbors,
and the seed. It consequently has `O(eta/r+1)` records. Its formation
scans only baseline adjacency lists. Refreshing its reporter exceptions
costs `O(K*(eta/r+1))`, with no inactive-neighbor adjacency scan.

When `r<1/d_seed`, the optimizer is nonzero, so (4) implies `eta/r>=1`.
The additive seed and iteration terms are therefore absorbed. The full
stage charge, including source construction, all scalar refreshes,
kinetic adjacency scans, and final materialization/repair, is

    O_tilde(eta*K/r).                               (11)

The waterfilling reporter changes only its mass target from `1` to
`eta`. The analytical core, true correction, and comparator are still
never supplied to the algorithm. Already exposed inactive boundaries
do not contribute their full degrees to (11).

## 6. Coordinatewise maximum is a valid monotone repair

Suppose the original repair produces a vector `z` such that

    0<=z<=x*_r,
    Qz<=b,
    0<=x*_r-z<=2*delta*w,
    2*delta<=alpha*r.

Replace it by

    xbar_new=max(xbar_old,z)                        (coordinatewise). (12)

Nonnegative Stieltjes subsolutions are closed under coordinatewise
maximum. To prove this, if the maximum selects `x_i` at row `i`, the
diagonal coordinate stays `x_i` and every other coordinate increases;
therefore that row of `Q*max(x,y)` is at most `(Qx)_i`. The same argument
applies when the row selects `y_i`, including ties.

Both arguments of (12) are safe subsolutions for the same right-hand
side `b` and lie below the current optimum. Hence

    xbar_old<=xbar_new<=x*_r,
    Q*xbar_new<=b,
    0<=x*_r-xbar_new<=2*delta*w.                    (13)

The source cap follows from the same degree-density norm bound as in
the main proof:

    0<=b-Q*xbar_new <= lambda*w+2*delta*w
                    <=2*lambda*w.

The error has support in `supp x*_r`, so the existing purely quadratic
objective-gap certificate also remains valid. A smaller coordinatewise
error is not being assumed to decrease a Q-norm; instead one reapplies
`Q<=I` and the same coordinatewise error bound. Materialization of (12)
uses the already charged union of the old baseline and the repaired
candidate. Baselines are now monotone; their exact mass deficits are
nonincreasing.

## 7. Repaired mass deficit approximates the optimum's deficit

The stronger sparsity identity (4), together with (13), implies

    eta_opt(r) <= eta_new
      = eta_opt(r)+w^T(x*_r-xbar_new)
      <= eta_opt(r)+2*delta*vol(supp x*_r)
      <= (1+alpha)*eta_opt(r).                     (14)

This only uses `2*delta<=alpha*r`; it remains valid for the final stage
when `delta` is further reduced for the requested objective tolerance.
The maximum repair is useful for monotonicity, but the approximation
(14) also holds for the original safe repaired vector.

## 8. Concavity gives a final-parameter bound for every stage

For a Stieltjes obstacle problem, `x*_r` is the least nonnegative
supersolution of `Qx>=b-alpha*r*w`. If `r=(1-t)*r1+t*r2`, the vector
`(1-t)*x*_(r1)+t*x*_(r2)` is a nonnegative supersolution at `r`.
Thus

    x*_((1-t)*r1+t*r2) <= (1-t)*x*_(r1)+t*x*_(r2).

Each optimizer coordinate is convex as a function of regularization.
Consequently `eta_opt(r)=1-w^T x*_r` is concave. It is nondecreasing
by optimizer monotonicity, and `eta_opt(0)=0`, because the unregularized
solution is `Q^(-1)b` and has mass one. Concavity therefore implies

    eta_opt(R)/R <= eta_opt(r)/r,  0<r<=R.          (15)

For a continuation stage at `r_j`, its baseline was repaired at
`r_(j-1)`, where `r_j<=r_(j-1)<=2*r_j`. Equations (14)--(15) give

    eta_baseline,j/r_j
      <= 2*(1+alpha)*eta_opt(r_(j-1))/r_(j-1)
      <= 4*eta_opt(rho)/rho.                       (16)

The first stage needs no exception oracle: at `r0=1/d_seed`, the optimum
and initial baseline are zero, so `eta_opt(r0)=1`; the same factor-two
argument applies to `r1>=r0/2`.

Let `J` be the number of continuation stages. The bound (16) gives

    sum_j eta_baseline,j/r_j
       <= 4*J*eta_opt(rho)/rho.

Combining this with `K_j=O(alpha^(-1/2)*polylog)` and the fully charged
stage bound (11) proves the stronger exact-word estimate

    O_tilde(eta_opt(rho)/(rho*sqrt(alpha)))          (17)

in the nonzero regime. The continuation stage count is absorbed in the
allowed logarithms; this argument does not claim a constant geometric
sum for the mass-weighted quantities. Since `eta_opt(rho)<=1`, (17)
implies the original theorem. The zero regime remains a separate `O(1)`
degree query and comparison.

The final repaired mass deficit, which is observable from the returned
sparse vector, lies between `eta_opt(rho)` and
`(1+alpha)*eta_opt(rho)` by (14). Thus the improved parameter has a
certified observable estimate. Also `eta_opt(rho)/rho>=vol(supp x*_rho)
>=1` in the nonzero regime, so inverse-deficit logarithms introduce no
new polynomial dependence or hidden full-graph factor.

## 9. Scope of the audit

The cap change, sharper exact work constant, maximum repair, and final
mass-deficit-dependent work bound are all valid under the baseline and
repair hypotheses explicitly stated above. The result is assembled from
the fresh main theorem's two energy inequalities and its paid local
reporter; no new solver or support oracle is introduced.

This note does not change stopping tolerances or certify a floating-point
implementation. In particular, replacing the exact cap by an inaccurately
estimated mass deficit would require a new normal-sector and feasibility
error account. The known exact scalar cap is the one used here.
