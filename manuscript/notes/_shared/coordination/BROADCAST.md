# Controller broadcast

**Verified snapshot:** 2026-08-24. **Active dispatch:** none. Do not open a new
research round automatically.

This file contains only what every direction needs now. Immutable review and
redistribution history lives in [`rounds/`](rounds/); detailed current proof
state lives in each direction's `STATUS.md`; formal roles and dependencies
live in [`../../registry.toml`](../../registry.toml).

## Global contract

- The end-to-end target is exact-real sparse PPR output with one terminal
  certificate and charged work
  `nnz(s)+O_tilde(1/(sqrt(alpha)*eps_ppr))` under adjacency-list access.
- Every discovery, repeated row read, numerical/response operation, rekey,
  certificate query, state access, validation, materialization, and output
  write is charged.
- An RPPR route states its regularization/bias conversion and terminal
  certificate. Accuracy namespaces are never silently identified.
- A STOP for a named recurrence, state representation, graph family, or finite
  trace is not a class lower bound.

## AESP--LOCSOR gate

The graph-uniform end-to-end claim remains open. Do not promote it until

```text
Lambda_J = max_{1 <= t <= J} overline_vol(S_t) / gamma_t
         = O(1/epsilon)
```

is proved with a graph-independent hidden constant, or a correct weaker
structural condition or alternative burn-in work argument sufficient for the
manuscript theorem is proved. The trajectory-dependent theorem and explicitly
conditional confinement corollaries remain usable. See the current
[`hybrid_aesp_locsor` handoff](../../hybrid_aesp_locsor/STATUS.md).

## Latest accepted boundary: Round 027

The AESP-CD direction now has an actual-finite lagged Euclidean reserve, but
its graph-uniform drift is only order `q^2`. The simplest correctly lagged
unsplit `q^-1 Q` reserve cannot have a uniform one-step accelerated
contraction while also carrying enough coefficient to pay the reachable K8
pulse. The complementary persistent K2 witness still decays globally at the
accelerated rate after logarithmic startup, and the K8 high-band payment ratio
tends to `14641/32256`.

Consequently, the live AESP route is a windowed, spectrally split,
nonlinear-transfer, or differently normalized low-Dirichlet Lyapunov. Round
027 proves no additive-resistant obstruction, graph-uniform net exponent,
solver theorem, resource vector, or finite-precision result. Exact formulas,
index repairs, and independent review are preserved in
[`Round 027`](rounds/2026-08-23-round-027.md) and the current
[`AESP-CD handoff`](../../aesp_cd_l1_rppr/STATUS.md).

## Cross-direction priorities

| Owner | Next falsifiable target |
| --- | --- |
| `aesp_cd_l1_rppr` | A finite windowed/spectral/nonlinear low-Dirichlet net exponent retaining every residual and correction. |
| `hybrid_aesp_locsor` | A nonadditive/logarithmic reset ledger across multiple actual nonsettled admissions. |
| `volume_gated_acceleration` | All-history causal solvency under a declared structural condition, or durable multi-admission debt. |
| `response_preconditioned_hybrid` | Sparse collision-sensitive refresh state or a geometrically paid replay theorem. |
| `propagate_settle_framework` | A new cyclic coupling or bounded-degree settlement gadget with seed chronology proved before reporter analysis. |
| `local_solver_oracle_hierarchy` | A lower-bound model that defeats residual-slack spreading and sparse-basis delayed synthesis, or a justified narrower class. |

## Reuse and routing rules

- Import a result only from its proof-owning note and keep its stated graph,
  seed, parameter, access, evidence, and output scope.
- `registry.toml` records only direct formal proof or construction imports;
  motivation and historical provenance do not create dependency edges.
- The shared results ledger may summarize reusable conclusions, but it does
  not override a direction's proof source or `STATUS.md`.
- Exact and numerical claim checks are registered under
  [`experiments/proof_audits`](../../../../experiments/proof_audits/README.md).
  Round numbers are provenance, not executable names.
- Controller validation remains `make note-audit`, `make test`, `make lint`,
  and the proportionate proof-audit/LaTeX targets for changed directions.
