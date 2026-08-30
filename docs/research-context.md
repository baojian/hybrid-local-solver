# Research Context

**Status:** Working research map for an active JMLR theorem draft.

## Central problem

This project studies whether acceleration and local iterative updates can be
combined for large-scale graph optimization without losing the computational
benefits of locality. The initial application is local PageRank from one seed
vertex on a finite simple connected graph with unit edge weights. General
seed distributions remain an explicitly separate extension.

The active theorem draft uses a threshold-batched RPPR active set as Stage I
and one ordinary principal PPR solve as an optional Stage II.  It identifies
the exact-real randomized setting in which convergence, locality, and the
target square-root dependence can be proved; deterministic finite precision
and implementation-level comparisons remain separate research goals.

## Intended contributions

The current contribution ledger is:

1. **Established in the manuscript model:** a threshold-batched active-set
   algorithm, an RPPR objective theorem, and a strict discover-once/solve-once
   point-source PPR composition.
2. **Established in the manuscript model:** a fully charged expected-work
   bound `O_tilde(1/(rho * sqrt(alpha)))` for RPPR and
   `O_tilde(1/(eps_ppr * sqrt(alpha)))` for semantic PPR accuracy.
3. **Established proof mechanism:** an exact grounded electrical-flow dual,
   support-safe Stieltjes pivots, and a block-Cholesky/Chebyshev theorem
   limiting complete exposed faces to `O_tilde(1/sqrt(alpha))`.  The dual
   identifies boundary residual violations with failed vertex constraints;
   the complexity contribution is the local threshold-batch bound, not
   Fenchel duality itself.
4. **Still targeted:** a deterministic finite-precision/bit-complexity
   realization and a practical persistent changing-face implementation.
5. **Still targeted:** reproducible experiments under an implementation-wide
   accepted residual and stopping convention.

Several algorithm-specific baselines are also established. Classical APPR has worst-case degree-weighted work
`Theta(1/(alpha * eps_appr))`, proved in
`manuscript/sections/appr_lower_bound.tex`. For fixed relative RPPR accuracy,
residual-thresholded coordinate ISTA and the coordinate-to-batch hybrid both
have exact worst-case work `Theta(1/(alpha * rho))`; the full-batch method has
the additional tight stale-scan logarithm in a broader disconnected,
general-seed model outside the canonical graph/seed contract. The
coarse phase of CF-Push is ordering-independently tight, while the full FIFO
fixed-SOR hybrid has a spider lower bound but no matching general upper bound.
These results use different accuracy namespaces and are not silently
identified with one another.  The active threshold-batch theorem does not
promote the older fixed-SOR or changing-momentum conjectures.

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

The canonical seed input is resolved as one vertex `v`, equivalently `s=e_v`;
see [`decisions/seed-convention.md`](decisions/seed-convention.md). General
unit-mass distributions remain explicitly scoped extensions.

The canonical graph class is also resolved as finite, simple, undirected,
connected, unit-weight, and nontrivial (`|V| >= 2`); see
[`decisions/graph-convention.md`](decisions/graph-convention.md). For the
point-source problem this is without loss after restriction to the seed
component.

The manuscript now fixes the choices needed for its exact-real theorem.  The
following table distinguishes that document-scoped contract from choices
still needed by the executable repository:

| Item | Current status |
| --- | --- |
| PageRank system | Fixed for the manuscript by `source_aligned_problem.tex`; executable adoption remains pending |
| `alpha` | Fixed for the manuscript as the lazy symmetric system parameter in `(0,1]`; baseline translations are explicit |
| Residual | Every manuscript algorithm defines and certifies its own residual; an implementation-wide convention remains open |
| `epsilon` | `eps_obj` and semantic degree-normalized `eps_ppr` are fixed and converted in the paper; baseline tolerances remain distinct |
| Hybrid rule | Fixed for the theorem as threshold-batched Stage I plus an optional fresh principal-PPR Stage II |
| Local work | Fixed for the theorem as fully charged adjacency-list/algebraic-word work; wall-clock instrumentation remains future work |

Do not transfer the manuscript's algorithm-specific certificates into code or
experimental comparisons without updating
[`mathematical-conventions.md`](mathematical-conventions.md), the residual
decision, and tests.

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
- [`solver-family-roadmap.md`](solver-family-roadmap.md): iterative, response,
  mixed, and lower-bound-model organization, including the current proof
  priorities and stop/go criteria.
- [`../manuscript/notes/README.md`](../manuscript/notes/README.md): exhaustive
  standalone-note inventory and build entry point.
- [`../manuscript/tex/shared/NOTATION.md`](../manuscript/tex/shared/NOTATION.md):
  reserved manuscript symbols and shared LaTeX ownership.
- [`literature/README.md`](literature/README.md): annotated literature index
  and paper-intake workflow.
- [`decisions/`](decisions/): accepted and open scientific decisions.
- [`../papers/README.md`](../papers/README.md): shareable PDF library policy.
