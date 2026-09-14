# Exact warm forcing, linear residual stability, and incremental contraction

These are fresh deterministic lemmas for the dyadic-continuation route.
The nonlinear support-work theorem is still open. In particular, the
incremental contraction below does not by itself imply the required bound
on the gradient of the error relative to the optimizer.

## 1. The true warm correction has a globally small error gradient

Use the notation of `dyadic_warm_corrector.md`: `lambda=alpha*rho`,
`x_o=x*_(2rho)`, `e*=x*_rho-x_o`, `h=b-lambda*w-Q*x_o`, and
`S=supp x*_rho`, `M=vol(S)<=1/rho`. The exact old KKT conditions give
`|h|<=lambda*w` everywhere. On `S`, `Qe*=h`. Outside `S`, nonnegativity of
`e*` and the Stieltjes signs imply `Qe*<=0`, while new KKT and the lower
bound on `h` give `Qe*>=h>=-lambda*w`.

Since `Qw=alpha*w`,

\[
 \sum_{i\notin S}w_i|(Qe^*)_i|
 =\sum_{i\in S}w_i h_i-\alpha w^Te^*
 \le\lambda M.
\]

It follows that

\[
 \boxed{\ \|Qe^*\|_2^2\le2\lambda^2 M.\ }                    \tag{1}
\]

The initial orthant gradient mapping is `G(0)=-[h]_+`. Every coordinate
where `h_i>0` lies in `S`: if the new correction were zero there, its
nonpositive off-diagonal response could not meet `Qe*-h>=0`. Thus

\[
 \boxed{\ \|G(0)\|_2^2\le\lambda^2M.\ }                     \tag{2}
\]

These estimates involve global vectors but have a local bound. They do
not sum the negative forcing entries at unvisited coordinates.

## 2. Unrestricted linear acceleration has the desired squared-residual sum

Let `alpha*I<=Q<=I`, `theta=sqrt(alpha)`, `a=1-theta`, and consider the
ordinary lazy accelerated quadratic iteration without projections, started
from rest. For an eigenvalue `t` of `Q`, the relative residual polynomial
`p_k(t)` satisfies

\[
 p_0=1,\quad p_1=1-t,\quad
 p_{k+1}=\frac{2(1-t)}{1+\theta}p_k
          -\frac{a(1-t)}{1+\theta}p_{k-1}.
\]

For `alpha<t<1`, define

\[
 r=\sqrt{\frac{a(1-t)}{1+\theta}},\quad
 \cos\phi=\sqrt{\frac{1-t}{1-\alpha}}.
\]

The exact expression is

\[
 p_k(t)=r^k\left[\cos(k\phi)+\theta\cot\phi\sin(k\phi)\right].
\]

The endpoint `t=alpha` is the continuous limit
`p_k=(1+k*theta)*a^k`; the endpoint `t=1` vanishes after the initial term.
Using `|sin(k*phi)|<=k*sin(phi)` and `r<=a` gives the uniform envelope

\[
 |p_k(t)|\le(1+k\theta)a^k.
\]

Moreover,

\[
 \sum_{k\ge0}(1+k\theta)^2a^{2k}
 =\frac1{1-a^2}+\frac{2\theta a^2}{(1-a^2)^2}
   +\frac{\theta^2a^2(1+a^2)}{(1-a^2)^3}
 \le\frac5{4\theta}.                                      \tag{3}
\]

For the last inequality, multiply by `theta*(1+a)^3`; the nonnegative
numerator of the difference is
`(1-a)*(4*a^3+7*a^2+8*a+1)/4`.
Spectral decomposition therefore proves

\[
 \boxed{\quad
 \sum_{k\ge0}\|Q(x_k-x^*)\|_2^2
 \le\frac5{4\theta}\|Q(x_0-x^*)\|_2^2.
 \quad}                                                    \tag{4}
\]

The same bound holds for `L0=Q-alpha*I` on the left. Combined with (1),
this is `O(lambda^2*M/theta)` for the unrestricted exact warm corrector.
It is not yet a theorem for changing obstacle faces or the cap projection.

## 3. The projected lazy map is incrementally contractive

This lemma holds for any closed convex projection set `C`, fixed quadratic
Hessian `alpha*I<=Q<=I`, and the same fixed affine forcing in both
trajectories. It does not require an orthant, box, or a support assumption.

Take differences between two states and write them as `x,z`, with

