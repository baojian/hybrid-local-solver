# A bounded component prepass for practical local solving

2026-09-05. Implemented privately in `pruned_rppr/component.py` as solve_fast.
The exact full-objective audit passed 54 cases and 5,184 independent
projection comparisons. Separate cases also checked zero-regime, alpha=1,
global and component zero-output certificates, and the fixed horizon with
early stopping disabled. All safe-output and objective certificates passed.
Finite audits supplement the derivation below; they are not its proof.

Use the fixed allowed set `A={i:d_i<=1/rho}` from `fixed-degree-pruning.md`.
Explore its seed component, with original-degree scan budget `B=1/rho`.
Query a queued vertex's degree before scanning its row; stop and fall back
to continuation if its full degree would exceed the remaining budget.
Scan original neighbor entries, querying and caching their original degrees.
Never queue a vertex outside A. Deterministic queues and comparison maps
cost `O_tilde(B)` for this entire preliminary search.

If the search empties its queue, its component C is fully known and
`vol(C)<=B`. The full optimum is supported in C: it lies in A, and every
other A-component has zero source and hence zero optimum. The restricted
objective on C therefore has exactly the original objective gap. If the
component is a singleton, return the exact density
`alpha*(1/d_seed-rho)/((1+alpha)/2)` immediately.

For a larger completed component put `M=Q_CC`, retain original degrees,
and compute

    beta = alpha + (1-alpha)/2 * min_i((d_i-deg_C(i))/d_i).

The Dirichlet graph quadratic form gives `beta I<=M<=I`. Choose dyadic
theta with `beta/4<theta^2<=beta`, theta<=1/2, and use the ordinary averaged
coupling recurrence with this theta. Project onto the known component's
density box `0<=f_i<=U=1/d_seed` and mass cap `sum d_i f_i<=1`. The optimum
is feasible: inverse positivity and `M w>=alpha w` give
`M^{-1}b<=w/d_seed`; weighted mass is at most one.

No diffuse-source or second-energy argument is needed once the whole
component has been charged. Full products and deterministic sorted-event
waterfilling cost `O_tilde(vol(C))` per iteration.

## Bounded arithmetic and safe output

Use exact rational raw products and projection, then round both auxiliary
and averaged primal degree densities downward to a fixed dyadic grid h.
The ordinary perturbation argument from the reviewed appendix gives

    E_next <= (1-theta) E + 5 h.

Indeed the auxiliary and primal rounding errors have density bounds h;
the general debit is at most `2.5 h+2.5(theta+theta^2)h<5h`, since
theta<=1/2. All states remain in the box and mass cap. The initial energy
is at most one. With `h<=theta tau/16`, the limiting energy debit is at
most `5 tau/16`. A block schedule with `a^K<=tau/2` yields gap below tau.
Immediate dyadic rounding prevents an iteration-dependent denominator.
Weighted waterfill sums cancel degree denominators, as in the main proof.

To retain the strong safe-output property, choose
`delta<=alpha rho/2`, `2 delta^2/rho<=epsilon`, and
`tau=alpha delta^2/8`. Also require `h<=min(delta/2,alpha rho/4,U)`.
After the accelerated run, compute one exact ordinary PG step p from the
stored state, then return `floor_h([p_density-delta]_+)`. The reviewed
terminal-repair proof applies to the principal matrix M and gives
`0<=output<=x*_rho` and gap at most epsilon. No newly positive outside
component row can exist in the restricted calculation.

Total work is
`O_tilde(B + vol(C)/sqrt(beta)) <= O_tilde(1/(rho sqrt(alpha)))`.
If the component search fails, the prepass costs only O_tilde(B), and the
already proved continuation theorem covers the fallback.

## Optional exact early certificate

At geometrically spaced iteration counts, one exact PG step p and
`G=x-p` give a subgradient at p of norm at most `(1-beta)||G||`.
If its squared bound is at most `beta^2 delta^2/4`, then
`||p-x*||<=delta/2` and its subgradient norm is at most delta/2. The same
clipping/rounding repair is already valid, so the solver can stop early.
Otherwise it continues to the certified fixed horizon; the extra full
component passes contribute only an allowed logarithmic factor. This
certificate is optional and must be checked for the actual stored point.

Implementation requirements: exact sorted breakpoint sweep must be
O(n log n), not a quadratic scan of all coordinates for every interval;
retain original degrees; count initial degree replies and excluded neighbor
entries; avoid global graph queries and expected hashing. A simple cached
oracle may reuse the prepass data during fallback, but cached traversals
and balanced-map lookups still count as work.

## Stronger deterministic forest certificate

The implementation now improves beta when only some component vertices have
excluded neighbors. Let `b_i=d_i-deg_C(i)`. Every vertex with b_i>0 is a root
with initial distance 1/b_i. Run a deterministic shortest-path search on
internal unit-length edges. Its parent forest assigns i a root r(i) and
distance `ell_i=depth_i+1/b_(r(i))`. Put

    L_r = sum_(i assigned to r) d_i ell_i,    L=max_r L_r.

For every density vector f supported in C, weighted Cauchy-Schwarz on its
parent path gives

    f_i^2 <= ell_i [sum_(internal path edges) (f_u-f_v)^2
                    + b_(r(i)) f_(r(i))^2].

After multiplying by d_i and summing, an internal edge's coefficient is
at most its root load L_r, and the root boundary-energy coefficient is
exactly L_r. Thus

    sum_i d_i f_i^2 <= L [sum_(internal edges) (f_u-f_v)^2
                          + sum_i b_i f_i^2].

Therefore `beta=alpha+(1-alpha)/(2L)` is a certified lower eigenvalue bound.
With no boundary roots, use beta=alpha. When every vertex is a root, this
reproduces the minimum killing-ratio bound; otherwise it improves on that
bound alpha. The shortest-path search and load sums cost O_tilde(vol(C))
on already exposed data. No randomized construction or linear solve occurs.

The fallback now uses the independently trajectory-checked integer solver
with a source-dependent initial-energy bound. Twelve exact stage comparisons
matched 768 rational-reference steps, and 32 full wrapper cases passed exact
full-graph objective checks. This changes scalar implementation and stage
lengths without requiring a new convergence hypothesis.
