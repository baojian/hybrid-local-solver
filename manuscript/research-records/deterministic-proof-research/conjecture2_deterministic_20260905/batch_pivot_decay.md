# Deterministic exact batch pivots: accelerated stage decay, arithmetic gap remains

Date: 2026-09-05. Independent derivation for OP2. The only existing manuscript file read was `/Users/baojian/git/hybrid-local-solver/manuscript/notes/problem_definitions/main.tex`. No other manuscript notes or prior agent work were consulted. This document is outside the repository.

**Status.** The argument below proves an accelerated bound on the number of **exact, all-violations** active-set stages, and consequently the desired bound on adjacency access and explicitly evaluated boundary residuals. It does **not** establish OP2's fully charged arithmetic bound: implementing the successive exact restricted solves is still an unresolved part of this route. No randomized algorithm is used or proposed here.

## 1. Definitions and algorithm

Write

\[
a=(1+\alpha)/2,\qquad c=(1-\alpha)/2,\qquad h=b-\alpha\rho D^{1/2}{\bf1}.
\]

On the nonnegative orthant, RPPR equals

\[
\phi(x)=\tfrac12x^TQx-h^Tx,\quad x\ge0.
\]

Its optimum is the original RPPR optimum. Here \(Q\) is a symmetric positive-definite M-matrix and \(\alpha I\preceq Q\preceq I\). The canonical nonzero regime makes \(h_v>0\), while \(h_i<0\) for all \(i\ne v\).

Set \(S_0=\varnothing\) and \(x^{(0)}=0\). At stage \(t\ge1\), form

\[
B_t=\{i\notin S_{t-1}: r_i(x^{(t-1)})>0\},\qquad r(x)=h-Qx.
\]

**Every** strict violation is included; this condition is essential. If \(B_t\) is empty, terminate. Otherwise set \(S_t=S_{t-1}\cup B_t\), solve exactly

\[
Q_{S_tS_t}x^{(t)}_{S_t}=h_{S_t},\qquad x^{(t)}_{S_t^c}=0.
\]

Thus \(B_1=\{v\}\). No inactive vertex outside the seed or the exposed boundary can violate, so the algorithm is local.

## 2. Basic safe-pivot facts

Let \(S\) be the old active set, \(B\) its new positive-residual batch, and \(r_B=h_B-Q_{BS}x_S>0\). The Schur complement and update obey

\[
D_B=Q_{BB}-Q_{BS}Q_{SS}^{-1}Q_{SB},\quad
\delta_B=D_B^{-1}r_B>0,\quad
\Delta_S=-Q_{SS}^{-1}Q_{SB}\delta_B\ge0.
\]

All principal matrices and Schur complements are positive-definite M-matrices, hence have nonnegative inverses. The displayed formulas prove positivity and coordinatewise monotonicity of all iterates by induction.

Every positive restricted solution lies below the global obstacle solution: global KKT gives \(Qx^*=h+w^*\), with \(w^*\ge0\). Therefore

\[
Q_{SS}(x^*_S-x_S)=w^*_S-Q_{S,S^c}x^*_{S^c}\ge0,
\]

and inverse positivity implies \(x_S\le x^*_S\). Thus every admitted vertex belongs to \(S^*=\operatorname{supp}(x^*)\), and \(\operatorname{vol}(S_t)\le1/\rho\). Finitely many nonempty batches reach the exact optimum, even in degenerate cases: an empty strict-violation set already satisfies KKT.

Let \(N\) be this eventual finite number of batches. Define \(\Delta_t=x^{(t)}-x^{(t-1)}\). Then

\[
(Q\Delta_t)_{S_{t-1}}=0.
\]

Hence the increments are pairwise Q-orthogonal. Moreover, since \(S_t\subseteq S^*\),

\[
\phi(x^{(T)})-\phi(x^*)
=\tfrac12\|x^*-x^{(T)}\|_Q^2
=\tfrac12\sum_{t=T+1}^{N}\|\Delta_t\|_Q^2.
\]

## 3. Admission-block Cholesky identities

Order the final principal matrix \(Q_{S_NS_N}\) by the batches \(B_1,\ldots,B_N\), with any fixed ordering inside each batch, and write its ordinary scalar Cholesky factorization

\[
Q_{S_NS_N}=LL^T.
\]

All diagonal entries of \(L\) are positive and all strictly lower entries are nonpositive. Indeed the Cholesky recurrence has numerator \(Q_{ij}-\sum_{k<j}L_{ik}L_{jk}\le0\). Consequently \(L^{-1}\ge0\), and every diagonal block \(L_{tt}\) has nonnegative inverse. Also

