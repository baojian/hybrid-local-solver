# Deterministic localization and mass-ledger investigation

Status: proved elementary lemmas and exact finite experiments. This document
does **not** prove OP2, and its hypercube evidence is not an asymptotic lower
bound for all deterministic algorithms.

Scope: the only existing project note read was the requested
`manuscript/notes/problem_definitions/main.tex`. No other manuscript note,
previous direction, or other agent's old work was read. The algorithms and
experiments here use no randomness.

## 1. A coarse underregularized solve suffices for support discovery

Write `w = D^(1/2) 1`, `q = (1+alpha)/2`,
`x = x_rho^*`, and `u = x_(rho/2)^*`. Monotonicity of the orthant obstacle
problem gives `0 <= x <= u`. On `S = supp(x)`, their equations imply

    Q_SS (u_S-x_S) >= (alpha*rho/2) w_S.

For completeness, monotonicity follows directly from inverse positivity.
If `T={i:x_i>u_i}` were nonempty, x is active on T, while the lower-
regularization optimality inequalities give
`[Q(x-u)]_T <= -(alpha*rho/2)w_T`. On the complement of T, `x-u<=0`,
so nonpositive off-diagonal entries imply
`Q_TT(x-u)_T <= -(alpha*rho/2)w_T`. Multiplication by the nonnegative
inverse contradicts positivity of `(x-u)_T`.

The extra term from `u_(V\S)` is nonnegative because the off-diagonal
entries of Q are nonpositive. Inverse positivity and the nonnegative
Neumann expansion of `Q_SS^(-1)` give

    u_i-x_i >= (alpha*rho/2) (Q_SS^(-1)w_S)_i
              >= alpha*rho/(1+alpha) * w_i,       i in S.

Set `eta = alpha*rho/[2(1+alpha)]`. If any approximation z satisfies

    ||D^(-1/2)(z-u)||_infinity <= eta,

then the explicitly thresholded set

    T = {i : z_i > eta*w_i}

satisfies `supp(x_rho^*) subset T subset supp(x_(rho/2)^*)`, and therefore
`vol(T) <= 2/rho`. The first inclusion is strict enough because `x_i>0`
on S. The second holds because `u_i=0` outside its support. Thus z itself
need not be a safe lower approximation.

It suffices that

    F_(rho/2)(z)-F_(rho/2)(u)
       <= alpha^3*rho^2 / [8(1+alpha)^2],

by strong convexity and `d_i>=1`. Once T has actually been discovered and
its adjacency lists paid for, ordinary deterministic accelerated projected
gradient on T solves the requested rho objective with work
`O(vol(T)/sqrt(alpha) * log(1/epsilon))`, up to explicit parameter logs.
The unresolved step is obtaining the coarse z in the requested local work.
The lemma does not grant that solve or its support for free.

### A less demanding certificate: approximate complementarity

There is a separate reduction that needs only a degree-scaled gradient
certificate, not the preceding small objective gap. Suppose y>=0 and set

    h=Qy-b+(alpha*rho/2)w.

Assume `|h_i|<=alpha*rho*w_i/4` on the positive support of y and
`h_i>=-alpha*rho*w_i/4` on its zero coordinates. Then y solves exactly a
nonuniformly regularized problem with coordinate parameters
`rho_i in [rho/4,3*rho/4]`. On a positive coordinate choose
`rho_i=rho/2-h_i/(alpha*w_i)`. On a zero coordinate choose
`rho_i=max(rho/4,rho/2-h_i/(alpha*w_i))`; the stated inequality places
this number at most 3*rho/4. These choices give the exact orthant KKT
conditions.

The same M-matrix comparison proof applies to coordinatewise ordered
regularization vectors. Therefore

    x*_(3rho/4) <= y <= x*_(rho/4),
    S_rho subset supp(y) subset S_(rho/4),
    vol(supp(y)) <= 4/rho.

This certificate allows degree-gradient errors of order alpha*rho in a
coarse support-discovery solver. Obtaining and checking it locally must
still be paid for; the reduction does not provide an accelerated solver.

## 2. Classical extrapolation: the negative-momentum charge

Let `A=I-Q>=0`, `lambda=alpha*rho`, and `beta in [0,1)`. For

    y_k = x_k + beta*(x_k-x_(k-1)),
    x_(k+1) = [A y_k + b - lambda*w]_+,

define `m_k=w^T x_k`, `x_(-1)=x_0=0`, and
`N_k=w^T[-y_k]_+`. Positivity of A and `w^T A=(1-alpha)w^T`
give

    lambda vol(supp(x_(k+1)))
      <= alpha(1-m_k)
         +(1-alpha)beta(m_k-m_(k-1))
         -(m_(k+1)-m_k) +(1-alpha)N_k.

The inactive coordinates' nonnegative incoming mass is simply discarded
to obtain this inequality. Summing it telescopes. If extrapolation were
nonnegative and the final mass obeyed
`m_K >= (1-alpha)beta*m_(K-1)`, the cumulative volume would be at most
`K/rho`. Without those properties, weighted negative momentum and the
endpoint term must be charged. An l2 convergence bound alone does not
provide the desired weighted l1 charge.

## 3. Feasible two-projection acceleration

Work with the smooth orthant objective

    H(x)=0.5*x^T Qx - b^T x + alpha*rho*w^T x,    x>=0.

Put `theta=sqrt(alpha)`, `a=1-theta`, and start `x_0=z_0=0`. Consider

    y_k = (x_k+theta*z_k)/(1+theta),
    p_raw = y_k - grad H(y_k),
    x_(k+1) = [p_raw]_+,
    z_(k+1) = [(1-theta)z_k+theta*y_k-grad H(y_k)/theta]_+.

