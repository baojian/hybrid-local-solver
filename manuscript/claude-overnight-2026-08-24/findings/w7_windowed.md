# W7 — Windowed net accelerated exponent for the safeguarded AESP-CD recurrence

**VERDICT: POSITIVE for Route B (validated reconstruction + Measured).** The windowed
form of the net-packing target `J_T^fin <= (1-c) qT + B` holds with large margin on every
known adversarial family and on every perturbation tried, including a **new, strictly worse
sustained-inflation family class** found by the adversarial sweep (tuned-rho path-boundary
cycles, windowed slope up to **0.145**) — still 7x below the counterexample threshold 1.
Measured window slopes are q-stable (plateau ~0.10–0.15 for the worst tuned families,
q in [1/64, 1/8]). No counterexample direction found. The same lagged unsplit `q^{-1}Q`
bank that provably fails one-step contraction on K_2 **does contract per window** with
stable `c_win ~ 0.62`. Recommendation: pursue the windowed proof.

Code: `w7_windowed/{engine,fengine,validate,windowed,search,search2}.py`;
data: `w7_windowed/{windowed_results,search_results,search2_results,search3_results,search4_results}.json`,
`p4_exact_520.json`, `p6_exact_250.json`. Compute ~6 min.

## 1. Reconstruction and validation status: VALIDATED (5/5 exact checks)

Reconstructed recurrence (exact shifted solves; hat coords keep all arithmetic rational):
`x_{-1}=x_0=0`; `d_t=x_t-x_{t-1}`; trial `a_t=x_t+beta_A d_t`;
`Delta_t=(1/alpha)||D^{-1/2}[c_rho-Qa_t]_-||_inf` on `supp(a_t)`; retraction
`rhat_i=min(beta_A dhat_i, Delta_t)`, `ell_t=a_t-r_t` (= coordinatewise
`max(x_t, [a_t-Delta_t D^{1/2}1]_+)`, a lower certificate); `x_{t+1}` = exact obstacle
solve of `min F_rho(z)+(kappa_A/2)||z-ell_t||^2`. Diagnostics exactly per sections 14/15:
`z_t^fin`, `Dfrak_t^fin` (expanded, cancellation-free), Moreau-envelope `Phi_t^fin` (extra
exact prox solve per stage), `gamma_t^fin`, `J_T^fin = sum log max(1,gamma_t)`,
`E_t^Q`, bank `Psi_t^A = Phi_t + (A/q)E^Q_{t-1}` with `A_*=6929307/98509850`.

All five published exact facts reproduce (`validate.py`, all Fractions, bit-exact):

1. **K_8 reachable pulse** (q=1/10, alpha=1/101, rho=1/112, given seed): x*, xhat_1,
   xhat_2 exact vector match; word `N N P F N N...`; `Delta_2=191403/1253344400`;
   **`gamma_2^fin = 57072309867/51440146040` and
   `gamma_3^fin = 192036347475007/168765931042095` exact Fraction match**;
   `D_2^fin/(alpha^2 Delta_2^2) = 48663286609745269/139594225` exact; `J = 0.2331 < 2log2`.
2. **K_2 family** (n=100): `x*=(7/16)(1,1)`; word all-N (no corrections ever);
   `e_t=(1+tq)(1-q)^t e_0`, `Phi_t`, `E_t^Q` closed forms exact for all t tested; the
   `Psi_3^A/Psi_2^A` identity of Round 027 exact; `0 <= 1-Psi_3/Psi_2 = 1.577e-3 <= (4+2/A_*)q^2`.
3. **K_8 small-q family** (q=1/100): seed positive/normalized, `xhat*=e^(0)/112` exact;
   word `N N F`; `D_2^fin = 1.71e-4 > 28q*7/112^2`; `E_1^Q-E_2^Q = 3.73e-10 < 197q^4*7/112^2`;
   ratio `4.60e5 > 28/(197q^3) = 1.42e5`; `gamma_2 = 1.0196 > 1`.
4. **P_3 momentum expansion** (alpha=1/100, rho=1/1000): `D_3 = 0.059263 in (0.0592, 0.0593)` (float; q irrational).
5. **P_4 neutral** (q=1/8, alpha=1/65, rho=7/40, endpoint seed): support fixed from stage
   **7** (exact match); last inflation event at stage **498** ("through stage ~498");
   **`J_500 = 1.023646`** vs project's "I_500 ~ 1.0236" — matches all stated digits
   (so I_T is the cumulative log-inflation sum). Bonus: asymptotic per-event
   gamma -> 1.023592 (same digits by coincidence).

Float engine (error-coordinate mode with rescaling; unlimited horizons) cross-checks the
exact engine: max |gamma| deviation 2e-13 over 520 P_4 stages; on the worst search family
(below) exact-vs-float over 200 stages: identical correction word, identical event count,
J agrees to 5 decimals (1.13924).

## 2. Windowed exponent test (w = ceil(1/q), horizons T = 20/q, up to 250/q on P_4)

