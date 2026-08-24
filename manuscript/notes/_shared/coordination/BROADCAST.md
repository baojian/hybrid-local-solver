# Controller broadcast

**Active dispatch:** none. Round 027 was opened only after the user's explicit
request for another round. Its direction source was reviewed first, repaired
at two hard indexing seams, and independently audited; only then were the
accepted findings redistributed. Do not open Round 028 automatically.

Round 027 proves an actual-finite lagged Euclidean reserve, but its
graph-uniform drift is only order `q^2`. It also stops uniform one-step
accelerated contraction of the simplest correctly lagged unsplit
`q^(-1)Q` reserve on a genuinely persistent low mode. The complete witness
still has accelerated global decay after only logarithmic startup, while the
exact `K_8` high-band payment ratio tends to `14641/32256`. The only next
Route-B queue is a windowed spectrally split, nonlinear-transfer, or
differently normalized actual-finite low-Dirichlet Lyapunov.
No additive-term-resistant obstruction, graph-uniform net exponent,
accelerated PPR/RPPR solver theorem, eleven-coordinate vector,
finite-precision theorem, or new formal dependency edge follows.

**Verified snapshot:** 2026-08-23, after two CLEAN independent reviews of
research Round 027. With
`omega_q^E=(1-q)^2 mu_E/(2q)`, the actual finite reserve satisfies
`Psi_(t+1)^E<=Psi_t^E-q Phi_t^fin+eta_t` but only the drift
`1-q^2/(1+q+q^2)`. Direct `K_8` payment forces
`A>14(1-q)kappa_A/197>=A_*`, `A_*=6929307/98509850`. The repaired bank is
`Psi_t^A=Phi_t+(A/q)E_(t-1)^Q`, and its first genuinely persistent `K_2`
transition is `Psi_3/Psi_2`, with relative loss at most
`(4+2/A_*)q^2`. Globally it decays after only `O(log(q^(-1)))` startup.

## Round 027 reviewed outcomes

- `lem:aesp-cd-q-weighted-euclidean-reserve`: on the realized finite
  recurrence,
  `Psi_t^E=Phi_t^fin+((1-q)^2 mu_E/(2q))||e_(t-1)||_2^2` obeys
  `Psi_(t+1)^E<=Psi_t^E-q Phi_t^fin+eta_t`, where
  `eta_t=2 kappa_A xi_t+kappa_A xi_t^2`. The comparison
  `Psi_t^E<=((1+q+q^2)/q)Phi_t^fin` gives only `q^2` drift. This is a valid
  actual-finite reserve, not an accelerated-rate theorem.
- `prop:aesp-cd-unsplit-q-energy-stagewise-stop`: direct payment of the
  Round026 `K_8` stage-two defect from the lagged unsplit drop forces
  `A>14(1-q)kappa_A/197>=6929307/98509850`. On uniform-seed `K_2`, with
  `q=1/n`, `n>=100`, and `rho=tau=1/16`, the support is full from stage one
  and stage two is persistent. For the correctly lagged bank
  `Psi_t^A=Phi_t+(A/q)E_(t-1)^Q`,
  `0<=1-Psi_3^A/Psi_2^A<=(4+2/A_*)q^2`. This stops only a uniform one-step
  comparison for the simplest unsplit template.
- The complete `K_2` trajectory satisfies
  `Psi_t^A/Psi_1^A<=(4/e)exp(-q(t-1))` and
  `Psi_1^A/Phi_0<=1+A/(q(1-q^2))`. All stages through `1/q` are before the
  fresh gate at `ell_t`. Thus the witness is compatible with the allowed
  soft-logarithmic additive term and is not a net-exponent counterexample.
- `eq:aesp-cd-k8-high-band-payment-limit`: on the same rational `K_8` family,
  `((1-q)mu_E D_2^fin/2)/(q^(-1)(E_1^h-E_2^h))` tends exactly to
  `14641/32256`. This keeps a split high-band payment live; it proves no
  general spectral window because the positive part does not commute with
  the projectors.
- Hard repairs: the first draft's current-index `E_t` reserve was corrected
  to lagged `E_(t-1)`. The first lagged draft's entry transition
  `Psi_2/Psi_1` was corrected to the genuinely persistent stage-two
  transition `Psi_3/Psi_2`, changing the exact bound to
  `(4+2/A_*)q^2`. The checker also tests the fresh gate at `ell_t` and the
  combined global normalization.
- Two independent read-only audits rederived the finite reserve, lagged and
  persistent indices, `K_2` chronology, gate, `K_8` floor, degree scaling,
  high-band limit, and scope. After both repairs, each returned **CLEAN**.
  Exact Round022--027 checkers, Ruff, diff hygiene, and the focused 51-page
  LaTeX build passed without final warnings. Full provenance is in
  [`Round 027`](rounds/2026-08-23-round-027.md).

## Round 026 reviewed outcomes

- `lem:aesp-cd-persistent-square-ledger`: with `u_t=Qe_t`, the previous and
  current finite end residuals combine exactly on `P_t`; they are not erased.
  Every window `2<=k<=ell` satisfies
  `sum G_t^per<=beta_A(1+alpha)/2`,
  `sum (G_t^per)^2<=beta_A^2(E_(k-1)^Q-E_ell^Q)`, and, on
  persistent-dominated stages,
  `alpha^2 sum Delta_t^2<=beta_A^2(E_(k-1)^Q-E_ell^Q)`. These are
  actual-finite controller banks, not a Euclidean collateral or net-exponent
  bound.
- `lem:aesp-cd-truncation-q-energy`: the boundary-aware scalar cap gives
  `<r_t,Qr_t><=beta_A^2<d_t,Qd_t>` and
  `<p_t,Qp_t><=beta_A^2<d_t,Qd_t>`. The two windowed left-hand sides receive
  separate copies of `beta_A^2(E_(k-1)^Q-E_ell^Q)` and must not be added under
  one copy.
- `prop:aesp-cd-k8-reachable-pulse`: for `q=1/10`, `alpha=1/101`, and
  `rho=1/112`, exact shifted solves from zero give
  `N,N,P0,F,N^infinity`. The two pre-gate harmful factors are
  `57072309867/51440146040` and
  `192036347475007/168765931042095`; all later corrections vanish and total
  inflation is below `2 log 2`. This is a reachable transient pulse, not an
  additive-term-resistant counterexample.
- `prop:aesp-cd-k8-q-bank-stop`: for every rational `0<q<=1/100`, the exact
  dense-seed family has
  `D_2^fin>28q*7/112^2` and
  `E_1^Q-E_2^Q<197q^4*7/112^2`. Direct raw payment by that same unsplit drop
  needs more than `28/(197q^3)`, and the `mu_E=kappa_A q^2` weighted payment
  still needs `Omega(q^(-1))`. This does not refute a `q^(-1)`-weighted,
  spectrally split, or differently normalized bank, an additive
  polylogarithmic allowance, the desired net exponent, the solver, or a
  resource vector.
- Two independent read-only audits rederived the identities, constants,
  degree scaling, phase chronology, gates, gammas, and small-`q` scope. One
  audit caught the initial tail-index presentation; after the exact
  `t=3+k`/`5/6` repair, both returned **CLEAN**. Exact Round-022--026 checkers,
  Ruff, diff hygiene, and the focused 48-page LaTeX build passed without final
  warnings. Full provenance is in
  [`Round 026`](rounds/2026-08-23-round-026.md).

## Round 025 reviewed outcomes

- `lem:aesp-cd-support-entry-shield`: for
  `E_t=supp(x_t) minus supp(x_(t-1))`,
  `0<=g_(t,E_t)<=beta_A a_(t-1,E_t)` and
  `alpha Delta_t=max(G_t^ent,G_t^per)`. Exact shifted solves therefore give
  zero first-entry violation. If `G_t^ent>G_t^per`, a finite common correction
  obeys `alpha Delta_t<=beta_A C_end,t-1`. This controls realized entry only;
  persistent rows remain separate.
- `lem:aesp-cd-one-sided-correction-excess`: relative to the residual-free
  driver at the same realized states,
  `Delta_t<=barDelta_t+delta_t` and
  `0<=[r_t-barr_t]_+<=delta_t D^(1/2)1`. Under the dual absolute polish its
  momentum norm is at most
  `(1-q)mu_t xi_(t-1)/(q alpha)`. The current residual or boundary multiplier
  may suppress a correction, so this is not an absolute trajectory-distance
  estimate or finite packing theorem.
- `cor:aesp-cd-entry-inflation-ledger`: on a pre-gate prefix, with
  `eta_gate=2 alpha tau/(1+alpha)` and
  `C_end,t<=delta alpha eta_gate^2 q^2`, every entry-dominated stage has
  `log max(1,gamma_t^fin)<=4 delta q` and the sum before `T` is at most
  `4 delta q T`. The per-stage target costs
  `V[3+tau_cd^(-1)log_+(2(1-alpha)sqrt(V)/(delta alpha eta_gate^2 q^2))]`;
  `V<=1/rho`, `T=O_tilde(1/q)` gives `O_tilde(1/(rho q))`. No resource vector
  follows because persistent-row stages remain open.
- `prop:aesp-cd-post-full-high-pass`: after an exact full correction, the
  first following stage has no correction and the next collapse driver is the
  exact filter in the verified snapshot. Its modal coefficient is
  `lambda[sigma_q lambda-kappa_A]/(kappa_A+lambda)^2`, with
  `sigma_q=(1-q)(3+q)/(1+q)^2`. On `K_8` at `q=1/10`, the exact mixed vector
  has `(C_Ae)_1=21267/121000000>0` despite `Qe>0`. The vector is a filter
  stress test, not a reachable-trajectory theorem or counterexample.
- The adversarial search found no exact rational/algebraic family whose net
  inflation defeats an allowed additive term. Floating path and weak-cut
  tails stayed at roughly `J/(qT)<=0.2` in the searched windows; these values
  are reconnaissance only. Apparent late `K_n` signals were roundoff after
  corrections had ceased. No floating trace, ratio, or counterexample claim
  is promoted.

The independent read-only audit first caught and repaired an inconsistent
`beta,q` checker sample, then rederived every support index, residual and norm
factor, the `4 delta q` constant and inner-work logarithm, the post-full
polynomial and threshold, and every displayed `K_8` fraction. It returned
**CLEAN** after the repairs. Exact Round-022--025 checkers, Ruff, diff hygiene,
and the focused 41-page LaTeX build passed without final warnings. Full
promotion and validation provenance are in
[`Round 025`](rounds/2026-08-22-round-025.md). The next queue is restricted to
a windowed high-energy charge or direct finite Lyapunov for persistent-row
mixed-mode partial corrections; do not infer graph-uniform closure or promote
the quarantined numerical searches.

## Round 024 reviewed outcomes

- `aesp_cd_l1_rppr`: `prop:aesp-cd-retraction-shadowing-stop` proves the exact
  `P_2` support-entry jump. For `0<alpha<1/4`, `rho=(1-alpha)/8`,
  `a=(alpha/8,0)`, and `a^eta=(alpha/8,eta)`, the support-indexed map has
  `L(a)=a` but `L(a^eta)=0` for every `eta>0`. On one fixed positive support,
  an explicit same-controller unclipped pair attains the matching local factor
  `1+1/alpha`. Iterating only this factor over `T` stages forces an
  exponentially small uniform perturbation and places a
  `V T^2 log(1/alpha)` term in the certified inner-work ledger. This is not
  actual finite instability, a direct-packing obstruction, or a solver lower
  bound.
- `lem:aesp-cd-full-correction-separation` works on the explicitly settled
  face `A=S*(rho)`, with `supp(x_t)=A`, `ell_t=x_t`, and
  `Q_A(x*-x_t)>=0`. Its map satisfies `S_A>=q beta_A I`, is entrywise
  nonnegative, and commutes with `Q_A`. If the solve after the full center is
  exact, `x_(t+1)=p(x_t)`, stage `t+1` has no correction. If instead
  `x_(t+1)>0` on `A` and is zero off `A`, then
  `alpha Delta_(t+1)<=2(1-q)||D_A^(-1/2)a_(t+1)||_infinity`
  `<=2(1-q)C_end,t+1`. This residual-only adjacent bound does not control
  partial-correction density or cumulative inflation.
- For nonempty optimal support `A`, `thm:aesp-cd-high-dirichlet-branch`
  assumes `||p(ell_t)-x_(t+1)||_2<=xi_t` and gives
  `||x*-x_(t+1)||_2<=(1-theta_A)||x*-x_t||_2+xi_t`. Under
  `theta_A>=c0*q`, choose
  `eta_gate=2 alpha tau/(1+alpha)`, `xi_t<=c0 q eta_gate/2`, and
  `T>=(c0 q)^(-1)log(2/eta_gate)` to reach the fresh gate and RPPR error
  `tau`. For `alpha<1/4`, `rho=tau=eps_ppr/2`,
  `V_eps=nnz(s)+2/eps_ppr`,
  `W_eps=nnz(s)+O_tilde(1/(sqrt(alpha) eps_ppr))`, and `k<=2/eps_ppr`, the
  promised-class shared-order vector is
  `(O(V_eps),O(V_eps),1,0,O(W_eps),O(W_eps),0,O(V_eps),O(V_eps),O(W_eps),Theta(k+1))`,
  with `C_ctl+C_rec+C_mat=O(W_eps)` jointly. It is unconditional only after
  conditioning on membership in that a-posteriori structural class; the
  unknown optimal face is not an algorithmic certificate.
- The adversarial counter-search found endpoint-path support-growth traces
  whose normalized inflation exceeded one at horizons of order `1/q`, in both
  floating exact-prox and literal finite C2-plus-absolute simulations. Longer
  runs showed a transient that saturated or declined after support settlement,
  compatible with the allowed soft-logarithmic `B`; the smallest-`q` traces
  were tolerance-sensitive. No exact family, sustained net obstruction, or
  numerical ratio is promoted.

Two independent read-only audits returned **CLEAN** after the settled-face and
stage-index quantifiers were made explicit. Together they rederived every `P_2`
sign and support decision, the sharp amplification, the spectrum and
entrywise positivity of `S_A`, the finite residual bound, the high-Dirichlet
gate and vector constants, and the narrow STOP/structural scopes. Exact
Round-022--024 checkers, Ruff, diff hygiene, and the focused 37-page LaTeX
build passed. Full promotion and validation provenance are in
[`Round 024`](rounds/2026-08-22-round-024.md). The next queue is restricted to
the low-Dirichlet actual-finite net/direct Lyapunov problem or a
boundary-aware retraction analysis; do not return to ambient Lipschitz
shadowing or promote the transient numerical path lead.

## Round 023 reviewed outcomes

- `aesp_cd_l1_rppr`: `prop:aesp-cd-p4-infinite-inflation` gives an exact
  rational invariant cone for the Round-022 `P_4` instance. From stage 44 the
  phase word `F N N F N^6 P_0` repeats forever; the harmful phase at
  `47+11j` has `log gamma>=315/33280`, hence
  `I_(44+11N)>=(315/33280)N`. Simultaneously,
  `||e_(55+11j)||_infinity<=(11/500)||e_(44+11j)||_infinity`. This is a fixed-
  `q=1/8`, exact-shifted-minimizer theorem. It supplies no finite-inner
  stability or eleven-vector and does not refute a rate-sensitive net bound.
- `lem:aesp-cd-finite-inner-identities` records the exact finite residual in
  the active fixed-row relation, next start mass, and next collapse.
  `prop:aesp-cd-c2-residual-stop` gives a scalar exact STOP: the usual C2
  relative condition can retain nonzero residual with relative size
  `Theta(sqrt(q))`. `cor:aesp-cd-dual-inner-stop` requires both C2 and
  `C_end<=mu_t xi/sqrt(V)`, obtains shifted-solve error at most `xi`, and
  charges at most `V[3+tau_cd^(-1)log_+(2V/xi)]` additional degree work.
- Conditionally on the **actual finite** sequence satisfying
  `J_T^fin<=(1-c)qT+B`, and for the displayed accelerated vector additionally
  requiring `alpha<1/4`, absolute `c>=c_0>0`, and
  `B=polylog(alpha^(-1),eps_ppr^(-1),V_eps)`,
  `cor:aesp-cd-conditional-finite-acceptance` chooses computable `T,xi`, and
  `cor:aesp-cd-frozen-conditional-contract` reaches a fresh complete terminal
  gate. With `rho=tau=eps_ppr/2`, the conditional accelerated vector is
  `(O(V_eps),O(V_eps),1,0,O(W_eps),O(W_eps),0,O(V_eps),O(V_eps),O(W_eps),Theta(k+1))`,
  where `V_eps=nnz(s)+2/eps_ppr`,
  `W_eps=nnz(s)+O_tilde(1/(sqrt(alpha) eps_ppr))`, `k<=2/eps_ppr`, and
  `C_ctl+C_rec+C_mat=O(W_eps)` jointly. The assumption is not proved.
- Gate correctness and the RPPR-to-PPR bias comparison are unconditional.
  The terminal test is one fresh unshifted product, not the shifted inner heap.
  Cached active rows, neighbor rekeys, the exact KKT-mass sum, one terminal
  interaction, `C_pre=C_resp=0`, and output/materialization charges are all
  explicit. For `1/4<=alpha<=1`, zero-start unshifted RPPR-CD reaches the same
  gate in at most `5/eps_ppr` degree work and has the same shared-order vector
  unconditionally with `W_eps=nnz(s)+O(1/eps_ppr)`.

Two independent read-only audits returned **CLEAN**. One reconstructed the
prefix, phase indexing, cone map, margins, defect/potential intervals, and
inflation floor with exact rational arithmetic. The other independently
rederived those facts and audited the finite-inner identities, C2 witness,
dual stop, computable conditional acceptance constants, terminal bridge, and
scope. Exact checker/build and shared validation provenance are in
[`Round 023`](rounds/2026-08-22-round-023.md). The next falsifiable target is
the actual-finite net exponent, not bounded transient inflation.

