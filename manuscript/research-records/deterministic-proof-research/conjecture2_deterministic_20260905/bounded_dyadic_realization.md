# A bounded dyadic realization of the deterministic local algorithm

This is a fresh extension of the proved exact-word algorithm. It is being
independently audited. It uses exact bounded rational arithmetic and
explicit downward rounding; it is not a claim about unchecked floating
point. No randomized procedure, trial, or numerical primitive is used.

The central perturbed comparison argument is recorded separately in
the fresh finite-precision notes. This note realizes its hypotheses using
local state whose coefficients do not grow with the iteration history.

## 1. Abstract interface and parameters

At one stage let r<1, lambda=alpha*r, U=4r, and let the safe baseline have
source s=b-Q*bar in [0,4lambda*w]. Choose theta by halving from 1/2 as in
the main algorithm, so theta is an inverse power of two, mu=theta^2<=alpha,
alpha<4mu, and a=1-theta. All vector inequalities below are coordinatewise.

The perturbed stage permits

    p0 = Proj_K(raw),
    p = p0 + ep,
    xi_new = a*xi + theta*p + ex,

where raw is the exact ordinary accelerated raw point of the actual
stored xi and z, K is the box [0,U*w] intersected with mass at most one,
and p and xi_new remain feasible. The errors are downward:

    -kappa_p*w <= ep <= 0,   -kappa_x*w <= ex <= 0.

Both the original comparison energy E and the auxiliary Q-metric energy B
satisfy

    E_new <= a*E + zeta,    B_new <= a*B + zeta,
    zeta = (5/2)kappa_x + (5/2)(theta+mu)kappa_p.

Let Gamma=zeta/theta. Consequently the objective gap is at most
a^k*E0+Gamma, and the actual trajectory satisfies

    ||Q(xi-e*)||^2 <= 18alpha^2*r + 4Gamma.

Downward kinetic rounding only helps the selected signed-flow inequality.
If Gamma<=alpha^2*r, the unchanged Cauchy argument gives

    sum_k vol(supp z_(k+1)) <= 180K/r.

The constant is 8*22+4: the response bound is at most 22alpha^2*r.
No exact or approximate true support is an input to these statements.

For a desired stage gap 0<tau<=alpha^2*r<1, choose a power-of-two grid h satisfying

    0<h<=min(1/8, theta*tau/256).

The realization below has kappa_p=h and kappa_x<=10h. Therefore

    Gamma <= 27h/theta <= 27tau/256 < tau/8.

Run K=m*q iterations, where m=1/theta is an integer and q is the smallest
integer with 2^q>=2/tau. Since (1-theta)^m<=exp(-1)<1/2,
a^K<=tau/2. Thus the actual stored primal gap is strictly below tau.
This iteration schedule uses only doubling and integer arithmetic, and
requires no growing exact power a^K, logarithm oracle, or square root.

## 2. State and exact local response

Use degree densities and store xi_i/w_i=sigma*X_i. Store sigma, X, and the
kinetic density z_i/w_i as multiples of h. At the start of an iteration,
1/2<=sigma<=1. All nonzero records are stored sparsely.

Instead of accumulating rational response coefficients, maintain the exact
neighbor sum

    L_i = sum_{j adjacent to i} X_j.

Each X_j is dyadic, so every L_i has the same dyadic denominator.
Changing X_j by a dyadic increment updates L_i at each neighbor using
integer addition. Only the changed support is scanned. The response is
then recovered exactly by

    (D^(-1/2)(Q-mu I)D^(1/2)X)_i
       = (q0-mu)*X_i - c*L_i/d_i,
    q0=(1+alpha)/2, c=(1-alpha)/2.

Maintain analogous neighbor sums for the current dyadic kinetic density.
The baseline is also dyadic; its source density is computed exactly as

    s_i/w_i = alpha*1_{i=seed}/d_i
              -q0*bar_i/w_i
              +(c/d_i)*sum_{j adjacent to i} bar_j/w_j.

In particular, multiplication by d_i cancels the only vertex-dependent
denominator in each response and source value. No approximate accumulated
gradient and no recursively compounded response error are present.

The exact same lazy raw-key formula as in the main proof therefore gives
the raw point for the actual represented xi and z. A dyadic sigma changes
the representation, but does not change the validity of that algebra.

## 3. A local rounded iteration

1. Use the exact ordered reporter to find the box/mass multiplier for raw.
   The ideal projection p0 is analytical until a coordinate is emitted.
2. Emit only coordinates with projected density at least h. For each one
   store p_i/w_i = floor_h(p0_i/w_i), where floor_h rounds down to a
   nonnegative multiple of h. Coordinates below h remain unmaterialized.
3. Remove the old sparse key exceptions. Set

       sigma_new = floor_h(a*sigma).

   For each emitted coordinate replace

       X_i <- floor_h(X_i + theta*(p_i/w_i)/sigma_new).

   The actual dyadic change in X_i, rather than its unrounded intended
   increment, is scattered to the exact neighbor sums.
