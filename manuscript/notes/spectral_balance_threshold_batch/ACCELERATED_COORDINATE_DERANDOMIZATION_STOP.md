# Accelerated-coordinate conditional-expectation stop

Date: 2026-09-04

## Scope and verdict

This companion audits one specific proposed replacement for the randomized
supplied-face solve: run accelerated randomized coordinate descent on the
current Stieltjes face, but choose each coordinate deterministically by the
method of conditional expectations and maintain the choice in a local score
heap.

The verdict is split.

- **Proved here (oracle iteration theorem).**  On a supplied fixed face, an
  omniscient coordinate choice does inherit the accelerated one-step
  contraction pathwise.
- **Refuted (direct local-score implementation).**  The exact branch score
  contains a coordinate correlation with the unknown optimum.  At a certified
  lower state this term is `r_i (Q^-1 r)_i`.  It is the dense inverse response,
  not a function of the maintained local residual alone.
- **Proved here (canonical counterexample).**  On a three-vertex, simple,
  connected, unit-weight point-source RPPR instance, the usual
  Gauss--Southwell/max-residual coordinate has one-step accelerated potential
  *strictly larger* than the randomized conditional mean.
- **Open.**  This is not a lower bound for every deterministic coordinate
  method.  A different pathwise potential, a charged pessimistic estimator,
  or a persistent inverse-response oracle could still derandomize the method.

Thus randomized accelerated coordinate descent does not currently close the
general `O_tilde(M/sqrt(alpha))` theorem.  Its randomness hides exactly the
same response information called `CenterLift` elsewhere in this direction.

## Source anchor

Allen-Zhu, Qu, Richtarik, and Yuan's NU-ACDM Algorithm 1 and Theorem 5.1 give
the update and expected strongly-convex rate used below; the linear-coupling
proof and the one-step potential are on arXiv `1512.09103v3`, PDF pp. 7--12:

<https://arxiv.org/abs/1512.09103>

Lu, Freund, and Mirrokni explain on PDF p. 6 that the ordinary accelerated
Lyapunov contains `||z-x*||^2`, so a gradient-greedy coordinate need not be
greedy for the Lyapunov and the needed coordinate cannot be selected from the
standard proof without the unknown optimum:

<https://proceedings.mlr.press/v80/lu18b.html>

The other nominally greedy accelerated construction of Locatello et al. does
not remove this issue: Algorithm 4, PDF pp. 6--7, uses a greedy atom for the
descent update but still samples a random atom for the auxiliary/model update:

<https://proceedings.mlr.press/v80/locatello18a.html>

These are source facts.  The exact score reduction and RPPR witness below are
new calculations.

## 1. Fixed-face randomized work

Let

```text
f(x)=x^T Q x/2-c^T x,       x*=Q^-1 c,
mu I <= Q,                  Q_ii=a for every i in U,
n=|U|,                      M=vol(U).
```

The normalized RPPR matrix has exactly this constant diagonal,
`a=(1+alpha)/2`, and `mu>=alpha`.  On an interior positive obstacle face the
separable `l1` term is linear and is absorbed into `c`; hence the calculation
is also the local calculation for RPPR.  A witness below stays strictly in
the positive orthant, so no projection qualification is hidden.

Use the Euclidean, uniform specialization of NU-ACDM.  Given the current
states `(y,z)`, put

```text
tau = 2/(1+sqrt(1+4n^2 a/mu)),
eta = 1/(tau n^2 a),
w   = tau z+(1-tau)y,
g   = Qw-c.
```

Uniformly sample `i`, and make the two coordinate updates

```text
y_i^+ = w-(g_i/a)e_i,
z_i^+ = [z+eta mu w-eta n g_i e_i]/(1+eta mu).
```

The parameter identity is

```text
mu(1-tau)=tau^2 n^2 a,
1+eta mu=1/(1-tau).
```

The standard potential is

```text
P(y,z)=f(y)-f(x*)+kappa ||z-x*||_2^2,
kappa=tau/[2 eta(1-tau)].
```

