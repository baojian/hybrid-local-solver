# Standalone problem definition: fully charged accelerated local PageRank

Last reconciled: 2026-08-29.

This is a numerical optimization research problem. This document is
intentionally self-contained: all project-specific definitions, assumptions,
accuracy requirements, cost rules, known boundaries, and open proof
obligations needed to understand the problem appear below. The papers listed
at the end provide background, but they are not required to interpret the
contract.

The desired graph-uniform complexity theorem is open. Results described as
proved, conditional, measured, or refuted must retain those labels.

## 1. Research question

Given only local adjacency-list access to a finite simple connected graph
with unit edge weights and at least two vertices, one seed vertex `v`
(equivalently `s=e_v`), a PageRank parameter `alpha`, and a target accuracy
`eps_ppr`, can an algorithm return a sparse personalized PageRank vector with
a valid terminal certificate in

```text
O_tilde(1 / (sqrt(alpha) * eps_ppr))
```

fully charged work?

“Fully charged” means that the bound includes seed input, graph discovery,
repeated reads, numerical updates, support changes, maintained inverse or
response state, certificate evaluation, memory operations, materialization,
and final output. A fast convergence argument does not solve the problem if
one of those costs is hidden.

The intended result is graph-uniform: its hidden constants may not depend on
the number of vertices, the number of edges, degrees, conductance, diameter,
or another undeclared graph parameter. A theorem may instead impose a graph
structure condition, but then it must be labeled structural rather than
graph-uniform.

Throughout, `O_tilde` hides only explicitly declared logarithmic factors in
quantities such as `1 / alpha`, `1 / eps_ppr`, and the charged active volume.
It must not conceal a polynomial dependence on a graph or accuracy parameter.

## 2. Exact input model

### 2.1 Graph

Let

```text
G = (V, E),    V = {1, ..., n},
```

be a finite, simple, undirected, connected graph with unit edge weights and
`n >= 2`.
The graph need not be supplied as a global matrix. The algorithm receives an
adjacency-list interface.

Let `A` be the symmetric adjacency matrix. For each vertex `i`, define

```text
N(i) = {j : {i,j} is in E},
d_i  = |N(i)| >= 1,
D    = diag(d_1, ..., d_n).
```

For `S` contained in `V`, define

```text
N(S)     = union_(i in S) N(i),
boundary(S) = N(S) minus S,
vol(S)   = sum_(i in S) d_i.
```

For a vector `x`,

```text
supp(x) = {i : x_i != 0}.
```

All vectors in this document are column vectors. Unqualified vector
inequalities are coordinatewise. Matrix inequalities use the Loewner order.

For the canonical point source, connectedness is without loss: on a
possibly disconnected positive-degree graph, the PPR and RPPR solutions
vanish outside the component containing `v`, and restriction to that
component preserves all degrees and equations. This does not promise that an
intermediate active induced subgraph is connected.

### 2.2 Seed

The canonical input is one seed vertex `v`. Its source vector is

```text
s = e_v,
```

so seed input and initialization cost `O(1)`. The shared mathematical layer
also permits a nonnegative probability vector `s`, but that is an explicitly
stronger extension, not the central complexity contract.

For unregularized PPR, linearity gives

```text
pi(s) = sum_v s_v pi(e_v).
```

This does not preserve the canonical work bound automatically. Independent
point-source solves generally incur a mixture factor up to `nnz(s)`, together
with input, merging, and output costs. RPPR is nonlinear in `s`: its threshold,
support, and admission chronology cannot be obtained by point-source
superposition.

### 2.3 PageRank parameter

The parameter satisfies

```text
alpha in (0, 1].
```

The normalization below is part of the problem definition. A result stated
with another teleportation parameter must provide the conversion explicitly.

## 3. Exact PageRank object

Define the normalized graph Laplacian, shifted PageRank matrix, and source by

```text
L = I - D^(-1/2) A D^(-1/2),
Q = alpha I + (1 - alpha) L / 2,
b = alpha D^(-1/2) s.
```

