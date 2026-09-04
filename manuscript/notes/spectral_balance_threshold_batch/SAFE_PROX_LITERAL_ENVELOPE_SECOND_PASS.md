# Literal exact-prox peeling envelope: second-pass audit

Date: 2026-09-04

This is a narrowly scoped, unregistered companion note.  It does not modify
the integration audit or any shared README, STATUS, CLAIMS, or results
registry.

## Verdict

No counterexample to the literal zero-start exact-prox
peeling/barrier/reflection envelope was found.  The direct-gradient
five-vertex slow graph returns to the accelerated scale under exact proximal
updates, and all tested growing-face structured families have a uniform
accelerated-length block contraction.

There is one new rigorous peeling-specific lemma.  The oriented
replenishment formula can be rewritten exactly as a Dirichlet-plus-total-
variation functional of the freeze-time field.  After retaining the
`u^T t` term discarded by the scalar two-step charge, the *entire weighted
freeze-time variation* is charged to two-step objective decrease with no
factor depending on `alpha` or the graph.

This stronger ledger still does not complete the rate proof.  Arbitrary
freeze-time landscapes are realizable in a single canonical peeling pass,
even with the momentum direction equal to the Perron vector.  Thus a proof
cannot assume a simple event order, bounded number of freeze layers, or a
graph-uniform Poincare inequality for the freeze field.  What remains is a
chronological response theorem showing that the exact proximal kernel turns
the paid event variation into accelerated progress before a new landscape
can be created.  The present ledgers do not provide that cross-round
statement.

## 1. Exact freeze-time variation identities

Consider one peeling pass from nested original subsolutions `x^-<=x` in the
requested direction `d=x-x^-`, up to time `theta`.  Let `tau_i in [0,theta]`
be the freeze time of coordinate `i`, with `tau_i=theta` for a coordinate
that never freezes.  Write

```text
u_i=tau_i d_i,                   accepted movement,
e_i=(theta-tau_i)d_i,           discarded movement,
t=c-Q(x+u),                     final slack,
zeta=e^Tt.
```

For an internal support edge `{i,j}`, put

```text
omega_ij=(-Q_ij)d_i d_j >= 0,
f_i=theta-tau_i.
```

The oriented-replenishment identity gives, after orienting every edge from
the larger `f` endpoint to the smaller one,

```text
zeta
 =sum_{edges} omega_ij max(f_i,f_j)|f_i-f_j|                 (1)
 =1/2 sum_{edges} omega_ij (f_i-f_j)^2
  +1/2 sum_{edges} omega_ij |f_i^2-f_j^2|.                  (2)
```

Thus the peeling gap is exactly one half weighted Dirichlet energy plus one
half weighted total variation of `f^2`.  This is an equality, not a bound.

Let `F={i:tau_i<theta}` be the actually frozen rows and define

```text
V=sum_{edges} omega_ij |f_i-f_j|
 =sum_{edges} omega_ij |tau_i-tau_j|.                       (3)
```

For a frozen row, its final slack is precisely the later-neighbor
replenishment.  Multiplying it by `u_i` and summing gives

```text
sum_{i in F} u_i t_i
 =sum_{edges} omega_ij (theta-max(f_i,f_j))|f_i-f_j|.
```

Consequently,

```text
zeta + sum_{i in F}u_i t_i = theta V,                       (4)
zeta <= theta V.                                            (5)
```

Rows that do not freeze may retain terminal slack, so using all rows in
`u^Tt` only increases the left side of the relevant progress bound.

### Event-variation two-step charge

Now assume this is round `k` of the exact-prox trajectory,

```text
x^k=P_1(w^(k-1)),       x^(k+1)=P_1(w^k),
w^k=x^k+u_k,
```

and put `G_k=phi(x^k)-phi(x*)`.  The exact negative-credit identity is

```text
G_(k-1)-G_(k+1)
 =zeta_k/theta_k +(1+1/theta_k)u_k^Tt_k + R_k,
R_k>=0.                                                       (6)
```

Combining (4)--(6) gives the stronger graph- and alpha-free statement

```text
V_k <= G_(k-1)-G_(k+1),                                     (7)
zeta_k <= theta_k V_k.                                      (8)
```

Indeed,

```text
zeta/theta +(1+1/theta)u^Tt
 >=(theta+1)V-zeta >= V.
```

Summing (7) over `m<=k<=n` yields the whole-block ledger

```text
sum_{k=m}^n V_k
 <=G_(m-1)+G_m-G_n-G_(n+1)
 <=2(G_(m-1)-G_(n+1)).                                      (9)
```

The scalar `zeta` ledger is the immediate corollary obtained from (8).
Equation (9) is strictly more informative: it records how much the peeling
event times vary across actual graph edges.

## 2. Arbitrary freeze landscapes are nevertheless realizable

The new variation ledger does not justify assuming that the freeze field is
simple.  The following construction is exact.

Let `Q=aI-beta N` be the normalized canonical matrix on any fixed finite
connected simple unit graph, so `Qh=alpha h`, `h_i=sqrt(d_i)`.  Fix
`theta>0` and an arbitrary prescribed vector

```text
tau in [0,theta]^V.
```

Choose the peeling direction `d=epsilon h`.  For each row `i`, define

```text
z^(i)_j=epsilon min(tau_i,tau_j)h_j,
s_i=(Qz^(i))_i.                                              (10)
```

Because `z^(i)<=epsilon tau_i h` and `N>=0`,

```text
s_i
 >=epsilon(a-beta)tau_i h_i
 =epsilon alpha tau_i h_i >=0.                              (11)
```

Take any canonical single-source instance with strictly positive optimum
`x*`, and, for sufficiently small `epsilon`, set

