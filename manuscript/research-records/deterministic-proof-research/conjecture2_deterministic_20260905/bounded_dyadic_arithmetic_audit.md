# Independent audit of the bounded dyadic realization

This audit concerns the fresh `bounded_dyadic_realization.md`, principally
its exact-sum realization in Sections 1–6. It also checks the arithmetic
changes in the optional approximate-sum rebase of Section 8. No other
manuscript notes or old research directions were consulted. This is an
audit of the mathematical realization, not a report that a particular
implementation has passed its tests.

## Verdict and scope

I found no denominator-growth, closed-tail, or rounded-continuation defect
in the current version. The exact-sum realization has a bounded rational
implementation under its stated rational-input assumptions. In
particular, summing weighted keys does not form an LCM of vertex degrees,
and neither projection multipliers nor products of past scales survive
in the next stored vectors. The optional scalar-only rebase has the same
bounded-coefficient property.

The following conditions are essential, not merely optimizations:

1. Theta is the reciprocal of a power of two chosen as in the main
   theorem. It is not an arbitrary number in `(0,1/2]` for purposes of
   the integer iteration schedule.
2. Grids are nested across continuation stages, or their precision is
   enlarged to represent the preceding baseline exactly.
3. Rational moments are reduced, or kept over a common denominator.
   A naive unreduced expression history is not covered.
4. All old sparse exceptions are removed before new-scale exceptions are
   inserted, and a rebase refreshes every exposed base-key record.
5. Emission uses a closed threshold at the first positive grid point.
   Enumerating all positive ideal entries first would not have the
   proved work charge.
6. The terminal projected-gradient response is formed from the actual
   stored candidate. In the scalar-only rebase variant, its approximate
   response ledger is not an exact terminal certificate.

These conditions are now explicit in the proposal. Rational alpha and
regularization are needed for this bounded-bit extension; arbitrary
exact-real inputs remain covered by the original exact-word theorem.
The input encoding of a rational requested tolerance must likewise be
included in the bit accounting. The claim is not independent of the
bits needed to name a vertex or return its degree.

## 1. Exact stored state and the rounding interface

Write the correction density as `xi_i/w_i = sigma X_i`. At iteration
start, `1/2 <= sigma <= 1` and feasibility implies `X_i <= 2U`. Both
`X_i` and the next kinetic density `p_i/w_i` are nonnegative grid
multiples.

Let `sigma' = floor_h(a sigma)`. Since `a >= 1/2`,
`a sigma >= 1/4`; hence `sigma' >= 1/8` under the stated grid bound.
Replacing the scale incurs a downward density loss less than `2U h`.
At an emitted coordinate the update

    X_i' = floor_h(X_i + theta (p_i/w_i)/sigma')

incurs a further physical density loss below `sigma' h <= h`. At a
nonemitted coordinate, `p_i=0` and this second loss is zero. The new
`X_i` cannot be smaller than the old `X_i` before a rebase, because the
old value was already on the grid. Thus scattering the actual stored
increment maintains the exact neighbor sums.

A rebase adds at most `h` more downward density loss. Consequently the
actual stored update satisfies

    0 <= a xi + theta p - xi_new <= (2U+2)h w <= 10h w.

It remains nonnegative and lies below a convex combination of two feasible
states, so both the box and mass constraints survive. Even before a
rebase, feasibility and `sigma' >= 1/8` give `X_i <= 8U <= 32`.
After the rebase or at the next ordinary iteration start the stronger
`X_i <= 2U` invariant is restored.

The abstract perturbation theorem then applies with
`kappa_p=h`, `kappa_x=10h`, and `kappa_raw=0`. Its energy floor is

    Gamma <= [25/theta + (5/2)(1+theta)]h <= 27h/theta.

Thus `h <= theta tau/256` gives `Gamma < tau/8`. The selected-flow
bound is unchanged by downward kinetic rounding: its adverse raw error
is zero. With the perturbed response estimate at most
`22 alpha^2 r`, the exact-raw ledger gives `180K/r`, as asserted.

No sum of a uniform error over the whole unknown graph is used here.
The energy estimates use the mass lost from a feasible nonnegative
state, which is at most one. Ideal projection coordinates discarded
below the grid therefore need not be materialized to justify the
perturbation bound.

## 2. Closed-tail emission

For an exposed record let its ideal projected density be

    p0_i/w_i = min(U, max(0, sigma K_i - shift - eta)).

For `0 < h <= U`, its rounded density is positive if and only if

    sigma K_i - shift - eta >= h.

Equivalently, the reporter must enumerate the closed tail

    K_i >= (shift + eta + h)/sigma.

Equality is a retained positive grid entry; a strict tail would be
incorrect. Conversely every emitted coordinate has rounded kinetic
density at least `h`, so its adjacency access is charged to actual
stored kinetic volume. Entries with ideal density in `(0,h)` require
neither enumeration nor adjacency scans.

The exact waterfill mass must still be evaluated before this rounding.
Replacing it by the mass of the rounded entries would define a different
projection and is not justified by this interface. Weighted subtree
moments permit that exact evaluation without enumerating its ideal
positive support.

