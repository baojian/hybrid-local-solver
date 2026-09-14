# The two identities that turn acceleration into local work

This expands the algebra behind the complete proof's comparison lemma and
selected-flow argument. It introduces no new algorithm or hypothesis. All
vectors below are mathematical analysis objects unless explicitly identified
as stored states. The main theorem, repair and complete access ledger remain
in [the proof](output/pdf/deterministic_conjecture2.pdf).

## Accelerated comparison with a single comparator

Work in any Hilbert inner product. Let `f` be one-smooth and
`mu`-strongly convex. Take `0<theta<=1`, set `theta^2=mu`, `a=1-theta`,
and put

\[
 y=\frac{x+\theta z}{1+\theta},\qquad
 g=\nabla f(y),\qquad q=az+\theta y-g/\theta,
 \qquad x^+=ax+\theta p.
\]

The only projection property needed for the chosen comparator `t` is
`<p-t,q-p> >= 0`. Expanding `q-t=(p-t)+(q-p)` gives

\[
 \|p-t\|^2\le\|q-t\|^2-\|p-q\|^2. \tag{1}
\]

The averaging identity is

\[
 x^+=y-g+\theta(p-q).
\]

Indeed, substituting the definition of `q` into the right side leaves
`(1-mu)y-theta a z+theta p=ax+theta p`.
Smoothness, with `h=theta(p-q)`, yields

\[
 f(x^+)\le f(y)+\langle g,-g+h\rangle
                     +\tfrac12\|-g+h\|^2
 =f(y)-\tfrac12\|g\|^2+\tfrac\mu2\|p-q\|^2.
\]

Adding `mu/2` times (1) cancels the last term. Write
`A=a(z-t)+theta(y-t)`, so `q-t=A-g/theta`. The resulting upper bound is

\[
 f(y)+\frac\mu2\|A\|^2-\theta\langle A,g\rangle. \tag{2}
\]

Strong convexity, applied at `x` and `t` and averaged with weights `a`
and `theta`, gives

\[
 a f(x)+\theta f(t)\ge f(y)
  +\langle g,a(x-y)+\theta(t-y)\rangle
  +\frac\mu2\{a\|x-y\|^2+\theta\|t-y\|^2\}.
\]

The vector multiplying `g` is exactly `-theta A`. Combining this with
(2), and using

\[
 \|A\|^2=a\|z-t\|^2+\theta\|y-t\|^2
                         -a\theta\|z-y\|^2,
 \qquad x-y=\theta(y-z),
\]

proves

\[
 \begin{split}
 f(x^+)-f(t)+\frac\mu2\|p-t\|^2
 \le{}&a\left(f(x)-f(t)+\frac\mu2\|z-t\|^2\right)\\
 &-\frac{\mu a\theta(1+\theta)}2\|z-y\|^2.
 \end{split}
\]

Since `a(1+theta)=1-mu`, this is the exact remainder in the proof.
Nothing in the derivation requires `t` to minimize `f` or requires the
comparison energy to be nonnegative.

For the ordinary energy, `f=J`, the metric is Euclidean and `t=xi*`.
For the response energy, the metric is `Q`, the function is
`Acal(xi)=||Qxi-s||^2/2+alpha lambda w^T xi`, and `t=Q^-1 s`.
The identities `Qw=alpha w` and `Q^-1 w=w/alpha` make its metric gradient
exactly `Qxi-s+lambda w`. Its metric Hessian is `Q`, with spectrum in
`[alpha,1]`. The proof's lower-box, upper-box and mass-face signs supply
(1) for this one comparator. This explains precisely why the same stored
recurrence admits both comparisons.

## The raw mass-flow identity

Now let `xi,z` denote the actual current correction and mirror states, and
set `S=D^-1/2 A D^-1/2`, `q0=(1+alpha)/2`, `c=(1-alpha)/2`, and
`Q=q0 I-cS`. Here `A` is the graph adjacency matrix, unrelated to the
temporary vector `A` in the preceding calculation. The recurrence gives

\[
 \begin{split}
 \theta z^{\rm raw}
 &=\theta a z+(\mu I-Q)\frac{\xi+\theta z}{1+\theta}
                                              +s-\lambda w\\
 &=\frac{\theta(I-Q)}{1+\theta}z
       -\frac{Q-\mu I}{1+\theta}\xi+s-\lambda w. \tag{3}
 \end{split}
\]

The coefficient simplification uses
`a(1+theta)+mu=(1-mu)+mu=1`.
Because `I-Q=(1-alpha)(I+S)/2`, multiplication by `D^1/2` transforms
the first term into a nonnegative mass transfer. Define

\[
 V=\theta D^{1/2}z,\qquad
 K_0=\frac{I+AD^{-1}}2,\qquad
 \beta=\frac{1-\alpha}{1+\theta}\le1-\theta=a.
\]

