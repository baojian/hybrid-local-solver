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
`O(q^-5)` coefficient is proved for the original score under arbitrary
projection. The exact projection-normal identity improves it to
`(C_n+1-q^2)/q^4` under the causal condition `n_i <= C_n b_i` on clipped
positive-residual rows; inactivity has `C_n=0`. A modified safe
positive-support envelope has coefficient
`(1-q^2)/q^4` under arbitrary projection; an exact three-vertex state explains
why clipped-zero residuals obstruct the same claim for the original score.
A reachable zero-start `K_{2,3}`-plus-seed-leaf family stays
projection-inactive through stage 4 and requires
`lambda(q) ~ 49/(3884 q^4)`. Hence the graph-uniform coefficient order is
exactly `Theta(q^-4)` for the support-aware ledger and the inactive original
subclass; the fixed-`r` `K_{2,r}` extension drives the graph-uniform leading
lower constant to `1/15`. These results do not imply convergence or a work bound, and reserve,
support, and gate evaluation must be charged when not cached.

These finite witnesses establish scoped GO/STOP statements for named
recurrences and event orders. They do not prove a convergence failure,
uniform recovery horizon, asymptotic work theorem, or finite-precision result.
The support-aware and inactive-original scalar coefficient order is now
closed. The remaining scalar gap is for the original all-coordinate score
under arbitrary projection: a reachable `Omega(q^-4)` lower order versus the
general `O(q^-5)` upper bound. The
unconditional zero-balance
`delta^2` all-history route and a small multiplier of this consumed-energy
reserve are both closed for the named recurrence and gate.
The direct critical endpoint-path attempt does not reach active projection:
exact threshold-tuned instances at `q=1/8,1/12,1/16` certify two vertices
before the intended full face. Bounding the normal-anchor ratio uniformly,
or finding a reachable family where it produces larger debt, is the remaining
scalar target.

The arbitrary-projection issue is now known to be genuinely reachable, not
merely algebraic. On one explicit 30-vertex point-seed graph at `q=12/625`,
the exact zero-start complete-gate trace reaches a clipped row whose post-step
residual is the positive all-coordinate maximum, with
`n_i/b_i=5.530040...` and strictly positive causal debt. Its actual required
coefficient is only `0.086694...`, or
`q^4 lambda=1.17814...e-8`; it therefore does not improve the existing
`Omega(q^-4)` lower order. An exact nine-point nearby-`q` screen is finite
only and supplies no asymptotic normal-anchor or debt scaling.

Build and audit from the repository root with:

```bash
make -C manuscript/notes/volume_gated_acceleration
uv run python -m experiments.proof_audits.runner \
  --tier full --note volume_gated_acceleration
```

The twelve mechanism-based exact-audit IDs are listed by
`make research-audit-list`; their provenance spans Rounds 013--024. The full
tier includes exhaustive connected labeled rooted graphs on two through five
vertices for `volume_gated_acceleration.nonpath_causal_stop`, plus every seed
of every connected NetworkX graph-atlas representative through order seven
for `volume_gated_acceleration.consumed_energy_reserve`. The latter also
checks the quartic family's exact formal series, rational replay grid, the
leading `K_{2,r}` formulas at six exact integer specializations, the
projection-normal identities, and three finite critical-path gate failures.
The new reachable-projection audit verifies the 32-stage chronology, strict
gate margins, clipped positive-residual row, positive debt, and optional
finite rational `q` screen.
