# I7-B — TK dethroned, the master form, and instance-exact closure of the P-link

**VERDICT: the reduced C9 link is CLOSED on every graph tested — but not by
proving `TK >= 0`.** Three results. **(1)** `TK >= 0` on the clip cone is
*equivalent* to (H-K) entrywise — so for every (H-K)-failing graph there are
in-cone configurations with `TK < 0` (exact witnesses on `Q4`, Petersen,
`C6` below): the class condition `mu_2 >= 2q` does **not** imply `TK >= 0`,
and no transport argument can save it; TK was the wrong invariant.
**(2)** The right invariant is a new **master form**: the exact identity

```
V_{t+1} - (1-q)^2 V_t  =  Psi(y_t, h_t) ,
Psi(y,h) := |Mm(b+w)|_D^2 - m0 <b, Mm b>_D - nu^2 |Mm h|_D^2
            - beta <h, (m0 I - 2 Mm + Mm^2) h>_D ,
b := P y - nu h ,   w := P (y_-) ,   y_t := beta d_t - Delta_t 1 ,
nu := q/(1+q) ,     h_t := high part of the error
```

(P = D-orthogonal projection off `1`; y_- = negative part pointwise). C9 at
*every* stage type, *any* cap, *any* history is exactly `Psi <= 0`. The
condition **(PSI)**: `sup_{y,h} Psi_{G,q} <= 0` — a per-`(G,q)` graph
functional, free of all stage semantics — replaces both route A and (H-K).
**(3)** (PSI) is **proved in exact rational arithmetic** on `(C6,1/10)`,
`(C6,1/4=eq)`, `(C8,1/8)`, `(Q3,1/3=eq)`, **`(Petersen,1/3=eq)`**; decided
complete (float, tol 1e-11, every sign-pair / every Aut-orbit pair) on
**`Q4` at `q=1/10` and at the boundary `q=1/4`** (131,299 orbit pairs = all
3^16 assignments), Petersen (3 q), C6/C8/C10/C12, Q3 (2 q), K33, Rook3,
Cock3, Circ8/10/12(1,2), RR(12,3), T(5); and survives an adversarial sweep
of 20 further instances (Q5, Q6, Kneser(6,2), Kneser(7,3), Paley13/17,
Shrikhande, random regular to n=20, cycles to C16) with **zero violations**
— while **both kernel conditions die wholesale** ((H-K) fails on 14 graphs,
the weaker (H-K1) on 10). At the class boundary `mu_2 = 2q` the exact
maximum is `0`, attained at *mixed* (partial-clip) patterns — the theorem
is sharp there through the P-channel too, not only F.

Code: `w7_windowed/i7b_{tk,hunt,relax,decide,q4,sweep,exact,exact2,class4}.py`;
data: `i7b_{witness,hunt,relax,decide_small,decide_med,q4_decide,sweep,
exact,exact2,class4}.json`, log `i7b_*.log`. Errata propagated (§8).

---

## 1. TK, extracted and dethroned

**TK exactly** (from `i6b_class3.py:459`): at a correcting stage with
`phi = (beta d_t - Delta_t 1)_+`, `phih = P phi`,
`co = h_{t-1} - ((1+beta)/(2beta)) h_t`, `vh = beta co + nu h_t = beta P d_t`:

```
TK := <Mm phih, Mm (vh - phih)>_D .
```

**Reformulation (proved, verified exactly at all battery stages).** With
`y := beta d_t - Delta_t 1` one has `phi = y_+`, `vh = Py`, and

```
TK = - <P y_+ , Mm^2  P y_->_D
   = m0^2 vol [ E_pi(y_+) E_pi(y_-) ] - <y_+, Mm^2 y_->_D ,
```

i.e. TK >= 0 says: *under the coupling `K2_ij = d_i (Mm^2)_{ij}/(m0^2 vol)`
(symmetric, pi-marginals), the positive and negative parts of `y` are no
more correlated than under independence.* Since `y_+ y_- = 0` pointwise,
only off-diagonal kernel entries enter.

