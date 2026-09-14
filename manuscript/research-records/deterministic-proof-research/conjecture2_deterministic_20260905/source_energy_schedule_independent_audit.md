# Independent adversarial audit of the optional source-energy schedule

Result: no mathematical or implementation defect found in the current `source_energy_schedule.md` and `source_energy_dyadic_rppr.py`. The refinement can replace the stage-length rule while keeping the stable recurrence, repair, and original worst-case work bound. This conclusion is conditional on the same safe-baseline input contract as the existing corrector; nonnegative bounded source alone does not establish that contract.

## Initial energy, derived independently

Use normalized coordinates, `lambda=alpha*r`, `mu=theta^2<=alpha`, and `e=x*_r-bar`. The inherited hypotheses are `0<=bar<=x*_r`, `s=b-Qbar>=0`, `s<=4lambda*w`, and `eta=w^T s/alpha=1-w^T bar`.

The original optimum satisfies `Qx*_r-b+lambda*w=r*>=0`. Therefore `Qe-s+lambda*w=r*`. If `e_i>0`, then `x*_i>0`, so `r*_i=0`; this proves the correction complementarity even where the baseline is nonzero. Consequently

`J(0)-J(e)=e^T Qe/2`, and `E0=(e^T Qe+mu*||e||^2)/2`.

The inequality `alpha*||e||^2<=e^T Qe` yields the prefactor `(1+mu/alpha)/2`. Write `g=(s-lambda*w)_+` in normalized coordinates, or `g_i/w_i` in the note's density notation. Since `e>=0`, the quadratic energy is at most `e^T g`. The three bounds follow respectively from `e<=4r*w`, `w^T e<=eta`, and Cauchy–Schwarz together with `alpha*||e||^2<=e^T Qe`. In particular, if `q=e^T Qe>0`, then `q<=sqrt(q/alpha)*sqrt(H2)` implies `q<=H2/alpha`; no division is needed when `q=0`.

The `min(1,...)` is also legitimate independently of the former coarse proof: degrees are positive integers, so `w_i>=1` and `||e||<=||e||_1<=w^T e<=1`. With `Q<=I` and `mu<=1/4`, `E0<1`. Finally `Hinf<=3lambda` and the prefactor is at most one, giving `Ebar<=3alpha*r*eta`. These arguments require the unweighted positive-degree graph model, or corresponding lower bounds on weights; the implementation already imposes positive integer degrees.

## Exact source normalization and bounded arithmetic

Code lines 23–38 implement the density conversion exactly. With `alpha=A/D`, `r=P/R`, grid `1/H`, and stored source numerator `N_i`, source density is `N_i/(2DHd_i)`. Thus

`source_density-lambda = (R*N_i-2AH*P*d_i)/(2DH*R*d_i)`.

The positive numerator in line 30 is therefore correct, including the degree factor and the distinction between the stage regularization and final requested regularization. The code uses the current stage's `self.rho`.

The H1 accumulator is integer addition. The Hinf update uses cross multiplication and retains only one winning degree. The H2 accumulator sums `ceil(G_i^2/d_i)` as integers and divides once by `C^2`; it does not sum rational values with unrelated degree denominators. For each positive term the upward excess is in `[0,1)`, so total excess is strictly below `n_positive/C^2`, and it is zero if there are no positive terms. Using this upper bound inside a minimum is safe because each of the three entries separately upper-bounds the same exact quadratic energy.

If every source numerator and degree has at most b bits, the ceiling term, cross products, and total accumulator require `O(b+log N)` bits in addition to the encoded parameters and grid. The scalar Fraction expressions in lines 39–47 combine a fixed number of parameter denominators and at most one selected degree; they do not introduce an N-term least-common-multiple. The schedule denominator doubles at most the original prescribed number of blocks, so it has `O(log(1/tau))` bits. This audit concerns a bit-length envelope, not a claim that the diagnostic counters trace every internal multiplication.

## Schedule and every-prefix certificate