\[
\|L\|_2\le1,\qquad \|L^{-1}\|_2\le\alpha^{-1/2}.
\]

Let

\[
r_t=r_{B_t}(x^{(t-1)}),\qquad \delta_t=x^{(t)}_{B_t},\qquad
z_t=L_{tt}^{-1}r_t\ge0.
\]

The diagonal pivot Schur complement is \(D_t=L_{tt}L_{tt}^T\), so

\[
\delta_t=L_{tt}^{-T}z_t,
\qquad \|\Delta_t\|_Q^2=\delta_t^TD_t\delta_t=\|z_t\|_2^2.
\]

These factor identities are analytical: they do not yet assert that the factor can be built cheaply.

## 4. The key inequality uses all violations

For \(t\ge2\), a vertex in \(B_t\) was outside \(S_{t-2}\) and was **not** admitted in \(B_{t-1}\). Since all strict violations were admitted, its earlier residual was nonpositive:

\[
r_{B_t}(x^{(t-2)})\le0.
\]

Subtracting the previous update gives

\[
r_t\le -Q_{B_t,S_{t-1}}\Delta_{t-1,S_{t-1}}.
\]

Put \(O=S_{t-2}\), \(P=B_{t-1}\). The previous update on old coordinates was

\[
\Delta_{t-1,O}=-Q_{OO}^{-1}Q_{OP}\delta_{t-1}.
\]

Thus

\[
r_t\le -C_{t,t-1}\delta_{t-1},\qquad
C_{t,t-1}=Q_{B_tP}-Q_{B_tO}Q_{OO}^{-1}Q_{OP}.
\]

The displayed \(C\) is the off-diagonal block after eliminating \(O\); it is entrywise nonpositive. Standard block Cholesky multiplication gives

\[
C_{t,t-1}=L_{t,t-1}L_{t-1,t-1}^T.
\]

Using \(\delta_{t-1}=L_{t-1,t-1}^{-T}z_{t-1}\), the inequality becomes

\[
r_t\le-L_{t,t-1}z_{t-1}.
\]

Multiplication by the **nonnegative** inverse \(L_{tt}^{-1}\) is legitimate and yields

\[
\boxed{\quad 0\le z_t\le-L_{tt}^{-1}L_{t,t-1}z_{t-1}.\quad}
\]

One must not instead multiply an inequality by \(L_{tt}^T\), whose off-diagonal entries can be negative. The definition \(z_t=L_{tt}^{-1}r_t\) avoids that mistake.

## 5. A well-conditioned block-bidiagonal comparison

Let \(\mathcal B\) retain only the diagonal blocks and first block subdiagonal of \(L\):

\[
\mathcal B_{tt}=L_{tt},\qquad
\mathcal B_{t,t-1}=L_{t,t-1},
\]

with every other block zero. This is a nonsingular lower triangular M-matrix. Because \(L\le\mathcal B\) entrywise,

\[
0\le\mathcal B^{-1}\le L^{-1}.
\]

For example, the difference identity is

\[
L^{-1}-\mathcal B^{-1}=L^{-1}(\mathcal B-L)\mathcal B^{-1}\ge0.
\]

Entrywise domination between nonnegative matrices implies domination of their Euclidean operator norms (apply to the coordinatewise absolute value of any input). Therefore

\[
\|\mathcal B^{-1}\|_2\le\alpha^{-1/2}.
\]

The block diagonal part of \(L\) has norm at most \(\|L\|_2\). The first block subdiagonal has norm equal to the maximum norm of one of its blocks, also at most \(\|L\|_2\). Hence

\[
\|\mathcal B\|_2\le2,
\qquad
\alpha I\preceq \mathcal B\mathcal B^T\preceq4I.
\]

Let \(w\) be supported on its first block, with \(w_1=r_1\), and put \(u=\mathcal B^{-1}w\). The preceding recurrence and induction give

\[
0\le z_t\le u_t=(\mathcal B^{-1})_{t1}r_1.
\]

This is where the argument obtains a truly block-bidiagonal object, even though the original Cholesky factor can have dense long-range block fill.

## 6. Chebyshev decay and the stage bound

Put

\[
q=\frac{2-\sqrt\alpha}{2+\sqrt\alpha}.
\]

The usual Chebyshev residual polynomial supplies a degree \(\ell-1\) polynomial \(p_{\ell-1}\) such that

\[
\max_{\lambda\in[\alpha,4]}|\lambda^{-1}-p_{\ell-1}(\lambda)|
\le\frac2\alpha q^\ell.
\]

