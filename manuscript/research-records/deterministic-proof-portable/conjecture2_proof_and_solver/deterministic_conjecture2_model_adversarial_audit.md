# Fresh adversarial audit: model, asymptotics, and hidden work

This audit rereads the current `deterministic_conjecture2_proof.md` against
only the authorized `problem_definitions/main.tex` and derives the main
potentially hidden costs directly. It does not treat earlier audit approval
as evidence. No old manuscript direction or other task was inspected.

## Result and exact scope

I found no actual defect in the current proof under the computational model
explicitly stated in the supplied reference. The earlier arbitrary-rho
additive-constant issue is fixed. The result establishes deterministic OP2
in that exact-real algebraic word model. It does not by itself establish
bit complexity, numerical robustness, or practical floating runtime.

The exact assumptions needed are:

1. A finite connected simple undirected unit-edge graph, with vertex IDs in
   [n], n>=2, and hence d_i>=1. The algorithm does not receive n or a global
   graph summary as useful preprocessing.
2. A single given seed ID, not an uncharged distributed input source.
3. Charged degree replies and charged adjacency-list entry inspections;
   each new ID is learned from the seed or an already charged list.
4. Exact real arithmetic and comparisons at unit word cost, including
   arbitrarily close comparisons and exact equality. The reference states
   this explicitly in its Computational model paragraph.
5. Deterministic comparison trees for all state maps, sets, and breakpoint
   orderings when claiming the worst-case word bound. Python hash maps in
   the verification prototype are not substituted into that proof.
6. A sparse list representing the output vector, as allowed by the
   reference. A triple (vertex,density,degree) represents density*sqrt(degree)
   without requiring a new square-root primitive.

The supplied reference also explicitly excludes coefficient-bit growth,
finite-precision stability, and rounding error from this baseline model.
Thus these are limitations of the proved scope, not assumptions silently
introduced by the candidate proof.

## Objective normalization and accuracy

The Q and b used by the proof are exactly the source's normalized lazy
RPPR matrices. The nonsmooth coefficient is alpha*rho, not rho alone, and
rho is never substituted for the requested objective tolerance epsilon.
All algorithmic iterates are nonnegative, so the absolute-value objective
reduces to the displayed quadratic plus linear term without changing its
value. The baseline correction identity is exactly

    F_r(bar+xi)-F_r(bar)
       = xi^T Qxi/2-(b-Qbar-alpha*r*w)^T xi.

No hidden objective rescaling enters the stopping certificate or final
output guarantee. In particular, the repair estimate bounds the original
F_r gap by 2delta²/r, rather than a density norm or a semantic PPR error.

The safe repaired error is supported where x*_r is positive, so its KKT
linear term vanishes. This is why the final objective error is quadratic.
Without safe containment, that step would be invalid; the proof establishes
containment first using its explicit Euclidean error certificate.

## Arbitrary real alpha does not hide a square root

Halving theta from 1/2 until theta²<=alpha takes O(1+log(1/alpha)) exact
comparisons and divisions. It gives alpha/4<mu=theta²<=alpha, including
alpha>1/4. Every algorithmic coefficient is obtained by arithmetic from
alpha and this dyadic theta. No exact sqrt(alpha) is needed.

The stage certificate maintains sigma=a^k by multiplication and compares
it to tau. Logarithms appear only in the analysis. The general-mu raw
identity is valid because its V coefficient simplifies to

    a I-(Q_mass-mu I)/(1+theta)
      = (1-alpha)/(1+theta)*(I+P)/2.

Thus using a lower curvature bound does not create an omitted response or
an additional inverse-alpha factor. Its forcing contains Q-mu I, whose
squared response is controlled by Q because these two matrices commute.
The projection itself is never assumed to commute with Q.

The exceptional alpha=1 case is diagonal and is handled directly.
Alpha=0 is outside the source problem.

## Explicit parameter logarithms and geometric sum

Write A=log(1/alpha), R=log(1/rho), and
E=log_+(1/epsilon) in the nonzero regime rho<1/d_seed<=1.
Every intermediate tolerance is

    tau_j=alpha^5*r_j²/8 >=alpha^5*rho²/8.

At the final stage, either no additional delta halving is required, or
minimal halving gives

    epsilon*rho/8 < delta_final² <=epsilon*rho/2.

Consequently every stage has

    tau_j >= min(alpha^5*rho²/8, alpha³*epsilon*rho/16),

with a harmless strict inequality in the second branch. Therefore

    log(1/tau_j) <= 5A+2R+E+log(16).

The iteration bound is explicitly

    K_j <= 1+(2/sqrt(alpha))*(5A+2R+E+log(16)).

This rules out polynomial dependence on inverse epsilon from the repair.
For the last partial dyadic stage,

    sum_j 1/r_j < 3/rho.

