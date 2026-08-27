# Direction status: path_terminal_modal_block

Last reviewed: 2026-08-28
State: proved-open
Agent family: codex
Role: direction
Branch: `agent/codex/path-terminal-static-cone`
Base commit: `0d6ed658be4aa9bee01e6d520e066d83e3797936`

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
- **Intended result:** Isolate sufficient, falsifiable chronology,
  entry-profile, and terminal-regime lemmas for a
  logarithmic terminal block without promoting measured entry coefficients or
  conditional linear dynamics to an unconditional theorem.

## Claim ledger

- **Source:** The safe-envelope construction, transported-center update, and
  conditional full-face recurrence are imported from
  `volume_gated_acceleration` with their exact algorithmic scope.
- **Proved here:** The degree-weighted cosine basis and norms; the exact modal
  solution; the identity `D_h=q*cot(phi_h)*V_h`; explicit proper-prefix and
  full-path restricted optima; the rank-one proper-prefix displacement and
  bound `0<b_n-b_(n-1)<=q*artanh(q)`; the interior directional factorization;
  the safe-envelope/global-range non-certificate implication; the ideal
  binomial packet's literal cosine coefficients; exact nonnegative full-face
  position/velocity kernels with row sums `1` and `k`; pointwise nonpositive
  ideal evolution; a uniform cosine-square inequality; and the conditional
  logarithmic block theorem. Also proved are the uniform prefix-frontier
  bounds `3488 q^2/1921 <= P_n <= 33q^2/16` and an exact chronology reduction:
  the shared-coordinate sign `D_n(j)>=0` implies raw positivity, nonpositive
  post-step residual, zero correction, and strict next-singleton admission,
  with raw-frontier lower constant `596861/326570` and strict rational gate
  slack. The reflected ideal packet splits `D_n` into an explicit nonnegative
  Pascal term and a correction difference `K_n`; the correction has a closed
  residual-only old/new-row recurrence and exact signed frontier triplet.
  Its correction-difference Green kernel satisfies
  `L_k=R_+^(k-1)+((1-q)/2) S_- J_(k-1)`, hence is coefficientwise
  nonnegative with row mass `((k+1)/2)(1-q)^(k-1)`. At `q=0`, the infinite
  constant-`U` derivative response also has a coefficientwise nonnegative
  generating series. The exact all-prefix leading correction generating
  function proves
  `c_n(j)-c_(n-1)(j)/2 >= 1/80` on every shared coordinate, sharply at
  `(n,j)=(4,2)`. The finite-`q` rescaling, stopped derivative-kernel bound,
  source total-variation and mass estimates, and exact initial response prove
  `K_n(j)>0` for every shared coordinate when `m>=64`, with rescaled margin
  `179/14400` for `n>=6`; an analytic perturbation handles `n<=5`. Hence the
  proper-prefix projection-inactive, zero-correction, exactly-next-singleton
  chronology is proved in the asymptotic range. The exact
  seed/last-three-frontier changing-face defect (including the final
  ambient-degree-one endpoint term), its even-extension transform
  `U_n(1-z)(1+3z)+M_n*z^2`, the bounds
  `0<U_n<=3q^3/40`, `|M_n|<=3q^4/2`, and the scalar position/velocity reduction
  then follow algebraically. On the full face, splitting the even ideal packet
  into two half-endpoint packets with opposite directed velocities proves that
  their complete `K/J` evolution is coordinatewise nonpositive. The literal
  entry correction `c=r_0-g` is also coordinatewise nonpositive for every
  `m>=64`. The infinite-line coefficient of `J_k` is the binomial tail
  `Pr(Bin(k-1,1/2)>=|r|)`; after cycle folding its maximum is at most
  `1+(k-1)/(2m)`. Hence positive residual is bounded exactly by this factor
  times the positive weighted mass of one static directed-velocity remainder.
  That remainder is now deconvolved exactly as `u=Ld`, where `d` is given
  coordinatewise by the last proper-prefix residuals and a lower binomial
  packet. The coefficient of `J_k L` is an explicit finite binomial window,
  so both remaining regime targets are finite signed convolution inequalities.
  For every `m>=64`, the signed static mass is now proved below `3q^3/50`,
  and the normalized endpoint value `beta=d_m/q^3` is proved to lie in
  `(-57/200,0)`. Comparing `d` with its exact endpoint geometric tail `h`
  then proves the desired `21q^3/80` positive-mass bound conditional only on
  `d>=h`, including the finite seed-endpoint correction. A local sufficient
  interface is explicit: `E_1>=0`, `F_2>=E_1/2`, and
  `F_r>=F_(r-1)/2`. Independently, if `C_n` is the prefix correction and
  `K_n=C_n-(1-q)C_(n-1)/2`, the exact temporal decrement
  `T_m=(1-q)K_(m-1)-K_m` satisfies
  `d_j=2(1-q)(L T_m)_j` on every interior row `1<=j<=m-4`, with the same
  identity at the seed after exact cancellation of the ideal endpoint atom.
  The geometric comparator has the analogous interior preimage
  `tilde h=-4h/(1-q)`. Hence an interior preimage comparison plus the three
  direct frontier rows and seed is another sufficient route to `d>=h`.
  The preimage comparison is not claimed necessary, and the fixed-prefix
  `q->0` limit is not substituted for the joint family `mq=1/16`. The local
  half-ratios are also exactly equivalent to
  `d_(m-1)+d_m/4>=0`, `d_(m-2)-d_m/8>=0`, and
  `d_j-d_(j+2)/4>=0`. On `j<=m-6`, the last cone has an exact folded-source
  ledger consisting of a source-free base, derivative packets
  `epsilon_n(1,2,-3)/4`, and point masses `mu_n=-q nu_n`. The sharp scalar
  window `2/5<nu_n<43/75` is proved. The mass folded-kernel estimate is also
  proved by an exact binomial smoothing maximum principle, finite dyadic
  lobe certificate, and entropy tail. The base/derivative estimates and five
  direct frontier rows remain OPEN. The original derivative target with
  constant `1/16` is rigorously false: an exact zero/first-moment calculation
  gives a fixed-distance limit below `-1/16` at distance six. The weaker
  sufficient replacement `-q/8` remains open.