The matrix \(H=\mathcal B\mathcal B^T\) is block tridiagonal, and

\[
\mathcal B^{-1}=\mathcal B^T H^{-1}.
\]

The polynomial approximation \(\mathcal B^Tp_{\ell-1}(H)\) has block bandwidth at most \(\ell\). For \(t\ge3\), take \(\ell=t-2\); its \((t,1)\) block is zero. Thus

\[
\|(\mathcal B^{-1})_{t1}\|_2
\le\frac4\alpha q^{t-2}.
\]

The same loose bound for \(t=2\) follows from \(\|\mathcal B^{-1}\|_2\le\alpha^{-1/2}\). Since the first batch is the seed alone,

\[
\|r_1\|_2=\alpha(1/\sqrt{d_v}-\rho\sqrt{d_v})\le\alpha.
\]

Consequently, for every \(t\ge2\),

\[
\|\Delta_t\|_Q=\|z_t\|_2\le4q^{t-2}.
\]

For every \(T\ge1\), the orthogonal-increment identity now gives

\[
\boxed{
F_\rho(x^{(T)})-F_\rho(x^*)
\le\frac{8q^{2(T-1)}}{1-q^2}
\le\frac9{\sqrt\alpha}e^{-2\sqrt\alpha(T-1)}.
}
\]

The last inequality uses \(1-q^2=8\sqrt\alpha/(2+\sqrt\alpha)^2\ge8\sqrt\alpha/9\) and \(\log(1/q)\ge\sqrt\alpha\). If exact termination occurs earlier, the gap is zero. Therefore

\[
T\ge1+\left\lceil\frac1{2\sqrt\alpha}
\log_+\frac9{\epsilon\sqrt\alpha}\right\rceil
\]

is a deterministic, margin-independent stage limit for additive objective gap \(\epsilon\).

### Sharper whole-tail estimate

The root agent supplied the following improvement, independently checked here. Write \(H=\mathcal B\mathcal B^T\), \(u=\mathcal B^{-1}w\), and let \(R_k=1-\lambda p_{k-1}(\lambda)\) be the normalized Chebyshev residual polynomial on \([\alpha,4]\), with \(|R_k|\le2q^k\). Then

\[
\begin{aligned}
\|\mathcal B^T(H^{-1}-p_{k-1}(H))w\|_2^2
&=w^TR_k(H)^2H^{-1}w\\
&\le4q^{2k}\|\mathcal B^{-1}w\|_2^2
\le4\alpha q^{2k},
\end{aligned}
\]

where \(\|w\|_2=\|r_1\|_2\le\alpha\). For \(k=T-1\), the polynomial vector is supported within the first \(T\) blocks; for \(T=1\), take \(p_{-1}=0\). Thus \(\|u_{>T}\|_2\le2\sqrt\alpha q^{T-1}\). Since \(0\le z\le u\), the improved bound is

\[
\boxed{F_\rho(x^{(T)})-F_\rho(x^*)\le2\alpha q^{2(T-1)}
\le2\alpha e^{-2\sqrt\alpha(T-1)}.}
\]

Accordingly, the sharper sufficient stage limit is

\[
T\ge1+\left\lceil\frac1{2\sqrt\alpha}\log_+\frac{2\alpha}{\epsilon}\right\rceil.
\]

## 7. What is charged and what remains open

Every active vertex is in \(S^*\). Its adjacency list can be read once and cached, at total cost at most \(1/\rho\). Evaluating all boundary residuals from current explicit active coordinates costs \(O(\operatorname{vol}(S_t))\) per stage, including updates and comparisons. Deterministic dictionaries or balanced trees introduce only logarithms in exposed state size. Hence graph exposure, repeated boundary evaluation, and explicit iterate reads/writes, **provided the exact iterate has already been computed**, total

\[
\widetilde O\!\left(\frac1{\rho\sqrt\alpha}\right)
\]

through the above stage limit. There is no uncharged terminal graph-wide scan.

But obtaining each exact restricted solution is not free. Dense incremental Cholesky can incur polynomial fill costs; restarting a deterministic Chebyshev/CG solve at every one of these stages introduces another \(\alpha^{-1/2}\) in its straightforward analysis, and approximate signs require further care. The comparison matrix \(\mathcal B\) itself involves Cholesky blocks, so constructing or applying it has not been shown to be cheap. This proof therefore cannot be reported as a proof of OP2.

A remaining sufficient numerical lemma would be a deterministic implementation of these stages (or suitably certified approximate stages) with total arithmetic and materialization cost \(\widetilde O(\operatorname{vol}(S^*)/\sqrt\alpha)\). Persistent Schur response reuse is a possible direction; neither a randomized SDD primitive nor a deterministic \(m^{1+o(1)}\) bound may silently replace the required \(\widetilde O(m)\) subroutine.

