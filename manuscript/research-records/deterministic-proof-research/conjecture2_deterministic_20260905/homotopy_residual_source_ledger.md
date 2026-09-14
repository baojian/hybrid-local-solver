# A square-root residual-source budget, and what a monotone corrector costs

Status: exact deterministic inequalities, including an explicit corrector
work bound. They do not close general OP2. The homotopy geometry and exact
hat representation used below are established in `homotopy_geometry.md`.
No exact optimizer, derivative, or Schur response is assumed available free.

Let `w=sqrt(d)`, `theta=sqrt(alpha)`, and `q0=(1+alpha)/2<=1`.
For nested supports along the exact regularization path, write
`p_S=alpha*Q_SS^(-1)w_S`, extended by zero. Its nonnegative derivative
jumps Delta p are pairwise Q-orthogonal and obey

    ||Delta p||_Q^2=alpha*w^T Delta p.

## 1. Positive derivative forcing is concentrated on the admission block

For one jump from S to S union B, put

    f=(Q*Delta p)_B=alpha*w_B-Q_BS*p_S>0.

The vector `Q*Delta p` is zero on S and nonpositive outside S union B.
Thus f is its entire positive part. Since Q has nonpositive off-diagonals,

    f_i <= Q_ii*Delta p_i=q0*Delta p_i,  i in B.

It follows that

    ||f||_2^2 <= q0*f^T Delta p_B
               =q0*||Delta p||_Q^2
               =q0*alpha*w^T Delta p.

With `R(Delta p)=w^T[Q*Delta p]_+`, Cauchy-Schwarz gives

    R(Delta p)
       <= sqrt(q0*alpha*vol(B)*w^T Delta p).          (1)

Admission blocks are disjoint, and the total derivative mass is at most
the final support volume M. Summing (1) therefore yields

    sum_j R(Delta p_j) <= sqrt(q0*alpha)*M
                         <= theta*M.                (2)

This improves the scale of a positive-residual budget by sqrt(alpha)
relative to a volume-only bound. It is not an assumption about a solver.

There is also a signed variation estimate. Since `w^TQ=alpha*w^T`,

    w^T|Q*Delta p|
       =2R(Delta p)-alpha*w^T Delta p
       <=2R(Delta p).

Thus the total weighted absolute residual variation of all derivative
admissions is at most `2theta*M`.

## 2. Exact secants inherit this budget

For consecutive exact secant predictors, the proven representation is

    e_j/h_(j+1)=sum_l kappa_j(s_l)*Delta p_l,

where all coefficients are nonnegative and `sum_j kappa_j(s)<=1`.
Positive-part subadditivity gives

    sum_j w^T[Q*e_j]_+/h_(j+1) <= theta*M.            (3)

The same argument bounds summed normalized weighted absolute residual
variation by `2theta*M`.

This residual is operationally meaningful. If ell_j is the safe secant
predictor and x* is the new exact optimum, then `e_j=x*-ell_j>=0` and
`supp(ell_j) subseteq supp(x*)`. On the new optimal support, its KKT
gradient is zero, so `Qe_j=-grad J_new(ell_j)` there. Outside that support,
`Qe_j<=0` and `grad J_new(ell_j)>=0`. Consequently

    w^T[Qe_j]_+ = w^T[-grad J_new(ell_j)]_+.

The positive residual is supported on the current predictor support and
its exposed boundary. It can be materialized by a charged scan there; this
does not reveal or grant the future support.

For a constant-factor geometric rho schedule, `h_(j+1)/rho_(j+1)` is a
constant. Thus (3) also gives

    sum_j R_j/rho_(j+1) <= O(theta*M),                (4)

where R_j is the actual positive residual mass of the exact predictor.
Initial predictor-residual scans cost O(M) over such a geometric schedule,
using `vol(S(rho_j))<=1/rho_j`. Computing the exact predictors themselves
still has to be paid for.

## 3. The same source budget applies to actual fixed-rho correction batches

The following comparison does not assume that a batch admission order is
the same as the natural regularization-path order. Start from a known exact
optimum x_old at rho_old, and put `rho_new=rho_old-h`, h>0. First solve on
the old support at the new parameter; subsequently perform exact safe
all-violations batches. Let S be any current admitted support containing the
old support, and let x_S be its exact principal solution at rho_new.

