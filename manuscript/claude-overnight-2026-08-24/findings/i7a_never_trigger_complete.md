# I7-A — Never-triggering, composed: CLOSED for the certified-warmup variant; REFUTED for the unmodified algorithm

**FINAL STATUS: COMPLETE-for-modified-algorithm, and the modification is
NECESSARY.** The two iteration-6 proofs compose into a complete
never-triggering theorem for a legally modified variant `fm-w` (certified
prox warmup after every face change — the task's option (ii), instantiated
with beta held at 0 rather than at its previous value). Every stage class of
`fm-w` is covered by a proved lemma; the single previously-open step (the
ENTRANCE LEMMA) is closed by a new warmup-contraction argument, and the
composed theorem needs *neither* the `alpha <= 1/5` base-case restriction
*nor* (H-sep) as an assumption (the latter becomes an exact-rational
algorithmic *gate*). Simultaneously, the fresh adversarial cell **rt22b
refutes the unmodified lemma**: literal `fm` fires its trigger at stage
`t = 13` (exact rationals, `Delta = 2.6e-3`, class F), three stages after
face lock — precisely the young-face transient that A1's tau-floor
near-failures (ratio 0.9926 on rt16b) warned about. The entrance gap was not
a proof deficiency; it was a real hole in the *statement*. The corrected
statement is the theorem below.

Code: `w7_windowed/i7a_fmw.py`; data `w7_windowed/i7a_out/*.json`. Exact
Fractions for every load-bearing predicate (NF, YPOS, CMP, KKT, UID, inertia
gate, lam_2 bisection); float only for the modal certificate *measurements*
(R, sharp, L-floor, R-decay) and for the integer warmup length J.

---

## 1. The modified algorithm `fm-w`

Identical to i5c's `fm` (face cap `w^(8)`, certified per-face `(q_r, beta)`
from the upper CW bracket, exact obstacle solves) except for the momentum
schedule. With `S_t := supp(x_t) ∪ supp(d_t)` and `stable_t` = number of
consecutive completed solves with `S` unchanged:

```
beta_t = beta(S)  if  stable_t >= J_S  and  GATE(S) passes,   else  beta_t = 0.
```

* **GATE(S)** (exact rational, per connected component of S): with
  `crit = kappa q_r^2/(1-q_r^2)`, require `inertia_le(Qt_C - crit*D_C) = 1`
  (exactly one mode at or below crit — A2's (H-sep), now *checked, not
  assumed*) and a strict bracket `lam_2 > th_lo > crit` from ~12 rounds of
  exact-inertia bisection. Fails ⟹ that face runs prox-only (`beta = 0`),
  which is unconditionally safe (§2, P-B). The one battery face that ever
  fails it is the S16-leaf all-overdamped lock face — the known (H-sep)
  violator, now handled by the gate instead of being an unproved exception.
* **Warmup length** (per component, `J_S` = max):

```
J_S = 1 + ceil( log(R0)/ (2 log(1/mu+)) ),        mu+ = m2+/(1-q_r^2) < 1,
R0  = C_S A_S^2 / (4 dn-_S m_psi^2 beta),         m2+ = kappa/(kappa+th_lo),
A_S = ||psi||_*^2 / m_psi,   m_psi = min_i psi_i/sqrt(d_i),  psi = Perron dir,
dn-_S = 1 - (1+beta) sqrt(m2+) / (2 sqrt(beta)) > 0,
C_S = (1+beta)^2 + beta (kappa+1)/kappa          (s_min >= beta*kappa/(kappa+1)).
```

## 2. The composed theorem and its proof

> **Theorem (never-triggering, complete, `fm-w`).** For the RPPR obstacle
> recurrence with exact solves, start `x_{-1} = x_0 = 0`, face cap, certified
> calibration, gate and warmup as above: **every stage of every run has
> `Delta_t = 0`** — no corrections, no retractions, every stage is N,
> `gamma_t = 1` and `J_T^fin = 0` exactly. No hypothesis on `alpha in (0,1/2)`
> beyond `kappa > 0`; no properness/interiorness hypothesis; disconnected
> faces handled per component (all operators block-diagonalize).

Proof components (P-A–P-E), each with its verification:

