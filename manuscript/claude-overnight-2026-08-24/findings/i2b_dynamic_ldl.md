# I2-B — Dynamic-order incremental LDL^T on trees: the comb, and HSEG-LDL

**VERDICT: MIXED, and the interesting half is positive (Measured).**
The **COMB does not win.** A dynamic-order incremental factorization — `HSEG-LDL`, a
seed-rooted implicit LDL^T carried on a *2-approximate heavy-path decomposition* that is
re-carved online — is **output-linear up to polylog on every tree family tested, including the
comb, with an alpha-free constant**: fitted `W ~ vol^q` gives **q = 0.92–1.11** on all five
scaling series, and `W / (vol * log2^2 vol) ∈ [1.59, 5.57]`, median 2.54, over **149 configs**
spanning `alpha ∈ {2^-6, 2^-10, 2^-14}` and seven families. Every one of the two iteration-1
backends is refuted on the comb exactly as predicted: **INC-LDL blows up (`nnz(L) ~ |S|^1.556`,
`W ~ vol^1.87`)** and **TREE-INC pays a growing update path (`up/admission ~ alpha^-0.45` on
path-likes, `W ~ vol^1.30` on the comb)**. The inherited `SEG-LDL` (iteration-2 partial work) is
*also* defeated by the comb (chain length grows to 32, `q = 1.09–1.18`) — its carving rule is
admission-order dependent; that is what HSEG-LDL repairs.
**The honest negative:** HSEG-LDL's constant is 6–57x worse than the best *per-family* backend, so
at the sizes reachable here it is the champion on no single family (on the comb it crosses COLD-LU
only around `vol ≈ 1.3e5`). It buys **uniformity of exponent**, not constants. And the
re-carve (swap) cost has a proved chain-length bound but **only an empirical amortization**.

Code: `w6_incremental/{dyn_ldl.py (SEG-LDL, inherited), dyn_ldl2.py (HSEG-LDL, new),
i2b.py, run_final.py, analyze_i2b.py, test_dyn.py, test_dyn2.py}`.
Raw: `res_final.json` (149 configs), logs `run_final.log`, `run_comb.log`.
**Every config asserts `||D^{-1/2}(Qx-b)||_inf < alpha*eps` and `semantic_err <= eps` against
`Model.solve_exact`; 149/149 pass, 0 backend errors, `min(eps - sem) = 1.77e-12 > 0`, max
frontier-query relative error `1.4e-10`.** Total compute ~11 min.

---

## 0. State of the inherited code (Measured)

`test_dyn.py` **had not been run**; it passes as written (`relerr <= 1.6e-11` vs dense solves of
every admitted prefix, on comb / comb+forced-rebuild / btree / path-3000). So **`dyn_ldl.py` was
correct**, not broken. What it implements (design (b), *not* re-rooting):

* the seed-rooted elimination order (fill-free on any tree) is kept, but the factorization is
  stored **implicitly**: the tree is carved into vertex-disjoint top-to-bottom paths; vertex `u`
  carries a reduced diagonal `a_u = Q_uu - sum_{light children c} w_c^2 / delta_c`; along one path
  the trailing minors obey `phi_i = a_i phi_{i+1} - w_{i+1}^2 phi_{i+2}`, i.e. an ordered product of
  `2x2` transfer matrices `N_i = [[a_i, -w_{i+1}^2],[1,0]]`;
* a **balanced segment tree of ordered `N_i` products** per path (normalized mantissa + `log2`
  scale) gives `delta_top = phi_1/phi_2` in **O(1)** and `x_{v_m}` in **O(log)**;
* admission = 1–2 leaf updates + one leaf update per path-level up the root chain — **no value
  propagation, no truncation, exact**; a `Lmax` trip-wire triggers a global HLD rebuild.

Two changes I made to it: (i) the `x`-query chain now carries `log2 x` end-to-end (the old code
took `log2` of a float that underflows on deep chains); (ii) `replay_seg_ldl` was wired into the
harness. Its **weakness is the carving rule**, see §2.

## 1. The COMB adversary (Measured)