- **Conditional:** If the actual entry position/velocity profiles satisfy the
  two displayed absolute bounds on a band of even modes and projection plus
  envelope subtraction remain inactive through the stated horizon, then every
  sufficiently large member requires at least
  `(1/8) q^-1 log(1/q)` terminal steps. The profile bounds rigorously imply
  the former combined `1/64` quadrature target.
- **Measured:** For `m=128,256,512,1024,2048`, the actual floating trajectory
  has entry weighted residual mass between `0.972971 q^2` and
  `0.972986 q^2`, entry range about `1.49939 q^(5/2)`, modal defects below
  `0.009` on the screened
  `sqrt(m/log m)` band, positive projection/envelope margins, and first range
  crossing `q*k=3.1235,3.8711,4.3666,4.7131,5.0172`. For `m=128,256`, those
  crossings are not literal certificates because all residuals are still too
  negative; the actual certificate occurs later. The screen reports both.
  On the wider diagnostic band, the maximum scaled position-profile errors
  decrease from `0.000880` to `0.000317`, the maximum scaled
  `V+G/5` errors remain below `0.195`, and `D_2/G_2` ranges from `-0.008138`
  to `-0.008022`. The packet remainder `c/q^3` is coordinatewise between
  about `-1.052` and `-0.168`, while the signed velocity source has extrema
  near `+/-3.64 q^3`. The directed cancellation reduces the measured positive
  weighted remainder mass from that moving-packet scale to about
  `0.258 q^3`--`0.260 q^3`. The corresponding pre-averaging positive mass
  `||d_+||_(1,D)` is about `0.43 q^3`, showing why Markov contractivity alone
  misses `21q^3/80`. The new endpoint-tail comparison is coordinatewise on
  the `m=64` floating screen (with equality at the defining endpoint), but
  this is evidence only. These are finite measurements and assert no limit.
