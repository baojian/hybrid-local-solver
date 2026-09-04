# Approximate greatest-safe-box maintenance: certified interface and stops

Date: 2026-09-04

## Verdict

**Open in the canonical general-graph model.**  Replacing the exact
greatest-safe-box LCP by a certified approximate LCP does not currently yield
a deterministic

```text
O_tilde(M/sqrt(alpha))
```

implementation, where `M=vol(supp(x_rho^*))`, all graph exposure,
arithmetic, response maintenance, certificate queries, and output writes are
charged, and neither the final support nor ambient preprocessing is supplied.

There is a rigorous positive interface: a box-feasible primal--dual pair can
be stopped by a completely computable complementarity test that preserves
the exact `1-sqrt(alpha)` linear-coupling contraction.  What is missing is a
support-linear deterministic routine that reaches this test over the whole
sequence without paying a new `alpha^(-1/2)` inner condition-number factor
per outer round.

An exact one-sided repair now strengthens this interface.  On every canonical
face, any nonnegative objective-accurate correction can be shifted by one
computable multiple of `sqrt(d)` and then clipped to the known cap by a
coordinatewise minimum.  The result is exactly box-feasible and rowwise safe;
polynomially small objective error is sufficient for `LCStop`, with no
strict-complementarity margin.  Hence certificate conversion is no longer
the missing step.  The remaining issue is a deterministic
`O_tilde(vol(S))` approximate nonnegative-QP solver, or a persistent method
with the same whole-run cost.  The sufficient tolerance is state-dependent
and can shrink with the current box width, so this open cost explicitly
includes the cumulative logarithmic precision/encoding charge.

There is also a rigorous obstruction to the most tempting warm-start
amortization.  On a canonical unit triangle, the exact correction active set
along a genuine SafeBoxLC trajectory is

```text
{1,2}, {1}, empty, {3}, {1,2,3}.
```

The graph support and Hessian remain fixed.  Thus neither insertion-only LCP
active sets nor response events tied only to support/edge growth describe the
inner sequence.  The previous exact correction is sometimes infeasible for
the next right-hand side.  This is a formal lower bound for coordinatewise
monotone correction warm starts and an exact refutation of active-set
monotonicity; it is not a lower bound for signed recycling, multilevel
methods, or every deterministic algorithm.

## Model and the approximate box certificate

Let `B` be a symmetric Stieltjes matrix satisfying

```text
mu I <= B <= L I,       s=sqrt(mu/L),
```

and let `f(u)=u^TBu/2-c^Tu` on the nonnegative orthant.  At one SafeBoxLC
round suppose

```text
x is a lower subsolution,       x<=z,
y=(x+s z)/(1+s),                S=supp(x)=supp(z).
```

Write

```text
hat_t = c_S-B_SS y_S,           u=y_S-x_S.
```

An **approximately complementary but exactly safe box pair** is any pair

```text
0<=e<=u,      t=hat_t+B_SS e>=0,      zeta=e^Tt.       (ABox)
```

Set `w_S=y_S-e`, `w_(S^c)=0`.  The inequalities in `(ABox)` are exact
one-sided certificates, while only complementarity is approximate.  They
are locally checkable after one product with `B_SS`.

### Proposition 1: certified inexact SafeBoxLC

Admit every exterior row whose full gradient at `w` is negative, call the
enlarged face `A`, and let `g` equal the full gradient on `A` and zero
elsewhere.  Make the usual update

```text
x+ = w-g/L,
z+ = (1-s)z+s w-(s/mu)g.
```

Then `w` is a lower subsolution, `x<=w`, and the standard order/support
invariants for `x+` and `z+` hold.  Moreover, with

```text
E(x,z)=f(x)-f(x*)+(mu/2)||z-x*||_2^2,
A(w;x,z)=(1/2)||w-x||_B^2+(s mu/2)||z-w||_2^2,
```

one has the exact computable-error inequality

```text
E(x+,z+) <= (1-s)E(x,z)
             +(1-s^2) zeta-(1-s)A(w;x,z).       (InexactLC)
```

Consequently the local stopping rule

```text
(1+s) zeta <= A(w;x,z)                           (LCStop)
```

