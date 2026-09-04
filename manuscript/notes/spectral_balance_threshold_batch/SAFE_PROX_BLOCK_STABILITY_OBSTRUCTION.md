# Safe-prox block stability: what the present ledgers can and cannot prove

Date: 2026-09-03

This is a narrowly scoped, unregistered research note.  It does not modify
the integration audit or any shared status/claims registry.

## Verdict

The exact-prox one-pass peeling/envelope recurrence is **not refuted** here.
In particular, the five-vertex slow ray for the direct-gradient
`PeelingLC` map does not transfer to the two-primal exact-prox recurrence.
In fact, a geometric slow ray is impossible for the exact-prox peeling map:
on such a ray the momentum direction is parallel to the current error, so
the whole raw momentum trial is safe and peeling is exact.

However, the currently advertised proof interface is insufficient for a
graph-uniform square-root theorem.  No block estimate

```text
G_t <= q0 G_s + C sum_(k=s+1)^(t-1) zeta_k,
```

with `q0<1`, block length `Theta(1/sqrt(alpha))`, and universal `C`, can be
derived from only

1. exact safe-box APG,
2. feasibility of the inexact correction,
3. the complementarity product `zeta`, and
4. the alpha-free two-step peeling charge.

A canonical Perron-mode safe trajectory satisfying all four black-box
properties forces `C=Omega(1/sqrt(alpha))`.  It uses a deliberately
conservative feasible correction, not the one-pass peeling correction.
Therefore it is an obstruction to the proposed *proof reduction*, not a
lower bound for the literal peeling/envelope algorithm.  A positive proof
must use an additional peeling-specific fact, such as the oriented event
structure, a quantitative lower bound on accepted momentum, or a stronger
negative-credit Lyapunov that is not summarized by `sum zeta_k`.

## 1. No geometric slow ray for exact-prox peeling

Let `Q` be symmetric positive definite Stieltjes, let one positive face be
fixed, and write `B=(I+Q)^(-1)`.  Let `x*` be the optimum on this face and
suppose an exact geometric error trajectory has

```text
a_k := x*-x^k = lambda^k a,      a>=0,      Qa>=0,
0<lambda<1.
```

For the two-primal momentum rule with fixed `theta in [0,1)`,

```text
d_k=x^k-x^(k-1)=(lambda^(-1)-1)a_k,
y_k=x^k+theta d_k.
```

Put `gamma=theta(lambda^(-1)-1)`.  If `gamma<=1`, then

```text
c-Qy_k=(1-gamma)Qa_k>=0.
```

Thus the raw trial is already a subsolution.  More explicitly, in the
one-pass peeling construction the starting slack is `Qa_k` and the pressure
of the full requested increment is `gamma Qa_k`.  Every positive-pressure
row has hit time `1/gamma>=1`, while a zero-slack row also has zero pressure.
No coordinate freezes before the end of the pass, `zeta_k=0`, and peeling,
the maximal safe ray, and the exact safe box all return `y_k`.

The exact proximal call then gives

```text
lambda a = B(1-gamma)a.
```

Hence `a` is an eigenvector of `Q`, say with eigenvalue `nu`, and `lambda`
satisfies

```text
lambda^2 - (1+theta)/(1+nu) lambda + theta/(1+nu) = 0.       (1)
```

For the accelerated choice

```text
q=sqrt(alpha/(1+alpha)),       theta=(1-q)/(1+q),
```

and `nu>=alpha`, both roots of (1) have modulus at most `1-q`; equality is
the repeated lowest-mode root at `nu=alpha`.  If `gamma>1`, then already
`lambda<theta/(1+theta)<1/2`, which is not a slow ray.  Consequently the
exact-prox peeling recurrence has no fixed-face geometric ray with factor
`1-Theta(alpha)`.  An envelope containing the peeling or maximal-ray point
cannot be slower on the same geometric state, since its center is
coordinatewise no smaller and the Stieltjes resolvent is order preserving.

This is the precise reason the persistent auxiliary-state slow ray of the
direct-gradient `PeelingLC` map does not automatically apply: on that map
the estimate displacement need not be parallel to the primal error, whereas
two consecutive primal errors on a geometric exact-prox ray force
parallelism.

## 2. A canonical obstruction to black-box constant-coefficient absorption

Take any finite connected canonical single-source RPPR instance whose
obstacle optimum is strictly positive.  Such an instance is obtained on any
fixed connected graph by choosing `rho>0` below the minimum normalized entry
of the unthresholded PPR solution.  In normalized coordinates,

```text
Qh=alpha h,       h_i=sqrt(d_i),       Qx*=c.
```

Choose `A_0>0` small enough that all states below remain positive and define

```text
b=1/(1+alpha),       A_k=b^k A_0,
x^k=x*-A_k h,        w^k=x^k.
```

Every `x^k=w^k` is an original subsolution because

```text
c-Qx^k=alpha A_k h>=0.
```

