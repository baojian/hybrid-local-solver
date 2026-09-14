# Final independent audit of the consolidated proof dependencies

Scope: the consolidated `deterministic_conjecture2.tex`, its two included
appendices, the authorized `problem_definitions/main.tex`, and the newly
requested reading guide. This is a fresh mathematical dependency audit,
not an inference from earlier audits or implementation tests. No proof
file was edited.

**Conclusion:** I found no unresolved mathematical or local-work gap that
invalidates the deterministic Conjecture 2 theorem in its stated model.
The reading guide, as initially inspected, needed the nontrivial-regime
qualification described below. That is a summary qualification, not a gap
in the theorem, which already states the unrestricted `+1` bound.

## Dependency chain

1. **Graph facts and obstacle order.** The newly added foundational
   paragraph is correct. The normalized adjacency spectrum lies in
   `[-1,1]` (also directly from the edgewise inequality `2|ab|<=a^2+b^2`).
   Its nonnegative Neumann expansion gives inverse positivity. The same
   expansion applies to every principal submatrix, justifying the implicit
   `Q_II^{-1}>=0` used in the least-supersolution proof. Taking absolute
   values cannot increase the objective; uniqueness gives the nonnegative
   optimizer. At zero coordinates, Stieltjes signs give the missing lower
   source inequality. Multiplication by `w^T` then proves both mass and
   support-volume bounds. On the alleged violation set of a supersolution,
   the outside contribution has the correct nonnegative sign, so the
   least-supersolution argument and regularization monotonicity hold. The
   margin outside `supp(x*_(r/2))` follows by comparing two coordinates
   that are both zero; it is not an assumed complementarity margin.

2. **The one-comparator sector is applicable.** At a lower active box face,
   `(Qp-s)_i<=0`; at the upper face, it is at least
   `Q(4rw)_i-s_i>=0`. A binding unit-mass face contributes
   `gamma*(alpha-m_s)>=0`. These verify the signs of every Euclidean
   projection-normal component. Since `Qt=s`, their sum is precisely
   `<p-t,Q(raw-p)>`. This proves the needed inequality in the Q metric
   for the fixed analytical comparator `t`; it does not assume that the
   Euclidean projection is a Q projection or is Q-nonexpansive on arbitrary
   pairs. The smaller exact mass cap changes the final contribution to
   zero, retaining the proof. Both `t` and the true correction are feasible
   by source positivity and inverse positivity; neither is computed.

3. **Negative auxiliary energy causes no problem.** I re-derived the
   comparison identity in an arbitrary Hilbert metric. Smoothness cancels
   the gradient cross term; the sector cancels the projection-distance
   term; the two strong-convexity inequalities apply to any comparator.
   They give the stated negative remainder without assuming comparator
   optimality or a nonnegative comparison energy. The auxiliary metric
   gradient is exactly the algorithm's gradient, and its metric Hessian
   has spectrum in `[mu,1]`. The subsequent upper estimate uses
   `B_k<=a^k B_0<=3 lambda m_s`, whose last inequality is valid even if
   `B_0<0`. Dropping the nonnegative mirror and mass terms gives the
   residual bound, and adding the KKT source produces coefficient 18.
   No monotonic decrease of a negative energy's magnitude is needed.

4. **Residual control really pays for repeated supports.** Direct
   substitution with arbitrary permitted dyadic theta gives the stated
   mass recurrence with `beta0=(1-alpha)/(1+theta)<=1-theta`. The positive
   error starts at zero. On the selected set the lower normal vanishes,
   while the upper and cap normals subtract nonnegative mass. Summing
   the selected signed term and telescoping loses only nonnegative terms;
   column stochasticity is applied to nonnegative vectors. Cauchy uses
   selected degree weights, giving the displayed squared-response bound.
   The spectral comparison for `Q-mu I` is valid because it commutes with
   Q. The scalar inequality then gives 148 times `K/r`. This bounds every
   support appearance, not just the union or an iteration count.