The exact orthant identity is

    theta*z_(k+1) = [x_(k+1)-a*x_k]_+.

Consequently `supp(z_k) subset supp(x_k)` and y_k is nonnegative with
the same support as x_k. A local implementation needs only that one
current support's gradient scan; z does not introduce a separate support.

### Convergence and squared projection dissipation

The scheme has accelerated energy contraction. Let

    E_k = H(x_k)-H(x*) + alpha/2 * ||z_k-x*||_2^2.

The usual smooth-descent and strong-convexity calculation, retaining the
orthant projection terms, yields

    E_(k+1) <= a E_k
       - alpha*theta*(1-alpha)/2 * ||z_k-y_k||_2^2
       - 1/2 * (||[a*x_k-p_raw]_+||_2^2
                    - ||[-p_raw]_+||_2^2).

For clarity, the projection terms arise because
`theta*z_raw=p_raw-a*x_k`; projection of z removes at least the positive
loss from projecting the gradient step. Since `x_k>=0`, the final
difference of squares is nonnegative and is at least

    ||[a*x_k-x_(k+1)]_+||_2^2.

Thus this variant has both accelerated convergence and a precise extra
squared dissipation. This does not imply local work acceleration.

### Fully explicit volume ledger

Let

    delta_k = w^T[a*x_k-x_(k+1)]_+,
    W_K = sum_(k=0)^(K-1) vol(supp(x_(k+1))).

Feasible y gives the one-step mass inequality

    alpha*rho*vol(supp(x_(k+1)))
       <= alpha + a*m_k + a*theta*w^T z_k - m_(k+1).

The orthant identity gives

    theta*w^T z_k = m_k-a*m_(k-1)+delta_(k-1).

Summation, with zero initial states, gives

    alpha*rho*W_K
       <= alpha*K - alpha*sum_(k=0)^(K-1)m_k
          + a^2*m_(K-1)-m_K
          + a*sum_(k=0)^(K-2)delta_k.

The endpoint term is at most `a*delta_(K-1)`, coordinatewise before
summing. Therefore the clean certificate is

    alpha*rho*W_K <= alpha*K + a*sum_(k=0)^(K-1)delta_k.

An `O(alpha*K)` total weighted deficit would establish the desired
amortized work. The l2 dissipation controls only the squares of the
coordinate deficits. Cauchy-Schwarz introduces the cumulative exposed
volume, and does not close the desired bound. The following exact examples
show that the missing weighted-l1 assertion cannot be assumed.

## 4. Exact hypercube experiment

For the d-dimensional hypercube, all degrees equal d. A single seed makes
the iterates constant on Hamming-distance layers `j=0,...,d`. A layer has
`binom(d,j)` vertices. This symmetry is used only to analyze the candidate
algorithm; the canonical input model does not supply this graph-wide
quotient to a local solver.

Let U_j and V_j denote the per-vertex mass variables
`D^(1/2)x` and `theta*D^(1/2)z`, divided by `alpha*rho*d`.
Let `C=1/(rho*d)`. The exact recurrence is

    T_j = U_j+V_j,
    P(T)_j = [j*T_(j-1)+(d-j)*T_(j+1)]/d,
    U'_j = [a/2*(T_j+P(T)_j) + C*1_(j=0)-1]_+,
    V'_j = [U'_j-a*U_j]_+.

Missing end layers contribute zero. The support volume at that iteration
is exactly `d*sum_{j:U'_j>0}binom(d,j)`.

`hypercube_mass_probe.py` evaluates this recurrence with integer
numerators over a common denominator. Thus support signs and the integer
work counts are exact; the displayed decimal ratios are only presentation.

For the prospective asymptotic family

    alpha=1/d^2,  rho=2^(-7d/8)/d,  K=3d,

the following **finite exact observations** were obtained:

| d | Peak iteration | Active layers at peak | Peak rho*volume | Mean rho*volume over K steps |
|---|---:|---|---:|---:|
| 128 | 108 | 0 through 70 | 57,329.586 | 13,039.789 |
| 256 | 219 | 0 through 143 | 4.18228524e9 | 9.88084776e8 |
| 512 | 378 | 0 through 261 | 1.26644848e19 | 1.77235871e18 |

Exact integer counts and every active layer are in
`hypercube_d128_scaled_exact.json`, `hypercube_d256_scaled_exact.json`, and
`hypercube_d512_scaled_exact.json`.

All three peak supports include more than half of the hypercube. Because
the whole-graph value `rho*vol(V)=2^(d/8)`, an extension of that fact to all
sufficiently large d would prove an exponential locality overhead for this
candidate while inverse-parameter and exposed-word logarithms grow only
polynomially in d. **That extension has not been proved.** These records
are exact finite evidence against an assumed constant mass/deficit bound,
not a graph-uniform impossibility result and not a disproof of OP2.

The degrees d are tiny compared with `1/rho`; excluding vertices with
degree larger than `2/rho` does not address these examples.

## 5. Current missing statements

1. Coarse underregularized support discovery needs its own accelerated,
   fully charged deterministic algorithm. The threshold margin in section
   1 alone is not such an algorithm.
2. For feasible two-projection acceleration, one would need a new control
   on weighted projection deficits or a different local implementation.
   A constant total-mass argument is contradicted by the exact probes.
3. An asymptotic hypercube lower bound for this candidate would require a
   uniform analytic lower bound on its radial support propagation. The
   finite exact computations do not replace that proof.
