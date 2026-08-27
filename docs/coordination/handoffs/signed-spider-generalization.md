# Handoff: signed-spider-generalization

- Agent family: codex
- Role: direction
- Branch: `agent/codex/supplied-face-dispatch`
- Base commit: `b708d141b7b051a43cee4c3ebfa4308ad0dd6f3b`
- Assignment state: ready_for_review
- Write scope:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/signed-spider-generalization.md`
  - `manuscript/notes/README.md`
  - `manuscript/notes/registry.toml`
  - `manuscript/notes/signed_spider_generalization/`
- Permitted shared files: the same five paths above.

## Outcome

- Added a general supplied-face solver theorem, independent of bipartiteness.
  The normalized two-sided residual stop
  `||D_U^(-1/2)(c_U-Q_UU x)||_infinity <= alpha tau` implies semantic error
  at most `tau` by an exact principal M-matrix row-sum bound.
- Proved the exact interval Chebyshev residual factor
  `2 chi^k/(1+chi^(2k))`, with
  `chi=(1-sqrt(alpha))/(1+sqrt(alpha))`, and the safe single-seed shifted-load
  bound `||c_U||_2 <= sqrt(2) alpha`.  This gives the explicit product count
  `ceil(log(2 sqrt(2)/tau)/(-log chi))`.
- Proved the exact CG dimension cap with the degree-`s` error annihilator and
  degree-`s-1` solution polynomial.  Selecting exact CG or interval
  Chebyshev gives
  `O(vol(U) min{|U|, alpha^(-1/2) log(2/tau)})` charged real-arithmetic work,
  including sparse products, vector passes, and output.
- Added the supplied-correct-face PPR corollary: choosing
  `rho=tau=eps_ppr/2` and zero-padding the restricted iterate gives semantic
  PPR error at most `eps_ppr`.  Supplying or independently validating the
  exact RPPR support remains excluded.
- Kept the scope strict.  Polynomial iterates need not preserve the safe
  lower-envelope/admission invariants; changing faces invalidate the fixed
  operator and leave the unamortized restart sum.  Distributed reduction
  latency, finite-precision exact-termination loss, bit complexity, boundary
  discovery, and separate response/reporting resources are not claimed.
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
- Realized the safe sparse route with a componentwise Collatz certificate.
  For `M_a=(I+J_a)/2` and any positive start, the coordinate-ratio lower
  bounds increase and the upper bounds decrease to `rho(M_a)`. Aggregating
  the resulting singular-value intervals and checking
  `1-rho_bar^2 >= gamma^2(1-rho_under^2)` certifies the required relative
  gap. The scalar relaxation is frozen only after this check.
- Charged component discovery and every Collatz product as complete face
  scans. Each fixed face eventually certifies for `gamma<1`, but the Perron
  gap can vanish across a family, so there is no uniform scan count. A scan
  budget expires into the safe graph-global parameter with all failed passes
  charged.
- Audited the complete-face boundary: `sigma_U=1` forces the certified upper
  advice to equal the graph-global parameter, so the layered funnel receives
  no sweep improvement. The estimator vectors remain separate from the solver
  state, preserving the adaptive color-block light-cone scope.
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

- `verify_supplied_face_dispatch.py` uses exact rational arithmetic to audit
  the Chebyshev closed form, shifted-load norm, principal M-matrix semantic
  conversion, and CG annihilator off-by-one.
- `verify_adaptive_spectral.py` passes 244 exact-rational cells: 120 certified
  tuning cells, 98 componentwise Collatz/certification cells, 11 adaptive
  scalar-SOR funnel cells including the interleaved witness, and 15
  red/full-operator Krylov propagation cells.
- `verify_spider.py` and `verify_fixed_face.py` retain all prior exact and
  deterministic checks.
- Independent read-only promotion audit passed the spectrum, Chebyshev count,
  load norm, two-sided semantic conversion, CG off-by-one, empty-face branch,
  PPR bridge, SOR-factor comparison, and changing-face scope.
- The note builds to 36 pages with no undefined references, citations, or
  overfull boxes. Focused Ruff/format, note inventory and target audits,
  coordination/scope audits, diff checking, and the repository tests pass.

## Review notes

- Provider-owned paths changed: none.
- The fixed-face cost result is conditional on an actual certified upper
  radius; it does not treat a lower Rayleigh estimate or spectral
  preprocessing as free.
- The Collatz routine is a posteriori and exact/outward-rounded: unchecked
  floating ratios are not certificates, and bit certification remains an
  additional implementation cost. Its power vectors supply scalar bounds
  only and are never used as a warm start.
- The adaptive SOR theorem counts source-first color-block depth. It is not a
  theorem for arbitrary coordinate interleavings.
- The polynomial theorem counts sparse operator dependency layers from a
  seed-supported zero start. It deliberately excludes vector-valued spectral
  advice and nonlocal response/preconditioning.
- These results close scalar tuning and local-polynomial alternatives on the
  layered family; they do not lower-bound response composition, compressed
  quotient solves, or local discovery algorithms.
