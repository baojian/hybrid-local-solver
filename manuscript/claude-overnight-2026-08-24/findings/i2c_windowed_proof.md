# I2-C — A windowed / absorption net-accelerated-exponent theorem for K_n

**VERDICT: K_n WINDOW THEOREM DRAFTED (one Open link).** For complete graphs the
windowed target is not merely *windowed* — it collapses to something strictly
stronger: **corrections stop after a finite, explicitly bounded time**, so
`J_T^fin <= B` uniformly in `T` and the Route-B net packing
`J_T^fin <= (1-c) q T + B` holds with **c = 1** (no loss of acceleration at all).
Every inequality of the chain is verified in exact rational arithmetic on a
**140-instance grid** (n in {2,4,8,16,32} x q in {1/10,1/100,1/400} x 5 seed
families x 2 rho regimes) plus the two published families: **17/17 predicates
pass, 0 failures, 7130 stage-level checks per universal predicate**. The single
Open link is isolated to one stage type (genuinely partial corrections) which
occurs **once** in the whole grid.

Code: `w7_windowed/{kn_modal,knproof2,kn_struct,p24_audit}.py` (plus the
iteration-1 `engine.py`, `knproof.py`). Data: `knproof2_results.json`,
`p24_audit.json`. Compute ~5 min.

---

## 0. What C1–C8 (iteration 1) are

They are **the lemma chain of the proof, not diagnostics.** Each `Ck` is the
exactly-checkable content of one lemma; the previous agent had already put the
skeleton in place (docstring of `knproof.py`) and closed C1–C8 on three
families. Restated precisely, with this round's extensions C9–C17:

| tag | lemma | assertion | status |
|---|---|---|---|
| C1 | L-A master | `(Qt + kap D) e_{t+1} = kap D (x* - ell_t)` | Proved-draft |
| C2 | L-B F-collapse | `Delta >= beta max d` => `ell_t = x_t` => `h_{t+1}=mh h_t`, `L_{t+1}=m0 L_t` | Proved-draft |
| C3 | L-C N-linear | N stage => both modes obey `u_{t+1} = p u_t - s u_{t-1}` | Proved-draft |
| C4 | L-C' V-decay | `V_{t+1} = s V_t` **exactly** on N stages | Proved-draft |
| C5 | L-E oscillation | `|P_h r_t| <= beta |P_h d_t|` (no low->high pump) | Proved-draft |
| C6 | L-D trigger | `alpha Delta_t = max_i [-(alpha aL + lam_h ah_i)]_+` | Proved-draft |
| C7 | L-F1 defect | `Dfin_t <= a_q(|e_{t-1}|_D^2 - |e_t|_D^2)`, `a_q=(1-q)/q` | verified (project ms-15) |
| C8 | L-F2 Phi floor | `2 Phi_t >= mu_E |e_t|_D^2` | verified (project ms-15) |
| C9 | L-I closing | `V_{t+1} <= (1-q)^2 V_t` at **every** stage | 3 of 4 cases Proved; 1 **Open** |
| C10 | L-H low floor | `L_t >= (1-q) L_{t-1} > 0` at every stage | Proved-draft |
| C11 | L-M monotone | `d_t >= 0`, `e_t >= 0` (lower certificate) | Proved-draft |
| C12 | L-S structure | `lam_h > alpha` <=> `p^2<4s` <=> `s<=(1-q)^2`; `m0 = 1-q^2`; low-mode char. poly `= (z-(1-q))^2` | Proved |
| C13 | L-G absorption | certificate fires; every later stage is N; `gamma_t = 1` | Proved-draft |
| C14 | L-G' | `R_{t+1} <= (s/(1-q)^2) R_t` on N stages | Proved-draft |
| C15 | correction census | every correcting stage is `CC` or `F` (else genuinely partial) | **53 F + 1 P**, see §4 |
| C16 | F-contraction | `s(2 - mh) <= (1-q)^2` — pure `(n,q)` inequality | Proved for `q <= 1/2` |
| C17 | P-certificate | certified rational bound `U <= (1-q)^2 V_t` at partial stages | 1/1, margin only 2.1% |

---

## 1. Setup and the two-mode reduction (L-A, L-S)

Hat coordinates `xh = D^{-1/2}x`, `Qt = D^{1/2} Q D^{1/2}`, `M := D^{-1} Qt`.
On `K_n`, `D = (n-1) I` and `M` has **exactly two eigenvalues**:

```
M 1 = alpha 1                                   (low mode, span{1})
M h = lam_h h,  h _|_ 1,  lam_h = alpha + (1-alpha) n / (2(n-1)).
```