## Round 022 reviewed outcomes

- Frozen target/audit contract: on every finite simple undirected unweighted
  no-isolate adjacency-list graph, for a sparse normalized nonnegative seed,
  `alpha in (0,1]`, and `eps_ppr in (0,1)`, the target is a deterministic
  exact-real finite-support output with
  `||D^(-1/2)(x_hat-x^0)||_infinity<=eps_ppr`. Set
  `rho=tau=eps_ppr/2`. For `alpha<1/4`, Route B is full-space safeguarded
  AESP-CD on one fixed `F_rho`, with dynamic greedy normalized-KKT exploration,
  safe lower retraction, cached rows, and the complete gate; for
  `alpha>=1/4`, use the declared zero-start monotone RPPR-CD fallback. Put
  `V_eps=nnz(s)+2/eps_ppr`,
  `W_eps=nnz(s)+O_tilde(1/(sqrt(alpha) eps_ppr))`, and
  `k=nnz(x_hat)<=2/eps_ppr`. The target shared-order vector is
  `(O(V_eps),O(V_eps),1,0,O(W_eps),O(W_eps),0,O(V_eps),O(V_eps),O(W_eps),Theta(k+1))`,
  with `C_ctl+C_rec+C_mat=O(W_eps)` jointly, no preprocessing, one terminal
  interaction, and only logarithmic soft factors. This is an open acceptance
  contract, not a proved theorem. The terminal safe-lower complete-gate
  certificate must give RPPR error `tau`, then `rho+tau=eps_ppr` gives PPR.
- `hybrid_aesp_locsor`: `prop:path-three-settled-reset-drop-obstruction` gives
  the exact settled `P_3` ratio
  `B_1/Delta_1=3/(4q_r^2)+O(1)`, so neither `O(Delta_1)` nor
  `O(Delta_1/q_r)` additive payment works for the declared KKT budget.
  `lem:settled-reset-optimum-drop-bound` preserves the sharp-order general
  bound
  `sum B_j<=((3-5alpha)/(alpha(1-alpha)))sum Delta_j`. This is not a work
  lower bound: the actual settled shock is below `2 Delta`, nonsettled
  displacement is excluded, and stage work sees `B` only logarithmically.
  The exact `6m^2+12m-6` caterpillar row-read identity applies only to the
  conservative literal no-sharing two-product register.
- `aesp_cd_l1_rppr`: `prop:aesp-cd-ledger-only-insufficient` constructs an
  abstract sequence satisfying all current scalar safeguard ledgers while
  accumulating `Omega(1/q)` inflation over `Theta(1/q^2)` steps with constant
  potential progress. It has no fixed `Q`, objective, boundary multipliers,
  or exact prox map and therefore does not refute Route B. Conversely,
  `prop:aesp-cd-p4-late-inflation` and the exact `P_7` corroboration show that
  positive inflation need not coincide with support additions or disappear
  after support stabilization. They are finite exact-shifted-solve traces,
  not an exponent counterexample, finite-inner theorem, end-to-end ledger, or
  work lower bound.

The remaining central lemma must exploit the same fixed Stieltjes operator
across stages and its coupled boundary complementarity, prove accelerated-
scale cumulative packing for the finite relative-inner recurrence, and remain
robust under every charged reset/rekey. Rate-to-gate termination, the terminal
RPPR-to-PPR bridge, cached heap/gate implementation, the full eleven-vector,
the large-`alpha` fallback, and exact-real-only scope remain explicit seams.
Exact contracts, source evidence, audit repairs, and validation are in
[`Round 022`](rounds/2026-08-22-round-022.md).

## Round 021 reviewed outcomes

- `response_preconditioned_hybrid`: `thm:three-label-pivot-gram-refresh`
  retains the canonical unweighted five-scalar state
  `(P_0,A_1,C_1,A_2,C_2)` for codes `00,01,10`, recovers the two required Gram
  entries, and exactly evaluates every positive reweight. Weighted appends
  first invert `z_1=M_1/w_1`, `z_2=M_2/w_2`, and
  `z_0=(M_0-M_1-M_2)/w_0`; the per-refresh vector is
  `(0,0,1,0,Theta(1),0,0,Theta(1),Theta(1),4,1)`.
  `prop:four-label-one-pivot-refresh-obstruction` gives the exact
  `49<121` versus `169>121` four-label STOP. `thm:co-side-gram-refresh`
  supplies arbitrary exact reweights using
  `k+binom(k,2)-c=Theta(k^2)` Gram cells, with necessity only in the linear
  explicit-Gram/open-set model. For `k>L+1`, richer/per-label measurements,
  quadratic state, and `Theta((k^2-c)r_new)` append arithmetic are charged.
- `hybrid_aesp_locsor`: under
  `rho<min{rho_can(m,alpha),rho_2(m,alpha)}`, the padded lower center `y^+`
  does not certify the second batch; its proximal warm start and the imported
  greedy order do. The actual endpoint is strictly nonsettled, commits the
  second canonical batch, and admits a second two-product/twelve-cell KKT
  reset before one genuine greedy continuation stage on `Uhat_2`. The complete
  vectors are `eq:branch-caterpillar-two-nonsettled-prefix-eleven-vector` and
  `eq:branch-caterpillar-two-nonsettled-post-eleven-vector`; total
  `R_int=m+1` and full `R_adj=m+1+O(A_2NS)`. The fresh `B_2` reset is not
  amortized, so there is no multi-face rate or speedup.
- `volume_gated_acceleration`: `prop:t-tree-causal-next-admission-stop` uses
  the six-vertex tree `01,12,23,24,45`, seed 0, and exact `q=1/5` recurrence.
  Restarted `Xi=delta^2` debt is negative at stage 5, survives the stage-9
  admission and its Schur drop, remains negative through stage 13, and first
  closes at stage 14. Counts are `J=5`, `T=17`, `nu_fin=10`, `n_fin=6`, and
  swept volume `125`. This refutes only uniform restarted-block recovery
  before the next admission; all-history solvency stays open. No nonpath
  eleven-vector is asserted, and computational minimality is scaffolding.

Exact contracts, reviews, corrections, and the stop-after-this-cycle queue are
in [`Round 021`](rounds/2026-08-22-round-021.md).

## Round 020 reviewed outcomes

- `response_preconditioned_hybrid`:
  `prop:three-label-norm-only-reweight-obstruction` proves that the complete
  four-norm state of one `00,01,10` bucket cannot distinguish two histories
  requiring opposite answers after weights `(1,3,2)`. The rejection vector is
  `(0,0,1,0,Theta(1),0,0,Theta(1),Theta(1),0,1)`; an exact six-read,
  twelve-write replay comparator has
  `(0,0,1,0,Theta(1),0,6,Theta(1),Theta(1),12,1)`.
- `hybrid_aesp_locsor`:
  `thm:branch-caterpillar-first-nonsettled-continuation` charges the first
  genuinely nonsettled canonical admission, two-product/twelve-cell KKT
  reset, one extrapolated relative-accuracy stage, and native suffix. The KKT
  quantity is a fresh estimate budget, not inherited contraction or speedup.
- `volume_gated_acceleration`: `prop:path-causal-two-admission-recovery`
  gives the face-general exact causal balance identity. On the named path,
  carried stage-4 credit keeps the ledger solvent through the stage-8
  admission; if discarded, stage 11 is the last local STOP and stage 12 the
  first local GO. Nonnegative balance means scalar-ledger closure only.

Exact Round020 contracts and audit repairs are in
[`Round 020`](rounds/2026-08-21-round-020.md).

## Round 019 reviewed outcomes

- `response_preconditioned_hybrid`:
  `thm:notched-sun-batched-columnwise-amplitude-delta-reporter` replaces the
  one-event interface by `B` nonempty unordered atomic batches. Every touched
  cell supplies exactly a gap-free block of its next declared tagged
  occurrences; the reporter stages and validates all tags, amplitudes, caps,
  stream identities, and same-column/same-label/same-tag signed pairs before
  mutating state. With `b_h=sum_(q,i)b_(h,q,i)`, `b_max=max_h b_h`, and
  `S_Sigma=sum_h |{q:sum_i b_(h,q,i)>0}|`, its delta set is exactly
  `{(q,i):c_(q,i)^(h-1)<k*_(q,i)<=c_(q,i)^h}` and it emits one remaining-label
  certificate per affected column. The exact vector is
  `(Theta(n),2,B,Theta(n+J+p+L_Sigma),Theta(C_frag+L_Sigma),0,0,Theta(n+J+p+L_Sigma),O(b_max),0,Theta(S_Sigma+rn))`.
  Nonnegative mode has `(p,C_frag,absolute mass)=(r,L_Sigma,A_Sigma)`; signed
  mode has `(2r,2L_Sigma,3A_Sigma)`. An invalid attempted batch adds its own
  interaction, staged validation, `O(1+b_hat)` temporary cells, and rejection
  output, with no persistent write. Exact crossing is defined only at batch
  boundaries. The theorem keeps the frozen graph/face/cut/ladder/pairing,
  fixed `n`, complete finite declared positive schedules, per-column margins,
  exact block separation, and exact-real arithmetic. Hidden internal chronology,
  undeclared/unbounded mass, arbitrary signed logical amplitudes, split pairs,
  coupled columns, arbitrary fragments, incomplete labels, template mutation,
  RPPR/KKT chronology, fixed-`alpha` uniformity, terminal solving, finite
  precision, rounding, word/bit complexity, and PPR remain excluded.
- `hybrid_aesp_locsor`: at any settled zero-momentum canonical face,
  `lem:branch-caterpillar-settled-proximal-append` zero-pads the center,
  momentum, and estimate point, while the proximal map appends the three
  strictly positive canonical demands divided by `L_A`.
  `SettledAuxAppend` writes exactly twelve new coordinate records plus one
  reset marker with transition vector
  `(0,0,0,0,O(1),O(1),0,Theta(C_(k+1)^can),O(1),12+Theta(1),0)` and no old-
  coordinate write, old-face product, adjacency query, or response call.
  `prop:branch-caterpillar-zero-estimate-carry-fails` proves
  `Sigma_k^es >= (mu_E/2) sum_(v in F_k)(x_(k+1))_v^2>0`, so the estimate proof
  must reset or explicitly bound and charge the analytical shock. The concrete
  `FirstAuxShock-BC-AESP_(1->2)` prefix vector is
  `(9+nu_1,3,2,0,O(1),O(1),O(1),O(C_2),O(C_2),Theta(C_2),6+Theta(2))`; the paid
  native post vector is
  `(vol(S* setminus Uhat_2),m-2,m-1,0,O(C(S*)),0,O(C(S*)+(m-2)log(2+m)),Theta(C(S*)),O(C(S*)),Theta(card(S*)),card(S* setminus Uhat_2)+card(S*)+Theta(m-1))`.
  Interaction and structural first-exposure totals are exactly `m+1`. This is
  a response-assisted settled transition: it pre-exposes the second batch,
  runs no accelerated stage after append, and hands directly to the native
  suffix. It proves no speedup, automatic subquadratic prefix, shock
  amortization, nonsettled-transition bound, class lower bound, other-
  representation obstruction, graph-uniform/PPR theorem, or finite-precision/
  bit result.
- `volume_gated_acceleration`: `prop:path-tight-pair-recovery-block` defines
  `R_(9:k)^post=Psi_9-Psi_k` only from realized post-reset fixed-`U_4`
  decreases. At the tight pair,
  `Psi_9=Psi_10>Psi_11>Psi_12>Psi_7>Psi_13`, so stage 12 is the last reviewed
  STOP and stage 13 the first reviewed GO. The repaired endpoint proof uses
  the variable banks `b_7(c_3)` and `b_13(c_4)`; their exact derivative signs
  show that the tight pair maximizes `Psi_13-Psi_7`, making only the longer
  `7->13` endpoint GO uniform over the held-pair-feasible rectangle. Both
  adjacent failures remain rectangle-uniform, while the positive `7->9` net
  remains tight-pair-only and its sign is not uniform. One scalar analytical
  accumulator leaves the vector unchanged at
  `(Theta(9),Theta(5),1,0,Theta(114),Theta(114),Theta(114),Theta(9),O(9),Theta(114),Theta(9))`.
  The reserve is a proof telescope available only after decreases occur, not
  advance state. This is a finite exact-real single-admission block, not a
  pointwise potential, online face-general rule, multi-admission telescope,
  global horizon, logarithm claim, asymptotic result, nonpath theorem,
  alternate-order result, intermediate-output guarantee, finite-precision
  theorem, or bit-complexity statement.

All three Round-019 owner checkers and independent audits passed. The response
audit rechecked 2,304 states and 233,892 legal nonempty batch transitions,
atomic rejection, the exact vector, and a clean 86-page build. The hybrid
audit rederived the imported state, all twelve records, shock, three vectors,
both horizon edges, and 308 exact transitions through `m=12`, then obtained a
clean 73-page build. The volume audit independently reproduced the chronology,
stage-12/13 signs, endpoint extremality, unchanged vector, and finite scope; it
found one narrow derivative-notation defect, repaired the fixed-symbol display
to variable banks, and passed the post-repair 49-page build. The exact
contracts, adjudication, completed durable synchronization, and validation live
in [`Round 019`](rounds/2026-08-21-round-019.md). Round 019 is redistributed;
do not propagate unqualified shorthand.

## Round 018 verified outcomes

- `response_preconditioned_hybrid`: for every column `q` and label `i`, declare
  positive schedules `a_(q,i,k)`, column length `L_q`, and column mass `A_q`;
  put `L_Sigma=sum_q L_q`. With
  `lambda_i=vartheta^2/[d_(u_i)(1+c_eta)]`,
  `epsilon=9vartheta^3/(1-3vartheta)`, capacity
  `kappa_(q,i)=g/lambda_i`, first over-capacity index `k*_(q,i)`, gap
  `gamma_(q,i)=kappa_(q,i)-A_(q,i,k*_(q,i)-1)`, and local future mass
  `F_(q,i)=A_q-A_(q,i)+A_(q,i,k*_(q,i)-1)`, the exact test
  `m_q=min_i(lambda_i gamma_(q,i)-epsilon F_(q,i))>0` keeps every unreported
  cell at most `g-m_q`. The global asynchronous horizon is
  `L_Sigma-mu_(q,i)+k*_(q,i)-1`, but other-column mass is absent from `F_(q,i)`.
  `thm:notched-sun-columnwise-amplitude-delta-reporter` emits one affected-
  column certificate per event and exactly `rn` first-crossing deltas. Its
  canonical vector is
  `(Theta(n),2,L_Sigma,Theta(n+J+p+L_Sigma),Theta(C_frag+L_Sigma),0,0,Theta(n+J+p+L_Sigma),O(1),0,Theta(L_Sigma))`.
  Nonnegative mode has `(p,C_frag,absolute mass)=(r,L_Sigma,A_Sigma)`; atomically
  paired signed `2`-minus-`1` mode has `(2r,2L_Sigma,3A_Sigma)`. This remains an
  exact-real frozen-template, fixed-`n`, declared finite-positive-mass GO. It
  excludes batches, undeclared/unbounded mass, arbitrary signed logical
  amplitudes, split signed pairs, cross-column coupled response, arbitrary
  fragments, RPPR chronology, fixed-`alpha` uniformity, finite precision, bit,
  and PPR claims.
- `hybrid_aesp_locsor`: `lem:branch-caterpillar-lazy-anchor` stores successful
  heap maxima as range-minimum tags and flushes a coordinate before its next
  write. Under zero padding, `lem:branch-caterpillar-incremental-face-transition`
  keeps every old residual/key verbatim and inserts exactly the three keys
  determined by retained candidate rows. Thus `FaceCarryLowerHeap` performs no
  old-row read, old-key rebuild, fresh old-face product, or eager anchor copy.
  For every fixed `2<=q<=m`,
  `thm:branch-caterpillar-incremental-face-handoff` has response-free prefix
  vector
  `(V_q^can+O(A_<q^fc),q+1+O(A_<q^fc),q,0,O(H_<q^fc),O(A_<q^fc+Q_<q^fc+q),0,O(C_q^can),O(C_(q-1)^can),O(D_<q^fc),3q+Theta(q))`
  and paid suffix
  `(vol(S* setminus Uhat_q),m-q,m-q+1,0,O(C(S*)),0,O(C(S*)+(m-q)log(2+m)),Theta(C(S*)),O(C(S*)),Theta(card(S*)),card(S* setminus Uhat_q)+card(S*)+Theta(m-q+1))`.
  The audit-corrected totals are `R_int=m+1` and
  `R_adj=m+1+O(A_<q^fc)`. The named `DenseFreshAESP` host still writes
  `q(3q-1)/2` fresh auxiliary records. Candidate exposure, numerical stages,
  missing endpoint products, margins/oracle logarithms, and the native response
  remain charged; this is no speedup, accelerated-energy transport, scalar
  potential, graph-uniform, finite-precision, PPR, or bit theorem.
- `volume_gated_acceleration`: retain `Psi=b^2+H_j`, the tight coefficients,
  and chronology `7->8^-->8^+->9`. In
  `prop:path-tight-pair-local-chain-stop`, the production change is
  `4798070852000000223973860697504672676758942656/1000717813631998065466639280969584524631500244140625>0`;
  the reset remains strictly negative by the exact Round-017 Schur slack; the
  follow-up change is
  `185418883451039233414483427688468628491104384871211336448/2666939846939373614068372111818330675602595627307891845703125>0`;
  and at the tight pair the net stage-7--9 change is positive. Production
  nonincrease would need
  `c_3<=2103479690463/41819574955745<c_3^tight`, while follow-up nonincrease
  would need
  `c_4>=2617155474971384896/14508305905763575885>c_4^tight`. Hence every held-
  pair-feasible pair passes the reset but fails both adjacent fixed-face steps;
  the net sign is not uniform over that rectangle.
  The vector remains
  `(Theta(9),Theta(5),1,0,Theta(114),Theta(114),Theta(114),Theta(9),O(9),Theta(114),Theta(9))`.
  This is finite exact-real local-chain evidence only, not an all-held-pairs,
  global, multi-admission, block-horizon, logarithm, asymptotic, nonpath,
  alternate-order, finite-precision, or bit result.

