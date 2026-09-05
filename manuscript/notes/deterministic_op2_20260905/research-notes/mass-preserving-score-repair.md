# Mass-preserving score repair

2026-09-05. **Proved cumulative work; accelerated convergence remains open.**
This is a separate candidate from the proved-rate averaged coupling method.

Use its degree-density notation, weighted mass `M(h)=sum_i d_i h_i`,
`s=sqrt(alpha)`, `q=1-s`, and score

\[
h=qv-K_d(u+sv)/(s(1+s))+sD^{-1}e_{seed}.
\]

The score has exact signed mass `B=q M(v)+s>0`. Define the repair

\[
R(h)=[h-\ell]_+,\qquad M(R(h))=M(h)=B,
\]

where `ell>=0` is the unique weighted simplex threshold (zero when h is
nonnegative). Then take

\[
v^+=[R(h)-s\rho]_+=[h-\ell-s\rho]_+,\qquad u^+=qu+sv^+.
\]

## Proved work bound and local implementation

If `Z=M(v)` and `V^+=vol(supp(v^+))`, then

\[
Z^++s\rho V^+\le M(R(h))=qZ+s.
\]

Consequently, from zero,

\[
s\rho\sum_{k<T}V_{k+1}
\le sT-s\sum_{k<T}Z_k-Z_T\le sT.
\]

In particular the cumulative auxiliary row volume is at most `T/rho`, and
both state masses stay at most one. The ordered reporter and cached PG
certificate from `averaged-positive-coupling.md` remain algebraically valid:
only the weighted threshold calculation changes. The score recurrence
depends on `u^+=qu+sv^+`, not on how v was selected. Computing ell uses
weighted rank-prefix queries with budget B and then adds `s rho` for reporting.
The fully charged implementation therefore costs `O_tilde(T/rho)`.
An accelerated iteration theorem would finish OP2, but none is proved here.

This arbitrary-T work statement uses the exact-real reporter without
rebasing its global multiplier. The floating-point prototype records its
occasional full-state rebases explicitly. Over an accelerated horizon their
number is polylogarithmic and the same bound would follow; without a rate
theorem, its rescaling cost must remain in the ledger. It is not silently
absorbed into an unconditional arbitrary-T practical-runtime claim.

## Proved fixed-point characterization

At any fixed point u=v=x (in density coordinates), the threshold equation is
the obstacle KKT system with regularizer `rho'=rho+ell/s`. In original
coordinates this is `Q x-c(rho')>=0`, complementary to x>=0.

For an obstacle solution at any rho', the corresponding prethreshold score
is nonnegative: on positive coordinates it is `x+s rho'`; on zero
coordinates it is the nonnegative source plus the off-diagonal neighbor
contribution, since `-K_d` has nonnegative off-diagonal entries. A nonnegative
score needs no mass repair, so ell=0. Thus the only fixed point is the desired
rho-regularized optimum. This does not exclude cycles or prove a rate.

## Proved order and mass properties of the repair map

On the domain `M(h)>0`, R is order-preserving, positively homogeneous, and
nonexpansive in weighted l1. To verify the latter two nontrivial claims,
work on a region with a fixed repaired positive set A. For a perturbation a,

\[
(DR(h)a)_i=a_i+\frac{\sum_{j\notin A}d_j a_j}{\operatorname{vol}(A)}
\quad(i\in A),\qquad (DR(h)a)_i=0\quad(i\notin A).
\]

Every derivative entry is nonnegative and each weighted column sum equals
the corresponding input weight. Hence the weighted l1 operator norm is one.
The continuous piecewise-linear map along a segment in `M(h)>0` gives the
global claims. Ordinary scalar soft thresholding after R is also
nonexpansive and order-preserving. These properties alone do not establish
accelerated convergence of the coupled recurrence.

## Proved energy accounting; the remaining signed term

For the current repair threshold ell, the auxiliary update is exactly an
orthant averaged-coupling step for the temporary objective
`phi_ell(x)=phi(x)+s ell w^T x` in original coordinates. The usual comparator
proof is valid for any feasible comparator, so it can still use the desired
optimum x*. After subtracting the extra linear objective terms and using
`X^+=qX+s Z^+`, it gives

\[
E^+\le qE+\alpha\ell(X^*-Z^+)
-\frac{\alpha q}{2}\|y-x\|^2
-\frac{\alpha s q}{2}\|z-y\|^2.
\]