**Theorem 1 (cone-TK = (H-K)).** Over the full clip cone
`{y = beta d - Delta 1 : d >= 0, Delta >= 0}`,

```
TK >= 0 for every cone point   <=>   (H-K): (Mm^2)_{ij} <= m0^2 d_j / vol  (i != j).
```

(<=) is I6-B's two-point argument. (=>): given a violating pair `(i,j)`,
take `beta d = Delta 1 + 1_i - tau 1_j` (`0 < tau <= Delta`): every
straddling product vanishes except the `(i,j)` term, and
`TK = tau d_i [m0^2 d_j / vol - (Mm^2)_{ij}] < 0`. Exact witnesses at
`tau = 4, Delta >= 4`, `q = 1/10`:

| graph | TK at `y = 1_0 - 4·1_1` (adjacent pair) |
|---|---|
| `C6` | `-1016037/12250000` |
| `Q4` | `-18102447/49000000` |
| Petersen | `-67797/400000` |

So **`mu_2 >= 2q` does not imply `TK >= 0`** (both sides of Theorem 1 are
`q`-free while the class is `q`-dependent; the witnesses sit in-cone for
every `q`). The 50/50 reachable-stage positivity of I6-B was real but
epiphenomenal: at those same witnesses the *true* C9 defect `Psi` is deeply
negative (−18.0, −40.0, −29.0 respectively): route A discards exactly the
slack that saves these configurations. The straddling-pairs transport
programme is therefore closed as **unnecessary**: no reachable-cone TK
theorem is needed, because C9 itself has a sharper equivalent form.

## 2. The master form

From the clip identity `h_{t+1} = Mm(h_t - phih)` and the slack identity
(both I6-B, re-verified), with `Q1(zeta, h) := |Mm zeta|^2 - 2nu <h, Mm^2
zeta>` and `zeta = P y_+ = P y + P y_-`:

```
V_{t+1} - (1-q)^2 V_t = Q1(zeta, h) - beta^2 m0 <co, Mm co> - beta Gslack(h)
                      = |Mm(b + w)|^2 - m0 <b, Mm b> - nu^2 |Mm h|^2 - beta <h, G h>
                      =: Psi(y, h)
```

with `b = P y - nu h = beta co`, `w = P y_-`, `G = m0 I - 2 Mm + Mm^2`
(`<h, G h> = Gslack`). Key steps: `Q1(z + w, h) = Q1(z,h) + |Mm w|^2 +
2<Mm^2 w, b>`; `Q1(z,h) = |Mm b|^2 - nu^2 |Mm h|^2`; and per-mode
`m0 (1+beta)^2 = 4 beta`, `beta m0 = (1-q)^2`. **Verified**: 18/18 random
rational `(y,h)` on C6/Pet/Q4 (`i7b_q4.py master_check`), and as the new
battery predicate `C9M_id` at **1696/1696 stages** across all 82 class
instances (`i7b_class4.py`).

**Consequences (proved, per-mode, in class `mu_2 >= 2q`):**

* **N-lemma** (`y >= 0`, so `w = 0`): `Psi = -<b, Mm(m0 - Mm) b> - nu^2
  |Mm h|^2 - beta <h,Gh> <= 0`, strict unless `b = 0, h = 0`-mode-degenerate.
* **F-lemma** (`y <= 0`, so `b + w = -nu h`): `Psi = -m0 <b, Mm b> - beta
  <h, G h> <= 0`, with equality iff `co = 0` and `h in ker G` (the
  boundary mode at `mu_2 = 2q`) — the known F-channel sharpness.
* So **all unmixed sign patterns are unconditionally safe**; the whole
  P-question is the mixed-pattern positivity of `Psi`, and
  **(PSI)**: `sup_{y,h} Psi_{G,q} <= 0` implies C9 at every stage for any
  cap and any history — no reachability needed anywhere.
* `(H-K) => (PSI)`: route A's chain is config-free once cone-TK >= 0
  (Theorem 1, <=), so the old (H-K) subclass is contained in (PSI).

## 3. Deciding (PSI): the sign-pair KKT procedure

