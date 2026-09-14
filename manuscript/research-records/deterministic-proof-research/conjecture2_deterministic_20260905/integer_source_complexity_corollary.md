# Concrete complexity of the integer and source-energy implementations

This corollary concerns the default complete wrappers
`solve_rppr_integer` and `solve_rppr_source_energy`, with rational alpha,
rho, and epsilon, and their existing deterministic AVL containers. It does
not modify their code. It uses the already audited rounded-work estimate

    sum_k vol(supp z_(k+1)) <=360 K/r                 (1)

for every stage prefix, the safe monotone repair, and the proved source
interface. Its purpose is to charge the actual realization, including scalar
rebases and exact arithmetic. It is not a new proof of the underlying
nonlinear estimate (1).

## 1. Statement and models

Assume the canonical finite simple connected graph, integer vertex labels,
positive integer degrees, and local adjacency-list access. In the nonzero,
nontrivial case 0<alpha<1 and 0<rho<1/d_seed, define

    a0 = ceil(log2(1/alpha)),
    r0 = ceil(log2(1/rho)),
    e0 = ceil(log2(max(1,1/epsilon))),
    L  = 16+4a0+3r0+e0.

These logarithms are for analysis; the code uses rational comparisons and
halving/doubling loops. Both default wrappers perform

    O(L^3/(rho sqrt(alpha)))                        (2)

arithmetic operations, comparisons, balanced-map accesses, and emitted or
read words, when an integer quotient/remainder is counted as an arithmetic
operation. Their first and repeated adjacency-entry inspections satisfy the
sharper bound

    O(L/(rho sqrt(alpha))).                         (3)

No factor involving the unexposed graph size enters these operation counts.
The output is a sparse list (i,f_i,d_i), representing x_i=f_i sqrt(d_i);
this is an exact radical representation, so no approximate square root is
required. Unlisted coordinates are zero. The proved output objective gap
is at most epsilon.

For an explicit bit-cost statement, let b_par bound the total binary length
of the signed numerators and positive denominators of the three rational
parameters. Let b_graph bound the binary length of every encountered vertex
label and degree, including the seed label and degree. Under canonical
labels in [n], b_graph=O(log n); the algorithm does not need to know n. Put

    B = O(b_par+b_graph+L),                         (4)

with a sufficiently large universal constant. Every stored numeric integer,
reduced rational numerator/denominator, and arithmetic temporary has O(B)
bits. Schoolbook multiplication/division and a deliberately conservative
Euclidean-gcd estimate give a total bit-arithmetic bound

    O(B^3 L^3/(rho sqrt(alpha))).                   (5)

This is a local-oracle bit-cost bound: encoded degree/label replies are paid
for, and any extra computation inside a user-supplied oracle must be added.
It is not a claim that an arbitrary callable graph oracle executes in unit
time. Nor does (2) silently add floor as a primitive to the canonical
exact-real algebraic model: it is an arithmetic-operation ledger for the
integer realization, with integer division fully implemented and charged in
(5). The original exact-real proof remains the statement for arbitrary real
parameters in that original model.

The zero regime rho*d_seed>=1 and the alpha=1 branch use O(1) scalar/word
operations and O(B^3) conservative bit work. Adding 1 to the right-hand
bounds gives a valid unrestricted upper bound. No independence from the bits
needed to encode input parameters or a returned graph word is asserted.

## 2. Stage schedule and a common precision bound

Write r_j for a stage's regularization and delta_j for its shift. At an
ordinary stage,

    delta_j=alpha*r_j/2,
    tau_j=alpha*delta_j^2/8=alpha^3*r_j^2/32.

Only the final stage may halve delta further. If any final halving occurs,
the value immediately before its last halving had squared shift greater
than epsilon*rho/2. Consequently

    delta_final^2 >epsilon*rho/8,
    tau_final >alpha*epsilon*rho/64.

If no such halving occurs, the ordinary formula applies instead. Thus every
stage satisfies

    tau_j >=tau_min
      :=min(alpha^3*rho^2/32, alpha*epsilon*rho/64).  (6)