Its conditional expectation contracts by `1-tau`.  Since
`tau=Theta(sqrt(mu/a)/n)`, this is
`O(n sqrt(a/mu) log(1/epsilon))` coordinate updates.  Uniform sampling has
expected row cost

```text
E[d_i]=M/n,
```

and therefore the supplied fixed-face expected work is

```text
O(M sqrt(a/mu) log(1/epsilon)).
```

For `a=Theta(1)` and `mu>=alpha`, this has the desired root dependence.  This
fixed-face expectation does not itself handle changing support or safe
publication.

In the project's edge-work model this fixed-face rate is not asymptotically
better than deterministic full-gradient NAG: `O(1/sqrt(mu))` full products
also cost `O(M/sqrt(mu))`.  Random coordinates become potentially useful only
if their individual sparse updates can be continued through support discovery
without full rescans.  Averaging all coordinate branches deterministically
just reconstructs a full-gradient step and returns to the existing
`InputConeFrontierNAG`/safe-publication problem.

## 2. Exact one-step branch score

Define the branch-independent auxiliary center and the coordinate step

```text
zbar=(z+eta mu w)/(1+eta mu),
delta=eta n/(1+eta mu)=eta n(1-tau).
```

Then `z_i^+=zbar-delta g_i e_i`.  Since the objective is quadratic and
`Q_ii=a`, expansion gives the exact branch value

```text
P_i
 = C-tau H_i,

C   = f(w)-f(x*)+kappa||zbar-x*||_2^2,
H_i = g_i^2/(2a)+n g_i(zbar_i-x_i*).             (branch score)
```

Indeed, the objective coordinate step contributes `-g_i^2/(2a)`, while

```text
kappa delta^2=(1-tau)/(2a),
2 kappa delta=tau n.
```

Consequently a coordinate has potential no larger than the random
conditional mean exactly when

```text
H_i >= (1/n) sum_j H_j.                          (CE choice)
```

This proves an **omniscient deterministic iteration theorem**: choosing a
maximizer of `H_i` at every step makes the usual expected contraction
pathwise.  But it is not an algorithm in the local model because `H_i`
contains `x_i*`.

There is also an exact omniscient way to retain the randomized *charged-work*
bound, rather than merely its iteration bound.  Let

```text
dbar=M/n,
P_0<=U_0,
W_k=sum_(j<k) d_(i_j),
```

where `U_0` is any supplied computable upper bound and fix a horizon `T`.
For the zero start on a positive face, for example,

```text
U_0=||c||_2^2[1/(2mu)+kappa/mu^2]
```

is valid by `Q>=mu I`; it requires no solve and affects only the logarithm.
Use the pessimistic estimator

```text
Z_k=P_k/[(1-tau)^k U_0]
    +[W_k+(T-k)dbar]/[T dbar].                  (work-potential estimator)
```

The random branch satisfies

```text
E_i[Z_(k+1)]<=Z_k,
```

because `E_i[P_i]<=(1-tau)P_k` and `E_i[d_i]=dbar`.  Therefore an omniscient
conditional-expectation choice keeps `Z_k` nonincreasing.  Since `Z_0<=2`,
at the horizon it gives simultaneously

```text
P_T<=2(1-tau)^T U_0,
W_T<=2T M/n.
```

In particular, this is a deterministic fixed-face
`O(M sqrt(a/mu) log(U_0/epsilon))` charged-work theorem *given the exact
branch-key oracle*.  Using `P_i=C-tau H_i`, the implementable-looking rule
would maximize

```text
H_i-lambda_k d_i,
lambda_k=(1-tau)^(k+1) U_0/(tau T dbar).        (charged CE key)
```

The degree penalty is observable, but `H_i` still contains `x_i*`.  Thus
coupling the randomized cost and convergence ledgers does not remove the
inverse-response obstruction; it isolates it more cleanly.

At the particularly favorable certified lower state

```text
y=z=w=u,             r=c-Qu>=0,
e=x*-u=Q^-1 r>=0,
```

the score becomes

```text
H_i=r_i^2/(2a)+n r_i e_i
   =r_i^2/(2a)+n r_i(Q^-1r)_i.                  (inverse-response score)
```

