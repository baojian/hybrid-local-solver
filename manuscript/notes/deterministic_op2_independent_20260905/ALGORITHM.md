# Algorithm and accelerated rate

At stage regularization `r`, maintain a safe baseline `bar_x` and a nonnegative
diffuse source `h = b - Q bar_x <= 4 alpha r w`, where `w_i = sqrt(d_i)`.
The unknown correction belongs to `K = {0 <= z <= 4 r w, w^T z <= 1}`.

```text
r0 = 1 / degree(seed)
bar_x = 0
for r in the halving schedule from r0 down to rho:
    h = b - Q bar_x
    theta = dyadic parameter comparable to sqrt(alpha)
    xi = z = 0
    choose certified stage gap tau from the required repair accuracy
    repeat until the proved energy bound is at most tau:
        y = (xi + theta*z) / (1 + theta)
        raw = (1-theta)*z + theta*y - (Q*y - h + alpha*r*w)/theta
        z = project raw onto the box and mass cap
        xi = (1-theta)*xi + theta*z
    bar_x = certified downward repair of bar_x + xi
return bar_x
```

Zero is exact when `rho*degree(seed) >= 1`; `alpha=1` has a direct seed formula.
The exact-real repair is `[candidate - delta*w]_+`, with stage gap
`tau = alpha^3 delta^2/2`. At the final stage choose
`delta <= alpha*r/2` and `delta^2 <= eps_obj*r/2`.

The ordinary energy contracts by `1-theta`, yielding
`K = O(alpha^(-1/2) log(1/tau))` iterations. A second energy bounds the residual
response of the actual constrained trajectory. Selected signed flow then proves
`sum_k vol(supp(z_k)) <= 148 K/r`, including repeated scans.

The vector operations above are implicit: shared scales update old entries,
cached responses change through active rows, and balanced trees perform exact
threshold searches and enumerate positive outputs. A dense implementation of
the pseudocode would not give the local bound. The geometric sum of `1/r`
completes the fully charged accelerated complexity.

The implemented bounded-integer refinement has directed rounding, a stronger
terminal projected-gradient repair, source-dependent stopping bounds, and
deterministic certified early checks. Intermediate accelerated states may
overshoot the optimum; the final repaired output is safe.
