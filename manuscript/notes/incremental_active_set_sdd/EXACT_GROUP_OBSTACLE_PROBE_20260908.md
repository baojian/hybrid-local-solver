# Exact obstacle gates after the neighborhood-type result

**Next construction and audit target.** General OP3 remains Open.
The default grouped producer returns original ACL output using
lambda=eps_appr/2 and kappa=lambda/2. The exact type-bound and four-type
output lower bound are already proved drafts in
`sec:op3-neighborhood-types`. The binary-tree grouped-order obstruction
is in `sec:op3-group-branching-obstruction` and remains representation-specific.

## Minimal extension, without modifying the audited default backend

For 0<lambda<1/2, initialize GroupFrontier at epsilon=2*lambda and set
kappa=0 before its first eligibility query. Initialization creates only
the seed group q=1; it performs no gate or numerical update, so this is
an exact interface change, not a retroactive stopping-rule mutation.
Admit exactly when h_i>0, equivalently q_t>lambda*d_i. The existing
positive Schur, volume-guard and reverse-group proofs should then give
the full KKT certificate

    u>=0, M*u >= e_v-lambda*d,
    u_i*(M*u-e_v+lambda*d)_i = 0.

Every prefix remains support-safe and has volume below 1/lambda, including
full support at positive alpha. Finite termination uses the number of
admissions, not a lower bound on a positive gate or pivot magnitude.

For lambda>=1/2, a single original degree query suffices. If d_v>=2,
u=0 is the exact obstacle. If d_v=1, set u_v=(1-lambda)_+ and other
coordinates zero. The outside residual is at most gamma*(1-lambda)_+
<=lambda*d_j, so no adjacency row is needed. This also handles lambda>=1.
Do not route large lambda through the backend's ACL epsilon<1 assertion.

Target the same fully paid trajectory-dependent group bound, and
O((1+V)(1+k)^2 log(2+V)) under the unsupplied global k-type promise.
No general small-k conclusion or bit-complexity claim follows.

## Canonical RPPR mapping to recheck explicitly

The project objective is

    F_rho(X) = 1/2 X'QX - alpha*(D^-1/2 e_v)'X
               + alpha*rho*||D^1/2 X||_1,
    Q = alpha I + (1-alpha)/2*(I-D^-1/2 A D^-1/2).

With bar_alpha=2alpha/(1+alpha), X=bar_alpha*D^1/2*u and lambda=rho,

    F_rho(X) = alpha*bar_alpha *
      [1/2 u'Mu - e_v'u + rho*sum_i d_i*|u_i|].

Check the original KKT signs and this scaling, keeping exact physical
potentials, original-degree records and the canonical coordinate chart
distinct. A canonical coordinate can contain sqrt(d_i); a rational audit
must not describe it as a rational scalar. Return the exact physical
representation and verify the descaled canonical KKT identities. State
any explicit square-root convention if claiming fully materialized exact
canonical coordinates. No arbitrary-graph OP2 result is implied.

## Falsifiable checks and later questions

Audit all positive and zero regimes, exact h=0 ties, tiny positive gates,
alpha through 2^-1024, all seeds on small graphs, mixed clique/independent
quotient blow-ups, and private huge hubs. Compare with independent dense
obstacles and original residual/KKT rows, with validators clearly excluded
from producer work. The original default backend and its existing audits
can remain unchanged.

After this bounded extension, return to broader OP3 compression. The
binary-tree example has many response groups but admits hierarchical
low-rank structure. A useful generalization needs a paid threshold reporter
and reconstruction for such compositions, not just a low-rank matrix.
The source neighborhood-diversity implication from vertex cover gives an
exponential parameter bound; improving that dependence is another concrete
structural target, but must not be confused with the arbitrary-graph target.
