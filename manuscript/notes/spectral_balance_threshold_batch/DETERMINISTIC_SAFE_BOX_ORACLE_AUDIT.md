# Deterministic near-linear safe-box oracle: reduction and source audit

Date: 2026-09-04

## Verdict

**Open.**  None of the audited primary-source theorems directly implements
one `SafeBoxLC` correction through `ABoxStop` in deterministic
`O_tilde(vol(S))` work.  There is, however, an exact and support-linear
reduction of the correction LCP to nonnegative quadratic flow diffusion on a
grounded graph.  A new exact one-sided repair now removes the output-format
gap:

```text
nonnegative objective-accurate quadratic point
    + one matrix product + a positive-barrier shift + cap-min
    => exact box feasibility + rowwise safety + a computable gap.
```

The required objective accuracy is only polynomially small in the current
state and canonical parameters, so it contributes logarithmically to a
solver whose cost is logarithmic in accuracy at that state.  This does not by
itself bound the whole-run precision as the current box width shrinks; the
oracle statement below explicitly charges precision dependence.  The
remaining gap is therefore algorithmic rather than a rounding or strict-
complementarity obstruction: no audited source supplies the approximate
nonnegative QP point in deterministic `O_tilde(vol(S))` work with that full
accounting.

The closest source results have one of five mismatches.

1. Chen--Peng--Wang solve the right nonnegative grounded-diffusion objective
   in randomized `O_tilde(vol(S))` time.  The repair below converts their
   output contract to `ABox` at sufficiently high polynomial accuracy, but
   their algorithm remains randomized.
2. Van den Brand et al. give a deterministic `m^(1+o(1))` convex-flow
   framework to high accuracy.  This is not `O_tilde(m)`, is not exact for
   quadratic costs.  The repair handles the certificate, but not the
   `m^(o(1))` overhead or the source theorem's precision qualifications.
3. Vladu solves nonnegative M-matrix quadratic programs in
   `O_tilde(|S|^(1/3) nnz(B_SS))` work, subject to the paper's linear-solve
   implementation qualifications.  The extra `|S|^(1/3)` factor already
   misses the target.  Its strictly positive central point can violate the
   cap before repair, but this is no longer a formal output obstruction.
4. K-matrix pivoting gives a linear number of exact pivots for one LCP, and
   SDD/Laplacian solvers accelerate a supplied linear face.  Neither theorem
   pays for exact sign decisions and changing-face discovery in near-linear
   total work.
5. Farfan--Ghadiri--Yang give a high-probability entrywise multiplicative
   approximation to one supplied SDDM linear system with nonnegative right
   hand side in almost-linear time.  This is substantially stronger
   coordinate information than an energy-norm solve, but it is randomized,
   applies after the linear face and right hand side are supplied, and does
   not solve the obstacle QP itself.  It is also randomized.

Consequently these sources do not close the desired deterministic total

```text
O_tilde(M/sqrt(alpha)),
    M=vol(supp(x_rho^*)).
```

They do identify a precise sufficient missing theorem: a deterministic
support-linear objective-approximate diffusion solver, followed by the proved
repair below.  Equivalently, one may state the combined primitive as the
**safe supersolution oracle** below.

## 1. Exact `ABox` interface

At one `SafeBoxLC` round, let `B` be symmetric Stieltjes with

```text
mu I <= B <= L I,             s=sqrt(mu/L),
```

and, on the already exposed face `S`, write

```text
hat_t=c_S-B_SS y_S,           u=y_S-x_S.
```

The computable certificate needed by the outer proof is

```text
0<=e<=u,
t=hat_t+B_SS e>=0,
zeta=e^Tt,
(1+s)zeta<=A(w;x,z),          w=y-e,              (ABoxStop)
```

where

```text
A(w;x,z)=.5||w-x||_B^2+(s mu/2)||z-w||_2^2.
```

The exact LCP solution has `zeta=0`.  Exactness is stronger than necessary:
any pair satisfying these displayed conditions preserves the outer
`1-sqrt(alpha)` contraction.  The inequalities `e<=u` and `t>=0` are exact
one-sided statements; small objective error alone does not imply either one.