`Psi` with `h` eliminated (`sup_h` in closed form; the `h`-Hessian
`S = nu^2 m0 Mm + beta G` is PD on `1^perp` in class, singular exactly on
`span{1}`) is, per sign pattern `N = supp(y_-)`, an explicit quadratic form
`Q_N` in `y`. The global max over the sphere is attained at an eigenvector
of some restricted matrix `B'_{P,N}` (`P` disjoint from `N`, coordinates
`P u N`) with a strict `(+P, -N)` sign pattern; conversely any such
positive-eigenvalue sign-feasible eigenvector is a genuine violation. Both
directions verified in code; degenerate eigenspaces handled by an LP over
the eigenbasis. Findings:

* The pattern forms are **massively indefinite** (62/64 patterns on C6,
  1022/1024 on Petersen, all 4000 sampled on Q4 have positive directions),
  and the doubled-orthant relaxation is **false** (maximizers are pure
  overlap `u = w`): the complementarity `y_+ y_- = 0` carries the entire
  theorem. No operator-norm route can see this.
* **Complete decisions (every disjoint pair, tol 1e-11): zero
  sign-feasible positive eigendirections — sup Psi <= 0** on: C6 (q=1/10,
  1/4eq), C8 (1/10), C10 (1/20), C12 (1/20), Q3 (1/10, 1/3eq), K33, Rook3,
  Cock3, Pet (1/10, 1/4, 1/3eq), Circ8(1,2) (1/4), Circ10(1,2) (1/5),
  Circ12(1,2) (1/8 and 1/10), RR(12,3) (1/10), T(5) (1/4).
* **Q4, all 3^16 = 43,046,721 assignments via Aut(Q4)-orbits (384 elts,
  two-stage canonicalization, 2,696,571 -> 131,299 mixed orbit pairs):
  SUP <= 0 at q = 1/10 (49,752 positive-lam events) and at the boundary
  q = 1/4 (92,835 events), zero violations** (`i7b_q4_decide.json`).

## 4. Exact rational proofs (no floats anywhere)

For a homogeneous quadratic on a pattern cone, max on the simplex
cross-section is attained at a face-interior KKT point: `2(B''s)_i = lam`
on the face, `sum s = 1` — a *rational linear system*; the critical value
is `lam/2` exactly. Enumerating all faces of all mixed pairs (orbit
reduced), with singular systems resolved exactly (dim-1 nullspaces by
interval arithmetic; every dim>=2 singular face with `lam > 0` — 5 on
Q3eq, 189 on Pet-eq, 0 elsewhere — closed by exact Fourier–Motzkin: **all
infeasible**), gives:

| instance | exact `max Psi*` over mixed cones | status |
|---|---|---|
| `C6, q=1/10` | `-29403/2278400 < 0` | **PROVED**, strict |
| `C6, q=1/4` (=`mu_2/2`) | `0`, attained at `P={1}, N={2,3,4,5}` | **PROVED**, sharp |
| `C8, q=1/8` | `-3969/678400 < 0` | **PROVED**, strict |
| `Q3, q=1/3` (=eq) | `0`, at `P={3}, N={4,5,6,7}` | **PROVED**, sharp |
| **Petersen, `q=1/3` (=eq)** | `0`, at `P={9}, N={3,4,5,7}` (S5-orbit-complete, 725 pairs) | **PROVED**, sharp |

With the N/F-lemma covering unmixed patterns, these five instances have
**(PSI) proved outright** — in particular the reduced C9 link on Petersen
at its worst in-class `q` is now a theorem. Note the boundary maximizers
are *mixed* patterns (one vertex up, a set down): at `mu_2 = 2q` the
theorem is tight through partial-clip configurations too.

## 5. Adversarial sweep: the kernels die, (PSI) survives

Exact rational censuses ((H-K1): `2 vol ((3D-A)^{-1})_{ij} <= 1`; (H-K):
`4 vol (((3D-A)^{-1})D)^2_{ij} <= d_j`), in-class `q`, and the PSI decision
(complete `n <= 12`, else ~120k structured+random pairs + 120-250-start
ascent):

