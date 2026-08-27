# I6-D — The HSEG-LDL re-carve amortization is PROVED (potential function), the thrash adversary fails to break it, and the tree theorem closes

**VERDICT: the last open piece of the tree theorem is closed by proof.**
The re-carve (swap) cost of HSEG-LDL's 2-approximate heavy-path maintenance is
amortized **O(log n) moved vertices per insertion — total moved
`<= (2·log_1.5 n + 2)·n ≈ 3.42 n log2 n`, total re-carve cost `O(n log^2 n)`,
alpha-free — by an explicit potential function (Proved, §2)**, for a
*full-walk* variant of the shipped rule that differs only in never truncating
the size bookkeeping (the shipped lazy walk is a real hole, §1; the repair
costs nothing asymptotically and **changes no measurement: FW ≡ LAZY exactly on
all 140 re-run campaign configs**). The predicted falsifier was built and
fails informatively: alternating, nested-light-descent, and armed-cascade
thrash families all collapse to **constant** amortized moved
(`mv/n = 1.50 / ≈3.0-falling / ≈1.4`), while the cascade proves the
**per-operation** worst case really is `Theta(n)` (a single admission fires 12
nested junctions and moves `1.01n` vertices) — so amortization is *necessary*,
and the proved `O(log n)` amortized budget is safe by a `log`-sized margin on
every family we could construct. With the amortization proved, growing-tree
PPR has total charged work **`O((nnz(s) + vol(S)) log^2 vol(S))` with
alpha-free constants (Proved for the backend; constants Measured:
`W/(vol·log2^2 vol) ∈ [1.59, 5.57]`, median 2.53, over 140 re-certified
configs)**. On certification (§5): trees **do not escape** the I5-F
`Theta(1/sqrt(alpha))` radius law for tightness factors `C < 2` (a path-end
adversary — a tree — forces it, measured `ell* ≈ [1 + ln(1/(C-1))/(4 sqrt a)]`),
but the hidden-exterior error gap on trees **saturates at exactly
`1 + lam^{2(ell-1)} <= 2`** (measured closed form, 5 alphas), unlike the
cycle's unbounded blow-up — and the theorem as stated needs only the
**residual certificate, whose cost is `O(vol(S))` and alpha-free**, so the
tree pipeline is alpha-free end to end.

Code: `w6_incremental/{i6d_amort.py (FW variant + adversaries + cert
adversary), run_i6d2.py}`. Raw: `res_i6d.json` (structural + cert),
`res_i6d2.json` (140 replayed configs, FW and LAZY side by side).
Compute ~3 min. Evidence labels strict: **Proved / Measured / Open** inline.

---

## 0. The swap rule, exactly (extracted from `dyn_ldl2.py`)

`HEAVY_FACTOR = 2.0`. During each admission's upward walk, at every junction
where the chain leaves light-child path `Pk` and enters `u = Pk.pvert`, after
`own[u] += 1`:

```text
fire  iff  sz(Pk.top) > 2.0 * sz(h(u))          # strict; sz maintained as
                                                # suffix sums of own[]
```

`h(u)` = the vertex immediately below `u` on `u`'s own path (`sz = 0` if `u`
is its path's bottom). On fire: `u`'s tail below `u` (all path vertices
below, which lie in `subtree(h(u))`) is detached into a new light path `T`
(`a_u += w^2/delta(T)` sign-correctly), and **all** of `Pk`'s path vertices
are spliced onto `u`'s path. `moved = |tail| + |Pk|` — *path lengths, not
subtree sizes* — each moved leaf costing one `set_leaf = O(log)` segment-tree
write; plus `O(1)` `delta_top` reads and one `O(log)` junction-weight fix.
Validated: an independent pure-counter simulation of this rule reproduces the
live structure's swap count and moved total exactly on `thrash_alt` at all 8
sizes (asserted).

## 1. A real hole in the shipped code, and the free repair (Measured)

