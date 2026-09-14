# Capped acceleration outside a certified comparison support

Status: exact deterministic lemmas and a sharper formulation of the remaining
work question. This document does not prove the cumulative support-work bound.
It uses only the permitted RPPR definitions and fresh current-task derivations.

Write `w=sqrt(d)`, `lambda=alpha*rho`, and

    J_rho(x)=0.5*x^T Qx-b^T x+alpha*rho*w^T x,  x>=0.

Let `x*=argmin J_rho`, `c=argmin J_(rho/2)`, and `S_c=supp(c)`.
The Stieltjes comparison principle gives `0<=x*<=c`, while the RPPR volume
identity gives `vol(S_c)<=2/rho`. Put `O=V\S_c`.

## 1. A strict original-gradient margin at the true optimum

Let `g*=Qx*-b+alpha*rho*w`. The orthant KKT conditions give `g*>=0` and
`g*_i*x*_i=0`. On O both `x*_i` and `c_i` are zero. All off-diagonal
entries of Q are nonpositive, so `x*<=c` implies

    (Qx*)_i >= (Qc)_i,  i in O.

The half-regularization KKT inequality at c therefore gives

    g*_i >= (Qc-b+alpha*rho*w/2)_i+alpha*rho*w_i/2
          >= alpha*rho*w_i/2,  i in O.                 (1)

This is a margin for the gradient at the original optimum, not merely a
gradient statement at c. In particular it includes any degenerate original
inactive constraints: they must lie inside S_c if their original margin
is smaller than the displayed positive threshold.

The exact quadratic expansion, valid for every x>=0, is

    J_rho(x)-J_rho(x*)
       = 0.5*(x-x*)^T Q(x-x*) + (g*)^T x.

Using (1) and Q>=alpha*I gives the useful joint certificate

    J_rho(x)-J_rho(x*)
       >= alpha/2*||x-x*||_2^2
          + alpha*rho/2*sum_(i in O) w_i*x_i.          (2)

No computation of c is supplied by this lemma. It is an analytical
comparator; an algorithm may not scan or use S_c for free.

## 2. An exact outside-mass ledger for the one-projection scheme

Let `theta=sqrt(alpha)`, `a=1-theta`, with 0<alpha<1. Consider the capped
one-projection update

    z_(k+1)=Proj_C(z_raw,k),
    x_(k+1)=a*x_k+theta*z_(k+1),
    C={x>=0:w^T x<=1},

started at zero. Define outside position and scaled auxiliary mass by

    M_k=sum_(i in O) w_i*x_(k,i),
    V_k=theta*sum_(i in O) w_i*z_(k,i).

Then, exactly,

    M_(k+1)=a*M_k+V_(k+1),                            (3)
    sum_(k=1)^K V_k=M_K+theta*sum_(k=1)^(K-1) M_k.    (4)

This is special to the averaging update. The aligned minimum variant has
an additional nonnegative deletion term and cannot use (3) as an equality.

The known accelerated energy bound is

    E_k=J_rho(x_k)-J_rho(x*)+alpha/2*||z_k-x*||_2^2
       <= a^k E_0.

Together with (2) and the mass cap, it implies

    0<=M_k<=min(1,C_0*a^k),
    C_0=2 E_0/(alpha*rho).                            (5)

The usual initial bound `E_0<=alpha/d_seed` gives
`C_0<=2/(rho*d_seed)`. The zero vector can be returned directly when
E_0=0, so that degenerate case causes no logarithmic convention issue.

For any positive C_0, (4)-(5) imply the infinite-horizon bound

    sum_(k=1)^infinity V_k <= log_+(C_0)+2.            (6)

Indeed M_k tends to zero. Thus the left side is
`theta*sum_(k>=1)M_k`. If C_0<=1, the geometric bound is at most C_0.
Otherwise put `j=ceil(log(C_0)/(-log(a)))`; bounding the first j terms
by one and the tail geometrically gives at most
`theta*j+1<=log(C_0)+theta+1`, since `-log(a)>=theta`.

A sharper tail statement follows directly from telescoping (3): for
every L>=0 and every N>L,

    sum_(k=L+1)^N V_k <= C_0*a^(L+1).                 (7)

To check (7), write its left side as
`M_N-a*M_L+theta*sum_(k=L+1)^(N-1)M_k`, apply (5), drop the negative
term, and sum the resulting geometric series. In particular once
`C_0*a^L<=theta`, the entire future outside scaled auxiliary mass is at
most theta, independent of the requested final accuracy.

These are mass estimates, not support-volume estimates. Arbitrarily small
positive auxiliary coordinates still count for adjacency work. Neither
(6) nor (7) gives a lower bound on a nonzero auxiliary coordinate.

