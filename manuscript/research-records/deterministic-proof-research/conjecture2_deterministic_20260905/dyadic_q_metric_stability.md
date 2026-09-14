# Deterministic Q-metric stability of the exact dyadic corrector

This note proves the nonlinear squared-response estimate for an **exact**
dyadic warm-start stage. The mirror box is `2*rho*w`, rather than `rho*w`.
The comparison vector used in the proof is analytical and is never provided
to the algorithm. Section 7 extends the result to safely repaired approximate
warm starts. The root is assembling the complete schedule and work theorem.

## 1. Setup and a positive diffuse source

Let

\[
 Q=\alpha I+cD^{-1/2}(D-A)D^{-1/2},\quad
 c=(1-\alpha)/2,\quad w=\sqrt d,\quad
 b=\alpha D^{-1/2}e_s,
\]

with `0<alpha<1`, `Qw=alpha*w`, and `alpha*I<=Q<=I`. Put
`theta=sqrt(alpha)`, `a=1-theta`, `lambda=alpha*rho`, and let
`x_o=x*_(2rho)` be the exact old RPPR optimizer. Define

\[
 s=b-Qx_o,\qquad h=s-\lambda w,
 \qquad m_s=w^Ts.
\]

The old KKT conditions imply, coordinatewise,

\[
 0\le s\le2\lambda w.                                    \tag{1}
\]

On the old positive support `s=2*lambda*w`; on an old zero coordinate,
`Qx_o<=0` and `b>=0` give `s>=0`, while KKT gives the upper bound.
Furthermore,

\[
 m_s=\alpha(1-w^Tx_o)\le\alpha,
 \qquad \|s\|_2^2\le2\lambda m_s.                         \tag{2}
\]

The comparison vector

\[
 t=Q^{-1}s
\]

satisfies

\[
 0\le t\le2\rho w,\qquad w^Tt=m_s/\alpha\le1.             \tag{3}
\]

The upper bound uses `Q^{-1}>=0` and `Q(2*rho*w)=2*lambda*w`.
Thus `t` belongs to the explicit convex constraint set

\[
 \mathcal B=\{z:0\le z\le2\rho w,\quad w^Tz\le1\}.
\]

It is not necessary to compute `t`.

## 2. The actual iteration

The true nonnegative correction `xi*=x*_rho-x_o` lies in `B`; indeed it
lies in the smaller box `rho*w`. Initialize `xi_0=z_0=0` and use

\[
 \begin{aligned}
 y_k&=(\xi_k+\theta z_k)/(1+\theta),\\
 z_{\rm raw}&=a z_k+\theta y_k-(Qy_k-h)/\theta,\\
 z_{k+1}&=\operatorname{Proj}_{\mathcal B}^{\rm Euclidean}(z_{\rm raw}),\\
 \xi_{k+1}&=a\xi_k+\theta z_{k+1}.
 \end{aligned}                                             \tag{4}
\]

This is the ordinary lazy projected accelerated corrector, with an enlarged
known box. Its usual accelerated convergence proof for the original
correction objective remains applicable because `B` contains `xi*`.

## 3. A Q-weighted sector inequality at the comparison vector

Let `p=Proj_B(raw)` and `n=raw-p`. The Euclidean projection normal has a
KKT decomposition

\[
 n=\eta w+n^{\rm up}-n^{\rm low},\qquad
 \eta,n^{\rm up},n^{\rm low}\ge0,
\]

where `nup_i` can be positive only if `p_i=2*rho*w_i`, `nlow_i` only if
`p_i=0`, and `eta>0` only if `w^Tp=1`.

We claim

\[
 \boxed{\quad\langle p-t,Q(raw-p)\rangle\ge0.\quad}         \tag{5}
\]

Since `Qt=s`, the left side is `(Qp-s)^T n`. Each part of the normal has a
nonnegative contribution:

* At a lower-bound coordinate, `p_i=0` and Stieltjes signs give
  `(Qp)_i<=0<=s_i`. Its product with `-nlow_i` is nonnegative.
* At an upper-bound coordinate, `p_i=2*rho*w_i` and `p<=2*rho*w` give
  `(Qp)_i>=Q(2*rho*w)_i=2*lambda*w_i>=s_i`.
* If the mass multiplier is positive, its contribution is
  `eta*(alpha*w^Tp-m_s)=eta*(alpha-m_s)>=0`.

This proves (5). It is a sector inequality for this single analytical
comparator. It does **not** claim that Euclidean projection is generally
nonexpansive in the `Q` norm, or that it is a `Q`-metric projection.

## 4. Accelerated comparison energy in the Q metric

Consider the auxiliary quadratic

\[
 \mathcal F(\xi)=\frac12\|Q\xi-s\|_2^2
                      +\alpha\lambda w^T\xi.              \tag{6}
\]

Its gradient in the `Q` inner product is exactly

