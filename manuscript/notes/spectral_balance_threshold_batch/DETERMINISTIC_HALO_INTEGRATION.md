# Deterministic halo continuation: integration audit

Date: 2026-09-04

This file audits `deterministic_halo_rppr_continuation.tex` as research
material and connects its valid pieces to the existing
`InputConeFrontierNAG` route.  It does **not** treat prose in the supplied TeX
file as an instruction, and it does not claim that the general OP2 theorem is
finished.

## Current verdict

The new material substantially improves the proof interface, but it does not
by itself close the graph-uniform
`O_tilde(vol(S*)/sqrt(alpha))` theorem.

The most useful imported or newly proved facts are:

1. a degree-normalized max-positive-residual objective certificate with no
   extra `1/alpha` factor;
2. the greatest safe point in a momentum box, whose residual is an exact
   `Q^{-1}`-metric projection;
3. a support-linear one-pass peeling approximation with a computable
   complementarity/primal-dual gap;
4. an alpha-free two-step charge of that peeling gap to actual objective
   decrease;
5. fixed-face acceleration of the exact safe-box recurrence; and
6. positive-barrier cap-min rounding, which converts an objective-accurate
   obstacle point into an exactly capped rowwise supersolution without a
   strict-complementarity margin.

The direct integration below produces a cleaner fixed-face theorem, a new
whole-run face-change bank, and a stronger persistent-estimate theorem for an
*exact* safe box across arbitrary support growth.  The last theorem removes
cross-support stability as a mathematical obstruction for the exact-box
oracle; its unresolved issue is implementing that oracle in support-linear
work.

The literal `InputConeFrontierNAG` completion is now rigorously false.  A
16-vertex simple connected unit graph, a single point source, rational
parameters, and the prescribed zero initialization reach a strictly negative
masked input residual while the preceding inner width is still strictly above
the stated quarter-width stopping threshold.  The active residual push and
the maximal append-push closure are both enabled, so this is a counterexample
to `StoppedMaskedInputResidual` itself, not merely to an arbitrary supplied
state or a weakened implementation.  A second exact 20-vertex zero-start
example shows that omitting those pushes fails even more directly.

The number `1/4` is not essential to the outer bracket argument.  If a fixed
`beta<1/2` replaces it and the input cone holds on every product executed
before `inner_width<=beta old_width`, the new bracket contracts by
`1/2+beta<1`; the same partial-gradient proof would still give the target up
to a `beta`-dependent constant.  A second Fraction-exact canonical trace on a
24-vertex graph refutes both `beta=1/3` and `beta=2/5`: the corresponding
first negative inputs have predecessor ratios `0.373214...` and `0.415110...`.
These facts are not monotone in beta: changing an earlier stop changes all
later phase centers.  After replacing the invalid monotone inference by exact
same-chronology cells, a 44-trace Fraction atlas with corroborating exact
eight- through twenty-two-leaf zero-root audits now proves continuous
counterexample coverage for every

```text
0<beta<0.4897917473484638....
```

A positive completion must therefore use one fixed beta in the remaining
interval up to `1/2`; a global refutation must extend the cell cover through
that interval.

A canonical two-vertex zero-start family separately proves that the direct
one-pass `PeelingLC` substitute needs `Omega(alpha^(-1))` rounds even for a
constant-factor objective reduction.  Its max-residual stopping rule needs
`Omega(alpha^(-1) log(1/alpha))` rounds at a fixed relative target.  Natural
repetition does not repair it: a second zero-start unit-edge family forces
`Omega(alpha^(-1))` total peeling passes when every outer trial repeats the
pass until the exact `ABoxStop` certificate accepts, while the objective gap
is still above a fixed fraction of its initial value.  Other
tempting deterministic repairs also have exact stops: a reset safe-box input
correction, a global scalar retraction, delayed safe-prox response charging,
and a local conditional-expectation rule for accelerated coordinate descent
all fail at their claimed proof interface.  Their supplied-state examples are
not additional zero-start lower bounds.

## 1. Degree-normalized stopping certificate

Let

```text
phi(x)=x^T Q x/2-c^T x,       x>=0,
Q h=alpha h,                  h_i=sqrt(d_i),
```

and let `x*` be the obstacle minimizer.  If `0<=L<=x*` and
`r=c-QL`, then

```text
phi(L)-phi(x*) <= (1/2) max_i [r_i]_+/h_i.       (MaxResidual)
```

Indeed, with `d=x*-L`, complementarity gives

```text
2(phi(L)-phi(x*))=d^TQd=d^Tr.
```

The unregularized point-source solution `x_0=Q^{-1}b` satisfies
`0<=x*<=x_0` and `h^T x_0=1`.  Therefore

```text
d^Tr <= max_i [r_i]_+/h_i * h^Td <= max_i [r_i]_+/h_i.
```

For a vector supported on a scanned core, a positive residual can occur only
on the core or its one-hop boundary.  The certificate is therefore local.
This is a useful replacement for accuracy conversions that lose a factor
`1/alpha`.

The support-radius theorem in the supplied note is also valid after adding
the standard nonempty-support qualification `rho<1/d_v` (otherwise the
distance statement is vacuous).  Chebyshev inverse decay gives

```text
dist(v,i)=O(alpha^{-1/2} log(1/(alpha rho)))
```

for every `i in S*`.  This controls graph distance, not the number of
same-distance safe-pivot waves, and so it is not a work proof by itself.

## 2. Direct safe-box gradient recurrence

The safe-box result becomes especially transparent when it is applied to the
original gradient recurrence rather than only to the outer proximal method.
The following fixed-face theorem is the main positive integration result.

Let `B` be a symmetric positive-definite Stieltjes matrix with

```text
mu I <= B <= L I,
```

and consider `f(x)=x^TBx/2-b^Tx` on a fixed positive face, with
`x*=B^{-1}b>0`.  Put

```text
s=sqrt(mu/L),       theta=(1-s)/(1+s),       R=I-B/L.
```

Assume `x_(k-1)<=x_k` are lower subsolutions.  Form the raw trial

```text
y_k=x_k+theta(x_k-x_(k-1)).
```

Let `q_k` be the greatest subsolution in the box `[x_k,y_k]`.  Equivalently,
if `hat t_k=b-By_k`, its safe residual is

```text
t_k=b-Bq_k=Proj_(R_+)^(B^{-1})(hat t_k).
```

Take the one-step smooth update

```text
x_(k+1)=q_k+t_k/L.
```

Because `R` is entrywise nonnegative, `x_(k+1)` is again a lower
subsolution.  On a fixed face,

```text
b-Bx_(k+1)=R t_k,
```

and hence

```text
t_(k+1)
 =Proj_(R_+)^(B^{-1})
    (R((1+theta)t_k-theta t_(k-1))).              (ResidualAPG)
```

This is exactly accelerated projected gradient, in the `B^{-1}` inner
product, for

```text
Psi(t)=||t||_2^2/(2L)+indicator_(t>=0).
```

The metric gradient of the smooth part is `Bt/L`, so its unit gradient map is
`R`.  Its metric spectrum is `spec(B/L) subset [mu/L,1]`.  Thus the standard
strongly-convex APG estimate gives

```text
Psi(t_k)
 <= (1-s)^k (Psi(t_0)+(1/2)||t_0||_(B^{-1})^2)
 <= (1-s)^k (1+L/mu)Psi(t_0).                    (FixedFaceResidualRate)
```

The max-residual certificate converts this directly into objective accuracy:

```text
f(q_k)-f(x*) <= (1/2) max_i (t_k)_i/h_i
              <= sqrt(L Psi(t_k)/2).
```

Consequently the exact safe-box gradient recurrence has the desired
`O(sqrt(L/mu) log(poly(L/mu)/epsilon))` product count on every fixed positive
face.  This proof uses neither a complementarity margin nor the ordinary
primal estimate potential.

For RPPR, `B=Q`, `L=1`, and `mu=alpha`.  For the shifted prox phase used in
the retained construction, `B=Q+alpha I`, `L=1+alpha`, and `mu=2alpha`.
Thus the fixed-face root is exactly the root already used by
`InputConeFrontierNAG`.

### 2.1 Persistent estimate state closes exact-box support changes

There is a stronger way to use the greatest safe box.  The earlier
counterexample resets the estimate state so that the next extrapolate again
has the ordinary two-primal-iterate formula.  Keeping the linear-coupling
estimate state instead makes exact clipping compatible with the usual
accelerated potential, even while the support grows.

Let `B` be Stieltjes with `mu I<=B<=L I`, let `x*` be the obstacle
minimizer, and let `s=sqrt(mu/L)`.  Suppose `x` is a lower subsolution,
`x<=z`, and `x,z` have the same certified support `S`.  Put

```text
y=(x+s z)/(1+s)
```

