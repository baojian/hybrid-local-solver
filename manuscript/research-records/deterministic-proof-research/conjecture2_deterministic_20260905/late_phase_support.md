# A deterministic late-phase kinetic-support bound

This is fresh work for Conjecture 2. It proves a support-volume lemma for the
lazy capped accelerated recurrence, but does **not** prove the conjecture:
obtaining the required warm start within the desired local work is unresolved.
No randomness is used.

The fresh acceleration subagent independently audited the proof, including
the margin, the sign of the diagonal term, boundary-edge multiplicities,
and the final constant, on 2026-09-05.

## Setup

Let `0 < alpha < 1`, `theta = sqrt(alpha)`, `a = 1-theta`,
`c = (1-alpha)/2`, `w_i = sqrt(d_i)`, and

\[
 Q=\alpha I+cD^{-1/2}(D-A)D^{-1/2},\qquad
 J_\rho(x)=\tfrac12x^TQx-\alpha e_s^TD^{-1/2}x
                  +\lambda w^Tx,\quad \lambda=\alpha\rho.
\]

All iterates are nonnegative. Let `xstar` minimize `Jrho` over the orthant.
The lazy capped accelerated state satisfies

\[
 u=D^{1/2}x,\qquad v=\theta D^{1/2}z,\qquad 0\le v\le u.
\]

Its next kinetic vector is

\[
 v_i^+=[q_i-\eta d_i]_+,\quad \eta\ge0,\qquad
 q=\frac a2\bigl(P(u+v)-(u-v)\bigr)+\alpha e_s-\lambda d,
 \quad P=AD^{-1}.
\]

The multiplier `eta` enforces `sum_i v_i^+ <= theta`. Its value is irrelevant
to the present estimate except for its nonnegativity. Define

\[
 E=J_\rho(x)-J_\rho(x^*)+\frac\alpha2\|z-x^*\|_2^2.
\]

Let `C = supp(xstar_(rho/2))` and `M = vol(C) <= 2/rho`.

## Uniform outside-core margin

Write `rstar = D^(1/2) grad Jrho(xstar)`. Monotonicity for the Stieltjes
obstacle problem gives `0 <= xstar_rho <= xstar_(rho/2)`. Therefore, on
`j outside C`, both optimizers vanish, and the nonpositive off-diagonals give

\[
 r_j^*\ge\frac\lambda2d_j.
\]

Indeed, at the smaller-regularization optimum the gradient of `J_(rho/2)` is
nonnegative. Replacing that optimum by the smaller `xstar_rho` can only
increase the gradient on a coordinate where both are zero; changing the
regularization adds `lambda*w/2`.

For `e=x-xstar`, the exact quadratic expansion and complementarity imply

\[
 J_\rho(x)-J_\rho(x^*)
 =\tfrac12e^TQe+\nabla J_\rho(x^*)^Tx
 \ge\tfrac12\|e\|_Q^2+\frac\lambda2\sum_{j\notin C}u_j.
\]

Consequently, with `m_out = sum_(j outside C) u_j`,

\[
 \|e\|_Q\le\sqrt{2E},\quad
 \theta\|z-x^*\|_2\le\sqrt{2E},\quad
 m_{\rm out}\le\frac{2E}{\lambda}.
\]

## Boundary-flux estimates

Let `b_i` be the number of edges from `i in C` to the complement, and let
`B = sum_(i in C)b_i <= M`. The boundary sum below counts each boundary edge
once. Write `f_i=e_i/sqrt(d_i)`. On the complement, `f_j=u_j/d_j >= 0`.
Thus

\[
 \begin{aligned}
 T_x&:=\sum_{i\in C,j\notin C}A_{ij}(f_i)_+\\
 &\le\sum_{i\in C,j\notin C}A_{ij}(f_i-f_j)_+
       +\sum_{i\in C,j\notin C}A_{ij}f_j\\
 &\le\sqrt{\frac Mc}\,\|e\|_Q+m_{\rm out}
 \le\sqrt{\frac{2ME}{c}}+m_{\rm out}.
 \end{aligned}
\]

For the kinetic error,

\[
 \begin{aligned}
 T_z&:=\sum_{i\in C,j\notin C}A_{ij}
       \left(\frac{\theta(z_i-x_i^*)}{\sqrt{d_i}}\right)_+\\
 &\le\theta\left(\sum_{i\in C}\frac{b_i^2}{d_i}\right)^{1/2}
                      \|z-x^*\|_2
 \le\sqrt{2ME}.
 \end{aligned}
\]

