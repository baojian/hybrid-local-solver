# Research Context

**Status:** Research map synchronized with the active arXiv theory manuscript, 2026-09-06.

## Central problem

This project studies whether acceleration and local iterative updates can be
combined for large-scale graph optimization without losing the computational
benefits of locality. The initial application is local PageRank from one seed
vertex on a finite simple connected graph with unit edge weights. General
seed distributions remain an explicitly separate extension.

The active paper, *Accelerated Local Algorithms for Personalized and Regularized PageRank*,
contains two complete algorithms: deterministic accelerated regularization
continuation and randomized threshold-batched active sets. Both attain the
point-source `O_tilde(1/(rho sqrt(alpha)))` RPPR work target and imply
`O_tilde(1/(eps_ppr sqrt(alpha)))` semantic PPR work. The deterministic
algorithm also has a specified bounded-arithmetic realization. These are
manuscript theorems; executable provider adoption and practical comparisons
remain separate work.

## Intended contributions

The current contribution ledger is:

1. **Established in the manuscript model:** deterministic continuation,
   two comparison energies, a signed-flow bound on cumulative kinetic volume,
   and a deterministic sparse threshold reporter. The proof charges every
   repeated scan and does not assume support confinement.
2. **Established in the manuscript model:** support-safe randomized threshold
   batching with expected work
   `O_tilde(V_* min(|S_*|, alpha^(-1/2)))`, using the published SDD solver only
   on charged, already discovered principal systems. A block-Cholesky/
   Chebyshev theorem limits the number of those systems.
3. **Established output consequences:** additive RPPR objective accuracy,
   safe subsolution and ACL residual certificates, semantic PPR conversion,
   and an optional set-only handoff followed by a deterministic CG or
   randomized SDD principal-PPR solve.
4. **Established separately for rational point-source inputs:** directed
   rounding, controlled neighbor-response error, scalar rebasing, and finite
   threshold search give the same soft local operation bound with explicit
   input/degree/label encoding factors in bit complexity. This does not
   certify ordinary unchecked floating-point execution.
5. **Explicit-distribution extension:** the randomized proof allows an initial
   positive-load block and gives additive seed-input work `O_tilde(nnz(s))`.
   The direct deterministic extension refreshes source exceptions and has
   `O_tilde((nnz(s)+1/rho)/sqrt(alpha))` work. These interfaces are stated
   separately from the canonical single-label input.
6. **Still targeted:** practical solver integration, persistent reuse across
   faces, and reproducible experimental comparisons under an accepted
   implementation-wide residual and stopping convention.

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
identified with one another.  The active theorems do not
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
| Algorithm | Two specified methods: deterministic continuation and randomized threshold batching; both permit a set-only PPR handoff |
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