Hence summing K_j/r_j gives the target 1/(rho sqrt(alpha)) times allowed
parameter logarithms. Stage setup and all halving loops fit in this bound.
For rho*d_seed>=1 the answer is zero after O(1) work; the current global
statement correctly includes that additive constant.

## No circular or global dependence in the state logarithm

Let Vbar_j be the baseline degree volume and
B_j=sum_k vol(supp z_(k+1)) at stage j. Before the stage, exposing the
baseline support and its neighbors creates at most 2Vbar_j+1 records.
Every later new record comes from an emitted support's charged adjacency
entries. Thus, independently of any tree-operation count,

    N_j <= 2Vbar_j+1+B_j,
    retained adjacency entries <= Vbar_j+B_j.

The proof's analytical charge gives B_j<=148K_j/r_j and
Vbar_j<=1/r_previous<=1/r_j. Therefore

    N_j=O((K_j+1)/r_j).

The log N_j factor is consequently bounded by allowed parameter logs and
logarithms of those logs; it cannot conceal unrestricted log n. This is not
a circular inference from total runtime: N_j is bounded by graph emissions
before balanced-tree runtime is charged.

A boundary node may have enormous degree, but its degree is just one
charged reply. Its adjacency list is not read until that node is actually
emitted. If it is emitted, every entry is charged in B_j, including its
first inspection and later repeated scans. No sum of inactive boundary
degrees appears elsewhere.

## Source, certificate, and unavailable information

Computing s=b-Qbar scans only bar and records its one-hop response. The
source record count is at most 2Vbar+1 and all source keys may be refreshed
at every iteration within O(K/r) dictionary operations. Nodes with zero
source need no source exception.

The proof's t=Q^-1 s, true correction, true support, and half-rho support
are all analytical comparators. The algorithm never computes an inverse,
queries those vectors, or asks whether a vertex belongs to them. The
objective certificate is the maintained scalar sigma<=tau; evaluating a
full gradient or global objective is not required for termination.

An omitted vertex has not appeared in any baseline or emitted-support
adjacency scan. Consequently no positive current primal or kinetic
coordinate is adjacent to it, and its source and maintained response are
zero. Its raw coordinate is strictly negative. Exact cap and upper clipping
cannot make it positive. This proves the omitted-node rule without a
boundary enumeration oracle.

## Every reporter operation is deterministic arithmetic/comparison work

The reporter stores a common affine key ordering, with sparse exceptions
only for the current kinetic vector, its response, and the fixed source.
Removing old exceptions, changing sigma, applying sparse response updates,
and installing new exceptions touch only charged lists. Updating the base
response and installing exceptions are distinct operations; both fit the
same cumulative degree-volume bound.

A clipped mass query is a difference of two weighted tail queries. All
breakpoints lie in two translated copies of the existing ordered keys.
Order statistics, deterministic binary search, and one exact affine root
solve suffice. No numeric bisection depending on a breakpoint separation
is used. Equality or a flat root interval permits an exact valid multiplier;
there is no need to know a smallest positive coordinate or complementarity
margin.

Positive projected outputs are enumerated by a strict tail query, so
positive raw candidates rejected by the cap do not trigger adjacency scans.
Saturated upper-box coordinates are output and charged like all other
positive coordinates. All auxiliary dictionaries can be AVL or other
deterministic balanced comparison trees; no expected-time hash-table or
randomized balancing assumption is needed.

## Materialization, repair, and discard

Starting from zero correction and using positive averaging, every nonzero
primal correction coordinate belongs to the union of previously emitted
kinetic supports. The union's degree volume is at most B_j. Thus the final
full approximate vector can be materialized from that union plus bar,
without examining other vertices. Repair is one scalar operation per such
coordinate and leaves a subset of the true support.

Building the next source scans the repaired support and charges its actual
original degrees. Clearing obsolete maps and adjacency caches costs at
most their allocated word count, already bounded above by Vbar_j+B_j+K_j.
Sorted sparse output, if desired, adds only an allowed comparison-tree or
sorting logarithm. No old primal scan is repeated inside the iterations.

Support recovery is not assumed: an arbitrarily tiny true coordinate may
be dropped by repair. Its error is covered by the global objective
certificate and quadratic repair estimate. The algorithm never searches
for its sign margin.

## Practical precision gaps, distinguished from proof defects

The exact-word proof does not provide any of the following:

- A bound on Fraction numerator/denominator size or machine-bit runtime.
- A floating implementation of exact tail differences robust to severe
  cancellation or exact ties.
- A proof that rounded projection preserves the second comparison sector,
  source nonnegativity, or safe containment without additional safeguards.
- A rule for rescaling and accumulated response-rounding errors that
  preserves the fully charged support bound.
- A bit model independent of log n even for reading a vertex label or a
  large degree; the source intentionally treats those as words.

Those are genuine engineering and stronger-model questions. They should
remain separate from the exact arithmetic theorem. The candidate proof
now states this separation and does not promote prototype structural
counts into a production runtime theorem.
