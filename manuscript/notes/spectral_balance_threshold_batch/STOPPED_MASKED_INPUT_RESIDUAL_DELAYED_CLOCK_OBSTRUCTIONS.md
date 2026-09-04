# Delayed path and fresh-star clock obstructions

Date: 2026-09-04

This is an unregistered companion note for the canonical zero-start,
one-push-maximal stopped masked-input-residual recurrence. It records two
local lemmas and separates them from finite floating-point search evidence.
It does not update the exact beta atlas.

## Normalization

Use the random-walk degree-coordinate operator

\[
 A=aI-\delta P,
 \qquad
 a=\frac{1+s^2}{2},
 \qquad
 \delta=\frac{1-s^2}{2},
 \qquad a+\delta=1.
\]

After multiplying states and widths by the source degree, every nonsource
load is \(-g\), where

\[
 g=\frac{s^2r}{2}>0,
 \qquad r=d_{\rm source}\rho.
\]

Only newly admitted exterior rows receive an immediate diagonal push during
maximal append closure. Rows admitted in an earlier append batch are not
pushed again later in the same closure.

## Lemma 1: a pendant path is not a cost-free same-product delay

Let a dormant unit path be attached to a certified port \(v_0\):

\[
 v_0-v_1-v_2-\cdots-v_L.
\]

Suppose \(v_1\) is admitted during an append closure with positive residual
\(r_1\), and suppose the closure subsequently advances along the path one
vertex per append batch. For \(2\le j<L\), the internal degree is two and
the new residual obeys the exact recurrence

\[
 r_j=-g+\lambda r_{j-1},
 \qquad
 \lambda=\frac{\delta}{2a}<\frac12.
\]

Consequently

\[
 r_j
 =\lambda^{j-1}r_1
  -g\frac{1-\lambda^{j-1}}{1-\lambda}.
\]

In particular, reaching internal vertex \(v_j\) requires

\[
 r_1>
 g\frac{\lambda^{-(j-1)}-1}{1-\lambda},
\]

which grows exponentially with \(j\). At the terminal degree-one leaf the
last coefficient is \(\delta/a\), rather than \(\delta/(2a)\), but this does
not remove the internal attenuation.

Moreover, the residual returned immediately to \(v_0\) is exactly the flux
from the first new push,

\[
 \frac{\delta}{d(v_0)}\frac{r_1}{a}.
\]

Pushes at \(v_2,v_3,\ldots\) stop at their already certified predecessors in
that closure. They do not propagate back to \(v_0\) until later products.
Thus increasing the path length neither increases the same-product packet
seen by the core nor creates a free temporal clock. A long path can only be
a multi-product relay, paid for by geometric attenuation and the repeated
negative load.

### Proof

When a new internal row \(v_j\) has only its newly pushed predecessor
\(v_{j-1}\) nonzero, its lower residual is

\[
 -g+\frac{\delta}{2}\frac{r_{j-1}}a.
\]

This proves the recurrence and its geometric solution. The algorithm's
append rule pushes only the new batch. Hence the push of \(v_j\) changes the
residual of \(v_{j-1}\), but does not push \(v_{j-1}\) again. Induction over
the append batches proves the flux claim. All statements are exact.

## Lemma 2: same-closure release from a fresh star port needs a large jump

Let an inactive port \(p\) have one upstream neighbor \(u\) and \(k\) dormant
degree-one leaves. Thus \(d(p)=k+1\). Suppose \(p\) is first admitted by the
pre-gradient input test in product \(t\). Write \(q_u^-\) for the upstream
input state at the preceding test and \(q_u^+\) for its value at the current
test. Then

\[
 q_u^-\le \frac{(k+1)g}{\delta},
 \qquad
 q_u^+>\frac{(k+1)g}{\delta}.
\]

If at least one leaf is also released by the subsequent append closure in
the same product, then necessarily

\[
 q_u^+>\frac{(k+1)g}{\delta^2}
       \ge \frac{q_u^-}{\delta}.
\]

Since \(\delta<1/2\), a nonzero upstream input state must therefore grow by a
factor strictly larger than \(1/\delta>2\) between these two tests. In a
fixed prefix with \(q_u\le M\), same-closure release is impossible whenever

\[
 k+1\ge \frac{\delta^2M}{g}.
\]

### Proof

While the port and leaves are inactive, its input residual is

\[
 \xi_p=-g+\frac{\delta}{k+1}q_u.
\]

The two first-admission inequalities follow immediately. Let \(e_p\) be
the port's lower residual at the active diagonal push. The input-cone order
gives \(e_p\le\xi_p\). A leaf can enter the subsequent append closure only
if

\[
 -g+\delta\frac{e_p}{a}>0.
\]

