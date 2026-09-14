# Tree-preconditioned exact batch solves: a cyclomatic-number extension

Date: 2026-09-05. Root proposed the rank-preconditioner argument; this note audits it and adds a deterministic grounded-resistance calculation and effective-spectrum bound. Only the specified manuscript and fresh task materials were consulted. No randomized primitive is used.

## 1. Degree-form principal system

Let S be any safe admitted set in the exact all-violations algorithm. Write d_i for full input degree, d_S(i) for degree within the induced graph G[S], D=diag(d_i), and c=(1-alpha)/2. With x=D^(1/2)y, the principal equation is

\[
H y=\alpha(e_v-\rho d),\qquad
H=D^{1/2}Q_{SS}D^{1/2}
=\alpha D+c\operatorname{diag}(d-d_S)+cL(G[S]).
\]

Choose any spanning forest F of G[S] by deterministic traversal. If

\[
r(S)=|E(G[S])|-|S|+\#\operatorname{components}(G[S]),
\]

then exactly r(S) induced edges are outside F. For their arbitrarily oriented signed incidence columns b_e, define

\[
T=\alpha D+c\operatorname{diag}(d-d_S)+cL(F),\qquad
U=(\sqrt c\,b_e)_{e\notin F}.
\]

Then

\[
H=T+UU^T,\qquad T\succeq\alpha D\succ0.
\]

The grounding diagonal uses full degree minus current induced degree; it must not be omitted. This preconditioning transforms only an unconstrained principal linear solve. No equivalence between a preconditioned LCP and the original LCP is being asserted.

## 2. An exact tree solve costs linear work

Each component of T has tree off-diagonal pattern. Root the component, eliminate leaves, and store the pivots and one parent multiplier per vertex. Positive definiteness ensures positive pivots. The factor construction and an inverse application cost O(vol(S)) arithmetic, adjacency processing, and explicit state operations.

The full degrees and internal degrees are obtained while scanning the cached active adjacency lists. Constructing the spanning forest and its complement also costs O(vol(S)). No future support or unseen neighbor list is required.

## 3. At most r+1 preconditioned CG steps

The symmetric preconditioned matrix is

\[
A=T^{-1/2}HT^{-1/2}=I+T^{-1/2}UU^TT^{-1/2}.
\]

The positive semidefinite update has rank at most r(S). Thus at most r(S) eigenvalues differ from 1, and A has at most r(S)+1 distinct eigenvalues. Exact-arithmetic PCG therefore solves the principal system in at most r(S)+1 iterations, regardless of the starting vector. This also follows directly by taking the residual polynomial that vanishes at all its distinct eigenvalues.

No square root or explicit transformed matrix is required by the algorithm: standard PCG uses H-vector products, applications of T^(-1), and scalar products. Each iteration costs O(vol(S)); the forest factor is built once per batch. The total per-stage arithmetic is consequently

\[
O((r(S)+1)\operatorname{vol}(S)).
\]

All arithmetic here follows the same exact-real-operation convention as the existing exact batch theorem and forest corollary. A finite-precision implementation needs residual checks and the earlier inexact-screen analysis; the exact distinct-eigenvalue termination assertion itself is not a finite-precision iteration bound.

## 4. Fully charged restricted-class result

Safe admission gives S_t subseteq S*, vol(S_t)<=1/rho. Cycle spaces embed under taking subgraphs, so r(S_t)<=r*=r(G[S*]). Combine the solve cost with the proved batch count

\[
T_{\rm batches}\le1+\left\lceil\frac1{2\sqrt\alpha}
\log_+\frac{2\alpha}{\epsilon}\right\rceil.
\]

The resulting deterministic, fully charged cost is

\[
\widetilde O\!\left(
\frac{r^*+1}{\rho}
\left[1+\frac1{\sqrt\alpha}\log_+\frac{2\alpha}{\epsilon}\right]
\right).
\]

In particular, the OP2 target holds when the induced final support has polylogarithmic cyclomatic number. The algorithm does not receive S* or r*: it builds each current forest and runs exact PCG to convergence. Graph discovery, current boundary evaluation, vector updates, and output materialization are included.