All three owner checkers/builds and independent audits passed. The response
audit additionally checked 2,304 states, 12,288 transitions, and all 360
supplemental single-column interleavings. The hybrid audit found the one round-
ledger contradiction described above; the source, checker, README, and STATUS
were repaired and re-audited through `m=10`. The volume audit independently
reproduced the chronology, Schur data, every transition sign, coefficient
bounds, vector, and finite scope. The exact contracts, adjudication,
cross-redistribution, validation, and next queue live in
[`Round 018`](rounds/2026-08-21-round-018.md). Round 018 is redistributed; no
unqualified shorthand may be propagated.

## Round 017 verified outcomes

- `response_preconditioned_hybrid`: declare positive occurrence amplitudes
  `a_(i,k)`, prefix masses `A_(i,k)`, event count `L=sum_i mu_i`, per-label mass
  `A_i`, and total logical mass `A`. With
  `lambda_i=vartheta^2/[d_(u_i)(1+c_eta)]`,
  `epsilon=9vartheta^3/(1-3vartheta)`, capacity
  `kappa_i=d_(u_i)(1+c_eta)sqrt(vartheta)`, first over-capacity index `k_i*`,
  `gamma_i=kappa_i-A_(i,k_i*-1)`, and
  `F_i=A-A_i+A_(i,k_i*-1)`, the exact test
  `m_A=min_i(lambda_i gamma_i-epsilon F_i)>0` keeps every unreported label at
  most `g-m_A`. `thm:notched-sun-amplitude-delta-reporter` emits at occurrence
  `k_i*`, the first certified and exact crossing even after earlier small
  occurrences. Its vector is
  `(Theta(n),2,L,Theta(n+J+p+L),Theta(C_frag+rL+L+n),0,0,Theta(n+J+p+L),O(1),0,Theta(rL))`.
  It emits `rL` certificates and exactly `rn` deltas; nonnegative streams use
  `(p,C_frag,absolute mass)=(r,rL,rA)`, while signed `2`-minus-`1` streams use
  `(2r,2rL,3rA)`. This remains an exact-real frozen-template, common-schedule,
  fixed-`n` GO; a failed margin is not a response lower bound.
- `hybrid_aesp_locsor`: `lem:branch-caterpillar-implicit-lower-heap` stores
  `r=ell_rho-Q_(UU)z` and keys `[-r_i]_+/(alpha sqrt(d_i))`; one coordinate
  write rekeys only its closed neighborhood, and the heap maximum plus three
  cached parents gives the exact anchored gate query. Standalone initialization
  has vector
  `(vol(U),1,0,0,O(C(U)),O(vol(U)),0,Theta(C(U)),O(1),Theta(C(U)),0)`.
  For every fixed `2<=q<=m`,
  `thm:branch-caterpillar-implicit-lower-handoff` has response-free prefix
  vector
  `(V_q^can+O(S_<q^row+A_<q^ih),2q+1+O(A_<q^ih),q-1,0,O(H_<q^ih),O(D_<q^ih),0,O(C_q^can),O(C_(q-1)^can),O(D_<q^ih),Theta(q))`
  and the same paid post vector as Round 016. The surviving shocks are
  `S_<q^row=3q^2` and `S_<q^adm=(q-1)(3q+2)/2`; `q=m` is still quadratic.
  `LiteralDenseLowerSweep` is a named representation comparison only. This is
  no speedup, transported acceleration, or response-free suffix.
- `volume_gated_acceleration`: choose
  `c_3=2978273417354/42112483166425` and
  `c_4=95554102960761584/1567701294665491845`. At the frozen stage-8 candidate,
  `delta_8^-=delta_8^+=28990137728/3755908203125`,
  `e_8^-=101253632777792/25604026220703125`, `e_8^+=13229/1501825`, the new-row
  normalized KKT value is `-13229/4260625`, the Schur pivot is
  `60073/170425`, and the exact optimum drop is
  `Delta_8=175006441/6398713140625`.
  `prop:path-tight-pair-schur-bank` proves the raw linear switch is larger than
  `Delta_8`, while the squared switch is strictly smaller; hence
  `Psi=b^2+H_j`, `H_3=Delta_8,H_4=0`, decreases across this isolated reset. The
  full vector remains
  `(Theta(9),Theta(5),1,0,Theta(114),Theta(114),Theta(114),Theta(9),O(9),Theta(114),Theta(9))`.
  This is a finite reset-local squared GO/linear STOP, not an all-held-pairs,
  multi-admission, global-potential, logarithm, asymptotic, or nonpath result.

The exact contracts, handoffs, independent clean audits, adjudication,
cross-redistribution, validation, and next falsifiable queue live in
[`Round 017`](rounds/2026-08-21-round-017.md). Round 017 is redistributed; no
unqualified shorthand may be propagated.

## Round 016 verified outcomes

- `response_preconditioned_hybrid`: declare exact positive multiplicities
  `mu_i`, total length `L=sum_i mu_i`, and last-unseen horizon
  `H=L-min_i mu_i`. Under the exact uniform-envelope condition
  `0<vartheta<=(sqrt(81H^2+3)+9H)^(-2)`, equivalently
  `18H sqrt(vartheta)+3vartheta<=1`,
  `thm:notched-sun-multiplicity-delta-reporter` emits a delta only at each
  label's first occurrence and one future-safe certificate per logical column
  per event. Its vector is
  `(Theta(n),2,L,Theta(n+J+p),Theta(C_frag+rL+n),0,0,Theta(n+J+p),O(1),0,Theta(rL))`,
  with `(p,C_frag)=(r,rL)` or `(2r,2rL)`. The scale is sharp only for the
  displayed uniform Neumann envelope; all frozen template, unit-amplitude,
  common-schedule, exact-real, and fixed-`n` promises remain.
- `hybrid_aesp_locsor`: `lem:branch-caterpillar-anchored-lower-transport`
  proves `x_(k+1)|_(Uhat_k)>=x_k`, safe zero padding, and an anchored maximum
  that never decreases old lower coordinates. For every fixed `2<=q<=m`,
  `TransportLower-BC-AESP_(0:q-1)` carries the lower vector through the first
  `q-1` admissions and certifies batch `q`. The prefix/post vectors are
  `eq:branch-caterpillar-transported-lower-prefix-eleven-vector` and
  `eq:branch-caterpillar-transported-lower-post-eleven-vector`; their
  interaction counts are `q-1` and `m-q+2`. Only the prefix has `C_resp=0`.
  Every candidate batch is row-pre-exposed, every test pays a full old-face
  sweep, all accelerated auxiliaries restart, and the suffix builds the native
  response on `Uhat_q`; this is lower-state preservation, not acceleration.
- `volume_gated_acceleration`: for
  `Phi_t(c;U)=delta_t+cq^(-1)e_t(U)`, the held `U_3` pair `6->7` is
  nonincreasing iff
  `c>=2978273417354/42112483166425`, while after the stage-8 face reset the
  held `U_4` pair `9->10` is nonincreasing iff
  `c<=95554102960761584/1567701294665491845`. Their exact positive gap rules
  out every fixed `c>=0`. The full vector remains
  `(Theta(9),Theta(5),1,0,Theta(114),Theta(114),Theta(114),Theta(9),O(9),Theta(114),Theta(9))`.
  This is a finite pairwise STOP only; time-/face-dependent coefficients,
  signed or longer blocks, aggregate potentials, and every asymptotic claim
  remain open.

The exact contracts, handoffs, nested hybrid audit provenance, independent
audits, cross-redistribution, validation, and next falsifiable queue live in
[`Round 016`](rounds/2026-08-21-round-016.md). Round 016 is redistributed; no
unqualified shorthand may be propagated.

## Round 015 verified outcomes

- `response_preconditioned_hybrid`: under the same frozen template, pairing,
  unit logical amplitudes, exact-real model, fixed `n`, and
  `0<vartheta<=(1296n^2)^(-1)`,
  `thm:notched-sun-permutation-delta-reporter` proves that every verified
  common permutation has one matching crossing and one universal unseen-label
  certificate per logical column. The vector remains
  `(Theta(n),2,n,Theta(n+J+p),Theta(C_frag+rn+n),0,0,Theta(n+J+p),O(1),0,Theta(rn))`,
  with `(p,C_frag)=(r,rn)` or `(2r,2rn)`. Repetitions, arbitrary amplitudes,
  different per-column schedules, and batches remain excluded.
- `hybrid_aesp_locsor`: `lem:branch-caterpillar-local-lower-gate-certificate`
  gives a response-free one-sided sign certificate for `k in {0,1}`. Its
  `k=1` incremental vector is
  `(nu_1,1,0,0,O(1),0,0,O(1),O(1),O(1),0)`.
  `LowerGate-BC-AESP_(0:1)` commits the first batch without settlement and has
  response coordinate zero only through its pre-second-interaction/two-gate
  prefix; `eq:branch-caterpillar-two-face-lower-prefix-eleven-vector` and
  `eq:branch-caterpillar-two-face-lower-post-eleven-vector` are authoritative.
  The post phase builds the native response directly on `Uhat_2`. Charged row
  validation pre-exposes the degree-six first-batch rows, so this is a
  comparison and scoped exposure STOP, not a speedup or unexposed exploration.
- `volume_gated_acceleration`: the finite bank
  `Phi_t^bank=delta_t+q^(-1)e_t` decreases on held `6->7` on `U_3` but first
  increases on held `9->10` on `U_4`, by
  `11777177533637842088/2957905129146728515625`, while `delta_t` decreases.
  The full vector remains
  `(Theta(9),Theta(5),1,0,Theta(114),Theta(114),Theta(114),Theta(9),O(9),Theta(114),Theta(9))`.
  Only this coefficient-one finite bank is refuted; different coefficients,
  signed phases, longer blocks, aggregate potentials, and every asymptotic
  logarithm claim remain open.

The exact contracts, handoffs, hybrid audit repair, independent audits,
cross-redistribution, validation, and next falsifiable queue live in
[`Round 015`](rounds/2026-08-21-round-015.md). Round 015 is redistributed; no
unqualified shorthand may be propagated.

## Shared message for every direction

- The primary semantic target is sparse PPR output with degree-normalized
  coordinate error `eps_ppr`; APPR thresholds, objective gaps, RPPR
  regularization, proximal residuals, and KKT diagnostics remain separate
  namespaces.
- The aspirational scales `O_tilde(1 / (sqrt(alpha) * eps_ppr))` and
  `O_tilde(1 / (rho * sqrt(alpha)))` are open graph-uniform targets. Structural,
  trajectory-dependent, conditional, and algorithm-specific results must keep
  those qualifiers.
- Final support volume is not a trajectory bound. Every accelerated or active-
  set direction must charge discovery, repeated old-face work, response
  maintenance, certificates, and output.
- `taxonomy.toml` records only direct formal proof or construction imports.
  Source prerequisites, motivating siblings, experiments, and companion-note
  provenance stay separately labeled in `STATUS.md`; they do not create graph
  edges. The inventory audit now enforces exact formal-field agreement.
- The newest central external comparator is Wei--Yang's 2026 growing-active-set
  SDD method. Its `O_tilde(1 / eps_appr^2)` tradeoff and polylogarithmic
  inverse-teleportation dependence do not directly settle the product target.

## Round 014 verified outcomes

- `response_preconditioned_hybrid`: for the exact frozen template, unit order,
  and `0<vartheta<=(1296n^2)^(-1)`,
  `thm:notched-sun-scale-delta-reporter` proves that
  `NotchedSunScaleDelta` emits one matching label and one universal future-safe
  certificate per logical column without a response/slack cell. Its complete
  vector is
  `(Theta(n),2,n,Theta(n+J+p),Theta(C_frag+rn+n),0,0,Theta(n+J+p),O(1),0,Theta(rn))`,
  with `(p,C_frag)=(r,rn)` or `(2r,2rn)` for separately checked signed streams.
- `hybrid_aesp_locsor`: one paid scan of the three live rows at actual
  `Uhat_1`, plus a separately charged four-coordinate exact response, computes
  `underline(mu)_1=mu_1`. `MarginCert-BC-AESP_1` uses the exact zero/positive-
  gap cap and explicit relative-oracle factor, carries a signed numerical
  endpoint into the second gate, and then hands off to the native reporter.
  Its prefix/post vectors are
  `eq:branch-caterpillar-first-layer-numerical-prefix-eleven-vector` and
  `eq:branch-caterpillar-first-layer-numerical-post-eleven-vector`; total work
  is `O(H_1+C(S*)log(2+C(S*)))`. This is response-assisted comparison only.
- `volume_gated_acceleration`: on the actual projected `q=1/5` path run,
  stages 6 and 7 hold the same `U_3`, yet `delta_7>delta_6` and
  `delta_7/e_7>5=q^(-1)`. The run has `J=4`, `T=16`, `n_fin=5`, `nu_fin=9`,
  swept volume `114`, one terminal return, and vector
  `(Theta(9),Theta(5),1,0,Theta(114),Theta(114),Theta(114),Theta(9),O(9),Theta(114),Theta(9))`.
  This is a finite pointwise STOP, not an asymptotic logarithm result.

The exact contracts, handoffs, independent audits, operational restoration
provenance, cross-redistribution, and next falsifiable targets live in
[`Round 014`](rounds/2026-08-21-round-014.md). Round 014 is redistributed; no
unqualified shorthand may be propagated.

## Highest-priority cross-direction interfaces

1. Output-sensitive finite-band response on high-cut-rank nonequitable cyclic
   cores, now specifically an implicit/batched coded bank, shifted-debt,
   transfer, sparsifier, or scale-aware group-query implementation with all
   construction and validation work charged. Fixed-face shifted debt is no
   longer an open graph-propagation primitive only in the following exact-real
   frozen-interface sense: on one fixed `(A,F)` partition, exposed cut, and
   ladder, the scalar recurrence costs
   `O_tilde(cvol(T)/sqrt(alpha)+C_frag)`. `r` nonnegative columns pay their
   summed product counts; signed columns split into `p=2r` certified streams
   without cancellation credit. `AllBoundaryFlush` then separately charges
   all cut scans, response contractions, rounds, retained debt, Chebyshev
   workspace, materialization, validation, and emission. Simultaneous
   mathematical intervals are not free replies. For a fixed number of columns,
   geometrically spaced all-boundary flushes fit the final-volume product scale
   under the full eleven-vector. A fixed-`n`, sufficiently near-one-`alpha`
   notched-sun epoch now rules out the named `EagerExactSlack` implementation:
   gate `g=((1-alpha)/2)^(5/2)` with band `g/2` emits one new label per event,
   yet eager separately addressed exact slacks force `Theta(pn^2)` response,
   control, and materialization for `Theta(rn)` delta/certificate output, with
   `p=r` for nonnegative streams and `p=2r` for signed certification. Its full
   vector is `eq:notched-sun-eager-eleven-vector`. This is a frozen-face
   representation/query STOP, not an RPPR chronology or a lower bound on
   implicit, batched, coded, scale-truncated, sparsified, or on-demand
   reporters. On that exact template and unit-amplitude stream,
   `NotchedSunScaleDelta` supplies the complementary narrow GO when
   `vartheta<=(1296n^2)^(-1)`: it stores no response/slack cell and emits each
   matching label plus a universal future-safe certificate from a verified
   scalar tail bound. Its complete vector is
   `eq:notched-sun-scale-delta-eleven-vector`.
   `NotchedSunPermutationDelta` now removes the prescribed common order by
   validating a seen-label set atomically; the pointwise matching and unseen-
   tail bounds preserve the same vector for every verified permutation.
   `NotchedSunMultiplicityDelta` further handles every declared positive
   common multiset: `L=sum_i mu_i` charges the stream,
   `H=L-min_i mu_i` controls the exact last-unseen scale, first occurrences
   emit deltas, and repeats do not. The scale is sharp only for the displayed
   uniform Neumann envelope. `NotchedSunAmplitudeDelta` further accepts one
   declared finite positive occurrence schedule shared by every column and
   stream. Its schedule-dependent capacity margin handles unseen and seen-but-
   unreported labels and emits at the first exact threshold crossing, while
   separately charging `L`, total logical mass, fragments, `rL` certificates,
   and `rn` deltas. `NotchedSunColumnAmplitudeDelta` then separates those
   schedules by logical column and arbitrary one-column-at-a-time interleavings.
   `NotchedSunBatchAmplitudeDelta` now admits atomic unordered batches of
   gap-free next occurrences across many cells and columns. It validates the
   entire batch before commit, emits exact first crossings only at the batch
   boundary, and charges `B`, `L_Sigma`, `S_Sigma`, `b_max`, fragment/physical
   mass, certificates, deltas, and rejected attempts separately. No internal
   chronology is defined. These remain frozen-template scalar-envelope GOs;
   failure of a margin is not a response lower bound. The remaining shifted-
   debt question is an output-sensitive partial flush beyond this promised
   template: undeclared or unbounded mass, arbitrary signed logical amplitudes/
   fragments, incomplete epochs, hidden within-batch chronology, coupled
   response columns, or template mutation under a charged implementation, or a
   different safe trace. Ambient-degree
   singleton paths with family-dependent `rho_n` refute pure geometric sleep
   for the canonical gate without giving a work or round lower bound; their
   append-only comparator is linear but has `R_int=n`. Adaptive target-bank
   reuse and bidirectional online rent-or-buy also close the target dimension
   and anchor-right-hand-side count; repeated cut scans or stored-response
   reads remain charged.
   Literal fresh explicit dense
   harmonic tables are ruled out; the fixed-attachment one-Green-direction
   case is closed by `FACR(p)`. The direct matched-report degree lift has a
   full-rank raw report cut but still fails exact KKT legality. Its first
   active-relay repair fails too: in the canonical all-violations trace a
   nonseed degree-two relay is preceded or co-admitted by its degree-one petal,
   so preloading all relays leaves at most one later petal. Raising the petals
   to degree three reverses the local thresholds but still fails globally:
   report quietness and anchor balance leave at most one petal outside a
   report-free all-relay face and its report-free next batch. A second-cycle
   feed also fails for backbone seeds: its report-quiet maximum principle keeps
   every petal nonpositive until a report appears. The anchor-seed counterrange
   has now been followed through its full canonical chronology too. After the
   corrected launch solve and a separate antipodal `n=6` check, at most three
   petals precede the first report; the first distance-two petal batch
   co-admits the seed-site report unless one entered earlier. Relay seeds are
   now exhausted too. With `rho_W=1/(2(2t+1))` and
   `rho_B=1/(2(4t+1))`, the singleton relay face either terminates or its first
   propagating batch contains `w_j`, possibly with `b_j`, before any petal.
   Backbone, anchor, and relay seeds therefore all fail the prescribed long
   report-free later-petal witness. Retire this double-cycle graph family only
   for that witness, not all cyclic witnesses or post-report traces. Next
   require a genuinely different feed/coupling or settlement gadget, and prove
   its exact seed and chronology before any varying-attachment reporter
   analysis.