The second branch is strict when it determines a stage through a final
halving; weak inequality in (6) is safe in all cases. Also tau_j<1/32.
The values tau_j decrease through continuation.

The dyadic momentum obeys

    theta^2<=alpha<4theta^2,   T=1/theta<2/sqrt(alpha).

For these wrapper tolerances the active grid ceiling is theta*tau_j/256:
it is smaller than 1/8 and theta*alpha^2*r_j/29. The latter comparison uses
alpha*r_j<1 and tau_j<=alpha^3*r_j^2/32.

The old baseline has been rounded to the preceding reciprocal-power-of-two
grid. Its reduced coordinate denominators divide the old grid denominator.
Since the tolerance ceilings decrease, the largest dyadic grid below the
new ceiling is automatically no coarser than the old one and represents
every old baseline coordinate. Thus the nesting restriction never forces
extra refinement beyond the new default ceiling. Inductively, the actual
minimal chosen grids satisfy

    theta*tau_j/512 <h_j<=theta*tau_j/256.           (7)

This assertion is for default complete wrappers. A separately invoked
corrector with an arbitrarily fine explicit grid or an arbitrary input
baseline need not satisfy the lower bound in (7).

Writing H_j=1/h_j, (6)-(7) imply

    log2 H_j <9+log2 T+log2(1/tau_min) <=L.

For example log2(1/tau_min)<=6+3a0+2r0+e0 and
log2 T<=1+a0/2 suffice. The original number of blocks is at most L; the
source-energy schedule is never longer. Therefore, for both wrappers,

    K_j<=T L.                                      (8)

The grid selection, momentum selection, tolerance adjustment, and schedule
loops contribute at most O(L) operations per stage. In the derived source
schedule, the base constructor's original schedule loop still runs before
replacement; counting both loops only changes this constant.

## 3. Geometric stage summation

Before the last stage, r_j=(1/d_seed)/2^j. The last stage may be shortened
to the exact requested rho. There are at most O(L) stages, but a stage-count
factor need not be multiplied into every work term:

    sum_j 1/r_j <3/rho.                             (9)

Indeed, the inverse parameters before the final stage form a geometric
series whose sum is less than twice its last term. That last parameter is
strictly greater than rho. Adding the final 1/rho gives (9). The one-stage
case is immediate.

This is an unweighted geometric sum. It does not assert an analogous
constant-factor sum for mass-deficit-weighted quantities.

## 4. Size of the exposed state and terminal work

Fix a stage r and K executed steps, possibly K=0. Its old baseline lies
below x*_r, so its support volume V_bar is at most 1/r. Initialization
exposes only its support, its immediate boundary, and the seed, using
V_bar adjacency entries. Thus there are at most 1+2V_bar initial vertex
records and O(1/r) source records.

Each selected row subsequently exposes at most one vertex per inspected
adjacency entry. By (1), with W denoting cumulative kinetic volume,

    W<=360K/r,
    N<=1+2V_bar+W<=363(K+1)/r.                     (10)

Here N bounds all exposed point records. Retained adjacency entries total
at most V_bar+W. Approximate-L records are created only by such exposures;
scalar rebases create no new graph records.

Every positive correction coordinate was selected at some previous step.
The full candidate therefore has support volume at most V_bar+W. Its
materialization and the exact terminal PG pass cost O(V_bar+W) entries and
record operations before the balanced-map logarithm. The implementation
scans only this candidate, accumulates numerators, and clips/floors a new PG
coordinate before ever inspecting that coordinate's row. In fact, under
the complete wrapper invariant, every candidate row was already cached by
initialization or a selected step; the pass rereads those cached entries.
Allowing the more general helper's degree/cache checks only preserves the
same upper bound.

The source-energy statistics make one additional charged pass over the
O(1/r) source records, including at zero-step stages. Output and safe maximum
repair use already exposed records; the repaired support volume is at most
1/r. All these operations remain in (10) when K=0.

From (8)-(10),

    log2(N+2)=O(L).                                 (11)