Stieltjes signs prove only the local lower bound
`(Q^-1r)_i>=r_i/a`.  They do not determine the coordinatewise response.  A
generic upper bound uses `1/mu` and loses the root acceleration.  Computing
the exact missing term for all coordinates is precisely a current-residual
inverse response.

The already-proved positive-walk barrier in the parent `README.md` also
applies to the most direct safe approximation of this key.  Expanding
`Q^-1r` by a universal nonnegative Neumann/walk polynomial needs
`Omega(alpha^-1 log(1/delta))` degree at fixed relative accuracy on the
Perron mode.  Signed Chebyshev, graph-specific elimination, or a retained
Schur response can escape that barrier, but each is again a nontrivial
response primitive rather than a heap of local residuals.

The cancellation in the randomized proof is now transparent: the factors
`1/p_i` in the auxiliary update make the expectation of the unknown
coordinate correlation equal the full inner product used by convexity.  The
individual correlations do not cancel, so ordinary conditional expectation
cannot select a branch from residual squares alone.

Conditioning through a binary sampler does not make the oracle smaller.  If a
random bit restricts the next coordinate to a subset `A`, the conditional
branch average contains

```text
sum_(i in A) g_i x_i*.
```

Hence every bit decision asks for a partial optimum correlation.  A singleton
heap asks for all such correlations, while a tree of conditional decisions
asks for group inverse-response queries.  The full-set expectation is useful
in the proof precisely because the complete sum becomes one global inner
product to which convexity applies; no analogous cancellation holds for an
adaptive proper subset.

## 3. Exact canonical RPPR counterexample

Take the three-vertex path, written as a center `0` joined to leaves `1,2`.
Its degrees are `(2,1,1)`.  Let

```text
alpha=1/1000,                 rho=1/10000,
a=1001/2000,                  b=999/2000,

Q = [[a,-b/sqrt(2),-b/sqrt(2)],
     [-b/sqrt(2),a,0],
     [-b/sqrt(2),0,a]].
```

This is the canonical normalized PageRank matrix of a finite simple connected
unit graph.  On the positive RPPR face its linear load is

```text
c=alpha D^(-1/2)e_0-alpha rho sqrt(d),
```

and its exact obstacle optimum is strictly positive:

```text
x*=(5003 sqrt(2)/20000, 4993/20000, 4993/20000).
```

Put `v=(9,10,11)`, `t=10^-6`, and

```text
u=x*-t Q^-1v.
```

All three coordinates of `u` are positive, `u<=x*`, and

```text
c-Qu=t v>0.
```

Initialize the fixed-face accelerated step with `y=z=u`; then `w=zbar=u`.
Write `H_i=t^2 R_i`.  Exact elimination gives

```text
R_0 = 243648243/2002 + 566433 sqrt(2)/4,
R_1 = 45110045/286   + 134865 sqrt(2)/2,
R_2 = 9026009/52     + 296703 sqrt(2)/4.
```

The unique largest residual, largest degree-normalized residual, and largest
coordinate-descent decrease are all at leaf `2`:

```text
11 > 10 > 9,
11 > 10 > 9/sqrt(2).
```

Nevertheless

```text
R_0+R_1-2R_2
 =-135584135/2002+242757 sqrt(2)/4
 >345156949/20020
 >0,
```

where the strict bound uses `sqrt(2)>7/5`.  Therefore

```text
R_2 < (R_0+R_1+R_2)/3,
P_2 > (P_0+P_1+P_2)/3.
```

In fact this branch violates the standard pathwise accelerated contraction,
not merely the conditional-average choice.  Here
`tau=2/(1+sqrt(18019))`, and exact expansion gives

```text
P_2-(1-tau)P(u,u)
 =3(sqrt(18019)-1)
   (-6754568984311+6020007979986 sqrt(2))
   /8024024008000000000000000
 >0.
```

The last sign already follows from `sqrt(2)>7/5`.  Thus
Gauss--Southwell/max residual selects a branch strictly worse than the
randomized conditional mean and fails the one-step accelerated Lyapunov
contraction on an exact point-source RPPR state.  The state and both
coordinate updates are interior, so obstacle projection cannot remove the
failure.

