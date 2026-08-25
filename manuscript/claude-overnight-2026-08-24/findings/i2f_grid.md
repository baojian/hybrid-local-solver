# I2-F — Are 2D grids a genuine obstruction for local PPR solvers?

Code: `/home/claude/work/overnight/i2f_grid/` (`gridlib.py`, `validate.py`,
`run_map.py`, `run_ext.py`, `fit.py`).  Data: `out/map.json`, `out/map.csv`,
`out/ext.json`; logs `out/run_map.log`, `out/run_ext.log`, `out/validate.log`.
Conventions as W1–W8: `Q = (1+a)/2 I − (1−a)/2 D^{-1/2}AD^{-1/2}`,
`b = a D^{-1/2}e_v`, semantic err `= ||D^{-1/2}(x−x*)||_inf`, certificate
`||D^{-1/2}(Qx−b)||_inf < a·eps ⇒ err < eps`.  Meter: scans charge `d_u`
(first `C_adj`, repeats `R_adj`); solver/transfer ops `C_resp`;
materialisation `C_mat`; coordinate writes `C_rec`; `W = Σ`.
Total compute ≈ 35 min.

## VERDICT

**Grids are NOT an obstruction — they are an obstruction *for one-hop,
polynomial and elimination mechanisms specifically*, and local multigrid
breaks it.**  (Measured.)  On `grid(w,w)` with a centre seed,
`W/vol(S_eps) ~ C·alpha^{-s}` at fixed eps:

| mechanism | s @ eps=1e-6 | s @ eps=1e-8 | raw (p_alpha, q_eps) |
|---|---|---|---|
| **output** `vol(S_eps)` | — | — | **(0.77, 0.29)** |
| push (one-hop) | 0.85 | — (skipped, too costly) | (1.65, 0.46) |
| trunc. Chebyshev (polynomial) | 0.75 | 0.69 | (1.50, 0.23) |
| push→Chebyshev (best split) | 0.81 | 0.76 | (1.56, 0.25) |
| ND-EES (elimination) | 0.69 | 0.61 | (1.45, 0.33) |
| **local multigrid, self-certified** | **0.20** | **0.12** | **(0.95, 0.27)** |
| **local multigrid, oracle-stopped** | **−0.06** | **0.06** | **(0.78, 0.36)** |

Oracle-stopped local MG reproduces the *output's own* exponents
`(0.77, 0.29)` to within noise: it is **output-linear and alpha-free**, at a
constant of **121–191 charged units per unit of `vol(S_eps)`** (60–87 per
unit of `vol(Omega)`), with a V-cycle count `3–6 ≈ log(1/eps)/2.6`
independent of alpha.  Every competing mechanism pays a *multiplicative*
`alpha^{-1/2}` (Chebyshev, elimination) or `alpha^{-1}` (push) over output.
Correctness verified against `spsolve` on **every** run (17 2-D cells × 7
variants + 1 deep cell + 6 3-D cells; max err/eps = 0.85 push, 0.26 MG,
0.21 Chebyshev, 0.17 ND; **0 failures**).

## 1. Parameter map: the classic target is meaningless on grids (Proved-draft)

**Structural identity.** On the interior of `Z^D` every degree is `2D`, so
`D^{-1/2}AD^{-1/2} = A/(2D) = I − L/(2D)` and therefore, *exactly*,

    Q = alpha·I + beta·L ,        beta = (1−alpha)/(4D)          (D=2: beta=(1−a)/8)

— a **positively shifted lattice Laplacian**; alpha is a mass term.
(Verified to 0 / 2.8e-17 in `validate.py` for D=2,3.)  A region `Omega`
strictly inside the grid with zero data outside has
`Q[Omega,Omega] = alpha I + beta L^Dir`, i.e. the global-restricted local
problem *is* a textbook shifted-Poisson problem.  Decay constant

    kappa_D = sqrt(alpha/beta) = sqrt(4D·alpha/(1−alpha)) ≈ 2 sqrt(D·alpha)