This logarithm depends on paid local history, not the total graph size.

## 5. Scalar rebase frequency

At every reset S=H. Until the next reset,

    S_next=floor((T-1)S/T),
    S-S_next<=H/T+1.

A reset requires S<H/2. Hence each completed reset interval has length
strictly greater than H/[2(H/T+1)]. Because (7) implies H>=T, that length
is greater than or equal to T/4 as a lower bound. Thus the number R_b of
rebases satisfies the convenient conservative estimate

    R_b<=4K/T=4theta K.                             (12)

Using O(theta K+1) also covers incomplete intervals and K=0 without cases.
Each rebase visits at most O(N) old X/L/exposed records and performs at most
O(N) balanced-map or reporter changes. Old/new map reclamation is included
in this charge. There are no rebase adjacency inspections.

This gives O((1+theta K)N log(N+2)) work for initial construction, final
passes, and every full-state scalar rebase. It explicitly pays repeated
old-state visits; they are not treated as free.

## 6. Two-tree queries and sparse updates

At each projection, four individually ordered breakpoint sequences are
searched: lower/upper translates of the base and exception trees. There are
O(log(N+2)) rank candidates per sequence, each using rank/tail queries of
O(log(N+2)) work. Thus root selection costs O(log^2(N+2)); exact equality
and zero-cap branches only shorten it. Inclusive tail reporting costs
O(log(N+2)+number_emitted), without enumerating rejected positive sub-grid
coordinates.

Outside full rebases, each emitted row and its boundary induces O(1)
logical map operations per adjacency entry. Restoring old exceptions and
installing new ones visits only the current/previous kinetic support and
boundary plus the fixed source. Summing these visits costs
O(W+K/r); balanced-map and reporter point operations add one logarithm.
Both the vertex registry and every solver point map/set use deterministic
AVL structures.

Combining these facts, a stage is bounded by

    O( L + K log^2(N+2)
         + [(K+1)/r]*(1+theta K)*log(N+2) ).        (13)

It also has only O((K+1)/r) total adjacency-entry inspections. Substitute
K<=TL, theta=1/T, and (11) into (13), obtaining O(T L^3/r). Equation (9)
then gives (2), and the adjacency count gives (3). No extra stage-count
factor is hidden in this last step.

## 7. Integer-state and tree coefficient sizes

The mass cap implies at ordinary iteration starts

    sum_i d_i*m_i <=2H,   sum_i d_i*p_i<=H,
    sum_i d_i*B_i<=H,

where m,p,B are the integer counts of normalized primal, kinetic, and
baseline densities. Immediately before a scalar rebase, sigma>=1/8 gives
the harmless larger bound sum d_i*m_i<=8H. Exact kinetic/baseline neighbor
counts are therefore O(H). The scalar-L error bound gives, at all relevant
states,

    |j_i-sum_neighbor m_l|<=4d_i,
    |j_i|<=8H+4d_i.                                (14)

Nonnegative source numerators sum to 2A times the cap count, at most 2AH.
The base and exception numerators are fixed-degree integer expressions in
A,D,T,H,S,d_i and these bounded counts. Their magnitudes are bounded by a
constant times D*T^2*H*(H+d_max), up to a further fixed parameter factor if
all setup expressions are included. Subtree integer sums add at most
log2(N+1) bits, and degree moments are at most N*d_max. Label comparisons
use at most b_graph bits.

Consequently state values, temporary products in updates, and tree moments
all have O(b_par+b_graph+L+log(N+2))=O(B) bits. No product of past projection
multipliers or past scales survives in stored vectors.

## 8. Root-query denominators do not accumulate degrees

The reporter uses q=(gamma+shift)G, where
G=2D H^2(T+1). Its initial q and box width have denominators dividing den(r).
A breakpoint is one integer-tree key divided by **one** degree, with an
optional width translation. Each candidate is freshly reconstructed from
that record. The two bracket endpoints store selected candidates; neither
is formed by summing an ever-growing list of breakpoints.

At a mass query, weighted moments are integer sums. Its rational result has
the form

    integer - q*free_degree_sum + width*upper_degree_sum.