For a flat waterfill interval with no free coordinates, there is no
division by a zero free-degree sum: the exact breakpoint/equality case
returns a valid multiplier. Once a positive-slope affine interval is
selected, its free-degree sum is positive and the displayed affine root
formula applies. Exact rank searches and breakpoint comparisons avoid
any iteration count depending on a tiny gap between breakpoints.

## 3. Explicit common denominator calculation

The following derivation sharpens, and in particular implies, the common
denominator bound in the proposal. Put

    alpha = A/D, theta = 1/T, h = 1/H, sigma = S/H,

where `T` and `H` are powers of two. All stored densities and neighbor
sums have denominator `H`. Write them as

    X_i = x_i/H, z_i/w_i = v_i/H, bar_i/w_i = beta_i/H,
    L_i = ell_i/H, M_i = m_i/H, Lbar_i = n_i/H.

Here all lower-case numerators are integers. Set

    P = (D+A)T^2 - 2D,
    F_i = 2 A H 1_{i=seed} - (D+A)d_i beta_i + (D-A)n_i,
    B_i = P d_i x_i - (D-A)T^2 ell_i.

Then

    d_i s_i/w_i = F_i/(2 D H),

and the weighted base key is exactly

    Wbase_i = -B_i/[2 D H (T+1)].

The kinetic exception simplifies before any denominator accounting:

    a z - (Q-mu I)z/(1+theta)
       = c (I + D^(-1/2) A_graph D^(-1/2))z/(1+theta).

In degree densities this yields, with

    E_i = T[(D-A)(d_i v_i + m_i) + (T+1)F_i],

the exact weighted exception

    Wexc_i = E_i/[2 D (T+1) S].

Consequently every full weighted key `W_i=d_i K_i` has denominator
dividing the single integer

    D_key = 2 D H (T+1) S,

and can be written

    W_i = [-B_i S + E_i H]/D_key.

There is no vertex degree in this denominator. The proposal's displayed
bound with an additional factor `T` is therefore conservative but valid.
Integer sums of such weighted keys require only the same denominator
and an additional logarithmic number of numerator bits.

The degree affects an individual ordering key only through `K_i=W_i/d_i`.
Comparing two ordering keys needs cross multiplication by the two
degrees, not an LCM of all degrees in a subtree. This costs a bounded
number of integers with an additional `O(log d_max)` bits.

Moreover the physical weighted raw values cancel the scale numerator:

    sigma W_i = -B_i S/[2 D H^2(T+1)]
                 + E_i/[2 D H(T+1)].

Including the common shift `alpha r/theta`, a common denominator for
the physical weighted raw values divides

    D_raw = 2 D H^2 (T+1) den(r).

The scale numerator `S` has disappeared entirely from this denominator.
Again the proposal's extra factor `T` is harmless.

On a nonflat affine interval the exact projection multiplier is

    eta = [sum_free d_i raw_i + U sum_upper d_i - 1]
          / sum_free d_i.

The extra denominator is a positive integer at most `N d_max`. It adds
only `O(log N + log d_max)` bits. An exact projected coordinate can add
its own degree factor, but it is immediately rounded onto the dyadic
grid. Neither the free-degree sum nor any local degree denominator is
propagated into the next kinetic vector.

This argument requires exact cancellation when the data structure forms
its weighted moments. Keeping reduced rationals or explicitly storing
the common denominator achieves this. A representation that retains
unreduced products from every arithmetic operation would not establish
the stated bound even though its denoted rational value is bounded.

## 4. Updates cannot accumulate scale history

The key dependence on the scale occurs only in the sparse exception.
Removing all old exceptions before changing scale leaves only base keys,
whose denominator is independent of `S`. Inserting the new exceptions
introduces only the new `S`. During removal or insertion there is a
common denominator containing just the corresponding scale, and while
the base states are being updated their denominator remains fixed.

There is also a direct integer implementation of each stored update.
If `S'` is the new scale numerator and `p_i/w_i = p_i_int/H`, then

    S' = floor((T-1)S/T),
    x_i' = x_i + floor(H p_i_int/(T S')),