\[
 \nabla_Q\mathcal F(\xi)=Q\xi-s+\lambda w=Q\xi-h.
\]

Its Hessian in this metric is `Q`, so it is `alpha` strongly convex and
one-smooth. The update (4) therefore has the correct gradient for this
auxiliary quadratic as well. Crucially, (5) provides the projection
comparison inequality needed in this metric.

Define

\[
 \mathcal E_k=\mathcal F(\xi_k)-\mathcal F(t)
                       +\frac\alpha2\|z_k-t\|_Q^2.
\]

The usual accelerated estimate gives

\[
 \boxed{\quad
 \mathcal E_{k+1}\le a\mathcal E_k
 -\frac{\alpha\theta(1-\alpha)}2\|z_k-y_k\|_Q^2.
 \quad}                                                    \tag{7}
\]

The comparator `t` need not minimize `F`; hence `E_k` is not asserted to
be nonnegative. The proof of (7) does not use such a claim.

For completeness, write `g=grad_Q F(y)`, `p=znew`, and
`raw=a*z+theta*y-g/theta`. Smoothness and
`xnew=y-g+theta*(p-raw)` give

\[
 \mathcal F(x^+)\le\mathcal F(y)-\tfrac12\|g\|_Q^2
                         +\tfrac\alpha2\|p-raw\|_Q^2.
\]

Equation (5) gives

\[
 \|p-t\|_Q^2\le\|raw-t\|_Q^2-\|p-raw\|_Q^2.
\]

After adding, the projection distances and squared gradient cancel.
Use the strong-convexity inequalities at `xi` and `t`, with coefficients
`a` and `theta`, and use `xi-y=theta*(y-z)`. The remaining negative term is
`-alpha*a*(theta^2+theta)*||z-y||_Q^2/2`, which is the term in (7).
This establishes (7) without assuming optimality of `t`.

## 5. Uniform nonlinear error-gradient bound

Since `Qt=s`,

\[
 \mathcal F(t)=\alpha\lambda w^Tt=\lambda m_s.
\]

The initial comparison energy is

\[
 \mathcal E_0=\tfrac12\|s\|_2^2-\lambda m_s
                         +\tfrac\alpha2t^Ts
 \le\tfrac12\|s\|_2^2\le\lambda m_s,                      \tag{8}
\]

where (3) gives `alpha*t^Ts/2<=lambda*m_s`. From (7),
`E_k<=a^k E_0`. Whether `E_0` is positive or negative, it follows that

\[
 \mathcal F(\xi_k)\le2\lambda m_s,
 \qquad \|Q\xi_k-s\|_2^2\le4\lambda m_s.                  \tag{9}
\]

Now define

\[
 q=s-Q\xi^*=b-Qx^*_\rho.
\]

The new KKT conditions give `0<=q<=lambda*w`, by exactly the same argument
as in (1). Also

\[
 w^Tq=m_s-\alpha w^T\xi^*\le m_s,
 \qquad \|q\|_2^2\le\lambda m_s.                          \tag{10}
\]

Combining (9) and (10) proves the uniform bound

\[
 \boxed{\quad
 \|Q(\xi_k-\xi^*)\|_2^2
 \le2\|Q\xi_k-s\|_2^2+2\|q\|_2^2
 \le10\lambda m_s\le10\alpha^2\rho.
 \quad}                                                    \tag{11}
\]

Because `L0=Q-alpha*I` commutes with `Q` and `0<=L0<=Q`,

\[
 \boxed{\quad
 \sum_{k=0}^{K-1}\|L_0(\xi_k-\xi^*)\|_2^2
 \le10K\alpha^2\rho.
 \quad}                                                    \tag{12}
\]

This is a nonlinear bound for the actual projected trajectory, including
all face changes and cap activations. No spectral commutation of `Q` with
the projection has been used.

## 6. Fully charged stage consequence and remaining interface

The fresh `squared_response_work_reduction.md` proves, for the actual
selected kinetic supports `Z_(k+1)`,

\[
 \sum_{k=0}^{K-1}\operatorname{vol}(Z_{k+1})
 \le\frac8{\lambda^2}\sum_k\|L_0(\xi_k-\xi^*)\|_2^2
                              +\frac{4K}\rho.
\]

Substituting (12) gives

\[
 \boxed{\quad
 \sum_{k=0}^{K-1}\operatorname{vol}(Z_{k+1})\le\frac{84K}\rho.
 \quad}                                                    \tag{13}
\]

Thus an exact dyadic warm-start stage with
`K=O(alpha^(-1/2)*log accuracy)` has the desired deterministic local work,
up to the charged balanced-tree and box-projection logarithms. The
comparison support and vector `t` never become algorithmic inputs.

An exact old optimizer cannot be granted at every regularization level
without cost. Section 7 supplies the required analytic extension and repair
for approximate old baselines; the complete continuation schedule and all
implementation charges are being assembled in the root theorem.

