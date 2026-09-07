# incremental_active_set_sdd

This standalone note audits the repeated-active-set factor in the August 2026
Wei--Yang PageRank/RPPR algorithm and asks exactly what is required to remove
it.  The note proves an exact block-Schur correction identity and a telescoping
energy law for nested restricted systems.  It also proves that warm starts
alone do not remove repeated-prefix work: any implementation that explicitly
materializes the whole active solution after every expansion has quadratic
write cost on endpoint paths.

The positive result is exact and stronger on the same graph class.  On an
endpoint-seeded path, a one-pass `LDL^T` message computes every active-set gate
in constant arithmetic per admitted vertex and materializes the solution only
once, in a final reverse pass.  Its total charged work is linear in the final
active volume, with no repeated factor and no polynomial dependence on
`1 / alpha`.  The source ACL and RPPR correctness arguments continue to hold
because the replacement uses exact restricted solutions.

For arbitrary graphs, the note gives a conditional plug-in theorem for an
implicit incremental solve-and-boundary interface.  Constructing that
interface with near-linear total local work remains open: the block correction
can be dense, and the energy telescope does not pay for full active-set matrix
passes or repeated vector output.

**September 6 exploration.**
[`OP3_DIRECTIONS_20260906.md`](OP3_DIRECTIONS_20260906.md) compares the
remaining directions after the new OP2 results. Section
`sec:op3-geometric-events` of `main.tex` gives a new proof-draft reduction:
constant-factor value publications have near-linear total delivery work,
and one final certified SDD solve gives the ACL output. Detecting and
producing those publications remains open. The section also proves a
scaled teleportation-continuation ordering and gives an exact support-birth
counterexample to a multiplicative warm-start bracket. These additions await
independent review; they do not resolve OP3 or supersede the earlier path
theorem. See [`VERIFICATION.md`](VERIFICATION.md) for the exact audit and
build checks.

Build from this directory with:

```bash
make
```

The overnight continuation is tracked in [`OVERNIGHT_STATUS.md`](OVERNIGHT_STATUS.md).
It now includes several constructive proof drafts:

- [`TREE_AFFINE_PROBE.md`](TREE_AFFINE_PROBE.md): an implemented persistent
  affine-curve solver on supplied trees, with `O(n log^2 n)` charged word
  work and storage. Local discovery at the OP3 work scale remains open.
- [`LOCAL_CYCLE_PROBE.md`](LOCAL_CYCLE_PROBE.md): an exact local solver on
  cycles with unequal pendant-leaf counts and an arbitrary seed, reaching
  the `O_tilde(1/eps_appr)` ACL scale on this promised family. The proof
  includes event location, cycle closure, degree queries and output work.
  An exact length-two-attachment witness blocks a naive extension.
- [`BOUNDED_ATTACHMENT_PROBE.md`](BOUNDED_ATTACHMENT_PROBE.md): a locally
  discovered cycle with finite tree attachments and a cycle seed. Retaining
  only changing responses gives `O_tilde(q^3/eps_appr)` work, with attachment
  size q discovered by the algorithm. This reaches the target scale for
  each fixed q; reading large inactive attachments remains a locality gap.
- [`TWO_PORT_FRONTIER_PROBE.md`](TWO_PORT_FRONTIER_PROBE.md): an implemented
  exact local solver when the positive support contains at most one nonseed
  vertex of degree at least three. Two retained vertices, immediate path
  elimination and a persistent planar reporter give
  `O((1+vol(S)) log^4(2+vol(S)))` work, without inactive row scans or
  attachment-size dependence. It handles shared candidates and multiple cycles.
- [`BRANCH_CORE_FLUX_PROBE.md`](BRANCH_CORE_FLUX_PROBE.md): an implemented
  ACL solver with a growing retained branching core. Physical-edge fluxes
  use scalar publication queues, giving `O_tilde((1+r^2)/eps_appr)` work
  and `O(vol(U)+r^2)` storage. It includes arbitrary shared frontier gates
  and scans only positive rows. The dense core factor remains explicit.
- [`LIVE_CORE_PEELING_PROBE.md`](LIVE_CORE_PEELING_PROBE.md): removes
  settled vertices of current reduced degree at most two, moving at most
  one grouped physical flux. Its bound uses maximum live-core size q:
  `O_tilde((1+q^2)/eps_appr)`. A source-valid tree family shows why q need
  not be small, even under depth-first admission.

