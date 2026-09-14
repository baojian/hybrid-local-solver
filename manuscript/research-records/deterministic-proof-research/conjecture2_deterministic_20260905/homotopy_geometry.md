# Deterministic geometry and exact ledgers for RPPR homotopy

These are fresh mathematical lemmas, not a complete algorithm for Conjecture
2. Exact homotopy optimizers and derivative responses are used to state the
identities; the cost of computing them is not assumed free.

Let `Q` be the RPPR Stieltjes matrix, `w=sqrt(d)`, `Qw=alpha*w`, and
`b=alpha*D^(-1/2)e_s`. Let `x(rho)` minimize

\[
 J_\rho(x)=\tfrac12x^TQx-b^Tx+\alpha\rho w^Tx,\qquad x\ge0.
\]

Write `r(rho)=Qx(rho)-b+alpha*rho*w`, and `S(rho)=supp x(rho)`.

## 1. Least supersolutions, convexity, and a safe secant

The optimizer is the coordinatewise least nonnegative supersolution of
`Qy >= b-alpha*rho*w`. To verify this, let `y` be any such supersolution and
let `I={i:x_i(rho)>y_i}`. On `I`, complementarity gives
`(Qx)_I=(b-alpha*rho*w)_I <= (Qy)_I`. Off-diagonal nonpositivity and
`(x-y)_(I complement)<=0` imply
`Q_II(x-y)_I <= 0`. Since `Q_II^(-1)>=0`, `I` must be empty.

Consequently, `x(rho)` is coordinatewise nonincreasing in `rho`. It is also
coordinatewise convex: for any `0<=t<=1`, the vector
`t*x(rho1)+(1-t)*x(rho2)` is a supersolution at
`rho=t*rho1+(1-t)*rho2`, and hence dominates `x(rho)`.

For `rho1>rho2>rho3`, put

\[
 \beta=\frac{\rho_2-\rho_3}{\rho_1-\rho_2},\qquad
 \ell=x(\rho_2)+\beta\bigl(x(\rho_2)-x(\rho_1)\bigr).
\]

Coordinatewise convexity yields

\[
 0\le\ell\le x(\rho_3),\qquad
 \operatorname{supp}\ell=S(\rho_2).
\]

The exact residual identity is

\[
 Q\ell-b+\alpha\rho_3w=(1+\beta)r(\rho_2)-\beta r(\rho_1).
\]

It is zero on `S(rho1)` and nonpositive on `S(rho2)`. In particular, the
predictor is safe, and its nonzero residual on the current support is
confined to `S(rho2) \ S(rho1)`.

## 2. A uniform box and mass cap for corrections

If `rho_old>rho_new`, put `h=rho_old-rho_new`. Then
`x(rho_old)+h*w` is a supersolution at `rho_new`, because its residual is
exactly `r(rho_old)`. The least-supersolution property gives

\[
 0\le x(\rho_{\rm new})-x(\rho_{\rm old})\le h w,
 \qquad
 w^T\bigl(x(\rho_{\rm new})-x(\rho_{\rm old})\bigr)
 \le\frac h{\rho_{\rm new}}.
\]

The secant error `e=x(rho3)-ell` obeys the same bounds with
`h=rho2-rho3`, because `ell>=x(rho2)`.

Thus a correction problem has a known convex feasible box, and a known
weighted-mass cap. These facts alone do not establish a support-work bound
for an accelerated corrector.

## 3. The derivative path and orthogonal admissions

Parameterize the path by increasing `t=-rho`. Except at its finitely many
support breakpoints, the derivative is

\[
 g(t)=\frac{d x(-t)}{dt},\qquad
 g_{S(t)}=\alpha Q_{S(t)S(t)}^{-1}w_{S(t)},\quad
 g_{S(t)^c}=0.
\]

The support is nested. As `t` increases, `g(t)` is coordinatewise
nondecreasing, and `0<=g(t)<=w`. One can obtain this directly by applying
the M-matrix comparison to nested supports; the upper bound follows either
from the box estimate above or from `Qw=alpha*w`.

Let `Delta g_j` denote the derivative jump at a support admission (a group
of simultaneous admissions is treated as one jump). These vectors are
nonnegative. For an earlier support `S_old` and a later one `S_new`,

\[
 (Q(g_{\rm new}-g_{\rm old}))_{S_{\rm old}}=0.
\]

Every earlier jump is supported on `S_old`, so distinct derivative jumps
are pairwise orthogonal in the `Q` inner product. Starting above the first
activation, where `g=0`, and ending at a support `S_final`, this gives

\[
 \langle\Delta g_i,\Delta g_j\rangle_Q=0\quad(i\ne j),
 \qquad
 \|\Delta g_j\|_Q^2=\alpha w^T\Delta g_j.
\]

For the second identity, pair a jump with the final derivative: orthogonality
identifies this inner product with its squared norm, while
`Qg_final=alpha*w` on the support of the jump. Hence

\[
 \sum_j\|\Delta g_j\|_Q^2
 =\alpha\sum_j w^T\Delta g_j
 =\alpha w^Tg_{\rm final}
 \le\alpha\operatorname{vol}(S_{\rm final}).
\]

At a final breakpoint, omit the derivative jump entering coordinates that
are still zero at the endpoint. Its coefficient in every correction below
is zero, so it does not affect the formulas.

## 4. Secant-error representation for arbitrary step sizes

Take increasing path times `t0<t1<...<tN`, and let
`h_j=t_j-t_(j-1)`. For `j=1,...,N-1`, let

\[
 e_j=x(t_{j+1})-x(t_j)
       -\frac{h_{j+1}}{h_j}\bigl(x(t_j)-x(t_{j-1})\bigr),
\]

