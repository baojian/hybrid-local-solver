# Safe-prox event variation does not force delayed response energy

Date: 2026-09-04

This is a narrowly scoped, unregistered companion note.  It does not modify
the integration audit or any shared README, STATUS, CLAIMS, or results
registry.

## Result

The fixed-face positive-kernel formula for an exact proximal response is
valid, but the paid one-pass peeling variation does **not** force a
graph-uniform amount of response energy in the next round, in an
accelerated-length block, or even over the entire future continuation.

More precisely, there is a fixed three-vertex canonical single-source graph
and a one-parameter family of strictly positive, all-safe states for the
literal peeling/barrier/reflection envelope such that

```text
V_k = Theta(delta^2 epsilon),
sum_{j>=k} (||r_(j+1)||^2 + 1/2 ||r_(j+1)||_Q^2)
    = O(delta^2 epsilon^2).
```

Consequently no constant `C`, independent even just of the supplied state,
can make

```text
V_k <= C sum_{j=k}^{k+M}
             (||r_(j+1)||^2 + 1/2 ||r_(j+1)||_Q^2)          (1)
```

hold for any horizon `M`, including `M=infinity`.  In particular, allowing
`M=O(1/sqrt(alpha))` does not repair (1).

This is an all-safe supplied-state obstruction.  The state includes a
genuine exact-prox transition into the current iterate and the current
center is genuinely selected by the full deterministic envelope.  It is
not proved reachable from the prescribed zero initialization.  Thus it
rules out the proposed local cross-round inequality, but does not refute a
zero-start theorem using an additional historical invariant.

## 1. Positive-kernel normal form

Let `w` be an original subsolution, `p=P_1(w)`, `r=p-w`, and
`A=supp(p)`.  Since `w<=p`, both `w` and `r` vanish off `A`.  Writing

```text
t=c-Qw,
```

the proximal optimality equations on `A` give the exact formula

```text
r_A = (I+Q_AA)^(-1) t_A,       r_(A^c)=0.                   (2)
```

The principal Stieltjes matrix `I+Q_AA` is a nonsingular M-matrix, so its
inverse is entrywise nonnegative.  Formula (2) is therefore the desired
positive-kernel representation, including at support changes after choosing
the new active face.

It also shows the scaling problem.  The response descent is quadratic in
`t`, whereas the peeling event ledger can be linear in `t` because its
discarded distance need not be small.

There is a sharp general bilinear statement.  If the selected center is the
peeling output, the event identity and nonnegativity of the terminal slack
give

```text
theta V=zeta+u_F^Tt
       <=(theta d-u)^Tt+u^Tt=theta d^Tt.
```

Combining this with (2), and using `lambda_max(Q_AA)<=1`, yields

```text
V <= d_A^T(I+Q_AA)r_A <= 2 ||d_A|| ||r_A||,
||r_A||^2 >= V^2/(4||d_A||^2).                              (2a)
```

Thus event variation does force a response **norm**, but only bilinearly
with the incoming direction.  Squaring (2a) produces a quadratic-in-`V`
credit, not the constant-coefficient linear energy credit needed by the
proposed block argument.  Replacing the Euclidean norm of `d` by its
available `Q`-energy also incurs `||d||<=alpha^(-1/2)||d||_Q`.

That spectral loss is real, not merely an artifact of Cauchy--Schwarz.  On
the same triangle with arbitrary `0<alpha<1`, put

```text
b=(1-alpha)/4,
tau=epsilon (ell,ell+1,ell+2),
ell >= (1-alpha)(1+2alpha)/(4alpha(1+alpha)),
d=delta (1,1,1).
```

The arbitrary-freeze construction gives starting-slack coefficients

```text
(alpha ell,
 alpha ell+(1+3alpha)/4,
 alpha ell+(3+5alpha)/4).
```

The displayed lower bound on `ell` is exactly what makes the preceding
center a subsolution; the other two rows then have still larger slack.  For
sufficiently small `epsilon,delta`, the full envelope again selects the
peel.  Its terminal slack and event variation are

```text
t=delta epsilon (3b,b,0),       V=(1-alpha)delta^2 epsilon.
```

Since `d` is the Perron direction,
`||d||_Q=delta sqrt(3alpha)`.  Also
`||r||<=||t||/(1+alpha)=delta epsilon b sqrt(10)/(1+alpha)`.
Therefore any inequality of the form

```text
V <= C ||d||_Q ||r||
```

requires

```text
C >= 4(1+alpha)/sqrt(30alpha)=Omega(alpha^(-1/2)).           (2b)
```

Thus the graph-uniform Euclidean bilinear bound (2a) cannot be converted to
the available incoming `Q`-energy with a constant coefficient.

## 2. Exact canonical triangle

Take the triangle graph, source vertex `0`, threshold `rho=1/100`, and

```text
alpha=1/8,       a=(1+alpha)/2=9/16,
beta=(1-alpha)/2=7/16,
theta=(1-sqrt(alpha/(1+alpha)))/(1+sqrt(alpha/(1+alpha)))=1/2.
```

All degrees are two, and the normalized canonical matrix is

