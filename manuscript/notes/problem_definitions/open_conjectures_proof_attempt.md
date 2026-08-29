# Proof attempts for OP1--OP3

Date: 2026-08-30

## Scope and status

This note uses `main.tex` in this directory as the only project-internal
mathematical source.  Public versions of the papers explicitly cited there
are used only to identify the guarantees of the named algorithms.  The three
questions are interpreted as affirmative conjectures.

The companion OP2 note now gives an affirmative proof of OP2 and, through
Proposition 3 below, OP1.  OP3 remains open.  The main concrete progress is:

1. an exact normalization and residual-to-semantic-error reduction;
2. a proof of the dependency chain `OP3 => OP2 => OP1` (with the standard
   materialized support-volume guarantee for OP3);
3. a single strengthened incremental active-set lemma that would imply all
   three desired bounds;
4. affirmative proofs in the parameter regimes
   `eps_ppr >= sqrt(alpha)` and `rho >= sqrt(alpha)` using the cited
   Wei--Yang guarantee;
5. a six-vertex counterexample to a tempting one-pass boundary-update lemma;
6. an exact identification of the remaining dynamic linear-algebra and
   boundary-reporting obstacle;
7. a support-safe maximal-extrapolation framework for OP2, together with a
   graph-realizable low-energy-decoy counterexample that refutes its proposed
   global scalar accelerated rate;
8. an exact-batch active-set route using one ordinary SDD solve and boundary
   scan per phase, without requiring the stronger fully dynamic primitive;
9. an exact reformulation of RPPR as a discounted optimal-stopping problem,
   under which the exact-batch method is monotone Howard policy iteration for
   a reversible random walk;
10. a graph-uniform Chebyshev/CG proof of the desired exact-batch depth rate
    in the `rho=0` limit; and
11. an exact endpoint-path formula showing that
    `Theta(1/sqrt(alpha))` batch phases are necessary for constant energy-gap
    reduction;
12. a block-Cholesky proof that exact first-violation batches halve the
    remaining RPPR energy every `O(1/sqrt(alpha))` phases on every graph and
    at every positive regularization level; and
13. a degree-thresholded approximate-SDD implementation whose activation and
    solve errors cost only an additive `eps_obj`, while every scanned support
    remains inside `S*(rho)`.

Throughout, `alpha` denotes the lazy parameter in `main.tex` and

\[
  beta := \frac{2\alpha}{1+\alpha}
\]

denotes the equivalent non-lazy parameter.  The case `alpha = 1` is
separable and is treated separately below.

## 1. Exact conversion to non-lazy degree coordinates

Let

\[
  L_\beta := D-(1-\beta)A,
  \qquad x=D^{1/2}y.
\]

Then

\[
  Q=\frac{1+\alpha}{2}D^{-1/2}L_\beta D^{-1/2}.
\]

Consequently, the PPR equation in degree coordinates is

\[
  L_\beta y_0=\beta s,
  \qquad \pi=Dy_0.
\]

Define the source residual of a candidate `y` by

\[
  r(y):=s-\beta^{-1}L_\beta y.
\]

### Lemma 1 (ACL residual implies the semantic error in OP1)

If `0 <= r(y) <= epsilon d` coordinatewise, then

\[
  0\le y_0-y\le \epsilon\mathbf 1
\]

and hence

\[
  \|D^{-1}(Dy-\pi)\|_\infty
  =\|y-y_0\|_\infty\le\epsilon.
\]

#### Proof

The matrix `L_beta` is a nonsingular M-matrix, so its inverse is
coordinatewise nonnegative.  Also

\[
  L_\beta\mathbf 1=\beta d.
\]

Since `L_beta(y_0-y)=beta r(y)`, inverse positivity gives

\[
  0\le y_0-y=\beta L_\beta^{-1}r(y)
  \le \epsilon\beta L_\beta^{-1}d
  =\epsilon\mathbf 1.
\]

This proves the claim.  In particular, the source-native ACL residual used
by Wei--Yang supplies the missing accuracy conversion mentioned in OP3.

### Lemma 2 (RPPR objective conversion)

Define

