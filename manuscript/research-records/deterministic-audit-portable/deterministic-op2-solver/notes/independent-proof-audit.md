# Independent audit of the reported deterministic OP2 proof

Audit started 2026-09-05 07:35 UTC; first full mathematical pass completed
07:41 UTC. The requested ten-hour research window is still in progress.

## Provenance and current conclusion

The task **Prove conjecture 2 deterministically** developed the proof in
`research/conjecture2_deterministic_20260905/deterministic_conjecture2.tex`.
The separate task **Explore deterministic Conjecture 2** reported its claim
and prior review at about 07:35. This session then read and independently
checked the full 450-line main TeX and its bounded-arithmetic appendix.
No private work from this session was sent to either task.

**First-pass conclusion: no gap found in the canonical exact-real OP2
theorem.** The argument appears to prove the requested fully charged
deterministic `O_tilde(1/(rho sqrt(alpha)))` bound. This is an independent
mathematical review, not a machine-checked formal proof. Independent exact
algebra/trajectory checks and implementation review continue.

At 07:51, independent exact checks completed successfully:
`independent_continuation_audit.py` checked 576 stage cases and 18,432
exact rational iterations on all connected graphs through four vertices,
all seeds, three alpha values, three regularizer ratios, and both mass
caps. It checked both energies, selected flow, the residual bound, and
every prefix's cumulative volume. A separate projection test checked
16,100 arbitrary raw inputs, including 6,486 upper-normal cases, 9,458
active mass caps, and 3,776 simultaneous upper/mass cases. Every ordinary
and special metric sector inequality held exactly. These finite audits
supplement the algebraic proof; dense optimum calculations are external
verification machinery and are not part of the local solver.

Reviewed main-file SHA256:
`514500298435b9bd9a8cda57d7e269405bc524024aad0cdc983b4208c111457d`.
Reviewed appendix SHA256:
`d65c3529f8df1a0ec94e21d1a9fcce86d9cea70ed8bcd455f538ef3a66c41a57`.

This session's earlier mass-repair candidate remains an unproved separate
algorithm. The new conclusion relies on the other task's continuation,
box-constrained coupling, and second-energy proof, not on a conjectured
rate for that candidate. Its finite searches must not be relabeled as
validation of the new algorithm.

## Main proof checks

1. **Stage feasibility.** A baseline below the optimum and residual source
   `0<=s<=4 alpha r w` imply `t=Q^{-1}s<=4r w`, by inverse positivity and
   `Q^{-1}w=w/alpha`. Both the correction optimum and t lie in the stated
   box and unit mass cap. These vectors are used only in analysis.

2. **Ordinary accelerated energy.** The comparison lemma is valid for a
   comparator satisfying its one projection inequality; optimality of the
   comparator is not required by its proof. The dyadic theta obeys
   `alpha/4<theta^2<=alpha`, so the smoothness and strong-convexity
   hypotheses hold. The initial correction energy is at most one because
   its weighted mass is at most one, all degrees are at least one, and
   `Q<=I`. Translation by the baseline preserves the objective gap.

3. **Second metric sector.** For any box/cap projection normal n,
   `(Qp-s)^T n>=0`: lower normals pair with nonpositive entries, upper
   normals pair with entries at least `4 alpha r w-s`, and the mass normal
   pairs with `alpha-m_s>=0`. This is a special comparator inequality,
   not a false general claim of Q-nonexpansiveness of Euclidean projection.

4. **Residual energy.** The Q-metric gradient of
   `A(xi)=||Q xi-s||^2/2+alpha lambda w^T xi` is exactly
   `Q xi-s+lambda w`. Its metric Hessian is Q. The comparison energy may
   be negative, which does not invalidate its contraction inequality.
   `B_0<=3 lambda m_s`, `A(t)=lambda m_s`, and nonnegative mass give
   `||Q xi-s||^2<=8 lambda m_s`. The optimum residual has squared norm
   at most `lambda m_s`; hence the claimed `18 lambda m_s` response bound.

5. **Selected flow and full volume.** Direct substitution gives the stated
   mass-coordinate recurrence, with coefficient
   `(1-alpha)/(1+theta)<=1-theta`. On coordinates above the comparator,
   lower normals vanish and the other normals subtract mass. Summing
   retains the signed response on exactly those selected coordinates.
   Every active coordinate outside `supp(x*_(r/2))` is selected and has
   residual margin at least `alpha r d_i/2`. Weighted Cauchy-Schwarz and
   the residual energy then bound *all repeated* auxiliary support volume
   by `148 K/r`. No support set or optimizer is computed by the solver.

6. **Safe terminal truncation.** Objective accuracy implies the required
   Euclidean error. Uniform density clipping gives a vector below the
   optimum. On retained positive coordinates, Stieltjes signs give the
   needed extra `alpha delta w` decrease of the matrix product; zero
   coordinates have nonpositive product. The absolute row-sum bound in
   degree densities supplies the residual upper bound. Support containment
   removes the KKT linear gap term and gives the stated final gap.

7. **Continuation.** The first stage has diffuse source because its
   regularizer is at least half `1/d_seed`. Repair preserves the baseline
   invariant for every factor-two decrease, including the last clamped
   stage. The sum of reciprocal regularizers is `O(1/rho)`. All accuracy
   costs enter logarithmically; no complementarity margin is assumed.

8. **Local reporter.** Common primal decay and sparse kinetic increments
   permit persistent normalized response records. Changes to the kinetic
   exceptions cost old and new kinetic volume; refreshing the fixed
   source costs `O(K/r)`. Weighted clipped waterfilling is an exact finite
   breakpoint problem with deterministic balanced-tree queries. An
   unexposed vertex has strictly negative raw value. Materialization,
   baseline rescanning, cache construction, and disposal are all charged
   to source exposure or emitted history. There is no restricted solve,
   ambient scan, free boundary oracle, or expected hashing bound.

## Appendix checks in the first pass

The improved end-stage PG repair uses a valid subgradient certificate and
is applied only after a stage. The smaller correction mass cap contains
both analytical comparators; its mass normal has zero contribution in the
second metric. The stronger mass-deficit work bound is consistent with
the KKT support-volume identity. Taking coordinatewise maxima of two
Stieltjes subsolutions is valid; no monotonicity of the quadratic norm is
needed or asserted.

The perturbation proof uses weighted mass bounds to avoid dependence on
the number of unknown coordinates. The downward rounding model preserves
feasibility, and the selected-flow proof absorbs raw score error. The
dyadic reporter enumerates only outputs that survive rounding, including
the equality case at one grid unit. Scalar rebases are charged full passes
over exposed records and introduce a controlled neighbor-sum error.
The exact terminal PG computation correctly avoids treating those
approximate neighbor sums as exact products. Encoding-length claims and
their realization in the packaged software still deserve direct checks.
