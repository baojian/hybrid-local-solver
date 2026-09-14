# Independent audit of the practical-refinements TeX appendix

Audited `practical_refinements_appendix.tex` against the fresh main TeX,
the mass-deficit refinement note, the perturbation theorem, and the
bounded-dyadic realization. Neither TeX file was modified. Line numbers
below refer to the version read at the beginning of this audit.

## Finding

No mathematical sign, constant, or scope defect was found. The appendix
correctly separates the stronger exact mass-deficit work bound from the
conservative rounded work bound, and it does not claim unchecked
floating-point correctness.

There is one small operational transcription omission in lines 314–334.
After defining `sigma'=floor_h(a sigma)` and updating X, the text assigns
`sigma=1` in the rebase branch but does not explicitly assign
`sigma=sigma'` in the non-rebase branch. The intended update follows from
the surrounding proof, but the algorithm description should say it.
That passage should also explicitly identify the next kinetic state as
`z=p`, refresh its exact neighbor sums, refresh the touched base keys,
and install the new exceptions after the scale transition. Those latter
operations are specified by the main reporter protocol and are implicit
here; spelling them out prevents a misleading literal implementation.
This finding was sent to the parent before this note was saved.

## Source mass and the exact refinement

At lines 92–107, `eta=m_s/alpha=1-w^T baseline` is exact and positive in
the stated nonzero regime. The comparator has mass exactly eta and the
true correction lies below it. Thus both fit the smaller cap. On the
active cap face the Q-sector contribution is exactly
`gamma(alpha eta-m_s)=0`; there is no missing positive or negative term.
The exact response estimate remains `18 lambda m_s`.

The support-deficit identity at lines 109–117 follows directly by summing
the nonnegative source over the positive optimizer support. Its source
equals `alpha q w` there and its total weighted mass is
`alpha eta_*(q)`. Hence

    vol(supp x*_q) <= eta_*(q)/q,

and the analytical half-parameter core has volume at most `2eta/r`.
The correction-core equality at lines 119–122 is also sound: at a
coordinate where the ordered optimizers are equal and positive,
Stieltjes signs impose the reverse ordering of their row products from
that forced by the two distinct stationarity penalties. The proposed
equality is therefore not discarding an active baseline coordinate.

Independently substituting `m_s=alpha eta` into lines 124–137 gives

    Y <= 2 B_0 + 4 H_2/lambda^2
      <= 4eta K/r + 72eta K/r = 76eta K/r.

This is correctly 76, rather than the looser 148 of the main unit-cap
proof. It charges the sum of supports over all iterations, not merely
their union. The baseline volume and source-record counts at lines
139–143 inherit eta because `baseline<=x*_r` and
`eta_*(r)<=eta`. In the nonzero regime optimizer support is nonempty,
so `eta/r>=1` absorbs the additive source and iteration work.

## Maximum repair and final-parameter dependence

Lines 145–158 use the correct closure property: if two nonnegative
vectors are subsolutions of `Qx<=b`, their coordinatewise maximum is
also a subsolution. At a row selected from either vector, its diagonal
coordinate stays fixed and all off-diagonal coordinates increase.
This preserves safety and the uniform density error below the optimizer.
The objective bound is reapplied using `Q<=I`; the text correctly avoids
assuming that a coordinatewise smaller error has a smaller Q norm.

The deficit comparison

    eta_*(r) <= eta_new <= (1+alpha) eta_*(r)

uses precisely `2delta<=alpha r`, together with the stronger support
bound. It holds after both the exact repair and the final rounded repair
once their common density-error invariant is proved.

At lines 161–180 the direction of convexity and of the ratio inequality
is correct. A convex combination of obstacle optimizers is a nonnegative
supersolution at the interpolated parameter, and dominates the least
supersolution there. Thus optimizer coordinates are convex, the mass
deficit is concave, and `eta_*(R)/R<=eta_*(r)/r` for `R>=r>0`.
The factor-two stage relation then gives
`eta_j/r_j<=4eta_*(rho)/rho`. The initial zero baseline is correctly
covered by `eta_*(1/d_seed)=1`. Summing the logarithmic number of stages
proves the displayed exact refinement. No geometric summability of the
mass-weighted stage quantities is incorrectly assumed.

## Perturbations and the rounded constant

Lines 185–241 correctly state the perturbation model for the actual
stored state. The ideal projection can be unmaterialized. Both errors
after that projection are downward; feasibility follows from this
direction, nonnegativity, and the downward-closed correction set.

