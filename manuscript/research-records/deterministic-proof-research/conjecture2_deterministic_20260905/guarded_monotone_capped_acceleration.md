# Fixed-face degree guard for monotone capped acceleration

The new `GuardedMonotoneCappedSolver` restricts the existing algorithm to a
fixed coordinate face containing the exact RPPR optimum. The same accelerated
energy contraction and lazy-work reduction hold. The initial-phase cumulative
support-work bound is still open, so this is not a general Conjecture 2 proof.
The original lazy and monotone implementations are unchanged by this extension.

Let Q=((1+alpha)/2)I-((1-alpha)/2)D^(-1/2)AD^(-1/2), w=sqrt(d),
b=alpha*D^(-1/2)e_s, lambda=alpha*rho, and
J(x)=x^TQx/2-b^Tx+lambda*w^Tx on x>=0. Assume positive degrees and
0<alpha<1. The diagonal alpha=1 case is separate; this iterative prototype
accepts rational theta in (0,1), with alpha=theta^2.

## 1. The strict coordinate guard contains the optimum

Let S be the nonempty support of x*. For an induced connected component T of
S, all positive coordinates adjacent to T also lie in T. Complementarity gives

    w_T^T Q_TT x*_T = alpha*(1{s in T}-rho*vol(T)).

Because Qw=alpha*w and off-diagonal entries are nonpositive,

    w_T^T Q_TT x*_T >= alpha*w_T^T x*_T > 0.

Thus every component T must contain the seed. Consequently S is connected,
the seed belongs to S, and

    mass(x*) + rho*vol(S) <= 1,
    rho*vol(S) < 1.                                      (1)

This argument also covers disconnected input graphs. In particular, define

    Allowed = {s : rho*d_s < 1}
              union {i != s : rho*(d_s+d_i) < 1}.        (2)

Every coordinate of S belongs to Allowed. Equality is safely rejected because
the positive mass in (1) makes the support-volume inequality strict. If
rho*d_s>=1, x*=0: the gradient at zero is nonnegative at the seed and every
other coordinate. The same condition makes (2) empty.

Let C_A={x>=0 : w^Tx<=1, x_i=0 for i not in Allowed}. This is a closed convex
set containing the original optimum. It therefore does not change the optimum.
It is not necessary to find the entire allowed set in advance; membership
requires only the seed degree and a queried degree of the particular vertex.

## 2. The same accelerated recurrence applies on this face

For theta=sqrt(alpha) and a=1-theta, use

    y=(x+theta*z)/(1+theta),
    z_raw=a*z+theta*y-grad J(y)/theta,
    zplus=Proj_C_A(z_raw),
    xhat=a*x+theta*zplus,
    xplus=argmin {J((1-s)*x+s*xhat): 0<=s<=1}.

The proof of capped acceleration uses the Euclidean projection inequality for
a closed convex set containing x*, together with alpha-strong convexity and
1-smoothness of J. These hold unchanged for C_A. Since both segment endpoints
belong to C_A, the line minimizer is feasible. Its objective is no larger than
that of xhat and no larger than that of x. Therefore, with

    E(x,z)=J(x)-J(x*)+alpha/2*||z-x*||_2^2,

one has exactly the same estimate

    E(xplus,zplus) <= a*E(x,z)
       - alpha*theta*(1-alpha)/2*||z-y||_2^2.             (3)

See `monotone_capped_acceleration_audit.md` for the audited algebra. From zero,
J remains nonpositive, and E contracts by a on every iteration. The lazy scale
sigma instead contracts by 1-s*theta; it is not the energy multiplier.

The true-gradient margin outside supp(x*_(rho/2)) is unchanged, since the
minimizer is unchanged. Restricting the next auxiliary support to Allowed only
removes coordinates from the positivity argument in that audit. Thus its
late-phase recurrence and charge also hold: when E<=alpha^2*rho,

    vol(supp zplus) <= vol(supp z)/2 + 15/rho,
    sum_(k=1)^K vol(supp z_k) <= vol(supp z_0)+30*K/rho. (4)

The initial phase and initial-state costs remain additional.

## 3. The guard is local and changes no other update

In degree coordinates f_i=x_i/sqrt(d_i), the existing reporter emits positive
values sigma*(key_i-tau), where tau>=theta*rho/sigma>0. The guarded subclass
forces every exposed forbidden coordinate to have key zero. It can never be
emitted, while allowed-coordinate keys retain the exact original formula.
The weighted water-fill threshold therefore computes precisely the Euclidean
projection onto C_A: forbidden coordinates contribute zero to every relevant
positive tail sum. No traversal of unexposed coordinates is required.

This override is valid during construction: the seed is exposed first, and its
degree is installed before its key is set. All later guard checks use cached
seed and vertex degrees. A forbidden boundary coordinate still receives its
charged degree reply and any sparse response updates. Its response is kept
because the implementation represents the actual full-vector Qx, but its own
adjacency list is never scanned as an auxiliary coordinate. A warm initializer
rejects every forbidden positive input coordinate after a charged degree
query; zero entries require no exposure. The supplied gap bound remains the
caller's certificate, as in the original initializer.

The extra work is a constant number of exact scalar operations per attempted
key update or warm-input entry. If W is the number of exposed records, V_init
is the charged warm-support volume, and D_k=vol(supp z_k), the existing local
implementation has the same bound, up to logarithms,

    O((1+V_init+K+sum_k D_k)*log(2+W))

plus explicitly materialized output. Cached adjacency lists are read once;
repeated adjacency scans total V_init+sum_k D_k. Initial and output state is
charged, and stored iteration history contributes O(K) words. This expression
is a reduction to cumulative support work, not a bound on that sum during the
initial phase. The guard alone does not bound the number of low-degree
coordinates that could be exposed.

## 4. Exact verification

`test_guarded_monotone_capped_solver.py` uses a dense independently formed
matrix and independently sorted projection restricted by (2). It checks exact
state, projection, line search, energy, locality, and full KKT optima on small
exhaustively enumerated graphs, plus explicit cap and boundary cases. Results
are saved in `guarded_monotone_capped_verification.json`. Structural counters
are not complete Python-operation, allocation, or rational-bit instrumentation.
No randomized algorithm, data structure, or test input is used.

The completed run passes all five test methods, with 996 exhaustive optimal
points retained by the face and 2997 exact dense step comparisons. The compared
line fractions include 998 zero, 334 interior, and 1665 full steps; the binding
cap case includes a forbidden coordinate that the ordinary capped projection
would emit with density 1/64, while the guarded projection excludes it exactly.
The degree-100 star reads one adjacency entry once and scans it five times,
queries only two degrees, and keeps its forbidden hub response without scanning
the hub. Seed and nonseed equality rejection and rejected warm-start degree
charges are checked explicitly. Maximum measured Fraction bit length is 34 in
this suite; this finite observation is not a bit-complexity guarantee.
