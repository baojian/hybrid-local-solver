# I6-C — Closing the ladder's two Opens

**Verdicts.**

* **Open 1 (the constant `Phi`): CLOSED, positive.** For every finite graph,
  every seed, every `alpha in (0,1)`: `max_u pi_u/d_u` is attained at the seed
  and only there, hence `Phi := max_u pr(e_u)_v / pi_v = 1` exactly, always.
  Proved by a five-line maximum principle (Theorem 1.1). The general-graph
  `O_B` corollary of the ladder now holds with no instance constant
  (Theorem 1.3 = "A''"). One erratum to I2-D's display is documented (§1.4).
* **Open 2 (`R+-` beyond the star): CLOSED as a scope theorem; the residual
  question is reduced to one sharply-bounded gap.** The maximum principle
  itself supplies the missing tools: (i) a nonempty `S_eps` always contains
  the seed, so the "remote-seed" route is void; (ii) the mass ceiling
  `M_eps <= (pi_v/d_v) vol(S_eps)` caps every bulk-travel argument. The
  proved `R+-` lower envelope is `W >= max(vol(S_eps), T_seed, T_bulk)`
  (Theorem 2.3, `T_bulk` new), and on **every uniformly-bounded-degree
  instance the entire envelope is `o(1/(sqrt(alpha) eps))`** (Theorem 2.5):
  within all mechanisms this campaign has proved, the `sqrt(alpha)`-coupling
  of Theorem B.4 is forced **only** by star-type seeds
  (`d_v sqrt(pi_v) = Omega(1/eps)`). Seed self-return
  `pi_v/gamma_alpha = Theta(1/alpha)` per se is *not* the criterion;
  `d_v sqrt(pi_v)` is (§2.6). What remains open is a single measured gap of
  width `~sqrt(1/eps)` on well-mixed bounded-degree instances (§2.8) — it
  **replaces** the old Open 2.

**Verification.** Three scripts, all pass:
`/home/claude/work/overnight/i6c/open1_maxprinciple.py` (18 instances x 5
alphas x {P1,P2,P3,P5} + 3 exact-rational cells: **0 failures**),
`/home/claude/work/overnight/i6c/open2_scope.py` (envelope/ceiling battery,
lollipop family, 60-run member battery: **0 failures**), and the extended
`/home/claude/work/overnight/i5d/verify_ladder.py` with the new check **C14**:
**45 cells x 14 checks, 0 failures** (rerun ~2 min). Logs in `i6c/out/`.
Conventions as I5-D: `H = I - c_a A D^{-1}`, `H pi = gamma_a e_v`,
`c_a = (1-alpha)/(1+alpha)`, `gamma_a = 2 alpha/(1+alpha)`, work `d_u` per op,
`err(z) = max_u |pi_u - z_u|/d_u <= eps = eps_ppr`.

---

## 1. Open 1: `Phi = 1` — the maximum principle

**Theorem 1.1 (maximum principle at the seed; Proved-draft).** Let `G` be
finite with no isolated vertices, `s >= 0`, `1^T s = 1`, and
`H pi = gamma_a s`. Then `u := pi_j/d_j` attains its maximum on `supp(s)`;
for the single seed `s = e_v`, `max_j pi_j/d_j = pi_v/d_v`, and
`pi_j/d_j < pi_v/d_v` strictly for every `j != v`.

*Proof.* Row `j` of the system is `pi_j = gamma_a s_j + c_a sum_{x~j} pi_x/d_x`.
Dividing by `d_j`,

```text
u_j = gamma_a s_j / d_j + c_a * avg_{x~j} u_x .
```

`pi >= 0` (Neumann series, F2), and `u_v >= gamma_a/d_v > 0`, so
`max u > 0`. If the maximum were attained at some `j` with `s_j = 0`, then
`max u = u_j = c_a * avg_{x~j} u_x <= c_a * max u < max u`, a contradiction.
Strictness off the seed for `s = e_v`: any `j != v` has
`u_j <= c_a max u = c_a u_v < u_v`. (On a component not containing `v`,
`pi = 0 < u_v`.) ∎