and let `w` be the exact greatest safe point in the box `[x,y]` on `S`.
Admit every exterior row on which the full gradient at `w` is negative, call
the enlarged face `A`, and define `g` to equal the full gradient on `A` and
zero elsewhere.  Then `g_A<=0` and every omitted gradient is nonnegative.
Make the linear-coupling update

```text
x^+=w-g/L,
z^+=(1-s)z+s w-(s/mu)g.                         (SafeBoxLC)
```

Then `x^+` is again a lower subsolution, `x^+<=z^+`, both new states have
the same safe support, and

```text
E(x^+,z^+) <= (1-s)E(x,z),
E(x,z):=f(x)-f(x*)+(mu/2)||z-x*||_2^2.           (ExactBoxLC)
```

Here is the complete argument.  If `t=-g_A>=0`, then on `A`

```text
c-Bx^+=(I-B_AA/L)t>=0,
```

because `I-B_AA/L` is entrywise nonnegative.  Thus comparison gives
`x^+<=x*`.  Also

```text
z^+-x^+=(1-s)(z-w-g/(sL))>=0.
```

This proves the order and support invariants.  Smooth descent, the global
strong-convexity model with the nonnegative omitted gradient terms deleted,
and exact expansion of the estimate update give

```text
E(x^+,z^+)
 <=(1-s){E(x,z)+f(w)-f(x)
          -s<g,z-w>-(s mu/2)||z-w||_2^2}.        (LCBridge)
```

The exact safe box has `e=y-w>=0`, `t=c-Bw>=0` on `S`, and `e^Tt=0`, so
`<g,y-w>=0`.  Since `s(z-y)=y-x`,

```text
s<g,z-w>=<g,y-x>=<g,w-x>.
```

Quadratic expansion at `w` now yields

```text
f(w)-f(x)-s<g,z-w>=-(1/2)||w-x||_B^2<=0,
```

which proves `ExactBoxLC`.  Notice that the proof explicitly allows a strict
subset of the final support and arbitrary safe frontier admissions; no
moving-face error appears.

This gives a complete deterministic accelerated *outer-product/oracle-call*
theorem for the original RPPR objective: with `mu=alpha`, `L=1`, the
max-positive-residual
certificate is reached in
`O(alpha^(-1/2) log(poly(1/alpha,1/epsilon)))` products.  It is not yet the
desired sparse-work theorem, because an exact greatest-safe-box LCP is not
known to cost one support-linear pass per product.  Solving that LCP from
scratch by an inner accelerated method would reintroduce a second
`alpha^(-1/2)` factor.

For the one-pass peeling point, put `e=y-w`, `t=c-Bw` on the old support and
`zeta=e^Tt`.  The same proof, now using `<g,y-w>=-zeta`, gives the exact
inexact inequality

```text
E(x^+,z^+)
 <=(1-s)E(x,z)+(1-s^2)zeta
   -(1-s){(1/2)||w-x||_B^2
           +(s mu/2)||z-w||_2^2}.                (PeelingLC)
```

Thus the coefficient of the computable peeling gap is universal and the
negative credits are explicit.  This is a sharper completion interface than
treating support changes as arbitrary perturbations.  The script
`safe_box_linear_coupling_experiment.py` audits both `ExactBoxLC` and
`PeelingLC` on deterministic graph families.

The additive term cannot simply be deleted.  On the canonical unit-edge
RPPR objective with `alpha=1/900` and `rho=1/100`, there is a rational safe
state for which one peeling pass increases the linear-coupling energy by

```text
E^+/E=993574003022/990625448701 > 1.
```

The state and every update are checked in
`peeling_lc_counterexample_exact.py`.  It is not asserted reachable from the
zero-start chronology.  Thus `PeelingLCAbsorption` may still exploit
reachability or a block ledger, but a generic per-step contraction theorem
for one-pass peeling is false even on a canonical point-source objective.

### 2.1.1 A certified approximate-box interface and a persistence stop

Exact complementarity is stronger than the outer proof needs.  At a
SafeBoxLC round, write

```text
hat_t=c_S-B_SS y_S,       u=y_S-x_S.
```

Suppose an inner routine returns an exactly feasible primal--dual pair

```text
0<=e<=u,       t=hat_t+B_SS e>=0,       zeta=e^Tt,
w=y-e.
```

The same linear-coupling calculation gives

```text
E(x+,z+) <= (1-s)E(x,z)+(1-s^2)zeta-(1-s)A,
A=(1/2)||w-x||_B^2+(s mu/2)||z-w||_2^2.          (CertifiedABox)
```

Consequently the fully local test

```text
(1+s)zeta<=A                                             (ABoxStop)
```

preserves the exact `1-s` contraction.  Also

```text
(1/2)||e-e_box||_B^2<=zeta,
```

so this is an actual LCP primal--dual certificate, not a heuristic inner
tolerance.  One peeling pass supplies a feasible initial pair in
support-linear work, although the two- and five-vertex slow families show
that it cannot always satisfy `ABoxStop` without refinement.

The natural insertion-only refinement is rigorously false even when the
graph support and Hessian never change.  On the canonical unit triangle with
`alpha=1/9`, source zero, and `rho=1/14`, one genuine positive-state
SafeBoxLC trajectory has exact correction-positive sets

```text
{0,1}, {0}, empty, {2}, {0,1,2}.
```

The first exact correction is infeasible for the second inner right-hand
side.  Any second-round feasible correction constrained to dominate the
first one coordinatewise has certified gap at least

```text
2269/373248
```

before the common trajectory scaling.  Thus correction faces can both delete
and insert coordinates between two fixed-support outer rounds.  A persistent
implementation must permit signed recycling or maintain a reusable spectral
response; graph-support events and a nonnegative correction accumulator do
not suffice.  This is not a lower bound against every dynamic LCP method.
The exact result and verifier are
`APPROXIMATE_SAFE_BOX_MAINTENANCE_AUDIT.md` and
`safe_box_lc_rhs_nonmonotonicity_exact.py`.

Restarting the one-pass peel repeatedly toward the same trial is also not a
constant- or polylog-pass implementation of `ABoxStop`.  On the canonical
single unit edge, put `s=1/m`, `alpha=s^2`, source zero, and `rho=1/4`.
There is an explicit strictly positive supplied SafeBoxLC state for which the
first `m/32` repeated peeling passes all obey

```text
(1+s)zeta_k>A_k.
```

Every pass has exactly two rational event times.  The construction scales its
residual and trial correction by `eta=s^3`, so it embeds without changing the
canonical point-source load, and its exact recurrence keeps the stopping
ratio above `1.41` through the certified horizon at `m=4096`.  Thus a single
fixed-support outer round can require
`Omega(alpha^(-1/2))` restarted peeling passes merely to recover the exact
outer contraction certificate.  The state is not proved reachable from the
zero-start SafeBoxLC history, and one such inner episode can still fit inside
the *total* target budget; the result rules out only per-round
constant/polylog refinement, not global amortization or signed response
recycling.  See `ITERATED_PEELING_ABOX_ROOT_OBSTRUCTION.md` and
`iterated_peeling_abox_root_obstruction_exact.py`.

Global amortization does not rescue this literal restarted procedure.  Take
the same unit edge with source zero, now with

```text
s=1/m,       alpha=s^2,       rho=1/2-s,
```

and start `SafeBoxLC` from its prescribed zero state.  After the first two
outer updates the full-support state has the exact projective form

```text
c-Qx=R(1,1),       z-x=(V,W),
kappa=R/(s^2V)->2,       r=W/V->0.
```

For every subsequent accepted repeated-peeling episode in the compact
region `1.8<=kappa<=2.5`, `0<=r<=0.55`, the second coordinate must be
completely exhausted.  If `gamma` denotes the remaining distance to the
exact box in units of `s^2V`, `ABoxStop` gives the uniform one-sided control

```text
0<=gamma<=(1+r^2)/(1-r)+O(s).
```

Direct substitution, without an exact-output or ODE assumption, yields a
controlled rational recurrence with

```text
1 <=(r^+-r)/s<=5.1,
-0.65 <=(kappa^+-kappa)/s<=4.
```

It follows from the exact zero-start boundary state that there are
`Omega(1/s)` genuine outer rounds with `r>=0.05`.  During each such round a
single pass moves the exhausted coordinate by at most `40s^2V`, whereas
acceptance requires total movement at least `0.049sV`.  Hence those rounds
perform `Omega(1/s)` passes apiece and

```text
total passes=Omega(1/s^2)=Omega(1/alpha).
```

Throughout this prefix the exact objective gap remains above one quarter of
the initial gap.  This is a whole-run canonical zero-start lower bound for
the specifically named “restart peeling until `ABoxStop`” implementation;
it is not a lower bound against a signed persistent LCP response or an exact
box oracle.  The proof and exact finite checks are in
`ZERO_START_REPEATED_PEELING_WHOLE_RUN_OBSTRUCTION.md` and
`zero_start_repeated_peeling_exact.py`.