2. No-restart support-safe acceleration on expanding subspaces. Round 022
   separates the routes and Round 023 sharpens Route B. Route A's declared
   observable settled KKT reset budget cannot be additively paid by the exact
   face drop with coefficient
   `O(1)` or `O(1/q_r)`; its sharp surviving settled order is
   `Theta(1/alpha)`, and the literal no-sharing two-product caterpillar
   register is quadratic. Neither fact is an accelerated-work lower bound:
   the actual settled analytical shock is below twice the drop, the inner
   oracle sees its initial budget logarithmically, and product sharing remains
   allowed. Route B, full-space safeguarded AESP-CD on one fixed objective,
   remains the only plausible graph-uniform route under the frozen target
   contract. Scalar safeguard ledgers alone are insufficient, and the exact
   fixed-operator `P_4` tail now proves that harmful inflation has positive
   density forever after support stabilization. Its geometric primal
   contraction leaves a net exponent possible and gives no small-`q` or
   finite-inner obstruction. Finite-inner residual identities and the scalar
   C2 STOP prohibit silently importing the exact cone; the dual absolute
   polish controls the residual with logarithmic extra work. The terminal
   gate, RPPR-to-PPR bridge, cached-row mechanics, and large-`alpha` fallback
   are now closed independently. Round 024 closes the a-posteriori
   high-Dirichlet class, Round 025 charges realized entries, and Round 026
   gives persistent controllers plus both truncation pieces exact windowed
   `Q`-energy banks. Its reachable `K_8` pulse is transient, while its small-
   `q` family stops alpha-independent direct conversion from the same unsplit
   drop. Round 027 adds an actual-finite Euclidean reserve with only `q^2`
   drift and stops uniform one-step accelerated contraction of the correctly
   lagged unsplit `q^(-1)Q` reserve at the genuinely persistent
   `Psi_3/Psi_2` transition. Its `K_2` witness is not additive-resistant, and
   the exact `K_8` high-band ratio `14641/32256` leaves spectral splitting
   live. The only remaining Route-B queue is a windowed spectrally split,
   nonlinear-transfer, or differently normalized actual-finite
   low-Dirichlet Lyapunov proving
   `J_T^fin<=(1-c)qT+B`, or an equivalent direct rate, with every residual,
   retraction, and rekey charged. Until it is proved, the accelerated rate and
   its full eleven-vector are conditional and there is no exact accelerated
   solver. For the literal zero-padded recurrence, pack or refute
   its remaining signed
   cross-term. For the proved transported-center recurrence, the exact
   remaining-gain occupancy identity replaces the false shortcut
   `weighted tail <= C q sum_t Delta_t`. A zero-start accuracy-driven path now
   forces `Omega(q^-4)` work for the named literal full-prefix implementation
   against `Theta(q^-3)` final product scale. The extra factor is
   `Theta(log(q/rho))`, so soft order and implicit implementations remain
   open. At `rho=tau=q/5`, exact support geometry proves only
   `J,nu_fin=Theta(q^-1)`, `T=Omega(q^-1)`, and the product-scale floor
   `mathfrak V_T=Omega(q^-2)=Omega(nu_fin/q)`. The moving-maximum theorem now
   supplies the complementary exact-real soft upper bounds
   `T=O(q^-2 log(1/q))` and
   `mathfrak V_T=O(q^-3 log(1/q))` for the named internally gated literal
   full-prefix path implementation, with all eleven coordinates and one
   terminal external return charged. It proves no matching lower exponent,
   log removal, sampled `Theta` law, product separation, nonpath result, or
   finite-precision claim. The Round-013 terminal-face lower candidate does
   not close this gap. Its full-face two-state residual recurrence and exact
   characteristic roots are valid only under inactive projection; two audits
   found no derivation of the actual entry coefficients or anti-cancellation,
   no complete rapid-front endpoint/base induction, and no uniform projection-
   inactivity or envelope-unclipping proof through
   `Theta(q^-1 log(1/q))` steps. The theorem and its lower vector were
   withdrawn. The retained `m=2,4,8` checks are finite scaffolding and imply no
   logarithm necessity, lower bound, or refutation. The exact `q=1/5` trace
   also stops frontier-only logic: the global correction suppresses a raw
   stage-6 violation and its maximizer moves from the seed to `v_2` by stage 9.
   Consecutive held stages 6 and 7 further prove that the moving correction can
   increase and can exceed `q^(-1)` times normalized face error with
   coefficient one. The coefficient-one bank
   `Phi_t^bank=delta_t+q^(-1)e_t` absorbs that spike but first increases on the
   next face's held stages 9 and 10 even though the correction falls. The full
   constant family fails on those same two held pairs: pair `6->7` requires
   `c>=2978273417354/42112483166425`, whereas pair `9->10` requires
   `c<=95554102960761584/1567701294665491845`. The exact positive gap rules out
   every fixed `c>=0`. Their tight endpoints define
   `TightPair-Schur_(3->4)`. It is flat on those named pairs, and its squared
   bank plus the remaining-optimum-drop reserve strictly decreases across the
   isolated frozen-candidate stage-8 reset; the raw linear switch exceeds the
   Schur drop. Both adjacent fixed-face steps still fail throughout the feasible
   rectangle, and only the tight pair has the reviewed positive `7->9` net.
   The realized post-reset fixed-`U_4` telescope first repairs that deficit at
   stage 13: `Psi_9=Psi_10>Psi_11>Psi_12>Psi_7>Psi_13`. Exact variable-bank
   derivatives extend only the longer `7->13` endpoint GO over the rectangle.
   The telescope is analytical reserve after realized decreases, not advance
   state or an online horizon. The general admission threshold is
   `2 alpha (rho+tau)/eta`. Any log-removal proof now needs a charged face-
   general recovery rule and a second-admission telescope, or an explicit
   production reserve, signed phase variable, cross-state cancellation, or
   genuinely aggregate space--time potential; a matching lower still needs
   actual entry coefficients and all conditional margins. Do not extend
   the centered response beyond paths before one route closes. For AESP-CD,
   the accepted next route is only a windowed spectrally split,
   nonlinear-transfer, or differently normalized actual-finite
   low-Dirichlet Lyapunov proving `J_T^fin<=(1-c)qT+B` while retaining the
   explicit residual forcing and surviving the Round027 persistent
   low-mode/high-band boundary.
   Horizon-uniform
   inflation and replaying only exact/scalar collapse ledgers are stopped.
   Exact
   transported-center cancellation and a fully charged endpoint-path
   centered-state `LDL^T` realization are already proved. Shock-free
   fixed-face-exact pointwise carryover, raw correction count, and monotone
   Euclidean log-error normalization are refuted routes.
3. A fully charged composition of settled response with iterative frontier
   repair. On the branch-seeded double-Y, every fully charged gate-compatible
   Phase-I prefix now has one paid support-only conversion to the fixed
   scalar/rank-two response, with exact prefix and post eleven-coordinate
   ledgers. On a growing branch-caterpillar, literal eager exact-tip keys are
   now ruled out at linear work, while a balanced implicit tridiagonal transfer
   state now supports a charged `O(m log(2+m))` all-positive delta reporter for
   the fixed-`m`, backbone-first positive-subset policy. For the stricter
   family range `rho<rho_can`, the actual canonical all-violations trace is
   exactly `m` three-label layers and a second delta reporter has the same
   charged scale. Any fully charged Phase-I prefix ending at one of those
   actual checkpoints now has one paid direct support-only conversion to that
   balanced reporter, with exact prefix/post eleven-coordinate ledgers and no
   replay of an earlier face. Its unconditional total is only
   `B_J^full+O(C(S*) log(2+C(S*)))`, and finiteness/validity alone cannot bound
   `B_J^full`: arbitrarily many exact-inner valid stages may be appended before
   the first gate. The named `Full-BC-AESP_0` policy supplies one separately
   charged fixed-family comparator for `m>=2`, branch seed, `alpha<1/2`, and
   `rho<rho_can`. It pays full-envelope exposure, keeps the common checkpoint at
   `Uhat_0={b_1}`, runs the prescribed capped AESP-CD stages, and composes at
   `k=0` in `O(H_*+C_* log(2+C_*))=O_tilde(C(S*)/sqrt(alpha))`. This is an
   exact-real, nonadaptive full-support witness. The soft order hides
   `log(1/(1-2alpha))` and is not uniform as `alpha` approaches `1/2`; it proves
   no adaptive locality, graph-uniform, finite-precision, or PPR result.
   Separately, `FirstLayer-BC_1` scans exactly
   `Uhat_1={b_1,b_2,a_1,r_1}`, commits the actual first canonical batch after
   one interaction, exactly settles the local face, and resumes the native
   response in place. Its prefix vector is
   `(9,2,1,0,O(1),0,O(1),O(1),O(1),Theta(1),Theta(1))`; the complete suffix is
   `eq:branch-caterpillar-first-layer-post-eleven-vector`, and the exact total
   is `O(C(S*) log(2+C(S*)))` without `log(1/(1-2alpha))`. This is a local
   response-native `k=1` RPPR execution, not an accelerated prefix. The signed
   gate-margin proposition gives the exact missing certificate:
   `mu_k=min_v g_(k,v)/beta_(k,v)`. Zero initial gap needs zero stages; for
   positive `Delta_(k,0)`, the imported sufficient stage cap contains
   `log_+(4 Delta_(k,0)/(alpha mu_k^2))`, and each relative-oracle stage still
   has its explicit `log(1/(1-2alpha))` factor. At actual `k=1`, one paid scan
   of the three live rows plus a separately charged four-coordinate exact
   response now computes the sharp `mu_1`. `MarginCert-BC-AESP_1` runs a
   genuine signed numerical prefix, carries its endpoint into the next gate,
   and retires the response arena; its exact total is
   `O(H_1+C(S*)log(2+C(S*)))`. This is a response-assisted comparison, not a
   speedup. The Round-015 local lower map now gives a strictly cheaper one-sided
   sign certificate at `k=0,1`: its `k=1` incremental response coordinate is
   zero. `LowerGate-BC-AESP_(0:1)` runs genuine numerical stages, commits the
   first batch without exact settlement, zero-resets on `Uhat_1`, and remains
   response-free only through the pre-second-interaction prefix. The post
   phase directly builds and charges the native response on `Uhat_2`. Under
   charged row validation, the first candidate rows must be exposed before
   commitment, so this is not a speedup or row-unexposed exploration theorem.
   Round 016 extends the local lower map to every fixed canonical face and
   proves that principal Stieltjes face monotonicity preserves a padded lower
   point across admission. `TransportLower-BC-AESP_(0:q-1)`, for every fixed
   `2<=q<=m`, carries a nonzero anchored lower vector through the first `q-1`
   admissions and certifies batch `q`, with explicit response-free prefix and
   paid `Uhat_q` suffix vectors. It restarts every momentum, proximal, center,
   and estimate-sequence record and pre-exposes the candidate rows. Round 017's
   `ImplicitLowerHeap` removes query-time full-face diagnostic construction;
   Round 018 then carries residuals, keys, and lazy lower-anchor tags through
   every expansion with only three new keys. Numerical work and fresh auxiliary
   arrays remain charged. Round 019 tests those auxiliaries at the smallest
   favorable settled zero-momentum checkpoint. Center, momentum, and estimate
   point zero-pad; the proximal map appends three positive cells, so exactly
   twelve coordinate records plus a reset marker replace dense old-coordinate
   repopulation. The inherited zero estimate certificate nonetheless gains a
   strictly positive analytical shock. The concrete audit settles with a native
   response, runs no accelerated stage after append, and hands directly to the
   paid suffix. Thus coordinatewise lower transport, incremental diagnostics,
   and this settled sparse append are closed, but shock amortization along
   nonsettled transitions, accelerated continuation, subquadratic automatic
   exploration, the remaining canonical range, and arbitrary pre-backbone
   interleavings stay open; neither a speedup nor a class lower bound follows.
4. A same-task lower bound that separates a fully specified budgeted row
   recurrence from persistent response under the eleven-coordinate execution
   ledger, rather than restricting only adjacency access or materialization.
   A fully exposed fixed-support exact-system candidate must also survive the
   finite-dimensional CG cap. The named full-vector `DiagSpecPoly(r)` path
   subclass now meets the product obstruction at `alpha=n^-2`; the full
   `RowRec` class remains open. On the actual sparse certificate, even the
   named supported-prefix polynomial class has a constant-work five-site
   counteralgorithm. Even `eps_ppr=1/(10n)`, which forces full support, admits
   a linear-work singleton-basis/fixed-profile recurrence and a linear-work
   same-task response against the quadratic product scale. The next same-task
   family must prevent both constant-prefix residual-slack spreading and
   sparse-basis cancellation, or justify a stronger Galerkin, trajectory, or
   materialization restriction.

## Do not reuse without its qualifier

- The aggregate Chebyshev debt flush is promoted only with its exact-real
  fixed-`(A,F)`, fixed-exposed-cut, fixed-ladder scope. The scalar recurrence is
  `O_tilde(cvol(T)/sqrt(alpha)+C_frag)`; `r` nonnegative columns multiply the
  sparse products and `r` signed columns require `2r` certified streams. The
  simultaneous exterior intervals are mathematical until the explicitly
  non-output-sensitive `AllBoundaryFlush` pays their cut scans, contractions,
  materialization, classification, validation, and emission. Both fixed-face
  and geometric eleven-vectors also pay interactions, memory, full-face state
  writes, and fragment storage. No online mutation, partial-flush, finite-
  precision/bit, terminal RPPR/PPR, or automatic gate theorem is implied. The
  singleton-path result uses ambient degrees, family-dependent `rho_n`,
  canonical all-violations batching, and `R_int=n`; it is a scheduling
  obstruction with a linear append-only comparator, not a path running-time or
  round lower bound.
- `prop:notched-sun-eager-slack-vector-obstruction` fixes one frozen
  notched-double-sun face containing every anchor and source petal, a rank-`n`
  exposed anchor--report cut, the complete shifted ladder, unit first-rung
  fragments, fixed `n>=5`, and sufficiently near-one `alpha`. Its gate is
  `g=((1-alpha)/2)^(5/2)` with band `g/2`; its separately addressed
  `EagerExactSlack` vector uses `p=r` nonnegative or `p=2r` signed certified
  streams and pays `Theta(pn^2)` response/control/materialization against
  `Theta(rn)` delta/certificate output. This is exact-real and representation-
  specific. It is not the earlier changing-face structural trace, an RPPR/KKT
  chronology, a general reporter lower bound, a terminal solver, or a finite-
  precision/word/bit claim.
- `thm:notched-sun-scale-delta-reporter` fixes that same frozen template, cut,
  ladder, gate, band, unit event order, and logical stream format, and further
  requires `0<vartheta<=(1296n^2)^(-1)`. Its entrywise Neumann argument makes
  one scalar future-tail certificate computationally available, so the named
  reporter needs no response/slack cell. The vector uses `p=r,C_frag=rn` for
  nonnegative columns or `p=2r,C_frag=2rn` for separately checked signed
  streams. This is an exact-real promised-template debt/query GO, not a generic
  dynamic reporter, RPPR/KKT chronology, arbitrary cyclic partial flush,
  terminal solver, uniform fixed-`alpha`, or finite-precision/word/bit result.
- `thm:notched-sun-permutation-delta-reporter` changes only the prescribed
  order in that contract. Every stream must name the same valid unused petal
  with the exact nonnegative unit or signed `+2/-1` amplitudes; the reporter's
  linear seen set validates the permutation online and supports the universal
  unseen-label certificate. The same vector and all fixed-template/scale
  qualifiers remain. Repetitions, missing petals, arbitrary amplitudes or
  fragments, different per-column schedules, batches, template mutation,
  RPPR/KKT chronology, finite precision, and word/bit complexity are excluded.
- `thm:notched-sun-multiplicity-delta-reporter` changes only the declared
  bounded-repetition axis of that contract. Positive counts `mu_i` determine
  authoritative length `L=sum_i mu_i` and last-unseen horizon
  `H=L-min_i mu_i`; the exact uniform-envelope scale is
  `0<vartheta<=(sqrt(81H^2+3)+9H)^(-2)`. One counter per label distinguishes
  first occurrences from repeats, and the full vector uses `L`, `rL`, and
  `C_frag=pL`. The sharpness claim applies only to the displayed uniform
  Neumann envelope. Arbitrary amplitudes/fragments, undeclared or unbounded
  repetition, incomplete epochs, per-column schedules, batches, template
  mutation, RPPR/KKT chronology, fixed-`alpha` uniformity as `L` grows,
  finite precision, and word/bit complexity remain excluded.