**Corollary 1.2 (`Phi = 1`; the operative form).** By reversibility
(`H^{-1} D` is symmetric because `HD = D - c_a A` is),

```text
pr(e_u)_v = gamma_a (H^{-1})_{vu} = pi_u d_v / d_u ,
```

so `pr(e_u)_v / pi_v = (pi_u/d_u)/(pi_v/d_v) <= 1` with equality iff
`u = v`. Hence I2-D Prop 2.6's constant `Phi = max_u pr(e_u)_v/pi_v` equals
`1` on **every** instance, and the potential weights of Lemma A.3 satisfy
`phi_u <= phi_v = 1` graph-free. *(Verified: P1/P2 over 18 zoo instances
(star centre+leaf, path end+mid, cycle, spider, caterpillar, theta, binary
tree root+leaf, grid centre+corner, 3-regular, decoy hub, complete, double
cycle, lollipop) x alpha in {0.9, 2^-2, 2^-4, 2^-8, 2^-12}: 90/90, strict —
max off-seed ratio `0.99951 < 1`; exact-rational (Fraction elimination) on
star5-leaf, path7, theta(2,3,4): 3/3.)*

**Theorem 1.3 ("A''": the general-graph `O_B` corollary, Phi-free;
Proved-draft).** Finite connected `G`, seed `v`, `eps` with
`eps vol(G) <= 1 - tau'` for some `tau' > 0`. Every `M+-` member whose output
`z + Mr`, `M in O_B` with `gamma_a B <= 1 - eps vol(G) - tau` (`tau > 0`),
satisfies `err <= eps`, performs

```text
N_v^+ >= ln( (1 - gamma_a B) / (eps vol(G)) ) / ( -ln(1 - gamma_a/pi_v) ),
W >= d_v N_v^+ .
```

*Proof.* Lemmas A.1–A.2 and A.3(i) of I5-D are already graph-free. The only
star-specific step was A.3(ii)'s `Psi_T <= ||r_mass||_1`, which needed
`||phi||_inf = phi_v`; that is now Corollary 1.2. Then
`Psi_T <= ||r||_1/gamma_a <= eps vol(G)/(1 - gamma_a B)` by A.3(i) and the
proof of Theorem A.4 goes through verbatim. ∎
This retires the `Phi` from the last statement in which it survived; the
star remains the extremal instance (`vol` smallest at fixed `m`, `pi_v`
maximal).

### 1.4 Erratum to I2-D Prop 2.6's display

I2-D wrote `Phi = max_u pr(e_u)_c/pi_c = max_u d_u pi_u/(d_c pi_c)`. The
first (operative, used-in-proofs) form is the one Theorem 1.1 settles at `1`.
The second display is a scale slip: the correct identity is
`pr(e_u)_c/pi_c = (pi_u/d_u)/(pi_c/d_c)`, i.e. degrees **divide**, not
multiply. The product form is not `<= 1` in general — measured
counterexample: leaf-seeded `K_{1,64}` at `alpha = 2^-12` has
`max_u d_u pi_u/(d_v pi_v) = 3857` (P3). I2-D's "measured `Phi = 1` on 10
zoo graphs" was correct because its zoo seeded the canonical high-value
vertices, where both forms coincide. No downstream statement used the
product form.

### 1.5 New check C14 in `verify_ladder.py`

