# A deterministic local algorithm for Conjecture 2

**Status, 2026-09-05:** complete candidate argument, assembled from fresh
lemmas with independent audits. The end-to-end statement and implementation
are undergoing further verification. This document is not a claim that the
requested ten-hour research period has been completed. No randomized
algorithm, randomized primitive, or randomized experiment is used.

The only manuscript source consulted is the user-authorized
`manuscript/notes/problem_definitions/main.tex`. All other references in this
note are newly produced artifacts of this task or primary external literature.
No existing manuscript directions or other tasks were inspected.

## 1. The theorem and computational model

Let the input be the finite connected simple unweighted undirected graph,
point seed v, original degrees d_i>=1, alpha in (0,1], and rho>0 of OP2.
Set w_i=sqrt(d_i), c=(1-alpha)/2, and

    Q=alpha I+c(I-D^(-1/2) A D^(-1/2)),
    b=alpha D^(-1/2)e_v,
    F_rho(x)=x^T Qx/2-b^T x+alpha*rho*||D^(1/2)x||_1.

For any epsilon>0, the algorithm below returns a nonnegative sparse list
xhat with

    F_rho(xhat)-F_rho(x*_rho)<=epsilon,
    0<=xhat<=x*_rho,
    vol(supp xhat)<=1/rho,

in deterministic work, in OP2's nontrivial regime rho<1/d_v,

    O_tilde(1/(rho*sqrt(alpha))).                    (T)

For unrestricted rho>0 the global statement is
O_tilde(1+1/(rho*sqrt(alpha))); the zero regime costs O(1).

The hidden factors are polylogarithmic in 1/alpha, 1/rho, 1/epsilon,
and the number of exposed or emitted words. They contain no polynomial in
the total graph size and no free preprocessing, support, boundary, solver,
or certificate oracle. Every adjacency entry inspection, arithmetic
operation, comparison, stored-state access, degree reply, and output word
is charged. The result uses the specified exact-real algebraic word model;
no bit-complexity or floating-point stability theorem is asserted here.

All computation can use degree densities f_i=x_i/w_i. Its operations are
rational when alpha and rho are rational: the displayed square roots are
analysis notation, and each output can retain the sparse radical form
xhat_i=f_i*sqrt(d_i). The acceleration parameter is chosen by rational
halving, so no square-root or logarithm primitive is needed by the algorithm.

If rho*d_v>=1, the optimum is zero and the algorithm returns zero after
querying d_v. If alpha=1, the only possible nonzero coordinate is
x_v=(1-rho*d_v)_+/sqrt(d_v), which is returned directly. Below assume
0<alpha<1 and 0<rho<1/d_v.

## 2. Standard obstacle facts used in the proof

On x>=0 write lambda=alpha*rho and

    J_rho(x)=x^T Qx/2-(b-lambda*w)^T x.

Its minimizer is x*_rho, the original RPPR minimizer. Q is Stieltjes,
alpha I<=Q<=I, and Qw=alpha*w. The standard KKT and mass properties are

    x*_rho>=0,
    r_rho=Qx*_rho-b+lambda*w>=0,
    r_rho,i*x*_rho,i=0,
    0<=b-Qx*_rho<=lambda*w,
    w^T x*_rho<=1, vol(supp x*_rho)<=1/rho.           (1)

The optimum decreases coordinatewise as rho increases. One proof uses the
least-supersolution characterization of a Stieltjes obstacle problem:
x*_rho is the least nonnegative y satisfying Qy>=b-lambda*w. Inverse
positivity on the set where two candidates are ordered incorrectly proves
this characterization and then the monotonicity.

Let C_rho=supp(x*_(rho/2)). This set is analytical, not algorithmic input.
Its volume is at most 2/rho. Outside C_rho, x*_rho=0 and

    r_rho,i>=lambda*w_i/2.                          (2)

Indeed Qx*_(rho/2)-b+lambda*w/2>=0, and both optima vanish at i. Their
coordinatewise order and the nonpositive off-diagonals give
(Qx*_rho)_i>=(Qx*_(rho/2))_i, proving (2).

The matrix in degree coordinates is

    D^(-1/2) Q D^(1/2)=q0 I-c D^(-1)A,
    q0=(1+alpha)/2.

Its absolute row sums are q0+c=1. Consequently

    |u|<=a0*w  implies  |Qu|<=a0*w.                 (3)

## 3. The certified baseline invariant

