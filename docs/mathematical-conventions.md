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

### APPR baseline notation

[`manuscript/sections/appr_lower_bound.tex`](../manuscript/sections/appr_lower_bound.tex)
continues the same scoped plain-italic, column-vector convention so that the
APPR push vectors \(p_t,r_t\) share the graph symbols \(G,V,E,A,D,d_u\) of the
RPPR formulation. Andersen, Chung, and Lang (2007) state their algorithm with
row vectors acting on the right of the lazy walk matrix; the manuscript
transposes it and records this explicitly. Two further scoped choices:

- \(a:=(1-\alpha)/2\) is the lazy half-step factor. The symbol \(\beta\) is
  already the FISTA momentum coefficient and must not be reused for it.
- \(Z_c,Z_L,Z\) denote cumulative pushed residual mass, because \(Q\) is the
  shifted PageRank matrix and \(R\) is an iterate-distance bound.

The executable reference is `src/baselines/appr.py`. It implements exactly
the active test above, charges \(d_u\) per push, and exposes FIFO, LIFO,
maximum-residual-ratio, and seeded-random legal orderings. The focused checks
in `tests/test_appr_lower_bound.py` use the center-seeded star from the
manuscript and cross-check FIFO output against the Numba APPR kernel in
`src/baselines/sdd_solver.py`. That kernel now re-enqueues the pushed vertex
when its retained residual is still active, as required by ACL Algorithm 1,
and includes the final partial queue round in reported work.

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

Three tolerances now appear in the manuscript and must stay distinct. None of
them is yet the repository's canonical stopping rule, and no translation
between them is asserted:

| Symbol | Macro | Meaning |
| --- | --- | --- |
| `eps_appr` | `\epsappr` | Degree-normalized APPR residual threshold: vertex `u` is active while `r(u) >= eps_appr * d_u`. |
| `eps_obj` | written out | Objective-gap target `F_rho(x_N) - F_rho(x*) <= eps_obj`. |
| `eps_pg` | written out | Proximal fixed-point residual tolerance of the source experiments. |

The only accuracy statement attached to `eps_appr` is the push invariant
consequence `||pi - p_T||_1 = ||r_T||_1 < eps_appr * vol(V)`.

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

The manuscript's two work measures share one unit: `d_i` is charged whenever
the neighborhood of vertex `i` is scanned. APPR work is
`W = sum_t d_{u_t}` over pushes; the proximal-gradient measure is
`Work(N) = sum_k [vol(supp(y_k)) + vol(supp(x_{k+1}))]`. They differ in which
coordinates a single iteration scans, not in the unit, so edge-operation
counts are comparable across the two without conversion.

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
