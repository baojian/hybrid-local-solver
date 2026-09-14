# Reading the deterministic Conjecture 2 proof

The theorem in `deterministic_conjecture2.tex` answers OP2 in the supplied
`problem_definitions/main.tex`: for every permitted graph, point seed,
teleportation parameter, regularization parameter, and positive additive
objective tolerance, a deterministic local algorithm returns the required
approximate minimizer. In the nontrivial regime `0 < rho < 1/d_seed`, its
fully charged work is

\[
  \widetilde O\!\left(\frac{1}{\rho\sqrt\alpha}\right)
\]

For unrestricted `rho > 0`, include an additive constant:
`Otilde(1 + 1/(rho sqrt(alpha)))`. The theorem uses the exact-real algebraic word model
specified in that source. The output also satisfies
`0 <= x_hat <= x_rho_star`, so its support is contained in the exact optimal
support. The proof does not require strict complementarity, an activation
margin, a supplied support, or a randomized primitive.

The main text proves the original result. The two included appendices give
a bounded-integer realization for rational inputs and practical refinements.
They can be read after the main proof; their sharper constants are not
premises of the original theorem.

The essential argument is this sequence:

1. **Preserve a diffuse source between stages.** A safe baseline `bar x`
   has `0 <= bar x <= x_r_star` and residual source
   `s = b - Q bar x` in the interval `[0, 4 alpha r w]`, where
   `w_i = sqrt(d_i)`. Its source mass is at most `alpha`. This supplies
   a correction box of height `4 r w` and an explicit correction mass cap.
   A halving schedule for `r` preserves these conditions after repair.

2. **Use one projected accelerated recurrence.** The correction and
   momentum states are averaged with a dyadic momentum parameter
   `theta` comparable to `sqrt(alpha)`. Only the momentum state is
   projected onto the box and mass cap. The ordinary accelerated energy
   gives the required objective accuracy in logarithmically many blocks
   of `O(1/sqrt(alpha))` iterations.

3. **Control the actual nonlinear residual by a second energy.** This is
   the central additional argument. For the analytical comparator
   `t = Q^{-1}s`, the Euclidean projection normal `n` satisfies
   `(p-t)^T Q n >= 0`. Lower-box, upper-box, and mass normals each have
   the required sign because `Q` is Stieltjes and `Qw = alpha w`.
   A general comparison lemma therefore applies in the `Q` metric to
   `A(xi) = ||Q xi-s||^2/2 + alpha^2 r w^T xi`. It yields

   \[
     \|Q(\xi_k-\xi^*)\|^2\le18\alpha^2 r
   \]

   throughout the actual projected trajectory. The comparator is not
   claimed to minimize this auxiliary quadratic, and the auxiliary
   energy is allowed to be negative. Neither fact prevents the proved
   comparison inequality from applying.

4. **Turn residual control into a bound on repeated local work.** The
   analytical set `supp(x_star_(r/2))` has degree volume at most `2/r`.
   Outside it, the stage optimum has residual margin at least
   `alpha r w_i/2`. A signed-flow inequality is summed only over the
   coordinates selected by the next momentum state. Cauchy's inequality
   and the second-energy bound then give

   \[
     \sum_{k=0}^{K-1}\operatorname{vol}(\operatorname{supp}z_{k+1})
       \le148K/r.
   \]

   This sum charges repeated scans of a vertex each time it is selected.
   The analytical set and the exact optima are never queried.

5. **Realize every iteration with exposed records.** A balanced search
   tree maintains the raw projection keys and degree-weighted moments.
   Tail queries locate the clipped mass constraint, and an exact finite
   breakpoint search determines its multiplier. Only positive stored
   momentum outputs are enumerated. Every positive state has already
   exposed its neighbors; an unexposed vertex has a negative raw value
   and cannot be selected. Source refreshes, old and new exceptions,
   degrees, repeated cached reads, materialization, and discarded state
   are all charged to the proved history bound.

6. **Repair and continue.** After reaching the prescribed stage
   objective tolerance, a certified truncation returns a lower baseline
   with a nonnegative diffuse source. The next regularization is no
   smaller than half the current one. At the last stage, the truncation
   shift is reduced until its proved objective error is at most the
   requested tolerance. The geometric sum of `1/r` over the stages
   completes the original work bound.

