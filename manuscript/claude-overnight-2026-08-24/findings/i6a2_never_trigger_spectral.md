# I6-A2 — The never-triggering lemma by the spectral/modal route

**VERDICT: PROVED-except-one-step.** The spectral route delivers a proved,
self-propagating Perron-dominance certificate that forces `Delta_t = 0` and
re-establishes itself at every subsequent stage of a face segment — the **cone
bridge closes**; the **factorization bridge (Z_-) is refuted twice over**
(proofs in §5). What the spectral route does *not* deliver is the base case at
each face entrance: the certificate is *reached* (geometric decay, explicit
bound, proved) rather than *held from entry*, and on 3 of 9 cells the certified
norm form has not yet decayed to 1 by the recorded horizon while the sharp
componentwise form holds from `t_lock + <= 7` on all 9. Never-triggering from
`t = 0` therefore decomposes exactly into: (i) a proved stage-1 base case,
(ii) a proved activation lemma (entering coordinates can never fire), (iii) the
proved fixed-face propagation theorem, and (iv) the entrance/pre-lock
componentwise gap — which is precisely the sibling route's (I6-A1) scope; the
interface is stated in §8. Everything displayed below that is labelled exact
was verified in exact rational arithmetic: **2 041 charged stages across the
nine i5c proper-face cells, 0 corrections, 0 failures on any exact predicate**
(`i6a2_battery.py`, `i6a2_results.json`, `i6a2_battery.log`; identity checks
200/200 each).

Throughout: hat coordinates, `Qt = D^{1/2} Q D^{1/2}`, face `S`,
`kappa = 1-2alpha`, per-face certified `(q_r, beta)` with
`beta = (1-q_r)/(1+q_r)` from i5c Lemma C. All engine quantities are those of
`i5c_core.run_i5c` (variant `fm`).

---

## 1. The trigger predicate, extracted exactly (T0: 2041/2041)

From `i5c_core.py:156-159` (and `engine.py:150-155`): with
`zeta(a)_i = ct_i - (Qt_S a)_i` on `S_t = supp(a_t)`,

```
Delta_t > 0   <=>   min_{i in S_t} zeta(a_t)_i < 0 .
```

The cap direction `w` and denominator `Qt_S w` scale the *size* of `Delta_t`,
never whether it is positive — **the never-triggering question is cap-free.**

**Reformulation (exact, load-bearing).** Let `Y_t := ct - Qt x_t` be the
full-space lower residual at the *state*. Since `a_t = x_t + beta_t d_t` and
`zeta` is affine,

```
zeta(a_t) = (1+beta_t) Y_t - beta_t Y_{t-1} =: u_t          (exact identity)
NEVER-TRIGGER(t)  <=>  u_t >= 0 on S_t
                  <=>  Y_t >= [(1-q_r)/2] Y_{t-1}  componentwise on S_t ,
```

using `beta/(1+beta) = (1-q_r)/2`. Verified: predicate equivalence **T0
2041/2041**; the last equivalence is algebra (`u = (1+beta)(Y_t - sigma
Y_{t-1})`, `sigma = beta/(1+beta)`), and its two sides agree 2041/2041 (CC =
CB2 counts). *Warning recorded:* the `sigma`-floor is the target itself, not an
independent invariant.

## 2. The exact linear dynamics in residual coordinates

On any stage with `Delta_t = 0` (so `ell_t = a_t`), the obstacle solve gives,
with `P := supp(x_{t+1})` (exact LCP consequences of `engine.obstacle_solve`):

```
(D1)  Y_{t+1} = kappa D (x_{t+1} - a_t)      on P          [CG 2041/2041 exact]
(D2)  Y_{t+1,i} <= - kappa d_i a_{t,i} <= 0  off P         [CAoff 2041/2041]
(D3)  on P:  Y_{t+1}|_P = Mm'_P u_t^{ext}|_P ,  Mm'_P := kappa D_P (Qt_P + kappa D_P)^{-1} ,
```

