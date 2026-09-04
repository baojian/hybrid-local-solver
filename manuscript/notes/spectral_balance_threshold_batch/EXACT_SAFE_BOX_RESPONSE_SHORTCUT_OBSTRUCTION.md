# Exact safe-box response: a scoped implementation obstruction

Date: 2026-09-03

## Verdict

**Open, not refuted as a theorem.**  The exact greatest-safe-box
linear-coupling recurrence has the proved product count

```text
O(alpha^(-1/2) log(poly(1/alpha)/eps_obj))
```

across arbitrary safe support growth.  I do not obtain a deterministic
`O_tilde(M/sqrt(alpha))` implementation, where
`M=vol(supp(x_rho^*))`, all graph exposure, arithmetic, response updates,
certificate queries, and output writes are charged, and no ambient
preprocessing or final-support oracle is supplied.

The precise reason is that the available persistent-response identity and
the exact safe-box oracle evolve different data:

- the compensated-halo identity changes the matrix monotonically at a fixed
  right-hand side and charges one positive rank-one downdate per revealed
  edge;
- the safe-box LCP keeps `Q_SS` fixed between support changes but receives a
  new trial residual `hat_t=c_S-Q_SS y_S` on every accelerated round.

Thus the revealed-edge rank and monotone movement ledgers do not implement
the box oracle.  The canonical construction below makes the separation exact:
there are no support or revealed-edge changes, yet one valid safe-box query
requires a dense inverse response.  It also refutes the tempting inference

```text
at most |S| K-matrix pivots + rank-one Schur updates
    => O_tilde(vol(S)) exact box work.
```

For the literal implementation that materializes the exact response after
each pivot, the same path query performs `Theta(|S|^2)` strict coordinate
updates although the path has `Theta(|S|)` volume.  This is a lower bound for
that eager pivot/Schur shortcut, not for all exact-box algorithms: a direct
tridiagonal solve handles this particular final system in linear work.

## Assumptions and normalization

Let `P_n` be the `n`-vertex unit path, with endpoint source `v=1`, and let

```text
Q = alpha I + (1-alpha)(I-D^(-1/2) A D^(-1/2))/2,
a = (1+alpha)/2,     beta = (1-alpha)/2,
c = alpha D^(-1/2)e_1-alpha rho D^(1/2)1,
```

where `0<alpha<1`.  Choose

```text
0 < rho < min_i (Q^(-1) alpha D^(-1/2)e_1)_i/sqrt(d_i).
```

Inverse positivity makes this interval nonempty.  The RPPR obstacle optimum
then has full support and equals

```text
x* = Q^(-1)c = Q^(-1) alpha D^(-1/2)e_1-rho D^(1/2)1 > 0.
```

Consequently `Qx*=c` on every row.  The graph is finite, simple, connected,
unit-weight, nontrivial, and single-source, exactly as in the canonical
contract.  The construction is in the exact-real arithmetic model.  It is a
valid all-safe-state construction; it is not asserted to occur on the
zero-start chronology.

## The fixed-support safe state

Fix the linear-coupling value `s=sqrt(alpha)`, and choose arbitrary positive
`r,delta` small enough for the vectors below to stay strictly positive.  Put

```text
sigma = delta e_n,
x     = x* - Q^(-1) sigma,
y     = x* + r Q^(-1)e_1,
z     = x + ((1+s)/s)(y-x).
```

Then `x<=z`, they have the same certified support `S=V`, and `x` is an
original lower subsolution because

```text
c-Qx = sigma >= 0.
```

Moreover `y=(x+s z)/(1+s)`, so this is exactly an admissible input to the
greatest-safe-box step in `SafeBoxLC`.  Its trial residual is

```text
hat_t = c-Qy = -r e_1.                         (1)
```

The correction LCP

```text
e>=0,    t=hat_t+Qe>=0,    e^Tt=0
```

has the strictly positive solution

```text
e = r Q^(-1)e_1,       t=0,       w_box=y-e=x*.   (2)
```

There is no support admission and no unexposed edge.  In particular the
matrix change `H` in the compensated-halo persistent-response identity is
exactly zero, while the safe-box correction in (2) is nonzero on all `n`
coordinates.  Any implementation driven only by revealed-edge rank-one
events therefore misses this query completely.  A separate persistent
right-hand-side/projection mechanism is necessary.