This first witness is a legal fixed-face warm state; it is not asserted to be
the state produced by the canonical zero-start active-set chronology.  There
is, however, a separate zero-start strengthening for the *supplied full face*.
On the same graph, take

```text
alpha=1/10,       rho=1/1000,       tau=2/(1+sqrt(199)).
```

Start NU-ACDM from `y_0=z_0=0` and choose the smallest-index maximizer of
`|g_i|`.  The exact first eight choices are

```text
0,1,2,0,1,2,0,1.
```

All primal and auxiliary coordinates remain nonnegative.  At iteration seven,
the chosen coordinate satisfies

```text
H_1-(H_0+H_1+H_2)/3
 =[-A+2B sqrt(199)]/D < -3.33e-6 <0,

A=5206883677438968880700576045466387285942759064488726267403483901,
B=184502567533428390482163481628210822751800043275281785240489199,
D=66415297273919678808531096953240398855459148134920443936880000000.
```

The sign is exact: `sqrt(199)<1411/100`, and substituting that rational upper
bound leaves a strictly negative numerator.  Hence even zero initialization
does not make gradient-greedy selection a conditional-expectation
derandomization on a supplied canonical positive face.  This trace supplies
the full face from the outset and is not claimed to be the same as a
minimal-face algorithm that changes its ACD parameters during admissions.

The executable certificate is
`accelerated_coordinate_derandomization_exact.py`.

## 4. Why an ordinary local heap does not repair the score

There are two independent implementation gaps.

1. **The key is an inverse response.**  Even in the lower-state normal form,
   the exact key needs `(Q^-1r)_i`.  Initializing those values at zero start
   means knowing `x*`; recomputing them from the current residual is a solve.
   A certified upper/lower response bracket could support an approximate key,
   but maintaining that bracket is the open persistent-response problem.

2. **Acceleration changes every logical key.**  Although the coordinate
   corrections are sparse, the next states contain the global mixtures
   `w=tau z+(1-tau)y` and `zbar`.  For every unselected `j`, generally
   `y_j^+=w_j` and `z_j^+=zbar_j` differ from their old values.  Hence the next
   `g_j` and `H_j` can change globally.  Lazy two-vector representations let a
   randomized algorithm query one sampled coordinate cheaply; they do not
   make an explicit max-key heap correct after updating only the selected row
   and its neighbors.  A specialized kinetic-envelope data structure is not
   ruled out, but no charged construction is supplied here.

This is exactly where the new one-pass peeling heap does **not** transfer to
ACD.  During one peeling pass the direction is fixed; freezing coordinate
`i` merely removes the column `Q[:,i]d_i`, so only `i` and its graph neighbors
need new event keys.  In ACD the interpolation and auxiliary contraction
change the logical direction before every coordinate choice.  Thus the
peeling result is valuable for computing a safe point on one segment, but it
does not maintain the accelerated conditional-expectation keys.

There is a third accounting distinction.  Selecting a branch below the
average potential does not by itself bound the degree of the chosen row.  The
work-potential estimator above repairs this algebraically by replacing `H_i`
with the charged key `H_i-lambda_k d_i`, but that key remains omniscient.  So
the cost ledger is not a second impossibility; it is a second quantity the
missing solution-free key must handle.

## 5. Honest theorem boundary and next test

The exact conclusion is a route stop, not a universal lower bound:

```text
randomized fixed-face ACD expectation
    does not imply
deterministic local ACD with a residual-score heap.
```

A usable positive theorem would follow from either of the following genuinely
new ingredients.

- `LocalACDPessimisticEstimator`: a solution-free quantity whose chosen
  branch contracts at the accelerated rate and whose update plus chosen-row
  cost is `O_tilde(d_i)`.
- `PersistentCoordinateResponse`: certified values or tight intervals for
  `(Q^-1r)_i` on all candidate rows, updated through coordinate steps and face
  growth in total `O_tilde(M/sqrt(alpha))` work.

The second premise is another formulation of `CenterLift`; it should not be
counted as a free heap key.  The first would be a genuinely different
derandomization and remains open.
