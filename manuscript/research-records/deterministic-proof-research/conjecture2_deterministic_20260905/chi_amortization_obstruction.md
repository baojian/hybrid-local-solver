# A clique–path obstruction to summing the chord-resistance guarantee

Date: 2026-09-05. This is a deterministic structural counterexample to an attempted bound on the sum of the current chi-based per-stage estimates. It is not an iteration lower bound for actual PCG and not a lower bound for OP2. Only permitted manuscript material and fresh task files were read.

## 1. Family and assertion

For an integer L >= 32, take a clique C on L vertices and attach a path with 2L additional vertices to a designated clique vertex a. The seed s is a different clique vertex. Set

\[
\alpha=L^{-2},\qquad\rho=(1000L^2)^{-1},\qquad M=1/\rho=1000L^2.
\]

The whole clique is admitted at batch 2. The next L batches each admit one successive path vertex. Throughout these batches, for **every** spanning forest F of the current induced support S,

\[
\operatorname{vol}(S)\ge L^2/2,\qquad
\chi(S,F)\ge L^2/64.
\]

Thus

\[
\sum_t\operatorname{vol}(S_t)\chi(S_t,F_t)^{1/3}
\ge\frac18L^{11/3},
\]

whereas M/sqrt(alpha)=1000L^3. All size and accuracy logarithms can be O(log L). The polynomial discrepancy is not hidden by the tilde notation.

This shows that choosing a better spanning forest cannot, by itself, make the existing trace-based CG estimate sum to the OP2 target. Actual PCG can outperform a trace-only estimate, and other structure can still make the graph easy.

## 2. The clique is admitted in batch 2

Write a0=(1+alpha)/2 and c=(1-alpha)/2; a denotes the attachment vertex only. The seed has degree L-1. Its seed-only degree-coordinate value is

\[
y_s=\frac{\alpha(1-\rho(L-1))}{a_0(L-1)}.
\]

At every other clique vertex i, multiplying the next residual by sqrt(d_i) gives

\[
\sqrt{d_i}\,r_i=c y_s-\alpha\rho d_i>0,
\]

because d_i<=L, c/a0>=3/5, rho(L-1)<1/1000, and rho L=1/(1000L). No path vertex is adjacent to the seed, so all its residuals are initially negative. Hence batch 2 consists exactly of the other clique vertices.

## 3. A lower bound at the attachment vertex

First solve on the clique alone. Its full degree vector is L-1 except d_a=L. Put

\[
k=a_0L-\alpha,\qquad B=c+\alpha(L-1).
\]

The non-attachment principal block of the degree-form matrix is kI-cJ. Eliminating those L-1 vertices leaves the scalar equation sigma y_a=F, with

\[
\sigma=a_0L-\frac{c^2(L-1)}B
=\frac{c^2+c\alpha L^2+\alpha^2L(L-1)}B,
\]

\[
F=\alpha\left[\frac cB(1-\rho(L-1)^2)-\rho L\right].
\]

For L>=32, c>=3/8, B<=1, and rho(L-1)^2<=1/1000. Therefore F>alpha/3. The displayed numerator of sigma is at most 1 and B>=3/8, so sigma<3. Consequently

\[
y_a^{(C)}>\alpha/9>\alpha/10.
\]

Safe M-matrix updates are coordinatewise nondecreasing, so every later safe restricted solution still satisfies y_a>=alpha/10.

## 4. The attached path advances for L batches

Suppose j>=1 path vertices have been admitted, with j<=L, and call the current attachment value A=y_a. The degree-coordinate values on the path solve

\[
2a_0y_i-c(y_{i-1}+y_{i+1})=-2\alpha\rho,
\quad y_0=A,\quad y_{j+1}=0.
\]

Let

\[
\eta=\log\frac{L+1}{L-1},\qquad \cosh\eta=a_0/c.
\]

The shifted variable y_i+rho is homogeneous. Its last value is therefore

\[
y_j=\frac{(A+\rho)\sinh\eta+\rho\sinh(j\eta)}{\sinh((j+1)\eta)}-\rho.
\]

For j<=L, (j+1)eta<3, eta>=2/L, and

\[
\frac{\sinh((j+1)\eta)-\sinh(j\eta)}{\sinh\eta}
=\frac{\cosh((j+1/2)\eta)}{\cosh(\eta/2)}\le\cosh3.
\]

Using cosh3-1<10 and A>=alpha/10 gives

\[
y_j\ge\frac{(A-10\rho)\sinh\eta}{\sinh3}
\ge\frac{0.18\alpha}{L\sinh3}>\frac\alpha{64L}.
\]

The next path residual is

\[
r_{j+1}=\frac c{\sqrt2}y_j-\alpha\rho\sqrt2
>\frac\alpha{256L}.
\]

The first path residual, immediately after the clique solve, satisfies the same weaker bound directly from A>=alpha/10. More distant inactive vertices have negative residual and no active neighbor. Thus each succeeding batch admits exactly the next path vertex, at least through L path vertices.

All formulas are applied only after a safe previous stage. Positivity and the stated support sequence therefore follow inductively from the safe-pivot lemma, rather than being assumptions on a possibly infeasible principal solution.

## 5. Every spanning forest has large chi

At every such stage, the induced graph is the whole clique plus a path prefix. Any spanning forest includes all its path bridges and a spanning tree of the clique.

The sum of clique-tree degrees is 2(L-1), so at least 3L/5 clique vertices have tree degree at most 4. Excluding the attachment vertex leaves a set U of at least L/2 vertices for L>=32. At least

\[
\binom{|U|}{2}-(L-1)\ge L^2/16
\]

clique edges with endpoints in U are chords.

For i in U, all incident input edges lie in the admitted clique. Thus its boundary grounding is zero, and

\[
T_{ii}=\alpha d_i+c\deg_F(i)\le1/L+2<3.
\]

For a chord e=(i,j) inside U, T_ij=0. Cauchy–Schwarz in the T inner product gives

\[
b_e^TT^{-1}b_e\ge\frac{(b_e^Tb_e)^2}{b_e^TTb_e}
=\frac4{T_{ii}+T_{jj}}\ge\frac23.
\]

Since c>=3/8, every one of these chords contributes at least 1/4 to chi. Therefore chi>=L^2/64, independently of the forest chosen and independently of how far the path prefix has advanced.

## 6. A polynomial accuracy can require these stages

At each of the first L path additions, the new residual exceeds alpha/(256L). Since Q_SS<=I, the Q-energy of its exact correction is at least the square of that residual. If one of these additions remains, Q-orthogonality of safe-pivot increments yields objective gap at least

\[
\frac{\alpha^2}{131072 L^2}=\frac1{131072L^6}.
\]

The choice epsilon=1/(10^8 L^8) therefore requires all these additions, while log(1/epsilon)=O(log L). Also n=3L, so there is no exponentially large graph hiding the discrepancy.

## 7. Limits of the obstruction

This is a lower bound on the **sum of the proved proxy**, not on realized PCG iterations. The clique has spectral structure that a stronger solver can exploit. Indeed incremental dense factorization on this entire O(L)-vertex example costs O(L^3), which fits M/sqrt(alpha). This motivates a real hybrid theorem, rather than treating the chi trace estimate as universally sharp.