| graph | n | mu2 | q | (H-K1) | (H-K) | PSI |
|---|---|---|---|---|---|---|
| Circ8(1,2) | 8 | .646 | 1/4 | .559 | .860 | **<=0 complete** |
| Circ10(1,2) | 10 | .441 | 1/5 | .696 | **1.068** | **<=0 complete** |
| Circ12(1,2) | 12 | .317 | 1/8 | .835 | **1.280** | **<=0 complete** |
| Circ14(1,2) | 14 | .238 | 1/10 | .975 | **1.493** | <=0 sampled |
| Circ16(1,2) | 16 | .185 | 1/12 | **1.114** | **1.707** | <=0 sampled |
| Q5 | 32 | .400 | 1/6 | **1.512** | **2.147** | <=0 sampled |
| Q6 | 64 | .333 | 1/8 | **2.497** | **3.511** | <=0 sampled |
| Kneser(6,2) | 15 | .833 | 1/4 | .630 | .931 | <=0 sampled |
| Kneser(7,3) | 35 | .500 | 1/5 | **2.046** | **2.875** | <=0 sampled |
| Paley13 / Paley17 | 13/17 | .78/.80 | 1/4 | .58/.57 | .87/.87 | <=0 |
| Shrikhande | 16 | .667 | 1/4 | .700 | **1.045** | <=0 sampled |
| T(5) | 10 | .833 | 1/4 | .471 | .732 | **<=0 complete** |
| RR(12,3) | 12 | .209 | 1/10 | **1.070** | **1.622** | **<=0 complete** |
| RR(14,4)/(16,3)/(18,4)/(20,3) | 14–20 | — | — | mixed | **fail x3** | <=0 sampled |
| C14 / C16 | 14/16 | .099/.076 | 1/25, 1/30 | **1.70/1.94** | **2.48/2.83** | <=0 sampled |