- `thm:notched-sun-amplitude-delta-reporter` changes only the unit-amplitude
  axis of that declared multiset contract. One positive occurrence schedule is
  shared by every logical column and stream; its prefix masses, per-label
  capacity, tight interleaving-mass horizon, and positive schedule margin are
  prevalidated. The delta occurs at `k_i*`, which may follow earlier
  subcapacity occurrences, not necessarily at first occurrence. The full vector
  separately charges `L`, `A`, `C_frag`, `rL` certificates, and `rn` deltas,
  with absolute supplied mass `rA` or `3rA`. A failed margin rejects only this
  scalar certificate. Undeclared/unbounded mass, arbitrary signed logical
  amplitudes, per-column schedules, batches, arbitrary fragment support,
  template mutation, RPPR/KKT chronology, fixed-`alpha` uniformity, terminal
  solving, finite precision, rounding, word/bit, and PPR claims remain excluded.
- `thm:notched-sun-columnwise-amplitude-delta-reporter` changes only the
  shared-column schedule and one-column-at-a-time interleaving promises. Each
  column has its own finite declared positive schedule and margin; unrelated
  events enlarge global latency but do not enter the local mass horizon because
  they leave that response block unchanged. It is not a simultaneous-batch or
  coupled-response theorem. `thm:notched-sun-batched-columnwise-amplitude-delta-reporter`
  then changes only the one-event interaction promise: accepted unordered
  batches must contain gap-free next declared occurrences and be atomically
  validated before commit. Crossings exist only at batch boundaries; no hidden
  internal order or subevent certificate is defined. Its `B`, `S_Sigma`,
  `b_max`, invalid-attempt, fragment/mass, state, and output charges may not be
  omitted. Both results keep the frozen template, face, cut, ladder, pairing,
  fixed `n`, complete positive schedules, exact separation, and exact-real
  model. Undeclared/unbounded mass, arbitrary signed logical amplitudes, split
  pairs, coupled columns, arbitrary fragments, incomplete labels, mutation,
  RPPR/KKT chronology, fixed-`alpha` uniformity, terminal/PPR solving, finite
  precision, rounding, and word/bit complexity remain excluded.
- `Full-BC-AESP_0` is a promised fixed-`m` branch-caterpillar, branch-seeded,
  `alpha<1/2`, `rho<rho_can`, exact-real, full-envelope `k=0` comparator. Its
  exact prefix vector pays full support exposure and all repeated AESP work;
  its soft product bound hides `log(1/(1-2alpha))` and is nonuniform at the
  upper alpha endpoint. It supplies no adaptive locality, graph-uniform,
  finite-precision, PPR, other-seed/range/policy, or nonzero-checkpoint claim.
  Separately, `prop:branch-caterpillar-uncapped-prefix-obstruction` says only
  that finite validity cannot bound an unspecified burn-in.
- `FirstLayer-BC_1` is a fixed-`m`, branch-seeded, exact-real,
  `alpha<1/2`, `rho<rho_can` response-native policy. It scans only
  `Uhat_1={b_1,b_2,a_1,r_1}`, makes one canonical interaction, and stops at
  actual checkpoint `k=1`; it performs no accelerated burn-in. Its exact
  `O(C(S*) log(2+C(S*)))` total and two eleven-vectors imply no other-range,
  seed, policy, graph, repeated-full-list, finite-precision, PPR, or graph-
  uniform theorem. The signed gate-margin result is only a sharp symmetric
  norm-ball/objective-gap interface obstruction. It treats zero initial gap as
  zero-stage success and uses
  `log_+(4 Delta_(k,0)/(alpha mu_k^2))` only for positive gap; it neither makes
  `mu_k` a free online certificate nor lower-bounds every local algorithm.
- `MarginCert-BC-AESP_1` has the same fixed-`m`, branch-seeded,
  `alpha<1/2`, `rho<rho_can` scope and begins only after actual checkpoint
  `Uhat_1`. Its sharp `mu_1` is obtained by a paid three-row scan and a
  separately charged exact four-coordinate response, which is then retired.
  The zero start has positive gap and runs genuine numerical stages, but the
  policy is only a response-assisted comparison: it proves no speedup,
  automatic exploration, other checkpoint/range/seed/policy, repeated full
  list, finite-precision, PPR, arbitrary-graph, or graph-uniform result. Its
  exact margin and oracle logarithms may not be hidden.
- `LowerGate-BC-AESP_(0:1)` is response-free only through its two-gate/pre-
  second-interaction prefix. The local lower map certifies exact boundary signs
  at `k=0,1` without `x_k`, `mu_k`, or a response, but every numerical/lower-
  map sweep and row validation is charged. The policy deliberately leaves the
  first committed face unsettled, zero-resets on `Uhat_1`, and then builds and
  charges the native `Uhat_2` response in its post phase. The degree-six first-
  batch rows are pre-exposed under the stated validation contract. It proves
  no speedup, cross-face acceleration, row-unexposed exploration, `k>=2`,
  finite-precision, PPR, arbitrary-graph, or graph-uniform theorem.
- `TransportLower-BC-AESP_(0:q-1)` extends only the coordinatewise lower-state
  invariant to every fixed `2<=q<=m`. Principal Stieltjes face monotonicity,
  zero padding, and the anchored maximum preserve the lower vector, but every
  AESP auxiliary record restarts at each face. Candidate rows are pre-exposed,
  every lower test pays a full old-face sweep, the analysis cap retains
  `mu_k` and the relative-oracle logarithm, and only the prefix has
  `C_resp=0`; the suffix explicitly builds the native response on `Uhat_q`.
  It proves no accelerated-energy transport, sublinear diagnostic, speedup,
  hidden-row exploration, other-range/seed/policy, finite-precision, PPR,
  arbitrary-graph, or graph-uniform result.
- `ImplicitLowerHeap-BC-AESP_(0:q-1)` changes only the implementation of those
  anchored lower tests. The exact residual heap gives closed-neighborhood
  rekeys and constant-size gate queries, but the policy still charges one raw-
  product initialization and one transported-anchor materialization per face,
  fresh AESP arrays, candidate-row exposure, all numerical work and oracle
  logarithms, and the native `Uhat_q` suffix. Its `q=m` face-transition shock
  remains quadratic, so it proves neither speedup nor a subquadratic prefix.
  `LiteralDenseLowerSweep` is only a named representation comparison, not an
  algorithm-class lower bound. All fixed-family, exact-real, range, seed,
  response-free-prefix, non-PPR, and non-finite-precision qualifiers remain.
- `SettledAuxAppend` applies only at an exactly settled zero-momentum canonical
  caterpillar checkpoint with retained candidate rows. The center, momentum,
  and estimate point zero-pad, but the proximal map has three strictly positive
  new cells; all four arrays therefore receive exactly twelve new coordinate
  records plus a reset marker. The transition vector includes no hidden old-
  face product, adjacency query, or response. The old zero estimate certificate
  nevertheless incurs a positive analytical shock that is neither computed nor
  available online for free. `FirstAuxShock-BC-AESP_(1->2)` pays native
  settlement and candidate exposure, runs no accelerated step after append,
  resets the estimate proof, and hands to the native response suffix. It proves
  no speedup, shock amortization, nonsettled transition bound, automatically
  exploring subquadratic prefix, representation/potential class lower bound,
  other graph/range/seed/policy result, graph-uniform/PPR theorem, finite-
  precision guarantee, or bit-complexity claim.
- `thm:path-moving-max-soft-upper` is an exact-real upper bound for the named
  internally gated literal endpoint-path implementation with one terminal
  external return. It proves `O(q^-2 log(1/q))` stages and
  `O(q^-3 log(1/q))` swept volume, not matching lower bounds, logarithm
  removal, sampled `Theta` powers, a product separation, a nonpath theorem, or
  finite-precision/bit complexity.
- `prop:path-monotone-correction-potential-fails` is only the exact finite
  `q=1/5` run. Its same-face stages 6 and 7 refute monotone correction debt and
  the coefficient-one bound `delta_t<=q^(-1)e_t`; the proximal and envelope
  states are strictly unclipped. It does not refute nonmonotone, phase-aware,
  space--time, or amortized potentials, the moving-maximum upper theorem,
  logarithm removal or necessity, matching lower bounds, or any asymptotic
  extension.
- `prop:path-correction-error-bank-potential-fails` is the same finite
  `q=1/5` run with its literal phase origin. It refutes only held-pair
  monotonicity of `delta_t+q^(-1)e_t`: the bank passes `6->7` on `U_3` and
  first fails `9->10` on `U_4` while `delta_t` decreases. Different
  coefficients, signed phases, longer blocks, nonlocal sums, locally rising
  amortized potentials, logarithm removal/necessity, and asymptotic claims
  remain open.
- `prop:path-no-constant-coefficient-bank` strengthens that finite STOP only
  across the two named held pairs. Exact affine constraints require
  `c>=2978273417354/42112483166425` on `6->7` and
  `c<=95554102960761584/1567701294665491845` on `9->10`, with a positive exact
  gap. It rules out every fixed `c>=0` for those two pairs, not time-/face-
  dependent coefficients, signed or multistep blocks, aggregate potentials,
  a global block horizon, logarithm necessity, lower bounds, nonpaths, or any
  asymptotic result. It does not refute coordinatewise lower-state transport
  whose accelerated auxiliary records restart.
- `prop:path-tight-pair-schur-bank` uses exactly the tight endpoints of those
  two local half-lines. The scalar bank is flat only on the named held pairs.
  At the frozen stage-8 candidate the raw linear switch exceeds the exact
  Schur drop, while the squared switch is strictly smaller; only
  `b^2+H_j`, with `H_3=Delta_8,H_4=0`, receives the proved isolated reset
  charge. Held-face evolution, the step producing the candidate, the step to
  stage 9, coefficient selection elsewhere, multiple admissions, and any
  global/logarithmic/asymptotic/nonpath claim remain open. Do not call this a
  global stagewise potential or conflate it with coordinatewise lower-state
  transport.
- `prop:path-tight-pair-recovery-block` retains the literal `q=1/5` phase and
  every Round-018 boundary. The adjacent production and follow-up comparisons
  fail throughout the held-pair-feasible rectangle; the positive `7->9` net is
  only a tight-pair fact and is not sign-uniform. The analytical telescope from
  realized fixed-`U_4` decreases is insufficient through stage 12 and first
  closes at stage 13. Exact variable-bank derivatives make only the longer
  `7->13` endpoint GO rectangle-uniform. This is one finite exact-real single-
  admission proof block, not advance state, a pointwise potential, online face-
  general rule, multi-admission telescope, global block horizon, logarithm
  theorem, asymptotic result, nonpath or alternate-order statement,
  intermediate-output guarantee, finite-precision theorem, or bit claim.
- The withdrawn Round-013 terminal-path candidate is quarantined. Under an
  inactive nonnegativity projection, `lem:path-full-face-linearized-roots`
  gives the correct two-state residual recurrence and characteristic roots;
  finite exact checks cover only `m=2,4,8` prefixes. There is no proved entry-
  coefficient or anti-cancellation bound, rapid-front boundary induction,
  uniform projection/envelope margin, asymptotic terminal-block lower bound,
  lower eleven-vector, logarithm necessity, or refutation of the reviewed
  moving-maximum upper bound.
- AESP--LocSOR's graph-uniform accelerated work is conditional on early AESP
  locality.
- Literal AESP--LocGD and ASPR lower bounds do not apply to every local solver.
- Measured SOR ladders are empirical arms unless a separate note proves the
  required theorem.
- Low-rank harmonic response is closed only under a cut-rank condition; the
  comb obstruction rules out the universal factorization.
- The notched-double-sun result obstructs only exact fixed linear loss tags on
  a prescribed structural face trace. It is fixed-`n`, near-one-`alpha`, and
  is not an RPPR trajectory or finite-band lower bound.
- The coded harmonic bank is a one-fixed-event measurement/candidate theorem,
  not a charged dynamic reporter. Adaptive use needs fresh source and target
  randomness, a summable failure schedule, and explicit construction,
  workspace, membership, and validation charges.
- The notched-sun finite-band calibration holds only for fixed `n`, fixed
  additive parameter, and `alpha` above an `n`-dependent threshold. It is a
  query-count result at one threshold, not a uniform fixed-`alpha` family.
- The matched-report sun is a canonical-trace legality obstruction for the
  direct degree-lift candidate. Although `Q_AW` has rank `n`, the theorem does
  not lower-bound reporter work, response rank, finite-band computation, or
  finite precision; all seed cases are part of the exact KKT split.
- The active-relay matched sun stops only the prescribed canonical
  all-violations chronology with a report-free common face containing all
  relays before a linear petal epoch. One positive relay seed is the sole
  precedence exception. The theorem neither covers arbitrary positive-subset
  policies nor excludes paired petal--relay traces, and it is not a reporter
  or response lower bound.
- The degree-three petal-cycle repair is also only a canonical all-violations
  chronology STOP. Its `n-1`-petal conclusion requires both a `W`-free face
  containing all relays and a `W`-free next batch. It exhausts every seed orbit
  for `alpha in (0,1)` and `rho>0`, but says nothing about positive-subset
  timing, reporter work/rank, finite-band computation, finite precision, or
  numerical stability.
- The double-cycle feed STOP fixes a backbone seed `s=e_(b_j)` and canonical
  all-violations batching. It proves only that the first petal batch contains a
  report; it makes no claim after `W` enters. For `alpha in (0,1)`, an anchor seed and
  `0<rho<(1-alpha)/8`, the complete canonical continuation has at most three
  report-free petals before the first report. Its corrected launch threshold
  is `lambda>8t+2-3/(2t)`, and `n=6` needs the separate antipodal two-neighbor
  argument. For every even `n>=4`, every relay seed has the exhaustive strict
  first-batch thresholds `rho_W=1/(2(2t+1))` and
  `rho_B=1/(2(4t+1))`: the face is absent, singleton-terminal, or reports in
  its first propagating batch before any petal. This retires the graph family
  only for the prescribed long report-free later-petal witness. Positive-subset
  timing, post-report behavior, response directions, reporter work/rank,
  finite-band computation, finite precision, and stability remain outside the
  three seed theorems. The anchor and relay audit vectors are incremental to
  the fully paid prefixes `P_firstW` and `P_firstW^relay`, never replacements.
- The branch-caterpillar obstruction fixes `m>=2`, `alpha in (0,1)`, seed `s=e_(b_1)`, and
  `0<rho<rho_cat(m,alpha)<=1/3`, and uses one legal exact-KKT positive-subset
  singleton order—not the canonical all-violations batch. It lower-bounds only
  literal separately addressed `EagerTipKey` rewrites. The new
  `CaterpillarKineticDelta` GO uses the same fixed family and branch seed but
  only a backbone-first positive-subset policy and delta-label interface. Its
  `O(m log(2+m))` exact-cell ledger excludes arbitrary pre-backbone
  interleavings, repeated full-list output, a uniform positive `rho` range,
  other seeds, finite precision, conditioning, `kappa=1`, and product or
  graph-uniform accelerated claims. `CaterpillarCanonicalLayerDelta` separately
  closes actual canonical all-violations only for the stricter fixed-family
  range `0<rho<rho_can(m,alpha)<=rho_cat(m,alpha)<=1/3`; its full vector is
  `eq:branch-caterpillar-canonical-eleven-vector`. The rest of
  `rho<rho_cat` remains open, and extra queries/replies are additive.
- The caterpillar Phase-I handoff is narrower still: it accepts only a fully
  charged prefix ending immediately after an actual strict-range canonical
  checkpoint, with its common layer/support records paid. One direct traversal
  constructs the arm absorptions, tridiagonal cells, and balanced transfer
  tree without replay. The prefix vector is
  `eq:branch-caterpillar-composite-prefix-eleven-vector`, the post vector is
  `eq:branch-caterpillar-composite-eleven-vector`, and the unconditional total
  is only `B_J^full+O(C(S*) log(2+C(S*)))`. Product work is conditional on an
  independent bound for `B_J^full`; no numerical energy, other seed/policy,
  larger `rho`, repeated full lists, precision, PPR conversion, or arbitrary
  graph claim is imported.
- The exact endpoint-path oracle result is an algebraic-cell materialization
  separation only. It is not a word/bit, precision-robust, recurrence, or
  `nu_fin / sqrt(alpha)` lower bound.
- The CG counteralgorithm defeats a fully exposed endpoint-path product
  candidate; it does not refute every local approximate-PPR lower bound.
- The Round-022 graph-uniform Route-B statement is a frozen target/audit
  contract, not a theorem. Its `rho=tau=eps_ppr/2` bridge, one terminal
  interaction, large-`alpha` fallback, exact-real cell model, and complete
  eleven-vector are mandatory acceptance conditions. Round 023 proves the
  gate/bias bridge, implementation mechanics, and fallback; the accelerated
  rate and vector remain conditional on the actual-finite net exponent.
- The settled `P_3` ratio concerns only the declared observable KKT upper
  budget `B`. The actual analytical settled shock is below `2 Delta`, and the
  relative inner work depends logarithmically on `B`; therefore the
  `Theta(1/alpha)` sharp budget coefficient is not an accelerated-work lower
  bound. Likewise `6m^2+12m-6` is only the literal no-sharing two-product row-
  read count, not a necessary cost or class lower bound.
- `prop:aesp-cd-ledger-only-insufficient` has no fixed `Q`, RPPR objective,
  boundary multipliers, or exact prox trajectory. It stops scalar-ledger-only
  proofs but does not refute fixed-operator Route B. The earlier `P_4` and
  `P_7` observations remain finite traces; the new `P_4` invariant-cone
  theorem proves infinite positive-density inflation at fixed `q=1/8` while
  retaining geometric primal contraction. It refutes horizon-uniform and
  transient-only inflation, not accuracy-logarithmic dependence, a net
  exponent, finite-inner robustness, or end-to-end work.
