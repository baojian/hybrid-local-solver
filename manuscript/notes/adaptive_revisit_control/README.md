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
absorption-safe switching checkpoint.  Mergeable work countdowns give a
best-arm theorem, and irreversible activation tokens realize that condition
with `kappa = 1` on endpoint paths: common forward Schur records and one
reverse solve cost at most `4 / rho`.  A two-vertex activation-breakpoint
argument proves that a continuous numerical/energy potential cannot pay
fixed activation work uniformly.

The portfolio inherits any `O_tilde(V_loc / sqrt(alpha))` bound possessed by one
of its arms, but it does not prove that the literal adaptive ladder or
two-rung SOR has such a graph-uniform bound.  In fact, the updated note proves
two exact obstructions.  On one edge, a support-safe fixed-band two-rung
handoff can skip spreading and take `Omega(1 / alpha)` exact-delivery work at
fixed regularization and accuracy.  On a finite unweighted RPPR tree, two
legal exact boundary-batch orders with the same terminal point have settled
revisit factors separated by at least `(L + 1) / 5`.  The remaining positive
target is therefore an order-independent activation-once transport
representation, or a quantitatively forced-spreading arm, for general
branching and cyclic graphs.

Build from this directory with:

```bash
make
```