There is nevertheless a finite generic fixed-support bound.  If `N`
successive repeated outputs all fail `ABoxStop`, the residual-at-freeze
identity, failure inequality, and coordinatewise telescoping imply

```text
N<min{(1+s)sqrt(|S|)/s,(1+s)^2/s^2}.             (RepeatedPeelBound)
```

Thus the two-vertex family is tight in its `alpha^(-1/2)` dependence at fixed
dimension.  The upper bound is still too large to charge independently at
every accelerated outer product, and the zero-start construction above shows
that a whole-run movement amortization of literal restarted peeling is also
false.  The bound remains useful only for diagnosing one inner episode or
for an algorithm with a genuinely persistent signed response state.

### 2.2 A persistent slow ray for one-pass peeling

The obstruction is stronger than an isolated energy increase.  There is a
canonical five-vertex graph on which the one-pass `PeelingLC` map has a
persistent invariant ray with contraction (1-\Theta(\alpha)).  The graph is

```text
E={03,04,13,14,23,24,34},   source=3,   d=(2,2,2,4,4).
```

Take (\rho d_3=1/5), put (s=\sqrt\alpha), and restrict to the symmetric
subspace in which vertices (0,1,2) agree.  If the leaf coordinate is
rescaled by (\sqrt2), the operator on the three orbits (leaf, source, other
hub) is

```text
              [ D       -b/2    -b/2 ]
B_hat(s) =    [ -3b/4    D      -b/4 ],
              [ -3b/4   -b/4     D   ]
D=(1+s^2)/2,  b=(1-s^2)/2.
```

Write the primal error and estimate displacement as

```text
a=x*-x,        v=z-x,        d=s v/(1+s).
```

In the stable event pattern the source is the unique coordinate frozen
during the peeling pass, at time `tau`, so

```text
u=(d_leaf,tau d_source,d_other),       t=B_hat a-B_hat u,
a^+=a-u-t,       v^+=(1-s)(v-u+t/s).                 (SlowRayMap)
```

There is an analytic positive branch of invariant rays

```text
(a^+,v^+)=lambda(s)(a,v)
```

for all sufficiently small positive (s), with

```text
lambda(s)=1-7s^2+49s^3+O(s^4),
tau(s)=s+2s^2+O(s^3).                              (SlowRayRate)
```

Here is a short exact derivation.  Normalize the source error to one and
write

```text
a=(X,1,J),       v=(sP,H,sR),
lambda=1-cs^2,   tau=eta s.
```

The invariant equations imply

```text
u+t=cs^2 a,
t=s u + s^2 (1-cs)/(1-s) v.
```

The leaf and other-hub equations solve rationally for (X) and (J) near
((s,c,\eta)=(0,7,1)).  Substitution into the source equation and the
source-freezing equation, followed only by clearing nonzero denominators,
gives two analytic equations whose constant terms in (s) are

```text
F(c,eta,0)=5(2c-7eta-7),
G(c,eta,0)=5(c-7)(eta+1).
```

The positive solution is ((c,\eta)=(7,1)), and its Jacobian is

```text
[[10,-35],
 [10,  0]],       det=350.
```

The analytic implicit-function theorem therefore supplies a unique local
branch.  Expanding its equations by one more order gives

```text
c=7-49s+O(s^2),       eta=1+2s+O(s^2),
X=1-(13/10)s^2+O(s^3),
J=1-(21/10)s^2+O(s^3),
v=(7s+O(s^2), 7/2+O(s), 7s+O(s^2)),
t=(14s^3+O(s^4), (7/2)s^2+O(s^3), 14s^3+O(s^4)).
```

All three final slacks are strictly positive for small (s).  Before the
first event, the residual and pressure have leading terms

```text
B_hat a = (7/8,7/4,7/16)s^2+O(s^3),
B_hat d = (-7/8,7/4,-7/16)s+O(s^2).
```

Thus only the source slack initially decreases, and it reaches zero at
`tau=s+O(s^2)`.  After it freezes, the two remaining slacks decrease
linearly to the displayed positive (14s^3+O(s^4)) endpoints.  Hence the
assumed event pattern is the actual peeling pass, not an extraneous algebraic
branch.

For this point-source objective the unconstrained solution is strictly
positive when (s) is small, so it is also the obstacle optimum.  Scale the
ray by a sufficiently small constant and set

```text
x=x*-kappa a,       z=x+kappa v.
```

Then (x) is a positive lower subsolution, (x\le z), and every subsequent
peeling state remains on the same ray.  Reducing its positive-residual
certificate by any fixed factor requires

```text
Omega(1/(1-lambda))=Omega(1/alpha)
```

rounds.  Consequently a graph-uniform `PeelingLCAbsorption` theorem valid
from every admissible safe state is false.  Any surviving theorem for this
one-pass map would have to use a special zero-start reachability invariant.

The zero-start chronology itself shows the same tail numerically.  At
relative certificate tolerance (10^{-2}), exact-box versus peeling round
counts for

```text
alpha       .03   .01   .003   .001   .0003   .0001
exact box     35    70    138    246      456      795
peeling       35    71    373   1052     3317     9615
```

have `sqrt(alpha) * exact_box_rounds` approaching (8), while
`alpha * peeling_rounds` stays near (1).  The stable projective ray is
locally attracting in all tested cases, but an analytic attraction proof
from the zero initialization is not claimed.  The complete deterministic
audit is `peeling_lc_symmetric_obstruction.py`.  The independent symbolic
certificate `peeling_lc_symmetric_ray_exact.py` performs the rational
elimination, checks the two limiting equations, verifies the implicit-function
Jacobian determinant `350`, and derives `c'(0)=-49`, `eta'(0)=2` without
using the floating-point ray solver.

### 2.3 A canonical zero-start two-vertex lower bound

The zero-start qualification does not rescue the direct one-pass
`PeelingLC` recurrence.  Put `s=sqrt(alpha)` and use the single unit edge with
source zero and

```text
rho=1/2-s,
Q=[[d,-b],[-b,d]],       d=(1+s^2)/2, b=(1-s^2)/2,
c=s^2(1/2+s,-1/2+s).
```

The exact optimum is `(s+s^2/2,s-s^2/2)>0`.  Starting from `x=z=0`, the
first product admits the source and the second product admits the other
vertex with exterior residual `s^3(3/2-s)>0`.  At that point, exactly

```text
x*-x=A(1,1),
A=s-s^2/2-3s^3/2+s^4,
z-x=A(p,sy),             p->1/2, y->3/2.
```

Every later pass has the same event word: coordinate zero freezes first and
coordinate one completes its move.  To see this without an attraction
assumption, let

```text
K_s={1/4<=p<=4, 1<=y<=4+8s/p}.
```

The exact reduced map has, after removal of powers of `s`, the boundary
limits

```text
(p^+-p)/s -> y/2-p,             y^+ -> 2+y/2,
[p^+(y^+-4)-8s]/s -> -6p        on y=4+8s/p.
```

The final source slack divided by `s^2` tends to `y/2`; the other final
slack is decreasing in `y` and, on the curved upper boundary, its ratio to
`s^3` tends to `2`.  These strict compact boundary signs show that `K_s` is
forward invariant and that the asserted event word is valid for all
sufficiently small `s`.  The explicit state after product two lies in `K_s`.

If the accepted increment divided by `A` is `(U,V)`, then

```text
D=dp-bsy,      U=s^2p/D,      V=s^2y/(1+s),
A^+/A=1-s^2-b(U+V).
```

On `K_s`, `p/D` and `y/(1+s)` are uniformly bounded.  Hence, for one
absolute `C`,

```text
A^+/A>=1-C s^2.
```

The objective gap and local stopping certificate are exactly

```text
f(x)-f(x*)=s^2 A^2,       Delta=s^2A/2,
f(0)-f(x*)=5s^4/4.
```

Since `A_2/s -> 1`, a fixed-factor objective reduction already needs
`Omega(s^(-2))=Omega(alpha^(-1))` products.  At a fixed relative target for
the displayed max-residual rule, taking
`N=(4C)^(-1)s^(-2)log(1/s)` leaves `A_N=Omega(s^(3/2))` and therefore
`Delta_N` above the target.  This stopping rule needs the stronger

```text
Omega(s^(-2) log(1/s))
 =Omega(alpha^(-1) log(1/alpha))
```

lower bound.  Both statements hold on this constant-volume canonical
zero-start family and rigorously refute `ZeroStartPeelingLCAbsorption` for
the recurrence as stated.

For diagnosis, the event map has an analytic slow projective ray.  Its
implicit-function Jacobian has determinant `1/2`, and

