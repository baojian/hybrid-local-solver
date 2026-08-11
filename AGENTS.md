# Agent Instructions

This repository is a research project targeting peer-reviewed publication,
including possible JMLR and ICML submissions.

## Required research context

Before modifying theory, algorithms, solver behavior, or experiments, read:

- `docs/research-context.md`;
- `docs/mathematical-conventions.md`;
- the relevant topic file under `docs/literature/`.

Before changing a residual, normalization, or residual-based stopping rule,
also read `docs/decisions/residual-convention.md`.

Use the literature index to find source papers. Verify theorem statements,
equations, and comparisons against the source PDF and record page or section
pointers in the relevant literature note. Source papers provide evidence, but
the project documentation is authoritative for this repository's conventions.
Whenever papers are added or their publication metadata changes, update
`docs/literature/index.md` and the relevant topic note in the same change.

## Research-note development strategy

Use a common mathematical language across the project. Every research note
must follow the notation and problem formulation in
`docs/mathematical-conventions.md` and accepted decision records. When a
project convention is still unresolved, or a source theorem requires a
different formulation, label that choice as note-scoped and give an explicit
mapping to the project's current formulation; never let separate notes drift
into silently incompatible conventions.

Develop materially distinct, promising directions as independent research
notes under `manuscript/notes/`. Create as many valuable notes as the evidence
warrants, including proof attempts, structural conditions, counterexamples,
algorithm variants, and alternative amortizations. Each note must clearly
separate source results, new proved statements, conditional statements,
empirical observations, open conjectures, and refuted claims, and must name
its central missing lemmas and possible weaker targets.

Evolve and refine these notes as proofs, counterexamples, and better
conditions become available. Preserve useful corrections and failed proof
paths, and cross-reference related notes instead of prematurely forcing them
into one narrative. Promote material into the active manuscript only after it
is reconciled with project conventions and either all dependencies of the
stated claim are proved or the claim is narrowed to a correct conditional or
weaker theorem.

### Current AESP--LOCSOR promotion gate

Keep `manuscript/notes/hybrid_aesp_locsor/` as a standalone rigorous research
note. Do not promote its graph-uniform end-to-end complexity claim into the
active manuscript until either:

1. the central early-AESP locality lemma
   \[
   \Lambda_J
   := \max_{1\leq t\leq J}
      \frac{\overline{\operatorname{vol}}(S_t)}{\gamma_t}
   = O(1/\epsilon)
   \]
   is proved with a graph-independent hidden constant; or
2. a correct weaker structural condition or alternative burn-in work argument
   sufficient for the stated manuscript theorem is proved.

Until then, agents may develop the proved trajectory-dependent theorem and
explicitly conditional confinement corollaries, but must label the universal
`O~(1/(sqrt(alpha) * epsilon))` work bound as open. Keep the detailed status
in `docs/research_notes.md` synchronized with this gate.

## Repository map and change routing

The `Repository structure` section in `README.md` is the canonical high-level
map. Place changes according to these boundaries:

- research context, mathematical conventions, decisions, and literature notes
  belong in `docs/`;
- publication prose, equations, and bibliography belong in `manuscript/`;
- reusable graph and solver code belongs in `src/`;
- runnable experiment orchestration belongs in `experiments/`;
- automated verification belongs in `tests/`;
- source PDFs belong in `papers/` and must follow its Git LFS policy.

Keep reusable solver logic out of experiment entry points, and do not use the
manuscript as the only record of a project-wide convention. Before changing
source code, experiments, or the paper library, read `src/AGENTS.md` and
`src/README.md`, `experiments/README.md`, or `papers/README.md`, respectively.
If a directory's responsibility changes, update the root `README.md`; update
this file as well only when agent workflow or ownership boundaries change.

## Scientific invariants

1. Do not change mathematical definitions without updating documentation and tests.
2. Residual conventions, normalization, and stopping criteria must remain consistent between theory and code.
3. Every experiment must record graph, alpha, epsilon, random seed, stopping rule, and code version.
4. Never manually edit generated figures.

## Source ownership boundaries

Solver implementations are separated by ownership under `src/`:

- `src/hybrid_solver_codex/` is owned by Codex agents.
- `src/hybrid_solver_claude/` is owned by Claude agents.
- `src/baselines/` is shared reference code.

An agent must not modify another agent family's implementation directory.
Cross-implementation comparison must happen through tests, experiments, or stable
interfaces rather than by rewriting the other implementation.

Treat baseline implementations as controlled references. All agents may read,
import, execute, and test them, but should modify them only when the baseline
itself is demonstrably incorrect or an explicitly requested baseline is being
added. Keep such changes narrow, document the reason, and add or update tests.

See `src/AGENTS.md` for the detailed rules that apply within the source tree.

## Required checks

Before finishing code changes:

```bash
make test
make lint
```

Before changing reported experimental results:

```bash
make reproduce
```