For integer `m=1/theta>=2`, `(1-1/m)^m<1/2`. One elementary proof is Bernoulli's strict inequality `(1+1/(m-1))^m>1+m/(m-1)>2`. Thus the loop in lines 48–56 selects the smallest nonnegative q with `Ebar/2^q<=tau/2`, and K=mq is sufficient.

The underlying rounded trajectory has `E_k<=a^k E0+Gamma`. The inherited grid remains based on tau, and ensures `Gamma=29h/theta<=29tau/256<tau/8`, as well as the kinetic-ledger error budget. The code only changes the horizon; it does not coarsen the grid when Ebar is small. At any positive iteration k, `Ebar/2^floor(k/m)+Gamma` is valid, including intermediate, non-block endpoints. The inherited `decay_denominator` starts at one and doubles only on a completed block, matching lines 59–63.

At k=0, the separate return of Ebar is valid and avoids a spurious perturbation term. When q=0, `Ebar<=tau/2<tau`, so the inherited strict assertion in `run()` is satisfied. If Ebar=0, positive definiteness forces e=0: the baseline is exactly optimal. The unchanged terminal PG, downward repair, and maximum with the baseline remain safe for both exact-zero and positive-error zero-step stages.

The auxiliary comparison and selected-flow proofs start with the same zero correction and mirror state, the same comparator, and the same grid-error bounds. They apply to arbitrary prefixes; shortening the horizon needs no new potential inequality. For K=0 the kinetic volume is exactly zero. The per-stage schedule is never longer than the coarse E0<=1 schedule. This does not imply that the repaired endpoints or adjacency counts of the two full continuations must be identical, since later baselines can differ.

## Operations and zero-step charges

Line 27 adds a source-record pass to the already assembled source. It uses AVL lookup for each degree, one integer division for each positive term, and a constant number of integer operations/comparisons. It makes no graph-oracle call. The new counters record the visited source records, positive terms, divisions, and schedule checks/doublings.

This pass is paid `O(|supp s| log N)` work, not literally free reuse of a previously counted read. Its order is covered by the source initialization bound `|supp s|<=2 vol(bar)+1`. The original constructor still computes the coarse block count before replacement; those coarse loop operations remain counted by the inherited metrics. Both schedule loops are polylogarithmic.

When K=0, the constructor still pays baseline input conversion, source exposure, degree replies, baseline adjacency scans, initial exception installation, and scalar setup. Candidate materialization, terminal PG, repair, stage diagnostics, and eventual local-state destruction also remain charged. They cannot be charged to K=0 kinetic work alone, but are covered by the separate per-stage baseline/setup term and the dyadic sum of `1/r`. The new source-stat scalars and fixed-size diagnostic dictionaries do not store another graph-indexed collection. No hidden whole-graph enumeration is introduced.

Lines 84–88 copy a fixed-size module namespace and rebind only the corrector class, reusing the exact continuation code and terminal repair. The original module's binding is unchanged. This is an implementation packaging choice, with cost constant in graph size; it does not affect the mathematical algorithm.

## Independent diagnostic

`audit_source_energy_schedule.py` imports no dense optimum solver. It uses the closed-form two-vertex obstacle solution and computes the complete acceleration energy in exact Fractions at every trajectory prefix. `source_energy_independent_verification.json` records:

- Seven initial-energy cases, including nonsquare alpha and both sides of a dyadic theta threshold.
- 155 exact energy-prefix checks, including non-block endpoints.
- One exact-zero stage and one positive-error zero-step stage.
- A public continuation whose final stage takes zero accelerated steps, with exact repaired objective/containment verification.
- Exact reconciliation of degree and adjacency replies, source-record visits, and schedule checks.

All checks passed. The sibling suite separately covers small asymmetric graphs and strict H2 upward rounding; this diagnostic adds analytical optimum and whole-energy prefix checks rather than duplicating that suite.

No core or refinement implementation was edited during this audit. The stable full-schedule solver remains available as a reference.
