# Zero-start repeated peeling: a whole-run `Omega(1/alpha)` obstruction

Date: 2026-09-04

## Verdict

**Proved here.**  Consider the natural certified implementation of
`SafeBoxLC` which, at every outer trial, repeats the literal one-pass
`PeelingLC` map toward that same trial until

```text
(1+s) zeta <= A,                    s=sqrt(alpha),
```

and only then performs the linear-coupling update.  On a canonical
point-source instance consisting of one unit edge, started from the required
zero state, this implementation performs

```text
Omega(1/s^2)=Omega(1/alpha)
```

peeling passes before reducing the objective gap by even a fixed constant
factor.  Each pass scans the two-vertex support, so this is also a charged
work lower bound for this particular implementation.  It rules out a
whole-run `O_tilde(1/s)` amortization of restarted peeling, not merely a
constant-pass implementation of one supplied outer state.

This result does **not** refute `ExactBoxLC`, a signed persistent LCP method,
or another approximate projection routine.  It refutes only the explicitly
named recipe which restarts the one-pass peeling dynamics from its current
feasible correction on every inner pass.

## Canonical zero-start family

Let `0<s<=s_0`, `alpha=s^2`, and take the simple connected graph consisting
of one unit edge.  With source vertex zero and

```text
rho=1/2-s,
```

the RPPR obstacle data are

```text
Q = [ a  -b ],       a=(1+s^2)/2,       b=(1-s^2)/2,
    [ -b  a ]

c=s^2(1/2+s,-1/2+s),
x_rho^*=(s+s^2/2,s-s^2/2).
```

The optimum is strictly positive.  Run `SafeBoxLC` from `x_0=z_0=0`, using
the trial

```text
y=(x+s z)/(1+s)
```

and repeated peeling to the first exact `ABoxStop` success.

The first update has singleton support.  The second admits the other endpoint
and gives, by direct substitution,

```text
c-Qx_2=R_2(1,1),       z_2-x_2=(V_2,W_2),

R_2=s^3(1-s)(2+s-2s^2)/2,
V_2=s(1-s)^2(1+2s)/2,
W_2=s^2(1-s)(3-2s)/2.                 (InitialFullState)
```

Thus, with

```text
kappa=R/(s^2 V),       r=W/V,
```

the zero-start full-support state satisfies

```text
(kappa_2,r_2) -> (2,0)                 as s -> 0.
```

Every quantity is rational when `s=1/m`.

## Exact two-dimensional invariant

### Lemma 1

After the second outer update, every later state has the form

```text
c-Qx_k=R_k(1,1),       z_k-x_k=(V_k,W_k),
```

with `R_k,V_k>0` and `W_k>=0`.

### Proof

Suppose a repeated-peeling inner solve accepts total movement `p` and ends
with safe slack `t=c-Q(x+p)>=0`.  The full-support linear-coupling update is

```text
x^+=x+p+t,
z^+=(1-s)z+s(x+p)+t/s.
```

Since

```text
I-Q=b [ 1  1 ],
      [ 1  1 ]
```

one has

```text
c-Qx^+=(I-Q)t=b(t_0+t_1)(1,1).
```

Moreover

```text
z^+-x^+=(1-s)(z-x-p+t/s)>=0.
```

The initial state is `(InitialFullState)`, proving the invariant.

Positive homogeneity permits division by `V_k` after every round without
changing any event time or stopping decision.  Consequently `(kappa,r)` is
the complete projective state.

## Why the exact-box outer recurrence is not the right limit

One tempting argument is to claim that every inner episode reaches the exact
greatest safe box.  That claim is false, even on this zero-start family.  If
an otherwise admissible supplied state has `kappa=2` and fixed
`0<xi<1`, `r=xi s`, the first pass exhausts coordinate one and has

```text
(1+s)zeta/A -> xi.
```

Thus that pass is accepted nonexactly.  Nonexact acceptance also occurs at
isolated later rounds of genuine zero-start finite runs.  There is therefore
no uniform exact-output boundary lemma and no single exact-box outer ODE.

The lower bound survives because every accepted episode exhausts coordinate
one, and its possible shortfall from the exact box is quantitatively bounded
by `ABoxStop`.  The rest of the proof uses that controlled recurrence and no
ODE convergence claim.

## Accepted-output normal form

Work on the compact rectangle

```text
K={1.8<=kappa<=2.5, 0<=r<=0.55}.               (OuterRectangle)
```

All assertions below hold for one common sufficiently small `s_0` and every
`0<s<=s_0`.  Put

