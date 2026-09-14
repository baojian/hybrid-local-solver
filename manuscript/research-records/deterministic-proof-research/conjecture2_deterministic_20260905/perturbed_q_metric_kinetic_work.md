# Perturbed energies and kinetic work under deterministic density errors

This is an abstract perturbation theorem for the completed algorithm. It
quantifies the errors that a directed-rounding or fixed-point implementation
must realize. It does not assert that the existing exact reporter already
satisfies this error model, or prove a complete bit-complexity theorem.
No randomization is used.

## 1. Error model

Fix one certified stage with regularization `r<=1`, `lambda=alpha*r`,
`0<=s=b-Qbar<=4lambda*w`, `m_s=w^Ts<=alpha`, and true correction
`e*=x*_r-bar>=0`. Use the box and mass cap

    C={z:0<=z<=4r*w, w^Tz<=1}.

Let `theta<=1/2`, `mu=theta^2<=alpha<4mu`, and `a=1-theta`.
Every stored state `x,z` is a specified mathematical vector in C. Form

    y=(x+theta*z)/(1+theta),
    raw=a*z+theta*y-(Qy-s+lambda*w)/theta.

Model the numerical mirror calculation by

\[
 p_0=\operatorname{Proj}_C(raw+u),\qquad p=p_0+e_p,
 \qquad x^+=a x+\theta p+e_x.                              \tag{1}
\]

Assume the following certified density bounds and directions:

\[
 |u|\le\kappa_r w,\qquad
 -\kappa_p w\le e_p\le0,\qquad
 -\kappa_x w\le e_x\le0,\qquad p,x^+\ge0.                 \tag{2}
\]

Thus p and xplus remain in C automatically. The first vector captures raw
gradient, fixed-source, response, and arithmetic errors. The second captures
downward projection rounding, and the third downward primal-state rounding.
The exact p0 is an analytical vector and need not be explicitly computed.
A projection implementation must nevertheless justify its representation
in the form (1)--(2); feasibility alone is insufficient.

The model is stated for one iteration. The bounds can vary by iteration,
in which case the recurrences below use their corresponding values.

## 2. Two dimension-independent matrix inequalities

The normalized RPPR matrix satisfies

\[
 |Qv|\le\kappa w\quad\hbox{if }|v|\le\kappa w,
 \qquad w^T|Qv|\le w^T|v|.                               \tag{3}
\]

The first follows from the absolute row sums of the degree-scaled Q matrix.
For the second, symmetry and `|Q|w=w` give
`w^T|Qv|<=w^T|Q||v|=w^T|v|`.
These bounds avoid summing uniform density errors over the unknown graph.

Let

    J(x)=x^T Qx/2-(s-lambda*w)^T x,
    A(x)=||Qx-s||^2/2+alpha*lambda*w^T x,
    t=Q^{-1}s.

Both t and e* are in C. Define the two comparison energies

\[
 E(x,z)=J(x)-J(e^*)+\tfrac\mu2\|z-e^*\|_2^2,
 \quad
 B(x,z)=A(x)-A(t)+\tfrac\mu2\|z-t\|_Q^2.                  \tag{4}
\]

The second energy need not be nonnegative.

## 3. Raw-density error costs at most 2 mu kappa_r

For the ideal perturbed projection p0, the Euclidean normal
`n0=raw+u-p0` satisfies the Euclidean sector at e* and the single-comparator
Q sector at t. The latter follows from the same lower, upper, and mass
normal signs as in the exact theorem, regardless of the raw input.

Replacing `raw+u` by `raw` subtracts the inner product with u. Since both
comparison vectors and p0 have mass at most one, (3) gives

\[
 |\langle p_0-e^*,u\rangle|\le2\kappa_r,
 \qquad |\langle p_0-t,Qu\rangle|\le2\kappa_r.
\]

The accelerated comparison identity therefore yields, for
`x0plus=a*x+theta*p0`,

\[
 E(x_0^+,p_0)\le a E(x,z)+2\mu\kappa_r,
 \qquad B(x_0^+,p_0)\le a B(x,z)+2\mu\kappa_r.            \tag{5}
\]

This step does not assume Euclidean projection is generally Q-nonexpansive.

## 4. Downward rounding has a mass-controlled energy cost

Let `d=xplus-x0plus=theta*e_p+e_x`. Then `d<=0`,
`|d|<=(theta*kappa_p+kappa_x)w`, and its lost mass is at most one because
both x0plus and xplus are nonnegative, and x0plus has mass at most one.
Write `kappa_d=theta*kappa_p+kappa_x`. Thus

    ||d||^2<=kappa_d*w^T|d|<=kappa_d.

Also `w^T|Qx0plus-s|<=1+alpha<=2`. The regularization terms decrease when
d is nonpositive. Exact quadratic expansion and (3) consequently give

\[
 J(x^+)-J(x_0^+)\le\tfrac52\kappa_d,
 \qquad A(x^+)-A(x_0^+)\le\tfrac52\kappa_d.               \tag{6}
\]

For the auxiliary quadratic, use `|Qd|<=kappa_d*w` for its linear term and
`||Qd||^2<=||d||^2` for its quadratic term.

Similarly, the mirror mass loss is at most one, so
`||e_p||^2<=kappa_p`. The weighted absolute masses of `p0-e*` and `p0-t`
are at most two. Hence each mirror-distance term in (4) increases by at
most `5*mu*kappa_p/2`, including the Q-metric term by (3).

Combining with (5) proves

\[
 \boxed{\quad E_{k+1}\le aE_k+\zeta_k,\qquad
 B_{k+1}\le aB_k+\zeta_k,\quad}                          \tag{7}
\]

where

