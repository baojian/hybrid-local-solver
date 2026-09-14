# Fixed degree pruning for the continuation proof

2026-09-05, independent refinement under audit.

The reported continuation proof permits permanently removing vertices with
original degree greater than `1/rho`, where rho is the **final** requested
regularizer. This threshold must stay fixed throughout continuation.
Changing it each stage would reopen vertices whose sources were not covered
by the preceding residual bound.

Let `A={i:d_i<=1/rho}`, `M=Q_AA`, and `w=w_A`. A is not globally enumerated.
A newly encountered vertex is classified after its ordinary degree reply.
Excluded vertices are never emitted and their adjacency lists are never
scanned. **All formulas retain original graph degrees**, including when
neighbors outside A are omitted from a matrix-vector update.

At every stage r>=rho, support volume gives `supp(x*_r) subset A`. Thus the
restricted obstacle optimum is the full optimum. The seed belongs to A in
the nonzero regime. Principal-matrix properties give

    alpha I <= M <= I,  M^{-1} >= 0,
    M w >= alpha w,     |M| w <= w.

The normalized adjacency on A is column-substochastic, with original
degrees. The selected-flow proof uses only nonnegativity and column sums
at most one, so it survives the restriction.

## The necessary change to the second energy

The identity `M w=alpha w` generally fails after deleting vertices. Replace
the second energy by

    A_M(xi) = ||M xi-s||^2/2 + lambda (M w)^T xi.

Its gradient in the M metric is `M xi-s+lambda w`, exactly the correction
gradient; its metric Hessian is M. The linear penalty is nonnegative.
For `t=M^{-1}s`, `A_M(t)=lambda w^T s=lambda m_s`. Diffuseness and inverse
positivity yield `t<=4r w`, because `M^{-1}w<=w/alpha`. Also
`m_s=w^T M t >= alpha w^T t`, so the source-mass cap contains t and the
correction optimum.

The special projection sector inequality remains valid. Lower faces have
`(M p-s)_i<=0`. At `p_i=4r w_i`, Stieltjes signs imply
`(M p)_i>=4r(M w)_i>=4 alpha r w_i>=s_i`. At an active mass cap C,

    w^T(M p-s) >= alpha C-m_s >= 0

for either C=1 or C=m_s/alpha. The same comparison lemma therefore gives
the second-energy recurrence. All residual bounds and the `148 K/r`
repeated-support bound follow unchanged. Their analytical comparison core
can be the restricted optimum at r/2, whose volume is at most 2/r; it
need not equal the unrestricted r/2 optimum when r/2<rho.

## Continuation, source, and terminal repair

Compute sources only on A: `s=b_A-M baseline`. Nonnegative baselines and
`M w>=alpha w` imply `m_s<=alpha`. The first source is the original point
source and its diffuse bound is unchanged.

Uniform terminal clipping improves the step that used
`Q(delta w)=alpha delta w`, since `M(delta w)>=alpha delta w`. The absolute
row sums in degree densities are at most one, which suffices for the
residual upper bound. A repaired baseline again supplies a source in
`[0,2 alpha r w]` **on the same fixed A**. No excluded vertex reopens.
All stage optima and final objective guarantees agree with the full graph.

For the bounded-arithmetic appendix, the changed linear penalty still
decreases under downward perturbations. The inequality
`w^T|M v|<=w^T|v|` supplies the same error bounds. Direct implementation
checks remain necessary, especially original degree denominators and the
terminal PG neighbor handling.

The private `pruned_rppr` package is a copied and attributed refinement of
the other task's packaged solver, with source files left unchanged. It
checks the restricted source-mass inequality, excludes high-degree keys,
still charges all original entries when scanning an allowed row, and
omits excluded coordinates from terminal PG output. The source-derived
uniform box `U=max(h,max_i(s_i/w_i)/alpha)` is optional: it contains the
analytical inverse response, satisfies `alpha U w>=s`, and lies between
the rounding grid h and the original bound 4r. Hence the same sector and
rounding proofs apply.

At 07:59 the full-objective independent audit passed 72 cases (17,652
iterations and 216 continuation stages), including all three configurations
of original settings, fixed pruning, and pruning with the tighter box.
Every final point lay below the exact full-graph optimum and met its
objective certificate. Every intermediate baseline was monotone and had
the required restricted source bounds. The audit is
`experiments/pruned_continuation_audit.py`; its exhaustive-face calculations
are external verification, not solver operations.

## Further safe refinement: a decreasing cutoff

At a stage boundary, the known full mass deficit
`eta_bar=1-w^T baseline` satisfies `eta_bar>=eta_*(rho)`. Thus vertices with
`d_i>eta_bar/rho` also cannot belong to the final optimum or any earlier
continuation optimum. Monotone baselines make this cutoff nonincreasing.
No removed vertex reopens, and the baseline itself has no positive removed
coordinate because `vol(supp baseline)<=eta_bar/r_stage<=eta_bar/rho`.
The previous source bound remains valid on the smaller set. This extension
is not implemented yet. **Do not substitute `m_s/alpha` for eta_bar** on a
restricted graph: killed boundary flux makes that quantity smaller, so it
need not upper-bound the full optimum's mass deficit.
