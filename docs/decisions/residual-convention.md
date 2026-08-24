# Residual Convention

- **Status:** Open
- **Last updated:** 2026-08-22
- **Applies to:** Theory, solvers, experiments, tables, and figures

## Context

The repository requires residual conventions, normalization, and stopping
criteria to remain consistent between theory and code.  The research-note
workspace now has a precise controller-level PageRank object, semantic output
target, and sufficient residual certificate in
[`../../manuscript/notes/_shared/problem_definition/README.md`](../../manuscript/notes/_shared/problem_definition/README.md).
That contract is intentionally scoped to research-direction comparison: the
implementation-wide orientation, residual formula, evaluation schedule, and
baseline conversions needed for an accepted repository decision remain open.

## Current decision

No canonical residual convention has been adopted.

Until this decision is resolved:

- do not assume a residual formula from a cited implementation or paper;
- do not label `epsilon` as an accuracy guarantee without defining its error
  measure;
- do not report convergence comparisons based on incompatible stopping rules;
- experimental scaffolding may record proposed conventions only when they are
  clearly labeled as provisional.

## Required content for resolution

An accepted decision must specify:

1. the exact PageRank linear system or fixed-point equation;
2. row- or column-vector orientation;
3. the residual formula and sign;
4. normalization by degree, volume, solution scale, or another quantity;
5. the norm or coordinatewise condition;
6. absolute versus relative interpretation;
7. the stopping rule and evaluation frequency;
8. conversion rules for each baseline;
9. tests that distinguish the adopted convention from alternatives.

The same change must update
[`../mathematical-conventions.md`](../mathematical-conventions.md), the paper,
solver code, experiment metadata, and tests.

## Alternatives to evaluate

Record source-grounded alternatives here before accepting one:

| Alternative | Source and exact pointer | Advantages | Risks or conversion needed |
| --- | --- | --- | --- |
| Proximal fixed-point residual \(r_{\mathrm{pg}}(x)=\|x-\operatorname{prox}_{g_\rho}(x-\nabla f(x))\|_\infty\) with unit step | Fountoulakis and Martínez-Rubio (2026), arXiv `2602.21138v2`, PDF p. 24, Appendix E, “Stopping criterion” | Computable without knowing the optimum; identical certificate for ISTA and FISTA; zero exactly at an RPPR minimizer | Must relate this certificate to PageRank-vector error, degree normalization, local computability, and the residuals used by APPR, LocSOR, AESP, and the hybrid solver |