4. If sigma_new<1/2, perform the rebase described below. Install the current
   kinetic/source key exceptions using the resulting scale.

The scale is always positive: a*sigma>=1/4 and h<=1/8 imply
sigma_new>=1/8. Because X_i<=2U at the start of the iteration, replacing
a*sigma by sigma_new causes a downward density error less than 2U*h.
Flooring the selected X increments contributes at most h because
sigma_new<=1. A rebase contributes at most one more h. Thus

    0 <= a*xi + theta*p - xi_new <= (2U+2)h*w <=10h*w.

Both perturbations are downward. Therefore p remains inside K, and so does
xi_new, since a+theta=1. This proves the abstract perturbation interface.

There is an essential reporter detail: enumerating all positive p0 and
then discarding sub-grid values would introduce an uncharged repeated
scan. Instead, if the raw density is sigma*K_i-shift and the exact mass
multiplier is eta, enumerate the CLOSED tail

    K_i >= (shift+eta+h)/sigma.

Those are exactly the coordinates with positive stored p. Ties at h must
be included. Since the prescribed h is smaller than U, upper clipping
does not invalidate this condition. The omitted sub-grid projection
entries need no reads, writes, or adjacency access.

## 4. Rebasing and its full charge

When sigma_new<1/2, replace every stored X_i by floor_h(sigma_new*X_i),
set sigma=1, and rebuild the exact neighbor sums and base keys. This adds
a downward density error of at most h, already included above.

The rebuild may scan the entire historical primal support once. That
volume is at most the previously emitted kinetic volume; it is not treated
as a free scalar-only operation. All neighbor sums, exposed records, and
base-key replacements are charged as well.

Each scale interval starts at one. A step decreases sigma by at most
theta+h. Crossing below 1/2 therefore requires at least
1/[2(theta+h)] steps. Since h<=theta, there are at most
4theta*K+1 rebases, which is O(1+log(1/tau)).

Writing B=sum_k vol(supp z_k), all rebases together cost

    O((theta*K+1)*(B+baseline_volume+1)*polylog(N+2)).

The proved B<=180K/r thus makes this only another allowed logarithmic
factor over the target local work. Repeated adjacency inspections remain
charged, including cached-list reads.

## 5. Why the exact rational temporaries have bounded bit length

Assume the numerical input alpha and r is rational; degree and vertex
labels are integers. Rational temporaries are reduced after arithmetic,
or represented with an explicitly shared denominator. Let h=2^-Bprec.
Across continuation stages choose nested nonincreasing grids, so the new
grid also represents every old baseline density exactly. The tolerance
schedule naturally permits this choice. The current dyadic scale is S*2^-Bprec
with 1<=S<=2^Bprec. Normalized X densities are bounded by 32 and kinetic
densities by four, so stored dyadic numerators need O(Bprec) bits beyond a
fixed constant. Neighbor sums add at most log(N+2) bits.

Let W_i=d_i*K_i be the weighted raw key. Its formula is

    W_i = -[(q0-mu)*d_i*X_i-c*L_i]/[theta*(1+theta)]
          + {a*d_i*z_i
             -[(q0-mu)*d_i*z_i-c*M_i]/(1+theta)
             +(d_i*s_i/w_i)/theta}/sigma.

Here z_i denotes its degree density and M_i its neighbor sum. Every term
in W_i has a denominator dividing one COMMON quantity formed from the
input parameter denominators, powers of two, theta*(1+theta), and the
current scale numerator S. Its logarithm is

    O(input_parameter_bits + Bprec + log(1/theta)).

The vertex degree does not occur in this denominator. Therefore all
weighted AVL subtree moments sum numbers with a common bounded denominator.
They do not form an LCM of vertex degrees. The node ordering still compares
K_i=W_i/d_i, whose extra degree denominator has only log d_i bits.

More explicitly, write alpha=A/Balpha, theta=1/T, h=1/H, sigma=S/H,
and every dyadic density and neighbor sum as an integer over H. Each
weighted key has denominator dividing

    2*Balpha*H*T*(T+1)*S.

The physical weighted raw values sigma*W_i cancel S. Their common
denominator divides 2*Balpha*H^2*T*(T+1), with the denominator of the
stage regularization included for the common shift. This formula was
derived independently in the arithmetic audit.

During an update, remove every old exception before installing any new one.
While old exceptions are being removed there is only the old common scale
denominator. After removal all keys are base keys. While new exceptions
are installed there is only the new denominator. Rebasing changes dyadic
base states, whose denominator remains a fixed power of two.

On an affine box-projection interval the exact multiplier is

    eta = (sum_{free i} d_i*raw_i
           +U*sum_{upper i}d_i -1)/sum_{free i}d_i.

This adds only the bit length of a degree sum. The exact projected
coordinates are immediately rounded down to the dyadic grid, so that
division's denominator never enters the next stored vector. All binary
tree root searches use exact rank and comparison operations, with no
breakpoint-margin search.