The raw perturbation costs at most `2mu kappa_r` in either energy. For
the primal rounding difference d, its lost mass is at most one and its
density is at most `kappa_d`, so `||d||^2<=kappa_d`. The quadratic and
linear terms cost at most `5kappa_d/2`. The mirror rounding cost is
`5mu kappa_p/2`. This gives exactly

    zeta = 2mu kappa_r + (5/2)kappa_x
                         + (5/2)(theta+mu)kappa_p.

The response bound `18alpha^2 r+4Gamma` follows from adding Gamma to
the auxiliary comparison energy, even though that energy need not be
nonnegative. The source-mass cap is allowed here, but the proof deliberately
uses the conservative unit-mass constants.

At lines 249–269 selection by the rounded p implies strict selection by
the ideal p0, so its lower projection normal vanishes. Upper/cap normals
and downward rounding only subtract mass. The only new adverse flow term
is bounded by `nu d_i`, with `nu=theta kappa_r`. Under
`nu<=lambda/4`, the stated Young inequality gives

    total kinetic volume <= 16H_2/lambda^2 + 8K/r
                         <= (16*22+8)K/r = 360K/r.

No eta factor is silently inserted into this rounded estimate. The final
paragraph at lines 472–479 correctly reserves the stronger eta-dependent
claim for the exact trajectory.

## Scalar-only rebasing

The closed threshold in lines 300–312 has the correct direction and
includes equality at h. Its equivalence to a positive rounded projection
requires `h<=U=4r`, which follows from the displayed precision budget.
There is no scan of sub-grid ideal positive coordinates.

The density errors at lines 314–339 are correct once the non-rebase scale
assignment mentioned above is made explicit. The temporary scale is at
least 1/8; normalized densities are bounded by 32. Scale flooring costs
at most `2Uh`, normalized X flooring at most h in physical density,
and a rebase adds at most another h. Thus `kappa_x<=10h`.

The approximate neighbor recurrence at lines 341–358 is correctly
transcribed. It uses the old X and L independently, and it must not
scatter the rebase's X differences. The error after a rebase is

    eL_new = sigma' eL + sum_adj floor_loss_X - floor_loss_L.

Since `sigma'<1/2`, the invariant `|eL_i|/d_i<=4h` holds. Exact scattered
changes between rebases preserve eL. This induces raw density error at
most `2h/theta`, because the primal response coefficient is
`sigma c/[theta(1+theta)]`.

Substitution in the energy formula gives at most `29h/theta`, and
`29/256<1/8`. Also `2h<=lambda/4` follows from the grid budget,
`tau<=alpha^2r`, and `theta<=1/2`. Thus both the gap and conservative
rounded work hypotheses are met. The rebase count and scalar-record
charge at lines 373–380 follow from `h<=theta`; no historical adjacency
read is hidden in the scalar-only variant.

## Bounded arithmetic and terminal repair

The weighted key equation at lines 392–410 has the correct signs and
degree normalization. A stronger common denominator than the one printed
is `2 B_alpha H(T+1)S`; the displayed extra T factor is conservative and
valid. Multiplying by the physical scale cancels S. Exact weighted moments
therefore do not accumulate degree denominators. The cap eta itself is
dyadic because it equals one minus the degree-weighted dyadic baseline
mass, so its use as a waterfill target introduces no missing parameter
denominator. Immediate flooring removes the exact projection's free-
degree denominator before the next stored vector is formed.

The encoding statement at lines 427–442 properly includes rational input
encodings, grid precision, momentum precision, exposed record count,
degree encodings, and fixed factors for intermediate products. An
approximate L record is bounded by its exact neighbor sum plus `4h d_i`,
so the included degree-encoding term also covers these records. The
statement does not confuse reduced Fraction measurements with every
internal arithmetic temporary. For b-bit rational operands, an
unreduced addition uses at most `2b+1` bits, and gcd/division do not
increase that envelope.

Finally, the PG-assisted tolerance `tau=alpha delta^2/8` yields both
position and valid-subgradient errors at most `delta/2`. Flooring after
clipping leaves total position density error at most `2delta`. The row
inequality at lines 460–466 is correct: clipping lowers the retained
Q row by at least `alpha delta w_i`, and downward grid flooring can
raise it by at most `h w_i`. The maximum repair then preserves safety
and the same error bound. The next factor-two stage obtains its required
source upper bound, and the final requested objective error follows.

The explicit instruction to compute an exact terminal PG response from
the actual candidate is necessary and present: approximate L is not
silently reused as an exact terminal certificate.

## Scope

This audit establishes consistency of the mathematical transcription,
subject to the one small operational update clarification above. It does
not compile or render the TeX, modify its files, or certify the separate
software implementation. The zero regime and alpha=1 are handled by the
main theorem; the appendix explicitly works in the remaining regime.
