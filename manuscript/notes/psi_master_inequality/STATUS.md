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
  claim and must be independently reconstructed.
- **Proved here:** No new claim yet; the direction has just been registered.
- **Conditional:** None yet.
- **Measured:** None yet.
- **Refuted:** None yet.
- **Open:** Analytic nonpositivity beyond finitely enumerated examples.

## Central blocker

Find a firmly-nonexpansive, covariance, cut, or spectral representation whose
sign is visible without exponential enumeration of clipping patterns.

## Dependencies and reusable outputs

- Formal registry dependencies: `aesp_cd_l1_rppr`.
- Source/shared prerequisites: source-aligned RPPR definition.
- Context/provenance: Fable iteration-7 files are read-only exploratory evidence.
- Supplies to: safeguarded acceleration and graph-family absorption analyses.

## Resume here

- Exact file/section/lemma: `main.tex`, opening reconstruction section.
- Next concrete action: independently derive the master identity and expose
  the clipping map as a projection.
- Stop/go test: prove a family-wide sign inequality or produce an exact
  admissible positive witness.

## Verification

- Source pointers checked: pending.
- Focused build/checks run: pending.
- Known gaps: all substantive claims are open.

## Repository handoff

- Provider-owned paths changed: none.
- Shared paths changed: none in the direction branch.
- Assignment state: active.