Consequently each stored number and arithmetic temporary has bit length
bounded by a polynomial logarithmic expression in input encoding lengths,
inverse numerical parameters, inverse target accuracy, exposed record
count, and maximum exposed degree. It has no linear dependence on the
number of iterations from retaining an exact product history.

This is a stronger bounded-coefficient implementation claim than the
original Fraction prototype. It is not a bit model independent of the
length needed to encode a graph label or a very large degree.

## 6. Completing a safe rounded continuation

At a stage choose delta<=alpha*r/2 as in the main proof, with
2delta^2/r<=epsilon at the final stage. Use the slightly conservative
PG-assisted tolerance

    tau = alpha*delta^2/8.

After the certified rounded accelerated stage, form the exact one-step
projected-gradient point y from the actual full candidate. It satisfies
gap(y)<=tau and ||y-x*_r||<=delta/2. Its valid subgradient is
(I-Q)(x-y), of norm at most sqrt(2tau)<=delta/2.

On positive coordinates this gives Qy-b<=-lambda*w+(delta/2)*w.
Form

    bar_new_i/w_i = floor_h([y_i/w_i-delta]_+).

Because h<=delta/2, the result is below x*_r and
0<=x*_r-bar_new<=2delta*w. On a positive retained coordinate, clipping
subtracts at least alpha*delta*w from Qy and grid rounding can increase
Q by at most h*w. Since h<=lambda/4 and delta<=lambda/2, this still gives
Q*bar_new<=b. At zero coordinates Stieltjes signs give the same inequality.
The source is therefore in [0,2lambda*w], ready for the next factor-two
stage, and the final objective gap is at most 2delta^2/r.

The inequalities h<=delta/2 and h<=lambda/4 follow from
h<=theta*tau/256 with this tau, alpha<=1, theta<=1/2, delta<=lambda/2,
and r<1. They may also be imposed explicitly in the grid-selection loop.

Compute the PG response by scanning only the materialized old candidate.
Evaluate each affected density and truncate immediately; do not scan a
newly positive PG neighbor before truncation. Thus this repair has the
same fully charged locality as the separately tested exact PG wrapper.

## 7. Status and implementation obligations

The abstract perturbation lemma, exact-rational denominator accounting,
closed-tail reporter, and rebase charge are being independently audited.
Before claiming a practical implementation, an implementation must verify:

- closed-tail handling of projection/grid ties;
- exact neighbor-sum updates from actual rounded X changes;
- correct old-exception removal before scale transitions;
- rebase rebuilding and charging of every old-support adjacency entry;
- exact or certified floor operations and final safe repair;
- measured coefficient sizes across the entire continuation.

The original exact-real theorem remains unchanged while this stronger
realization is tested.

## 8. Optional scalar-only rebase with a certified response error

There is a more practical rebase that avoids rereading historical
adjacency lists. Keep the same dyadic X state and local exact scattered
increments, but at a rebase do the following independent scalar updates:

    X_i <- floor_h(sigma*X_i),
    L_i <- floor_h(sigma*L_i),
    sigma <- 1.

Use the OLD values for both updates. Do not scatter the X rebase
differences into L, since that would double-count the transformation.
The current-z and fixed-baseline neighbor sums remain exact and unchanged.
Rebuild all base keys and sparse exceptions from the resulting state.

Now L approximates the actual primal neighbor sum. Let

    E_i = L_i - sum_{j adjacent i} X_j.

Between rebases, scattering the actual dyadic increments preserves E
exactly. At a rebase, writing the nonnegative individual floor losses as
r_j<h and r_L<h gives

    E_i_new = sigma*E_i + sum_{j adjacent i}r_j-r_L.

Because sigma<1/2 at a rebase and d_i>=1,

    |E_i_new|/d_i <= sigma*|E_i|/d_i+2h.

Starting from zero therefore gives |E_i|/d_i<=4h at every iteration.
This estimate does not multiply by the number or volume of unexposed
vertices. The primal raw-response density error is consequently at most

    kappa_raw = 2h/theta.

The exact local projection is now the projection of a raw point with that
uniform density error. All other rounding bounds are unchanged. The full
perturbed comparison theorem gives

    Gamma <=29h/theta < tau/8

under the same h<=theta*tau/256. Since theta*kappa_raw=2h<=lambda/4,
the perturbed selected-flow ledger yields

    sum_k vol(supp z_(k+1)) <=360K/r.

The rebase still visits and updates every exposed state/key record, and
these scalar/tree operations are fully charged. It performs no adjacency
scan. The number of rebases is unchanged. Its stored numbers remain dyadic,
and the common-denominator arithmetic argument remains valid for an
approximate L just as for an exact neighbor sum.

The final PG repair must compute its exact response from the actual full
candidate by the already charged one-time support scan. It must not reuse
the approximate L as an exact terminal response.

This variant has an independent mathematical audit. It is a separate
implementation option; passing tests of exact-sum rebasing do not by
themselves verify its approximate-response state management.