At the beginning of a stage with regularization r, let lambda=alpha*r.
The algorithm has a sparse baseline xbar satisfying

    0<=xbar<=x*_r,
    s=b-Qxbar>=0,
    s<=4*lambda*w.                                 (4)

The first inequality implies w^T xbar<=1. With m_s=w^T s, Qw=alpha*w gives

    0<=m_s=alpha*(1-w^T xbar)<=alpha.               (5)

The fixed source s is computed by scanning only the baseline support.
It is supported on that support, its exposed neighbors, and the seed.
After the repair proved below the baseline support has volume at most
1/r_previous; thus the number of source entries is O(1/r+1). An inactive
source neighbor requires a degree query and a scalar source entry, not a
scan of its adjacency list.

The unknown unregularized correction

    t=Q^(-1)s=x*_0-xbar

is used only in analysis. From inverse positivity and (4)--(5),

    0<=t<=4*r*w,  w^T t=m_s/alpha<=1.               (6)

The desired correction e*=x*_r-xbar is nonnegative, and (1), (4) imply

    0<=e*<=t, w^T e*<=1.                           (7)

## 4. One stage: ordinary acceleration with a box and mass cap

Choose theta by starting at 1/2 and halving until theta^2<=alpha.
Let mu=theta^2 and a=1-theta. Then

    alpha/4<mu<=alpha,  sqrt(alpha)/2<theta<=sqrt(alpha).

This choice is shared across all stages. Define the convex correction set

    K_r={z: 0<=z_i<=4*r*w_i, w^T z<=1}.             (8)

Both e* and t belong to K_r. Initialize xi_0=z_0=0. Repeatedly compute

    y_k=(xi_k+theta*z_k)/(1+theta),
    zraw_k=a*z_k+theta*y_k-(Qy_k-s+lambda*w)/theta,
    z_(k+1)=EuclideanProjection_(K_r)(zraw_k),
    xi_(k+1)=a*xi_k+theta*z_(k+1).                  (9)

The projection is deterministic clipped waterfilling; its charged local
implementation is described in Section 9. No monotone line search or
intermediate primal cleanup is used. Such changes need not preserve the
second energy that is crucial below.

The actual stage objective is

    J(xi)=xi^T Qxi/2-(s-lambda*w)^T xi.

It equals F_r(xbar+xi)-F_r(xbar) on nonnegative corrections. Since e* is
feasible, its constrained and unconstrained-orthant optima agree.

The standard one-projection accelerated estimate, with strong convexity
lower bound mu, is

    E_(k+1)<=a*E_k,
    E_k=J(xi_k)-J(e*)+mu*||z_k-e*||_2^2/2.         (10)

For completeness, this estimate follows by applying the quadratic
smoothness upper bound to xi_+=a*xi+theta*z_+, the strong-convexity lower
bounds at xi and e*, and the projection inequality
<z_+-e*,zraw-z_+>>=0. The same algebra is stated for a general metric and
comparator in the next section. Since e* is supported where x*_r is
positive, r_r^T e*=0. Therefore

    J(0)-J(e*)=||e*||_Q^2/2,
    E_0<=||e*||_2^2<=1.                            (11)

The algorithm maintains the scalar bound a^k. It stops a stage as soon
as a^k<=tau, for the tolerance prescribed in Section 8. This gives a
fully known objective-gap certificate, without evaluating the unknown
optimum. The number of steps is at most

    K<=1+theta^(-1)*log(1/tau).                     (12)

## 5. The second energy: the key deterministic stability argument

The Euclidean projection in (9) is not asserted to be a Q-metric
projection. It does, however, have a Q-metric sector inequality relative
to the one particular comparator t in (6).

Let p be a projection output and n=zraw-p its Euclidean normal. Decompose
n into lower-box normals, upper-box normals, and eta*w for the mass cap,
where eta>=0 and eta>0 only when w^T p=1. Then

    <p-t,Qn>=<Qp-s,n>>=0.                          (13)

Each term has the required sign separately. At p_i=0, Qp_i<=0<=s_i and
its lower normal is nonpositive. At p_i=4*r*w_i, all other coordinates
are at most their upper bounds, hence Qp_i>=4*alpha*r*w_i>=s_i and its
upper normal is nonnegative. The mass-normal term is
eta*alpha*(w^T p-w^T t)>=0 by (6). This proves (13), including simultaneous
active constraints and degenerate ties.

Consider the auxiliary quadratic

    A(xi)=||Qxi-s||_2^2/2+alpha*lambda*w^T xi.       (14)

