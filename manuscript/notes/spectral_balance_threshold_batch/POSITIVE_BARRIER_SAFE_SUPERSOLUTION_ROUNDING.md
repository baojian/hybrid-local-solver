# Positive-barrier rounding of an approximate safe-box correction

Date: 2026-09-04

## Verdict

**Proved here.**  The one-sided rounding part of `ExactBoxMaintenance` is
easier than the current oracle audit states.  Let `B` be Stieltjes and let the
known box endpoint `u` satisfy

```text
u>=0,                 F(u):=hat_t+B u>=0.
```

If `h>0` is a positive barrier with `Bh>=sigma h>0`, then an arbitrary
approximation `e_tilde` can be converted, once `k=Bh` is available, using one
additional sparse residual product and coordinatewise operations, into an
**exactly** nonnegative, capped, rowwise supersolution.  Computing `k` from
scratch costs one further sparse product (and it may be cached while the face
is fixed):

```text
k       = B h,
gamma   = max{0,
              max_i (-e_tilde_i/h_i),
              max_i (-F(e_tilde)_i/k_i)},
e_bar   = e_tilde+gamma h,
e       = min{u,e_bar}.                            (BarrierCap)
```

All inequalities and the minimum are coordinatewise.  The output obeys

```text
0<=e<=u,              F(e)>=0.                    (ExactSafe)
```

For a canonical PageRank face `B=Q_SS` and
`h_S=(sqrt(d_i))_(i in S)`, the full-space identity `Qh=alpha h` gives

```text
B h_S=alpha h_S-Q_(S,S^c)h_(S^c)>=alpha h_S.
```

Thus `sigma=alpha` is always available, including on a proper exposed face.
The sharper row denominators `(Bh_S)_i` should be used when the boundary
grounding is nonzero.

This does **not** give the desired total
`O_tilde(M/sqrt(alpha))` implementation.  A fresh deterministic accelerated
projected solve of the nonnegative quadratic still costs
`O_tilde(sqrt(L/mu))` products inside each of
`O_tilde(sqrt(L/mu))` outer rounds.  The rounding adds only a constant number
of products and a
logarithmic accuracy requirement; the unresolved part is a support-linear
approximate obstacle solver, or a persistent solver whose work is amortized
over the linked right-hand sides.

## 1. The lattice lemma missed by isolated clipping

Put

```text
C={q:F(q)=hat_t+Bq>=0}.
```

### Lemma 1 (supersolutions are closed under coordinatewise minimum)

If `B_ij<=0` for `i!=j` and `p,q in C`, then

```text
r=min{p,q} in C.
```

#### Proof

Fix row `i` and suppose, without loss of generality, that `r_i=p_i`.  Since
`r_j<=p_j` and `B_ij<=0` for every `j!=i`,

```text
F_i(r)
 =hat_t_i+B_ii p_i+sum_(j!=i) B_ij r_j
 >=hat_t_i+B_ii p_i+sum_(j!=i) B_ij p_j
 =F_i(p)>=0.
```

This holds in every row.  No positive definiteness is needed for this
lattice statement.  Dually, lower subsolutions in safe-point coordinates
are closed under coordinatewise maximum.

The qualification is important.  Decreasing one coordinate of a
supersolution in isolation can make its diagonal row negative.  Clipping to
the SafeBox endpoint is different: the endpoint `u` is itself a
supersolution, so the *simultaneous* coordinatewise minimum is safe.

### Lemma 2 (positive-barrier repair followed by a safe cap)

Assume `h>0` and `k=Bh>0`.  Define `(BarrierCap)`.  Then `(ExactSafe)` holds.

#### Proof

The definition of `gamma` gives `e_bar>=0`, and

```text
F(e_bar)=F(e_tilde)+gamma k>=0.
```

Both `u` and `e_bar` are therefore nonnegative supersolutions.  Lemma 1 gives
`F(min{u,e_bar})>=0`, while the minimum visibly lies in `[0,u]`.

In safe-point coordinates `w=y-e` and `u=y-x`, the same operation is

```text
w=max{x, y-e_tilde-gamma h}.
```

It is exactly a downward barrier shift followed by flooring at the known
lower subsolution `x`; it keeps `x<=w<=y` and `c-Bw>=0`.

### Corollary 3 (relation to the exact box)

Let `e*` be the unique lower-orthant LCP solution

```text
e*>=0,                F(e*)>=0,
e*_i F_i(e*)=0.
```

