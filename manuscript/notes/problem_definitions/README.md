**Problem definitions**

**Merged lineage.** This is the corrected merge: the user-owned v2 notation
baseline from `3b9e9ce` is authoritative, including bold vectors and matrices
and the optimum symbols `\bm{x}^*`, `\bm{x}_0^*`, and `\bm{x}_\rho^*`. The
point-source, connected-unit-graph additions from v1 are retained without
renaming those objects. The temporary v1/v2 split has been retired.

This standalone reference note collects the exact PageRank and regularized
PageRank (RPPR) problems used by the project, their equivalent lazy,
non-lazy, symmetric, mass-coordinate, and degree-coordinate formulations, and
standard source-backed properties of those problems. It also records three
explicitly open complexity questions without presenting them as established
claims.

The note deliberately contains no algorithm, new theorem, experiment, or
proved complexity bound. In particular, it does not adopt a repository-wide
residual or stopping rule. It distinguishes the semantic PPR output error,
the RPPR regularization scale, a locally declared objective-gap target, and
the source-native APPR tolerance used only in the nested-SDD open question.

**Build**

Run `make` in this directory. The mathematical reference is
[`main.tex`](main.tex); the source, scope, and operational handoff follow
below.

**Direction status: problem_definitions**

- Last reviewed: 2026-08-29
- State: source
- Agent family: codex
- Role: reference
- Branch: `main`
- Base commit: `5d4e0ffc54b5988fa2ca7aff65eef847a8b16cd0`
- Allowed write scope: `manuscript/notes/problem_definitions/` plus the note
  inventory, workflow, and validation files needed to maintain this reference.

**Exact question and contract**

- **Question:** What are the exact PPR and RPPR problem definitions used by
  the project, how do the common formulations translate, and which elementary
  or published properties can be used without importing an algorithmic claim?
  What are the three root or source-level complexity questions attached to
  these definitions?
- **Model:** A finite simple undirected connected graph with unit edge weights
  and at least two vertices, one seed vertex `v` with `s=e_v`,
  `alpha in (0, 1]`, the shared
  lazy symmetric PageRank system, and its RPPR surrogate for `rho > 0`. The
  general unit-mass distribution remains an algebraic extension, not the
  canonical computational input.
- **Accuracy namespace:** `eps_ppr` is only the document-scoped
  degree-normalized semantic PPR error. It is distinct from the RPPR
  objective-gap target `eps_obj`, the source-native `eps_appr`, `rho`, and any
  algorithm-specific diagnostic.
- **Access and charged work:** The input is represented by adjacency lists and
  one seed label. A scan of vertex `i` costs `d_i`, and a scan of a set costs
  its degree volume. The baseline is an exact-real algebraic word model that
  also charges arithmetic, state access, certificate evaluation, and output;
  global preprocessing and storage must be reported separately. The note
  states no proved algorithm or work bound.
- **Intended result:** A single buildable source reference containing only
  exact definitions, algebraically equivalent formulations, and standard
  properties with explicit provenance and scope, followed by clearly labeled
  open complexity questions.

**Claim ledger**

- **Source:** The PageRank/RPPR formulation, nonnegativity and support-volume
  facts, alternative scalings, and degree-normalized accuracy certificate are
  traced to the papers and exact literature-note pointers listed in
  `main.tex`.
- **Standard consequence:** Unregularized PPR is linear in the source, so a
  general distribution is a weighted sum of point-source PPR vectors and its
  semantic errors compose by the triangle inequality. This is not a
  same-complexity reduction, and no RPPR superposition is asserted.
- **Standard consequence:** For a point source, RPPR has the exact zero
  solution precisely when `rho >= 1/d_v`; the nonzero regime is therefore
  `0 < rho < 1/d_v`.
- **Standard consequence:** An RPPR objective gap at most `eps_obj` gives
  degree-normalized PPR error at most
  `rho + sqrt(2 eps_obj / alpha)`. Thus `rho = eps_ppr/2` and
  `eps_obj <= alpha eps_ppr^2/8` suffice for the semantic PPR requirement.
- **Proved here:** None. Short calculations are included only to verify
  equivalence of conventions or to derive standard consequences of the
  displayed source facts.
- **Conditional:** None.
- **Measured:** None.
- **Refuted:** None.
- **Open:** Graph-uniform semantic PPR work
  `O_tilde(1/(sqrt(alpha) eps_ppr))`; graph-uniform local RPPR work
  `O_tilde(1/(rho sqrt(alpha)))` with separately stated optimization accuracy;
  and reuse of Wei--Yang's nested SDD systems to improve source-native ACL
  work from `O_tilde(1/eps_appr^2)` toward `O_tilde(1/eps_appr)`.

**Central blocker**

There is no definition-maintenance blocker. The three complexity questions
remain open research targets; their route-specific blockers and evidence stay
in the owning notes. Any future change to an accepted graph, seed, parameter,
residual, or output convention must be reconciled here and in the shared
source-aligned definition.

**Dependencies and reusable outputs**

- Formal registry dependencies: none.
- Source/shared prerequisites: `docs/mathematical-conventions.md`,
  `docs/decisions/graph-convention.md`,
  `docs/decisions/seed-convention.md`,
  `docs/decisions/residual-convention.md`, and
  `manuscript/tex/shared/source_aligned_problem.tex`.
- Shared-source responsibility: this note is the expanded reference
  presentation and therefore does not import the compact fragment verbatim;
  shared equations and symbols must remain synchronized with that fragment.
- Supplies to: every research note or manuscript section that needs a compact
  definition and source map for PPR or RPPR.

**Resume here**

- Exact file/section/lemma: `main.tex`, Sections 2--8.
- Next concrete action: synchronize this note after an accepted convention or
  correction changes the shared PageRank/RPPR contract.
- Stop/go test: admit only root-level or source-explicit open questions here;
  keep algorithms, novel claims, experiments, and route-specific conjectures
  in their owning notes.

**Verification**

- Source pointers checked: the relevant entries in
  `docs/literature/local-solvers.md` and
  `docs/literature/acceleration.md`, including the source PDF page and section
  pointers recorded there.
- Focused checks: the note builds to a nine-page PDF with resolved citations
  and cross-references; the note inventory reports 27 consistent notes; all
  213 tests and `make agent-audit` pass.
- Known gaps: the note intentionally does not resolve the implementation-wide
  residual sign, stopping schedule, finite-precision behavior, or a local
  solver complexity theorem.