## 3. The exact work ledger retains the helpful cap multiplier

Use mass coordinates `u=D^(1/2)x`, `v=theta*D^(1/2)z`, and the column
stochastic matrix `P=A D^(-1)`. Thus `0<=v<=u`, `sum u<=1`, and
`sum v<=theta`. The one-projection recurrence is

    r=a/2*[P(u+v)-(u-v)]+alpha*e_seed,
    v'=[r-beta*d]_+,
    u'=a*u+v',

where `beta=lambda+gamma`, `gamma>=0`, and gamma is chosen by the weighted
simplex projection. When gamma>0 the projected scaled mass is exactly
theta. Let `Z'=supp(v')`. Since `sum r=a*sum v+alpha`, summing over Z'
gives the exact identity

    lambda*vol(Z')
       = alpha+a*sum v-sum v'
         -gamma*vol(Z')-sum_(i notin Z') r_i.          (8)

All unexposed coordinates have r_i=0, so the final sum is analytically
finite and does not require a whole-graph oracle scan. Put
`R_k=-sum_(i notin Z_(k+1)) r_(k,i)`. Summing (8), using v_0=0, yields

    lambda*sum_(k=1)^K vol(Z_k)
       = alpha*K-theta*sum_(k=0)^(K-1)sum v_k-sum v_K
         +sum_(k=0)^(K-1)[R_k-gamma_k*vol(Z_(k+1))].  (9)

The cap subtraction must be kept. R_k alone may be large because stopped
old position mass can feed other vertices. The same phenomenon can force
a large gamma_k, whose subtraction cancels most of that contribution.
For example, on the two-vertex edge with seed one, an admissible state
u=(1,0), v=0 has r=(-a/2+alpha,a/2). For sufficiently small theta and
lambda, the cap selects only vertex two. Then R=a/2-alpha but
gamma=a/2-theta-lambda, so
`R-gamma*vol(Z')=theta+lambda-alpha`. This example is an algebraic check
of the ledger, not a claimed trajectory from the RPPR initialization.

## 4. A cap-multiplier budget from the omitted projection cross term

Write `m*=w^T x*`. In the nonzero regime, the RPPR mass identity gives
`m*<=1-rho*vol(supp(x*))<1`. Let the simplex projection multiplier in
z coordinates be nu, so

    z_i^+=[z_i^raw-nu*w_i]_+,  gamma=theta*nu.

If `nu>0`, then `w^Tz^+=1`. On positive projected coordinates the
projection residual is `nu*w_i`; on zero coordinates it is at most this
value. Since x* is nonnegative,

    <z_raw-z^+, z^+-x*>
       =nu*(1-m*)
          +sum_(z_i^+=0)(nu*w_i-z_i^raw)*x*_i
       >=nu*(1-m*).                                 (10)

When nu=0 the same lower bound follows from orthant projection.
The exact squared-distance identity retains twice this cross term:

    ||z^+-x*||^2
       =||z_raw-x*||^2-||z_raw-z^+||^2
          -2<z_raw-z^+,z^+-x*>.

In the accelerated proof, multiplying by alpha/2 and using (10) gives
the additional dissipation

    E_(k+1)<=a*E_k-theta*gamma_k*(1-m*).              (11)

Other already known nonnegative dissipation terms can also be retained.
The argument applies both to the averaging update and to the aligned
minimum update, since both cancel at most the same projection square.
Summing (11) gives

    sum_(k=0)^(K-1) gamma_k
       <= E_0/[theta*(1-m*)]
       <= theta/[d_seed*(1-m*)].                    (12)

This controls the sum of cap threshold shifts. It does not by itself
control the shifts multiplied by active volume, or the active volumes
without a shift. The distinction matters when many densities lie very
close to the simplex threshold.

## 5. What would complete this route

The already proved volume bound charges all auxiliary work on S_c by

    sum_(k=1)^K vol(Z_k intersect S_c)<=2K/rho.

Consequently only outside-S_c work needs a new theorem. One sufficient
form is

    sum_(k=1)^K vol(Z_k intersect O)
       <= [1/(rho*theta)]*polylog(1/alpha,1/rho,exposed words).

Equivalently, a suitable outside-core version of (9) must control net
stopped-mass reflection after the cap subtraction. The strict margin
(1), the monotonicity of rescaled positions
`a^(-k)x_k`, and the tail kinetic-mass estimate (7) are exact available
ingredients. No inequality converting them to the displayed support
count has been established here.

An entropy bound for ordinary reversible Markov semigroups cannot simply
be substituted: this recurrence contains clipping, inertia, and a global
simplex multiplier. In particular, ordinary entropy/Pinsker inequalities
control weighted mass differences, not the number of arbitrarily small
positive coordinate activations.
