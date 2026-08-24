# Response-preconditioned hybrid note

This standalone note defines a common active-set interface for iterative
frontier repair and persistent settled-face response. The proof source is
`main.tex` and its included sections; [`STATUS.md`](STATUS.md) is the current
claim ledger and handoff.

The proved framework includes nested-face orthogonality, Schur-response and
boundary-variation ledgers, response-energy packing, fixed-face reporters,
and exact finite constructions on declared structured families. It also
records which operations must be charged: response applications, boundary
queries, fragment handling, replay, state writes, materialization, and output.

The current boundary is deliberately narrow. A reused four-decoder-norm state
does not determine every positive slack-weight refresh. Adding one canonical
pivot norm repairs the three-label bucket, while a general explicit linear
Gram-statistic state needs quadratic statistics in the label count. This is
not an unrestricted real-cell lower bound. Maintaining richer measurements
output-sensitively on high-rank nonequitable cores, and composing them into a
graph-uniform RPPR solver, remain open.

The diagnostic backend in `src/hybrid_solver_codex/response_hybrid.py` and
driver `experiments/explore_response_hybrid.py` are dense correctness tools,
not output-sensitive implementations.

Build and audit from the repository root with:

```bash
make -C manuscript/notes/response_preconditioned_hybrid
uv run python -m experiments.proof_audits.runner \
  --tier full --note response_preconditioned_hybrid
```

The ten durable audit IDs cover fixed-face/path checks; frozen, scale-aware,
permutation, multiplicity, amplitude, asynchronous-column, and simultaneous-
batch reporters; the norm-only reweighting obstruction; and pivot/co-side Gram
refresh. `make research-audit-list` shows their Round 012--021 provenance.
The first eight are seeded numerical proof audits; the last two use exact
rational arithmetic. None supplies a finite-precision theorem or replaces the
LaTeX proofs.
