# Independent audit of directed-rounding tree-to-cube verification

The current `capped_tree_cube_interval.py` gives valid enclosures for the
stated exact radial recurrence, including the stable-slope tightening and
component mass-cap intersections. One constructor bug was found and corrected
by the author during this audit: an explicit upper Fraction endpoint had been
ignored. No remaining certificate defect was found on the audited valid input
domain. This is a finite symmetry-reduced certificate, not a local algorithm
or an asymptotic support-work theorem.

## 1. Interval operations and constants

Each lower addition, multiplication, or division uses Decimal ROUND_FLOOR;
each upper operation uses ROUND_CEILING. Multiplication and division consider
all four endpoint pairs, with division rejecting a denominator containing zero.
Negation uses exact sign changes. Square correctly treats intervals spanning
zero. Positive-part and unit-clipping maps are monotone and are applied to both
endpoints. Decimal integer/Decimal endpoint construction is exact; Fraction
constants are separately divided downward and upward. The corrected two-Fraction
constructor now uses the explicit upper endpoint.

All analytical constants in the run come from integers or exact Fraction values:
theta=1/L, alpha=theta^2, c=(1-alpha)/2, and rho=gamma*L/cube_volume. Conversion
and subsequent arithmetic enclose the exact values. Dependency between these
constants may widen the interval but cannot invalidate containment. The nominal
ROUND_HALF_EVEN computation is used only to pick a scalar projection candidate;
no nominal result is accepted as a certificate without an outward residual.

The audited parameter domain is integer power-of-two L>=2, nonnegative integer
prefix/cube factors p,s, nonnegative integer horizon, positive precision, and
positive rational gamma. Projection requires nonempty arrays of matching
length, strictly positive integer weights, and a nonnegative cap. These are
satisfied by the graph construction and the tested calls. This review does not
assert special behavior for invalid arguments or concurrent changes to the
class-wide Decimal contexts.

## 2. Why the cap threshold enclosure is rigorous

For fixed exact raw aggregate masses r_i and weights w_i>0, define

    F(t)=sum_i [r_i-w_i*t]_+, t>=0.

The projection multiplier eta is zero if F(0)<=cap; otherwise it is the positive
root F(eta)=cap. For cap zero, use the smallest multiplier making F zero.
The code's sorted nominal computation supplies only a nonnegative candidate c.
An outward interval evaluation contains F(c)-cap for every exact raw vector and
cap represented by the input intervals.

If the certified lower endpoint of F(c) is positive, then F(c)>0 for every such
exact input. Wherever F is positive its decreasing slope has magnitude at least
m=min_i w_i. For eta>=c, integrate this slope from c to eta. For 0<eta<c,
integrate in the reverse direction. If eta=0 because the cap is inactive,
cap-F(c)>=F(0)-F(c), so the same estimate still holds. Consequently

    |eta-c| <= |F(c)-cap|/m.

The code rounds the residual absolute bound and division outward. Thus its
initial radius delta gives a genuine multiplier bracket.

For a class satisfying r_i.lo-(c+delta)*w_i>0 by a downward-rounded test, that
class remains positive for every threshold between c and every possible eta
in the current bracket. The slope throughout this segment is therefore at
least the sum Wstable of these weights. The improved bound

    |eta-c| <= residual_bound/Wstable

is valid on the same bracket. Taking the minimum with the old radius remains
valid, and repeating the argument three times is sound. The code forms the
upper threshold with upward rounding and performs the positivity test through
outward interval arithmetic, so no unstable class is mistakenly counted.

If F(c)>0 cannot be certified, the fallback

    0<=eta<=max(0,max_i r_i.hi/w_i)

is valid for every nonnegative cap. Positive-part evaluation of
r_i-[eta.lo,eta.hi]*w_i then encloses each projected mass. Ties, cap inactivity,
a zero cap, and thresholds exactly on a breakpoint are covered by these
arguments; exact active-set classification is not required.

## 3. The quotient graph and line search

For h=p*log2(L), m=s*log2(L), and width=2^h, the prefix has layer counts 2^j
for 0<=j<=h. Each prefix leaf connects to the zero vertex of its own m-cube.
Cube distance layer j has width*binom(m,j) vertices. The resulting aggregate
cube volume is exactly

    width*(m*2^m+1).

The anchor's extra degree is its prefix edge. Internal forward/backward
multiplicities satisfy count_j*right_j=count_(j+1)*left_(j+1), as checked in
the code. Their fractions by vertex degree are the exact column-stochastic
mass transition. Every class has constant degree and identical exact state by
rooted/cube automorphisms. A positive aggregate class mass therefore means
every vertex in that class is positive.

Let weight_j=count_j*degree_j and density_j=u_j/weight_j. The full-graph
quadratic energy on a radial vector is

    alpha*sum_j u_j^2/weight_j
      +c*sum_edges_between_layers edges_j*(density_j-density_(j+1))^2.

The implemented linear and curvature expressions are its exact line derivative
and second derivative, including the source term -alpha*u_0/degree_0 and the
regularization term lambda*sum u. The source class contains one vertex.
Direction Vplus-theta*u is precisely the segment from u to a*u+Vplus.
When curvature.lo>0, outward division followed by unit clipping encloses the
exact line fraction. Otherwise [0,1] encloses every valid minimizing fraction;
if exact curvature is zero, positive definiteness makes the direction zero,
so this fallback is harmless and includes the canonical choice zero.

The convex-form update avoids treating a movement with uncertain sign as an
independent negative mass. Intersecting each new u coordinate with [0,1] and
each V coordinate with [0,theta.hi] is valid: the exact iterates obey the global
caps sum u<=1 and sum V<=theta. The endpoint intersection cannot remove the
exact value. The assertions also reject an empty interval intersection.

## 4. What the work counts certify

A condition V_j.lo>0 certifies that the exact aggregate class mass is strictly
positive, hence its full integer degree volume belongs to the auxiliary
support. Summing these volumes gives a lower bound on exact cumulative support
work. Conversely, V_j.hi>0 includes every exact positive class, so the analogous
sum is an upper bound. An undecided zero is counted only in the upper bound.
The normalization rho*work/L uses exact Fraction arithmetic. Likewise the
half-cube-step count is a valid lower bound because it uses only certified
positive classes. None of these counts charges an implementation on the
original explicit graph; this is a quotient-based verification experiment.

## 5. Independent exact tests

`test_capped_tree_cube_interval.py` constructs the full seven-vertex graph for
L=2,p=1,s=1 and uses a separately formed dense Fraction matrix. It checks all
aggregate u and V coordinates and the line fraction against eight exact steps
for both the ordinary and monotone rules. Exact support volumes also bracket
the reported lower and upper work counts. A separate zero-optimum run exercises
the zero-curvature [0,1] fallback for two steps.

Projection tests use independently sorted exact Fraction water filling. They
include all combinations of three small rational raw values with two weight
patterns and four caps at two precisions, explicit ties and breakpoint equality,
large weight ratios, interval-box corners and midpoints, a forced fallback,
and stable-slope tightening from the crude slope1 to certified slope111.
Basic interval-operation checks cover signed multiplication/division, squares
across zero, and explicit Fraction endpoints. Results are saved separately in
`capped_tree_cube_interval_verification.json`. No randomized test is used.

The completed run passes all six test methods: 1198 projection cases, 16 exact
trajectory steps, 25 signed arithmetic pairs, and two zero-curvature steps.
No large instance was rerun as part of this independent audit.
