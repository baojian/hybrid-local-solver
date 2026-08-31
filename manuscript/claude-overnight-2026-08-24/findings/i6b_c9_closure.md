# I6-B — C9 closed: the clip identity and the truncation-covariance argument

**VERDICT: the single Open link of the `K_n` absorption theorem is CLOSED — C9
is now PROVED at every stage type, including genuinely partial corrections, for
every `n >= 2` and every `q <= 1/2`, with no new hypothesis.** The instrument is
an exact **clip identity** (`ell_t = x_t + phi_t` with
`phi = (beta d_t - Delta_t 1)_+`, hence `h_{t+1} = mh (h_t - P_h phi)`) plus a
one-line **truncation-covariance lemma** (`Cov(psi(v), v) >= Var(psi(v))` for
nondecreasing 1-Lipschitz `psi`). The old certified bound was not merely loose
— on a purpose-built battery of **103 genuinely partial stages** it **fails 47
of 53 K_n instances (by up to 7.76x)**; the published `K_8` pulse at 0.979 was
the *luckiest* case, not the worst. The repaired bound passes 103/103 with
margin `<= 0.87`, and on `K_n` obeys the proved margin law
`V_{t+1}/((1-q)^2 V_t) <= max(theta_F, mh/m0) < 1`. Full reruns:
**K_n 140-instance grid 18/18 predicates, 0 failures; class 82-instance battery
100% in-class on all 21 predicates** (the one C13 miss is the known Q4-eq
horizon artefact, re-verified to absorb at `t_abs = 17` with `T = 30`).

**The `K_n` absorption theorem is COMPLETE (Proved-draft, fully verified, no
Open links).** The `mu_2 >= 2q` class theorem is complete under one added pure
graph condition **(H-K)** — `q`-independent, exactly checkable, satisfied by
8 of the 11 tested families — and for graphs failing (H-K) the P-link is
reduced to a per-stage certified inequality that passed at all 30 partial
stages found on those graphs (route B / TK below).

Code: `w7_windowed/{i6b_sanity,i6b_pgen,i6b_cgen,i6b_knproof3,i6b_class3}.py`.
Data: `i6b_pbattery.json`, `i6b_cbattery.json`, `i6b_knproof3_results.json`,
`i6b_class3.json`, `i6b_class3.log`. All exact Fractions. Compute ~4 min.

---

## 0. The Open link, restated exactly

**C9 (L-I, the closing inequality).** With
`V_t := |h_t|^2 - p <h_t, h_{t-1}> + s |h_{t-1}|^2` on `K_n`
(`p = mh(1+beta)`, `s = mh beta`, `mh = kappa/(kappa+lam_h)`), and in general
`V_t := V(h_t, h_{t-1})`, `V(u,v) = <u,u>_D - (1+beta)<u, Mm v>_D +
beta <v, Mm v>_D` on the D-orthogonal complement of `1`,
`Mm = kappa (kappa D + Qt)^{-1} D`:

```
V_{t+1} <= (1-q)^2 V_t     at EVERY stage t.
```

Status before this round: proved for N stages (`V_{t+1} = s V_t` exactly),
clean stages (`r = Delta*1`, same identity), and F stages (`<=>`
`s(2-mh) <= (1-q)^2` `<=>` `q <= 1/2` on `K_n`; `<=> mu_2 >= 2q` in general);
**Open at genuinely partial stages** (`beta min_i d_i < Delta < beta max_i d_i`),
where the certified bound C17

```
U = mh^2(|tah| + Ku)^2 + p mh (|tah| + Ku)|h_t| + s|h_t|^2,
Ku = min(beta |P_h d|, (sqrt n / 2)(Delta - beta min_i d_i))
```

passed its single grid occurrence (`K_8` pulse, `t=2`) with only 2.1 % margin
(`U/((1-q)^2 V_t) = 0.9790`) against a true ratio of 0.456 — and, as Half 2 of
i4a found, **failed outright** (3.69) at a class-battery P stage.

## 1. Scarcity solved: a battery of 103 genuinely partial stages

P stages need a *spread* in `beta d_t` with the trigger `Delta` landing strictly
inside its range; block-structured seeds manufacture exactly that.

* **K_n battery** (`i6b_pgen.py`): 820 exact cells — `k`-block seeds
  `[w/k x k, (1-w)/(n-k) x (n-k)]` over `n in {4..24}`, `q in {1/4..1/50}`,
  `K_8`-pulse perturbations (`w`, `rho`, `q` varied around the published cell),
  3-level seeds, and `v`-pulse seeds with `cv` up to 300, at near-edge `rho`.
  **53 P stages** (46 distinct cells), plus 605 F and 0 CC stages.