```text
p=2-4s+8s^2+O(s^3),       y=4-8s+52s^2+O(s^3),
lambda=1-4s^2+4s^3+O(s^4),
tau=s+5s^2+11s^3+O(s^4).
```

The theorem, including the invariant-domain proof, is in
`PEELING_LC_TWO_VERTEX_ZERO_START_OBSTRUCTION.md`.  The exact symbolic and
zero-start numerical reproducers are `peeling_lc_two_vertex_ray_exact.py`
and `peeling_lc_two_vertex_obstruction.py`.

## 3. One-pass peeling is an exact inexact-projection interface

Run the one-pass peeling construction from `x_k` toward `y_k` and write

```text
q_k^peel=x_k+u_k,
e_k=theta(x_k-x_(k-1))-u_k,
t_k=b-Bq_k^peel,
zeta_k=e_k^Tt_k.
```

Then `e_k>=0`, `t_k>=0`, and

```text
B^{-1}(t_k-hat t_k)=e_k.
```

For every `v>=0`,

```text
<t_k-hat t_k,t_k-v>_(B^{-1})
 =e_k^T(t_k-v)
 <=e_k^Tt_k=zeta_k.                              (ApproxProjectionVI)
```

Thus `zeta_k` is not merely a heuristic clipping score.  It is a rigorous
additive error for the metric projection in `ResidualAPG`, and it is locally
computable.

There is also a direct-gradient analogue of the new proximal two-step
identity.  Let

```text
x_(k+1)=q_k^peel+t_k/L,       d_k=x_k-x_(k-1).
```

Exact quadratic expansion gives

```text
f(x_(k-1))-f(x_(k+1))-zeta_k/theta
 =(1+1/theta)u_k^Tt_k
   +(1/2)||d_k+u_k||_B^2
   +||t_k||_2^2/L-||t_k||_B^2/(2L^2)
 >=0.                                                     (DirectTwoStepCharge)
```

Therefore

```text
zeta_k <= theta(f(x_(k-1))-f(x_(k+1))).
```

The coefficient has no `1/alpha`.  The symbolic scalar cancellation is
checked by `input_peeling_bridge_exact.py`; the vector statement follows
from the displayed quadratic expansions and `B<=LI`.

This closes the *accounting* of the one-pass approximation error.  In view of
`ExactBoxLC`, exact safe-box clipping and all support insertions do preserve
one common accelerated last-iterate potential.  What remains is to absorb the
one-pass `zeta` term (preferably together with the two displayed negative
credits) or to maintain the exact box incrementally in support-linear
amortized work.

### 3.1 The scalar debit is not a sufficient black-box interface

The alpha-free two-step charge is exact, but it cannot by itself yield the
needed constant-coefficient block absorption.  On any canonical full-support
single-source instance, let `Qh=alpha h` and take the valid safe-prox
trajectory

```text
x^k=x*-A_k h,       A_k=(1+alpha)^(-k)A_0,
w^k=x^k.
```

The safeguard deliberately discards the requested momentum.  It is feasible,
is followed by the exact proximal update, and satisfies every black-box fact
used by the proposed reduction.  Its gap and peeling debit are

```text
G_k=(alpha/2)A_k^2||h||^2,
zeta_k=2 theta alpha G_k,
zeta_k<=theta(G_(k-1)-G_(k+1)).
```

Over `M=ceil(c/sqrt(alpha))` steps,

```text
G_M/G_0=1-2c sqrt(alpha)+O(alpha),
sum zeta_k/G_0=2 theta c sqrt(alpha)+O(alpha).
```

Consequently any purported black-box estimate

```text
G_M<=q_0G_0+C sum zeta_k,       q_0<1,
```

forces `C=Omega(alpha^(-1/2))`; a polylogarithmically longer block still
forces a divergent coefficient.  Thus exact-safe-box APG, correction
feasibility, `zeta`, and the two-step charge do not logically imply the
desired block theorem.  A proof must additionally use the oriented peeling
events, a quantitative accepted-momentum invariant, or the negative terms
discarded from `PeelingLC`.

This is a proof-interface obstruction, not a counterexample to the literal
exact-prox peeling/envelope algorithm: the displayed reset is not its peeling
point.  In fact a fixed-face geometric slow ray is impossible for the
two-primal exact-prox peeling map.  On such a ray, the requested momentum is
parallel to the current error and remains safe; peeling accepts it exactly,
and the rate obeys the ordinary accelerated characteristic polynomial.  A
negative example for that distinct method must therefore be time-varying or
use face growth.  The complete argument is in
`SAFE_PROX_BLOCK_STABILITY_OBSTRUCTION.md`.

### 3.1.1 A fixed-face residual proof does not paste across support entry

Face growth creates two exact breakpoint terms which a zero-extension of the
fixed-face residual state misses.  If `x^k` is an exact proximal point, its
global KKT residual has the decomposition

```text
c-Qx^k=bar_sigma^k-lambda^k,
bar_sigma^k>=0 on supp(x^k),       lambda^k>=0 off supp(x^k).
```

When the next support grows and the momentum parameter is `theta`, the raw
residual on the enlarged face is

```text
(1+theta)bar_sigma^k-theta zero_extend(bar_sigma^(k-1))
  +theta lambda^(k-1).                         (MultiplierInjection)
```

The last term can be strictly positive on a newly admitted coordinate.  It
is absent from the fixed-face recurrence.  Independently, if `S` grows to
`A=S union E`, block inversion gives

```text
(u,0)^T Q_AA^(-1)(u,0)
 >=u^T Q_SS^(-1)u,                              (MetricLift)
```

with a strict Schur-complement increase whenever the new block couples to
the component seen by `u`.

Both effects are strict on a canonical unit edge with source zero,
`alpha=1/99`, and `rho=1/3`.  The first proximal residual is

```text
(2/447,-17/14751)
 =(2/447,0)-(0,17/14751).
```

At the next full-support momentum trial the actual and zero-extended raw
residuals are respectively

```text
(307,4877)/1622610,
(307,3347)/1622610.
```

Both are already positive, so the actual safe-box clipping credit is exactly
zero although the multiplier injection is positive.  On the same example
the inverse metric of an old scalar jumps from `99/50` to `50`, a factor
`2500/99`.  Thus neither zero-appending the residual nor telescoping the
changing principal inverse metric closes the face breakpoint.  This is not a
global rate counterexample; a viable proof may instead keep the inactive
dual multiplier, use a full primal estimate sequence, or pay an explicit
support-discovery term.  The exact derivation is in
`EXACT_SAFE_PROX_SUPPORT_GROWTH_AUDIT.md`, with verifier
`exact_prox_support_lift_counterexample.py`.

### 3.2 The peeling debit is exactly paid edge-event variation

The literal exact-prox trajectory has a stronger invariant than the scalar
debit.  In one peeling pass let `tau_i in [0,theta]` be the freeze time,
put `f_i=theta-tau_i`, and, for an internal edge, set

```text
omega_ij=(-Q_ij)d_i d_j>=0.
```

The oriented replenishment identity is exactly

```text
zeta
 =sum_{ij} omega_ij max(f_i,f_j)|f_i-f_j|
 =(1/2)sum_{ij}omega_ij(f_i-f_j)^2
  +(1/2)sum_{ij}omega_ij|f_i^2-f_j^2|.           (FreezeGap)
```

If `F={i:tau_i<theta}` and

```text
V=sum_{ij}omega_ij|tau_i-tau_j|,
```

then the accepted-movement credit satisfies the second exact identity

```text
zeta+sum_(i in F) u_i t_i=theta V.               (FreezeCredit)
```

Keeping the `u^Tt` term in the exact two-step objective identity, instead of
discarding it when proving `DirectTwoStepCharge`, now yields for the literal
exact-prox sequence

```text
V_k<=G_(k-1)-G_(k+1),
sum_(k=m)^n V_k<=2(G_(m-1)-G_(n+1)),              (EventVariationBank)
```

with no graph or `alpha` factor.  This strictly refines the scalar
`sum zeta` bank: it pays the entire weighted spatial variation of every
freeze-time field.

The refinement does not by itself prove the rate.  Indeed arbitrary event
landscapes occur in one legal canonical all-safe pass.  On any fixed
connected unit graph choose `d=epsilon h` and any prescribed
`tau in [0,theta]^V`; for each row define

```text
z^(i)_j=epsilon min(tau_i,tau_j)h_j,
slack_i=(Qz^(i))_i>=epsilon alpha tau_i h_i.
```