For an SPD M-matrix it is the least nonnegative supersolution.  Hence the
rounded point satisfies

```text
e*<=e<=u.
```

In particular the repair approaches the exact box from its safe side as
`e_tilde` approaches `e*`; it requires no strict-complementarity or cap-slack
margin.

## 2. A quantitative certified-gap bound

The following bound shows that the rounding can be combined with an
objective-accurate deterministic nonnegative-QP method.  It also identifies
where `alpha` enters: in the precision requested of the approximate solve,
not as a new number of rounding passes.

Assume

```text
mu I<=B<=L I,          Bh>=sigma h>0,
delta=||e_tilde-e*||_(infinity,h)
     :=max_i |e_tilde_i-e*_i|/h_i.
```

Define the weighted absolute row norm

```text
K_h=max_i sum_j |B_ij|h_j/h_i.
```

Because `B` is Stieltjes,

```text
K_h=max_i {2B_ii-(Bh)_i/h_i} <=2L-sigma.         (BarrierRowNorm)
```

Let

```text
C_gamma=max{1,K_h/sigma},
eta=(1+C_gamma)delta,
C_u=h^T F(u)+K_h h^T u.                          (ComputableScale)
```

### Lemma 4 (distance and complementarity after rounding)

The output of `(BarrierCap)` obeys

```text
0<=e-e*<=eta h,
zeta:=e^T F(e)<=eta C_u.                         (RoundedGap)
```

#### Proof

Write `t*=F(e*)`.  Since `e*>=0` and `t*>=0`, the primal and residual
deficits of `e_tilde` satisfy

```text
max_i [-e_tilde_i/h_i]_+ <=delta,
max_i [-F_i(e_tilde)/(Bh)_i]_+
 <=K_h delta/sigma.
```

Thus `gamma<=C_gamma delta`.  Corollary 3 and `e<=e_bar` now give

```text
0<=d:=e-e*<=eta h.
```

Moreover `F(e)=t*+Bd`, `e<=u`, and

```text
h^Tt*<=h^TF(u),
```

because their difference is
`h^TB(u-e*)=(Bh)^T(u-e*)>=0`.  Complementarity and the weighted row bound
therefore give

```text
zeta
 =d^Tt*+e^TBd
 <=eta h^Tt*+sum_i e_i |(Bd)_i|
 <=eta {h^TF(u)+K_h h^Tu}.
```

Every quantity on the right except `delta` is supplied or computable with a
sparse product.

### Corollary 5 (a sufficient `ABoxStop` precision)

For the SafeBoxLC state, put `s=sqrt(mu/L)`.  Since

```text
u=y-x,                 z-y=u/s,
w=y-e,
```

its computable allowance is

```text
A(e)
 =.5||u-e||_B^2+(s mu/2)||u/s+e||_2^2
 >=mu(1+s)||u||_2^2/(2s).                        (AllowanceFloor)
```

For completeness, set `a=(z-x)/(1+s)`, so `u=sa`.  The cancellation of the
cross term gives the exact Euclidean identity

```text
||u-e||_2^2+s||a+e||_2^2
 =s(1+s)||a||_2^2+(1+s)||e||_2^2.
```

Using `B>=mu I` proves `(AllowanceFloor)` (and retains the additional
nonnegative term `mu(1+s)||e||_2^2/2`).  If `u=0`, the cap forces `e=0`
and `ABoxStop` holds exactly.  If `u!=0`, the sufficient condition

```text
delta <= mu||u||_2^2
         /[2s(1+C_gamma)C_u]                     (DistanceTarget)
```

implies

```text
(1+s)zeta<=A(e).
```

No complementarity margin appears.

For the nonnegative quadratic

```text
chi(q)=.5 q^TBq+hat_t^Tq,        q>=0,
```

any nonnegative output satisfying

```text
chi(e_tilde)-chi(e*)<=Delta
```

has

```text
delta<=sqrt(2Delta/mu)/min_i h_i.                (ObjectiveToDistance)
```

There is a sharper direct objective-gap conversion than substituting this
last bound into `(RoundedGap)`.  Put

```text
h_min=min_i h_i,             H=||h||_2,
C_2=||hat_t||_2+2L||u||_2.
```

For a nonnegative `e_tilde`, no primal-sign shift is needed.  If
`d_tilde=e_tilde-e*`, then

```text
||d_tilde||_B<=sqrt(2Delta),
|(B d_tilde)_i|<=sqrt(B_ii)||d_tilde||_B
                 <=sqrt(2LDelta).
```