* **Class battery** (`i6b_cgen.py`): 168 exact cells on `K_{3,3}`, `K_{2,4}`,
  `Q_3`, `Q_4`, Petersen, rook, cocktail(3,4), `C_6`, `Circ_12(1,2,3)`, `K_8`,
  with 1-vertex pulse seeds, `q` at/near/just past `mu_2/2`. **31 P stages**
  (Q3:7, Pet:8, Rook3:8, C6:3, Circ12:3, Cock3:1, K8:1).
* **Adversarial hunt** on the three (H-K)-failing graphs (`Q_4`, Petersen,
  `C_6`) with extra seed shapes (`w` up to 0.9, 2-vertex pulses, prand):
  **19 more P stages**.

Every stage carries exact energies, the clip set, and all certificate margins.
The **tuned-rho path families (P24 etc.)** do have partial stages — 126 in
`T = 4800` under the baseline cap, 23 face-aligned (known from i4a) — but they
sit on **proper faces**, where the interior-face `V` is not the governing
object (i5c measured the projected C9 failing there by up to 8x); they are
outside the scope of both theorems, whose crux on proper faces is the momentum
calibration (i4a §3), not C9.

## 2. The margin law

Old vs new certified margins over the battery (`margin := bound/((1-q)^2 V_t)`):

| battery | # P | true ratio max | OLD margin | NEW margin (proof bound) |
|---|---|---|---|---|
| `K_n` grid | 53 | 0.657 | **max 7.76, >1 at 47/53** | max **0.674**, all `<= max(theta_F, mh/m0)` |
| class | 31 | 0.710 | (i4a: 3.69 fail) | route A max 0.784, route B max 0.774, **0 fails** |
| adversarial (Q4/Pet/C6) | 19 | — | — | route B max **0.870**, 0 fails |

By `q` on `K_n` (new proof bound vs its proved law):

| q | # | true max | new max | law `max(theta_F, mh/m0)` |
|---|---|---|---|---|
| 1/4 | 18 | 0.647 | 0.674 | 0.729 |
| 1/6 | 5 | 0.657 | 0.667 | 0.692 |
| 1/10 | 25 | 0.657 | 0.664 | 0.670 |
| 1/20 | 4 | 0.657 | 0.659 | 0.660 |

**Answer to the branch question: the margin of the *repaired* bound is bounded
away from 1** — uniformly `<= max(theta_F, mh/m0)` on `K_n`, `< 1` for
`q < 1/2`, approaching 1 only through `theta_F` at the C16 boundary
(`q -> 1/2`, `n -> infinity` on `K_n`; `mu_2 -> 2q` in class), i.e. through
the **F-channel that is already the theorem's sharp boundary** — there is no
P-specific tightness anywhere. The margin has no dependence on clip fraction
(1/8 to all-but-one coordinates clipped: new margin 0.64–0.674 throughout,
while the old margin wanders 0.78–7.76). The OLD bound is not fixable by a
constant: it fails 47/53 and is structurally wrong (below). **Branch (a):
sharpen — with a different functional, not a different theorem.**

### 2.1 Where the old 0.9790-vs-0.456 gap came from (published pulse, exact)

At `K_8` pulse `t=2` (all as shares of `(1-q)^2 V_t`): true `V_{t+1}` = 0.456;
old bound 0.979. The two lossy steps, exactly:

* **sign-flipped Cauchy–Schwarz on V's middle term**: the old bound replaces
  `-p<h_{t+1}, h_t>` (true value **+0.149** because it *keeps* its sign
  structure) by `+ p mh(|tah|+Ku)|h_t|` = **+0.434** — cost **0.285**;
* **triangle inequality** `|h_{t+1}| <= mh(|tah| + |P_h r|)`: the retraction
  *anti-aligns* with the error (`|h_{t+1}|` true `5.72e-5` vs bound
  `1.67e-4`, factor 2.91), so the first term is 0.269 vs true 0.032 —
  cost **0.238**.

(0.285 + 0.238 = 0.523 = the whole gap.) S1/S2 of the absorption certificate
were sharp; these two steps, both *inside the old C17 only*, were the leak. The
repair below never bounds `h_{t+1}` in norm at all.

## 3. The repair: clip identity + truncation covariance

Everything below is verified exactly, stage-by-stage, in `i6b_sanity.py`
(12+18+18 stages, all identities `==`) and across both batteries (0 identity
failures at 84 battery P stages; general form re-verified inside
`i6b_class3.py`).

