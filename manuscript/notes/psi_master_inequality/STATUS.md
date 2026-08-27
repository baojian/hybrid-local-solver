# Direction status: psi_master_inequality

Last reviewed: 2026-08-27
State: proved-open
Agent family: codex
Role: direction
Branch: `agent/codex/psi-master-inequality`
Base commit: `4a979a6907880fb2dc76d1c51dbb7d12dc8bd5b3`
Allowed write scope: `manuscript/notes/psi_master_inequality/` and `docs/coordination/handoffs/psi-master-inequality.md`

## Exact question and contract

- **Question:** When is the exact one-step master form `Psi` nonpositive for
  every admissible clipped state?
- **Model:** Source-aligned RPPR and the precisely reconstructed Fable
  accelerated proximal recurrence.
- **Accuracy namespace:** A note-scoped Lyapunov absorption certificate; it is
  not identified with an unresolved global stopping rule.
- **Access and charged work:** The first task is an analytic trajectory
  inequality.  Any algorithmic corollary must separately charge graph access,
  clipping, face changes, and inverse primitives.
- **Intended result:** A theorem for a nontrivial infinite graph family, a
  verifiable structural condition, or an exact counterexample.

## Claim ledger

- **Source:** Fable's iteration-7 master identity is the starting exploratory
  claim; its finite exact decisions remain read-only evidence.
- **Proved here:** The degree-scaled recurrence and its full algebraic cap
  domain; the exact identity
  `V(h_(t+1),h_t)-(1-q)^2 V(h_t,h_(t-1))=Psi(y_t,h_t)`; the equivalent
  clip/slack decomposition; and nonpositivity for the two unmixed channels
  `y>=0` and `y<=0` under `mu_2>=2q`.
- **Conditional:** None yet.
- **Measured:** None yet.
- **Refuted:** None yet.
- **Open:** Analytic nonpositivity beyond finitely enumerated examples.

## Central blocker

Control the mixed-sign clipping term without exponential enumeration.  The
identity itself is now reconstructed; the live route is a covariance or
positive-association condition that can be proved on an infinite family.

## Dependencies and reusable outputs

- Formal registry dependencies: `aesp_cd_l1_rppr`.
- Source/shared prerequisites: source-aligned RPPR definition.
- Context/provenance: Fable iteration-7 files are read-only exploratory evidence.
- Supplies to: safeguarded acceleration and graph-family absorption analyses.

## Resume here

- Exact file/section/lemma: `lem:psi-master-identity` and
  `eq:psi-slack-decomposition` in `main.tex`.
- Next concrete action: derive the mixed-clipping kernel condition and prove
  it analytically on complete bipartite graphs.
- Stop/go test: prove a family-wide sign inequality or produce an exact
  admissible positive witness.

## Verification

- Source pointers checked: shared problem/results summaries,
  `aesp_cd_l1_rppr`, `volume_gated_acceleration`, the acceleration/local-solver
  literature notes, and Fable iteration-6/7 evidence.
- Focused build/checks run: `make -C
  manuscript/notes/psi_master_inequality` and `git diff --check` pass.
- Known gaps: mixed clipping, proper faces, finite inner residuals, and all
  algorithm/work consequences.

## Repository handoff

- Provider-owned paths changed: none.
- Shared paths changed: none in the direction branch.
- Assignment state: active.
