# Audit of deterministic reusable-preconditioner primitives

Scope: external primary sources only, read on 2026-09-05. This is a bounded source audit, not a claim that no suitable theorem exists anywhere. No randomized algorithm was run or proposed for the requested solver.

The desired primitive would build a reusable approximation in `tilde O(m sqrt(kappa))` total work and apply its inverse in `tilde O(m)` work while the solver learns a nested sequence of principal submatrices. I did **not** find a source establishing this primitive with every stated property.

- Lee, Peng, and Spielman, *Sparsified Cholesky Solvers for SDD Linear Systems*, prove existence of linear-sized approximate Cholesky factors with linear-work triangular application, together with fast construction algorithms. The construction is not a deterministic black box: their displayed strongly-diagonally-dominant-set routine chooses a uniform random subset and retries. This source cannot certify compliance with the no-randomness constraint. [Primary paper](https://arxiv.org/pdf/1506.08204), especially PDF pp. 7–8, Figure 1.

- Kyng, Meierhans, and Probst Gutenberg, *Derandomizing Directed Random Walks in Almost-Linear Time*, explicitly give deterministic Laplacian solves. Their Theorem 1.1 states `m^(1+o(1)) log(1/epsilon)` time under the stated weight/condition assumptions; Theorem 1.2 gives a general directed version with polylogarithmic condition dependence. This is an almost-linear result, not the required `m polylog(m)` primitive; it also does not state reusable cheap inverses for adaptively growing principal submatrices. [Primary paper](https://arxiv.org/pdf/2208.10959), PDF p. 4.

- Li and Vaughn, *Deterministic Spectral Sparsification in Almost-Linear Time for Dense Graphs* (August 2026 preprint), state deterministic sparsifier construction in `m^(1+o(1)) + tilde O_epsilon(n^2)` time with nearly linear edge count, under their explicit polynomial weight and parameter assumptions. This is useful evidence of the deterministic cost distinction, but is neither a general near-linear sparse-graph solver nor the desired adaptive reuse theorem. Its introduction also distinguishes earlier randomized near-input-sparsity constructions from deterministic polynomial-time constructions. [Primary preprint](https://arxiv.org/html/2608.13910v1), abstract and introduction.

- Durfee, Gao, Goranci, and Peng, *Fully Dynamic Spectral Vertex Sparsifiers and Applications*, do maintain Schur-complement-related objects under changes and terminal additions, but their resulting dynamic solver is stated with expected amortized polynomial update/query dependence and randomized guarantees. It supplies neither the determinism nor the specific fully charged target here. [Primary paper](https://arxiv.org/abs/1906.10530).

## Two reuse distinctions that require a proof

These observations are elementary, independent of the source audit.

1. If `P` spectrally approximates `Q`, then `P_SS` spectrally approximates `Q_SS` by extending test vectors by zero. But a fast application of `P^(-1)` is not automatically a fast application of `(P_SS)^(-1)`. In general `(P^(-1))_SS` is the inverse of a Schur complement, not `(P_SS)^(-1)`.

2. If `P=LL^T` is sparse lower triangular and `S` is a leading prefix in that exact order, then `P_SS=L_SS L_SS^T`; hence a suitable sparse factor would indeed support cheap leading-principal solves. The missing part is building and updating such a factor in the **admission order**, without knowing the final support or paying dense Schur fill. A theorem for a fixed supplied matrix and an algorithmically chosen elimination order does not automatically provide this online property.

Neither observation is an impossibility result. They explain why citing a static approximate inverse or a static sparsifier is insufficient to close the present numerical ledger.