Because `D` is a multiple of `I`, the `D`-orthogonal projection onto `1^perp`
**is plain mean-centering** `P_h u = u - mean(u) 1`. This single fact is what
makes `K_n` tractable (see §5).

**L-0 (face lock).** `Qt + kap D` is a strictly diagonally dominant irreducible
M-matrix. If `ctil = alpha(s - rho d) > 0` componentwise, then any coordinate
with `x_i = 0` would need `((Qt+kap D)x)_i >= ctil_i > 0` while the off-diagonals
are negative and `x >= 0`, i.e. `((Qt+kap D)x)_i <= 0` — contradiction. So
**every iterate from `t = 1` on is interior**, and the KKT system is an
equality. (Hypothesis (H0): `s_i > rho d_i` for all `i`. Verified `ctil_pos`
and `fullsupp` on 140/140 instances; `t_F = 1`.)

**L-A (master identity).** Interior + `Qt xh* = ctil` gives, exactly,

```
(M + kap) e_{t+1} = kap (x* - ell_t),      e_t := x* - x_t.          [C1]
```

Split `e = L*1 + h`. With `m0 = kap/(kap+alpha)`, `mh = kap/(kap+lam_h)`:

```
L_{t+1} = m0 (x*-ell)_L ,      h_{t+1} = mh (x*-ell)_h .
```

**L-S (structural identities, all exact rationals).** `m0 = 1 - q^2`, and the
low-mode N-recurrence `L_{t+1} = m0[(1+beta)L_t - beta L_{t-1}]` has
characteristic polynomial

```
z^2 - 2(1-q) z + (1-q)^2 = (z - (1-q))^2        <-- critically damped
```

i.e. **the low mode is exactly the accelerated mode `(A+Bt)(1-q)^t`** — this
*is* the published `K_2` closed form `e_t = (1+tq)(1-q)^t e_0`, and it is the
reason the one-step Lyapunov bank fails there (a critically damped mode loses
only `O(q^2)` per step). With `p := mh(1+beta)`, `s := mh*beta`:

```
lam_h > alpha   <=>   p^2 < 4s (underdamped high mode)   <=>   s <= (1-q)^2.
```

All three are **equivalent**, and `lam_h > alpha` holds for every `n >= 2` and
every `q`, so both structural side conditions are free. [C12: 140/140]

## 2. The stage taxonomy and the exact V-Lyapunov (L-B, L-C, L-D)

`d_t = x_t - x_{t-1} >= 0`, trial `a_t = x_t + beta d_t`,
`ta := x* - a_t = (1+beta)e_t - beta e_{t-1}`, retraction
`r_t = min(beta d_t, Delta_t * 1)`, `ell_t = a_t - r_t`.

**L-D (trigger).** `alpha Delta_t = max_i [-(alpha ta_L + lam_h ta_{h,i})]_+`.
A correction fires **iff the modal combination goes negative in some
coordinate** — the low mode enters with weight `alpha ~ q^2` and the high mode
with weight `lam_h ~ 1/2`. [C6]

**L-C.** On N stages (`Delta=0`, `r=0`) both modes are two-term linear, and the
quadratic form

```
V_t := |h_t|^2 - p <h_t, h_{t-1}> + s |h_{t-1}|^2
```

satisfies **`V_{t+1} = s V_t` exactly** (companion-matrix identity, no
inequality). [C4: 7076/7076]

**L-B.** On F stages `r = beta d`, `ell = x_t`, so `h_{t+1} = mh h_t` and
`V_{t+1} = chi(mh) |h_t|^2` with `chi(z) = z^2-pz+s` and the identity
`chi(mh) = s(1-mh)`. [C2: 53/53]

## 3. The positive-part coupling — resolved on K_n (L-E)

This is the known non-commutation obstacle: `r_t = min(beta d_t, Delta 1)` is a
coordinatewise operation and does not commute with the modal projection. On
`K_n` it is nevertheless **provably harmless**:

> For any coordinatewise 1-Lipschitz `phi` and `u in R^n`,
> `|P_h phi(u)|^2 = (1/2n) sum_{i,j} (phi(u_i)-phi(u_j))^2
>                <= (1/2n) sum_{i,j} (u_i-u_j)^2 = |P_h u|^2`,
> using `sum_i (u_i - ubar)^2 = (1/2n) sum_{i,j}(u_i-u_j)^2`.

`v |-> min(v, Delta)` is 1-Lipschitz, hence **`|P_h r_t| <= beta |P_h d_t|`**:
the retraction can never pump the slow (low) mode into the fast (high) mode.
[C5: 7130/7130] The **positive part is a variance contraction**. Equally
important, `r_t >= 0` means the low mode is only ever *helped*:

**L-H (low-mode floor).** `(x*-ell)_L = ta_L + mean(r) >= ta_L`, and
`m0[(1+beta) - beta/(1-q)] = 1-q` exactly, so

```
L_t >= (1-q) L_{t-1} > 0   propagates through EVERY stage type (N, P, F).
```
[C10: 7130/7130; combined with L-M `e_t >= 0`, C11: 7130/7130]

## 4. The absorption certificate (L-G) — the heart of the theorem

Set `C_ta = (1+beta)^2 + beta^2/s`, `dn_lb = (1 - p^2/(4s))/2`,
`wh2 = (alpha*beta/lam_h)^2`, and

```
R_t := C_ta V_t / ( dn_lb * wh2 * L_{t-1}^2 ).
```

> **Absorption Lemma.** If at some stage `t`
> **(i)** `L_t >= (1-q) L_{t-1} > 0` and **(ii)** `R_t <= 1`,
> then `Delta_t = 0`, and (i),(ii) again hold at `t+1`. Hence **every stage from
> `t` on is an N stage**, `gamma_u = 1` for all `u >= t`, and
> `J_T^fin = J_t^fin =: B` for all `T >= t`.

*Proof.* Trigger side: (S1) `|ta_h|^2 <= C_ta(|h_t|^2 + s|h_{t-1}|^2)`
(weighted Cauchy–Schwarz); (S2) `dn_lb(|h_t|^2+s|h_{t-1}|^2) <= V_t` (from
`2 sqrt(s)|h_t||h_{t-1}| <= |h_t|^2+s|h_{t-1}|^2` and `dn_lb <= 1-p/(2 sqrt s)`,
valid because `p^2<4s`). Chaining with (ii): `lam_h |ta_h| <= alpha beta L_{t-1}`,
while (i) gives `alpha ta_L >= alpha beta L_{t-1}`; since `|ta_h|_inf<=|ta_h|_2`,
every modal coordinate `alpha ta_L + lam_h ta_{h,i} >= 0`, so `Delta_t = 0` by
L-D. Propagation: the stage is N, so `V_{t+1} = s V_t` (L-C) and
`L_t^2 >= (1-q)^2 L_{t-1}^2` (L-H), giving
`R_{t+1} <= [s/(1-q)^2] R_t <= R_t` because `s <= (1-q)^2` (L-S). QED

Exact verification: **S1 1488/1488** (worst ratio 1.0000 — Cauchy–Schwarz is
attained, so `C_ta` is sharp), **S2 1488/1488** (worst 0.9025), **premise =>
`lam_h|ta_h| <= alpha beta L_{t-1}` and `Delta_t = 0`: 1128/1128**,
**C13 140/140**, **C14 7076/7076**.

### The one Open link: finite absorption time (L-I / C9)

The lemma is useless unless (ii) is *reached*. `R` decays iff
`V_{t+1} <= (1-q)^2 V_t` at every stage (C9). Four cases:

| case | condition | status |
|---|---|---|
| N | `Delta = 0` | **Proved**: `V_{t+1} = s V_t`, `s <= (1-q)^2` |
| CC (clean) | `Delta <= beta min_i d_{t,i}` => `r = Delta*1` => `P_h r = 0` | **Proved**: identical to N, `V_{t+1} = s V_t` |
| F (full) | `Delta >= beta max_i d_{t,i}` | **Proved for `q <= 1/2`**, see below |
| P (genuinely partial) | `beta min d < Delta < beta max d` | **OPEN** |

*F case.* `V_{t+1} = chi(mh)|h_t|^2 = s(1-mh)|h_t|^2` and
`V_t >= (1-p^2/4s)|h_t|^2`, so C9 reduces to the **pure `(n,q)` inequality**

```
s (2 - mh) <= (1-q)^2 .                                            [C16]
```

`mh` is *increasing* in `n` (since `lam_h` decreases), so the worst case is
`n -> infinity`, `lam_h -> (1+alpha)/2`, `mh -> 2(1-2alpha)/(3-3alpha)`. Exact
rational evaluation: the inequality holds for every `n >= 2` **iff `q <= 1/2`**
(i.e. `alpha <= 1/5`) — with *equality exactly at `q = 1/2`* and failure above
(`q=0.51`: `0.241178 > 0.240100`). Since the RPPR regime is `q ~ sqrt(alpha)`
small, this is free: at `q=1/10` the ratio is `0.7236/0.81`, at `q=1/400`
`0.8845/0.9950`. [C16: 140/140, margin ratio 0.50–0.67]