In the Hilbert metric <u,v>_Q=u^T Qv, its gradient is

    grad_Q A(xi)=Qxi-s+lambda*w,

because Q^(-1)w=w/alpha. Its metric Hessian is Q, with spectrum in
[alpha,1], so it is 1-smooth and mu-strongly convex in that metric. Thus
(9) uses exactly this metric gradient, although its projection is Euclidean.

The accelerated comparison estimate needs only the sector inequality
relative to its comparator, not metric projection against every feasible
point and not optimality of the comparator. Consequently (13) yields

    B_(k+1)<=a*B_k,
    B_k=A(xi_k)-A(t)+mu*||z_k-t||_Q^2/2.            (15)

Here t is not an optimizer of A; B_k can be negative. Neither fact
invalidates the inequality. To verify the comparison estimate directly,
for a quadratic f with metric Hessian H in [mu I,I], combine

    f(u)>=f(y)+<grad f(y),u-y>+mu*||u-y||^2/2

at u=x and u=t, and the smoothness upper bound at x_+=a*x+theta*p.
Use x+theta*z=(1+theta)y and theta^2=mu, then the sector term
mu*<p-t,raw-p>>=0. The resulting remainder is nonnegative (one may retain
mu*theta*(1-mu)*||z-y||^2/2), giving (15). This calculation is in the
chosen Hilbert metric and therefore applies to (14).

The initial constants are small. From 0<=s<=4*lambda*w,

    ||s||_2^2<=4*lambda*m_s,
    A(t)=lambda*m_s,
    ||t||_Q^2=t^T s<=4*r*m_s.

Since mu<=alpha, these imply B_0<=3*lambda*m_s. Equations (14)--(15),
nonnegativity of xi_k, and the nonnegative distance term give

    A(xi_k)<=4*lambda*m_s,
    ||Qxi_k-s||_2^2<=8*lambda*m_s.                 (16)

Finally q=s-Qe*=b-Qx*_r satisfies 0<=q<=lambda*w and
w^T q<=m_s. Hence ||q||_2^2<=lambda*m_s. Combining with (16),

    ||Q(xi_k-e*)||_2^2<=18*lambda*m_s
                            <=18*alpha^2*r.        (17)

This is a uniform nonlinear stability theorem for the actual projected
trajectory. It is not an extrapolation from an unrestricted linear
spectral argument or from numerical experiments.

## 6. Selected signed flow pays for every kinetic support

Write P=A_graph D^(-1), K0=(I+P)/2, and

    u=D^(1/2)xi, V=theta*D^(1/2)z,
    u*=D^(1/2)e*, V*=theta*u*,
    beta0=(1-alpha)/(1+theta)<=a.

Direct substitution in (9) gives

    Vraw-V*=beta0*K0*(V-V*)+H-R*,
    H=-D^(1/2)(Q-mu I)(xi-e*)/(1+theta),
    R*=D^(1/2)r_r.                                 (18)

K0 is nonnegative and column stochastic. Let

    e=(V-V*)_+, nminus=(V*-V)_+,
    Eselect={i:Vnew_i>V*_i}.

On Eselect the projection's lower normal is absent. Its mass and upper
normals subtract nonnegative mass. Summing the exact raw identity over
Eselect therefore gives

    ||e_new||_1+sum_(i in Eselect) R*_i
       <=beta0*||e||_1+sum_(i in Eselect) H_i.       (19)

The last term is selected and signed. No false bound on total unselected
Laplacian flux is used. Since the correction starts at zero, e_0=0.
Outside C_r, e*=0 and (2) gives R*_i>=lambda*d_i/2. Summing (19) yields

    (lambda/2)*Dout <=sum_k sum_(i in Eselect_k) H_(k,i),
    Dout=sum_k vol(supp z_(k+1) outside C_r).        (20)

The selected total degree-volume is at most Dout+2K/r. Cauchy's inequality
applied to (20) gives

    (lambda^2/4)*Dout^2 <=(Dout+2K/r)*H2,
    H2=sum_k ||D^(-1/2)H_k||_2^2.

Because Q-mu I and Q commute and 0<=Q-mu I<=Q, (17)--(18) imply

    H2<=18*alpha^2*r*K.

Solving the scalar quadratic inequality, using
Dout<=8H2/lambda^2+2K/r, and adding the kinetic volume inside C_r proves

    sum_(k=0)^(K-1) vol(supp z_(k+1))<=148*K/r.      (21)