Equivalently,

```text
Q = [(1 + alpha) / 2] I
    - [(1 - alpha) / 2] D^(-1/2) A D^(-1/2).
```

The smooth quadratic objective is

```text
f(x) = 0.5 x^T Q x - b^T x,
grad f(x) = Qx - b.
```

Because the eigenvalues of `L` lie in `[0, 2]`,

```text
alpha I <= Q <= I.
```

Thus `Q` is symmetric positive definite, `f` is `alpha`-strongly convex and
1-smooth, and the unique minimizer is

```text
x^0 = Q^(-1) b.
```

The personalized PageRank vector is

```text
pi = D^(1/2) x^0.
```

Let `P = A D^(-1)`. This is column-stochastic. The same vector satisfies

```text
pi = [2 alpha / (1 + alpha)] s
     + [(1 - alpha) / (1 + alpha)] P pi.
```

Therefore the teleportation probability in the usual fixed-point notation
is `2 alpha / (1 + alpha)`, not `alpha` itself.

Useful structural identities are

```text
Q_ij <= 0 for i != j,
Q^(-1) >= 0,
Q D^(1/2) 1 = alpha D^(1/2) 1,
x^0 >= 0,
pi >= 0,
1^T pi = 1.
```

These maximum-principle and Stieltjes-matrix properties are central to local
support certificates.

## 4. Required output and semantic accuracy

The algorithm returns a sparse vector `x_hat` as an explicit list of nonzero
coordinates. Every coordinate not listed is interpreted as zero. Define

```text
pi_hat = D^(1/2) x_hat.
```

The semantic accuracy requirement is

```text
max_i |pi_hat_i - pi_i| / d_i <= eps_ppr,
```

or equivalently,

```text
||D^(-1/2) (x_hat - x^0)||_infinity <= eps_ppr.
```

This is a coordinatewise, degree-normalized solution guarantee. It is not an
objective-gap requirement, an L1 error requirement, or an iteration-level
activation threshold.

Writing `k = nnz(x_hat)` output entries costs at least `Omega(k)`. Output
work and output storage must therefore be included in the final bound.

## 5. A sufficient terminal certificate

For any candidate `x`, let

```text
r(x) = Qx - b = grad f(x).
```

The following implication holds:

```text
||D^(-1/2) r(x)||_infinity <= alpha * eps_ppr
    =>
||D^(-1/2) (x - x^0)||_infinity <= eps_ppr.
```

Indeed,

```text
x - x^0 = Q^(-1) r(x)
```

and the normalized maximum principle gives

```text
||D^(-1/2) Q^(-1) D^(1/2)||_infinity = 1 / alpha.
```

For a sparse `x`, the residual can be nonzero only on

```text
supp(x) union N(supp(x)) union {v}.
```

This makes a local terminal check possible in principle, but every necessary
row exposure, degree read, residual update, and comparison must be charged.

This certificate is sufficient for the semantic target. It is not imposed as
the only allowable implementation stopping rule. A different certificate is
acceptable only if its formula, normalization, evaluation schedule, and
conversion to the semantic error are proved explicitly.

## 6. Accuracy namespaces

The following quantities must remain distinct:

| Symbol | Meaning |
| --- | --- |
| `eps_ppr` | Degree-normalized PPR solution error in Section 4. |
| `eps_appr` | Vertex-activation threshold for literal APPR: vertex `u` is active while its residual is at least `eps_appr * d_u`. |
| `eps_obj` | Objective-gap target such as `F(x) - F(x*) <= eps_obj`. |
| `eps_pg` | Proximal fixed-point residual tolerance. |
| `eps_kkt` | KKT diagnostic tolerance whose norm and scaling must be stated. |
| `eps_in` | Inner-solver tolerance whose certificate must be stated. |
| `eps_burn` | Burn-in tolerance; it is not a final PPR tolerance. |
| `eps_sol` | Direction-specific solution diagnostic whose norm and scaling must be stated. |
| `rho` | Regularization parameter for RPPR; it is not an accuracy tolerance by itself. |

