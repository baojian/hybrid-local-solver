# A deterministic factorization/rank-PCG hybrid on two support regimes

Date: 2026-09-05. This restricted-class result complements the low-cyclomatic theorem. It does not establish general OP2. No final support is supplied and no randomized primitive is used.

Let n*=|S*|, M=1/rho, and let

\[
T_0=1+\left\lceil\frac1{2\sqrt\alpha}\log_+\frac{2\alpha}{\epsilon}\right\rceil,
\qquad K=M T_0.
\]

The exact all-violations proof bounds the number of stages by T0, with active volume at most M.

## Incremental dense factorization costs O((n*)^3), not once per stage

Use admission order, with deterministic order inside each new batch. The leading principal Cholesky factor is unchanged when the matrix is bordered. Computing each newly admitted scalar row costs O(i^2) when its index is i. Thus the total factor arithmetic over every stage is O((n*)^3).

The triangular solve at a stage with n_t active vertices costs O(n_t^2). Nonempty batches give strictly increasing integer n_t, so

\[
\sum_t n_t^2\le\sum_{i=1}^{n^*}i^2=O((n^*)^3).
\]

Initializing or reading the relevant dense principal entries costs no more than this. Consequently the fully charged exact algorithm using incremental factorization has cost

\[
O((n^*)^3+K)
\]

apart from deterministic dictionary logarithms. The K term includes current boundary evaluation, graph exposure and explicit output coordinates. This is already the OP2 target whenever (n*)^3=O(K), allowing many cycles and dense induced supports.

## A support-agnostic hybrid

Let B=max(1,floor(K^(1/3))). Perform incremental dense factorization while every current admitted size n_t is at most B. If a batch would cross B, switch permanently to the forest-preconditioned exact PCG method from the cyclomatic extension. No new dense factor row need be started for the crossing batch.

The whole dense phase costs O(B^3)=O(K), even though the final support is unknown. If the threshold is never crossed, the algorithm completes in O(K). If it is crossed, all later principal solves cost at most

\[
O((r^*+1)K),
\]

where r* is the induced final support's cyclomatic number. Thus this single deterministic algorithm meets OP2 on the union of the following regimes:

- n*<=floor(K^(1/3));
- r* is polylogarithmic in the allowed problem/accuracy parameters.

The support threshold is computable from alpha, rho and epsilon. There is no final-support oracle, graph-wide final check, or uncharged abandoned factorization. The algorithm always remains correct beyond these regimes, but its general work bound still contains the rank factor.

The clique–path chi obstruction lies in the first regime: n*=O(L), K=Theta(L^3) up to accuracy logarithms, while its cyclomatic number and chi are Theta(L^2). This explains precisely why that obstruction invalidates the trace-sum argument without invalidating a hybrid algorithm.