This charges repeated appearances, not only distinct discovered vertices.
It also bounds the union of all kinetic support volumes. The comparison
set, t, e*, and all unknown optima in this argument are analytical only.

## 7. Approximate output repair creates the next valid baseline

Suppose a completed stage at r returns the nonnegative full vector
xtilde=xbar+xi with certified objective gap at most

    tau=alpha^3*delta^2/2,
    0<delta<=alpha*r/2.                            (22)

Strong convexity gives ||xtilde-x*_r||_2<=eta=alpha*delta. Set

    xbar_new=[xtilde-delta*w]_+.                    (23)

Since w_i>=1 and delta>=eta,

    0<=xbar_new<=x*_r,
    0<=x*_r-xbar_new<=(delta+eta)w<=2delta*w.        (24)

The source after repair is exactly nonnegative, not merely approximately
so. If xbar_new,i>0, off-diagonal nonpositivity and
xbar_new>=xtilde-delta*w give

    (Qxbar_new)_i <= (Qxtilde)_i-alpha*delta*w_i
                   <= (Qx*_r)_i <= b_i.

The middle inequality uses ||Q(xtilde-x*_r)||_2<=eta and w_i>=1.
At a zero coordinate, Qxbar_new<=0<=b. Hence s_new=b-Qxbar_new>=0.
By (1), (3), and (24),

    s_new<=lambda*w+2delta*w<=2*alpha*r*w.          (25)

Also the repaired support has volume at most 1/r. At a following stage
r_new with r/2<=r_new<=r, equations (24)--(25) and optimum monotonicity
establish exactly (4): xbar_new<=x*_(r_new) and
s_new<=4*alpha*r_new*w.

The repair requires no global scan. Materialize the full xtilde only on
the baseline support and the union of emitted kinetic supports. Its size
and volume are charged by (21) and the previous baseline. Compute (23)
coordinatewise and discard zeros. To build the next source, scan only the
newly repaired support; all its lists were already exposed, or their first
inspection is charged now. There is no full-graph verification.

Because the repaired vector is supported inside the true support, its
objective error is purely quadratic. Equation (24) gives

    F_r(xbar_new)-F_r(x*_r)
       =||xbar_new-x*_r||_Q^2/2
       <=2*delta^2/r.                              (26)

This supplies the final-output guarantee as well as the continuation
invariant.

## 8. Complete continuation schedule

Start at r0=1/d_v with xbar=0. Its exact optimum is zero. For stages
j=1,2,... set

    r_j=max(rho,r0/2^j),

stopping once r_j=rho. Consecutive ratios are at most two. At the first
stage s=b and b_i<=2*alpha*r_1*w_i, so (4) holds without any previous solve.
At every intermediate stage choose delta_j=alpha*r_j/2. At the final
stage, start with that value and halve it until additionally

    delta_j^2<=epsilon*rho/2.

Set tau_j=alpha^3*delta_j^2/2. Execute (9) until the maintained scalar
a^k is at most tau_j, then repair by (23). Use the repaired vector as the
next baseline, or return it after the final stage.

Induction by Section 7 proves all stage invariants. Equation (26) proves
the requested final objective error and support containment. The algorithm
never assumes an exact previous optimizer or a smallest nonzero margin.
All precision choices involve only the input parameters and elementary
arithmetic comparisons.

There are O(1+log(1/rho)) stages since d_v>=1. Their iterations satisfy
K_j=O(alpha^(-1/2)*L), where L is a fixed sum of the allowed parameter
logarithms. Moreover sum_j 1/r_j=O(1/rho); the final partial halving changes
only a constant. Thus (21) sums to the target (T), before the reporter's
polylogarithmic factors.

## 9. Local deterministic implementation and full charge

Here is a sufficient exact reporter; optimizing its logarithmic exponent
is unnecessary for (T). Maintain xi=sigma*X in degree densities, with
sigma=a^k, and maintain the normalized sparse response
(Q-mu I)xi/sigma. Ordinary averaging changes X only at the newly emitted
kinetic coordinates. Its response changes are accumulated by one charged
scan of those coordinates' adjacency lists. The preceding kinetic vector
and its response are treated as sparse temporary key exceptions.

The fixed source s also gives sparse key exceptions. Refreshing every
source key on each iteration costs O(|supp s|) deterministic dictionary
operations, already O(1/r) per iteration by Section 3. This does not scan
inactive source neighbors' adjacency lists. Degrees are queried and cached
on first exposure. There is no dependence on the sum of inactive boundary
degrees.