preserves the exact outer contraction

```text
E(x+,z+) <= (1-s)E(x,z).                         (LCContract)
```

For canonical RPPR, `B=Q`, `mu=alpha`, and `L=1`.  Therefore any
deterministic implementation satisfying `(LCStop)` in total
`O_tilde(M)` work per outer round would give the desired total work, up to
the existing logarithmic accuracy factor.

#### Proof

The exact LCP correction `e*` is the least nonnegative supersolution of
`hat_t+B_SS e>=0`.  Hence `(ABox)` gives `e*<=e<=u`, so
`x<=w<=w_box`; in particular `w` is a true lower subsolution.  The
Stieltjes signs then give the same order and support invariants as in the
exact-box proof.

On `S`, `g=Bw-c=-t`, and therefore

```text
<g,y-w> = -e^Tt = -zeta.
```

Substituting this identity into the exact linear-coupling bridge and
expanding the quadratic between `x` and `w` gives `(InexactLC)`.  Finally,
`1-s^2=(1-s)(1+s)`, so `(LCStop)` cancels the entire inexactness debit.

The same pair has the usual primal--dual accuracy interpretation.  For

```text
chi(e)=e^TB_SS e/2+hat_t^Te,       e>=0,
```

convexity at the feasible point `e` and strong convexity at the exact
minimizer give

```text
(1/2)||e-e*||_B^2
 <= chi(e)-chi(e*)
 <= e^Tt=zeta.                                    (Gap)
```

Thus `(LCStop)` is not a heuristic residual threshold; it is an exact
primal--dual certificate with the units needed by the outer Lyapunov.

The support-linear one-pass peeling construction is a valid way to produce
an initial `(ABox)` pair: it preserves `0<=e<=u`, makes `t>=0`, and reports
the exact gap `zeta=e^Tt`.  If `(LCStop)` happens to hold, no further inner
work is needed.  It does not hold uniformly.  The persistent five-vertex
slow ray for one-pass PeelingLC contracts only by `1-Theta(alpha)`; if
`(LCStop)` held on every round of that ray, `(LCContract)` would instead give
`1-sqrt(alpha)`.  Consequently a worst-case approximate-box algorithm needs
a genuine refinement mechanism after peeling, not merely evaluation of the
gap certificate.

### Proposition 2: objective accuracy can be repaired exactly

For canonical `B=Q_SS`, let `h_i=sqrt(d_i)`.  Then

```text
Q_SS h_S>=alpha h_S.
```

Given a nonnegative approximate point `tilde_e`, define

```text
gamma=max_i[-(hat_t+Q_SS tilde_e)_i/(alpha h_i)]_+,
q=min{u,tilde_e+gamma h_S}.
```

The shifted point is a supersolution.  The coordinatewise minimum of two
Stieltjes supersolutions is again a supersolution, and `u` is one; therefore
`q` satisfies `(ABox)` exactly.  If the QP objective error is `delta`, energy
Cauchy--Schwarz gives a computable bound of order `sqrt(delta)` on both the
shift and `q^T(hat_t+Q_SS q)`.  Completing squares also gives

```text
A(w;x,z)>=alpha*s||z-x||_2^2/[2(1+s)].
```

Thus a polynomially small explicit `delta` implies `LCStop`; if `z=x`, the
cap is zero and no solve is needed.  The full constants and proof are in
`POSITIVE_BARRIER_SAFE_SUPERSOLUTION_ROUNDING.md`.  This proposition does not make the
trajectory's exact correction faces monotone, so the obstruction below still
rules out insertion-only warm starts.

## Exact nonmonotonicity on the genuine linear-coupling trajectory

Take the three-cycle `C_3` (equivalently the unit triangle), whose vertices
all have degree two.  Let

```text
alpha=1/9,      s=1/3,      L=1,
Q = [ 5/9  -2/9  -2/9 ]
    [ -2/9  5/9  -2/9 ]
    [ -2/9 -2/9   5/9 ].                         (TriangleQ)
```

This is exactly the canonical normalized PageRank matrix.  Here is one fully
explicit canonical realization.  Choose source vertex one and `rho=1/14`,
and use the common positive rescaling `x_tilde=sqrt(2)x`.  The rescaled linear
term is