`comb(B,T)`: backbone `b_0..b_{B-1}` (a path), each `b_i` carrying a pendant path of `T` vertices;
seed at `b_0`. `T = round(1/sqrt(alpha))` so teeth are exactly as deep in value as the backbone is
long. `eps` tuned by growing the real trace (a value proxy is unusable — the greedy outer loop
solves on `S_t` and therefore *under*-estimates `x`, so it stops far earlier than the final `x0`
suggests) to the finest `eps = 2^-k` with `|S*| <= 2500`.

`W / vol(S*)`, all backends replaying the identical trace with their own meter:

| B | T | alpha | eps | \|S*\| | vol | E | COLD-LU | INC-LDL | TREE-INC | SEG-LDL | **HSEG-LDL** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 32 | 8 | 2^-6 | 2^-34 | 288 | 574 | 39 | 54.6 | 68.9 | 61.9 | 210.9 | **244.4** |
| 32 | 32 | 2^-10 | 2^-34 | 1056 | 2110 | 63 | 84.4 | 340.4 | 119.1 | 277.6 | **331.9** |
| 32 | 128 | 2^-14 | 2^-7 | 2500 | 5017 | 141 | 181.0 | 531.5 | 243.6 | 786.5 | **477.7** |
| 128 | 8 | 2^-6 | 2^-34 | 370 | 742 | 48 | 65.5 | 73.0 | 63.7 | 214.0 | **250.9** |
| 128 | 32 | 2^-10 | 2^-30 | 2486 | 4979 | 103 | 130.3 | 545.0 | 134.8 | 301.1 | **365.0** |
| 128 | 128 | 2^-14 | 2^-7 | 2500 | 5017 | 141 | 181.0 | 531.5 | 243.6 | 786.5 | **477.7** |
| 512 | 8 | 2^-6 | 2^-34 | 370 | 742 | 48 | 65.5 | 73.0 | 63.7 | 214.0 | **250.9** |
| 512 | 32 | 2^-10 | 2^-30 | 2486 | 4979 | 103 | 130.3 | 545.0 | 134.8 | 301.1 | **365.0** |
| 512 | 128 | 2^-14 | 2^-7 | 2500 | 5017 | 141 | 181.0 | 531.5 | 243.6 | 786.5 | **477.7** |

**`B` is the wrong knob.** Rows for `B = 128` and `B = 512` are *identical*: the active set is a
value-triangle of reach `R ≈ ln(2/(alpha·eps))/sqrt(2 alpha)`, and once `R < B` the backbone end is
never seen. `B` matters only through `min(B, R)`; `B = 32` is the *clipped* regime, `B >= 128` the
unclipped one, and both are covered. The informative sweep is therefore **`eps` at fixed `(B,T)`**,
i.e. growth of `vol` itself (§3).

### Is the prediction confirmed?

**INC-LDL: CONFIRMED, and the law is sharper than "quadratic".** On `comb(512,128)`, as `|S|` goes
`392 -> 8286`, `nnz(L)/|S|` goes `10.5 -> 54.7`, fitting **`nnz(L) ~ |S|^1.556`** — i.e.
`nnz(L) = Theta(|S|^{3/2})`, not `Theta(|S|^2)`. This is exactly the geometry: the elimination
front after eliminating the backbone prefix is a clique on the `~R ≈ sqrt(|S|)` currently-active
teeth, so each admitted vertex adds `Theta(sqrt(|S|))` fill. Charged work fits `W ~ vol^1.87`
(fill + the symbolic reach DFS). Compare btree/`rrt`, where the same backend really is quadratic
(`nnz(L)/|S| = 512` at `|S| = 2047`, capped).

**TREE-INC: CONFIRMED.** The truncated upward delta-path per admission (`up_total/|S|`):

| family | a=2^-6 | a=2^-10 | a=2^-14 | fitted |
|---|---|---|---|---|
| path | 27.2 | 97.1 | 323.5 | **alpha^-0.45** |
| caterpillar | 19.5 | 67.5 | 221.3 | **alpha^-0.44** |
| comb | 14.7 | 30.6 | 64.7 | alpha^-0.27 (tooth depth co-varies with alpha) |
| btree / rrt2000 | 9.0 / 6.4 | 9.0 / 6.4 | 9.0 / 6.4 | alpha-frozen (shallow) |