\[
  \Psi_{\beta,\rho}(y)
  :=\frac12y^TL_\beta y-\beta s^Ty
    +\beta\rho\|Dy\|_1.
\]

Then, exactly,

\[
  F_\rho(D^{1/2}y)=\frac{1+\alpha}{2}\Psi_{\beta,\rho}(y).
\]

Thus an additive gap `eps_obj` for `F_rho` is exactly the additive gap

\[
  \xi=\frac{2\,\mathrm{eps\_obj}}{1+\alpha}
\]

for `Psi`.

#### Proof

Substitute `x=D^{1/2}y`, use the displayed factorization of `Q`, and use
`(1+alpha) beta/2=alpha` in the linear and regularization terms.

## 2. Logical dependencies among the questions

### Proposition 3 (OP2 implies OP1)

An affirmative answer to OP2 implies an affirmative answer to OP1, with the
same success-probability convention.

#### Proof

Given `0 < eps_ppr < 1`, invoke OP2 with

\[
  \rho=\frac{\mathrm{eps\_ppr}}2,
  \qquad
  \mathrm{eps\_obj}=\frac{\alpha\,\mathrm{eps\_ppr}^2}{8}.
\]

The regularization-bias proposition in `main.tex` gives semantic PPR error at
most `eps_ppr`.  The OP2 work becomes

\[
  \widetilde O\!\left(\frac{1}{\rho\sqrt\alpha}\right)
  =\widetilde O\!\left(
      \frac{1}{\sqrt\alpha\,\mathrm{eps\_ppr}}
    \right),
\]

and the permitted dependence on the objective gap remains polylogarithmic.

### Proposition 4 (OP3 implies OP2 and OP1)

If OP3 returns an ACL `eps_appr` approximation in
`O_tilde(1/eps_appr)` fully charged work, then OP1 follows by choosing
`eps_appr=eps_ppr` and applying Lemma 1.  In fact this gives the stronger
bound `O_tilde(1/eps_ppr)`, since `alpha <= 1`.

OP3 also implies OP2, provided its fully charged output guarantee includes
the standard materialized support-volume bound
`vol(supp(p))=O_tilde(1/eps_appr)`.

To see this, call OP3 with `eps_appr=rho` and write its ACL output as
`p=Dy`, with source residual

\[
  r=s-\beta^{-1}L_\beta y,
  \qquad 0\leq r\leq\rho d.
\]

Then `y>=0` and

\[
  L_\beta y\geq\beta(s-\rho d).
  \tag{A}
\]

The RPPR minimizer `y*` is the least nonnegative supersolution of (A).  One
direct proof uses the monotone obstacle fixed-point map

\[
  T_\rho(z)
  :=\left[(1-\beta)D^{-1}Az
           +\beta D^{-1}s-\beta\rho\mathbf 1\right]_+.
\]

Inequality (A) is exactly `y>=T_rho(y)`.  Monotonicity gives a decreasing
sequence `y>=T_rho(y)>=T_rho^2(y)>=...`; contraction in the `D`-norm makes
it converge to the unique fixed point `y*`.  Hence

\[
  y\geq y^*,
  \qquad
  S^*(\rho)\subseteq U:=\supp(y).
\]

Restrict the RPPR objective to `U` and run a standard accelerated
proximal-gradient method there.  The restricted optimum is the global
optimum because `U` contains `S*(rho)`.  Each iteration costs
`O(vol(U))=O_tilde(1/rho)`, and the spectrum remains in `[alpha,1]`, so
`O(alpha^{-1/2} log(alpha/eps_obj))` iterations suffice.  Including the
OP3 call, the total fully charged work is

\[
  \widetilde O\!\left(\frac1\rho
  +\frac{1}{\rho\sqrt\alpha}
     \log\frac{\alpha}{\mathrm{eps\_obj}}\right)
  =\widetilde O\!\left(\frac{1}{\rho\sqrt\alpha}\right).
\]

Thus the dependency chain is `OP3 => OP2 => OP1`.  If OP3 were interpreted
without a support-volume/materialization guarantee, the first implication
would need that guarantee added explicitly.

## 3. A sufficient incremental active-set lemma

