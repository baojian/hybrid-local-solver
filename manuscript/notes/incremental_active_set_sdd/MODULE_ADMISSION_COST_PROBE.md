# Next probe: changed module responses and a causal work charge

Second night, block 3, 8 September 2026. **Conditional / Open** research
directions below; no general OP3 theorem or new lower bound is claimed.

## Completed primitives; do not repeat these audits

The supplied persistent response construction, fixed-response strict target
reporter and known convex summand removal are implemented and proved as
drafts. Read `sections/op3_recursive_modules.tex`,
`sections/op3_module_reporter.tex`, `sections/op3_module_curve_removal.tex`
and their named audit JSON files. The reporter allows arbitrary fields and
positive target changes, including decreases. It does not maintain curves
under graph admissions. Removal streams only the known child, deletes zero
jumps and preserves all old versions.

The graph-structure source checkpoint is in
`docs/literature/lcp-solvers.md`, subsection “Shamir and Sharan, 2004”.
It is context, not an implemented local source import. Its graph records do
not include the numerical response. The old triangle-to-paw reachable trace
remains in `MODULE_REPORTER_AND_UPDATE_PROBE.md`.

## Which replacement operation is actually expensive?

At a join, changing a large child can be cheap if the unchanged siblings
are small: start from the changed child's new transformed curve and merge
the siblings. Their vertices are neighbors of a newly inserted vertex
whose membership follows that child. At a union the unchanged siblings
need not be adjacent to that vertex. A changed large child inside a union
can therefore be the difficult step. Signed removal prices the removed
curve, not just the few structural records that changed.

Test a connected core built as the join of a universal vertex u with the
union of two stars A and B. Their centers are a and b. Give the old star
leaves unequal private-leaf counts. Add a sequence of new vertices j to A,
each adjacent only to {u,a}, with no private leaves. Every induced core in
the sequence is still union/join, and each new vertex has original degree
two. Its insertion changes a small part of the cotree, but changes A's
response nonlinearly before it is added to B's response at their union.

The next audit must count **genuine curve events**, not just module sizes.
Compare at least (i) subtract old A and add new A, (ii) start from new A
and add B, and (iii) any whole-curve transformation that actually preserves
the shared field. A large physical module can have only a few events.
Do not manufacture an obstruction by choosing an unnecessarily expensive
merge direction or by retaining zero jumps. Original diagonal degrees
must include every future j from the outset.

A per-insertion example would not establish excessive cumulative local
work: the old core vertices must first have entered through positive
original gates. In particular, the full response curve at arbitrary h
contains events that the current physical h=0 trajectory may never use.

## A useful residual budget may prevent the naive counterexample

Here is an elementary derivation to audit and use as a candidate charge.
For any restricted exact obstacle response u with zero exterior, physical
seed v and original matrix M, put r=e_v-Mu. Every r_i is nonnegative:
on positive coordinates it equals lambda*d_i, and on zero coordinates it
equals e_v(i)+gamma*sum_{j~i}u_j. Therefore

    sum_i r_i = 1 - bar_alpha*sum_i d_i*u_i <= 1.

In the two-star construction an unadmitted degree-two j has
r_j=gamma*(u_u+u_a). If an old A-leaf with q private leaves is already
positive, its core equation implies

    gamma*(u_u+u_a) > lambda*(2+q).

Indeed, after eliminating its positive private leaves the scalar kernel
is strictly increasing and its birth field is lambda*(2+q). Hence the
number L of still-unadmitted such j satisfies

    L*lambda*(2+q) < 1.

Large q may create many distinct response events, but may also restrict
how many low-degree admissions remain once those expensive old vertices
are positive. This is a reason to test a causal cumulative charge before
declaring the representation route refuted. It is not yet a bound on
general module events, and it says nothing about a hypothetical global
curve update performed before the old coordinates become positive.

Falsify with exact original restricted responses, varied alpha/lambda,
unequal pendant profiles and legal admission orders. If a cost k can be
associated with remaining candidates whose residual is at least
Omega(lambda*k), the displayed mass budget suggests a phase charge;
proving that association and handling changes between phases are open.

## Return to the arbitrary-graph question

After this bounded admission-cost test, revisit the generic sparse coarse
system and the constrained-diffusion route. The existing sparse certificate
has rank-dependent work; fixed-field response primitives alone do not
remove that rank factor. A useful next result must either reduce repeated
coarse-coordinate work or supply a local constrained solve with all source
parameter, graph-exposure, original-residual and failed-certificate costs.
Keep general OP3 **Open**, keep ACL and exact RPPR accuracy distinct, and
record representation-specific failures without promoting them to lower
bounds for the graph problem.
