# Exact warm-start CG repeats a long path correction

Date: 2026-09-05. This is a deterministic implementation obstruction, not a lower bound for OP2. Only the specified problem-definitions manuscript and fresh files from this task were read. No randomized algorithm or construction is involved.

## Statement

Let an integer L >= 8 be given. On the unweighted path with vertices 0,...,2L, seed vertex 0 and set

\[
\alpha=L^{-2},\qquad \rho=(100L)^{-1},\qquad M=1/\rho=100L.
\]

The exact all-violations batch algorithm admits singleton prefixes through at least stage L. Suppose the implementation solves each new principal system by ordinary unpreconditioned CG, starting from the preceding exact principal solution extended by zero, and asks for Euclidean solution error at most

\[
\delta=\alpha^2/1024.
\]

At stage t, for 2 <= t <= L, at least t CG steps are required to meet that accuracy. A conventional full principal sparse matrix-vector product costs Theta(t), so the cumulative work through stage L is Omega(L^3), while the OP2 target M/sqrt(alpha) is Theta(L^2). All relevant logarithms are O(log L), including the accuracy logarithm for the explicit epsilon below.

This disproves an amortization claim based solely on exact warm starts, orthogonality of principal-solution increments, and the standard full-matvec CG implementation. It does not exclude approximate warm starts deliberately retaining useful long-range errors, preconditioning, saved response operators, or structural direct solvers. A direct tridiagonal solve gives the desired bound on this very family.

## Exact Green function

Write a=(1+alpha)/2 and c=(1-alpha)/2. For the prefix S_t={0,...,t-1}, t <= L, let D_t=diag(1,2,...,2) and

\[
H_t=D_t^{1/2}Q_{S_tS_t}D_t^{1/2}=aD_t-cA_{S_tS_t}.
\]

Put

\[
\eta=\log\frac{L+1}{L-1},\qquad \beta=a/c=\cosh\eta.
\]

The first diagonal of H_t/c is beta, the other diagonals are 2beta, and adjacent off-diagonals are -1. The continuant recurrence therefore gives

\[
\det(H_t/c)=\cosh(t\eta).
\]

Cofactors give the two entries

\[
(H_t^{-1})_{0,t-1}=\frac{1}{c\cosh(t\eta)},\qquad
(H_t^{-1})_{t-1,t-1}=\frac{\cosh((t-1)\eta)}{c\cosh(t\eta)}.
\]

These formulas also hold for t=1.

For t <= L, one has t eta <= L eta <= 2 log 3 < 3: the function L log((L+1)/(L-1)) decreases for L > 1, and L >= 2. Also c >= 3/8.

## Positive singleton admissions

Use degree coordinates y=D_t^{-1/2}x. The principal equation is

\[
H_ty=\alpha(e_0-\rho d).
\]

At the missing right boundary,

\[
H_t\mathbf1=\alpha d+c e_{t-1}.
\]

Consequently its last solution coordinate is exactly

\[
y_{t-1}^{(t)}=
\frac{\alpha}{c\cosh(t\eta)}
-\rho\left(1-\frac{\cosh((t-1)\eta)}{\cosh(t\eta)}\right).
\]

Since the cosh ratio is at least exp(-eta),

\[
1-\frac{\cosh((t-1)\eta)}{\cosh(t\eta)}
\le1-e^{-\eta}=\frac2{L+1}\le\frac2L.
\]

It follows that

\[
y_{t-1}^{(t)}\ge
\frac{2\alpha}{\cosh3}-\frac{2\alpha}{100}
>\frac\alpha{10},\qquad t\le L.
\]

If t >= 1, the residual at the next vertex t, whose full degree is 2, equals

\[
r_t(x^{(t)})=\frac c{\sqrt2}y_{t-1}^{(t)}-\alpha\rho\sqrt2
\ge\alpha\left(\frac{3}{80\sqrt2}-\frac{\sqrt2}{200}\right)
>\frac\alpha{64}.
\]

All more distant inactive residuals equal their strictly negative forcing. Starting from the positive seed, safe M-matrix updates therefore prove by induction that every batch through stage L+1 is the next singleton, and every principal solution is positive. No unproved positivity premise was used in the endpoint calculation.

## The correction still changes the seed

At stage t >= 2, extend x^(t-1) by zero to S_t. It solves the old principal equations exactly, so its new residual vector has the form