The raw kinetic density at each exposed vertex is an affine key. A
fully explicit formula, in symmetric coordinates, is

    R=(Q-mu I)xi/sigma, Tz=(Q-mu I)z,
    K_i=-R_i/[theta*(1+theta)*w_i]
          +[a*z_i/w_i-Tz_i/((1+theta)*w_i)+s_i/(theta*w_i)]/sigma,
    raw_i/w_i=sigma*K_i-lambda/theta.

The bracket is supported only on the kinetic support, its exposed
neighbors, and the fixed source. It justifies the exception refreshes for
arbitrary mu<=alpha without reading the old primal vector. A
balanced binary tree ordered by these keys stores subtree cardinality,
degree weight, and degree-weighted key sum. Coordinates not exposed have
zero state, zero source, and strictly negative raw value, so they cannot
be selected and need no record. The projection is

    z_i/w_i=min(U,(raw_i/w_i-mu_cap)_+), U=4*r,

where mu_cap>=0 is zero if the unclamped mass is at most one, and otherwise
makes the mass exactly one. If T(q)=sum_i d_i*(key_i-q)_+, a clipped mass
query is a difference of two weighted tail queries. It costs O(log N).
The breakpoints are two translated copies of the ordered key set, at raw
density and raw density minus U. Deterministic rank selection in their
implicit merge, followed by binary search among the 2N breakpoint ranks,
finds the containing affine interval in O(log^3 N) operations. Solve the
one affine equation there exactly. Ties and flat intervals can use any
valid multiplier; the unique projected vector is unchanged.

Finally enumerate only keys with positive projected value. The tree never
scans all positive raw candidates rejected by the mass cap. Saturated box
coordinates are included in this same output set. Each emitted vertex and
all its adjacency entries are charged. No inverse, linear-system solver,
spectral sparsifier, random sample, or retry is part of this primitive.

With N exposed records, the stage work is therefore bounded by

    O((K*(1+|supp s|)+sum_k vol(supp z_k)
          +vol(supp xbar)+1)*polylog(N+2)).          (27)

This includes tree updates, scalar arithmetic, every first and repeated
adjacency inspection, source and response updates, and stored-state reads
and writes. Final materialization and repair are paid by the same support
union. No repeated full scan of the old primal state occurs during the
iterations. Equations (21), (25), and the geometric schedule prove (T).

All vertex-state maps and sets may also use deterministic balanced
comparison trees; their worst-case logarithmic costs are included in (27).
The exact Fraction prototype instead uses Python point dictionaries to
check the numerical trajectory and structural counts. Its hash-table and
integer-bit costs are not the theorem's worst-case word-operation ledger.

The number of records and retained adjacency entries is itself bounded
by the charged stage history. They may be discarded between stages except
for the repaired support and its required local source records. Thus the
state logarithms in (27) involve only exposed words and the allowed input
parameters, rather than the unknown global graph size.

## 10. Verification and remaining engineering scope

The mathematical components have separate task-local proofs and audits:
`dyadic_q_metric_stability.md`, `dyadic_q_metric_independent_audit.md`,
`squared_response_work_reduction.md`, and
`warm_spectral_incremental_lemma.md`. Earlier exact lazy reporter,
waterfilling, and acceleration prototypes were independently checked against
full rational computations. The new box/source reporter passed 6,250
independent exact projection cases and 198 independent sparse-state checks.
The full continuation wrapper passed 24 exact cases, 38 stage comparisons
before and after repair, and 1,398 correction iterations. A separately
implemented PG-assisted repair also passed exact tests and reduced iteration
counts on the tested fixtures.

The complete proof passed two independent end-to-end mathematical audits
and a fresh adversarial audit of the computational model, allowed parameter
logarithms, and all local-access charges. These audit records are
deterministic_conjecture2_full_audit.md,
deterministic_conjecture2_independent_audit_localization.md, and
deterministic_conjecture2_model_adversarial_audit.md.

A completed mathematical proof in this word model does not by itself give
a production-quality floating-point implementation. Practical precision,
rounding-safe comparisons, rescaling, and empirical constants should be
reported separately. This note does not silently promote existing exact
Fraction experiments into a bit-complexity or wall-clock guarantee.
The fresh notes perturbed_q_metric_kinetic_work.md and
bounded_dyadic_realization.md establish a separate route to bounded dyadic
state and controlled rounding. Its implementation is currently being
verified; the exact-real theorem above does not depend on that extension.
