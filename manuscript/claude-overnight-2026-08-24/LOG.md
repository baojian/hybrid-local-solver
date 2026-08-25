# Campaign log

- 2026-08-24 12:40 UTC (20:40 CST): campaign started; infra built (lib/model.py,
  zoo.py, meter.py), sanity-checked against manuscript theorems (APPR star
  interval reproduced). Insurance staging of note sources completed while the
  device was online. Driver wakeup scheduled 15:09 UTC; morning consolidation
  scheduled 22:45 UTC (06:45 CST).
- 2026-08-24 ~13:55 UTC: Iteration 1 complete (8/8 agents returned; ~1.36M
  agent tokens). Scoreboard v1 written. Headlines: W2 refutes product-scale
  information LB (info is Θ~(1/ε)); W3 carry-mode randomized APCG holds √α
  exponent with growing support; W4 EES hits product scale on spiders; W6
  incremental LDL is α-free output-linear on non-branching families; W7
  validates reconstruction 5/5 and finds windowed slopes ≤0.145 (Route B
  likely true); W8 finds the practical prize of the classic wedge is <10×
  and relocates the frontier to grids/fill.
- Next: Iteration 2 (6 agents: I2-A..I2-F) launching immediately in the same
  turn; driver wakeup at 15:09 UTC will run Iteration 3.
- 2026-08-24 (I2-C, resumed after credit outage): K_n window/absorption theorem
  drafted. Resumed from w7_windowed/knproof.py (C1-C8) + engine.py. Built an
  exact modal engine for K_n (kn_modal.py, bit-exact vs engine.py incl. both
  published gamma constants, 50x faster) and extended the lemma chain to
  C1-C17: 140 instances (n in {2,4,8,16,32} x q in {1/10,1/100,1/400} x 5 seeds
  x 2 rho), 17/17 predicates pass, 0 failures. K_n turns out to ABSORB
  (corrections stop, t_abs <= 12, B = J_inf <= 0.369 < log 2), so Route-B net
  packing holds on K_n with c = 1. One Open link: V-contraction at genuinely
  partial correction stages (1 occurrence in the whole grid; certified bound
  passes with only 2.1% margin). Findings: findings/i2c_windowed_proof.md;
  P_24 audit spec pinned to exact rho = 65/4096.

- 2026-08-24 (I2-B, resumed after credit outage): dynamic-order incremental
  LDL^T on trees. Inherited dyn_ldl.py (SEG-LDL: seed-rooted implicit LDL^T on
  path-carved 2x2 continued-fraction segment trees) was CORRECT — test_dyn.py
  had never been run and passes (1e-11 vs dense prefix solves). Built the COMB
  adversary and confirmed BOTH iteration-1 predictions: INC-LDL nnz(L) ~
  |S|^1.556 (W ~ vol^1.87), TREE-INC up-path ~ alpha^-0.45 (W ~ vol^1.30).
  SEG-LDL is ALSO defeated (chain length -> 32; its carving rule is admission-
  order dependent and the comb's degree-2 teeth capture the backbone's path).
  Fix built and validated: HSEG-LDL (dyn_ldl2.py) maintains a 2-approximate
  heavy-path decomposition online, subtree sizes carried as a third aggregate
  in the same segment tree, O(moved) splice on swap. Result: q = 0.92-1.11 on
  all five scaling series (comb included), W/(vol*log2^2 vol) in [1.59, 5.57]
  over 149 configs, alpha-free; 149/149 certificates pass. Honest gap: the
  re-carve amortization is Open (worst case O(|S|*depth*log^2); measured
  moved/|S| <= 0.44 and falling). Findings: findings/i2b_dynamic_ldl.md.