**Proved here (least-supersolution fact).**  Let `e*` solve

```text
e*>=0,       t*=hat_t+B_SS e*>=0,       e*_i t*_i=0.
```

Every nonnegative supersolution `q` with `hat_t+B_SS q>=0` satisfies
`e*<=q`.  Indeed, if `E={i:e*_i>0}`, then

```text
B_EE(q_E-e*_E)>=-B_(E,S\E)q_(S\E)>=0,
```

and `B_EE^(-1)>=0`.  Since the supplied endpoint `u` obeys

```text
hat_t+B_SS u=c_S-B_SS x_S>=0,
```

the exact lower-orthant LCP automatically has `e*<=u`.  Thus an **exact**
nonnegative quadratic-program solver is sufficient; an approximate one does
not inherit this automatic cap.

## 2. Exact reduction to grounded quadratic diffusion

For canonical RPPR, let

```text
Q=alpha I+((1-alpha)/2)(I-D^(-1/2)AD^(-1/2)),
H=D_S^(1/2),                  beta=(1-alpha)/2,
K=H Q_SS H.
```

Set

```text
e=Hp,        h=H hat_t,       r=Ht=h+Kp,
U=H^(-1)u.
```

Then complementarity, the cap, and the gap are preserved exactly:

```text
0<=p<=U,       r=h+Kp>=0,       p^Tr=e^Tt=zeta.   (DegreeABox)
```

Moreover

```text
K=beta L(G[S])+diag(g),
g_i=alpha d_i+beta deg_(S^c)(i)>0.                (GroundedK)
```

Thus `K` is the Dirichlet matrix of the graph obtained by giving every
internal edge conductance `beta` and connecting vertex `i` to a ground node
with conductance `g_i`.  It has `O(vol(S))` nonzeros and can be formed from
the exposed adjacency lists in `O(vol(S))` work.

There is also a literal reduction to the pure-Laplacian dual used by
Chen--Peng--Wang.  Add a ground vertex `0`, let `L_bar` be the augmented
Laplacian, choose any `tau>0`, and put

```text
d_0=g^T U+tau.
```

Consider

```text
min_(p>=0,q>=0)
    .5 [p;q]^T L_bar [p;q]+h^Tp+d_0 q.             (GroundedDiffusion)
```

**Proved here.**  If `p*` is the exact correction in degree coordinates,
then `(p*,0)` is the unique optimum of `(GroundedDiffusion)`.  Its ordinary
vertex gradients are `h+Kp*=r*>=0`.  Its ground gradient is

```text
d_0-g^Tp* >= g^T(U-p*)+tau >0.
```

These are precisely the KKT conditions.  Uniqueness follows because the
augmented graph is connected, the Laplacian is strictly convex modulo
constants, and the total linear coefficient is positive.  Equivalently,
Fenchel duality turns this into separable quadratic flow with vertex
divergence upper bounds; nonnegative zero-cost slack arcs to a reservoir turn
those inequalities into fixed flow-balance constraints.

This is an algebraic reduction, not by itself the desired deterministic
algorithmic theorem.  A raw approximate solution of `(GroundedDiffusion)`
need not satisfy the cap or rowwise inequalities.  The following repair shows
that this output mismatch is removable without a complementarity margin.

## 3. Exact positive-barrier and cap-min repair

Let `B` be symmetric Stieltjes with `mu I<=B<=L I`, and suppose a known
positive vector `v` satisfies

```text
Bv>=mu v.
```

For `F(e)=hat_t+Be`, let `e*` be the complementary solution and let `u>=0`
be the known cap supersolution `F(u)>=0`.  Given any nonnegative
objective-approximate QP point `tilde_e`, compute

```text
gamma=max_i [-F_i(tilde_e)/(mu v_i)]_+,
qbar=tilde_e+gamma v,
q=min(u,qbar).                                      (BarrierCapRepair)
```

