# Direction status: hybrid_aesp_locsor

Last reviewed: 2026-08-24
State: proved-open

## Exact question and contract

- **Question:** Can an accelerated signed burn-in hand off to a momentum-free
  local or persistent-response tail with graph-uniform product-scale work and
  no replay of the prefix?
- **Model:** The general note treats single-seed PPR with AESP followed by
  omega-one LocSOR, and RPPR with composite Catalyst followed by proximal
  local refinement. Exact-real structured results cover the center-seeded
  three-arm spider, branch-seeded double-Y, and fixed-`m` branch caterpillar
  under their explicit `alpha`, `rho`, seed, gate, and admission-order ranges.
- **Accuracy namespace:** PPR uses the note-scoped degree-normalized gradient
  certificate `eps_ppr`. RPPR uses a weighted fixed-point residual `eps_sol`;
  exact response arms have zero proximal residual. No RPPR-to-PPR conversion
  is implicit.
- **Access and charged work:** Coordinate work costs `d_u`, batched work costs
  `vol(S)`, and the fully charged prefix includes discovery, row reads,
  numerical recurrence, queue/gate/certificate work, response operations,
  state writes, validation, materialization, and output in the shared
  eleven-resource order.
- **Intended result:** A graph-uniform
  `O_tilde(1/(sqrt(alpha)*eps_ppr))` PPR solver, or the analogous
  `O_tilde(1/(rho*sqrt(alpha)))` RPPR solver, with one complete terminal
  certificate and return.

## Claim ledger

- **Source:** The locally evolving-set, AESP, LocSOR, RPPR/Catalyst, and
  Stieltjes-system ingredients are source results mapped in the note and
  project literature files.
- **Proved here:** Finite convergence after every finite signed handoff;
  objective-gap and weighted-gradient-mass tail bounds; a general
  trajectory-dependent handoff theorem; and exact, fully charged common-state
  response handoffs on the three-arm spider, double-Y, and strict canonical
  branch-caterpillar ranges. On the caterpillar, the note proves lower-point
  gates, all-face lower-state transport, local residual-heap maintenance,
  lazy face carry, sparse settled auxiliary appends, and two actual
  nonsettled continuations. The settled three-vertex reset audit proves the
  observable budget/drop ratio is `Theta(1/alpha)`, while the actual
  analytical shock is below a constant multiple of the drop. The literal
  no-sharing two-product register reads `6m^2+12m-6` stored rows, explicitly
  as a representation-specific identity.
- **Conditional:** The trajectory-dependent theorem yields the target
  product scale under a graph-independent early-AESP locality bound. The
  multi-reset nested telescope is conditional on exact settlement and ordered
  lower-center identities absent from the current nonsettled execution, and
  has coefficient `Theta(alpha^-2)`.
- **Measured:** The imported AESP experiments motivate early acceleration;
  they do not establish the locality lemma or end-to-end work theorem.
- **Refuted:** Uniform one-coordinate weighted-L1 contraction, the uncapped
  “any finite burn-in” work claim, shock-free transport of all accelerated
  state, and alpha-uniform or `O(1/sqrt(alpha))` additive payment of the
  declared observable settled reset budget. These STOPs are not solver or
  work lower bounds.
- **Open:** A graph-independent early-prefix bound or alternative burn-in
  work argument; a nonadditive/logarithmic ledger for observable reset budgets
  over multiple actual nonsettled transitions; adaptive row exposure; and a
  graph-uniform composition including all margin, response, validation,
  memory, and output charges.

## Central blocker

The promotion gate remains unchanged. Do not promote the universal
`O_tilde(1/(sqrt(alpha)*epsilon))` work claim until either

```text
Lambda_J = max_{1 <= t <= J} overline_vol(S_t) / gamma_t
         = O(1/epsilon)
```

is proved with a graph-independent hidden constant, or a correct weaker
structural condition or alternative burn-in work argument sufficient for the
manuscript theorem is proved. Until then, only the proved
trajectory-dependent theorem and explicitly conditional confinement
corollaries may be used. The latest reset-budget STOP narrows the search away
from simple additive payment; it does not close or refute the promotion gate.

## Dependencies and reusable outputs

- Formal registry dependencies: `adaptive_revisit_control` and
  `aesp_cd_l1_rppr`.
- Source/shared prerequisites: Source AESP/locally-evolving-set and LocSOR
  analyses, RPPR support facts, the safe-center/relative-oracle interfaces,
  and the canonical structured reporters imported explicitly in `main.tex`.
- Supplies to: The synthesis and response-composition directions: exact
  resource ledgers, charged common-state conversions, incremental lower gates,
  sparse face-transition mechanisms, nonsettled continuation examples, and
  the settled reset-budget boundary.

## Resume here

- Exact file/section/lemma: Start with
  `sec:settled-reset-budget-amortization`,
  `prop:path-three-settled-reset-drop-obstruction`,
  `lem:settled-reset-optimum-drop-bound`,
  `prop:conditional-nested-reset-budget-telescope`, and the preceding
  nonsettled continuation sections in `main.tex` and its included files.
- Next concrete action: Test a nonadditive or logarithmic reset ledger on the
  actual Round-020/021 nonsettled branch-caterpillar trajectory, preserving
  every residual, row exposure, product, state write, and margin factor.
- Stop/go test: Go only if the same declared ledger survives at least two
  actual nonsettled admissions with graph-independent constants and yields a
  charged prefix bound. Stop if it assumes exact settlement, uses an unknown
  optimum as an algorithmic certificate, pre-exposes uncharged rows, or turns
  the observable `Theta(1/alpha)` budget ratio into a work lower bound.

## Verification

- Source pointers checked: `README.md`, `main.tex` and included sections,
  `registry.toml`, the shared problem/results ledgers, and the Round-022 record.
- Focused checks: The nine exact audits are registered under durable
  `hybrid_aesp_locsor.*` IDs in
  `experiments/proof_audits/registry.toml`. Run all of them with
  `uv run python -m experiments.proof_audits.runner --tier full --note
  hybrid_aesp_locsor`.
- Review status: The prior Round-022 independent review rederived the path
  demands, Schur drop, observable reset, asymptotics, conditional telescope,
  and literal product count, and required explicit scope that the result is
  neither a work lower bound nor a necessity result for other
  representations. This structural reorganization changes no theorem,
  equation, or claim status.
- Known gaps: The structured response handoffs are exact-real,
  family-specific RPPR statements; the composite prefix covers only its
  stated `alpha` range; candidate rows remain pre-exposed in the generic
  growing-face policy; and no graph-uniform accelerated-energy or
  finite-precision theorem follows.
