# Independent end-to-end audit of the deterministic OP2 proof

Audited artifact: `deterministic_conjecture2_proof.md`, as read in full on
2026-09-05. This audit rechecked the assembled argument rather than relying
on earlier component approvals. The canonical input and work assumptions
were checked against the authorized `problem_definitions/main.tex`.
No other existing manuscript notes or task histories were read.

**Result:** no mathematical gap was found in the assembled candidate proof.
The ordinary averaging update, box constant four, between-stage repair,
and exact-real word model are essential parts of the statement audited.
An explicit affine-key formula, given below, was recommended for Section 9
to make the arbitrary-momentum implementation easier to verify. This is an
exposition completion, not a change to the algorithm or bound.

## 1. Compatibility with the requested problem

The canonical graph is finite, connected, simple, undirected, with unit
edge weights and at least two vertices. Therefore every `d_i>=1`; this
fact is legitimately used in the Euclidean-to-degree-density error bounds
in the repair. The objective and matrix normalization match OP2 exactly.
The target is additive RPPR objective error, and no PPR-bias substitution
is used in its place. The listed work includes arithmetic, comparisons,
state access, degree replies, adjacency entries, and output.

The zero regime and `alpha=1` cases are correct. For the latter, the seed
coordinate is `(1-rho*d_v)_+/sqrt(d_v)` and all other coordinates are zero.
Representing this as a density plus its original degree is consistent with
the stated sparse radical output convention and costs constantly many words
per nonzero coordinate. Internal computation can remain in degree densities.

## 2. Baseline and source invariants

The stage assumptions `0<=bar<=x*_r` and
`0<=s=b-Qbar<=4*alpha*r*w` imply

* `m_s=alpha*(1-mass(bar))` lies in `[0,alpha]`;
* `t=Q^{-1}s` lies in the mass-one box `0<=t<=4*r*w`;
* the true correction `e*=x*_r-bar` is nonnegative and is dominated by `t`.

The last point follows from `x*_r<=x*_0`, equivalently from the
least-supersolution comparison with the unregularized optimizer. The proof
uses neither `t` nor either true support as an algorithmic oracle.

## 3. Arbitrary-metric comparator estimate

The sector inequality relative to `t` was checked separately for lower,
upper, and mass normals. In particular, at an upper-bound coordinate
`p_i=4*r*w_i`, Stieltjes signs and the coordinate bounds on every other
entry give `Qp_i>=4*alpha*r*w_i>=s_i`. For the mass normal,
`eta*w^T(Qp-s)=eta*(alpha-m_s)>=0` when it binds. Thus
`<p-t,Q(raw-p)>=0` holds even when several constraints are active.

For completeness, the general comparison estimate can be checked without
assuming the comparator is optimal. In a fixed Hilbert metric let `f` be
one-smooth and `mu` strongly convex, `theta^2=mu`, `a=1-theta`,
`g=grad f(y)`, `raw=a*z+theta*y-g/theta`, and `p` satisfy the sector
relative to `t`. The identity

    xplus=y-g+theta*(p-raw)

and smoothness give

    f(xplus)<=f(y)-||g||^2/2+mu*||p-raw||^2/2.

The sector gives

    ||p-t||^2<=||raw-t||^2-||p-raw||^2.

Add these inequalities with coefficient `mu/2`, expand `raw-t`, and use
strong convexity at `x` and `t` with weights `a` and `theta`. The remainder
is exactly bounded by

    -mu*theta*(1-mu)*||z-y||^2/2.

Hence `Eplus<=aE` for `E=f(x)-f(t)+mu*||z-t||^2/2`, regardless of the sign
of `E` or optimality of `t`. This validates the key use in the assembled
proof and does not assume general Q-metric nonexpansiveness of projection.

For the auxiliary objective
`A(x)=||Qx-s||^2/2+alpha*lambda*mass(x)`, its Q-gradient is
`Qx-s+lambda*w` and its metric Hessian is Q. The actual `alpha` in the
linear penalty must remain there when the momentum uses `mu<alpha`.
The source bounds give `A(t)=lambda*m_s`, `B0<=3*lambda*m_s`, and therefore
`A(x_k)<=4*lambda*m_s`, including the possibility that `B0<0`.
The residual `q=b-Qx*_r` satisfies `0<=q<=lambda*w` and mass at most `m_s`.
Consequently the constant `18` in

    ||Q(x_k-e*)||^2<=18*lambda*m_s<=18*alpha^2*r

is correct.

## 4. Dyadic momentum and selected flow

The halving choice has `alpha/4<mu<=alpha` and
`sqrt(alpha)/2<theta<=sqrt(alpha)` for `0<alpha<1`.
In mass coordinates, the coefficient on the previous kinetic vector is

    aI-(Q-mu I)/(1+theta)=(I-Q)/(1+theta)
                          =((1-alpha)/(1+theta))*K0.

It is nonnegative and column sums equal `beta0<=a`. At the fixed pair
`u*,V*=theta*u*`, the raw value equals `V*-R*`, since
`a*theta+mu=theta`. This checks the full raw error identity in Section 6.

On the selected positive-error coordinates, lower normals vanish while
upper and cap normals subtract nonnegative mass. The initial positive
kinetic error is zero. Telescoping therefore leaves the signed selected
forcing and a nonnegative loss, exactly as stated.

Outside the analytical half-r support, the margin is `lambda*d_i/2` in
mass coordinates, and the selected set there is exactly the emitted kinetic
support. Weighted Cauchy gives

    (lambda^2/4)*Dout^2<=(Dout+2K/r)*H2.

