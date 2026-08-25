# I3-C — The Perron truncation lemma: PROVED, and the general-graph crux relocated

**VERDICT on the named inequality: PROVED, exactly, with no constant — and in a
strictly stronger form than asked.** For every positive `v`, every `u >= 0` and
every `Delta > 0`,

```
||P min(u, Delta v)||_2 <= ||P u||_2 ,        P = I - v v^T / ||v||^2 ,
```

and the same holds in the **Q-weighted norm** `||.||_Q` (the norm the C7/C8
defect chain actually uses), and for **every coordinatewise 1-Lipschitz map
applied in the `v`-scaled coordinates**, not just `min(.,Delta)`. The proof is a
two-line weighted-variance argument (§2). Evidence: **Proved-draft** (§2),
plus 1.5M random samples, adversarial local search, 2520 exact-rational
instances, and 420/420 exact checks inside the actual recurrence — 0 violations
anywhere (§3).

**But the lemma does not, by itself, deliver the general-graph theorem, and the
reason is now precisely identified.** The i2c note located the crux in
*non-regularity* (`D != cI`). That was the wrong diagnosis: in the engine's own
hat coordinates the slow eigenvector **is** the constant vector and the
retraction cap **is** already a multiple of it, so non-regularity costs nothing.
The real obstruction is the **support face**. When `|S*| < n` the operator
governing the recurrence is the principal submatrix `Qt_{S*}`, whose Perron
vector `v_S` is *not* `D_S^{1/2}1`; the algorithm's cap `Delta * D^{1/2}1` is
then misaligned with `v_S`, and L-E is **refuted in the actual recurrence** with
ratio **238.5** on the P24 tuned-rho cell (§6). Refuted-draft, explicit
counterexample.

Code: `w7_windowed/{i3c_search,i3c_search2,i3c_transfer,i3c_pstage,i3c_p24,i3c_face}.py`.
Data: `i3c_search.json`, `i3c_transfer.json`, `i3c_pstage.json`, `i3c_face.json`.
Compute ~32 min.

---

## 1. The inequality, stated in the project's coordinates

The engine (`engine.py:156`) works in hat coordinates `xh = D^{-1/2} x` and
retracts

```
rh_i = min(beta * dh_i, Delta)              (cap at a CONSTANT level)
```

Multiplying by `D^{1/2}` (a positive diagonal, so it commutes with `min`):

```
r_i = min(beta * d_i, Delta * v_i)   in x-coordinates,   v := D^{1/2}1.
```

> **The engine's cap is already `Delta * v`.** The i2c remark that "the
> retraction cap is a multiple of `1`, misaligned with `v`" is a coordinate
> confusion: `Delta*1` in *hat* coordinates is `Delta*v` in *x* coordinates.

Which `v` and which projector are the right ones is forced, not chosen:

* `Qt = D^{1/2} Q D^{1/2}`, `M := D^{-1} Qt`. `M` is **`D`-self-adjoint**
  (`<u,Mw>_D = u' Qt w`), and `M 1 = alpha 1` because `Qt 1 = alpha d`.
  So **in hat coordinates the slow eigenvector is the constant vector**, and the
  spectral projector is the **degree-weighted mean-centering**
  `P u = u - (<u,1>_D / vol) 1`, with the `D`-norm.
