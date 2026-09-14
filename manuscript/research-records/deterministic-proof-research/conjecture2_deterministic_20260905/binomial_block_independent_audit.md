# Independent audit of the binomial block refinement

The inspected source is `binomial_block_dyadic_rppr.py`, SHA-256
`83410bc3a47566860df969d47b8865e76b1aa0e5fb552bdf125f2be9be088f0f`.
Only fresh task files are used. No implementation is modified.
The completed derivation `binomial_block_schedule_audit.md` was also read
independently; its scalar, every-prefix, setup, power-size, and wrapper
scope arguments agree with the verification below.

**Finding: the refinement is correct.** It changes the fixed endpoint and
its scalar certificate, with the previously audited rounded trajectory,
source interface, mass cap, grid, repair, and kinetic-work lemma inherited.

## Scalar bound

For integer `T>=2`, write `a=1-1/T` and `m=min(6,T)`. The finite positive
binomial expansion gives

    a^(-T) = (1+1/(T-1))^T
            >= S = sum_{k=0}^m binom(T,k)/(T-1)^k.

The first three terms give `S>=1+3T/[2(T-1)]>5/2`. The code constructs
`S=N/(T-1)^m` exactly: its `choose` update is the integer identity
`binom(T,k+1)=binom(T,k)*(T-k)/(k+1)`. Its returned numerator is

    U=ceil(2^16*(T-1)^m/N),    beta=U/2^16.

Consequently `a^T<=1/S<=beta`, with upward rounding error less than `2^-16`.
Also `beta<2/5+2^-16<1/2`, justifying the implementation's strict assertion.
There are at most seven terms, including k=0, and at most seven integer
divisions. Every setup integer has O(log T) bits: a convenient explicit
upper bound for the recorded setup size is `6*bit_length(T)+18`. No power
whose exponent is T is constructed by the algorithm.

## Prefix, endpoint, and zero-step certificates

Let `Ebar` be the inherited source-energy upper bound and let Gamma bound
the accumulated perturbation floor. The prior theorem gives
`E_k<=a^k Ebar+Gamma`. At a positive prefix with `q=floor(k/T)`,

    E_k <= Ebar*beta^q+Gamma.

The code increments its current power only after the inherited iteration
counter completes a T-step block. This implements the displayed q exactly.
The initial certificate is Ebar without Gamma; no perturbation has then
occurred. The schedule chooses the first q satisfying
`Ebar*beta^q<=tau/2` by an exact cross-product comparison. At its endpoint,
the inherited grid bound gives `Gamma<=29*tau/256`, so the total bound is
strictly below tau. If q=0, the output certificate is simply
`Ebar<=tau/2<tau`; calling `run` does not execute an iteration.

The source-energy constructor and its original half-contraction schedule
still run before the replacement schedule. They only compute setup values.
Since beta<1/2, the new number of blocks is never greater than the inherited
number. Zero-step setup, baseline/source initialization, materialization,
and terminal repair are still required and still charged; the refinement
does not declare an entire zero-step stage free.

## Wrapper and work scope

The new `step` calls the unchanged source/integer `step` and updates two
scalar power counts afterward. It does not modify projection, emitted
support, state rounding, exception rebuilding, or graph queries. Thus its
trajectory is exactly a prefix of the source-energy trajectory with the
same baseline and parameters. A later continuation stage may start from a
different repaired baseline because its predecessor stopped earlier; that
is covered by the same certified repair interface, rather than by a claim
that entire multi-stage outputs agree.

The wrapper reuses the stable integer continuation code with a copied
globals mapping whose only changed class binding is the new corrector.
The direct/zero branches, tolerance calculation, exact terminal repair,
safe maximum, result type, and outer regularization schedule are identical.
The every-prefix rounded kinetic bound `360K/r` therefore remains valid
at the earlier prescribed endpoint.

Target powers and current powers are stored as `U^q` and `2^(16q)`, without
introducing a graph degree denominator. Each has at most `16q+1` bits.
Since q is no greater than the original O(L) block count, these scalars are
O(L) bits. Power updates and schedule comparisons add O(L) arithmetic
operations per stage, with O(B)-bit operands in the existing encoded-input
model. The previously audited O(L^3/(rho*sqrt(alpha))) arithmetic bound and
its conservative bit extension are unchanged. The computation is entirely
deterministic and uses no floating-point approximation to the exponential.

## Bounded independent evidence

`audit_binomial_blocks_independent.py` and
`binomial_blocks_independent_audit_results.json` record all passing checks:

- 256 exact comparisons against `(1-1/T)^T` for every T=2,...,257, including
  non-dyadic T allowed by the standalone scalar function.
- Four separately computed truncated-binomial checks for T equal to
  `2^32`, `2^128`, `2^512`, and `2^2048`, without constructing exponent-T
  powers. Setup bit bounds hold.
- Thirteen corrector stages, including two zero-step stages, with 539
  exact prefix comparisons against a separate source-energy corrector.
  Grid, all integer state maps, both reporter registries, emitted entries,
  multiplier, degree/adjacency query sequences, and kinetic counts agree.
- On those same 539 prefixes, independent exact KKT optima and edge-form
  objective evaluation verify the complete accelerated energy, including
  its kinetic distance term, below the newly reported certificate.
- Six full output checks cover multiple continuation stages, non-power
  rational alpha, alpha=1, the exact zero regime, and a nontrivial
  near-contact instance that takes zero accelerated steps. Actual gaps are
  bounded by the returned certificates and requested tolerances.

The new endpoints save 294 iterations relative to the old half-block
endpoints over these bounded fixtures. This is evidence about these cases,
not an additional asymptotic speedup claim. No correction is requested.
