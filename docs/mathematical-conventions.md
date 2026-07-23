# Mathematical Conventions

**Status:** Active registry; unresolved items are explicitly marked below.

## Problem setting

This document records mathematical conventions shared by proofs,
implementations, and experiments. It must describe a convention before code or
reported results depend on that convention.

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
