# Certified inexact batch discovery with an explicit objective error floor

Date: 2026-09-05. This is a continuation of this agent's independent `batch_pivot_decay.md` derivation, outside the manuscript repository. Only the allowed canonical `problem_definitions/main.tex` and this agent's own new work were used.

**Claim status.** The theorem below establishes a deterministic algorithm with \(\widetilde O(\alpha^{-1/2})\) support-discovery stages and \(\widetilde O(1/(\rho\sqrt\alpha))\) graph-access, boundary-evaluation, and output work. It permits certified inexact restricted solves with no dependence on a smallest nonzero support value or pivot residual. A straightforward deterministic Chebyshev implementation still costs \(\widetilde O(1/(\rho\alpha))\) arithmetic overall. The fully charged OP2 target remains unproved by this route.

## 1. Setup and explicit schedule

Use the canonical \(Q,b,\alpha,\rho,d\) and point seed \(v\). Put

\[
a=(1+\alpha)/2,\quad c=(1-\alpha)/2,\quad
h=b-\alpha\rho D^{1/2}{\bf1},\quad
\phi(x)=\tfrac12x^TQx-h^Tx\quad(x\ge0).
\]

On nonnegative vectors, \(\phi=F_\rho\). Assume \(0<\rho<1/d_v\); the complementary regime has optimum zero. Write \(x^*\) for the unique optimum, \(S^*=\operatorname{supp}(x^*)\), and \(\operatorname{vol}(S^*)\le1/\rho\).

Given objective tolerance \(\epsilon>0\), choose

\[
\boxed{\delta=\sqrt{\epsilon\alpha\rho/8}},\qquad
\boxed{T=1+\left\lceil\frac1{2\sqrt\alpha}
\log_+\frac{8\alpha}{\epsilon}\right\rceil},
\]

where \(\log_+(u)=\max\{0,\log u\}\). Start with \(S_1=\{v\}\).

For \(k=1,\ldots,T\):

1. On \(S_k\), compute \(\widetilde x^{(k)}\) with the deterministic certificate
   \[
   \|Q_{S_kS_k}\widetilde x^{(k)}_{S_k}-h_{S_k}\|_2\le\alpha\delta.
   \]
2. Materialize the lower vector
   \[
   \ell_i^{(k)}=\max\{0,\widetilde x_i^{(k)}-\delta\sqrt{d_i}\}\quad(i\in S_k),
   \qquad \ell_i^{(k)}=0\quad(i\notin S_k).
   \]
3. If \(k=T\), return \(\ell^{(k)}\). Otherwise evaluate every exposed outside residual \(r_i(\ell^{(k)})=h_i-(Q\ell^{(k)})_i\) and let
   \[
   B_{k+1}=\{i\notin S_k:r_i(\ell^{(k)})>0\}.
   \]
   If this set is empty, return \(\ell^{(k)}\); otherwise set \(S_{k+1}=S_k\cup B_{k+1}\), scan newly admitted adjacency lists, and continue.

There is no random choice. Every strict violation of the lower vector is included. Outside the seed and current boundary, an unlisted residual is \(-\alpha\rho\sqrt{d_i}<0\), so it does not need to be queried.

## 2. Safe sets, certified lower vectors, and omitted violations

For any admitted set \(S\), denote the exact principal solution by

\[
X(S)_S=Q_{SS}^{-1}h_S,\qquad X(S)_{S^c}=0.
\]

Inductively this solution is positive on \(S\). Indeed, if an outside batch has positive residual at \(X(S)\), the Schur update is

\[
\delta_B=(Q_{BB}-Q_{BS}Q_{SS}^{-1}Q_{SB})^{-1}r_B>0,
\qquad \Delta_S=-Q_{SS}^{-1}Q_{SB}\delta_B\ge0.
\]

Both assertions follow from the M-matrix inverse signs. A positive principal solution satisfies \(X(S)\le x^*\): global KKT \(Qx^*=h+w^*\), \(w^*\ge0\), gives

\[
Q_{SS}(x^*_S-X(S)_S)=w^*_S-Q_{S,S^c}x^*_{S^c}\ge0.
\]