**P-A (LCP subsolution comparison — new lemma, closes the prox class).**
Let `A = Qt + kappa D` (strictly diagonally dominant Z-matrix: row margin
`d_i(1-alpha) > 0`, hence M-matrix), and let `x` solve the LCP
`x >= 0, Ax - r >= 0, x^T(Ax - r) = 0`. If `v >= 0` satisfies
`(Av - r)_i <= 0` wherever `v_i > 0`, then `x >= v`.
*Proof.* Let `E = {i : v_i > x_i}` and `y = v - x`. For `i in E`: `v_i > 0`
so `(Av)_i <= r_i`; and either `x_i > 0` (so `(Ax)_i = r_i`) or `x_i = 0`
(so `(Ax)_i >= r_i`); both give `(Ay)_i <= 0`. Off `E`, `y <= 0`, and
`A_{E,E^c} <= 0`, so `A_{EE} y_E <= -A_{E,E^c} y_{E^c} <= 0`; multiplying by
`A_{EE}^{-1} >= 0` (M-matrix principal submatrix) gives `y_E <= 0`,
contradiction unless `E` is empty. ∎
Applied with `v = a_t`, `r = ct + kappa D a_t`: **never-fire at `t`
(`zeta(a_t) >= 0` on `supp(a_t)`) implies `x_{t+1} >= a_t >= x_t`.** The
monotone invariant is thus *self-sustained along the induction* rather than
imported. Verified: CMP `x_{t+1} >= a_t` exact at **3 840/3 840** cert
stages (and its predicted failure at the one fired J2 stage — see §4).