### A fully charged forest corollary

For an input tree, or more generally when the induced exact support \(G[S^*]\) is a forest, the arithmetic gap above disappears: every discovered principal graph \(G[S_t]\) is a forest. No final-support oracle is needed. One can simply rebuild a direct forest solve at every batch stage.

To see the cost concretely, root each active tree, form its parent ordering from the cached active incidence entries, and eliminate leaves. If a leaf \(i\) has current diagonal \(\gamma_i>0\), right-hand side \(h_i'\), and coupling \(\beta_i\le0\) to parent \(p\), update

\[
\gamma_p\leftarrow\gamma_p-\beta_i^2/\gamma_i,
\qquad h_p'\leftarrow h_p'-\beta_i h_i'/\gamma_i.
\]

Store the leaf's scalar data. Once the root is solved, back substitution uses

\[
x_i=(h_i'-\beta_i x_p)/\gamma_i.
\]

Positive pivots follow from positive definiteness, and no off-tree fill occurs. Initialization and parent-order construction cost \(O(\operatorname{vol}(S_t))\); elimination and substitution cost \(O(|S_t|)\). Every adjacency read, scalar operation, state word, and boundary evaluation is thus covered by \(O(\operatorname{vol}(S_t))\) per stage. The exact batch-stage theorem proves the full deterministic bound

\[
O\!\left(\frac1\rho\left[1+\frac1{\sqrt\alpha}
\log_+\frac{2\alpha}{\epsilon}\right]\right)
\]

up to deterministic dictionary logarithms, on this forest class. This is a restricted-case theorem only; it supplies no direct sparse-factorization bound for arbitrary cyclic induced supports.

## 8. Why arbitrary chronological decay is false

The all-violations recurrence is essential. For a normalized star with \(m\) leaves,

\[
Q=aI-\frac c{\sqrt m}(e_0{\bf1}_{\rm leaves}^T+{\bf1}_{\rm leaves}e_0^T)
\]

has eigenvalues \(\alpha,a,1\). Fix \(\alpha\in(0,1)\) as a constant and choose \(\rho=c/(2m)\). After the seed-only solve, every leaf is a strict violation, so arbitrary **singleton** safe pivots can admit them in any order. For distinct leaves,

\[
(Q^{-1})_{ij}=\frac{c^2}{a m\alpha}=\Theta(1/m),
\]

even when their admission indices are separated by \(\Theta(m)\). Thus original inverse entries do not decay exponentially with arbitrary pivot-index distance. Eager scalar response updates under such a singleton order can take quadratic work. This is only an obstruction to that implementation or decay claim, not an OP2 lower bound; all-violations batching admits the leaves together.

## 9. Primary background sources

- Foniok, Fukuda, Gärtner, Lüthi, *Pivoting in Linear Complementarity: Two Polynomial-Time Cases*, especially Theorem 5.6: [arXiv paper](https://arxiv.org/abs/0807.1249). It establishes short K-matrix pivot paths, not the fully charged RPPR arithmetic target.
- Martínez-Rubio, Wirth, Pokutta, *Accelerated and Sparse Algorithms for Approximate Personalized PageRank and Beyond*, COLT 2023: [PMLR paper](https://proceedings.mlr.press/v195/martinez-rubio23b.html). Its accelerated active-set bounds contain additional sparsity factors; they do not directly give OP2 as stated here.
- Demko, Moss, Smith, *Decay Rates for Inverses of Band Matrices*, Mathematics of Computation 43 (1984): [original AMS paper](https://www.ams.org/mcom/1984-43-168/S0025-5718-1984-0758197-9/S0025-5718-1984-0758197-9.pdf). The approximation-theoretic decay argument in Section 6 is written out here for the particular block-bidiagonal comparison needed above.

The block comparison and resulting batch-stage bound above are an independent derivation; no novelty claim is made without a broader literature audit.

## 10. Certified approximate solves: a forced-recurrence extension

The stage bound does not intrinsically require exact boundary signs or precision depending on the smallest nonzero pivot. It admits the following robust extension, which still does not remove repeated-solve arithmetic.

For an admitted set \(S\), write \(X(S)\) for its exact positive principal solution. Suppose a deterministic restricted solver returns \(\widetilde x\) with

\[
|\widetilde x_i-X_i(S)|\le\delta\sqrt{d_i}\quad(i\in S).
\]

Use the explicitly materialized lower vector

\[
\ell_i=\max\{0,\widetilde x_i-\delta\sqrt{d_i}\}\quad(i\in S),\qquad
\ell_i=0\quad(i\notin S).
\]

Then \(0\le\ell\le X(S)\le x^*\), and \(0\le X_i(S)-\ell_i\le2\delta\sqrt{d_i}\). Admit every outside vertex with \(r_i(\ell)>0\). Since outside residuals increase as old nonnegative coordinates increase, every admitted vertex is also an exact violation of \(X(S)\), so all safe-pivot facts remain valid.

For an omitted outside vertex \(i\),

\[
r_i(X(S))\le r_i(\ell)+\sum_{j\in S}(-Q_{ij})(X_j(S)-\ell_j)
\le 2c\delta\sqrt{d_i}\le\delta\sqrt{d_i}.
\]

The degree factor follows from \(-Q_{ij}=c/\sqrt{d_id_j}\) on edges and the fact that at most \(d_i\) neighbors contribute. No adjacency list of \(i\) must be scanned to compute its residual: its incoming contributions are obtained from the scanned active lists.

Now consider the exact principal solutions on the sets selected by these approximate screens. The key recurrence in Section 4 becomes

\[
r_t\le -L_{t,t-1}z_{t-1}+\eta_t,
\qquad 0\le\eta_t\le\delta\sqrt{d_{B_t}},
\]

where \(\eta_t\) can be chosen as the positive part of the batch's residual one round earlier. Therefore

\[
z_t\le-L_{tt}^{-1}L_{t,t-1}z_{t-1}+L_{tt}^{-1}\eta_t.
\]

For analysis after \(T\) approximate-screen stages, hypothetically continue with exact all-violation stages until the optimum is reached. The first subsequent exact batch can still have a forcing term bounded as above; every later batch has zero forcing. All batches are disjoint subsets of \(S^*\), so the vector \(\eta\) of all forcing blocks satisfies

\[
\|\eta\|_2^2\le\delta^2\operatorname{vol}(S^*)\le\delta^2/\rho.
\]

Induction gives the nonnegative domination

\[
z\le\mathcal B^{-1}(w+\eta),
\]

where \(w\) is the first-block forcing from Section 5. Using \(\|u+v\|_2^2\le2\|u\|_2^2+2\|v\|_2^2\), the sharper whole-tail estimate from Section 6, and \(\|\mathcal B^{-1}\|_2\le\alpha^{-1/2}\), yields

\[
\boxed{
F_\rho(X(S_T))-F_\rho(x^*)
\le4\alpha q^{2(T-1)}+\frac{\delta^2}{\alpha\rho}.
}
\]

For the actual final output \(\ell_T\), principal stationarity on \(S_T\) makes the additional objective difference purely quadratic:

\[
F_\rho(\ell_T)-F_\rho(X(S_T))
=\tfrac12\|\ell_T-X(S_T)\|_Q^2
\le2\delta^2\operatorname{vol}(S_T)\le2\delta^2/\rho.
\]

For example, choose \(\delta^2=\epsilon\alpha\rho/8\) and

\[
T\ge1+\left\lceil\frac1{2\sqrt\alpha}
\log_+\frac{8\alpha}{\epsilon}\right\rceil.
\]

Then the geometric term is at most \(\epsilon/2\), the forcing term at most \(\epsilon/8\), and the output term at most \(\epsilon/4\), so the returned lower vector has gap below \(\epsilon\).

If an approximate screen finds no violating vertex early, every exact positive residual is bounded by \(\delta\sqrt d\). Such exact violations belong to \(S^*\); strong convexity gives the direct bound

\[
F_\rho(X(S))-F_\rho(x^*)\le\frac{\|r(X(S))_+\|_2^2}{2\alpha}
\le\frac{\delta^2}{2\alpha\rho},
\]

and adding the same final-output error justifies early termination.

A full Euclidean error bound \(\|\widetilde x-X(S)\|_2\le\delta\) is a sufficient, stronger way to obtain the required coordinate certificate because \(d_i\ge1\). It can be obtained deterministically by a standard Chebyshev restricted solve, or certified from \(\|Q_{SS}\widetilde x-h_S\|_2\le\alpha\delta\). This takes \(\widetilde O(\operatorname{vol}(S)/\sqrt\alpha)\) arithmetic for one solve. Repeating it across the accelerated number of stages still gives only a straightforward \(\widetilde O(1/(\rho\alpha))\) total bound. Thus this extension removes a **sign-certification and precision gap**, but it does not remove the principal remaining **arithmetic amortization gap**.