- **Open:** Prove the two entry profile inequalities by uniform signed bounds
  for the homogeneous/base, constant-`U`, varying-`U`, `M_n`, and final
  endpoint pieces. For the static inequality, prove the displayed local
  endpoint half-ratios, or the sufficient interior temporal preimage cone
  together with the seed and three direct frontier rows (or otherwise prove
  `d>=h`). Equivalently, close the explicit base/derivative folded-kernel
  ledger for the two-step cone and its five frontier rows; then prove its early
  `J_kL` convolution counterpart and the projection/unclipped-envelope
  invariant in exact arithmetic.
- **Refuted:** A range crossing is not always a certificate when
  the residual maximum is negative. Characteristic roots or the measured
  table alone do not prove a logarithmic block. No frontier/seed surrogate
  replaces the moving global correction. Domination by the undamped `q=0`
  Pascal arithmetic average is also false: at `(n,j)=(5,2)`,
  `X_5(2)<(X_4(2)+X_4(1))/2` for every `0<q<=1/80`, with scaled limiting
  defect `-27/160`. This does not refute the finite-`q` comparator damped by
  `(1-q)/2`, which remains open. No general accelerated-local lower bound is
  claimed.

## Central blocker

1. **Entry profile lemma:** For
   `H_m=floor(sqrt(m/(64 log(16m))))`, prove
   `m*|C_(2s)-G_(2s)|/alpha <= 1/256` and
   `m*|V_(2s)+G_(2s)/5|/alpha <= 1/4` for all `1<=s<=H_m`.
   The exact velocity identity then gives the previous combined `1/64`
   quadrature inequality. The source identity is proved; the remaining
   concrete subproblem is a uniform signed Green-kernel estimate for its
   five-piece decomposition.
2. **Conditional-regime lemma:** Through
   `K_m=floor((1/8)q^-1 log(1/q))`, prove every raw proximal point is positive
   and every safe subtraction is strictly unclipped. The positive-residual
   part is now reduced to proving a uniform static bound on
   `||(w-w_dir)_+||_(1,D)/q^3`. The signed-mass and endpoint-tail ledger is
   proved, so the static bound now needs only the explicit local half-ratios
   for `d-h`, or the exact sufficient interior temporal-preimage comparison
   plus the four direct boundary checks. The sharper source-ledger route
   has closed the mass kernel, disproved the original `-q/16` derivative
   constant, and isolates the base kernel, a replacement `-q/8` derivative
   bound, and five direct frontier rows. A
   separate early/late position lower bound must exploit the
   exact first-step margin, which is only order `q^2`.

Each lemma is independently falsifiable by `verify.py`; changing the
constants is permitted only with a corresponding proof.

## Dependencies and reusable outputs

- **Formal registry dependencies:** `volume_gated_acceleration`.
- **Context/provenance:** The Round-013 terminal candidate motivated the
  direction; historical finite traces are not proof imports.
- **Reusable outputs:** Exact modal formulas, explicit optimum transports,
  the fixed-face directional factorization, the changing-face source entries,
  factored transform, and scalar `C/V` target reduction for the proved
  `m>=64` proper-prefix chronology, the
  exact `K/J` remainder decomposition, the ideal folded-shift sign lemma, the
  reflected prefix ideal/correction split, its exact residual-only recurrence,
  the positive correction-difference Green kernel and constant-source
  generating-series cancellation, and the all-prefix leading correction
  generating function with sharp shared-coordinate `1/80` margin, the
  finite-`q` stopped-kernel perturbation preserving `179/14400` from prefix
  six onward, the directed two-wave ideal packet, the exact entry-correction
  sign, and the no-loss folded `J_k` alias bound,
  weighted Popoviciu bridge from centered energy to residual range, and a
  deterministic screen that retains the literal global correction and
  transported-center semantics.

## Resume here

- **Exact pointer:** `main.tex`, Lemmas `lem:terminal-modal-packet` and
  `lem:terminal-modal-regime` are the two missing statements; Theorem
  `thm:terminal-modal-conditional-log` is ready to consume them.
