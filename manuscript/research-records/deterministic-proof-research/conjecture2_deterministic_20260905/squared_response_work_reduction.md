# A squared-response criterion for fully charged accelerated locality

This is a deterministic sufficient-condition theorem, not a proof of general
Conjecture 2. Unlike the earlier total unselected L1-flux proposal, it follows
from the selected signed-flow identity and needs a squared response bound.
It applies to the actual one-projection capped recurrence, including an
optional correction box and primal descent cleanup. The missing analytic
condition is stated explicitly below.

## 1. Correction variables and comparison region

Let theta=sqrt(alpha), a=1-theta, c=(1-alpha)/2, lambda=alpha*rho,
w=sqrt(d), P=A D^(-1), K0=(I+P)/2, and L0=Q-alpha*I.
The case alpha=1 is diagonal and should be handled directly.

A fixed nonnegative baseline xbar gives the correction objective

    J(xi)=xi^T Q xi/2-h^T xi,
    h=b-lambda*w-Q*xbar.

Assume the true correction xi*=x*_rho-xbar is nonnegative and belongs to
the chosen convex mass cap, and to any additionally imposed coordinate box.
For exact dyadic continuation, xbar=x*_(2rho), 0<=xi*<=rho*w and
w^T xi*<=1. The baseline is not free algorithmic input: every continuation
stage must compute and pay for it.

The correction KKT slack is exactly the original slack,

    r*=Q*xi*-h=Q*x*_rho-b+lambda*w >=0.

Let C=supp(x*_(rho/2)). Then vol(C)<=2/rho, and outside C,
xi*=0 and r*_i>=lambda*w_i/2. This comparison region is analytical and
is never supplied to the algorithm.

At every mirror update use

    y=(xi+theta*z)/(1+theta),
    zraw=a*z+theta*y-grad J(y)/theta,
    znew=projection of zraw onto the nonnegative capped set.

The optional box is 0<=z_i<=rho*w_i in the dyadic case. The raw-step
identity below does not depend on how the next primal xi is chosen. Thus
ordinary accelerated averaging, the already-audited monotone segment
search, or an additional primal descent cleanup all share this criterion.
Their separate convergence proofs still have to apply.

## 2. Exact selected-flow identity

Use mass coordinates

    u=D^(1/2)*xi, V=theta*D^(1/2)*z,
    u*=D^(1/2)*xi*, V*=theta*u*.

Let e=(V-V*)_+ and n=(V*-V)_+, so V-V*=e-n. Direct substitution gives

    Vraw-V* = a*K0*(V-V*)+H-R*,
    H=(a/2)*(P-I)*(u-u*), R*=D^(1/2)*r*.

Here K0 is nonnegative and column stochastic. The mass-cap multiplier
subtracts eta*d, eta>=0, from Vraw before taking its positive part.
An upper-box multiplier, if present, subtracts a further nonnegative vector.
On E={i:Vnew_i>V*_i}, the lower nonnegativity constraint is inactive, so

    e_new_i = a*(K0 e)_i-a*(K0 n)_i+H_i-R*_i
                -eta*d_i-upper_i.

Summing on E and discarding only nonnegative losses gives

    ||e_new||_1 + sum_(i in E) R*_i
       <= a*||e||_1 + sum_(i in E) H_i.               (1)

The selected H term remains signed. In particular, this argument does not
replace it by an all-vertex positive flux and does not invoke the false
uniform L1-flux bound.

Start the correction from xi_0=z_0=0. Then e_0=0. Outside C, V*=0, so
E outside C is exactly the newly emitted kinetic support outside C.
Summing (1) over k=0,...,T-1 yields

    (lambda/2)*Dout <= sum_k sum_(i in E_k) H_(k,i),  (2)
    Dout=sum_k vol(supp(z_(k+1)) outside C).

The discarded terminal error mass and the theta-weighted previous error
masses are nonnegative. The same is true for cap and upper-box losses.

## 3. Cauchy inequality converts squared response into paid support

Define

    B=T*vol(C) <= 2*T/rho,
    H2=sum_k sum_i H_(k,i)^2/d_i.

The selected degree-volume over all k is at most Dout+B. Cauchy's inequality
applied directly to the signed sum on the right of (2) gives

    (lambda^2/4)*Dout^2 <= (Dout+B)*H2.              (3)

Writing A0=4*H2/lambda^2, the nonnegative solution of (3) obeys

    Dout <= A0+sqrt(A0*B) <= 2*A0+B.

Moreover a/(2c)=1/(1+theta), so

    D^(-1/2)*H = -L0*(xi-xi*)/(1+theta),
    H2 <= sum_k ||L0*(xi_k-xi*)||_2^2.

Adding the kinetic volume inside C proves the explicit bound

    sum_k vol(supp z_(k+1))
       <= 8/lambda^2 * sum_k ||L0*(xi_k-xi*)||_2^2
            +4*T/rho.                              (4)

This is a proved trajectory inequality, without an assumed support oracle.
The lazy reporter implementation charges all adjacency, arithmetic, boundary,
state, and output work to this cumulative kinetic volume and T, up to its
already-audited deterministic balanced-tree logarithms. Optional primal
cleanup has its separately proved multiplicative cost.

## 4. The precise missing stability theorem

The desired numerical condition at a dyadic warm stage is

    sum_k ||L0*(xi_k-xi*)||_2^2
       <= C*lambda^2/(rho*sqrt(alpha))*polylog.       (5)

Since T=O(alpha^(-1/2)*log accuracy), (4) and (5) would give the requested
local work per stage. A geometric rho schedule would add only logarithmic
factors, provided approximate warm starts were also safely and economically
handled. Neither the projected stability statement (5) nor that approximate
continuation interface has been proved here.

There is real evidence for examining (5): an exact dyadic correction has
||Q*xi*||_2^2<=2*lambda^2/rho. On its true support Q*xi*=h and |h_i|<=lambda*w_i.
Outside, Q*xi*<=0, its density is at most lambda in magnitude, and its
weighted absolute mass is at most lambda*vol(supp xi*). The resulting
squared-norm bound is global, despite an arbitrarily large inactive boundary.

For unrestricted linear Nesterov from rest, the exact residual polynomial
obeys |p_k(t)|<=(1+k*theta)*(1-theta)^k for every eigenvalue t in [alpha,1].
Consequently its squared sum is O(1/theta). Because L0 and Q commute and
0<=L0<=Q, this gives (5) for that linear trajectory. A projection or changing
obstacle face need not preserve this spectral argument: Q times a coordinate
projection does not commute with Q, and Q^2 is generally not Stieltjes.

The linear calculation is not a proof for the actual constrained algorithm.
It identifies the remaining nonlinear stability claim rather than concealing
it in an invocation of accelerated convergence.