```text
q=s/(1+s),       u=qV(1,r),       R=s^2V kappa.
```

### Lemma 2 (no acceptance before coordinate-one exhaustion)

Every repeated-peeling episode started from a state in `K` fails `ABoxStop`
at every pass output at which coordinate one still has positive remaining
direction.  Consequently its accepted total movement satisfies

```text
p_1=u_1=qVr.                                  (Exhaustion)
```

### Proof

At the first pass, coordinate zero is the first row to hit zero: its pressure
is `qV(a-br)>0`, while the other pressure is `qV(-b+ar)<0`.  If coordinate
one later hits zero before the end of the pass, the output has

```text
t=(h,0),       e=u-p>0.
```

The same event word repeats from such an output until coordinate one is
exhausted.  Indeed, at any such cumulative output `t_1=0` gives

```text
h=t_0=p_1-p_0=(R-s^2p_0)/a,
e_0-e_1=u_0-u_1+h>0.                          (OneRowState)
```

In fact `e_0-e_1>=qV(1-r)>=0.44sV` and `e_0<=qV<=sV`.
Consequently `-be_0+ae_1<0`, while `ae_0-be_1>0`: row zero again hits
first.  Coordinate one then either hits later, returning to
`(OneRowState)`, or exhausts its remaining direction.

It remains to rule out `ABoxStop` at `(OneRowState)`.  Uniformly on `K`,

```text
e_0 >= qV(1-r) >= (0.44+o(1))sV,
h   >= s^2V(kappa-s)/a >= (3.5-o(1))s^2V,
```

and hence `zeta=e_0h>1.5s^3V^2` for small `s`.  On the other hand, the exact
eigenbasis identity

```text
(1/2)p^TQp=(s^2/4)(p_0+p_1)^2+(1/4)(p_0-p_1)^2
```

together with `p<=u`, `p_1-p_0=h<=R/a<=5s^2V`, gives

```text
A/(s^3V^2)
 <= (1+r^2)/2+O(s) <0.7+O(s).
```

Therefore `(1+s)zeta>A`.  The only other pass outcome exhausts coordinate
one, proving `(Exhaustion)`.

Define the exact-box continuation after `(Exhaustion)` by

```text
H=(kappa-qr)/a,
T=s^2VH,
p_0^box=p_1+T,
delta=p_0^box-p_0,       gamma=delta/(s^2V).
```

Feasibility gives the following exact accepted-output normal form:

```text
p/V=(qr+s^2(H-gamma), qr),
t/V=s^2(a gamma,H-b gamma),                  (AcceptedForm)
0<=gamma<=H/b.
```

Here `gamma=0` is exact-box acceptance and `gamma>0` is nonexact acceptance.
The equality follows simply by observing that a further movement `delta` in
coordinate zero changes the slack by `-Q(delta,0)` and reaches `(0,T)`.

### Lemma 3 (the ABox control)

Uniformly for accepted outputs from `K`,

```text
0<=gamma<=G(r)+O(s),
G(r):=(1+r^2)/(1-r).                          (GammaBound)
```

### Proof

The feasibility bound in `(AcceptedForm)` already gives
`gamma<=H/b=O(1)`.  Consequently `(AcceptedForm)` gives the uniform
expansions

```text
zeta/(s^3V^2)=gamma(1-r)/2+O(s),
A/(s^3V^2)=(1+r^2)/2+O(s).
```

The quadratic part of `A` is `O(s^4V^2)` by the displayed eigenbasis
identity; the momentum part supplies the second expansion.  Since
`1-r>=0.45`, `ABoxStop` now gives `(GammaBound)`.

## A controlled outer recurrence from zero start

Substitution of `(AcceptedForm)` into the full-support update gives the exact
rational transition

```text
D=1-qr-s^2(H-gamma)+a s gamma,

r^+=[r(1-q)+s(H-b gamma)]/D,

kappa^+=b(H+s^2 gamma)/[(1-s)D].             (ControlledOuterMap)
```

Uniform expansion on `K`, using `(GammaBound)`, gives

```text
(r^+-r)/s
 =2kappa-r+r^2-gamma(1+r)/2+O(s),

(kappa^+-kappa)/s
 =kappa(1+r)-r-kappa gamma/2+O(s).            (ControlledDrift)
```

This is a controlled difference inclusion, not an assertion that `gamma`
has a limit.  It is nevertheless enough.  On `0<=r<=0.55`,

```text
G(r)<=2.895,
2(1.8)-r+r^2-G(r)(1+r)/2>1.10,
1+r-G(r)/2=(1-3r^2)/[2(1-r)]>0.
```

