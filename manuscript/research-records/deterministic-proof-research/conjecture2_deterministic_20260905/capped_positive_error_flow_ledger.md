# Capped kinetic support charged to positive boundary flow

Status: rigorous deterministic inequalities, including a conditional local-work
theorem. The required integrated flow estimate for the actual accelerated
trajectory remains open. No other manuscript notes or previous directions
were used.

## 1. Notation and the scope of the recurrence

Let `theta=sqrt(alpha)`, `a=1-theta`, `c=(1-alpha)/2`,
`lambda=alpha*rho`, `w=sqrt(d)`, and `P=A D^(-1)`. The columns of P sum
to one. Write `K=(I+P)/2`, `u=D^(1/2)x`, and
`V=theta*D^(1/2)z`. The smooth orthant objective is

    J(x)=0.5*x^T Qx-b^T x+lambda*w^T x.

The capped mirror step in all the current variants has the mass-coordinate
form

    Vnew=[a*K*V + a/2*(P-I)*u + alpha*e_seed
                   -lambda*d-gamma*d]_+,                 (1)

where `gamma>=0` is the simplex multiplier and `sum Vnew<=theta`.
This note does not require `V<=u` or any particular primal update. In
particular, it applies to a primal point chosen by minimizing J on the
segment from x to `a*x+theta*znew`.

Let `x*` be the rho minimizer, `u*=D^(1/2)x*`, and `V*=theta*u*`.
Let `C=supp(x*_(rho/2))`, so `vol(C)<=2/rho`, and define the
mass-coordinate optimal gradient

    r*=D^(1/2)*grad J(x*)
      =alpha*u*+c*(I-P)*u*-alpha*e_seed+lambda*d.

The orthant KKT conditions give `r*>=0`. Stieltjes comparison with the
half-regularization solution gives

    r*_i>=lambda*d_i/2,  i outside C.                       (2)

Also `u*_i=V*_i=0` outside C. C is only an analytical comparator, never
an assumed input or an uncharged support oracle.

## 2. A positive-error support ledger

Define coordinatewise nonnegative vectors

    e=(V-V*)_+,
    f=[a/2*(P-I)*(u-u*)]_+.

The fixed-pair identity is

    a*K*V*+a/2*(P-I)*u*+alpha*e_seed-lambda*d=V*-r*. (3)

It follows directly from `c=a*(1+theta)/2` and the definition of r*.
Subtracting (3) from (1), using K entrywise nonnegative, and dropping
the nonnegative cap subtraction proves

    enew <= [a*K*e+f-r*]_+.                                (4)

Here the scalar identity
`([v+t]_+-v)_+=[t]_+` for `v>=0` justifies subtracting V* through
the orthant projection. On an outside-C coordinate where Vnew is
positive, (2)-(4) yield

    enew_i+lambda*d_i/2 <= (a*K*e+f)_i.

On every remaining coordinate, `enew_i<=(a*K*e+f)_i`.
Since K preserves total mass, summing gives the exact useful inequality

    lambda/2*vol(supp(Vnew) outside C)+||enew||_1
        <= a*||e||_1+||f||_1.                              (5)

For any Kiter successive steps,

    lambda/2*sum_k vol(supp(V_(k+1)) outside C)
      +||e_Kiter||_1+theta*sum_(k=0)^(Kiter-1)||e_k||_1
        <= ||e_0||_1+sum_(k=0)^(Kiter-1)||f_k||_1.          (6)

In particular, the zero initialization has e_0=0. A proof that

    sum_k ||f_k||_1 <= theta*polylog(parameters)             (7)

over the initial accelerated phase would establish the missing outside-C
support bound. Work inside C is at most `2*Kiter/rho`.

This ledger charges every positive coordinate, including arbitrarily
small ones. It is therefore stronger for the locality question than an
outside-mass estimate. It deliberately discards the cap's helpful
subtraction, so proving (7) is sufficient but not necessary.

## 3. The true optimum has only seed-supplied positive divergence

Put `L0=I-P`. If a nonseed coordinate is active at the optimum, its
KKT equality gives

    c*(L0*u*)_i=-alpha*u*_i-lambda*d_i<0.

If it is inactive, `u*_i=0`, and
`(L0*u*)_i=-(P*u*)_i<=0`. Thus the positive part of `L0*u*` is
supported only at the seed. If the solution is nonzero, its seed is
active: otherwise summing the active-coordinate equations would make
the nonnegative grounded energy equal a strictly negative regularization
term. At the active seed,

    c*(L0*u*)_seed=alpha-alpha*u*_seed-lambda*d_seed<=alpha.

The zero solution satisfies the same bound trivially. Since every
Laplacian vector has zero total sum,

    c*||(L0*u*)_+||_1<=alpha,
    c*||L0*u*||_1<=2*alpha.                               (8)

This includes all inactive boundary coordinates; no boundary scan is
being supplied by the proof.

## 4. A computable sufficient flow condition

Positive-part subadditivity, zero total Laplacian sum, and (8) show

    ||f||_1
      <= a/2*(||(P-I)*u|_+||_1+||(I-P)*u*|_+||_1)
      <= [c*||(I-P)*u||_1/2+alpha]/(1+theta).              (9)

Consequently a bound

    c*||(I-P)*u_k||_1<=B*alpha

would give `||f_k||_1<=(B/2+1)*alpha/(1+theta)`.
More generally, an integrated bound

    c*sum_k ||(I-P)*u_k||_1
        <= theta*polylog(parameters)                       (10)

is sufficient over `Kiter=O(theta^(-1)*polylog(parameters))` steps.
It need not hold at every individual iteration with a constant B.