Consequently, when `sigma=mu` (as on a canonical PageRank face),

```text
gamma<=sqrt(2LDelta)/(mu h_min),
||e-e*||_2
 <=sqrt(2Delta/mu) K_sharp,
K_sharp=1+(H/h_min)sqrt(L/mu).                   (SharpRoundedDistance)
```

Here coordinatewise order `0<=e-e*<=e_bar-e*` justifies passing from the
unclipped to the clipped Euclidean distance.  For a general barrier
`Bh>=sigma h`, replace the second term in `K_sharp` by
`H sqrt(L mu)/(sigma h_min)`.

Writing `d=e-e*`, complementarity gives

```text
zeta=d^TF(e*)+e^TBd
 <=||d||_2 {||hat_t||_2+2L||u||_2}
 <=sqrt(2Delta/mu) K_sharp C_2.                 (SharpObjectiveGap)
```

Thus the explicit sufficient objective tolerance is

```text
Delta <=(mu/2)
         [mu||u||_2^2/(2s K_sharp C_2)]^2.       (ObjectiveTarget)
```

The weighted bound remains useful for arbitrary signed approximations and
for using the sharper row values `(Bh)_i`; `(ObjectiveTarget)` is the better
generic consequence of a nonnegative objective-gap guarantee.

Therefore a standard deterministic accelerated projected method can run to
the corresponding objective tolerance, apply `(BarrierCap)`, compute the
exact `zeta` and `A(e)`, and continue until the directly checkable
`ABoxStop` test succeeds.  Tightening the target by a polynomial in
`1/alpha` changes the accelerated iteration bound only by
`O(sqrt(L/mu) log(1/alpha))`; the rounding itself does not add a
`1/alpha` number of passes.  This statement is statewise: `(ObjectiveTarget)`
can shrink like `||u||_2^4`.  A graph-uniform target-work theorem must also
bound the cumulative encoding or logarithmic precision needed as `u` shrinks,
or include that cost directly in the open `SafeSupersolution` oracle.  No such
uniform precision theorem is claimed here.

This is a certification statement in the exact-real/algebraic-cell model.
Finite-precision directed rounding and bit complexity remain separate.

## 3. The augmented-ground objective also rounds

The positive ground coordinate in the pure-Laplacian reduction is not an
obstruction either.  Suppose

```text
B=L_int+diag(g),        B 1=g>0,
d_0=g^Tu+tau,           tau>0,
```

and let `L_bar` be the Laplacian obtained by joining coordinate `i` to a
ground vertex with conductance `g_i`.  The augmented diffusion objective is

```text
J(p,q)=.5[p;q]^T L_bar[p;q]+hat_t^Tp+d_0 q,
        p>=0, q>=0.
```

Put `v=p-q 1`.  Internal and ground-edge differences give the exact identity

```text
J(p,q)=chi(v)+q(1^That_t+d_0).                   (GroundSplit)
```

The exact optimum is `(e*,0)`.  If `t*=F(e*)`, then

```text
chi(v)-chi(e*)
 =.5||v-e*||_B^2+(t*)^T(v-e*)
 =.5||v-e*||_B^2+(t*)^Tv.
```

Since `p=v+q1>=0`, one has `(t*)^Tv>=-q 1^Tt*`.  Also

```text
(1^That_t+d_0)-1^Tt*
 =d_0-g^Te*
 =g^T(u-e*)+tau>=tau.
```

Therefore every nonnegative augmented output satisfies the quantitative
error bound

```text
J(p,q)-J(e*,0)
 >=.5||v-e*||_B^2+tau q
 >=(mu/2)||v-e*||_2^2+tau q.                    (GroundGap)
```

Thus an additive objective-accurate grounded-diffusion output supplies a
possibly signed approximation `v` to `e*`; `(BarrierCap)` then makes it
exactly nonnegative, capped, and rowwise feasible.  The same sharp bound
`(SharpRoundedDistance)` applies because its residual-repair term dominates
the possible primal-sign repair when `sigma=mu<=L`.

This strengthens the source audit boundary.  A near-linear approximate
grounded-diffusion theorem can be converted to the `ABox` interface; a
separate strict-margin active-face recovery or one-sided rounding theorem is
not needed.  The Chen--Peng--Wang solver remains randomized, while the
audited deterministic convex-flow algorithms retain `m^(o(1))` overhead.
Those algorithmic mismatches, and finite-precision exact sign certification,
remain unchanged.

