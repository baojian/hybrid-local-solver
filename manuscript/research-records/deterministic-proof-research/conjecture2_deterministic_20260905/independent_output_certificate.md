# An independent local certificate for a sparse nonnegative output

This certificate uses only strong convexity and the objective's explicit
subgradient. It does not use the accelerated recurrence, stage invariants,
selected-flow theorem, or the solver's reported gap. It is optional: the
bound can be conservative and need not certify every accurate output.

Let a sparse vector `x>=0` be supplied as degree densities `f_i=x_i/w_i`.
Write `r=Qx-b+alpha*rho*w` and choose

    v_i = r_i             if x_i>0,
    v_i = min(r_i,0)      if x_i=0.

On a zero coordinate, `Qx-b<=0` by the nonpositive off-diagonal signs and
`b>=0`. Thus the selected value belongs to the subgradient interval of the
weighted absolute-value term, and `v` is a valid subgradient of the original
unconstrained objective `F_rho`. Equivalently, it is the minimum-norm
orthant subgradient. Strong convexity gives

    F_rho(x)-F_rho(x*_rho) <= ||v||^2/(2*alpha).

Indeed minimize `F_rho(x)+v^T(y-x)+(alpha/2)||y-x||^2` over all `y`.

The vector `v` can be supported only on the output support, its immediate
neighbors, and the seed. Elsewhere `x_i=0` and `r_i=alpha*rho*w_i>0`, so
`v_i=0` exactly. Its computation scans each output adjacency list once;
adjacency lists of newly encountered zero-output neighbors are not scanned.
It costs `O((1+vol(supp x))*log(N+2))` word operations with deterministic
maps, in addition to scalar encoded arithmetic. The graph is assumed to be
the same simple undirected graph as in the problem definition.

## Common-denominator upper bound

For bounded arithmetic let the supplied densities share denominator `H`:
`f_i=B_i/H`. The solver's dyadic final output has this property with `H`
equal to its largest reduced denominator. Direct one-coordinate branches
also have a common denominator. Write `alpha=A/D`, `rho=P/R`,
`C=2*D*H*R`, and let `J_i` be the exact sum of neighboring output counts.
Then

    r_i/w_i = T_i/(C*d_i),
    T_i = (D+A)*R*d_i*B_i - (D-A)*R*J_i
          - 2*A*H*R*1(i=seed) + 2*A*H*P*d_i.

Use `V_i=T_i` on positive output coordinates and `V_i=min(T_i,0)` elsewhere.
The true squared norm is

    ||v||^2 = sum_i V_i^2/d_i / C^2.

Avoid a sum of coprime degree denominators by using the rigorous upper bound

    norm_upper = sum_i ceil(V_i^2/d_i) / C^2,
    gap_upper = norm_upper/(2*alpha).

All record accumulation uses integers. For `M` nonzero selected numerators,
the squared-norm excess is less than `M/C^2` when `M>0`, and is zero when
`M=0`. Therefore `gap_upper` is a fully independent, exact upper bound.
Comparing it with a requested tolerance returns either a certificate or an
inconclusive result; a larger bound does not disprove the solver's tighter
convergence certificate.

Status: independently audited without a defect. Root's exact tests cover
1,161 arbitrary small outputs; the independent audit adds 504 outputs,
including accurate-but-inconclusive cases and hash-forbidden labels.
The certificate independently verifies all eleven saved integer benchmark
outputs below their requested tolerances. Full records are in
`saved_benchmark_independent_certificates.json`; no solver was rerun to
obtain these certificates.
