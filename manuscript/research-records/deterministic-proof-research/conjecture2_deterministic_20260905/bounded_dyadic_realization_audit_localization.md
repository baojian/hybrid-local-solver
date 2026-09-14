# Independent audit of bounded-dyadic stage errors and continuation

Audited: `bounded_dyadic_realization.md`, Sections 1, 3, 4, and 6, together
with the perturbation interface in `perturbed_q_metric_kinetic_work.md`.
The degree-denominator/tree bit analysis is being audited independently by
the pivot agent. No existing manuscript directions were consulted.

**Result:** the audited stage realization and rounded continuation are
mathematically sound. Two small exposition corrections were sent to the
root: the abstract stage should state `tau<=alpha^2*r`, and the response
formula should use the degree-conjugated Q operator when applied to the
stored density X. The actual Section 6 tolerance already satisfies the
stronger tau restriction, and the displayed scalar response formula is
correct.

## 1. Perturbed comparison and the constant 180

With exact raw evaluation, only downward mirror and primal errors remain.
The two energy recurrences have additive error

    zeta=(5/2)kappa_x+(5/2)(theta+mu)kappa_p.

For kappa_x<=10h, kappa_p=h, and theta<=1/2,

    Gamma=zeta/theta
      <=[25+(5/2)theta(1+theta)]h/theta
      <=27h/theta.

The grid condition h<=theta*tau/256 consequently gives
Gamma<=27tau/256<tau/8. The stronger abstract hypothesis tau<=alpha^2*r
therefore ensures Gamma<=alpha^2*r. It is automatically satisfied by
Section 6, since tau=alpha*delta^2/8 and delta<=alpha*r/2 imply

    tau<=alpha^3*r^2/32<=alpha^2*r.

The squared Q-error is at most 22alpha^2*r. Because there is no raw-step
error, the original selected-flow/Cauchy coefficient eight, rather than
the general perturbed coefficient sixteen, applies. The total kinetic work
is therefore at most `(8*22+4)K/r=180K/r`.

For the block stopping rule, theta is dyadic, so m=1/theta is an integer.
The inequality `(1-theta)^m<1/2` gives a^K<=tau/2 when K=m*q and
2^q>=2/tau. Initial actual-objective energy is at most one, and the
stationary perturbation contribution is below tau/8. Thus the actual
stored candidate has gap below tau, without storing exact powers with
denominators growing linearly in K.

## 2. Exact realization of the downward state error

At the beginning of an iteration, sigma>=1/2 and the physical density is
boxed by U. Hence X_i<=2U. Also a>=1/2, so a*sigma>=1/4. Since h<=1/8,
`floor_h(a*sigma)>=1/8`; division by the new scale is always defined.

The scale decrease caused by flooring is less than h. Its effect on a
physical coordinate is therefore at most 2U*h downward. On an emitted
coordinate, flooring the updated X creates a further physical density loss
of at most sigma_new*h<=h. On every un-emitted coordinate the intended
kinetic addition is zero, so no update to X is needed. A subsequent rebase
adds at most h more. The total primal density loss is bounded by
`(2U+2)h<=10h`, exactly as required by the abstract theorem.

The mirror rounding is componentwise downward by less than h. The actual
mirror remains nonnegative and below its ideal feasible projection.
The new primal is below the feasible convex combination a*xi+theta*p,
and is nonnegative by its explicit stored construction. Thus every actual
stored state satisfies both the box and mass constraint.

The use of actual dyadic X increments in neighbor sums is essential.
Scattering an unrounded intended increment would evaluate a different raw
point at the next iteration and invalidate the claimed zero raw error.

## 3. Closed-tail emission and rebasing

The stored mirror density is positive exactly when the ideal projected
density is at least h, provided h<=U. This condition follows from the
actual tolerance/grid prescription. Equality must be included; the stated
closed-tail threshold is therefore correct. Values strictly between zero
and h remain unmaterialized and incur no adjacency inspection. Their
omission still obeys the global downward error bound h.

The rebase changes each physical coordinate to its downward h-grid value,
so its additional error is at most h in density. A coordinate can become
newly nonzero only when kinetic mass was emitted there. Therefore the
historical primal support volume is at most the cumulative emitted kinetic
volume, even after global scale changes and rebases.

Within a scale interval a step decreases sigma by at most theta+h. Starting
from one and crossing below one-half requires at least
`1/[2(theta+h)]` steps. Since h<=theta, at most `4theta*K+1` rebases occur.
For the block schedule theta*K=q=O(log(1/tau)). Rebuilding the exact
neighbor sums by scanning the entire historical support at each rebase is
therefore explicitly paid by the kinetic-history bound times one allowed
logarithmic factor. This audit does not treat that rebuild as a free scalar
rescaling.