(D=1 reproduces the project's `lambda = (1−√a)/(1+√a) = e^{−2√a}`; **in 2D the
per-hop decay is `e^{−2√(2a)}`, faster than the 1D kernel by √2**).

**Exact kernel and the eps-support.**  In 2D `G(r) = (2πbeta)^{-1}K_0(kappa r)`
so `pi_v/d_v = (alpha/pi)·K_0(kappa_2 r)`, and the semantic support radius is
`R(a,eps) = z*/kappa_2` with `K_0(z*) = pi·eps/alpha`.  Measured L∞ radii vs
this prediction (exact solves): `(2^-8,1e-6) 36 vs 36.3`; `(2^-10,1e-6) 57 vs
57.7`; `(2^-4,1e-8) 18 vs 19.0`; `(2^-12,1e-4) 7 vs 7.5`. It is exact in both
the near-field (log) and far-field (exponential) branches.

**(i) Trivialisation boundary.**  `max_v pi_v/d_v = (alpha/pi)[ln(2/kappa_2) −
gamma] ≈ (alpha/2pi)ln(1/(2alpha))`; above it `x = 0` is already eps-accurate.
Predicted `eps*(2^-10) = 7.9e-4`; measured `|S| = 1` at `(2^-10, 1e-3)` and
`|S| = 0` at `(2^-12, 1e-3)`.  **The whole non-trivial grid regime is
`eps = O(alpha·log(1/alpha))`** — W8's anomaly A3 with the constant pinned.

**(ii) Output size.**  For `eps ≪ alpha`, `z* ≈ ln(alpha/(pi·eps))`, hence

    vol(S_eps) ≈ 4·pi·R^2 = (pi/(2·alpha))·ln^2(alpha/(pi·eps))
              = Theta( log^2(1/eps) / alpha )         — POLYLOG in 1/eps.

Measured (eps=1e-6, alpha 2^-4…2^-12): 1 956 / 5 924 / 16 468 / 42 132 /
96 388; formula at 2^-8 gives 20 470 vs 16 468 (within 25 %).

**(iii) Comparison with the classic target `T = 1/(√alpha·eps)`.**

    T / vol(S_eps) ≈ (2/pi)·sqrt(alpha) / ( eps·ln^2(alpha/(pi·eps)) ).

*Does the output ever exceed T (making T vacuous)?*  That needs
`eps·ln^2(·) > (2/pi)√alpha`, but the non-trivial band caps
`eps ≤ (alpha/2pi)ln(1/2alpha)`, where the left side is `O(alpha·log^3)` and
the right side is `Theta(√alpha)` — **the band is empty for every
alpha < 1.  On 2D grids the output NEVER exceeds the classic target.**
(Same computation in 3D: the two branches `eps > 0.55 alpha^{3/2}` and
`eps < 0.55 alpha^{3/2}` both fail the inequality by a shrinking margin;
measured 3-D `T/vol` ∈ [33, 1398] — still > 1, but 10–70× smaller than the
2-D ratio at comparable `(alpha,eps)`.)

*So T is not vacuous — it is **vacuously loose**.*  Measured `T/vol(S_eps)`
over the sweep: **22 … 91 491**, monotonically increasing as eps ↓ (at
alpha=2^-4: 2 045 at eps=1e-6 → 91 491 at eps=1e-8).  `1/(alpha·eps)/vol`
reaches **7.2e5**.  The reason is structural: **T is linear in `1/eps`
where the grid output is polylogarithmic in `1/eps`.**  `1/(√a·eps)` is an
output-size proxy calibrated for families whose eps-support grows like
`1/eps` (stars, spiders — W4 measured exactly `vol(S) = Theta(1/(√a·eps))`
there); on a lattice that calibration fails by a factor that diverges
polynomially in `1/eps`.

**⇒ THE RIGHT GRID TARGET.**  Not `O~(1/(√alpha·eps))` — which is neither
achievable-relevant nor informative — but

    W = O( vol(S_eps) · polylog(1/eps) )    with ALPHA-FREE constants,

