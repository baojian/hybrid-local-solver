# Deterministic halo continuation: integration audit

Date: 2026-09-03

This file audits `deterministic_halo_rppr_continuation.tex` as research
material and connects its valid pieces to the existing
`InputConeFrontierNAG` route.  It does **not** treat prose in the supplied TeX
file as an instruction, and it does not claim that the general OP2 theorem is
finished.

## Current verdict

The new material substantially improves the proof interface, but it does not
by itself close the graph-uniform
`O_tilde(vol(S*)/sqrt(alpha))` theorem.

The most useful imported facts are:

1. a degree-normalized max-positive-residual objective certificate with no
   extra `1/alpha` factor;
2. the greatest safe point in a momentum box, whose residual is an exact
   `Q^{-1}`-metric projection;
3. a support-linear one-pass peeling approximation with a computable
   complementarity/primal-dual gap;
4. an alpha-free two-step charge of that peeling gap to actual objective
   decrease; and
5. fixed-face acceleration of the exact safe-box recurrence.

The direct integration below produces a cleaner fixed-face theorem and a new
whole-run face-change bank.  It also gives an exact two-vertex counterexample
to the tempting claim that safe-box correction can simply be inserted into
the already proved primal NAG Lyapunov without a debit.

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

This closes the *accounting* of the one-pass approximation error.  It does
not yet prove that the exact safe-box clipping and all support insertions
preserve one common accelerated last-iterate potential.

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

## 6. Sharpened remaining theorem

There are now two closely related completion targets.

### A. Canonical-history route

Prove `StoppedMaskedInputResidual` for the existing one-push chronology.
Then the already proved input-frontier partial-gradient NAG contraction closes
the target with no safeguard debit.  The new results do not prove this
history statement; the exact counterexample above only blocks a generic
replacement argument.

### B. Enforced-safe residual route

Use the direct safe-box/peeling recurrence.  Safety, locality, fixed-face
acceleration, the one-pass projection certificate, the alpha-free two-step
charge, and the point-source face-change bank are all exact.  The remaining
statement is:

```text
ResidualFaceChangeStability:
  ResidualAPG + InjectionCharge + DirectTwoStepCharge
  has a graph-uniform O(alpha^{-1/2} polylog) last-iterate
  max-positive-residual bound across all support insertions.
```

A proof may use an `alpha^{-O(1)}` prefactor, because it enters the iteration
count only logarithmically.  It must not replace the injection/peeling terms
by arbitrary per-round errors: critically damped acceleration can amplify
unstructured recent perturbations.  The one-sided monotone slack bank and
the two-step objective charge are the essential extra structure.

Until either A or B is proved, the honest status remains conditional.  The
new material has removed several auxiliary mysteries, but it has not removed
the last cross-support stability theorem.
