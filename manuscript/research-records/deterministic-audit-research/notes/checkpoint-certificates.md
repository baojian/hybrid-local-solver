# Deterministic PG checkpoints with a charged support ledger

Private refinement, September 5, 2026. This does not change the main two-energy
proof or assume support containment for accelerated iterates. It is an optional
early stopping rule with a prescribed-horizon fallback.

## Certificate

At an actual nonnegative stored candidate x in a continuation stage, compute

    p = [x - (M x - b + lambda w)]_+.

The orthant subgradient v=(I-M)(x-p) at p satisfies

    ||v|| <= (1-alpha)||x-p||.

Strong convexity therefore implies

    ||p-x_r|| <= ||v||/alpha,
    F_r(p)-F_r(x_r) <= ||v||^2/(2 alpha).

The second statement follows by minimizing the strong-convexity subgradient
lower bound over the ambient space; the first uses strong monotonicity and
the optimum's zero subgradient. Thus any upper bound R2 on
(1-alpha)^2 ||x-p||^2 satisfying

    R2 <= alpha^2 delta^2 / 4

supplies both distance <=delta/2 and a valid subgradient norm <=delta/2
(because alpha<=1). The established PG clipping, grid rounding, and safe
maximum can be applied immediately. They retain the same final order,
source, and objective guarantees. The certified point is **p**, not x;
the implementation reports this distinction in the stage summary.

## No scan of newly positive PG rows

In original-degree densities, compute incoming values

    a_i = alpha 1{i=v} + c d_i f_i + c sum_{j~i} f_j,
    p_i/w_i = [a_i/d_i - lambda]_+.

Only rows of supp(x) are scanned. All other affected vertices are neighbors
of those rows or the seed; their degrees are queried and original-degree
pruning is applied before retaining a PG entry. Every other allowed vertex
has x=p=0. The squared displacement can thus be computed on the affected
records without scanning a newly positive PG row. Its positive degree-volume
can be very large; the procedure neither charges it as small nor scans it.

## Repeated checkpoint work

At step k the candidate support is contained in the baseline support union
all prior emitted kinetic supports. Its volume is bounded by

    vol(supp baseline) + sum_{j<=k} vol(supp z_j) = O(k/r).

Check only k=1,2,4,... before the prescribed horizon. Summing their candidate
scan costs and state materializations is O(K/r), up to the same tree factors,
because the prefix work theorem holds for every k and the checkpoint indices
sum to less than 2K. Failed checks leave the actual trajectory unchanged.
The successful PG pass is reused for terminal repair. All failed scans and
degree replies are separately included in the returned metrics.

## Bounded arithmetic and an implementation correction

An exact Fraction sum of squared PG displacements can accumulate a least
common multiple of many unrelated original degrees. Exact-real correctness
is unaffected, but that is unsuitable for the bounded-bit extension. The
first component implementation used such a sum; it was replaced during this
audit before final delivery.

If each density displacement has form a_i/(C d_i), use

    U2 = sum_i ceil(a_i^2/d_i) / C^2.

Then ||x-p||^2 <= U2 < ||x-p||^2 + N/C^2 for N nonexact affected records
(the weak bound <= with all affected records also suffices). The numerator
sum uses integers on one common denominator, so its length grows only
logarithmically in the number of records. This is a conservative certificate;
failure simply leaves the prescribed convergence schedule available.

For integer continuation with H the density-grid denominator, stored
candidate densities have denominator dividing H^2. One valid choice is

    C = 2 denom(alpha) H^2 denom(r).

For the direct component solver, replace H^2 by H, since it stores the
primal candidate directly on its density grid. These choices clear each
coordinate's PG numerator exactly. There is no floating comparison.

## Status

The certificate and its charged-work proof are established above. Completed
checks in `results/checkpoint-certificate-audit.json`: 875 common-denominator
norm comparisons, 576 exact PG-point comparisons, and 126 full solver cases
covering 294 stages and 1,746 checks. All 294 stages certified early. Every
stage's safe order, source bounds, objective gap, and all actual degree and
first-incidence replies were checked. A virtual-star test activated a degree
2^100 PG vertex while scanning only the original candidate's one edge.

The pre-existing integer/rational trajectory comparison was rerun after
factoring the PG pass: all 12 cases / 768 steps and 32 wrapper comparisons
still passed. The default fast solver now uses these checkpoints in its
continuation fallback as well as its completed-component route. The explicit
integer/source-energy wrappers retain `early_certificate=False` by default
for reference-trajectory compatibility; callers can enable it.
