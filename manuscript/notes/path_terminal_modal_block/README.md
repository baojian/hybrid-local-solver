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
analytic perturbation handles prefixes two through five. The remaining
entry-profile problem also contains the final
degree-one endpoint term.
It also gives exact nonnegative position/velocity propagators.  A directed
half-endpoint split of the ideal packet now retains the literal outward entry
momentum: the two directed binomial waves remain nonpositive for all time.
The actual entry position correction is proved coordinatewise nonpositive,
and the folded velocity kernel has exact maximum coefficient at most
`1+(k-1)/(2m)`.  Consequently all positive residual is reduced to the
degree-weighted positive mass of one static directed-velocity remainder; the
damping makes the apparent factor-`k` and repeated-reflection losses uniformly
bounded. The remainder is further deconvolved exactly as `u=Ld`, with `d`
given directly by the final proper-prefix state and a lower binomial packet;
the early `J_kL` kernel is an explicit binomial window. It then proves a conditional
anti-cancellation theorem: two quantified entry
position/velocity profile bounds plus projection/envelope regime preservation
would force `Omega(q^-1 log(1/q))` terminal steps for the named
transported-center execution.

The two entry profiles and the terminal projection/envelope regime are not
proved. On the regime side, the signed static mass is now bounded by
`3q^3/50`, while the endpoint coefficient lies in `(-57/200,0)`. An exact
geometric endpoint comparator reduces the full `21q^3/80` static target to
coordinatewise tail dominance `d>=h`, and a concrete local sufficient route
is the half-ratio family `E_1>=0`, `F_2>=E_1/2`,
`F_r>=F_(r-1)/2`. An exact correction identity also writes the interior
tail difference as `d=2(1-q)L((1-q)K_(m-1)-K_m)` and gives the seed identity
with the endpoint atom cancelled. Thus another sufficient route is an
interior temporal preimage comparison plus three direct frontier rows and
the seed. Positivity of that preimage is neither claimed nor necessary, and
fixed-prefix `q->0` asymptotics do not settle the joint family `mq=1/16`.
Those local inequalities remain open, as do the early
convolution analogue and an early/late lower position margin. A further exact
simplification makes the half-ratios the two-step spatial cone
`d_j>=d_(j+2)/4`, with two endpoint initial conditions. On rows through
`m-6`, the cone has an exact folded-source ledger with a base term, the
`epsilon_n(1,2,-3)/4` derivative packets, and newest-row masses
`mu_n=-q nu_n`; the scalar window `2/5<nu_n<43/75` is proved. The mass
folded-kernel estimate is also proved by an exact binomial maximum principle,
finite dyadic certificate, and entropy tail. The base and derivative
folded-kernel estimates and five direct frontier rows remain open. The
original proposed derivative constant `-q/16` is now rigorously ruled out by
an exact fixed-distance asymptotic at distance seven; the weaker sufficient target `-q/8`
replaces it. A
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
static `u=Ld` reduction at `m=8,12`. The remaining
entry-profile problem is a sharp signed summation of the source traces, not
their support calculation. Numerical observations are labeled
**Measured**, not promoted to an asymptotic theorem or a lower bound for other
algorithms.

Build with `make`. Run the screen with:

```bash
python3 verify.py 128 256 512 1024
```