## 4. PG-assisted rounded continuation

Let the actual completed-stage gap be at most
`tau=alpha*delta^2/8`. The exact projected-gradient point y decreases the
objective, so

    ||y-x*_r||_2<=sqrt(2tau/alpha)=delta/2.

If Delta=x-y, a valid subgradient at y is `(I-Q)Delta`, of norm at most
sqrt(2tau)<=delta/2. At every positive y coordinate its orthant normal is
zero. Thus the true gradient there is at most delta/2 in Euclidean units,
and, because w_i>=1,

    Qy_i-b_i<=(-lambda+delta/2)w_i.

The repaired density is `floor_h([y_i/w_i-delta]_+)`. It is below x*_r.
Its total error density is at most delta/2+delta+h<=2delta when h<=delta/2.
On a retained positive coordinate, the uniform shift decreases the
Q-product by alpha*delta*w_i; clipping other coordinates can only help.
Additional downward grid error can raise the product by at most h*w_i.
Since delta<=lambda/2 and h<=lambda/4, the resulting Q-product is still
strictly below b_i. At a zero repaired coordinate the Stieltjes signs give
Qbar_i<=0<=b_i directly.

Thus the actual dyadic baseline has nonnegative source, source density at
most lambda+2delta<=2lambda, support inside the true old support, and
objective error at most 2delta^2/r. The next factor-two stage therefore
has the same constant-four source bound.

The conditions h<=delta/2 and h<=lambda/4 follow by a wide margin from
h<=theta*tau/256 and the stated tau and delta bounds. Imposing them
explicitly is harmless and makes an implementation easier to audit.

Finally, the PG step needs only the old candidate support's adjacency scan.
Newly positive PG neighbors are evaluated and truncated before any of their
adjacency lists are inspected. The repaired support can then be scanned
under its proved volume bound. This order preserves the charged locality
of the continuation repair.

## 5. Exposition correction for the density response

With stored density X defined by `xi_i/w_i=sigma*X_i`, the response formula
should be written

    (D^(-1/2)(Q-mu I)D^(1/2)X)_i
       =(q0-mu)X_i-c*L_i/d_i.

Writing `((Q-mu I)X)_i/w_i` instead overloads X as both a normalized
coordinate vector and a density vector. The intended scalar computation,
neighbor sums, and perturbation bound are unaffected by this notation fix.

## 6. Audited scalar-only neighbor-sum rebase refinement

The root subsequently proposed avoiding rebase adjacency scans by maintaining
approximate primal neighbor sums, while current-kinetic and baseline sums
remain exact. This refinement fits the nonzero-raw-error version of the
perturbed theorem.

Let `E_i=L_i-sum_(j~i)X_j`. Exact scattered changes to X preserve E between
rebases. At a rebase, independently apply

    X'_j=floor_h(sigma*X_j),
    L'_i=floor_h(sigma*L_i),

using the old values and no neighbor scatter for the rebase itself. Writing
the two nonnegative rounding losses explicitly gives

    E'_i=sigma*E_i+sum_(j~i)loss_X,j-loss_L,i.

Thus `|E'_i|/d_i<=sigma*|E_i|/d_i+2h`, and since the triggering sigma is
less than one-half, `|E_i|/d_i<=4h` is invariant from zero. The slightly
sharper additive h and invariant 2h are also possible, but unnecessary.

The only response approximation is the primal neighbor term. The resulting
raw-density error is

    u_i/w_i=sigma*c*E_i/[theta*(1+theta)*d_i],

so `|u_i|<=2h*w_i/theta`. Hence the complete abstract parameters become

    kappa_raw=2h/theta, kappa_p=h, kappa_x<=10h.

The energy perturbation obeys

    Gamma<=27h/theta+4h<=29h/theta<tau/8

under h<=theta*tau/256. The raw density error is absorbed by the selected
margin because theta*kappa_raw=2h<=lambda/4 under the stated stage tolerance.
The general perturbed support theorem therefore gives `360K/r`.

Every scalar rebase remains explicitly charged over the exposed records,
but it need not inspect adjacency entries. Current-kinetic and baseline
neighbor sums must not be scaled, because their physical vectors do not
change at a primal rebase. The final PG-assisted repair must use the already
specified exact full-candidate gradient scan; reusing approximate primal L
there without an error term would change its certificate. That one terminal
scan is covered by the kinetic history.
