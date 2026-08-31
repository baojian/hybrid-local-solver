# Direction status: class_separation_ladder

Last reviewed: 2026-08-30
State: proved-open
Agent family: claude (proof packages); codex (contract and source audit)
Role: direction
Branch: `main`
Base commit: `df0725fcf687`
Allowed write scope: the note directory plus its exact registry, generated
index, shared-command, coordination-record, and handoff integration files.

## Exact question and contract

- **Question:** On one instance, holding the primitive, fully charged work
  model, output representation, and accuracy guarantee fixed, how much work does each
  of three one-hop algorithm classes need, and which single axiom separates
  each class from the next?
- **Model:** Shared source-aligned PageRank quadratic
  (`subsec:shared-source-aligned-problem`), restated note-locally in the push
  scale `bold H = bold I - c_alpha bold A bold D^(-1)`,
  `gamma_alpha = 2 alpha/(1+alpha)`, state `(bold z, bold r)` with
  `bold r = gamma_alpha bold e_v - bold H bold z`. Instance: centre-seeded
  star `K_{1,m}`, `m = floor(1/(8 eps_ppr))`, `eps_ppr <= 1/16`.
- **Accuracy namespace:** The required sparse output is `xhat`; internally the
  note writes `zhat = pihat` and returns `xhat = D^(-1/2) zhat`. The guarantee
  is exactly `max_u |pi_u - zhat_u|/d_u <= eps_ppr`. The source-native APPR
  threshold `eps_appr` occurs only in the manuscript comparison; choosing it
  numerically equal to `eps_ppr` there is explicit and is not a namespace
  identification.
- **Access and charged work:** `W_adj = sum_t d_(u_t)` counts inspected
  adjacency entries. `Work` is the Problem-1 exact-real word work and also
  charges arithmetic, comparisons, state reads/writes, degree replies,
  conversion to `xhat`, and emitted output words. Hence `Work >= W_adj`, and
  every one-hop push costs `Theta(d_u)` fully charged. Preprocessing is not
  free. Policies may be adaptive, randomized, or batched; all lower bounds are
  pathwise. No finite-precision or bit-complexity claim is made.
- **Root scope:** This note addresses only semantic PPR Problem 1 and its
  graph-uniform `O-tilde(1/(sqrt(alpha) eps_ppr))` open target. It does not
  address RPPR Problem 2 or the nested-SDD reuse question.
- **Intended result:** A class ladder on one instance, plus an explicit
  statement of what it does not establish about the semantic problem.

## Claim ledger

- **Source:** The instance is the manuscript's `eq:hard-star-size`. The
  literal-APPR anchor for rung one is `thm:appr-star-lower-bound` with
  `prop:appr-upper-bound`; the certificate-stopped member bound compared
  against in rung two is `subsec:cf-star-lower`.
- **Proved here:** Rung one, `Omega(1/(alpha eps_ppr))` for the signed-step
  monotone class `M_pm` and hence for `M_+`, with explicit constants and a
  general-graph version carrying no instance constant
  (`lem:ladder-locality`, `lem:ladder-kappa-step`, `lem:ladder-terminal`,
  `thm:ladder-monotone-lower-bound`, `cor:ladder-monotone-constants`,
  `thm:ladder-monotone-general`). Rung two, `Omega(1/(sqrt(alpha) eps_ppr))`
  for the signed-relaxation class `R_pm`, via an energy identity, a fast-mode
  cap and an equal-magnitude displacement cap
  (`lem:ladder-energy`, `lem:ladder-fast-mode`, `lem:ladder-displacement`,
  `thm:ladder-signed-lower-bound`), together with a pathwise residual-mass cap
  extending it to one-hop output maps
  (`prop:ladder-residual-mass-cap`). Rung three, exact elimination on the star
  with `W_adj = 2m` and fully charged `Theta(m)` work
  (`prop:ladder-elimination`). The ladder itself,
  `cor:ladder-ladder`.

  Every one of these is **Proved-draft**: the argument is complete and written
  out, and it has not been independently audited. Nothing is promoted.
- **Imported upper:** SOR has a proved
  `O(log(1/alpha)/(sqrt(alpha) eps_ppr))` fully charged upper bound. Its source
  certificate is in the mass-residual scale; in the note's push scale the
  correct threshold is `gamma_alpha eps_ppr`, not `eps_ppr`.
- **Conditional:** The exact `Theta(1/(sqrt(alpha) eps_ppr))` order for `R_pm`
  is not proved. Removing the logarithm from the upper bound remains open.
- **Measured:** Tightness calibrations only, never the bounds themselves: the
  semantic-stop flatness `N(omega*) sqrt(alpha) in [1.35, 1.50]`; the
  `omega -> 2` member scan-work constant
  `W_adj sqrt(alpha) eps_ppr in [0.083, 0.094]`; the
  conjecture `Phi = 1` behind the open item below; and the
  `pi_v/gamma_alpha` scalings behind `prop:ladder-signed-general` outside
  closed-form families.