```text
x=x*-Q^(-1)s,       x^-=x-d.
```

Then `x^-<=x` are strictly positive original subsolutions: their slacks are
`s` and `s+Qd=s+epsilon alpha h`, respectively.

At peeling time `r`, coordinate `j` has moved by
`epsilon min(r,tau_j)h_j`.  At `r=tau_i`, (10) makes row `i` exactly tight.
For every `r<tau_i`, the difference between the time-`tau_i` and time-`r`
movement is nonnegative and bounded coordinatewise by
`epsilon(tau_i-r)h`; hence its `i`th `Q`-image is at least

```text
epsilon alpha(tau_i-r)h_i>0.
```

Row `i` therefore cannot hit earlier.  Once it freezes, later movement only
replenishes it by the Stieltjes signs.  Thus the literal event pass realizes
exactly the prescribed freeze schedule `tau` (with simultaneous events
allowed).

This construction is a valid all-safe-state canonical result, not a claim
about zero-start reachability.  Its implication is precise: the oriented
event formula by itself cannot bound the number of event layers, impose a
monotone spatial order, or supply graph-independent expansion of the
freeze-time field.  Any such fact must come from the chronological relation
between successive exact proximal points.

## 3. Reproducible literal simulator

The companion script is
`safe_prox_literal_envelope_audit.py`.  It has no dependency beyond NumPy
and implements:

- the canonical normalized RPPR matrix and single-source threshold load;
- exact monotone active-set obstacle solves for `P_1`;
- exact greatest-safe-box correction as a dense audit oracle;
- one-pass peeling with all freeze times;
- maximal scalar ray, positive barrier, and safe reflection;
- the coordinatewise peeling/barrier/reflection envelope;
- objective, safety, support, complementarity-gap, oriented-event,
  negative-credit, and two-step-charge checks.

It is intentionally a dense deterministic audit, not a charged local
implementation.  Example commands are:

```text
python3 safe_prox_literal_envelope_audit.py \
  --family direct-peeling-five --source 3 \
  --alphas .001,.0001,.00001,.000001 \
  --rho-fractions .2 --relative-tolerance .01

python3 safe_prox_literal_envelope_audit.py \
  --family path --first 80 \
  --alphas .01,.003,.001,.0003,.0001 \
  --rho-fractions .0001 --relative-tolerance .01
```

The script also provides cycles, stars, brooms, lollipops, barbells, binary
trees, combs, alternating fans, and seeded connected random graphs.

## 4. Deterministic search results

All values below use relative max-residual tolerance `10^-2`.  `Ksqrt`
denotes `K sqrt(alpha)`.  `block1` is the largest observed objective-gap
ratio over any sliding block of `ceil(sqrt((1+alpha)/alpha))` rounds whose
starting gap remained above the numerical floor.

### Direct-gradient slow graph under exact prox

The graph is

```text
E={03,04,13,14,23,24,34},       source=3,       rho d_source=1/5.
```

```text
alpha       exact-box Ksqrt   peel Ksqrt   envelope Ksqrt   envelope block1
1e-3             7.874          7.874          7.842             .494
1e-4             7.970          7.980          7.960             .529
1e-5             7.997          7.997          7.994             .539
1e-6             8.004          8.004          8.003             .540
```

Only two peeling rounds clipped in each run.  The direct-gradient
`Theta(1/alpha)` tail is absent; exact prox and peeling agree to the
accelerated scale through four decades.

### Endpoint path with continuing face growth

For the 80-vertex path, endpoint source, and `rho d_source=10^-4`:

```text
alpha       envelope Ksqrt   optimum support   support-change rounds   block1
.01              4.600              38                   25              .165
.003             4.765              64                   46              .213
.001             5.471              80                   75              .241
.0003            5.958              80                   75              .275
.0001            6.490              80                   75              .328
```

At every alpha the exact-box, peeling-only, and full-envelope round counts
were within three rounds of one another.  Peeling clipped in at most seven
rounds for the full envelope.

### Structured face-growth stress at `alpha=10^-4`

```text
family                         vertices   envelope Ksqrt   block1
alternating fans (12; 3/9)        84          6.570          .482
lollipop (12-clique, tail 30)     42          6.590          .514
binary tree depth 6               127         6.610          .533
broom (handle 20, leaves 30)      50          6.660          .524
comb (spine 16, teeth 3)          64          6.750          .568
barbell (10-cliques, bridge 20)   40          6.450          .442
```

These finite results are counterexample searches only.  They do not prove a
uniform contraction, and the increasing `block1` values are consistent with
the ordinary lowest-mode accelerated limit rather than evidence for a
better constant.

## 5. Sharpened no-progress boundary

The second pass narrows the missing statement to the following form.

> **Chronological event-response lemma (open).**  For the literal zero-start
> exact-prox peeling/envelope trajectory, an accelerated-length block either
> contracts the true gap by a universal factor, or the exact proximal
> responses to that block's paid freeze-time variation force an equal amount
> of additional objective decrease.  The coefficient must be independent of
> the graph, `alpha`, support changes, and the number of event layers.

Equations (7)--(9) provide the complete payment side.  Exact safe-box APG
provides the ideal contraction side.  What is absent is a stable comparison
that uses the *signed spatial location and time ordering* of the paid event
variation.  A comparison depending only on `sum zeta_k` is already known to
lose a spectral factor, while Section 2 rules out replacing chronology by a
generic same-pass regularity assertion.

Therefore the literal method remains a plausible accelerated algorithm, but
the existing exact-box theorem plus the current peeling ledgers still do not
constitute a rigorous `O_tilde(1/sqrt(alpha))` round proof.