| family | q | corrections | J_T at T=20/q | tail slope J vs qT | max per-window infl/(qw), j>=1 | per-window dlogPhi |
|---|---|---|---|---|---|---|
| K_2, n=100..800 | 1/100..1/800 | **0** (word all-N) | 0 | **0** | 0 | 1.1->1.9 (->2) |
| K_8-q | 1/100 | 1 (stage-2 F only) | 0.01939 (= log gamma_2 ~ 1.94q) | 0 | 0 (window 0 only: 0.019) | 1.06->1.89 |
| K_8-q | 1/200 | 1 | 0.00985 (~1.97q) | 0 | 0 | same |
| K_8-q | 1/400 | 1 | 0.00496 (~1.98q) | 0 | 0 | same |
| P_4 neutral | 1/8 | sustained, period-11 forever | J grows linearly | **0.01695** (exact, T=520) | 0.0246 | 2.4-6.4 |

- K_2's one-step STOP is a *bank* failure, not inflation: J is identically 0; global decay
  is accelerated (per-window log Phi decrease -> 2 = 2qw).
- K_8's pulse is a one-window transient: per-pulse cost ~2q nats -> vanishes per window.
- P_4 realizes the "infinite inflation cone": inflation events **never stop** (period-11
  `...N N N N N N P F N N F...` cycle, per-event gamma -> 1.023592, checked to T=2000),
  so J_T is unbounded — but linear with slope 0.017 << 1. Windowed form holds with
  c ~ 0.98, B ~ 0.
- Windowed bank (the object that failed one-step): on K_2, `Psi^A` with A=A_* has one-step
  loss O(q^2) (fails c*q) but per-window log-decrease **0.68/0.65/0.63/0.62** at
  n=100/200/400/800 for the window starting at the failing transition (1.43 for later
  windows) — a stable windowed contraction constant c_win ~ 0.62 where the stagewise
  version provably fails.

## 3. Worse-family search (float sweeps on the validated engine; worst candidates re-run exact)

Transient everywhere (J bounded, slope 0): K_16/K_32 v-pulse analogues (cv=12..100:
<=3 events, all by stage 7, J <= 0.13); chains of 2-4 K_8s (single-edge coupling, any seed
split): **zero** events; barbell K8-P4-K8: zero; stars (center/leaf seed): <=3 events;
dense/two-end-seeded paths: <=1 event. Repeated K_8 pulses could not be provoked — the
high band dies too fast (sqrt(7/11) per stage) and coupling does not re-seed it.

**New sustained family class (the real adversarial frontier): endpoint-seeded paths P_n
with rho tuned near a support breakpoint** (last support coordinate near the kink).
These sustain P/F correction cycles forever with per-event gamma up to 1.42.
Best (adversarially tuned over n <= 48, rho, seed) windowed slope S(q):

| q | 1/8 | 1/12 | 1/16 | 1/24 | 1/32 | 1/64 |
|---|---|---|---|---|---|---|
| S(q) | 0.088 | 0.104 | 0.110 | 0.102 | **0.145** | 0.125 |

(worst cell: q=1/32, n=24, rho=0.01603, 109 events in T=4800, maxwin 0.61; largest
single-window ratio seen anywhere: 0.76 — a one-window spike, absorbable in B; actual
per-window log Phi decay 2.2-2.5 nats >> qw=1 throughout). S(q) plateaus at 0.10-0.15
with no drift toward 1. Spider graphs (k legs = k support boundaries) **anti-amplify**:
slope 0.008 (k=3) -> 0.002 (k=10) — boundaries dilute rather than multiply.

Startup intercepts B_est: K_2: 0; K_8-q: J_infty ~ 2q; P_4: -0.04; tuned paths: |B| < 1.

## 4. Caveats

- Model-reconstruction, exact shifted solves (xi_t = 0): the finite-inner residual term is
  not exercised; this isolates exactly the correction-inflation object J_T^fin of
  eq:aesp-cd-actual-finite-net-packing. Validation passed on every family with published
  constants, so labeled **validated reconstruction**; search families are Measured on it.
- Search coverage: paths, spiders, stars, complete graphs, K_8 chains/barbells, n <= 64,
  q in [1/64, 1/8], LS tail slopes on T = 120-250/q. Not exhaustive; no family class
  showed slope growth toward 1 under tuning.

## 5. Meaning for Route B and next target

The windowed exponent **holds on all known and all newly found adversarial families with
q-stable margin c >= 0.85** (and the windowed unsplit bank itself contracts at c_win ~ 0.62
on the K_2 killer). This is strong Measured evidence that the Route-B target is TRUE and
the obstacle is proof technique. Next: (i) attempt a per-window (w = Theta(1/q)) telescoped
version of the lagged `q^{-1}Q` reserve — pay the K_8 pulse into B (< 2log2), prove
window contraction on fixed faces; (ii) add the tuned-rho path family (P_24, q=1/32,
rho=0.01603) to the audit battery as the sharpest sustained-inflation stress test — any
windowed lemma must absorb per-event gamma ~ 1.4 recurring every ~q^{-1}/2 stages;
(iii) the observed pairing of harmful events with interleaved gamma < 1 stages (e.g. 0.064)
suggests a two-sided ledger (credit helpful corrections) as the nonlinear transfer.