No equality or implication between two rows of this table is assumed. A
conversion must be a stated lemma with all constants and parameter ranges.

## 7. Local access and fully charged work

### 7.1 Adjacency-list access

Scanning vertex `i` reveals its incident neighbors and costs `d_i`. Scanning
a set `S` costs

```text
vol(S) = sum_(i in S) d_i.
```

The first scan and every repeated scan are charged. A previously discovered
vertex is not a permanently free row unless its adjacency data was stored and
the storage and later reads are included in the ledger.

### 7.2 Required cost categories

A complete theorem reports all applicable categories:

1. seed-vertex input and initialization;
2. first graph exposure and degree queries;
3. repeated adjacency reads and active-row scans;
4. coordinate, gradient, splitting, propagation, Krylov, or other numerical
   recurrence operations;
5. factorization, elimination, Schur-complement, response, sketch, or
   preconditioner construction and application;
6. active-set admission, retraction, restart, correction, rekey, and
   switching work;
7. boundary tests, interval refinement, certificate queries, and final
   validation;
8. persistent storage and temporary workspace;
9. state reads, state writes, and intermediate vector materialization;
10. external interactions and every emitted reply;
11. final sparse output construction and writing.

Any global preprocessing must be reported separately. It may not be hidden in
a seed-local bound. An oracle that supplies the future active set, an exact
restricted inverse, a boundary report, or a preconditioner must have its
construction, representation, application, memory, and output costs charged.

Iteration counts and elapsed time are useful secondary measurements. Neither
replaces degree-weighted work.

### 7.3 Arithmetic and randomness

The primary theoretical target uses exact-real or algebraic-cell arithmetic.
This does not mean that exact minimizers are free: all operations needed to
obtain them remain charged. It also does not imply a finite-precision or bit-
complexity theorem.

A randomized algorithm must state its success probability, randomness model,
and the cost of failed attempts or randomness-dependent rebuilding.

## 8. Desired complexity and comparison baselines

For `eps_ppr in (0, 1)`, the main target is a deterministic exact-real
algorithm with

```text
work = O_tilde(1 / (sqrt(alpha) * eps_ppr)).
```

The preferred target also uses

```text
O(1 / eps_ppr)
```

persistent memory and temporary workspace, up to declared logarithmic
factors, and emits its terminal vector and certificate once.

Three comparisons explain the target:

1. Literal lazy single-seed APPR has tight worst-case degree work
   `Theta(1 / (alpha * eps_appr))` for
   `alpha in (0, 1]` and `eps_appr in (0, 1/16]` under its own activation
   rule. This is an algorithm-specific statement, not a lower bound for every
   local solver and not automatically a statement about `eps_ppr`.
2. Global accelerated methods improve the spectral dependence from
   `1 / alpha` to `1 / sqrt(alpha)`, but their iterates or gradient scans can
   become nonlocal.
3. For fixed relative RPPR accuracy, residual-thresholded coordinate ISTA and
   a coordinate-to-batch hybrid have algorithm-specific worst-case work
   `Theta(1 / (alpha * rho))`. This does not rule out a different accelerated
   local method.

The unresolved goal is to retain the accelerated dependence on `alpha`
without paying global or repeatedly expanding support costs.

## 9. RPPR: the sparse-support surrogate

A principal route uses L1-regularized personalized PageRank (RPPR). For
`rho > 0`, define

```text
g_rho(x) = alpha * rho * ||D^(1/2) x||_1,
F_rho(x) = f(x) + g_rho(x),
x*(rho)  = argmin_x F_rho(x).
```

The unique minimizer is nonnegative. On the nonnegative orthant, RPPR is the
obstacle problem

```text
minimize    0.5 x^T Q x - c_rho^T x
subject to  x >= 0,
```

where

```text
c_rho = b - alpha * rho * D^(1/2) 1.
```

Define the one-sided KKT field

```text
kappa_rho(x) = Qx - c_rho
             = grad f(x) + alpha * rho * D^(1/2) 1.
```

