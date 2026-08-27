# Direction status: problem_definitions

Last reviewed: 2026-08-27
State: source
Agent family: codex
Role: reference
Branch: `agent/codex/problem-definitions-note`
Base commit: `b5f34cf8a02d07ab5fbca9c2e0304e815177a7c3`
Allowed write scope: `manuscript/notes/problem_definitions/` plus the
registered inventory and coordination files.

## Exact question and contract

- **Question:** What are the exact PPR and RPPR problem definitions used by
  the project, how do the common formulations translate, and which elementary
  or published properties can be used without importing an algorithmic claim?
- **Model:** A finite simple undirected unweighted graph without isolated
  vertices, a sparse nonnegative column seed distribution of unit mass,
  `alpha in (0, 1]`, the shared lazy symmetric PageRank system, and its RPPR
  surrogate for `rho > 0`.
- **Accuracy namespace:** `eps_ppr` is only the document-scoped
  degree-normalized semantic PPR error. It is distinct from `eps_appr`,
  `eps_obj`, `eps_pg`, `rho`, and any algorithm-specific KKT tolerance.
- **Access and charged work:** The input is represented by adjacency lists and
  a sparse seed list. A scan of vertex `i` costs `d_i`, and a scan of a set
  costs its degree volume. The note states no algorithm or work bound.
- **Intended result:** A single buildable source reference containing only
  exact definitions, algebraically equivalent formulations, and standard
  properties with explicit provenance and scope.

## Claim ledger

- **Source:** The PageRank/RPPR formulation, nonnegativity and support-volume
  facts, alternative scalings, and degree-normalized accuracy certificate are
  traced to the papers and exact literature-note pointers listed in
  `main.tex`.
- **Proved here:** None. Short calculations are included only to verify
  equivalence of conventions or to derive standard consequences of the
  displayed source facts.
- **Conditional:** None.
- **Measured:** None.
- **Refuted:** None.
- **Open:** None inside this reference note. The repository-wide residual
  decision remains open outside its scope.

## Central blocker

There is no research blocker. This is a maintenance reference: any future
change to an accepted graph, seed, parameter, residual, or output convention
must be reconciled here and in the shared source-aligned definition.

## Dependencies and reusable outputs

- Formal registry dependencies: none.
- Source/shared prerequisites: `docs/mathematical-conventions.md`,
  `docs/decisions/residual-convention.md`, and
  `manuscript/tex/shared/source_aligned_problem.tex`.
- Supplies to: every research note or manuscript section that needs a compact
  definition and source map for PPR or RPPR.

## Resume here

- Exact file/section/lemma: `main.tex`, Sections 2--6.
- Next concrete action: synchronize this note after an accepted convention or
  correction changes the shared PageRank/RPPR contract.
- Stop/go test: reject any addition that is an algorithm, a novel claim, an
  experiment, a complexity target, or an unresolved conjecture.

## Verification

- Source pointers checked: the relevant entries in
  `docs/literature/local-solvers.md` and
  `docs/literature/acceleration.md`, including the source PDF page and section
  pointers recorded there.
- Focused checks: the note builds to a six-page PDF with resolved citations
  and cross-references; the note inventory reports 27 consistent notes;
  `make note-targets`, `make agent-audit`, and all 210 tests pass. Ruff's code
  checks pass; repository-wide format checking remains red only on two
  pre-existing verifier scripts outside this assignment.
- Known gaps: the note intentionally does not resolve the implementation-wide
  residual sign, stopping schedule, finite-precision behavior, or a local
  solver complexity theorem.