Since `Q-mu I` is PSD, commutes with Q, and is at most Q,
`H2<=18*alpha^2*r*K`. The scalar bound
`Dout<=8H2/lambda^2+2K/r` plus the inside volume `2K/r` gives
`148K/r`. Every occurrence of a kinetic vertex is counted, not only its
first appearance. No total unselected flux estimate is invoked.

## 5. Repair and final accuracy

For `tau=alpha^3*delta^2/2`, strong convexity gives
`||xtilde-x*_r||_2<=alpha*delta=eta`. Because `delta>=eta` and `w_i>=1`,
`barnew=[xtilde-delta*w]_+` is a lower bound on the true old optimum.
The correct error estimate is

    0<=x*_r-barnew<=(delta+eta)w<=2delta*w.

At a positive repaired coordinate, raising the other clipped coordinates
above `xtilde-delta*w` can only lower that coordinate's Q-product. Therefore
`Qbarnew_i<=Qxtilde_i-alpha*delta*w_i<=Qx*_r,i<=b_i`.
At a zero repaired coordinate, `Qbarnew_i<=0<=b_i`. This proves exact source
nonnegativity, with no numerical sign certificate or support margin assumed.

The absolute row sums of `D^(-1/2)QD^(1/2)` are one. Thus the repaired source
is at most `lambda*w+2delta*w<=2alpha*r*w`, restoring the next stage's
constant-four bound whenever its regularization is between `r/2` and `r`.

Both the repaired vector and the true optimum vanish outside the true
support. The first-order KKT term in their objective difference is therefore
zero. With `Q<=I` and support volume at most `1/r`, the final gap is bounded
by `2delta^2/r`. The final halving requirement
`delta^2<=epsilon*rho/2` proves the requested output accuracy, while retaining
coordinatewise containment and output volume at most `1/rho`.

## 6. Schedule and its logarithms

The initial exact zero optimizer at `r0=1/d_v` is available after one degree
query. The first positive stage obeys `r1>=r0/2`, so its seed source is at
most `2alpha*r1*w`; no prior solve is assumed. Subsequent stages follow by
the repaired invariant. The final partial halving preserves every ratio
condition used in the proof.

The reciprocal regularizations form a geometric sum before the last stage,
and the last stage contributes at most one further `1/rho`. In particular
`sum_j 1/r_j=O(1/rho)` and the number of stages is
`O(1+log(1/rho))`. At intermediate stages,
`tau_j=alpha^5*r_j^2/8`. At the last stage, repeated halving of delta makes
it at least a constant times the smaller of its initial value and the
accuracy threshold. Hence `log(1/tau_j)` is bounded by a fixed sum of the
allowed logarithms in `1/alpha`, `1/rho`, and `1/epsilon`, with harmless
positive-part conventions for large epsilon.

The initial actual-objective energy is at most one: correction mass at
most one and `w_i>=1` imply Euclidean norm at most one, while `Q<=I` and
`mu<=1` bound both halves of the initial energy. Maintaining `a^k` and
comparing it with tau is therefore a valid optimum-free stopping certificate.

## 7. Local implementation accounting

The fixed source has at most the baseline support, its neighbors, and the
seed as candidate nonzero records. Because the repaired baseline support
lies in the true previous support, its incident-edge count is at most
`1/r_previous`. Refreshing every fixed source key each iteration is thus
paid by `O(K/r)` scalar key operations. No inactive source neighbor's
adjacency list must be scanned merely to refresh that key.

An explicit key formula for arbitrary mu is as follows. Write
`R=(Q-mu I)xi/sigma`, `sigma=a^k`, and

    e_i=a*z_i/w_i-((Q-mu I)z)_i/((1+theta)*w_i)+s_i/(theta*w_i),
    K_i=-R_i/(theta*(1+theta)*w_i)+e_i/sigma.

Then

    zraw_i/w_i=sigma*K_i-lambda/theta.

Only the current kinetic support, its exposed neighbors, and the fixed
source can have nonzero `e_i`. Removing old exceptions, changing sigma,
applying sparse R updates, and installing new exceptions preserve the
ordering of unchanged base keys. Each response update scans exactly the
emitted kinetic support and does not recursively scan its boundary.

For the clipped waterfill, define
`tau=(lambda/theta+mu_cap)/sigma` and `U=4r`. Its mass equals

    sigma*(T(tau)-T(tau+U/sigma)),
    T(q)=sum_i d_i*(K_i-q)_+.

An augmented balanced tree answers each weighted tail in logarithmic time.
The two breakpoint lists are translated copies of the stored key ordering.
Selection in their implicit merge using rank-select queries, followed by
binary search over breakpoint ranks, costs `O(log^3 N)` conservatively.
Once the containing interval is known, one affine equation gives an exact
multiplier; no real-number bisection or smallest nonzero support margin is
needed. Enumeration visits only `K_i>tau`, which is exactly the positive
projected support, including saturated coordinates.

The historical primal support is the union of emitted kinetic supports;
it is not rescanned during iteration. Its final materialization, addition
to the previous baseline, and truncation are covered by the accumulated
work. The next source is built by scanning only the repaired support.
Thus the stage accounting and geometric sum include every operation listed
in the canonical work model.

## 8. Scope and audit conclusion

The proof deliberately uses ordinary accelerated averaging within each
stage. An arbitrary line search or cleanup that only decreases the original
objective has not been shown to preserve the auxiliary Q-metric energy and
is not part of the audited theorem. The end-stage repair restarts the next
stage and is covered by a separate invariant.

The argument establishes a deterministic exact-real word-model result.
Floating-point robustness, coefficient-bit growth, and practical constants
are separate implementation questions, as the theorem itself states.
Within the requested model, the assembled mathematical argument and local
work accounting pass this independent audit.