Consequently, after reducing `s_0` once, every step in `K` obeys

```text
1 <=(r^+-r)/s<=5.1,
-0.65<=(kappa^+-kappa)/s<=4.                 (DriftBounds)
```

The exact zero-start values satisfy

```text
1.95<=kappa_2<=2.01,       0<=r_2<=4s
```

for all sufficiently small `s`.  Bootstrap `(DriftBounds)` for
`0<=n<=floor(0.1/s)`.  Before a first exit from `K`, they imply

```text
1.885<kappa_(2+n)<2.41,
0<=r_(2+n)<0.52,
```

which is strictly inside `K`; hence no exit exists.  They also imply

```text
r_(2+n)>=0.05
```

whenever `ceil(0.06/s)<=n<=floor(0.1/s)`.  This establishes the required
whole zero-start outer prefix directly, including its initial boundary
layer, without selecting a limiting `gamma` or invoking an ODE.

## Root-scale passes on root-scale many rounds

Fix a round in the last displayed interval.  Thus

```text
1.8<=kappa<=2.5,       0.05<=r<=0.55.         (PassRectangle)
```

On the first peeling pass, the row-zero hitting fraction is at most `12s`.
At that event the row-one slack is at most `8.5s^2V`; since
`u_1>=0.049sV`, row one also hits during this pass for sufficiently small
`s`.  Its total movement is at most `24s^2V`.

Every later nonterminal pass starts from `(OneRowState)`.  Its row-zero
hitting fraction is at most

```text
h/[a(e_0-e_1)]<=24s.
```

If row one then hits, its total movement is
`theta e_1+theta(b e_0-ae_1)/a=theta(b/a)e_0`.  If it exhausts instead, the
failure to hit gives the same quantity as an upper bound on `e_1`.  Thus in
either case that pass moves coordinate one by at most `24s^2V`; use the
common bound `40s^2V` for all passes.

Lemma 2 requires total coordinate-one movement

```text
p_1=qVr>=0.049sV.
```

Therefore each such outer round uses at least `1/(1000s)` peeling passes.
The interval contains at least `0.03/s` outer rounds, so the prefix uses at
least

```text
1/(40000s^2)                                           (PassLowerBound)
```

passes for all sufficiently small `s`.

Finally, this prefix is required even for a fixed relative objective target.
On the full-support invariant,

```text
x_rho^*-x=(R/s^2)(1,1),
phi(x)-phi(x_rho^*)=R^2/s^2.
```

From `(ControlledOuterMap)`, `H<=5`, and `gamma>=0`,

```text
V^+/V=(1-s)D
 >=(1-s)(1-0.55s-5s^2)>=1-1.7s.
```

Thus throughout the prefix `V` remains at least `0.36s`, because
`V_2/s->1/2`; also `kappa>=1.8`.  The gap is consequently at least
`0.4s^4`, while

```text
phi(0)-phi(x_rho^*)=5s^4/4.
```

In particular it remains above one quarter of the initial gap throughout
the prefix.  Combining this fact with `(PassLowerBound)` proves the claimed
`Omega(1/alpha)` whole-run lower bound.

## Consequence for the proof program

The following implementation route is now **Refuted**:

```text
for every SafeBoxLC outer trial:
    restart PeelingLC from the current feasible point toward that trial;
    repeat until ABoxStop;
    perform the LC update.
```

The supplied-state root-scale obstruction was not enough to reach this
conclusion, because one expensive inner episode could fit inside the total
target budget.  The zero-start family above forces a root-scale episode on a
root-scale number of genuine outer rounds.  Therefore global movement
amortization does not rescue restarted peeling.

Live alternatives are narrower:

1. maintain a signed persistent correction/response state rather than
   restarting the peeling geometry;
2. realize the exact greatest-safe-box projection through a genuinely
   persistent deterministic inverse primitive; or
3. use a different approximate projection certificate whose progress is not
   generated by repeated one-pass freezes.

## Exact finite verification

Run

```bash
uv run python \
  manuscript/notes/spectral_balance_threshold_batch/zero_start_repeated_peeling_exact.py \
  --m 128
```

The checker uses `fractions.Fraction` for `(InitialFullState)`, every peeling
event, every `ABoxStop` comparison, and every outer update.  Its default run
checks the zero-start prefix through outer time approximately `0.1`; decimal
projective states are display-only.  Larger `m` causes rapid rational
denominator growth, so the exact checker is a finite identity guard rather
than the asymptotic proof, which is the uniform controlled-recurrence
argument above.