The constraint set

    {x>=0 : w^T x<=1,
             c*||(I-P)*D^(1/2)x||_1<=2*alpha}

is convex and contains x*. Its existence is not an algorithm: projection
or minimization over this set still requires a fully charged local
implementation and an accelerated convergence proof.

## 5. Two situations where the ledger already closes

### 5.1 The primal point is held at the exact optimum

If u=u* for every step of an interval, f=0. Any initial capped mirror
state satisfies `||e_0||_1<=sum V_0<=theta`. Equation (6) therefore gives

    sum_k vol(supp(V_(k+1)) outside C)<=2/(rho*theta).        (11)

This rigorously bounds all subsequent auxiliary ghosts, regardless of
how small their positive entries are. It is a conditional statement
about such an interval, not a claim that the algorithm reaches x*
in finitely many iterations.

### 5.2 Every primal point is an exact safe principal solution

Let x=X(S) be the exact principal minimizer for a safe active set S, with
`0<=x<=x*`, all coordinates in S positive, and zero elsewhere. If S is
nonempty it contains the seed. On S both gradients vanish, so

    c*(P-I)*(u-u*)=alpha*(u-u*)<=0.

Thus f is zero on S. Outside S, the seed is absent and
`(I-P)*u*<=0`, as proved in section 3, so

    f_i<=a/2*(P*u)_i, i outside S.

Summing the restricted KKT equations gives the exact outgoing-flow
identity

    alpha*sum u+c*sum_(i outside S)(P*u)_i
       =alpha-lambda*vol(S)<=alpha.                      (12)

Hence `||f||_1<=alpha/(1+theta)`. When S is empty, the same conclusion
follows from (8), since f is then `a/2*((I-P)*u*)_+`.
If every primal point of a zero-started sequence has this property,
equation (6) and `vol(C)<=2/rho` give

    sum_k vol(supp(V_(k+1)))
       <= (2+2/(1+theta))*Kiter/rho < 4*Kiter/rho.          (13)

The numerical cost of finding these exact principal solutions remains
unresolved in the general graph. Equation (13) must not be used to
assume those solves are free.

## 6. Why a scalar flow limiter needs a new convergence argument

Let v be the accelerated primal candidate. A sufficient condition for
replacing it in the existing energy argument is `J(xnew)<=J(v)`.
For a radial scaling `tau*v`, write

    A=v^T Qv,  B=b^T v-lambda*w^T v.

When A>0 and `0<=tau<1`, direct quadratic expansion shows

    J(tau*v)<=J(v)  iff  tau>=2*B/A-1.                   (14)

Imposing the flow constraint by shrinking tau can conflict with (14).
Likewise, truncating the segment from x to v at its first intersection
with the flow ball can increase the objective relative to v. Convexity
of the flow ball alone does not preserve the accelerated cancellation.
These are exact algebraic limitations of a proposed proof technique,
not reachable-state counterexamples to any concrete RPPR algorithm.

The outstanding theorem is either (7)/(10) for the actual initialized
trajectory, or an affordable new primal update that enforces an adequate
flow condition while retaining accelerated convergence.

## 7. A sharper ledger charges only selected signed boundary flow

Total positive flow is a potentially wasteful sufficient condition:
stopped position coordinates can have persistent Laplacian variation
without generating further positive auxiliary coordinates. The following
identity retains this distinction exactly.

At each step put

    E={i: Vnew_i>V*_i},
    n=(V*-V)_+,
    h=a/2*(P-I)*(u-u*).

Thus `V-V*=e-n`, while `enew` is supported exactly on E. Every selected
coordinate is positive before and after projection. Subtracting (3) on
E gives the equality

    enew_i+r*_i+gamma*d_i
        =a*(K*e)_i-a*(K*n)_i+h_i,  i in E.             (15)

Every positive auxiliary coordinate outside C is in E, because V*=0
there. Summing (15), using (2), and retaining all nonnegative losses,
gives

    lambda/2*vol(supp(Vnew) outside C)+||enew||_1
      <=a*||e||_1+Phi,                                  (16)

where the signed per-step charge is

    Phi=sum_(i in E) h_i-gamma*vol(E)
          -a*sum_(i outside E)(K*e)_i
          -a*sum_(i in E)(K*n)_i.                       (17)

The same telescoping as in (6) proves

    lambda/2*sum_k vol(supp(V_(k+1)) outside C)
      +||e_Kiter||_1+theta*sum_(k=0)^(Kiter-1)||e_k||_1
         <=||e_0||_1+sum_k Phi_k.                       (18)

Phi may be negative on a given step; it should not be replaced by its
positive part unless the resulting loss is explicitly acceptable. In
particular, (17) keeps the cap subtraction and both killed-transport
terms. A still valid intermediate relaxation replaces Phi by
`sum_(i in E) f_i`, which ignores flow at all unselected coordinates.

Writing `delta y=D^(-1)*(u-u*)`, the signed flow in (17) is exactly

    sum_(i in E) h_i
      =a/2*sum_({i,j} edge, i in E, j outside E)
                         (delta y_j-delta y_i).          (19)

All edges internal to E cancel. Thus the sharper missing estimate is a
bound on selected-set boundary flux after the three subtractions in
(17), rather than a bound on all graph Laplacian variation. Equations
(15)-(19) are identities or one-sided inequalities for the actual
initialized algorithm, although E and x* are analytical comparators and
need not be computed by that algorithm.

No bound of order `theta*polylog` on the sum in (18) has yet been proved.
In particular, a maximum outside position-mass bound alone does not
control this adaptive signed boundary flux without an additional
reservoir-lifetime or transport argument.
