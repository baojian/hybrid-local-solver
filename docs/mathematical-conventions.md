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

### Source-aligned manuscript and research-note notation

The active manuscript and every standalone research note share one reference
RPPR formulation. It preserves the mathematics of Fountoulakis and
Martínez-Rubio (2026) while following the author's typography: vectors are
bold lowercase, matrices are bold uppercase, and graphs and sets are
calligraphic. Thus \(\bm{x},\bm{s}\) are column vectors and
\(\bm{A},\bm{D},\bm{Q},\bm{I}\) are matrices. The generic optimum is
\(\bm{x}^*\), the unregularized PPR optimum is \(\bm{x}_0^*\), and the RPPR
optimum is \(\bm{x}_\rho^*\). These names must not be replaced by
\(x^0\) or \(x^\star(\rho)\).

The canonical reusable definition is
[`manuscript/tex/shared/source_aligned_problem.tex`](../manuscript/tex/shared/source_aligned_problem.tex),
and the reserved-symbol inventory is
[`manuscript/tex/shared/NOTATION.md`](../manuscript/tex/shared/NOTATION.md).
The active paper and each research-direction note input that definition rather
than restating it. The controller-owned `problem_definitions` note is the sole
exception: it presents the same definitions in an expanded reference form and
must keep every shared equation and symbol synchronized with the reusable
fragment. Reusable LaTeX commands are declared only under
`manuscript/tex/shared/`; structural tests reject local declarations, missing
imports, and duplicate core definitions outside this explicit exception.
Proof-local indexed quantities remain permitted only when their scope is
stated and they do not reuse a reserved symbol.

In this manuscript reference, \(\preceq,\succeq\) denote Loewner order,
whereas \(\leq,\geq\) on vectors and matrices denote entrywise order.
In particular, inverse positivity \(\bm Q^{-1}\geq0\) is an entrywise
statement, distinct from positive definiteness \(\bm Q\succ0\).

This shared layer is a source-grounded manuscript reference convention. It
does not become an implementation or stopping-rule convention until the
remaining decisions and tests below are completed.

### APPR baseline notation

[`manuscript/sections/appr_lower_bound.tex`](../manuscript/sections/appr_lower_bound.tex)
continues the same column-vector convention; its push vectors and graph
matrices follow the bold typography above. Andersen, Chung, and Lang (2007)
state their algorithm with
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
The lower-bound experiment rejects `eps_appr` outside `(0, 1/16]`, exactly the
parameter regime of the star theorem; it does not label out-of-regime runs as
theorem verification.

## PageRank formulation

The project studies local PageRank as its initial graph problem. The canonical
graph class and seed input are fixed: the graph is finite, simple, undirected,
connected, has at least two vertices and unit edge weights, and the
end-to-end input is one seed vertex `v` with `s=e_v`. All vectors are column
vectors. In manuscript mathematics, vectors and matrices are bold; in
particular, the generic optimum is `\bm{x}^*`, the PPR optimum is
`\bm{x}_0^*`, and the RPPR optimum is `\bm{x}_\rho^*`. See
[`decisions/graph-convention.md`](decisions/graph-convention.md) and
[`decisions/seed-convention.md`](decisions/seed-convention.md).

The following remaining definitions are not yet fixed and must not be
inferred from a cited paper:

- transition-matrix orientation;
- the exact linear system or fixed-point equation;
- the role and admissible range of `alpha`;
- the error measure associated with `epsilon`.

When these choices are adopted, update this document, the paper, and tests in
the same change.

The current source-grounded manuscript reference uses the accepted connected
unit-weight graph and point-source conventions and defines
\[
\bm{\mathcal{L}}=\bm{I}-\bm{D}^{-1/2}\bm{A}\bm{D}^{-1/2},
\qquad
\bm{Q}=\alpha\bm{I}+\frac{1-\alpha}{2}\bm{\mathcal{L}},
\]
\[
F_\rho(\bm{x})
=
\frac12\langle \bm{x},\bm{Q}\bm{x}\rangle
-\alpha\langle \bm{D}^{-1/2}\bm{s},\bm{x}\rangle
+\alpha\rho\|\bm{D}^{1/2}\bm{x}\|_1.
\]
Here \(\bm{s}\geq\bm{0}\), \(\langle\mathbf{1},\bm{s}\rangle=1\). The canonical
end-to-end computational problem takes one seed vertex `v`, hence
\(\bm{s}=\bm{e}_v\). The exact optima are denoted by
\(\bm{x}_0^*=\bm{Q}^{-1}\bm{b}\) and \(\bm{x}_\rho^*\), with
\(\bm{x}^*\) reserved for an objective-generic optimum. General unit-mass
distributions remain available for
source-aligned algebra and explicitly scoped extensions, but they are not the
input contract of the central complexity target. See
Fountoulakis and Martínez-Rubio (2026), PDF page 3,
Section 3 and equation (RPPR). This candidate does not yet determine the
hybrid solver's transition-matrix orientation, output transformation, or
residual convention.

## Algorithm parameters

- `alpha` denotes the PageRank parameter, but its exact convention remains
  unresolved.
- `epsilon` denotes a target accuracy, but it has no meaning until its error
  measure and normalization are specified.
- The SOR relaxation parameter is `omega`, with `1 < omega < 2`.

The following accuracy namespaces appear in the manuscript workspace and must
stay distinct. None is yet the repository's canonical stopping rule, and no
translation between them is asserted:

| Symbol | Macro | Meaning |
| --- | --- | --- |
| `eps_appr` | `\epsappr` | Degree-normalized APPR residual threshold: vertex `u` is active while `r(u) >= eps_appr * d_u`. |
| `eps_obj` | `\epsobj` | Objective-gap target `F_rho(x_N) - F_rho(x*) <= eps_obj`. |
| `eps_pg` | `\epspg` | Proximal fixed-point residual tolerance of the source experiments. |
| `eps_ppr` | `\epsppr` | Document-scoped degree-normalized PPR target; its exact formula must be stated. |
| `eps_in` | `\epsin` | Document-scoped inner-solver target; its exact certificate must be stated. |
| `eps_kkt` | `\epskkt` | Document-scoped KKT diagnostic target; no solution-error implication is assumed. |
| `eps_burn` | `\epsburn` | Document-scoped burn-in target; it is not a final PPR tolerance. |
| `eps_sol` | `\epssol` | Document-scoped solution diagnostic; its norm and scaling must be stated. |

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

The manuscript's work measures share one unit: `d_i` is charged whenever the
neighborhood of vertex `i` is scanned. APPR, thresholded coordinate ISTA, and
CF-Push use `W = sum_t d_{u_t}` over coordinate pushes. The full-batch
proximal-gradient measure is
`Work(N) = sum_k [vol(supp(y_k)) + vol(supp(x_{k+1}))]`. They differ in which
coordinates a single iteration scans, not in the unit, so edge-operation
counts are comparable without a unit conversion. Their stopping tolerances
remain distinct.

## Invariants

- Experiments record graph, `alpha`, `epsilon`, random seed, stopping rule,
  solver parameters, code version, and dirty-worktree status.
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
