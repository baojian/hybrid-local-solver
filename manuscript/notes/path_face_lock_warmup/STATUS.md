# Direction status: path_face_lock_warmup

Last reviewed: 2026-08-27
State: proved-open
Agent family: codex
Role: direction
Branch: `agent/codex/path-face-lock-warmup`
Base commit: `4a979a6907880fb2dc76d1c51dbb7d12dc8bd5b3`
Allowed write scope: `manuscript/notes/path_face_lock_warmup/` and `docs/coordination/handoffs/path-face-lock-warmup.md`

## Exact question and contract

- **Question:** Can the safe proximal warmup after a face lock be bounded
  independently of path length, or at worst logarithmically, before momentum
  becomes componentwise safe?
- **Model:** Source-aligned RPPR on endpoint paths, followed by symmetric
  spiders if the path mechanism survives.
- **Accuracy namespace:** Note-scoped componentwise KKT and face-retraction
  certificates; no repository-wide stopping-rule identification.
- **Access and charged work:** Adjacency-list sweeps are charged by scanned
  degree; exact inverse and spectral-oracle costs must be reported separately.
- **Intended result:** A proved warmup theorem, a correct weaker structural
  condition, or an explicit counterexample to graph-size-independent warmup.

## Claim ledger

- **Source:** The Fable face-lock construction and the project path
  position/velocity profiles motivate the question.
- **Proved here:** No new claim yet; the direction has just been registered.
- **Conditional:** None yet.
- **Measured:** None yet.
- **Refuted:** None yet.
- **Open:** The post-lock warmup bound and its spider extension.

## Central blocker

Express the Fable componentwise entrance gate in the exact path variables and
determine whether the existing position/velocity estimates imply it.

## Dependencies and reusable outputs

- Formal registry dependencies: `aesp_cd_l1_rppr`, `path_terminal_modal_block`.
- Source/shared prerequisites: source-aligned RPPR definition.
- Context/provenance: Fable iteration-7 notes are read-only exploratory evidence.
- Supplies to: safeguarded acceleration and spider-generalization directions.

## Resume here

- Exact file/section/lemma: `main.tex`, opening proof-obligation section.
- Next concrete action: derive the gate in normalized path coordinates.
- Stop/go test: prove a uniform bound or record the first exact family that
  forces the warmup to grow.

## Verification

- Source pointers checked: pending.
- Focused build/checks run: pending.
- Known gaps: all substantive claims are open.

## Repository handoff

- Provider-owned paths changed: none.
- Shared paths changed: none in the direction branch.
- Assignment state: active.
