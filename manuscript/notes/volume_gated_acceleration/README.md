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

These finite witnesses establish scoped GO/STOP statements for named
recurrences and event orders. They do not prove a convergence failure,
uniform recovery horizon, asymptotic work theorem, or finite-precision result.
The live causal-ledger target is now a useful structural promised-class
condition, an explicitly justified reserve, or a stronger observable; the
unconditional zero-balance `delta^2` all-history route is closed for the named
recurrence and gate.

Build and audit from the repository root with:

```bash
make -C manuscript/notes/volume_gated_acceleration
uv run python -m experiments.proof_audits.runner \
  --tier full --note volume_gated_acceleration
```

The ten mechanism-based exact-audit IDs are listed by
`make research-audit-list`; their provenance spans Rounds 013--022. The full
tier includes exhaustive connected labeled rooted graphs on two through five
vertices for `volume_gated_acceleration.nonpath_causal_stop`.