The formal statements are `thm:op3-persistent-tree`,
`thm:op3-local-cycle`, `cor:op3-local-cycle-acl`,
`thm:op3-bounded-attachments`, `thm:op3-two-port-frontier`,
`thm:op3-branch-core-flux`, and `thm:op3-live-core-peeling` in `main.tex`.
The implementations pass 1,152
tree, 5,265 leaf-cycle, and 1,909 bounded-attachment exact comparisons, plus
the larger KKT diagnostics recorded with each audit. The two-port solver
adds 8,329 exact comparisons and nine larger KKT cases; its planar reporter
passes 5,136 exact extreme queries and 1,606 static-chain comparisons.
`SCHUR_RELATIVE_REPORTER_PROBE.md` records why a constant-relative
approximate Schur-key reporter does not by itself preserve ACL quietness.
The growing-core solver adds 27,120 exact comparisons, 17 additional
residual diagnostics, and separate intermediate flux/inverse checks.
`BRANCH_CORE_COST_AUDIT.json` confirms cubic work for its explicit inverse
backend on easy balanced trees; this identifies the next representation cost.
These drafts await independent review; arbitrary-graph OP3 remains open.
The live-core extension passes 54,240 exact comparisons and 50 additional
checks. Its ten implicit-tree width diagnostics show the remaining limit.
The root-threshold follow-up now gives exact resistance/group identities,
two exact-stopping counterexamples and a separate ACL counterexample.
Its audits cover 22,440 actual traces and 13,179 complete symbolic minimum
sequences; see `ROOT_THRESHOLD_ORDER_PROBE.md`. The next bounded target is
`ORDERED_PATH_CLUSTER_PROBE.md`. No new local tree work theorem is claimed.

## Latest complete tree result

**Proved here, awaiting independent review:** `thm:op3-local-top-tree`
gives a deterministic exact obstacle/ACL algorithm on arbitrary trees with
O(cvol(U) log^4(2+cvol(U))) local exact-real word work and
O(cvol(U) log^3(2+cvol(U))) space, including every retained version.
Graph discovery, home-edge payloads, failed queries, all cluster operations
and final output are charged. The source balancing algorithm is imported;
the complete application callbacks are implemented and exactly audited.
This implies O_tilde(1/eps_appr) tree ACL work and exact O_tilde(1/rho)
tree RPPR work in the nonzero regime. It is not a numerical-stability claim.

**Measured:** `TOP_TREE_CALLBACK_AUDIT.json` checks 650 source-valid faces,
167,384 legal binary joins, 26,130 independent Schur oracles, 168,294 valid
summaries, 650 exposure transitions and 1,296 payload refreshes. Supplied
hierarchy enumeration is reference work, not the published online algorithm.

**Proved here / Measured:** a uniform shift C=1/bar_alpha makes every
cluster load negative while allowing the physical seed to be interior.
The geometric root may therefore differ from the seed. The exact shifted
reporter and one-cycle restoration identities are in
`sec:op3-shifted-tree-clusters`; 564 faces check 33,550 conditional identities
and 1,972 valid physical-seed-interior clusters. Two cycle witnesses pass.

**Next Open target:** `UNICYCLE_TOP_TREE_PROBE.md` specifies local unicyclic
continuation: one exceptional two-parent candidate, a charged point query,
one paid re-rooting at cycle closure, two fixed cycle ports and the corrected
root solve. A triangle witness proves that the uncorrected spanning-tree
response can be negative; retain signed affine responses. Arbitrary-graph
OP3 remains Open. No result has been promoted to the active manuscript.

The latest structural theorem is now the full unicyclic extension:
`thm:op3-local-unicyclic` in `sections/op3_local_unicyclic.tex`, a proof draft
awaiting independent review. It gives the same O_tilde(1/eps_appr) local ACL
scale for arbitrary seeds and unbounded attachments, using the published
online top-tree source algorithm and exactly audited application code.
[`UNICYCLE_TOP_TREE_PROBE.md`](UNICYCLE_TOP_TREE_PROBE.md) records the
completed obligations. The next Open construction is
[`BOUNDED_CYCLE_RANK_PROBE.md`](BOUNDED_CYCLE_RANK_PROBE.md), which seeks a
paid extension to several locally exposed cycles. General OP3 remains Open.

The next extension is now proof-drafted as `thm:op3-local-cycle-rank`:
arbitrary graphs admit a fully charged local exact solve with work
O_tilde((1+r^3+q)/eps_appr), where r counts active cycles and q counts cycles
revealed by active-row scans. See
[`BOUNDED_CYCLE_RANK_PROBE.md`](BOUNDED_CYCLE_RANK_PROBE.md) and the exact
`LOCAL_CYCLE_RANK_CLUSTER_AUDIT.json`. The fast hierarchy is a source import;
reference rebuilds are not claimed as fast updates. Selected inverse entries
are now implemented and audited, giving the next Open transaction in
[`COARSE_INVERSE_UPDATE_PROBE.md`](COARSE_INVERSE_UPDATE_PROBE.md).