where `x(t)` denotes `x(-t)` in this section. For a derivative jump at time
`s`, define the hat coefficient

\[
 \kappa_j(s)=
 \begin{cases}
  (s-t_{j-1})/h_j,&t_{j-1}\le s\le t_j,\\
  (t_{j+1}-s)/h_{j+1},&t_j\le s\le t_{j+1},\\
  0,&\text{otherwise}.
 \end{cases}
\]

Integration of the piecewise constant derivative gives the exact formula

\[
 e_j=h_{j+1}\sum_\ell\kappa_j(s_\ell)\Delta g_\ell.
\]

For each time `s`, the nonzero hat functions have sum at most one. Away
from the two endpoint intervals their sum is exactly one. Consequently,

\[
 \boxed{\quad
 \sum_{j=1}^{N-1}\frac{e_j}{h_{j+1}}
 \le\sum_\ell\Delta g_\ell\le w,
 \qquad
 \sum_{j=1}^{N-1}\frac{w^Te_j}{h_{j+1}}
 \le\operatorname{vol}(S_{\rm final}).
 \quad}
\]

The inequality is coordinatewise in the first display. It holds for
arbitrary step sizes, including constant-factor regularization schedules.

Pairwise orthogonality additionally gives

\[
 \boxed{\quad
 \sum_{j=1}^{N-1}\frac{\|e_j\|_Q^2}{h_{j+1}^2}
 =\sum_\ell\|\Delta g_\ell\|_Q^2
                 \sum_j\kappa_j(s_\ell)^2
 \le\alpha\operatorname{vol}(S_{\rm final}).
 \quad}
\]

For a single correction, `0<=kappa<=1` and the jump energy identity imply

\[
 \|e_j\|_Q^2
 \le\alpha h_{j+1}w^Te_j.
\]

## 5. Exact predictor energy and the algorithmic gap

The safe predictor is supported inside the new true support. Therefore
the linear KKT term at the new optimizer vanishes, and its objective gap
is **exactly** `||e_j||_Q^2/2`. Resetting the mirror point to the predictor
gives accelerated energy at most `||e_j||_Q^2`, since `Q>=alpha*I`.

These identities give a genuine amortized budget for exact predictor
errors: total normalized correction mass is at most the final support
volume, and total normalized correction energy is at most `alpha` times
that volume. They do not yet give a fully charged local algorithm.

In particular, one still needs a deterministic correction procedure whose
actual adjacency work can be charged to these budgets while discovering
new support. Exact prior optimizers, exact derivative responses, or the
future support cannot be assumed available without paying for them.

## 6. What the box and mass cap alone cannot imply

The following is an exact **admissible-state example**, not a trajectory
counterexample. It rules out deriving a uniform `O(1/rho)` kinetic-support
bound solely from the correction box, correction mass cap, the invariant
`0<=v<=u`, and the ordinary initial-energy scale `E=O(alpha*rho)`.

Take an integer `L>=64`, `theta=1/L`, `alpha=1/L^2`, and any integer `N>=L`.
The graph consists of a seed with `N` adjacent hubs, each hub having
`D=floor(L/8)` private leaves. The degrees are `N` at the seed, `D+1` at each
hub, and one at each leaf. Write

\[
 q_0=(1+\alpha)/2,\quad c=(1-\alpha)/2,\quad
 \rho_{\rm old}=1/(2N),\quad
 \rho=\rho_{\rm new}=h=1/(4N).
\]

Both exact optimizers are supported only at the seed. In degree-density
coordinates `f_i=x_i/sqrt(d_i)`, their seed values are

\[
 f_{\rm old}=\frac{\alpha}{2q_0N},\qquad
 f_{\rm new}=\frac{3\alpha}{4q_0N}.
\]

The hub KKT residuals are nonnegative because `D+1>=9`; leaves also have
positive residual. In fact, the optimizer at `rho/2` is still seed-only.
The true correction has seed density `alpha*h/q0`.

Now consider the correction state whose position has seed density
`theta*h` and is zero elsewhere, and whose mirror vector is zero.
This state lies in the box `0<=xi<=h*w`, has mass `theta/4<=h/rho=1`, and
satisfies `0<=v<=u`. Its accelerated energy relative to the true correction
obeys

\[
 \begin{aligned}
 E&=\tfrac12q_0N(\theta h-\alpha h/q_0)^2
       +\tfrac\alpha2N(\alpha h/q_0)^2\\
 &\le\alpha Nh^2=\alpha\rho/4.
 \end{aligned}
\]

Use the lazy correction recurrence with the exact shifted forcing
`b-alpha*rho*w-Q*xold`. At every hub its raw next kinetic mass is

\[
 v_{\rm raw,hub}
 =\alpha h\left(\frac{L-1}{2}+\frac{2c}{q_0}-(D+1)\right)>0.
\]

The seed's raw kinetic value is negative and every leaf's is negative.
The total positive raw mass is less than `theta/8`, so the mass cap
`theta*h/rho=theta` does not bind. Each hub's raw value is also below its
coordinate box cap `theta*h*(D+1)`. Therefore every hub is selected, and

\[
 \operatorname{vol}(Z^+)=N(D+1)
 =\Theta\left(\frac1{\rho\sqrt\alpha}\right).
\]

This can exceed `1/rho` by an arbitrarily large factor. The state has not
been shown reachable from the prescribed zero correction initialization,
and this example does **not** violate the desired cumulative work bound:
one scan of this size is within that bound. It identifies the missing
ingredient precisely: a successful early-phase argument must exploit the
actual trajectory, the secant-error structure, or another invariant beyond
these box, mass, and energy constraints.