where `u^{ext}` is `u_t` read on all of `P` (equal to `u_t` when the face does
not grow). `Mm'_P >= 0` entrywise, strictly positive per connected component
(inverse of an irreducible M-matrix times positive diagonals). On a fixed face
`S` this is the two-term recurrence the task predicted, in the engine's own
coordinates:

```
Y_{t+1} = A Y_t + B Y_{t-1},   A = (1+beta) Mm'_S,  B = -beta Mm'_S,  c = 0 ,
```

i.e. the affine part vanishes identically in `Y`-coordinates — `Y` is already
the deviation variable (`Y = Qt_S(x*_S - x)` with `x*_S := Qt_S^{-1} ct_S` the
face solution; fixed point `Y = 0`). `Mm'_S` is `*`-self-adjoint for
`<u,v>_* := sum u_i v_i / d_i`, with eigenvalues `m_k = kappa/(kappa+lam_k)`
(`lam_k` = eigenvalues of `M_S = D_S^{-1} Qt_S`) and Perron pair
`(m_S, psi := D_S w_S)`, `m_S = kappa/(kappa+alpha_S)`.

**Sign structure (exact).** `Y_t >= 0` on `S_t` at every stage (CA 2041/2041);
`Y_t <= 0` off `supp(x_t)` (proved from the LCP, (D2)); within a fixed-face
N-run, `u_t >= 0 => Y_{t+1} = Mm' u_t >= 0` (proved).

**Activation lemma (proved; CNEW 89/89 + 89/89).** If `j` enters the support
at the solve `t -> t+1` (`x_{t+1,j} > 0 = x_{t,j}`), then `Y_{t,j} <= 0` (by
(D2) at stage `t`, since `j` was off `supp(x_t)`) and `Y_{t+1,j} = kappa d_j
x_{t+1,j} > 0` (by (D1), `a_{t,j} = 0`). Hence for ANY `beta_{t+1} >= 0`

```
u_{t+1,j} = (1+beta_{t+1}) Y_{t+1,j} - beta_{t+1} Y_{t,j} > 0 .
```

**Entering coordinates can never fire the trigger at entry, for any momentum
schedule.** This is beta-free and face-change-free, and covers the growing
boundary of the pre-lock phase. (All 89 activation events across the battery
confirm both inequalities exactly.)

**Base case at `t = 1` (proved).** `Delta_0 = 0` trivially (`a_0 = 0`). At
`t = 1`: `Y_1 = kappa D x_1` on `S_1` and `Y_0 = ct`. For `i in S_1` with
`ct_i <= 0`, `u_{1,i} > 0` trivially. For `ct_i > 0`: dropping the nonpositive
off-diagonal terms of `(Qt + kappa D) x_1 = ct` on `supp(x_1)` gives the
diagonal bound `x_{1,i} >= ct_i / [d_i (kappa + (1+alpha)/2)]`, hence
`u_{1,i} = (1+beta_1) kappa d_i x_{1,i} - beta_1 ct_i >= 0` provided

```
kappa >= beta_1 (1+alpha)/2 ,   which holds for every beta_1 <= 1 iff alpha <= 1/5
```