- 2026-08-24 (I2-E, resumed after credit outage): information UPPER bound on
  spiders. Inherited upper_algo.py had the right envelope but an O(log D)
  certificate and a k-sweep that missed the true maximum. Rewrote with the
  O(1)-per-probe certificate (three lemmas: W''=(ln lam)^2 W convexity for C4
  endpoints; monotonicity in m so only the shallowest open arm binds; doubling
  keeps open arms at <=2 depths). Derived the collapse: the whole certificate
  is the scalar condition y/(1-y^2) <= beta, y=lam^{m+1}, beta=k*eps/(2s), whence
  T*eps = t/(2 sinh t) with sup 1/2 -- so T <= (1+o(1))/eps, NO 1/sqrt(alpha),
  NO log. Corrected iteration 1's guessed allocation: k*=2s/(e eps) at depth
  1/(2s) is a local extremum (T*eps=1/e), the true worst is shallow-and-wide
  (k~1/(2eps), depth 1). Measured T*eps in [0.375,0.629] over 16 cells,
  slope(log T vs log 1/eps)=1.00+-0.05, alpha-free; minimax hill-climb found
  nothing above 0.5625; champions re-validated in exact Fractions.
  Tree extension built and validated (tree_envelope.py): monotone scalar-load
  continued fraction R_w=c/(d_w-c*sum R_x), two-evaluation bracketing, best-first
  frontier scan; 48/48 + 30/30 eps-VALID against independent Gaussian-elimination
  solves, max T*eps=0.4531 over 105 tree cells, and NO degree bound is needed.
  Obstruction on general graphs isolated: cycles (multi-port Schur complements
  are matrix-valued, so no single all-reflecting closure maximizes), not hubs.
  Info cannot exceed 1/eps by listing (sum_v u_v <= 1); ex-1/eps would need
  dark probing, Open, no family found. TWO-SIDED: spider information complexity
  is Theta(1/eps), matched to a factor 80, alpha-free => the product scale
  1/(sqrt(alpha)*eps) is COMPUTATIONAL. Findings: findings/i2e_info_upper.md.
- 2026-08-24 ~15:4x UTC: I2-D complete (findings/i2d_separation_package.md,
  code w9_i2d/). Restarted from scratch after the credit outage; reused
  w1_monotone_lb/gpush.py. THE CORE FIND: a single potential Psi(r) =
  pr(r)_c/pi_c = (pi_c - p_c)/pi_c retires Lemmas 3/4/5 of W1 and closes G2.
  Exact, axiom-free: any invariant-preserving update has dPsi = -dp_c/pi_c, so
  Psi moves ONLY at seed-based ops, for EITHER sign of eta; and r >= 0 forces
  r_c <= Psi, giving the one-sided multiplicative step -dPsi <= kappa*Psi,
  kappa = 2 alpha/((1+alpha) pi_c) (= 4a/(1+a)^2 on the star). Hence
  N_c^+ >= ln((1-B)/(eps*vol))/(-ln(1-kappa)) for the SIGNED-eta class M+-,
  constant c = W*alpha*eps >= 0.0433 vs iteration 1's proved 3/256 = 0.0117
  (3.7x stronger) and the member frontier 0.0867 (exactly 2x). 600 member runs
  + pump adversary: 0 failures, tightest members at N_c^+/LB = 1.015. Works on
  ANY graph (Prop 2.6), so G3's leaf-flow ledger is retired too. G2 CLOSED:
  the anti-acceleration axiom is r >= 0, NOT the sign of the step.
  G1 reframed and SHARP: out = p + M r with M one-hop nonneg is governed by
  one scalar, its column mass B; Gale/Hall gives the exact escape condition
  (per-cut, S=V is the only alpha-carrying cut); threshold B = 1 - eps*vol is
  attained at W=0 and matched by M=B*I at W=m (LP bisection agrees to 4 dp).
  NEGATIVE RESULT, reported as such: the planned "second instance kills B=1"
  is FALSE on every radius-1 instance (two-seed shared-M LP feasible at B=1,
  W=1; the leaf-seeded star is escapable in m+1 work by a tuned partial push,
  verified 2e-17). B=1 costs only Omega(vol) transport on larger radius.
  T3 UPPER HALF proved: x_j = (j+1) lam^j verified to 1e-13, stopping test
  reduces to x_j <= eps*m, giving W_SOR <= m*ceil((1/t) ln(2/(t eps m)))
  = O(m(log(1/eps)+log(1/alpha))/sqrt(alpha)); measured 0.53-0.57 of the
  bound on 18 cells. T4 separation on ONE instance with both classes precise:
  M+- = Theta(1/(alpha eps)) vs R+- = O~(1/(sqrt(alpha) eps)), ratio measured
  0.34 -> 5.84 as alpha goes 1/4 -> 2^-12, tracking 1/(sqrt(a) log(1/a)).
  Open: companion class LB for signed-RESIDUAL methods (would make it
  class-vs-class); Phi=1 in the general-graph version (measured, not proved).
