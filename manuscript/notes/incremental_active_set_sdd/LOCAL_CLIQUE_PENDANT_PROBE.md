# Local scalar responses on clique cores with unequal leaves

7 September 2026. **Proved here**, draft awaiting independent review.
The complete special-case algorithm is implemented and exactly audited.
General OP3 remains **Open**. Proof authority:
`sections/op3_local_clique_pendants.tex`, especially
`lem:op3-clique-scalar-response` and `thm:op3-local-clique-pendants`.

## Question, promise and charged model

The finite simple connected unweighted graph is promised to be an unknown
clique of size `k>=3`, with `t_i>=0` private degree-one leaves at core vertex
`i`. The physical seed `v` is a core vertex. Counts can be unequal and
arbitrarily large. Verifying the promise on unread rows is not included.
Use original full degrees and local degree/adjacency queries. Charge every
query, incidence, dictionary operation, response record, sort comparison,
update and output in the exact-real word model. No rational bit-complexity
or floating-point stability bound is claimed.

Put `gamma=(1-alpha)/(1+alpha)`, `bar_alpha=1-gamma`,
`M=D-gamma*A`, `b=e_v-lambda*d`. The physical solution is the nonnegative
obstacle minimizer. If `lambda*d_v>=1`, return zero with one degree query.
Otherwise the seed is positive. Its row and neighbor degrees reveal all
core identifiers: they are the seed and its neighbors with degree greater
than one. Thus `k`, every core degree, and `t_i=d_i-(k-1)` cost `O(d_v)`
without reading an inactive core row or an attachment subtree.

## Exact scalar construction

Let `S=sum_core u_i`, `a_i=d_i+gamma`, `c_i=a_i-gamma^2*t_i`, and
`z_i=b_i+gamma*S`. The core response is

- `phi_i(S)=0` if `z_i<=0`;
- `phi_i(S)=z_i/a_i` if `0<z_i<=a_i*lambda/gamma`;
- `phi_i(S)=(z_i-gamma*lambda*t_i)/c_i` otherwise.

Each private leaf has value `max(0,gamma*phi_i(S)-lambda)`.
These expressions follow directly from the original core and leaf
obstacle equations. They are continuous. Since
`c_i=k-1+gamma+(1-gamma^2)*t_i>=k-1+gamma`, every affine slope of
`F(S)=sum_i phi_i(S)` is at most `k*gamma/(k-1+gamma)<1`.
Hence `F(S)=S` has a unique nonnegative root.

Initialize all pieces at zero and sort their at most `2k` positive
breakpoints. On a current interval maintain `F(S)=A*S+B` and compute
`B/(1-A)`. Stop if this lies before the next event; otherwise cross that
event and update constant-size aggregate coefficients. Exact equalities
are allowed and zero coordinates stay inactive. This finite sweep has no
contraction-iteration factor involving `1/(1-A)`.

Evaluate the core values once and read further rows only at positive core
vertices. Their rows enumerate the private leaves that may need output.
All `k` computed values, including zeros, are charged to the already read
positive seed row. Work is `O(1+cvol(U)*log(2+cvol(U)))` and storage is
`O(1+cvol(U))`, including original accesses and output.

With `lambda=eps_appr/2`, this gives local ACL work
`O_tilde(1/eps_appr)`. Separately, `lambda=rho` gives the exact RPPR
solution with work `O_tilde(1/rho)` on this family. This exact-obstacle
algorithm is distinct from the general certified publication method,
which may stop early and has an ACL-only conclusion.

## Measured

`LOCAL_CLIQUE_PENDANT_AUDIT.json` records 1,464 exact original-matrix
obstacle comparisons for core sizes three through six, unequal counts,
every core seed, four parameter pairs, and exact core/leaf/zero gate ties.
There are 765 nonzero partial-core cases and 4,847 inactive core instances
whose rows remain unread. Six implicit finite graphs receive full original
core/leaf equation checks using explicit leaf multiplicities.

The largest example has pendant counts `[0,2,0,4,10^18]`, core seed zero,
`alpha=1/1009`, and `lambda=1/40`. Its ambient size is `10^18+11`, but the
algorithm reads six positive rows and 24 original incidences; the huge
inactive core row remains unread. This is finite exact-word evidence,
not a claim that representing an arbitrarily large integer costs one bit.

The actual scalar sweep is in
`experiments/proof_audits/incremental_active_set_sdd/local_clique_pendants.py`.
It imports neither top-tree balancing nor a fast SDD solver. Independent
dense original obstacle solutions are validators only.

## Context/provenance and novelty limits

The companion direction `delayed_reflection_ladder` already discusses
cliques and complete bipartite graphs in `12_subsec_equitable_shells.tex`,
and tree quotients and hidden partition refinement in
`14_subsec_equitable_tree_quotients.tex`. Unequal pendant counts can break
degree-equitable distance shells. For counts `(0,1,4)` and seed zero,
the core degrees are `2,3,6`; separating these cores leaves a triangular
quotient. The scalar construction handles this unequal coupling directly.
These are comparisons, not imported lemmas or new registry dependencies.

Scalar breakpoint methods are classical. Kiwiel's primary institutional
preprint, [Breakpoint searching algorithms for the continuous quadratic
knapsack problem](https://rcin.org.pl/Content/139441/PDF/RB-2002-77.pdf),
30 December 2002, introduction (printed p. 1; PDF p. 3), describes the
monotone piecewise-linear multiplier equation with `2n` breakpoints and
earlier `O(n log n)` sorting methods. That problem has different constraints;
no theorem from it is imported here. The possible contribution to investigate
is the graph-local reduction, positive-only discovery and complete original
residual/work accounting. No novelty claim is established by this search.

## Next falsifiable target

`MULTIPARTITE_CORE_PROBE.md` gives a candidate extension with one scalar
total coupled through part responses. Its supplied-part algebra passes
261 exact original obstacle comparisons, but local positive-row startup,
part discovery and one incremental event structure remain **Conditional /
Open**. Complete and charge these mechanisms before claiming a multipartite
local theorem. The clique construction also shows that the forced-refresh
family in `BATCHED_COARSE_CERTIFICATE_PROBE.md` is an obstruction to that
specific representation, not a graph-uniform lower bound.
