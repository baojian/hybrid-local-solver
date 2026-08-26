# Direction status: path_terminal_modal_block

Last reviewed: 2026-08-27
State: proved-open
Agent family: codex
Role: direction
Branch: `agent/codex/path-terminal-modal-block`
Base commit: `71764c15c5bc2bb92f01d9d807942acf61e4be85`

## Exact question and contract

- **Question:** Does the terminal full face of the named short endpoint-path
  transported-center execution require
  `Omega(q^-1 log(1/q))` consecutive fixed-face steps?
- **Model:** The finite endpoint path `P_m`, single endpoint seed,
  `q=1/(16m)`, `alpha=q^2`, and `rho=tau=q/5`, with ambient degrees, exact-real
  zero start, complete all-violations admission, transported estimate center,
  and the literal full-prefix state.
- **Accuracy namespace:** The note-scoped one-sided normalized KKT certificate
  `r_i(ell) >= -alpha*tau` on every active row. It is not the unresolved
  repository-wide stopping decision.
- **Support and inverse primitive:** Nested singleton path admissions followed
  by a fixed full face; the numerical primitive is the projected accelerated
  recurrence, not a persistent inverse oracle.
- **Access and charged work:** The named implementation has adjacency-list
  access and literally sweeps every visited path prefix. This note studies
  terminal step chronology only. It makes no unconditional eleven-resource
  lower bound and no lower bound for implicit response implementations or
  other algorithms.
- **Intended result:** Isolate a sufficient, falsifiable pair of lemmas for a
  logarithmic terminal block without promoting measured entry coefficients or
  conditional linear dynamics to an unconditional theorem.

## Claim ledger

- **Source:** The safe-envelope construction, transported-center update, and
  conditional full-face recurrence are imported from
  `volume_gated_acceleration` with their exact algorithmic scope.
- **Proved here:** The degree-weighted cosine basis and norms; the exact modal
  solution; the safe-envelope/global-range non-certificate implication; the
  ideal binomial packet's literal cosine coefficients; a uniform
  cosine-square inequality; and the conditional logarithmic block theorem.
- **Conditional:** If the actual entry quadratures track the ideal packet on a
  band of even modes and projection plus envelope subtraction remain inactive
  through the stated horizon, then every sufficiently large member requires
  at least `(1/8) q^-1 log(1/q)` terminal steps.
- **Measured:** For `m=128,256,512,1024,2048`, the actual floating trajectory
  has entry weighted residual mass between `0.972971 q^2` and
  `0.972986 q^2`, entry range about `1.49939 q^(5/2)`, modal defects below
  `0.009` on the screened
  `sqrt(m/log m)` band, positive projection/envelope margins, and first range
  crossing `q*k=3.1235,3.8711,4.3666,4.7131,5.0172`. For `m=128,256`, those
  crossings are not literal certificates because all residuals are still too
  negative; the actual certificate occurs later. The screen reports both.
- **Open:** Prove the entry quadrature inequality and the uniform
  projection/unclipped-envelope invariant in exact arithmetic.
- **Refuted:** A range crossing is not always a certificate when
  the residual maximum is negative. Characteristic roots or the measured
  table alone do not prove a logarithmic block. No frontier/seed surrogate
  replaces the moving global correction, and no general accelerated-local
  lower bound is claimed.

## Central blocker

1. **Entry packet lemma:** For
   `H_m=floor(sqrt(m/(64 log(16m))))`, prove the actual even-mode entry data
   `(C_(2s),D_(2s))` are within `1/64` relative error of the displayed ideal
   binomial packet for all `1<=s<=H_m`.
2. **Conditional-regime lemma:** Through
   `K_m=floor((1/8)q^-1 log(1/q))`, prove every raw proximal point is positive
   and every safe subtraction is strictly unclipped.

Either lemma is independently falsifiable by `verify.py`; changing the
constants is permitted only with a corresponding proof.

## Dependencies and reusable outputs

- **Formal registry dependencies:** `volume_gated_acceleration`.
- **Context/provenance:** The Round-013 terminal candidate motivated the
  direction; historical finite traces are not proof imports.
- **Reusable outputs:** Exact modal formulas, the weighted Popoviciu bridge
  from centered energy to residual range, and a deterministic screen that
  retains the literal global correction and transported-center semantics.

## Resume here

- **Exact pointer:** `main.tex`, Lemmas `lem:terminal-modal-packet` and
  `lem:terminal-modal-regime` are the two missing statements; Theorem
  `thm:terminal-modal-conditional-log` is ready to consume them.
- **Next action:** Derive an admission-by-admission signed residual recursion
  that bounds the physical-space remainder from the binomial packet in both
  the entry residual and its quadrature state.
- **Stop/go test:** Promote the logarithmic block only after both missing
  lemmas are proved uniformly in `m`; a larger floating screen is evidence but
  never a substitute.

## Verification

- **Deterministic screen:** `python3 verify.py 128 256 512 1024 2048`
  passed.  It reported first range crossings
  `q*k=3.123535156,3.871093750,4.366577148,4.713073730,5.017150879`
  and literal certificate times
  `q*k=3.733886719,3.985839844,4.366577148,4.713073730,5.017150879`.
  It also checks the exact combined entry-quadrature defect against `1/64`
  on `H_m`, labeling the check vacuous when `H_m=0`; the wider-band modal
  statistic remains a separate diagnostic.
- **Build:** A clean `latexmk` rebuild produced an eight-page PDF with no
  LaTeX, package, overfull/underfull, or undefined-reference warning.
- **Audits/tests:** `make note-audit`, `make note-targets`,
  `make agent-audit`, `git diff --check`, focused Ruff lint/format checks, and
  the 210-test suite passed.  The full repository `make lint` remains blocked
  by 1,345 pre-existing findings under
  `manuscript/claude-overnight-2026-08-24/`; the new verifier is Ruff-clean.
- **Known numerical boundary:** The screen is float64. The sibling note's
  rational checks for `m=2,4,8` cover only finite `1/(2q)` terminal prefixes.
