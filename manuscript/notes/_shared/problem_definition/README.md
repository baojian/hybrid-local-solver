# Exact working problem definition

**Status:** controller-level research contract. This is precise enough for
direction comparison, but it does not close the repository-wide residual
decision in `docs/decisions/residual-convention.md`.
The canonical seed scope is fixed by
[`docs/decisions/seed-convention.md`](../../../../docs/decisions/seed-convention.md).
The canonical graph scope is fixed by
[`docs/decisions/graph-convention.md`](../../../../docs/decisions/graph-convention.md).

## One-sentence target

Given adjacency-list access to a finite simple connected graph with unit edge
weights and at least two vertices, one seed vertex `v` (equivalently
`\bm{s}=\bm{e}_v`), a PageRank parameter `alpha`, and an accuracy
`eps_ppr`, compute a sparse approximation to the corresponding personalized
PageRank vector with degree-normalized coordinate error at most `eps_ppr`,
while charging every graph exposure, repeated local operation, response
update, certificate query, and output write; the
aspirational graph-uniform work scale is
`O_tilde(1 / (sqrt(alpha) * eps_ppr))`.

That target is an open research objective, not a theorem currently established
by this repository.

## Exact input and PageRank object

The shared theoretical model is:

- a finite, simple, undirected, connected graph
  `\mathcal{G} = (\mathcal{V}, \mathcal{E})` with
  `|\mathcal{V}| >= 2` and unit edge weights;
- symmetric adjacency matrix `\bm{A}`, degrees `d_i > 0`, and
  `\bm{D} = diag(d_1, ..., d_n)`;
- one seed vertex `v`, with canonical source vector `\bm{s} = \bm{e}_v` and constant
  seed-input cost;
- `alpha in (0, 1]`.

Define

```text
\bm{\mathcal L} = \bm{I} - \bm{D}^(-1/2) \bm{A} \bm{D}^(-1/2)
\bm{Q} = alpha \bm{I} + (1 - alpha) \bm{\mathcal L} / 2
\bm{b} = alpha \bm{D}^(-1/2) \bm{s}.
```

The unique source-aligned solution is

```text
\bm{x}_0^* = \bm{Q}^(-1) \bm{b},
\bm{\pi}   = \bm{D}^(1/2) \bm{x}_0^*.
```

Equivalently, with `\bm{P} = \bm{A} \bm{D}^(-1)` acting on column vectors,

```text
\bm{\pi} = [2 alpha / (1 + alpha)] \bm{s}
           + [(1 - alpha) / (1 + alpha)] \bm{P} \bm{\pi}.
```

This parameterization is intentional. A paper using a different teleportation
parameter must supply the conversion rather than silently reusing `alpha`.
The canonical LaTeX definition is
[`../../../tex/shared/source_aligned_problem.tex`](../../../tex/shared/source_aligned_problem.tex).

### Seed-component reduction

Connectedness loses no point-source solution behavior. If a larger
positive-degree unit-weight graph is disconnected and `\bm{s}=\bm{e}_v`, then `\bm{Q}` is
block diagonal after ordering by components and the load is supported only on
the component `C(v)`. Consequently both the PPR solution and the RPPR
minimizer are zero outside `C(v)`, while their restrictions are exactly the
solutions on `G[C(v)]`. Degrees and adjacency-list charges inside the
component are unchanged. No free global connectivity scan is assumed.

Ambient connectedness does not imply that an active or restricted induced
face is connected; results that keep componentwise face ledgers remain
necessary.

## General-distribution extension boundary

The shared algebra also permits a nonnegative unit-mass distribution
`\bm{s} = sum_v s_v \bm{e}_v`. For unregularized PPR the solution map is linear:

```text
\bm{x}_0^*(\bm{s}) = sum_v s_v \bm{x}_0^*(\bm{e}_v),
\bm{\pi}(\bm{s})   = sum_v s_v \bm{\pi}(\bm{e}_v).
```

If point-source approximations have semantic errors `eps_v`, their weighted
sum has error at most `sum_v s_v eps_v`. This is an algebraic extension, not
a preservation of the canonical work theorem. Running a point-source solver
independently at every nonzero source generally multiplies its principal
work. For a point-source cost proportional to `1 / eps_v`, the optimal
elementary error allocation has mixture factor

```text
H_1/2(s) = (sum_v sqrt(s_v))^2,
```

which lies between `1` and `nnz(s)` and equals `nnz(s)` for a uniform
`nnz(s)`-point distribution. Input, merging, and output are charged in
addition.