For any sufficiently small `epsilon`, subtracting `Q^(-1)slack` from a
strictly positive canonical single-source optimum produces nested positive
subsolutions whose peeling pass realizes exactly those freeze times.  Thus
one cannot assume bounded event layers, spatial monotonicity, or a universal
Poincare inequality for a single pass.  A completion must use the
chronological response of the *next exact proximal calls* to the already paid
variation.  No counterexample to that literal envelope was found: the direct
five-vertex slow family and the tested growing-face graph families retain a
bounded `K sqrt(alpha)` and constant accelerated-block contraction through
the tested scales.  The proof, construction, and deterministic simulator are
in `SAFE_PROX_LITERAL_ENVELOPE_SECOND_PASS.md` and
`safe_prox_literal_envelope_audit.py`.

### 3.3 Positive next-step response does not absorb event variation

The hoped-for chronological completion through the next exact proximal
response has an exact positive-kernel representation but no state-uniform
linear energy charge.  If `w` is a subsolution, `p=P_1(w)`,
`r=p-w`, `t=c-Qw`, and `A=supp(p)`, then

```text
r_A=(I+Q_AA)^(-1)t_A,       r_(A^c)=0.            (PositiveResponse)
```

The principal Stieltjes inverse is entrywise nonnegative.  When peeling is
the selected safe-envelope center, `FreezeCredit` further gives

```text
V<=d_A^T(I+Q_AA)r_A<=2||d_A||_2||r_A||_2,
||r_A||_2^2>=V^2/(4||d_A||_2^2).                 (BilinearResponse)
```

This is sharp in the relevant scaling: it is quadratic rather than linear
in `V`.  The usual conversion to the available incoming `Q`-energy also
necessarily loses the desired root factor.  An all-safe canonical triangle
family for arbitrary `0<alpha<1` obeys

```text
V<=(constant)||d||_2||r||_2,
V/(||d||_Q||r||_2)>=4(1+alpha)/sqrt(30 alpha).
```

Thus an `alpha`-independent energy-norm bilinear bound is already false.
On the canonical unit triangle at `alpha=1/8`, source zero, and
`rho=1/100`, there is a one-parameter family of strictly positive all-safe
states, including a genuine preceding exact-prox transition, for which the
full ray/barrier/reflection/peeling envelope selects peeling and

```text
V=(7/8)delta^2 epsilon,
sum_(j>=k)(||r_(j+1)||_2^2+(1/2)||r_(j+1)||_Q^2)
 <=(2392409/20000)delta^2 epsilon^2.
```

Hence

```text
V / (whole future response energy)
 >=17500/(2392409 epsilon) -> infinity.
```

Allowing an accelerated-length block, or even the entire future, therefore
does not turn the already-paid event variation into a constant-coefficient
response-energy bank for arbitrary admissible states.  The state is not
proved reachable from the prescribed zero initialization, so a genuinely
historical invariant could still exclude it.  The exact construction and
verifier are in `SAFE_PROX_EVENT_RESPONSE_COUNTEREXAMPLE.md` and
`safe_prox_event_response_counterexample_exact.py`.

## 4. Support growth is a monotone inactive-slack injection

The single-source simplification gives an additional exact bank which is not
present in a generic obstacle problem.

For any monotone lower-subsolution sequence `x_(k-1)<=x_k<=x*`, define the
full signed residual and its positive/negative parts by

```text
g_k=b-Bx_k=p_k-n_k,
p_k=[g_k]_+,       n_k=[-g_k]_+.
```

The vector `n_k` is coordinatewise nonincreasing.  Once a coordinate is
positive in `x_k`, subsolution feasibility gives `(n_k)_i=0` forever.  If it
is still inactive, then its own increment is zero and

```text
(g_k-g_(k-1))_i=-(B(x_k-x_(k-1)))_i>=0
```

by the nonpositive off-diagonal entries.  Hence its negative slack can only
fall.

The raw momentum residual has the exact decomposition

```text
b-B(x_k+theta(x_k-x_(k-1)))
 =(1+theta)p_k-theta p_(k-1)
   +theta n_(k-1)-(1+theta)n_k.                  (SlackInjection)
```

The positive part of the face-change term satisfies

```text
[theta n_(k-1)-(1+theta)n_k]_+
 <=theta(n_(k-1)-n_k).                           (InjectionCharge)
```

For point-source RPPR, on every not-yet-active vertex of the final support,
the initial negative residual is at most `alpha rho h_i`.  Since
`vol(S*)<=1/rho`, the entire degree-weighted positive injection bank obeys

```text
sum_k h^T [theta n_(k-1)-(1+theta)n_k]_+
 <=theta h^Tn_0
 <=theta alpha rho vol(S*)
 <=theta alpha.                                  (PointSourceInjectionBank)
```

Coordinatewise, every injected residual is at most
`theta alpha rho h_i`.  The same statement applies across the shifted-prox
phases: at a phase center the proximal right-hand-side shift cancels the
diagonal shift, and on an inactive coordinate the old lower bracket is zero.

`safe_box_gradient_experiment.py` checks this decomposition and bank while
auditing the exact-box and peeling candidates.  This is a stronger and more
specific description of support changes than an arbitrary moving-face
path-length bound.  It uses exactly the point-source hypothesis emphasized in
the current problem definition.

The bank is not yet a last-iterate theorem.  Bounded total variation can be
placed late, and an accelerated recurrence is sensitive to recent impulses.
A completion must combine `PointSourceInjectionBank` with the local
max-residual stopping certificate, rather than simply discard the bank as a
fixed additive floor.

## 5. Exact obstruction to the naive InputCone completion

It is tempting to safeguard the ordinary NAG input, reset its estimate state
so that the physical convex-combination identity remains true, and invoke the
already proved `InputConeFrontierNAG` potential contraction.  That inference
is false for arbitrary safe states.

Let the graph be one unit edge, let

```text
alpha=9/100,       rho=1/100,       s=3/10,
Q=[[109,-91],[-91,109]]/200,
c=[alpha(1-rho),-alpha rho].
```

The exact optimum is `(107/200,89/200)`.  Take

```text
x=(19/50,13/50),       z=(29/50,27/100).
```

The current residual is `(3,303)/10000`, so `x` is a strict lower
subsolution and `x<=z`.  The ordinary NAG input is

```text
q=(277/650,341/1300)
```

with residual

```text
(-6189/260000,13011/260000).
```

The exact greatest-safe-box correction is `(6189/141700,0)`, giving

```text
q_safe=(4169/10900,341/1300),
c-Qq_safe=(0,171/5668).
```

After resetting the estimate state to realize `q_safe` and taking the usual
unit-smooth NAG step, the standard primal estimate potential has exact ratio

```text
E_next/E_old=161210/208081
             >7/10=1-s.
```

The witness is checked by
`input_safeguard_nag_counterexample_exact.py`.  It is a graph-derived,
point-source objective and uses only rational arithmetic.  The displayed
state is not claimed reachable from the canonical zero-start history, so it
does not refute `StoppedMaskedInputResidual`.  It does refute the generic
proof step

```text
safe-box input correction => no increase in the ordinary NAG potential.
```

The stopping qualifier also cannot be proved from matrix signs and a
nonnegative phase-start residual alone.  On the connected unit graph

```text
E={01,02,03,12},       d=(3,2,2,1),       s=3/10,
```

the normalized shifted RPPR matrix has diagonal `109/200` and row coupling
`91/(200d_i)`.  Starting a phase from zero with residual
`(4,1,128,32)`, the first pushed product gives next input residual

```text
(308749/8175,
 1494353/32700,
 -310303/1700400,
 13853693/850200).
```

Its positive residual width is exactly
`1494353/4185600>1/4` of the initial width, so the quarter rule executes a
second product even though its active input residual is already strictly
negative.  `stopped_input_cone_arbitrary_counterexample_exact.py` verifies
the fractions.  With RPPR `alpha=9/191`, point source zero, and
`rho=1/1000`, scaling this residual by `10^-6` embeds it exactly at a strictly
positive lower phase center `ell<x*`: the shifted load is
`c+alpha ell`, and its residual at `ell` is the scaled displayed vector.
Thus even the canonical point-source right-hand-side form and an arbitrary
valid lower phase center are insufficient.  Any successful
`StoppedMaskedInputResidual` induction must use reachability of that center
from the zero-start outer chronology, not only Stieltjes positivity,
nonnegative initialization, and the stopping guard.

### 5.1 The exact reduced cone map

The remaining reachability question can be written as a small positive-system
map.  Normalize the shifted matrix by its smoothness constant and write

```text
Bbar=B/L=d I-K,       R=I-Bbar=(1-d)I+K,
theta=(1-s)/(1+s),    kappa=s/(1+s),
```

where `K>=0` and the normalized diagonal `d` is constant.  At the start of an
executed product the clamp normal form is

```text
x=lower,        q=(x+s z)/(1+s),
m=L(q-x)>=0,    r=b_phase-Bq>=0.
```

