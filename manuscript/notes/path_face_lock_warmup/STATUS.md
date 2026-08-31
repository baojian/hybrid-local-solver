# Direction status: path_face_lock_warmup

Last reviewed: 2026-08-29
State: proved-open
Agent family: codex
Role: direction

## Exact question and contract

- **Question:** Can the safe proximal warmup after a face lock be bounded
  independently of graph size, or at worst logarithmically, before momentum
  becomes componentwise safe?
- **Model:** Source-aligned RPPR on endpoint paths and symmetric spiders.
- **Accuracy namespace:** Note-scoped componentwise KKT and face-retraction
  certificates; no repository-wide stopping-rule identification.
- **Access and charged work:** Adjacency-list sweeps are charged by scanned
  degree; exact inverse, state-write, and repeated-resolvent costs must be
  reported separately.
- **Intended result:** A proved warmup theorem, a correct weaker structural
  condition, or an explicit counterexample to graph-size-independent warmup.

## Claim ledger

- **Source:** The Fable face-lock construction and project path profiles
  motivate the question. Fable's `Proved-draft` labels are not imported.
- **Proved here:** The exact fixed-face residual recurrence is
  `y_(t+1)=M((1+beta)y_t-beta*y_(t-1))`, with
  `M=kappa(Q_S+kappa I)^(-1)`. For every graph face and `alpha<=1/5`, one
  pure-prox solve certifies the immediately following first momentum trigger
  by the entrywise bound `M>=I/2`. A reset after any fixed safe momentum burst
  has Perron contraction only `1-Theta_L(q^2)` and is not accelerated. Exact
  cone witnesses refute one, two, and three warmups on full endpoint paths and
  four on a full 16-arm star. More strongly, for every fixed integer `J>=1`,
  the leaf-seeded unit-star family
  `q_B=1/[2(B+1)]`, `rho_B=1/(4B)` reaches the full face at state four and has
  a negative seeded-leaf second momentum trigger for every sufficiently large
  `B`. Thus there is no universal constant warmup for this reachable policy.
  Conversely, on any supplied full `B`-star face, the cone-uniform choice
  `J_B=max{3,1+ceil(log_(3/2)(8(B-1)))}` makes every later trigger kernel
  entrywise nonnegative. The same reachable family has the quantitative lower
  bound `J >= log_(3/2)(B)-O(1)` for this policy: below that scale the seeded
  second trigger is at most `-2 alpha_B/B`. Hence the exact repeated-solve
  policy has matching `Theta(log B)` warmup scale. A stronger upper condition
  gives every kernel entry margin `a_k/(4B)` on finite horizons. On every
  strict connected proper face, the global-beta Perron trigger is a damped
  oscillation, so no finite warmup makes the permanent tail cone-safe. A
  face-tuned beta repairs this: a spectral-ratio/Perron-spread warmup makes
  every exact trigger-kernel entry strictly positive. A face-tuned
  Perron-split window works without a spectral gap: it records the Perron and
  orthogonal components of every actual common-cap correction and halves its
  two-scale root whenever an explicit `ceil(2/q_face)` event gate passes. A
  reachable proper-face `P3` trajectory shows that the common cap becomes
  nonuniform in Perron coordinates, so the full-face master theorem cannot be
  imported by a ground-state transform alone. Every rejected face-tuned
  window spends a fraction
  `Theta((1/q_face+1/phi_min)^(-1))` of the Perron mean, which is exact but
  does not close an accelerated packing. A finite error-bar version of the
  gate retains half-contraction under an explicit inner residual budget. A
  conditional one-admission final-full-star theorem gives explicit finite-inner residual
  tolerances for any fixed momentum horizon and an observable primal guard.
  Alternatively, monotone Collatz brackets from pure-prox probes plus an
  observable error-bar gate give a conditional accepted fixed-face window
  with accelerated root rate, without computing lower eigendata.  Birkhoff
  contraction and a proof-only spectral estimate now bound the bracket
  hitting time; full paths show this bound can be
  `Omega(n^2 log n)` probes and therefore cannot be graph-uniform.  A
  Schur-complement admission lemma pays squared same-point boundary residuals
  from telescoping restricted-optimum gains whenever replay starts at a
  certified coordinatewise lower checkpoint. Combining this with volume
  doubling gives the conditional work bound
  `W_adm <= 2*C_res*(V+Delta_tot/eta)` under a volume-normalized admission
  margin; paying discarded `Theta(vol(A)/q)` windows needs the correspondingly
  stronger `/q` margin.
- **Conditional:** The proper-face Perron-split theorem gives accelerated
  contraction for a fixed face whenever its observable two-charge gate passes;
  rejected windows have a Perron-mean payment, but that payment can still
  permit `Theta(1/q_face^2)` stages. The finite gate is rigorous under supplied
  Perron/error certificates; their construction remains charged.
