# Volume-gated acceleration research note

This standalone note studies active-volume flattening, RPPR safe support
gates, and accelerated continuation across expanding principal subspaces. The
proof source is `main.tex` and its included sections;
[`STATUS.md`](STATUS.md) is the current claim ledger and handoff.

The note proves the `1/rho` safe-support cap, exact path conditioning and
admission identities, response-assisted append-only path continuations, and a
sequence of exact finite stress tests for correction/error banks. Those tests
separate held-face evolution, admission resets, follow-up recovery, and causal
credit. On the named `q=1/5` path, old causal credit remains solvent while a
restart needs several stages to recover. An asymmetric six-vertex T tree
shows that the same restarted causal gate can remain negative through the
next admission. A second exact six-vertex trace starts the ledger at the
actual zero initialization, retains all credit from three consecutive
singleton admissions, and still becomes negative for two held checkpoints.
It therefore refutes unconditional zero-balance all-history solvency for the
named `delta^2` ledger.

The note then tests the narrowest causal energy repair.  The reserve
`R_k = E_0 + D_k - E_k` stores only transported-center energy already consumed
by executed fixed-face contractions; exact transported admissions leave it
unchanged.  A unit coefficient repairs the six-vertex trace, and coefficient
`3` repairs every rooted connected graph-atlas trace through order seven at
`q=1/5`.  An exact leaf-seeded `K_{1,4}` family nevertheless forces the
minimum coefficient to grow as `1/(32 q^3)`, ruling out a constant or
polylogarithmic multiplier uniformly in `q`.  The named complete gate
preserves the score exactly across admission. On its interior traces, a coarse
`O(q^-5)` coefficient follows from the baseline energy comparison. The exact
projection-normal identity improves it to `(C_n+1-q^2)/q^4` under the causal
condition `n_i <= C_n b_i` on clipped positive-residual rows; inactivity has
`C_n=0`. A modified safe positive-support envelope has coefficient
`(1-q^2)/q^4` under arbitrary projection. For the declared point-seed
parameters `rho=tau=q/5` with an interior initial singleton, a first-admission
energy floor pays every
clipped-zero residual and proves the same `(1-q^2)/q^4` coefficient for the
original all-coordinate score under arbitrary projection.
A reachable zero-start `K_{2,3}`-plus-seed-leaf family stays
projection-inactive through stage 4 and requires
`lambda(q) ~ 49/(3884 q^4)`. Hence the graph-uniform coefficient order is
exactly `Theta(q^-4)` for both the support-aware and original ledgers, even
with arbitrary projection; the fixed-`r` `K_{2,r}` extension drives the
graph-uniform leading
lower constant to `1/15`. These results do not imply convergence or a work bound, and reserve,
support, and gate evaluation must be charged when not cached.

For the same exact-real point-seed recurrence, the transported shock budget
does yield a separate convergence result.  At `rho=tau=q/5`, the exact
identity for `E_0+D_k` is at most `q^2` on every graph.  Once a fixed face has
contracted below `4q^10/(25(1+q^2)(1+3q^2)^2)`, a direct residual bound makes
the original safe envelope certificate-safe on every active row.  The
complete gate must then either admit a nonempty violating batch or certify
globally.  Thus each face is held for at
most `O(q^-1 log(1/q))` steps, the whole finite execution has
`T=O(q^-2 log(1/q))` and swept active volume
`O(q^-3 log(1/q))`, and its terminal PPR error is at most `2q/5`.  A fully
charged dense-response exact-real fallback has the same
`O(q^-3 log(1/q))` arithmetic order and `O(q^-2)` persistent storage.  This
is graph-uniform finite convergence and an honest fallback work bound, but it
remains a factor `O_tilde(q^-1)` above the desired product-scale work and
supplies no finite-precision or bit-complexity guarantee.

That logarithm belongs to the named fixed-step candidate-envelope policy, not
to a dense exact-response implementation per se.  If a policy is allowed to
gate directly on the fully materialized exact restricted optimum that dense
center transport already computes, its safe-envelope correction is zero and
it can run the same complete gate immediately on every face.  This exact
active-set comparator uses `O(q^-2)` cumulative gate scans and
`O(q^-3)` dense factor/solve arithmetic, removing the hold logarithm but not
the extra polynomial response factor.  It is a different control policy, not
a sharper chronology theorem for the named recurrence.

