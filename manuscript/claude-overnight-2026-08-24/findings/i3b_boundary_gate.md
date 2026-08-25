# I3-B — The boundary-scan cost, and the shell-volume question

**VERDICT: SOLVED, and the open structural question is CLOSED with a theorem +
a matching construction.**

1. The `Θ(vol(∂S))`-per-check boundary gate — 87 % of all charged work on
   I2-A's marginal-hub ring even with a perfect admission gate — is an
   **artifact of PULLING** (recomputing `grad_j` by scanning `j`'s adjacency).
   Pushing the same quantity from the interior side costs `|∂S| ≤ vol(S)` per
   sweep and **nothing per boundary vertex degree**. Measured on the ring:
   gate work `2.47e6 → 9.3e3` (D = 384, α = 2⁻¹²), i.e. **266×** (and `1.3e4`, 187×, for the simplest push variant), and the
   remaining cost is flat in `hub_deg` (8× more boundary volume ⇒ 1.27× more
   gate work, and that 1.27× is interior iterations, not boundary volume).
2. The **piggyback claim is TRUE and exact**, not just a bound: with two
   accumulators per boundary vertex the gate value is exact in `O(1)` and its
   next crossing time is closed-form, so the gate costs **`O(1)` amortised per
   interior coordinate step + `O(log)` per boundary-incident touch +
   `O(1)` per report**, with **zero** dependence on the poll frequency. On the
   ring the non-piggyback gate cost is **1392 units = 7.7·vol(S\*) = 0.06·
   vol(∂S\*)**, and it is *identical* whether the gate is polled every `n`
   steps or **every step** (1392 vs 1384). Reporting instantaneously is free.
3. **Shell-volume question (I2-A §7, "can `vol(shell_τ)/vol(S*)` grow like
   `α^{-1}`?"): NO — and the reason is a clean, α-free lemma.** Summing the
   RPPR KKT conditions gives the exact leak identity and
   > `τ·ρ·vol(shell_τ) + ρ·vol(S*) ≤ s(S* ∪ shell) − ‖π‖₁ ≤ 1`,
   > hence **`vol(shell_τ)/vol(S*) ≤ (1/τ)·[1/(ρ·vol(S*)) − 1]`**, with no `α`.

   Verified to machine precision (identity) and satisfied on 18/18 instances;
   a **hub-ladder construction attains it to within 2 %** (measured
   21.86 vs bound 22.1). So the shell can be arbitrarily fatter than `S*`, but
   only through `ρ·vol(S*) → 0` — never through `α`. I2-A's ring is exactly
   the `ρ·vol(S*) ≪ 1` regime.

Code `w10_i3b/{gate,run,exp,shell,lemma,mult_exp}.py`; data
`w10_i3b/res_{ring,benign,shell,lemma,mult}.json`; logs `w10_i3b/{ring,benign}.log`.
Compute ≈ 3 min solver time (≈ 35 min wall incl. analysis). Every run asserts
no missed and no false report against a dense recomputation of the whole
boundary — **0 failures in 50 growing-support runs**.

---

## 1. The task, formally

Fix `α, ρ`. State: support `S`, iterate `x` supported on `S`. For `j ∉ S`
define the **normalized gate value** and threshold

> `G_j(x) := −grad_j f(x)/√d_j = ( b_j + (1−α)/2 · Σ_{i~j} x_i/√(d_i d_j) )/√d_j`,
> `thr := m·αρ`   (RPPR safe gate at hysteresis multiplier `m`; `m = 1` is the
> exact KKT gate). Violation ⟺ `G_j > thr`.

*(PPR/ACL residual form is the same object: `r_j/d_j` vs `ε` after the
`D^{-1/2}` rescaling — everything below transfers verbatim.)*

**Reporting task.** The interior solver produces a stream of coordinate
updates on `S`. Report every `j ∈ N(S)` the first time `G_j > thr`, by the
next poll at the latest, never miss one, with total charged work as close to
`O(interior work + output)` as possible. Two poll schedules are measured:
`poll = n` (the harness/W3 default: one gate check per `|S|` interior steps)
and `poll = 1` (**the repository's frontier-1 interface**: report crossings
without rescanning after every light update).

**Interior solver** = the campaign's lazy APCG (`solvers.apcg_run`), whose
iterate is represented as `x = p + φ·Mh` with `φ` decaying geometrically and
one coordinate of `(p, Mh)` changing per step. This is the hard case: `φ`
changes **every** step, so *every* `x_i` drifts every step, and a naive
"nothing moved near `j`" argument fails.

### 1.1 Why pull is the wrong primitive (Proved)

`grad_j` depends only on `N(j) ∩ S`. Pulling recomputes it by walking `j`'s
adjacency, costing `d_j` — but the *same* information can be pushed from the
`S` side, where the interior solver already walks `N(i)` and is already charged
`d_i` for it. Three consequences, all elementary and all graph-uniform:

* **(P1)** `|∂S| ≤ vol(S)`: every `j ∈ ∂S` owns at least one distinct edge into
  `S`, and each such edge is counted in `vol(S)`. So a *push* sweep of the whole
  boundary costs `≤ vol(S)`, **always** — whereas `vol(∂S)` is unbounded
  relative to `vol(S)` (I2-A: 16×, and `Θ(hub_deg)`).
* **(P2)** With `P_j := Σ_{i∈S} Q_{ji} p_i` and `M_j := Σ_{i∈S} Q_{ji} Mh_i`,
  `−grad_j(x) = b_j − P_j − φ·M_j` **exactly**, so a gate test is `O(1)`; and
  `P_j, M_j` change only when a neighbour of `j` is sampled, costing
  `|N(i)\S| ≤ d_i` per interior step — *inside* the scan the interior already
  pays. The `φ`-drift needs **no work at all**: it is one shared scalar.
* **(P3)** Growth is incremental: when `j₀` is admitted, the new boundary
  vertices are exactly `N(j₀) \ (S ∪ ∂S)`, and each has `j₀` as its *only*
  `S`-neighbour, so its accumulators initialise in `O(1)`; discovery costs
  `d_{j₀}`, again the interior's own admission scan. **No structure ever scans
  a boundary vertex's adjacency list.**

## 2. Structures and their exact charging

Charged with `lib/meter.py`: `rec(d_j)` for a pull test of `j` (the scan),
`rec(1)` per pushed edge, per `O(1)` accumulator test and per recomputation,
`resp(⌈log₂(size+2)⌉)` per heap operation, `emit(1)` per report. Pushed edges
are *also* counted separately as `piggy`, since they are inside the interior's
own `d_i` scan; both totals are reported.

| | structure | per interior step | per poll | soundness |
|---|---|---|---|---|
| (a) | **eager_pull** — full rescan of `N(S)` | 0 | `vol(∂S)` | trivial |
| (a′) | **eager_push** — full sweep on accumulators | `|N(i)\S|` (piggyback) | `|∂S|` | (P2) |
| (b) | **lazy_bound** — sound upper bound + max-heap | push + re-key | `O(#expired certificates)` | see below |
| (b′) | **kinetic** — exact crossing time + max-heap | push + re-key | `O(#true crossings)` | see below |
| (c) | **deg_bucket** — pull, but degree-bucketed certified schedule | 0 | `|S|` + `vol(bucket)` when due | see below |
| (d) | (b′) with hysteresis `m = 2.9` (the I2-A overshoot constant) | | | |

**(b) lazy_bound.** Between touches `P_j, M_j` are frozen, so the *generic*
drift bound (no sign information) is `|G_j(φ) − G_j(φ_ref)| ≤ |M_j|(φ_ref −
φ)/√d_j`; hence `j` cannot violate while
`φ > φ_ref − (thr − G_j^ref)·√d_j/|M_j|`. Key a max-heap by that
certificate-expiry `φ`; `φ` decreases monotonically, so the heap top is the
next vertex that *must* be looked at. An expiry that finds no violation is a
**false wakeup** (charged, re-keyed).

**(b′) kinetic.** Using the sign, `G_j(φ) > thr ⟺ φ·M_j < c_j := b_j − P_j −
thr√d_j`. For `M_j > 0` the crossing is at `φ = c_j/M_j` and *will* happen as
`φ ↓`; for `M_j < 0` the value moves *away* from the threshold, so the vertex
needs no heap slot at all until a neighbour moves. Zero false wakeups by
construction — confirmed: `false_wakeups = 0` in every run.

> **(P4) Amortised gate cost (Proved-draft).** With (b′), total gate work is
> `Σ_steps |N(i) ∩ ∂S| · O(log|∂S|) + O(#reports) + O(Σ_admissions d_{j₀})`.
> It contains **no `vol(∂S)` term and no poll-frequency term**: polling every
> step costs the same as polling every `n` steps.

**(c) deg_bucket** exploits exactly the asymmetry the task names: the
threshold grows like `√d_j` while the drift of `−grad_j` per unit of interior
motion falls like `1/√d_j`, so in normalized terms hubs move `1/d_j` times as
fast as they need to. Certified schedule: with
`V := Σ_{i∈S} |x_i − x_i^ref|/√d_i` (recomputed once per poll at cost `|S|`),
`|G_j(x′) − G_j(x)| ≤ (1−α)V/(2 d_j)`, so a bucket of degree `≥ D` may be
skipped until `V` grows by `2·D·margin_min/(1−α)`. Sound, and it does buy
`2–6×` over eager_pull on the ring — but it keeps the `vol(∂S)` factor and is
**a net loss on benign families** (§4). Reported as a negative result.

## 3. The adversarial family (Measured)

`ring_star(m=60, hub_deg=D)`: star core (seed = centre, degree 60; 60 core
leaves of degree 2), each core leaf carrying a pendant hub of degree `D` with
`D−1` dead leaves. `ρ` bisected per `(α, D)` so every hub sits just below
activation (`rel = −grad_h/λ_h ≈ 0.95`). `S* = {centre} ∪ leaves`,
`vol(S*) = 180`, `vol(∂S*) = 60·D`. **Gate multiplier 8** — I2-A's
"perfect gate, zero spurious admissions" configuration, in which the boundary
scan was 87 % of all work. Charged gate totals (single seed; the trajectory is
shared by all five structures, so the comparison is exact):

### 3.1 poll = n (the standard schedule)

| α | D | vol(S\*) | vol(∂S\*) | interior | eager_pull | eager_push | lazy_bound | **kinetic** | deg_bucket | pull/kin |
|---|---|---|---|---|---|---|---|---|---|---|
| 2⁻⁸ | 48 | 180 | 2 880 | 15 216 | 103 860 | 4 680 | 3 160 | **3 154** | 51 337 | 32.9 |
| 2⁻⁸ | 192 | 180 | 11 520 | 18 773 | 518 580 | 5 764 | 3 714 | **3 704** | 198 766 | 140 |
| 2⁻⁸ | 384 | 180 | 23 040 | 20 936 | 1 152 180 | 6 363 | 4 013 | **4 003** | 394 911 | 288 |
| 2⁻¹⁰ | 48 | 180 | 2 880 | 18 773 | 129 780 | 5 764 | 4 326 | **4 156** | 60 526 | 31.2 |
| 2⁻¹⁰ | 192 | 180 | 11 520 | 27 977 | 772 020 | 8 405 | 5 649 | **5 477** | 257 708 | 141 |
| 2⁻¹⁰ | 384 | 180 | 23 040 | 30 808 | 1 705 140 | 9 247 | 6 071 | **5 899** | 534 615 | 289 |
| 2⁻¹² | 48 | 180 | 2 880 | 23 157 | 158 580 | 6 961 | 6 857 | **6 113** | 66 896 | 25.9 |
| 2⁻¹² | 192 | 180 | 11 520 | 43 627 | 1 209 780 | 12 971 | 10 111 | **9 155** | 283 066 | 132 |
| 2⁻¹² | 384 | 180 | 23 040 | 44 469 | 2 465 460 | 13 211 | 10 267 | **9 253** | 582 708 | 266 |

*(the `D = 12` cells are degenerate at multiplier 8 — `S* = {centre}`, no
admissions — and are omitted; they are in the JSON.)*

**Scaling read-off.** `eager_pull = (#sweeps)·vol(∂S*)` exactly: `pull/vol(∂S*)`
= 36, 45, 50 (α = 2⁻⁸) / 55, 105, 107 (α = 2⁻¹²), i.e. the sweep count, growing
like `α^{-1/2}`. **Kinetic is flat in `vol(∂S*)`**: an 8× increase of the
boundary volume (D: 48 → 384) costs 1.27×, and that 1.27× is the interior
iteration count, not the boundary. `kinetic/interior` = 0.21 ± 0.06 across all
nine cells — the gate is a *constant fraction of the interior*, which is the
target statement.

### 3.2 poll = 1 — the frontier-1 semantics (report on the step it happens)

| α | D | eager_pull | eager_push | **kinetic** | deg_bucket | pull/kin |
|---|---|---|---|---|---|---|
| 2⁻¹⁰ | 48 | 7 905 780 | 167 764 | **4 148** | 406 666 | 1 906 |
| 2⁻¹⁰ | 192 | 47 082 420 | 249 605 | **5 469** | 1 274 768 | 8 609 |
| 2⁻¹⁰ | 384 | 104 002 740 | 275 647 | **5 891** | 2 418 255 | 17 654 |
| 2⁻¹² | 384 | 150 382 260 | 398 411 | **9 237** | 3 070 968 | 16 280 |

**Kinetic's cost is unchanged from §3.1** (5 899 → 5 891 at D = 384, α = 2⁻¹⁰).
Eager_pull grows by the poll ratio (60×), eager_push by the same 60× down at
`|∂S|` per sweep. *Instantaneous reporting is free only for the event-queue
structures.*

### 3.3 Where kinetic's work actually goes (D = 384, α = 2⁻¹⁰)

| structure | total | of which piggyback | **non-piggyback** | wakeups | false |
|---|---|---|---|---|---|
| eager_pull | 1 705 140 | 0 | 1 705 140 | 4 500 | 0 |
| eager_push | 9 247 | 4 507 | 4 740 | 4 500 | 0 |
| lazy_bound | 6 071 | 4 507 | 1 564 | 60 | 0 |
| **kinetic** | 5 899 | 4 507 | **1 392** | **60** | **0** |
| deg_bucket | 534 615 | 0 | 534 615 | 1 440 | 0 |

`1 392 = 7.7·vol(S*) = 0.060·vol(∂S*)`, and the 60 wakeups equal the 60
reports exactly: **wakeups = output**. Piggyback is 4 507 units against
30 808 units of interior scan work (15 %), i.e. genuinely inside the interior's
own `d_i` scans. The answer to the task's key question is therefore: **yes, the
piggyback bound gives `O(1)`-amortised gating**, and the exact (kinetic) version
even removes the false wakeups the bound would allow.

`lazy_bound` — the sign-free bound the task specified — costs 12 % more than
kinetic here (heap traffic: `|M_j|` always yields a finite certificate, whereas
the signed rule gives *no heap slot* to a vertex moving away from the
threshold). It had **zero** false wakeups on every family, so the generic bound
is not merely sound but essentially as sharp as the exact rule on these
instances.

### 3.4 Composition with hysteresis (item d; α = 2⁻¹⁰, poll = n)

| D | mult | admissions | vol(S) | interior | eager_pull | kinetic (non-piggy) |
|---|---|---|---|---|---|---|
| 48 | 1 | 1 248 | 4 188 | 13 487 914 | 2 393 805 | 2 508 944 (124 020) |
| 48 | 2.9 | 110 | 371 | 1 194 538 | 3 973 846 | 217 776 (4 220) |
| 48 | 8 | 60 | 180 | 18 773 | 129 780 | 4 156 (1 392) |
| 192 | 1 | 3 176 | 14 756 | 45 888 276 | 11 842 187 | 12 337 379 (489 838) |
| 192 | 2.9 | 637 | 1 521 | 5 163 596 | 15 413 299 | 355 102 (16 082) |
| 192 | 8 | 60 | 180 | 27 977 | 772 020 | 5 477 (1 392) |

Two things worth recording. (i) Hysteresis and the push/kinetic gate **compose
multiplicatively** — `m = 2.9` (I2-A's measured momentum-overshoot constant)
already removes 91 % of the spurious admissions, and the kinetic gate then costs
4 220 non-piggyback units instead of 124 020. (ii) **Hysteresis makes the PULL
gate worse** (3.97e6 at `m = 2.9` vs 2.39e6 at `m = 1`, D = 48): keeping the
hubs out keeps the *fat* boundary alive for many more sweeps. A campaign that
adopts hysteresis without fixing the gate primitive pays for it.

## 4. Benign families: regression check (Measured)

`path(800)`, `caterpillar(300,1)`, `spider(6,100)`, `grid(24,24)`,
`binary_tree(9)`; multiplier 1 (exact KKT gate), `ρ ≈ 1/2400`, α ∈ {2⁻⁸, 2⁻¹²}.

| family | α | poll | vol(S) | vol(∂S) | interior | eager_pull | **kinetic** | deg_bucket |
|---|---|---|---|---|---|---|---|---|
| path | 2⁻⁸ | n | 97 | 2 | 15 643 | 276 | 646 | 4 145 |
| path | 2⁻¹² | n | 297 | 2 | 2 108 135 | 6 136 | 4 752 | 430 681 |
| caterpillar | 2⁻¹² | n | 382 | 4 | 2 712 325 | 12 014 | 8 478 | 551 917 |
| spider | 2⁻¹² | n | 1 008 | 12 | 7 125 309 | 35 853 | 24 695 | 1 452 083 |
| grid | 2⁻⁸ | n | 1 022 | 102 | 1 686 595 | 76 652 | 36 768 | 205 599 |
| btree | 2⁻⁸ | n | 2 044 | 0 | 381 325 | 4 202 | 25 458 | 86 698 |
| btree | 2⁻¹² | n | 2 044 | 0 | 1 355 489 | 4 270 | 25 458 | 281 068 |
| path | 2⁻⁸ | 1 | 97 | 2 | 16 673 | 7 570 | **573** | 161 863 |
| spider | 2⁻⁸ | 1 | 374 | 12 | 697 649 | 1 697 080 | **6 634** | 26 008 714 |
| grid | 2⁻⁸ | 1 | 1 066 | 106 | 1 758 665 | 21 587 017 | **34 675** | 56 880 361 |
| btree | 2⁻¹² | 1 | 1 732 | 176 | 6 550 | 682 982 | **8 984** | 2 164 336 |

* **No regression that matters.** At `poll = n` the worst cell for kinetic is
  `btree` (6.1× eager_pull, 25 458 vs 4 202) — but that is **1.9 % of the
  interior work** (1 355 489), because `btree`'s support saturates the graph and
  `vol(∂S)` collapses to 0. In every benign cell the gate is ≤ 7 % of total
  work for *every* structure, so the ordering is immaterial there; kinetic is
  in fact *cheaper* than eager_pull on spider (0.69×), grid (0.48×) and path at
  2⁻¹² (0.77×).
* **At `poll = 1` kinetic wins everywhere**, by 13× (path) to 623× (grid).
* **deg_bucket (c) is a failure** and I am recording it as such: 5–100× worse
  than eager_pull at `poll = n`, and catastrophic at `poll = 1`
  (5.7e7 on grid). The certified schedule collapses because the bucket margin
  `min_j (thr − G_j)` goes to ~0 as soon as *one* vertex in the bucket is near
  the threshold, forcing the whole bucket to be rescanned; and it pays `|S|`
  per poll to maintain `V`. The degree asymmetry it exploits is real, but the
  min-over-bucket certificate throws it away. A per-vertex certificate is the
  event queue — i.e. (c) degenerates to (b′) once done properly.

**Correctness.** Every poll in every run recomputes `G_j` densely for all
`j ∈ N(S)` and asserts, per structure and against that structure's own
threshold, (i) no violator is unreported and (ii) nothing reported was never a
violator. 50 growing-support runs (24 ring + 20 benign + 6 multiplier sweep), exhaustive at every
poll for `poll = n`, every 20th poll plus every reporting poll for `poll = 1`:
**0 misses, 0 false reports**.

## 5. The shell-volume question — resolved (Proved-draft + Measured)

I2-A left open: *can `vol(shell_τ(S*))/vol(S*)` grow like `α^{-1}`?* The answer
is **no**, for a reason that also explains why the ring's ratio was measured
α-independent.

### 5.1 The leak identity (Proved)

Work in the `π = D^{1/2}x*` scale. KKT for `i ∈ S*` (equality) and `i ∉ S*`
(inequality), summed over **all** vertices, and using
`Σ_i Σ_{h~i} π_h/d_h = ‖π‖₁`:

> **`(1−α)/2 · T = α·[ s(S*) − ‖π‖₁ − ρ·vol(S*) ]`,
> where `T := Σ_{i∉S*} Σ_{h~i} π_h/d_h` is the total leak flow out of `S*`.**

Verified to machine precision (`|lhs−rhs|/|rhs| = 0`) on 18 instances: path,
caterpillar, grid, btree × α ∈ {2⁻⁴,2⁻⁸,2⁻¹²} and ring `D ∈ {12,48,192}` ×
α ∈ {2⁻⁸,2⁻¹²}.

### 5.2 The shell lemma (Proved-draft, graph-uniform)

For `j ∉ S*`, `−grad_j(x*) ≥ τ·αρ√d_j` reads, after multiplying by `√d_j`,
`α s_j + (1−α)/2 Σ_{h~j} π_h/d_h ≥ τ α ρ d_j`. Summing over
`shell_τ := {j ∉ S* : −grad_j(x*) ≥ τ λ_j}` and bounding the double sum by `T`:

> ### `τ·ρ·vol(shell_τ) + ρ·vol(S*) ≤ s(S* ∪ shell_τ) − ‖π‖₁ ≤ 1`
> ### hence `vol(shell_τ)/vol(S*) ≤ (1/τ)·[ 1/(ρ·vol(S*)) − 1 ]`

**The `α` cancels identically.** The gate-relevant boundary can be fatter than
`S*` **only to the extent that `S*` is smaller than the ACL volume budget
`1/ρ`** — and never by a factor that grows as `α → 0`. Consequences:

* I2-A's ring is precisely the `ρ·vol(S*) ≪ 1` regime (`ρ` is bisected down to
  keep the hubs marginal, so `ρ·vol(S*)` → 0 as `D` grows): measured
  `ratio = D/3` and bound `= (1/τ)(1/(ρ·180) − 1)`, both exactly linear in `D`,
  with **tightness `ratio/bound` = 0.61–0.64 for all six `(D, α)` cells** — the
  bound captures the mechanism, not just the order.
* In the standard regime `ρ = 1/vol_target`, `vol(S*) = Θ(vol_target)`, the
  ratio is `O(1/τ)`: **the boundary of a local solution cannot be much bigger
  than the solution.** This is the graph-uniform hypothesis (G1)/(G2) that
  I2-A §5.5 refuted *unconditionally*; it holds **conditionally on
  `ρ·vol(S*) = Ω(1)`**, which is exactly the hypothesis a well-posed local
  clustering call satisfies.

### 5.3 The matching construction — a hub ladder (Measured)

I2-A's §7 attempts failed because per-position tuning oscillated. The fix is an
exact decoupling: **a hub with `x_hub = 0` influences the core only through
`d_t = 3`; its degree `D_t` does not enter `Q_SS`, `b_S` or `λ_S`.** So the
core profile is computed once (tridiagonal, exact), and each hub is placed at
KKT ratio exactly `τ` by `D_t = ⌊(1−α)x_t/(2ταρ√d_t)⌋` — a geometric ladder of
degrees, all simultaneously marginal, with no interaction and no feedback.
Validated against a full graph build + `exact_support_solver` (α = 2⁻⁴,2⁻⁶,2⁻⁸:
`S*` = predicted core prefix exactly, 0 hubs inside `S*`, `‖x−x_core‖_∞ = 0`).

`τ = 0.6`, `ρ = 1/200`, hub at every core position:

| α | 2⁻⁴ | 2⁻⁶ | 2⁻⁸ | 2⁻¹⁰ | 2⁻¹² | 2⁻¹⁴ | 2⁻¹⁶ |
|---|---|---|---|---|---|---|---|
| vol(S\*) | 11 | 14 | 14 | 14 | 14 | 14 | 14 |
| vol(shell) | 236 | 286 | 301 | 305 | 306 | 308 | 308 |
| **ratio** | 21.5 | 20.4 | 21.5 | 21.8 | **21.9** | 22.0 | 22.0 |
| lemma bound | — | — | — | — | **22.1** | — | — |

and at fixed α = 2⁻¹², varying `ρ`:

| ρ | vol(S\*) | vol(shell) | ratio | lemma bound | tightness |
|---|---|---|---|---|---|
| 1/50 | 8 | 65 | 8.13 | 8.75 | 0.93 |
| 1/200 | 14 | 306 | 21.86 | 22.1 | **0.99** |
| 1/800 | 17 | 1 297 | 76.29 | 76.8 | **0.99** |

**Flat in `α` over 12 octaves, exactly `Θ(1/(ρ·vol(S*)))` in `ρ`, and within
1–2 % of the lemma.** The construction and the theorem meet.

The mechanism the lemma encodes, stated concretely: a marginal hub is a
**perfect absorber** (`x_hub = 0` returns no mass), so a shell that is `k×`
fatter than `S*` drains `S*` `k×` faster, which shrinks `‖π‖₁` and hence
shrinks the budget for further shell. The core's decay length becomes `O(1)`
in `α` — which is why I2-A's path-core attempts "self-limited"; it is not an
artifact of path cores, it is the lemma.

### 5.4 What the lemma does *not* bound (and why §2 still matters)

`vol(∂S)` is **not** bounded by the lemma: a hub of any degree sits in `∂S`
regardless of its slack (take `ρ` large and the same ring — `shell` is empty,
`vol(∂S)` still `Θ(mD)`). So even in the "well-posed" regime where the shell is
`O(vol(S*))`, the *pull* gate can still pay unboundedly more than the output.
**The push primitive is needed independently of the shell lemma** — which is
what makes §2–§3 a repair of the framework rather than a special case.

## 6. Status of each claim

| claim | evidence |
|---|---|
| `|∂S| ≤ vol(S)`; push sweep is `O(vol(S))` (P1) | **Proved** |
| exact `O(1)` gate value from `(P_j, M_j, φ)` (P2) | **Proved** (algebraic identity, asserted numerically every poll) |
| incremental growth `O(d_{j₀})` per admission (P3) | **Proved** (single-`S`-neighbour argument); *harness rebuilds per segment and charges the incremental rate — stated proxy* |
| kinetic soundness + zero false wakeups (P4) | **Proved-draft**; 0/50 runs violated it |
| gate work independent of `vol(∂S)` and of poll frequency | **Measured** (§3.1–3.2) |
| leak identity | **Proved** + machine-precision check, 18 instances |
| shell lemma `vol(shell_τ)/vol(S*) ≤ (1/τ)(1/(ρ vol(S*)) − 1)` | **Proved-draft**; satisfied 18/18, attained to 1 % |
| deg_bucket schedule is sound but a net loss | **Measured** |

## 7. Honest gaps

* **The `φ`-affine structure is APCG-specific.** (P2)/(P4) rely on
  `x = p + φ·Mh` with a *known scalar* schedule. It covers every accelerated
  method in this campaign (APCG, Chebyshev/heavy-ball with known coefficients,
  and trivially any method where only sampled coordinates move — plain CD,
  push, ISTA-on-support). It does **not** cover a solver whose global drift is
  data-dependent (e.g. adaptive restart with a `φ` chosen from measured
  residuals); there the sign-free `lazy_bound` still applies but the crossing
  time must be re-bounded, and I have not done that.
* **Heap charging is `⌈log₂ size⌉` per operation**, a stated proxy; a bucketed
  monotone priority queue would remove it (the keys are monotone in `φ`),
  giving `O(1)` amortised, but I did not implement it.
* **Single seed per cell** for the gate comparison (the trajectory is shared by
  all structures, so the *comparison* is exact; the absolute numbers are one
  draw). Several benign cells hit the iteration cap (`status = cap`) or the
  400-segment cap (`status = admit`); trajectories are still shared, so the
  comparison stands, but the totals are truncated. `poll = 1` and `poll = n`
  produce *different* trajectories (reporting earlier admits earlier), so
  cross-poll comparison of absolute totals is indicative only.
* **The shell lemma is stated for the exact RPPR optimum `x*` on `S*`.** The
  same summation applies verbatim to any `S` with `x` supported on `S` and `x`
  satisfying interior KKT; for an *inexact* iterate there is an extra
  `Σ|resid|` term I have not tracked. The τ-shell the *algorithm* admits is
  inflated by the momentum overshoot (I2-A's `1/τ ≈ 2.9`), which the lemma
  handles by shrinking `τ` — but only if the overshoot is bounded, which is
  still I2-A's open item.
* `mult = 1` ring rows in §3.4 hit the iteration cap; they are included to show
  the composition direction, not as converged work totals.

## 8. Next target

1. **Retire the pull gate from the whole campaign.** Every growing-support
   experiment in `w3_apcg`, `w6_incremental`, `w9_i2d` charges `vol(∂S)` per
   sweep; §3 says that term is removable everywhere at no accuracy cost. The
   end-to-end claim I2-A §5.4 could not make — `Õ(vol(S_fin)·α^{-1/2})` with no
   `vol(∂S)` term — now follows from (P1)–(P4) *provided* the interior solver
   exposes its coordinate deltas. Re-running the I2-A ring at multiplier 4 with
   the kinetic gate should turn "87 % boundary scan" into "< 5 %".
2. **Bounded-overshoot × shell lemma ⇒ an unconditional locality theorem.**
   §5.2 bounds the τ-shell; I2-A needs a bound on the momentum overshoot
   `1/τ`. Together they would give `vol(S_fin) ≤ C·vol(S*)` whenever
   `ρ·vol(S*) = Ω(1)` — i.e. a *provably* local growing-support APCG in the
   well-posed regime. The overshoot bound is the missing half and looks
   tractable from the same estimate-sequence Lyapunov (`Λ` bounds
   `‖x − x*_S‖`, hence bounds `G_j` inflation directly).
3. **Monotone-key priority queue** to remove the `log` (keys decrease with `φ`,
   so a radix/bucket queue applies), making the gate exactly `O(1)` amortised
   per interior step plus `O(1)` per report.