i.e. **output-linear, alpha-free**.  The rest of this note answers *that*
question.  (Note this also reframes W8's "grid ridge": the grid's 4.3×
prize over `T` understates the real gap by 3–4 orders of magnitude,
because `T` itself is 10^2–10^5 above output there.)

## 2. Candidates (all charged, all self-certified unless stated)

Common region machinery: a centred square `Omega` of odd side `m` from the
ladder `{q·2^k − 1 : q ∈ 1,3,5}` (ratio ≈ 1.33, each coarsenable by
`m → (m−1)/2` to a ≤16-cell dense level), grown until the **measured**
certificate `max_{Omega ∪ ∂Omega} |r_v|/√d_v < alpha·eps` holds.  The
stencil certificate was verified equal to the global `Model.cert_resid` to
1e-9 relative.  **All failed region attempts are charged.**

1. **MG** — local geometric multigrid: red-black GS (`nu1=2, nu2=1`),
   full-weighting restriction, bilinear prolongation, rediscretised coarse
   operators `A_l = alpha I + beta·L_l/4^l`, dense LU at the coarsest level
   (factor charged `(2/3)n^3` once, `2n^2` per solve).  Charging: level-0
   sweeps and the certificate pass charge `d_u` per vertex (`C_adj/R_adj`);
   **every** coarse relaxation (`5·n_l`), restriction (`9·n_c`),
   prolongation (`3·n_f`) and coarse solve charges `C_resp`; every level
   array charges `C_mat`.  Measured split: `C_adj+R_adj ≈ 57 %`,
   `C_resp ≈ 38 %`, `C_mat ≈ 1–4 %` — the multilevel machinery is a
   *minority* of the bill but is fully paid.
   *Early region rejection* (honest and free): the boundary residual is a
   floor no further cycling can lower, so once `ring_cert ≥ alpha·eps` after
   2 cycles the region is provably too small and is abandoned at once.
2. **ND-EES** — same region, exact solve of `Q[Omega,Omega]` by sparse LU
   with a fill-reducing (nested-dissection-like `MMD_AT_PLUS_A`) ordering;
   charges `Σ_j nnz(L[:,j])^2` factor flops (`C_resp`), `nnz(L)+nnz(U)`
   fill (`C_mat`), `2·nnz` solves, plus the exploration scans.
3. **PUSH** — literal lazy FIFO ACL push at threshold eps (the bit-identical
   C kernel from W8).  Self-certifying by the one-sided ACL bound.
4. **CHEB** — W5's truncated Chebyshev with the free measured certificate.
5. **PUSHCHEB** — push to a warm tolerance `eps_w ∈ {1e-2…1e-5}`, then
   Chebyshev warm-started; best split reported (push work included).
6. Oracle brackets for MG and ND (stop at true semantic error ≤ eps) to
   separate mechanism cost from the cost of self-certification.

**Safety of under-exploration.**  When the region ladder runs into the host
grid's boundary the algorithm returns `status = "maxed"` and *refuses to
certify*; the semantic error may then exceed eps (demonstrated in
`validate.py`: `alpha=2^-8, eps=1e-6` on a deliberately undersized
`grid(101,101)` gives `err/eps = 3.94` with `cert/(alpha·eps) = 77.8`,
i.e. the certificate correctly reports failure).  In the reported sweep the
grid was always sized large enough: **all 17 cells returned `cert` for MG,
ND and Chebyshev**, and every certified run was asserted against the exact
solve.

## 3. Charged work — `W / vol(S_eps)` (Measured)

Non-degenerate cells only (`|S| ≥ 250`, `eps ≤ alpha/25`); full 17-cell table
in `out/map.csv`, raw numbers in `out/map.json`.