Here `X*=w^T x*`; the threshold ell has degree-density units. Thus a concrete
remaining target is to control the discounted sum of
`ell_k (X*-Z_(k+1))`, after retaining the two negative terms. This sum is not
known to be nonpositive. In particular, numerical leaf-seeded stars can
have a positive repair threshold while `Z^+<X*`, even from zero. The whole
energy inequality may still contract because of its negative terms.

The finite-horizon identity obtained by iterating the displayed inequality
is rigorous, but no acceptable graph-uniform bound on its signed sum has
been proved. A claim that mass repair automatically improves the old
potential would be incorrect.

For clarity, the underlying algebra does not assume x* minimizes the
temporary objective. Write `p=q x+s z^+` and `a=q x+s x*`. The orthant
auxiliary step is the projection of `y-grad(phi_ell)(y)` onto `q x+s R_+^n`.
Smoothness, strong convexity, and this projection's variational inequality
give

\[
\phi_\ell(p)\le \phi_\ell(a)
+\frac{1-\alpha}{2}\|y-a\|^2-\frac12\|p-a\|^2.
\]

Strong convexity along the segment from x to x* bounds the first term by
`q phi_ell(x)+s phi_ell(x*)-alpha s q ||x-x*||^2/2`.
Since `p-a=s(z^+-x*)`, its last squared norm cancels the auxiliary part of
the new energy. The remaining norm identity is

\[
\frac{1-\alpha}{2}\|y-a\|^2
-\frac{\alpha sq}{2}\|x-x^*\|^2
=\frac{\alpha q}{2}\|z-x^*\|^2
-\frac{\alpha sq}{2(1+s)}\|z-x\|^2.
\]

Finally, `||y-x||^2+s||z-y||^2=s||z-x||^2/(1+s)`, which proves the
displayed energy accounting after removing the temporary linear load.

A constant step size eta in (0,1] instead uses `s=sqrt(eta alpha)` and
`h=qz-eta K y/s+b eta/s`, with prethreshold load still `s rho w` and signed
mass `q Z+s`. The same argument has one further favorable term
`-(1-eta)||p-y||^2/(2 eta)`. Its repair debit is still
`alpha ell (X*-Z^+)`, and its work proof is unchanged. Nevertheless, a
deterministic grid of 24,408 prescribed states still violates the standard
one-step potential at each tested eta in `{1,1/2,1/4,1/10,1/100}`. The result
is `results/mass-repair-step-size-states.jsonl`; this is numerical,
algorithm-specific, and does not refute a zero-start rate.

## Exact quadratic energy identity, retaining all dissipation

In original orthonormal coordinates put `K=Q-alpha I`, `p=q x+s z^+`,
`a=q x+s x*`, and

\[
\eta=[s\rho w+\ell w-h]_+.
\]

Then `z^+=h-(s rho+ell)w+eta`, `eta^T z^+=0`, and the following
is an **identity**, not only an inequality:

\[
\begin{aligned}
E^+-qE={}&\alpha\ell(X^*-Z^+)-\alpha\eta^T x^*
-\frac{\alpha sq}{2(1+s)}\|z-x\|^2\\
&-\frac12\|p-y\|_{I-Q}^2
-\frac12\|y-a\|_K^2
-\frac{sq}{2}\|x-x^*\|_K^2.
\end{aligned}
\]

Here both `K` and `I-Q` are positive semidefinite. To prove it, use the exact
quadratic expansion of `phi(p)-phi(a)` around y, together with
`p-y+grad(phi)(y)+s ell w=s eta`. The cross term becomes
`(||y-a||^2-||p-y||^2-||p-a||^2)/2`, plus the displayed multiplier terms.
Also use the exact segment identity
`phi(a)=q phi(x)+s phi(x*)-sq||x-x*||_Q^2/2`. The same alpha-part norm
identity as above completes the calculation. The exact rational prescribed
path-state audit now verifies this identity term by term as well.