\[
 y=\frac{x+\theta z}{1+\theta},\qquad
 r=a z+\theta y-Qy/\theta.
\]

Let `p` be the difference of the two projected mirror outputs. Firm
nonexpansiveness of Euclidean projection gives

\[
 \langle p,r-p\rangle\ge0.
\]

The new primal difference is `xplus=a*x+theta*p`. Define
`E(x,z)=(||x||_Q^2+alpha*||z||^2)/2` and `L0=Q-alpha*I`.
Direct expansion gives the exact identity

\[
\begin{aligned}
 aE(x,z)-E(x^+,p)
 ={}&\frac{\alpha\theta(1-\alpha)}2\|z-y\|_2^2
      +\frac{a\alpha}2\|z-y\|_{L_0}^2
      +\frac\theta2\|y\|_{L_0}^2\\
    &+\frac12\|x^+-y\|_{I-Q}^2
      +\alpha\langle p,r-p\rangle.
\end{aligned}                                               \tag{5}
\]

Every term is nonnegative, so

\[
 E_{\rm difference,new}\le a E_{\rm difference,old}.          \tag{6}
\]

The identity can be obtained by completing the smooth quadratic step
using `xplus=y-Qy+theta*(p-r)`, followed by
`||p||^2=||r||^2-||p-r||^2+2<p,p-r>`.
The last term in (5) is exactly the projection-sector contribution; no
coordinatewise comparison of the projections is used.

Apply (6) to two consecutive states of a single trajectory from zero.
For the boxed/simplex corrector, `x_1=theta*z_1` is coordinatewise at most
`[h]_+`, so its first difference energy obeys

\[
 E_{\Delta,0}=\tfrac12\|x_1\|_Q^2
              +\tfrac\alpha2\|z_1\|_2^2
 \le\|[h]_+\|_2^2\le\lambda^2M.
\]

Consequently,

\[
 \boxed{\quad
 \sum_{k\ge0}\alpha\|z_{k+1}-z_k\|_2^2
 \le\frac{2\lambda^2M}{\theta}.
 \quad}                                                     \tag{7}
\]

This is a useful nonlinear squared-velocity budget at the desired scale.
It does not automatically bound the cumulative squared `L0` error relative
to the optimizer, which is the missing support-work quantity.

## 4. A valid pointwise support interface requiring two stability bounds

Let `xi` be the correction position, `y=(xi+theta*z)/(1+theta)`, and
`F(xi)=J_rho(x_o+xi)`. Let `G(y)=y-[y-grad F(y)]_+` be its orthant gradient
mapping. For any selected mirror coordinate,

\[
 \theta z_{{\rm raw},i}=y_i-\nabla F_i(y)-a\xi_i>0.
\]

Here selection after the nonnegative cap multiplier implies positivity of
the raw coordinate, even if its upper box bound is attained. Thus the
ordinary projected-gradient point is positive there, and
`G_i(y)=grad F_i(y)`.

Outside `C=supp x*_(rho/2)`, the true KKT residual obeys
`rstar_i>=lambda*w_i/2`, and
`rstar_i=G_i(y)-(Q(y-e*))_i` at every selected coordinate. Therefore

\[
 \operatorname{vol}(Z_{k+1}\setminus C)
 \le\frac8{\lambda^2}
       \left(\|G(y_k)\|_2^2+\|Q(y_k-e^*)\|_2^2\right).       \tag{8}
\]

Proving cumulative bounds on both squared quantities in (8) at scale
`lambda^2*M/theta` would establish the desired continuation-stage work.
The separate selected-flow reduction being written by the root needs only
one cumulative squared `L0` error and is potentially sharper.

## 5. A tempting but invalid use of the velocity budget

One must not turn (7) into a selected-forcing bound by reversing the mirror
identity. If `n=zraw-znew` is the projection normal and `rstar` is the true
KKT residual, the correct identity is

\[
 -L_0(y-e^*)=\theta(z_{k+1}-z_k)
             +\alpha(z_k-e^*)+r^*+\theta n.                 \tag{9}
\]

On selected positive-error coordinates `znew>e*`, the box/simplex normal
is nonnegative. Equation (9) gives a lower bound involving the velocity,
not the upper bound required to charge positive forcing. The proposed
closure based on the opposite sign is invalid and has been withdrawn.
No support theorem is claimed from (7) alone.