RPPR does not have this superposition property: its weighted `L1` threshold,
optimal support, and admission chronology depend nonlinearly on the combined
source. General-seed RPPR therefore requires a separate merge-aware proof and
is not part of the canonical target. An exact three-vertex path in
[`aesp_cd_l1_rppr`](../../aesp_cd_l1_rppr/sections/body/06b_prop_aesp_cd_dynamic_reporters.tex)
shows two source-component reporters stopping separately even though
the combined two-source problem must activate the middle vertex.

## Required output and semantic accuracy

The primary output is a finite-support vector `x_hat`, represented by its
nonzero coordinates, with `pi_hat = D^(1/2) x_hat`. Coordinates not listed are
interpreted as zero. The semantic target is

```text
max_i |pi_hat_i - pi_i| / d_i <= eps_ppr.
```

Thus `eps_ppr` means a degree-normalized PPR solution error here. It is not
`eps_appr` (the APPR activation threshold), `eps_obj` (objective gap),
`eps_pg` (proximal fixed-point residual), or a KKT diagnostic.

For this source-aligned quadratic, the literature supplies the sufficient
certificate

```text
||D^(-1/2) (Q x_hat - b)||_infinity < alpha * eps_ppr
    =>
||D^(-1) (pi_hat - pi)||_infinity < eps_ppr.
```

The implication may be used when its assumptions are preserved. Whether this
quantity, its sign convention, and its evaluation schedule become the
repository's implementation-wide stopping rule is still an open decision.
Every experiment and theorem must therefore name its actual certificate.

## Access and charged work

The default local input model is adjacency-list access. Scanning vertex `i`
reveals its incident neighbors and costs `d_i`; scanning a set `S` costs
`vol(S) = sum_{i in S} d_i`. First discovery and repeated scans are both
charged. Reading the seed vertex costs `O(1)`. A theorem for a general sparse
distribution must additionally charge its seed list, all component or mixture
work, merging, and output.

A valid end-to-end ledger also charges, when present:

- active-set discovery and degree queries;
- repeated reads of old active rows;
- coordinate, gradient, splitting, Krylov, or propagation operations;
- factor, elimination, Schur, response, sketch, and preconditioner updates;
- boundary tests, rekeys, interval refinements, and certificate verification;
- vector materialization, state writes, and final output writes;
- any global preprocessing separately from seed-local work.

Iteration count and wall-clock time are useful secondary measurements but do
not replace this ledger. Randomized algorithms state success probability and
charge randomness-dependent rebuilds.

## Complexity question

For `alpha in (0, 1]` and `eps_appr in (0, 1/16]`, literal lazy single-seed
APPR has worst-case degree work
`Theta(1 / (alpha * eps_appr))` under its own threshold namespace. This is not
a statement about every monotone local method. Global acceleration improves
spectral dependence from `1 / alpha` to `1 / sqrt(alpha)` but can activate
nonlocal coordinates. The central question is whether a fully charged local
algorithm can obtain the analogous

```text
O_tilde(1 / (sqrt(alpha) * eps_ppr))
```

scale under the semantic output definition above, or whether a precisely
defined computational restriction forces a larger bound. No equality between
`eps_appr` and `eps_ppr` is assumed in making this comparison.

## RPPR working surrogate

Many directions use the regularized objective

```text
f(x)       = 0.5 x^T Q x - b^T x
g_rho(x)   = alpha * rho * ||D^(1/2) x||_1
F_rho(x)   = f(x) + g_rho(x)
x*(rho)    = argmin_x F_rho(x).
```

Source results give `x*(rho) >= 0` and
`vol(supp(x*(rho))) <= 1 / rho`. RPPR is used to create support-safe sparse
cores, homotopies, and local KKT gates. Its natural aspirational work scale is
`O_tilde(1 / (rho * sqrt(alpha)))`.

RPPR is not silently the final PPR problem. A theorem using it must state the
regularization-to-PPR error conversion, its chosen relation between `rho` and
`eps_ppr`, and the certificate used for any inexact RPPR solve.

## Theorem acceptance checklist

Before a result is described as solving the target, it must state:

1. graph class, access model, seed model, and admissible parameter regime;
2. exact output representation and accuracy namespace;
3. deterministic or probabilistic guarantee;
4. support evolution: fixed, nested, or nonnested;
5. inverse primitive: iterative, persistent response, or mixed;
6. all discovery, repeated-read, update, query, rebuild, and output charges;
7. preprocessing and storage bounds;
8. whether the theorem is graph-uniform, structural, trajectory-dependent,
   conditional, or algorithm-specific.

The target is not solved by a fast tail with an uncharged burn-in, a small
final support with an uncontrolled trajectory, an oracle that supplies the
future support, or a lower bound that omits a stronger permitted response
primitive.
