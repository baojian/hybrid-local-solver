# Exact safe-prox acceleration across support growth: two strict interface obstructions

Date: 2026-09-04

This is an unregistered companion audit.  It does not modify the integration
note or any shared claims registry.

## Verdict

The fixed-face exact-safe-box theorem cannot be extended merely by
zero-appending its residual state, by telescoping the same `Q_SS^{-1}`
estimate-sequence energy over growing principal faces, or by replacing those
principal metrics with the fixed full-dimensional `Q^{-1}` metric while
keeping the ordinary fixed-orthant APG recurrence.

Two exact effects occur at a support insertion:

1. an inactive obstacle multiplier is released into the next momentum
   residual with a positive coefficient; and
2. the inverse metric on an old vector increases by a Schur-complement term.

A canonical two-vertex point-source instance makes both effects strict.  In
that instance the greatest-safe-box projection does no clipping at the
support-changing round, so its same-round clipping credit is exactly zero
while the multiplier injection is positive.

This is a proof-interface obstruction, not a rate counterexample.  A global
square-root theorem for the exact-prox recurrence remains possible, but its
Lyapunov must account explicitly for inactive multipliers/support discovery,
or use a different global primal state.  The fixed-face proof cannot simply
be pasted across support breakpoints.

## 1. The missing multiplier in the fixed-face recurrence

Let

```text
x^k=P_1(w^(k-1)),       S_k=supp(x^k),
r^k=c-Qx^k.
```

The proximal KKT system has an obstacle multiplier `lambda^k>=0` and gives
the global identity

```text
r^k=bar(s)^k-lambda^k,
bar(s)^k=x^k-w^(k-1),
bar(s)^k_i lambda^k_i=0.                       (KKTResidual)
```

Here `bar(s)^k` is zero off `S_k`; on `S_k` it is the nonnegative proximal
displacement used by the fixed-face proof.  For the momentum trial

```text
y^k=x^k+theta(x^k-x^(k-1)),
```

its exact raw original residual is

```text
hat(t)^k=c-Qy^k=(1+theta)r^k-theta r^(k-1).
```

Suppose `S_k=S_(k-1) union E` grows.  Restricting to the new face and using
`(KKTResidual)` gives

```text
hat(t)^k_(S_k)
 =(1+theta)bar(s)^k-theta overline{bar(s)^(k-1)}
   +theta lambda^(k-1)_(S_k).                  (MultiplierInjection)
```

The bar denotes zero extension from the old face.  On every newly admitted
coordinate `i in E`, the last term may be strictly positive because that row
was an active obstacle at the preceding proximal point.  It is absent from
the fixed-face recurrence

```text
(1+theta)s_k-theta s_(k-1).
```

Embedding only the nonnegative displacement state in the final support
therefore does not reproduce the actual residual dynamics.

There is nevertheless an exact fixed-metric identity.  Extend
`e^k=y^k-w^k` by zero off `S_k`, put `t^k=c-Qw^k`, and define

```text
C_S={z in R^n : z_S>=0}.
```

The correction LCP is exactly the full-dimensional projection formula

```text
t^k=Pi_{C_(S_k)}^{Q^{-1}}(hat(t)^k).             (MovingConeProjection)
```

Indeed, its KKT multiplier is `e^k`, which is supported on `S_k`, and
`t^k=hat(t)^k+Qe^k`.  Thus the metric can be held fixed, but the feasible
cone changes whenever the positive proximal support grows.

More importantly, even changing only the projection description does not
restore one ordinary fixed-cone APG recurrence.  Let

```text
B=(I+Q)^{-1},        t^k=c-Qw^k.
```

Full proximal KKT gives the exact identity

```text
r^k=B t^(k-1)-(I-B)lambda^k,

hat(t)^k=B((1+theta)t^(k-1)-theta t^(k-2))
          -(1+theta)(I-B)lambda^k
          +theta(I-B)lambda^(k-1).             (FullKKTRecurrence)
```

The last two terms vanish on a fixed full positive face, but not in general
at a support insertion.  They are the full-dimensional form of the released
multiplier in `(MultiplierInjection)`.

## 2. Exact canonical support-entry witness

Use the unit edge, source zero, and

```text
alpha=1/99,       rho=1/3,
Q=[ 50/99  -49/99 ],
  [ -49/99  50/99 ],
c=(2/297,-1/297).
```

The accelerated proximal root and momentum are

```text
sqrt(alpha/(1+alpha))=1/10,       theta=9/11.
```

Starting from zero, the first exact proximal point and its greatest safe-box
center are

```text
x^1=(2/447,0),       w^1=(40/4917,0).
```

The first original residual decomposes exactly as

```text
r^1=(2/447,-17/14751)
   =(2/447,0)-(0,17/14751)
   =bar(s)^1-lambda^1.                         (FirstMultiplier)
```

The next exact proximal point has full support:

```text
x^2=(203/19800,3347/2950200)>0.
```

At the momentum trial from `(x^1,x^2)`, the actual raw residual and the
zero-appended fixed-face prediction are respectively

```text
hat(t)^2
 =(307/1622610,4877/1622610),

hat(t)^2_zero
 =(307/1622610,3347/1622610).
```

Their difference is exactly