**(1) Clip identity.** `min(a,b) = a - (a-b)_+` applied to
`r_t = min(beta d_t, Delta_t 1)` gives, pointwise,

```
ell_t = a_t - r_t = x_t + phi_t ,      phi_t := (beta d_t - Delta_t 1)_+ .
```

The leash point is *`x_t` plus the clip excess*. With the master identity
(L-A) and `P` the (D-)orthogonal projection off `1` (which commutes with `Mm`):

```
h_{t+1} = Mm (h_t - phih_t) ,        phih := P phi        [K_n: h_{t+1} = mh(h - phih)]
```

N stages: `Delta = 0`, `phi = beta d`, `h - phih = (1+beta)h - beta h^- = tah`
(recovers L-C). F: `phi = 0` (L-B). Clean: `phih = beta P d` (same as N). So
**one formula covers all four stage types**; expanding `V`:

```
V_{t+1} = VF + |Mm phih|_D^2 - (1-beta) <Mm h_t, Mm phih>_D ,
VF := beta <h_t, Mm(I - Mm) h_t>_D            [K_n: VF = s(1-mh)|h_t|^2]
```

**(2) Slack identity.** Completing the square per mode, with
`co_t := h_{t-1} - ((1+beta)/(2 beta)) h_t` (the co-mode; note
`V_t = s|co|^2 + (1 - mh/m0)|h|^2` exactly on `K_n`):

```
(1-q)^2 V_t - VF = beta^2 m0 <co, Mm co>_D + beta * Gslack ,
Gslack := m0|h|^2_D - 2<h, Mm h>_D + |Mm h|^2_D  = sum_k (m0 - m_k(2-m_k)) h_k^2 .
```

`Gslack >= 0` is *exactly* C16 (per mode `m_k(2-m_k) <= m0 <=> mu_k >= 2q`),
so in class the whole right side is nonnegative. C9 at a correcting stage is
thus **equivalent** to

```
|Mm phih|^2 - (1-beta) <Mm h, Mm phih>  <=  beta^2 m0 <co, Mm co> + beta Gslack.   (*)
```

**(3) The variable that makes `phi` tractable.** `beta(p_k/(2 s_k)) - beta =
(1-beta)/2` for *every* mode (`p_k/(2s_k) = (1+beta)/(2beta)` is
`k`-independent), whence the exact vector identity

```
beta * P d_t = beta * co_t + nu * h_t =: v_t ,      nu := q/(1+q) = (1-beta)/2 ,
```

and `phi = psi(v)` pointwise with `psi(z) := (z + beta dL - Delta)_+` —
**nondecreasing and 1-Lipschitz** (the constant is irrelevant).

**(4) Truncation-covariance lemma.** For any weights `pi`, any `v`, and any
nondecreasing 1-Lipschitz `psi`:

```
Var_pi(psi(v)) <= Cov_pi(psi(v), v) .
```

*Proof.* Two-point form: both sides are
`(1/2) sum_{ij} pi_i pi_j (psi_i - psi_j) * X_ij` with `X = (psi_i - psi_j)`
resp. `(v_i - v_j)`, and `0 <= psi_i - psi_j <= v_i - v_j` whenever
`v_i >= v_j`. QED. (Equivalently: `Var(u) - Var(min(u,c)) = 2Cov(u, phi) -
Var(phi) >= Var(phi)` — *clipping reduces variance by at least the variance of
the clipped excess* — the clipped-variance identity requested by the brief.)

**(5) The K_n bound.** On `K_n`, `Mm` acts as the scalar `mh` on the high
space, so with `m := |phih|`, `X := |co|` the left side of (*) is
`mh^2 E`, `E := Var(phi) - 2 Cov(phi, v) + 2 beta Cov(phi, co)` (substituting
`nu h = v - beta co`), and by (4) and Cauchy–Schwarz:

```
E <= -m^2 + 2 beta m X <= beta^2 X^2 .
```

Since `mh <= m0`: `mh^2 beta^2 X^2 <= beta^2 m0 mh X^2 = beta m0 s X^2`, which
is exactly the co-term of the slack, and `beta Gslack = beta g |h|^2 >= 0` iff
`q <= 1/2` (C16). **C9 is proved at every stage, `n >= 2`, `q <= 1/2`.** The
per-channel accounting gives the *margin law*