The first estimate uses the actual edge Dirichlet energy; a global
Euclidean estimate would unnecessarily lose a factor `1/sqrt(alpha)`.

## Support-volume theorem

Let `Zplus = supp(vplus)`. Then

\[
 \boxed{\quad
 \operatorname{vol}(Z^+)
 \le M+(2+\sqrt2)\frac{\sqrt{ME}}\lambda
          +6a\frac E{\lambda^2}.
 \quad}
\]

To prove this, substitute the fixed-point pair
`ustar = D^(1/2)xstar`, `vstar = theta*ustar` into the raw map. Direct
algebra gives `qstar = theta*ustar-rstar`. For `j outside C`, therefore,
`qstar_j <= -lambda*d_j/2`.

Let `delta_u=u-ustar`, `delta_v=v-vstar`. Outside `C`,
`delta_u-delta_v=u-v >= 0`, so the diagonal part of

\[
 q-q^*=\frac a2P(\delta_u+\delta_v)-\frac a2(\delta_u-\delta_v)
\]

is nonpositive. For every `j in Zplus outside C`, `q_j > 0`, because
`eta >= 0`. Summing these strict inequalities and enlarging the nonnegative
incoming sums gives

\[
 \frac\lambda2\operatorname{vol}(Z^+\setminus C)
 \le\frac a2\left(T_x+T_z+2m_{\rm out}\right).
\]

Here the final term bounds incoming mass from the complement using
`0 <= v <= u` and column stochasticity of `P`. Insert the flux estimates:

\[
 \frac\lambda2\operatorname{vol}(Z^+\setminus C)
 \le\left(\sqrt{\frac a{1+\theta}}+\frac a{\sqrt2}\right)\sqrt{ME}
       +\frac{3a}{2}m_{\rm out}
 \le\left(1+\frac1{\sqrt2}\right)\sqrt{ME}
       +\frac{3aE}{\lambda}.
\]

Adding `vol(Zplus intersect C) <= M` proves the boxed inequality.

In particular, if `E <= alpha^2*rho`, then

\[
 \operatorname{vol}(Z^+)\le\frac{10+2\sqrt2}{\rho}
 <\frac{13}{\rho}.
\]

## Consequence and precise missing step

Once the state reaches `E <= alpha^2*rho`, energy contraction makes the same
condition hold subsequently, and the remaining
`O(alpha^(-1/2) log(alpha^2*rho/epsilon))` steps use
`O(1/(rho*sqrt(alpha)))` times logarithmic factors of fully charged work
under the lazy threshold reporter.

This theorem by itself does not bound the work before that energy level.
Starting from zero gives only `E0 <= alpha/d_s`; substituting the whole
geometrically decreasing energy sequence into the theorem leaves an
unacceptable initial-work term.

A regularization increment `Delta rho = O(sqrt(alpha)*rho)` between exact
solutions creates energy at the desired scale, but naive continuation
requires too many such warm-start solves. No claim is made that this
observation alone provides an accelerated continuation algorithm.

## Exact-solution continuation calculation

Let `rho'=(1-delta)rho`, let `x0=xstar_rho`, and initialize both accelerated
state vectors to `x0` for the new objective. Put `h=xstar_rho'-x0 >= 0`,
`Delta lambda=alpha*delta*rho`, and `M'=vol(supp xstar_rho')<=1/rho'`.
The variational inequalities and strong convexity imply

\[
 \|h\|_Q\le\Delta\lambda\sqrt{M'/\alpha},\qquad
 J_{\rho'}(x_0)-J_{\rho'}(x_{\rho'}^*)
 \le\frac{(\Delta\lambda)^2M'}{2\alpha}.
\]

Since the mirror-distance contribution is at most the same upper bound,

\[
 E_{\rho'}(x_0,x_0)
 \le\frac{(\Delta\lambda)^2M'}\alpha
 \le\frac{\alpha\delta^2\rho}{1-\delta}.
\]

Thus an exact-solution decrement with `delta=Theta(sqrt(alpha))` supplies
the late-phase energy scale. One cannot silently treat these exact warm
starts as free.

For a general approximate state, the elementary center-change estimates
give a transfer inequality of the form

\[
 \sqrt{E_{\rho'}(x,z)}
 \le\sqrt{E_\rho(x,z)}
       +O\bigl(\delta\sqrt{\alpha\rho}\bigr).
\]

Using only this estimate with the accelerated contraction keeps the energy
at `O(alpha^2*rho)` only for decrements of order `delta=O(alpha)` per step.
This is a limitation of this generic transfer argument, not a lower bound
on all possible continuation or predictor schemes.