For `S` containing the seed, define the exact restricted state

\[
  y^{(S)}_S
   :=\beta L_{\beta,S}^{-1}(s|_S-\lambda d_S),
  \qquad
  y^{(S)}_{V\setminus S}:=0.
\]

Its boundary residual is

\[
  r_S(v)=\frac{1-\beta}{\beta}
          \sum_{u\in N(v)\cap S}y^{(S)}(u),
  \qquad v\notin S.
\]

The Wei--Yang active-set process repeatedly adds

\[
  T(S):=\{v\in\partial S:r_S(v)>(\lambda+\kappa)d_v\}.
\]

The following is the precise missing statement suggested by the proof
attempt.

### Incremental active-set lemma (unproved)

There is a randomized local data structure which, for the nested sets
generated above,

1. inserts each newly active vertex and its incident adjacency entries;
2. maintains a sufficiently accurate representation of `y^(S)`;
3. reports every boundary violation in `T(S)` without false negatives; and
4. materializes the final sparse output,

in total work

\[
  \widetilde O(\operatorname{vol}(S_{\rm final})),
\]

where the omitted factors are polylogarithmic in the inverse accuracy,
`1/beta`, and the inverse failure probability.  In particular, the work is
not the sum of the volumes of all intermediate sets.

### Consequences if this lemma is proved

- Set `lambda=kappa=eps_ppr/2`.  The active-set mass identity gives
  `vol(S_final) <= 2/eps_ppr`; Lemma 1 gives OP1 and the same result is OP3.
- Set `lambda=rho` and
  `kappa=min{rho, xi/(2 beta)}`, where
  `xi=2 eps_obj/(1+alpha)`.  The active sets stay inside the exact RPPR
  support and `vol(S_final) <= 1/rho`.  The standard active-set objective
  certificate then gives `O_tilde(1/rho)` work, which is stronger than OP2.

Thus the strengthened lemma is a common sufficient core for the three
questions.

## 4. Parameter regimes that already follow

Combining the classical local-push/ISTA bounds with the Wei--Yang active-set
bounds gives the currently available graph-uniform envelopes

\[
  \widetilde O\!\left(
    \min\left\{\frac1{\alpha\,\mathrm{eps\_ppr}},
                 \frac1{\mathrm{eps\_ppr}^2}\right\}
  \right)
\]

for semantic PPR (using Lemma 1), and

\[
  \widetilde O\!\left(
    \min\left\{\frac1{\alpha\rho},\frac1{\rho^2}\right\}
  \right)
\]

for RPPR with polylogarithmic objective-accuracy dependence.  The desired
bounds interpolate between the two terms in each envelope; the largest
remaining multiplicative gap is `1/sqrt(alpha)` near
`eps_ppr=alpha` or `rho=alpha`.

The public Wei--Yang theorem cited by `main.tex` gives, with high
probability, an ACL epsilon approximation in

\[
  \widetilde O(\epsilon^{-2})
\]

work and support volume at most `2/epsilon`.  By Lemma 1, this is also the
semantic accuracy required by OP1.  Therefore, if

\[
  \mathrm{eps\_ppr}\ge\sqrt\alpha,
\]

then

\[
  \frac1{\mathrm{eps\_ppr}^2}
  \le
  \frac1{\sqrt\alpha\,\mathrm{eps\_ppr}},
\]

so OP1 is affirmative in this regime.  Only
`eps_ppr < sqrt(alpha)` remains from the displayed target bound.

For RPPR, the same paper gives

\[
  \widetilde O(|S^*|\operatorname{vol}(S^*))
  =\widetilde O(\rho^{-2})
\]

work with only polylogarithmic dependence on the objective accuracy and
`1/beta`.  Here `|S^*| <= vol(S^*) <= 1/rho`.  Therefore, if

\[
  \rho\ge\sqrt\alpha,
\]

then

\[
  \rho^{-2}\le(\rho\sqrt\alpha)^{-1},
\]

so OP2 is affirmative in this regime.  Only `rho < sqrt(alpha)` remains.

