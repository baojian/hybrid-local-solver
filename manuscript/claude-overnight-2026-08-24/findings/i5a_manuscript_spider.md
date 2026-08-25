# I5-A — Verification: does the manuscript's long spider trivialize the semantic problem?

**Target claim** (I4-C §6.1): *"The manuscript's long spider has `S_eps = EMPTY` for
`alpha <= 2^-8` — `z = 0` is a valid semantic output at `W = 0`.
`thm:cf-spider-lower` is about the certificate, not the problem."*

**Manuscript object**: `sections/cf_push_two_stage_analysis.tex`,
`subsec:cf-spider-lower` (`lem:cf-spider-wave`, `thm:cf-spider-lower`), instance:
fixed `theta in (0,1/4)`, `k = theta/eps` arms, `L >= M+1`,
`M = floor(L_sp/2)`, `L_sp = log(1/theta)/(-log lambda)`, seed at the center,
`tau = eps/sqrt(a)`, FIFO `omega_star` Phase II.

**Verdict in one line.** The emptiness claim is **TRUE in the theorem's own
asymptotic regime** (exact threshold below; the theorem's dyadic parameter range is
entirely inside it), the theorem itself **remains literally true** as stated, and
one part of I4-C's interpretation must be **corrected**: the `Omega(1/(alpha*eps))`
is not even "about the certificate" — the certificate is reachable on this instance
at `Theta(1/eps)`-scale work; the cost is attributable specifically to the
**fixed-`omega_star` FIFO dynamics**. A pendant-seed variant restores
`S_eps != EMPTY` while preserving the wave and the `Omega(1/(alpha*eps))`
(measured), so a minimal-edit repair exists; no center-seeded calibration can do
the same.

Code: `/home/claude/work/overnight/i5a/{common.py, part1_threshold.py,
part2_sim.py, part3_repairs.py, part4_certfloor.py}`, logs in `i5a/out/`.
Total rerun < 2 min.

---

## 1. Exact emptiness threshold (Proved-draft + exact-arithmetic verification)

For the center-seeded equal-arm spider (`k` arms, length `L`), the
degree-normalized solution `u_i = pi_i/d_i` attains its maximum at the center, and

> **`u_max = u_0 = (sqrt(a)/k) * (1 + lam^{2L})/(1 - lam^{2L})
>        = (sqrt(a)/k) * coth(2L * artanh(sqrt(a)))`.**

Derivation: substitute `psi(L-1) = lam(1+lam^{2L-2})/(1+lam^{2L})` into
`u_0 = gamma/(k(1 - c*psi(L-1)))` and simplify with `c = 2lam/(1+lam^2)`,
`gamma = (1-lam)^2/(1+lam^2)`, `sqrt(a) = (1-lam)/(1+lam)`. Verified **in exact
rational arithmetic** against the W2 closed forms and against an independent
`Fraction` Gaussian elimination (`part1_threshold.py` A); the arm profile is
strictly decreasing from the center, so `u_max = u_0`.

Hence, with `eps = theta/k` (the ratio `u_0/eps` is `k`-free):

> **`S_eps = {i : u_i >= eps} = EMPTY  <=>  sqrt(a)*(1+zeta)/(1-zeta) < theta`,
> `zeta := lam^{2L}`.**

For the manuscript's minimal `L = M+1`: `2M <= L_sp < 2M+2` gives
`zeta in [theta*lam^2, theta)`, so the threshold converges to

> **`sqrt(a) < theta*(1-theta)/(1+theta)`**, i.e.
> `alpha < alpha*(theta) ~ theta^2 ((1-theta)/(1+theta))^2`
> (`= 49/5184 ~ 0.00945` for `theta = 1/8`; `~ 0.00304` for `theta = 1/16`).

Numbers (`part1_threshold.py` B–D, `u_0/eps` exact to closed form; float table,
exact-Fraction spot checks):

| theta | alpha | bypass `tau*k>1` | `u_0/eps` | `S_eps` |
|---|---|---|---|---|
| 1/8 | 2^-6 | **no** (`tau*k=1`) | 1.176 | nonempty |
| 1/8 | 2^-7 | yes | **0.899** | **EMPTY** |
| 1/8 | 2^-8 | yes | 0.617 | EMPTY |
| 1/8 | 2^-10 | yes | 0.318 | EMPTY |
| 1/8 | 2^-12 | yes | 0.159 | EMPTY |
| 1/16 | 2^-8 | **no** (`tau*k=1`) | 1.104 | nonempty |
| 1/16 | 2^-9 | yes | **0.796** | **EMPTY** |
| 1/16 | 2^-12 | yes | 0.282 | EMPTY |

A fine scan over all `alpha` (300k log-grid points) shows the **only** parameters
satisfying both the theorem's bypass hypothesis `sqrt(a) < theta` and
`S_eps != EMPTY` form a fixed window just below `theta^2`:

- `theta = 1/8`: `alpha in [0.01073, 0.01563)` — width factor 1.46, **no dyadic
  alpha inside**;
- `theta = 1/16`: `alpha in [0.00315, 0.00391)` — width factor 1.24, no dyadic
  alpha inside.

**Answer to Part 1.** The claim is regime-dependent with the exact threshold
above; the manuscript's asymptotic regime (fixed `theta`, `alpha -> 0`) is
entirely inside the empty region, and so is **every dyadic `alpha` admitted by
the theorem's hypotheses** (`alpha <= 2^-7` for `theta = 1/8`; `alpha <= 2^-9`
for `theta = 1/16`). I4-C's "`alpha <= 2^-8`" was computed for its own `L ~
1/sqrt(a)`; with the manuscript's exact `L = M+1` the emptiness starts one octave
earlier (`2^-7` at `theta = 1/8`). Longer arms (`L > M+1`, which the theorem
permits) only decrease `u_0`, so emptiness is monotone in `L`.

## 2. Certificate vs. semantics vs. dynamics on this instance

All measured on the literal `alg:cf-push` FIFO implementation
(`part2_sim.py`; push rule eq. cf-push-z/r, manuscript queue convention).
`lem:cf-spider-wave` itself was verified **push-by-push**: for all macro-cycles
`m <= M` every arm executes depths `m, m-1, ..., 1` with residuals
`C*lam^{2m-l}` to max relative deviation `2.8e-15`, and the center residuals are
exactly `gamma*lam^{2j}` for `j <= M` (deviations appear only after the front
reaches the leaf, outside the lemma's stated range). The lemma and theorem are
mechanically sound.

- **(a) Semantic output at zero work.** For `theta = 1/8`, `k = 64`,
  `alpha in {2^-7..2^-12}`: `err(z=0)/eps = u_0/eps = 0.899, 0.617, 0.450,
  0.318, 0.225, 0.159`. So `z = 0` satisfies
  `||D^{-1}(pi - z)||_inf <= eps` at `W = 0`. Confirmed.
- **(b) Certificate at `z = 0`.** `r = gamma*e_v` gives
  `max_u |r_u|/(gamma*eps*d_u) = 1/(eps*k) = 1/theta = 8.00` (measured
  exactly). The stopping rule is violated at `z = 0` by the factor `1/theta`:
  the algorithm cannot stop there. This is the certificate-vs-semantic gap in
  its purest form.
- **(c) But the certificate itself is CHEAP here.** Two independent
  measurements (`part4_certfloor.py`):
  - LP over arm-symmetric outputs supported in radius `R`: the certificate
    `|gamma*e_v - Hz| <= 0.999*gamma*eps*d` is feasible at **`R_min = 3`,
    constant across `alpha = 2^-6..2^-12`** (infeasible at `R = 2`; the
    reconstructed full `z` verifies the true certificate at margin 0.999).
    Support volume `7k = 448 = Theta(theta/eps)` — no `alpha` dependence at
    all. (Mechanism: all interior values the certificate needs are
    `O(gamma/k) = O(gamma*eps/theta)`, i.e. within a constant factor of the
    per-row slack `2*gamma*eps`, so a constant number of slack rows absorbs
    the decay; only `z_0 ~ gamma` is large, and the center row's `gamma*theta`
    slack handles it.)
  - The manuscript's own monotone primitive run at the final tolerance
    (`omega = 1`, threshold `gamma*eps*d`, i.e. Phase I at `tau = eps`)
    **meets the certificate** with `W = 1344–2688 ~ (21–42)*k` over
    `alpha = 2^-6..2^-12` — `W*sqrt(a)*eps -> 0`, `W*alpha*eps -> 0`.
  Meanwhile the fixed-`omega_star` FIFO run measures `W*alpha*eps ~
  0.082–0.091` flat over `2^-7..2^-12` (`W ~ 2.4–3.0 x` the `k*M(M+1)` floor),
  i.e. `Theta(1/(alpha*eps))` exactly as the theorem states.

**Conclusion (correcting I4-C §6.1's attribution).** On this instance the
three levels separate cleanly, all measured:

| level | work on this instance |
|---|---|
| semantic problem (`||D^{-1}(pi - z)||_inf <= eps`) | `0` (take `z = 0`) |
| certificate `|r| < gamma*eps*d` (any output / monotone push) | `Theta(theta/eps)` support; `W ~ (2–6) x` that via `omega=1` push |
| fixed-`omega_star` FIFO to the same certificate | `Theta(1/(alpha*eps))` |

The `Omega(1/(alpha*eps))` is a property of the **relaxation dynamics** (the
signed triangular wave), not of the certificate and not of the problem. I4-C's
sentence "a sharp statement about the `gamma*eps*d`-activation certificate"
is right only in the narrow sense that the stopping rule forbids stopping at
`z = 0`; the *cost of reaching* that stopping rule is `Theta(1/eps)`-scale, so
the certificate cannot carry the `1/(alpha*eps)` either. Incidentally this
also shows the two-stage design is what arms the instance: Phase I at
`tau = eps` (plain APPR) would finish cheaply, but the theory-selected switch
`tau = eps/sqrt(a)` silences it (`tau*k = theta/sqrt(a) > 1`) and hands the
whole instance to the SOR stage.

## 3. Repairs: can the instance be made semantically nontrivial?

**(i) Center-seeded calibrations cannot keep `Omega(1/(alpha*eps))`.**
Nonemptiness for a center seed forces `eps*k <= sqrt(a)*coth(2L*artanh
sqrt(a))`, which caps the wave's threshold budget. Fixed-ratio family
(`theta_run = 2*sqrt(a)`, `L = ceil(0.2/sqrt(a))`, `k = 64`; bypass holds,
`tau*k = 2`; `S_eps` genuinely rich — up to 833 vertices including arm
prefixes of depth `Theta(1/sqrt(a))`): measured `W*alpha*eps` **decays**
`0.156 -> 0.019` over `alpha = 2^-4..2^-12` while `W*sqrt(a)*eps ~ 0.62–1.22`
(mild log growth). The wave still executes, but with `k = Theta(sqrt(a)/eps)`
arms the total is `Theta~(1/(sqrt(a)*eps))` — consistent with the section's own
upper-bound target, hence **no obstruction survives** in any center-seeded
regime where the semantic task is nontrivial. (The original construction is
nonempty only in the fixed window `alpha in [0.0107, 0.0156)` for `theta=1/8`,
where measured `W*alpha*eps ~ 0.093–0.099` — real but not an `alpha -> 0`
family.)

**(ii) A pendant seed restores nontriviality and keeps the bound (Measured).**
Attach one degree-1 pendant `p` to the center; seed `s = e_p`; take
`eps = gamma_alpha`, `k = round(theta/eps) = Theta(theta/alpha)`, `L = M+1` as
before. Then, measured over `alpha = 2^-6..2^-12`
(`part3_repairs.py`):

- `u_p/eps = 1 + c_a*u_v/gamma_a = 2.05 -> 1.16 > 1`: **`S_eps = {p}`,
  `z = 0` is semantically INVALID** (and the certificate gap at `z=0` is
  `~1/eps`);
- the single-write output `z = pi_p e_p` is semantically valid for
  `alpha <= 2^-7` (`err/eps = 0.87 -> 0.16`): the semantic optimum is `O(1)`;
- Phase I does exactly one unit of work (the pendant push), then the bypass
  `tau*k > 1` silences it at the center;
- the triangular wave survives **structurally intact**: every arm executes the
  exact depth pattern `m, m-1, ..., 1` for all cycles `m <= M` (packet
  constants perturbed by `O(1/k)`, <= 12%; center decay `lam^2` in geometric
  mean); interior-push count `>= 1.97–2.87 x` the lemma floor `k*M(M+1)/2`;
- `W*alpha*eps = 0.070, 0.086, 0.084, 0.082, 0.082` over `2^-8..2^-12` —
  **flat**, matching the original instance's constant.

So the pendant variant witnesses `Omega(1/(alpha*eps))` for the FIFO
fixed-`omega_star` method on an instance where the zero vector is *not* a
valid answer. It does not (and cannot) make the *problem* hard: the semantic
optimum remains `O(1)`, and by (i) no spider calibration pushes semantic
hardness past `Theta~(1/(sqrt(a)*eps))`.

## 4. What the theorem does and does not establish

- **True as stated, mechanically verified.** `thm:cf-spider-lower` is an
  algorithm-specific lower bound; the manuscript's status table already scopes
  it ("for the FIFO fixed-`omega_star` implementation"), and
  `lem:cf-spider-wave` is exact in its stated range.
- **The instance does not witness problem-level hardness.** In the theorem's
  regime the semantic optimum on the instance is `W = 0`, and the certificate
  optimum is `Theta(1/eps)`-scale. A reader who takes the spider as evidence
  that *the problem* resists `O~(1/(sqrt(a)*eps))` would be misled; the
  section's later sentence "It does not by itself prove a corresponding lower
  bound for an arbitrary algorithm" is correct and, per this analysis, can be
  sharpened: it does not even prove one for *this* algorithm under a semantic
  (oracle) stopping rule.
- **The star results are unaffected.** On `prop:cf-phase-one-star`'s star,
  `u_center/tau = 1/((1+c)*theta) > 1` and every leaf is also above threshold:
  the star instances are semantically nontrivial as used. Only the long spider
  has the dilution issue (its `Theta(1/sqrt(a))`-deep arms absorb
  `1 - Theta(sqrt(a))` of the seed mass — the same mechanism that creates the
  wave work destroys the semantic content).

## 5. Recommended minimal edit

The smallest change that removes the interpretive exposure, in order of
priority:

1. **Add a remark after `thm:cf-spider-lower`** (or fold into
   `subsec:cf-two-stage-scope`), e.g.:

   > *Remark (scope of the obstruction).* On this family the semantic target is
   > itself degenerate for small `alpha`: the maximal degree-normalized value is
   > `||D^{-1}pi||_inf = (sqrt{alpha}/k)\,\coth(2L\,\mathrm{artanh}\sqrt{alpha})`,
   > so once `sqrt{alpha} < theta_sp (1-lambda^{2L})/(1+lambda^{2L})`
   > (asymptotically `sqrt{alpha} < theta_sp(1-theta_sp)/(1+theta_sp)`), the
   > zero vector already satisfies `||D^{-1}(pi - z)||_inf <= eps_ppr` at zero
   > work, while the stopping test `|r| < gamma_alpha eps_ppr d` is violated at
   > `z=0` by the factor `1/theta_sp`. Theorem `thm:cf-spider-lower` is
   > therefore a lower bound on the work the implemented method performs before
   > its residual test is met — an obstruction to the algorithm and its
   > stopping rule, not a hardness statement about the `eps_ppr`-approximation
   > problem on this family.

2. **If a semantically nondegenerate witness is wanted**, state the pendant
   variant in that remark (one sentence): seed at a degree-1 pendant `p` on the
   center, `eps_ppr = gamma_alpha`, `k = Theta(theta_sp/alpha)`; then
   `pi_p/d_p > eps_ppr` (so `z=0` is invalid) and the same FIFO wave yields
   `W = Omega(1/(alpha\,eps_ppr))` — noting the wave constants change by
   `O(1/k)` and that a full re-proof of `lem:cf-spider-wave` for the perturbed
   constants is then needed (the measured depth pattern is unchanged; the exact
   cancellation identity is not, so the lemma would need an inequality form).
   Alternatively keep the original instance and simply do not claim semantic
   hardness.
3. **Optionally strengthen `subsec:cf-design-consequences`** with the measured
   fact that the certificate is not the bottleneck either: on the same spider,
   `omega = 1` push at `tau = eps_ppr` meets the final residual test in
   `Theta(theta_sp/eps_ppr)`-scale work (measured `(2\text{–}6)\times` the
   minimal certificate support `~ 7k`), so the `1/(alpha eps)` is specifically
   the fixed-`omega_star` signed dynamics — which is precisely the section's
   motivation for Chebyshev/variable-relaxation or wave-abandoning triggers.
4. **No change to the theorem statement, the wave lemma, the star
   propositions, or the status table is required.** If desired, the status-table
   row could read "False for the FIFO fixed-`omega_star` implementation (on an
   instance whose semantic optimum is `O(1)`; see Remark)".

## 6. Evidence classification

| claim | class |
|---|---|
| `u_max = (sqrt(a)/k)(1+lam^{2L})/(1-lam^{2L})`; profile decreasing | Proved-draft (algebra + exact Fractions) |
| emptiness iff `sqrt(a)(1+zeta)/(1-zeta) < theta`; band `[0.0107, 0.0156)` for `theta=1/8`, no dyadic alpha; theorem's dyadic range all EMPTY | Proved-draft threshold; Measured band edges (300k-point scan) |
| `z=0` valid at `W=0` in theorem regime; certificate violated at `z=0` by `1/theta` | Proved-draft (one-line) + Measured |
| wave lemma exact for `m <= M` (2.8e-15); FIFO `W*alpha*eps ~ 0.082–0.091` flat | Measured (literal simulator) |
| certificate reachable with support radius 3 (const), vol `7k`; `omega=1` meets it in `(21–42)k` | Measured (LP + simulation) |
| center-seeded nontrivial calibrations give `W = Theta~(1/(sqrt(a)eps))`, not `1/(alpha eps)` | Measured + scaling argument |
| pendant repair: `S_eps={p}`, wave depth-pattern intact, `W*alpha*eps` flat `~0.082` | Measured |

Caveats: simulations are float64 (wave residuals cross-checked to 1e-15
against closed forms; emptiness ratios `u_0/eps` are `O(1)` quantities far from
cancellation, and were confirmed in exact rational arithmetic at
`alpha in {1/16, 1/64, 1/256}`). The LP floor is over arm-symmetric outputs;
by convexity + symmetry of the constraint set this bounds the maximal support
radius over arms, and the independent `omega=1` measurement corroborates the
`Theta(1/eps)` certificate scale. The pendant-variant wave lemma is verified
numerically, not re-proved; adopting it in the manuscript requires an
inequality-form re-proof of `lem:cf-spider-wave`.
