# Audit of the standalone TeX transcription

Audited `deterministic_conjecture2.tex` against the independently audited
complete argument. The TeX and its compile artifacts were not edited.

## Findings requiring attention

1. At the version read, line 133 has literal `qquad` rather than `\qquad`
   in the analytical-comparator display. This is a transcription typo,
   not an error in the underlying inequalities. It was reported to root.
2. The exact-real computational-model attribution was rechecked against
   authorized main.tex lines 193--202: it explicitly specifies that model,
   including scalar, comparison, stored-state, degree, adjacency, and output
   charges. The TeX attribution is correct; my initial concern is withdrawn.

Optional exposition improvements: “constant-size radical representation”
means a constant number of algebraic words, not bounded bit length; and
`E_k` is reused for an energy and later for a selected set. Neither changes
the proof, but “constant-word representation” and a separate selected-set
symbol would remove possible ambiguity.

## Mathematical transcription checks

- The objective, normalized Q, source b, zero regime, and alpha=1 output
  agree with the authorized definition.
- The theorem now correctly restricts the pure target bound to the
  nonzero regime and includes the additive O(1) term globally.
- The least-supersolution proof has the correct restricted-matrix
  inequality direction; its complement term is nonnegative before being
  subtracted.
- The half-rho exterior slack and degree-scaled infinity inequality have
  the correct signs.
- Baseline source bounds, comparator t, and the correction box/cap agree
  with the proved argument.
- The halved theta satisfies alpha/4<mu<=alpha, including alpha>1/4.
- Every term and coefficient of the four-line accelerated update is
  transcribed correctly.
- The Hilbert-metric comparison lemma is correctly stated and proved for
  a nonoptimal comparator. The sign of the projection sector and the
  negative remainder coefficient are correct.
- The auxiliary energy has coefficient alpha*lambda on its mass term;
  replacing alpha with mu there would be wrong, but the TeX retains alpha.
- The 18 alpha²r response bound follows from the displayed initial
  constants; no nonnegativity of the comparison energy is assumed.
- The general-mu raw identity retains Q-mu I and beta0=(1-alpha)/(1+theta).
  This is essential and is transcribed correctly.
- The selected signed-flow charge and Cauchy step correctly produce the
  coefficient 148, counting repeated kinetic support scans.
- Repair uses tau=alpha³delta²/2 and delta<=alpha*r/2. Its source and
  final objective estimates have the correct constants.
- The final delta-halving rule guarantees 2delta²/rho<=epsilon. All
  intermediate and final stages repair their approximate outputs.
- The explicit key has the correct factors theta, 1+theta, sigma, and w;
  its clipped tail-mass identity and translated breakpoints agree with
  the exact projection.
- Source refresh, response scans, emitted support enumeration,
  materialization, and obsolete-state deletion are included in the
  stated charge. The key formula supports those claims without an old
  primal scan.
- Degree-density output can retain f_i*sqrt(d_i). The theorem expressly
  excludes bit-complexity and floating-stability guarantees, so its
  operation count does not implicitly bound rational numerator sizes.

The mathematical transcription passes. Root reports that the qquad typo
and an additional compilation-detected escaped frac typo were corrected.
No new mathematical hole was found.

## Bibliography check

The supplied reference's author, title, and August 2026 date agree with its
front matter. The cited official COLT/PMLR page confirms Fountoulakis and
Yang, the 2022 title, and the source open complexity question:
https://proceedings.mlr.press/v178/open-problem-fountoulakis22a.html .
