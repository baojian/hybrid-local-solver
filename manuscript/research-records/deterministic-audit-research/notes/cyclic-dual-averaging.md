# Cyclic dual averaging: independent deterministic route audit

Date: 2026-09-05. Status: **Open** for local OP2.

## Source interface

Lin, Song, and Diakonikolas, ICML 2023, Algorithm 1 and Theorem 1, give a
deterministic accelerated cyclic method for composite convex minimization.
Its smoothness constant is formed from truncated row/column seminorms.
This is the nonrandomized A-CODER algorithm; its variance-reduced variant is
not used. The source provides convergence on a supplied domain, not the
unknown-support locality theorem needed here.

Primary source: https://proceedings.mlr.press/v202/lin23g/lin23g.pdf,
PDF pp. 4--5 (Assumption 2, Algorithm 1, Theorem 1).

## Proved here: a dimension-independent smoothness bound

Use the project's symmetric coordinates. Write

\[
 a=(1-\alpha)/2,\quad P=D^{-1/2}AD^{-1/2},\quad
 K=Q-\alpha I=a(I-P),\quad c=b-\alpha\rho D^{1/2}{\bf1}.
\]

Split the orthant objective as

\[
 f(x)=\tfrac12x^TKx,\qquad
 g(x)=\tfrac\alpha2\|x\|^2-c^Tx+I_{x\ge0}.
\]

This split preserves convexity of both terms, and `g` is alpha-strongly
convex. In particular, putting the entire diagonal of Q into g would make
the remaining smooth term indefinite, so that shortcut is not used.

For singleton coordinate blocks, choose the row seminorm
`K_j = K[j,:]^T K[j,:]`. The source's matrix determining smoothness is

\[
 \widetilde K=U^TU+V^TV,
\]

where U is the upper triangular part of K including its diagonal, and V is
its strictly upper triangular part (after the selected coordinate order).
Indeed, each truncated row seminorm is the outer product of the correspondingly
truncated row. Since P is entrywise nonnegative and has norm one,

\[
 |U|\le a(I+P),\quad |V|\le aP,
 \quad\|U\|_2\le2a,\quad\|V\|_2\le a.
\]

The norm implications use `|Bz| <= |B||z|` and spectral-norm monotonicity for
nonnegative matrices; they do not rely on triangular truncation preserving
norm for arbitrary signed matrices. It follows that

\[
 L_{\mathrm{cyclic}}^2=2\|\widetilde K\|_2\le10a^2.
\]

The readily available conservative choice `L_cyclic=4a=2(1-alpha)` is
therefore valid for every ordering and every principal face. The case
alpha=1 has no off-diagonal interactions and is solved directly.

This removes a possible dimension-dependent loss in the supplied-domain
cyclic theorem. It proves neither support containment nor an amortized
local-work bound. A full sweep over a supplied face has linear edge work;
the number and volume of actually scanned faces remain to be justified.

## A distinct potential locality mechanism

For the noncyclic analogue, and with a rowwise cyclic correction in A-CODER,
the accumulated gradient has a telescoping structure. If p_k is the mixed
cyclic gradient, then

\[
 z_k=\sum_{i<k}a_i\nabla f(x_i)+a_kp_k.
\]

This follows directly from
`q_k=p_k+(a_(k-1)/a_k)(grad f(x_(k-1))-p_(k-1))` and
`z_k=z_(k-1)+a_k q_k`.

Thus a false activation is controlled by accumulated gradients, rather
than by only the latest extrapolated point. It is worthwhile checking whether
this gives a support or volume invariant. No such invariant has been proved.
Overshooting auxiliary coordinates alone neither proves nor refutes it.

## Falsification obligations

1. Sweep canonical connected unit graphs and all seed positions deterministically.
2. Include regularization values immediately above every exact homotopy support
   transition, not only a coarse regularization grid.
3. Test all observable vectors and mixed within-sweep states, and distinguish
   current support, ever-scanned support, and support volume.
4. If a numerical false activation appears, construct an exact rational or
   certified interval replay before recording a counterexample theorem.
5. If no escape appears, derive a symbolic invariant; finite tests are not a
   substitute for proving it.

The audit program is `experiments/cyclic_dual_averaging.py`. Its full-graph
reference optimum is used only for falsification and would not be available
to a local solver.

## Proved here: exact-support containment fails on a canonical tree

The coarse atlas initially missed this failure; component-relative thresholds
are essential when auditing very small boundary signals.

Take the complete rooted binary tree of depth seven (255 vertices, 254 unit
edges), root source, and reverse breadth-first coordinate order. Set

\[
 \alpha=1/10,\qquad
 \rho_0=6561/27330520,\qquad
 \rho=\tfrac{10001}{10000}\rho_0
      =65616561/273305200000.
\]

Use the above split and `L_cyclic=9/5`. An exact rational principal solve
shows that the optimum is positive on levels zero through six and zero on
all leaves. Its leaf slack in degree coordinates is

\[
 (D^{-1/2}(Qx^*-c))_{\rm leaf}
       =6561/1093259200000>0.
\]

Nevertheless, at iteration 61 the A-CODER auxiliary iterate is strictly
positive on every leaf. A 220-bit outward-rounded dyadic interval calculation
encloses its degree-coordinate value in an interval with strictly positive
rational endpoints, both approximately `4.5307597693066986e-8`. Every previous
leaf auxiliary value is certified exactly zero by the same enclosure.

The finite computation is a certificate: all arithmetic, outward rounding,
and square-root enclosures are integer operations, and the exact reference
solution uses Fractions. The complete certificate and endpoints are in
`results/cyclic-interval-witness.json`; its reproducible verifier is
`experiments/cyclic_interval_witness.py`.

The level reduction does not replace the graph by a weighted counterexample.
Every vertex on a level has the same state. Vertices on one level are
nonadjacent, so their within-sweep order has no effect. Dividing a symmetric
vertex state by `sqrt(d_i)` gives the rational degree-coordinate row

\[
 (K_{\rm deg}y)_\ell
  =\tfrac{1-\alpha}{2}
     \left(y_\ell-\frac{y_{\ell-1}+2y_{\ell+1}}{d_\ell}\right),
\]

with the obvious endpoint rows. Coordinate scaling commutes with the
nonnegative proximal map and the common scalar step schedule. Thus the eight
level recurrences exactly represent singleton-coordinate A-CODER on this
finite simple unit graph.

**Scope:** this refutes strict optimal-support containment for this specific
A-CODER realization. It is not a graph-uniform work lower bound and does not
rule out a different deterministic method. A possible weaker bound on total
scanned volume must be investigated separately. Numerical radial families
also show `rho * scanned_volume > 1`, but no asymptotic no-polylog theorem is
claimed from those finite measurements.