Only q's one selected degree denominator and the fixed parameter denominator
occur. On the final affine interval the root algebraically equals

    (integer + width*upper_degree_sum - target)/free_degree_sum.

The positive free-degree sum is at most N*d_max; it introduces one integer
denominator, not a least common multiple of degrees. The implementation's
uncancelled intermediate expression has only a fixed number of O(B)-bit
factors and is immediately reduced. Exact breakpoint/equality or zero-cap
returns have the same bound. A projected coordinate may introduce its own
degree, but its integer floor is computed immediately; that denominator is
not carried to the next state.

Thus both reduced results and unreduced temporary products in the root
search have O(B) bits independently of the number of search candidates or
iterations.

## 9. Source statistics and terminal repair denominators

The optional source-energy calculation uses C=2D H den(r) and

    G_i=max(den(r)*N_i-2A H num(r)*d_i,0).

It sums G_i and ceil(G_i^2/d_i) as integers; the final denominators are C and
C^2. Its maximum retains one chosen degree denominator. The rounding excess
is less than n_positive/C^2 when that count is nonzero. These facts prevent
the degree-LCM growth that an exact accumulated H2=sum d_i*g_i^2 could have.
The final energy bound combines a fixed number of parameter/statistic
scalars. Its repeated dyadic block division introduces only O(L) additional
bits. The zero-step branch returns the initial bound directly.

Terminal candidate densities have denominator dividing H^2. Before dividing
by a target vertex degree, PG incoming numerators are accumulated using only
c=(1-alpha)/2 and the seed alpha. All their denominators divide 2D H^2;
thus this sum also has no degree-LCM growth. Only after accumulation does a
single coordinate acquire its own degree denominator. Subtracting lambda
and delta introduces fixed parameter denominators; clipping and grid floor
immediately eliminate them. The maximum repair and new baseline again have
denominators dividing H. Subsequent stages therefore never inherit degree
or projection-root denominators.

All exact output and retained summary statistics consequently have O(B)
bits per integer or rational component. The requested tolerance's input
encoding is included even if epsilon is numerically large.

## 10. Bit arithmetic and storage

An addition/comparison/multiplication/division on O(B)-bit integers costs at
most O(B^2) by elementary algorithms. For a deliberately conservative gcd
bound, Euclid has O(B) division steps, each costing O(B^2), hence O(B^3).
A Fraction arithmetic operation creates only a constant number of products
and reductions, so it costs O(B^3). Integer floor/ceiling and remainder are
fully paid by integer division. Applying this upper bound to (2) proves (5),
including state reads/writes and encoded oracle replies whose bit cost is
at most O(B) per word.

This is intentionally conservative and does not use GMP, randomized
arithmetic, or an unproved constant-time gcd. It does not identify Python
wall time with the arithmetic upper bound.

Current-stage records and cached entries occupy
O(T L/rho) words in the worst stage. The wrapper retains repaired summaries
from prior stages, but their total output volume is O(sum_j1/r_j)=O(1/rho),
plus O(L) scalar metadata. It does not retain entire corrector histories.
Peak storage is therefore

    O(L/(rho sqrt(alpha))) words,
    O(B L/(rho sqrt(alpha))) bits,

up to ordinary pointer/object constants. Optional diagnostic full-state
snapshots are excluded from the default-run bound; if requested repeatedly,
their explicitly counted scans must be added.

## Conclusion of the audit

The suggested cubic logarithmic arithmetic ledger is valid for the actual
default integer/source-energy realization. The potentially missing terms
are paid: scalar rebases contribute one logarithmic schedule factor,
two-tree root queries contribute two data-structure logarithms, the
geometric stage sum prevents an additional stage factor, common-denominator
source statistics and terminal PG prevent degree-LCM growth, and zero-step
stages retain initialization/repair charges. The conservative bit extension
necessarily includes encoded parameter, degree, and label lengths. It does
not weaken the separate graph-uniform exact-real theorem by silently hiding
those bit lengths inside its allowed logarithms.