\[
r^{\rm start}=r_{t-1}(x^{(t-1)})e_{t-1}.
\]

The exact correction is

\[
\Delta_t=Q_{S_tS_t}^{-1}r^{\rm start}.
\]

Using Q_t^{-1}=D_t^{1/2}H_t^{-1}D_t^{1/2},

\[
(\Delta_t)_0
=\frac{\sqrt2\,r_{t-1}(x^{(t-1)})}{c\cosh(t\eta)}
\ge\frac{2\sqrt2}{64\cosh3}\alpha
>\frac\alpha{256},\qquad 2\le t\le L.
\]

Yet the k-step Krylov correction belongs to

\[
\mathcal K_k(Q_t,e_{t-1})=
\operatorname{span}\{e_{t-1},Q_te_{t-1},...,Q_t^{k-1}e_{t-1}\}.
\]

Because Q_t is tridiagonal, these vectors vanish outside the last k coordinates. For k < t, the seed coordinate has not changed at all. Therefore the Euclidean error is greater than alpha/256, hence greater than delta. At least t CG iterations are required. This argument is exact arithmetic and uses no finite-precision phenomenon.

With conventional full matvecs, stage t costs Omega(t^2), and summing t from ceil(L/2) through L gives Omega(L^3). Exploiting only the expanding sparse support of each Krylov vector still entails Omega(t^2) explicit scalar-vector work over a solve; a compressed representation or direct response formula would constitute additional structural reuse.

## This accuracy can be required by a nontrivial polynomial objective tolerance

The certified lower-screen schedule from the fresh inexact batch proof is

\[
\delta^2=\epsilon\alpha\rho/8.
\]

The selected delta corresponds to

\[
\epsilon=\frac{\alpha^3}{131072\rho}
=\frac{100}{131072 L^5}.
\]

Thus log(1/epsilon), log(1/alpha), log(1/rho), and log n are all O(log L).

Moreover one cannot already stop at stage L-1 for this epsilon. The stage-L correction has

\[
\|\Delta_L\|_Q^2=r_{L-1}^2(Q_L^{-1})_{L-1,L-1}
\ge r_{L-1}^2\ge\alpha^2/4096,
\]

because Q_L <= I. Orthogonality of exact safe-pivot increments implies

\[
F_\rho(x^{(L-1)})-F_\rho(x^*)\ge\alpha^2/8192>\epsilon
\]

for L >= 8. Earlier principal iterates have at least the same gap.

The same increments satisfy the global Q-orthogonal energy budget (in particular their summed squared Q-norm is at most alpha). This example shows why that budget is insufficient: a polynomially small absolute error can force a fresh long-range correction even when the new energy is small.

## What a successful reuse argument would need

A saved tridiagonal factor reduces each stage to O(t), yielding O(L^2) total work. More generally, the missing lemma must use an efficiently applicable accumulated response operator or a structural decomposition. It cannot follow merely from the energy budget for independent restarted CG solves. This result makes no claim that arbitrary cyclic support graphs admit such an operator at the required cost.


## Primary-source MPRGP rate check

Dostál and Schöberl, *Minimizing Quadratic Functions Subject to Bound Constraints with the Rate of Convergence and Finite Termination* (2005), Theorem 5.1, proves

\[
f(x^{k+1})-f(x^*)\le\eta[f(x^k)-f(x^*)],\qquad
\eta=1-\frac{\bar\alpha\lambda_{\min}(A)}{2+2\widehat\Gamma^2},\quad
\widehat\Gamma=\max(\Gamma,\Gamma^{-1}).
\]

At the best displayed parameters Gamma=1 and stepsize 1/||A||, this is 1-1/(4kappa), giving a condition-number bound rather than a square-root-condition-number bound. The CG face steps can work better in practice, but that theorem does not supply the missing accelerated global guarantee. This is a statement about the proved bound, not an algorithmic lower bound.

Primary source: [author-uploaded original paper](https://www.researchgate.net/publication/226697431_Minimizing_Quadratic_Functions_Subject_to_Bound_Constraints_with_the_Rate_of_Convergence_and_Finite_Termination); [publisher DOI](https://doi.org/10.1007/s10589-005-4557-7). Theorem 5.1 and equations (5.1)-(5.3) were read directly.