- The AESP-CD one-edge counterexample refutes only packing collateral charge by
  monotone Euclidean log-error with coefficient `o(1/q)`, including
  alpha-independent and polylogarithmic coefficients. It does not refute a
  multistep collapse potential, another potential, or a local surrogate.
- The three-arm token theorem is exact-real, center-seeded, single-branch
  RPPR with `rho<1/3`. Its `kappa=1` and `O(C(S*))=O(1/rho)` ledger excludes
  two branching vertices, cycles, finite precision or bit complexity, an
  RPPR-to-PPR conversion, and a graph-uniform accelerated-arm conclusion.
- The double-Y theorem is exact-real and fixes the seed at one branch vertex,
  `s=e_o`, with `alpha in (0,1)` and `rho in (0,1/3)`. Its fixed SPD rank-two
  core does not cover other seeds, a growing branch backbone, cycles, a
  Phase-I work bound, finite precision, or an RPPR-to-PPR conversion.
- The double-Y Phase-I handoff accepts only a fully charged gate-compatible
  prefix. Its prefix and post eleven-coordinate vectors include certificate
  replies, terminal materialization, response recovery, rounds, and both
  memory peaks; the unconditional total is only
  `B_J^full+O(C(S*))`. Product work still needs an independent bound on
  `B_J^full`, and the particular Catalyst/AESP prefix requires `alpha<1/2`.
- `FACR(p)` is an exact-cell, absorption-only reporter on a simple-cycle core
  with supplied closure certificates, one fixed attachment, and exterior
  coordinates held at zero. Its `O(V_fin+|R| log(2+|R|)+Z)` work and
  `O(V_fin)` memory do
  not cover varying attachments, exterior-coordinate updates, finite
  precision, bit complexity, or numerical stability.
- The endpoint-edge zero-shock result refutes only fixed-face-exact,
  shock-free pointwise carryover. It is not a cumulative-shock or newly
  admitted-volume obstruction and gives no asymptotic work lower bound.
- The transported-center cancellation identity applies to a general safe
  interior face expansion; only its charged implementation GO is path-specific.
  That implementation is internally gated exact-real endpoint-path RPPR with
  `R_int=1` and one terminal external certificate/output stage; intermediate
  external emissions are excluded. Its centered-momentum and append-only
  `LDL^T` state avoids eager dense-shift writes, but the exhaustive vector still
  charges every old-face recurrence, response, state, materialization,
  validation, and output operation. There is no bound on `T`, late shocks,
  swept volume, branching/cyclic graphs, graph-uniform work, finite precision,
  or bit complexity. PPR conversion requires the terminal one-sided
  certificate and `rho=tau=eps_ppr/2`.
- The weighted-shock occupation identity is exact, but the terminal-edge
  family refutes only a universal `C q sum_t Delta_t` collapse. Its
  `(1-q)/q` ratio at `T=2`, `J=1`, `nu_fin=2`, and swept volume `3` gives no
  lower bound on `T`, swept volume, product work, or any other asymptotic work;
  occupancy-based bounds, terminal-accuracy floors, and other potentials
  remain open.
- The zero-start swept-prefix theorem is exact-real and specific to the named
  literal full-prefix endpoint-path implementation. For integer `n>=2`, put
  `q=1/n`, `chi=(1-q)/(1+q)`, `L=n^2`, and let the endpoint-seeded
  ambient-degree path `P_N=(v_0,...,v_N)` have `N=L+1` edges. It forces
  `mathfrak V_T>=q^-4` against `nu_fin/q=Theta(q^-3)`, with full vector
  `eq:path-swept-eleven-vector`, `R_int=1`, and terminal-only external output.
  The factor is `Theta(log(q/rho))`: no soft-order, implicit-implementation,
  general product, nonpath, finite-precision, or bit-complexity conclusion
  follows. At the separate constant ratio `rho=tau=q/5`, only the exact
  product-scale floors in `prop:path-constant-ratio-floor` are proved. The
  `q=1/5` maximizer switch in `prop:path-frontier-only-gate-fails` refutes a
  frontier-only proof shortcut, not the unproved `T=Theta(q^-2)` or
  `mathfrak V_T=Theta(q^-3)` laws and not any product separation.
- The notched-sun adaptive audit uses fresh independent source and target
  blocks with `delta_k=delta/(k(k+1))`. It rules out only explicit dense
  per-event harmonic-table writes. Because the frontier is a singleton, table
  application can be factored in `O(p_k+r_k)` arithmetic; no
  `Theta(p_k*r_k)` application lower bound is claimed.
- The `alpha=n^-2` path result is for exact full-vector
  `DiagSpecPoly(r)` under its named spectral-atom charge. It excludes supported
  growing-prefix recurrences and arbitrary implicit, rational, nonlinear, or
  adaptive responses, and has no finite-precision consequence.
- The five-site path counteralgorithm concerns the different exact-cell sparse
  residual-certificate task at `eps_ppr=1/10`. It refutes product work only
  for the named `CertPrefixPoly` class/task and neither shortens the ordinary-CG
  trajectory nor weakens the full-vector `DiagSpecPoly(r)` theorem.
- At `eps_ppr=1/(10n)`, the same exact-cell path task forces full support but
  still admits `Theta(n)` singleton-basis/fixed-profile recurrence work with
  `C_mat=0` and a `Theta(n)` same-task append-only response. This refutes only
  the broad `CertPrefixPoly` task/class, not ordinary CG, full-vector
  `DiagSpecPoly(r)`, finite precision, or a narrower justified
  Galerkin/trajectory/materialization class.

## Round 001 verified redistribution

- `aesp_cd_l1_rppr`: a singleton-support single-edge run has a full safe
  correction every other stage, so support growth cannot pay the raw count.
  All those defects are negative and `I_T = 0`; future proofs must pack only
  rounds with `gamma_t > 1`.
- `response_preconditioned_hybrid`: on the notched double sun, exact
  Schur-diagonal-loss updates are dense, and for each fixed size they span
  linear dimension when `alpha` is sufficiently close to one. Stop pursuing a
  universal exact polylogarithmic linear tag; scale-aware nonlinear, coded,
  sparse-recovery, and cyclic-transfer routes remain live.
- `local_solver_oracle_hierarchy`: use the eleven-coordinate ledger. A free
  graph-dependent inverse collapses exposed-system recurrence iterations, and
  the path theorem separates exact intermediate materialization from one
  append-only response but does not close the computational lower bound.
- Concurrent coded-bank and shifted-debt claims in the response direction were
  not part of the notched-double-sun assignment. Their folder-local status is
  preserved, but controller promotion requires a separate proof audit.

## Audit result and redistribution

Every registered direction now has a controller-reviewed `STATUS.md` with its
exact contract, evidence ledger, blocker, dependencies, resume pointer, and
known inconsistencies. The reusable work is grouped into four active chains:

1. `aspr23_bound_audit` + `aesp_cd_l1_rppr` +
   `volume_gated_acceleration`: safe support is substantially closed; each
   AESP-CD positive log term is bounded by an a-posteriori collateral fraction,
   but its cumulative accelerated-scale packing remains open. Raw correction
   count and direct Euclidean log-error packing are refuted charges.
2. `incremental_active_set_sdd` + `propagate_settle_framework` +
   `response_preconditioned_hybrid`: correction algebra and structural
   responses are closed; the common blocker is the high-cut-rank within-epoch
   finite-band reporter.
3. `rlsor_terminal_exact_rung` + `frontier_adaptive_ladder` + `two_rung_sor`:
   the durable conclusion is empirical. `B = 2.5` is best among six tested
   points, not a proved optimum.
4. `local_solver_oracle_hierarchy`: guard every lower bound by its actual
   recurrence, materialization, response, preprocessing, control, precision,
   memory, interaction, and output restrictions.

`hybrid_local_solver_complete_note` is the proof-bearing consolidated
theorem-attempt/archive. `hybrid_local_solver_synthesis` is the
controller-facing integration and gap map; it points to proof owners instead of
duplicating their derivations. Neither is an additional solver backend.

## Controller corrections exposed by the audit

- The taxonomy and manifest now record the audited AESP-CD target: safe lower
  centers are proved; the live target is cumulative correction
  log-inflation/effective correction rounds. The research and acceleration
  literature ledgers have been synchronized to the same boundary.
- The manifest now says `measured-best-tested-b2p5`; a fine per-alpha sweep
  and independent reproduction remain open.
- “Exact rung” in empirical SOR notes means a unit coordinate settlement, not
  an exact restricted block solve.
- `cvol` is now defined locally in both `incremental_active_set_sdd` and
  `response_preconditioned_hybrid`, so each proof source is standalone with
  respect to its charged-volume unit.
- Several README/status-table summaries omit hypotheses or work qualifiers.
  Their folder-local `STATUS.md` records the exact discrepancy; do not repeat
  the short summary without checking it.
- Cross-note provenance is broader than the acyclic taxonomy dependencies.
  Treat a narrative cross-link as provenance, not automatically as a theorem
  dependency, and avoid introducing a false dependency cycle.

## Round 002 verified redistribution

- `aesp_cd_l1_rppr`: for every round,
  `log max(1,gamma_t) <= C_t^col <= 1`; the charge uses only collateral
  coordinates, has the exact collapse amplitude for `t >= 2`, and may
  overcharge a benign collateral round. It is a-posteriori because it uses
  `x*`. The next theorem is cumulative time packing or a local surrogate.
- `response_preconditioned_hybrid`: the fixed-event coded-bucket theorem is
  sound after making both random layers fresh under adaptivity and charging a
  summable failure schedule, capacity, membership, and workspace. It supplies
  a measurement/candidate family, not its dynamic construction. On the
  notched sun, the finite-band threshold isolates one leaf only pointwise for
  fixed size and sufficiently near-one `alpha`; all hierarchy and validation
  work remains charged.
- `local_solver_oracle_hierarchy`: exact CG defeats the concrete endpoint-path
  product candidate at `alpha=n^-4`, using `O(n^2)` versus target
  `Theta(n^3)`, while the charged LDL comparison costs `Theta(nu_n)`. The
  reusable dimension condition applies only after a fixed-support exact SPD
  system is fully exposed with linear-cost matrix--vector access and enough
  vector memory.

The durable evidence and review corrections are recorded in
[`Round 002`](rounds/2026-08-21-round-002.md). The next round should attack
the cumulative collateral packing, dynamic construction of the fixed-event
response measurements, and the surviving exact-system dimension regime.

## Round 003 verified redistribution

- `aesp_cd_l1_rppr`: `prop:aesp-cd-euclidean-packing-fails` gives an exact
  full-support single-edge safeguarded run with a harmful stage-two collateral
  charge `Theta(q)` but only `Theta(q^2)` same-step and two-stage-prefix
  Euclidean log-progress. No `o(1/q)` coefficient works. Continue with
  multistep collapse, another potential, or a locally checkable surrogate.
- `response_preconditioned_hybrid`:
  `prop:notched-sun-fresh-dense-coded-table-charge` makes the natural fresh
  two-layer coded construction valid over the whole prescribed epoch using
  `delta_k=delta/(k(k+1))`, then proves that explicit dense harmonic-table
  writes carry an unsuppressed anchor-size overhead. The singleton frontier
  allows `O(p_k+r_k)` factored application, so the promoted obstruction is the
  table write, not an entrywise application bound. Pursue only implicit,
  batched, or compressed realizations of this route.
- `local_solver_oracle_hierarchy`:
  `thm:surviving-path-polynomial-obstruction` closes the named exact
  full-vector `DiagSpecPoly(r)` escape at `alpha=n^-2`: cyclicity gives degree
  `n-r-1`, and the named full-vector application rule gives
  `Omega(n*nu_n)=Omega(nu_n/sqrt(alpha))` recurrence work under the concrete
  budget. This is not the full `RowRec` lower bound and does not cover
  supported-growing-prefix or arbitrary implicit/rational response routes.

All three results passed focused builds and independent proof/scope reviews;
the corrections and validation record are in
[`Round 003`](rounds/2026-08-21-round-003.md). Round 003 is redistributed. No
unqualified version of any result should be propagated.

## Round 004 verified redistribution

- `adaptive_revisit_control`:
  `thm:three-arm-spider-token-countdown` extends irreversible common-state
  activation tokens to the center-seeded unweighted three-arm spider. Exact
  affine prefix products and two root aggregates survive every legal certified
  boundary-batch order with `kappa=1` and total exact-cell work
  `O(C(S*))=O(1/rho)`. This closes one branching vertex only; two branch
  vertices, cycles, precision, bit complexity, accuracy conversion, and a
  graph-uniform accelerated arm remain open.
- `two_rung_direct_theory`:
  `thm:direct-fixed-attachment-cycle-reporter` gives the absorption-only
  `FACR(p)` reporter on a simple-cycle core. Supplied certified components all
  attach at one fixed vertex, so every boundary key is affine in one monotone
  Green-response scalar. Static crossing lists report both gates in
  `O(V_fin+|R| log(2+|R|)+Z)` exact-cell work and `O(V_fin)` memory with no
  global rekey. Changing exterior coordinates, varying attachments, and
  precision/bit guarantees remain open.
- `volume_gated_acceleration`:
  `prop:one-edge-zero-shock-fails` gives an exact pointwise counterexample to
  transporting a zero fixed-face-exact energy through safe admission without
  a shock or equivalent transported state. It does not refute cumulative
  shock, multistep transport, newly admitted-volume amortization, or give an
  asymptotic work lower bound.

All three results passed focused builds and independent proof, resource, and
scope audits. Review fixes distinguish supplied-certificate verification from
online closure discovery, state the exact-cell/finite-precision boundaries,
orient the endpoint error vector explicitly, and retain the
fixed-face-exact/pointwise qualifier. The durable record is
[`Round 004`](rounds/2026-08-21-round-004.md). Round 004 is redistributed; no
unqualified version of these structural results should be propagated.

## Round 005 verified redistribution

- `propagate_settle_framework`:
  `prop:notched-sun-rppr-trace-obstruction` proves that, at every common
  anchor-containing face, each unseeded notched-double-sun pair `(f_i,w_i)`
  has equal exact RPPR demand and is co-admitted by the canonical all-positive
  gate. Apart from at most one seed pair, the prescribed `F`-only structural
  epoch cannot be a canonical single-seed trace while
  `W intersect U = empty`. The finite-band consequence is only for one
  simultaneous uniform point-estimate call at one common face; arbitrary
  asynchronous interval refinement remains open. This is not a reporter or
  representation lower bound, and the structural response audit remains
  valid.
- `evolving_support_cg`:
  `thm:endpoint-path-exact-cg-certificate` proves that endpoint-seeded exact
  ordinary CG at `alpha_n=n^-2`, `eps_ppr=1/10`, and zero start first satisfies
  the actual degree-normalized residual certificate at `K=n`. Its residual is
  a frontier singleton while its direction fills the visited prefix. The
  selected literal sequential rereading/materialized exact-cell implementation
  costs `Theta(n^2)=Theta(nu_n/sqrt(alpha_n))`. This is not a recurrence-class,
  adaptivity, or finite-precision lower bound.
- `hybrid_aesp_locsor`:
  `thm:three-arm-composite-response-handoff` converts any fully charged
  gate-compatible Phase-I prefix on the center-seeded unweighted three-arm
  spider, for `0<alpha<1` and `0<rho<1/3` in exact real-cell arithmetic, to the
  common affine activation-token response in one paid pass after discarding
  signed numerical and momentum state. The note's particular composite
  Catalyst/AESP prefix is available only in its stated range `alpha<1/2`.
  Post-work is `O(C(S*(rho)))`, and total work is
  `B_J^full+O(C(S*(rho)))`. The product corollary requires an independent fully
  charged bound on `B_J^full`; no numerical-energy carryover, shock-free
  continuation, RPPR-to-PPR conversion, general-graph, or finite-precision
  claim is made.

All three outcomes passed focused builds and independent mathematical,
resource, and scope audits. Review fixes distinguish active-face membership
from graph exterior, simultaneous point estimates from asynchronous interval
refinement, and the structural pruning threshold `tau_fb` from the KKT demand
scale. They also give separate fresh/stored eleven-coordinate trace ledgers,
remove mandatory scan/output claims, verify the CG continuant and literal
ledger, and preserve the handoff's fully charged-prefix premise. The durable
record is [`Round 005`](rounds/2026-08-21-round-005.md). Round 005 is
redistributed; no unqualified version of these results should be propagated.

## Round 006 verified redistribution

- `propagate_settle_framework`:
  `prop:matched-report-sun-gate-obstruction` rules out the direct
  matched-report degree lift. On the even simple unweighted sun with degrees
  `4,1,2`, the raw anchor--report cut has rank `n`, but exact report quietness
  and the nonseed anchor equation force every report-free canonical prefix to
  contain at most one `F` petal. All seed cases are exhausted. This is only a
  legality obstruction; the next candidate is an active relay stem.
- `adaptive_revisit_control`:
  `thm:double-y-two-core-token-countdown` gives the branch-seeded unweighted
  double-Y an exact-real `kappa=1` common-state countdown for every legal
  certified batch order. The response is scalar before the second branch and
  a fixed SPD rank-two Schur core afterward, with total
  `O(C(S*))=O(1/rho)` charged work. For
  `rho<zeta/[3(3+zeta)]`, `zeta=(1-alpha)/(1+alpha)`, every legal order reaches
  that phase. Growing cores and the independent Phase-I bound remain open.
