# Exact working problem definition

**Status:** controller-level research contract. This is precise enough for
direction comparison, but it does not close the repository-wide residual
decision in `docs/decisions/residual-convention.md`.

## One-sentence target

Given adjacency-list access to a large undirected graph, a local seed
distribution supplied in sparse form, a PageRank parameter `alpha`, and an
accuracy `eps_ppr`, compute a sparse approximation to the corresponding
personalized PageRank vector with degree-normalized coordinate error at most
`eps_ppr`, while charging every seed-entry read, graph exposure, repeated local
operation, response update, certificate query, and output write; the
aspirational graph-uniform work scale is
`O_tilde(1 / (sqrt(alpha) * eps_ppr))`.

That target is an open research objective, not a theorem currently established
by this repository.

## Exact input and PageRank object

The shared theoretical model is:

- a finite, simple, undirected, unweighted graph `G = (V, E)` with no isolated
  vertices;
- symmetric adjacency matrix `A`, degrees `d_i > 0`, and
  `D = diag(d_1, ..., d_n)`;
- a nonnegative column seed distribution `s` with `1^T s = 1`, supplied as a
  sparse list of its `nnz(s)` nonzero entries; reading and initializing that
  list is charged, and the default local case is the single seed `s = e_v`;
- `alpha in (0, 1]`.

Define

```text
L = I - D^(-1/2) A D^(-1/2)
Q = alpha I + (1 - alpha) L / 2
b = alpha D^(-1/2) s.
```

The unique source-aligned solution is

```text
x^0 = Q^(-1) b,
pi  = D^(1/2) x^0.
```

Equivalently, with `P = A D^(-1)` acting on column vectors,

```text
pi = [2 alpha / (1 + alpha)] s
     + [(1 - alpha) / (1 + alpha)] P pi.
```

This parameterization is intentional. A paper using a different teleportation
parameter must supply the conversion rather than silently reusing `alpha`.
The canonical LaTeX definition is
[`../../../tex/shared/source_aligned_problem.tex`](../../../tex/shared/source_aligned_problem.tex).

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
charged. Reading and initializing the sparse seed costs `Theta(nnz(s))`; the
displayed aspirational work scale is therefore interpreted for a single seed
or with this input term added explicitly.

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