The numerical certificate in step 1 implies

\[
\|\widetilde x-X(S)\|_2\le\delta,
\]

since \(Q_{SS}\succeq\alpha I\). Because \(d_i\ge1\), this is stronger than \(|\widetilde x_i-X_i(S)|\le\delta\sqrt{d_i}\). Consequently

\[
0\le\ell\le X(S)\le x^*,\qquad
0\le X_i(S)-\ell_i\le2\delta\sqrt{d_i}.
\]

For outside coordinates, increasing old coordinates increases \(r=h-Qx\). Thus every violation of \(\ell\) is a strict violation of \(X(S)\). The safe Schur update applies, proving the induction and

\[
S_k\subseteq S^*,\qquad \operatorname{vol}(S_k)\le1/\rho.
\]

Conversely, if an outside vertex is omitted because \(r_i(\ell)\le0\), then

\[
\begin{aligned}
r_i(X(S))
&\le\sum_{j\in S}(-Q_{ij})(X_j(S)-\ell_j)\\
&\le\sum_{j\in S\cap\mathcal N(i)}
\frac c{\sqrt{d_id_j}}\,2\delta\sqrt{d_j}
\le2c\delta\sqrt{d_i}
\le\delta\sqrt{d_i}.
\end{aligned}
\]

This is the only loss caused by inexact discovery.

## 3. Hypothetical exact completion and Cholesky blocks

Suppose the algorithm reaches its stage budget \(T\). For analysis only, continue from \(S_T\) by admitting all exact violations of \(X(S_T)\), then all exact violations of each successive principal solution, until the optimum is reached. The sets remain subsets of \(S^*\), and finitely many admissions suffice. This continuation is never computed and is not free algorithmic input or preprocessing.

Let its combined batch sequence be \(B_1=\{v\},B_2,\ldots,B_N\); stages through \(T\) use approximate screening, and stages after \(T\) use exact screening. Put

\[
X_t=X(S_t),\quad X_0=0,\quad
\Delta_t=X_t-X_{t-1},\quad
r_t=(h-QX_{t-1})_{B_t}.
\]

Order \(Q_{S_NS_N}=LL^T\) by these batches. Ordinary Cholesky of a positive-definite M-matrix has positive diagonal and nonpositive strictly lower entries, so \(L^{-1}\ge0\). Define

\[
z_t=L_{tt}^{-1}r_t\ge0.
\]

The pivot Schur complement is \(D_t=L_{tt}L_{tt}^T\), the new coordinates are \(\delta_t=(X_t)_{B_t}=L_{tt}^{-T}z_t\), and

\[
\|\Delta_t\|_Q^2=\|z_t\|_2^2.
\]

Furthermore, \(Q\Delta_t=0\) on \(S_{t-1}\). Hence the increments are pairwise Q-orthogonal and

\[
F_\rho(X_T)-F_\rho(x^*)=\tfrac12\sum_{t>T}\|z_t\|_2^2.
\]

## 4. Forced block-bidiagonal recurrence

For \(t\ge2\), define

\[
\eta_t=\bigl[(h-QX_{t-2})_{B_t}\bigr]_+.
\]

If the preceding screen was approximate, Section 2 gives \(0\le\eta_t\le\delta\sqrt{d_{B_t}}\). This includes \(t=T+1\): its first exact-completion batch was omitted by the preceding approximate screen. For \(t\ge T+2\), the preceding screen was exact and \(\eta_t=0\). Set \(\eta_1=0\).

The residual identity gives

\[
r_t\le\eta_t-Q_{B_t,S_{t-1}}\Delta_{t-1,S_{t-1}}.
\]

Eliminate \(O=S_{t-2}\), with \(P=B_{t-1}\). The off-diagonal Schur block is

\[
C_{t,t-1}=Q_{B_tP}-Q_{B_tO}Q_{OO}^{-1}Q_{OP}
=L_{t,t-1}L_{t-1,t-1}^T.
\]

Since \(\Delta_{t-1,O}=-Q_{OO}^{-1}Q_{OP}\delta_{t-1}\) and \(\delta_{t-1}=L_{t-1,t-1}^{-T}z_{t-1}\),

