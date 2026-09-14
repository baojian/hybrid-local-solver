# Independent audit of the integer implementation complexity corollary

This audit checks `integer_source_complexity_corollary.md` against the fresh
stable `integer_dyadic_rppr_solver.py`, `source_energy_dyadic_rppr.py`, and
the already independently audited two-tree realization. It does not
re-prove the nonlinear kinetic-work theorem, which is explicitly a premise
of the corollary. No implementation changes or new solver runs are needed.

**Finding: the stated cubic-log arithmetic bound and conservative bit
extension are valid under the corollary's declared model.**

## Precision and schedule

At an ordinary stage `tau=alpha^3*r^2/32`. If the last stage halves its shift,
the previous shift failed the stopping comparison, giving final
`delta^2>epsilon*rho/8` and `tau>alpha*epsilon*rho/64`. Otherwise the ordinary
formula applies. Thus the displayed minimum lower bound on tau is correct.
Stage tolerances decrease, so the fresh default dyadic grid is never
coarser than its predecessor. Every preceding baseline denominator divides
that predecessor's grid denominator, and hence divides the new denominator.
The baseline compatibility constraint cannot cause an additional hidden
precision loss in a complete default wrapper.

For the stated `L=16+4a0+3r0+e0`, the explicit estimate is

    log2(H) < 9+log2(T)+log2(1/tau_min)
            <=16+(7/2)a0+2r0+e0 <= L.

The number of standard blocks is at most L, and the source-energy
constructor only shortens that number. Its base constructor still computes
the original schedule; that loop is paid by another O(L) scalar operations.
The code's optional full integer-size snapshot is not called by the default
wrapper. Its normal diagnostic summary is of fixed size and does not scan
the state at each iteration.

## All repeated state visits

The prefix kinetic ledger gives `W<=360K/r`. Initialization adds at most
`1+2/r` exposed records, so `N<=363(K+1)/r` is safe, including K=0.
Every positive correction coordinate was emitted previously. Therefore
candidate materialization and the terminal PG scan cost O((K+1)/r), even
though the candidate support is larger than the current kinetic support.
The repaired baseline and each stage's source have O(1/r) volume/records.

With a reset starting at S=H, one scale decrement is at most H/T+1, and
the trigger requires losing more than H/2. Since H>=T, each complete reset
interval is longer than or equal to T/4; the conservative `4K/T` count is
valid. A scalar rebase really does visit every old X/L/exposed record, but
the resulting cost is explicitly included as

    O((1+theta*K)*N*log(N+2)).

It reads no adjacency. The old/new exception refresh costs are bounded by
current and previous kinetic volume plus the fixed source per step. The
four-sequence root search costs O(log^2(N+2)) per step. These observations
give the corollary's stage expression without omitting a history scan.

Substitution of `K<=T*L` and `log(N+2)=O(L)` gives O(T*L^3/r).
Before the final shortened stage the inverse regularizations form a
geometric sequence; adding the last stage gives `sum 1/r_j<3/rho`.
Consequently no extra number-of-stages multiplier is required. The same
sum gives O(T*L/rho) total first/repeated adjacency-entry inspections.

## Encoded arithmetic and storage

The common grid and mass caps bound X/z/baseline counts by O(H) after their
degree weights are included. The approximate neighbor invariant is
`|J_i-sum_neighbor M_j|<=4d_i`, which permits large individual degrees but
adds only their input encoding length. Base and exception coefficients are
fixed-degree polynomial expressions in the current parameters and counts.
Subtree moments add O(log N) bits, not a product of N coefficients.

A query breakpoint has one selected degree denominator, possibly combined
with the fixed regularization denominator. Weighted tree moments are
integer sums. The affine root divides by one free-degree sum. Intermediate
Fraction expressions combine only a fixed number of these bounded-size
factors; algebraic cancellation and immediate reduction do not accumulate
denominators across successive rank candidates. Projection floors discard
per-coordinate denominators before the next iteration.

Source-energy statistics use integer sums and integer upward divisions;
their final common denominator and the one retained maximum's degree do
not create a degree LCM. Terminal candidate denominators divide H^2, so
PG neighbor accumulation has denominator dividing `2D*H^2` before division
by the target degree. The subsequent floor returns to denominator H.
Thus all persistent and temporary arithmetic operands have O(B) bits for
`B=O(b_par+b_graph+L)`.

The deliberately loose O(B^3) charge per exact Fraction operation is valid
using elementary integer arithmetic and a conservative Euclidean-gcd
bound. This is a separate encoded-input/local-oracle theorem, not an
assertion that floor is free in the original exact-real model. The costs
inside a user-supplied graph oracle must be added, as the corollary states.

The wrapper's retained summaries contain repaired outputs and scalar
statistics rather than corrector histories. Their cumulative output volume
is O(sum 1/r_j). Temporary overlap while constructing the next corrector
changes only the constant in the peak-state bound. Consequently the stated
O(L/(rho*sqrt(alpha))) words and O(BL/(rho*sqrt(alpha))) bits follow. Repeated
optional full-state diagnostic snapshots remain outside the default bound
and require their explicitly charged additional scans.

No correction is requested. The direct/zero branches, K=0 stages, arbitrary
rational parameter encoding lengths, and potentially enormous discovered
degrees have all been kept separate from the paid local record count.
