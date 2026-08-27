# Handoff: signed-spider-generalization

- Agent family: codex
- Role: direction
- Branch: `agent/codex/signed-spider-adaptive-spectral`
- Base commit: `a52f70e607d69d9674d1ef50da38e384c3440906`
- Assignment state: ready_for_review
- Write scope:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/signed-spider-generalization.md`
  - `manuscript/notes/README.md`
  - `manuscript/notes/registry.toml`
  - `manuscript/notes/signed_spider_generalization/`
- Permitted shared files: the same five paths above.

## Outcome

- Proved a fully charged face-specific tuning proposition. A certified upper
  Jacobi-radius bound gives the same finite SOR power estimate, with total cost
  `C_spec(U) + O(vol(U)/(gamma t_U) log(2/(gamma t_U tau)))` when the certified
  gap is at least `gamma t_U`.
- Identified the required certificate scale: this upper-bound tuning rule needs
  additive `O(t_U^2)` accuracy in the squared Jacobi radius for a
  constant-relative sweep rate, and that scale can be `Theta(alpha)`. A raw
  Rayleigh or power estimate from below is unsafe when silently used as the
  required upper certificate.
- Charged concrete estimation routes. Materializing the face block costs one
  degree-volume scan; a dense certified SVD has cubic real-arithmetic cost and
  quadratic workspace, plus encoding-dependent bit certification. A sparse
  estimator costs its actual number of face passes, with no graph-uniform pass
  count asserted without an estimator theorem.
- Extended the layered finite-propagation stop to every arbitrary finite
  scalar relaxation schedule whose literal local row updates remain grouped
  as one complete source-color block followed by the other color. Scalars may
  depend on the full history, randomness, exact eigenvalues, or global scalar
  reductions. The far layer remains unchanged for the same number of color
  blocks, so the relative-contraction and product-work stops survive.
- Proved the distinct zero-start polynomial light cone: every degree-`d`
  `p_d(Q)b`, and every scalar recurrence with at most `d` sparse PageRank
  matvec dependency layers, is supported within source distance `d`. The
  funnel therefore stops Chebyshev semi-iteration, unpreconditioned CG/Krylov,
  heavy ball, and variable Richardson through `Theta(1/sqrt(alpha))` complete
  matvec layers and at the same product-work scale.
- Recorded both sharp scope boundaries. An interleaved Gauss--Seidel
  permutation reaches the far funnel layer in one coordinate pass, so an
  order-free word “sweep” is invalid. Exact eigenvalues used only as scalars
  preserve locality; eigenvector transforms, nonzero global warm starts,
  inverse/Schur/Green responses, and dense preconditioners do not. `Q^{-1}`
  is an explicit one-step counterexample to any overbroad polynomial claim.

## Evidence

- `verify_adaptive_spectral.py` passes 146 exact-rational cells: 120 certified
  tuning cells, 11 adaptive scalar-SOR funnel cells including the interleaved
  witness, and 15 red/full-operator Krylov propagation cells.
- `verify_spider.py` and `verify_fixed_face.py` retain all prior exact and
  deterministic checks.
- The note builds to 31 pages with no undefined references, citations, or
  overfull boxes. Focused Ruff/format, note inventory and target audits,
  coordination/scope audits, diff checking, and the repository tests pass.

## Review notes

- Provider-owned paths changed: none.
- The fixed-face cost result is conditional on an actual certified upper
  radius; it does not treat a lower Rayleigh estimate or spectral
  preprocessing as free.
- The adaptive SOR theorem counts source-first color-block depth. It is not a
  theorem for arbitrary coordinate interleavings.
- The polynomial theorem counts sparse operator dependency layers from a
  seed-supported zero start. It deliberately excludes vector-valued spectral
  advice and nonlocal response/preconditioning.
- These results close scalar tuning and local-polynomial alternatives on the
  layered family; they do not lower-bound response composition, compressed
  quotient solves, or local discovery algorithms.