\[
r_t\le\eta_t-L_{t,t-1}z_{t-1}.
\]

Multiplication by \(L_{tt}^{-1}\ge0\) preserves the inequality:

\[
\boxed{z_t\le-L_{tt}^{-1}L_{t,t-1}z_{t-1}+L_{tt}^{-1}\eta_t.}
\]

Let \(\mathcal B\) retain the diagonal and first block subdiagonal of \(L\). It is a lower triangular M-matrix satisfying

\[
0\le\mathcal B^{-1}\le L^{-1},\qquad
\|\mathcal B^{-1}\|_2\le\alpha^{-1/2},\qquad
\|\mathcal B\|_2\le2.
\]

The first inequality follows from \(L\le\mathcal B\) and
\(L^{-1}-\mathcal B^{-1}=L^{-1}(\mathcal B-L)\mathcal B^{-1}\ge0\).
Nonnegative entrywise domination implies Euclidean norm domination. The bound on \(\mathcal B\) follows by splitting it into block diagonal and first subdiagonal, each of norm at most \(\|L\|_2\le1\).

Let \(w\) be supported on its first block with \(w_1=r_1\). The first block agrees exactly, and induction in the forced recurrence gives

\[
0\le z\le\mathcal B^{-1}(w+\eta).
\]

All forcing batches are disjoint subsets of \(S^*\), so

\[
\boxed{\|\eta\|_2^2\le\delta^2\sum_t\operatorname{vol}(B_t)\le\delta^2/\rho.}
\]

This disjoint-support bound avoids multiplying the error floor by the number of stages.

## 5. Terminal principal-solution error floor

Put \(H=\mathcal B\mathcal B^T\) and \(q=(2-\sqrt\alpha)/(2+\sqrt\alpha)\). Then \(H\) is block tridiagonal with spectrum in \([\alpha,4]\). Let \(R_k\) be its normalized Chebyshev residual polynomial, with \(R_k(0)=1\) and \(\max_{[\alpha,4]}|R_k|\le2q^k\), and write \(p_{k-1}(\lambda)=(1-R_k(\lambda))/\lambda\). For \(k=0\), use \(R_0=1\) and \(p_{-1}=0\).

The whole-tail estimate is sharper than summing separate bounds for every inverse block. Since \(\mathcal B^{-1}=\mathcal B^TH^{-1}\), spectral calculus gives

\[
\begin{aligned}
\|\mathcal B^T(H^{-1}-p_{k-1}(H))w\|_2^2
&=w^TR_k(H)^2H^{-1}w\\
&\le4q^{2k}\,w^TH^{-1}w
=4q^{2k}\|\mathcal B^{-1}w\|_2^2.
\end{aligned}
\]

Here

\[
\|w\|_2=\|r_1\|_2=\alpha(1/\sqrt{d_v}-\rho\sqrt{d_v})\le\alpha,
\qquad \|\mathcal B^{-1}w\|_2\le\sqrt\alpha.
\]

For \(k=T-1\), the vector \(\mathcal B^Tp_{k-1}(H)w\) is supported within the first \(T\) blocks by bandwidth, so it has zero tail beyond \(T\). (For \(T=1\), this polynomial vector is simply zero.) Consequently

\[
\boxed{\|P_{>T}\mathcal B^{-1}w\|_2\le2\sqrt\alpha\,q^{T-1}.}
\]

This sharper whole-tail argument was supplied by the root agent and independently checked here.

Let \(P_{>T}\) select the tail blocks. Entrywise domination, the triangle inequality, and \(\|u+v\|^2\le2\|u\|^2+2\|v\|^2\) give

\[
\begin{aligned}
F_\rho(X_T)-F_\rho(x^*)
&=\tfrac12\|P_{>T}z\|_2^2\\
&\le\|P_{>T}\mathcal B^{-1}w\|_2^2
  +\|P_{>T}\mathcal B^{-1}\eta\|_2^2\\
&\le4\alpha q^{2(T-1)}+\frac{\delta^2}{\alpha\rho}.
\end{aligned}
\]