## 4. What the result does and does not buy

### The positive consequence

Suppose an approximate nonnegative-QP routine reaches a certified objective
gap `Delta` in

```text
T_approx(nnz(B),Delta)
```

work.  Then `(BarrierCap)` converts its output to a valid `ABox` pair using
one residual product after `Bh` is available (at most two products when it is
formed from scratch), `O(|S|)` coordinate operations, and adaptive
logarithmic precision.  Thus a deterministic support-linear approximate
obstacle solver with logarithmic accuracy dependence would be enough for the
SafeSupersolution oracle; a new one-sided active-set rounding theorem is not
additionally required.  This conditional statement charges the required
whole-run precision; the statewise bound alone does not prove that charge.

### The remaining product-count loss

A fresh accelerated projected solve has

```text
T_approx=O_tilde(nnz(B)sqrt(L/mu)).
```

Used independently in every one of
`O_tilde(sqrt(L/mu))` SafeBoxLC rounds, this gives

```text
O_tilde(M L/mu)=O_tilde(M/alpha)
```

for canonical RPPR.  The new rounding therefore repairs the exact
feasibility interface but does not provide the persistent near-linear
maintenance needed for `O_tilde(M/sqrt(alpha))` total work.  Ordinary
Chebyshev also applies only after a linear correction face has been supplied;
it does not identify the obstacle face.

### A `1/alpha` geometric sensitivity is unavoidable

The barrier coefficient cannot in general be bounded by the raw row-residual
deficit without inverse spectral scale.  On the canonical two-vertex unit
edge, for arbitrary `alpha in (0,1]`,

```text
B=Q,                  h=(1,1),
Bh=alpha h,           hat_t=-alpha h,
u=h,                  e*=h.
```

For `0<delta<1`, take `e_tilde=(1-delta)h`.  Its residual is

```text
F(e_tilde)=-alpha delta h.
```

Every capped supersolution equals `e*=u`, by the least-supersolution
property.  Hence any exact repair must move by `delta h`, namely the residual
deficit divided by `alpha`.  This is an unavoidable conditioning of the
*correction magnitude*.  It does not imply `Omega(1/alpha)` arithmetic:
Chebyshev or accelerated convergence reaches the extra factor in accuracy
logarithmically.

### The repair is not a zero-solve oracle

The exact-feasibility statement holds for an arbitrary input, but the
`ABoxStop` conclusion still needs the input to approximate the obstacle
solution.  In particular, applying `(BarrierCap)` to `e_tilde=0` is not a
support-linear replacement for the inner solve.

Here is an exact canonical example.  On one unit edge, choose

```text
s in (0,1/4],       alpha=s^2,
B=[[a,-b],[-b,a]],  a=(1+s^2)/2, b=(1-s^2)/2,
rho=1/4,             delta=s^4.
```

At a strictly positive full-support `SafeBoxLC` state, let the exact
correction, its complementary residual, and the cap be

```text
e*=(delta,0),       t*=(0,delta),       u=(2delta,delta).
```

Such a state is compatible with the canonical point-source load.  Indeed,
the original optimum is `(a-rho,b-rho)` and one may take

```text
x=(a-rho,b-rho)-s^2(b,a)-delta 1,
y=x+u,             z=x+(1+s)u/s.
```

These vectors are positive for the displayed range, and
`hat_t=c-By=t*-Be*`, so `u` is a supplied safe cap.  Starting the repair
from zero gives

```text
gamma=a delta/alpha=a s^2 >=max_i u_i,
e=min(u,gamma 1)=u.
```

It is exactly feasible, but direct calculation gives

```text
zeta=s^8(1+3s^2),
A=(5/2)s^9(1+s)^2,
(1+s)zeta/A=2(1+3s^2)/(5s(1+s))>1.
```

Thus the certified outer contraction rejects this safe point.  This is not an
artifact of choosing the canonical barrier `h=1`.  Normalize any positive
barrier direction as `h=(1,r)`.  The strict condition `Bh>0` forces

```text
b/a<r<a/b.
```

Only the first row of `F(0)=(-a delta,(1+b)delta)` is negative, so the exact
barrier shift has

```text
gamma h=(a delta/(a-br), ar delta/(a-br)).
```

For `s<=1/4`,

```text
2b^2-a^2=(1-6s^2+s^4)/4>0,
b-a^2=(1-4s^2-s^4)/4>0.
```

