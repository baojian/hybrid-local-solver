# A zero-start two-vertex obstruction to one-pass PeelingLC

## Scope

This note gives a canonical zero-start counterexample to the claim that the
one-pass peeling substitute in `PeelingLC` preserves an accelerated round
bound.  The graph is the single unit edge, it is simple, undirected, connected,
and the load is the canonical point-source RPPR load.  The example therefore
removes both qualifications of the earlier five-vertex slow-ray calculation:
it is not an arbitrary safe state, and no attraction conjecture is needed.

The result does **not** refute `ExactBoxLC`; exact greatest-safe-box clipping
remains accelerated in product count.  It also does not refute the distinct
exact-prox peeling envelope.

## Canonical family

Put `s=sqrt(alpha)` and use the unit edge with source zero.  In normalized
coordinates,

```text
Q_s = [[d,-b],[-b,d]],
d=(1+s^2)/2,                 b=(1-s^2)/2,
rho_s=1/2-s,
c_s=s^2(1/2+s,-1/2+s).
```

For every sufficiently small positive `s`, the obstacle is inactive and

```text
x*=(s+s^2/2,s-s^2/2)>0.
```

Run persistent-estimate linear coupling from `x^0=z^0=0`.  At every round,
form

```text
y=(x+s z)/(1+s),
```

replace `y` by the one-pass peeling point `w` in the box `[x,y]`, put
`t=c_s-Q_s w`, and make the full-support update

```text
x^+=w+t,
z^+=(1-s)z+s w+t/s.
```

The first round admits the source.  The source-only trial in the second round
is accepted in full, and its exterior residual is

```text
(c_s-Q_s w)_1=s^3(3/2-s)>0.
```

Thus the second vertex is admitted.  A direct calculation gives

```text
x*-x^2=A_2(1,1),
A_2=s-s^2/2-3s^3/2+s^4,

z^2_0-x^2_0=s(1/2+s)(1-s)^2,
z^2_1-x^2_1=s^2(1-s)(3/2-s).
```

In particular, the construction starts from the prescribed zero state and
reaches the slow invariant domain after exactly two rounds.

## Exact reduced event map

Suppose at the start of a later round that

```text
x*-x=A(1,1),
z-x=A(p,s y),                A>0.
```

Set

```text
D=dp-bsy,
U=s^2 p/D,
V=s^2 y/(1+s).
```

In the event regime used below, coordinate zero freezes first at

```text
tau=s(1+s)/D,
```

and coordinate one then moves until time one.  The accepted increment divided
by `A` is `(U,V)`, and the final residual divided by `A` is

```text
T_0=s^2-dU+bV,
T_1=s^2+bU-dV.
```

Because `Q_s-I=-b 11^T`, the next error remains exactly symmetric:

```text
x*-x^+=A^+(1,1),
A^+/A=R_s(p,y):=1-s^2-b(U+V).                  (1)
```

The projective momentum variables obey

```text
P_s(p,y)=(1-s)(p-U+T_0/s)/R_s(p,y),
Y_s(p,y)=(1-s)(sy-V+T_1/s)/(s R_s(p,y)).       (2)
```

All these expressions have removable limits at `s=0`.  Uniformly on compact
subsets with `p>0`,

```text
(P_s-p)/s -> y/2-p,
Y_s         -> 2+y/2.                           (3)
```

## A forward-invariant zero-start domain

For sufficiently small `s`, define

```text
K_s={1/4<=p<=4,  1<=y<=4+8s/p}.
```

This is a forward-invariant domain for (2), and throughout it the peeling
event is exactly “coordinate zero freezes first; coordinate one never
freezes.”  Here are the boundary checks.

- At `p=1/4`, the first limit in (3) is at least `1/4`; at `p=4`, it is at
  most `-2+o(1)`.  Hence the two `p` boundaries point inward.
- At `y=1`, `Y_s -> 5/2`, so the lower `y` boundary points inward.
- On the curved upper boundary `y=4+8s/p`, direct expansion gives

  ```text
  [P_s(p,y)(Y_s(p,y)-4)-8s]/s -> -6p<0.
  ```

  This is precisely the inward condition `Y_s<=4+8s/P_s`.

For completeness, the upper-layer expansion at `y=4+A s` is

```text
P_s(p,y)(Y_s(p,y)-4)-8s
 =s[pA/2-6p-4]+O(s^2).
```