so TREE-INC is **not** alpha-free on any path-like family, and on the comb it is superlinear in
volume (`q = 1.25–1.34`). The `1/sqrt(alpha)` is structural: the per-step pivot contraction is
`1 - c*sqrt(alpha)`, so no relative-tolerance truncation can shorten the path.

**SEG-LDL (the inherited structure): also defeated — a result the task did not anticipate.** Its
carving rule is "a new vertex extends its parent's path iff the parent is the childless bottom of
that path". On the comb the **gate admits a tooth vertex before the next backbone vertex** (the
gate is `r_w/sqd_w`, and a degree-2 tooth vertex beats a degree-3 backbone vertex at the same
distance), so each tooth **captures the backbone's continuation** and the backbone is chopped into
segments. Measured chain length on `comb(512,128)`: `lev_mean 4.9, lev_max 32` and rising with
`vol`, giving `q = 1.09–1.18`. The `Lmax = 2 log2 n + 6` trip-wire never fires — the degradation
is *below* the trip-wire and therefore silent.

## 2. HSEG-LDL: the repair (design, Proved-draft + Measured)

Keep everything from SEG-LDL; replace the carving with a **2-approximate heavy-path decomposition
maintained under leaf insertions**:

* `own[i] = 1 + sum of subtree sizes of the LIGHT children of verts[i]`, so
  `sz(verts[i]) = suffix_sum(own, i)`. `own` is carried **as a third aggregate in the same segment
  tree** as the `2x2` matrix products and the `log2 w` prefix sums — so subtree sizes survive
  splices for free and cost nothing extra asymptotically.
* **Admit `v` under `p`**: extend/create as before, then walk the chain of paths to the root. At
  each jump the chain enters `u = P_k.pvert` from its light child path `P_k`; point-add `+1` to
  `own[posin[u]]` and compare `sz(P_k.top)` against `2 * sz(h)`, `h` = the vertex just below `u` on
  `u`'s own path.
* **Swap** when `sz(P_k.top) > 2 sz(h)`: detach `u`'s tail below `u` into a new light path (its
  contribution `w^2/delta_top` is *subtracted* from `a_u`), splice `P_k`'s vertices on after `u`
  (its contribution is *added back*), fix the single junction weight `w(u, P_k.top)`, and relabel
  only the moved vertices. **Cost O((|tail| + |P_k|) log)** — only vertices that actually move.

The factor 2 does double duty: it bounds the chain and it self-amortizes the swaps (§4).

**Correctness (Measured).** `test_dyn2.py` compares `query_x(u)` against a **dense solve of every
admitted prefix**, on: comb BFS order; comb with a hand-built *teeth-before-backbone* order (the
adversarial one); binary tree; a 40-star (every admission is a new light child of the root); a
random recursive tree under a random admission order; and a 4000-path at `alpha = 2^-12` (values
down to `1.7e-56`, exercising the `log2` bookkeeping). Max relative error **`3.3e-11`** (paths),
`1.6e-14` elsewhere. In the campaign, frontier queries match the exact per-round trace to
`1.4e-10` relative, and the final vector is certified.

**The O(moved) splice mattered.** My first version re-`reload`ed the *whole* path on each swap.
On `caterpillar(4000)` at `alpha = 2^-14` that moved 31 995 vertices for `|S| = 2160`
(`W/vol = 919.8`); with the O(moved) splice the same config moves **129** (`mv/|S| = 0.06`) and
`W/vol = 249.5`. Measured `mv/|S| <= 0.44` on every family and every size (max 0.435, at the smallest
caterpillar config; it *falls* with size — on `comb(512,128)` it goes `0.276 -> 0.084` as `vol`
goes `796 -> 16 589`, while `W/vol` stays flat at `517 -> 461`).

## 3. Scaling fits — the central table (Measured)

`W ~ C * vol^q`, log-log least squares over each `eps`-series (capped points excluded):