Per grid cell: (a) star: `pr(e_u)_c` maximised at `c`, strictly, and
`pr(e_c)_c = pi_c` (so `Phi = 1` exactly on the ladder's instance);
(b) reversibility `pr(e_u)_c = pi_u d_c/d_u` entrywise; (c) mini-zoo at the
cell's `alpha` (path-end, leaf-seeded star, binary tree): `argmax pi/d ==
seed`, strict, plus the mass ceiling of §2.2. **45 x 14 checks, 0 failures.**

---

## 2. Open 2: the scope of the `R+-` `sqrt(alpha)`-coupling

### 2.1 Seed-support lemma (unconditional)

**Lemma 2.1.** `S_eps := {u : pi_u/d_u > eps}` is either empty or contains
`v`; it is nonempty iff `pi_v/d_v > eps`.
*Proof.* Theorem 1.1. ∎
This is the general criterion behind i4c §6.1's discovery that the
manuscript's long spider has `S_eps = emptyset` (there `pi_v/d_v < eps`), and
it kills, at one stroke, every "remote seed" hard-instance design: a seed
made worthless (`pi_v/d_v <= eps`) *empties the entire output*, so `z = 0`
is correct at `W = 0`. *(Part A2: lollipop family — seed at the far end of a
`1/sqrt(alpha)` path feeding a pool, the natural remote-seed candidate — has
`S_eps = emptyset` on all 6 tuned cells; pool mass `0.001–0.03`, exactly as
Lemma 2.2 forces.)*

### 2.2 Mass ceiling (unconditional)

**Lemma 2.2.** For every `S subseteq V`:
`M_S := sum_{u in S} pi_u <= (pi_v/d_v) * vol(S)`.
*Proof.* `pi_u <= (pi_v/d_v) d_u` termwise (Theorem 1.1). ∎
*(P5: verified on the full battery; on the tuned instances of Part A the
ceiling is 92–100% attained — it is the right inequality, essentially tight.)*

### 2.3 The proved `R+-` lower envelope

Per-op caps (both are the `tau` functional of I5-E at `tau = 1`, i.e. the
Cauchy–Schwarz `|(H_sym y)_u| = |<y, e_u>_{H_sym}| <= sqrt(2 Phi) *
sqrt((H_sym)_{uu})` with `(H_sym)_{uu} = 1`, plus `Phi_t <= Phi_0 =
gamma_a pi_v/(2 d_v)`):

```text
|delta| = omega |r_u| <= 2 sqrt(2 Phi_0 d_u) = 2 sqrt(gamma_a pi_v d_u / d_v) =: capD(u).
```

**Theorem 2.3 (envelope; Proved-draft, pathwise, any graph).** Every `R+-`
member stopping with `err(z) <= eps` pays

```text
W >= max( vol(S_eps),                                       [output floor]
          T_seed := d_v (pi_v - eps d_v)_+ / capD(v),        [seed travel]
          T_bulk := dmin_S (M_eps - eps vol(S_eps))_+ / capD(dmax_S) ),  [bulk travel — NEW]
```

where `M_eps = sum_{S_eps} pi_u` and `dmin_S, dmax_S` are the extreme degrees
on `S_eps`. *Proof.* Output floor: I4-D. Seed travel: `z_v` changes only at
ops based at `v`, must reach `pi_v - eps d_v`, each op moves it at most
`capD(v)` (i4c Prop 3.4 / i5e B1 at `tau_v({v}) = 1`). Bulk travel:
`sum_{S_eps} z_u^T >= M_eps - eps vol(S_eps)`; each op based at
`u in S_eps` contributes at most `capD(u) <= capD(dmax_S)` to that sum and
costs `>= dmin_S`; ops based outside `S_eps` contribute nothing to it. ∎
*(Star consistency: `T_seed * sqrt(alpha) eps = 3/128 = 0.0234` on the
dyadic grid — exactly Theorem B.4's constant, seen in the Part-A control
rows. Part B asserts `W >= envelope` on every finishing member run: 0
violations in 60 runs, including greedy Southwell and random policies.)*

### 2.4 Ceilings: what the envelope can never certify

**Proposition 2.4 (Proved-draft).** With `Delta := max degree on
`S_eps ∪ {v}`` and using `eps vol(S_eps) < 1` (I4-D) and Lemma 2.2:

```text
vol(S_eps) * sqrt(a) eps  <  sqrt(alpha),
T_seed * sqrt(a) eps     <=  (Delta eps / 2) * sqrt((1+alpha)/2),
T_bulk * sqrt(a) eps     <=  sqrt( Delta * (pi_v/d_v) * (1+alpha)/8 ).
```

*Proof.* First: immediate. Second: `T_seed <= (d_v/2) sqrt(pi_v/gamma_a)`,
`pi_v <= 1`. Third: `M_eps <= (pi_v/d_v) vol(S_eps)` (Lemma 2.2), then
`T_bulk <= (dmin/sqrt(dmax)) sqrt(pi_v/d_v) vol(S_eps) (1+alpha)/(4 sqrt(alpha))`;
multiply by `sqrt(alpha) eps` and use `eps vol(S_eps) < 1`,
`dmin/sqrt(dmax) <= sqrt(Delta)`. ∎

So the **only** way any envelope term reaches the star scale
`c/(sqrt(alpha) eps)` is:

* `T_seed`: `d_v sqrt(pi_v) >= 2c/eps * (1+alpha)^{-1/2}...` — i.e.
  **`d_v sqrt(pi_v) = Omega(1/eps)`**, forcing `d_v = Omega(1/eps)` (since
  `pi_v <= 1`) *and* `pi_v = Omega((eps d_v)^{-2}...)` — the reflecting
  high-degree-with-mass seed. The star has it (`d_v = m`, `pi_v = Theta(1)`).
* `T_bulk`: `pi_v/d_v = Omega(1/Delta)` — a *retentive* seed holding
  constant degree-normalized mass.

### 2.5 Bounded degree kills the retentive corner too

**Theorem 2.5 (bounded-degree scope; Proved-draft modulo one classical
citation).** If all degrees are `<= Delta = O(1)` and `vol(S_eps) ->
infinity` (any family with `vol(S_eps) = Theta(1/eps)` qualifies), then

```text
envelope * sqrt(alpha) * eps  =  O( sqrt(alpha) + Delta eps + sqrt(Delta(pi_v/d_v)) )  -> 0 ,
```

because `pi_v/d_v <= (1+alpha) d_v / vol(G) + C sqrt(Delta alpha) -> 0`.
The last bound is the classical discounted return-probability estimate for
simple random walk on bounded-degree graphs
(`p_k(v,v) <= (bipartite-safe stationary term) + C' Delta^{3/2} k^{-1/2}`,
via `vol(B_r(v)) >= r+1` and a Nash-type argument; summed against
`gamma_a c_a^k` it gives the display). We cite it rather than re-derive.
*(Measured across the battery: the fitted kernel constant is `<= 0.12`
with the bipartite-safe floor `(1+alpha) d_v/vol(G)` — Part A `krnC`
column; and `envelope * sqrt(alpha) eps` is `<= 0.031` everywhere on the
bounded-degree battery and halves with each halving of `eps`, i.e. behaves
as `Theta(sqrt(eps))`, while the star-control rows sit flat at `0.0234`.)*