The dense-response factor is intrinsic to the fallback's explicit scalar
Cholesky representation.  On any fixed-gap family of 3-regular `n`-vertex
spectral expanders, take `q=1/(2n)`.  A resolvent estimate puts every normalized RPPR
coordinate strictly more than `tau=q/5` above zero, so the same terminal
certificate forces the active face to become all `n` vertices.  Linear
treewidth and strict Stieltjes fill then require `Omega(n^2)=Omega(q^-2)`
explicit factor cells and `Omega(n^3)=Omega(q^-3)` ordinary scalar pivot
arithmetic even with the best offline ordering.  This rules out a
product-scale implementation only in the exact original-basis explicit
Cholesky/LDL response class.  It does not prove the per-face logarithm
necessary and leaves compressed, matrix-free, iterative, approximate, and
other non-Cholesky responses open.

On structured graphs that remaining factor can be removed without hiding
response materialization.  A fresh leaf-elimination solve, full materialized
state, and complete scan on every comparator face cost `O(q^-2)` in total on
every tree.  Fresh block--cut decomposition and dense leaf-block elimination
cost `O(b^3 q^-2)` when every biconnected block has size at most `b`, hence
product scale up to polylogarithms for polylogarithmic `b`.  On endpoint
paths, the append-only tridiagonal records already proved in this note give
the same fully charged `O(q^-2)` bound; all faces are prefixes and every batch
is a singleton.  Under the exact
shared/source KKT map, the companion activation-once path solver implements
the identical gate trace with one final reverse materialization in only
`O(q^-1)` charged work.  Companion lazy-response results separately solve the
same terminal RPPR task in `O_tilde(q^-2)` work on arbitrary trees and on
polylogarithmic-size biconnected blocks.  Those latter algorithms generate
their own response traces and therefore are not complexity theorems for this
note's literal comparator batches.  No cited backend supplies the complete
changing-face violation interface on arbitrary cyclic graphs, so that
graph-uniform composition remains open.

The finite witnesses establish scoped GO/STOP statements for named
recurrences and event orders. By themselves they prove no convergence
failure or uniform recovery horizon; the separate transported-energy theorem
above supplies the graph-uniform soft horizon without turning any finite
witness into an asymptotic claim.  Product-scale work is now closed for the
exact-optimum comparator on trees and polylogarithmic-size biconnected blocks,
and for the response-generated terminal task on the imported structured
classes, but remains open for the named recurrence and for the exact
comparator on arbitrary cores.  Every finite-precision
result remains open.
The support-aware and original all-coordinate scalar coefficient orders are
now closed at `Theta(q^-4)`, including arbitrary projection in the theorem's
interior point-seed scope. The
unconditional zero-balance
`delta^2` all-history route and a small multiplier of this consumed-energy
reserve are both closed for the named recurrence and gate.
The direct critical endpoint-path attempt does not reach active projection:
exact threshold-tuned instances at `q=1/8,1/12,1/16` certify two vertices
before the intended full face. The normal-anchor identity remains a useful
step-local refinement, but no uniform bound on that ratio is needed for the
all-history scalar order.

The arbitrary-projection issue is now known to be genuinely reachable, not
merely algebraic. On one explicit 30-vertex point-seed graph at `q=12/625`,
the exact zero-start complete-gate trace reaches a clipped row whose post-step
residual is the positive all-coordinate maximum, with
`n_i/b_i=5.530040...` and strictly positive causal debt. Its actual required
coefficient is only `0.086694...`, or
`q^4 lambda=1.17814...e-8`; it therefore does not improve the existing
`Omega(q^-4)` lower order. An exact nine-point nearby-`q` screen is finite
only and supplies no asymptotic normal-anchor or debt scaling; the scoped
quartic theorem pays this event through the consumed first-admission reserve.

Build and audit from the repository root with:

```bash
make -C manuscript/notes/volume_gated_acceleration
uv run python -m experiments.proof_audits.runner \
  --tier full --note volume_gated_acceleration
```

The fifteen mechanism-based exact-audit IDs are listed by
`make research-audit-list`; their provenance spans Rounds 013--027. The full
tier includes exhaustive connected labeled rooted graphs on two through five
vertices for `volume_gated_acceleration.nonpath_causal_stop`, plus every seed
of every connected NetworkX graph-atlas representative through order seven
for `volume_gated_acceleration.consumed_energy_reserve`. The latter also
checks the quartic family's exact formal series, rational replay grid, the
leading `K_{2,r}` formulas at six exact integer specializations, the
projection-normal identities, the first-admission quartic constants, and
three finite critical-path gate failures.  The Round-026 exact scalar audit
checks the expander normalization and RPPR margin constants together with the
filled-clique storage and scalar pivot-update identities.
The Round-027 structured-response audit checks the exact shared/source
parameter and KKT map, strict gate equivalence, and face/product constants.
The reachable-projection audit verifies the 32-stage chronology, strict
gate margins, clipped positive-residual row, positive debt, and optional
finite rational `q` screen.