| series | alpha | pts | vol range | COLD-LU | INC-LDL | TREE-INC | SEG-LDL | **HSEG-LDL** |
|---|---|---|---|---|---|---|---|---|
| comb B=512, T=128 | 2^-14 | 12 | 796–16 589 | q=1.23 | **q=1.87** | q=1.30 | q=1.18 | **q=0.95** C=759 |
| comb B=512, T=32 | 2^-10 | 35 | 456–6 608 | q=1.47 | **q=1.58** | q=1.25 | q=0.98 | **q=1.00** C=359 |
| comb B=32, T=128 | 2^-14 | 7 | 796–8 254 | q=1.23 | **q=1.61** | q=1.34 | q=1.09 | **q=0.92** C=917 |
| caterpillar | 2^-14 | 37 | 427–4 947 | q=1.86 | q=1.02 C=15.1 | q=1.45 | q=1.02 | **q=0.93** C=435 |
| path | 2^-14 | 36 | 443–3 549 | q=1.99 | q=1.00 C=10.5 | q=1.43 | q=1.10 | **q=1.11** C=138 |

**HSEG-LDL is the only backend with `q ≈ 1` on all five series.** `q < 1` on the comb series
reflects a constant that *falls* as the structure warms up; `q = 1.11` on the path is the
`log(vol)` factor showing up as an apparent exponent over an 8x range.

### alpha-freeness of the constant (Measured)

Zoo, `eps` tuned to `|S*| <= 2500` (so `|S*|` itself grows as `alpha` falls):

| family | a=2^-6 | a=2^-10 | a=2^-14 | max/min | chain `lev_mean/max` | swaps, `mv/|S|` |
|---|---|---|---|---|---|---|
| path | 226.9 | 276.0 | 324.0 | 1.43 | 1.00 / 1 | 0, 0.00 |
| caterpillar | 169.0 | 209.2 | 249.5 | 1.48 | 1.03 / 2 | 30, 0.04 |
| spider | 387.0 | 487.0 | 488.8 | 1.26 | 1.87 / 2 | 0, 0.00 |
| rrt2000 | 318.5 | 318.5 | 318.5 | **1.00** | 3.31 / 6 | 77, 0.16 |
| comb(512,·) | 250.9 | 365.0 | 477.7 | 1.90 | 1.77 / 2 … 2.08 / 6 | <= 27, <= 0.28 |

The residual drift is `log(vol)`, not `alpha`: normalizing,
**`W / (vol * log2 vol) ∈ [19.1, 53.6]`, median 29.2**, and
**`W / (vol * log2^2 vol) ∈ [1.59, 5.57]`, median 2.54**, over all 149 configs. On `path` the
normalized constant is `29.9 / 28.7 / 27.9` at `alpha = 2^-6/-10/-14` — flat to 7%. `rrt2000` is
*exactly* alpha-invariant (the trace is alpha-frozen).

### Full tree zoo, `W/vol` (Measured)

| family | alpha | \|S*\| | vol | E | COLD-LU | INC-LDL | TREE-INC | SEG-LDL | **HSEG** | OR-SDD | OR-INC |
|---|---|---|---|---|---|---|---|---|---|---|---|
| path | 2^-14 | 1553 | 3105 | 1552 | 1946.1 | **10.5** | 1142.7 | 324.5 | 324.0 | 13363 | 24.4 |
| caterpillar | 2^-14 | 2160 | 4319 | 1111 | 1433.0 | **17.4** | 810.7 | 343.0 | 249.5 | 10274 | 22.3 |
| spider | 2^-14 | 2481 | 4968 | 310 | 393.9 | **64.5** | 554.0 | 413.8 | 488.8 | 2837 | 20.2 |
| btree(12) | 2^-10 | 2047 | 6140 | 10 | **6.7** | >9836 (cap) | 25.5 | 270.8 | 381.9 | 33.3 | 34.7 |
| rrt2000 | 2^-14 | 2000 | 3998 | 14 | **24.9** | >15098 (cap) | 34.7 | 232.7 | 318.5 | 164.2 | 18.9 |
| theta(200³) | 2^-14 | 602 | 1206 | 201 | 258.1 | **20.9** | n/a | n/a | n/a | 1540 | 18.0 |

HSEG-LDL/best-per-family ratio: path 21–31x, caterpillar 10–14x, spider 6–7.6x, rrt 13x,
**btree 57x**. On the comb at the largest measured size (`vol = 15 158`) COLD-LU is 254.7 and HSEG
419.4 — HSEG's `q = 0.95` vs COLD-LU's `q = 1.23` puts the crossover at **`vol ≈ 1.3e5`**, beyond
this campaign. State this plainly: *the target is met in exponent, not yet in constants.*

