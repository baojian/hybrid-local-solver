# Local multipartite responses, including every physical seed

Date: 7 September 2026, second-night block 1. **Proved here**, draft awaiting
independent review. Proof authority: `sections/op3_local_multipartite.tex`,
labels `lem:op3-multipartite-scalar`, `lem:op3-multipartite-startup`,
`lem:op3-multipartite-paid-events`, `thm:op3-local-multipartite`,
`lem:op3-canonical-core`, `lem:op3-multipartite-leaf-seed` and
`thm:op3-canonical-multipartite`. General OP3 remains **Open**.

## Exact scoped result

The input is a finite simple connected unweighted graph promised to be a
complete multipartite core with arbitrary private leaves. The solver knows
only physical seed, alpha, lambda and original degree/adjacency queries.
Neither core size, partition, seed type nor future support is supplied.
The promise is assumed, not verified on unread rows. Every physical seed
is allowed, including an original core vertex whose original degree is one.

Let M=D-gamma*A, gamma=(1-alpha)/(1+alpha), b=e_v-lambda*d and u be the
physical obstacle response. For returned positive support U, total exact-
real word work is O(1+cvol(U)*log(2+cvol(U))) and space O(1+cvol(U)).
The work includes degree/row queries, dictionaries, complement snapshots,
classification, every curve/event copy, failed gate tests and final output.
Comparison dictionaries price the abstract Python operations; worst-case
constant-time Python hashing is not assumed. Rational bit complexity and
unchecked floating-point stability are not conclusions.

Original obstacle mass gives lambda*vol(U)<1. Thus lambda=eps_appr/2 and
output bar_alpha*D*u give the original ACL target in O_tilde(1/eps_appr)
work. Separately, lambda=rho and bar_alpha*D^(1/2)*u give exact RPPR in
O_tilde(1/rho) on this family. These are distinct accuracy namespaces.
No supplied fast numerical solver or top-tree balancing is used here.

## The complete local mechanism

Original degree greater than one recognizes the canonical non-leaf core.
It is again complete multipartite unless it is a singleton; an empty core
means the two-vertex graph. A leaf seed is positive after the initial zero
check. Its neighbor's exact original gate is gamma*(1-lambda)-lambda*d_a.
A nonpositive gate stops after one seed incidence, even if the parent has
10^18 private leaves. A positive gate pays for the anchor row, and exact
elimination gives u_v=1-lambda+gamma*u_a, diagonal d_a-gamma^2, and load
gamma*(1-lambda)-lambda*d_a. The original degree remains in all penalties.
The physical seed is retained as a distinguished leaf and recovered once.

The exact anchor star either certifies the answer or finds a positive
adjacent core vertex. Two positive original rows enumerate every canonical
core identifier and identify two complete parts. No zero row is read.

Each part is reduced to a scalar mass response through T/gamma+F_g(T)=S.
The transformed piece has slope below n_g/N. Negative input intervals are
retained. Each identified core vertex creates at most two events, once.
Previously built curves stay in one shared event heap. Exact restricted
roots increase as parts are inserted, so old events are consumed at most
once. Provisional affine roots are never used as original gate certificates.

An unknown-core heap stores lambda*d_i/gamma. At an exact restricted root
S, its minimum is an exact original quietness test. A positive gate pays
for a representative row; its nonneighbors among unknown identifiers are
its full part. Each removed identifier is charged once, and every outside
classification is an actual incidence of this positive representative.
This also pays for deletion snapshots and stale heap entries. All values
are recovered once at the end, not between insertions. Positive rows are
cached and positive private leaves emitted through their parent row.

## Exact audits and limits

Both executables live under `experiments/proof_audits/incremental_active_set_sdd/`
and are registered with `--full` as their extended tier. Their registered
module entry points and direct-file execution are supported.

- `LOCAL_MULTIPARTITE_PENDANT_AUDIT.json`: 3,640 explicit original obstacle
  comparisons, 3,944 independent restricted optima, 6,772 unknown original
  gate checks, and 16 implicit original-equation certificates. The huge
  six-core example has 1,000,002,000,000,000,008 ambient vertices; three
  positive rows inspect 16 original incidences, leaving a complete two-
  vertex heavy part unread.
- `CANONICAL_MULTIPARTITE_PENDANT_AUDIT.json`: 4,840 explicit comparisons,
  including 2,664 physical leaf seeds and 1,650 original degree-one-core
  cases; 4,348 independent restricted optima, 6,318 unknown original gates,
  1,996 distinguished-seed recoveries, and 56 implicit certificates.
- Both suites reverse incidence order, include exact zero/birth/gate ties,
  validate original full matrices independently, check monotone restricted
  solutions, and verify scanned rows equal the final positive support.
  The canonical suite includes source-leaf, post-elimination ordinary-leaf,
  unknown-part and zero ties. Dense matrices are validation only.

The suites overlap; these counts are executions, not a sum of distinct
inputs. Every saved JSON records parameters, exact arithmetic, graph
families, stopping rule, source/backend hashes and version provenance.

## Next question and provenance

The next bounded target is `RECURSIVE_MODULE_RESPONSE_PROBE.md`: exact
union/join composition may preserve a small final curve, and the saved
distinct-edge charge may pay for all ancestor copies on a supplied reduced
decomposition. That charge uses all core edges. Local module discovery and
skipping inactive regions are separate missing lemmas.
Generic coarse systems still incur repeated rank-dependent writes; neither
this promised-family result nor a future supplied-decomposition result
settles general OP3. Reassess that general bottleneck after the bounded audit.

Formal imports are within this note, whose registry dependencies remain
empty. The former supplied-part proposal is preserved in
`MULTIPARTITE_CORE_PROBE.md`; the clique source-comparison discussion is
in `LOCAL_CLIQUE_PENDANT_PROBE.md`. There is no scalar-search novelty claim,
new cross-note proof import or promotion into the active manuscript.