```text
c_tilde=alpha e_1-2 alpha rho 1,
```

and direct inversion gives the strictly positive RPPR optimum

```text
x_tilde*=(2/7,1/7,1/7).
```

For `lambda=1/100`, set

```text
x_tilde_0=x_tilde*-Q^(-1)lambda(0,0,1/4),
z_tilde_0=x_tilde_0+lambda(7/4,3/2,1).
```

Both states are strictly positive, `x_0<=z_0`, and
`c_tilde-Qx_tilde_0=lambda(0,0,1/4)>=0`.  Thus this is an exact canonical
full-support safe state.  Because `(ResidualLC)` is homogeneous, the table
below divides out the common factor `lambda`.

It is convenient to describe a SafeBoxLC state by

```text
a=c-Qx>=0,          v=z-x>=0.
```

Since `q=s/(1+s)=1/4`, its box trial residual and exact transition are

```text
hat_t = a-qQv,
(e,t) = LCP(Q,hat_t),
a+ = (I-Q)t,
v+ = (1-s)(v/(1+s)+e+t/s).                       (ResidualLC)
```

Start from

```text
a_0=(0,0,1/4),       v_0=(7/4,3/2,1).
```

The first five exact LCPs are:

| round | `hat_t` | correction-positive set | `e` | `t` |
| --- | --- | --- | --- | --- |
| 0 | `(-5/48,-1/18,7/24)` | `{1,2}` | `(13/48,5/24,0)` | `(0,0,5/27)` |
| 1 | `(-5/648,2/81,5/72)` | `{1}` | `(1/72,0,0)` | `(0,7/324,43/648)` |
| 2 | `(7/1944,35/1944,1/81)` | `empty` | `(0,0,0)` | `hat_t` |
| 3 | `(2/729,5/972,-5/2916)` | `{3}` | `(0,0,1/324)` | `(1/486,13/2916,0)` |
| 4 | `(-5/5832,-29/17496,-1/243)` | `{1,2,3}` | `(247/13608,29/1512,38/1701)` | `(0,0,0)` |

Every equality follows by substituting in `(ResidualLC)` and the three-row
complementarity system.  At round four the safe point reaches the optimum,
so a normal implementation may stop there.  The nonmonotonicity occurs
strictly before termination.

The previous exact correction is not generally a feasible warm start.  For
example, substituting `e_0` into the round-one LCP gives

```text
hat_t_1+Qe_0=(125/1296,13/162,-1/27),
```

whose third coordinate is negative.

There is also a quantitative obstruction to a correction state that is
allowed only to increase coordinatewise.  The round-one exact correction is
`e_1=(1/72,0,0)`, whereas

```text
[e_0-e_1]_+=(37/144,5/24,0).
```

For every round-one feasible correction `bar_e>=e_0`, `(Gap)` and
`Q>=alpha I` imply

```text
bar_e^T(hat_t_1+Q bar_e)
 >= (alpha/2)||bar_e-e_1||_2^2
 >= 2269/373248.                                 (MonotoneFloor)
```

Scaling the initial `(a_0,v_0)` by `lambda` scales this floor by
`lambda^2`; the relative obstruction is unchanged.  Thus a monotone
correction warm start cannot attain arbitrarily accurate certified gaps even
over two consecutive genuine rounds.  Deletion or signed correction is
essential.

The companion script `safe_box_lc_rhs_nonmonotonicity_exact.py` verifies the
complete table, the infeasible old correction, and `(MonotoneFloor)` using
rational arithmetic.

## Warm starts and what the example rules out

The triangle proves all of the following with fixed `Q` and fixed graph
support:

1. correction-positive sets are neither increasing nor decreasing;
2. a previously exact correction need not remain primal feasible;
3. the right-hand-side change has both signs and can move the violated row;
4. an update rule that only adds a nonnegative response has a positive
   primal--dual gap floor on the next query.

Therefore the movement and orthogonality ledgers for nested restricted
minimizers do not apply to successive box corrections.  Likewise, an
incremental K-LCP theorem that pivots each coordinate only once applies to
one fixed right-hand side, not to the full outer sequence.