When `alpha=1`, all three questions are elementary.  PPR is the point mass at
the seed, and RPPR has the single possible nonzero coordinate

\[
  (x_\rho^*)_v
  =\max\{0,(1-\rho d_v)/\sqrt{d_v}\}.
\]

A degree query and a constant-size output suffice.

## 5. Exact nested-system identities

Let `S' = S union T`, and write

\[
  L_{\beta,S'}=
  \begin{bmatrix}
    L_{\beta,S}&-C\\
    -C^T&L_{\beta,T}
  \end{bmatrix},
  \qquad C=(1-\beta)A_{S,T}.
\]

The new restricted solution obeys

\[
  y^{(S')}_T
  =\left(L_{\beta,T}-C^TL_{\beta,S}^{-1}C\right)^{-1}
    \left(h_T+C^Ty^{(S)}_S\right),
\]

\[
  y^{(S')}_S
  =y^{(S)}_S+L_{\beta,S}^{-1}Cy^{(S')}_T,
\]

where `h=beta(s-lambda d)`.  For a nonseed insertion batch,

\[
  h_T+C^Ty^{(S)}_S
   =\beta(r_S(T)-\lambda d_T)>0.
\]

These identities prove monotonicity, but they do not yet give a fast update:
the Schur complement is generally dense and the harmonic correction on `S`
is generally global.

There is also a useful energy budget.  Let

\[
  \phi(y)=\tfrac12y^TL_\beta y-h^Ty.
\]

For consecutive exact restricted minimizers,

\[
  \phi(y^{(S)})-\phi(y^{(S')})
  =\frac12\|y^{(S')}-y^{(S)}\|_{L_\beta}^2.
\]

Therefore these squared update energies telescope over all phases.  This is
a plausible amortization potential for a warm-started solver.  It does not,
by itself, pay for discovering boundary violations or materializing all
changed coordinates.

## 6. Grounded electrical-flow formulation

There is an exact obstacle-problem/flow interpretation that may be useful for
a different proof route.  Form an augmented graph by adding a ground vertex
`g`.  Give every original edge conductance `1-beta`, and connect each vertex
`i` to `g` with conductance `beta d_i`.  If `B` is the grounded incidence
matrix and `W` is the diagonal conductance matrix, then

\[
  B^TWB=L_\beta.
\]

Since the RPPR optimum is nonnegative, its degree-coordinate problem is

\[
  \min_{y\ge0}
  \left\{
    \frac12\|W^{1/2}By\|_2^2-h^Ty
  \right\},
  \qquad h:=\beta(s-\rho d).
\]

Fenchel duality gives the quadratic-flow problem

\[
  \min_f\ \frac12 f^TW^{-1}f
  \quad\text{subject to}\quad
  B^Tf\ge h.
\]

The dual slack is complementary to the positive primal support.  Thus RPPR
is a grounded electrical obstacle problem, and finding a new active vertex is
equivalent to finding a violated/slack-tightening vertex constraint.  Global
near-linear convex-flow machinery does not by itself prove locality, because
constructing its input or checking all inequalities scans the whole graph.
But this formulation isolates the local requirement as a separation/reporting
problem for the dual vertex inequalities, consistent with the boundary
component of the incremental active-set lemma.

## 7. A counterexample to one-pass boundary updates

A tempting lemma is false: it is not enough to update a boundary score only
when a newly activated vertex is adjacent to that boundary vertex.

Consider the six-vertex graph with edges

\[
  \{01,02,03,25,34,45\}.
\]

Thus vertex `0` has degree 3, vertex `1` has degree 1, and vertices
`2,3,4,5` have degree 2.  Use seed `0`, non-lazy parameter

\[
  \beta=\frac1{20},
\]

and `lambda=kappa=3/40`, so the activation threshold is
`(lambda+kappa)d_v=(3/20)d_v`.

For `S={0}`, the exact restricted solution is

\[
  y^{(S)}_0=\frac{31}{2400}.
\]

The three boundary residues at vertices `1,2,3` are all

\[
  r_S(1)=r_S(2)=r_S(3)
  =19y^{(S)}_0=\frac{589}{2400}.
\]

Vertex `1` violates its threshold `3/20`, but vertices `2` and `3` do not
violate their threshold `3/10`.  Hence only vertex `1` is inserted.

For the new set `S'={0,1}`, direct solution of the two-by-two system gives

\[
  y^{(S')}_0=\frac{563}{33560},
  \qquad
  y^{(S')}_1=\frac{409}{33560}.
\]

Vertices `2` and `3` are not adjacent to the newly inserted vertex `1`, but
their boundary residues become

\[
  r_{S'}(2)=r_{S'}(3)
  =19y^{(S')}_0
  =\frac{10697}{33560}
  >\frac3{10}.
\]

Both now violate.  Their scores changed only because the old coordinate at
vertex `0` changed globally after the restricted solve.  Therefore an
incremental proof must propagate harmonic changes from old active
coordinates, or answer boundary queries from an implicit representation; a
one-time scan of each newly inserted adjacency list is insufficient.

## 8. Why the most direct proof routes stop

### OP1: localized Chebyshev iteration

A degree-`O_tilde(1/sqrt(alpha))` polynomial approximates `Q^{-1}` in the
spectral norm.  A global Chebyshev solve therefore has the desired iteration
count.  The missing local invariant is a graph-uniform bound on the total
volume touched by its signed, nonmonotone intermediate vectors.  The
nonnegative residual-mass argument that proves APPR locality does not apply
to those iterates.  Truncating small coordinates introduces perturbations
whose accumulation has not been bounded in the semantic infinity norm at
the desired work.

### OP2: FISTA

If every accelerated iterate stayed inside the optimal RPPR support, the
standard iteration bound and `vol(S_rho^*) <= 1/rho` would prove OP2.
That premise is false on arbitrary graphs.  The cited 2026 Fountoulakis--
Martinez-Rubio paper gives seed-at-leaf stars on which standard FISTA
transiently activates the high-degree center and incurs graph-size-dependent
work even though the optimum stays on the seed.  This refutes the proof
strategy, not OP2.

A companion attempt replaces FISTA momentum by the largest scalar
extrapolation that preserves the subsolution order.  This succeeds completely
at locality: all scanned coordinates remain inside the exact optimal support.
It does not succeed at acceleration.  Active components of arbitrarily small
objective energy can still determine the global scalar momentum.  A family
of two-vertex active blocks with large private inactive neighborhoods forces
alternating contact and recovery steps, while a dominant degree-one block
contracts only as

\[
  \left(\frac{(1-\alpha)^2}{1+\alpha}\right)^k
\]

in relative energy after `k` steps.  For `k=Theta(1/sqrt(alpha))` this tends
to one.  Thus the global scalar-MSE rate is false; an energy-aware local or
multiscale momentum rule would be a genuinely new algorithmic requirement.

### OP3: solving each nested system from scratch

The final active volume is `O(1/eps_appr)`, but there may be
`O(1/eps_appr)` strict expansions.  A nearly-linear solve and a full boundary
scan at every phase therefore sum to `O_tilde(1/eps_appr^2)`.  Warm-starting
only the SDD solve is not enough: the six-vertex example shows that old
coordinates can change scores at boundary vertices that have no newly
inserted neighbor.  The unresolved primitive is a combined dynamic SDD
solve and dynamic boundary-heavy-hitter/reporting mechanism.

## 9. Output lower bounds: the locality factors are necessary

The linear dependence on `1/eps_ppr` in OP1 and OP3, and on `1/rho` in
OP2, cannot be improved even when the teleportation parameter is a fixed
constant.

### Proposition 5 (star output lower bound for PPR)

Fix a non-lazy `beta` strictly between zero and one.  Consider a star with
`m` leaves and use its center as the seed.  The exact PPR mass is

\[
  \pi_0=\frac1{2-\beta},
  \qquad
  \pi_i=\frac{1-\beta}{m(2-\beta)}
  \quad (i\text{ a leaf}).
\]

Every leaf has degree one.  Choose

\[
  m=\left\lfloor
      \frac{1-\beta}{2(2-\beta)\,\mathrm{eps\_ppr}}
    \right\rfloor
\]

for sufficiently small `eps_ppr`.  Then every leaf has degree-normalized
PPR value greater than `eps_ppr`.  A sparse semantic approximation cannot
omit any leaf, so it must emit `Omega(1/eps_ppr)` words.  A local algorithm
must also inspect `Omega(m)` center adjacency entries to learn their labels.

By Lemma 1, the same lower bound applies to an ACL approximation with this
accuracy.  Thus the `1/eps_appr` target in OP3 is output-optimal up to
logarithmic factors.

### Proposition 6 (star output lower bound for RPPR)

On the same star, assume all coordinates of the degree-coordinate RPPR
solution are positive.  Solving the two symmetry equations gives

\[
  y_0=\frac1{m(2-\beta)}-\rho,
  \qquad
  y_i=\frac{1-\beta}{m(2-\beta)}-\rho
  \quad (i\text{ a leaf}).
\]

Choose

\[
  m=\left\lfloor
      \frac{1-\beta}{2(2-\beta)\rho}
    \right\rfloor.
\]

For sufficiently small `rho`, all `m` leaf coordinates are positive and
each is `Theta(rho)`.  If the lazy objective-gap target is chosen below
`alpha y_i^2/2`, strong convexity implies that omitting even one leaf cannot
meet the requested gap.  This target is only polynomially small in `rho`, so
its logarithm is permitted by OP2.  Hence some instances require
`Omega(1/rho)` output work.  For constant `alpha`, the conjectured OP2 bound
matches this lower bound up to logarithmic factors.

## 10. Current verdict

| Question | Status of this attempt | Exact remaining regime/blocker |
|---|---|---|
| OP1 | affirmative, by Proposition 3 and the OP2 theorem in the companion note | no mathematical blocker remaining; implementation inherits the thresholded SDD solver from OP2 |
| OP2 | affirmative: thresholded exact-batch reoptimization uses `O_tilde(1/(rho sqrt(alpha)))` fully charged work and only logarithmic objective-gap precision | independent proof audit of the block-Cholesky and inexact-threshold arguments |
| OP3 | no arbitrary-graph proof | maintain nested SDD solutions and all boundary violations in total near-final-volume work |

The OP2 proof orders the final active support by its release batches and
factors the principal PageRank matrix as `LL^T`.  The phase corrections are
the blocks of `L^{-1}h`; a block was nonviolating one phase earlier, so the
nonnegative adjacent transfer dominates the next block.  Applying `L^{-1}`
to the block residuals accumulates `1,2,...,m` copies, while
`||L^{-1}||<=1/sqrt(alpha)`.  This gives a constant energy contraction every
`Theta(1/sqrt(alpha))` phases.  Degree-scaled activation threshold
`Theta(alpha sqrt(rho eps_obj))` absorbs approximate SDD solves and tiny
activation margins without leaving `S*(rho)`.  The stronger incremental
lemma is no longer needed for OP1 or OP2, but remains a possible route to
OP3's near-final-volume work.  The scalar global momentum rule remains
refuted and is not used by the proof.

## Public sources consulted

- Z. Wei and M. Yang, *A Simple Active-Set Method for PageRank-Based Local
  Graph Clustering*, [arXiv:2608.16339](https://arxiv.org/abs/2608.16339)
  (2026).
- K. Fountoulakis and D. Martinez-Rubio, *Complexity of Classical
  Acceleration for l1-Regularized PageRank*,
  [arXiv:2602.21138v2](https://arxiv.org/abs/2602.21138) (2026).
- D. Martinez-Rubio, E. Wirth, and S. Pokutta, *Accelerated and Sparse
  Algorithms for Approximate Personalized PageRank and Beyond*,
  [COLT 2023](https://proceedings.mlr.press/v195/martinez-rubio23b.html).
- D.-H. Li, Y.-Y. Nie, J.-P. Zeng, and Q.-N. Li, *Conjugate Gradient Method
  for the Linear Complementarity Problem with S-Matrix*, Mathematical and
  Computer Modelling 48 (2008), 918--928,
  [doi:10.1016/j.mcm.2007.10.017](https://doi.org/10.1016/j.mcm.2007.10.017).
