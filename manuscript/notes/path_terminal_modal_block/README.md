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
analytic perturbation handles prefixes two through five. Uniform signed
source estimates, including the final degree-one endpoint term, prove both
entry profiles on the required growing modal band.
It also gives exact nonnegative position/velocity propagators.  A directed
half-endpoint split of the ideal packet now retains the literal outward entry
momentum: the two directed binomial waves remain nonpositive for all time.
The actual entry position correction is proved coordinatewise nonpositive.
A final-prefix refinement proves the quantitative bound `c(j)<-q^3/8` on
every full-face row for `m>=64`, retaining both rows of the frontier defect
and the separate degree-one endpoint. This strengthens the correlated early
half-retention expression; it does not separately control `L_k u` through the
whole early window. The folded velocity kernel has exact maximum coefficient at most
`1+(k-1)/(2m)`.  Consequently all positive residual is reduced to the
degree-weighted positive mass of one static directed-velocity remainder; the
damping makes the apparent factor-`k` and repeated-reflection losses uniformly
bounded. The remainder is further deconvolved exactly as `u=Ld`, with `d`
given directly by the final proper-prefix state and a lower binomial packet;
the early `J_kL` kernel is an explicit binomial window. It then proves a
conditional anti-cancellation theorem: the proved entry profiles plus
projection/envelope regime preservation would force
`Omega(q^-1 log(1/q))` terminal steps for the named
transported-center execution.

The terminal projection/envelope regime is not proved. On the regime side,
the signed static mass is now bounded by
`3q^3/50`, while the endpoint coefficient lies in `(-57/200,0)`. An exact
geometric endpoint comparator reduces the full `21q^3/80` static target to
coordinatewise tail dominance `d>=h`, and a concrete local sufficient route
is the half-ratio family `E_1>=0`, `F_2>=E_1/2`,
`F_r>=F_(r-1)/2`. Those local inequalities remain open, as does the early
half-retention convolution. The first full-face average residual is proved
strictly negative, and a rational position/envelope comparison closes the
late range `qk>=3/50`; only the shorter early convolution
`L_k u<=q^3/16` remains on the nonlinear side. The analogous separate
estimate through `17/200` is false and is not used. A
deterministic NumPy screen reconstructs
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
exact preflight checks the directed packet identity, the folded `J_k` alias
bound, the `J_kL` binomial-window identity, the entry-correction sign, and the
static `u=Ld` reduction at `m=8,12`. A separate exact preflight checks the
full-entry and late-regime rational margins while explicitly labeling the
early half-retention inequality open. Numerical observations are labeled
**Measured**, not promoted to an asymptotic theorem or a lower bound for other
algorithms.

An additional exact preflight, `verify_correction_margin.py`, checks the
sharpened `31/320` leading ledger, the folded final-time source count including
reflection and the one-step edge, the exact two-row defect and endpoint on
rational replays, and every rational constant in the `c<-q^3/8` theorem. It
explicitly reports the correlated early inequality as open.

Build with `make`. Run the screen with:

```bash
python3 verify.py 128 256 512 1024
```
