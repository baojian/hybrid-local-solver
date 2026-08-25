# W5 — Truncated Chebyshev with certified truncation-error control

Code: `/home/claude/work/overnight/w5_cheb/` (`cheb.py`, `run_validate.py`,
`run_amp.py`, `run_scaling.py`, `run_star_spider.py`; JSON in `out/`).
Logs: `logs/w5_*.log`. All work degree-charged via the Meter convention
(scan(u)=d_u, repeats counted in R_adj); W below = C_adj+R_adj.
Accuracy target throughout: the **certificate** ||D^{-1/2}(Qx-b)||_inf <
alpha\*eps (implies semantic err < eps; makes eps a *relative* accuracy —
note: the raw absolute semantic target err<=eps is trivially met by x=0
whenever alpha < c\*eps, which poisons naive fits). Every reported run
verified against `solve_exact`; **0 of 480 scaling runs failed
verification**.

## 0. Validation (Measured)

Untruncated Chebyshev (theta=(1+a)/2, delta=(1-a)/2, sigma=theta/delta,
u_k=1/(2 sigma - u_{k-1})) tracks the exact envelope ||e_k||_2 =
0.707\*||e_0||_2/t_k, t_k=T_k(sigma), for a=2^-4 and 2^-8 down to machine
floor (`run_validate.py`): rate lambda_cheb=(1-sqrt a)/(1+sqrt a) confirmed.

## 1. Exact error-propagation recurrence (Proved-draft)

Key simplification: **(theta I - Q)/delta = N** (the normalized adjacency),
exactly. If truncation removes g_k from the iterate at step k
(y_k <- y_k - g_k), the truncated 3-term recurrence satisfies, exactly,

    y_K - x* = (T_K(N)/t_K)(y_0 - x*)  -  SUM_{k=1..K} (t_k/t_K) U_{K-k}(N) g_k

(U_m = 2nd-kind Chebyshev; proof: v_j = t_j u_j turns the homogeneous
perturbation recurrence into v_{j+1} = 2 N v_j - v_{j-1}; verified
numerically against a real perturbed run to 2.5e-8 relative). Since
spec(N) in [-1,1], |U_m| <= m+1, and t_k/t_K <= 2 lam^{K-k}:

    ||Q y_K - b||_2 <= ||r_0||_2/t_K + SUM_k min(2(K-k+1)lam^{K-k}, Abar) ||g_k||_2,
    Abar(alpha) = max_m 2(m+1)lam^m  ~=  0.74/(2 sqrt(alpha))  (peak at m* ~ 1/(2 sqrt a)).

**Certified stopping rule (no assumption):** maintain the exact ledger
||g_k||_2 with O(1)/step running sums S_a, S_b (weights 2(K-k+1)lam^{K-k});
stop when ||r_0||_2/t_K + 2(S_a+S_b) < alpha\*eps. Valid because
||D^{-1/2}v||_inf <= ||v||_2. Truncation budget: allow ||g_k||_2 <=
0.45 alpha eps/(Abar K).

**The free measured certificate (trivial but decisive):** the iteration
computes r_k = b - Q y_k *on the already-charged scan of supp(y_k)*, so
||D^{-1/2} r_k||_inf < alpha eps is a true per-iteration certificate at
zero extra charge. Consequence: truncation needs certification only for
*termination*, never for *correctness*. This is the honest replacement for
ZSB+24's unproven residual-reduction assumption: correctness is
assumption-free; the assumption moves into the work bound only.

## 2. Amplification measurement (Measured)

Inject e_i at step k0=K-m, propagate the exact linearized recurrence
(`run_amp.py`, out/amp.json). Envelope A <= (t_{k0}/t_K)(m+1), peak at
m ~ 1/(2 sqrt a). Measured A2max = max over sites/m, fit A2max ~ C alpha^-r:

| graph | r | C | attains envelope? |
|---|---|---|---|
| star (site=center, d=300) | 0.40 | 0.37 | YES (envelope r=0.40, C=0.76 over this range) |
| decoy_hub (site=hub, d=300) | 0.39 | 0.38 | YES |
| path | 0.21 | 0.57 | no (~sqrt of envelope; spread spectral measure) |
| caterpillar | 0.23 | 0.51 | no |
| spider | 0.18 | 0.51 | no |
| grid | 0.16 | 0.46 | no |
| btree | 0.15 | 0.52 | no |