It is uniformly negative for every `A<=8/p`; points a fixed distance below
`y=4` have a strict zeroth-order margin.  Together with the uniform
`O(s^2)` remainder in the first line of (3), this checks the whole domain,
not only its boundary points.

The event checks are equally local.  On `K_s`, `D>0`, the initial pressure of
coordinate one is negative, and `tau<1` for all sufficiently small `s`.
Moreover,

```text
T_0/s^2 -> y/2>0.
```

The expression `T_1` is decreasing in `y` for small `s`; its minimum is on
the curved upper boundary, where

```text
T_1/s^3 -> 2>0.
```

Thus coordinate one retains positive slack at time one.  After factoring the
displayed powers of `s`, every expression is continuous on the compact
limiting domain.  The strict boundary signs therefore prove all of the above
claims for one common `s_0>0`.

Finally, the explicit two-round state satisfies

```text
p_2 -> 1/2,                    y_2 -> 3/2
```

as `s->0`, so `(p_2,y_2)` lies in `K_s` for all sufficiently small `s`.
This closes the zero-start reachability argument; convergence to a projective
eigenray is not assumed.

## Slow-round lower bound

On `K_s`, both `p/D` and `y/(1+s)` are bounded by absolute constants.
Equation (1) consequently gives one absolute `C` such that

```text
1-C s^2 <= A^+/A < 1.                           (4)
```

Therefore

```text
A_k >= A_2(1-C s^2)^(k-2).
```

The objective gap and max-positive-residual stopping certificate are exact on
these symmetric errors:

```text
f(x^k)-f(x*)=s^2 A_k^2,
Delta_k=(1/2) max_i(c_s-Q_s x^k)_i=s^2 A_k/2.
```

The initial objective gap is

```text
f(0)-f(x*)=5s^4/4.
```

Since `A_2/s -> 1`, (4) first implies that reducing the objective gap below
any fixed constant strictly smaller than its round-two value requires

```text
Omega(s^(-2))=Omega(alpha^(-1))
```

rounds.  For example, throughout a sufficiently small absolute multiple of
`s^(-2)` rounds, the gap remains a fixed positive fraction of the initial
gap `5s^4/4`.

The particular local stopping rule is even slower at a fixed relative
target.  Fix any constant `epsilon_0>0`.  For

```text
N=floor((4C)^(-1) s^(-2) log(1/s)),
```

the elementary bound `log(1-C s^2)>=-2C s^2` gives

```text
A_N=Omega(s^(3/2)),
Delta_N=Omega(s^(7/2))
       > epsilon_0 [f(0)-f(x*)]
```

for all sufficiently small `s`.  Hence this max-residual rule cannot certify
the target before

```text
Omega(s^(-2) log(1/s))
  = Omega(alpha^(-1) log(1/alpha))
```

rounds.  Both the objective lower bound and this stronger stopping-certificate
lower bound hold on a graph of constant final volume.  In particular the
canonical zero-start one-pass PeelingLC recurrence cannot be the desired
deterministic `O_tilde(M/sqrt(alpha))` algorithm.

## Slow projective ray (diagnostic, not needed by the lower bound)

The reduced map also has an analytic projective fixed point.  Dividing the
first fixed-point equation by `s` gives at `s=0`

```text
F_0=-p+y/2,                    G_0=2-y/2.
```

Its solution is `(p,y)=(2,4)`, and the Jacobian

```text
[[-1,1/2],[0,-1/2]]
```

has determinant `1/2`.  The implicit-function theorem therefore gives an
analytic valid-event branch with

```text
p(s)=2-4s+8s^2+O(s^3),
y(s)=4-8s+52s^2+O(s^3),
lambda(s)=1-4s^2+4s^3+O(s^4),
tau(s)=s+5s^2+11s^3+O(s^4),
T_0(s)=2s^2-8s^3+O(s^4),
T_1(s)=8s^3+O(s^4).
```

The analytic branch explains the observed tail, while the invariant-domain
argument above supplies the missing rigorous zero-start lower bound.

## Reproduction

- `peeling_lc_two_vertex_obstruction.py` reproduces the exact event word and
  the numerical zero-start trajectory.
- `peeling_lc_two_vertex_ray_exact.py` checks the removable-limit equations,
  implicit-function Jacobian, and rational series coefficients symbolically.