Then `qbar` is a nonnegative supersolution.  Supersolutions of a Stieltjes
system are closed under coordinatewise minimum: on a row where
`min(p,u)_i=p_i`, decreasing the other coordinates from `p` can only increase
that row because all off-diagonal entries are nonpositive; rows taking `u_i`
are identical.  Hence

```text
0<=q<=u,       F(q)>=0,       zeta=q^T F(q)>=0.
```

For canonical RPPR take `B=Q_SS`, `mu=alpha`, and
`v_i=sqrt(d_i)`.  The full identity `Qv=alpha v` gives

```text
Q_SS v_S=alpha v_S-Q_(S,S^c)v_(S^c)>=alpha v_S,
```

so the barrier hypothesis holds on every exposed face.

The repair also has a margin-free quantitative guarantee.  Suppose

```text
chi(tilde_e)-chi(e*)<=delta,
chi(e)=e^TBe/2+hat_t^Te,
v_min=min_i v_i,       V=||v||_2,
K=1+V sqrt(L/mu)/v_min,
R=||hat_t||_2+2L||u||_2.
```

Strong convexity gives `||tilde_e-e*||_B<=sqrt(2 delta)`.  Energy
Cauchy--Schwarz on each row gives

```text
gamma<=sqrt(2L delta)/(mu v_min),
||q-e*||_2<=K sqrt(2 delta/mu),
0<=zeta<=R K sqrt(2 delta/mu).                    (RepairGap)
```

At a SafeBoxLC round, writing `u=s(z-x)/(1+s)` and completing squares yields

```text
A(w;x,z)>=mu s ||z-x||_2^2/[2(1+s)]=:A0.          (BoxAllowance)
```

If `z!=x`, the explicit tolerance

```text
delta<=mu A0^2/[2(1+s)^2 R^2 K^2]
```

implies `(1+s)zeta<=A`.  If `z=x`, then `u=0`, `q=0`, and the test holds
without an inner solve.  Thus polynomially accurate nonnegative objective
optimization plus `(BarrierCapRepair)` is a certified `ABox` oracle; no
strict primal, dual, or cap margin is needed.  The complete proof is also
recorded in `POSITIVE_BARRIER_SAFE_SUPERSOLUTION_ROUNDING.md`.

The approximate optimization is still essential.  On a canonical
point-source unit edge there are strictly positive `SafeBoxLC` states for
which applying the same repair to `tilde_e=0` returns the safe cap but has

```text
(1+s)zeta/A=2(1+3s^2)/(5s(1+s))>1.
```

The same conclusion holds for every positive barrier direction `v` with
`Bv>0`, not only `v=1`: positivity confines `v_2/v_1` between `b/a` and
`a/b`, which makes the repair hit both cap coordinates.  Thus barrier repair
solves the exact one-sided-output problem, not the obstacle optimization
problem itself; the exact family is recorded in the same companion note and
verifier.

The elementary examples remain useful only as warnings against using a
raw approximate point or clipping it without first constructing a second
supersolution.  They are not obstructions to the repaired pipeline.

## 4. Primary-source comparison