Law: worst-case amplification ~ 0.37/sqrt(alpha), attained only by
injections **at high-degree hub coordinates** with ~1/(2 sqrt a) steps
remaining; on 1D-like graphs it is ~alpha^-1/4, on trees/grids ~O(1).
Running-peak over horizons is ~1.6x endpoint, same scaling. This sets the
certified budget tau ~ eps alpha/(K\*A); the measured slack (envelope vs
1D/tree attainment) is a factor alpha^{-1/4..-1/3} of head-room the 2-norm
ledger cannot see.

## 3. End-to-end scaling W ~ alpha^-p eps^-q (Measured; 8 graphs x 5 alphas x 2 eps)

Variants: `cheb_none` (untruncated, measured-cert stop), `cheb_fixed`
(best fixed semantic tau in {eps,sqrt(a)eps,a\*eps}/4, measured-cert stop
— i.e. the *recommended certified* algorithm), `cheb_cert` (pure 2-norm
ledger, self-stopped), `cheb_restart` (K0=2/sqrt(a) cycles, exact local
residual each cycle), `cheb_meas` (adaptive tau, per-iter measured cert),
`push` (batched ACL, eps_appr=eps gives cert=alpha\*max r/d <= alpha eps
exactly; W <= 1/(alpha eps)).

| graph | cheb_fixed (p,q) | cheb_cert | cheb_restart | push | winner @a=2^-12,e=1e-3 |
|---|---|---|---|---|---|
| star_center k=1/(4eps) | **0.51, 1.00** | 0.51, 1.12 | 0.49, 1.00 | 1.01, 1.00 | cheb 33k vs push 1.42M (43x) |
| path_end | 1.01, 0.35 | 1.02, 0.31 | 0.99, 0.00 | 1.08, 0.81 | cheb (modest) |
| spider(16,100) | 1.02, 0.74 | 1.00, 0.39 | 0.95, 0.57 | 0.43, 2.01 | tie: 262k vs 303k |
| caterpillar | 0.93, 0.41 | 0.99, 0.34 | 0.96, 0.58 | 1.04, 0.88 | cheb |
| decoy_hub(60,2e4) | **0.88, 0.31** | 2.16, 0.29 (!) | 2.03, 0.07 (!) | 0.94, 0.63 | cheb_fixed 20.3k vs push 218k vs untrunc 6.76M |
| star_leaf(1e4) | 0.00, 0.00 (trivial) | 0.53, 0.16 (!) | 0.50, 0.18 (!) | 0.00, 0.15 | push W=7, cheb_meas W=1; 2-norm-cert pays 3.4M |
| grid(100x100) | 1.31, 0.74 | 1.47, 0.47 | 1.42, 0.84 | **0.52, 1.48** | push 173k vs cheb 1.36M (8x) |
| btree(d=12) | 1.42, 1.15 | 0.92, 0.43 | 1.28, 0.21 | **0.21, 1.15** | push wins big |

(rms of 2-parameter fits < 0.15 except btree/decoy where regime crossovers
— hub entry at K~dist, graph saturation — dominate; raw rows in
out/scaling.json.)

**Reading:** p~0.5, q~1 is achieved exactly where hoped — mass-dense,
low-diameter support (center star). On geometric-decay graphs the honest
law is W = Theta(K \* vol(supp_tau(x*) cap B_K)): 1D gives p~1 (K and
radius both ~ a^-1/2), q~log only; grid gives p~1.3-1.5; btree saturates
the whole tree. **Truncation does not buy a traveling wavefront: interior
coordinates are above threshold and must be rescanned every step** — the
K-fold rescan of the filled ball is the fundamental cost. Chebyshev beats
push in eps everywhere (q ~ 0.3-0.7 vs 0.8-2.0) but loses the alpha race
whenever vol(B_r) grows superlinearly (grid, btree) — push's thresholded
support is sub-volumetric, Chebyshev's is not.

## 4. Star and spider specifically (Measured)

**Center star, k=1/(4 eps)** (`run_star_spider.py`): W = K\*2k + 25
exactly (mean per-iter vol/2k in [0.97,1.00]); measured
W\*sqrt(alpha)\*eps in [1.00,1.03] over eps in {1e-2,1e-3}, alpha in
{2^-6..2^-12}. The symmetric leaves indeed forbid truncation (nothing is
small relative to tau ~ alpha eps), support = whole star, and that is
*fine*: vol=2k=1/(2eps) and K ~ 1/sqrt(a) give **W = 1/(sqrt(alpha)
eps)** on the nose — the task's arithmetic verified. Push: W\*(alpha eps)
= 0.35 constant. Crossover at all measured alphas: cheb wins 2.7x
(a=2^-6) to 22-43x (a=2^-12).

