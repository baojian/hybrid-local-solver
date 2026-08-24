# Direction status: response_preconditioned_hybrid

Last reviewed: 2026-08-24
State: proved-open

## Exact question and contract

- **Question:** Can settled-face response state and iterative frontier repair
  be composed without repeated old-face solves, dense boundary scans, or
  uncharged materialization?
- **Model:** Shared exact-real PageRank/RPPR principal systems with nested
  active faces, persistent Schur or harmonic response state, and a newly
  admitted iterative frontier. Structured reporter theorems use their stated
  notched-sun template, schedule, amplitude, and batching contracts.
- **Accuracy namespace:** Each theorem states its own residual, slack, or
  crossing margin; no numerical proof audit is promoted to a finite-precision
  guarantee or silently identified with `eps_ppr`.
- **Access and charged work:** Adjacency exposure, response construction and
  application, source/target measurements, fragments, validation, replay,
  state reads/writes, materialization, and output are charged separately.
- **Intended result:** An output-sensitive persistent-response backend whose
  total work composes with the local iterative product scale.

## Claim ledger

- **Source:** Schur complement, grounded-Laplacian, Chebyshev, and dynamic
  spectral machinery are imported only where cited; the graph-local
  implementation target is not a source theorem.
- **Proved here:** Nested response/correction orthogonality, dual locality,
  boundary variation and leverage/energy packing, fixed-face aggregate flush
  and reporter interfaces, and the structured notched-sun reporter chain from
  fixed order through positive amplitudes, independent columns, and atomic
  simultaneous batches. Exact algebra shows that four fixed decoder norms do
  not determine a genuine three-label slack reweight; one pivot norm repairs
  that collision, and the general explicit co-side Gram construction uses
  quadratic statistics.
- **Conditional:** The mixed solver reaches a graph-uniform local bound only
  if those measurements and refreshes can be maintained output-sensitively on
  changing high-rank cores, or if a paid partial-flush/rebuild schedule is
  proved.
- **Measured:** Seeded binary64 audits reproduce the Round-012--019 structured
  calculations. They are numerical proof audits, not theorem evidence beyond
  the exact statements they check.
- **Refuted:** Pure geometric sleep on the singleton path, eager exact slack
  vectors on the frozen notched sun, and reuse of the norm-only three-label
  state after genuine positive reweighting. The four-label witness refutes the
  one-pivot five-scalar repair, not arbitrary real-cell states.
- **Open:** A sparse collision-sensitive invariant or geometric paid
  replay/rebuild policy that survives repeated slack-weight changes while
  charging richer measurements, old-cut reads, validation, workspace, and
  decoder output.

## Central blocker

The current explicit general repair keeps `Theta(k^2)` Gram statistics and
needs richer per-label measurements or quadratic append arithmetic when the
code family is large. The next proof must either sparsify that state according
to actual collisions or show that full aggregate refreshes occur
geometrically, with every intervening partial query output-sensitive. No
current theorem supplies that dynamic high-rank implementation.

## Dependencies and reusable outputs

- Formal registry dependencies: `incremental_active_set_sdd`,
  `propagate_settle_framework`, `volume_gated_acceleration`,
  `aesp_cd_l1_rppr`, `evolving_support_cg`, and
  `delayed_reflection_ladder`.
- Source/shared prerequisites: Shared PageRank/RPPR formulation, accuracy
  namespaces, adjacency model, eleven-resource order, and cited response and
  spectral primitives.
- Supplies to: The mixed architecture and any direction needing charged
  settled-anchor/frontier composition, finite-band reporting, or replay
  boundaries.

## Resume here

- Exact file/section/lemma: Start with
  `thm:three-label-pivot-gram-refresh`, `thm:co-side-gram-refresh`,
  `prop:four-label-one-pivot-refresh-obstruction`, and the preceding batched
  columnwise reporter chain.
- Next concrete action: Test a sparse collision-aware subset of the co-side
  state, or a geometric paid replay policy, on at least two genuine weight
  refreshes of a high-rank collision pattern.
- Stop/go test: Go if full flushes are geometric and partial queries cost only
  polylogarithmic overhead plus packed validation/output. Stop if every light
  admission triggers a product-scale flush.

## Verification

- Source pointers checked: `README.md`, `main.tex` and included sections,
  `registry.toml`, and shared problem/results ledgers.
- Focused checks: Ten registered `response_preconditioned_hybrid.*` audits
  cover the Round-012--021 mechanisms. Run the recorded full tier with
  `uv run python -m experiments.proof_audits.runner --tier full --note
  response_preconditioned_hybrid`.
- Review status: The numerical audits retain fixed seeds and trial counts; the
  final two use exact rational arithmetic. Prior independent review qualified
  the Gram-state necessity claim to explicit linear statistics. This
  reorganization changes no theorem or claim scope.
- Known gaps: The dense diagnostic backend is not output-sensitive; no
  unrestricted information lower bound, graph-work theorem, RPPR completion,
  or finite-precision theorem is claimed.
