# adaptive_revisit_control

This standalone note develops the theoretical direction suggested by the
frontier adaptive ladder's charge-weighted revisit memory.  It proves exactly
what the scalar revisit ratio records, refines it into a causal four-way
ledger that certifies neighbor-generated backflow after exact pushes, and
shows why the scalar alone cannot determine whether relaxation should be
raised or lowered.

Several positive safeguards are proved.  First, every causal variable-relaxation
controller clamped to `[1, 2 - delta]` terminates under the note-scoped live
degree-normalized residual gate, with a condition-free energy/work bound.
The same ledger gives a no-reset safeguard: cap an adaptive prefix, then
switch to exact Gauss--Seidel on the same state with a quantified near-baseline
ceiling.  Second, a branchable weighted portfolio of finitely many local
policies costs at most the best policy's work divided by its allocated share.  Uniform shares
give a best-of-`K` factor `K`; learned shares with a fixed exploration floor
retain a distribution-free per-instance guarantee.  Thus revisit learning can
improve allocation without being trusted for correctness or worst-case
safety.  A geometric restart portfolio also gives a `4K`-type best-arm bound
with only one live solver state, provided a clean instance reset is available.

For one irreversible common state, exact RPPR settlement is an
absorption-safe switching checkpoint. Under interference-monotone,
own-service-progress countdowns, the mergeable interface gives a best-arm
theorem. Irreversible activation tokens prove those conditions with
`kappa = 1` on endpoint paths: common forward Schur records and one reverse
solve cost at most `4 / rho`. They also give a `kappa = 1` common-state
countdown on the smallest genuinely branching family, a center-seeded
three-arm unweighted spider of arbitrary arm lengths. One exact affine
transfer product per actual arm prefix and two scalar root aggregates support
every legal certified boundary-batch order. Forward response records,
terminal recovery, control, adjacency exposure, state writes and storage, and
exact output are charged separately and total `O(C(S*)) = O(1 / rho)` in the
exact real-cell model. No arm-private trajectory or eager rekey of untouched
tips is hidden. The same token tightness survives on the double-Y seeded at
one branch vertex, `s=e_o`, with two adjacent degree-three branch vertices.
Four pendant-prefix products couple through a scalar core before the second
branch is admitted and a fixed
full-rank `2 x 2` Schur core afterward. Every legal committed batch updates
only these common records. Adjacency, gate/control, response construction,
updates and queries, state writes, persistent and transient cells, recovery,
validation, and exact output are separately charged and remain
`O(C(S*)) = O(1 / rho)`. The construction holds for `0 < rho < 1/3`; with
`zeta = (1 - alpha)/(1 + alpha)`, the explicit condition
`rho < zeta/[3(3 + zeta)]` forces every legal order to admit the second branch
and genuinely enter the rank-two phase. A two-vertex activation-breakpoint
argument proves that a continuous numerical/energy potential cannot pay
fixed activation work uniformly.

The growing-core test is now resolved negatively for one named state, not for
all implicit responses.  On an explicit degree-three branch caterpillar with
branch path `b_1,...,b_m`, branch seed `s=e_{b_1}`, fixed
`alpha in (0,1)`, and `0 < rho < rho_cat(m,alpha) <= 1/3`, an exact KKT
positive-subset policy may follow a legal singleton order that first admits
the whole backbone, then a length-`m` endpoint
arm, and finally the deferred pendant leaves.  The active response core
therefore reaches dimension `m`, while `m+1` positive leaf tips remain live.
Every long-arm admission strictly changes all of their exact demands.  The
literal `EagerTipKey` representation, which stores and refreshes one exact
cell per live tip with no lazy indirection, must perform at least `m(m+1)`
old-key writes.  A sequential exact implementation has exhaustive resource
vector
`(Theta(m), Theta(m), 3m+1, 0, Theta(m^2), 0, Theta(m^2), Theta(m), O(m), Theta(m), Theta(m))`
in the shared order
`(C_adj,R_adj,R_int,C_pre,C_ctl,C_rec,C_resp,M_pers,M_tmp,C_mat,C_emit)`.
The quadratic control coordinate is the eager rekey cost; the separate
quadratic response coordinate belongs to the chosen repeated linear
tridiagonal sweeps.  Full positive-tip lists at every checkpoint would add
quadratic output as well.
The threshold is defined separately for each fixed `m`; no positive
`m`-uniform `rho` range is claimed.  This chronology is not the canonical
all-violations batch, which may co-admit the deferred leaves once positive.

This obstruction does not apply to lazy affine keys, sign-persistence flags,
kinetic/group reporting, or on-demand implicit queries.  Eliminating the
actual pendant prefixes leaves an SPD tridiagonal branch system, and a
balanced affine-transfer tree supports one append/update or one named tip
query in `O(log(2+m))` exact operations with `O(m)` retained cells.  Every
requested tip must still be charged: querying all live tips along the witness
already makes `q = Theta(m^2)`.  A charge-comparable dynamic all-positive-tip
reporter for every legal order remains open.  At the first long-arm append,
one new activation cannot pay `m+1` old-key rewrites, explicitly violating the
ordinary linear activation-token template; pairwise rekey tokens pay the
execution only with quadratic initial mass.

