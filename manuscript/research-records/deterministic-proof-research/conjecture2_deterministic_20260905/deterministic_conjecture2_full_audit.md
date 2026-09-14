# Independent adversarial audit of the complete deterministic OP2 argument

Audited document: `deterministic_conjecture2_proof.md`, as read on
2026-09-05 after its dyadic-theta and repaired-final-output updates.
Only the authorized problem-definition manuscript and fresh current-task
artifacts were consulted. This audit does not use randomized checks.

## Verdict

The assembled mathematical argument passes this independent audit in its
explicit exact-real algebraic word model. I found no missing mathematical
invariant in the stage, stability, repair, final accuracy, or cumulative
local-work arguments. One minor theorem-scope correction is necessary:
the displayed `O_tilde(1/(rho sqrt(alpha)))` bound should be stated in the
OP2 nonzero regime `rho<1/d_seed`; the arbitrary-rho zero case costs O(1),
so a global statement needs `O_tilde(1+1/(rho sqrt(alpha)))`.

Section 9 benefits from the explicit key and update formulas below. They
supply the implementation detail behind its claimed common ordering and
show that its reporter can be implemented without rescanning old primal
coordinates. This is a clarification of a workable construction, rather
than an unidentified algorithmic oracle.

## 1. Source problem, coordinates, and model

The authorized problem definition explicitly restricts the substantive OP2
bound to `0<rho<1/d_seed` and allows additive objective tolerance epsilon.
In that regime `rho<1`, so all additive O(1), parameter-halving, and
stage-bookkeeping costs fit the claimed bound. The graph is connected and
has original degrees at least one; this assumption is used materially in
both the repair and the support-to-word count.

For x>=0, the absolute-value objective equals its displayed quadratic plus
linear term. The correction objective is valid even though the baseline
plus an intermediate correction can have mass greater than one: no such
mass constraint is imposed by RPPR. The correction cap itself contains both
the true correction and the analytical comparator.

Using degree densities makes all arithmetic rational for rational inputs.
Choosing theta by halving makes its square rational as well. Radical-form
outputs `f_i sqrt(d_i)` are sufficient to represent the requested x. The
proof expressly excludes bit-complexity and floating-stability claims;
there is no hidden assertion that these exact words have bounded bit size.

## 2. Obstacle and support facts

The stated Stieltjes KKT facts are consistent with the original objective.
In particular, at an inactive coordinate `Qx*<=0<=b`, while at an active
coordinate `Qx*=b-alpha*rho*w`; hence
`0<=b-Qx*<=alpha*rho*w` globally.

The half-rho margin is valid: outside `supp(x*_(rho/2))`, both relevant
coordinates vanish; decreasing other entries increases that coordinate of
Qx because the off-diagonals are nonpositive. This is the direction needed
for the exterior slack lower bound `alpha*rho*w/2`.

The degree-normalized matrix has absolute row sum exactly one. Thus a
uniform density error produces a uniform density response bound, even at
an arbitrarily high-degree inactive boundary vertex.

## 3. Baseline and analytical comparator

The invariant `bar<=x*_r`, `0<=s=b-Qbar<=4alpha*r*w` implies
`m_s=alpha*(1-mass(bar))` in [0,alpha]. Inverse positivity gives
`t=Q^-1 s<=4r w`, and its mass is at most one. The true correction
`e*=x*_r-bar` is nonnegative and at most t, so both belong to the explicit
box/cap. The algorithm never needs their values or supports.

Computing s touches only the baseline support and its one-hop neighbors.
The number of these records is bounded by the baseline degree volume;
it is not necessary to scan those neighbors' own adjacency lists.

## 4. Dyadic theta is valid with unchanged constants

Starting theta at 1/2 and halving until `theta²<=alpha` gives
`alpha/4<mu=theta²<=alpha` for every `0<alpha<1`. Thus the number of
iterations loses at most a factor of two relative to `1/sqrt(alpha)`.
Both objectives used in the proof are mu-strongly convex and one-smooth
in their respective metrics.

