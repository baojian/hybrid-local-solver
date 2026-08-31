# Direction status: seed_maximum_principle

Last reviewed: 2026-08-27
State: proved-open
Agent family: codex
Role: direction
Branch: `agent/codex/seed-maximum-principle`
Base commit: `71764c15c5bc2bb92f01d9d807942acf61e4be85`
Allowed write scope: `manuscript/notes/seed_maximum_principle/` plus the
registered controller files.

## Exact question and contract

- **Question:** Does the seed maximize the response row relevant to the
  monotone unsettled-value potential, and what terminal bound follows for
  nonnegative output maps on a general connected graph?
- **Model:** The shared source-aligned PPR operator, specialized to one seed:
  `H = I - c_alpha A D^-1`, `gamma_alpha = 1-c_alpha`,
  `H pi = gamma_alpha e_v`.
- **Accuracy namespace:** `eps_ppr` is the shared degree-normalized solution
  error.  No identification with `eps_appr`, objective gap, or a KKT residual.
- **Access and charged work:** The structural maximum principle has no access
  cost.  Its corollary uses the existing one-hop push charge `d_u`, charges
  every seed operation, and permits an output map with nonnegative entries and
  column mass at most `B`.
- **Intended result:** Close the response-row constant exactly and state the
  resulting general-graph terminal potential and operation lower bound.

## Claim ledger

- **Source:** Only the shared PPR definition and elementary reversibility of
  an undirected graph are used.
- **Proved here:** `pi_u/d_u <= pi_v/d_v`; the reciprocity identity
  `pr(e_u)_v/pi_v = d_v*pi_u/(d_u*pi_v)`; the exact response-row maximum
  `Phi_v=1`; the nonnegative-residual terminal bound; and the corresponding
  monotone seed-operation lower bound with an output map.
- **Conditional:** None within the stated exact-arithmetic model.
- **Measured:** None.
- **Refuted:** The transcribed identity
  `pr(e_u)_v/pi_v = d_u*pi_u/(d_v*pi_v)` is false on irregular graphs; its
  degree ratio is inverted.
- **Open:** Integrating the correction into the separately owned
  `class_separation_ladder` note after its independent audit, and deciding the
  unrelated bounded-seed-degree signed-relaxation question.

## Central blocker

The mathematical question handled here is closed.  The remaining work is
cross-direction integration: the class-ladder note was untracked and owned by
another direction agent when this proof was written, so it was deliberately
left untouched.

## Dependencies and reusable outputs

- Formal registry dependencies: none.
- Source/shared prerequisites: the shared source-aligned PPR definition.
- Supplies to: monotone-push class lower bounds and any response calculation
  needing the seed row of the discounted Green kernel.

## Resume here

- Exact file/section/lemma: `main.tex`, Theorem `thm:seed-normalized-maximum`
  and Corollary `cor:seed-output-terminal`.
- Next concrete action: replace the inverted ratio and open `Phi=1` claim in
  the class-ladder direction, then rerun its focused audit.
- Stop/go test: do not apply the terminal corollary to signed residuals or
  signed output maps; both nonnegativity assumptions are used essentially.

## Verification

- Source pointers checked: `docs/mathematical-conventions.md`, the shared
  source-aligned problem, the class-ladder transcription, and its campaign
  source package.
- Focused checks: the note builds to a five-page PDF with no LaTeX warnings;
  the note inventory reports 19 consistent notes; an independent graph-atlas
  screen verified the maximum and reciprocity identities on 27,120 rooted
  graph/parameter cases; all 210 repository tests pass; and the coordination
  audit passes.  Repository-wide lint remains red only on 1,345 pre-existing
  findings under `manuscript/claude-overnight-2026-08-24/`, outside this
  assignment.
- Known gaps: no finite-precision statement and no lower bound for signed
  relaxation or stronger response primitives.