For one explicit policy/interface, the implicit route is now positive.
`thm:branch-caterpillar-kinetic-delta-reporter` fixes the same branch seed,
fixed `m`, and family-dependent range of `rho`, and requires the exact-KKT
positive-subset policy to commit the backbone singletons
`b_2,...,b_m` before taking arbitrary nonempty subsets of the then-known
positive pendant tips.  This is not canonical all-violations batching.
`CaterpillarKineticDelta` uses the separable last Green column and a strict
crossing-key heap to retain the exact all-positive live-tip set.  It emits
only labels that newly become positive, supports exact membership and
proposed-batch checks, and never re-emits a still-live positive label merely
because its demand changes.  For `2m-1 <= J <= 3m`, one delta/certificate
exchange per committed batch plus one terminal return has exhaustive vector
`(Theta(m), Theta(m), J+1, 0, O(m log(2+m)), 0,
O(m log(2+m)), Theta(m), O(m), Theta(m), Theta(m))`.
This includes every transfer update and named query, heap/control operation,
stored-row validation, retained/scratch cell, exact candidate write, delta and
certificate label, reply header, and final output.  Total exact-cell work is
`O(m log(2+m)) = O(C(S*) log(2+C(S*)))`.  Requiring a complete positive-tip
list at every checkpoint can itself cost `Theta(m^2)` output.  No `kappa=1`,
arbitrary pre-backbone interleaving, finite-precision, conditioning, or
graph-uniform accelerated theorem is claimed.  The vector
counts the membership test for every proposed committed label; each additional
speculative/repeated membership call and any separate reply/round are added to
the control, interaction, and output coordinates.

The actual canonical all-violations policy is now closed on a smaller explicit
fixed-family subrange.  Define `rho_can(m,alpha)` as the minimum of `rho_cat`
and the affine strict-demand thresholds for the three vertices in each next
distance layer (`eq:branch-caterpillar-canonical-threshold`).  For
`0 < rho < rho_can(m,alpha)`, the canonical faces are
`U_k = B_(k+1) union A_k union {r_1,...,r_k}` and every one of the exactly `m`
batches has three labels: `{b_(k+2),a_(k+1),r_(k+1)}` until the final
`{a_m,r_m,r_(m+1)}` batch.  Thus every boundary vertex is newly live and its
row is first scanned at that checkpoint, although its label may have been
revealed one layer earlier.  Every such vertex is strict positive; positive
ties are co-admitted, equality is inactive, and the strict parameter promise
prevents equality on this trace.

`thm:branch-caterpillar-canonical-layer-reporter` gives the named exact-real
`CaterpillarCanonicalLayerDelta` implementation.  Early side leaves change
only their branch diagonal/load cell, a long-arm append adds one arm-transfer
cell and changes only the induced branch-core absorption cell at `b_1`, and a
backbone append adds one tridiagonal cell.
Balanced transfer updates and at most two parent-coordinate queries per batch
therefore cost `O(log(2+m))`.  The exhaustive vector is
`(Theta(m), Theta(m), m+1, 0, Theta(m), 0,
O(m log(2+m)), Theta(m), O(m), Theta(m), Theta(m))` at
`eq:branch-caterpillar-canonical-eleven-vector`, including every exact demand
test, delta/certificate reply, retained and scratch cell, terminal recovery,
validation, candidate write, and exact output.  Total work is
`O(m log(2+m)) = O(C(S*) log(2+C(S*)))`.  The theorem fixes the branch seed,
fixed `m`, the family-dependent strict range `rho < rho_can`, exact-real
arithmetic, canonical batching, and a delta interface.  It makes no claim for
the rest of `rho < rho_cat`, other seeds or policies, a uniform positive
`rho` range, finite precision, conditioning, `kappa=1`, PPR conversion, or
product-scale work.

The portfolio inherits any `O_tilde(V_loc / sqrt(alpha))` bound possessed by one
of its arms, but it does not prove that the literal adaptive ladder or
two-rung SOR has such a graph-uniform bound.  In fact, the updated note proves
two further exact obstructions.  On one edge, a support-safe fixed-band two-rung
handoff can skip spreading and take `Omega(1 / alpha)` exact-delivery work at
fixed regularization and accuracy.  On a finite unweighted RPPR tree, two
legal exact boundary-batch orders with the same terminal point have settled
revisit factors separated by at least `(L + 1) / 5`.  The remaining positive
target is therefore an implicit reporter for the canonical range
`rho_can <= rho < rho_cat`, arbitrary pre-backbone interleavings, or a
quantitatively forced-spreading arm. Cycles, finite precision, bit
complexity, and any `rho`-to-`eps_ppr` conversion remain open.

Build from this directory with:

```bash
make
```