- **Measured:** The finite exact path screens record horizon passes only; they
  are not all-time theorems.
- **Refuted:** Constant post-lock warmup for the specified reachable star
  policy; cone-uniform one-to-three warmups on the registered paths; four on
  full stars; fixed-burst/reset acceleration of the Perron mode; and direct
  preservation of the actual common cap under a proper-face Perron transform.
- **Open:** A graph-size-independent statement for the realized endpoint-path
  chronology; a finite-inner restart/window implementation of face tuning on
  unequal arms and changing proper faces; and charged spectral certificates.

## Central blocker

For paths, the actual residual profile after prefix admission is not yet
characterized. For spiders, the exact full-star scale is logarithmic and its
finite-horizon entrywise margin is known, but that margin decays in time and
strict proper faces oscillate under global momentum. The resolvent cost is not
local merely because the face is exposed: the literal full-star policy costs
`Theta(B log B)`. Face tuning gives permanent exact safety, but its spectral
ratio and Perron-spread certificate may be costly and nongraph-uniform. A
finite-inner changing-face theorem must retain those costs. The Perron-split
gate removes the need for a permanent tail on an accepted fixed-face window,
but failed-window packing and Perron-pair construction remain charged. Collatz probes
remove the need for full eigendata after their bracket is tight, but the path
STOP proves their hitting time is not graph-uniform, and admission replay
count is amortized only conditionally. Without a volume-normalized boundary
margin, arbitrarily many tiny-gain admissions can create `Theta(V^2)` replay
work (or `Theta(V^2/q)` including discarded windows); without an
alignment/payment certificate the observable gate can also keep restarting.

## Dependencies and reusable outputs

- Formal registry dependencies: `aesp_cd_l1_rppr`, `path_terminal_modal_block`.
- Source/shared prerequisites: source-aligned RPPR definition.
- Reusable outputs: exact trigger-kernel recurrence; rational path/star cone
  witnesses; exact spider junction and volume formulas; a three-class exact
  reachable-star LCP verifier; matching logarithmic bounds for the exact star
  policy; a strict finite-horizon kernel margin; and a proper-face oscillation
  obstruction with a face-tuned exact repair; and a Collatz-bracketed gated
  fixed-face accelerated window.
- Supplies to: safeguarded acceleration and spider-generalization directions.

## Resume here

- Exact file/section/lemma: `main.tex`, especially
  `sec:reachable-star-family`, `thm:reachable-star-logarithmic-lower`,
  `cor:star-logarithmic-kernel-margin`, and
  `prop:star-finite-inner-window`, `prop:proper-face-global-momentum-stop`,
  `prop:proper-face-perron-split-window`,
  `cor:proper-face-perron-accepted-paid`,
  `cor:proper-face-finite-perron-gate`,
  `prop:proper-face-componentwise-perron`,
  `prop:p3-proper-perron-cap-stop`, and
  `thm:face-tuned-permanent-safety`, `thm:collatz-gated-window`, and
  `prop:collatz-projective-hitting`, `lem:boundary-admission-gain`, and
  `cor:conditional-admission-work`.
- Next concrete action: combine safe signed-scratch face solves with batched
  same-point admissions, and seek a graph-local certificate for the Perron
  data or a decomposition when the spectral cluster is wide.
- Stop/go test: go if a finite-horizon relative tolerance and charged restart
  retain acceleration; stop if repeated resolvents or state materialism exceed
  the target local budget.

## Verification

- `verify_warmup.py` reproduces the exact registered path and cone-star
  witnesses.
- `verify_reachable_star.py` uses exact `Fraction` arithmetic and a three-class
  LCP mask enumeration. Its default `B=50,J=6` case reaches full state four,
  has a nonnegative first momentum trigger, and reproduces the exact negative
  seeded-leaf fraction at stage 11. It also proves the residual-margin
  inequalities by nonnegative coefficients after substituting `B=b+2`, and
  checks a nonvacuous `B=10000,J=6` logarithmic-lower instance.
- The reachable-family derivation and default exact fraction were independently
  rederived from the three-class recurrence and spectral polynomial.
- The registered `path_face_lock_warmup.proper_perron_cap_stop` audit replays
  the reachable settled `P3` face, checks its quadratic-surds Perron pair, and
  certifies both the transformed-cap mismatch and the negative global Perron
  trigger.
- Known gaps: finite path horizon passes are not all-time; the strict kernel
  margin decays with the horizon; and all star bounds are exact, face-specific,
  and do not hide the repeated inverse cost.

## Repository handoff

- Provider-owned paths changed: none.
- Shared paths changed: none in this direction update.
- Assignment state: active under `windowed-spectral-lyapunov-7h`.
