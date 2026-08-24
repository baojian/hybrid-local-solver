# AESP-CD RPPR note

This standalone note develops a composite AESP outer loop with local proximal
coordinate descent for the shared regularized PageRank model. The proof source
is `main.tex` and its included sections; [`STATUS.md`](STATUS.md) is the
current claim ledger and handoff.

The note proves the local KKT-mass and relative-oracle interfaces, safe lower
centers and retraction, fixed-envelope locality, finite residual identities,
several exact trajectory calibrations, and an unconditional accelerated result
on the a-posteriori high-Dirichlet class. It also records sharp failures of
raw correction counting, Euclidean-only collateral packing, black-box
shadowing, and the simplest unsplit lagged energy bank.

The live target is a windowed, spectrally split, nonlinear, or differently
normalized low-Dirichlet Lyapunov for the actual finite safeguarded sequence.
No graph-uniform exact accelerated solver or unconditional
`O_tilde(1/(rho*sqrt(alpha)))` end-to-end theorem is claimed. In particular:

- the abstract ledger witness is not an RPPR instance or an exact-proximal
  trajectory;
- the finite P4/P7 traces prove no infinite periodicity and no finite-inner
  work theorem;
- the fixed-P4 theorem refutes a horizon-uniform inflation bound while its
  primal error still converges geometrically, so it is not a net-exponent
  counterexample;
- the retraction discontinuity is a STOP for black-box shadowing, not a
  counterexample to direct finite-sequence packing or a graph-uniform solver
  theorem;
- entry-dominated stages and persistent-row energy now have explicit charges,
  but the low-Dirichlet nonlinear transfer remains open.

Build the note from the repository root with:

```bash
make -C manuscript/notes/aesp_cd_l1_rppr
```

Run all six exact audits with:

```bash
uv run python -m experiments.proof_audits.runner \
  --tier full --note aesp_cd_l1_rppr
```

Their durable IDs are:

- `aesp_cd_l1_rppr.safeguarded_outer_ledger` (Round 022 provenance);
- `aesp_cd_l1_rppr.fixed_operator_p4_tail` (Round 023);
- `aesp_cd_l1_rppr.retraction_and_fixed_face` (Round 024);
- `aesp_cd_l1_rppr.boundary_shielding_filter` (Round 025);
- `aesp_cd_l1_rppr.persistent_q_energy` (Round 026);
- `aesp_cd_l1_rppr.weighted_reserve_boundary` (Round 027).

The full tier includes the optional P7 corroborating trace. These audits check
the scoped exact identities and source guardrails; they do not promote the
open graph-uniform theorem.
