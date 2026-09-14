# Exact local capped-box reporter and ordinary corrector

This note covers the new, separately versioned `capped_box_corrector.py`.
It does not modify the earlier lazy, monotone, or cleanup solvers. The
implementation uses deterministic AVL trees and exact rational degree
coordinates. Its counter report is a structural verification, not a claim
that arbitrary-precision Python arithmetic has unit bit cost.

The analytic stage interface and Q-metric stability are in the fresh
`dyadic_q_metric_stability.md`. The present note supplies the charged local
projection and source-initialization interface; it is not a replacement for
the complete continuation theorem being assembled separately.

## 1. Exact capped-box projection from one ordered tree

Each exposed vertex has a positive integer degree `d_i` and stored key `K_i`.
Given `sigma>0`, a shared shift `h`, a density upper bound `U>0`, and mass cap
`M>=0`, the Euclidean projection in normalized coordinates has densities

\[
 p_i=\min\{U,\max\{0,\sigma K_i-h-\eta\}\},\qquad \eta\ge0.
\]

This follows from minimizing `sum_i d_i*(p_i-raw_i)^2/2` subject to
`0<=p_i<=U` and `sum_i d_i*p_i<=M`: the degree cancels from the coordinate
stationarity equation. If the mass at `eta=0` is at most `M`, use `eta=0`.
Otherwise choose any nonnegative multiplier giving mass exactly `M`.
The projected point is unique even if the multiplier lies on a plateau.

The augmented AVL stores subtree record count, total degree, and weighted
key sum. Define the strict suffix moments

\[
 W(t)=\sum_{K_i>t}d_i,\qquad S(t)=\sum_{K_i>t}d_iK_i.
\]

Both are available with one root-to-leaf traversal. For
`l=(h+eta)/sigma`, `u=l+U/sigma`, the exact mass is

\[
 \Phi(\eta)=\sigma[S(l)-S(u)]-(h+\eta)[W(l)-W(u)]+UW(u). \tag{1}
\]

Its right derivative magnitude is `W(l)-W(u)`. Strict suffixes are
intentional: a coordinate with raw value exactly `eta` has just left the
positive set, whereas one with raw value exactly `eta+U` has just entered
the unsaturated interval. Formula (1) also handles ties and zero slopes.

The two sorted breakpoint sequences are

\[
 \{\sigma K_i-h\}_i,\qquad \{\sigma K_i-h-U\}_i.          \tag{2}
\]

Their within-sequence order is the existing AVL order. There is no need to
maintain or sort their merged order. When `Phi(0)>M>0`, initialize a bracket
with lower endpoint zero and upper endpoint the largest raw value. The
lower mass is strictly above `M`; the upper mass is strictly below `M`.
Binary-search each of the two sequences for the crossing of `Phi` through
`M`, obtaining candidate values by AVL rank selection. At a candidate:

* If its mass equals `M`, return it, including plateau equalities.
* If its mass exceeds `M`, increase the lower bracket endpoint.
* If its mass is smaller than `M`, decrease the upper endpoint.

Candidates already outside the current bracket can be discarded using
only their value. After searching both sequences, the open bracket contains
no breakpoint of either sequence. The mass is affine there; its right slope
at the lower endpoint is positive in magnitude, since the bracket masses
strictly straddle `M`. Therefore the exact root is

\[
 \eta=\eta_{\rm low}+
      \frac{\Phi(\eta_{\rm low})-M}{W(l)-W(u)}.           \tag{3}
\]

For `M=0`, the largest positive raw value is a valid multiplier. Empty trees
and inactive caps return zero. Thus every case, including a root at a tie or
a plateau, is explicitly covered.

There are at most `2*ceil(log_2(N+1))` binary-search candidates, each needing
`O(log(N+2))` rank and suffix work. Threshold computation costs
`O(log^2(N+2))` deterministic comparisons and exact arithmetic operations.
Finally enumerate only keys strictly above `(h+eta)/sigma`, clipping each
emitted density at `U`. This costs `O(log(N+2)+|Z|)`. Rejected positive raw
records are not enumerated, updated, or adjacency-scanned.

## 2. Sparse source initialization and lazy identities

Let the supplied nonnegative baseline have densities `bar_f_i`. The caller
must establish analytically that it lies below the desired optimizer. The
constructor checks its mass and the source inequalities

\[
 s=b-Q\bar x,\quad 0\le s_i/w_i\le C\alpha\rho,
 \qquad w^Ts=\alpha(1-w^T\bar x)\le\alpha.                \tag{4}
\]

It first exposes the seed and the nonzero baseline vertices. It scans only
the adjacency lists of those baseline vertices, queries the degrees of
their boundary, and accumulates the source there. No adjacency list is read
merely because its vertex belongs to the boundary or source support. The
source is zero outside the seed and closed baseline neighborhood.

If the baseline support volume is `B`, initialization uses `O(B+1)` degree
replies and numerical records and scans exactly `B` directed adjacency
entries. The nonzero source has at most `2B+1` records, irrespective of the
degrees of its boundary vertices. This cardinality bound, rather than their
degree sum, pays for refreshing their keys at each subsequent iteration.
Here the outer scheme supplies a canonical sparse map of positive baseline
entries. If a caller instead includes additional zero entries, reading those
entries is an extra explicit `baseline_input_records` charge.