| Source | Randomness and output | Stated work | What it actually solves | Safe-box verdict |
| --- | --- | --- | --- | --- |
| Koutis--Miller--Peng (FOCS 2011), Theorem 4.6 | Randomized/expected; energy-norm approximate linear solution | `O_tilde(m log n log(1/eta))` | One supplied SDD linear system | Useful only after a correction face is known.  It does not identify the face or certify coordinatewise signs/caps. |
| Farfan--Ghadiri--Yang (2025), Theorem 1.1 | Randomized/high probability; two-sided entrywise multiplicative approximation | `O_tilde(m 2^(O(sqrt(log n))) log U log^2(U/(epsilon delta)))` bit operations, for integer data and non-exponentially-small `epsilon` | One supplied SDDM linear system with nonnegative right hand side | Stronger coordinate information than an energy-norm solve, but the obstacle face and right hand side must already be known; it does not solve the QP and is not deterministic. |
| Kyng--Meierhans--Probst Gutenberg (FOCS 2022), main Eulerian-solver theorem | Deterministic; approximate pseudoinverse | `m^(1+o(1)) log(1/eta)` under polynomial edge-weight and normalized-gap assumptions | One supplied directed Laplacian system | Removes randomness, but not the obstacle/LCP layer; it is also almost-linear rather than `O_tilde(m)`. |
| Li--Vaughn (2026), main sparsification theorem | Deterministic spectral sparsifier | `m^(1+o(1))+O(n^2 epsilon^(-9/2) log^(113/2+o(1)) n)` | `(1+/-epsilon)` spectral sparsification, advertised for dense graphs | Does not replace Chen--Peng--Wang's randomized sparsifier within `O_tilde(m)` on a sparse local face; when `n=Theta(m)`, the displayed `n^2` term is prohibitive. |
| Chen--Peng--Wang (FOCS 2021), Theorem 1.1 and generalized-diffusion definitions | High probability; exactly lower-bound-feasible potential with relative objective accuracy | `O(m log^8 n log(1/epsilon))` | Nonnegative quadratic flow diffusion / generalized diffusion | The grounded `K` objective is directly a generalized diffusion with quadratic vertex weights; `(BarrierCapRepair)` converts sufficiently accurate nonnegative output to `ABox`.  Randomness remains. |
| Vladu (STOC 2025), nonnegative-QP theorem and runtime corollary | Optimization theorem is an IPM analysis; generic M-matrix scaling invoked in the runtime proof is high probability, and the paper explicitly idealizes exact linear solves | `O_tilde(n^(1/3) nnz(A) log(1/epsilon))` | Nonnegative symmetric-M-matrix QP to additive objective error | `(BarrierCapRepair)` handles the cap/certificate, but the `n^(1/3)` factor and implementation qualifications remain. |
| Foniok--Fukuda--Gärtner--Lüthi (DCG 2009), Theorem 5.6 and Corollary 5.10 | Deterministic exact pivot path given an exact vertex oracle | At most `n` pivots from zero, `2n` from an arbitrary cube vertex | One K-matrix LCP | The vertex oracle evaluates a complementary basis via a principal solve and global signs.  Pivot count is not near-linear arithmetic or local-access work. |
| Végh (quadratic-cost-flow result) | Deterministic exact algorithm in the rational/arithmetic model | `O(m^4 log m)` | Separable convex quadratic minimum-cost flow | Exact but far from near-linear; it does not supply the target local complexity. |
| Chen et al. (FOCS 2022) | Randomized framework; high-accuracy convex extension | `m^(1+o(1))` | Exact integral linear min-cost flow; general edge-separable convex flow only to high accuracy | Quadratic flow is covered only approximately, and the exponent is not `O_tilde(m)`. |
| van den Brand et al. (FOCS 2023), Theorem 1.1 and following convex-cost remark | Deterministic | `m^(1+o(1)) log U log C` for exact integral linear min-cost flow; convex edge costs to high accuracy in `m^(1+o(1))` | Min-cost flow and convex edge-cost extensions | The convex extension is approximate but can be followed by `(BarrierCapRepair)` if its guarantee is instantiated on this QP; the `m^(o(1))` and precision qualifications still miss the target. |

Source-specific qualifications matter:

- Chen--Peng--Wang state that spectral-sparsifier construction is their only
  randomized component.  `(BarrierCapRepair)` now handles their objective-
  accuracy output contract.  Replacing the sparsifier is still not an
  immediate deterministic theorem: the replacement must preserve their
  recursive running-time and accuracy analysis on the grounded instance.
- The August 2026 Li--Vaughn theorem is a genuine deterministic
  `(1+/-epsilon)` sparsification advance, but its stated running time contains
  an `n^2` term and is aimed at dense graphs.  It therefore does not furnish a
  sparse-face `O_tilde(m)` drop-in replacement.
- Their graph model assumes the ratio of largest to smallest conductance is
  polynomial in the number of vertices.  In `(GroundedK)` this ratio can
  include `1/min{alpha,1-alpha}`; an unrestricted `alpha` needs an extension
  or an explicit dependence on its encoding/weight ratio.