**Leaf-seeded star k=1e4, eps=1e-2:** trivial for push (W=7) and for
measured-cert Chebyshev (W=1: cert holds after 1 step since far-leaf mass
1/k < eps d) — but the 2-norm-ledger variants pay W=0.6-3.4M: the sqrt(vol)
conservatism of the provable ledger forces keeping the hub+leaves. To make
wrong-side stars genuinely hard you need eps << 1/k (then it's the center
star up to one hop).

**Spider k=16:** W(L) at a=2^-8, e=1e-3: 42k, 63k, 66.6k, 66.6k, 66.6k
for L=25..400 — local slope in L: 0.59 -> 0.0. Neither kL nor kL^2:
**W = K \* 2k\*min(L, R_tau)** with measured reach saturating at R~63 ~
ln(1/tau)/(2 sqrt a). Alpha sweep at L=100: W\*alpha = 273, 264, 260, 246,
162 — essentially constant: **W ~ k/alpha \* polylog**, the K x vol
product. No wavefront-width saving exists (interior is not truncatable).

**Decoy hub (60-path + deg-2e4 hub at mid):** untruncated 6.76M,
semantic-tau truncated 20.3k (333x saving; hub coordinate is
semantically tiny and truncated, so the 2e4 leaves are never scanned),
push 218k (truncated cheb beats push 10.7x). The 2-norm-certified ledger
FAILS here economically (p~2.1): tau_2 ~ alpha eps/(Abar K sqrt(vol))
cannot drop the hub.

## 5. Theorem and honest assumption (Proved-draft / proposed)

Proved-draft (above): the exact propagation identity, the 2-norm ledger
certificate, and the free measured certificate.

**Proposition (trees, provable along W5 lines):** on a tree that is a
union of b rays from the seed (path b=1..2, spider b=k, caterpillar
b=O(m)), the solution and all iterates decay along each ray at per-hop
ratio <= lambda_cheb (transfer-matrix root of c x = (a/2)(x_- + x_+);
branching only shrinks it), so with semantic tau = alpha eps/4 the support
stays in B_R, R <= ln(x_max/tau)/(2 sqrt a), and measured-cert truncated
Chebyshev does total work
  W = O( K \* vol(B_R) ) = O( b \* alpha^-1 \* ln^2(1/(alpha eps)) ),
improving to W = O( eps^-1 alpha^-1/2 log ) whenever vol(supp_tau(x*)) <=
C/eps saturates within O(1) hops (center star). Correctness needs no
assumption (measured certificate).

**General-graph assumption (the honest replacement for ZSB+24's):**
(A) *volume stability:* vol{v: |x*_v| >= tau sqrt(d_v)} <= C polylog \*
min(1/eps, vol(B_{R_tau})) at tau = alpha eps/4, and
(B) *iterate confinement:* supp(y_k) stays within the tau/2-superlevel set
of x* plus an O(m*)-hop margin. (B) is exactly what the literature's
residual-reduction assumption buys; it held on every zoo instance for
semantic tau (0/480 failures, spider reach 63 vs bound 110) but is what a
proof must supply per graph class. Under (A)+(B):
W = O(K \* vol(S_tau)) with the measured certificate exact.

## Failure map and next target

- 2-norm-certified truncation fails economically on high-degree decoys
  (decoy_hub, star_leaf): provable tau shrinks by sqrt(vol). Fixed by the
  measured certificate + semantic tau (assumption moves to the work bound).
- Fundamental failure axis: K-fold rescan of essential high-degree hubs
  (center of a needed star: R_adj = K d_hub) and of volumetric balls
  (grid p~1.3, btree p~1.4 — push beats Chebyshev outright there).
- NEXT: (i) hub response/Schur compression — close out deg>=D vertices
  with a one-shot leaf-bundle response (C_resp), removing the K\*d_hub
  rescan; predicted to restore p~0.5 on star_leaf at eps<<1/k and on
  decoy variants with essential hubs. (ii) push-then-Chebyshev hybrid:
  push to localize the eps-support, Chebyshev restricted to it (targets
  grid/btree where push's sub-volumetric support wins). (iii) prove (B)
  for bounded-degree trees via the ray transfer matrix.
