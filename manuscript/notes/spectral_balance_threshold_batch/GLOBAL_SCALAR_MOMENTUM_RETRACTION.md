# Global scalar momentum retraction: exact rate boundary

Date: 2026-09-04

This is an unregistered companion note.  It does not modify the canonical
algorithm or any shared claim registry.

## Verdict

The maximal global scalar safeguard

```text
q_gamma=x+gamma theta d,    0<=gamma<=1,
```

does enforce `MaskedInputResidual` and therefore makes every individual
partial-gradient product legal.  On a fixed full face it has an unconditional
gradient-rate fallback, but no square-root product theorem follows from the
usual NAG potential: an exact connected RPPR example makes that potential
increase even after the existing diagonal push and clamp.

No canonical zero-start slow family was found.  There is an exact reason this
negative target is at least as hard as the current central conjecture: until
the first strict retraction, the safeguarded and unsafeguarded histories are
identical.  A first `gamma<1` on a canonical executed product is already a
counterexample to `StoppedMaskedInputResidual`.  Conversely, if that claim is
true, the scalar safeguard is identically inert and inherits the conditional
`O(1/s)` rate.  Thus this modification does not bypass the history question;
it relocates it to bounding the cumulative cost after a first violation.

## Exact scalar and transition

Use the normalized variables of
`STOPPED_MASKED_INPUT_RESIDUAL_REDUCTION.md`:

```text
A=B/L=aI-K,                  a=(1+s^2)/2,
theta=(1-s)/(1+s),
e=(h-Bx)/L>=0,               d>=0.
```

On the old certified face the maximal admissible scalar is exactly

```text
gamma
 = min {1, min_(i:(Ad)_i>0) e_i/[theta(Ad)_i]}.   (1)
```

Rows with `(Ad)_i<=0` impose no upper bound.  An exterior row has `d_i=0`
and input residual `e_i+gamma theta(Kd)_i`; if it becomes positive it is
zero-admitted by the input frontier and is automatically safe.  Thus (1)
also gives the maximal scalar after input-frontier enlargement.

Put

```text
xi=e-gamma theta A d.
```

Then `xi>=0` on the gradient face and the reduced pushed transition is

```text
p^(0)=((1-a)I+K)xi/a,
d^+=[gamma theta d+xi-s p^(0)/(1-s)]_+.          (2)
```

The chronological append formula and the next-input shield are unchanged.
In particular, the safeguard provides legality but does not create a new
positive residual bank: decreasing `gamma` merely deletes a common fraction
of every coordinate's requested momentum.

### First-retraction equivalence

Start the safeguarded and original algorithms from the same canonical zero
state and use the same deterministic tie rules.  If the original product has
nonnegative input residual, `gamma=1` is feasible in (1), hence maximal.  The
two products and all subsequent deterministic pushes, admissions, and stops
are identical.  Induction proves:

```text
first safeguarded product with gamma<1
 = first original executed product violating MaskedInputResidual.   (3)
```

Therefore a canonical slowdown construction must first solve the existing
canonical counterexample problem.  This is a logical equivalence at the
first event, not evidence that no later slowdown exists.

## Exact potential debit

Let `z` be the physical NAG estimate state.  Since

```text
z=x+(1-s)d/s,
```

the scalar input retraction is exactly the estimate reset

```text
z_gamma=x+gamma(z-x).
```

For `a=x*-x` and `r=z-x`, its change in the standard estimate potential is

```text
Delta_ret
 = (mu/2)(||a-gamma r||^2-||a-r||^2)
 = (mu/2)(1-gamma)
     [2<a,r>-(1+gamma)||r||^2].                  (4)
```

This can be positive.  Safe partial-gradient NAG followed by the certified
push/clamp gives only

```text
E_(t+1) <= (1-s)(E_t+Delta_ret).                 (5)
```

There is no sign cancellation in (4) supplied by maximality of (1): one
binding coordinate controls `gamma`, while the positive cross term in (4) is
global.

The exact verifier `global_scalar_momentum_retraction_exact.py` makes this
failure literal on the smallest connected graph, one unit edge.  At
`s=1/20`, use

```text
e=(0,1),
d=(5,0).
```

The normalized retained matrix has diagonal `401/800` and edge coupling
`399/800`.  The zero-residual first row has `(Ad)_0>0`, so formula (1)
gives the maximal scalar

```text
gamma=0.
```

The safeguarded input residual is therefore `e` itself.  After the ordinary
gradient, active diagonal push, and auxiliary clamp, the exact potential
ratio is

```text
E^+/E
 =48495311162/42232935441
 =1.148281... >1>19/20=1-s.                     (6)
```

Scaling embeds the state at a strictly positive phase center of the
canonical endpoint-source edge instance with `alpha=1/799` and
`rho=1/100000`; its encoded previous state is also strictly positive.  The
center and momentum are supplied rather than generated from zero, so (6) is
a proof-interface obstruction, not a canonical runtime lower bound.

## What rate is actually established

On a fixed full face, `q_gamma` lies between the lower current `x` and the
maximal safe extrapolate.  Along this subsolution segment the quadratic
objective cannot increase.  A unit gradient step has the standard
strongly-convex factor `1-mu/L=1-s^2`, and the Stieltjes lower push is
objective-improving.  Hence the safeguarded method retains the unconditional
fallback

```text
f(x_t)-f(x*) <= (1-s^2)^t [f(x_0)-f(x*)],        (7)
```

for a fixed full face.  The safe omitted-gradient argument gives the
corresponding active-face version once the true output support is fixed.
This is `O(s^-2 log(1/epsilon))`, not the desired square-root count.

To prove `O(s^-1)` one needs an additional quantitative statement such as

```text
sum_t positive_part(Delta_ret,t)
    <= O(1) times the accelerated potential decrease,
```

or a root-window lower bound on accepted momentum.  Formula (6) rules out a
per-product version for arbitrary safe states.  A canonical lower bound, on
the other hand, must exhibit the first event in (3) and then show that such
events recur often enough to reduce the rate.  Neither statement is proved
by the present chronology.