```text
Q = [  9/16  -7/32  -7/32 ]
    [ -7/32   9/16  -7/32 ] .                              (3)
    [ -7/32  -7/32   9/16 ]
```

Its eigenvalues are `1/8,25/32,25/32`.  The single-source obstacle optimum
is strictly positive:

```text
x*_0=21/(50 sqrt(2)),       x*_1=x*_2=13/(50 sqrt(2)).      (4)
```

Fix `delta=1/100` and let `0<epsilon<=1/100`.  Put

```text
d=delta (1,1,1),
q=(1/4,19/32,37/32),
s=delta epsilon q,
aerr=Q^(-1)q=(24/5,131/25,149/25),
x=x*-delta epsilon aerr,
x^-=x-d,
w^old=x-s.                                                  (5)
```

All three vectors are strictly positive.  Their original slacks are

```text
c-Qx       =s,
c-Qx^-     =s+(delta/8)(1,1,1)>0,
c-Qw^old   =s+Qs
            =delta epsilon (1/128,635/1024,1661/1024)>0.    (6)
```

Also `x^-<=w^old<=x`, and the interior proximal equations give exactly

```text
x=P_1(w^old).                                                (7)
```

Thus (5) is not an arbitrary infeasible snapshot: it is a nested all-safe
state with a genuine preceding exact proximal call.

## 3. The full envelope chooses the one-pass peel

Starting from `(x^-,x)`, the literal one-pass peeling event times are

```text
tau=epsilon (2,3,4).                                        (8)
```

Indeed, before the first event `Qd=(delta/8)1`; after vertex `0` freezes,
the pressure on vertices `1,2` is `11 delta/32`; after vertex `1` freezes,
the pressure on vertex `2` is `9 delta/16`.  The slacks in (5) therefore
make the three vertices hit successively at exactly (8).  The accepted
movement and final slack are

```text
u=delta epsilon (2,3,4),
t=c-Q(x+u)=delta epsilon (21/32,7/32,0).                    (9)
```

This peeling candidate also wins the coordinatewise deterministic envelope:

- the maximal scalar ray and positive barrier both accept
  `2 delta epsilon (1,1,1)`;
- the reflected candidate has increment
  `s/a=delta epsilon (4/9,19/18,37/18)`;
- every one of these increments is coordinatewise at most `u`.

The event variation from (8) is

```text
V=sum_{i<j}(-Q_ij)d_i d_j |tau_i-tau_j|
 = (7/8) delta^2 epsilon.                                  (10)
```

For comparison, (2) and (9) give the exact immediate response

```text
r_(k+1)=delta epsilon (238/513,112/513,49/513),             (11)
```

and its exact response energy is

```text
||r_(k+1)||^2+1/2||r_(k+1)||_Q^2
 = (876169/2807136) delta^2 epsilon^2.                      (12)
```

Already (10)--(12) disprove a same-round linear charge of `V` to response
energy.

## 4. Even the whole future response budget is too small

The stronger statement does not require knowing which safe-envelope branch
wins later.  Every safe-envelope continuation obeys

```text
0<=r_(j+1)<=x^(j+1)-x^j,
x<=x^(k+1)<=x^(k+2)<=...<=x*.
```

All vectors are coordinatewise nonnegative, hence

```text
sum_{j>=k} ||r_(j+1)||^2
 <= ||sum_{j>=k} r_(j+1)||^2
 <= ||x*-x||^2
 = (53762/625) delta^2 epsilon^2.                            (13)
```

Since `lambda_max(Q)=25/32`, (13) yields

```text
sum_{j>=k} (||r_(j+1)||^2+1/2||r_(j+1)||_Q^2)
 <= (2392409/20000) delta^2 epsilon^2.                       (14)
```

Combining (10) and (14),

```text
 V_k / (whole future response energy)
 >= 17500/(2392409 epsilon) -> infinity.                    (15)
```

This also explains why the alpha-free two-step event charge remains valid:
the first-order term is the same-round discarded-momentum debit
`zeta=(theta d-u)^Tt`, not future proximal descent.  In this family
`theta d-u=Theta(delta)` while `t=Theta(delta epsilon)`.  Any valid
accelerated proof must retain that oriented/discarded credit or impose a
genuinely chronological zero-start invariant; it cannot replace it by a
uniform delayed response-energy bank.

## 5. Scope and remaining boundary

The exact verifier is `safe_prox_event_response_counterexample_exact.py`.
It uses rational arithmetic and checks (3), (5)--(12), the branch
comparisons, and the constants in (13)--(15).

The zero-start simulations in `safe_prox_literal_envelope_audit.py` do not
exhibit this blow-up in the corresponding peeling-output diagnostic: on the
direct five-vertex graph the largest observed single-round
`V/response-energy` was about `2.30` down to `alpha=10^-5`; on the 80-vertex
endpoint path it was below `3.57` for the tested values
`alpha=10^-3,3*10^-4,10^-4`.  These are diagnostics, not a theorem.  The
remaining possible route is therefore sharply historical: prove that the
specific zero-start chronology forbids states like (5), or charge their
discarded momentum directly.  Positive-kernel response alone cannot do so.