- **Refuted:** The reading of `thm:cf-spider-lower` as a semantic obstruction.
  On that instance `S_eps_ppr` is empty in the relevant regime, so the
  all-zero vector is a valid output at zero work; it is a certificate lower
  bound, and it is why the hard instance here is the star, which is
  semantically nontrivial (`obs:ladder-nontrivial`). The scope audit of that
  theorem is separate work and is not asserted in this note.
- **Corrected during contract audit:** A one-hop output map can yield a
  zero-*push* oracle escape, but not a zero-full-work Problem-1 algorithm;
  applying the map and emitting the answer remain charged. The transport cut
  now uses `H^(-1) r` in push scale, equivalently `pr(r_mass)` in mass scale.
- **Open:** `open:ladder-phi` (general-graph terminal bound for output maps
  near the escape threshold; equivalently whether `Phi = 1` when the seed
  maximizes `d_u pi_u`) and `open:ladder-beyond-star` (whether any
  bounded-seed-degree family forces the rung-two bound).

## Central blocker

`open:ladder-beyond-star`. The rung-two bound is star-specific through exactly
one quantity, the seed self-return amplification `pi_v/gamma_alpha`, which is
`Theta(1/alpha)` only because a degree-`Theta(1/eps_ppr)` seed reflects its
mass back in one step. Falsifiable form: exhibit a family with
`vol(S_eps_ppr) = Theta(1/eps_ppr)` and bounded seed degree on which every
`R_pm` member needs `Omega(1/(sqrt(alpha) eps_ppr))`; or prove that a
`Theta(1/eps_ppr)`-degree seed is necessary, making the star the unique hard
shape for one-hop relaxation.

## Dependencies and reusable outputs

- Formal registry dependencies: none.
- Source/shared prerequisites: `tex/shared/source_aligned_problem.tex`,
  `tex/shared/research_note_preamble.tex`, and the note-scoped declarations in
  `tex/shared/class_separation_ladder_commands.tex`. The shared problem
  fragment is synchronized with the current fully charged computational model;
  the class note adds only its push-scale dictionary.
- Context/provenance: transcribed from the campaign packages
  `w1_monotone_lb.md`, `i2d_separation_package.md`, `i4c_signed_class_lb.md`
  and `i5d_ladder_paper.md` under
  `manuscript/claude-overnight-2026-08-24/findings/`. The transcription
  changes medium, not content; two statements are marked as imported rather
  than re-derived (the transport characterization with its escape threshold,
  and the SOR block law with its certificate-stopped upper bound).
- Supplies to: the monotone rung generalizes `thm:appr-star-lower-bound` from
  literal lazy APPR to a class, which is the statement the introduction
  gestures at when it justifies the pivot to signed and response methods.

## Resume here

- Exact file/section/lemma:
  `sections/body/07_sec_ladder_manuscript_relation.tex`,
  `open:ladder-beyond-star`.
- Next concrete action: search bounded-degree families with
  `vol(S_eps_ppr) = Theta(1/eps_ppr)` for one whose seed self-return
  amplification is `Theta(1/alpha)`; the caterpillar and hub-ladder families
  already in the zoo are the first candidates, and
  `prop:ladder-signed-general` gives the measurable quantity to screen on.
- Stop/go test: if every bounded-seed-degree family in the zoo amplifies only
  `Theta(1/sqrt(alpha))`, promote the necessity direction to the primary
  target instead.

## Verification

- Source pointers checked: all eight manuscript labels cited by this note
  (`thm:appr-star-lower-bound`, `prop:appr-upper-bound`,
  `prop:appr-rppr-bridge`, `eq:hard-star-size`, `eq:appr-accuracy`,
  `subsec:cf-star-lower`, `eq:cf-opt-sor-identities`, `thm:cf-spider-lower`)
  were confirmed to resolve in `manuscript/sections/`.
- Focused build/checks run: `make` builds `main.pdf` (17 pages) with no LaTeX
  warning, unresolved reference, or overfull/underfull box. The rendered pages
  were visually inspected. `uv run python
  manuscript/claude-overnight-2026-08-24/i5d/verify_ladder.py` reproduces
  45 cells x 13 checks with 0 failures.
- Known gaps: the verification grid is dyadic only, so the general-`eps_ppr`
  constants are proved but not numerically exercised. The multi-base extension
  of the primitive-characterization lemma is proved only on the star. The
  checker was rerun in the repository's project environment; no result depends
  on the environment choice.

## Repository handoff

- Provider-owned paths changed: none.
- Shared paths changed in the current reconciliation:
  `manuscript/tex/shared/source_aligned_problem.tex` and
  `manuscript/tex/shared/class_separation_ladder_commands.tex`.
- Assignment state: ready_for_review