| alpha | eps | vol(S) | push | cheb | hyb | ND-EES | **MG** | MG-oracle |
|---|---|---|---|---|---|---|---|---|
| 2^-6 | 1e-4 | 1 172 | 81.8 | 183.3 | 180.4 | 437.0 | **145.9** | 71.9 |
| 2^-8 | 1e-4 | 2 068 | 229.4 | 701.3 | 599.0 | 2 265.7 | **344.8** | 89.9 |
| 2^-4 | 1e-6 | 1 956 | 53.8 | 44.6 | 46.0 | 261.8 | **104.2** | 157.2 |
| 2^-6 | 1e-6 | 5 924 | 179.8 | 158.7 | 126.1 | 790.9 | **166.4** | 136.9 |
| 2^-8 | 1e-6 | 16 468 | 583.4 | 394.6 | 354.4 | 2 575.9 | **245.1** | 130.4 |
| 2^-10 | 1e-6 | 42 132 | 1 831.7 | 1 043.5 | 1 379.3 | 4 207.0 | **232.5** | 120.8 |
| 2^-12 | 1e-6 | 96 388 | — | 4 350.2 | — | — | **410.2** | — |
| 2^-4 | 1e-8 | 4 372 | 83.4 | 47.9 | 45.6 | 483.2 | **134.0** | 134.3 |
| 2^-6 | 1e-8 | 14 596 | — | 126.5 | 125.8 | 696.5 | **186.4** | 182.1 |
| 2^-8 | 1e-8 | 46 340 | — | 327.9 | 336.0 | 1 964.0 | **158.1** | 144.7 |
| 2^-10 | 1e-8 | 143 060 | — | 831.7 | 1 079.9 | 5 844.4 | **247.3** | 190.8 |

