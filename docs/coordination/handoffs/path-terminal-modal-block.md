# Handoff: path-terminal-modal-block

- Agent family: codex
- Role: direction
- Branch: `agent/codex/path-terminal-boundary-source`
- Base commit: `8e039042f4325be6b6640587cba753c8967ee28b`
- Assignment state: ready_for_review
- Write scope:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/path-terminal-modal-block.md`
  - `manuscript/notes/README.md`
  - `manuscript/notes/registry.toml`
  - `manuscript/notes/path_terminal_modal_block/`
- Permitted shared files:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/path-terminal-modal-block.md`
  - `manuscript/notes/README.md`
  - `manuscript/notes/registry.toml`

## Outcome

- Requested result: Continue the literal full-path terminal logarithmic-block
  analysis, prove every uniform inequality currently available, and preserve
  any remaining gap as exact, falsifiable lemmas rather than promoting
  floating evidence to a theorem.
- Implemented result: Added a standalone fifteen-page note deriving the exact
  degree-weighted path-cosine basis, damped modal roots and quadratures, safe
  global-correction/range semantics, the ideal binomial packet transform, a
  uniform phase-energy bound, and a conditional
  `Omega(q^-1 log(1/q))` theorem.  The note isolates three sufficient missing
  lemmas: proper-prefix projection/correction/admission chronology,
  low-even-mode entry position/velocity profiles, and a
  projection/unclipped-envelope invariant through the logarithmic horizon.
  A follow-up derives the exact identity `D_h=q*cot(phi_h)*V_h`, all proper-
  prefix and full-path restricted optima, the rank-one proper-prefix transport
  with `0<b_n-b_(n-1)<=q*artanh(q)`, the fixed-face directional factorization,
  and pointwise nonpositivity of the ideal packet evolution. A second
  follow-up proves, conditional on that open proper-prefix chronology, the
  exact changing-face defect at the seed and last three
  frontier rows, including the final ambient-degree-one endpoint. Even
  reflection removes the seed term, and the remaining source transform
  factors as `U_n(1-z)(1+3z)+M_n*z^2`, with exact uniform bounds
  `0<U_n<=3q^3/40` and `|M_n|<=3q^4/2`. It also reduces the open `C/V`
  profiles to two scalar signed-sum inequalities. The
  full-face `K/J` propagators are nonnegative with row sums `1` and `k`, so the
  source algebra and scalar profile reduction are therefore exact under the
  chronology hypothesis, not unconditional claims about the projected
  admission execution. A further conditional addendum exactly sums the
  constant-`U` response, derives its fixed-mode position/velocity limits and
  the early-base velocity limit, and reduces the final endpoint velocity to
  one position scalar. The regime-side obstruction is now the factor-`k` loss without signed/variation
  control of the velocity remainder. The profile constants rigorously imply
  the earlier combined `1/64` target. A
  deterministic screen reconstructs the literal admission and terminal
  recurrence and tests all three hypotheses at finite sizes.
- Deliberately unchanged: The dirty main worktree, the source
  `volume_gated_acceleration` note, its historical verifier, and all solver
  implementations.  This branch does not claim an unconditional terminal
  theorem, a class lower bound, or a lower bound for implicit-response or
  other accelerated local algorithms.

## Evidence

- Tests added or changed: Extended `verify.py`, which replays exact algorithmic
  semantics in deterministic float64 arithmetic, checks admission projection,
  correction, and gating, measures entry packet/quadrature defects, checks the
  full-face projection and envelope margins, and reports both the first raw
  range crossing and the first literal safe-envelope certificate. Before that
  screen it now performs an exact rational replay at `m=8` and verifies the
  boundary entries and formal Laurent-polynomial recurrence at representative
  proper and final prefixes. It also checks six total-variation cells,
  15 finite geometric-sum cells, and three fixed-mode limit cells for the
  constant-`U` response.
- Commands run: clean note build; `python3 verify.py 128 256 512 1024 2048`;
  `make note-audit`; `make note-targets`; `make agent-audit`; `make test`;
  focused Ruff lint and format checks; `git diff --check`; and `make lint`.
- Results: The note built to 18 pages with no LaTeX, package,
  overfull/underfull, or unresolved-reference warnings.  The deterministic
  screen passed all five sizes.  It checks the exact combined
  `(|C-G|+|D|)/|G| <= 1/64` condition on the literal `H_m` band and labels
  finite sizes with `H_m=0` as vacuous. It now also directly checks
  `m|C-G|/alpha<=1/256`, `m|V+G/5|/alpha<=1/4`, and the exact velocity
  identity; wider-band profile and `K/J` remainder values remain explicitly
  measured. The
  19-note registry, note targets, coordination audit, focused Ruff checks,
  diff check, and 210 tests passed.
  The test command emitted 15 temporary-directory cleanup warnings.  The full
  repository lint command remains red on 1,345 pre-existing findings under
  `manuscript/claude-overnight-2026-08-24/`; the newly added verifier has no
  Ruff findings.

## Review notes

- Provider-owned paths changed: New note directory
  `manuscript/notes/path_terminal_modal_block/` only.
- Shared paths changed: Note registry/README and this scoped coordination
  assignment/handoff.
- Semantic correction: At `m=128,256`, the measured values
  `q*k=3.123535156,3.871093750` are first raw-range crossings, not literal
  certificates.  Because the residual maximum is then negative, the literal
  certificates occur later at `q*k=3.733886719,3.985839844`.  For
  `m=512,1024,2048`, the two events coincide at the displayed precision.
- Promotion-audit correction: The low-mode packet asymptotic is
  `|G_(2s)| ~ exp(-1/16) alpha/m = 16 exp(-1/16) q^3`; the earlier omission
  of `exp(-1/16)` was a constant typo and did not affect the theorem's
  conservative amplitude bounds.  The note also records why zero-padding the
  newly admitted endpoint rules out an instantaneous certificate at entry.
- Open decisions or follow-up: First prove the proper-prefix raw-positivity,
  zero-safe-correction, and next-row-violation chronology, or retain it as an
  explicit hypothesis. Conditional on it, decompose the frontier transform
  into the homogeneous packet/base discrepancy, the now-exact constant-`U` response,
  the small total variation of `U_n`, the `M_n=O(q^4)` trace, and the single
  final endpoint term, then prove the two
  entry profile bounds uniformly in `m` by uniformizing the fixed-mode limits
  and controlling the remaining signed Green sums; also prove projection inactivity plus
  unclipped global correction through
  `floor((1/8)q^-1 log(1/q))`.  Until all three statements hold in exact arithmetic,
  retain evidence `proved-open` and every asymptotic terminal claim as
  conditional.