This extends the forest case r*=0. It does not prove the conjecture for general cyclic support graphs, where r* may be Theta(1/rho).

## 5. A computable grounded-resistance spectral parameter

Define

\[
\chi(S,F)=\operatorname{tr}(T^{-1/2}UU^TT^{-1/2})
=c\sum_{e=(i,j)\notin F}(e_i-e_j)^TT^{-1}(e_i-e_j).
\]

Then all eigenvalues of A lie in [1,1+chi]. Consequently a standard PCG/Chebyshev energy estimate uses O(sqrt(1+chi) log(1/tol)) iterations. This can improve the raw cyclomatic bound when many chord directions have small grounded resistance.

The value chi can be computed deterministically in O(vol(S) log|S|) exact arithmetic, without one tree solve per chord. Here is an explicit procedure.

Root each forest component and let kappa_i be its leaf-elimination pivot. For nonroot i with parent p, put f_i=c/kappa_i. The covariance representation of G=T^(-1) is

\[
y_{\rm root}=\xi_{\rm root},\qquad
y_i=f_i y_p+\xi_i,
\]

where the formal independent covariance contributions satisfy Var(xi_i)=1/kappa_i. Equivalently this is just the triangular LDL^T inverse identity. Thus

\[
G_{rr}=1/\kappa_r,\qquad
G_{ii}=1/\kappa_i+f_i^2G_{pp}.
\]

For vertices i,j in the same tree, let l=LCA(i,j), and let P_i be the product of the factors f along the root-to-i path (P_root=1). Then

\[
G_{ij}=G_{ll}\frac{P_i}{P_l}\frac{P_j}{P_l}.
\]

Every chord has endpoints within one forest component. An ordinary deterministic binary-lifting LCA structure takes O(|S| log|S|) preprocessing and O(log|S|) work per query, after which its grounded resistance is

\[
R_T(i,j)=G_{ii}+G_{jj}-2G_{ij}.
\]

No probability distribution needs to be generated or sampled: the covariance language only states the exact inverse-factor algebra. For alpha=1, c=0 and H=T is diagonal, so chi=0 and this auxiliary formula can be skipped. Products and subtraction above are statements in exact arithmetic; interval or stable numerical variants would be needed if chi were used as a floating-point certificate.

## 6. A sharper effective-spectrum estimate

A standard residual-polynomial argument improves the trace-based bound. Order eigenvalues A as lambda_1>=lambda_2>=...>=1. Since sum(lambda_i-1)=chi,

\[
\lambda_{j+1}\le1+\frac\chi{j+1}.
\]

For any integer j>=0, multiply a degree-k Chebyshev residual polynomial on [1,lambda_(j+1)] by

\[
\prod_{i=1}^j(1-\lambda/\lambda_i).
\]

This kills the largest j eigenvalues. On the remaining spectral interval each additional factor lies in [0,1], so it cannot enlarge the error. Therefore after j+k PCG iterations the relative energy error is at most

\[
2\left(\frac{\sqrt{1+\chi/(j+1)}-1}{\sqrt{1+\chi/(j+1)}+1}\right)^k.
\]

If ell=log(2/tol), this gives an iteration bound of order

\[
\min_{j\ge0}\left\{j+\ell\sqrt{1+\chi/(j+1)}\right\}
=O\left(\ell+\chi^{1/3}\ell^{2/3}\right),
\]

also capped by the exact r+1 bound. Choosing j of order chi^(1/3) ell^(2/3) suffices; if this exceeds r, use exact termination instead. The algorithm need not compute the eigenvalues or explicitly deflate: exact PCG minimizes the error over the relevant polynomial space automatically.

This provides an additional deterministic structural parameter, but it still does not establish the general OP2 target. A proof that the relevant r or chi costs amortize over all admission stages is missing. The path obstruction shows that such a bridge must use the preconditioner/response structure rather than merely the orthogonal energy of successive principal solutions.