It is therefore necessary that

\[
 \frac\delta a
 \left(-g+\frac{\delta}{k+1}q_u^+\right)>g.
\]

Using \(a+\delta=1\) gives
\(q_u^+>(k+1)g/\delta^2\). Combining this with the preceding nonadmission
inequality proves the jump and fixed-prefix bounds.

## Consequence for a near-half family

These lemmas rule out two naive arguments.

1. Merely making a pendant path longer cannot create an arbitrarily delayed,
   same-product residual packet approaching one half.
2. Merely sending \(k\) to infinity at a completely dormant star port cannot
   produce a fresh one-product release inside a fixed bounded prefix.

They do **not** rule out a universal near-half construction. Three escape
routes remain mathematically open:

- keep the port active for several products while only its leaves remain
  dormant;
- scale \(g=s^2r/2\) to zero and let the trigger phase grow with \(k\);
- replace a whole clock branch while preserving its finite-prefix interface
  response at the degree-two source.

The first route is the one compatible with the exact dormant-star packet
bound already recorded in BETA_STOP_CLOCK_GLUING_AUDIT.md. It requires
simultaneously controlling the leaf trigger, port input residual, earlier
stop maxima, and remote strict failure.

## Finite search evidence, not proof

At target \(\beta=.487\), floating-point scans based on the exact 27-vertex
beta-.486 relay found no strict failure in the following bounded families:

- one pendant path of length \(1\) or \(2\) at every nonsource vertex, eight
  root scales, and 71 threshold values: 29,536 runs;
- one \(k\)-leaf star for
  \(k\in\{2,3,4,6,8,12,16\}\), every nonsource port, four root scales, and 36
  threshold values: 26,208 runs.

After the clock-only change deleting (5,8) and adding (4,10), further scans
found no target-.487 failure among

- paths of length \(1,2,3\): 19,656 runs;
- the same bounded star family: 26,208 runs;
- all 240 simple two-edge switches inside the clock branch that preserve
  every involved vertex degree, at 81 threshold values: 19,440 runs.

These computations only motivate the structural lemmas. They are not an
exhaustive graph search and do not certify nonexistence of a delayed clock.
Any future numerical hit must be replayed by the Fraction-exact tracer.

The removable zero-root recurrence permits a more stable finite audit, with
states scaled before taking \(s\to0\). On the later branch-boundary topology

~~~text
BETA_04864_CLOCK_REWIRE_EDGES - {(1,11)} + {(1,4)},
~~~

the unmodified graph at its optimized threshold has the limiting failure
cell approximately

~~~text
[0.4864752557..., 0.4865654337...).
~~~

At target beta=.487, the following zero-root scans found no failure:

- one pendant path of every length \(1,\ldots,8\), at every nonsource port,
  with 251 evenly spaced rho_scale values in [.005,.03]: 52,208 runs;
- one star with
  \(k\in\{1,2,3,4,5,6,8,10,12,16,24,32,48,64,96,128\}\), at every
  nonsource port, with 126 threshold values in the same interval: 52,416
  runs.

The initial 171-value coarse scan of two leaves at distinct ports also
reported zero failures in 55,575 runs.  That negative observation was later
**falsified by a finer rho scan**: attaching leaves at ports `4` and `15`
has the Fraction-exact zero-root cell

~~~text
[0.48618996153896166..., 0.4870260368530394...).
~~~

Thus this computation is itself useful evidence that an evenly spaced rho
grid can miss a very narrow valid cell.  It must not be quoted as an
obstruction, even within the bounded two-leaf family.  See
`STOPPED_MASKED_INPUT_RESIDUAL_BETA_0487_TWO_LEAF_ZERO_ROOT_LIMIT.md`.

After the exact cover advanced to \(0.4865812687\ldots\), a tighter audit at
target beta=.48659 also found no failure:

- paths of every length \(1,\ldots,8\), at every nonsource port, with 151
  threshold values in [.0144,.0159]: 31,408 runs;
- stars at every nonsource port, with
  \(k\in\{1,2,3,4,5,6,8,10,12,16,24,32,48,64,96,128,192,256\}\) and 126
  threshold values in [.014,.0165]: 58,968 runs.

A separate zero-root neighborhood audit at target beta=.48657 tested every
connected one-delete/one-add internal clock-branch topology around the same
branch-boundary graph: 39 existing clock edges times 52 nonedges, with 86
threshold values in [.0147,.01555]. None of the 168,474 evaluations retained
a failure, although the unmutated base does fail at its separately optimized
threshold. This is finite grid evidence only. It is not a continuous-rho
local-optimality theorem, and it does not include multi-edge or
growing-topology families.