*P case — OPEN.* The proved bounds
`|P_h r| <= min( beta|P_h d| , (sqrt n /2)(Delta - beta min_i d_i) )` give a
certified rational upper bound `U` on `V_{t+1}`. **Census over the whole grid:
53 F stages, 1 P stage, 0 CC stages** — the only genuinely partial correction
anywhere is the published `K_8` pulse at `t=2`, and there
`U / ((1-q)^2 V_t) = 0.9790`: it passes, but **with only a 2.1 % margin**, so
the bound is *not* robust and cannot be labelled Proved. This is the single
Open inequality of the draft. The measured (as opposed to certified) ratio at
that stage is `V_{t+1}/V_t = 0.3694`, i.e. reality has 55 % of margin — the
gap is in the estimate, not the mechanism.

### Consequences, verified exactly

* absorption fires in **140/140** instances, `t_abs <= 12` (mean 5.6, min 1);
* the a-priori bound `t_abs <= t_F + ceil(log R_{t_F} / log((1-q)^2/eta))`
  (`eta` = worst per-stage V-ratio) is `<= 22` and dominates the actual
  `t_abs` in every instance where it applies (103/103);
* `B = J_infinity <= 0.36918 nats < log 2 = 0.6931` over the entire grid
  (worst cell `K32, q=1/10, v-pulse, rho at the edge`); the published pulse
  gives `B = 0.233072`;
* worst per-stage V-ratio anywhere: **0.6563 vs `(1-q)^2 >= 0.81`**
  (per q: `1/10`: 0.534/0.810, `1/100`: 0.646/0.980, `1/400`: 0.656/0.995);
* **window telescope** (`w = ceil(1/q)`): window 0 carries all the inflation,
  **every later window contributes exactly 0 nats**.

> **Theorem (K_n, draft).** Let `G = K_n`, `n >= 2`, seed `s > 0` with
> `s_i > rho d_i` for all `i`, `q = sqrt(alpha/(1-alpha)) <= 1/2`. Assume L-I at
> genuinely partial stages. Then there is a finite `t_abs` with an explicit
> bound such that every stage `t >= t_abs` is correction-free, and for all `T`
> ```
> J_T^fin <= B := sum_{t < t_abs} log gamma_t  <  log 2 ,
> ```
> so `J_T^fin <= (1-c) q T + B` holds with `c = 1`.

Evidence labels: **Proved-draft** for C1–C8, C10–C14, C16 and the two
Cauchy–Schwarz steps S1/S2 (verified exactly on every tested `K_n` family);
**Open** for C9/C17 at genuinely partial stages (margin 2.1 % on its one
occurrence).

## 5. What extends to general graphs — and the crux

**Extends unchanged:** L-A (master identity holds on any graph on the interior
face), L-D (trigger `alpha Delta = max_i[-(M ta)_i]_+`), L-B (F-collapse),
L-M (monotone lower certificate), the `r >= 0` half of L-H, L-F (ms-15), and
the per-eigenspace V-form.

**The crux is L-E, and it is not "window + spectral gap".** On `K_n` the slow
eigenvector is `1` and `D = (n-1)I`, so the spectral projection *is*
mean-centering and the coordinatewise `min` is a **variance contraction**. On a
general graph the slow direction is the `D^{1/2}`-Perron vector `v` (non
constant), the relevant projection is `P = I - v v^T D/(v^T D v)`, and
`min(., Delta * 1)` does **not** contract `|P . |`: the retraction cap is a
multiple of `1`, misaligned with `v`, so the positive part genuinely pumps the
slow mode into the fast modes. Concrete next target: replace the cap `Delta*1`
by `Delta * v` (or prove a `v`-weighted Lipschitz-variance inequality
`|P min(u, Delta v)| <= |P u|`), which would transport L-E verbatim.

**Second gap:** two modes become `m` modes; the retraction's inter-mode coupling
matrix is not diagonal, so the `V`-form must be replaced by a block form whose
off-diagonal blocks are controlled by the same missing inequality.

**Third and most important:** the `K_n` result is an **absorption** theorem —
corrections *stop*. `P_4` and the tuned-rho path families (§6) show that on
general graphs corrections **never** stop (period-11 cycles to `T = 2000+`,
per-event `gamma -> 1.0236`; tuned paths sustain `gamma ~ 1.44` for
`T = 4800`). So on general graphs the absorption route is unavailable and a
genuine window telescope with `c < 1` is required. `K_n` therefore establishes
the *mechanism* (modal reduction + variance contraction of the positive part +
low-mode floor) but **not** the general technique. The right reading: the
proof gives a full, exactly verified template, and the general case needs
(a) the `v`-weighted L-E, and (b) a replacement for absorption — a per-window
budget in which correcting stages are charged against the `s <= (1-q)^2` slack
accumulated by the intervening N stages (the census `53 F : 1 P` says the slack
is large, `s/(1-q)^2 ~ 0.66`, i.e. ~0.41 nats of V-margin per N stage against
the ~1.0 nat a correction can cost).

