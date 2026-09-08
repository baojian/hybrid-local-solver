# Conjecture 3: second-night results and the next decision

Research window completed: **481.581 new active minutes**; prior-night work and unverified gaps are excluded.

**Conjecture 3 remains open.** I recommend making local discovery the main
next question, using the new significant-potential envelope theorem as a
precise target. The supplied numerical solver now has substantially more
of its correctness, error, range and work accounting in place, but its
general weighted constructor remains an explicit condition.

The work concerns the original ACL/APPR target
`O_tilde(1/eps_appr)` without a polynomial `1/alpha` factor. It does not
replace this target by the different RPPR normalization. All new proof
claims are drafts awaiting independent review. The exact active-time
record is `OVERNIGHT_20260907_WORK_LOG.json`; the first night's work and
unverified gaps are excluded.

## The cleanest new local target

Let `u` be the full obstacle solution for `M=D-gamma*A`, with
`lambda=eps_appr/2`. A supplied set `U` need only contain

    { i : u_i > eps_appr/8 }.

It can omit the smaller positive coordinates. If `v` is the restricted
obstacle solution using original full degrees, then `0 <= v <= u` and
`||u-v||_infinity <= eps_appr/8`. A feasible numerical approximation `w`
with the same coordinate accuracy, followed by
`x=(w-eps_appr/8)_+`, satisfies the original ACL residual inequalities.
The output is `(1-gamma)*D*x`, and its support remains inside the true
positive support.

The proof is a short maximum-principle argument. Its exact audit covers
1,097 physical inputs, every admissible supplied envelope on the tested
small graphs, threshold ties, omitted positive coordinates, empty sets and
751,993 clipped-output residual certificates.

**The missing algorithm:** find such a `U` with original volume
`O(1/eps_appr)` in fully charged `O_tilde(1/eps_appr)` local work. The theorem
does not provide that finder. An existing boundary-event formulation is
another valid route; neither requires proving an exact-support recognizer.

## One tempting route is now ruled out

Ordinary breadth-first exploration, even with a degree filter, cannot
find this envelope at the target asymptotic work. The counterexample is
an original unweighted tree: a degree-three seed joins a long path and
two binary branches. Every degree is at most three.

For path length and binary height `N`, take `lambda=1/(16*N^2)` and
`alpha=lambda^2`. The explicit subsolution
`z_i=2*lambda*(N-i)^2` on the path, with zero values on the branches,
proves that the path coordinate at distance `floor(N/2)` has potential
at least `1/32`. BFS spends `Omega(2^(N/2))` original row work before
even discovering its label. The target expression, including any fixed
polylogarithms in the ambient size and input parameters, is polynomial
in `N`. This proves a failure of the BFS rule, **not a lower bound on
arbitrary local algorithms**. Our earlier local tree result already
handles this family.

The finite original-tree audit also gives a concrete example with
33,554,943 ambient vertices and positive-support volume only 3,193.
A path vertex of potential approximately 0.534 remains undiscovered
under a 65,536 row-degree budget; discovering it requires at least
98,329 units. Supplied symmetry is used only to validate the example.

## What the supplied numerical route now has

- Corrected signed-domain VWF elimination with persistent function values,
  integrals, exact recovery and accounting for all allocated versions.
- Explicit mixed relative/additive accelerated tolerances, compression and
  refinement. The child error budget is `eta/(2^34*kappa)`; it needs no
  hidden minimum objective gap, split separation or curvature drop.
- A spectral edge-floor wrapper and a simultaneous recursive range proof.
  They control logarithmic numerical ranges without assuming every nonzero
  scalar has polynomial magnitude in the current shrinking graph size.
- A computable spectral gap certificate and a complete conditional supplied
  near-linear recurrence, including scalar-piece input size, nonconstant
  base solves and global failure probability.
- A genuinely nested implementation on supplied families. The fixed policy
  passes 389,120 inner accelerated steps. On the same two physical profiles,
  certified stopping uses 6,525 steps plus 12,605 paid tree certificates.
  A third signed profile exercises actual piece changes and positive
  compression errors. All four saved physical outputs pass the original
  ACL certificate after the proved repair.

These are finite exact integration checks, not a benchmark establishing
general asymptotic complexity. The general fast constructor is not
implemented. CPW's printed constructor still assumes a polynomial weight
ratio; checked arbitrary-weight tree and sparsification primitives motivate
an extension but do not by themselves prove it. The complete source contract
is stated explicitly in `sections/op3_supplied_recursion.tex`.

## Recommended next decisions

| Priority | Direction | Concrete success criterion |
|---|---|---|
| 1 | Potential-driven local discovery or geometric boundary events | Produce the envelope or a valid terminal boundary certificate while charging every exposed row, failed check and old-value update. Test the argument against the binary-branch/path family and dense cores. |
| 2 | Close the supplied weighted-constructor contract | Reconcile the actual weighted forest, routing and core sparsification construction with its source assumptions and full cost. Keep this separate from locality. |
| 3 | Review and extract the structural results | Independently check the tree/unicyclic and canonical multipartite results, persistent VWF primitives and new envelope proof; turn the strongest complete pieces into a shorter presentation. |

I would stop investing in breadth-first exploration with degree filtering and in
an unquantified “warm start should be cheap” argument. The numerical tools
make a more focused discovery question possible; further large audit suites
should answer a specific remaining mathematical uncertainty.

## Where to review

- Main proof: `main.tex`, especially the sections on mixed additive oracles,
  recursive ranges, spectral certificates, supplied recursion and significant
  envelopes. The bibliography identifies source imports separately.
- Latest evidence and checks: `OVERNIGHT_20260907_BLOCK12_AUDIT.json` and
  `VERIFICATION.md`. Full JSON records include source/backend hashes.
- The remaining constructor review is mapped in
  `WEIGHTED_CONSTRUCTOR_REVIEW_20260908.md`, including a visually checked
  Claim 5.14 display/proof mismatch and its small routing example.
- Earlier second-night blocks retain the structural core/module results and
  the development of the numerical route in `STATUS.md` and the work ledger.

The focused checks pass. The repository-wide checks retain the previously
recorded unrelated test, lint and oversized-note failures; reproduction
stops at its test prerequisite. Exact final counts and the final PDF review
are recorded in the block audit rather than inferred from an overall green
repository status.