## 4. Amortization argument (Proved-draft, with a stated hole)

Let `S_t` be the active set, `T_t` the seed-rooted tree it induces, `H_t` the maintained carving.

**(a) Chain length — proved.** The invariant maintained is: for every light edge `(u,c)`,
`sz(c) <= 2 sz(h(u))` where `h(u)` is `u`'s heavy child. Then
`sz(u) >= sz(c) + sz(h(u)) >= sz(c) + sz(c)/2 = 1.5 sz(c)`, so subtree sizes shrink by `>= 1.5x`
across every light edge and the number of light edges from any vertex to the seed is
`L <= log_{1.5}|S| ≈ 1.71 log2|S|`.
*Consequence:* an admission touches `O(L)` path-tops, each for `O(log|S|)` segment-tree nodes, and
an `x`-query walks the same chain — **`O(log^2 |S|)` charged units per admission and per boundary
query**, hence `W_admit + W_query = O((|S*| + Σ_t |F_t|) log^2 |S*|)`, alpha-free and eps-free.
Measured `lev_mean <= 5.0`, `lev_max <= 10` everywhere (btree, the deepest-chain family), against
the bound `1.71 log2(2047) = 18.8`. This is the piece that matches
`W ≈ 2.5 · vol · log2^2 vol`.

**(b) Number of swaps at a fixed vertex — proved.** Consider swaps at `u`. Immediately after a swap
promoting `c`, `sz(c) > 2 sz(h_old)`. For `c` to be demoted later, some sibling `c'` must reach
`sz(c') > 2 sz(c)`; then `sz(u) >= sz(c) + sz(c') > 3 sz(c) >= 3 · (value of sz(c) at the previous
swap)`. So **`sz(u)` at least triples between consecutive swaps at `u`**, giving
`#swaps(u) <= log_3 |S*|`.
Measured totals: `<= 77` swaps for `|S| = 2000` (rrt), `<= 30` (caterpillar), `<= 27` (comb),
`0` (path, spider, btree).

**(c) Re-carve cost — Open, this is the hole.** A swap at `u` moves `|tail| + |P_c| <= 2 sz(u)`
vertices at `O(log)` each. Combining (b) naively gives only
`O(Σ_u sz(u) · log_3|S| · log|S|) = O(|S| · depth · log^2|S|)` — a genuine `depth` factor, not
polylog, in the worst case. What is missing is a potential that pays for the *length of the moved
path* rather than its subtree size; array-backed segment trees cannot split in `O(log)`.
**The textbook remedy is a link-cut tree** (splay-based preferred paths with ordered `2x2`
aggregates + a secondary structure for the light-child sums `Σ w^2/delta`), which gives amortized
`O(log|S|)` per access and closes the gap. Empirically the hole is not exercised: total moved
vertices `<= 0.44 |S*|` on every family and size measured, and *decreasing* in size
(`comb(512,128)`: `0.276 -> 0.084` over a 21x volume range), i.e. the observed re-carve cost is
`o(|S|)`, with a constant below 1/2.
*So: the polylog claim is **proved for admission + query cost given the invariant**, and the
invariant's maintenance cost is **measured** to be sublinear but **not proved** to be polylog.*

**Potential-function form (for the write-up):**
`Phi_t = K1 * Σ_{v ∈ S_t} log_{1.5}( sz_t(parent(v)) / sz_t(v) ) + K2 * Σ_{u ∈ S_t} (log_3|S*| - #swaps_t(u)) * sz_t(u)`.
The first term is the total light-depth and is `O(|S| log|S|)` at all times, bounding queries; the
second is the swap credit. An admission raises `Phi` by `O(log^2|S|)` (its own light-depth plus the
`Σ_{u ∈ anc(v)} 1/sz(u) = O(log|S|)` size-ratio perturbation); a swap at `u` releases
`K2 · sz(u)` and costs `O((|tail| + |P_c|) log|S|)` — bounded by the release **iff**
`|tail| + |P_c| = O(sz(u)/log|S|)`, which is exactly the unproved step.

## 5. What breaks off-trees (Proved-draft)

