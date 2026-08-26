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
`O(q^-5)` coefficient and a low-frequency `O(q^-3)` coefficient are proved for
the scalar account.  These do not imply convergence
or a work bound, and
reserve evaluation must be charged when the restricted optimum and energy are
not cached.

These finite witnesses establish scoped GO/STOP statements for named
recurrences and event orders. They do not prove a convergence failure,
uniform recovery horizon, asymptotic work theorem, or finite-precision result.
The live causal-ledger target is now to prove the stated low-frequency
condition on a useful reachable promised class, close the gap between the
`q^-3` star lower order and `q^-5` unconditional sufficient coefficient, or
find a stronger exact obstruction.  The unconditional zero-balance
`delta^2` all-history route and a small multiplier of this consumed-energy
reserve are both closed for the named recurrence and gate.

Build and audit from the repository root with:

```bash
make -C manuscript/notes/volume_gated_acceleration
uv run python -m experiments.proof_audits.runner \
  --tier full --note volume_gated_acceleration
```

The eleven mechanism-based exact-audit IDs are listed by
`make research-audit-list`; their provenance spans Rounds 013--023. The full
tier includes exhaustive connected labeled rooted graphs on two through five
vertices for `volume_gated_acceleration.nonpath_causal_stop`, plus every seed
of every connected NetworkX graph-atlas representative through order seven
for `volume_gated_acceleration.consumed_energy_reserve`.