The two distinctions most useful during review are that iteration count
alone does not establish locality, and that projection is not asserted to
be nonexpansive in the `Q` metric for arbitrary pairs. The selected-work
inequality establishes locality; the sector inequality holds for the one
specific analytical comparator needed by the second energy.

The appendices use three different sufficient stage budgets. They concern
three explicitly different terminal repairs:

| Realization | Sufficient stage gap | Terminal operation |
|---|---|---|
| Main exact-real theorem | `alpha^3 delta^2 / 2` | Clip density by `delta`. |
| Exact projected-gradient refinement | `alpha delta^2 / 2` | One exact projected-gradient step, then clip. |
| Bounded-integer implementation | `alpha delta^2 / 8` | The same exact terminal gradient, then clip and round downward. |

Each uses `delta <= alpha r/2` and obtains final gap at most `2 delta^2/r`.
The complete integer wrapper also takes the coordinatewise maximum with
the previous safe baseline. This preserves the Stieltjes subsolution
condition and prevents the baseline from decreasing.

For rational inputs, the appendices control rounding errors in both
energies. Densities lie on a dyadic grid, global scales are periodically
rebased, and degree-weighted tree moments have common denominators.
No denominator is allowed to grow as an unbounded product over iterations.
With `L` the explicit parameter-and-accuracy logarithm in Appendix A.10,
the resulting bounds are

\[
 O\!\left(\frac{L^3}{\rho\sqrt\alpha}\right)
 \quad\text{word/arithmetic operations},\qquad
 O\!\left(\frac{L}{\rho\sqrt\alpha}\right)
 \quad\text{adjacency inspections}.
\]

A separately stated conservative bit bound multiplies the first quantity
by `B^3`, where `B` bounds the encountered integer encoding lengths.
This extension does not assert stability of an ordinary floating-point
implementation.

In the same nontrivial regime, the actual rounded algorithm also satisfies
the stronger bound

\[
 \widetilde O\!\left(
   \frac{1-\sum_i\sqrt{d_i}\,x^*_{\rho,i}}
        {\rho\sqrt\alpha}\right).
\]

The numerator is an analytical mass deficit in `[0,1]`; it is not required
as an input. The source mass makes its stage surrogate available, and the
returned vector estimates the final deficit within a factor `1+alpha`.
This refinement retains an additional permitted stage-count logarithm.

The standalone package in `deliverables/deterministic-rppr` contains the
bounded-integer implementation. Its default `solve` combines the source
energy bound, a certified binomial block schedule, geometric cached
objective checks, and direct replacement of persistent tree exceptions.
An inconclusive objective check continues to a proved deterministic
fallback horizon. The optional `solve_with_singleton` can certify the
exact one-coordinate optimum after reading only the seed row and querying
its neighboring degrees; its trial
work and any fallback work are reported separately.

Two further options preserve the theorem while changing the trajectory.
`solve_adaptive` chooses the next regularization from the exact maximum
of the repaired residual source. It can skip halving stages, but requires
a separately charged source pass and is not faster on every measured
fixture. The mass-scaled grid refinement in Appendix A.14 replaces the
rounding floor `29 h/theta` by `29 eta h/theta`, where `eta` is the exact
remaining correction mass. It permits coarser dyadic state while keeping
the actual stage tolerance, terminal repair, and work guarantees. Its
grid must represent the incoming baseline exactly; unused grid bits need
not be retained. Neither option is needed by the default algorithm or by
the main theorem.

The proof is a mathematical argument. Exact implementation tests, distinct
objective certificates, and the fresh audits performed within this task
provide additional checks. They are not substitutes for its lemmas or a
claim of external peer review. The 183-case package integration manifest
checks complete outputs against exhaustive exact optima. The default and
combined backends produce identical outputs and certificates on that
manifest; these are paired backend checks on the same cases, not 366
different graph instances.

The adaptive continuation and mass-scaled-grid research implementation
also passed this same 183-case manifest, with their own complete outputs
and separate work ledgers checked independently. These are additional
backend validations on the same fixed cases. Small exact prefix audits
separately cover the two energy inequalities, rounding, rebases, and
zero-step branches; the integration manifest alone is not claimed to
exercise every branch.

For a concrete calculation, `worked_three_vertex_example.md` derives the
entire regularization path of a three-vertex graph and compares it with
the returned dyadic solution. Its figure is only an illustration; all
reported certificates and breakpoints in the accompanying data are exact.

Only the designated `problem_definitions/main.tex` was read from the
manuscript. The supplied source and other manuscript notes were not edited.
