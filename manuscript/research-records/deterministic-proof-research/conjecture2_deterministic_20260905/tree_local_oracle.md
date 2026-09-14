# Exact local tree obstacle solving: threshold messages and a branching-depth bound

Date: 2026-09-05. This note proves a local exact oracle with a branching-depth parameter and identifies the remaining gap to a universal near-linear local tree oracle. The only existing manuscript read is the specified problem-definition file. No randomized primitive is used.

**Status:** A universal O(vol(S*) polylog vol(S*)) local bound is neither proved nor refuted here. The concrete algorithm below achieves

\[
O\bigl((\operatorname{vol}(S^*)+|S^*|(B^*+1))\log(2+\operatorname{vol}(S^*))\bigr),
\]

where B* is the maximum number of active vertices of **full input degree at least 3** on a seed-to-support path. In particular this is a near-linear exact local oracle for paths, stars, and trees with polylogarithmic branching depth. The bound has no alpha or accuracy factor. All claims use exact arithmetic.

## 1. Point-seed structure

Root the input tree at seed v. Work in degree coordinates y_i=x_i/sqrt(d_i), with

\[
H=aD-cA,\quad a=(1+\alpha)/2,\quad c=(1-\alpha)/2,
\quad f=\alpha(e_v-\rho d).
\]

Assume 0<alpha<1 and f_v>0; otherwise alpha=1 is diagonal, or f_v<=0 makes the zero vector optimal.

Every connected component of positive coordinates contains a vertex with positive forcing. Otherwise its principal equation would have a strictly negative right-hand side and an inverse-positive principal matrix, contradicting positivity. Since only the seed has positive forcing, S* is a connected rooted subtree.

For a nonroot child i whose parent is p, if y_i=0 then all descendants of i are zero. Its inactive residual is

\[
r_i=f_i+c y_p=-\alpha\rho d_i+c y_p.
\]

Therefore i is positive precisely when

\[
y_p>\tau_i,\qquad \tau_i=\alpha\rho d_i/c.
\]

For necessity, if the parent is at or below this threshold, setting the entire child subtree to zero satisfies its conditional KKT conditions: the child residual is nonpositive and every deeper forcing is negative. Uniqueness makes this its conditional optimum. Conversely, a child at zero with parent above threshold would violate stationarity. This threshold requires the child's full degree, but not its adjacency list.

For a current connected safe active set S, every inactive boundary child has the same residual formula. A strict violation is a safe M-matrix pivot. Thus one may reveal a child's adjacency list **only after** its parent has crossed this threshold in the exact current principal solution. Every revealed list belongs to S*. Degrees of boundary stubs cost at most one query per exposed active incidence entry.

## 2. Constant-size current subtree messages

Fix a current positive principal solution on S. For an active rooted subtree with root i, eliminating its descendants yields

\[
\tfrac12\gamma_i y_i^2-b_i y_i+\text{constant},\qquad \gamma_i>0.
\]

Let beta_i be the minimum value of y_i at which any currently inactive boundary descendant becomes a strict violation, assuming all currently active descendants retain their linear principal equations. Store a witness boundary child attaining this minimum. Set beta_i=+infinity when that subtree has no inactive boundary.

This definition only encodes exact affine principal equations, not a claim that all those equations stay feasible for every hypothetical y_i. Comparisons are used at the current positive principal solution, where they are valid.

For a length-one active child edge (i,j), eliminating the child message contributes

\[
\gamma_i\mathrel{-}=c^2/\gamma_j,
\qquad b_i\mathrel{+}=c b_j/\gamma_j.
\]

Since y_j=(c y_i+b_j)/gamma_j, the child subtree's next boundary threshold in y_i is

\[
\tau_{i\leftarrow j}=(\gamma_j\beta_j-b_j)/c.
\]

At i, beta_i is the minimum of all child-subtree thresholds and all direct inactive-child thresholds alpha rho d/c. A deterministic indexed heap stores this minimum and its witness. The diagonal and RHS contributions are maintained by sums. When one child message changes, only one heap entry and two sums change.

At the seed, the exact current value is y_v=b_v/gamma_v. The condition y_v>beta_v identifies a strict boundary violation through its stored witness. If y_v<=beta_v, all inactive residuals are nonpositive, and the positive principal solution is the global obstacle optimum.

A naive implementation updates every ancestor after a pivot. The next section removes full-degree-2 chains from that ancestor cost.

## 3. Exact compression of degree-2 chains

An active full-degree-2 vertex with both neighbors active has no unseen side branch. Such internal vertices can be condensed. Keep as explicit junctions the seed, active full-degree-at-least-3 vertices, active physical leaves, and the current active endpoint of each unfinished degree-2 chain.

For a compressed chain with endpoints u,z, after eliminating its internal vertices its contribution has the form

\[
E(u,z)=\tfrac12 A u^2-Buz+\tfrac12 C z^2-fu-gz+\text{constant},\qquad B>0.
\]

Endpoint unary terms are excluded; internal unary terms are included. For a single edge, A=C=f=g=0 and B=c. The endpoint diagonal coefficients need not be positive individually; the actual internal elimination pivots are positive because the underlying principal matrix is SPD.

