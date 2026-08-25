# I4-E — Value-guided admission + incremental factorisation (SP2): one mechanism that is provably output-bounded and measured alpha-free

**Direction:** I4-D's SP2, verbatim: *"Exhibit one mechanism that is
simultaneously output-bounded (does not read volume outside `S_eps ∪ dS_eps`)
and alpha-free (cycle count `O(log(1/eps))`)."*  I4-D located the whole
remaining gap here: the two alpha-free mechanisms in the arsenal (elimination,
local AMG) select their region **by BFS ball** and are therefore not
output-bounded (ball trap: `W*eps` grows like `M^2` while the correct output
is empty); the one output-bounded mechanism (push) selects **by value** and is
therefore not alpha-free (`1/(alpha*eps)`).

Code `i4e/{vgf.py, common.py, run_trap.py, run_zoo.py, run_fail.py, fit.py,
fit2.py, smoke.py}`; data/logs `i4e/out/{trap.json, zoo.json, zoo.log,
fail.json, fail.log}`.  Conventions, model and Meter exactly as I3-A / I4-D
(`Q = (1+a)/2 I − (1−a)/2 D^{-1/2}AD^{-1/2}`, `b = a D^{-1/2}e_v`,
`pi = D^{1/2}x`, `u = pi/d`, semantic err `= max_i |pi_hat_i − pi_i|/d_i`,
scans charge `d_u`, ring vertices charge **one degree query** per I4-D Lemma D).
**Every run in every table was verified against the exact solve and against
exhaustive membership of `S_eps`: 0 semantic failures and 0 missed vertices in
71 charged runs.**

---

## VERDICT