The optimum satisfies

```text
x*(rho) >= 0,
kappa_rho(x*(rho)) >= 0,
x_i*(rho) * kappa_rho,i(x*(rho)) = 0 for every i.
```

### 9.1 Support, bias, and monotonicity

Let `S*(rho) = supp(x*(rho))`. Then

```text
vol(S*(rho)) <= 1 / rho,
0 <= D^(-1/2) (x^0 - x*(rho)) <= rho * 1.
```

Thus RPPR simultaneously provides a sparse optimal support and a PPR bias
bound. If `rho' >= rho`, then

```text
x*(rho') <= x*(rho),
S*(rho') is contained in S*(rho).
```

RPPR is therefore an internal localization device, but it is not
automatically the final PPR answer.

### 9.2 One-sided lower-point certificate

Suppose an algorithm maintains a point `ell` satisfying

```text
0 <= ell <= x*(rho).
```

If, for some `tau > 0`,

```text
kappa_rho,i(ell) >= -alpha * tau * sqrt(d_i)
for every i,
```

then the normalized maximum principle gives

```text
||D^(-1/2) (x*(rho) - ell)||_infinity <= tau.
```

Combining this with the RPPR bias bound yields

```text
||D^(-1/2) (x^0 - ell)||_infinity <= rho + tau.
```

Moreover, if `ell_i = 0` and `kappa_rho,i(ell) < 0`, then
`i` belongs to `S*(rho)`. Negative KKT demand at a valid lower point is
therefore a support-safe admission rule.

The natural choice

```text
rho = tau = eps_ppr / 2
```

gives, for a process that admits only support-safe vertices and stops at the
displayed global gate,

```text
PPR error <= eps_ppr,
peak certified support volume <= 2 / eps_ppr.
```

Maintaining a valid lower point, finding all relevant violations locally, and
reaching the gate at accelerated fully charged work are algorithmic tasks;
the inequalities above do not solve them by themselves.

### 9.3 General KKT diagnostic

For an arbitrary vector `x`, put `lambda_i = alpha * rho * sqrt(d_i)` and
define the minimum-magnitude KKT vector by

```text
kappa_min,i(x) = grad_i f(x) + lambda_i,   if x_i > 0,
                 grad_i f(x) - lambda_i,   if x_i < 0,
                 grad_i f(x)
                   - clip(grad_i f(x), -lambda_i, lambda_i),
                                             if x_i = 0.
```

Here `clip(z, lower, upper) = min(max(z, lower), upper)`.

Then

```text
R_kkt,rho(x) = ||D^(-1/2) kappa_min(x)||_infinity
```

certifies

```text
||D^(-1/2) (x - x*(rho))||_infinity
    <= R_kkt,rho(x) / alpha.
```

Consequently, an RPPR algorithm may use this diagnostic if it charges its
evaluation and combines `rho + R_kkt,rho(x) / alpha` with the desired PPR
error. It must not silently identify `R_kkt,rho` with `eps_ppr`.

## 10. Candidate solver architecture

The project does not require one particular architecture, but current work
organizes candidates along three independent axes:

| Axis | Alternatives | Question controlled |
| --- | --- | --- |
| Graph access | Adjacency queries, supplied subgraph, global matrix | Which graph information is available and charged? |
| Support evolution | Fixed, nested, nonnested | Which restricted systems occur, and are downdates needed? |
| Inverse realization | Iterative recurrence, persistent response, mixed | Where are conditioning, update, state, and materialization costs paid? |

For an active set `S`, define the restricted Green operator

```text
G_S = Q_SS^(-1).
```

If a disjoint batch `T` is added, the new block is governed by the Schur
complement

```text
K_T = Q_TT - Q_TS G_S Q_ST.
```

A backend-neutral solver conceptually needs four operations:

1. `Expand(T)`: incorporate a support-safe batch without silently
   materializing the old active face;
2. `BoundaryBounds()`: return certified intervals for boundary KKT demand or
   residual values;
