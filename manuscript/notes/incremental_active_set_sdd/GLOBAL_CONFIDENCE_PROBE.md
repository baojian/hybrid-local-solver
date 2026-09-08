# Confidence and full supplied recurrence: block 12 candidate

**Block 12 outcome.** The conditional resistance-estimator wrapper is proved using the checked Tropp matrix Chernoff source and exact-audited on 180 weighted cases. Full supplied recurrence is formalized under an explicit actual-positive-weight constructor contract. That constructor/source extension remains Conditional; no fast resistance estimator is implemented. See `sections/op3_supplied_recursion.tex`. The older proposal follows.

**Conditional until the source and complete proof are checked.** General
OP3 remains Open. The fixed-length nested audit and its independently
certified variant are running; do not edit their scripts or imported
helpers during those runs.

## Explicit confidence rather than inverse-polynomial in shrinking n

The source KLP Section 4 obtains all effective-resistance estimates to a
constant relative factor with constant success probability, using a
symmetric approximate inverse and a Johnson–Lindenstrauss transform.
Independently repeat the estimator an odd O(log(1/delta)) times and take
coordinatewise medians. If a majority of the complete estimate vectors
are good, all medians are good. A scalar Chernoff bound makes the failure
probability at most delta/2. Pay every estimate vector and median operation.

Scale the medians to obtain leverage overestimates p'_e with
w_e*R_e <= p'_e <= C*w_e*R_e, so t=sum p'_e <= C*(n-1).
For independent sampling probabilities p_e=p'_e/t, define on 1-perp

    Y_e = (w_e/p_e) * G^{+/2} b_e b_e' G^{+/2}.

Then E Y=I and ||Y_e||<=t. Matrix Chernoff with q samples gives
failure at most 2*(n-1)*exp(-epsilon^2*q/(3*t)) for epsilon in (0,1).
Choose epsilon=1/3 and q>=27*t*log(4*n/delta), and scale the sampled
Laplacian by 3/2. It lies between G and 2G, with O(n log(n/delta))
edge records. This is an independent confidence wrapper around the
source estimator, not a claim that its printed 1-1/n^2 theorem already
states arbitrary delta. The matrix square root is proof notation only.

Primary source newly located: Joel A. Tropp, *User-Friendly Tail Bounds
for Sums of Random Matrices*, Foundations of Computational Mathematics
12:389–434 (2012), DOI 10.1007/s10208-011-9099-z. Author journal PDF:
https://users.cms.caltech.edu/~jtropp/papers/Tro11-User-Friendly-FOCM.pdf .
Cached /tmp/op3-tropp2012.pdf and .txt. Corollary 5.2 and Remark 5.3
are located but not yet fully read/rendered; verify constants and both
tails before using the displayed simplified bound. Add source metadata
to both literature index and topic note if this argument is retained.

## Precise size/cost recurrence candidate

M=m+S includes every scalar piece, including one piece per vertex. Let
M0 be the original supplied input size. Pick a global logarithmic bound
L containing log(2+M0), initial numerical logs and log(1/p), and
K=A*L^12 for a sufficiently large universal A. Base cases should use
n<=K (rather than an unjustified constant-size curve claim): dense
forward-piece work is O(m+(S+1)*n^4), since the graph matrix is built
once, each bound QP uses at most n dense principal solves, and there
are at most S+1 piece-policy iterations. This is O(M*poly(L)).

For nonbase cases choose j=min(n,ceil(C*m*L^2/K)). If this equals n,
use a whole-graph constant-factor spectral sparsifier with all vertices
retained. Otherwise use the weighted source forest/routing construction
and core sparsifier. In both cases adjusted quality <=K, core edges
O(j*L), and j=O(m*L^2/K); above the base threshold j>=10.
The spectral floor only doubles quality and retains all forest bridges.
Constructors scan only the supplied graph; this is not local discovery.

Exact elimination has input size O(M); each compressed root gets O(L^2)
bins by the simultaneous range theorem. Therefore

    M_child <= C*m*L^4/K <= C*M*L^4/K.

There are at most C*sqrt(K)*L children (APG calls times refinement calls).
For large A their total input size is at most M/2. All nonrecursive graph,
forest, residual, export, compression, guard, coordinate and allocation
work is O(M*poly(L)); a safe polynomial exponent may be used rather
than claiming CPW's particular log^8 exponent. Base n^4 costs may give
a much larger logarithmic exponent. Summing all levels is near-linear
in M0 up to those explicit logarithmic factors.

The total size summed over the entire successful recursion tree is at
most 2*M0, so the number of constructor calls is at most 2*M0. Allocate
failure p/(4*M0) per call and cap the number of calls at 2*M0+1.
Conditional probabilities for fresh randomness hold on adaptive inputs;
the union bound then applies. This replaces a guessed enormous future
call count. A deterministic work cap O(M0*poly(L)) can abort pathological
failed-source executions; on the all-good event no cap is reached.

The constructor extension still needs its exact positive-weight primitive
contracts and allocation costs reconciled with CPW's stated polynomial
weight-ratio assumption. Do not label the supplied full theorem proved
until that source composition is explicit. The corrected numerical pieces
and their exact audits remain independent of this source extension.