**Conclusion (scope).** Within every mechanism this campaign has proved —
output floor, seed travel, bulk travel; all pathwise per-op-cap arguments —
the `Theta(1/(sqrt(alpha) eps_ppr))` class bound for `R+-` is exclusively a
**star-type phenomenon**: it requires `d_v sqrt(pi_v) = Omega(1/eps)`.
No bounded-degree family can be proved hard by these tools.

### 2.6 What replaces "self-return" as the criterion

I5-D §7 framed Open 2 around `pi_v/gamma_alpha = Theta(1/alpha)`. The right
invariant is sharper: the caps all run through
`Phi_0 = gamma_a pi_v/(2 d_v)`, and the forcing criterion is
`d_v sqrt(pi_v) = Omega(1/eps)` (equivalently `d_v^2 pi_v = Omega(1/eps^2)`,
the task's `d_v^2 pi_v >~ vol^2 alpha... ` display evaluated at
`vol(S_eps) = Theta(1/eps)`). High self-return without high degree cannot
force (Theorem 2.5); high degree without retained mass cannot either
(`T_seed` needs `pi_v > eps d_v` — Lemma 2.1's criterion — and the log-free
travel needs `pi_v = Omega(1)`-scale mass).

### 2.7 Member side (Measured): bounded-degree instances are *not* shown easy

Part B, well-mixed bounded-degree instances (`cycle`/`path`, `vol(G) =
1/(2 eps)`, `S_eps = V`), `eps in {2^-5,2^-6,2^-7}`, `alpha in {eps^2,
eps^3}`, five members each. Findings:

* Frontier member: **forward natural-order sweeps at `omega = 2 - 2
  sqrt(alpha)`**, at `W * sqrt(alpha) * eps = 0.094–0.164`, flat in `alpha`
  — i.e. the best member found still pays `Theta(1/(sqrt(alpha) eps))`, the
  star scale. SOR(`omega*`) sits 1.3–1.5x above it; GS and greedy Southwell
  are `Theta(1/alpha)`-type; nothing approaches `O~(vol)`.