The construction rests on two tree-only facts.

1. **Leaf elimination is rank-1 and local.** Eliminating a leaf `c` updates only `a_{parent}` by
   `-w^2/delta_c`. Hence "the impedance of everything hanging below `u`" is a **scalar** `delta_u`,
   the light contributions **add**, and a path's trailing minors satisfy a scalar three-term
   recurrence — a `2x2` transfer matrix with an `O(1)` aggregate that a segment tree can compose.
2. **Growth is by leaves.** Each admitted vertex has exactly one admitted neighbour, so the tree
   only ever gets a new leaf: `link` at a path end, never a `link` that closes a cycle.

On a general graph both fail. Eliminating a degree-`d` vertex creates a `d`-clique; a subgraph
hanging off a separator of size `k` has a **`k x k` dense Schur complement**, not a scalar, so the
transfer object becomes `2k x 2k` and composing two of them costs `k^3` (or `k^ω`). The whole
scheme therefore generalizes to **bounded treewidth with a `k^3` factor** and dies as soon as
separators grow. Corroboration from the measurements: **theta** (2-connected, treewidth 2) is still
output-linear for admission-order INC-LDL (`20.9 · vol`, `nnz(L)/|S| = 3.0`, alpha-flat) — *being
cyclic is not the obstruction*; **grid** (iteration 1, treewidth `~sqrt(n)`) defeats every real
backend (`INC-LDL 1027 · vol ≈ COLD-LU`). Additionally, an admission that closes a cycle needs a
`link` between two interior path vertices — an operation the current structure has no answer for
(the outer loop's `assert len(par) == 1` is precisely this assumption), so the tree backends are
simply `n/a` on theta above.

## 6. Honest gaps

1. **Constants.** HSEG-LDL is 6–57x above the best per-family backend at measured sizes; the comb
   crossover with COLD-LU is at `vol ≈ 1.3e5`, unmeasured. The meter constants (`MATC = 16` per
   `2x2` node, `QRYC = 10` per query node) are a stated proxy, not calibrated flops; they inflate
   HSEG relative to backends charged per scalar nonzero. A fair reading compares **exponents**, and
   compares constants only within a backend across `alpha`.
2. **Re-carve amortization is Open** (§4c). No family here forces the bad case; a family designed so
   that a long path repeatedly loses and regains heaviness at a shallow vertex would.
3. **`B` never bites** in the comb matrix (`B = 128` and `512` give identical traces): the
   value-reach clips before the backbone end. The comb's difficulty is `T ~ 1/sqrt(alpha)` plus a
   large reach, not `B`.
4. **`eps` is unusually fine in some configs** (down to `2^-34` where the graph saturates). The
   certificate is asserted in every case; but `W/vol` at such `eps` is a statement about a
   *saturated* active set, and those points are what makes `COLD-LU` look bad on `path` (`E = |S*|`,
   one admission per round).
5. **INC-LDL is capped** (memory) on btree and rrt2000; reported values are lower bounds (`>`).
6. **Non-trees untested for HSEG.** theta/grid have no HSEG number at all — not a negative result,
   an unimplemented one.
7. Only one random tree instance (`rrt(2000, seed 7)`); no ensemble.

## 7. Next falsifiable target

The sharp remaining question is now **(c), not the ordering**: *does a splay-based (link-cut)
preferred-path version of HSEG-LDL achieve worst-case amortized `O(log^2)` per admission on trees,
including a family engineered to thrash the heavy/light boundary?* Concretely: build
`thrash(k)` — a shallow root with two children whose subtrees are grown alternately so that each
crosses the other's `2x` threshold `Theta(log)` times, with each subtree a long path so every swap
moves `Theta(len)` vertices. Prediction: array-backed HSEG-LDL degrades to `Theta(|S| · depth)`
there (falsifying the empirical `mv/|S| <= 0.44`), while an LCT version stays `O(|S| log^2)`. If
that holds, trees are **closed** — `W = O(vol · polylog)`, alpha-free, hence an
`O~(1/eps)`-flavoured bound on trees — and the next frontier is bounded treewidth with the `k^3`
transfer-matrix cost, where `theta` (already output-linear) is the `k = 2` warm-up and `grid` the
known wall.