3. `Repair(tolerance)`: reduce numerical error on the current active face;
4. `Finalize()`: materialize the sparse answer and terminal certificate once.

Three broad realizations are being studied:

- **Iterative:** local coordinate, row, Krylov, or propagation updates. These
  make conditioning explicit but may repeatedly revisit old active rows.
- **Persistent response:** retained elimination, factor, Schur, harmonic, or
  comparable inverse state. These can reuse settled structure but may require
  dense boundary reporting or high-rank updates.
- **Mixed:** persistent state on a settled core and iterative repair on a
  changing frontier. This must charge conversion, both states, switching,
  validation, and final materialization.

For a final active volume `V` and a preconditioner `P_S`, a useful conditional
design template is

```text
O_tilde(
    U_response(V)
    + V * sqrt(sup_S kappa_eff(S))
    + V
),
```

where

```text
kappa_eff(S) = condition_number(P_S^(-1/2) Q_SS P_S^(-1/2))
```

is the ratio of the largest to smallest eigenvalue of the displayed
symmetric positive-definite matrix, and `sup_S` ranges over active sets that
can occur in the execution.

`U_response` includes every response update, query, state, and output
cost. Without a graph-aware preconditioner, the spectral term naturally
scales as `O_tilde(V / sqrt(alpha))`. This expression is a design template,
not a general theorem.

## 11. Central open theorem and current proof boundary

### 11.1 Why accelerated outer iterations are insufficient

An accelerated method may need only `O_tilde(1 / sqrt(alpha))` outer stages,
but a stage can scan a large active volume. Outer iteration count therefore
does not imply local work.

Objective convergence also does not control weighted L1 gradient mass without
a support-volume factor. Smoothness gives

```text
||grad f(x)||_2^2 <= 2 * (f(x) - f(x^0)).
```

If `Omega_x = supp(grad f(x))`, then

```text
||D^(1/2) grad f(x)||_1
    <= sqrt(vol(Omega_x)) * ||grad f(x)||_2.
```

The missing support-volume control is exactly the locality question.

Momentum adds another difficulty: a star-graph construction shows that an
accelerated RPPR method can transiently activate a high-degree center even
when the optimal support contains only the seed leaf. Small final or optimal
support alone does not bound the work of the trajectory.

### 11.2 Early-AESP locality gate

In an AESP outer stage `t`, let `overline_vol(S_t)` denote its average inner
active volume and let `gamma_t` denote the average fraction of weighted
residual mass processed by its local inner updates. The stages entering the
ratio have `gamma_t > 0`. Define

```text
Lambda_t = overline_vol(S_t) / gamma_t,
Lambda_J = max_(1 <= t <= J) Lambda_t.
```

For a burn-in ending after stage `J`, the proved trajectory-dependent
accounting has the form

```text
burn_in_work = O_tilde(Lambda_J / sqrt(alpha)),
hybrid_work  <= burn_in_work
                + O(1 / (sqrt(alpha) * eps_ppr)).
```

Thus the target follows conditionally if there is a graph-independent
constant `K` such that

```text
Lambda_J <= K / eps_ppr.
```

This graph-uniform early-locality inequality has not been proved. The
universal AESP-to-local-tail complexity claim must remain open until this
inequality is proved, or until a correct weaker structural condition or an
alternative burn-in argument is sufficient for the full theorem.

### 11.3 Components that are already controlled

The open target should not be confused with the following completed or
conditional components:

1. The direct PPR residual certificate in Section 5 is proved.
2. The RPPR support-volume bound, bias bound, support-safe admission rule, and
   one-sided terminal bridge in Section 9 are proved.
3. With `rho = tau = eps_ppr / 2` and `alpha >= 1/4`, zero-start monotone
   greedy RPPR coordinate descent reaches the one-sided gate in at most
   `5 / eps_ppr` degree work, plus sparse-seed input and output. This already
   lies within the target order because `1 / sqrt(alpha)` is bounded in this
   regime.