- Vladu's canonical runtime corollary suppresses polylogarithmic dependence on
  condition number and numerical scales, but it retains `n^(1/3)` iterations.
  Its paper notes that the displayed implementation assumes exact linear
  solves and calls the tolerance of approximate solves by IPMs folklore.
- Exact integral min-cost-flow rounding does not transfer to irrational or
  rational quadratic optima.  The deterministic 2023 theorem itself labels
  its convex-cost extension as high accuracy, not exact.

Primary sources:

- Ioannis Koutis, Gary L. Miller, and Richard Peng,
  [*A Nearly-`m log n` Time Solver for SDD Linear Systems*](https://arxiv.org/abs/1102.4842),
  FOCS 2011, Theorem 4.6.
- Angelo Farfan, Mehrdad Ghadiri, and Junzhao Yang,
  [*Entrywise Approximate Solutions for SDDM Systems in Almost-Linear
  Time*](https://arxiv.org/abs/2511.16570), arXiv:2511.16570,
  Theorem 1.1.
- Rasmus Kyng, Simon Meierhans, and Maximilian Probst Gutenberg,
  [*Derandomizing Directed Random Walks in Almost-Linear Time*](https://arxiv.org/abs/2208.10959),
  FOCS 2022, `solver.tex` main Eulerian-solver theorem and Section 1.
- Jason Li and Trevor Vaughn,
  [*Deterministic Spectral Sparsification in Almost-Linear Time for Dense
  Graphs*](https://arxiv.org/abs/2608.13910), arXiv:2608.13910, main theorem.
- Li Chen, Richard Peng, and Di Wang,
  [*2-Norm Flow Diffusion in Near-Linear Time*](https://arxiv.org/abs/2105.14629),
  FOCS 2021, Theorem 1.1, Section 2.1, and the generalized-diffusion
  definitions.
- Adrian Vladu,
  [*Breaking the Barrier of Self-Concordant Barriers: Faster Interior Point
  Methods for M-Matrices*](https://arxiv.org/abs/2504.20619), STOC 2025,
  Section 1.1's nonnegative-QP theorem, the runtime corollary, and the
  M-matrix-solver section.
- Jan Foniok, Komei Fukuda, Bernd Gärtner, and Hans-Jakob Lüthi,
  [*Pivoting in Linear Complementarity: Two Polynomial-Time Cases*](https://arxiv.org/abs/0807.1249),
  *Discrete & Computational Geometry* 42(2), 2009, Theorem 5.6 and
  Corollary 5.10.
- László A. Végh,
  [*Strongly Polynomial Algorithm for a Class of Minimum-Cost Flow Problems
  with Separable Convex Objectives*](https://arxiv.org/abs/1110.4882),
  *SIAM Journal on Computing*; quadratic-cost theorem.
- Li Chen, Rasmus Kyng, Yang P. Liu, Richard Peng, Maximilian Probst
  Gutenberg, and Sushant Sachdeva,
  [*Maximum Flow and Minimum-Cost Flow in Almost-Linear Time*](https://arxiv.org/abs/2203.00671),
  FOCS 2022, main theorem and Section 10.
- Jan van den Brand, Li Chen, Rasmus Kyng, Yang P. Liu, Richard Peng,
  Maximilian Probst Gutenberg, Sushant Sachdeva, and Aaron Sidford,
  [*A Deterministic Almost-Linear Time Algorithm for Minimum-Cost
  Flow*](https://arxiv.org/abs/2309.16629), FOCS 2023, Theorem 1.1 and the
  convex-edge-cost remark immediately following it.

## 5. Complexity consequences

### Supplied face is not the obstacle problem

If an exact active set `E={i:e*_i>0}` were supplied, then

```text
B_EE e*_E=-hat_t_E,       e*_(S\E)=0,
```

followed by sign checks solves the LCP.  A fast SDD solver accelerates this
linear algebra.  It does not supply `E`; approximate energy error also does
not justify the exact sign checks when a coordinate is arbitrarily close to
zero.  Combining a linear pivot bound with a near-linear solve independently
at each pivot gives at best a repeated-solve bound, not one near-linear LCP.

### Condition-number methods lose the outer square root

For canonical `Q`, `alpha I<=Q<=I`.  A fresh deterministic
Chebyshev/projected first-order solve therefore uses

```text
O_tilde(alpha^(-1/2))
```

matrix products, each costing `O(vol(S))` on the supplied face.  The outer
linear-coupling loop already has `O_tilde(alpha^(-1/2))` rounds.  Applying
this fresh bound independently gives `O_tilde(M/alpha)`, not
`O_tilde(M/sqrt(alpha))`.  This multiplication is an upper-bound diagnosis,
not a lower bound against recycling.

### What the available flow solvers give after repair

The proved rounding lemma means that a sufficiently accurate solver for the
grounded nonnegative QP really does produce `ABoxStop`.  Applied directly to
the `K` objective as a generalized diffusion with quadratic vertex weights,
Chen--Peng--Wang therefore gives a randomized
`O_tilde(M/sqrt(alpha))` completion, subject to the theorem's recursive
accuracy and numeric-scale qualifications stated above.  This conclusion
does not extract `p` from an approximate augmented-ground pair, whose ground
coordinate could obscure the original QP gap.  It is outside the requested
deterministic model.

The 2023 deterministic framework would instead give roughly

```text
M^(1+o(1))/sqrt(alpha)
```

over the outer loop, with additional precision/weight-scale qualifications.
The `M^(o(1))` factor is not hidden by this project's `O_tilde` notation.

## 6. The exact missing theorem

The following deterministic primitive is sufficient for the desired
implementation.

> **SafeSupersolution oracle (open).**  Given an exposed canonical face `S`,
> its grounded SDDM matrix `K`, vectors `h,U` with `U>=0` and
> `h+KU>=0`, and the current computable allowance `A>=0`, return in
> `O_tilde(nnz(K))=O_tilde(vol(S))` work a pair `(p,r)` satisfying
> 
> ```text
> 0<=p<=U,       r=h+Kp>=0,       (1+s)p^Tr<=A.
> ```
> 
> All adjacency exposure, arithmetic, output writes, one-sided sign
> certification, and precision dependence are charged; no final active set,
> ambient preprocessing, or strict-complementarity margin is supplied.

Invoking this oracle once in each of
`O_tilde(alpha^(-1/2))` outer rounds and using `vol(S_j)<=M` would close

```text
sum_j O_tilde(vol(S_j))
    <= O_tilde(M/sqrt(alpha)).
```

The grounded-diffusion reduction proves that the open primitive is not a new
algebraic problem class, and `(BarrierCapRepair)` removes the one-sided
rounding and active-face-identification issue.  The missing content is now a
deterministic, genuinely `O_tilde(nnz(K))` objective-approximate solver for
that nonnegative quadratic diffusion, with the stated local and precision
accounting.  None of the audited SDD, diffusion, convex-flow, IPM, or K-LCP
source theorems currently supplies it.

## 7. Claim status

**Source.**  The complexity and output guarantees in the comparison table are
attributed only to the linked primary papers.

**Proved here.**  The exact degree-coordinate reduction, the augmented-ground
reduction `(GroundedDiffusion)`, uniqueness of `(p*,0)`, automatic upper cap
for the exact least supersolution, supersolution min-closure,
`(BarrierCapRepair)`, and its explicit margin-free objective-accuracy bound.

**Conditional.**  The randomized `O_tilde(M/sqrt(alpha))` consequence after
instantiating the audited generalized-diffusion solver with the required
polynomial accuracy, and the deterministic
`M^(1+o(1))/sqrt(alpha)` consequence after instantiating the deterministic
convex-flow framework with its stated qualifications.

**Open.**  The `SafeSupersolution` oracle and hence a deterministic
`O_tilde(M/sqrt(alpha))` implementation of `SafeBoxLC` through `ABoxStop`.

**Refuted.**  The black-box implications “near-linear SDD solve implies
near-linear LCP,” “a raw approximate QP point is already `ABox`,” and “exact
integral min-cost-flow rounding makes quadratic flow exact.”  Objective
accuracy *with* `(BarrierCapRepair)` is a valid `ABox` interface.