Two chain contributions can be joined at an internal vertex z with unary (a d_z/2)z^2-f_z z. If the first chain has coefficients (A,B,C,f,g) and the second has (A',B',C',f',g'), put

\[
K=C+a d_z+A'>0,\qquad q=g+f_z+f'.
\]

Eliminating z gives the composed coefficients

\[
\begin{aligned}
A_{\rm new}&=A-B^2/K,& C_{\rm new}&=C'-(B')^2/K,\\
B_{\rm new}&=BB'/K,& f_{\rm new}&=f+Bq/K,\\
g_{\rm new}&=g'+B'q/K.
\end{aligned}
\]

This is constant work. Store the back-substitution equation

\[
z=(Bu+B'w+q)/K
\]

for final recovery. In particular, extending a current degree-2 frontier by one newly active vertex appends one edge, absorbs the previous frontier's unary, and updates this chain summary in constant work. A new physical branching vertex becomes a new explicit junction instead.

If a child junction j has subtree coefficients (gamma_j,b_j,beta_j), and its chain from parent junction i has coefficients (A,B,C,f,g), put D=C+gamma_j>0. The contribution to the parent's message is

\[
A-B^2/D\quad\hbox{on its diagonal},\qquad
f+B(g+b_j)/D\quad\hbox{on its RHS}.
\]

The child value is

\[
y_j=(B y_i+g+b_j)/D,
\]

so the next descendant boundary event occurs at parent potential

\[
\tau_{i\leftarrow j}=(D\beta_j-g-b_j)/B.
\]

Again these are constant-size updates. The parent's heap stores this single key for the entire active child chain/subtree.

## 4. Local algorithm and work accounting

Start with the seed-only positive principal solve and reveal its adjacency list. Create one degree-known inactive stub per child, keyed by alpha rho d/c.

Repeatedly compare the seed value b_v/gamma_v with beta_v. If there is a strict violation, take the stored witness boundary child, safely admit it, and only then reveal its adjacency list. Create its new boundary stubs. Extend a degree-2 chain or create a new junction as appropriate. Recompute the affected message and update the single affected contribution/key at each compressed ancestor through the root.

The old exact positive solution need not be explicitly rewritten after each activation: its principal solution is represented by the current Schur messages. The next boundary test is exact from the scalar threshold invariant. At termination, traverse the compressed tree to recover junction values, then reverse the stored chain eliminations to recover every active coordinate. This costs O(vol(S*)).

Every vertex is admitted at most once and is in S*. Total adjacency reading and stub creation cost O(vol(S*)); heap initialization and changes for those stubs add only a logarithm. Between a newly admitted vertex and the root, all compressed internal ancestors other than the root have full input degree at least 3. Thus there are at most B*+1 message updates per activation, each involving O(1) arithmetic and an O(log(2+vol(S*))) indexed-heap operation.

Total work is consequently

\[
O\bigl((\operatorname{vol}(S^*)+|S^*|(B^*+1))\log(2+\operatorname{vol}(S^*))\bigr).
\]

Storage is O(vol(S*)), apart from implementation bookkeeping. There is no inactive-branch scan, final-support oracle, global residual scan, numerical margin dependence, or uncharged repeated materialization of old iterates.

## 5. Static piecewise-linear messages and the remaining locality issue

For a **fully supplied finite tree**, one can instead consider its complete obstacle response R_i(t): the optimum value at child i when its parent is fixed at t. For point-seed negative nonroot forcing, define on u>=0

\[
F_i(u)=a d_i u-f_i-c\sum_{j\text{ child of }i}R_j(u).
\]

This is strictly increasing and piecewise linear; its inverse gives R_i(t)=0 when ct<=F_i(0), and R_i(t)=F_i^{-1}(ct) otherwise. Parametric monotonicity implies each vertex activates at most once, so the number of breakpoints in a subtree response is at most its number of vertices.

The affine-composition-tree data structure supports evaluation, inverse evaluation, ordered breakpoint updates, and lazy planar affine transformations. Small-to-large addition of response functions followed by the affine map (u,z)->((a d_i u-f_i-cz)/c,u) is a natural way to represent these static messages with polylogarithmic overhead. Retaining versions or reversible operation records is needed for final reconstruction. Flat zero pieces require the straightforward generalized-inverse/domain convention rather than assuming strict bijectivity everywhere.

Primary source for the data structure: Agarwal, Phillips and Sadri, *Lipschitz Unimodal and Isotonic Regression on Paths and Trees*, Section 3, [author-hosted paper](https://www.cs.toronto.edu/~sadri/publications/regression.pdf). Its problem is different; its static data-structure operations must not be cited as a theorem granting the local obstacle oracle here.

In the local setting, discovering a new branch changes response maps along its ancestor path. The preceding exact local algorithm handles that path explicitly after compressing degree-2 chains. Replacing the remaining branching-depth factor by a universal polylogarithm requires a dynamic/lazy message-melding argument with fully charged maintenance. The static affine-composition-tree result alone does not provide it. No general near-linear local oracle is claimed in this note.


## 6. Exact-arithmetic checks

The scalar message and minimum-threshold invariant were checked with rational arithmetic against independent dense principal solves on a 16-vertex path, a 16-vertex star, a 31-vertex binary tree, and a 20-vertex comb. At every safe addition, the message seed value equaled the principal solution exactly, its threshold test agreed with explicit evaluation of every boundary residual, and the reported witness was a strict violation. The examples finished with 8, 16, 31 and 10 active vertices respectively.

The two-port composition formulas were separately checked with rational arithmetic against direct Schur elimination on chains of lengths 2 through 8. All coefficients agreed exactly. These checks validate the algebra on the stated examples; the complexity bound follows from the message/chain invariants above, not from the probes. No random graph or randomized arithmetic was used.
