# Research Context

**Status:** Working research map for an early-stage JMLR project.

## Central problem

This project studies whether acceleration and local iterative updates can be
combined for large-scale graph optimization without losing the computational
benefits of locality. The initial application is local PageRank near a seed
set.

The intended hybrid solver will couple or switch between an accelerated outer
process and efficient local inner updates. The research must identify when
this combination converges, when it remains local, and when its total work
improves on appropriate baselines.

## Intended contributions

The current targets are:

1. A precisely defined hybrid local-solver algorithm and switching or coupling
   rule.
2. Convergence and complexity guarantees consistent with the implemented
   residual, normalization, and stopping rule.
3. A locality-aware work analysis covering outer iterations, local updates,
   and edge operations.
4. Reproducible comparisons with relevant local and accelerated methods.
5. Empirical evidence explaining when acceleration helps or harms locality.

These are research targets, not established claims.

One baseline result is now established rather than targeted: classical APPR
has worst-case degree-weighted work `Theta(1/(alpha * eps_appr))`, proved in
`manuscript/sections/appr_lower_bound.tex`. The upper bound is Andersen,
Chung, and Lang (2007); the matching ordering-independent lower bound is
proved here. Contribution 3 is measured against it.

## Current scope

In scope:

- local PageRank as the first concrete graph problem;
- Catalyst, AESP, APPR, evolving-set methods, LocGD, LocCH, and LocSOR as
  literature or baseline directions to investigate;
- theory, implementation, and experiments that share the same conventions;
- dependence on `alpha`, `epsilon`, graph structure, and solver parameters.

Out of scope unless explicitly added later:

- unsupported claims of superiority across all graph problems;
- global-only speedups that do not account for locality;
- comparisons made under incompatible accuracy definitions;
- manually edited experimental figures.

## Open definitions

The following choices remain unresolved and block definitive theorem or
accuracy claims:

| Item | Needed decision |
| --- | --- |
| PageRank system | Exact equation and transition-matrix orientation |
| Seed input | Domain and normalization |
| `alpha` | Meaning, range, and correspondence with cited methods |
| Residual | Formula, sign, orientation, and normalization |
| `epsilon` | Norm and absolute, relative, local, or global interpretation |
| Hybrid rule | Trigger, state transfer, and termination behavior |
| Local work | Counted update and edge-operation model |

Resolve these in
[`mathematical-conventions.md`](mathematical-conventions.md) and the relevant
decision record before relying on them in code or reported results.

## Evidence and authority

Use this order when sources appear to conflict:

1. `AGENTS.md` for repository-wide invariants and required checks.
2. `docs/mathematical-conventions.md` and accepted decision records for project
   definitions.
3. The paper for claims being prepared for submission.
4. Implementation and tests for executable behavior.
5. `docs/literature/` and source PDFs for external evidence.
6. `docs/research_notes.md` for exploratory ideas that are not yet decisions.

A discrepancy among items 2–4 is a defect to resolve, not a choice an agent
may make silently.

## Documentation map

- [`mathematical-conventions.md`](mathematical-conventions.md): definitions
  shared by theory, code, and experiments.
- [`research_protocol.md`](research_protocol.md): experiment metadata and
  reproducibility requirements.
- [`research_notes.md`](research_notes.md): tentative hypotheses and proof
  ideas.
- [`../manuscript/notes/README.md`](../manuscript/notes/README.md): exhaustive
  standalone-note inventory and build entry point.
- [`../manuscript/tex/shared/NOTATION.md`](../manuscript/tex/shared/NOTATION.md):
  reserved manuscript symbols and shared LaTeX ownership.
- [`literature/README.md`](literature/README.md): annotated literature index
  and paper-intake workflow.
- [`decisions/`](decisions/): accepted and open scientific decisions.
- [`../papers/README.md`](../papers/README.md): shareable PDF library policy.