and a rebase replaces `x_i` by

    floor(S' x_i/H).

These are bounded integer divisions and additions. No product of the
previous values of `S` is retained. A rational temporary for the exact
projection need exist only long enough to perform its grid floor.

The current grid must exactly represent the prior baseline. Choosing
nested nonincreasing grids does this because every old dyadic grid
divides every finer one. The proposed stage-tolerance schedule permits
this choice: the regularization decreases, and the final requested
repair radius is halved only in the direction of increasing precision.
Equivalently one may set the new precision to the maximum of the old
precision and the newly required precision.

Neighbor sums consist of at most `N` nonzero stored densities, each
bounded by 32. They therefore use `O(Bprec+log(N+2))` bits. Factors
`d_i X_i` and the exact seed density add degree-encoding bits. The stage
regularizations and repair radii are rational products of the original
inputs and dyadic factors; their denominators do not grow by a new
unrelated factor at every stage.

## 5. Rebase work and exposed records

Starting at scale one, each step lowers the scale by at most `theta+h`.
Crossing below one half takes at least `1/[2(theta+h)]` steps. With
`h<=theta`, there are at most `4theta K+1` rebases, which is logarithmic
in the inverse stage tolerance for the prescribed iteration count.

In an exact-sum rebase, rounding each `X_i` can change the order of base
keys. Thus keys cannot merely be rescaled globally. All exposed sums and
keys are refreshed; adjacency entries of the historical primal support
are scanned and charged. Every nonzero historical correction coordinate
was created by a prior kinetic emission. Hence its degree volume is at
most the accumulated emitted kinetic volume. Zeroed historical records
can be retained and visited, with their number bounded by the same
exposure charge.

The resulting rebuild cost is a logarithmic multiple of previously
charged local work. It is not a zero-cost mass rescaling. No adjacency
list of an inactive high-degree boundary record is required merely to
refresh that record's scalar response or its ordered key.

## 6. Terminal PG repair and safe continuation

Let the actual full candidate have objective gap at most
`tau=alpha delta^2/8`, where `delta<=lambda/2`. Its exact projected-
gradient point `y` has no larger gap, so strong convexity gives

    ||y-x*||_2 <= delta/2.

With `Delta=x-y`, the vector `(I-Q)Delta` is a valid subgradient at `y`.
The unit-step descent inequality gives `||Delta|| <= sqrt(2tau)`, and
therefore its subgradient norm is at most `sqrt(2tau)<=delta/2`.
At a positive coordinate of `y`,

    (Qy-b)_i <= -lambda w_i + (delta/2)w_i,

using `d_i>=1` to turn an absolute coordinate bound into the displayed
density bound.

Set `t=[y-delta w]_+`, and round its density down by at most `h` to obtain
the new baseline. The position bound and `h<=delta/2` give

    0 <= x* - bar_new <= (delta/2+delta+h)w <= 2delta w.

In particular `bar_new<=x*`. On a retained positive coordinate, the
clipping vector equals `delta w` at that coordinate and is at most
`delta w` elsewhere. Stieltjes signs therefore give

    Qt <= Qy - alpha delta w.

The final downward density rounding can increase that coordinate of Q
by at most `h w` (the sharper estimate is `c h w`). Hence

    Qbar_new-b <= [-lambda + delta/2 - alpha delta + h]w <= 0

under the stated `delta<=lambda/2`, `h<=lambda/4`. At a zero coordinate,
`Qbar_new<=0<=b` directly. This verifies safety without an activation-
margin assumption.

The optimum source is between zero and `lambda w`; since
`|Q(x*-bar_new)|<=2delta w`, the new source lies between zero and
`2lambda w`. The support is contained in the optimum support, and has
volume at most `1/r`. Complementarity removes the linear objective term
on that support, giving final gap at most `2delta^2/r`.

The parameter inequalities used above follow from the prescribed grid;
imposing them explicitly is also harmless. The end-stage projected-
gradient calculation scans only the materialized candidate support and
evaluates its affected neighbors. Newly positive ideal PG neighbors
are clipped and rounded before any of their adjacency lists are scanned.
Only retained safe output coordinates can require further adjacency
exposure. Unexposed coordinates with zero candidate and no nonzero
neighbor have zero PG output and need no visit.

## 7. Optional approximate-sum rebase

For the Section 8 variant let
`E_i=L_i-sum_adj X_j`. Between rebases, scattering the actual stored
increments preserves `E_i`. At a rebase the stated use of the old values
gives exactly

    E_i_new = sigma E_i + sum_adj floor_loss_j - floor_loss_L.

Here `sigma<1/2`, each loss is in `[0,h)`, and `d_i>=1`. The proposal's
conservative recurrence

    |E_i_new|/d_i <= sigma |E_i|/d_i + 2h

therefore yields `|E_i|/d_i<=4h` uniformly. Newly exposed records have
zero preexisting error: a nonzero primal neighbor would already have
exposed them. The raw density error is at most
`4c h/[theta(1+theta)] <= 2h/theta`.

This adds at most `4h` to the energy floor. With `theta<=1/2`, the
resulting floor is at most `29h/theta`, still below `tau/8` under the
same grid choice. The raw-error selected ledger now uses its perturbed
constant `360K/r`. The neighbor ledger remains dyadic despite being
approximate, so the common-denominator derivation is unchanged. The
one-time exact terminal PG response must not be replaced by this ledger.

## Practical conclusion

The bounded-dyadic construction removes the specific practical gap of
an exact Fraction trajectory retaining increasingly large products of
past scales. Its arithmetic is deterministic and margin independent.
It does not establish the accuracy of ordinary binary floating-point
code, nor remove the need to test exact root selection, closed ties,
stale exception removal, rounded scatter updates, and rebase rebuilding.
Those are implementation obligations rather than missing mathematical
steps in the current realization.