```
V_{t+1} / ((1-q)^2 V_t)  <=  max( theta_F , mh/m0 ) ,
theta_F := mh(1-mh)/(m0-mh)   (the F-stage constant; < 1 iff C16 strict),
mh/m0 = (kappa+alpha)/(kappa+lam_h) < 1 always,
```

verified 53/53 on the battery (worst observed 0.674 vs law 0.729). Note what
the proof *never* uses: the value of `Delta`, the trigger, monotonicity of
`d_t`, or which coordinates clip — C9 holds for **any** cap `Delta >= 0`, so
the earlier convexity/breakpoint and census (C15) considerations are moot.
Battery footnote: `Cov(phih, h) < 0` at 39/53 P stages — a sign *assumption*
on the cross term would have been false; routing the covariance through `v`
is what works.

## 4. General graphs: route A under (H-K), route B unconditional

The only step that used `K_n` is `Mm = mh I` on the high space. In general the
clip can move co-mode energy across the band, and two certified routes replace
it (both verified in `i6b_class3.py` / `i6b_cgen.py`):

**Route A (comonotone-kernel).** Write `vh := P v = beta P d`. If

```
TK := <Mm phih, Mm (vh - phih)>_D >= 0                              (Mm^2-truncation)
```

then `|Mm phih|^2 <= <Mm phih, Mm vh>` and the K_n chain repeats verbatim in
the `Mm`-image: `E_gen <= beta^2 |Mm co|^2 <= beta^2 m2 <co, Mm co>
<= beta^2 m0 <co, Mm co>` — closing (*) with margin `m2/m0` and **no other
condition**; it closes with `<=` even at the class boundary `mu_2 = 2q`.
`TK >= 0` is the positive-association statement
`Cov_K(f, g) >= 0` for the *comonotone* pair `f = (v-c)_+`, `g = min(v,c)`
under the coupling kernel `K_{ij} := (D Mm^2)_{ij} / (m0^2 vol)` (symmetric,
`pi`-marginals). From the two-point identity
`Cov_K(f,g) = (1/2) sum_{ij} (pi_i pi_j - K_ij)(f_i-f_j)(g_i-g_j)` and
`(f_i-f_j)(g_i-g_j) >= 0`, a sufficient condition is the kernel bound

> **(H-K)**  `(Mm^2)_{ij} <= m0^2 d_j / vol` for all `i != j`.

**(H-K) is a pure graph condition, independent of `q`**: since
`kappa D + Qt = ((1-alpha)/2)(3D - A)` exactly, `Mm = c(alpha) N` with
`N := (3D-A)^{-1} D` and `c = 2(1-2alpha)/(1-alpha)` (verified bit-exactly),
and `m0 = c/2`, so (H-K) reads `4 vol (N^2)_{ij} <= d_j` — one exact rational
check per graph, valid for every `q`. Census (worst ratio; `<= 1` = holds):

| graph | K33 | K24 | Q3 | Rook3 | Cock3 | Cock4 | Circ12 | K_n | Q4 | Pet | C6 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ratio | 0.750 | 0.750 | 0.953 | 0.876 | 0.674 | 0.640 | 0.915 | 0.595 (K8) | **1.377** | **1.144** | **1.064** |
| (H-K) | yes | yes | yes | yes | yes | yes | yes | yes | no | no | no |

**Route B (unconditional certificate).** Without TK, split `Mm^2` at `m2`:

```
E_gen <= m2^2 (-m^2 + 2 beta X m) + (1-beta) sqrt(spread_h * spread_phi),
spread_h := m2^2|h|^2 - |Mm h|^2,  spread_phi := m2^2 m^2 - |Mm phih|^2,
```

(the first bracket by lemma (4) in the plain metric — unconditional; the second
by Cauchy–Schwarz in the `(m2^2 - Mm^2)`-seminorm). Fully rational per stage
with certified `m2` brackets; self-limiting because `spread_h` vanishes exactly
in the dangerous mode-2-concentrated configurations.

**Measured:** `TK >= 0` at **50/50** partial stages on general graphs
(31 battery + 19 adversarial, including all 30 on the (H-K)-failing `Q4`,
Petersen, `C6`); route B passed **50/50** (worst margin 0.870); the two
i4a P stages that killed the old C17 now pass (`C17' 2/2`).

## 5. Integration: full predicate chains re-run

