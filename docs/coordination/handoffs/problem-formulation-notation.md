# Handoff: problem-formulation-notation

- Agent family: codex
- Role: manuscript
- Branch: `agent/codex/problem-formulation-notation`
- Base commit: `549660ec928ebb868be17454bfec3484bc359a66`
- Assignment state: ready_for_review
- Write scope:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/problem-formulation-notation.md`
  - `docs/literature/local-solvers.md`
  - `manuscript/main.tex`
  - `manuscript/references.bib`
  - `manuscript/sections/problem_formulation.tex`
  - `manuscript/tex/shared/NOTATION.md`
- Permitted shared files: same as the write scope above.

## Outcome

- Requested result: organize the notation inventory compiled from eight prior
  papers and incorporate the useful material into the active manuscript's
  problem formulation.
- Implemented result:
  - rewrote the problem section around one undecorated lazy SSPD PageRank/RPPR
    model instead of a paper-specific notation catalogue;
  - added a conversion table for the reference lazy, rescaled lazy, non-lazy
    mass-coordinate, and non-lazy degree-coordinate systems;
  - defined the document-scoped degree-normalized PPR output target and proved
    its sufficient scaled-system certificate;
  - separated APPR activation, semantic PPR error, RPPR regularization,
    objective gap, proximal fixed-point tolerance, and relative KKT accuracy;
  - unified coordinate and batch work under repeated adjacency-list scans;
  - registered the new convention symbols and added the missing Wei--Yang
    bibliography entry;
  - recorded source-PDF pointers for the Zhou et al. (2024) and Chen et al.
    (2023) formulations and conversions;
  - preserved the user's pre-existing `manuscript/main.tex` title, abstract,
    and compact section-label edits while changing the section title to
    “Problem Formulation and Notation.”
- Deliberately unchanged:
  - no implementation-wide residual or stopping-rule decision was adopted;
  - no solver, experiment, theorem outside the problem formulation, or
    provider-owned path was changed;
  - paper-specific breakpoints, momentum variables, residual ratios, and
    stage counters remain local to the analyses that use them.

## Evidence

- Tests added or changed: none; existing structural manuscript tests cover
  shared-notation ownership and duplicate core definitions.
- Commands run:
  - `make paper`
  - Poppler render of compiled PDF pages 3--7, followed by visual inspection
  - `make test`
  - `make lint`
  - `make agent-audit`
  - `git diff --check`
- Results:
  - paper builds successfully with resolved citations and cross-references;
  - rendered problem-formulation pages have no clipping, overlap, or broken
    tables;
  - `210 passed`;
  - `ruff check .` passes;
  - repository-wide `ruff format --check .` reports two pre-existing files
    outside this assignment that it would reformat:
    `manuscript/notes/path_face_lock_warmup/verify_warmup.py` and
    `manuscript/notes/signed_star_acceleration/verify_star.py`;
  - coordination audit and whitespace check pass.

## Review notes

- Provider-owned paths changed: none.
- Shared paths changed: the seven files listed in the write scope.
- Open decisions or follow-up:
  - decide separately whether the document-scoped semantic PPR target should
    become the repository-wide implementation convention; that would require
    the decision-record, code, experiment-metadata, and test updates specified
    in `docs/decisions/residual-convention.md`;
  - the two unrelated Ruff-format findings should be handled by their owning
    assignments rather than folded into this manuscript change.
