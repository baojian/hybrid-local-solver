# I5-B — VGF-SP3: incremental solves across rounds, the (e')-gated stop, and what actually causes the round count

**Direction:** I4-E's stated next target, verbatim: *"SP3 — the incremental
factorisation that removes the round-count multiplier"*, plus tighter value
bounds via I4-F's (e') certificate, and the fan trap.

Code: `i4e/{vgf3.py, run_sp3.py, run_zoo3.py, run_fan3.py, fit3.py, smoke3.py}`
(new; `vgf.py` and everything earlier untouched).  Data/logs:
`i4e/out/{sp3,zoo3,fan3}.json`, `{sp3,zoo3,fan3}.log` (`*_v1.*` = pre-bugfix
runs, superseded).  Conventions, Meter (`DQMeter`), model, and verification
protocol identical to I4-E.  **444 charged runs; 0 unsound certificates and 0
missed `S_eps` vertices on every certified run; the only 4 non-certified runs
are 15-second WALL-caps of `v3E` on `grid3d`/`exp5reg` (reported as failures,
used nowhere).**

Mechanisms measured: `vgf` (I4-E, unchanged) · `v3` (VGF-SP3 core) ·
`v3E` (SP3 + (e') early stop) · `v3O` (SP3, oracle-stopped) · `push` ·
`composed` (I4-B).

---

## VERDICT

1. **SP3 as designed was built, and it does NOT kill the round-count
   alpha-exponent.  The i4e §10 prediction is REFUTED in its stated form.**
   The per-round full re-solve and full re-scan are gone (see §1: cached
   rows, a maintained one-signed residual, residual-driven *band* solves,
   incremental ring accumulators) — and the rounds barely move:
   path `R = 5→40` (vgf) vs `5→34` (v3) over `alpha = 2^-4 … 2^-14`;
   rounds-exponent `+0.30 → +0.28`.  Diagnosis (§3): the round count was
   never caused by re-solve *cost*; it is caused by the **one-hop reach of
   the value lower bounds**, and on path-like families the *residual band
   that must be re-lifted each round has volume `Θ(min(1/sqrt(alpha),
   vol(S)))` — the same scale as `vol(S)` itself* (`vol(S_eps) =
   Θ~(1/sqrt(alpha))` there).  Incremental factorisation can only shave the
   log factor between `vol(S)` and the band.
2. **It still buys a real exponent reduction, at a ~1.5–2x constant price.**
   Zoo median mechanism exponent `q` (`W/vol(S_eps) ~ alpha^-q`, 15 families
   × 3 alphas): **vgf +0.256 → v3 +0.197 → v3E +0.156**, max
   `+0.365 → +0.267`; oracle floor `v3O +0.104`.  On the worst families
   (6-point fits, `2^-4…2^-14`): path `+0.362 → +0.253` (v3) `→ +0.236`
   (v3E); spider `+0.363 → +0.281 → +0.153`.  In *absolute* work at
   `alpha ≥ 2^-12`, `vgf` is still cheaper on most benign families
   (`v3/vgf ≈ 1.2–1.9x`) — SP3 wins the exponent, loses the constant.
3. **What does collapse rounds is the (e') certificate, not the
   factorisation.**  Where it fires it removes the endgame — the sweeps that
   grind the ring bound from `~eps` down to `gamma*eps = 2*alpha*eps/(1+a)`:
   spider `R: 38 → 14` at `2^-14`, `21 → 10` at `2^-12`; caterpillar
   `19 → 12`; and the spider mechanism exponent falls `+0.363 → +0.153`.
   It is *sound by construction* (supersolution + maximum principle;
   the one soundness bug found — AMG-route negative residuals clipped out of
   `psi` — was fixed and re-run; final tally 0 unsound certs).  But it fires
   *flakily* at `2^-14` on path/caterpillar: the fixed radius
   `K = 4/sqrt(alpha)` is **provably too small below `alpha ≈ 2^-13`** —
   the exterior-pessimism tax is `e^{-sqrt(2 alpha) K}/gamma ≈
   alpha^{-1}·e^{-4 sqrt 2}`, which crosses 1 as `alpha` falls.  `K =
   Theta(log(1/alpha)/sqrt(alpha))` is the correct schedule (still on the
   `sqrt(alpha)` work scale up to the polylog).  **Rounds do not become
   `O(log)`; they lose roughly half their exponent** — consistent with
   stopping at `nu ≈ 2 sqrt(alpha) eps` instead of `2 alpha eps`.
4. **The FAN TRAP is broken — mostly by SP3 itself, the rest by (e').**
   `fan_trap(400, K=50, D=200)`: work `W*eps` **103.4 (vgf) → 5.64 (v3)**
   (18x), because admitted fan volume is now solved **once** (`O(vol(new))`)
   instead of re-solved every remaining round; region inflation
   `x516 (vgf) → x42 (v3)`; and with (e') the *stop happens before the fan
   is admitted*: **region x516 → x9.9** (`vol 20k → 387`, `vol(S_eps)=39`).
   The measured attempt cost is the honest price of exclusion:
   `Theta(vol(B_1(active ring)))` per attempt — on `K=200/800` the ring ball
   dwarfs the region and the attempts are (correctly) skipped or wasted
   (`v3E` 43.5/1.83 vs `v3` 2.93/1.42).  **Two-sided `Up(h)` exclusion at
   the gate is provably impossible for this family** — the blockers' true
   values sit *above* `gamma*eps`, so no sound upper bound can exclude them;
   early certification is the only sound fix, and it works.
5. **Output-boundedness survives everything.**  Ball trap: `v3` flat in `M`
   (74/96/67 over `M = 100/400/1600`) and ~2x *below* vgf; hidden hub flat
   (0.51); region exponents on the decomposition families `+0.034 / +0.041 /
   +0.052 / −0.095` — alpha-free.  Lemma V2 carries over verbatim (§2).
6. **Answer to "is there now a single mechanism output-bounded AND
   alpha-free end-to-end": NOT YET.**  Region: alpha-free, proved
   output-bounded.  Mechanism (oracle): `+0.104` median.  Self-certified:
   `+0.156` (v3E) — better than I4-E's `+0.256` but not `~0.05`.  The
   remaining gap is now split across *two* named residuals: (i) the
   lower-bound propagation reach (rounds where (e') has not yet fired), and
   (ii) the (e') radius schedule + attempt amortisation.

Evidence grade: **Measured** throughout; **Proved-draft** for the carrying
over of Lemmas V1–V3 to band solves and for the (e') soundness argument
(§2); **Open** for everything in §7.

---

## 1. What SP3 changed (mechanism, all charged)

`vgf3_local` in `i4e/vgf3.py`.  Differences from `vgf_local`:

* **No per-round re-scan.**  A row is scanned once at admission (`C_adj`);
  every later use (band assembly, residual update, BFS margin) is charged as
  a repeat via `scan_idx` (`R_adj`) — but only for **band** rows, never all
  of `S`.
* **A maintained residual replaces re-solving.**  `r = b − Q x` on `S`,
  updated edge-by-edge (charged `C_rec`) when `x` lifts; a `dirty` set
  tracks where it changed, so finding the active set never scans `S`.
  `r ≥ 0` throughout (every solve is a Dirichlet solve on a sub-region with
  frozen complement; M-matrix ⇒ lifts are nonnegative and `r` only
  increases off the solved block) — the old Lemma V1 induction applies
  unchanged, with bands in place of full regions.
* **Residual-driven band solves.**  `lift()` repeatedly solves
  `{i : r_i/sqd_i ≥ zeta·alpha·eps}` (`zeta = 0.5`) exactly, with a BFS
  margin **inside S** that grows the band geometrically across passes (2x
  volume per pass), so a lift costs `O(vol(final band)·log)` — the final
  band is the true influence region of the update.  Solves route through
  the unchanged `_region_solve` (forest / MMD-LDL / AMG triage).
* **Micro extension solves** on each admitted burst only (`O(vol(new))`,
  I4-E's ext-solve) keep admission running inside a sweep; `lift()` runs
  once per sweep.
* **Incremental ring bounds.**  `acc[y] = Σ_{w∈S, w~y} ulb[w]` maintained
  exactly under admission and lifts (kinetic-gate accumulators, I3-B);
  since `x/sqd ≤ ulb ≤ u`, `nu = max_h c_a·acc[h]/d_h` remains a sound
  upper bound on the true ring residual — certification needs no ring
  recomputation beyond an `O(|ring|)` max (charged).
* **(e') early stop** (`ecert=True` = `v3E`): when a *violator* with value
  `< eps` is about to be admitted (or at sweep end with `nu < eps`), build
  I4-F's profile-localized supersolution on `Omega_K = B_K(supp psi)`,
  `K = ceil(4/sqrt(alpha))`, `psi` = ring `Lo` values + interior `|r|`
  (signed residuals kept for exactly this reason), exterior bound
  `max(psi)/(1−c)`; stop iff `max_T Ghat < eps`.  Charged: BFS reads
  (outside-`S` rows pay first exposure), `rec(nnz)`, LDL
  (`Σ colcnt²` + materialised `nnz`), with a fill-estimate abort charged
  `O(|Omega|)` (campaign triage convention).  Attempts are spaced by 3x
  total-work growth, capped at 12, skipped when `vol(ring) > 60·vol(S)`;
  `Omega` capped at `2(vol(S)+vol(ring)) + 2000`.

**Soundness of the stop (Proved-draft).**  `G = (I−cP)^{-1} psi ≥` the true
error profile whenever `psi ≥ |rho|/d` pointwise (one-signedness not
required); ring `psi` uses `ulb`-sums ≥ the realized values, interior uses
the maintained `|r|`, and `rho ≡ 0` outside `S ∪ ring`.  Localization with
exterior value `max(psi)/(1−c)` is a supersolution by M-matrix comparison
(I4-F §7).  Verified: 444 runs, 0 certified runs with `err > eps`, 0 misses.

---

## 2. Decomposition, before vs after (E1, `eps=1e-5`, alphas `2^-4..2^-14`)

Mechanism exponent `q` in `W/vol(S_eps) ~ alpha^-q` (6-point fits), rounds
exponent, and region exponent:

| family | q vgf | q v3 | q v3E | q v3O | R-exp vgf→v3E | region-exp v3 |
|---|---|---|---|---|---|---|
| path | +0.362 | +0.253 | +0.236 | +0.165 | +0.30 → +0.25 | +0.034 |
| caterpillar | +0.311 | +0.279 | +0.242 | +0.160 | +0.28 → +0.26 | +0.041 |
| spider | +0.363 | +0.281 | **+0.153** | +0.139 | +0.30 → **+0.16** | +0.052 |
| grid2d | +0.134 | +0.173 | +0.116 | +0.099 | +0.08 → +0.07 | −0.095 |

Round counts (path): vgf `5,6,8,13,22,40`; v3 `5,6,8,13,20,34`; v3E
`5,6,8,13,12,34` (the `2^-14` cell is the flaky-K case of §3).  Spider v3E:
`5,5,7,12,10,14`.

* The region stays alpha-free everywhere (`|exp| ≤ 0.1`); the rounds are
  essentially untouched by incrementality alone; the *work* exponent drops
  because each remaining round now costs `O(vol(band))` instead of
  `O(vol(S))` — path band total `bv = 2.8e4 ≈ 20·vol(S)` at `2^-14`
  against vgf's `R·vol(S) = 40·vol(S)` *of scans* plus solve constants.
* grid2d: `v3` is *worse* than vgf (+0.173 vs +0.134, and 1.3–1.6x in
  absolute W): 2-D residual spread makes bands ≈ the whole region, so the
  incremental machinery is pure overhead.  SP3 helps 1-D-like supports,
  is neutral-to-negative on 2-D+.

## 3. Why the rounds survive (the sharpest new fact)

Per sweep, the value frontier advances `~log2(nu/floor)` hops (one-hop
lower-bound chains, unchanged from I4-E).  The sweeps' *cost* was the
target, and it fell; but the *count* is set by bound reach, and on
path-likes the residual band that a sweep must re-lift extends
`~ln(lift/(zeta·alpha·eps))/sqrt(2·alpha)` hops back into `S` — the same
`Theta~(1/sqrt(alpha))` scale as `vol(S_eps)` itself.  So on exactly the
families where the round count is worst, **"make a stalled round
`O(vol(new))`" is impossible for any method that maintains an exact
residual: the influence region of one admission IS `Theta(vol(S))` up to
logs.**  The i4e §7(a) proof obligation should be restated: either
(i) prove the *value expansion* reaches `Omega(vol(S))` new volume per
sweep (false as implemented: measured `5→34` rounds), or (ii) accelerate
the *bound propagation* itself — a frontier iteration whose certified lower
bounds advance `Theta(1/sqrt(alpha))` hops per `O(vol(band))` of work
(Chebyshev/accelerated-ESP on the frontier, cf. HLX25 notes), or
(iii) stop earlier via the certificate ((e'), §4).

## 4. The (e') stop: rounds, radius law, and honest cost

* Fires (`sb=ecert`) on spider/caterpillar/path at `2^-8..2^-12` and
  collapses the endgame (spider `38→14` rounds, `12.36→9.37` W·eps at
  `2^-14`; `3.40→3.83` at `2^-12` — the attempt cost can exceed the saving
  at small scale).
* **Radius law.**  With `K = 4/sqrt(alpha)` the exterior tax is
  `e^{-sqrt(2a)K}·nu/gamma`; certifiability at `nu ≈ 2 sqrt(a) eps`
  requires `e^{-4 sqrt 2} < ~sqrt(a)` — fails below `~2^-13`, exactly
  matching the observed non-firing at `2^-14` (path, caterpillar).
  The correct schedule is `K = Theta(log(1/alpha)/sqrt(alpha))`; cost stays
  `O~(1/sqrt(alpha))`.
* Attempt spam is bounded (12 tries × 3x work spacing) but on high-degree /
  expander shapes the splu-based fill probe burns wall time — the 4
  wall-capped zoo cells; the *charged* aborts are cheap.  A colcount-only
  symbolic probe would fix the wall time.

## 5. Fan trap (E2) and the other adversaries

`fan_trap(400,K,200,at=20)`, `a=2^-10`, `eps=1e-4`, `vol(S_eps)=39` for
`K≥50`:

| K | push | composed | vgf | **v3** | **v3E** | v3O | region v3E / v3 / vgf |
|---|---|---|---|---|---|---|---|
| 10 | 193.8 | 11.3 | 25.0 | 33.6 | 52.3 | 32.3 | ×1.03 (support is big) |
| **50** | 7.95 | 1.67 | **103.4** | **5.64** | 22.9 | 0.365 | **×9.9** / ×42 / ×516 |
| 200 | 7.82 | 1.15 | 16.7 | **2.93** | 43.5 | 0.613 | ×27 / ×27 / ×167 |
| 800 | 7.76 | 1.26 | 1.11 | 1.42 | 1.83 | 1.32 | ×22 / ×22 / ×22 |

The vgf catastrophe (938x over oracle) was mostly *re-solving* the admitted
fan every round; SP3 removes that (`103→5.6`).  (e') removes the *volume*
(`×516→×9.9`) when the ring ball is affordable, at `Theta(vol(B_1(ring)))`
per attempt — that read is irreducible for any certificate that must
*bound* the parked band's values, and `Up(h)`-exclusion cannot work at all
(their `u ≥ gamma·eps`).  Ball trap: v3 flat in `M` and 2x below vgf; v3E
never falsely fires (`S_eps` empty ⇒ correctly refuses; attempts bounded).
Hidden hub: flat, 2x above vgf (constant overhead).  Shallow support:
v3 265 vs vgf 159 at `2^-12` (worse constants), v3E 184, oracle 26.8 — the
shallow-support family remains (e')-fixable in principle but the fixed-K
attempts fire too late; same radius law as §4.

## 6. Zoo (E3, 15 families × `{2^-4,2^-8,2^-12}`, `eps=1e-5`)

45 cells × 6 mechanisms; all certified except the 4 `v3E` wall-caps
(exp5reg×3, grid3d 2^-8); 0 misses on certified runs.  Median/max mechanism
exponent: push `+0.934/+1.006`; composed `+0.021/+0.161`; vgf
`+0.256/+0.365`; **v3 `+0.197/+0.398`; v3E `+0.156/+0.267`; v3O
`+0.104/+0.196`**.  `W` ratio to push: vgf median `0.18`, v3 `0.41`, v3E
`0.36` (v3's constant costs it half of vgf's median advantage; the traps
are where SP3 pays).  Per-family `q` (v3E): negative on btree/rrt/pa_tree/
exp3reg/exp5reg, `+0.19..+0.27` on path-likes/theta/prism/grid2d — the
same split as I4-E, shifted down ~0.1.

## 7. Updated claim and proof obligations

> **Claim I5-B (Measured; Proved-draft core carried from I4-E).**  vgf3
> (`v3E`) preserves P1 (output bound, no adjacency term) and P2 (no-miss,
> one degree query per ring vertex) verbatim; on the 15-family zoo it is
> certified with `W ≤ C(G)·vol(S_eps)·alpha^-q`, `q` median `+0.156`, max
> `+0.267` (vs `+0.256/+0.365` for I4-E VGF), with the region alpha-free
> and the fan-trap region inflation reduced `×516 → ×9.9`.

Obligations, updated from i4e §7:

* **(a) REPLACED.**  ~~Incremental factorisation makes a stalled round
  `O(vol(new))`~~ — built, and refuted as the route to `q=0` (§3): the
  influence region of an admission is `Theta(vol(S))` on the worst
  families.  New form: *a certified lower-bound propagation that advances
  `Theta(1/sqrt(alpha))` hops per `O(vol(band))` work* (accelerated
  frontier iteration), OR *(e') firing at `nu = Theta(sqrt(alpha)·eps)`
  with `K = Theta(log(1/alpha)/sqrt(alpha))` on a named class* — either
  one kills the endgame that is the entire remaining rounds exponent.
* **(b) Unchanged.**  Conditional region bound `vol(S_{theta·gamma·eps}) =
  O~(vol(S_eps))` with explicit band-mass hypothesis (fan trap still the
  counterexample; measured `+0.03..+0.05` on the zoo).
* **(c) PARTIALLY DELIVERED.**  The computable amplification (I4-D SP1) now
  exists and is *deployed* as (e'); missing: the theorem
  `Ahat_e'(T) ≤ C·sqrt(alpha)` on a named class (I4-F measured it), the
  radius schedule above, and attempt amortisation `O(final attempt)`.
* **(d) Unchanged** (inner-solver triage) plus: a symbolic-only fill probe
  so triage aborts cost wall-time `O(nnz)`.

## 8. Next target

**(e')-first VGF**: make the certificate the *primary* stopping rule with
the corrected radius `K = c·log(1/alpha)/sqrt(alpha)`, amortised attempts,
and a `nu`-schedule that tries at `nu ≈ 2^j·sqrt(alpha)·eps` — predicted to
take the path/caterpillar/spider rounds to their `2^-12` v3E values at all
alphas and `q` toward the oracle `+0.10`; combined with a frontier
Chebyshev lower-bound propagation (obligation (a), second form) it is the
remaining route to a single mechanism that is output-bounded and alpha-free
end-to-end.