1. **SP2 is answered in the affirmative, with one named residual.**  The
   mechanism — **VGF** (Value-Guided incremental Factorisation) — is
   **provably output-bounded** (Lemma V2: the admitted region is contained in
   the level set `S_{θγε}`, with *no adjacency or distance term anywhere in
   the bound*) and **measured alpha-free in its region** (region-inflation
   alpha-exponent **+0.033**) and **in its work per unit of output when
   oracle-stopped** (median exponent **+0.064**, max **+0.209**, against
   push's **+0.934**).
2. **The ball trap is broken, decisively.**  `W*eps` versus clique size `M`:
   ball-based elimination grows as **`M^2.9`** (128 → `2.76e6`), ball-based
   AMG as **`M^1.9`**, while **VGF is FLAT** (143 → 125 over `M = 100 …
   1600`) and its oracle-stopped variant is flat at **0.014 = O(1)**, the
   information-theoretically correct answer, since `S_eps` there is empty.
   At `M = 1600` VGF is **22 000×** below elimination and **10×** below push.
   Same on the **hidden hub**: VGF flat at 0.25 while elimination and AMG grow
   **linearly in `M`** (6.3 → 600 for `M = 10^3 → 10^5`).
3. **The self-certified method still carries `alpha^{+0.26}`, and the cause is
   now pinned to one place: the ROUND COUNT, not the region.**  On path-like
   families the region inflation is alpha-free (`×1.31/1.32/1.57` at
   `a = 2^-4/-8/-12`) but the number of solve rounds grows `5 → 8 → 22`,
   exponent `+0.27` — matching the measured `W/vol(S_VGF)` exponent `+0.28`
   to two digits.  A genuinely incremental factorisation (per-round cost
   `O(vol(new))` instead of `O(vol(S))`) would remove the multiplier; this is
   the precise next target.
4. **Two of the three adversarial families I built do break it, and one of them
   badly.**  The **fan trap** (ring vertices whose true `u` sits inside the
   band `[γε, ε]`) inflates the region **516×** and costs **938×** the
   oracle-stopped work — a sharpened form of I4-D's SP1: the loose certificate
   does not merely over-solve, it **over-admits volume**.  The **expander
   pocket** (small volume, treewidth `Θ(N)`) kills the elimination inner
   solver (`N^2.9`) but is repaired by the AMG triage; the *region rule*
   survives untouched.
5. **The speculation floor is load-bearing, not a tuning knob.**  Dropping it
   from `θ = 0.1` to `θ = 10^-3` destroys the ball trap: region
   `1146 → 160 400` (the whole graph), `W*eps  199 → 1.9e5`.  The provable
   output bound and the measured ball-trap flatness are the *same fact*.
6. **A negative result worth recording.**  The optimism literal push gets away
   with — stopping at threshold `eps` rather than `γ·eps` — is **unsound for
   value-guided admission** and fails loudly: `err/eps = 6.5` and **1153
   missed vertices** on a 2-D grid.  The reason is structural: `Lo` is a
   *lower* bound on `u`, so `Lo(h) < eps` does not imply `u_h < eps`.

Evidence grade: **Proved-draft** for §2 (Lemmas V1–V3: the monotone lower
bound, the output bound, the no-miss guarantee — all short, and checked
exhaustively on every run); **Measured** for §3–§6; **Open** for the
alpha-freeness of the self-certified method (residual `alpha^{0.26}`) and for
everything the fan trap breaks.

---

## 1. The mechanism

`vgf_local` in `i4e/vgf.py`.  State: an admitted region `S`, an exact solve
`x_S` of `Q[S,S] x = b[S]`, and a per-vertex **lower bound** `ulb[w] ≤ u_w`.
`c_a = (1−a)/(1+a)`, `γ = 2a/(1+a)`, `gate = γ·eps`, `spec_floor = θ·gate`
(`θ = 0.1`).

For a ring vertex `h` define the **certified value contribution**

>  `Lo(h) := (c_a / d_h) · Σ_{w ∈ S, w ~ h} ulb[w]`.

This is I4-D's Lemma D residual row, read as a value rather than as a residual:
`Lo(h) = res_h/d_h` in the push scale `M pi = γ s`, `M = I − c_a A D^{-1}`,
so `|(D^{-1/2}(Q x̂ − b))_h| = ((1+a)/2)·Lo(h)` **exactly**.  The one object
serves as both the admission key and the certificate.

Each round:

1. **Solve** `Q[S,S] x_S = b[S]` exactly.  Route chosen by a charged `O(nnz)`
   structural test: **forest → HSEG-LDL two-pass** (I2-B), cost `O(|S|)`;
   else **sparse LDL with MMD**; else, if `Σ colcnt² > κ·nnz` (high
   treewidth), **SA-AMG V-cycles on the same region** (I3-A machinery, region
   choice orthogonal to inner solver).
2. **Ring refresh** — one push sweep out of `S`, re-using the same adjacency
   read that assembled `Q[S,S]`; `|dS|` degree queries (Lemma D), never
   `vol(dS)`.
3. **Certificate**: stop iff `max_h Lo(h) < γ·eps` and the interior residual
   `< α·eps`.
4. **Value-guided admission** with a volume budget `growth·vol(S)`
   (`growth = 3`): pop ring vertices in decreasing `Lo`; a **violator**
   (`Lo ≥ gate`) is always admitted; a **speculative** candidate is admitted
   only while `Lo ≥ θ·gate` **and** its degree fits the budget.  Interleaved
   with **extension solves**: the exact solve of `Q[N,N] x_N = b_N −
   Q[N,S] x_S` on the *newly admitted* vertices only, with the already-solved
   region frozen as Dirichlet data — admitted volume is never re-solved, and
   the frozen data being a lower bound keeps `x_N` a lower bound too.

**Admission never consults adjacency, distance, or shell index.**  That single
change is the whole difference from `direct_local`/`amg_local`, whose inner
solvers VGF reuses verbatim.

### Charging (identical to I3-A/I4-D plus Lemma D)
`scan_idx` charges `d_v` (first exposure `C_adj`, repeats `R_adj`); each ring
degree query 1 unit `C_resp`; factorisation `Σ colcnt²` + `nnz(L)+nnz(U)`
materialised + `2·nnz` per triangular solve; each heap operation
`⌈log₂(size+2)⌉`; every accumulator push and ring test 1 unit `C_rec`; AMG
levels/transfers/RAP/coarse solves at their true nonzero counts.  The forest
route is charged `4|S|` (up pass) `+ 3|S|` (down pass), never less.

---

## 2. What is proved (Proved-draft)

**Lemma V1 (monotone lower bound).**  At every instant `ulb[w] ≤ u_w` for all
`w`.  *Proof.*  Induction.  (i) A full or extension solve sets
`ulb[w] = x_w/√d_w` where `x` solves a Dirichlet system on a sub-region with
frozen data that is itself `≤ u`; `Q` is a symmetric M-matrix, so
`Q[S,S]^{-1} ≥ 0` entrywise and the solution is dominated by the restriction of
the true solution.  (ii) An admitted `v ∉ supp(s)` receives
`ulb[v] = Lo(v) = (c_a/d_v) Σ_{w∈S,w~v} ulb[w] ≤ (c_a/d_v) Σ_{w~v} u_w = u_v`,
the last step being I4-D's Lemma C identity.  The seed is in `S` from the
start.  ∎

**Lemma V2 (OUTPUT BOUND — the point of the whole direction).**  Every
certified-admitted vertex satisfies `u_h ≥ γ·eps`; every speculatively
admitted vertex satisfies `u_h ≥ θ·γ·eps`.  Hence

>  `S ⊆ {seed} ∪ { v : u_v ≥ θ·γ·eps }`,
>  `vol(S) ≤ d_seed + vol(S_{θγε}) < d_seed + 1/(θ·γ·eps)`  (I4-D Lemma A).

**No adjacency, distance, shell or ball radius appears in this bound.**  A
high-volume structure hanging off the support is admitted *only if its own
value clears the bar* — which is exactly what a BFS-ball rule cannot promise
and why the ball trap exists.  ∎

**Lemma V3 (no misses).**  VGF returns only when
`max_h Lo(h) < γ·eps` and the interior residual `< α·eps`, i.e.
`‖D^{-1/2}(Q x̂ − b)‖_∞ < α·eps`.  By the repository certificate `err < eps`,
hence every `v ∉ S` has `u_v < eps`, i.e. `S_eps ⊆ S`.  ∎
*Checked independently on every run by exhaustive set difference against the
exact `S_eps`: **0 misses in 71 runs**.*

**Lemma V4 (rounds).**  Each round either certifies or grows `vol(S)`; the
budget caps growth at `growth·vol(S)`, so rounds where the budget binds are
`O(log_{growth} vol(S))`.  *(Rounds where the lower-bound expansion stalls
before the budget are **not** bounded by this — that is exactly the residual
of §5.)*

---

## 3. THE DECISIVE MEASUREMENT — `W*eps` versus `M` (E1/E2)

`ball_trap(400, M, at=60)`: a 400-path from the seed with `K_M` hung by a
single edge at depth 60.  `alpha = 7.4e-6`, `eps = 1e-3`; **`S_eps` is empty**,
so the correct output is the zero vector and the ideal work is `O(1)`.
`vgfO` = VGF stopped by the oracle (semantic error), the mechanism-cost floor.

| `M` | push | I4-B composed | ball elim (`directDQ`) | ball AMG (`amgDQ`) | **VGF** | **VGF-O** |
|---|---|---|---|---|---|---|
| 50 | 1245 | 311 | 128 | 317 | 1070 | 0.41 |
| 100 | 1245 | 910 | 803 | 887 | **143** | **0.014** |
| 200 | 1241 | 4 627 | 5 830 | 3 228 | **160** | **0.014** |
| 400 | 1243 | 2 096 | 44 610 | 9 688 | **199** | **0.014** |
| 800 | 1241 | 1 159 | 349 000 | 45 550 | **272** | **0.014** |
| 1600 | 1241 | 665 | **2 760 000** | 184 400 | **125** | **0.014** |
| **fitted slope in `M` (100→1600)** | **0.00** | — | **+2.94** | **+1.92** | **−0.05** | **0.00** |

**The prediction is confirmed exactly: `W*eps` FLAT in `M` for value-guided
admission, `M^2` for both ball-based mechanisms.**  At `M = 1600` VGF is
`2.2e4 ×` below elimination, `1.5e3 ×` below ball AMG, `10 ×` below push, and
`5.3 ×` below the I4-B composed solver at its best point.  `VGF-O` at `0.014`
is `8.9e4 ×` below push — the correct `O(1)`.

**Non-degenerate cell** (`alpha = 2^-10`, `eps = 1e-4`, `vol(S_eps) = 119`, so
the output is genuinely nonempty):

| `M` | push | composed | `directDQ` | `amgDQ` | **VGF** | **VGF-O** |
|---|---|---|---|---|---|---|
| 50 | 36.4 | 18.0 | 12.8 | 22.3 | 25.2 | 0.34 |
| 100 | 36.6 | 9.5 | 80.3 | 68.2 | **1.36** | 0.30 |
| 200 | 36.3 | 7.5 | 583 | 273 | **1.64** | 0.30 |
| 400 | 36.3 | 8.9 | 4 461 | 872 | **2.28** | 0.30 |
| 800 | 36.3 | 5.0 | 34 900 | 3 786 | **1.08** | 0.30 |
| slope in `M` | 0.00 | — | **+2.85** | **+1.86** | **−0.28** | 0.00 |

**Hidden hub** (`hidden_hub(6, M)`, `alpha = 2^-6`, `eps = 1e-3`;
`vol(S_eps) = 11` fixed, one ring vertex of unbounded degree):

| `M` | push | composed | `directDQ` | `amgDQ` | **VGF** |
|---|---|---|---|---|---|
| `10^3` | 1.253 | 0.351 | 6.33 | 6.54 | **0.250** |
| `10^4` | 1.253 | 0.351 | 60.3 | 60.5 | **0.246** |
| `10^5` | 1.253 | 0.351 | 600.3 | 600.5 | **0.246** |

Exactly linear in `M` for the ball methods (I4-D Lemma E), flat for VGF, and
VGF is the cheapest mechanism measured on this family.

---

## 4. THE FULL SWEEP (E3) — 15 families × `alpha ∈ {2^-4, 2^-8, 2^-12}`, `eps = 1e-5`

All 45 cells certified; **0 misses, 0 semantic failures**.  `W*eps` at the
three alphas, and the fitted **mechanism** exponent `q` in
`W/vol(S_eps) ~ alpha^{-q}` (`q = 0` ⇔ alpha-free):

| family | `vol(S_eps)` | push `W*eps` | composed | **VGF** | **VGF-O** | `q` push | `q` comp | **`q` VGF** | **`q` VGF-O** |
|---|---|---|---|---|---|---|---|---|---|
| path | 471 | 0.030/1.46/64.5 | 0.017/0.062/0.32 | 0.010/0.059/0.71 | 0.010/0.031/0.21 | +0.934 | +0.083 | +0.313 | +0.092 |
| caterpillar | 635 | 0.041/1.90/82.9 | 0.029/0.108/0.38 | 0.017/0.091/0.82 | 0.017/0.051/0.26 | +0.932 | +0.021 | +0.256 | +0.047 |
| comb | 1 088 | 0.087/3.29/129 | 0.092/0.218/0.76 | 0.037/0.153/1.46 | 0.037/0.077/0.36 | +0.942 | +0.007 | +0.290 | +0.037 |
| spider | 2 130 | 0.118/5.40/214 | 0.118/0.421/2.16 | 0.054/0.322/3.40 | 0.054/0.176/0.89 | +0.925 | +0.096 | +0.320 | +0.079 |
| star | 12 000 | 3.36/55.4/888 | 1.74/1.74/1.74 | 3.34/3.34/3.34 | 3.34/3.34/3.34 | +1.006 | −0.000 | **−0.000** | **−0.000** |
| btree | 32 764 | 0.81/80.3/1 405 | 1.18/9.30/9.30 | 6.04/10.8/10.7 | 2.41/10.8/10.7 | +0.919 | −0.055 | **−0.323** | −0.157 |
| rrt | 15 998 | 1.16/41.5/965 | 6.03/6.20/6.23 | 2.48/5.09/5.25 | 2.48/3.96/5.25 | +0.967 | −0.239 | **−0.110** | −0.110 |
| pa_tree | 13 983 | 0.72/27.6/836 | 2.53/5.41/5.55 | 1.60/5.00/5.57 | 0.76/2.81/4.49 | +0.953 | −0.177 | **−0.094** | +0.003 |
| theta | 1 203 | 0.070/3.28/137 | 0.060/0.320/1.11 | 0.029/0.166/1.95 | 0.029/0.088/0.48 | +0.927 | +0.086 | +0.318 | +0.064 |
| prism | 1 806 | 0.104/4.66/189 | 0.107/0.334/1.72 | 0.064/0.389/4.40 | 0.064/0.287/1.14 | +0.919 | +0.067 | +0.328 | +0.083 |
| grid2d | 26 080 | 0.45/28.5/735 | 4.76/122/167 | 3.51/88.3/592 | 3.51/22.5/186 | +0.774 | +0.083 | **+0.365** | +0.157 |
| grid3d | 23 808 | 1.28/39.4/717 | 21.5/234/252 | 19.0/411/290 | 19.0/83.2/290 | +0.859 | +0.161 | +0.209 | +0.209 |
| decoy_hub | 471 | 0.030/1.46/64.5 | 0.017/0.062/0.32 | 0.010/0.059/0.71 | 0.010/0.031/0.21 | +0.934 | +0.083 | +0.313 | +0.092 |
| exp3reg | 27 000 | 0.92/76.2/1 318 | 70.7/107/109 | 69.4/219/220 | 14.9/219/220 | +0.976 | −0.256 | −0.126 | +0.152 |
| exp5reg | 45 000 | 1.75/89.7/1 498 | 254/293/291 | 410/453/485 | 172/453/485 | +0.971 | −0.222 | −0.217 | −0.060 |
| **MEDIAN** | | | | | | **+0.934** | **+0.021** | **+0.256** | **+0.064** |
| **MAX** | | | | | | **+1.006** | **+0.161** | **+0.365** | **+0.209** |

**Reading.**

* **Push is `alpha^{-0.93…-1.01}` on every one of the 15 families** — the
  literal `Theta(1/(alpha·eps))` law, reproduced cleanly.
* **VGF's mechanism exponent is `+0.256` median, `+0.365` max**, i.e. it
  removes **73 %** of push's alpha dependence in the exponent, and on 5 of 15
  families the exponent is **negative** (work per unit output *falls* as alpha
  falls).  Oracle-stopped it is `+0.064` median, `+0.209` max: **alpha-free
  within measurement noise**.
* **VGF beats push on the median cell by 5.5× (`vgf/push` median 0.18)** and by
  up to **260×**; it loses by up to 234× on `exp5reg` at `alpha = 2^-4`, where
  the output is `Theta(n)` and push is already near-optimal.  Against the I4-B
  composed solver the median ratio is **1.00** (max 5.1, min 0.40): VGF matches
  the hindsight-composed portfolio on the ordinary zoo *and* wins on the traps.
* **Best-of count over the 45 cells:** push 10, composed 9, VGF 8, VGF-O 18.
  No self-certified mechanism dominates — but VGF is the only one that is
  never catastrophic (see §6 for its two catastrophes).
* `W/vol(S_eps)` for VGF ranges `26 … 3 581` charged units per unit of output,
  with the top of the range at `exp5reg`/`grid2d` — the same two families that
  cost the arsenal the most in I4-D.

### Where VGF's residual alpha-dependence lives (the sharpest result in §4)

Decomposing `W = [W / vol(S_VGF)] · [vol(S_VGF) / vol(S_eps)] · vol(S_eps)`:

| quantity | median alpha-exponent | max | reading |
|---|---|---|---|
| **region inflation** `vol(S_VGF)/vol(S_eps)` | **+0.033** | +0.086 | **alpha-free** |
| work per unit of the region actually solved | **+0.219** | +0.315 | the residual |
| rounds `R` on path-likes (`a = 2^-4/-8/-12`) | `5 → 8 → 22` ⇒ **+0.27** | | **the cause** |

The region-inflation ratio itself is `1.00 … 6.9` across all 45 cells (median
1.40) — **the sound gate `γ·eps` costs almost nothing in region size on the
ordinary zoo**, contradicting the natural worry that admitting down to
`2α·eps` would blow the region up by `1/α`.  The `+0.27` exponent that remains
is the **round count**, and it matches the `+0.28` work exponent on paths to
two digits.  Its cause is mechanical: the push lower bound decays by `~c_a/d`
per step outside the solved region, so a round's expansion reaches
`~log₂(ν/floor)` shells; as alpha falls the true decay length grows but the
lower bound's reach does not, so more rounds are needed, and each round pays
`O(vol(S))` for the re-solve and re-sweep.

---

## 5. The stopping-rule / mechanism split, and the speculation floor

**Certificate cost (SP1, measured here as a work ratio).**  `VGF / VGF-O` over
the 45 zoo cells: **median 1.29×, max 4.94×** — far milder than I4-D's
`~10×` for self-certified AMG on grids, because the value gate reuses the same
quantity for admission and certification.  On the adversarial families it is
much worse (§6a: 938×).

**The speculation floor `θ` is the theorem, not a knob.**  `spec_theta`
controls how far below `gate` a value-ordered speculative admission may go.
Lowering it buys rounds on benign families and *destroys* the trap families:

| family | `θ = 0.1` | `θ = 10^-3` | `θ = 10^-5` |
|---|---|---|---|
| path `a=2^-12` `W*eps` (region ×) | 0.706 (×1.57) | 0.344 (×1.61) | **0.288** (×1.76) |
| spider `a=2^-12` | 3.40 (×1.76) | 1.59 (×1.78) | **1.27** (×1.90) |
| grid2d `a=2^-12` | 592 (×2.57) | 387 (×2.57) | **264** (×2.57) |
| **ball_trap `M=400`** | **199** (vol 1 146) | **1.9e5** (vol **160 400**) | 3.2e4 (vol 160 400) |

At `θ = 10^-3` the ball trap's clique falls inside the speculative band and the
region becomes the **entire graph** — a 140× region blow-up and a 950× work
blow-up.  So the 2.5× constant that a lower floor buys on benign families is
paid for by losing Lemma V2.  **`θ = 0.1` is reported everywhere above.**

**Refuted shortcut (negative result).**  Running VGF with the *semantic* gate
`eps` instead of `γ·eps` — the same optimism that literal push (`push_c(m,eps)`)
gets away with throughout this campaign — is **unsound**:

| family | `err/eps` | vertices of `S_eps` **missed** |
|---|---|---|
| grid2d 120² `a=2^-8` | **6.48** | **1 153** |
| rrt 2000 `a=2^-8` | **6.46** | **304** |
| path 4000 `a=2^-8` | **5.65** | **14** |

The reason is structural and worth recording: `Lo(h)` is a *lower* bound on
`u_h`, so `Lo(h) < eps` does not imply `u_h < eps`.  Push's residual `r_h/d_h`
is a different object with a different (and, empirically, forgiving)
amplification.  **The optimism does not transfer.**

---

## 6. HONEST FAILURE HUNT (E4) — what breaks

### 6a. FAN TRAP — *"certifying that a vertex is below threshold is what costs"*.  **BREAKS IT, badly.**
`fan_trap(400, K, D=200, at=20)`: a 400-path seeded at 0; `K` "blockers" of
degree `200` hung on path vertex 20.  Each blocker's value is
`u_at·c_a/200` — far below `eps`, but tunable into the band `[γ·eps, eps]`,
where the **sound** gate must admit it and pay its full degree.
`alpha = 2^-10`, `eps = 1e-4`.

| `K` | `vol(S_eps)` | push | composed | `directDQ` | **VGF** | **VGF-O** | `vol(S_VGF)/vol(S_eps)` | `VGF/VGF-O` |
|---|---|---|---|---|---|---|---|---|
| 10 | 4 067 | 194 | 11.3 | 10.9 | 25.0 | 14.1 | ×1.0 | 1.8 |
| **50** | **39** | 7.9 | **1.67** | 50.3 | **103.4** | **0.110** | **×516** | **938** |
| 200 | 39 | 7.8 | 1.15 | 198 | 16.7 | 0.224 | ×167 | 74 |
| 800 | 39 | 7.8 | 1.26 | 787 | **1.11** | 0.644 | ×22 | 1.7 |

**At `K = 50` VGF reads 516× the output volume and does 938× the
oracle-stopped work, losing to both push (13×) and the composed solver (62×).**
This is I4-D's SP1 in its sharpest form: the loose certificate does not merely
*over-solve* a region, it **over-admits volume** — and because admission is by
value, a family engineered to place volume precisely in `[γ·eps, eps]` extracts
the full `1/α` band width.  The non-monotonicity in `K` is diagnostic: at
`K = 800` the hub's own degree `802` depresses the blocker values below the
gate again and the family stops biting.
**A computable instance-adaptive amplification bound (I4-D SP1) would repair
this exactly; nothing else in the arsenal will.**

### 6b. EXPANDER POCKET — *"value-admitted region of small volume but treewidth `Θ(N)`"*.  **Breaks the inner solver; the region rule survives.**
`exp_pocket(20, N, 3)`: a 20-path into a random 3-regular expander on `N`
vertices, `alpha = 2^-8`, `eps = 1e-5`.  The whole pocket is genuinely inside
`S_{γε}`, so the region is *correct*; it is the elimination that dies.

| `N` | `vol(S_eps)` | VGF **/ldl** | VGF **/auto** (AMG triage) | `directDQ` | push | composed |
|---|---|---|---|---|---|---|
| 500 | 1 540 | 6.28 | **5.92** | 8.76 | 10.9 | 4.64 |
| 1 500 | 4 540 | 135 | **25.4** | 260 | 17.7 | 10.6 |
| 4 000 | 8 020 | **2 629** | **76.4** | 4 253 | 10.6 | 45.1 |
| slope in `N` | | **+2.9** | **+1.2** | +3.0 | ≈0 | +1.1 |

Pure elimination on the value-selected region is `N^{2.9}` (fill), exactly as
on the BFS-selected region.  The charged `Σcolcnt² > κ·nnz` triage flips to
SA-AMG and recovers `N^{1.2}` — `W/vol(S_eps)` goes `384 → 559 → 635`, i.e.
grows *sub-logarithmically*.  **The failure is entirely in the inner solver and
is repaired by triage; the value-guided region rule is untouched.**  (Push is
still the best mechanism on this family, at `W/vol = 132` for `N = 4000`.)

### 6c. SHALLOW SUPPORT — a milder, structural version of 6a.  **Breaks it mildly.**
`path(40000)`, `eps = c·u_max`, so `S_eps` is `O(1)` while the sound gate
reaches out to `S_{γε}`:

| cell | `vol(S_eps)` | `vol(S_VGF)` | ratio | push | composed | **VGF** | **VGF-O** | `VGF/VGF-O` |
|---|---|---|---|---|---|---|---|---|
| `a=2^-4, c=0.5` | 3 | 9 | ×3.0 | 2.88 | 28.6 | 18.4 | 6.5 | 2.8 |
| `a=2^-8, c=0.5` | 11 | 59 | ×5.4 | 39.7 | 80.5 | 49.8 | 16.1 | 3.1 |
| **`a=2^-12, c=0.5`** | **45** | **311** | **×6.9** | 579 | 108 | **159** | **10.4** | **15.4** |
| `a=2^-12, c=0.05` | 191 | 461 | ×2.4 | 747 | 17.0 | 28.8 | 5.4 | 5.3 |

The region inflation grows like `alpha^{-0.24}` in this regime — not the
`alpha^{-1/2}` I expected, but clearly not alpha-free either.  VGF still beats
push by 3.6× at the worst cell and loses to the composed solver by 1.5×.

### 6d. Where VGF simply is not the right mechanism
`exp5reg` and `exp3reg` at `alpha = 2^-4`: `vol(S_eps) = Theta(n)`, the whole
graph is the output, and push does `W/vol = 15.3` against VGF's `3 581`
(234×).  On the extremal instances of I4-D's Lemma A — where the output *is*
the graph — a solver that factorises anything is paying for structure that
does not exist.  **VGF does not dominate; it is a third member of the
portfolio, not a replacement for it.**

---

## 7. THE CLAIM, stated precisely

> **Claim I4-E (Measured, with a Proved-draft core).**
> Let `G` be simple, undirected, unweighted, with no isolated vertices,
> accessed by adjacency-list scans (scanning `i` costs `d_i`, repeats charged)
> together with an `O(1)` degree query.  Let `s = e_v`, `alpha ∈ (0,1]`,
> `eps ∈ (0,1]`, `gamma = 2 alpha/(1+alpha)`, `theta ∈ (0,1]` a fixed constant.
> Then `vgf_local` (i4e/vgf.py) outputs `x_hat` with
> `max_i |pi_hat_i − pi_i|/d_i ≤ eps` and
>
> **(P1, proved)** admits only vertices `h` with `u_h ≥ theta·gamma·eps`, hence
> reads region volume `vol(S) ≤ d_v + vol(S_{theta·gamma·eps}) <
> d_v + 1/(theta·gamma·eps)`, **with no adjacency, distance or ball-radius
> term in the bound**;
>
> **(P2, proved)** never omits a vertex of `S_eps`, and charges every ring
> vertex exactly one degree query, never `d_h`;
>
> **(M1, measured, 15 families × 3 alphas × `eps = 1e-5`, 45/45 certified,
> 0 misses)** total charged work satisfies
> `W ≤ C(G) · vol(S_eps) · alpha^{-q}` with `q` median `+0.256`, max `+0.365`
> and `C ∈ [26, 3581]`; oracle-stopped, `q` median `+0.064`, max `+0.209`;
>
> **(M2, measured, ball trap and hidden hub)** `W·eps` is **flat** in the
> adversarial parameter `M` (slopes `−0.05` and `0.00`) where ball-based
> elimination is `M^{2.9}` / `M^{1.0}` and ball-based AMG is `M^{1.9}` / `M^{1.0}`.

**Hypotheses that are doing real work and must be stated with the claim.**
1. `O(1)` degree query (I4-D Lemma E; without it no bound in `1/eps` exists).
2. Single seed.  `nnz(s)` seeds add `Theta(nnz(s))` and Lemma V1 is unchanged,
   but nothing here was measured with `nnz(s) > 1`.
3. The constant `theta = 0.1`.  §5 shows the claim is **false** for
   `theta ≤ 10^-3` on the ball trap.
4. `C(G)` is *not* graph-uniform: it ranges over `26 … 3 581` on the zoo and is
   **unbounded on the fan trap** (§6a), where `vol(S_VGF)/vol(S_eps) = 516`.
   So (M1) is a *per-family* statement, not a theorem about all graphs.
5. Exact arithmetic is assumed for the inner solves; the AMG route is
   iterative and stops at `0.05·alpha·eps` measured residual.

**What a proof would need.**
* **(a) The round count.**  Lemma V4 bounds only budget-binding rounds.  A
  proof needs: *the value-guided expansion from an exactly-solved region `S`
  reaches `Omega(vol(S))` new volume before stalling*, or else an incremental
  factorisation making a stalled round cost `O(vol(new))` rather than
  `O(vol(S))`.  Measured, the round count is the entire residual
  `alpha^{+0.26}` (§4), so this single lemma would upgrade (M1) to `q = 0`.
* **(b) Region inflation.**  A proof that `vol(S_{theta·gamma·eps}) =
  O(vol(S_eps)·polylog(1/(alpha·eps)))` **on a named class** — measured `+0.033`
  on the zoo, but **refuted in general by the fan trap** (516×), so the class
  must exclude "volume parked in the band `[gamma·eps, eps]`".  The honest form
  is a *conditional* theorem with the band-mass as an explicit hypothesis.
* **(c) SP1, unchanged from I4-D.**  A locally computable
  `A_hat(S) ≥ A(S) = err/theta_resid`, charged in the ledger, that is
  `O(alpha^{-1/2})` when the true amplification is.  §6a shows this is now the
  *only* thing between VGF and output-linearity: with a sharp certificate the
  gate would be `~eps` rather than `~2·alpha·eps`, the fan trap would collapse
  to `VGF-O`'s `0.110` and the shallow-support family to `10.4`.
* **(d) Inner-solver triage.**  A charged, sound criterion for choosing
  forest-LDL / MMD-LDL / AMG.  The `Σ colcnt² > kappa·nnz` test used here is a
  heuristic; §6b shows the choice is worth `N^{1.7}`.

---

## 8. Answering the direction's question in one line

> **Is a single mechanism now both output-bounded and alpha-free?**
> **Output-bounded: yes, provably** (Lemma V2 — the bound contains no
> adjacency term, and the ball trap and hidden hub confirm it operationally:
> flat in `M` where every ball method is polynomial in `M`).
> **Alpha-free: yes in the region (exponent `+0.033`) and yes in the mechanism
> (oracle-stopped exponent `+0.064` median, `+0.209` max); NOT yet in the
> self-certified algorithm (`+0.256` median, `+0.365` max), and the entire
> residual is the round count, which is a fixable implementation property and
> not a property of value-guided admission.**
> So SP2's existence question is answered positively for the *region rule* and
> the *mechanism*, and remains **Open by a factor `alpha^{-0.26}`** for the
> end-to-end self-certified algorithm.

---

## 9. Ledger, verification, caveats

* **Verification.**  Every one of the 71 charged runs (45 zoo + 14 trap + 12
  failure) was checked against `spsolve`/CG for `err = max_i |pi_hat_i −
  pi_i|/d_i ≤ eps` **and** against `S_eps ⊄ supp(x_hat)` by exhaustive set
  difference.  **0 semantic failures, 0 misses.**  The only runs in this report
  with `err > eps` are the deliberately-unsound `gate = eps` runs of §5, which
  are reported as a refutation and used nowhere else.
* **Ledger.**  As §1.  The forest route is charged `7|S|` per solve; the MMD
  route `Σcolcnt² + 3·nnz(L+U)`; the AMG route at I3-A's true per-level counts.
  Ring vertices cost one `C_resp` unit each (I4-D Lemma D) and are **never**
  scanned; a ring vertex later admitted pays its full degree at that point.
  Heap operations are charged `⌈log₂⌉`; the ring is *not* fully heapified each
  round — only the candidate band `Lo ≥ theta·gate`, selected by an `O(|dS|)`
  threshold test that is itself charged.
* **Caveats, stated plainly.**
  1. The per-round full re-solve means VGF is "incremental" only in the
     amortised, geometric-ladder sense plus the extension solves; a *strict*
     up-looking incremental factorisation in admission order was **not** built,
     and on a star that ordering is provably dense (`|S|²`).  This is why
     §7(a) is the top open item.
  2. Ball-trap slopes rest on 6 points over one decade of `M`; hidden-hub on 3
     points over two decades.
  3. `VGF-O` is oracle-stopped: it lower-bounds mechanism cost and is **not**
     an algorithm.  Its gap to `VGF` is SP1.
  4. `growth = 3.0` and `theta = 0.1` are fixed constants chosen from the
     smoke tests; §5 documents the sensitivity of the second.
  5. The composed-solver column is I4-B's solver run unmodified with its own
     `Ledger`; its `W` is comparable to `VecMeter.total()` by construction
     (`ledger.from_vecmeter` docstring), but its triage sometimes flips on the
     ball trap, which is why its column is non-monotone in `M`.
  6. No file outside `i4e/` was modified; `amglib.py`, `composed.py` and
     `ledger.py` are imported as-is, so every earlier campaign number stands.

---

## 10. Next target

**SP3 — the incremental factorisation that removes the round-count multiplier.**
Concretely: maintain a Schur complement (a *response matrix*) on the open
frontier of `S`, eliminating a vertex as soon as all its neighbours are
admitted, so that a round costs `O(vol(new) + |frontier|²)` rather than
`O(vol(S) + fill(S))`.  On a path and on a star the frontier is `O(1)` and the
per-round cost collapses to `O(1)`; on a 2-D grid it is `O(sqrt(area))` and the
cost is nested-dissection-optimal.  Predicted: VGF's `W/vol(S_VGF)` alpha-
exponent falls from `+0.22` to `0`, making the self-certified method alpha-free
end-to-end — which, with Lemma V2 already proved, would be the first single
mechanism that is *both*.

Second target, unchanged and now more urgent: **SP1**, because §6a shows it is
the only remaining source of unbounded region inflation.