For a general Hilbert metric and comparator t, the accelerated comparison
calculation is exact. Put `g=grad f(y)` and
`raw=a z+theta y-g/theta`. Combining smoothness with the single-comparator
sector inequality gives

    f(xplus)+mu/2||p-t||²
      <= f(y)+mu/2||a(z-t)+theta(y-t)||²
                     -theta<g,a(z-t)+theta(y-t)>.

Strong convexity at x and t, weighted by a and theta, then gives the
remainder

    -mu*a*(theta²+theta)/2 ||z-y||²
      =-mu*theta*(1-mu)/2 ||z-y||².

This proves both stage convergence and the second comparison contraction.
Optimality of t is not used in this calculation.

The ordinary stage's initial energy is at most `||e*||²<=1`: the
correction has mass at most one, and w_i>=1. Thus the scalar stopping
certificate `a^k<=tau` requires no unknown objective or norm evaluation.

## 5. The non-Euclidean sector and second energy

All three projection-normal contributions have the claimed sign:

- A lower normal is nonpositive, while `Qp-s<=0` there.
- An upper normal is nonnegative, while `Qp-s>=4alpha*r*w-s>=0` there.
- An active mass normal has contribution `eta*(alpha-m_s)>=0`.

This is only a sector inequality at the particular t. It does not invoke
the false general nonexpansiveness of Euclidean clipping in Q norm.

The auxiliary function's Q-gradient is precisely `Qxi-s+lambda*w` because
`Q^-1 w=w/alpha`. The initial comparison energy is bounded by
`3lambda*m_s` even when mu is strictly smaller than alpha. A negative
comparison energy creates no reversal of an inequality: its upper bound
still yields `A(xi_k)<=4lambda*m_s`.

The global response estimate, including inactive coordinates, is therefore
`||Q(xi_k-e*)||²<=18alpha²r`. Its derivation does not require active-face
commutation or a safe intermediate xi.

## 6. Raw identity and support accounting with mu<alpha

The raw update in mass variables has V coefficient

    a I-(Q_mass-mu I)/(1+theta)
      =c/(1+theta)*(I+P)
      =beta0*K0,

where `beta0=(1-alpha)/(1+theta)<=a`. Thus the displayed identity (18)
is correct: no extra diagonal V term is missing.

The forcing is
`H=-D^(1/2)(Q-mu I)(xi-e*)/(1+theta)`. Since Q and Q-mu I commute and
`0<=Q-mu I<=Q`, its squared sum is bounded by the global Q-response bound.
The selected signed-flow argument drops only nonnegative quantities,
including upper-box normals, cap normals, killed transported mass, and
terminal kinetic excess. Cauchy's inequality applies to the selected
space-time indices; their volume is at most `Dout+2K/r`.

The scalar quadratic bound then gives

    total kinetic degree volume <=148K/r.

This counts repeated scans and also bounds the degree volume of the union
of emitted supports. It does not merely count newly discovered vertices.

## 7. Repair and final objective guarantee

The new tolerance `tau=alpha³delta²/2` implies Euclidean error at most
`eta=alpha*delta`. For `bar_new=[tilde-delta*w]+`, delta>=eta gives
`bar_new<=x*_r`. At positive repaired coordinates, clipping other entries
upwards can only decrease the current Q coordinate; therefore

    Qbar_new <= Qtilde-alpha*delta*w <= Qx*_r <= b.

At zero coordinates the source sign follows directly from Stieltjes
signs. This establishes exact source nonnegativity without requiring any
minimum support margin.

The repaired density error is at most `2delta`; the absolute row-sum
bound gives `s_new<=alpha*r*w+2delta*w`. The condition
`delta<=alpha*r/2` therefore gives `s_new<=2alpha*r*w`, sufficient for
all next-stage ratios in [1/2,1].

The repaired error is supported inside the true positive support. Its
linear KKT term consequently vanishes, and

    F_r(bar_new)-F_r(x*_r)
       =||bar_new-x*_r||_Q²/2 <=2delta²/r.

