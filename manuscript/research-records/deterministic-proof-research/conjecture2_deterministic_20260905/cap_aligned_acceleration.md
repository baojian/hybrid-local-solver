# Cap-aligned deterministic acceleration: convergence proved, work bound open

This is a fresh construction based only on the permitted RPPR definitions and current-task derivations. No randomized operation is used. The result below is an accelerated convergence theorem with explicit support handling; it is not yet an OP2 work theorem.

Write `w_i=sqrt(d_i)`, `lambda=alpha rho`, and

\[
H(x)=\tfrac12x^TQx-b^Tx+\lambda w^Tx,\qquad
C=\{x\geq0:w^Tx\leq1\}.
\]

The RPPR optimum belongs to `C`. Put `theta=sqrt(alpha)`, `a=1-theta`, and initialize `x=z=0`. One iteration is

\[
y=\frac{x+\theta z}{1+\theta},\qquad g=\nabla H(y),\qquad p=y-g,
\]

\[
z^{\rm raw}=az+\theta y-g/\theta,
\qquad z^+=P_C(z^{\rm raw}),\qquad
v=ax+\theta z^+,
\]

\[
\boxed{x^+=\min\{[p]_+,v\}\quad\text{coordinatewise}.}
\tag{1}
\]

## Why the alignment matters

When `x,z in C`, their convex combination `y` belongs to `C`. Since `I-Q>=0` and `w^T(I-Q)=(1-alpha)w^T`,

\[
w^T((I-Q)y+b)=(1-\alpha)w^Ty+\alpha\leq1.
\]

Consequently the ordinary projected-gradient point `[p]_+` already obeys the mass cap. Only the auxiliary `z` projection can bind. Merely capping `z` while keeping `[p]_+` as the next `x` allows newly positive coordinates that the `z` cap rejects. Formula (1) removes precisely such newborn coordinates.

The Euclidean weighted-simplex projection has the form

\[
z_i^+=\max\{z_i^{\rm raw}-\nu w_i,0\},\quad\nu\geq0,
\]

with `nu=0` if the positive-part mass is at most one, otherwise chosen so `w^Tz^+=1`. The algebraic identity

\[
\theta z^{\rm raw}=p-ax
\tag{2}
\]

implies the exact aligned identity

\[
\boxed{\theta z^+=[x^+-ax]_+.}
\tag{3}
\]

Indeed, if `z_i^+>0`, then `p_i=ax_i+theta z_i^++theta nu w_i`, so `x_i^+=ax_i+theta z_i^+`. If `z_i^+=0`, (1) gives `x_i^+<=ax_i`. Therefore `supp(z^+) subset supp(x^+)`; furthermore, if `x_i=0` and `x_i^+>0`, then `z_i^+>0`. A cap-rejected new coordinate cannot become a new `x` support element.

Both points remain feasible: `v in C` by convexity, and `0<=x^+<=v` implies `x^+ in C`. This last implication uses the downward-closed nature of the mass-capped orthant, not arbitrary convexity alone.

## Self-contained accelerated energy proof

Let `x*` be the RPPR optimum and define

\[
E(x,z)=H(x)-H(x^*)+\frac\alpha2\|z-x^*\|_2^2.
\]

The proposed `x^+` is exactly the Euclidean projection of `p` onto the box `[0,v]`. Since `v` itself belongs to that box,

\[
\|x^+-p\|^2\leq\|v-p\|^2
=\alpha\|z^+-z^{\rm raw}\|^2,
\tag{4}
\]

where (2) was used. Smoothness of `H` gives

\[
H(x^+)\leq H(y)-\tfrac12\|g\|^2
+\tfrac12\|x^+-p\|^2.
\tag{5}
\]

Because `x* in C`, the projection Pythagorean inequality gives

\[
\|z^+-x^*\|^2\leq\|z^{\rm raw}-x^*\|^2
-\|z^+-z^{\rm raw}\|^2.
\tag{6}
\]

Multiply (6) by `alpha/2` and add (5). The terms in (4) cancel. Expanding

\[
z^{\rm raw}-x^*=a(z-x^*)+\theta(y-x^*)-g/\theta
\]

cancels the two `||g||²/2` terms. Use

\[
\theta(z-y)=y-x
\]

to rewrite the remaining linear-gradient contribution as

\[
a\langle g,x-y\rangle+\theta\langle g,x^*-y\rangle.
\]

Apply strong convexity from `y` to `x` and `x*`, with weights `a` and `theta`. The `theta ||y-x*||²` terms cancel, leaving

\[
E(x^+,z^+)\leq aE(x,z)
-\frac{\alpha a}{2}\|x-y\|^2
-\frac{\alpha a\theta}{2}\|z-y\|^2.
\]

Since `||x-y||²=alpha ||z-y||²` and `a(1+theta)=1-alpha`,

\[
\boxed{E(x^+,z^+)\leq(1-\sqrt\alpha)E(x,z)
-\frac{\alpha\sqrt\alpha(1-\alpha)}2\|z-y\|^2.}
\tag{7}
\]

Thus objective convergence is accelerated. At `alpha=1` the seed-only separable problem is solved immediately, so there is no singular edge case.

## Deterministic local projection and remaining work question

The raw auxiliary coordinate is nonpositive outside the current support, its exposed boundary, and the seed. Projection onto `C` can only decrease coordinates. Sorting positive exposed breakpoints `z_i^{raw}/w_i`, with weights `d_i`, therefore finds the water-filling multiplier deterministically without a global graph scan. In degree coordinates the projection is `max(z_i^{raw}/w_i-nu,0)`, with weighted mass `sum_i d_i y_i<=1`; only scalar arithmetic and comparisons are needed when `theta` is represented exactly.

One full current-support adjacency scan computes the gradient; `z` adds no separate scan because of (3). Sorting and materialization cost is charged in the number of exposed records. The simple instantaneous bound is still only

\[
\operatorname{vol}(\operatorname{supp}(x^+))\leq1/(\alpha\rho),
\]

from the nonnegative incoming mass. It does not establish OP2. A cumulative support or auxiliary-support ledger is still required; neither the mass cap nor accelerated energy alone proves it.

## Further valid caps, without an asserted work improvement

The seed is in the optimal support in the nonzero regime. Summing optimality over the support shows `w^Tx* + rho vol(S*) <=1`, so the known tighter mass cap `w^Tx<=1-rho d_v` is valid. A maximum principle also gives the uniform degree-coordinate upper bound

\[
0\leq x_i^*/w_i\leq1/d_v-\rho.
\]

At a positive nonseed maximum, the degree-coordinate equation would say `a y_i <=c y_i-alpha rho`, an impossibility; the maximum is therefore at the seed. Its row equation then yields the bound. Intersecting `C` with these upper boxes preserves the convergence proof, since the set remains convex and downward closed. No improved volume theorem follows from these caps here.