## 6. AUDIT-BATTERY SPEC — tuned-rho path stress family (P_24)

Drop-in cell for the project's exact checker. All constants exact rationals.

```
graph    : path P_24, nodes 0..23, edges {i,i+1}, i=0..22
           degrees d = (1, 2,2,...,2, 1)
seed     : s = e_0   (s_0 = 1, s_i = 0 otherwise)   -- endpoint seeding
q        : 1/32
alpha    : q^2/(1+q^2) = 1/1025
kappa    : 1 - 2 alpha = 1023/1025
beta     : (1-q)/(1+q) = 31/33
mu_E     : kappa*alpha/(alpha+kappa) = 1023/1049600
rho      : 65/4096 = 0.015869140625      <-- EXACT, dyadic
horizon  : T = 4800 (= 150/q); window w = ceil(1/q) = 32
```

**Construction rule (why this rho).** The family works by tuning `rho` just
**above** the support breakpoint at which the far endpoint leaves `S*`. Bisection
gives `rho* = 0.0157290668...` (`|S*|: 24 -> 23`). Take the smallest convenient
dyadic strictly above `rho*`: `65/4096`. Then `|S*| = 23` with `x*_23 = 0`
**exactly** — the last support coordinate sits on the kink, which is the
mechanism that re-arms the correction trigger forever.

**Expected behaviour (acceptance criteria).**

| quantity | value |
|---|---|
| `|S*|` | 23 (node 23 off support, `x*_23 = 0` exactly) |
| inflation events in `T=4800` | 91, last at `t = 4748` (**sustained**) |
| `J_4800` | 17.894 |
| tail slope of `J_T` vs `qT` | **0.1255** (target `< 1`; measured `<< 1`) |
| max per-event `gamma` | **1.4391** |
| max per-window ratio `infl/(q w)`, `j>=1` | 0.5819 |
| correction word, stages 0..25 | `NNNFNNNNNNNNNNNNNNNNNNNNNN` |
| exact-vs-float agreement | identical word; `max|gamma_exact-gamma_float| = 2.2e-16` |

**Sensitivity (include as neighbouring cells — the family is sharp).**

| rho | `|S*|` | slope | events | verdict |
|---|---|---|---|---|
| `1/64 = 0.015625` (**below** rho*) | 24 | 0.000 | 6 | **transient** — does not stress |
| `65/4096 = 0.0158691` | 23 | 0.1255 | 91 | sustained (spec cell) |
| `2/125 = 0.016` | 23 | 0.1236 | 98 | sustained |
| `641/40000 = 0.0160250` | 23 | 0.1176 | 93 | sustained |
| `101/6300 = 0.0160317` | 23 | 0.1183 | 100 | sustained |
| `1/62 = 0.0161290` | 23 | 0.1090 | 92 | sustained |
| `33/2000 = 0.01650` | 22 | 0.0945 | 82 | sustained |
| `17/1000 = 0.017` | 22 | 0.1237 | 104 | sustained |

**What a windowed lemma must survive here:** per-event `gamma` up to `1.44`
recurring roughly every `52 ~ 1.6/q` stages, a single window absorbing `0.58 q w`
nats, and `J_T` growing linearly forever at slope `~0.13` — while per-window
`log Phi` decay stays at `2.2-2.5` nats `>> q w = 1`. Any `c` claimed by a
window theorem must satisfy `1 - c >= 0.13` on this cell.

## 7. Next target

1. **Close L-I.** Either (a) prove that genuinely partial corrections are
   impossible on `K_n` after `t_F` under (H0) — the census `0 CC : 1 P : 53 F`
   suggests P stages are a measure-zero startup phenomenon — or (b) sharpen the
   `|P_h r|` estimate at P stages (the certified bound wastes 55 % of the true
   margin; the loss is in `|ta_h|_inf <= |ta_h|_2` and in the two
   Cauchy–Schwarz steps, and a direct `ell_t = max(a_t, x_t + ... )` coordinate
   argument should recover it).
2. **`v`-weighted L-E for general graphs**: does `|P min(u, Delta v)| <= |P u|`
   hold for the `D`-orthogonal complement of the Perron vector `v`? This single
   inequality is the whole general-graph crux.
3. Add the `P_24` cell above to the exact-checker battery and re-test any
   candidate window lemma against it before believing it.