Moreover `x^(k+1)=P_1(w^k)` exactly, so this is a legitimate exact-prox
trajectory with a feasible safeguard that discards the requested momentum.
For `d_k=x^k-x^(k-1)=alpha A_k h` and any fixed requested
`theta in (0,1]`, the correction from the raw trial back to this center is

```text
e_k=theta d_k=theta alpha A_k h,
t_k=c-Qw^k=alpha A_k h.
```

It is correction-LCP feasible (`e_k,t_k>=0`), and its computable product is

```text
zeta_k=e_k^Tt_k
      =theta alpha^2 A_k^2 ||h||^2
      =2 theta alpha G_k,
G_k=phi(x^k)-phi(x*)=(alpha/2)A_k^2||h||^2.       (2)
```

Here the raw trial itself is the exact safe-box point, and direct expansion
also gives the advertised same-round certificate

```text
phi(w^k)-phi(w_box^k)
 =G_k[1-(1-theta alpha)^2]
 <=2 theta alpha G_k=zeta_k.
```

The alpha-free two-step charge holds (as it must from the exact identity):

```text
zeta_k <= theta(G_(k-1)-G_(k+1)).                 (3)
```

Indeed, after division by `theta G_k`, (3) is the elementary inequality

```text
2 alpha <= (1+alpha)^2-(1+alpha)^(-2).
```

Now take a block of `M=ceil(c/sqrt(alpha))` rounds, with fixed `c>0`.  The
gap ratio and total debit are exactly

```text
G_M/G_0=b^(2M),
sum_(k=1)^(M-1) zeta_k/G_0
 = [2 theta/(2+alpha)](1-b^(2(M-1))).             (4)
```

As `alpha -> 0`, the first expression is `1-2c sqrt(alpha)+O(alpha)`, while
the second is `2 theta c sqrt(alpha)+O(alpha)`.  Therefore, for every fixed
`q0<1`, an inequality

```text
G_M <= q0 G_0 + C sum_(k=1)^(M-1) zeta_k
```

requires

```text
C >= (1-q0+o(1))/(2 theta c sqrt(alpha)).         (5)
```

No graph- and alpha-independent `C` is possible from the black-box
assumptions above.  The unavoidable factor is at least
`Omega(alpha^(-1/2))`.

The same obstruction survives the polylogarithmic slack in an
`O_tilde(1/sqrt(alpha))` block.  If
`M=alpha^(-1/2)L(alpha)` with any fixed polylogarithmic `L` (more generally,
with `sqrt(alpha)L(alpha)->0`), then (4) gives

```text
G_M/G_0=1-O(sqrt(alpha)L(alpha)),
sum zeta_k/G_0=O(sqrt(alpha)L(alpha)),
```

so a fixed contraction requires
`C=Omega(1/(sqrt(alpha)L(alpha)))`, which still diverges.

This example is canonical and single-source, but the safeguard `w^k=x^k`
is intentionally not one-pass peeling.  On this Perron ray the raw momentum
is safe, so literal peeling accepts it and accelerates, by Section 1.
Equation (5) therefore does not refute the literal recurrence.  It proves
that the lag-two ledger alone cannot establish its missing block-stability
premise.

## 3. The stronger normwise APG spectral loss

There is also a standard impulse calculation explaining why a generic
inexact-APG theorem is even less suitable.  On a `Q`-eigenvalue `nu=alpha`,
the unprojected residual recurrence has the repeated root `r=1-q`:

```text
Delta t_(j+1)=2r Delta t_j-r^2 Delta t_(j-1)+delta_j.
```

A single impulse gives `Delta t_j=j r^(j-1) delta`.  Its largest amplitude
over `j=Theta(1/q)` is `Theta(delta/q)`.  Since an inexact metric projection
controls `||delta||_(Q^(-1))^2`, while the following primal gap is
`Theta(||t||_(Q^(-1))^2)`, a fully generic squared-energy perturbation bound
can lose `Theta(q^(-2))=Theta(1/alpha)`.  The reachable safe-reset trajectory
above improves this to the still-fatal lower bound (5) because its
complementarity product contains the cross term with the current slack.

## 4. Exact status of the literal peeling/envelope method

The available facts establish:

- exact safe-box APG has the square-root product count, including arbitrary
  support growth when the persistent estimate state is used;
- exact-prox one-pass peeling has the alpha-free two-step charge;
- a direct-gradient `PeelingLC` slow ray is not an exact-prox slow ray;
- no proof that treats peeling only through `zeta_k` and (3) can supply the
  universal constant `C` required by lag-two absorption.

They do **not** establish either a square-root round bound or an
`Omega(1/alpha)` lower bound for the literal exact-prox
peeling/barrier/reflection envelope from zero.  Closing the positive result
requires a peeling-specific block theorem beyond the current scalar debit,
for example a statement that persistent loss of accelerated momentum forces
a proportionate oriented-edge debit before a low mode can survive.  A
negative result would require a genuinely time-varying or growing-face
construction; a fixed geometric slow ray is ruled out above.