- **Next action:** Split the explicit changing-face transform into the homogeneous
  packet/base discrepancy, the constant-`U` response, the total-variation
  correction `U_n-U_{n-1}`, the `M_n=O(q^4)` trace, and the single final
  endpoint term; bound their signed Green-kernel sums strongly
  enough to prove the displayed `C` and `V` profiles. Separately,
  prove `eq:terminal-modal-static-base-kernel-target`, replace the disproved
  `eq:terminal-modal-static-derivative-kernel-target` by the sufficient
  `-q/8` bound, and prove the five direct frontier
  rows (equivalently, prove `eq:terminal-modal-static-local-half-ratios`), or the exact sufficient
  temporal-preimage and boundary comparison, which implies the
  explicit local-average inequality
  `eq:terminal-modal-static-finite-target`; use the displayed binomial-window
  kernel for the early signed convolution, and combine these bounds with an
  early/late lower bound for the literal position candidate.
- **Stop/go test:** Promote the logarithmic block only after both missing
  lemmas are proved uniformly in `m`; a larger floating screen is evidence but
  never a substitute.

## Verification

- **Deterministic screen:** `python3 verify.py 128 256 512 1024 2048`
  passed. Before the floating screen, it now uses exact
  `Fraction` arithmetic at `m=8,12` to check all chronology-reduction
  constants and identities, finite strict `D_n>0`, raw positivity,
  post-residual sign, and exact gate behavior. It also uses exact arithmetic
  at `m=8`, prefixes `n=4,6,7,8`, to check source support, every displayed
  entry (including the final degree change), and the formal transformed
  recurrence along the exact replay. A separate exact
  correction preflight checks the residual-only recurrence and signed source
  at `m=12`, the positive Green identity through `k=12`, and the leading
  correction formulas through prefix 256; the latter audit the all-prefix
  shared-coordinate theorem and recover its exact minimum `1/80`. A fourth
  exact preflight checks the early-source mass identity, analytic small-prefix
  ledger, stopped derivative prefixes through length 128, point-source fold,
  and final `179/14400` arithmetic. A fifth exact preflight checks the
  half-endpoint cycle split, directed evolution, folded `J_k` alias bound,
  the exact `J_kL` binomial window, entry-correction sign, and `u=Ld`
  deconvolution at `m=8,12`. A sixth exact preflight checks the rational
  `3/50` signed-mass ledger, the `57/200` endpoint ledger, the finite
  alternating-tail stencil, the exact signed-mass formula, and the temporal
  correction/smoothing identity, two-step equivalence, exact
  `2/5<nu_n<43/75` mass window, signed smoothing base, and dyadic
  one-dimensional lobe certificate; it labels the base/derivative
  folded-kernel ledger, uniform local half-ratios, and temporal preimage
  comparison open.
  The floating screen
  reported first range crossings
  `q*k=3.123535156,3.871093750,4.366577148,4.713073730,5.017150879`
  and literal certificate times
  `q*k=3.733886719,3.985839844,4.366577148,4.713073730,5.017150879`.
  It also checks the two entry profiles and the exact combined
  entry-quadrature defect against their stated constants on `H_m`, labeling
  the checks vacuous when `H_m=0`; it verifies the two formulas for `D_h`
  agree, and keeps wider-band modal/profile statistics separate.
- **Build:** A clean `latexmk` rebuild produced a 32-page PDF with no
  LaTeX, package, overfull/underfull, or undefined-reference warning.
- **Audits/tests:** `make note-audit`, `make note-targets`,
  `make agent-audit`, `git diff --check`, focused Ruff lint/format checks, and
  the 210-test suite passed.  The full repository `make lint` remains blocked
  by 1,345 pre-existing findings under
  `manuscript/claude-overnight-2026-08-24/`; the new verifier is Ruff-clean.
- **Known numerical boundary:** The screen is float64. The sibling note's
  rational checks for `m=2,4,8` cover only finite `1/(2q)` terminal prefixes.
  The focused post-change command `python3 verify.py 64` passed and measured
  static positive mass `0.255090q^3` with nonendpoint tail-dominance margin
  `0.00029775q^3`; this finite measurement is not used in the proof.