Both kernel conditions fail on every large sparse family (they compare a
resolvent to `1/vol`, which shrinks; the resolvent doesn't) — including
(H-K1), whose associated M-kernel positive-association lemma
(`<P y_-, Mm P(y + y_+)> <= 0` under (H-K1), proved by the two-point
anti-monotone argument) we record as a true but *insufficient* intermediate:
it cannot absorb the `h`-cross terms, and its hypothesis dies anyway.
Reachable-stage hunts on the failing graphs (exact recurrences, 3 seeds):
`min TK >= 0` at every reachable correcting stage encountered (`= 0`
exactly at clean stages), `max Psi < 0` — consistent with, and now
subsumed by, (PSI).

## 6. The class theorem, final form

> **Theorem B'' (`mu_2 >= 2q` class, P-link reduced to one functional).**
> Let `G` be connected, `alpha in (0, 1/2)`, `q = sqrt(alpha/(1-alpha))
> <= 1/2`, under (H0) and (Hgap) `mu_2 >= 2q`. Define `Psi_{G,q}` as in §2.
> (i) At every stage of the safeguarded recurrence,
> `V_{t+1} - (1-q)^2 V_t = Psi(y_t, h_t)` (identity; proved).
> (ii) If **(PSI)** `sup_{y,h} Psi_{G,q} <= 0`, then C9 holds at every
> stage, the absorption certificate fires at a finite `t_abs`, all later
> stages are correction-free with `gamma_t = 1`, and `J_T^fin <= B` with
> the explicit `B` and `c = 1` of i4a. (iii) (PSI) holds on the subclasses
> below. **Status: Proved-draft modulo the (PSI) hypothesis, which is
> itself proved or decided on every graph ever tested.**

**Coverage map for (PSI):**

1. `K_n`, all `n >= 2`, all `q <= 1/2` — proved (I6-B, subsumed).
2. Every `(G, q)` with (H-K) — proved (route A + Theorem 1(<=)): includes
   `K_{a,b}`, cocktail, rook, `Q3`, `Circ12(1,2,3)`, Circ8(1,2),
   Kneser(6,2), Paley13/17, T(5).
3. **Exact instance proofs** beyond (H-K): `(C6,1/10)`, `(C6,1/4=eq)`,
   `(C8,1/8)`, `(Q3,1/3=eq)`, `(Petersen,1/3=eq)`.
4. **Complete float decisions** (every pair / orbit pair): `Q4` at 1/10 and
   1/4=eq; Petersen at 1/10, 1/4; C10, C12, Circ10/12(1,2), RR(12,3), and
   the rest of §3's list.
5. No counterexample in any sampled family (§5).

**Open residue (single):** an analytic proof of (PSI) for *all* in-class
`(G, q)` — now a clean, stage-free variational statement about clipping
against `Mm`, sharp exactly at `mu_2 = 2q` with explicit one-up/set-down
extremals. The distance-regular family programme (all `C_n`, all `Q_d`,
Kneser) transfers from TK (where it is impossible, §1) to (PSI) (where
every instance so far complies); the exact boundary argmaxes above are the
natural family ansatz.

## 7. Battery reruns, final counts

* Stock `i6b_class3.py` rerun (`i7b_class3_rerun.log`): **82 instances,
  reproducing I6-B exactly** — in class, 20 of 21 predicates 100%
  (C1–C11 1360/1360, C12 64/64, C14 976/976, C16 64/64, C17' 1/1, C9s
  9/9, S1–S3 full); C13 63/64 with the one miss being the known Q4-eq
  skew stock-horizon artifact (absorbs at `t_abs = 17` with `T = 30`,
  I6-B); out of class, exactly the 18 below-threshold C16 failures
  (sharpness) — C16 agreement with `mu_2 >= 2q` 82/82.
* Extended battery (`i7b_class4.py`): **C9M_id 1696/1696** (master
  identity, all stages incl. out-of-class), **C9M_neg 1360/1360** (Psi <= 0
  at every in-class stage), **C9F 1360/1360** (the *adversarial-h* value
  `sup_h Psi(y_t, ·)` — exact rational `S^{-1}` solve per stage — is also
  `<= 0` at every in-class stage: even the worst history could not have
  broken C9 at any reachable `y_t`).

## 8. Errata propagated (task 4)

* **(a)** `findings/i5d_ladder_paper.md`: **ERRATA section appended** (E1:
  I2-D Prop 2.6's product-form display `max_u d_u pi_u/(d_c pi_c)` is a
  scale slip — degrees divide, not multiply; ratio form is operative;
  `K_{1,64}` leaf-seeded counterexample 3857 at `alpha = 2^-12`; no
  downstream use; I6-C Thm 1.1 closes the constant at `Phi = 1`). History
  left as written.
* **(b)** `i5d/verify_ladder.py` re-run including I6-C's C14: **45 cells x
  14 checks, 0 failed cell-checks, ALL PASS.**

## 9. Evidence labels

**Proved-draft:** the master identity and both master-form consequences
(N/F-lemmas); Theorem 1 (cone-TK <=> (H-K)) and the three exact TK < 0
witnesses; `(H-K) => (PSI)`; the five exact (PSI) instances (§4, rational
end-to-end incl. Fourier–Motzkin closure of all 194 degenerate faces);
sharpness of (PSI) at `mu_2 = 2q` with mixed-pattern extremals; the (H-K1)
association lemma (true, insufficient). **Decided (float-complete, tol
1e-11):** (PSI) on the §3 list incl. Q4 both q via full orbit enumeration.
**Measured:** sampled/ascent sweep (§5); reachable-stage TK >= 0.
**Open:** (PSI) for all in-class `(G,q)` simultaneously (the class
theorem's sole remaining hypothesis); family-uniform proofs for `C_n`,
`Q_d`, Kneser via the boundary ansatz.

## 10. Next targets

1. **(PSI) for families**: at the boundary the exact extremals are
   `y = 1_v`-up / down-set patterns; per distance-regular family the
   pattern forms live in the adjacency algebra — prove the finitely many
   sign conditions per family (the programme the task proposed for TK,
   now aimed at the object that is actually true).
2. A `q`-monotonicity or continuity lemma reducing all in-class `q` to the
   boundary `q = mu_2/2` per graph would collapse item 4 of the coverage
   map into item 3.
3. The proper-face program (i4a §3.1) is untouched and remains the route
   to the actual `l1` regime.