Let `pi=Rr/d` be `L` times the simultaneous active diagonal-push increment,
and let `u>=0` be the residual left after that push and the maximal exterior
append closure.  On old active rows, and with zero momentum on newly admitted
rows, the next state is exactly

```text
m^+ = [theta(m+r)-kappa pi]_+,
r^+ = u-Bbar m^+.                                  (ReducedInputCone)
```

Without an append, `u=K pi`.  With append batches, `u` has the exact
chronological representation

```text
u_i=sum_(j:time(j)>=time(i)) K_ij pi_j,
```

where the active push is batch zero and every appended diagonal increment is
placed at its admission time.  Thus the open statement is precisely that the
canonical zero-start state makes `Bbar m^+<=u` on every product that the
quarter rule actually executes.

This formula also shows why chronological flux *alone* is not the missing
invariant.  On the three-vertex path `0-2-1`, at `s=1/10`, take batch times
`(1,0,0)` and nonnegative increments

```text
pi_old=(20/99,20/99,200/99).
```

They generate the valid chronological residual `r=(0,1,1/10)`.  Starting
with `m=0`, one product has

```text
u_i=29403/101000 > (1/4) max_j r_j  for every i,
r^+_1=-2601/44440<0.
```

Hence even a nonnegative chronological-flux phase center can violate the
input cone before the quarter stop.  The witness is exact in
`input_cone_chronological_flux_counterexample_exact.py`.  It is not a
canonical-history counterexample: its old increments need not arise from the
preceding retained product.  A proof must retain at least the constitutive
relation between those increments and the previous residual/momentum, not
only their admission order.

Even membership in the one-step post-push cone is insufficient.  Consider
the eight-vertex graph formed by a universal hub `0`, a leaf `1` adjacent
only to the hub, and a six-clique on vertices `2,...,7`, also joined to the
hub.  In the row-normalized coordinates above, take `s=1/100` and the prior
nonnegative residual `w=e_0`.  If

```text
r = K(Rw/d),
```

and `r` is normalized by its leaf value, symmetry gives exactly

```text
r_0=2/7,       r_1=1,       r_i=11/36  (2<=i<=7).
```

Thus `r` is not an arbitrary positive vector: it is the residual produced by
one legal diagonal post-push operation.  Nevertheless, setting the current
momentum increment to zero and applying `ReducedInputCone` gives

```text
max_i u_i-1/4 = 4007369027/39203920000 >0,
r^+_1          = -33165/16161616 <0.
```

The quarter rule therefore executes while the next leaf input residual is
strictly negative.  The full rational calculation is
`input_cone_postpush_counterexample_exact.py`.  This still is not a complete
zero-start trajectory, because `m=0` has not been coupled to the preceding
product that generated `r`.  It proves that a successful induction must
track a joint residual--momentum cone; even “the residual came from a legal
previous push” is not enough.

There is correspondingly strong but still finite evidence for the genuinely
reachable statement.  At `s=3/10` and relative outer tolerance `1/32`, the
piecewise-affine exact audit now covers *every* source threshold
`0<d_v rho<1` on all 728 connected labelled five-vertex simple graphs.  Its
29,903 rational trace cells contain 256,301 executed products and no negative
input residual.  The analogous four-vertex audit covers 38 graphs, 1,353
cells, and 12,841 products.  This eliminates isolated threshold samples as an
explanation for the earlier tests, but it remains a finite certificate at one
root and one stopping accuracy.  The reproducer is
`retained_prox_parametric_rho_exact.py`.

That finite pattern does not extend to all graphs.  Take the 16-vertex graph

```text
E={(0,1),(0,10),(1,2),(2,3),(3,4),(4,5),(5,6),(7,12),
   (8,9),(9,10),(9,11),(10,15),(11,12),(12,13),(12,14),
   (13,14),(14,15)}.
```

It is simple, connected, undirected, and unit-weighted.  Use source zero,

```text
s=1/224,       alpha=1/100351,
d_0 rho=481/8000,       rho=481/16000,
```

and start the two-certificate retained-prox chronology from zero.  Enable
input-residual frontier admission, one simultaneous active diagonal push per
product, and immediate diagonal pushes through maximal exterior closure.  At
one-based phase 20, product 10, the exact active face is

```text
{0,1,2,3,4,5,6,8,9,10,11,12,14,15}.
```

The input residual at vertex 11 is strictly negative, with

```text
xi_11/old_width = -1.533358898...e-8.
```

The preceding completed product has exact width ratio

```text
inner_width/old_width = 0.2583894607814098... > 1/4,
```

so the literal quarter rule must execute the failing product.  Every branch,
admission, push, phase update, and comparison is rational; the general trace
checker is `retained_prox_input_cone_trace_exact.py`.  This is a canonical
zero-start counterexample to `StoppedMaskedInputResidual` and therefore
removes the literal quarter-stopped Route A.  The dedicated instance and
asserting wrapper are `STOPPED_MASKED_INPUT_RESIDUAL_ZERO_START_COUNTEREXAMPLE.md`
and `stopped_masked_input_residual_zero_start_counterexample_exact.py`.

Moving the constant to one third still does not repair the route.  A separate
24-vertex simple connected unit graph, at the same root and with
`d_0 rho=173/8000` and `rho=173/16000`, has a Fraction-exact first failure
at one-based phase 13, product 7.  Its active vertex 16 satisfies

```text
xi_16/old_width = -9.274461320...e-8,
inner_width/old_width = 0.3732141756300159... > 1/3.
```

Thus the one-third rule must also execute its failing product.  See
`STOPPED_MASKED_INPUT_RESIDUAL_ONE_THIRD_COUNTEREXAMPLE.md` and
`stopped_masked_input_residual_one_third_counterexample_exact.py` for the
44-edge instance and exact assertions.

The same graph and parameters refute the two-fifths rule after its altered
outer stopping chronology.  At one-based phase 14, product 7, active vertex
16 has

```text
xi_16/old_width = -4.846557184...e-9,
inner_width/old_width = 0.4151107187959626... > 2/5.
```

This second run is certified by
`STOPPED_MASKED_INPUT_RESIDUAL_TWO_FIFTHS_COUNTEREXAMPLE.md` and
`stopped_masked_input_residual_two_fifths_counterexample_exact.py`.

The correct scope of each witness is its exact beta chronology cell:

```text
max{ratios at stopped products} <= beta
  < min{ratios at continued products}.
```

Outside this cell an earlier phase endpoint can change, so predecessor ratios
cannot be ordered monotonically.  Replaying forty-four exact cells on graphs
of at most 49 vertices removes that ambiguity: consecutive cells overlap from
zero through

```text
(0, 0.48979117875734753...).
```

The highest pieces are a 51-edge bridge, a 63-edge dense graph refuting
`beta=0.45`, structured double/triple-clock grafts, and a 27-vertex
edge-retimed graphs.  A 62-edge retiming reaches `0.482907...`; adding
`(8,11)` and decreasing the retained root to `s=1/1792` gives a 63-edge cell;
one further `(3,6)` chord and a root retiming to `s=1/672` extends the cover
to `0.484545...`.  A separate 64-edge graph supplies three overlapping root
retimings at beta `0.4847`, `0.485`, and `0.486`, reaching `0.486133...`;
a clock-side degree-preserving swap, one further rewire, two overlapping
branch-boundary retimings, and a two- through twenty-two-leaf ladder reach the
finite endpoint `0.4897911787...`.  Every
graph is simple, connected, unit-weight, and uses
one point source and zero initialization.  See
`STOPPED_MASKED_INPUT_RESIDUAL_BETA_CELL_ATLAS.md` and
`stopped_masked_input_residual_beta_cell_atlas_exact.py` for the complete
overlap certificate; the high cells and edge sets are in
`STOPPED_MASKED_INPUT_RESIDUAL_HIGH_BETA_COUNTEREXAMPLE.md` and
`STOPPED_MASKED_INPUT_RESIDUAL_TRIPLE_CLOCK_COUNTEREXAMPLE.md`.

On the final 35-vertex, 72-edge eight-leaf topology, three exact scaled
`s=0` rho retimings give an overlapping limiting relay from
`0.4880686430540822...` through `0.488691166865773...`, with strict
active-input failures.  All stop decisions and non-forced comparisons have
nonzero exact margins.  The remaining equalities are forced
closure/inheritance events and harmless automorphic twin-leaf maximum ties.
If a forced active zero becomes negative at small positive `s`, the run fails
earlier; otherwise continuity carries it to the strict limiting failure.
For each fixed beta inside the relay, a sufficiently small positive
`s=s(beta)` therefore gives a counterexample.  A 39-vertex twelve-leaf
topology has the corroborating zero-root cell
`[0.4886720900294752...,0.48889876186669784...)` and a slightly stronger
finite positive-root cell ending at `0.4888994588075898...`.  The next
41-vertex fourteen-leaf topology has an audited zero-root relay ending at
`0.489037149172748...` and a stronger finite relay ending at
`0.48903788718422087...`.  The 43-vertex sixteen-leaf topology has a
corroborating zero-root cell ending at `0.48913580953910807...` and a stronger
finite cell ending at `0.4891365074011953...`.  See
`STOPPED_MASKED_INPUT_RESIDUAL_BETA_04885_EIGHT_LEAF.md`.

