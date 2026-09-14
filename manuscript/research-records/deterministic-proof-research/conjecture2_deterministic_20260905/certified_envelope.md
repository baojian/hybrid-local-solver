# Certified lower envelopes for deterministic restricted RPPR solves

Status: proved deterministic safety and objective-certificate lemmas; the OP2 cumulative-work bound remains open. Only the permitted problem-definitions manuscript note was read.


This lemma identifies what is available, and what remains missing, for an adaptive approach. Use the exact normalization of the problem definitions and write

\[
w_i=\sqrt{d_i},\qquad h=b-\alpha\rho w.
\]

On nonnegative vectors, RPPR is the obstacle quadratic

\[
\Phi(x)=\tfrac12x^TQx-h^Tx,\qquad x\geq0.
\]

Let `S` contain the seed, and suppose its unconstrained restricted solution

\[
z_S=Q_{SS}^{-1}h_S
\]

is strictly positive. Extend it by zero outside `S`. Then `z<=x_rho^*`. Indeed, with `g^*=Qx_rho^*-h>=0`,

\[
Q_{SS}(x^*_{\rho,S}-z_S)
=-Q_{S,S^c}x^*_{\rho,S^c}+g^*_S\geq0,
\]

and `Q_SS^(-1)>=0`.

For any approximate restricted solve `v_S`, compute the residual and scalar certificate

\[
e_S=h_S-Q_{SS}v_S,\qquad
\eta=\|D_S^{-1/2}e_S\|_\infty,\qquad\delta=\eta/\alpha.
\]

The degree-scaled principal matrix

\[
B_S=D_S^{-1/2}Q_{SS}D_S^{1/2}
\]

is an M-matrix with `B_S one >= alpha one`, since deleting outside columns removes nonpositive entries. Inverse positivity gives `B_S^(-1)one <= (1/alpha)one`. Therefore

\[
|v_S-z_S|\leq\delta w_S.
\]

Define a lower envelope by

\[
\ell_i=\max\{0,v_i-\delta w_i\}\quad(i\in S),
\qquad\ell_i=0\quad(i\notin S).
\tag{18}
\]

Then

\[
0\leq\ell\leq z\leq x_\rho^*,\qquad
0\leq z_S-\ell_S\leq2\delta w_S.
\tag{19}
\]

Taking a coordinatewise maximum with any previous certified lower envelope preserves safety and the second bound. Notice that (18) does **not** assert `Q_SS ell_S<=h_S`; order safety is the invariant here, not coordinatewise residual sign.

### Safe admissions

For any boundary vertex with

\[
r_i(\ell):=h_i-Q_{iS}\ell_S>0,
\tag{20}
\]

admission is safe. More generally, let `J` consist of any such vertices and `T=S union J`. Since off-diagonal entries of `Q` are nonpositive and `ell<=z`,

\[
h_J-Q_{JS}z_S\geq h_J-Q_{JS}\ell_S>0.
\]

If `z` is extended by zeros on `J`, the expanded restricted solution satisfies

\[
z_T^{\rm new}-z_T
=Q_{TT}^{-1}
\begin{pmatrix}0\\h_J-Q_{JS}z_S\end{pmatrix}\geq0.
\tag{21}
\]

The new coordinates are strictly positive because the inverse has positive diagonal entries and every new residual is positive. Old coordinates remain strictly positive. The earlier comparison with `x_rho^*` applies again. Thus every admitted vertex is in the true optimal support, and throughout the algorithm

\[
\operatorname{vol}(S)\leq1/\rho.
\]

The initial set `{v}` satisfies the positivity assumption in the nonzero point-source regime `rho<1/d_v`.

### An objective certificate when no lower-envelope boundary residual is positive

If (20) holds for no boundary vertex, all coordinates outside `S` satisfy the obstacle optimality inequality at `ell`; vertices outside `S union boundary(S)` have zero diffusion contribution and are nonseed vertices. A subgradient of the original RPPR objective can then be chosen to vanish outside `S`. On `S`, its magnitude is at most that of `Q_SS(ell_S-z_S)` coordinatewise.