**`K_n` grid, 140 instances + 2 published (`i6b_knproof3.py`, 60 s): 18/18
predicates PASS, 0 failures.** C1 7130/7130, C3/C4 7076/7076, C5/C6/C7/C8/C9/
C10/C11 7130/7130, C12/C13/C16 140/140, C14 7076/7076, C15 (census: 53 F + 1 P)
54/54, **C17' 1/1**, **C9s (the proof bound `V_{t+1} <= VF + mh^2 beta^2|co|^2`
at every correcting stage) 54/54**. Absorption 140/140, `t_abs <= 12`,
`max J_total = 0.36918 < log 2` — all i2c numbers reproduced.

**Class battery, 82 instances (`i6b_class3.py`, 15 s with cached certified
brackets): all 21 predicates 100 % in-class.** C1–C11 1360/1360 each in class
(1696/1696 all), C12 64/64, **C13 64/64** (63 at the stock horizons + Q4-eq
skew re-verified `t_abs = 17` at `T = 30`, C17'/C9s passing there too),
C14 976/976, C15 census 9/9, C16 64/64 in class — and out of class exactly the
18 below-threshold cells fail C16 (sharpness, agreement with `mu_2 >= 2q`
82/82) — **C17' 2/2 (was 0/2)**, **C9s 11/11**, S1/S2/S3 as before.

## 6. The theorems, final form

> **Theorem A (K_n absorption — COMPLETE).** Let `G = K_n`, `n >= 2`, seed
> `s` with `s_i > rho d_i` for all `i` (H0), `q = sqrt(alpha/(1-alpha)) <= 1/2`.
> Then `V_{t+1} <= (1-q)^2 V_t` at every stage (Lemma C9', §3 — proved), hence
> the absorption certificate fires at a finite `t_abs` with the explicit
> a-priori bound of i2c, every stage `t >= t_abs` is correction-free,
> `gamma_t = 1` there, and `J_T^fin <= B < log 2` for all `T`; the Route-B net
> packing holds with `c = 1`. **Status: Proved-draft (every link), verified
> exactly on 140 instances — no Open links.**

> **Theorem B (`mu_2 >= 2q` class — complete under (H-K)).** Let `G` be
> connected, `alpha in (0, 1/2)`, `q <= 1/2`, under (H0), (Hgap)
> `mu_2 >= 2q`, and **(H-K)** `4 vol ((3D-A)^{-1}D)^2_{ij} <= d_j` (`i != j`).
> Then C9 holds at every stage (routes §4), absorption fires, and
> `J_T^fin <= B` with `c = 1` as in i4a. **Status: Proved-draft on the (H-K)
> subclass** — which contains `K_n`, complete multipartite/cocktail, `K_{a,b}`,
> rook, `Q_3`, `Circ_12(1,2,3)` of the tested families. For graphs failing
> (H-K) (`Q_4`, Petersen, `C_6` among tested): the P-link is reduced to
> `TK >= 0` **or** the route-B inequality — both certified per stage, passing
> 50/50 including every boundary cell; that residue is the only remaining Open
> fragment, now scoped to "positive association of the `Mm^2` kernel on
> sparse-diameter graphs".

## 7. Evidence labels

**Proved-draft:** the clip identity, slack identity, `beta P d = beta co + nu h`,
truncation-covariance lemma, C9' on `K_n` (all stages, `q <= 1/2`), the margin
law `max(theta_F, mh/m0)`, route A modulo `TK >= 0`, the (H-K) => `TK >= 0`
kernel lemma, `Mm = c(alpha) (3D-A)^{-1} D` and the `q`-independence of (H-K);
all verified exactly wherever they assert equalities/inequalities (0 failures
across the ~115k stage-level predicate checks of the two reruns plus the
battery identity checks).
**Measured:** `TK >= 0` beyond (H-K) (50/50, incl. 30 stages on Q4/Pet/C6);
route-B margins `<= 0.87`; old-C17 failure census (47/53).
**Open (single residue):** `TK >= 0` (or any C9-at-P proof) for in-class graphs
failing (H-K); everything else previously Open about C9/C15/C17 is closed.

## 8. Next targets

1. **`TK >= 0` beyond (H-K).** The failing entries of (H-K) are
   nearest-neighbour pairs, while `(f_i-f_j)(g_i-g_j) != 0` only for pairs
   *straddling the cap*; a transport/ordering argument on
   `sum_{straddle} (pi_i pi_j - K_ij)(v_i - c)(c - v_j)` should beat the
   entrywise condition — this would make Theorem B unconditional on `G`.
2. Propagate C9' into the manuscript ladder (i5d) and retire the C15/C17
   scaffolding there; the F/P/CC case split in the write-up collapses to the
   single clip identity.
3. The proper-face program (face-calibrated momentum, i4a §3.1) is unaffected
   and remains the route to the actual `l1` regime.
