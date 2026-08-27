# Direction status: path_terminal_modal_block

Last reviewed: 2026-08-28
State: synthesis
Agent family: codex
Role: direction
Branch: `agent/codex/path-terminal-semantic-stop`
Base commit: `f4bf4299c52ec171bf49f6f7040ec674004c8fdd`

## Exact question and contract

- **Question:** Does the terminal full face of the named endpoint-path
  transported-center execution require
  `Omega(q^-1 log(1/q))` consecutive fixed-face steps?
- **Model:** The endpoint path `P_m`, endpoint seed, `q=1/(16m)`,
  `alpha=q^2`, `rho=tau=q/5`, ambient degrees, exact-real zero start,
  complete all-violations admission, transported estimate center, and the
  literal projected/safe-envelope recurrence.
- **Accuracy namespace:** The note distinguishes its one-sided normalized KKT
  certificate from degree-normalized RPPR semantic error.  Neither is the
  repository-wide stopping decision.
- **Access and charged work:** Adjacency-list access; one restricted sweep is
  charged by active volume.  The named terminal phase scans the full path.
- **Intended result:** Prove an asymptotic logarithmic terminal block for the
  named literal recurrence and record, without overclaim, its charged
  certification-work consequence.
- **Result:** For every sufficiently large `m`, the named execution has no
  terminal certificate during its first
  `K_m=floor((8q)^-1 log(1/q))` full-face steps.
- **Threshold:** Existence is proved; no explicit cutoff is asserted.  The
  proper-prefix and interior static theorems are uniform from `m=64`, while
  the five frontier signs use positive joint first-order limits.
- **Scope exclusions:** No claim is made for other algorithms, alternate face
  schedules, nonlocal response primitives, exact-spectrum polynomials, or an
  eleven-resource class.  Exact CG can terminate on the `(m+1)`-dimensional
  path in at most `m+1` matvecs, so the logarithmic block is not a generic
  Krylov lower bound.

## Claim ledger

- **Source:** The RPPR bridge, safe-envelope rule, and transported-center
  recurrence are imported from `volume_gated_acceleration` with their stated
  scope.
- **Proved here:** The five-step chain below, including the full static cone,
  the nonlinear early/late regime, and the asymptotic terminal block.
- **Conditional:** Intermediate tail, late-position, and modal-band theorems
  retain explicit hypotheses, all discharged by the final synthesis for
  sufficiently large `m`.
- **Measured:** Floating screens through `m=2048` check signs and margins but
  are not proof inputs.
- **Refuted:** The stronger separate early `q^3/16` bound through `17/200`, a
  global folded quarter-mass shortcut, and coordinate-error monotonicity.
- **Open:** An explicit common frontier cutoff and the unnecessary stronger
  separate `L_k u<=13q^3/200` inequality.

1. Exact prefix optima, transports, and the correction recurrence reduce
   chronology to a shared sign.  A finite-`q` stopped ledger proves the sign
   for every prefix when `m>=64`, including the degree-one final endpoint.
   Thus projection stays inactive, safe correction is zero, and exactly the
   next singleton is admitted.
2. Exact changing-face sources and their Laurent transforms prove the entry
   position and velocity profiles on the required modal band.  The ideal
   packet splits into two directed nonpositive waves and the actual entry
   correction obeys `c(j)<-13q^3/100` for every row.
3. The static remainder satisfies `u=Ld`.  The folded derivative/base/mass
   theorem proves the two-step cone on `0<=j<=m-6` for every `m>=64`.
   Exact joint first-order formulas give positive limits on the five frontier
   rows.  Hence, for all sufficiently large `m`, the local half-ratios hold,
   `d>=h`, and `||u_+||_(1,D)<21q^3/80`.
4. The finite stopped ledger proves scaled half-retention, raw positivity,
   projection inactivity, and zero safe subtraction for `qk<3/50`, with
   exact margin `1807/115200`.  The static bound and the late position ledger
   prove strict raw positivity and envelope dominance for `qk>=3/50`, with
   rational transition slack `1667/625000`.  The first late integer follows
   an already-proved early integer, so there is no induction gap.