(`—` = push skipped above a 1.5e9-charge cap, or grid too large for the
deep cell's full contender set; `2^-12, 1e-6` is `w = 773`, `n = 597 529`.)

**Fitted alpha-exponents of `W/vol(S)`** (`W/vol ~ C·alpha^{-s}`), §C of
`fit.py`:

| eps | push | cheb | hyb | ND | **MG** | **MG-oracle** |
|---|---|---|---|---|---|---|
| 1e-6 (α 2^-4…2^-10) | 0.85 | 0.75 | 0.81 | 0.69 | **0.20** | **−0.06** |
| 1e-6 (α 2^-4…2^-12) | — | 0.83 | — | — | **0.25** | — |
| 1e-8 (α 2^-4…2^-10) | — | 0.69 | 0.76 | 0.61 | **0.12** | **0.06** |

Two-parameter fits over the 10 non-degenerate cells, `W ~ alpha^{-p} eps^{-q}`:
output `(0.77, 0.29)`; push `(1.65, 0.46)`; cheb `(1.50, 0.23)`; hyb
`(1.56, 0.25)`; ND `(1.45, 0.33)`; **MG `(0.95, 0.27)`; MG-oracle
`(0.78, 0.36)`** (rms 0.16–0.42).

### Reading the laws

* **Chebyshev is `K × vol` with `K = Theta(log(1/eps)/√alpha)` — confirmed
  directly.**  Measured iteration counts at eps=1e-6, alpha 2^-4…2^-10:
  36, 99, 219, 461 (slope 0.55 in `1/alpha`; ratio to
  `ln(1/eps)/(2√(2·alpha))` = 1.8–3.0, drifting only through truncation
  slack).  `p_cheb − p_out = 1.50 − 0.77 = 0.73 ≈ 1/2 + logs`.
* **ND elimination pays the SAME overhead as Chebyshev.**  Nested
  dissection on an `R×R` region is `Theta(R^3)` flops = `R × vol`, and
  `R = Theta(log(1/eps)/√alpha)`, so the overhead factor is again
  `~alpha^{-1/2}`: measured `p_nd − p_out = 0.68`.  Elimination is *not*
  worse than polynomial in exponent — it is worse only in constant (ND is
  3–24× above MG in absolute charge, and its `C_mat` fill is real).
  This closes W4's open item: the treewidth-aware kernel does rescue grids
  from `m^3`-dense catastrophe (W4's ratio 1.2e5 vs push), but only to the
  same `alpha^{-1/2}·vol` line that Chebyshev already sits on.
* **The push→Chebyshev hybrid cannot beat the polynomial floor.**  Best
  split found is `eps_w` ∈ {1e-2…1e-4}; the measured exponent is *identical*
  to plain Chebyshev (`1.56` vs `1.50`), and the largest win anywhere is
  1.26× (alpha=2^-6, eps=1e-6).  Warm-starting removes a `log` from `K`, not
  the `alpha^{-1/2}`: **any polynomial (Krylov) method needs
  `Omega(1/√alpha)` matvecs on the region because `sqrt(cond(Q_Omega)) =
  Theta(1/√alpha)`, and each matvec costs `vol(Omega)`.**
* **Push is `Theta(1/alpha)` sweeps of the region**, `p_push − p_out = 0.88`.
  Its `1/(alpha·eps)` worst case is far from tight here (measured push uses
  0.6–7.5 % of it), but its *shape* is the diffusive mixing time of the
  region, and it is the only contender whose exponent in eps (0.46) is
  visibly worse than output (0.29).
* **MG is `Theta(log(1/eps))` V-cycles of the region, alpha-free.**
  Measured V-cycle residual reduction factor: **0.024–0.066 across
  alpha ∈ {2^-4, 2^-8, 2^-12}** (rate degrades only from the shift
  vanishing, i.e. toward pure Poisson).  Measured cycle counts:
  1–2 (eps=1e-3/1e-4), 3–4 (1e-6), 4–6 (1e-8) — **a function of eps only**.
  Per-cycle cost ≈ 8.3·vol(Omega) (4 level-0 sweeps + 1 certificate pass at
  `d_u = 4` each, plus ≈ 3.3·vol of charged coarse work).

### MG cost decomposition (§E of `fit.py`)

`W_MG = [region inflation vol(Omega)/vol(S)] × [region search] × [cycles] ×
[≈8.3 per vol unit]`.  At eps=1e-6/1e-8 the inflation is **2.0–3.9** and
`W/vol(Omega)` is **53–87**, essentially flat in alpha.  The only residual
alpha-growth in the *certified* variant is the region inflation, and it is
fully explained in §4.

## 4. The certification tax (the one honest caveat)

For a region-restricted solve the standard certificate is loose by exactly
`Theta(1/alpha)` on a lattice, and this is *provable in closed form here*
(Proved-draft): for `v ∈ ∂Omega`, `r_v = beta·x_∂` (one interior neighbour),
so `cert = beta·pi_∂/(2D)`, while the true error is `err ≈ pi_∂/(2D)`
(W8's maximum principle, `err = max_{v∉Omega} pi_v/d_v`).  Hence

    err / (cert/alpha) = 4D·alpha/(1−alpha)      (= 8·alpha in 2D),

i.e. the certificate over-certifies by `1/(8 alpha)`, forcing an **extra
certified radius `Delta R = ln(1/(8 alpha))/kappa_2`** — the same order as
`R` itself.  Measured: at `(2^-10, 1e-6)` `R_sem = 57`, certified region
half-width 95 (predicted `Delta R = 55`); at `(2^-12, 1e-6)` `R_sem = 87`,
certified 191 (predicted `Delta R = 141`).  Squared, that is the 2.0–6.1×
region inflation, and it is **exactly the gap between MG-certified
(s = 0.20/0.25) and MG-oracle (s = −0.06)**.

This tax is paid by ND too (identically), and *not* by push (whose one-sided
ACL bound is exact).  It is a certificate artefact, not a mechanism cost: the
true amplification from a boundary residual to the outside error on `Z^2` is
`Theta(1)` (the closed form above), so a lattice-aware certificate would
recover the fully alpha-free law.  **Open (and cheap): a certificate of the
form `err ≤ (4D/(1−alpha))·cert` for regions whose complement is a lattice —
provable from the same maximum principle — would make certified MG
output-linear and alpha-free outright.**

## 5. Winner map (self-certified bracket)

| alpha \ eps | 1e-3 | 1e-4 | 1e-6 | 1e-8 |
|---|---|---|---|---|
| 2^-4 | push | push | cheb | hyb |
| 2^-6 | push | push | hyb (MG 1.05×) | hyb (MG 1.47×) |
| 2^-8 | push | push | **MG** | **MG** |
| 2^-10 | (trivial) | push | **MG** | **MG** |
| 2^-12 | (trivial) | push | **MG** (10.6× cheb) | — |

MG's speedup over the previous best incumbent: 1.6× (2^-8, 1e-6), 4.4×
(2^-10, 1e-6), **10.6× (2^-12, 1e-6)**, 3.0× (2^-10, 1e-8) — and the ratio
grows like `alpha^{-1/2}` with no visible ceiling.  Push still wins the
`eps ≳ alpha/25` corner, but that corner is precisely where the grid is
degenerating toward triviality (`|S| ≤ 600`, `R ≤ 13`): there is essentially
no multiscale structure for a V-cycle to exploit and the region-search
granularity dominates.

## 6. 3D sanity (Measured, partial — 6 cells)

`grid3(w,w,w)`, centre seed, `w ≤ 43` (`n ≤ 79 507`).  All checks passed.

| alpha | eps | vol(S) | R | T/vol | push | cheb | MG | ND |
|---|---|---|---|---|---|---|---|---|
| 2^-4 | 1e-4 | 1 218 | 3 | 32.8 | 19.9× | 72.9× | 151× | 4 279× |
| 2^-4 | 1e-5 | 4 974 | 6 | 80.4 | 25.7× | 71.8× | 132× | 9 384× |
| 2^-4 | 1e-6 | 13 086 | 8 | 305.7 | 35.8× | 50.6× | 163× | 69 757× |
| 2^-4 | 1e-7 | 28 614 | 10 | 1 397.9 | 45.8× | 48.6× | 93× | 31 902× |
| 2^-6 | 1e-4 | 1 686 | 4 | 47.5 | 56.5× | 297× | 300× | 27 685× |
| 2^-6 | 1e-5 | 12 654 | 8 | 63.2 | 72.5× | 235× | **168×** | 72 139× |

Three dimension-dependent facts.  (a) The classic target is *closer* to
output in 3D (`T/vol` 33–1 398 vs 22–91 491 in 2D), consistent with
`T/vol ~ √alpha/(eps·ln^D)`: the higher the dimension, the better `1/(√a·eps)`
approximates output size — it becomes exact in the `1/eps`-support limit.
(b) **ND elimination is catastrophic in 3D** (`R^{(3D-3)} = R^6` fill-in ⇒
`10^4–7·10^4 ×` output) — the D=3 separator cost `n^2` is a genuine wall,
confirming that the elimination line is dimension-fatal while the
polynomial and multilevel lines are not.  (c) MG's crossover has simply not
arrived at these sizes: `n ≤ 8e4` in 3D caps `R ≤ 10`, where
`K_cheb ≈ 30–40` is already smaller than MG's per-vol constant; the first
cell with `R = 8` and `alpha = 2^-6` already flips (MG 168× vs cheb 235×),
matching the 2-D pattern that MG wins once `K_cheb ≳ 100`, i.e.
`R ≳ 40`.  Reaching that in 3D needs `n ~ 10^6` — untested (Open).

## 7. What grids say about the open problem

1. **The classic target is the wrong yardstick on lattices** (Proved-draft
   §1, Measured §1).  It is 22–9.1e4× above the output over the tested
   sweep and diverges like `√alpha/(eps·log^2)`.  Any claim of the form
   "achieves `O~(1/(√alpha·eps))` on grids" is vacuous; conversely W8's
   measured grid ridge (4.3× prize) *understates* the real headroom by
   2–5 orders of magnitude, because it measures against `T`, not output.
2. **A clean mechanism separation, all under one meter** (Measured §3):

   | mechanism class | overhead over output on grids | reason |
   |---|---|---|
   | one-hop / monotone push | `Theta(1/alpha)` | region mixing time |
   | polynomial (Chebyshev, Krylov, warm-started) | `Theta(1/√alpha)` | `√cond(Q_Omega) = Theta(1/√alpha)` matvecs, each `vol` |
   | elimination (nested dissection, WY, EES) | `Theta(1/√alpha)` in 2D; `Theta(R^{4})` in 3D | `R^3 = R·vol` separator flops |
   | **multilevel response (V-cycle)** | **`Theta(log(1/eps))`, alpha-FREE** | error is resolved scale by scale; the shift only helps |

   The first three are all "one pass over the region per unit of radius".
   Multigrid is the only mechanism in the campaign's arsenal whose pass
   count is set by `log(1/eps)` rather than by the region's radius.
3. **Multigrid IS a persistent multilevel response, and it is charged as
   one** (response-track framing).  The hierarchy `{A_l}` is a family of
   coarse response operators built once per region; a V-cycle is one
   query against that response; the transfers are the response's
   restriction/prolongation maps.  Under the campaign's meter, that
   response costs 38 % of the total and buys the `alpha^{-1/2}` back.  This
   is the first mechanism in the campaign whose *charged* work matches the
   output law on a family where push, Chebyshev and elimination all fail —
   and it does so **without any assumption** (correctness is the measured
   certificate; only termination speed depends on the V-cycle rate, which
   was measured at 0.024–0.066 uniformly in alpha).
4. **Precise statement of the residual gap.**  Certified local MG is
   output-linear up to (i) `Theta(log(1/eps))` cycles, (ii) a region
   inflation `(1 + Delta R/R)^2` with `Delta R = ln(1/(8 alpha))/kappa`
   caused solely by the `1/alpha`-loose restricted-solve certificate, and
   (iii) a ≤1.8× ladder/search constant.  (ii) is removable by a
   lattice-aware certificate (§4); (i) is intrinsic to any residual-driven
   method; (iii) shrinks with a finer ladder.
5. **What is genuinely open.**  Geometric multigrid used the lattice
   *structure* (a rediscretised coarse operator, a bilinear prolongation).
   The claim that survives to general graphs is therefore not proved here.
   The right successor is **algebraic multigrid / graph coarsening as a
   charged local response**: build the coarse levels from the explored
   region only, charge the aggregation and the Galerkin triple product,
   and ask whether the alpha-free cycle count survives on expanders,
   spiders and the closed 3-regular family that broke EES.

## 8. Next falsifiable target

**"Local ALGEBRAIC multigrid — smoothed-aggregation levels built on the
explored region only, with aggregation, Galerkin `RAP` assembly, transfers
and all coarse relaxations charged — achieves `W = O(vol(S_eps)·log(1/eps))`
with alpha-free constants on every family in the campaign zoo, including the
closed 3-regular `double_cycle` and `rand_reg(n,3)` regions where EES pays
`m^3`; and its V-cycle rate stays below 0.3 uniformly in alpha."**

Secondary, cheap and decisive:
* **Lattice-aware certificate** (`err ≤ (4D/(1−alpha))·cert` for lattice
  complements, from the §4 maximum principle) — would move certified MG's
  measured `s` from 0.20 to ≈ 0, closing the last alpha-dependence.
* **3D crossover**: one `n ≈ 10^6` 3-D cell at `alpha = 2^-8, eps = 1e-7`
  (`R ≈ 40`) to confirm MG overtakes Chebyshev at the same `K ≈ 100` mark
  as in 2D.
* **W8 grid-ridge restatement**: recompute the grid prize against
  `vol(S_eps)` instead of `1/(√alpha·eps)` — the "practical prize" there is
  10^2–10^5, not 4.3×.