The next 45-vertex eighteen-leaf graph has a retimed finite cell ending at
`0.4893806599606024...` and an audited zero-root family ending at
`0.4893830355111828...`.  Its phase-27 failure at active leaf `28` occurs
with simultaneous input batch `[19,22,23]`; this is the first high leaf-ladder
row in which fresh admissions and an already-active strict failure coexist.

Adding `(2,45)` and `(18,46)` gives a 47-vertex, 84-edge twenty-leaf graph.
At root `s=1/65536`, its exact finite cell is
`[0.48907818585092405...,0.4895138464285235...)`, overlapping E18.  Its
phase-26, product-8 failure is again at already active leaf `28`, but the input
batch is empty, so the chronology returns to the earlier already-active
failure mechanism.  The corresponding zero-root audit gives
`[0.48907818669711567...,0.48951378405604035...)` and classifies 40 forced
equality groups over 27 coordinates plus six structural twin-maximum ties;
all other relevant comparisons are strict, with tightest strict margin about
`2.6944e-8`.  It robustly corroborates the slightly stronger finite E20 row.

Adding `(5,47)` and `(19,48)` gives a 49-vertex, 86-edge twenty-two-leaf
graph.  Retiming the source scale to the exact fixed-branch equioscillation
value gives, at root `s=1/65536`, the finite cell
`[0.48869803978352204...,0.48979117875734753...)`.  The strict phase-27,
product-8 failure is at already active leaf `28` with empty input batch.
Product 7 continues after append closure admits and pushes `{22,23}`.  In the
zero-root branch, the product-3 row-41 and product-7 row-25 ratios are exactly
equal and jointly attain the open upper endpoint.  This is an equality across
distinct products, not a within-product maximum or stopping tie; the full
comparison audit still classifies all algorithmic equalities as forced.  The
audited zero-root cell is
`[0.48869804073544294...,0.4897917473484638...)`.  The finite-prefix
earlier-failure-or-continuity lemma used by the atlas turns every fixed beta
strictly inside this limiting cell into a sufficiently small positive-root
counterexample; the zero-root computation alone is not presented as a graph
instance.

The pushes are nevertheless doing real work.  If both the active push and the
append pushes are disabled, an even sparser exact zero-start obstruction is a
20-vertex path plus the chord `14-18`, at the same root and
`rho=1067/40000`.  Its fourth product in zero-based phase 18 has
`xi_18/old_width=-2.643407105...e-8`, while the predecessor ratio is
`0.321070341...`.  See `INPUT_FRONTIER_ONLY_ZERO_START_OBSTRUCTION.md` and
`input_frontier_only_zero_start_obstruction_exact.py`.  Thus a repaired proof
may exploit the push flux; it may not delete the pushes as implementation
details.

There is one exact constant-slack repair interface.  Replace the quarter
threshold by a fixed `beta` and stop a phase as soon as

```text
inner_width <= beta old_width,       0<beta<1/2.
```

Since the retained outer contraction coefficient is `1/2`, the next bracket
obeys

```text
new_width <= (1/2+beta) old_width.                  (BetaBracket)
```

Consequently, for every fixed `beta<1/2`, the already proved conditional
partial-gradient NAG analysis still yields the desired root dependence if the
following replacement statement is true:

```text
BetaStoppedMaskedInputResidual:
  every product executed before the beta stop has nonnegative active
  masked input residual on the canonical zero-start chronology.
```

The finite exact cell atlas reaches `0.48979117875734753...`; audited E18,
E20, and E22 zero-root families independently corroborate the limiting
leaf-ladder mechanism.  The E22 zero-root lift extends the overall result to
the open endpoint `0.4897917473484638...`.
Proving `BetaStoppedMaskedInputResidual` at any one fixed beta in the
remaining interval up to `1/2` would complete this route.  Refuting the route
requires extending the overlapping cells through that interval or proving a
uniform parametric construction.

The exact potential debit for an input correction is also informative.  Let
`q_raw-x=u+e`, `q_safe-x=u`, and reset
`z_safe=z_raw-(1+s)e/s`.  With `mu=s^2L`,

```text
(mu/2)(||z_safe-x*||^2-||z_raw-x*||^2)
 =sL(1+s)e^T(x*-x)
  -L(1+s)^2(e^Tu+||e||^2/2).                    (InputSafeguardDebit)
```

The first comparator cross term can be positive.  This is the precise debit
that the fixed-face residual formulation avoids and that a cross-face proof
must not silently drop.

### 5.2 Maximal global momentum retraction is safe but not accelerated

A simpler safeguard replaces the raw extrapolate by

```text
q_gamma=x+gamma theta d,        0<=gamma<=1,
```

and takes the maximal scalar satisfying the active input cone.  In the
normalized notation `A=B/L`, `e=(h-Bx)/L`, its value is exactly

```text
gamma=min{1,min_(i:(Ad)_i>0)e_i/[theta(Ad)_i]}.  (GlobalRetraction)
```

This makes every executed partial-gradient product legal.  It does not,
however, produce a new accelerated Lyapunov.  In estimate coordinates the
operation is the reset `z_gamma=x+gamma(z-x)`, whose exact debit is

```text
Delta_ret=(mu/2)(1-gamma)
          [2<x*-x,z-x>-(1+gamma)||z-x||_2^2].    (RetractionDebit)
```

The sign can be positive.  On the smallest connected graph, one unit edge,
at `s=1/20`, the supplied safe state

```text
e=(0,1),       d=(5,0)
```

has maximal `gamma=0`.  After the ordinary gradient, simultaneous diagonal
push, and auxiliary clamp, the standard potential ratio is exactly

```text
E^+/E=48495311162/42232935441=1.148281...>1>1-s.
```

This state embeds at a strictly positive phase center of the canonical
endpoint-source objective with `alpha=1/799` and `rho=1/100000`, but is not
asserted reachable from zero.  More importantly, before the first strict
retraction the safeguarded and original canonical histories are identical.
Thus the first `gamma<1` is exactly the first counterexample to
`StoppedMaskedInputResidual`; if that claim is true, the safeguard is inert
and the conditional root-rate proof already applies.  The scalar modification
therefore relocates rather than resolves the chronological question.  Without
a cumulative debit or accepted-momentum bound, only the ordinary
`O(s^-2 log(1/epsilon))` fixed-full-face fallback is proved.  See
`GLOBAL_SCALAR_MOMENTUM_RETRACTION.md` and
`global_scalar_momentum_retraction_exact.py`.

### 5.3 Direct conditional-expectation derandomization needs inverse response

On a supplied fixed face, uniform accelerated coordinate descent has the
desired expected work.  Its one-step potential can also be derandomized by an
omniscient branch choice.  For constant diagonal `Q_ii=a`, the exact branch
form is

```text
P_i=C-tau H_i,
H_i=g_i^2/(2a)+n g_i(zbar_i-x_i*).              (ACDBranchScore)
```

Choosing any `H_i` at least its average recovers the expected contraction
pathwise.  At a certified lower state `y=z=w=u`, with
`r=c-Qu>=0`, this apparently deterministic key reduces to

```text
H_i=r_i^2/(2a)+n r_i(Q^-1r)_i.                  (InverseResponseKey)
```

The missing term is the dense current-residual inverse response, not a local
residual score.  On the canonical unit three-vertex path, center source,
`alpha=1/1000`, and `rho=1/10000`, there is an exact positive full-face lower
state with residual proportional to `(9,10,11)`.  Max residual, max
degree-normalized residual, and max coordinate-descent decrease all choose
leaf two, but its `H_2` is strictly below the branch average.  Its accelerated
potential is therefore strictly above the randomized conditional mean and,
more strongly, exceeds `(1-tau)` times the pre-step potential.  Thus the
standard pathwise accelerated contraction itself fails for this local rule.

This is not merely an arbitrary-warm-state phenomenon.  On the same supplied
full face at `alpha=1/10`, `rho=1/1000`, starting NU-ACDM from
`y_0=z_0=0` and repeatedly choosing the smallest-index maximizer of `|g_i|`
gives the exact first eight choices

```text
0,1,2,0,1,2,0,1.
```

All primal and auxiliary coordinates stay nonnegative, but at iteration
seven the chosen branch has `H_1<(H_0+H_1+H_2)/3`; its potential is again
strictly worse than the conditional mean.  This is a zero-start result for a
supplied full face, not the changing-face minimal-support chronology.