5. **Repair closes the induction.** The main exact-real repair uses its
   stated conservative tolerance, not an appendix tolerance. Strong
   convexity gives norm error `alpha*delta`; `||Q||<=1` and `w_i>=1`
   justify the componentwise Q bound at retained positive coordinates.
   Uniform clipping and Stieltjes signs preserve a nonnegative source.
   Error support lies inside the optimizer's support, so complementarity
   removes the objective's linear term. The next parameter differs by at
   most a factor two, giving the next diffuse source and baseline order.
   The first source satisfies the same condition directly. The appendix's
   less conservative tolerances rely on their separate exact terminal PG
   step and, for the integer version, the extra downward grid rounding.
   Those are distinct proved repairs; their budgets are not interchanged.

6. **The exact reporter is a finite local construction.** Store only
   exposed records. A positive baseline row is scanned at source formation;
   a positive kinetic row is scanned at emission; ordinary averaging
   creates no positive primal coordinate outside that history. Thus an
   unexposed coordinate has zero source, state, and neighbor response,
   making its raw density strictly negative. No unexposed record can
   contribute to projection. Weighted positive-tail moments give the
   clipped mass exactly. A kth item in the implicit merge of two ordered
   breakpoint lists can be found by a partition search using tree rank
   queries in `O(log^2 N)` work; binary search over breakpoint ranks gives
   the claimed `O(log^3 N)` total. Flat intervals and exact ties allow a
   multiplier without an accuracy-dependent numerical search. The
   appendix's four-sequence bracket pruning gives its sharper `log^2 N`
   variant. No order-statistic or boundary operation is free.

7. **Complete work, tiny epsilon, and zero steps.** Each emitted row pays
   its full degree, including cached rereads. Previous/current exceptions,
   fixed-source refreshes, degree replies, response scatters, materialized
   historical primal state, and obsolete-record disposal all fit the
   stated per-stage ledger. Inactive high-degree boundary records pay
   scalar operations and degree replies, without a row scan. Final shift
   halving and the accelerated horizon introduce only logarithmic
   inverse-epsilon dependence; the stage inverse parameters sum
   geometrically. In the rounded appendices, scalar rebases are fully
   charged passes over retained history, closed-tail emission avoids
   materializing sub-grid positives, and exact terminal PG rereads its
   candidate support. Source/binomial zero-step stages report the initial
   energy bound but still pay setup, source statistics, materialization,
   and repair through the `(K+1)/r` term. Geometric checkpoints pay their
   own repeated cached scans and temporary state. The bit extension uses
   bounded common denominators and explicitly pays integer division; it
   does not import floor into the original arbitrary-real model.

## Explicit scope and remaining qualifications

The proof depends on the canonical simple undirected unit-edge graph,
positive integer degrees, point seed, and the declared charged local oracle.
In particular `w_i>=1` is used in the repair accuracy conversion. It makes
no claim for arbitrary fractional edge weights or general mixed sources.
Deterministic balanced comparison trees supply the stated map and rank
operations. Exact-real arithmetic is the core theorem's model; the
appendix's bit bounds additionally require rational parameters and include
encountered degree/label encodings. Expensive internals of a supplied oracle,
extra manual continuations, and extra diagnostics are separate charges.

The output is explicitly a sparse list representing the vector, as allowed
by the supplied problem definition: `(i,f_i,d_i)` represents
`x_i=f_i*sqrt(d_i)`. The theorem does not assume that evaluating a literal
square root is a free field-arithmetic primitive. The rounded algorithm's
constant-size representation is equally exact. Arbitrary fixed-precision
floating arithmetic is not certified by these arguments.

These are declared hypotheses and scope limits, not missing analytical
lemmas. The guide's initial wording, however, described every regularization
parameter while displaying the bound without the theorem's additive one.
I requested either a nontrivial-regime qualifier or the unrestricted
`Otilde(1+1/(rho sqrt(alpha)))` statement, and the same qualification for
its mass-deficit display. The core theorem already handles zero/direct
branches correctly. The rest of the guide's mathematical dependency
description and the three distinct repair budgets match the proof.
Its implementation-test counts are ancillary factual records, not premises
of this proof audit or newly reproduced tests.