```text
hat(t)^2-hat(t)^2_zero
 =theta lambda^1
 =(0,1530/1622610)>0.                          (StrictInjection)
```

Both raw vectors are already strictly positive.  Hence their
`Q^{-1}`-metric projections onto the nonnegative orthant are the vectors
themselves, and they remain different after the greatest-safe-box map.
In particular, the actual support-changing trial is already safe:

```text
w^2=y^2,       ||w^2-y^2||_Q^2/2=0.
```

Thus the clipping credit cannot pay `(StrictInjection)`; it vanishes while
the injected multiplier is nonzero.

The same instance directly separates the actual recurrence from the natural
fixed-full-dimensional APG recurrence.  With `t^0=c` and
`t^1=c-Qw^1`, ordinary APG would feed the fixed projection with

```text
B((1+theta)t^1-theta t^0)
 =(13637/32452200,89737/32452200)>0.
```

The actual raw argument differs by the exact KKT term

```text
theta(I-B)lambda^1
 =(-833/3605800,867/3605800) != 0.              (FixedFullFailure)
```

Both the predicted and actual arguments lie strictly inside the positive
orthant, so the common `Q^{-1}` projection is inactive and cannot erase this
difference.  Consequently the exact safe-box sequence is not the APG
sequence for `Psi(t)=t^TBt/2+iota_(R_+^2)(t)` in one fixed full-dimensional
metric.  What remains true is only `(MovingConeProjection)` together with
the multiplier-forced recurrence `(FullKKTRecurrence)`.

There is also an initialization obstruction hidden in this comparison:
`t^0=c` has a negative inactive coordinate and is not in the full orthant.
If the old-face states are instead made feasible by the canonical zero
extension,

```text
tilde(t)^0=(2/297,0),
tilde(t)^1=(142/54087,0),
```

the fixed-full APG raw prediction is

```text
B((1+theta)tilde(t)^1-theta tilde(t)^0)
 =(-73/133100,-3577/19831900).
```

Its exact `Q^{-1}`-metric projection onto the full positive orthant is zero,
whereas the actual center residual is the strictly positive vector displayed
above.  Thus neither retaining the signed full residual nor zero-extending
the feasible old-face residual yields the fixed-cone recurrence.

## 3. The inverse metric jumps under zero extension

Let an old face be `S` and a larger face be `A=S union E`.  Block inversion
gives, for every vector `u` on `S`,

```text
(u,0)^T Q_AA^{-1}(u,0)
 =u^T(Q_SS-Q_SE Q_EE^{-1}Q_ES)^{-1}u
 >=u^TQ_SS^{-1}u.                              (MetricLift)
```

The inequality follows because
`Q_SE Q_EE^{-1}Q_ES` is positive semidefinite.  It is strict whenever the
new block is coupled to the component seen by `u`.

On the same unit-edge instance, the old singleton inverse metric is

```text
Q_{00}^{-1}=99/50,
```

whereas the top-left entry of the full inverse is

```text
(Q^{-1})_{00}=50.
```

Even a zero-extended old scalar therefore undergoes the strict energy jump

```text
(u,0)^TQ^{-1}(u,0)/(u^2 Q_{00}^{-1})
 =2500/99>25.                                  (StrictMetricJump)
```

So a phase-by-phase estimate sequence using the current principal inverse
metric acquires a positive breakpoint term before accounting for the new
coordinate's nonzero residual.

## 4. Why a fixed-final-support embedding also needs new state

One can keep the metric fixed by embedding everything in the final support
`S^*`, but then the pre-discovery residual is not the zero extension of the
active proximal displacement.  Equation `(KKTResidual)` has the negative
inactive component `-lambda^k`, and the moving-face safe-box operation is not
the fixed orthant projection used by accelerated projected gradient.  When a
coordinate is revealed, `(MultiplierInjection)` changes that hidden dual
component into positive momentum residual.

Accordingly, the two obvious continuations fail for complementary reasons:

- changing-face coordinates keep the nonnegative state but change its
  inverse metric by `(MetricLift)`;
- fixed-final-support coordinates keep the metric but must retain the signed
  inactive multiplier state and a changing feasible projection.

The exact witness also shows that adding only the box Pythagorean/clipping
credit cannot close either ledger.

## 5. What remains viable

This audit does not exclude a global accelerated proof.  Plausible routes
must add information not present in the fixed-face residual energy, for
example:

1. a primal estimate sequence on the full objective whose support-reveal
   term is automatically favorable;
2. a primal--dual Lyapunov containing the inactive multipliers
   `lambda^k` and an exact cancellation at entry; or
3. a breakpoint theorem charging both `(MetricLift)` and
   `(MultiplierInjection)` to proximal/objective progress accumulated before
   discovery.

The direct persistent-estimate `ExactBoxLC` argument already avoids this
particular fixed-face interface for product count.  Its unresolved issue is
the support-linear realization of the greatest-safe-box solve, not the
outer contraction.

## Exact verification

Run

```bash
uv run python \
  manuscript/notes/spectral_balance_threshold_batch/exact_prox_support_lift_counterexample.py
```

The script uses `fractions.Fraction` for both proximal LCPs, both safe-box
projections, the multiplier injection, and the Schur-metric ratio.