\[
 \boxed{\quad
 \zeta_k=2\mu\kappa_{r,k}
       +\tfrac52\kappa_{x,k}
       +\tfrac52(\theta+\mu)\kappa_{p,k}.
 \quad}                                                  \tag{8}
\]

For uniform bounds, set `Gamma=zeta/theta`. Then

\[
 E_k\le a^kE_0+\Gamma,
 \quad B_k\le a^kB_0+\Gamma,
 \quad \|Q(x_k-e^*)\|^2\le18\alpha^2r+4\Gamma.           \tag{9}
\]

For nonuniform bounds, use the explicitly maintained convolution
`Gamma_(k+1)=a*Gamma_k+zeta_k`, `Gamma_0=0`, in place of Gamma.
Upward bounds on this scalar provide a meaningful rounded stopping
certificate once the implementation has certified (1)--(2).

## 5. The perturbed selected ledger still bounds repeated support work

Use the mass coordinates of the exact proof and let
`Cstar=supp(x*_(r/2))`, `Bvol=K*vol(Cstar)<=2K/r`. Let Dout count all
emitted kinetic degree-volume outside Cstar over the K iterations.

At a coordinate selected by the actual rounded mirror p, `p>e*` implies
`p0>=p>e*`. Thus the lower normal of p0 is absent. The upper and cap normals,
and the additional downward rounding ep, all subtract nonnegative mass.
The only new adverse term in the selected raw identity is
`theta*D^(1/2)u`, whose density magnitude is at most `theta*kappa_r`.

Consequently the exact selected-flow argument gives

\[
 \frac\lambda2D_{\rm out}
 \le\sqrt{(D_{\rm out}+B_{\rm vol})H_2}
       +\nu(D_{\rm out}+B_{\rm vol}),\qquad
 \nu=\theta\kappa_r,                                    \tag{10}
\]

where

\[
 H_2\le K(18\alpha^2r+4\Gamma)
\]

under uniform error bounds. Downward primal rounding does not add a direct
term to this raw identity; its influence is already covered by (9).

Assume

\[
 \boxed{\nu\le\lambda/4.}                               \tag{11}
\]

Then (10) implies

    Dout<=Bvol+4*sqrt((Dout+Bvol)*H2)/lambda.

Put `Y=Dout+Bvol` and apply
`4*sqrt(Y*H2)/lambda<=Y/2+8H2/lambda^2`. Since total kinetic volume is at
most Y, this gives the explicit perturbed bound

\[
 \boxed{\quad
 \sum_k\operatorname{vol}(\operatorname{supp}p_k)
 \le\frac{16H_2}{\lambda^2}+\frac{8K}{r}.
 \quad}                                                  \tag{12}
\]

In particular, if `Gamma<=alpha^2*r`, then

\[
 \boxed{\quad\sum_k\operatorname{vol}(\operatorname{supp}p_k)
 \le360K/r.\quad}                                       \tag{13}
\]

This theorem permits perturbed support decisions. It needs no smallest
nonzero activation margin and no sum over unexposed vertices.

## 6. Concrete sufficient precision budgets

For a stage gap target `tau<=alpha^2*r`, choose K so that
`a^K<=tau/2`, using the initial bound `E0<=1`. It is sufficient to realize

\[
 \boxed{
 \kappa_r\le\frac{\tau}{12\theta},\qquad
 \kappa_x\le\frac{\theta\tau}{15},\qquad
 \kappa_p\le\frac{\tau}{15(1+\theta)}.
 }                                                        \tag{14}
\]

Each of the three contributions to `Gamma=zeta/theta` is then at most
`tau/6`, so `Gamma<=tau/2`. The actual stored point has objective gap at
most tau. Moreover `theta*kappa_r<=tau/12<=lambda/4` because
`tau<=alpha^2*r<=lambda`. Thus the perturbed kinetic bound (13) also holds.
The completed proof's conservative tolerance satisfies these inequalities.

The required density errors are inverse-polynomial in the displayed input
parameters and target gap. Their bit precision is therefore logarithmic in
those inverse quantities. This observation is not by itself an arithmetic
implementation theorem: accumulation in lazy response records, weighted
aggregate sums, source evaluation, and threshold projection must still be
shown to meet the three errors in (14), at the charged work bound.

## 7. What this establishes and what remains to implement

The abstract analytic obstacle is resolved under (1)--(2): simultaneously
controlling the two energies and the kinetic ledger does not require a
dimension-dependent error norm. Uniform density error in the raw step is
absorbed into the outside residual margin, and downward rounded states have
energy costs controlled by their feasible mass.

A concrete finite-precision implementation still needs all of the following
facts, not just a small machine unit roundoff:

1. Its lazy stored vectors denote feasible nonnegative states and can be
   related to the exact recurrence by the pointwise errors (2).
2. Its clipped waterfill output is below the projection of a raw vector
   whose density error is certified, with the stated uniform downward loss.
3. Its source and response errors are controlled without rescanning all
   historical coordinates at every iteration. Periodic, explicitly paid
   scalar rebases are allowed.
4. The final baseline repair is certified for the actual stored candidate,
   for example using the projected-gradient certificate and rounded repair
   in `finite_precision_repair_and_scaling.md`.
5. Any word-to-bit complexity claim includes integer labels, original
   degrees, represented input parameters, rounding precision, and all
   refinement/rebase operations. The original theorem intentionally treats
   these as exact-real words instead.

The root is analyzing this arithmetic realization independently. Until it
is proved, the precise certified alternative is to run a candidate numerical
stage, evaluate the end-stage certificate, and accept only a passing repaired
baseline; a failed certificate triggers deterministic refinement. Such an
acceptance rule certifies correctness but alone does not prove the desired
precision-dependent running time or number of refinements.
