# A deterministic teleportation homotopy: proved nesting, open work bound

This is an independent structural derivation from the permitted problem
definitions. It is not a proof of Conjecture 2 or a novelty claim.

Fix the graph, point source v, and regularization rho. Write L=D-A for the
combinatorial Laplacian in this note only. For 0<alpha<1 put

    c=(1-alpha)/2, theta=alpha/c=2alpha/(1-alpha),
    y_alpha=D^(-1/2)x_rho^*(alpha), u_theta=y_alpha/theta,
    h=e_v-rho d.

On the nonnegative orthant the original objective, after substituting
x=theta D^(1/2)u, is the positive constant c theta^2 times

    J_theta(u)=u^T(L+theta D)u/2-h^T u, u>=0.

Thus u_theta is its unique minimizer. Its KKT conditions are

    u_theta>=0, (L+theta D)u_theta-h>=0,
    u_theta^T[(L+theta D)u_theta-h]=0.

**Proved lemma.** If 0<theta_2<theta_1, then
u_{theta_1}<=u_{theta_2} coordinatewise. In particular the support of the
original RPPR minimizer can only expand when alpha decreases, with rho and
the point source fixed.

Proof. Let u_1,u_2 be the two optima and let
T={i:(u_1)_i>(u_2)_i}. Suppose T is nonempty. Every i in T has (u_1)_i>0,
so its KKT equality holds at theta_1. At theta_2 the KKT inequality gives

    [(L+theta_2 D)(u_1-u_2)]_T
      <= -(theta_1-theta_2)D_T(u_1)_T < 0.

On T^c, u_1-u_2<=0. Since all off-diagonal entries of L+theta_2 D are
nonpositive, their contribution from T^c to the T rows is nonnegative.
Consequently

    (L+theta_2 D)_{TT}(u_1-u_2)_T < 0.

The principal inverse is nonnegative, which implies
(u_1-u_2)_T<=0, a contradiction. This proves the lemma.

The conclusion is about support and the rescaled u. It does not assert that
the original degree-coordinate values y_alpha, or x_rho^*(alpha), increase
as alpha decreases. Their extra factor theta changes with the parameter.

At alpha=1 the nonzero solution has support {v}; this is compatible with
the limiting nested-support statement. All supports in a schedule decreasing
alpha down to a fixed target remain inside the target support, so their
union volume is at most 1/rho. Reading each admitted adjacency list once
would therefore cost at most 1/rho.

## Proposed use and unresolved point

A geometric theta schedule has only logarithmically many parameter changes.
Successive full matrices L+theta D are spectrally equivalent within a factor
two when theta is halved. If the next support were already exposed, this
would make previous inverses plausible preconditioners.

The newly admitted coordinates are not supplied. They can form a large
unknown region, and the previous inverse does not automatically solve or
precondition that region. Spectral equivalence on a fixed full matrix is
therefore not a local algorithm or a charged reuse bound. The outstanding
target is to handle support expansion and inverse reuse together in total
~O(1/(rho sqrt(alpha_target))) deterministic work.