`HDynTree.admit` ends its walk with `elif not changed: break` — when `Pk`'s
float contribution `w^2/delta` freezes, the walk stops, **skipping `own_add`
and the heavy check at every junction above**. Maintained sizes can therefore
undercount without bound and the 2-approx invariant is enforced only lazily;
the chain-length bound (and hence the `O(log^2)` admission cost and the
potential argument) is *not* guaranteed for the shipped rule.
**Repair (`HDynTreeFW`)**: sizes and heavy checks always walk the full
junction chain (`O(chain·log) = O(log^2)` per admission — same asymptotics);
only the *value* update stops early, which is exact (frozen contribution ⇒
`a_u` unchanged ⇒ all higher deltas unchanged), and a swap un-freezes it
(`a_u` changed). Correctness re-verified against dense solves of every
admitted prefix (max relerr `4.4e-14`, 8 config/alpha combinations).
**FW ≡ LAZY — identical `W`, swaps, moved — on 140/140 replayed campaign
configs** (values freeze only beyond the certified reach at these `eps`), so
all previous measurements stand unchanged for the repaired rule.

## 2. The amortization theorem (Proved)

**Setting.** Any tree, any sequence of `n` leaf admissions (adversarial),
full-walk rule, hysteresis 2. Sizes are integers; at fire
`sz(C) >= 2·sz(H) + 1` (`C` = promoted light subtree, `H = subtree(h(u))`).

**Invariant (continuous; induction over admissions).** After every admission,
every light edge `(u,c)` satisfies `sz(c) <= max(1, 2·sz(h(u)))`. (Off-chain
edges don't change size; chain edges are checked bottom-up and a fire restores
them; a swap changes no sizes, and its two new/changed edges satisfy the bound
— demoted: `sz(H) < sz(C)/2`; other light siblings compare against a *larger*
heavy child. A brand-new singleton light path can sit at `sz=1 > 2·0` until
the first admission beneath it — that is the `max(1,·)`.) Crossing any light
edge then shrinks subtree size by `>= 3/2` (for `sz(c)=1` edges by `>= 2`), so
the number of light edges on any root chain is `Lambda <= log_1.5 n`, and
**admissions and queries cost `O(log^2 n)` each** — this re-proves I2-B(a)
including the previously-glossed singleton case.

**Potential.**

```text
Phi  =  sum over light edges (u,c) of  max(0, 2·sz(c) - sz(h(u)))   >= 0,  Phi_0 = 0.
```

* **Insertion of `x`:** `sz(v) += 1` exactly for `v` on `x`'s root chain.
  Light edges with `c` on the chain gain `+2` each (`<= Lambda` of them);
  edges with `h(u)` on the chain only *decrease*; a newly created light edge
  enters at `max(0, 2 - sz(h)) <= 2`. So `ΔPhi <= 2·log_1.5 n + 2`.
* **Swap at `u`:** the `(u,C)` term leaves `Phi`, releasing
  `2·sz(C) - sz(H) >= sz(C) + sz(H) + 1` (using `sz(C) >= 2 sz(H)+1`; the
  hysteresis constant 2 is exactly what makes this `>= sz(C)+sz(H)` — a
  strict-majority rule `c=1` would *not* self-amortize). The demoted edge
  `(u, H_top)` enters at `max(0, 2 sz(H) - sz(C)) = 0`; every other term can
  only fall (bigger heavy child). And
  `moved = |tail| + |P_C| <= sz(H) + sz(C) <` release. Deferred fires
  (`sz(C)` far above threshold) release even more — the accounting also
  covers the lazy variant's swaps; laziness endangers only the invariant.

Summing: **total moved `<= (2·log_1.5 n + 2)·n ≈ 3.42·n·log2 n`; total
re-carve cost `O(moved · log n) = O(n log^2 n)`**; per-vertex swap counts
`<= log_2 n` (promoted-child size at least doubles between fires at a fixed
`u` — sharpens I2-B(b)). All alpha-free. This replaces I2-B §4(c)'s
`O(|S|·depth·log^2)` worst case; **no link-cut tree is needed for the
amortized claim** (LCT would additionally fix the per-operation worst case,
which is genuinely `Theta(n)` — §3 cascade).