4. On a fixed, already certified active envelope of degree volume `V`, a
   suitable accelerated outer method with local coordinate inner solves has
   conditional work `O_tilde(V / sqrt(alpha))`. What remains open is obtaining
   and maintaining `V = O(1 / eps_ppr)` graph-uniformly while charging all
   finite-stage corrections and certificate operations.
5. Several paths, trees, spiders, caterpillars, and bounded-core families
   admit exact structured handoffs or persistent responses. These results are
   graph-family-specific and do not establish the arbitrary-graph theorem.

Consequently, the primary unresolved regime is small `alpha`, especially the
actual-finite low-Dirichlet accelerated branch and its interaction with
changing local support.

### 11.4 Additional unresolved proof obligations

1. **Actual finite accelerated recurrence.** A proof must cover the iterates
   produced by finite inner solves, including residuals, retractions,
   positive-part mixing, corrections, and rekeys. A proof only for ideal
   shifted minimizers is insufficient.
2. **Low-Dirichlet accelerated transfer.** Existing simple Euclidean or
   unsplit one-step energy banks do not yield a graph-uniform accelerated net
   exponent. A windowed, spectrally split, nonlinear, or differently
   normalized argument remains open.
3. **Multiple support admissions.** Reset or handoff costs across genuinely
   nonsettled active-set expansions need a nonadditive amortization or a
   structural bound. Paying each reset independently can lose the target
   dependence on `alpha`.
4. **Output-sensitive response maintenance.** Persistent response state must
   survive changing, potentially high-rank cores without a dense boundary
   refresh or full old-face replay after every light update.
5. **Arbitrary-graph incremental response.** Exact append-only mechanisms are
   understood on several structured paths, trees, and bounded cores, but not
   as a general graph-uniform solve-and-boundary interface.
6. **Lower-bound model.** A general impossibility theorem must precisely state
   which recurrence, representation, response, materialization, memory, and
   output operations are allowed. Broad adjacency access alone is too weak a
   restriction: sparse-basis construction and persistent responses defeat
   several path candidates.
7. **Finite precision.** The current main contract is exact-real. Stability,
   bit complexity, and robust certificate evaluation remain separate open
   obligations.

## 12. Scope of known negative results

Several tempting arguments are known to fail, but each failure is scoped:

- momentum need not preserve a small transient support, even when the RPPR
  optimum is very sparse;
- support additions alone cannot pay every accelerated correction;
- raw correction count need not measure harmful inflation;
- pointwise momentum nonexpansion is false for some small graphs;
- ordinary restart after every support expansion can erase acceleration;
- a dense exact response can hide boundary reads, factor updates, and output
  materialization;
- a path that forces many ordinary Krylov steps may still admit a sparse
  supported-prefix or persistent-response solution to the same certificate
  task;
- a finite trace that stops one credit ledger is not a lower bound for all
  local solvers.

These facts prune proof strategies. They do not disprove the main target.

## 13. What counts as solving the problem

A claimed solution must state and prove all of the following:

1. graph class, seed model, access interface, and complete parameter range;
2. exact output representation and the semantic accuracy guarantee;
3. terminal certificate, its evaluation schedule, and its conversion to
   semantic error;
4. deterministic guarantee or success probability;
5. fixed, nested, or nonnested support evolution;
6. iterative, persistent-response, or mixed inverse primitive;
7. all input, discovery, repeated-read, numerical, response, control,
   validation, memory, materialization, and output charges;
8. preprocessing, persistent-memory, and temporary-workspace bounds;
9. the exact logarithmic factors hidden by `O_tilde`;
10. whether the theorem is graph-uniform, structural,
    trajectory-dependent, conditional, or algorithm-specific;
11. for an RPPR route, the regularization bias, inexact-solve error, chosen
    relation between `rho` and `eps_ppr`, and their final composition;
12. for finite arithmetic, stability and precision assumptions.

The target is not solved by any of the following in isolation:

- an accelerated outer iteration count with unbounded per-stage volume;
- a fast local tail with an uncharged burn-in;
- a small final support with uncontrolled transient work;
- an oracle that supplies the future support or an exact restricted inverse;
- a certificate that requires an uncharged global scan;
- an RPPR theorem without a PPR bias conversion;
- a measured trend without a mathematical guarantee;
- a counterexample to one implementation presented as a class lower bound.

## 14. Useful forms of a new contribution

A valuable contribution need not immediately prove the full target. It may
instead provide one of the following, with precise scope:

- a graph-uniform end-to-end algorithm satisfying Section 13;
- a structural theorem under a natural, checkable graph condition;
- a correct replacement for the early-AESP locality gate;
- an actual-finite accelerated Lyapunov or windowed net exponent;
- an output-sensitive incremental response or reporter;
- a complete multi-admission reset amortization;
- a conversion between a computable RPPR diagnostic and `eps_ppr`;
- a finite-precision version of a current exact-real result;
- a rigorously defined lower-bound model with an identical task for all
  compared algorithms;
- a smallest exact counterexample that refutes a specific proposed lemma
  without overstating its consequences.

Every contribution should separate source facts, newly proved statements,
conditional statements, measured observations, open conjectures, and
refuted claims.

## 15. Terminology

- **PPR:** personalized PageRank, the semantic output problem defined in
  Sections 3 and 4.
- **APPR:** a classical approximate-PPR residual-push method and local-work
  baseline.
- **RPPR:** the L1-regularized PPR optimization surrogate in Section 9.
- **Catalyst:** an outer acceleration framework based on approximately
  solving regularized auxiliary problems with warm starts.
- **AESP:** Accelerated Evolving Set Process, an accelerated local graph
  method whose local inner work is trajectory-dependent.
- **LocSOR:** localized successive over-relaxation, used as a momentum-free
  local refinement mechanism.
- **Persistent response:** retained factor, elimination, Schur, harmonic, or
  related state used to answer changes in a restricted system without
  rebuilding every active prefix.
- **Gate:** a support-admission, stopping, or certificate test based only on
  information the algorithm has paid to obtain.
- **Settled core:** an active region whose numerical response is represented
  persistently rather than repeatedly recomputed.
- **Frontier:** the changing boundary region still handled by local updates,
  interval refinement, or support admission.

## 16. Selected background papers

These references motivate the formulation and candidate methods. The problem
contract above remains fully specified without them.

1. Reid Andersen, Fan R. K. Chung, and Kevin J. Lang. “Using PageRank to
   Locally Partition a Graph.” *Internet Mathematics* 4(1):35-64, 2007.
   DOI: 10.1080/15427951.2007.10129139.
2. Kimon Fountoulakis, Farbod Roosta-Khorasani, Julian Shun, Xiang Cheng, and
   Michael W. Mahoney. “Variational Perspective on Local Graph Clustering.”
   *Mathematical Programming* 174:553-573, 2019.
   DOI: 10.1007/s10107-017-1214-8.
3. Hongzhou Lin, Julien Mairal, and Zaid Harchaoui. “Catalyst Acceleration
   for First-order Convex Optimization: From Theory to Practice.” *Journal
   of Machine Learning Research* 18(212):1-54, 2018.
4. David Martínez-Rubio, Elias Wirth, and Sebastian Pokutta. “Accelerated
   and Sparse Algorithms for Approximate Personalized PageRank and Beyond.”
   *Proceedings of the 36th Conference on Learning Theory*, PMLR
   195:2852-2876, 2023. arXiv:2303.12875v1.
5. Binbin Huang, Luo Luo, Yanghua Xiao, Deqing Yang, and Baojian Zhou.
   “Accelerated Evolving Set Processes for Local PageRank Computation.”
   *Advances in Neural Information Processing Systems* 38, 2025.
   arXiv:2510.08010v4.
6. Kimon Fountoulakis and David Martínez-Rubio. “Complexity of Classical
   Acceleration for L1-Regularized PageRank.” arXiv:2602.21138v2, 2026.