- `local_solver_oracle_hierarchy`:
  `thm:five-site-supported-prefix-counteralgorithm` refutes the proposed
  sparse-certificate path separation for the named class. At `n>=8`,
  `alpha=n^-2`, and `eps_ppr=1/10`, both a degree-four `CertPrefixPoly`
  execution and a same-task five-row `LDL^T` response have constant
  exact-cell ledgers and `nu_fin=11`. This does not affect exact full-vector
  `DiagSpecPoly(r)` or the ordinary-CG trace.

All three outcomes passed focused builds and independent mathematical,
resource, and scope review. The reconciliation keeps the matched-report result
at KKT legality, fixes the double-Y seed and exact-real/fixed-core scope, and
keeps the five-site result on the identical sparse-certificate task with all
eleven coordinates charged. The durable handoffs, review corrections, and
validation record are in [`Round 006`](rounds/2026-08-21-round-006.md).
Round 006 is redistributed; no unqualified version should be propagated.

## Round 007 verified redistribution

- `propagate_settle_framework`:
  `prop:active-relay-matched-sun-preload-obstruction` stops only the intended
  relay-first chronology on the even active-relay matched sun. In every
  report-free canonical all-violations trace, each nonseed degree-two relay is
  preceded or co-admitted by its degree-one petal. A face containing all relays
  therefore already contains at least `n-1` petals. One positive relay seed is
  the sole precedence exception; positive report seeds violate the epoch and
  nonpositive seed loads give zero. Paired petal--relay traces and arbitrary
  positive-subset policies remain possible, and no reporter lower bound is
  claimed.
- `hybrid_aesp_locsor`:
  `thm:double-y-composite-response-handoff` converts every fully charged
  gate-compatible Phase-I prefix on the branch-seeded double-Y into the exact
  scalar/rank-two response in one paid support-only pass, with no private replay.
  Stable prefix and post vectors report all eleven resources, including
  external certificate replies, terminal materialization, recovery response,
  rounds, and both memory peaks. Unconditional total work is
  `B_J^full+O(C(S*))`; the product corollary still requires an independent
  bound on `B_J^full`. The result is exact-real, fixed-core, branch-seeded RPPR,
  and the particular Catalyst/AESP prefix additionally requires `alpha<1/2`.
- `local_solver_oracle_hierarchy`:
  `thm:tight-certificate-sparse-basis-counteralgorithm` proves that the
  endpoint task at `alpha=n^-2`, `eps_ppr=1/(10n)` forces full output support
  and `nu_fin=2(n-1)`. Exact singleton-basis propagation plus delayed synthesis
  of one fixed spatial profile nevertheless costs only `Theta(n)` with
  `C_mat=0`; a same-task append-only `LDL^T` response also costs `Theta(n)`,
  versus `Theta(n^2)` product scale. Only the broad path-specific exact-cell
  `CertPrefixPoly` task/class is refuted.

All three outcomes passed focused builds and independent mathematical,
resource, and scope review. Reconciliation narrowed the relay theorem to the
canonical all-violations gate, expanded the hybrid handoff from a bespoke
subledger to exact prefix/post eleven-vectors with reply emissions and
sum/peak composition, and checked the path profile and residual constants in
exact rational arithmetic. The durable handoffs, corrections, redistribution,
and validation record are in
[`Round 007`](rounds/2026-08-21-round-007.md). Round 007 is redistributed; no
unqualified version should be propagated.

## Round 008 verified redistribution

- `propagate_settle_framework`:
  `prop:petal-cycle-relay-first-obstruction` stops the degree-three-petal
  repair under the exact single-seed canonical all-violations gate. If a
  `W`-free face contains every relay and its next all-violations batch is also
  `W`-free, report quietness and anchor balance force all but at most the
  seed-paired petal to be active already. The local relay-before-petal window
  and rank-`n` raw cuts survive, but the required long report-free chronology
  does not. The incremental fresh/stored audit vectors are respectively
  `(Theta(n),1,0,0,Theta(n),0,0,0,O(1),0,0)` and
  `(0,0,0,0,Theta(n),0,0,0,O(1),0,0)`; the complete paid trace prefix is
  retained separately. The stable resource and timing anchor is
  `rem:petal-cycle-relay-trace-ledger`.
- `adaptive_revisit_control`:
  `prop:branch-caterpillar-eager-rekey-obstruction` gives, for each fixed
  `m`, one legal branch-seeded positive-subset singleton order reaching an
  `m`-vertex tridiagonal response core. Each long-arm append changes all
  `m+1` deferred leaf demands, so literal `EagerTipKey` performs quadratic
  old-key writes. Its implementation vector is
  `(Theta(m),Theta(m),3m+1,0,Theta(m^2),0,Theta(m^2),Theta(m),O(m),Theta(m),Theta(m))`;
  demanding every positive-tip list at every checkpoint instead makes
  `C_emit=Theta(m^2)`. The balanced affine-transfer comparator still permits
  logarithmic append/update/named-tip queries and keeps implicit reporters
  open; its stable anchor is
  `rem:branch-caterpillar-implicit-transfer-comparator`.
- `volume_gated_acceleration`:
  `prop:transported-schur-ledger` proves exact transported-center cancellation,
  and `prop:path-implicit-transport-ledger` realizes it on endpoint prefixes
  with centered momentum and append-only `LDL^T`. The full vector is
  `(O(nu_fin),O(J+1),1,0,O(mathfrak V_T+nu_fin),O(mathfrak V_T+nu_fin),`
  `O(mathfrak V_T+J+nu_fin),O(nu_fin),O(nu_fin),`
  `O(mathfrak V_T+n_fin),Theta(n_fin+1))`. Expansion-specific append work is
  charged to newly admitted volume, while all old-prefix work remains in
  `mathfrak V_T`; no total accelerated-work theorem follows. The stable
  exhaustive-vector anchor is `eq:path-transport-eleven-vector`.

All three outcomes passed independent mathematical, model, scope, and
resource review. Reconciliation preserves canonical all-violations versus
positive-subset chronology, distinguishes eager key arrays from implicit
transfer state, and keeps the endpoint-path identity separate from bounds on
steps, shocks, or swept volume. The detailed proofs and every vector use the
shared order
`(C_adj,R_adj,R_int,C_pre,C_ctl,C_rec,C_resp,M_pers,M_tmp,C_mat,C_emit)`.
The durable handoffs, review corrections, redistribution messages, and
validation provenance are in
[`Round 008`](rounds/2026-08-21-round-008.md). Round 008 is redistributed; no
unqualified version should be propagated.

## Round 009 verified redistribution

- `propagate_settle_framework`:
  `prop:double-cycle-feed-report-obstruction` stops the proposed independent
  cycle feed only for exact backbone-seeded canonical all-violations traces.
  Every report-free prefix is petal-free, and the first petal batch, if any,
  contains a report. An anchor seed instead has a report-free first-petal
  counterrange `0<rho<(1-alpha)/8`; no post-`W`, all-orbit, positive-subset,
  response-direction, or reporter/work claim follows. Beyond the complete
  paid prefix, the fresh/stored audit vectors are respectively
  `(Theta(n),1,0,0,Theta(n),0,0,0,O(1),0,0)` and
  `(0,0,0,0,Theta(n),0,0,0,O(1),0,0)`. The stable scope and resource anchor is
  `rem:double-cycle-feed-trace-ledger`.
- `adaptive_revisit_control`:
  `thm:branch-caterpillar-kinetic-delta-reporter` gives the named exact-real
  `CaterpillarKineticDelta` reporter on the fixed-`m`, branch-seeded,
  family-`rho` caterpillar for every backbone-first exact-KKT positive-subset
  order. It maintains the exact all-positive live-tip set, emits only newly
  positive delta labels, and charges proposed-label membership and certificate
  replies. For `2m-1<=J<=3m`, `eq:branch-caterpillar-kinetic-eleven-vector` is
  `(Theta(m),Theta(m),J+1,0,O(m log(2+m)),0,O(m log(2+m)),Theta(m),O(m),Theta(m),Theta(m))`,
  giving `O(m log(2+m))` exact-cell work. Canonical all-violations,
  pre-backbone interleavings, full-list output, uniform `rho`, finite precision,
  `kappa=1`, and product work remain open.
- `volume_gated_acceleration`:
  `lem:weighted-shock-occupation` identifies the exact remaining-gain
  occupancy in the transported-center shock tail. The terminal-edge equations
  `eq:terminal-edge-parameters`--`eq:terminal-edge-final-kkt` give an internally
  gated exact-real execution with `T=2`, `J=1`, `nu_fin=2`, swept volume `3`,
  and ratio `(1-q)/q` in `eq:no-q-shock-packing`. Its exhaustive vector at
  `eq:terminal-edge-eleven-vector` is
  `(O(2),O(2),1,0,O(5),O(5),O(6),O(2),O(2),O(5),Theta(3))`.
  This refutes only universal `C q sum_t Delta_t` packing, not an
  occupancy-based bound or a `T`, swept-volume, product-work, or other
  asymptotic lower bound.

All three outcomes passed independent mathematical, policy/model, scope, and
resource review. The cyclic audit required the inactive-anchor case split and
an explicit no-post-`W` qualifier. The kinetic audit was clean after
rederiving the Green-column factorization, scalar rank-one update, strict heap
and no-duplicate semantics, family reach range, suffix persistence, exact
batch range, and all eleven coordinates. The path audit required only the
notation repair `b` to `beta_edge`. Every displayed vector uses
`(C_adj,R_adj,R_int,C_pre,C_ctl,C_rec,C_resp,M_pers,M_tmp,C_mat,C_emit)`.
The durable handoffs, review corrections, redistribution messages, and
validation provenance are in
[`Round 009`](rounds/2026-08-21-round-009.md). Round 009 is redistributed; no
unqualified version should be propagated.

## Round 010 verified redistribution

- `propagate_settle_framework`:
  `prop:double-cycle-anchor-seed-obstruction`, for `alpha in (0,1)`, follows the anchor-seed
  counterrange `0<rho<(1-alpha)/8` through its complete exact canonical
  continuation for every even `n>=6`. Before the first report, only
  `f_j,f_(j-1),f_(j+1)` can enter; the first batch meeting a distance-two petal
  co-admits `w_j` unless a report entered earlier. The corrected launch
  threshold is `lambda>8t+2-3/(2t)`, and the antipodal `n=6` case uses a
  separate two-neighbor check. Relay seeds, positive-subset batching,
  post-report behavior, response directions, and reporter/work lower bounds
  remain open. The fixed-anchor fresh/stored proof-audit vectors at
  `eq:double-cycle-anchor-audit-vectors` are
  `(O(1),1,0,0,O(1),0,0,0,O(1),0,0)` and
  `(0,0,0,0,O(1),0,0,0,O(1),0,0)`; each is composed with, and never replaces,
  the fully paid prefix `P_firstW`.
- `adaptive_revisit_control`:
  `thm:branch-caterpillar-canonical-layer-reporter` fixes `m>=2`,
  `alpha in (0,1)`, branch seed `s=e_(b_1)`, and
  `0<rho<rho_can(m,alpha)<=rho_cat(m,alpha)<=1/3`. The actual canonical
  all-violations trace is exactly `m` three-label layers. The exact-real
  `CaterpillarCanonicalLayerDelta` reporter scans/tests each newly live
  boundary row, emits only strict-positive delta labels, co-emits ties, and
  charges one certificate reply per batch. Its full vector at
  `eq:branch-caterpillar-canonical-eleven-vector` is
  `(Theta(m),Theta(m),m+1,0,Theta(m),0,O(m log(2+m)),Theta(m),O(m),Theta(m),Theta(m))`,
  giving `O(m log(2+m))` exact-cell work. The remaining canonical range,
  other seeds/policies, full-list output, uniform `rho`, precision,
  conditioning, `kappa=1`, accuracy conversion, and product work are excluded.
- `volume_gated_acceleration`:
  `prop:path-zero-start-swept-separation` fixes integer `n>=2`, sets
  `q=1/n`, `alpha=q^2`, `chi=(1-q)/(1+q)`, `L=n^2`, and
  `rho=tau=(q/3)chi^L`, and uses the endpoint-seeded ambient-degree path
  `P_N=(v_0,...,v_N)` with `N=L+1` edges. Mandatory prefix discovery gives
  `L<=J<=L+1`, `T>=J`, and `mathfrak V_T>=L^2=q^-4`, while
  `nu_fin/q=Theta(q^-3)`. For the named literal full-prefix implementation,
  `eq:path-swept-eleven-vector` is
  `(Theta(nu_fin),Theta(J+1),1,0,Theta(mathfrak V_T),Theta(mathfrak V_T),`
  `Theta(mathfrak V_T),Theta(nu_fin),O(nu_fin),Theta(mathfrak V_T),Theta(nu_fin))`.
  This is an exact-real log-free lower bound only: the factor is
  `Theta(log(q/rho))`, leaving soft order, implicit implementations, the
  constant-ratio `rho=tau=q/5` case, nonpaths, product work, and precision open.

All three outcomes passed independent mathematical, policy/model, scope, and
resource review. The cyclic review corrected the launch solve's omitted third
anchor neighbor and separated the antipodal `n=6` case. The adaptive review
was mathematically clean and hardened the arm-transfer versus induced
branch-core absorption wording and the newly-live versus previously revealed
label distinction. The path audit rederived the mandatory prefix, stage and
swept-volume bounds, exact accuracy logarithm, interface, and all eleven
coordinates. Every vector uses
`(C_adj,R_adj,R_int,C_pre,C_ctl,C_rec,C_resp,M_pers,M_tmp,C_mat,C_emit)`.
The durable handoffs, review reconciliation, redistribution messages, and
validation provenance are in
[`Round 010`](rounds/2026-08-21-round-010.md). Round 010 is redistributed; no
unqualified version should be propagated.

## Round 011 verified redistribution

- `propagate_settle_framework`:
  `prop:double-cycle-relay-seed-obstruction` fixes every even `n>=4`, every
  relay seed `s=e_(r_j)`, `alpha in (0,1)`, and `rho>0`. With
  `t=(1+alpha)/(1-alpha)`,
  `rho_W=1/(2(2t+1))`, and `rho_B=1/(2(4t+1))`, the exact strict first-batch
  split at `eq:double-cycle-relay-first-batch` is: absent initialization for
  `rho>=1/2`; a terminal singleton for `rho_W<=rho<1/2`; exactly `{w_j}` for
  `rho_B<=rho<rho_W`; and exactly `{w_j,b_j}` for `0<rho<rho_B`. Equality
  leaves the zero-demand vertex inactive. Every propagating relay trace
  therefore reports before any petal. Together with the backbone and anchor
  stops, this retires the double-cycle family only for the prescribed long
  report-free later-petal witness. The complete paid prefix
  `P_firstW^relay` is retained; the fresh/stored fixed-site proof-audit vectors
  at `eq:double-cycle-relay-audit-vectors` are
  `(O(1),1,0,0,O(1),0,0,0,O(1),0,0)` and
  `(0,0,0,0,O(1),0,0,0,O(1),0,0)` and never replace prefix work.
- `hybrid_aesp_locsor`:
  `thm:branch-caterpillar-composite-response-handoff` fixes `m>=2`, branch
  seed `s=e_(b_1)`, `alpha in (0,1)`, and the strict range
  `0<rho<rho_can(m,alpha)<=rho_cat(m,alpha)<=1/3`. A fully charged Phase-I
  prefix ending immediately after actual canonical checkpoint `Uhat_k`
  converts by one paid direct support traversal to
  `CaterpillarCanonicalLayerDelta`; it reconstructs no earlier face. The
  exact prefix vector at
  `eq:branch-caterpillar-composite-prefix-eleven-vector` is
  `(C_adj^J,R_adj^J,k,C_pre^J,C_ctl^J,C_rec^J,C_resp^J,M_pers^J,M_tmp^J,C_mat^J,C_emit^J)`.
  With `J_post=m-k`, the post vector at
  `eq:branch-caterpillar-composite-eleven-vector` is
  `(O(vol(S*)),O(J_post+2),J_post+1,0,O(C(S*)),0,`
  `O(C(S*)+J_post log(2+m)),O(C(S*)),O(C(S*)),Theta(|S*|),`
  `|S* minus Uhat_k|+|S*|+Theta(J_post+1))`.
  The unconditional total is only
  `B_J^full+O(C(S*) log(2+C(S*)))`; the product corollary is conditional on
  an independent `B_J^full=O_tilde(C(S*)/sqrt(alpha))` bound. No numerical
  estimate-sequence energy is retained.
- `volume_gated_acceleration`:
  `prop:path-constant-ratio-floor` fixes `0<q<=1/4`, `alpha=q^2`,
  `rho=tau=q/5`, and
  `L_q=floor(log(5/3)/(-log((1-q)/(1+q))))`. It proves
  `L_q<=J_q<=5/q`, `T_q>=J_q`,
  `1+2L_q<=nu_fin<=5/q`, and
  `mathfrak V_(T_q)>=L_q^2`; hence only the exact product-scale floors
  `J_q,nu_fin=Theta(q^-1)` and
  `mathfrak V_(T_q)=Omega(q^-2)=Omega(nu_fin/q)`. Its full literal
  implementation ledger is `eq:path-constant-ratio-eleven-vector`.
  `prop:path-frontier-only-gate-fails` then gives the exact `q=1/5` STOP: a
  seed-attained correction suppresses the raw stage-6 frontier violation, and
  the maximizer switches to `v_2` at stage 9. Independent review corrected
  the general gate in `eq:path-global-correction-gate` to
  `2 alpha (rho+tau)/eta`; the `rho=tau` specialization and exact trace are
  unchanged. Neither result proves `T=Theta(q^-2)`,
  `mathfrak V_T=Theta(q^-3)`, or a product separation.

