# Independent audit of the practical schedules TeX transcription

Inspected: `practical_schedules_appendix.tex`, its fresh established source
notes, and the main document's seed notation and theorem labels. No TeX or
implementation file was changed by this audit.

Follow-up: root applied both corrections below. A fresh inspection confirms
the stated nontrivial regime, separate direct-branch costs, and omega as
the subgradient symbol. The logarithmic indices were also renamed to avoid
collision with the continuation parameter. The transcription now passes.

The mathematical transcription agrees with the source-energy,
binomial-block, independent-output-certificate, and integer-complexity
notes, subject to the following two corrections sent to root.

1. The explicit-complexity subsection needs the nontrivial regime
   `0<alpha<1` and `0<rho<1/d_seed` before defining its L and displaying the
   asymptotic bounds. The source corollary includes this restriction.
   Without it, arbitrarily large rho makes `ceil(log2(1/rho))` negative,
   so the displayed expression is not a valid unrestricted cost bound.
   The zero and alpha=1 branches should separately be stated to cost O(1)
   arithmetic/word operations and conservative O(B^3) bit work. An additive
   one gives an unrestricted asymptotic extension in an appropriately
   nonnegative parameter notation.
2. The independent-certificate subsection names its subgradient vector v,
   while v is the main document's point seed and also appears in the
   residual numerator's `1(i=v)`. Rename the subgradient vector throughout
   that subsection; the indicator should continue referring to the seed.

The following components were checked and require no mathematical change:

- Initial energy from complementarity; all three source-statistic bounds;
  the `3*alpha*r*eta` estimate; and preservation of both displayed bounds
  after upward replacement of H2.
- Common-denominator source formula, integer ceilings, one retained maximum
  degree denominator, and explicit charge for source computation even at
  zero accelerated steps.
- Half-block and binomial-block stopping comparisons, prefix exponents,
  zero-step certificate without Gamma, and terminal repair at zero steps.
- The positive truncated inverse-binomial inequality, strict beta<1/2,
  exact T=2/T=4 values, and constant-degree setup. Stored block powers have
  O(q) bits independent of T beyond its separate parameter encoding.
- Original-objective subgradient validity, locality to the supplied support
  and boundary, integer residual numerator, upward squared-norm sum, and
  the explicitly inconclusive interpretation of a larger bound.
- Final tolerance lower bound, nested default grids, K<=T*L, local exposed
  record count, complete-rebase frequency, repeated state/key visits,
  two-tree root cost, and the geometric `sum 1/r_j<3/rho` argument.
- The stage cost retains K+1, so zero-step initialization and terminal work
  are not omitted. The arithmetic ledger expressly includes integer
  quotient/remainder and is distinguished from the original arbitrary-real
  theorem. The bit statement separately includes parameter and encountered
  graph-word encodings, exact Fraction reductions, and oracle-internal
  computation rather than hiding those costs.

The TeX's bounds correctly concern the default complete wrappers. They do
not assert the lower-grid estimate for an independently invoked corrector
with an arbitrarily fine user-supplied grid. The new block factor changes
only a fixed stage endpoint; no stronger across-stage speed comparison is
asserted. Compilation and rendering remain root's responsibility.