This refutes only the direct residual-score/heap implementation, not every
deterministic accelerated coordinate method.  A usable derandomization still
needs either a solution-free locally maintainable pessimistic estimator or a
persistent certified approximation to `(Q^-1r)_i`; the latter is precisely
another `CenterLift` interface.  The derivation and exact verifier are in
`ACCELERATED_COORDINATE_DERANDOMIZATION_STOP.md` and
`accelerated_coordinate_derandomization_exact.py`.

The row-cost coupling is not an additional algebraic obstruction.  For a
fixed horizon `T`, adding normalized remaining expected row cost to the
potential produces an omniscient conditional-expectation estimator whose
branch key is

```text
H_i-lambda_k d_i.
```

It yields simultaneously pathwise accelerated error and at most twice the
uniform-sampling expected row work.  The observable degree penalty leaves the
same unknown `H_i`, so this positive result sharpens the remaining issue to
the solution-dependent inverse-response key alone.

## 6. Sharpened remaining theorem

There are now three closely related completion targets.

### A. Early-stopped canonical-history route

The literal quarter-width `StoppedMaskedInputResidual` statement is refuted
by the exact zero-start graph above.  Its surviving constant-slack replacement
is:

```text
  find one fixed beta in [0.4897917473484638...,1/2)
for which BetaStoppedMaskedInputResidual holds.
```

Then `BetaBracket` and the already proved input-frontier partial-gradient NAG
contraction close the target with no safeguard debit.  Forty-four exact
same-chronology cells plus the audited limiting-family checks already cover
continuously below the displayed endpoint.  They neither prove that a
remaining fixed threshold works nor
cover the interval all the way to `1/2`.

### B. Exact-box linear-coupling route

`ExactBoxLC` already proves graph-uniform accelerated convergence across all
safe support insertions.  Its sole missing implementation statement is:

```text
ExactBoxMaintenance:
  maintain the greatest safe point in each changing momentum box in
  O_tilde(vol(current support)) amortized work per outer product.
```

This is an algorithmic linear-algebra problem rather than a stability
conjecture.  A black-box inner solve on every product is too expensive.
The monotone rank-one response and one-pass peeling formulas in the supplied
note are plausible ingredients for a persistent implementation, but they do
not yet prove this amortized bound.

Revealed-edge persistence alone cannot maintain the box oracle.  On an
endpoint-seeded canonical unit path with full final support, there are valid
fixed-support `SafeBoxLC` states whose trial residual is `-r e_v`; the exact
correction is the dense vector `r Q^{-1}e_v>0`, although the support and the
compensated-halo matrix do not change at all.  Moreover, a literal monotone
principal-pivot implementation exposes the path in order, and each new pivot
strictly changes every old response coordinate.  It therefore performs
`n(n-1)/2` materialized response writes for path volume `2(n-1)`.

This is not a lower bound against an implicit path recurrence or a multilevel
response data structure, but it refutes the shortcut “one revealed-edge
update and one pivot per coordinate imply support-linear exact maintenance.”
The exact construction and rational audit are in
`EXACT_SAFE_BOX_RESPONSE_SHORTCUT_OBSTRUCTION.md` and
`exact_safe_box_response_shortcut_obstruction.py`.

There is an exact support-linear reduction of one correction query to a
grounded nonnegative quadratic diffusion.  In degree coordinates its matrix
is

```text
((1-alpha)/2)L(G[S])
  +diag(alpha d_i+((1-alpha)/2)deg_(S^c)(i)).
```

The exact orthant LCP solution automatically lies below the momentum-box cap.
A raw objective-approximate diffusion solution need not satisfy either the
cap or the rowwise supersolution inequalities.  This output mismatch is now
repaired exactly.  For canonical `Q`, let `h_i=sqrt(d_i)` and, for any
nonnegative approximate correction `tilde_e`, set

```text
gamma=max_i[-(hat_t+Q_SS tilde_e)_i/(alpha h_i)]_+,
e=min{u,tilde_e+gamma h_S}.                       (BarrierCapRepair)
```

Because `Q_SS h_S>=alpha h_S` and Stieltjes supersolutions are closed under
coordinatewise minimum, this `e` is exactly capped and rowwise safe.  An
explicit strong-convexity bound shows that polynomially small objective error
is enough for `ABoxStop`, with no strict-complementarity margin; the extra
precision enters only logarithmically for a logarithmic-accuracy solver at
one supplied state.  A full target-work theorem must additionally charge the
whole-run precision as the box width shrinks; that dependence is included in
the open oracle statement below, not silently assumed bounded here.  Thus the
randomized near-linear generalized-diffusion theorem would implement the
outer route in randomized target work.  It does not meet the requested
deterministic model.  Existing deterministic convex-flow results give
`M^(1+o(1))`, not `O_tilde(M)`.  The remaining exact-box gap is therefore a
deterministic support-linear approximate-QP solver, not one-sided rounding.
See `POSITIVE_BARRIER_SAFE_SUPERSOLUTION_ROUNDING.md` and
`DETERMINISTIC_SAFE_BOX_ORACLE_AUDIT.md`.

The word “approximate” cannot be dropped from that missing solver.  A new
canonical unit-edge family applies the repair to the zero correction and
obtains an exactly safe capped output, but its `ABoxStop` ratio is
`2(1+3s^2)/(5s(1+s))>1`.  Hence the positive barrier is a certified rounding
layer, not a zero-work substitute for finding the obstacle solution.  On
this family the conclusion is direction-independent: every `h>0` with
`Bh>0` is forced by `b/a<h_2/h_1<a/b` to hit the same full cap.

Nor does the condition-two `eta=1` safe-prox inner problem immediately close
the outer loop.  Two positive canonical full-face subsolutions can have the
raw momentum center `y=x*+epsilon h`; then
`P_1(y)=x*+epsilon h/(1+alpha)`.  Every original-safe repaired output lies
below `x*` and therefore has raw-centered proximal-objective error at least

```text
epsilon^2||h||_2^2/[2(1+alpha)].
```

This is a legal safe-state pair, not a claim that a named zero-start safe-prox
trajectory reaches it.  Repairing the center changes the queried proximal
objective.  Consequently the existing accelerated-proximal theorem cannot
simply be pasted onto the
safe inner solver; a safeguarded-center estimate sequence or a quantitative
reset-packing theorem is still required.  The construction and exact check
are in `POSITIVE_BARRIER_SAFE_SUPERSOLUTION_ROUNDING.md`.

### C. One-pass enforced-safe route

Use the direct safe-box/peeling recurrence.  Safety, locality, fixed-face
acceleration, the one-pass projection certificate, the alpha-free two-step
charge, the persistent-estimate inequality `PeelingLC`, and the point-source
face-change bank are all exact.  Section 2.3 now rules out even the canonical
zero-start version of `PeelingLCAbsorption`: the unit-edge family needs
`Omega(alpha^(-1))` rounds for constant-factor objective reduction, and its
max-residual stopping rule takes
`Omega(alpha^(-1) log(1/alpha))` rounds at a fixed relative target.  Therefore
the memoryless direct one-pass map itself is no longer a completion route.
Section 2.1.1 also
shows that restarting the pass until `ABoxStop` costs `Omega(alpha^(-1))`
total passes on a different canonical zero-start unit-edge family before a
constant-factor reduction.  A surviving modification must retain the
unfinished projection response, change the safeguard, or use the distinct
exact-prox envelope.  The first precise remaining statement is:

```text
PersistentProjectionResponse:
  a support-linear carry-over state reactivates replenished peeling
  coordinates and makes ResidualAPG + InjectionCharge +
  DirectTwoStepCharge obey a
  graph-uniform O(alpha^{-1/2} polylog) last-iterate
  max-positive-residual bound across all support insertions.
```

For the exact-prox peeling/barrier/reflection envelope, Section 3.1 rules out
only the black-box reduction through `sum zeta`: the literal rate remains
open, and a proof must use a peeling-specific retained-momentum or oriented
event invariant.

A proof may use an `alpha^{-O(1)}` prefactor, because it enters the iteration
count only logarithmically.  It must not replace the injection/peeling terms
by arbitrary per-round errors: critically damped acceleration can amplify
unstructured recent perturbations.  The one-sided monotone slack bank and
the two-step objective charge are the essential extra structure.

Until the beta-stopped route, `ExactBoxMaintenance`,
`PersistentProjectionResponse`, or a genuinely
peeling-specific exact-prox block theorem is proved, the sparse-work theorem
remains conditional.  The new material *has* removed cross-support stability
for the exact safeguard: the remaining gap is now sharply located at
support-linear realization.  A memoryless direct one-pass realization is
provably insufficient; an exact or persistent approximate projection state,
or a different exact-prox mechanism, is essential.