The example does **not** prove that a signed warm start is ineffective.
Recycled Krylov, a reusable preconditioner, or a representation that permits
both active-set deletions and insertions remains possible.  Nor does five
rounds give an asymptotic runtime lower bound.

## Deterministic SDD and multilevel audit

On a supplied correction face `E`, the linear algebra is the principal SDDM
system `B_EE`.  A useful elementary fact is that spectral preconditioning
quality survives active-set changes: if

```text
P <= B <= kappa P,
```

then for every coordinate set `E`,

```text
P_EE <= B_EE <= kappa P_EE.                     (Restriction)
```

This follows by padding a vector on `E` with zeros.  Thus a single
full-support preconditioner is not invalidated *spectrally* by the triangle's
active-set changes.

What `(Restriction)` does not provide is the required local data structure:

- the final support is not known before safe discovery, so a full-support
  preconditioner cannot be built for free;
- applying or factoring `P_EE` must remain support-linear under arbitrary
  insertions and deletions of `E`;
- a deterministic low-stretch tree is cheaply restrictable, but its generic
  support-graph condition number is not polylogarithmic, so PCG can retain a
  polynomial inner factor;
- recursive sparsifier/Schur chains with the needed near-linear deterministic
  construction currently incur the known `M^(1+o(1))` overhead, and their
  moving-face numerical state is not supplied by `(Restriction)`;
- geometric rebuilds can amortize preprocessing over monotone graph-support
  growth, but they do not amortize the nonmonotone correction faces occurring
  between two graph insertions.

Hence low-stretch and multilevel methods are plausible numerical backends,
not a proof of `O_tilde(M)` total inner work per outer round in this model.
A deterministic `O_tilde(m)` supplied-SDD solve would remove the condition
factor on each already identified correction face, but it would not by itself
bound the number of correction-face changes needed to reach `(LCStop)`.  A
deterministic `O_tilde(m)` *safe-box LCP* routine, including face discovery
and one-sided certification, would be sufficient once per outer round; that
is precisely the stronger primitive that is presently missing.

## Does signed RHS variation prove an unconditional lower bound?

No.  It proves a structural lower bound only for monotone active-set or
nonnegative-response persistence.  An unconditional dynamic-solve lower
bound would require an access model and a reduction showing that the linked
SafeBoxLC right-hand sides encode sufficiently many independent inverse
queries.  The triangle supplies neither: its matrix is fixed and tiny, and a
factorization solves every listed query in constant work.

Similarly, dynamic-inverse and OMv lower bounds for arbitrary online matrix
or demand updates cannot be imported without such a reduction.  The
canonical sequence is one-source, support-safe, and generated by its own
linear-coupling transition; treating its right-hand sides as adversarial
arbitrary demands would overstate the result.

A standard fresh Chebyshev/CG call has an
`O_tilde(alpha^(-1/2))` product guarantee.  Multiplying that bound by the
outer `O_tilde(alpha^(-1/2))` count explains why the naive nested solve gives
`O_tilde(M/alpha)`, but an upper-bound multiplication is not a lower bound on
persistent recycling.

## Precise remaining theorem

To close ExactBoxMaintenance via approximation, it is enough to prove a
deterministic algorithm that, along the canonical zero-start SafeBoxLC
history, maintains `(ABox)` and reaches `(LCStop)` with total work

```text
O_tilde(M/sqrt(alpha))
```

over all outer rounds.  Such a theorem must explicitly charge:

1. signed round-to-round trial-residual changes;
2. correction-face deletions and reinsertions;
3. principal-matrix changes from safe graph-support admissions;
4. application of old-face Schur/Krylov responses;
5. exact one-sided feasibility checks, complementarity gaps, and boundary
   reporting; and
6. construction and restriction of every deterministic preconditioner.

The triangle rules out replacing items 1--2 by a monotone ledger.  The path
construction in `EXACT_SAFE_BOX_RESPONSE_SHORTCUT_OBSTRUCTION.md` rules out
paying items 3--4 merely by counting rank-one edge events or eagerly
materialized pivot responses.  No argument here rules out a genuinely signed
persistent multilevel representation, so the graph-uniform theorem remains
open rather than false.
