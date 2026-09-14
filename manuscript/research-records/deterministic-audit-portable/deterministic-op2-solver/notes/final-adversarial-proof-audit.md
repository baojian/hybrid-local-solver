# Final adversarial proof pass

This is an additional independent reasoning pass over the complete proof and
its private implementation refinements. It does not replace the first-read
audit or claim formal machine verification. No new gap was found in the
checks recorded below.

## Fixed restriction and comparison

On A={d_i<=1/rho}, retain original degrees. Entrywise Stieltjes signs give
Mw>=alpha w and |M|w<=w; principal eigenvalue bounds remain alpha I<=M<=I.
This restriction stays fixed throughout continuation. Every stage optimum
for r>=rho equals its full-graph counterpart. The analytical optimum at r/2
in the volume proof is restricted to A, including when r/2<rho.

For monotonicity, let S={x_r>x_(r/2)}. On S, KKT and Stieltjes signs yield
M_SS(x_r-x_(r/2))_S<=-alpha r w_S/2, contradicting inverse positivity.
Outside supp(x_(r/2)), both optima are zero in that coordinate; monotonicity
of their neighbors then gives the required slack margin alpha r w_i/2.

The second energy must use lambda(Mw)^T xi after restriction. Its M-gradient
is still M xi-s+lambda w, and A(M^{-1}s)=lambda w^T s. The normal-cone sector
is needed only at that inverse-source comparator. It holds on lower faces,
upper faces, and the active source-mass cap separately. A negative second
energy is allowed by the comparison lemma and does not invalidate unrolling.

## Signed-flow accounting

The mass-coordinate transition is nonnegative and column-substochastic.
On selected coordinates where the next kinetic state exceeds its comparator,
lower projection normals vanish; upper and cap normals subtract. The fixed
outside-core slack is charged independently of how tiny a positive emission
is. Telescoping removes old excess stock. Cauchy--Schwarz uses selected
degree-volume and the actual squared response, not a general signed l1
propagation bound. This proves every-prefix work and therefore also pays
geometric checkpoints and final materialization.

## Rounded implementation

Between scalar rebases, exact point increments preserve the discrepancy
between stored normalized neighbor sums and true sums of normalized positions.
At rebase its per-degree magnitude obeys e_new<=sigma e+2h with sigma<1/2,
so e<=4h. The raw-key perturbation is at most 2h/theta.

Before a step sigma>=1/2 and normalized positions<=2U<=8. Flooring sigma
loses at most8h, flooring a selected normalized increment loses at mosth,
and an optional position rebase loses at mosth. Every displacement is
downward, preserving feasibility. The raw-sector and quadratic perturbations
give zeta<=29h and the stated two-energy bounds. A grid h<=theta*tau/256
leaves strict tolerance slack. The separate h<=theta*alpha^2*r/29 condition
also directly controls the response-work error in the general stage API.

The rounded selected-flow charge includes error on the selected analytical
core; it is not enough to absorb only the outside error. Let D be repeated
outside volume, B<=2K/r the core allowance, and nu=2h<=lambda/4. Then

    (lambda/2-nu)D <= sqrt(H2(D+B))+nu B,
    H2<=22 alpha^2 r K.

Using sqrt(H2(D+B))<=lambda(D+B)/8+2H2/lambda gives
D+B<=4B+16H2/lambda^2<=360K/r. This checks the stated rounded constant
including the core raw-error term. The bound H2 follows from Gamma<=alpha^2 r
and the squared response estimate, using 0<=M-mu I<=M and commutation.

An independent exact perturbation audit then checked 16,128 one-step cases
on arbitrary feasible state pairs, all signed raw-error corners, and actual
downward grid floors. It checked both energy inequalities and the selected
flow directly, on full-graph and Dirichlet matrices. All passed, including
1,012 active-cap cases and 266 upper-face cases. This supplements the
algebraic proof and the earlier exact trajectory comparisons.

The rebase count is O(K theta+1): one step decreases scale by at most
theta+h, and h<=theta/256. Rebases read scalar records and inspect no graph
incidences. Ghost neighbor-sum records left by independent downward floors
stay within the same error bound and cannot be treated as exact responses in
the terminal PG pass; the implementation recomputes that pass exactly.

Source numerators share denominator 2 denom(alpha) H d_i. Reporter moments
cancel the degree factor. Source-square and PG-displacement sums round upward
before aggregation, avoiding a least common multiple of unrelated degrees.
All exact waterfill tests are finite breakpoint searches, with closed tails
for positive rounded emissions. No unresolved precision-dependent bisection
or floating sign test is used.

## Degenerate and short stages

The source-energy bound can prescribe zero iterations. Its bound then has
no accumulated-rounding term. One exact PG/clipping pass still supplies the
stage guarantee, and source construction plus baseline volume pays its work.
If the correction optimum is zero, preserving the old safe baseline avoids
unnecessary erosion. Tiny positive corrections may also be below the requested
stage tolerance without requiring support identification.

A checkpoint certifies its projected-gradient point, not necessarily its
input candidate. The code records that distinction and reuses the successful
pass. Failed checks do not change the trajectory. Newly positive PG rows may
have arbitrarily large total original degree; only their records and degree
replies are needed. Terminal clipping precedes any further row scan.

## Component and pilot refinements

The forest paths form rooted trees, so each used edge belongs to only one root
tree. Its summed coefficient is bounded by that root's load, which proves
the Poincare bound. Original boundary degrees are retained. Unit edge lengths
ensure each initialized boundary root keeps its own root status.

A partial pilot uses beta_C only for its restricted acceleration. Acceptance
uses alpha and the full-A PG point, including boundary records outside C.
Failure discards its candidate and restarts continuation from zero; no
unverified diffuse source or warm baseline enters the main proof. One bounded
pilot plus fallback preserves the OP2 work bound. If C contains the full
optimum, the stricter pilot tolerance and norm-rounding allowance guarantee
acceptance by the fixed horizon without a strict-complementarity margin.

The integer component step is an exact algebraic transcription. Its inactive
mass-cap test is an exact integer comparison of box-projected mass; when
active, every reporter key is refreshed before querying. This full-region
pass is valid only because region volume<=1/rho; it is not applied to local
continuation's growing history.

## Ordinary coordinates and fixed-size exact components

The ordinary rational-coordinate wrapper reserves one quarter of the target
for the density solve, bounds square roots downward by arithmetic bisection,
and returns the explicit rational certificate 2B+eta^2. Safe order gives
support containment, so the KKT linear term vanishes in the quadratic error
identity. Unit mass and original degrees at least one control the conversion
norm without a dimension factor. All conversion operations and output words
are additional charged work, and no additional graph query is made.

The new exact obstacle solve is permitted only after component discovery
completes and only for at most sixteen vertices. Its symmetric density
matrix is positive definite and Stieltjes. A positive inactive violation
gives a positive new coordinate through the Schur pivot; inverse positivity
makes every old coordinate increase. Thus there are at most sixteen pivots,
and exact terminal KKT conditions identify the global optimum because the
completed retained component contains it. The enforced constant size pays
all cubic elimination and quadratic storage costs, including rational
encoding growth. This branch returns a final exact answer; its nondyadic
values never enter the continuation baseline interface. Incomplete pilots
continue to require the existing full-problem certificate.

The later changes to the parallel core manuscript add explicit definitions,
standard-property derivations, and clarification of selected-flow and exposure
invariants. They do not change the core argument used here. Its newly expanded
optional schedules and stronger mass-deficit statements are not needed by
this report or asserted for this package merely because they appear there.