For readers who prefer the earlier two-subsolution momentum notation, take

```text
d  = Q^(-1)(sigma+r e_1)/theta,
x- = x-d
```

for any `theta>0` and still smaller `r,delta`.  Then `x-<=x` are strictly
positive subsolutions, `x+theta d=y`, and the same trial residual (1)
results.

## Exact sequential pivot trace on the path

Pass to degree coordinates.  With `H=D^(1/2)`, the correction matrix is

```text
K = H Q H = aD-beta A,
```

an irreducible tridiagonal Stieltjes matrix.  Diagonal scaling preserves
positivity and complementarity.  Scale `r=1`.  Starting from the empty
correction set, let `E_k={1,...,k}` and materialize the exact restricted
response

```text
u^(k)_(E_k) = K_(E_k,E_k)^(-1)e_1,
u^(k)_(V\E_k) = 0.                              (3)
```

Strict inverse positivity gives `u^(k)_i>0` for every `i<=k`.  Its LCP
residual is zero on `E_k`, is

```text
(K u^(k)-e_1)_(k+1) = -beta u^(k)_k < 0         (4)
```

when `k<n`, and is zero on every vertex beyond `k+1`.  Hence `k+1` is the
unique violated row and the monotone principal-pivot path is forced to expose
the path in order.

Write the block extension as

```text
K_(k+1) = [ K_k       q ] ,      q=-beta e_k,
          [ q^T   kappa ]
```

and let

```text
S_k = kappa-q^T K_k^(-1)q > 0.
```

The Schur formula is

```text
u^(k+1)_(k+1) = beta u^(k)_k/S_k > 0,
u^(k+1)_(1:k) = u^(k) +
                 beta u^(k+1)_(k+1) K_k^(-1)e_k.    (5)
```

Every entry of `K_k^(-1)e_k` is strictly positive.  Equation (5) therefore
changes all `k` previously materialized coordinates strictly at pivot
`k+1`.  An eager exact response array incurs

```text
sum_(k=1)^(n-1) k = n(n-1)/2 = Theta(n^2)
```

coordinate writes, before charging pivot selection or factor maintenance.
Since `vol(P_n)=2(n-1)`, the bound is quadratic in the supplied-face volume.
Storing each new Schur lift `K_k^(-1)e_k` explicitly has the same dense
triangular total size.

The companion script
`exact_safe_box_response_shortcut_obstruction.py` checks the canonical
full-support linear-coupling state, (3)--(5)'s strict prefix changes, and the
unique frontier violation using rational arithmetic for `K=aD-beta A`.

## What this does and does not establish

**Proved here.**  Revealed-edge rank-one persistence alone cannot realize
the greatest-safe-box oracle: the oracle can have a dense nonzero response
when the revealed-edge update count is zero.  Also, the short K-matrix pivot
path does not make literal materialized Schur continuation support-linear;
on canonical paths it makes quadratically many strict response-coordinate
changes.

**Refuted.**  The implication “one rank-one event per revealed edge plus at
most one pivot per safe coordinate yields a deterministic
`O_tilde(M/sqrt(alpha))` implementation” is false without an additional
right-hand-side response representation.  Edge-event and pivot counts do
not pay the dense old-face lifts.

**Not refuted.**  This is not a lower bound for every deterministic
algorithm, for the zero-start history, or for an implicit separator/multilevel
representation.  In particular, the path's final linear system is easy.
Nor does it contradict the exact safe-box contraction theorem.

**Still needed for a positive theorem.**  A complete implementation must
maintain, in one persistent state, both:

1. principal-matrix changes caused by safe support insertions; and
2. the round-by-round signed right-hand-side changes of the projected LCP.

It must apply the resulting dense old-face response implicitly, report all
threshold-relevant boundary coordinates with no false negatives, preserve a
certified lower bracket, and charge the complete sequence by
`O_tilde(M/sqrt(alpha))`.  The standard black-box deterministic
Chebyshev/CG guarantee for a fresh box costs
`O_tilde(alpha^(-1/2))` products inside each of the already
`O_tilde(alpha^(-1/2))` outer rounds; generic deterministic SDD machinery
currently leaves the known `M^(1+o(1))/sqrt(alpha)` scale.  Neither observation
is a proof of impossibility, but both show that the missing object is a
genuine persistent projected-response data structure, not a direct
corollary of the existing rank-one or Schur identities.
