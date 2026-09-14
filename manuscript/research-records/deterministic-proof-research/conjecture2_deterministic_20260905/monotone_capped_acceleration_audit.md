# Monotone capped acceleration: independent audit

Status: the convergence, lazy implementation, and final-phase support
recurrence below are sound. The initial-phase work remains unproved, so
this is not a general OP2 proof. No randomness is used.

Let `J(x)=x^TQx/2-b^Tx+lambda*w^Tx` on the nonnegative orthant, where
`lambda=alpha*rho`, `w=sqrt(d)`, `theta=sqrt(alpha)`, and `a=1-theta`.
Assume 0<alpha<1; alpha=1 is handled directly by the diagonal solution.
Let `C={x>=0:w^Tx<=1}`, which contains the optimum x*.

## 1. Monotone line search preserves accelerated energy contraction

Given x,z in C, compute the ordinary capped mirror step

    y=(x+theta*z)/(1+theta),
    z_raw=a*z+theta*y-grad J(y)/theta,
    z^+=Proj_C(z_raw),
    x_hat=a*x+theta*z^+.

Choose x^+ to minimize J on the segment from x to x_hat. Equivalently,

    x^+=(1-gamma)*x+gamma*z^+,  0<=gamma<=theta.       (1)

Both segment endpoints belong to C. The line search gives

    J(x^+)<=J(x_hat),
    J(x^+)<=J(x).

The already proved one-projection energy inequality applies to x_hat and
z^+. Replacing x_hat by x^+ only decreases its objective term. Therefore

    E(x^+,z^+)<=a*E(x,z)
        -alpha*theta*(1-alpha)/2*||z-y||_2^2,
    E(x,z)=J(x)-J(x*)+alpha/2*||z-x*||_2^2.           (2)

Starting from x=z=0, the objective satisfies `J(x_k)<=0` throughout, and
the objective convergence rate remains accelerated. The cap-multiplier
dissipation previously obtained by retaining the projection cross term
also survives, since the line search decreases J further.

The relation `theta*z^+<=x^+` need not survive (1). No proof below uses it.
The weaker facts `x,z>=0` and `x,z in C` do survive.

## 2. Exact line coefficients need only the new auxiliary support

Put `ell(x)=-b^Tx+lambda*w^Tx`. Maintain the scalars

    A=x^TQx,  L_x=ell(x).

For the newly materialized z^+, compute

    B=(z^+)^TQx,
    C_z=(z^+)^TQz^+,
    L_z=ell(z^+).

On the line in (1),

    J((1-gamma)x+gamma z^+)
       =J(x)+gamma*G+gamma^2*H/2,
    G=B-A+L_z-L_x,
    H=C_z-2B+A=||z^+-x||_Q^2.

If H=0, then z^+=x and gamma=0 is valid. Otherwise choose

    gamma=min(theta,max(0,-G/H)).                     (3)

The scalar state updates are

    A^+=(1-gamma)^2*A+2gamma(1-gamma)*B+gamma^2*C_z,
    L_x^+=(1-gamma)*L_x+gamma*L_z.

Let `L0=Q-alpha*I`, `r=L0*x`, and `t^+=L0*z^+`. The existing lazy state
provides Qx_i as `alpha*x_i+r_i` at any selected coordinate. Thus B uses
only the support of z^+. Computing t^+ requires one charged scan of that
support and its nonrecursively exposed neighbors; C_z then uses
`alpha*||z^+||^2+(z^+)^Tt^+`. L_z needs only the auxiliary mass and its
seed coordinate. No line coefficient requires a scan of old x support.

The lazy updates become

    x^+=(1-gamma)*x+gamma*z^+,
    r^+=(1-gamma)*r+gamma*t^+.

Replace the old fixed scale `a^k` by a maintained positive scale sigma:

    sigma^+=(1-gamma)*sigma,
    X=x/sigma,  R=r/sigma.

Since `1-gamma>=a>0`, the scale never vanishes. The normalized X and R
receive sparse additions `gamma*z^+/sigma^+` and `gamma*t^+/sigma^+`.
Even when gamma=0, z^+ and t^+ are retained for the next mirror query.

The raw mirror identity and its ordered-tree keys remain unchanged:

    z_raw=a*z-r/[theta*(1+theta)]-t/(1+theta)
             +b/theta-theta*rho*w.

They require a single shared positive scale, not the special formula
sigma=a^k. Reverting old sparse exceptions, updating the scale, updating
sparse base keys, and installing new exceptions therefore have exactly the
same charged support-local implementation as the original lazy reporter.

For the full run from zero, old x entries are contained in the union of
previous auxiliary supports and their final materialization is charged to
that history. For an externally supplied warm start, its initial state and
eventual output entries still have to be charged; the late-phase theorem
does not grant a large preexisting support for free.

## 3. Support recurrence without theta*z<=x