## 3. The thrash adversary: built, and it validates rather than falsifies (Measured)

* **`thrash_alt`** (one junction, two path arms, always extend the light arm —
  fires as often as hysteresis allows): `mv/n → 1.500` exactly, flat from
  `n = 2^10` to `2^17`; swaps `= Theta(log n)` (8→15); worst single admission
  moves `0.75n`. Sizes triple per phase, so each phase's `~2·sz` insertions
  pay its `~3·sz` moved: amortized constant, as the potential predicts with
  slack.
* **`thrash_nested`** (the task's falsifier: complete binary arena, 6 nested
  junction levels, adaptive driver that descends the *live* light side at
  every junction — maximal simultaneous boundary pressure): `mv/n = 3.40 →
  2.99` **falling** over `n = 1000 → 16000`; `mv/(n·log2 n)` falls `0.34 →
  0.21`; `lev_mean ≈ 6` (all levels active). 7x above random trees, still
  constant.
* **`cascade`** (ladder of `k` junctions armed to within one admission of
  threshold, geometric arms `h_i ≈ 1.5^{k-i}`): one deep admission fires up to
  12 junctions and moves `1.01n–1.32n` vertices — **the per-operation worst
  case is `Theta(n)`, so the `O(n log^2)` claim is unavoidably amortized** —
  while the same runs' *total* `mv/n ≈ 1.4`. The arming constraint
  (`sz` light `<= 2·sz` heavy at every level simultaneously) forces the
  geometric arm decay; that geometry is exactly why every cascade's total
  collapses to `O(n)`: re-arming level `i` costs `Theta(sz_i)` fresh disjoint
  insertions.
* **Repair needed: none.** The hysteresis-2 rule survives its falsifier; no
  family forced `omega(1)` amortized moved. Gap between proved `O(log n)` and
  measured `O(1)` amortized: **Open** (every construction tried — batch,
  ladder, cascade, nested descent — collapses geometrically, suggesting the
  truth is `Theta(n)` total moved; the `Theta(log)`-per-insertion question is
  a clean combinatorial problem, not blocking anything).

Random families with the final rule (`n = 4000`, 2 seeds each): rrt
`mv/n <= 0.44`, preferential attachment `<= 0.24`, random-leaf-attach `0`
(path-like); `lev_max <= 8` against the bound `20.5`.

## 4. THE TREE THEOREM (assembled)

**Theorem (backend, Proved).** On any tree, for any admission sequence of
`n` vertices and any `Q` boundary-value queries interleaved, HSEG-LDL-FW
maintains the exact source-aligned solve on the admitted set with total
charged structure work `O((n + Q)·log^2 n)`, alpha-free and eps-free:
`O(log^2)` per admission and per query (§2 invariant), plus amortized
re-carve `O(log^2)` per admission (§2 potential). Exactness: every query
agrees with the dense solve of the admitted prefix (float-verified to
`4.4e-14`; the transfer-matrix recurrences are exact modulo rounding).

**Corollary (pipeline, Measured constants).** Growing-active-set PPR on trees
— greedy residual-gated growth (`core.grow_trace`), HSEG-LDL-FW backend,
final output the exact solve on `S` — has total charged work (gate + backend
+ queries + certificate + output)

```text
W  <=  c · (nnz(s) + vol(S_final)) · log2^2 vol(S_final),
       c ∈ [1.59, 5.57], median 2.53      (140/140 configs)
```

with alpha-free `c` (path: 226.9/276.0/324.0 `W/vol` at `alpha =
2^-6/-10/-14` — drift is `log vol`; rrt: exactly alpha-invariant), fitted
exponents `q = 0.92–1.11` across the five scaling series (comb x3,
caterpillar, path), including the comb that kills INC-LDL (`q=1.87`),
TREE-INC (`q=1.30`), and SEG-LDL (`q=1.18`).