All three outcomes passed independent mathematical, policy/model, scope, and
resource review. The relay audit checked the singleton settlement, both strict
threshold equalities, all rotations/parity classes, and prefix-versus-proof
ledger. The caterpillar audit checked all `k` endpoints, prior delta/reply
charges, the direct branch-cell count, no-replay semantics, both vectors, and
sum/peak composition. The path audit replayed the first nine stages exactly
and supplied the general-threshold correction above. Every vector uses
`(C_adj,R_adj,R_int,C_pre,C_ctl,C_rec,C_resp,M_pers,M_tmp,C_mat,C_emit)`.
The durable handoffs, review corrections, redistribution messages, and
validation provenance are in
[`Round 011`](rounds/2026-08-21-round-011.md). Round 011 is redistributed; no
unqualified version should be propagated.

## Next controller priorities

1. Replace the now-retired double-cycle witness with a genuinely different
   bounded-degree feed/coupling or settlement gadget escaping all accumulated
   chronology obstructions. Audit response directions only after a long legal
   report-free chronology exists.
2. Extend or refute the caterpillar checkpoint handoff on
   `rho_can<=rho<rho_cat` or under arbitrary pre-backbone positive-subset
   interleavings. `FaceCarryLowerHeap` already preserves the response-free lower
   map, residual keys, and lazy anchor through every fixed canonical admission
   without old-face raw-product/key rebuild or eager anchor copy. At a settled
   zero-momentum checkpoint, `SettledAuxAppend` further shows that four explicit
   auxiliary arrays need only twelve new coordinate records plus a reset marker,
   but the inherited estimate proof has a positive analytical face shock. Next
   bound and amortize that shock along actual nonsettled transitions, then run a
   charged accelerated continuation, or return the first exact obstruction.
   Do not turn the settled audit into a speedup or class lower bound. Any attempt
   to avoid candidate-row pre-exposure must name and charge a trusted-metadata
   access model. Preserve the analysis-side margin and
   `log(1/(1-2alpha))` factors, restarted versus transported state, distinct
   prefix/post response coordinates, and delta output separate from repeated
   full lists.
3. For transported-center paths, remove the logarithm in the reviewed
   `T=O(q^-2 log(1/q))`, `mathfrak V_T=O(q^-3 log(1/q))` upper bound or prove
   matching constant-ratio lower bounds using the moving global correction.
   The next upper attempt must name a nonmonotone, phase-aware, or space--time
   block potential: monotone correction debt, the coefficient-one `q^(-1)`
   pointwise error surrogate, and every fixed nonnegative coefficient in
   `delta+cq^(-1)e` now fail on the two reviewed held pairs. The tight face-
   dependent endpoints give an exact squared-bank charge for the isolated
   frozen-candidate stage-8 reset, while both adjacent steps fail throughout
   the feasible rectangle and the positive `7->9` net is tight-pair-only. The
   realized fixed-`U_4` recovery telescope first closes the longer `7->13`
   endpoint, and only that endpoint GO is rectangle-uniform. Next derive a
   face-general closing rule whose reserve is charged as decreases occur and
   test it across a second admission; otherwise test an explicit production
   reserve or cross-state cancellation and return the shortest exact failure.
   Do not treat the finite telescope as advance credit or a global horizon.
   Separately pack the literal zero-padding cross-term. A
   renewed slow-mode route must
   derive the actual full-face entry coefficients and an anti-cancellation
   estimate and prove projection inactivity plus envelope unclipping through
   the proposed asymptotic window. Conditional roots and finite traces are not
   enough. Move to a nonpath response only after one surviving path interface
   has a total-work theorem.
4. Seek a different same-task family or independently justified
   Galerkin/trajectory/materialization subclass that defeats both
   constant-prefix residual-slack spreading and exact singleton-basis
   propagation. Preserve all eleven coordinates and the same response/output
   task.
5. For the positive shifted-debt route, build a packed partial flush between
   checkpoints beyond the exact promised notched-sun scale trace, or prove a
   different support-safe response trace. Common event permutations, declared
   multiplicities, finite positive occurrence amplitudes, independent column
   schedules, asynchronous one-column events, and declared atomic gap-free
   batches are now closed on the frozen template. Next relax undeclared or
   unbounded mass, arbitrary signed logical amplitudes/fragments, incomplete
   epochs, coupled response columns, changing capacity/weights, or template
   mutation and either preserve an output-sensitive universal future
   certificate or force the first exact response query/state expansion. Charge
   batches, affected columns, maximum staging, invalid attempts, logical and
   physical mass, fragments, certificates, and distinct output separately; do
   not invent within-batch chronology or treat a failed margin as a lower bound.
   The singleton-path
   obstruction already refutes pure geometric sleep, and the fixed notched-sun
   STOP rules out eager separately addressed slacks. Charge every capacity/
   slack-weight change, source-side anchor-cut scan, and target-side response
   read.

## Round 012 verified redistribution

- `response_preconditioned_hybrid`: the aggregate Chebyshev theorem now fixes
  `(A,F)`, exposed cut, and ladder; states scalar, `r`-column, and signed-split
  costs including `C_frag`; distinguishes mathematical intervals from the
  paid `AllBoundaryFlush`; and supplies complete fixed-face, geometric, and
  singleton-path eleven-vectors. The deterministic check artifact records its
  command and seed. Independent review rederived every cost and the path
  comparator and found the reconciled direction clean.
- `hybrid_aesp_locsor`: validity plus finiteness is now formally obstructed as
  a prefix bound. The named `Full-BC-AESP_0` policy gives a separately paid,
  fixed-family, full-envelope `k=0` witness and composes with the reviewed
  suffix at product scale. Independent review required `alpha<1/2` in the
  obstruction, an arbitrary reachable-prefix/exact-inner-stage construction,
  and explicit `log(1/(1-2alpha))` nonuniformity; all three repairs passed
  focused re-audit.
- `volume_gated_acceleration`: `thm:path-moving-max-soft-upper` controls the
  full moving correction without locating its maximizer and proves
  `K_q=O(q^-1 log(1/q))`, `T=O(q^-2 log(1/q))`, and
  `mathfrak V_T=O(q^-3 log(1/q))` with a complete exact-real literal-path
  vector. Independent review rederived the energy cap, gate threshold, block
  ceiling, face count, vector, and exclusions and found no actionable issue.

Every promoted vector uses
`(C_adj,R_adj,R_int,C_pre,C_ctl,C_rec,C_resp,M_pers,M_tmp,C_mat,C_emit)`.
The durable handoffs, corrections, controller adjudication, checks, and next
queue are in [`Round 012`](rounds/2026-08-21-round-012.md). Round 012 is
redistributed; no unqualified shorthand above may be propagated.

## Round 013 verified redistribution

- `response_preconditioned_hybrid`:
  `prop:notched-sun-eager-slack-vector-obstruction` fixes a frozen face,
  rank-`n` cut, ladder, unit fragment policy, gate, band, fixed `n`, and
  sufficiently near-one `alpha`. It proves exactly one new delta label per
  event but `Theta(pn^2)` work for the named `EagerExactSlack` state against
  `Theta(rn)` output, with `p=r` or `2r` and complete vector
  `eq:notched-sun-eager-eleven-vector`. Independent review rederived the graph,
  asymptotics, trace, signed streams, exact cyclic-factor comparator, all
  eleven coordinates, and representation-only exclusions and found it clean.
- `hybrid_aesp_locsor`: `FirstLayer-BC_1` reaches the actual local
  `Uhat_1` checkpoint after one canonical interaction, with exact prefix and
  native suffix vectors and total `O(C(S*) log(2+C(S*)))` work. The separate
  signed gate-margin proposition is sharp for symmetric norm-ball
  certificates. Review rederived the four-row degree total `9`, both arenas,
  suffix composition, margin identity, equality witness, and gap conversion.
  It required one narrow repair: zero initial gap is zero-stage success, and
  `log_+(4 Delta_(k,0)/(alpha mu_k^2))` is used only for positive gap. The
  corrected statement preserves the per-stage `log(1/(1-2alpha))` factor.
- `volume_gated_acceleration`: the proposed terminal-face logarithmic lower
  theorem failed two independent audits and was withdrawn together with its
  lower vector and claimed refutation. Only the conditional inactive-
  projection two-state recurrence and exact roots in
  `lem:path-full-face-linearized-roots`, plus finite exact checks, remain as
  direction-local scaffolding. The missing actual coefficients, anti-
  cancellation, rapid-front endpoint/base induction, and uniform projection/
  envelope margins prohibit every asymptotic lower conclusion.

Every promoted vector uses
`(C_adj,R_adj,R_int,C_pre,C_ctl,C_rec,C_resp,M_pers,M_tmp,C_mat,C_emit)`.
The durable handoffs, review corrections, controller adjudication, checks, and
next queue are in [`Round 013`](rounds/2026-08-21-round-013.md). Round 013 is
redistributed; no unqualified shorthand and no withdrawn volume claim may be
propagated.

## Round 014 verified redistribution

- `response_preconditioned_hybrid`:
  `thm:notched-sun-scale-delta-reporter` proves the narrow
  `NotchedSunScaleDelta` GO on the exact Round-013 template when
  `0<vartheta<=(1296n^2)^(-1)`. The verified scalar matching/tail certificate
  replaces response/slack storage and gives the complete output-sensitive
  vector `eq:notched-sun-scale-delta-eleven-vector`. Independent review
  rederived the decomposition, entrywise Neumann bound, constants, event and
  signed-stream logic, vector, and exclusions and found it clean.
- `hybrid_aesp_locsor`:
  `lem:branch-caterpillar-first-layer-margin-certificate` charges the exact
  `mu_1` certificate at actual `Uhat_1`, and
  `thm:branch-caterpillar-first-layer-numerical-handoff` gives the capped
  signed numerical splice with complete prefix/post vectors and exact margin
  and oracle factors. The separately paid exact response makes this a
  comparison, not a speedup. Independent review rederived both `m` cases,
  chronology, arenas, caps, response retirement, vectors, emissions, peaks,
  and scope and found it clean.
- `volume_gated_acceleration`:
  `prop:path-monotone-correction-potential-fails` supplies the exact finite
  `q=1/5` STOP against monotone correction debt and the coefficient-one
  `q^(-1)` face-error bound. An independent exact-Fraction replay reproduced
  the admission/hold/certification chronology, rational inequalities,
  unclipped states, `J=4,T=16,n_fin=5,nu_fin=9`, swept volume `114`, and vector
  specialization and found it clean. The logarithm remains open.

At 15:58 the host switched automatically from
`agent/prove-aesp-cd-inner-oracle` (`513e848`) to updated `main` (`14f3e60`)
after PR #26 and preserved the uncommitted Round-014 direction work in retained
stash `e47d263`, named
`WIP Round 014 before switching to latest main (2026-08-21)`. The controller
applied it non-destructively: all 12 direction files were restored without
conflict or data loss, and both affected audits repeated their build, checker,
and source checks. This is operational provenance, not a mathematical event.

Every promoted vector uses
`(C_adj,R_adj,R_int,C_pre,C_ctl,C_rec,C_resp,M_pers,M_tmp,C_mat,C_emit)`.
The durable handoffs, audits, redistribution messages, restoration provenance,
checks, and next falsifiable targets are in
[`Round 014`](rounds/2026-08-21-round-014.md). Round 014 is redistributed; no
unqualified shorthand may be propagated.

## Round 015 verified redistribution

- `response_preconditioned_hybrid`:
  `thm:notched-sun-permutation-delta-reporter` proves that the Round-014
  pointwise matching and unseen-tail bounds survive every online-verified
  common permutation. `NotchedSunPermutationDelta` atomically validates the
  common unused label and exact amplitudes, retains a linear seen set, and has
  the same complete vector, including `p=r,C_frag=rn` or
  `p=2r,C_frag=2rn`, without response, slack, future-label scan, or numerical
  materialization. Independent review rederived the constants, event logic,
  vector, and exclusions and found it clean.
- `hybrid_aesp_locsor`:
  `lem:branch-caterpillar-local-lower-gate-certificate` gives an exact one-
  sided response-free sign certificate at `k=0,1`, while
  `prop:branch-caterpillar-first-layer-row-preexposure-obstruction` charges the
  candidate rows required before first-batch commitment.
  `thm:branch-caterpillar-two-face-lower-handoff` gives a genuine numerical
  prefix with `C_resp=0` only through the pre-second-interaction endpoint and
  complete prefix/post vectors. The first face is committed unsettled; the
  post phase directly builds and pays the `Uhat_2` native response. Independent
  review required that scope wording repair, then rederived the lower map,
  chronology, vectors, rounds, emissions, peaks, and direct suffix cleanly.
- `volume_gated_acceleration`:
  `prop:path-correction-error-bank-potential-fails` gives the finite exact
  `q=1/5` STOP: `Phi_t^bank=delta_t+q^(-1)e_t` passes held `6->7` on `U_3` but
  first increases on held `9->10` on `U_4` while `delta_t` falls. The full run
  and eleven-vector are unchanged from Round 014. An independent dense
  rational replay recovered the complete chronology, exact fractions, gate/
  envelope facts, and vector and found no defect.

Every promoted vector uses
`(C_adj,R_adj,R_int,C_pre,C_ctl,C_rec,C_resp,M_pers,M_tmp,C_mat,C_emit)`.
The durable handoffs, audit repair, independent checks, redistribution
messages, exact validation, and next queue are in
[`Round 015`](rounds/2026-08-21-round-015.md). Round 015 is redistributed; no
unqualified shorthand may be propagated.

## Round 016 verified redistribution

- `response_preconditioned_hybrid`:
  `thm:notched-sun-multiplicity-delta-reporter` handles every verified common
  permutation of declared positive multiplicities. `L=sum_i mu_i` controls
  interactions/fragments and `H=L-min_i mu_i` controls the exact last-unseen
  scale. First occurrences emit deltas, repeats emit none, and the reporter
  stores one counter per label but no response/slack cell. Independent review
  rederived the root, envelope-only sharpness, event semantics, stream counts,
  vector, and exclusions and returned clean.
- `hybrid_aesp_locsor`:
  `lem:branch-caterpillar-anchored-lower-transport` proves all-face padded and
  anchored lower-state preservation. For every fixed `2<=q<=m`,
  `thm:branch-caterpillar-transported-lower-handoff` gives an explicit
  response-free prefix and paid `Uhat_q` response suffix. All AESP auxiliaries
  restart; candidate rows and full old-face tests remain charged. The owner's
  nested independent audit checked the algebra, finite caps, `q=m` edge,
  vectors, rounds, emissions, and response/energy scope and returned clean.
- `volume_gated_acceleration`:
  `prop:path-no-constant-coefficient-bank` derives incompatible exact
  coefficient half-lines from held `6->7` on `U_3` and held `9->10` on `U_4`
  after the face reset. It excludes every fixed `c>=0` on those two pairs only;
  the full run/vector are unchanged and all variable, block, aggregate, and
  asymptotic routes remain open. Independent exact-rational replay recovered
  the thresholds, positive gap, chronology, vector, and scope and returned
  clean.

Every promoted vector uses
`(C_adj,R_adj,R_int,C_pre,C_ctl,C_rec,C_resp,M_pers,M_tmp,C_mat,C_emit)`.
The durable handoffs, nested audit provenance, independent checks,
redistribution messages, exact validation, and next queue are in
[`Round 016`](rounds/2026-08-21-round-016.md). Round 016 is redistributed; no
unqualified shorthand may be propagated.

## Round 017 verified redistribution

- `response_preconditioned_hybrid`:
  `thm:notched-sun-amplitude-delta-reporter` replaces unit events by one finite
  declared positive occurrence schedule shared across every column and stream.
  Its exact capacity indices, tight future-mass horizons, and positive margin
  cover unseen and seen-but-unreported labels; occurrence `k_i*` is the first
  certified and exact crossing. The complete vector charges schedule
  preprocessing, fragment and logical mass, `rL` certificates, and exactly
  `rn` deltas with no response/slack state. Independent review rederived the
  envelopes, horizons, crossings, signed/nonnegative counts, vector, and
  exclusions; the checker, exhaustive state/transition audit, and 79-page build
  were clean, with no edit.
- `hybrid_aesp_locsor`:
  `lem:branch-caterpillar-implicit-lower-heap` and
  `thm:branch-caterpillar-implicit-lower-handoff` replace query-time dense lower
  sweeps by exact residual/heap maintenance and three-parent queries. The raw-
  product initialization shock `3q^2`, anchor-write shock
  `(q-1)(3q+2)/2`, fresh AESP state, candidate rows, and native response remain
  charged; `q=m` is still quadratic. Independent review checked residual/key
  semantics, locality, both product interfaces, `q=2,q=m`, both vectors,
  emissions, peaks, and the representation-only dense comparator; the checker,
  Ruff, and 65-page build were clean apart from three pre-existing overfull
  warnings, with no edit.
- `volume_gated_acceleration`:
  `prop:path-tight-pair-schur-bank` chooses the tight held-pair endpoints,
  reproduces the frozen stage-8 Schur data, stops a unit raw-linear shock charge,
  and proves the squared switch is strictly paid by the exact optimum drop. The
  tight pair maximizes the reset jump over the locally feasible rectangle, but
  the result is reset-local and supplies no global potential. Independent dense
  exact-rational replay reproduced every fraction, chronology, extremality,
  inequality, reserve identity, vector, and exclusion; the checker and 44-page
  build were clean, with no edit.

Cross-redistribution preserves three distinctions: declared local mass capacity
can maintain a certificate without settling a response; incremental within-face
diagnostics do not remove phase-entry initialization/materialization; and a
squared isolated-reset charge does not control held evolution or produce a
global potential. No Round-017 result may be composed across those boundaries
without a new charged proof.

Every promoted vector uses
`(C_adj,R_adj,R_int,C_pre,C_ctl,C_rec,C_resp,M_pers,M_tmp,C_mat,C_emit)`.
The durable handoffs, clean audits, controller adjudication, redistribution
messages, exact validation, and next queue are in
[`Round 017`](rounds/2026-08-21-round-017.md). Round 017 is redistributed; no
unqualified shorthand may be propagated.