The absolute row sums of `B_S` are at most `1` (diagonal `(1+alpha)/2`, absolute off-diagonal row sum at most `(1-alpha)/2`). Thus (19) gives

\[
|g_i|\leq2\delta w_i\quad(i\in S),
\qquad g_i=0\quad(i\notin S).
\]

At a zero coordinate one selects zero if it lies in the subdifferential interval, otherwise the endpoint nearest zero; this can only decrease the magnitude. Strong convexity now gives

\[
F_\rho(\ell)-F_\rho(x_\rho^*)
\leq\frac{\|g\|_2^2}{2\alpha}
\leq\frac{2\delta^2\operatorname{vol}(S)}{\alpha}
\leq\frac{2\delta^2}{\alpha\rho}.
\tag{22}
\]

It suffices to solve until `delta<=sqrt(alpha rho eps_obj/2)` before the boundary test.

### Fully charged work and the remaining gap

All operations in this paragraph are deterministic. On each current `S`, conjugate gradients can attain the required residual in

\[
\widetilde O\bigl(\operatorname{vol}(S)/\sqrt\alpha\bigr)
\]

work because the principal matrix spectrum lies in `[alpha,1]`. This includes the sparse matrix-vector products, scalar arithmetic, and a final residual scan; the omitted logarithms involve `1/alpha`, `1/rho`, and `1/eps_obj`. The lower envelope and a complete boundary test require `O(vol(S))` work: scan adjacency lists only of `S`, accumulate the boundary contributions, and charge all boundary degree replies, state accesses, and comparisons. The number of boundary records is at most `vol(S)` even though boundary volume itself can be arbitrarily larger. No boundary adjacency lists are scanned unless their vertices are later safely admitted.

For an explicit iteration bound, initialize each restricted CG solve at zero. Since `0<=z<=x_rho^*<=x_0^*` and exact PageRank has unit mass,

\[
\|z\|_{Q_{SS}}^2=h_S^Tz_S
\leq b_S^Tz_S\leq\alpha/d_v\leq\alpha.
\]

The standard CG energy estimate and `lambda_max(Q_SS)<=1` imply

\[
\eta_k\leq\|h_S-Q_{SS}v_k\|_2
\leq2\sqrt\alpha\left(\frac{1-\sqrt\alpha}{1+\sqrt\alpha}\right)^k
\leq2\sqrt\alpha\exp(-2k\sqrt\alpha)
\quad(0<\alpha<1).
\]

Thus taking

\[
k\geq\frac{1}{2\sqrt\alpha}
\max\left\{0,\log\frac{2\sqrt2}{\alpha\sqrt{\rho\,\varepsilon_{\rm obj}}}\right\}
\]

(rounded up, or terminating earlier at exact convergence) ensures
`eta_k<=alpha sqrt(alpha rho eps_obj/2)`. At `alpha=1` the system is diagonal and one step is enough. Each CG iteration requires one sparse principal-matrix product and `O(|S|)` further scalar operations. All storage for the current support, its adjacency lists, boundary degree replies, and sparse output is `O(vol(S))`; output costs at most that many words. Reusing a previous approximate solve as a warm start can help in practice but is not needed for this bound.

At every unsuccessful boundary test, at least one new true-support vertex can be admitted. This proves finite termination with the objective certificate above, but only yields the naive cumulative bound

\[
\widetilde O\left(
\frac{1}{\sqrt\alpha}\sum_{\text{restricted solves}}\operatorname{vol}(S)
\right)
\subseteq
\widetilde O\left(\frac{1}{\rho^2\sqrt\alpha}\right).
\tag{23}
\]

The inverse-support-volume factor in (23) cannot simply be dropped. A proof of `sum vol(S)=tilde O(1/rho)` for this method, or a persistent numerical mechanism that avoids paying each full restricted solve, is still needed to reach OP2. This supplement is a safe deterministic baseline and a precise missing-amortization statement, not a proof of Conjecture 2.