(equality exactly at `alpha = 1/5` — the same threshold as i2c's `q <= 1/2`).
So `Delta_1 = 0` is a theorem in the RPPR regime.

## 3. Modal structure — the task's Step 1, corrected

With `beta = (1-q_r)/(1+q_r)`: `4beta/(1+beta)^2 = 1 - q_r^2` **(exact;
200/200)**. Mode `k` obeys `z^2 - p_k z + s_k`, `p_k = (1+beta) m_k`,
`s_k = beta m_k`; real roots iff `m_k >= 1-q_r^2` iff `lam_k <= crit :=
kappa q_r^2/(1-q_r^2)`.

* **The task sheet's "the calibration makes EVERY mode overdamped" is FALSE,
  and the sheet's "smallest multiplier is m_S" inverts the order:** `m_k` is
  *decreasing* in `lam_k`, so `m_S` is the *largest* multiplier and high modes
  are *underdamped*. Exact inertia of `Qt_S - crit*D_S` (rational symmetric
  elimination, `i6a2_battery.inertia_below`) over all **79 distinct faces** of
  the battery: `n_od := #{lam_k <= crit} = 1` on **78 faces**; `n_od = 2 =
  |S|` on exactly one (the S16-leaf locked face, `alpha_S ~ 0.375`, where
  `crit ~ 1.50 > lam_max`). Only the Perron mode is overdamped, generically.
* **Overdamped modes (proved, exact):** `chi(0) = s > 0`, `chi(1) = 1-m > 0`,
  and the exact factorization `chi(1-q_r) = [(1-q_r)/(1+q_r)]*[(1-q_r^2) - m]
  <= 0` for `m >= 1-q_r^2` (200/200) give both roots real in `(0,1)` with
  `z_- <= 1-q_r <= z_+`. Implicit differentiation of `chi(z_pm) = 0` gives
  `dz_+/dm = z_+^2 / (m * sqrt(disc)) > 0` and `dz_-/dm < 0`: **`z_+` is
  strictly increasing in `m`, so the Perron mode governs** (`z_+(m_S)` is the
  spectral radius of the face recurrence), and `z_-` is strictly *decreasing*
  (this kills the factorization bridge, §5).
* **Underdamped modes:** modulus `sqrt(s_k) = sqrt(beta m_k) <
  sqrt(beta(1-q_r^2)) = 1-q_r` **(exact, 200/200)**.
* **The load-bearing equivalence (exact, 200/200):**

```
n_od = 1   <=>   lam_2^S > crit   <=>   m_2 < 1-q_r^2   <=>   s_2 < (1-q_r)^2 ,
```

i.e. **"exactly one overdamped mode" IS the strict N-stage V-decay condition**
`(H-sep)`. The i5c-measured `s_2^S < (1-q_r)^2` (C9face) is not a coincidence
but the inertia statement; it is certified exactly by `n_od = 1`, with no
eigensolver, on 78/79 faces. (Lemma C guarantees `n_od >= 1` always:
`alpha_S <= ub <= crit`.)

## 4. The cone bridge, proved: the Perron-dominance certificate

Fix a face `S` (connected; the battery's faces all are), `(q_r, beta)` its
certified calibration with `q_r < 1`, and assume **(H-sep)** `lam_2^S > crit`
(exact inertia certificate). Split `Y = L*psi + h` in `<.,.>_*`,
`L = <w,Y>/||w||_D^2`, `<psi, h>_* = 0`. On an N-run the split is exact and
uncontaminated:

```
L_{t+1} = m_S [(1+beta) L_t - beta L_{t-1}] ,        h_{t+1} = Mm' [(1+beta) h_t - beta h_{t-1}] .
```

Constants (all rational-certifiable from the CW bracket and inertia):
`s_k = beta m_k`; `s_2 = beta m_2`, `s_min = beta kappa/(kappa+lam_max^S)`
(Gershgorin `lam_max^S <= 1` if wanted); `C_S := (1+beta)^2 + beta^2/s_min`;
`dn_S := 1 - (1+beta) sqrt(m_2) / (2 sqrt(beta)) > 0` (positive iff (H-sep));
`m_psi := min_{i in S} sqrt(d_i) w_i > 0`; and the pair-form (i4a's `V` with
face constants, in `*`-geometry)

```
V_t := ||h_t||_*^2 - (1+beta) <h_t, Mm' h_{t-1}>_* + beta <h_{t-1}, Mm' h_{t-1}>_*
     = sum_k [ h_{t,k}^2 - p_k h_{t,k} h_{t-1,k} + s_k h_{t-1,k}^2 ]        (modal V-form)
R_t := C_S V_t / ( dn_S * m_psi^2 * beta^2 * L_{t-1}^2 ) .
```

> **Theorem (fixed-face never-trigger propagation; PROVED).** Suppose at stage
> `t` (both states supported in `S`, the face unchanged through `t+1`):
> **(i)** `L_t >= (1-q_r) L_{t-1} > 0` and **(ii)** `R_t <= 1`.
> Then `Delta_t = 0`, the stage is N, and (i), (ii) hold again at `t+1` with
> `R_{t+1} <= [s_2/(1-q_r)^2] R_t < R_t`. Hence by induction **no stage of the
> remaining face segment ever triggers**, and `gamma = 1` exactly throughout.

*Proof.* (a) *Trigger.* `u_t = [(1+beta)L_t - beta L_{t-1}] psi + (1+beta)h_t
- beta h_{t-1}`. By (i) and the exact identity `(1+beta)(1-q_r) = 2beta`,
`(1+beta)L_t - beta L_{t-1} >= beta L_{t-1}`. Componentwise, `|v_i| <=
sqrt(d_i) ||v||_*`; per mode `|(1+beta)h_k - beta h_k^-| <= (1+beta)|h_k| +
beta|h_k^-|`, and weighted Cauchy–Schwarz gives `((1+beta)A + beta B)^2 <=
((1+beta)^2 + beta^2/s_k)(A^2 + s_k B^2)`, so `||(1+beta)h_t - beta
h_{t-1}||_*^2 <= C_S * sum_k (h_k^2 + s_k h_k^{-2})`. Each underdamped mode
satisfies `V_k >= dn_k (h_k^2 + s_k h_k^{-2})` with `dn_k = 1 -
p_k/(2 sqrt(s_k)) >= dn_S` ((H-sep) makes every `k >= 2` underdamped and
`p/(2 sqrt s) = (1+beta) sqrt(m)/(2 sqrt(beta))` increasing in `m`). Chaining:
`max_i |(1+beta)h_{t,i} - beta h_{t-1,i}| / psi_i <= (1/m_psi) sqrt(C_S V_t /
dn_S) <= beta L_{t-1}` by (ii). Hence `u_t >= 0` on `S`, so `Delta_t = 0` (§1).
(b) *Propagation.* The stage being N keeps the linear recurrences exact; per
mode `V'_k = s_k V_k` (companion identity, verified in-engine as c9face
251/251), and `V_k >= 0` (underdamped) with `s_k <= s_2` give `V_{t+1} <= s_2
V_t`. The floor propagates by i5c Lemma D (`m_S >= 1-q_r^2`, Lemma C). Then
`R_{t+1} <= [s_2/(1-q_r)^2] R_t`, and `s_2 < (1-q_r)^2` strictly by (H-sep)
(§3). ∎

> **Corollary (reach = absorption; PROVED).** On a face segment starting at
> `t_0` with `L`-floor holding, either a correction occurs among the first
> `K := ceil( log R_{t_0} / log((1-q_r)^2/s_2) )` stages of the segment, or
> none ever occurs on the segment. In particular a no-correction prefix of
> length `K` upgrades itself to a never-triggering tail, unconditionally — no
> (Hgap), no F-stage bound, no P-stage certificate: **on an fm run the only
> stage type the induction ever meets is N, so the i2c/i4a Open links (P), (F)
> are vacuous inside this theorem's scope.**

**Where the trajectories actually enter the cone (Measured, float on the
`w^(8)`-split; exact arithmetic elsewhere).** Per cell: `t_lock` (face = S*),
`tcs` = first stage from which the *sharp* componentwise form
`max_i |(1+beta)h_t - beta h_{t-1}|_i/(beta L_{t-1} psi_i) <= 1` holds for the
rest of the run, `tc` = same for the certified norm form `R_t <= 1`:

| cell | t_lock | tcs | tcs - t_lock | tc | R at T (if > 1) |
|---|---|---|---|---|---|
| P12 | 60 | 65 | +5 | 188 | — |
| S16leaf | 3 | 10 | +7 | — (n_od=2, out of (H-sep) scope) | float underflow |
| cat5_2 | 21 | 25 | +4 | 57 | — |
| bt15root | 10 | 2 | (pre-lock) | 24 | — |
| cat4_3 | 70 | 74 | +4 | 151 | — |
| P18 | 78 | 83 | +5 | — | 9.96, decaying |
| P16 | 55 | 60 | +5 | 221 | — |
| P20 | 103 | 108 | +5 | — | 6.10, decaying |
| P24 | 123 | 129 | +6 | — | 2.62, decaying |

The sharp form enters within **<= 7 stages of face lock on every cell**; the
certified norm form pays `sqrt(d_max C_S/dn_S)/m_psi` (~10^3 on P24: `1/dn_S ~
227` from the near-critical second mode, spread `max w/min w = 14.7` in
`m_psi`) and on the three long paths has not yet decayed to 1 at the recorded
horizon — it decays at `s_2/(1-q_r)^2 ~ 0.989 < 1` per stage and extrapolates
to reach 1 at `t ~ 490` on P24. **The cone constant survives the Perron spread** (it enters
once, as `m_psi`), but the near-critical `1/dn_S` is the dominant, honest cost
of the norm route; the spread alone does not decide it.

## 5. The factorization bridge, refuted (both regimes)

The scalar telescoping `(E - z_+)(E - z_-) u = 0`, `u_{t+1} - z_- u_t =
z_+^t (u_1 - z_- u_0)`, would lift to matrices via `Z_pm := [(1+beta) Mm' pm
sqrt((1+beta)^2 Mm'^2 - 4 beta Mm')]/2` and need `Z_- >= 0` entrywise.

1. **Generic faces ((H-sep), 78/79 in the battery): `Z_pm` is not real.** The
   discriminant operator has modal eigenvalues `m_k((1+beta)^2 m_k - 4 beta)
   < 0` for every `k >= 2` (§3), so it is indefinite (exact inertia) and no
   real square root commuting with `Mm'` exists.
2. **All-overdamped faces (the S16-leaf lock, `n_od = |S| = 2`): `Z_-` is real
   but has strictly negative off-diagonal entries — PROVED.** For `|S| = 2`
   with simple modes `m_1 > m_2`, Lagrange interpolation gives `Z_- =
   z_-(m_2) I + [(z_-(m_1) - z_-(m_2))/(m_1 - m_2)] (Mm' - m_2 I)`; the
   divided difference is negative because `z_-` is *strictly decreasing* in
   `m` (§3), and `Mm'_{ij} > 0` off-diagonal, so `(Z_-)_{ij} < 0`.
   Numerically on that face: `Z_- = [[0.1381, -0.0134], [-0.0009, 0.1381]]`
   (and `Z_+ >= 0` entrywise, by the same argument with `z_+` increasing).
   The negative momentum term cannot be factored away entrywise even when the
   spectrum fully cooperates. **Route (b) dropped, with proof.**

## 6. Refuted candidate invariants (exact, the negative space of the proof)

* **CB1** `Y_t >= (1-q_r) Y_{t-1}` componentwise: **1545/1952** same-face
  stages, worst ratio **0.5539** (cat4_3) — the natural strong floor is
  *false* about a quarter of the time, while the `w`-functional floor
  `L^Y_t >= (1-q_r) L^Y_{t-1}` holds **1952/1952**. Never-triggering is
  genuinely modal-plus-bridge, not a componentwise geometric decay: any
  componentwise induction (sibling route) must target the `sigma = (1-q_r)/2`
  floor, **not** the `(1-q_r)` floor.
* **CJ** `u_t >= 0` on `S_{t+1}` (incoming face): fails at **21/2041** stages
  (all at activations). The induction cannot carry `u >= 0` across the growing
  boundary; the activation lemma (§2) is what actually holds there.
* The naive componentwise induction threshold `min_i (Mm' Y)_i / Y_i >=
  1-q_r^2` is a Collatz–Wielandt *upper*-bound violation for any non-Perron
  `Y` (CW: `min_i <= m_S`), with margin `m_S - (1-q_r^2)` measured 0.3–0.6 %
  — there is no slack for a fixed-cone argument; only the trajectory-adapted
  pair-cone of §4 closes.

## 7. Never-triggering: assembled statement and corollary

> **Lemma (never-triggering, spectral scope).** For the fm recurrence with the
> i5c certified calibration, `alpha <= 1/5`: (0) `Delta_0 = Delta_1 = 0`
> (proved, §2); (a) coordinates entering any face never trigger at entry
> (proved, §2); (b) on every face segment satisfying (H-sep) whose entrance
> data satisfies (i)+(ii) of §4, no stage of the segment triggers (proved);
> (c) on every face segment a no-correction prefix of explicit length `K`
> forces never-triggering on the whole remaining segment (proved). The
> remaining unproved step is exactly: **the entrance data of each of the
> <= |S*| face segments satisfies the certificate** (equivalently: the
> pre-lock, pre-`tcs` stages do not trigger) — verified exactly at 2041/2041
> stages, 79/79 faces, 89/89 activations, but not yet a lemma.

> **Corollary (Route-B, conditional).** In the lemma's scope `J_T^fin = 0`
> exactly on the never-triggering range: every stage is N, `r_t = 0`,
> `Dfin_t = 0`, `gamma_t = 1`; the Route-B packing holds with `c = 1` and `B`
> = the single initialization re-tune jump (i5c §5), on this variant, under
> (H-sep) + entrance hypotheses. No claim about `eps_ppr` output semantics;
> this is the RPPR surrogate's inflation ledger.

Hypotheses, separated: **algorithmic** — fm calibration (Lemma C upper-CW
bracket, `q_r`-grid), face-aligned cap irrelevant here (never-trigger is
cap-free, §1); exact solves. **structural** — `alpha <= 1/5` (base case);
(H-sep) `lam_2^S > kappa q_r^2/(1-q_r^2)` per face (exact inertia certificate;
78/79 faces; the one violator is all-overdamped, where a two-block variant of
§4 with `z_+(m_2) < z_+(m_S)` replacing the V-form is the natural extension —
not written out); entrance certificate (open).

## 8. Interface for merging with I6-A1 (componentwise induction)

What the sibling needs to prove, in this note's variables, is exactly:

```
(GAP)  for the <= |S*| + t_lock-bounded prefix stages of each face segment:
       Y_t >= [(1-q_r_t)/2] Y_{t-1}  componentwise on S_t .
```

My route supplies, for free, to any such induction: the base case `t <= 1`;
the entering coordinates (activation lemma, beta-free); `Y_t >= 0` on `S_t`
and `Y_t <= 0` off `supp(x_t)` (sign frame); the guarantee that the induction
only ever meets N stages so the linear dynamics (D1)–(D3) are exact; and the
handoff: once the componentwise induction reaches `tcs` (= `t_lock + <= 7`
measured), §4 takes over *permanently* with a proved self-propagating
certificate. Conversely the sibling's induction, if it closes, discharges my
only open hypothesis. The two proofs compose rather than overlap: mine is the
tail and the boundary, theirs is the bulk prefix. Warning to the merge: do
NOT attempt the `(1-q_r)` componentwise floor (refuted, §6) or `u >= 0` on
`S_{t+1}` (refuted, §6); the correct componentwise target is the `sigma`-floor
(GAP), which is *equivalent* to never-triggering, so their induction must
strengthen it by a genuinely different invariant (my §4 cone is one; theirs
will be another).

## 9. Evidence labels

**Proved-draft:** trigger reformulation (§1); dynamics identities (D1)–(D3);
activation lemma; `t <= 1` base case (`alpha <= 1/5`); modal overdamping
structure incl. `z_+` monotone, underdamped modulus `< 1-q_r`, and
`n_od = 1 <=> s_2 < (1-q_r)^2`; the §4 propagation theorem + reach corollary;
the §5 refutation of `Z_-` (both regimes). **Verified exactly:** T0/CA/CAoff/
CC/CG 2041/2041 each; CNEW 89+89/89+89; `L^Y`-floor 1952/1952; inertia 79/79
faces; identity checks A1–A5 200/200 each. **Measured (float):** the
`w^(8)`-split certificate table of §4 (tcs, tc, R-decay); spread/`dn_S`
overhead decomposition. **Refuted-draft:** task-sheet Step 1 as written
("every mode overdamped"); CB1; CJ; the entrywise factorization bridge.
**Open:** the entrance certificate (GAP) — the single missing step; the
two-block extension for all-overdamped faces; rational-certified `dn_S`, `s_2`
brackets (currently float; the exact inertia already certifies their signs).