Together with `r>b/a`, these inequalities imply respectively that the two
displayed coordinates are at least `2delta` and `delta`.  Hence **every**
positive-barrier direction caps
to the same point `u`, and every such zero-input repair fails `ABoxStop`.

The new rounding theorem therefore removes the *one-sided output*
obstruction, not the need to compute an objective-accurate input.  The exact
companion script checks the instance and two interior barrier directions at
`s=1/10`.

### A condition-two safe prox does not automatically accelerate

The supplied continuation note's `eta=1` proximal obstacle has Hessian
`Q+I`, condition number at most two, and a subsolution center makes its
monotone projected iterations safely local.  `(BarrierCap)` has an even
stronger barrier there, since `(Q+I)h=(1+alpha)h`.  This closes the inner
oracle only when its center is already an original subsolution; it does not
license the extrapolated center required by a standard accelerated
proximal-point theorem.

There is a clean exact boundary on a canonical full positive face.  Put
`alpha=s^2`, `theta=(1-s)/(1+s)`, and choose a sufficiently small `epsilon>0`.
The two consecutive points

```text
x_minus=x*-(epsilon+2epsilon/theta)h,
x=x*-epsilon h
```

are positive original subsolutions.  They form a legal pair of safe states;
this example does not additionally claim that a particular zero-start safe
prox implementation reaches that pair.  Their raw accelerated center is

```text
y=x+theta(x-x_minus)=x*+epsilon h,
```

which is unsafe, and its exact `eta=1` prox is

```text
P_1(y)=x*+epsilon h/(1+alpha)>x*.
```

Every original-safe output `z` obeys `z<=x*`.  Writing
`d=P_1(y)-z=epsilon h/(1+alpha)+r` with `r>=0` and using
`(Q+I)h=(1+alpha)h` gives

```text
H_y(z)-H_y(P_1(y))
 =.5||d||_(Q+I)^2
 >=epsilon^2||h||_2^2/[2(1+alpha)].
```

Hence exact safety is incompatible with arbitrarily accurate solution of
this *raw-centered* prox query.  Repairing the center instead changes the
proximal problem, so an off-the-shelf accelerated-proximal theorem no longer
applies.  This does not rule out a new safeguarded-center estimate sequence
or a reset-packing analysis; it identifies the extra theorem such a route
would need.  The exact script checks a point-source unit-edge instance at
`s=1/10`.

### Safe clipping can increase the complementarity gap

Although clipping to `u` preserves feasibility, its post-clipping gap must be
recomputed.  At `alpha=1/3` on the same unit edge, take

```text
B=(1/3)[[2,-1],[-1,2]],       h=(1,1),
hat_t=(0,1),                  e*=0,
u=(3,0),                      e_bar=(3,1).
```

Both `u` and `e_bar` are nonnegative supersolutions and
`min{u,e_bar}=u`.  Nevertheless

```text
e_bar^T F(e_bar)=17/3 < 6=u^T F(u).
```

Thus feasibility is lattice-monotone, while the particular certificate
`e^TF(e)` is not.  The rounded pair's gap, rather than a pre-clipping gap,
must be used in `ABoxStop`.

The companion script
`positive_barrier_safe_supersolution_rounding_exact.py` checks all five exact
algebraic tests in this note, including the canonical two-vertex sensitivity,
zero-input, unsafe-center prox, and gap-nonmonotonicity calculations.

## 5. Claim status

**Proved here.**  Minimum closure of Stieltjes supersolutions;
positive-barrier repair plus a supersolution cap; the exact distance and
complementarity bounds; the candidate-independent allowance floor; and the
augmented-ground gap extraction; and the canonical two-vertex sensitivity,
direction-independent zero-input rejection, unsafe-prox-center accuracy
floor, and gap-nonmonotonicity examples.

**Conditional.**  If a deterministic support-linear approximate obstacle
solver with logarithmic accuracy dependence is supplied, this rounding turns
it into the `SafeSupersolution` oracle in support-linear additional work.

**Open.**  Such a deterministic support-linear approximate solver over the
linked changing right-hand sides, or an equivalent persistent response
implementation, and hence the general
`O_tilde(M/sqrt(alpha))` deterministic RPPR theorem.

**Refuted.**  The claims that clipping to the known SafeBox endpoint can
destroy rowwise feasibility, or that objective approximation additionally
needs a strict-complementarity margin merely to obtain an exact `ABox` pair.
The different claim that clipping an isolated coordinate to a non-feasible
cap can destroy its own residual remains true.