As \(\log(1/q)\ge\sqrt\alpha\),

\[
\boxed{
F_\rho(X_T)-F_\rho(x^*)
\le4\alpha e^{-2\sqrt\alpha(T-1)}
+\frac{\delta^2}{\alpha\rho}.
}
\]

The first term is at most \(\epsilon/2\) under the explicit stage schedule; the second equals \(\epsilon/8\).

## 6. Actual output error and early termination

Both \(X_T\) and \(\ell^{(T)}\) are supported on \(S_T\), and principal stationarity makes their objective difference exactly quadratic:

\[
\begin{aligned}
F_\rho(\ell^{(T)})-F_\rho(X_T)
&=\tfrac12\|\ell^{(T)}-X_T\|_Q^2\\
&\le\tfrac12\|\ell^{(T)}-X_T\|_2^2
\le2\delta^2\operatorname{vol}(S_T)
\le2\delta^2/\rho
=\epsilon\alpha/4\le\epsilon/4.
\end{aligned}
\]

Thus budget termination returns

\[
\boxed{F_\rho(\ell^{(T)})-F_\rho(x^*)\le7\epsilon/8<\epsilon.}
\]

If an approximate screen is empty at an earlier stage on \(S\), every exact outside positive residual satisfies \(r_i(X(S))\le\delta\sqrt{d_i}\). The set \(B=\{i\notin S:r_i(X(S))>0\}\) would be a safe exact batch and is therefore a subset of \(S^*\). Hence \(\|r(X(S))_+\|_2^2\le\delta^2/\rho\). Strong convexity on the nonnegative orthant gives

\[
F_\rho(X(S))-F_\rho(x^*)
\le\frac{\|r(X(S))_+\|_2^2}{2\alpha}
\le\frac{\delta^2}{2\alpha\rho}.
\]

To see the first inequality directly, minimize the strong-convexity lower model at \(X(S)\): its gradient is zero on \(S\), and minimizing each outside quadratic over a nonnegative coordinate retains only its negative gradient. Adding the actual-output error gives

\[
F_\rho(\ell)-F_\rho(x^*)
\le\epsilon/16+\epsilon\alpha/4\le5\epsilon/16<\epsilon.
\]

Therefore early termination is also justified, without computing the unknown exact positive-residual set.

## 7. Fully charged ledger of what this theorem does and does not achieve

- Every admitted list is scanned once. Total initial graph access and cached graph size are \(O(1/\rho)\).
- A boundary evaluation scans the cached active incidence entries and accumulates residual contributions. It costs \(O(\operatorname{vol}(S_k))\), with only logarithmic extra cost for deterministic dictionaries. Degrees of exposed boundary labels can be cached. No recursive scan of an inactive boundary vertex is used.
- Certificate evaluation is one restricted sparse matrix-vector product, plus a vector norm. Lower-vector materialization, boundary comparisons, and sparse output cost at most the same scale.
- Through \(T=\widetilde O(\alpha^{-1/2})\) stages, the preceding operations total \(\widetilde O(1/(\rho\sqrt\alpha))\).
- A deterministic Chebyshev solve on a fixed admitted principal matrix, using its spectrum \([\alpha,1]\), can attain the numerical certificate in \(\widetilde O(\operatorname{vol}(S_k)/\sqrt\alpha)\) work. For example its residual polynomial decreases Euclidean residual by at most \(2((1-\sqrt\alpha)/(1+\sqrt\alpha))^j\). In this regime \(\|h_{S_k}\|_2\le2\alpha\), so only logarithmic precision factors are needed. At \(\alpha=1\), the solve is diagonal.
- Paying that last solve cost independently at every stage yields only \(\widetilde O(1/(\rho\alpha))\) total arithmetic. The present theorem does not provide the reuse needed to improve it. In particular, the analytical Cholesky and comparison matrices are not asserted to be cheaply available.

The remaining question for this route is a deterministic implementation of the repeated restricted responses with a total cost matching the already-proved stage and boundary ledger. Neither randomness nor a hidden polynomial factor in the exposed support size is permissible.