The implementation accepts rational `alpha` and `theta` with
`0<theta<=1/2` and `mu=theta^2<=alpha<4mu`, `alpha<1`. No square roots are
computed. Define `L_mu=Q-mu I`, `lambda=alpha*rho`, and `a=1-theta`.
The stored maps are

\[
 X_i=\xi_i/(\sigma w_i),\qquad
 R_i=(L_\mu\xi)_i/(\sigma w_i),\qquad
 z_i=z_i^{\rm normalized}/w_i,\qquad
 t_i=(L_\mu z^{\rm normalized})_i/w_i.
\]

The kinetic keys obey

\[
 K_i=-\frac{R_i}{\theta(1+\theta)}
 +\frac{a z_i-t_i/(1+\theta)+(s_i/w_i)/\theta}{\sigma}.    \tag{5}
\]

The second term is an exception only on the current `z`, its response
support, and the fixed source support. With `h=lambda/theta`, multiplying
(5) by `sigma` and subtracting `h` gives exactly the ordinary accelerated
raw density

\[
 a z_i+\theta y_i-
    \frac{(Qy)_i/w_i-s_i/w_i+\lambda}{\theta},\qquad
 y=(\xi+\theta z)/(1+\theta).                            \tag{6}
\]

Project (6) with upper density `U=C*rho` and mass one. The default `C=4`
is the repaired-baseline interface. Then set
`xi_new=a*xi+theta*z_new`, implemented by `sigma*=a` and point additions
to `X` only on `Z_new`. Scatter `L_mu*z_new`, add the corresponding sparse
increments to `R`, and reinstall the new exceptions. In degree coordinates
this response has diagonal `alpha-mu+c` and neighbor coefficient `-c/d_i`.

At an unexposed vertex the source, primal, mirror, and their responses are
all zero: any nonzero response would already have exposed it during a
neighbor scatter. Its raw density is `-lambda/theta<0`, so it cannot be
selected. This justifies restricting the reporter to exposed records.

The constructor's conservative convergence bound is
`E0 <= C*lambda*mass(s)/mu`. Indeed the correction linear source is
`h=s-lambda*w`, so
`gap(0)<=||(h)_+||²/(2mu)<=C*lambda*mass(s)/(2mu)`, and the initial mirror
term is at most that objective gap. Ordinary acceleration then gives the
reported bound `a^k*E0`. This statement depends on the baseline and feasible
optimizer hypotheses; source checks alone do not certify those hypotheses.

## 3. Fully charged local work

Write `D_k=vol(supp z_k)` and `S=|supp s|<=2B+1`. Source refreshes cost
`O(S log(N+2))` each iteration and are explicit; the source is not treated
as a single seed or as a free global affine update. Old and new exceptions
cost `O((D_k+D_{k+1}+S)log(N+2))`. Each selected vertex adjacency is cached
after its first read, and every repeated response scatter is charged.

Over `K` steps, including initialization and output materialization, the
deterministic exact-real operation bound is

\[
 O\!\left((B+1)\log(N+2)+K\log^2(N+2)
       +\bigl[K(B+1)+\sum_{k=1}^K D_k\bigr]\log(N+2)\right). \tag{7}
\]

The total exposed state and output records are at most
`O(B+1+sum D_k)`; cached adjacency entries satisfy the same bound. Persistent
primal/response maps are never scanned inside a step. Output sorting, if
requested, is absorbed by the logarithm in (7). There is no global graph-size
query; `N` is the current exposed tree count.

For a deterministic worst-case word-model implementation, the auxiliary
vertex-indexed maps and sets can also be comparison-balanced trees; all
their operations fit the logarithm in (7). The Fraction prototype uses
ordinary Python maps for those point records, and its counters do not certify
worst-case Python hash-table running time. The projection order structure
itself is the explicit deterministic AVL implementation being tested.

Together with the separately proved source-comparator estimate for `C=4`,
`sum D_k<=148K/rho`, and a baseline with `B=O(1/rho)`, formula (7) gives the
required deterministic stage cost up to logarithms. Original-objective line
search or cleanup is deliberately absent: the auxiliary Q-metric energy
need not be preserved by those modifications.

## 4. Independent exact validation

`test_capped_box_corrector.py` uses a separately written dense rational
projection: it explicitly sorts all breakpoints and interpolates adjacent
mass values. Dense matrix recurrence and exhaustive KKT support enumeration
are confined to test code; production receives a query-only graph wrapper.

The saved `capped_box_corrector_verification.json` reports:

* 2,068 exhaustive small projection cases, including ties, zero cap, cap
  equality, empty input, inactive caps, and multiplier plateaus.
* 141 deterministic graph trajectories and 987 exact recurrence, energy,
  Q-error, response, and adjacency-charge comparisons; 665 use actual alpha
  different from theta squared. Three use a repaired exact old baseline.
* A separate feasible injected state with a binding mass cap, checked against
  the dense recurrence. This is not asserted to arise from zero.
* An 8,192-record reporter fixture with 8,191 positive raw records rejected,
  one emitted coordinate, and 96 query tree visits.
* A degree-1,000 source-boundary vertex whose adjacency is never read. Full
  iteration of persistent `X`, `R`, degree, key, and baseline maps is banned
  during a measured step, which still succeeds.

These finite tests check the implemented interface and accounting. They do
not replace the analytical stage estimate or a bit-complexity analysis.