Let `S_c=supp(x*_(rho/2))`, `M=vol(S_c)<=2/rho`, and let O be its
complement. Define mass coordinates

    u=D^(1/2)x,  v=theta*D^(1/2)z,
    P=A_graph*D^(-1),  c=(1-alpha)/2.

The next scaled auxiliary vector is

    v^+=[q-kappa*d]_+,  kappa>=0,
    q=a/2*[P(u+v)-(u-v)]+alpha*e_seed-lambda*d.

At the optimum pair `u*=D^(1/2)x*`, `v*=theta*u*`, the raw vector is
`q*=theta*u*-D^(1/2)grad J(x*)`. The strict outside-core gradient margin
gives `q*_i<=-lambda*d_i/2` on O.

Write `D_prev=vol(supp z)`, `D_next=vol(supp z^+)`, and
`m_out=sum_O u_i`. The exact quadratic gap identity gives

    ||x-x*||_Q<=sqrt(2E),
    theta*||z-x*||_2<=sqrt(2E),
    m_out<=2E/lambda.

The two already verified boundary-flux bounds are

    T_x<=sqrt(2ME/c)+m_out,
    T_z<=sqrt(2ME).

Here T_x and T_z sum positive incoming degree densities of respectively
x-x* and theta(z-x*) across edges from S_c to O, counting each boundary
edge once. The T_x estimate uses the actual Q Dirichlet energy.

The new point is the outside diagonal term. Without v<=u it is bounded
above by `a*v_i/2`, after dropping the nonpositive `-a*u_i/2`. Incoming
mass from O is at most `m_out+m_v`, where

    m_v=sum_O v_i
        <=theta*sqrt(D_prev)*||z-x*||_2
        <=sqrt(2D_prev E).

Thus positivity on the next outside support implies

    lambda/2*vol(supp(z^+) intersect O)
       <=a/2*(T_x+T_z+m_out+2m_v).

Substitution gives the claimed general feasible-state bound

    D_next<=M+(2+sqrt(2))*sqrt(ME)/lambda
              +4a*E/lambda^2
              +2a*sqrt(2D_prev E)/lambda.           (4)

Every sign in this argument remains valid under the line-search update;
in particular it never reinstates the lost v<=u invariant.

## 4. Final-phase amortization

If `E<=alpha^2*rho`, use M<=2/rho and Young's inequality to obtain

    2a*sqrt(2D_prev/rho)<=D_prev/2+4a^2/rho.

Equation (4) consequently implies

    D_next<=D_prev/2+(4+2sqrt(2)+4a+4a^2)/rho
            <=D_prev/2+(12+2sqrt(2))/rho
            <D_prev/2+15/rho.                       (5)

Energy contraction preserves the required energy level thereafter.
Summing K instances of (5) yields

    sum_(k=1)^K D_k<=D_0-D_K+30K/rho
                     <=D_0+30K/rho.                (6)

With the lazy reporter and line-coefficient implementation, this controls
the additional final-phase scans and arithmetic, up to logarithmic factors
and the explicitly charged initial state. It does not control the work
needed to reach the phase or remove the D_0 term without accounting for it.

## 5. J<=0 alone does not give a small instantaneous auxiliary support

The following is only an admissible-state example, not a trajectory from
the prescribed initialization and not a cumulative-work counterexample.
It shows that the new monotone objective constraint must be combined with
additional trajectory information in an early-phase theorem.

Take integers L>=64 and N>=L, set `theta=1/L`, `alpha=1/L^2`, and
`rho=1/(4N)`. Join the seed to N hubs; each hub has
`D=floor(L/8)` private leaves. Degrees are N at the seed, D+1 at each hub,
and one at each leaf. Put `q0=(1+alpha)/2`.

The exact RPPR optimum is seed-only, with seed degree density

    x*_seed/sqrt(N)=3alpha/(4q0*N),
    m*=w^Tx*=3alpha/(4q0).

Its hub KKT gradients are positive because
`D+1>3c/q0`; the half-regularization optimum is also seed-only because
`D+1>7c/q0`. Choose x=x*, and choose z supported only at the seed with
weighted mass 1/2. Then x,z belong to C, J(x)<0, D_prev=N, and

    E=alpha/(2N)*(1/2-m*)^2<=alpha*rho/2.

The next raw scaled auxiliary mass at each hub is

    [2a*m*+a*theta-alpha*(D+1)]/(4N)>0.

The seed raw mass is also positive, and all leaves have negative raw mass.
The total positive raw mass is

    a*theta/2+alpha-alpha*(D+2)/4<theta/2,

so the mass cap does not bind. Therefore the next auxiliary support has

    D_next=N*(D+2)=Theta(1/(rho*sqrt(alpha))).

All involved degrees are below the safe degree guards. Since x is already
optimal, the line search chooses gamma=0 in this example; an algorithm
with an exact optimality certificate could of course terminate instead.
The example is solely a limitation of instantaneous state-based reasoning.
One scan of the displayed size is within the desired cumulative budget.
