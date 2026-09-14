# Exact continuation with projected-gradient repair

`pg_repaired_rppr_solver.py` is a separately named implementation. The
conservative wrapper and the capped-box accelerated corrector remain
unchanged. The new wrapper performs the same regularization schedule and
density shift, but adds one full projected-gradient step after each ordinary
accelerated stage and before truncation.

This implements section 2 of `finite_precision_repair_and_scaling.md` using
exact Fractions only. It does not insert a different update into the stage,
and does not claim a floating-point or bit-complexity guarantee.

## 1. Larger certified stopping tolerance

At a stage with regularization `r`, put `lambda=alpha*r` and prescribe
`0<delta<=alpha*r/2`. The accelerated candidate `x` is computed to

\[
 J_r(x)-J_r(x^*)\le\tau=\alpha\delta^2/2,
\]

instead of the conservative `alpha^3*delta^2/2`. Then compute

\[
 y=[x-\nabla J_r(x)]_+,\qquad \bar x=[y-\delta w]_+.
\]

For completeness, projection optimality and `Q<=I` give
`J_r(x)-J_r(y)>=||x-y||²/2`. Writing `Delta=x-y`, the vector
`v=(I-Q)Delta` belongs to the subdifferential of the nonnegative constrained
objective at y. Thus `||v||<=sqrt(2tau)=sqrt(alpha)*delta<=lambda/2`.
At every positive y coordinate its orthant normal vanishes, so
`Qy_i-b_i=v_i-lambda*w_i<=0`; at every zero y coordinate Stieltjes signs
give the same inequality. Hence `Qy<=b` globally.

The objective gap of y is at most tau, so strong convexity gives
`||y-x*||<=delta`. Consequently the shifted positive part satisfies

\[
 0\le\bar x\le x^*,\qquad Q\bar x\le b,\qquad
 0\le x^*-\bar x\le2\delta w.
\]

The last bound, the degree-scaled absolute row-sum bound, and
`2delta<=alpha*r` imply `0<=b-Qbar<=2alpha*r*w`. This restores the
constant-four source bound at the following factor-two stage. The usual
safe-support and final-gap bounds remain

\[
 \operatorname{vol}(\operatorname{supp}\bar x)\le1/r,
 \qquad J_r(\bar x)-J_r(x^*)\le2\delta^2/r.
\]

The final stage further halves delta until `delta²<=epsilon*r/2`, exactly
as in the conservative wrapper. The returned final certificate therefore
has the same form and still implies the requested objective accuracy.

## 2. A single charged candidate-support scan

The helper `projected_gradient_truncate` accepts an already materialized
sparse candidate in degree densities `f_i=x_i/w_i`. With `c=(1-alpha)/2`,
the PG density is

\[
 y_i/w_i=\left[c f_i+\frac{c}{d_i}\sum_{j\sim i}f_j
                     +\frac{\alpha\mathbf1_{i=s}}{d_i}-\lambda\right]_+.
\]

It first records the candidate values and their already queried degrees.
It scans each candidate adjacency list once, accumulating the numerator

\[
 A_i=c d_i f_i+c\sum_{j\sim i}f_j+\alpha\mathbf1_{i=s}.
\]

Only after this scan does it visit the affected scalar records, obtain any
missing degrees, and compute `max(0,A_i/d_i-lambda-delta)`. Equivalently it
forms the nonnegative PG density and immediately truncates it. The code
counts the intermediate positive records and their degree sum, but never
enumerates their adjacency lists merely because they became positive.

If the candidate support has volume B, this requires B repeated adjacency
entries, `O(B+1)` affected scalar records and degree replies, and
`O((B+1)log(N+2))` deterministic balanced-map work. It makes no global graph
query. Missing row reads are charged separately from repeated cached scans.

In the actual continuation implementation, all positive candidate vertices
belong to the old baseline or previously emitted mirror supports. Their
adjacency and neighbor degrees are already cached in the completed
corrector. Consequently the PG repair adds B repeated entry scans and no
new oracle replies in the tested full trajectories. The general helper
also supports an uncached input, charging those reads explicitly.

The candidate support volume is at most the baseline volume plus cumulative
kinetic volume. Thus the additional end-stage pass fits the existing charged
bound. This argument does not assume that the untruncated PG support has
small volume. Only the retained safe support is passed into the next stage.

Counters distinguish candidate records and volume, first and repeated
adjacency entries, degree replies, numerator updates, affected records,
positive and newly positive PG records and volume, truncated positive
records, and retained records. These are structural counts. Python point
dictionaries and Fraction arithmetic are not a worst-case implementation
of the comparison-map word model or a bounded-bit numerical solver.

## 3. Exact independent checks and iteration comparisons

`test_pg_repaired_rppr_solver.py` passed all three test groups. It checks seven
complete deterministic cases and 13 nontrivial stages. At each stage it
independently computes the dense PG step, compares the repaired output
exactly, and verifies pre-PG, post-PG, and repaired objective gaps, source
nonnegativity, source upper bounds, support containment, coordinate error,
and graph-entry counters. The dense optimum is obtained by exhaustive KKT
support enumeration. Zero and alpha-one branches are included.

For the representative fixtures, the exact comparison was:

| Fixture | Conservative iterations | PG-assisted iterations | Added PG entry scans |
|---|---:|---:|---:|
| Non-dyadic final rho, alpha=2/5 | 31 | 25 | 2 |
| Three-stage tree, alpha=1/8 | 152 | 107 | 14 |
| Two-vertex path, alpha=1/100 | 736 | 450 | 4 |
| Triangle, alpha=1/3 | 48 | 39 | 10 |
| Leaf-seeded star, alpha=1/4 | 47 | 35 | 3 |
| Total | 1014 | 656 | 33 |

These are actual exact iteration counts on those fixtures, not a universal
claim that changing a repaired baseline can never increase a later stage's
iteration count. No wall-clock or floating-point speed claim is inferred.

The small-alpha final gap denominator decreased from 16,418 bits in the
conservative fixture to 10,031 bits here; it remains a large exact-rational
calculation. All certificate comparisons are exact; large fractions are
summarized by their bit sizes in the saved JSON.

## 4. A newly positive degree-10^12 neighbor, removed before any scan

A separate repair fixture gives a direct test of the subtle scan rule.
Take a star whose hub has degree `D=10^12`, choose a leaf as seed, and set

\[
 \alpha=1/4,\quad r=\frac3{5D+3},\quad
 \delta=\alpha r/2,\quad q_0=5/8,\quad c=3/8.
\]

The exact optimum is seed-only with density
`f*=alpha*(1-r)/q0`; its hub KKT inequality is at equality because
`c*f*/D=alpha*r`. Give the repair helper the candidate seed density
`f=f*+e`, with `e=delta/2`. Its exact objective gap is
`q0*e²/2<=alpha*delta²/2`, so it is a certified valid repair input.

The PG step produces

\[
 y_s/w_s=f^*+ce,\qquad y_h/w_h=ce/D>0.
\]

The new hub density is strictly below delta and is therefore immediately
truncated. The helper reads the seed's single adjacency entry, obtains one
hub degree reply, and returns only the seed. A test guard raises an error if
the hub adjacency is requested; the test passes. Intermediate positive PG
volume is `D+1`, while measured adjacency work is exactly one entry.

This is an explicitly constructed certified candidate for the repair
procedure. It is not a claim that a specified zero-start accelerated stage
first reaches that exact candidate. The ordinary full-trajectory fixtures
and this targeted repair fixture test complementary guarantees.

Results are saved in `pg_repaired_rppr_solver_verification.json`. No original
solver or wrapper was modified.
