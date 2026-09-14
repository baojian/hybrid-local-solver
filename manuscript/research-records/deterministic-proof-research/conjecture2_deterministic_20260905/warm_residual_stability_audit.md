# Warm-start squared-residual stability: a proved linear bound and the obstacle gap

Status: the commuting linear theorem below is proved. The corresponding
orthant/capped obstacle theorem is still open. Deterministic floating-point
checks are diagnostic only. No existing manuscript notes beyond the requested
problem definition were consulted.

Write `theta=sqrt(alpha)`, `a=1-theta`,
`beta=(1-theta)/(1+theta)`, and `L0=Q-alpha I`.
The proposed sufficient estimate is

    sum_k ||L0 (x_k-x*)||² <= O(alpha² rho / theta)

for acceleration restarted from the exact dyadic solution
`x_0=z_0=x*_(2rho)`. A polylogarithmic factor would still suffice for the
intended local-work reduction. It must hold for the actual initialized
trajectory, not an arbitrary feasible state with stored momentum.

## 1. Exact commuting linear theorem

For unconstrained Nesterov acceleration on a quadratic with
`alpha I <= Q <= I`, initialized at rest, write

    x_k-x* = p_k(Q)(x_0-x*).

The scalar residual polynomials satisfy

    p_0(t)=1, p_1(t)=1-t,
    p_(k+1)(t)=(1+beta)(1-t)p_k(t)-beta(1-t)p_(k-1)(t).

For every `t in [alpha,1]`,

    |p_k(t)| <= (1+k theta) (1-theta)^k.                 (1)

Proof: for `alpha<t<1`, put

    r=sqrt(beta*(1-t)),
    cos(phi)=sqrt((1-t)/(1-alpha)).

Then `r<=1-theta`, `0<phi<pi/2`, and the recurrence has the exact form

    p_k(t)=r^k [cos(k phi)
                    + theta*sqrt(1-t)/sqrt(t-alpha)*sin(k phi)].

The inequality `|sin(k phi)|<=k sin(phi)` bounds the second term by
`k theta sqrt((1-t)/(1-alpha))<=k theta`. The endpoints follow by
continuity, with `p_k(alpha)=(1+k theta)(1-theta)^k` and
`p_0(1)=1,p_k(1)=0` for positive k.

Since `(1+s)^2 exp(-2s)` decreases on the nonnegative half-line,

    sum_(k>=0) (1+k theta)^2 (1-theta)^(2k)
       <= 1 + integral_0^infinity (1+theta t)^2 exp(-2theta t) dt
       = 1+5/(4theta) <= 9/(4theta).                  (2)

For every symmetric operator B commuting with Q, spectral expansion gives

    sum_(k>=0) ||B(x_k-x*)||²
       <= 9/(4theta) ||B(x_0-x*)||².                 (3)

Also `||B(x_k-x*)||<=||B(x_0-x*)||` at every k. In particular B can be
Q or L0. The two-sequence lazy method reduces to this same recurrence
when neither its orthant nor cap projection changes the raw step.

The standard Nesterov recurrence used here is given in Shi, Du, Jordan,
and Su, *Understanding the acceleration phenomenon via high-resolution
differential equations*, Mathematical Programming (2022):
https://doi.org/10.1007/s10107-021-01681-8 . The bound (1)--(3) above is a
self-contained derivation, not a claim attributed to that source.

## 2. Why this does not establish the obstacle estimate

Orthant projection does not commute with Q. Even in a fixed proper face S,
principal evolution uses `Q_SS`, whereas the fully charged exterior
response involves `Q_(outside,S)`. Thus an estimate for
`Q_SS (x_S-x*_S)` is not automatically an estimate for global
`Q(x-x*)` or `L0(x-x*)`.

A weighted cap shift is proportional to w only on the coordinates retained
by the joint cap/orthant projection. Although `L0 w=0`, truncating w at an
active boundary can produce a nonzero L0 response. It is incorrect to
discard the cap correction merely by using `L0 w=0`.

Euclidean clipping can increase the Q norm. For example, let

    Q=[[1,-9/10],[-9/10,1]], x*=(1,0), v=(0,-1).

Then `v-x*=(-1,-1)` has squared Q norm `1/5`, whereas
`[v]_+-x*=(-1,0)` has squared Q norm `1`. Rescale Q by 1/2 if an
upper spectral bound 1 is desired. This only rejects a general metric
projection inequality; v is not claimed to be a reachable warm state.

For an exact dyadic warm pair, `e0=x*_rho-x*_(2rho)>=0`, and on the OLD
support `Qe0=alpha*rho*w`. Outside the new support `Qe0<=0`. Newly active
coordinates can have either sign in Qe0: they obey

    Qe0=alpha*rho*w-r_old,

where `r_old` is the old nonnegative obstacle slack. Therefore a proof
assuming `Qe0>=0` throughout the new support is invalid.

If both dyadic solutions have full support in a connected graph, then
`e0=rho*w` is a pure alpha eigenmode; this special case cannot exhibit
face conversion. The difficult regime is a growing partially active
support with possible inertial overshoots and subsequent clipping.

## 3. Bounded diagnostics

`warm_residual_probe.py` computes deterministic graph quotients and
principal obstacle solutions, restarts from the dyadic solution, and
measures all three sums: global Q error, global L0 error, and ordinary
unit-step gradient mapping. The actual graph, rather than its quotient,
defines weighted Euclidean norms. Quotients are used only to analyze a
specified symmetric graph; they are not supplied to a local algorithm.

The initial 108 long-double runs use paths, binary trees, and tree-clique
families; L=16,32,64; three regularization scales; and lazy, monotone,
cap-aligned, or ordinary projected Nesterov updates, each for 20L steps.

- Maximum `theta sum ||Q error||² / ||Q initial_error||²`: 0.97691.
- Maximum `theta sum ||L0 error||² / (alpha² rho)`: 0.33108.
- All global Q-error peaks were at the initial iterate.
- Some runs created coordinates outside the exact target support.

These finite, uncertified observations neither prove the estimate nor
exclude other deterministic graph families. They are recorded in
`warm_residual_probe_initial.jsonl`. No asymptotic conclusion follows.