The old KKT residual in the sign convention of a positive descent source is

    r_old=b-alpha*rho_old*w-Q*x_old<=0.

Consequently, on S,

    x_S=x_old+Q_SS^(-1)[alpha*h*w_S+(r_old)_S]
        <=x_old+h*p_S.                              (5)

For a new batch B outside S, its positive actual forcing is

    f_B^x=(b-alpha*rho_new*w-Q*x_S)_B>0.

Off-diagonal nonpositivity and (5) give

    f_B^x <= (r_old)_B+h*(alpha*w_B-Q_BS*p_S)
            <=h*f_B^p,                              (6)

where f_B^p is the uniform-RHS derivative forcing from section 1. Both
principal increments use the same inverse-positive extension operator:
their old-support equation is zero and their B equation is respectively
f_B^x or f_B^p. Hence

    0<=Delta x<=h*Delta p,
    ||Delta x||_Q^2=(f_B^x)^T Delta x_B
                    <=h^2*||Delta p||_Q^2.          (7)

Applying the disjoint-block source budget to this arbitrary nested support
sequence yields

    sum_batches w^T[Q*Delta x]_+ <=h*theta*M.        (8)

The first old-support solve can be included: its increment is exactly
`h*p_(S_old)`, corresponding to the first derivative admission block
S_old from the zero derivative. Thus (8) also includes its source. It does
not include the prior work required to obtain x_old.

Outside each newly solved support, `Q*Delta x<=0`; this is the positive
incoming change of boundary residual. Since `w^TQ*Delta x=alpha*w^TDelta x`,
the total weighted absolute residual variation is at most twice the
left side of (8). Thus this is a budget for the actual successive boundary
responses, not only a path regularity identity.

At a geometric rho change, h/rho_new is constant. A deterministic procedure
that could compute/report these responses at cost proportional to their
weighted variation divided by `alpha*rho_new` would fit the OP2 target.
The identities do not provide such a procedure: dense Schur response
computation cannot be skipped, and arbitrarily tiny coordinate changes
cannot each be charged as if they exceeded that threshold.

## 4. Fully charged monotone coordinate correction

Here is a deterministic correction rule with an explicit work inequality.
Given a safe lower point x at fixed rho, maintain

    r=b-alpha*rho*w-Q*x,
    R=w^T[r]_+.

For a chosen threshold tau>0, report a coordinate satisfying
`r_i>tau*w_i` and perform its exact positive coordinate minimization

    Delta x_i=r_i/Q_ii.

The Stieltjes sign pattern keeps x below the exact optimum. In particular
any newly positive coordinate is a safe admission. Its residual becomes
zero; every other residual increases by `-Q_ji*Delta x_i>=0`.
The total positive residual mass can increase by at most the sum of these
incoming increments, whether or not previously negative entries cross zero.
Since `sum_(j!=i)w_j*(-Q_ji)=(Q_ii-alpha)w_i`, exactly

    R_new <= R-alpha*w_i*Delta x_i
           <= R-alpha*tau*d_i.                      (9)

A local adjacency scan and all residual updates for this push cost
O(d_i), or O(d_i log E) with a deterministic threshold-reporting tree on
E exposed words. Initial residual materialization is also charged. Thus
the total update work before all residuals satisfy the threshold is

    O(R_initial/(alpha*tau) * log(E+2)).             (10)

No random choice or uncharged global maximum search is required. A
deterministic eligible-coordinate queue/tree suffices.

Equations (4) and (10) quantify the remaining loss. Even at thresholds
`tau_j=Theta(alpha*rho_(j+1))`, they only prove cumulative push work

    tilde O(M/alpha^(3/2)),                          (11)

which has an extra factor 1/alpha over the requested M/sqrt(alpha).
Some final accuracy/support certificates require an even smaller tau;
no sufficient final-accuracy assertion is made for the displayed threshold.
Using the looser `tau_j=Theta(rho_(j+1))` would make (10) meet the target
work, but the resulting residual tolerance does not supply the required
coarse-support or arbitrary-epsilon certificate.

The missing algorithmic feature can therefore be stated concretely: a
successful corrector or persistent response reporter should charge work
roughly to `R_j/(alpha*rho_(j+1))`, rather than introducing the additional
inverse-gap loss in (10) at useful residual accuracy. The source budget (3)
would fund such work. This note does not construct that primitive, and
the budget does not allow dense response computation to be treated as free.