* Conjugating by `D^{1/2}` sends `M` to `Q` (plain-symmetric) and `1` to
  `v = D^{1/2}1`, with `Q v = alpha v` (the task's check). Then
  `||P u||_{2,x} = ||P_h uh||_{D,hat}` — **the two descriptions are the same
  statement.** The plain Euclidean projector orthogonal to `v` *is* correct in
  x-coordinates; the `D`-weighted one is correct in hat coordinates. Mixing them
  is what fails (§4).

Eigenvalues: with `mu_k` the normalized-Laplacian (`L_sym`) eigenvalues,

```
lam_k(M) = alpha + (1-alpha) mu_k / 2 ,      mu_1 = 0 -> lam_1 = alpha.
```

## 2. The weighted-variance identity and the proof

Let `v > 0`, `pi_i := v_i^2 / ||v||^2`, and `w := u / v` coordinatewise.

> **ID1 (variance identity).**
> ```
> ||P u||_2^2 = ||v||^2 * Var_pi(w) = (||v||^2 / 2) * sum_{i,j} pi_i pi_j (w_i - w_j)^2 .
> ```
> *Proof.* `||Pu||^2 = ||u||^2 - (v'u)^2/||v||^2 = sum_i v_i^2 w_i^2 -
> (sum_i v_i^2 w_i)^2/||v||^2 = ||v||^2 [ E_pi w^2 - (E_pi w)^2 ]`. The pair form
> is the standard variance identity. ∎

For `v = D^{1/2}1` this reads: **`pi` is the random-walk stationary distribution
`d_i/vol`, `w` is the hat vector, and `||P u||^2 = vol * Var_pi(xh)`.**

> **Lemma L-E\* (Perron truncation, PROVED).** For any `v > 0`, any
> `phi: R -> R` that is 1-Lipschitz, and `Phi_v(u)_i := v_i phi(u_i/v_i)`,
> ```
> ||P Phi_v(u)||_2 <= ||P u||_2 .
> ```
> In particular `min(u, Delta v)_i = v_i min(w_i, Delta) = Phi_v(u)_i` with
> `phi = min(., Delta)`, giving the named inequality.
> *Proof.* By ID1 both sides are `||v||^2/2 * sum_{i,j} pi_i pi_j (.)^2` of the
> pairwise differences of `w` resp. `phi(w)`, and `|phi(w_i)-phi(w_j)| <=
> |w_i-w_j|` termwise. ∎

**No degree-ratio constant is needed.** The `K_n` argument (`P_h` = plain
mean-centering, `|P_h u|^2 = (1/2n) sum_{ij}(u_i-u_j)^2`) is exactly the
`pi = uniform` special case; on `K_n`, `d_i` is constant so `pi` *is* uniform.

> **ID2 (Q-form identity — the stronger version).** With `Q = alpha I +
> ((1-alpha)/2) L_sym` and `E` the edge set,
> ```
> ||P u||_Q^2 = <u,Qu> - alpha (v'u)^2/||v||^2
>             = alpha * vol * Var_pi(w)  +  ((1-alpha)/2) * sum_{(i,j) in E} (w_i - w_j)^2 .
> ```
> The second term is the **Dirichlet form in the `w` coordinates**. Both terms
> are sums of squared differences of `w`, so **both contract** under any
> coordinatewise 1-Lipschitz `phi` applied to `w`:
> ```
> ||P Phi_v(u)||_Q <= ||P u||_Q .                              (PROVED)
> ```
> Verified to `3.7e-15` relative on 60 graphs x 4 alphas x 400 vectors, and
> exactly on 5040 rational instances.

This is the form the project actually needs: `EQ_t = <e_t, Qt e_t>` in hat
coordinates *is* `<e,Qe>` in x-coordinates, so the defect chain C7/C8 lives in
`||.||_Q`, and it is now closed by the same one-line argument.

## 3. Measured — the violation hunt (0 violations)

| variant | samples | violations | worst ratio `||P z||/||P u||` |
|---|---|---|---|
| **V1 named** (`P = I-vv'/|v|^2`, Euclid, cap `Delta*v`) | 1,515,000 | **0** | 1.000000 |
| **V4 Q-weighted norm** (4 values of `alpha`) | 2,727,000 | **0** | 1.000000 |
| **V6 general 1-Lipschitz `phi` in `w`** | 606,000 | **0** | 1.000000 |
| **V7 plain Euclid in hat, correct projector** | 909,000 | 0 | 0.99999982 (Measured only, unproved) |
| V2 **misaligned cap** `Delta*1` (x-coords) | 606,000 | 595 | **7.463** (`P3`) |
| V3 **plain projector** `I-11'/n`, correct cap | 606,000 | 616 | **5.379** (`P3`) |
| V5 **D-weighted-in-x norm**, correct P and cap | 909,000 | 627 | **1.316** (`S30`) |

Empirical minimum of `||Pu|| - ||P min(u,Delta v)||` for V1: `-4.4e-16`, i.e.
float round-off at instances where **both sides are 0** (`u` proportional to `v`,
or truncation inactive); no true negative. Adversarial local search
(log-normal multiplicative moves, 7 graphs incl. stars/brooms/double-stars,
shrinking step) drove the ratio to `1.000000000000` and never past it.
101-graph zoo: `K_n`, paths, cycles, stars, barbells, brooms, caterpillars,
double stars, circulant regulars, 30 random trees, 30 ER, plus `P24`, `S30`.
`u` drawn from 6 families incl. lognormal(0,3) (extreme ratios), sparse, and
integer ties. Exact-rational replication: **2520/2520 for ID1 and V1,
5040/5040 for V4.**

**Necessity of the pairing.** V2/V3/V5 show all three ingredients are load
bearing: the cap must be a multiple of `v`, the projector must be the
`v`-orthogonal one, and the norm must be the one in which that projector is
orthogonal. V5 is the only "wrong" variant that survives with a **constant**:
since `sqrt(d_min)||.||_2 <= ||.||_D <= sqrt(d_max)||.||_2`, V1 gives
`||P z||_D <= sqrt(d_max/d_min) ||P u||_D` — measured worst 1.316 against a
bound of 5.39 on `S30`.

## 4. Transfer of C1–C17 to general graphs

Exact-Fraction battery, 20 general-graph instances (paths, stars centre/leaf
seeded, caterpillars, double stars, barbell, 4 random trees, 3 ER, broom, K6,
P24 tuned), `T = 22`, all checks in hat coordinates with the `D`-weighted
projector.

| tag | status on general graphs | evidence |
|---|---|---|
| C1 master | transfers **on the interior/support face**; global form void when `|S*|<n` | 383/383 exact |
| C2 F-collapse | transfers verbatim | 5/5 exact |
| C3 N-linear | transfers per mode (`m` modes, not 2) | structural |
| C4 V-decay | transfers **per mode** exactly; aggregate `V_{t+1} <= s_2 V_t` | structural |
| **C5 L-E** | **PROVED in general** (§2), in `D`- and `Q`-norms | 420/420 exact + 1.5M samples |
| C6 trigger | transfers verbatim | 420/420 exact |
| C7,C8 | project ms-15, graph-independent | inherited |
| C9 closing | N and CC cases transfer (`s_k <= (1-q)^2` for all `k`); F case = C16; **P case Open** | see below |
| **C10 low floor** | transfers **only on the interior face**; **fails on proper faces** | 395/400; fails on P24 |
| C11 monotone | transfers verbatim | 420/420 exact |
| **C12 structural** | **transfers and sharpens** (see below) | 20/20 + 300/300 exact |
| C13 absorption | **does NOT transfer** — depends on C10 | P24: 16 corrections to `t=393` |
| C14 | transfers on N stages with `s_2/(1-q)^2` | structural |
| C15 census | **inverts**: P stages become the common case | P24: 10 P vs 6 F |
| **C16 F-contraction** | **exact general threshold: `mu_k >= 2q`** | 300/300 exact, 20/20 agreement |
| C17 | still **Open**, and now dominant | — |

### C12, sharpened and proved for all graphs

With `m_k = kappa/(kappa+lam_k)`, `p_k = m_k(1+beta)`, `s_k = m_k beta`:

```
m_0 = kappa/(kappa+alpha) = 1 - q^2                       (graph-independent)
s_k <= (1-q)^2   <=>   lam_k >= alpha   <=>   mu_k >= 0   (always, equality iff mu_k = 0)
p_k^2 < 4 s_k    <=>   lam_k >  alpha   <=>   mu_k >  0   (strict iff G connected)
```

*Proof.* `4 beta/(1+beta)^2 = 1-q^2 = m_0`, so `p^2 < 4s <=> m < m_0 <=> lam >
alpha`; and `s = m beta` is decreasing in `lam` with `s = m_0 beta = (1-q)^2` at
`lam = alpha`. ∎ So **every high mode of every connected graph is underdamped and
contracts at least as fast as the critical `(1-q)^2`** — C12 is free in general.

### C16, and why P24 is the sharpest stress case

```
s_k (2 - m_k) <= (1-q)^2
   <=>  m_k(2-m_k) <= 1-q^2  <=>  (1-m_k)^2 >= q^2  <=>  m_k <= 1-q
   <=>  lam_k >= kappa q/(1-q) = q(1+q)/(1+q^2)
   <=>  **mu_k >= 2q** .
```

Exactly verified on **300/300** rational `(q, mu)` pairs, with equality on both
sides at `mu = 2q` (there `m_k = 1-q` and `s(2-m)-(1-q)^2 = 0` exactly), and
20/20 agreement with the direct test on the graph battery.

*Consistency with i2c.* On `K_n`, `mu_2 = n/(n-1)`, so C16 `<=> q <= n/(2(n-1))`,
whose infimum over `n` is **`q <= 1/2`** — reproducing the i2c statement
including its numbers (`q=1/10`: `0.723477` vs `0.810000`; `q=0.51`, large `n`:
`0.241124 > 0.240100`; equality exactly at `q=1/2`).

*On P24 tuned* (`q=1/32`, so `2q = 0.0625`): `mu_2 = 0.009262`, **3 of 24 modes
sit below `2q`**, and `s_2(2-m_2)/(1-q)^2 = 1.000946 > 1`. **C16 fails.** This
is a quantitative explanation of why the tuned-rho path family is the project's
sharpest stress case: it is a graph whose spectral gap is an order of magnitude
below the `2q` threshold.

## 5. Measured — genuinely partial stages on non-regular graphs

2160 exact instances scanned (paths, stars, caterpillars, double stars,
barbells, random trees, ER; 8 seeds x 6 rho x 2 q): **57 correcting stages with
`Delta < beta max d`, of which 47 genuinely partial**. At every one of them all
three L-E forms hold:

```
worst ratio  D-weighted  0.998808     Q-weighted 0.998123     plain (K_n form) 0.998479
plain-form violations in the recurrence: 0 ;  D-form: 0
```

Note the plain (`K_n`) form is *violable in general* (§3, V3, ratio 5.38) yet is
never violated by the recurrence's own `(d_t, Delta_t)` — the recurrence's `d_t`
is a nonneg. momentum vector and `Delta_t` is set by the modal trigger, so the
adversarial configurations are not reachable. That is Measured, not proved; only
the `D`/`Q`-weighted forms have a proof.

## 6. Refuted-draft — where L-E genuinely breaks: the support face

On a **proper** support face `S* ⊊ V` the master identity is
`(Qt_S + kappa D_S) e_{t+1} = kappa D_S (x^* - ell)_S`, so the governing
operator is `M_S = D_S^{-1} Qt_S`, **not** `M`. Its bottom eigenpair is
`(alpha_S, v_S)` with `alpha_S > alpha` strictly and `v_S` **not** proportional
to `D_S^{1/2}1`. The engine still caps at `Delta * D^{1/2}1` — misaligned.

| case | `|S*|` | `alpha_S/alpha` | `cos(v_S, D_S^{1/2}1)` | spread of `v_S` | face slow rate | `1-q` |
|---|---|---|---|---|---|---|
| P24 small rho | 24 | 1.000 | **1.000000** | 1.414 | 0.968750 | 0.968750 |
| P12, P16, S12-leaf, cat6_2 | full | 1.000 | **1.000000** | — | `= 1-q` | `1-q` |
| **P24 tuned** | **23** | **2.194** | **0.909911** | **14.62** | **0.968186** | 0.968750 |

**On every full-support instance `v_S = D^{1/2}1` exactly** (`cos = 1.000000`,
`alpha_S = alpha`, face rate `= 1-q` to all digits) — so the lemma applies
verbatim and the whole chain is on the interior face. On P24 tuned it does not,
and:

> **Counterexample (Refuted-draft).** P24, `q = 1/32`, `rho = 65/4096`
> (the i2c audit cell), `T = 400`. Of the 16 correcting stages, the
> **face-aligned** L-E `||P_{v_S} r_t|| <= beta ||P_{v_S} d_t||` holds at only
> **12/16**, worst ratio **238.4586**. The correction pumps the face-slow mode
> into the face-fast modes by a factor 238 in energy.

This also explains the C10 failure directly: the face's slow-mode contraction is
`0.968186 < 1-q = 0.968750`, so `L_t >= (1-q) L_{t-1}` is *false by design* —
the reservoir that keeps `alpha ta_L` positive drains faster than the certificate
assumes, the trigger re-arms forever, and absorption never fires (P24: 16
corrections, last at `t = 393`; word `N=384, F=6, P=10`). Face lock happens at
`t_F = 75`; the first post-lock C10 failure is at `t = 86`, so **this is a face
*geometry* effect, not a startup effect**.

**Algorithmic consequence (concrete and testable):** replace the retraction cap
`Delta * D^{1/2}1` by `Delta * v_{S_t}` — the Perron vector of the current
active face — and L-E transfers verbatim to proper faces by §2 (which holds for
*any* `v > 0`). That is a one-line change to `engine.py:156` and is the single
most promising next experiment.

## 7. The general-graph statement now in reach

> **Theorem (general graph, interior-face regime; draft).** Let `G` be connected,
> and assume (H0) `s_i > rho d_i` for all `i`, so `x^*` is interior and the face
> locks at a finite `t_F`. Let `mu_2 = mu_2(L_sym(G))`, `q = sqrt(alpha/(1-alpha))`.
> Then, with `P` the `D`-orthogonal projector onto `1^perp` in hat coordinates:
>
> 1. **(L-E, PROVED)** `||P r_t||_D <= beta ||P d_t||_D` and
>    `||P r_t||_Q <= beta ||P d_t||_Q` at every stage — corrections never pump
>    the slow mode into the fast modes, on **any** graph.
> 2. **(L-H, PROVED)** `L_t >= (1-q) L_{t-1} > 0` at every stage, because
>    `m_0 = kappa/(kappa+alpha) = 1-q^2` and `m_0[(1+beta) - beta/(1-q)] = 1-q`
>    are **graph-independent identities**.
> 3. **(L-S, PROVED)** every mode `k >= 2` is underdamped with
>    `s_k <= (1-q)^2`, strictly iff `G` is connected.
> 4. **(F-contraction)** the F case of C9 holds **iff `mu_2 >= 2q`**.
> 5. Consequently, if `mu_2 >= 2q`, the absorption certificate of i2c runs
>    verbatim with `lam_h -> lam_2` and one extra loss `|ta_h|_inf <=
>    ||ta_h||_D / sqrt(d_min)` in the trigger step — modulo the **same single
>    Open link** as `K_n` (genuinely partial stages, C9/C17).
>
> **The `K_n` absorption theorem therefore extends to every connected graph with
> `mu_2 >= 2q` under (H0)**, at the cost of a `1/sqrt(d_min)` factor in the
> absorption radius. Non-regularity costs nothing; only the spectral gap and the
> support face do.

**And the sharp negative:** outside (H0) — i.e. exactly the `l1`-regularized
regime where `rho` is large enough to sparsify the optimum — the slow direction
changes with the active face, the algorithm's cap stops being aligned with it,
and L-E is false in the recurrence (238x). That, not non-regularity, is the
general-graph crux now.

## 8. Next targets, ranked

1. **Face-aligned retraction.** Change the cap to `Delta * v_{S_t}` and re-run
   the P24 tuned cell: does L-E hold at all 16 corrections, does C10 return, and
   do the corrections stop? (One-line change; the lemma of §2 covers it for any
   `v>0`.) If yes, the whole i2c chain transfers to proper faces and the
   general-graph absorption theorem closes.
2. **Close C9/C17 at P stages.** On general graphs P stages are the *majority*
   of corrections (10 of 16 on P24) rather than a 1-in-54 curiosity, so the one
   Open link of the `K_n` proof becomes the load-bearing one. The certified
   bound wastes 55% of the true margin (i2c §4).
3. **Below the `mu_2 >= 2q` threshold** (paths, long trees, any graph with gap
   `<< q`) the F-contraction is false by an exact margin. Replace it by a
   two-stage or windowed F-bound that charges the `(1+q^2)` overshoot at
   `mu -> 0` against the `s_k/(1-q)^2 < 1` slack of neighbouring N stages.
4. Add the V2/V3/V5 counterexample cells (`P3` with the lognormal `u`, `S30`) to
   the exact-checker battery as *negative* controls: any future lemma that
   claims a projector/norm pairing must fail them.