* The proved envelope is attained-scale `T_bulk = 0.175/sqrt(alpha eps)`
  (cycle; `0.087` path) — **exactly flat** in both parameters. Member/LB gap:
  cycle `4.0 -> 6.3`, path `9.4 -> 20.8` as `eps` halves twice — growth
  `~sqrt(2)` per halving, i.e. the predicted `sqrt(1/eps)` window.
* No member run violated the envelope or any per-op cap (asserted per op).
* Methodological trap worth recording: **fwd+bwd alternating sweeps are
  SSOR, not SOR** — they destroy the `omega*` acceleration entirely
  (43 824 vs 86 sweeps on `path(8)` at `alpha = 2^-15`); Young's theory
  needs the consistently-ordered one-directional sweep (natural or
  red–black both work, measured).

### 2.8 The residual open (replaces Open 2)

> On well-mixed bounded-degree instances (`vol(G) = Theta(1/eps)`,
> `S_eps = V`), the proved `R+-` lower bound is
> `Theta(max(1/eps, 1/sqrt(alpha eps)))` (Theorem 2.3) and the measured
> member frontier is `Theta~(1/(sqrt(alpha) eps))`. Close the
> `sqrt(1/eps)` window: either (a) a genuinely new mechanism — necessarily
> *not* a per-op travel cap; it must count sweeps/slow-mode round trips —
> proves `Omega(1/(sqrt(alpha) eps))` for all of `R+-` there, in which case
> bounded-degree families *do* force the star scale after all (and §2.5
> means any such proof is structurally new); or (b) some member beats
> `1/(sqrt(alpha) eps)` there, in which case star-type seeds are necessary
> full stop.

Everything else formerly under Open 2 is closed: the remote-seed branch is
void (Lemma 2.1), the bulk branch is capped (Lemma 2.2 + Prop 2.4), the
spider route was already closed (i4c §6.1), and the seed-mechanism
dichotomy is Theorem 2.5.

---

## 3. Updated status of the ladder package

| item | was (I5-D §7) | now |
|---|---|---|
| Open 1 (`Phi`) | Measured on 10 graphs, Open | **CLOSED**: `Phi = 1` proved (Thm 1.1/Cor 1.2); A'' proved (Thm 1.3); C14 added; I2-D display erratum filed |
| Open 2 (`R+-` beyond star) | Open, two branches | **CLOSED as scope theorem** (Thms 2.3–2.5, Lemmas 2.1–2.2); residual: the `sqrt(1/eps)` member-vs-LB window of §2.8 |

**Open list of the package after I6-C (complete):**
1. §2.8's `sqrt(1/eps)` window on well-mixed bounded-degree instances
   (successor of Open 2; strictly narrower).
2. (Inherited, unchanged, out of ladder scope): one-hop *block* relaxations
   escape Lemma B.3 by design (i5e); exact-arithmetic assumption of the W1
   characterization lemma; `Theta`-tightness of B.5's semantic-stop constant
   is Measured only.

**Audit readiness.** With C14 the single script `verify_ladder.py` covers
every numbered claim of I5-D *plus* Open 1 (630 cell-checks, 0 failures);
`i6c/open1_maxprinciple.py` and `i6c/open2_scope.py` cover the new
statements (exact-rational spot checks included). All proofs above are
short, self-contained, and flagged Proved-draft (unaudited); the single
imported classical fact (bounded-degree return-probability decay, §2.5) is
isolated and numerically corroborated. The package is, in our judgment,
ready for external audit with one honest Open remaining (§2.8).

**Supersession.** This note supersedes I5-D §7's two Opens and I2-D
Prop 2.6's `Phi`-dependent form (use Theorem 1.3); it leaves every other
I5-D statement untouched. The I5-E `tau` framework is confirmed as the
unifying language: both caps of Theorem 2.3 are `tau = 1` instances, and
`tau_v(V) = pi_v/gamma_a` remains the block-escape parameter.
