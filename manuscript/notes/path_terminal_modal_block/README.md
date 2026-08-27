# path_terminal_modal_block

This note isolates the open terminal-face mechanism in the short endpoint-path
candidate from `volume_gated_acceleration`. It proves the exact weighted cosine
decomposition, the scalar damped-wave formula, the literal global-correction
range implication, explicit prefix optima/transports, the exact entry-velocity
quadrature, and pointwise nonpositivity of the ideal packet evolution.
It also proves the proper-prefix chronology---inactive projection, zero safe
correction, and one next-singleton admission at every prefix---for every
`m >= 64`, and hence the exact three-frontier changing-face source and its
factored Fourier transform in that range.  The chronology first reduces
exactly to one shared-coordinate sign:
if `D_n(j)=-r_n(p_n)(j)+(1-q)r_(n-1)(p_(n-1))(j)/2 >= 0`, then raw
positivity, nonpositive post-step residual, zero correction, and strict next
admission all follow with explicit rational slack. A reflected ideal-packet
split further writes `D_n` as an
explicit nonnegative binomial contribution plus one correction difference.
The correction obeys a closed residual-only moving-frontier recurrence. Its
temporal Green kernel is exactly coefficientwise nonnegative, and the
constant-source derivative trace has a positive infinite-sum generating
series. The all-prefix `q -> 0` correction generating function is also solved
coefficientwise and has sharp uniform shared-coordinate half-difference margin
`1/80`. An exact rescaling makes the finite-`q` homogeneous recurrence equal
to the `q=0` recurrence. A stopped-binomial-kernel bound, total-variation
control of the derivative source, a sharp mass bound, and the exact initial
response preserve margin `179/14400` from prefix six onward; a separate
analytic perturbation handles prefixes two through five. The growing-band
position profile is proved for all sufficiently large `m`. Its exact
five-piece decomposition has uniform base and endpoint remainders `o(q^2)`;
the three limiting absolute constants admit the rational upper ledger
`257/92160<1/256`. The proof includes the finite constant-`U` Chebyshev sum
and the cancellation that makes the final degree-one endpoint term `O(q^3)`.
It also gives exact nonnegative position/velocity propagators. A uniform
continuum limit for the velocity trace retains the cancellation among the
homogeneous base, derivative sources, and final endpoint. Rational
total-variation bounds give the strict ledger
`3479/14400<1/4`, proving the growing-band velocity profile as well. It then
proves a conditional anti-cancellation theorem: the two proved entry profiles
and projection/envelope regime preservation would force
`Omega(q^-1 log(1/q))` terminal steps for the named transported-center
execution.

The terminal projection/envelope regime is not proved. A deterministic NumPy
screen reconstructs
the actual admission trajectory, measures the packet and modal defects, checks
the sharpened profiles and projection/envelope margins, verifies the exact
velocity identity, and reports both the first range crossing and the first
literal safe-envelope certificate. A rational-arithmetic preflight separately
checks the source support, every displayed boundary entry, and the formal
Laurent-polynomial transform identity at representative prefixes along the
now-proved replay. A second rational preflight checks the new
frontier constants, shared/frontier residual identities, post-residual
identity, and finite shared-sign replay at `m=8,12`. A third exact preflight checks the ideal/correction
recurrence and signed source triplet, the positive Green identity, and the
exact leading-order correction formulas through prefix 256. A fourth exact
preflight checks the finite-`q` source constants, stopped derivative-prefix
bound `[-4,4]`, early-prefix ledger, and final `179/14400` margin. A fifth
preflight checks the exact rational position ledger and the finite
constant-`U` Chebyshev response. A sixth preflight checks the rational
velocity total-variation ledger and the continuum normalization. The sole
remaining theorem interface is the nonlinear terminal regime.
Numerical observations are labeled
**Measured**, not promoted to an asymptotic theorem or a lower bound for other
algorithms.

Build with `make`. Run the screen with:

```bash
python3 verify.py 128 256 512 1024
```