Every column of `AD^-1` sums to one, so `K0` is column stochastic.
Also `D^1/2 S D^-1/2=AD^-1`. Equation (3) is therefore

\[
 V^{\rm raw}=\beta K_0V
       -\frac{D^{1/2}(Q-\mu I)}{1+\theta}\xi
       +D^{1/2}(s-\lambda w).
\]

For the stage minimizer `xi*`, define the slack
`r*=Qxi*-s+lambda w >= 0` and `V*=theta D^1/2 xi*`.
At the formal state `xi=z=xi*`, the raw mirror is
`xi*-r*/theta`; this is just the recurrence with `y=xi*`.
Subtracting that identity from the actual one gives

\[
 V^{\rm raw}-V^*=\beta K_0(V-V^*)+H-R^*,\qquad
 H=-\frac{D^{1/2}(Q-\mu I)(\xi-\xi^*)}{1+\theta},
 \qquad R^*=D^{1/2}r^*. \tag{4}
\]

This is an identity for the actual states. It does not assume they solve
an unconstrained linear system or remain below the exact optimum.

## Why the signed sum pays for every repeated scan

Decompose `V-V* = e-n`, where `e=(V-V*)_+` and `n=(V*-V)_+`.
Select only `I_k={i:V_(k+1,i)>V*_i}`. On this set, the projected mirror
is positive. Its lower-box normal is absent; upper-box and mass normals
can only decrease the coordinate. Equation (4) gives, on the selected set,

\[
 e_{k+1,i}+R_i^*\le\beta(K_0e_k)_i
                  -\beta(K_0n_k)_i+H_{k,i}.
\]

Sum over that set, drop the nonpositive term, and use nonnegativity and
column stochasticity for the `e_k` term. The result is

\[
 \|e_{k+1}\|_1+\sum_{i\in I_k}R_i^*
 \le\beta\|e_k\|_1+\sum_{i\in I_k}H_{k,i}. \tag{5}
\]

No unselected forcing term is added. Telescoping is valid because
`e_0=0` and

\[
 \sum_{k=0}^{K-1}(\|e_{k+1}\|_1-\beta\|e_k\|_1)
 =\|e_K\|_1+(1-\beta)\sum_{k=1}^{K-1}\|e_k\|_1\ge0.
\]

Outside the analytical core `C=supp(x*_(r/2))`, the comparator vanishes,
so selection is exactly positive kinetic support. There the slack is at
least `lambda d_i/2` in mass coordinates. Let `D_out` be the sum of the
outside-core degree volumes over **all** iterations, and let
`B_core=K vol(C) <= 2K/r`. Weighted Cauchy applied to the last term of
(5) yields

\[
 \frac\lambda2 D_{\rm out}
 \le \sqrt{(D_{\rm out}+B_{\rm core})H_2},\qquad
 H_2=\sum_k\|D^{-1/2}H_k\|^2\le18\alpha^2rK.
\]

The last inequality follows from the second energy and the commuting
spectral inequality `0 <= Q-mu I <= Q`. If `D_out>B_core`, squaring and
using `D_out+B_core<2D_out` gives `D_out<=8H2/lambda^2`.
If `D_out<=B_core`, no estimate is needed. In both cases,

\[
 \sum_k\operatorname{vol}(\operatorname{supp}z_{k+1})
 \le D_{\rm out}+B_{\rm core}
 \le\frac{8H_2}{\lambda^2}+2B_{\rm core}
 \le\frac{148K}{r}.
\]

The sum counts repeated appearances with their full degrees. An iteration
bound or a bound on distinct discovered vertices would not imply it.

For the rounded algorithm, a raw error of density at most `kappa_r` adds
at most `nu d_i` to a selected coordinate, where `nu=theta kappa_r`.
Downward mirror rounding retains the same sign argument. With exact cap
`eta`, the core satisfies `B_core<=2 eta K/r`. The proved grid budget also
bounds the effective rounding floor by `alpha^2 r eta`, so the response
estimate gives `H2<=22 alpha^2 r eta K`. If `nu<=lambda/4`, put
`W=D_out+B_core` and absorb the outside error to obtain

\[
 W\le2B_{\rm core}+\frac4\lambda\sqrt{WH_2}
   \le2B_{\rm core}+\frac W2+\frac{8H_2}{\lambda^2},
 \qquad W\le\frac{360\eta K}{r}.
\]

The primal rounding error is already reflected in the response bound for
the actual `xi`; equation (4) requires no extra term for its history.
The remaining source refreshes, reporter updates, rebases, checkpoints,
terminal scans, state disposal and output are charged separately in the
proof and [implementation map](proof_to_implementation_map.md).