5. The proved modal-band energy and range bridge exclude the one-sided
   certificate through `K_m`, yielding the unconditional asymptotic terminal
   block for the named recurrence.
6. Positivity of the full-face propagators, the entry lower bounds, and the
   proved unclipped safe envelope give the two-sided semantic estimate
   `||p_k-p*||_inf<q/5` once `qk>=4`.  Thus a theorem-timed semantic return
   uses `O(q^-2)` charged work even though the prescribed certificate retains
   its logarithmic delay.

## Charged implementation ledger

The named implementation literally charges one full-face scan of
`vol(P_m)=2m=1/(8q)` per terminal step.  Consequently

`W_terminal >= (1/(8q))*floor((1/(8q))*log(1/q))`

`>= (1/(64q^2))*log(1/q)-1/(8q)`.

At `eps_ppr=rho+tau=2q/5`, this is
`Omega(eps_ppr^-2 log(1/eps_ppr))`.  Relative to the log-free scale
`1/(sqrt(alpha)*eps_ppr)=5/(2q^2)`, the prescribed certification runtime has
a logarithmic overhead.  This is not a semantic-error lower bound: the
iterate is proved accurate by `ceil(4/q)` full-face steps.  It does not
refute a soft-O work target and
does not extend beyond the named sweep-linked implementation resources.

## Open or refuted stronger statements

- **Optional open:** An explicit common cutoff for the five frontier signs,
  in particular a theorem uniform from `m=64`.
- **Optional open:** The stronger separate convolution
  `L_k u<=13q^3/200`.  The correlated early theorem makes it unnecessary.
- **Refuted:** The separate `q^3/16` estimate through `17/200`.
- **Refuted:** A global quarter-mass folded-kernel shortcut; the exact
  normalized coefficient is `3/8` at `k=2`, target zero, source one.
- **Refuted:** Coordinatewise monotonicity of the error under face growth.

None of these optional statements is needed for the asymptotic terminal
block.

## Central blocker

There is no remaining blocker for the core asymptotic theorem.  The only
unresolved quantitative refinement is an explicit common cutoff for the five
frontier limits; it is not needed for a sufficiently-large-`m` result.

## Dependencies and reusable outputs

- **Formal registry dependencies:** `volume_gated_acceleration`.
- **Reusable outputs:** Exact prefix chronology; changing-face source
  transforms; position and velocity entry profiles; the directed ideal-packet
  split; static `u=Ld` deconvolution; the interior folded-source cone; five
  exact frontier first-order limits; the correlated early stopped ledger; the
  late position/envelope bridge; and the exact-CG full-face escape comparison.

## Verification

- `verify.py` checks chronology, changing-face source identities, entry
  profiles, the directed packet, static deconvolution, and the literal
  full-face screen.
- `verify.py` includes the exact folded derivative completion and interior
  cone checks.
- `verify_static_frontier.py` checks the exact five-row reduction, joint
  first-order limits, and positive polynomial certificates.
- `verify_stopped_baseline.py` and `verify_finite_stopped_ledger.py` check the
  stopped leading comparison, folded Abel-ten ledger, endpoint atoms, and
  early margin.
- `verify_regime_reduction.py` checks the late rational constants.
- `verify_asymptotic_closure.py` checks the implication-chain arithmetic and
  the integer early/late handoff without claiming an explicit frontier
  cutoff.
- `verify_semantic_stop.py` checks the exact `s=4` rational constants and
  reports the semantic/certificate crossing separation as labeled float64
  evidence.
- Final build, repository note/target/agent audits, focused Ruff/format,
  control-byte/conflict-marker scans, and diff checks are required before
  promotion.

## Resume here

Promote the asymptotic synthesis together with its semantic/certificate
separation.  Further work may seek an explicit frontier cutoff or sharpen the
proved semantic constant `4` toward the measured value near `3.43`.
