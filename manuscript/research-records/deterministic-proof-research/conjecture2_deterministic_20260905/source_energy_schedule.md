# A computable initial-energy bound for shorter certified stages

This refinement changes only the prescribed number of accelerated steps.
It uses the same safe baseline, boxed mass projection, dyadic rounding, and
terminal repair as the completed deterministic proof. No new graph access,
support information, randomization, or numerical convergence test is needed.

## Bound from the already assembled source

At a stage let `lambda=alpha*r`, `mu=theta^2<=alpha`,
`s=b-Q*bar`, `eta=(w^T s)/alpha`, and `e=x*_r-bar`. The stage assumptions
give `0<=bar<=x*_r`, `0<=s<=4*lambda*w`, `0<=e<=4*r*w`, and `w^T e<=eta`.
Write `h=s-lambda*w`. At the correction optimum,

    Qe-h = r* >= 0,       (r*)^T e = 0.

The latter follows from the original complementarity and `bar<=x*_r`:
where the original optimum is zero, both `bar` and `e` are zero. Hence

    J(0)-J(e) = (1/2) e^T Qe,
    E0 = (1/2)e^T Qe + (mu/2)||e||^2
       <= ((1+mu/alpha)/2) e^T Qe.

For each stored source coordinate put

    g_i = max(s_i/w_i-lambda, 0).

Unstored source coordinates have `g_i=0`. Define the finite, explicitly
computable source statistics

    H1 = sum_i d_i*g_i,
    H2 = sum_i d_i*g_i^2,
    Hinf = max_i g_i, with max(empty)=0.

Complementarity and nonnegativity imply all three bounds

    e^T Qe = e^T h <= 4*r*H1,
    e^T Qe <= eta*Hinf,
    e^T Qe <= H2/alpha.

For the last, use `e^T Qe <= ||e||*sqrt(H2)` and
`alpha*||e||^2<=e^T Qe`; the zero-energy case is immediate.
Consequently the following quantity is a valid initial-energy bound:

    Ebar = min(1, ((1+mu/alpha)/2)
                      * min(4*r*H1, eta*Hinf, H2/alpha)).

It is also bounded by `3*alpha*r*eta`, since `Hinf<=3*alpha*r` and
`(1+mu/alpha)/2<=1`. Computing it visits each source record once. This cost
is already covered by source initialization. Exact `H2` is useful in the
word model, but its degree denominators can accumulate over many coprime
degrees. The bounded-arithmetic implementation uses the upper bound below.

## Bounded-denominator squared statistic

Write `alpha=A/D`, `rho=P/R`, and `h=1/H`. The integer-state solver stores
source density as `N_i/(2*D*H*d_i)`. Put

    C = 2*D*H*R,
    G_i = max(R*N_i - 2*A*H*P*d_i, 0).

Then `g_i=G_i/(C*d_i)` and

    H1 = sum_i G_i / C,
    Hinf = max_i(G_i/d_i) / C,
    H2_upper = sum_i ceil(G_i^2/d_i) / C^2 >= H2.

Every per-record accumulation uses integers. The squared-statistic excess
is less than `n_positive/C^2` when there is at least one positive source
statistic, and is zero otherwise. The maximum stores only one selected
degree denominator. Thus neither scalar sum accumulates coprime degree
denominators. Replace `H2` by `H2_upper` in `Ebar`. This remains an upper
bound, and the other two terms still imply `Ebar<=3*alpha*r*eta`.
Bit sizes grow only logarithmically with the number and degrees of exposed
records, in addition to the encoded parameters and grid. Integer division
cost is included in the usual bounded-arithmetic extension.

## Certified shorter schedule

The audited rounded trajectory satisfies

    E_k <= a^k*E0 + Gamma,      Gamma < tau/8,

with the existing grid and `a=1-theta`. Let `m=1/theta`, and choose the
smallest nonnegative integer `q` such that

    Ebar / 2^q <= tau/2.

Run `K=m*q` steps. Because `a^m<1/2`, the final gap is below `tau`.
For every completed block, a valid reported bound is

    Ebar / 2^(completed blocks) + Gamma.

When no step has been taken, `Ebar` itself is valid and avoids adding a
rounding error that has not occurred. In particular `Ebar=0` certifies that
the baseline is already the exact optimum at this stage. A zero-step stage
may still use the unchanged terminal repair and safe maximum; it cannot
damage the baseline certificate.

The schedule is never longer than the original `E0<=1` schedule. The
selected-flow theorem applies to every prefix, including the shorter
prefix; its auxiliary-energy proof is unchanged. Grid selection still
uses the target tolerance `tau`, not `Ebar`. Source initialization and
stage-final work must remain charged even when `K=0`.

## Verification obligations

An implementation should record `Ebar`, the three source statistics, and
the paid source-record count. Tests should independently compare `Ebar`
with the exact initial energy on small obstacle problems, check
zero-step and zero-energy cases, then verify the full repaired output
against exact KKT solutions. Changing the iteration count changes the
trajectory endpoint; equality with the longer reference output is neither
required nor expected. The objective and locality guarantees are the
properties to test.

Status: independently checked by the acceleration subagent, including the
bounded-denominator variant. Implementation and end-to-end tests are in
progress in separate files; the stable fixed-schedule solver is unchanged.
