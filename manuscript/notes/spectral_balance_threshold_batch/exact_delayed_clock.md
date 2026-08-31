# Exact delayed-event certificate for a canonical moving projected-NAG trace

## Theorem and scope

There is a finite simple, connected, undirected, unit-edge graph on 34
vertices, a point source at vertex 0, and legal canonical parameters

\[
 \alpha={1\over1000},\qquad \rho={1\over100000}<1/d_0,
 \qquad d_0=1,\qquad \varepsilon_{\rm obj}=10^{-20},
\]

for which the exact-positive lower-envelope projected-NAG moving-face
recurrence has publication iterations

\[
 \boxed{0,1,2,3,4,38}.
\]

After the event at iteration 4, iterations 5 through 37 are all exactly
quiet although a nonempty event occurs at 38.  Hence the claim “every
nonterminal face expansion is followed by another publication in at most one
product” is false for this named canonical recurrence.

This is a chronology counterexample for a proposed immediate-publication
lemma.  It is not a lower bound for every deterministic RPPR algorithm, and
it does not show that the total moving-face clock exceeds
\(\widetilde O(1/\sqrt\alpha)\).

The graph has 69 edges and volume 138, so
\(\rho\operatorname{vol}(V)=0.00138<1\).  Exact rational elimination of the
full degree-coordinate system gives a strictly positive solution at all 34
vertices; hence the canonical optimal support is \(S^*=V\).

## Exact arithmetic reduction

Let

\[
 Q=aI-cD^{-1/2}AD^{-1/2},\qquad
 a={1+\alpha\over2},\quad c={1-\alpha\over2},
\]

and let the canonical normalized load be

\[
 \ell=-\alpha\rho D^{1/2}{\bf1}
       +{\alpha\over\sqrt{d_0}}e_0.
\]

Write every normalized state as \(x=D^{1/2}y\).  On a current face \(U\),
one NAG product becomes

\[
 \bar y=y+\beta(y-y^-),\qquad
 y_i^+=c\left(\bar y_i+{1\over d_i}
              \sum_{j\in U:\,ij\in E}\bar y_j\right)+b_i,
 \tag{1}
\]

where

\[
 b_i=-\alpha\rho+{\alpha\over d_0}{\bf1}_{i=0},
 \quad
 \sqrt\alpha={\sqrt{10}\over100},
 \quad
 \beta={1-\sqrt\alpha\over1+\sqrt\alpha}
       ={1001-20\sqrt{10}\over999}.
 \tag{2}
\]

The auxiliary reconstruction factor is

\[
 {1-\sqrt\alpha\over\sqrt\alpha}=10\sqrt{10}-1.       \tag{3}
\]

Thus every state, retraction shift, lower-envelope coordinate, and residual
lies in \(\mathbb Q(\sqrt{10})\).  In these coordinates the sign of the
normalized exterior residual equals the sign of

\[
 \widehat r_i=d_i b_i-
 \left(a d_i\underline y_i-c\sum_{j:\,ij\in E}\underline y_j\right).
 \tag{4}
\]

For \(z=p+q\sqrt{10}\), its sign is decided without approximation by
comparing \(p^2\) and \(10q^2\) after the trivial same-sign cases.  Every
maximum, clipping branch, retraction shift, and publication decision is
therefore exact.

## Certified trace

The edge list is embedded in `exact_delayed_clock.py`.  Exact field
evaluation gives

\[
\begin{array}{c|l}
t&\text{new vertices}\\ \hline
0&1\\
1&2\\
2&3,20\\
3&4,9,11,17,18,19,21,28\\
4&5,8,10,12,13,14,16,22,24,25,27,29,30,32,33\\
38&6,7,15,23,26,31.
\end{array}
\]

The minimum positive rationalized residual in the last batch is

\[
 7.55507171300928\cdot10^{-5}>0.
\]

For every published coordinate, the verifier also checks exactly that the
normalized residual exceeds the manuscript gate

\[
 {\vartheta\over2}={1\over16}
   \sqrt{\alpha\rho\varepsilon_{\rm obj}}.
\]

Consequently the batches are unchanged if exact positivity is replaced by
this finite canonical threshold.  For every iteration
\(t=5,\ldots,37\), every exterior rationalized residual is nonpositive; the
largest is exactly represented and has value

\[
 -2\cdot10^{-8}<0.
\]

The separation is strict on both sides and is not a floating-point branch
artifact.

The original recurrence permits a quiet early stop when the interior
degree-scaled residual norm is at most \(10^{-10}\).  The verifier compares
the squared norm exactly on every quiet step.  Its minimum ratio to the
squared stopping threshold is

\[
 4.09312681762\cdot10^{11}>1,
\]

so no earlier termination bypasses the delayed event.  It also asserts that
the lower envelope is an active lower subsolution at every iteration.

## Reproduction

Run

```text
python3 exact_delayed_clock.py
```

The verifier uses exact `Fraction` coefficients for
\(p+q\sqrt{10}\), asserts the complete ordered batch list, certifies all 33
quiet iterations, and checks that the final face contains all 34 vertices.
It also checks graph simplicity/connectivity, the positive full-face exact
solution, the lower-subsolution inequalities, the finite publication gate,
and every early-stop branch.