The earlier two-term bound discards the three final nonnegative quadratic
terms and the orthant complementarity term. They cannot be omitted when
looking for a sharp zero-start proof. A new deterministic numerical probe
(`experiments/mass_repair_port_probe.py`) identified a zero-start radial
unit-tree case where the repair term exceeds the coarse coupling term by
over three thousand. This is now **exactly certified**: branches `[1,4]*4`,
426 actual unit-graph vertices, alpha=1/1000000, rho=1177637/40000000,
iteration 56. The exact ratio is about 3016.141514; the full energy still
contracts. All first 56 steps satisfy the exact energy identity and work
ledger. See `experiments/mass_repair_exact_zero_start_port.py` and
`results/mass-repair-exact-zero-start-port.json`. This refutes the coarse
proof inequality, not the desired rate.

Another proposed trajectory shortcut is false even from zero: repair need
not wait until the primal or auxiliary mass exceeds the optimal mass.
On the 100-ary unit tree of depth 4, alpha=1/1000000 and rho=1/400000000,
iteration 5 has ell>0, primal mass about 9.72e-6, auxiliary mass about
0.00423, and optimal mass exactly 989899/2000000. This is certified by
`experiments/mass_repair_exact_undershoot.py` and its JSON output.

An alternative exact bookkeeping form uses `e_X=X*-X` and the current ell:
the signed term equals `s ell (e_X^+-q e_X)`. Thus setting
`F_k=E_k-s ell_(k-1)e_(X,k)` leaves a variation term
`-sq(ell_k-ell_(k-1))e_(X,k)`, in addition to all negative terms above.
Neither positivity of this modified potential nor control of its variation
term is proved. In particular, ell need not be monotone.

## Proved conditional bound during a fixed auxiliary-support interval

Suppose the auxiliary support stays equal to a nonempty set S throughout an
interval, and write `V=vol(S)`. Outside S the primal density decays by q at
each step. Put `U_0=sum_(i outside S) d_i u_(k0,i)` at the start of that
interval. Since

\[
h=\frac q2(I+P_d)v-\frac{q}{2s}(I-P_d)u+sD^{-1}e_{seed},
\]

all negative h coordinates are outside the *next* auxiliary support, and
`[-h_i]_+<=q u_i/(2s)` there. Thus, on the fixed-support interval,
`H_(k0+j)<=q^(j+1) U_0/(2s)`.

If A is the repaired positive set, the exact repair mass equation gives
`ell vol(A)=H-sum_(0<h_i<=ell) d_i h_i<=H`. Since S is contained in A,

\[
\ell_{k_0+j}\le \frac{q^{j+1}U_0}{2sV}.
\]

The energy accounting above consequently implies, after r steps in the
interval,

\[
E_{k_0+r}\le q^r\left(E_{k_0}+\frac{sX^*U_0}{2V}\,r\right).
\]

This is a conditional fixed-support estimate, not a whole-run theorem.
Active-set changes can repeatedly create new primal history outside the
auxiliary support; their aggregate effect is precisely what remains to be
controlled. The displayed bound does not bound the number of such intervals.

## Numerical-score correction, 05:29 UTC

Dense equitable simulations must form h directly as `q z-K y/s+b/s` in
orthonormal quotient coordinates. Computing a raw regularized update and
then adding `s rho w` back can catastrophically cancel on enormous cells.
An old record incorrectly reported cumulative negative score mass near
`2.87e109`; direct formation on the same case gives about `0.0137082`.

The exact identity above gives the universal invariant `H<=q M(u)/(2s)`,
which is now asserted by the dense audit. Earlier extreme-cell H statistics
and repair convergence censuses require corrected replay. Numerical audit
notices mark those result directories. This does not alter the exact work,
fixed-point, order, energy-accounting, or fixed-support lemmas, nor the
deterministic local reporter, which maintains h directly.

## A certified obstruction to the old potential proof

The potential `E=phi(x)-phi(x*)+alpha||z-x*||^2/2` does not uniformly satisfy
`E^+<=(1-s)E` after repair. The exact witness uses a 128-vertex unit path,
seed 0, alpha=1/10000, rho=1/200, whose optimal support is the first 72
vertices. In density coordinates set

`x=x*+delta/d_100 e_100`, `z=x*/2`,
`delta=(1-M(x*))/10000`.

Exact rational arithmetic gives `(E^+-qE)/E=0.009430689681499922...>0`.
See `experiments/mass_repair_exact_state_witness.py` and its JSON result.
This is a prescribed feasible state, not a zero-start iterate, and therefore
refutes only that uniform one-step proof. Zero-start convergence, a modified
potential, and block contraction remain open. Initial deterministic
experiments are encouraging but cannot replace a proof.