Hence the final halving rule `delta²<=epsilon*rho/2` proves the requested
accuracy, safe containment, and volume bound simultaneously.

## 8. Complete schedule and cost of materialization

The initial zero optimum at `r0=1/d_seed` is exact. At the first positive
stage, `r1>=r0/2` makes its source b satisfy the invariant directly.
Every subsequent threshold ratio is at most two. Each intermediate stage
uses a tolerance at most `alpha^5 r²/8<1`, so the stage stopping logarithm
is positive. Additional final halvings contribute only logarithmic
parameter dependence.

The final partial halving changes `sum_j 1/r_j=O(1/rho)` by only a
constant. Stage count, parameter setup, and scalar-bound maintenance fit
inside the same allowed polylogarithmic factors.

Final materialization scans the old baseline plus the union of emitted
correction coordinates once. Every positive correction coordinate was
emitted at least once because the primal update is a positive convex
combination from zero. The repair discards zeros coordinatewise and the
new source is built by scanning the repaired support. Each operation is
paid by the previous baseline or the current cumulative emitted volume;
there is no terminal full-graph traversal.

## 9. Explicit reporter construction

The following formulas make the common-key claim concrete. Write

    xi=sigma*X,  R=(Q-mu I)xi/sigma,  Tz=(Q-mu I)z,
    sigma=a^k.

For each exposed vertex use

    key_i = -R_i/[theta(1+theta)w_i]
      + [a z_i/w_i-Tz_i/((1+theta)w_i)+s_i/(theta*w_i)]/sigma.

Then exactly

    zraw_i/w_i = sigma*key_i-lambda/theta.

The bracket is a sparse exception supported on z, its exposed neighbors,
and s. Its list can be removed and reinstalled as sigma changes; the
unexceptional base ordering does not change. Ordinary primal averaging
updates X only on emitted coordinates and updates R by one charged scan
of those coordinates. In degree coordinates all these formulas are
rational, with `R_i/w_i` stored directly if desired.

For cap multiplier eta, set `q=(lambda/theta+eta)/sigma` and `U=4r`.
The projected mass is

    sigma*[Tail(q)-Tail(q+U/sigma)],
    Tail(t)=sum_i d_i*(key_i-t)_+.

Each Tail query uses a degree-weighted subtree aggregate in logarithmic
time. The only breakpoints are the two translates of the ordered key
set. Rank selection in their implicit merge takes O(log²N) using subtree
cardinalities and ordered selections; an outer binary search over ranks
therefore takes O(log³N). The final affine equation is solved exactly.
Flat intervals and duplicate breakpoints do not affect the unique
projected vector. Include eta>=0 explicitly by testing its mass first.

Only keys strictly above q are enumerated. They are precisely the nonzero
projected support, including saturated coordinates. Rejected positive-raw
candidates are not scanned. Dictionary access can also be deterministic,
using a separate balanced tree keyed by vertex labels.

## 10. Omitted-node and retained-state logic

Before a stage, every baseline source neighbor is exposed. During a stage,
each emitted coordinate's adjacency list is scanned when its response is
added. Therefore any vertex not yet exposed has no neighbor in the baseline
support or in any historically emitted correction support. Its source,
primal state, kinetic state, and response are all zero, giving strictly
negative raw value `-lambda*w_i/theta`. Its unknown degree need not be
queried to establish this sign. Neither the cap nor the upper box can make
such a raw value positive.

On first exposure, its previous primal/response state is thus zero; the
newly scanned contribution is added immediately. Every record and every
retained adjacency entry arises from a charged source scan or kinetic
scan. Clearing obsolete records between stages is bounded by the same
record history. No hidden dependence on the degree sum of inactive source
neighbors, global n, or total edge count is introduced.

## Remaining scope

This audit validates the exact-word mathematical construction. Production
floating arithmetic, reliable comparisons under rounding, bit complexity,
and empirical constants remain separate engineering questions. They do
not follow from the exact arithmetic proof or from the existing finite
Fraction diagnostics.