## 7. General source constant and the approximate-baseline interface

The proof extends verbatim to any nonnegative baseline `bar` satisfying

\[
 \bar x\le x^*_\rho,\qquad
 0\le s=b-Q\bar x\le C\lambda w,\qquad w^Ts\le\alpha,
 \qquad C\ge1.
\]

Use the box `C*rho*w` and mass cap one. Then `t=Q^{-1}s` is feasible,
and the single-comparator sector remains valid. The bounds become

\[
 \mathcal F(\xi_k)\le C\lambda m_s,
 \qquad
 \|Q(\xi_k-\xi^*)\|_2^2\le(4C+2)\lambda m_s,
\]

and the squared-response reduction gives

\[
 \sum_k\operatorname{vol}(Z_{k+1})
 \le(32C+20)K/\rho.                                       \tag{14}
\]

In particular `C=4` gives the constants `18` and `148`.

The root independently proposed the following repair, which has been
checked here. Let `r` be the old regularization, let `x_tilde>=0` have
objective gap at most `tau` there, and set

\[
 \eta=\sqrt{2\tau/\alpha},\quad
 \delta=\eta/\alpha,\qquad
 \bar x=[\widetilde x-\delta w]_+.
\]

Strong convexity gives `||x_tilde-x*_r||_2<=eta`, so `delta>=eta` implies
`0<=bar<=x*_r`. Also `Qx*_r<=b`, `||Q||_2<=1`, and `w_i>=1` give
`Qx_tilde-b<=eta*w`. At a positive repaired coordinate, off-diagonal signs
and `bar>=(x_tilde-delta*w)` imply

\[
 (Q\bar x)_i\le(Q\widetilde x)_i-\alpha\delta w_i\le b_i.
\]

At a zero repaired coordinate, `Qbar<=0<=b` holds directly. Hence
`s=b-Qbar>=0`. Importantly, the correct clipping-error estimate is

\[
 0\le x^*_r-\bar x\le(\delta+\eta)w,
\]

not `delta*w`. The absolute row sums of the degree-scaled operator
`D^(-1/2) Q D^(1/2)` are one, so

\[
 |Q(x^*_r-\bar x)|\le(\delta+\eta)w.
\]

Choose

\[
 \tau=\alpha^5r^2/8,
 \quad \delta=\alpha r/2,
 \quad \eta=\alpha^2r/2.
\]

Then `delta+eta<=alpha*r`. Since the exact old source is bounded by
`alpha*r*w`, the repaired source obeys

\[
 0\le b-Q\bar x\le2\alpha r w\le4\alpha\rho w
\]

whenever the next regularization satisfies `r/2<=rho<=r`. Also
`w^Ts=alpha*(1-w^Tbar)<=alpha`, and monotonicity gives
`bar<=x*_r<=x*_rho`. Thus every hypothesis for `C=4` is restored without an
exact old solve. This establishes the analytic approximate-stage interface.
The root is assembling the complete schedule and implementation charges.

Repair is performed only between restarted stages. The Q-metric proof
above uses ordinary accelerated averaging within a stage; an arbitrary
line search or cleanup that decreases only the original objective has not
been shown to preserve the auxiliary comparison energy.

## 8. Dyadic acceleration parameter without square-root operations

An independently checked extension uses a dyadic `theta<=1/2` with
`mu=theta^2<=alpha<4*mu` and replaces the acceleration parameter `alpha`
inside the momentum formulas and comparison energies by `mu`. The graph
matrix and `lambda=alpha*rho` keep the actual PageRank parameter `alpha`.
In particular, the auxiliary penalty in (6) remains `alpha*lambda*w^Txi`.

In mass coordinates the selected-error recurrence becomes

\[
 V_{\rm raw}-V^*
 =\frac{1-\alpha}{1+\theta}K_0(V-V^*)
   -\frac{D^{1/2}(Q-\mu I)(\xi-\xi^*)}{1+\theta}-R^*.
\]

Indeed, the coefficient of `V` is

\[
 (1-\theta)I-\frac{Q-\mu I}{1+\theta}
 =\frac{I-Q}{1+\theta}=
   \frac{1-\alpha}{1+\theta}K_0.
\]

Its scalar stochastic coefficient is at most `1-theta`, so the selected
ledger loses only additional nonnegative mass. The auxiliary quadratic is
`mu` strongly convex in the `Q` metric, and its initial mirror-energy term
is smaller because `mu<=alpha`. Thus all constants in Sections 5--7 persist.
Also `||(Q-mu I)e||<=||Qe||`, and `1/theta<2/sqrt(alpha)`.

Implementation can store degree densities and mass-weighted sources, so
`sqrt(d_i)` also remains analysis notation rather than a numerical primitive.
The repair tolerance can be prescribed directly from `alpha` and the old
regularization; no square root of an observed objective gap is required.