- 2026-08-24 ~15:45 UTC (I2-F, fresh start after the credit outage): grid
  frontier resolved. Parameter map (Proved-draft): the classic 1/(sqrt(a)eps)
  target is vacuously loose on 2D grids (22-91491x above output, diverging like
  sqrt(a)/(eps log^2)) because grid output is Theta(log^2(1/eps)/alpha) --
  polylog in 1/eps -- while the target is linear. Right target restated as
  output-linear with alpha-free constants. LOCAL GEOMETRIC MULTIGRID achieves it
  (Measured): W/vol(S) alpha-exponent 0.20 certified / -0.06 oracle vs 0.85 push,
  0.75 Chebyshev, 0.81 push->Cheb, 0.69 nested-dissection EES; V-cycle rate
  0.024-0.066 alpha-free; 17/17 cells certified and verified. Push, polynomial
  and elimination mechanisms all pay one pass per unit radius (alpha^-1/2 or
  alpha^-1); multilevel response pays log(1/eps). Certified MG's residual
  alpha-dependence traced to the restricted-solve certificate being loose by
  exactly 1/(8 alpha) on a lattice -- removable. Code i2f_grid/, findings
  findings/i2f_grid.md. Next: local ALGEBRAIC multigrid on the general zoo.
- 2026-08-24 ~16:10 UTC (I3-B): boundary-scan cost SOLVED; the shell-volume
  question I2-A left open is CLOSED (theorem + matching construction).
  (1) The Theta(vol(dS))-per-check gate is an artifact of PULLING grad_j
  through j's adjacency. Pushing two accumulators (P_j = sum Q_ji p_i,
  M_j = sum Q_ji Mh_i) from the interior side makes -grad_j = b_j - P_j -
  phi*M_j EXACT in O(1); |dS| <= vol(S) always, and maintenance costs
  |N(i)\S| <= d_i per interior step -- inside the d_i scan the interior
  already pays. (2) KINETIC gate: between touches G_j is affine in phi with
  phi monotone, so the crossing time is closed-form -> max-heap, zero false
  wakeups, wakeups == output. Ring (m=60, hub_deg 48/192/384, mult 8):
  eager_pull 1.03e5..2.47e6 tracking (#sweeps)*vol(dS*), kinetic 3.2e3..9.3e3
  FLAT in hub_deg (266x at D=384), non-piggyback cost 1392 = 7.7*vol(S*) =
  0.06*vol(dS*), IDENTICAL at poll=n and poll=1 (1392 vs 1384) -- instantaneous
  (frontier-1) reporting is free. At poll=1 pull/kin = 1.9e3..1.8e4. Benign
  regression: worst cell btree 6.1x eager_pull but 1.9% of interior; kinetic
  cheaper on spider/grid/path-2^-12; at poll=1 kinetic wins 13x-623x
  everywhere. deg_bucket (certified degree schedule) is a NEGATIVE result:
  5-100x worse, min-over-bucket margin collapses. 0 misses / 0 false reports
  in 50 runs, exhaustive dense check every poll.
  (3) LEAK IDENTITY (Proved, machine-precision on 18 instances):
  (1-a)/2 * T = a*[s(S*) - ||pi||_1 - rho*vol(S*)], T = total leak flow.
  SHELL LEMMA (Proved-draft): tau*rho*vol(shell_tau) + rho*vol(S*) <=
  s(S* u shell) - ||pi||_1 <= 1, hence vol(shell_tau)/vol(S*) <=
  (1/tau)[1/(rho*vol(S*)) - 1] -- ALPHA-FREE. So the answer to I2-A section 7
  is NO: the shell cannot grow like alpha^-1; it grows only through
  rho*vol(S*) -> 0. Matching HUB LADDER construction (exact decoupling: a hub
  with x=0 affects the core only through d_t=3, so D_t is a free per-position
  parameter) measures ratio 21.5-22.0 flat over alpha = 2^-4..2^-16 and
  8.1/21.9/76.3 for rho = 1/50,1/200,1/800 -- within 1-2% of the bound.
  Code w10_i3b/, findings findings/i3b_boundary_gate.md. Next: retire the pull
  gate campaign-wide; combine the shell lemma with a momentum-overshoot bound
  for an unconditional locality theorem in the rho*vol(S*) = Omega(1) regime.