**P-B (prox stages never fire — unconditional).** If stage `t` never fired,
then by P-A and KKT, `Y_{t+1} := ct - Qt x_{t+1} = kappa D (x_{t+1} - a_t)
>= 0` on `supp(x_{t+1})`. A stage with `beta = 0` has `a = x`, so its trigger
vector is `zeta(a_{t+1}) = Y_{t+1} >= 0` on `S_{t+1} = supp(x_{t+1})`: it
cannot fire. Covers: `t <= 1` (kills A2's `alpha <= 1/5` base case), every
face-change stage, every warmup stage, entering coordinates (activation
lemma subsumed), and prox-only gated faces. Verified: YPOS exact
**3 821/3 821**, NF at prox stages **3 269/3 269** (cert battery).

**P-C (cone bound — a priori entrance mass).** For any `Y >= 0` on `S`
(*-inner product `<u,v>_* = sum u_i v_i / d_i`, Perron direction `psi > 0`):
`<psi, Y>_* >= m_psi * ||Y||_{*,1} >= m_psi ||Y||_*`, hence the Perron
coefficient `L` and orthogonal part `h` of any nonnegative state satisfy
**`||h||_*/L <= ||psi||_*^2/m_psi = A_S`.** (One line; ell1 >= ell2.)

**P-D (warmup contraction and the ENTRANCE LEMMA — the gap, closed).** On a
stable face, a prox solve maps `Y -> Mm'_S Y` (`Mm' = kappa D (Qt_S +
kappa D_S)^{-1}`), so modal coordinates contract as `L' = m_S L`,
`h'_k = m_k h_k`, giving `(||h||/L) *= m_2/m_S <= mu+ := m2+/(1-q_r^2) < 1`
per warmup stage (Lemma C gives `m_S >= 1-q_r^2`; the gate's bisection gives
`m_2 <= m2+ < 1-q_r^2`). At the first momentum stage `t* = r + J_S` (face
entered at `r`, `J_S - 1` contracting solves, plus `h_{t*} = m h_{t*-1}`
from the last one):
`V_{t*} = sum_k beta m_k (1-m_k) h_{t*-1,k}^2 <= (beta/4)||h_{t*-1}||^2`,
so `R_{t*} <= C_S A_S^2 mu+^{2(J_S-1)} / (4 dn_S m_psi^2 beta) <= 1` by the
choice of `J_S`, and the L-floor holds (`L_{t*} = m_S L_{t*-1} >=
(1-q_r^2) L_{t*-1} > 0`; the degenerate branch `Y_r|_S = 0` is stationary
and trivially never fires). **This is the entrance certificate A2 §4 (i)+(ii),
proved at every segment entrance.** Two structural remarks: (a) the identity
`mu+ = s_2/(1-q_r)^2` (exact algebra: `beta(1-q_r^2) = (1-q_r)^2`) says a
warmup stage contracts the certificate ratio at exactly A2's per-stage
R-decay rate but *squared per stage* — the warmup is A2's reach-corollary
prefix `K` spent where never-firing is free, at half length; (b) nothing
here needs `x*`, properness, or a global spectral assumption.

**P-E (segment tail — A2's fixed-face propagation theorem, unchanged).**
From `t*` on, (i)+(ii) self-propagate with ratio `s_2/(1-q_r)^2 < 1`
(strict, by the gate) and force `Delta = 0` at every remaining stage of the
segment; a mid-segment face change hands control back to P-B. Per-component
application is licensed by block-diagonality. ∎

**Corollary (Route B).** On `fm-w`, `J_T^fin = 0` *exactly and
unconditionally*: every stage is N, `r_t = 0`, `Dfin_t = 0`, `gamma_t = 1`;
the Route-B packing target holds with `c = 1` and `B` = the i5c §5
initialization jump. The i2c/i4a open links (P), (F) are vacuous on this
variant. (RPPR surrogate ledger only; no `eps_ppr` output-semantics claim.
Warmup cost: `sum_S J_S` extra prox stages, each charged as usual.)

## 3. The unmodified lemma is FALSE: the rt22b counterexample

`rt22b` = random tree, `n = 22` (seed 11), seed vertex 5, `q = 1/28`,
`rho = 1/96` (interior: `|S*| = 22`). Literal `fm` (i5c code, exact
rationals): admission burst `t = 1..10` with a face change at *every* stage
(sizes 4→22), lock at `t = 10` with an upward beta re-tune
(`beta: 227/273 -> 27/29`), then

```
t = 13  (lock face 3 stages old):  zeta(a_13)_8  = -2.50e-6 < 0,
                                   zeta(a_13)_10 = -3.32e-6 < 0,
        Delta_13 = 2.61e-3 > 0,  class F (full retraction), exact rationals.
```

The same cell under `fm-w`-cert: **NF 160/160** (and 400/400 in the long
run, §4). Under `fm-w` with a deliberately too-short warmup (`J = 2`): fires
once at `t = 34`, eleven stages into the lock segment, whose momentum
entrance measured `sharp = 1.97 > 1`, `R = 305` — the uncertified-entrance
scenario realized. Placement of the old evidence: A1's two tau-floor
failures (rt16b `t=3` ratio 0.9926; cat4_3 `t=75` ratio 0.841) were this
mechanism surviving by luck; K8ctl (the only firing cell known before
tonight) is the same disease (`fm` fires; `fm-w`-cert: entrance `R = 0.257
<= 1`, NF 30/30). The never-triggering of `fm` on the 12-cell i6 battery was
a property of that battery, not of the algorithm.

## 4. Verification (exact unless labelled float)

**Battery: 19 cells** = 9 i5c proper cells + K8ctl + 4 A1 fresh cells
(P24rho2, P24rho3, rt18, rt16b) + **5 new adversarial short-segment cells**
(rt20a, rt22b, P30lr, cat6_2, bt31 — rapid admission, small rho; screened:
rt22b has 11 face changes in 24 stages, P30lr 27 changes). Both transient
cells from A1 (rt16b, cat4_3) included. Per-inequality counts, `fm-w`-cert:

| check (exact) | count | note |
|---|---|---|
| NF `Delta_t = 0` | **3 840/3 840** | all 19 cells, incl. K8ctl and rt22b(T=400) |
| YPOS `Y_t >= 0` on `supp(x_t)` | 3 821/3 821 | P-B premise |
| CMP `x_{t+1} >= a_t` | 3 840/3 840 | P-A conclusion |
| KKT identity on `supp(x_{t+1})` | 3 840/3 840 | |
| UID `zeta(a_t) = (1+beta)Y_t - beta Y_{t-1}` on `S_t` | 3 821/3 821 | A2 §1 identity |
| GATE inertia certificates | all momentum faces | S16 lock face correctly rejected (n_od = 2) |

Momentum coverage (cert): **571 momentum stages across 8 cells** (rt22b-400
228, bt15 118, bt31 69, cat5_2 50, cat4_3 44, rt16b 39, K8ctl 21, rt18 2),
**0 fires**; entrance certificate (float): `R_{t*} <= 1` at **8/8** first
momentum stages (largest `R = 0.26`), sharp form <= 1 at 8/8, L-floor
571/571, R-decay `R_{t+1} <= (s_2/(1-q_r)^2) R_t` at 100% of checkable
pairs (227/227 on rt22b-400) except float-underflow noise on bt15/bt31
(state error ~1e-21 — exact-arithmetic claim unaffected). **The decisive
exhibit — rt22b-cert `T = 400`: the certified warmup (`J = 149`) ends and
momentum engages at `t = 172` on the counterexample's own lock face,
entrance `R = 1.7e-4`, then 228 consecutive momentum stages with
NF 400/400** — the modified algorithm provably-and-verifiably does what the
original provably cannot. K8 formula audit: predicted bound
`R0 mu+^{2(J-1)} ~ 0.80`, measured `R_{t*} = 0.257`.

Control (`fm-w` with `J = 2`, same gate): NF **3 599/3 600** — the single
fire is rt22b `t = 34` above; 183 momentum entrances, `R <= 1` at 0/183
(norm certificate violated at every one), sharp <= 1 at 176/183; **all 176
sharp-certified entrances launched fire-free segments; the one fire came
from a sharp-violating entrance.** Original `fm` on the 4 new cells:
rt20a/cat6_2/P30lr never fire in 120 stages; rt22b fires at `t = 13` (§3).

## 5. What remains open (honestly), and what is dead

1. **Certified online computation of `J_S`** (engineering, not mathematics):
   `J_S` needs upper brackets on the Perron functionals `A_S, 1/m_psi` —
   implemented tonight via the exact-rational `w^(8)` proxy; entrywise
   certified Perron brackets (standard M-matrix technology) are the missing
   piece, and enter only inside a log. The theorem itself quantifies over
   the true constants and is complete.
2. **The certified `J_S` is large on near-critical faces** (paths: 86–900;
   trees/caterpillars/K8: 8–86), because the *norm-form* certificate pays
   `A_S^2/dn_S` — mirror of A2's `tc` data. Within the battery horizons the
   path family therefore ran prox-only under cert (still 0 fires — P-B), and
   convergence there matches prox, not accelerated momentum: err(fm-w-cert)
   ~1e-2 vs err(fm-w-J2) ~1e-6 at equal T on P12–P24. **The residue for
   *practical* acceleration-with-complete-proof is exactly: prove the SHARP
   componentwise certificate propagates** (empirical record now
   176/176 + A2's `tcs = t_lock + <= 7`), which would shrink `J_S` to O(1).
   It is one cleanly stated inequality; the refuted-invariants lists of A1
   §5/A2 §6 fence off the approaches that cannot work.
3. All-overdamped faces (gate failure): prox-only forever is safe and
   convergent (rate `m_S`), so never-triggering is closed; the two-block
   momentum extension remains unwritten and is now optional.
4. The unmodified `fm` never-triggering lemma: **dead** (rt22b). Do not
   revive; any future statement must carry an entrance condition.
5. Inexact inner solves: unchanged scope note from A1 §7 — all conclusions
   degrade to `Delta_t = O(eps_in)`.

## 6. Evidence labels

**Proved-draft:** P-A (new, complete proof above); P-B; P-C; P-D (entrance
lemma, closed); the composed theorem and Route-B corollary (P-E cites A2 §4,
proved there); the `mu+ = s_2/(1-q_r)^2` identity; gate correctness
(exact inertia).
**Verified exactly:** the §4 table (3 840 cert + 3 600 J2 + 480 fm stages);
the rt22b counterexample (exact rationals, reproducible:
`run_i5c(Inst(rt22b), 20, 'fm')`).
**Measured (float):** R/sharp/L-floor/R-decay values; J-formula audit.
**Refuted-draft:** the unconditional never-triggering lemma for unmodified
`fm` (rt22b, stage 13); `J = 2` warmup sufficiency (rt22b, stage 34).
**Open:** items 1–3, 5 of §5.
