# Mathematical Conventions

**Status:** Active registry; unresolved items are explicitly marked below.

## Problem setting

This document records mathematical conventions shared by proofs,
implementations, and experiments. It must describe a convention before code or
reported results depend on that convention.

## Typographic notation

The notation typography follows the author's NeurIPS 2024 and 2025 papers:

- ordinary italic letters denote scalars;
- bold lowercase letters denote vectors;
- bold uppercase letters denote matrices;
- calligraphic uppercase letters denote graphs, sets, and indexed families;
- blackboard-bold letters denote number systems, spaces, and distributions.

The active manuscript implements these habits in
[`manuscript/tex/shared/math_commands.tex`](../manuscript/tex/shared/math_commands.tex):
`\v...` commands produce vectors, `\m...` commands produce matrices, `\g...`
commands produce calligraphic symbols, and `\s...` commands produce
blackboard-bold symbols. The shorthand `\mc` remains available for an
occasional calligraphic symbol that has no semantic alias. Long-standing
shortcuts such as `\R`, `\E`, `\G`, and `\N` are retained for compatibility
with the archived writing style.

These typography rules do not resolve vector orientation, transition-matrix
orientation, or any of the scientific choices listed below.

### Source-aligned RPPR notation

The active manuscript's reference RPPR formulation deliberately follows the
plain italic notation of Fountoulakis and Martínez-Rubio (2026):
\(x,s,A,D,Q,I\), with \(x\) and \(s\) interpreted as column vectors. This is a
scoped exception to the bold vector/matrix typography above, chosen so that
the imported objective, KKT conditions, FISTA updates, and locality analysis
can be compared symbol-for-symbol with arXiv `2602.21138v2`.

The complete source-to-manuscript notation inventory is in
[`manuscript/sections/problem_formulation.tex`](../manuscript/sections/problem_formulation.tex).
Notation copied there is a source-grounded reference convention; it does not
become an implementation or stopping-rule convention until the remaining
decisions and tests below are completed.

## PageRank formulation

The project studies local PageRank as its initial graph problem. The following
definitions are not yet fixed and must not be inferred from a cited paper:

- whether vectors are rows or columns;
- graph directionality, weighting, and treatment of isolated vertices;
- adjacency and degree matrix notation;
- transition-matrix orientation;
- the exact linear system or fixed-point equation;
- seed-vector normalization;
- the role and admissible range of `alpha`;
- the error measure associated with `epsilon`.

When these choices are adopted, update this document, the paper, and tests in
the same change.

The current source-grounded candidate, recorded for evaluation rather than
adopted implementation-wide, assumes an undirected unweighted graph with no
isolated vertices and uses
\[
\mathcal{L}=I-D^{-1/2}AD^{-1/2},
\qquad
Q=\alpha I+\frac{1-\alpha}{2}\mathcal{L},
\]
\[
F_\rho(x)
=
\frac12\langle x,Qx\rangle
-\alpha\langle D^{-1/2}s,x\rangle
+\alpha\rho\|D^{1/2}x\|_1.
\]
Here \(s\geq0\), \(\langle\mathbf{1},s\rangle=1\), and the single-seed case is
\(s=e_v\). See Fountoulakis and Martínez-Rubio (2026), PDF page 3,
Section 3 and equation (RPPR). This candidate does not yet determine the
hybrid solver's transition-matrix orientation, output transformation, or
residual convention.

## Algorithm parameters

- `alpha` denotes the PageRank parameter, but its exact convention remains
  unresolved.
- `epsilon` denotes a target accuracy, but it has no meaning until its error
  measure and normalization are specified.
- The SOR relaxation parameter is `omega`, with `1 < omega < 2`.

Do not translate between alternative `alpha` conventions implicitly. Any
translation used for a baseline must be stated and tested.

## Residuals and stopping rules

No canonical residual has been adopted. The controlling decision record is
[`decisions/residual-convention.md`](decisions/residual-convention.md).

Every stopping rule must specify:

- the exact residual or error formula;
- its norm;
- whether it is absolute or relative;
- any degree or volume normalization;
- whether the condition is global, local, or coordinatewise;
- how `epsilon` enters the condition;
- when the condition is evaluated.

Theory, solver code, experiment metadata, tables, and plots must use the same
meaning or document an explicit conversion.

## Work and complexity accounting

Report at least:

- outer acceleration iterations;
- local inner iterations or updates;
- edge operations;
- dependence on `alpha` and `epsilon`.

Any alternative unit of work must be defined and reported in addition to,
rather than silently replacing, these quantities.

## Invariants

- Experiments record graph, `alpha`, `epsilon`, random seed, stopping rule,
  solver parameters, and code version.
- Mathematical definitions change only with corresponding documentation and
  tests.
- Generated figures are never manually edited.

## Definition checklist

Before declaring a mathematical convention resolved:

1. Write its exact formula and domain here.
2. Update the corresponding notation and statement in the paper.
3. Add tests that distinguish it from plausible alternative conventions.
4. Update experiment metadata and validation.
5. Record the decision and rejected alternatives under `docs/decisions/`.