**Certificate used (state it, per project policy):** the residual certificate
`||D^{-1/2}(Q x_hat - b)||_inf < alpha·eps_ppr ⇒ semantic err < eps_ppr`,
asserted on every config (`min(eps - sem) = 1.77e-12 > 0`). Its cost is
`O(vol(S))` reads (residual support ⊆ `S ∪ ∂S`; boundary edges are exposed by
scanning `S`) — **alpha-free**; it is included in the charged `W` above.

## 5. Certification on trees: does the I5-F radius law bite? (Measured + Proved-draft)

The I5-F `Theta(1/sqrt alpha)` radius lower bound used the cycle `C_{2K+4}` —
unavailable on trees. The tree-native adversary is the **path end**: a path
ending `ell` beyond the truncation boundary vs a long path agree on
`B_K(boundary)` for every `K < ell` (all visible degrees 2), and both are
trees. Measured over 5 alphas (`2^-4..2^-12`), the error ratio follows the
closed form

```text
err_short / err_long  =  1 + lam^{2(ell-1)},    lam = (1-sqrt a)/(1+sqrt a)
```

(matches to 3 digits at every sampled `(alpha, ell)`). Consequences:

1. **For tightness `C < 2`, trees do NOT escape:** any sound `C`-tight
   `K`-local certificate needs `K >= ell*(C) - 1` with measured
   `ell*(C)·sqrt(alpha) →` const: `C=1.1: 0.61–0.62`, `C=1.25: ≈0.39`,
   `C=1.5: ≈0.22` (formula `ell* = 1 + ln(1/(C-1))/(2 ln(1/lam))`, matching
   within 1–2 vertices everywhere). Same `Theta(1/sqrt alpha)` scale as the
   cycle, smaller constant.
2. **For `C >= 2` the tree gap saturates:** a one-ended tree exterior can
   amplify the hidden error by at most `2 + o(1)` (single reflection; no
   cycle ⇒ no resonant `1/(1-lam^L)` build-up), and measured `ell*(2) = 2–3`
   flat in alpha. So a factor-`(2+delta)`-tight `O(1)`-radius certificate is
   *not excluded* on trees — whether one exists (sound against all tree
   exteriors, e.g. branching ones) is **Open**; the sandwich argument
   (M-matrix monotonicity between dead-end and open-path exteriors) is a
   plausible route but was not carried out.
3. **The theorem doesn't need any of this.** Tight-radius certification
   matters only for stopping *earlier* than the residual test allows. With
   the residual certificate the pipeline is **alpha-free end to end** (§4);
   the alpha-dependence lives where it must: in `vol(S_final)` itself (the
   value-reach `~1/sqrt alpha` on path-likes), which is charged as output.

## 6. What the theorem does NOT cover (honesty)

1. **Non-trees.** Everything here is tree-only: leaf-rank-1 elimination and
   growth-by-leaves (I2-B §5). Bounded treewidth inherits a `k^3`
   transfer-cost factor (untested); grids remain the known wall. An admission
   closing a cycle is an unimplemented `link` type.
2. **Constants, not champions.** HSEG-LDL-FW still pays 6–57x over the best
   per-family backend at reachable sizes (comb crossover vs COLD-LU
   `~vol 1.3e5`, unmeasured). The claim is uniformity of exponent.
3. **The amortized-vs-worst-case gap is real:** single admissions can cost
   `Theta(n·log)` (cascade). A link-cut backend would make it worst-case
   `O(log^2)` per op; not built.
4. **Proved `O(log n)` amortized moved vs measured `O(1)`:** bound likely
   loose by a log; open combinatorial question (§3).
5. **The meter constants** (`MATC=16`, `QRYC=10`) remain a stated proxy;
   compare exponents across backends, constants only within one.
6. **`C >= 2`-tight `O(1)`-radius tree certification** is conjectural (§5.2);
   and the `C < 2` lower bound here reuses I5-F's indistinguishability logic
   on a tree family — the formal reduction to *arbitrary* certificate
   algorithms is inherited from I5-F, not re-derived.
7. Random-tree evidence is 3 families x 2 seeds at `n = 4000`; no large
   ensemble.
