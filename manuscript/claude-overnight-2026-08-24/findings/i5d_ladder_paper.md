# I5-D — The three-class ladder on one instance: a manuscript-ready package

**What this is.** A self-contained candidate manuscript section unifying the
campaign's three class complexity results on a single instance (the
centre-seeded star): monotone-residual one-hop methods pay `Theta(1/(alpha eps))`,
signed-residual one-hop relaxation pays `Theta(1/(sqrt(alpha) eps))`, and
elimination pays `Theta(1/eps)`. Each rung drops exactly one axiom and buys
exactly one factor of `sqrt(alpha)`. Sources unified:
`findings/w1_monotone_lb.md` (iteration 1), `findings/i2d_separation_package.md`
(iteration 2, supersedes W1's Lemmas 3-5), `findings/i4c_signed_class_lb.md`
(iteration 4). Status labels are per statement: **Proved-draft** (complete
argument written here, unaudited), **Measured** (numerics only), **Open**.
Nothing here has passed the repository's promotion gate; see §9.

**Verification.** One script re-checks every numbered inequality below on the
full dyadic grid `alpha in {2^-4..2^-12} x eps in {2^-4..2^-8}`:
`/home/claude/work/overnight/i5d/verify_ladder.py` (reuses `w1_monotone_lb/`,
`w9_i2d/`-derived reductions, `i4c/`, `lib/zoo.py`; rerun ~2 min).
Result: **45 cells x 13 checks, 0 failures** (§8).

**Two consolidation gains over the sources** (both new to this note):
(i) restating the monotone potential in the push scale turns it into the
*relative error at the seed*, which removes the instance constant `Phi` from
every main statement (it survives only in one optional corollary — §7, Open 1);
(ii) a Cauchy-Schwarz on the energy gives a pathwise residual-mass cap
`||r||_1 <= 2 sqrt(alpha/(1+alpha))` for the whole signed class (Prop B.6),
which lets the signed lower bound tolerate one-hop output post-processing.

---

## 1. Setting, one scale, and the dictionary

Conventions of `tex/shared/source_aligned_problem.tex` and
`sections/appr_lower_bound.tex`. Graph `G` finite, simple, undirected,
unweighted, no isolated vertices; degrees `d_u`; `vol(S) = sum_{u in S} d_u`;
seed `s = e_v`; `alpha in (0,1)`. Write

```text
c_alpha = (1-alpha)/(1+alpha),      gamma_alpha = 2 alpha/(1+alpha),
H = I - c_alpha A D^{-1},           H pi = gamma_alpha e_v,
```

so `pi` is the shared lazy PPR vector `pi = D^{1/2} Q^{-1} b` of the
manuscript (`prop:appr-rppr-bridge` route: `M_op = ((1+alpha)/2) H` and
`pi = alpha M_op^{-1} e_v`). Note the two identities
`1 - c_alpha = gamma_alpha` and `1 + c_alpha = 2/(1+alpha)`.

**State and primitive.** An algorithm maintains `(z, r)` with `z^0 = 0`,
`r = gamma_alpha e_v - H z` (so `r^0 = gamma_alpha e_v`), and applies one-hop
operations

```text
push(u, delta):   z_u += delta;   r_u -= delta;   r_w += c_alpha delta / d_u  (w ~ u),
```

charged work `d_u` (one adjacency-list scan of `u`, the manuscript's unit).
The policy choosing `(u_t, delta_t)` is arbitrary: adaptive, randomized,
batched; all bounds below are pathwise, so randomized policies obey them with
probability 1. By W1 Lemma 1 (characterization; Proved-draft, transported),
`push(u, delta)` is the *only* one-hop update that preserves the invariant
`z + H^{-1} r = pi` exactly and changes `z` only at its base; the neighbour
split is forced, the scalar `delta` is the only freedom.

**Semantic guarantee.** The output `zhat` (finite support, unlisted
coordinates zero) must satisfy the manuscript's degree-normalized error

```text
err(zhat) := max_u |pi_u - zhat_u| / d_u <= eps,      eps := eps_ppr.
```

Throughout, `eps` means `eps_ppr` — never `eps_appr`; the bridge to the
manuscript's APPR theorem is stated explicitly in §7, and no namespace
equality is assumed.

**Dictionary to the mass scale** (the scale of `sections/appr_lower_bound.tex`
and of W1/I2-D, where the monotone results were first proved). With
`pr(h) = alpha M_op^{-1} h` and APPR state `(p, r_mass)`:

```text
z = p,        r = gamma_alpha * r_mass,        delta = alpha * eta,
pi - z = H^{-1} r = pr(r_mass),
```

and the W1 generalized push `gp(u, eta)` is `push(u, alpha eta)`. Class-M
feasibility `eta <= 2 r_mass_u/(1+alpha)` is exactly `delta <= r_u`. Lazy ACL
push (amount `xi = r_mass_u`) is `push(u, omega r_u)` with
`omega = (1+alpha)/2`; full non-lazy push is `omega = 1`; GS-SOR with
`omega > 1` overshoots `r_u` past zero. *(Dictionary verified per cell to
1e-11 on mirrored random signed sequences — check C13.)*

**Facts** (each one line, any graph): **F1** `H^T 1 = gamma_alpha 1`, so
`sum_u (H^{-1} r)_u = ||r||_1 / gamma_alpha` for `r >= 0` (mass conservation);
**F2** `H^{-1} >= 0` entrywise (Neumann series, `c_alpha < 1`);
**F3** `(H^{-1})_{vv} = pi_v / gamma_alpha` (the seed row of the defining
system); **F4** `max_u pr(h)_u/d_u <= max_u h_u/d_u` for `h >= 0`
(`pr(d) = d`); **F5** `|H^{-1} h| <= H^{-1} |h|` entrywise.

---

## 2. The three classes, and why the comparison is fair

**Definition 2.1 (classes).** All classes share the state, primitive, work
charge, instance, and guarantee of §1; they differ in one constraint each.

| class | constraint on `push(u, delta)` | contains |
|---|---|---|
| `M+` monotone push | `0 < delta <= r_u` (equivalently `r >= 0` stays, steps positive) | lazy/non-lazy APPR any ordering, damped `omega <= 1`, Jacobi, partial and below-threshold pushes |
| `M+-` signed step | `delta in R`, but `r >= 0` after every op | `M+` plus anti-pushes ("pumping") |
| `R+-` signed relaxation | `delta = omega r_u`, `omega in (0,2)`; `r` unrestricted | GS (`omega=1`), SOR/CF-Push phase II incl. `omega*`, Gauss-Southwell, adaptive/per-vertex/random `omega` |

Lattice: `M+ = M+- ∩ R+-` (a positive step keeping `r_u >= 0` is exactly
`omega in (0,1]`), and neither of `M+-`, `R+-` contains the other
(anti-pushes have `delta/r_u <= 0`; over-relaxation violates `r >= 0`).
The constraint `omega in (0,2)` is exactly *pathwise energy dissipation*
(Lemma B.1): `R+-` is the class of one-hop updates that never increase the
error energy. Dropping that too leaves the unrestricted one-hop writer, which
on the star can simply write the answer — that is rung 4 (§5).

**Definition 2.2 (one-hop output maps `O_B`).** `out = z + M r` with
`M >= 0`, `M_{uw} = 0` unless `w in N[u]`, and column mass
`sum_u M_{uw} <= B` for every `w`. `B = 0` is `out = z`.

**Fairness.** Both lower-bound theorems are stated primarily for `out = z` —
the same output map, on the same instance, under the same guarantee and work
charge; the *only* difference between the classes compared in §6 is the class
axiom. Output post-processing is then handled symmetrically as extensions:
Theorem A tolerates every `M in O_B` up to the sharp escape threshold
`B < (1 - eps vol)/gamma_alpha` (on the star), and Theorem B tolerates
`B <= (1/16) sqrt((1+alpha)/alpha)` (Prop B.6). The thresholds differ because
the classes do: I2-D Prop 1.3 shows `B >= (1 - eps vol)/gamma_alpha` escapes
at `W = 0` *for every class* (the seed's own residual column covers the whole
radius-1 instance), so no lower bound of any kind survives past it; below it,
what each class can hide in `r` differs, and §4 quantifies it for `R+-`.
In mass-scale terms `B_mass = gamma_alpha B` and the threshold is the
`B_mass = 1 - eps vol` of I2-D.

**The hard instance.** `K_{1,m}` with centre `c`, leaves `L`, seed `v = c`,

```text
m = floor(1/(8 eps)),   eps <= 1/16   =>   1/(16 eps) <= m <= 1/(8 eps),
vol = 2m,   eps vol <= 1/4,   eps m <= 1/8,
```

identical to `eq:hard-star-size` of the manuscript. Closed forms (eliminate
the leaves from `H pi = gamma_alpha e_c`; check C1):

```text
pi_c = gamma_alpha/(1 - c_alpha^2) = (1+alpha)/2,        pi_l = c_alpha pi_c / m = (1-alpha)/(2m).
```

For `alpha < 3/4`, `pi_u/d_u > eps` for every `u` (`pi_l = (1-alpha)/(2m)
>= 4(1-alpha) eps > eps`), so `S_eps = V`: every correct output must write
`m+1` nonzero coordinates, giving the universal floor `W >= m >= 1/(16 eps)`
for *any* algorithm (this is I4-D's `vol(S_eps)` floor; it also makes the
instance semantically nontrivial, unlike the long spider — §7).

---

## 3. Theorem A: the monotone classes pay `Theta(1/(alpha eps))`

The potential is the **relative unsettled value at the seed**:

```text
Psi := (pi_c - z_c)/pi_c = e_c/pi_c,        e := pi - z,        Psi(0) = 1.
```

In the mass scale `Psi = pr(r_mass)_c/pi_c = <phi, r_mass>` with
`phi_u = pr(e_u)_c/pi_c`, which is I2-D's potential; the z-scale form makes
its two properties trivial and graph-free.

**Lemma A.1 (locality; exact, sign-free).** Every `push(u, delta)` changes
`Psi` by `-delta/pi_c * [u = c]`. In particular `Psi` is invariant under every
operation not based at the seed, for either sign of `delta`.
*Proof.* `z_c` changes only at seed-based ops, by the definition of the
primitive. ∎ *(Check C2: the mass-scale form `Delta pr(r)_c = -alpha eta
[u=c]` verified to 1e-10 on random signed sequences, every cell.)*

**Lemma A.2 (kappa-step).** If `r >= 0` then `r_c <= (gamma_alpha/pi_c) e_c`.
Consequently every `M+-`-feasible op multiplies `Psi` by at least
`1 - kappa`, `kappa := gamma_alpha/pi_c`, and `Psi` decreases only at
seed-based ops with `delta > 0`.
*Proof.* `e = H^{-1} r`, so
`e_c = sum_u (H^{-1})_{cu} r_u >= (H^{-1})_{cc} r_c = (pi_c/gamma_alpha) r_c`,
using F2 (off-diagonal terms `>= 0`) and F3. A seed op has `delta <= r_c`
(feasibility `r_c >= 0` after), so
`-Delta Psi = delta/pi_c <= r_c/pi_c <= kappa Psi`; ops with `delta <= 0` or
`u != c` do not decrease `Psi` (Lemma A.1). Also `Psi >= 0` throughout
(F2). ∎ On the star

```text
kappa = kappa_+ := gamma_alpha/pi_c = 4 alpha/(1+alpha)^2 < 1.
```

*(Check C3: both the inequality `r_c pi_c <= pr(r)_c` and the multiplicative
step verified on random signed `r>=0` sequences, every cell.)*

**Lemma A.3 (terminal smallness of `Psi`).** Suppose the run stops with
output `out = z + M r`, `M in O_B`, and `err(out) <= eps`. Then, with `r >= 0`
at stopping:
(i) [graph-free] `||r||_1 (1/gamma_alpha - B) <= eps vol`, and
`Psi_T <= (eps d_c + B ||r||_1)/pi_c`;
(ii) [star] `Psi_T <= ||r||_1 / gamma_alpha <= eps vol/(1 - gamma_alpha B)`.
*Proof.* (i) Sum the guarantee `(pi - z - Mr)_u <= eps d_u` over `u`: by F1
`sum_u e_u = ||r||_1/gamma_alpha`, and `1^T M r <= B ||r||_1` by the column
bound; subtract. The coordinate `u = c` of the guarantee gives
`e_c <= eps d_c + (Mr)_c <= eps d_c + B ||r||_1` since every entry of row `c`
of `M` is at most its column mass `<= B`. (ii) On the star,
`phi_l = c_alpha < 1 = phi_c` (reversibility: `pr(e_l)_c = m pi_l =
(1-alpha)/2`, divide by `pi_c`), so
`Psi_T = <phi, r_mass> <= ||r_mass||_1 = ||r||_1/gamma_alpha`, and (i)'s first
display bounds `||r||_1`. ∎

**Theorem A.4 (class lower bound for `M+-`, hence `M+`; Proved-draft).**
Centre-seeded `K_{1,m}`, `m = floor(1/(8 eps))`, `eps <= 1/16`,
`alpha in (0,1)`. Every member of `M+-` (arbitrary adaptive / randomized /
batched policy, arbitrary stopping rule) whose output `z + Mr`, `M in O_B`
with `gamma_alpha B <= 1 - eps vol - tau` (any `tau > 0`), satisfies
`err <= eps` on this instance, performs

```text
N_c^+  >=  ln(1/Psi_T) / (-ln(1 - kappa_+))          seed ops with delta > 0,
W  >=  m N_c^+,
```

with `Psi_T` bounded by Lemma A.3(ii); for `out = z` (`B = 0`),
`Psi_T <= 2 eps m/(1+alpha) <= 1/4` and

```text
N_c^+ >= ln((1+alpha)/(2 eps m)) / (-ln(1 - kappa_+)),        W >= m N_c^+.
```

*Proof.* `Psi(0) = 1`; by Lemmas A.1-A.2, after any op sequence containing
`N_c^+` positive seed ops, `Psi >= (1-kappa_+)^{N_c^+}` (all other ops do not
decrease `Psi`; positive seed ops each retain a factor `>= 1-kappa_+`).
Combine with the terminal bound and take logs; each seed op is charged
`d_c = m`. For `B = 0`, Lemma A.3(i) at the single coordinate `c` gives
`Psi_T <= eps m/pi_c` directly. ∎

**Corollary A.5 (explicit constants; Proved-draft).** Using
`-ln(1-kappa) <= kappa/(1-kappa)` and `(1-kappa_+)(1+alpha)^2 = (1-alpha)^2`:

```text
B = 0:   W  >=  ln(4) (1-alpha)^2 / (64 alpha eps)          (all eps <= 1/16),
         W  >=  ln(4(1+alpha)) (1-alpha)^2 / (32 alpha eps)  (dyadic grid, eps m = 1/8).
```

Numerically `W * alpha * eps >= 0.0190` (general) and `>= 0.0397` (dyadic)
for `alpha <= 1/16`, approaching `ln(4)/64 = 0.0217` and `ln(4)/32 = 0.0433`
as `alpha -> 0`. This is 1.6-3.7x stronger than W1's `3/256`, and covers
signed steps, all output maps in the admissible `O_B` range, and every
stopping rule. *(Checks C4-C5: three member policies (APPR-FIFO, greedy
non-lazy, cheap-first) plus the anti-push pump adversary (`||r||_1` pumped to
4, sub-grid): `N_c^+ >= LB` and `W >= m*LB` on every run, every cell,
0 failures; measured member minimum `N_c^+/LB = 1.50-1.56` and
`W alpha eps >= 0.130` on this battery; I2-D's 14-policy zoo has the member
frontier at `N_c^+/LB = 1.015` and `W alpha eps = 0.0867`.)*

**Theorem A′ (general graphs; Proved-draft, no instance constant).** For any
connected `G`, seed `v`, output `z`: every `M+-` member with `err <= eps` has

```text
N_v^+ >= ln( pi_v/(eps d_v) ) / (-ln(1 - gamma_alpha/pi_v)),      W >= d_v N_v^+,
```

which is `Omega( (pi_v/alpha) * ln(pi_v/(eps d_v)) )` seed-op mass for small
`alpha`, and is informative exactly when `pi_v > eps d_v`, i.e. when the seed
itself is in `S_eps`. *Proof:* Lemmas A.1-A.3(i) used nothing about the star.
∎ The star is the extremal case: `d_v = m = Theta(1/eps)` and
`pi_v = Theta(1)`. (I2-D's Prop 2.6 needed the constant
`Phi = max_u d_u pi_u/(d_c pi_c)`; the present restatement eliminates it —
see §7, Open 1, for what remains of that question.)

**Why the axiom is exactly `r >= 0`, not the step sign.** Lemma A.2 is where
`r >= 0` enters, twice: it caps the feasible seed step (`delta <= r_c`), and
it converts `r_c` into `Psi` (`r_c <= kappa pi_c Psi`... i.e. the seed cannot
hold residual out of proportion to its own unsettled value). Anti-pushes only
raise `Psi` and must be repaid at the same multiplicative rate — the pump
adversary measures 3.7x *worse*, never better (I2-D §2; re-verified here).
Over-relaxation (`omega > 1`) breaks `delta <= r_c` precisely by letting
`r_c` go negative, and §4 shows that is worth exactly `sqrt(alpha)`.

---

## 4. Theorem B: signed one-hop relaxation pays `Theta(1/(sqrt(alpha) eps))`

Now drop `r >= 0` and restrict to relaxations `delta = omega r_u`,
`omega in (0,2)` (class `R+-`). The proof replaces the order argument
(`Psi >= 0` dies with `r >= 0`) by a quadratic energy argument.

**Lemma B.1 (energy identity; exact).** Let `Phi(e) := (1/2) e^T D^{-1} H e`
(`D^{-1}H` symmetric positive definite). A `push(u, delta)` changes it by

```text
Phi(e) - Phi(e^+) = (delta/d_u) (r_u - delta/2),
```

which for `delta = omega r_u` is `[omega(2-omega)/2] r_u^2/d_u >= 0`. Hence
`Phi` is non-increasing along every `R+-` path, and `omega in (0,2)` is
*exactly* the dissipativity condition. Initially
`Phi_0 = gamma_alpha pi_v/(2 d_v)`; on the star `Phi_0 = alpha/(2m)`.
*Proof.* `e^+ = e - delta ehat_u`, `(D^{-1}He)_u = r_u/d_u`,
`(D^{-1}H)_{uu} = 1/d_u`; expand the quadratic. `Phi_0` from `e^0 = pi`,
`H pi = gamma_alpha e_v`. ∎ *(Check C6: per-block exact identity verified to
mixed tolerance 1e-6 on a 7-schedule battery, every cell; i4c verified it to
1e-44 relative at 60-digit precision.)*

**Lemma B.2 (fast-mode cap).** Let `y := D^{-1/2} e`, so
`Phi = (1/2) y^T H_sym y` with `H_sym = I - c_alpha D^{-1/2} A D^{-1/2}`,
spectrum in `[gamma_alpha, 2/(1+alpha)]`. For any unit eigenvector `q` of
`H_sym` with eigenvalue `mu`, the coefficient `yhat_q = <y, q>` satisfies, at
every time,

```text
(1/2) mu yhat_q^2 <= Phi <= Phi_0,        i.e.   |yhat_q| <= sqrt(2 Phi_0/mu).
```

*Proof.* `Phi = (1/2) sum_k mu_k yhat_k^2`, all `mu_k > 0`, and Lemma B.1. ∎

**The star's exact two-dimensional reduction.** On `K_{1,m}`,
`D^{-1/2}AD^{-1/2}` has the symmetric eigenpairs `lambda = +1` and
`lambda = -1` with unit eigenvectors
`q_{+-} = (sqrt(m), +-1, ..., +-1)/sqrt(2m)`, and `m-1` leaf-difference
eigenvectors with `lambda = 0` vanishing at `c`. So `H_sym` has the **slow
mode** `q_+` (`mu_- ... = 1 - c_alpha = gamma_alpha`), the **fast mode** `q_-`
(`mu_+ = 1 + c_alpha = 2/(1+alpha)`), and an inert middle block; seed-symmetric
dynamics live in the 2-dim `(e_c, E_L)` plane, `E_L := sum_l e_l`
(`yhat_{+-} = (e_c +- E_L)/sqrt(2m)` up to sign convention; the reduction
reproduces the full simulator — check C6's reconciliation, every cell).

**Lemma B.3 (equal-magnitude / displacement cap; Proved-draft).** A centre
relaxation `push(c, delta)` changes `y` by `-(delta/sqrt(m)) ehat_c`, hence it
moves the two modes by **equal magnitudes**

```text
|Delta yhat_+| = |Delta yhat_-| = |delta| |q_{+-}(c)| / sqrt(m) = |delta|/sqrt(2m).
```

The slow coefficient carries the answer, but the fast coefficient lives in
the interval of Lemma B.2; applying that lemma before and after the op,

```text
|delta| <= sqrt(2m) * 2 sqrt(2 Phi_0/mu_+) = 2 sqrt(alpha(1+alpha))
```

at every centre relaxation, for every `omega in (0,2)`, pathwise. Moreover
the fast mode is `1 - O(alpha)`-saturated already at `t = 0`, and consecutive
same-vertex ops compose to a single relaxation with
`omega_eff = 1 - prod_j(1 - omega_j) in (0,2)` (i4c E2), so bursts do not
evade the cap. ∎ *(Checks C7-C8: `|yhat_-|/cap <= 1` and `|delta_c|/cap <= 1`
never violated across the battery, every cell; both near-attained — max
utilizations 0.975-1.000 and 0.854-0.979.)*

**Theorem B.4 (class lower bound for `R+-`; Proved-draft).** Centre-seeded
`K_{1,m}`, `m = floor(1/(8 eps))`, `eps <= 1/16`, `alpha in (0,1)`. Every
member of `R+-` (arbitrary adaptive / randomized / per-vertex-`omega` policy)
that stops with `err(z) <= eps` performs

```text
N_c >= (pi_c - eps m) / (2 sqrt(alpha(1+alpha))) >= 3/(16 sqrt(alpha(1+alpha)))
```

centre relaxations, and therefore

```text
W >= m N_c >= 3/(256 eps sqrt(alpha(1+alpha)))            (all eps <= 1/16;
    coefficient 3/128 on the dyadic grid, where m = 1/(8 eps) exactly).
```

*Proof.* `z_c^0 = 0` and `z_c` changes only at centre relaxations, so the sum
of `|Delta z_c| = |delta|` over centre ops is at least
`z_c^T >= pi_c - eps d_c = pi_c - eps m >= 1/2 - 1/8 = 3/8`. Divide by Lemma
B.3's cap; each centre op is charged `d_c = m >= 1/(16 eps)`. ∎
*(Check C9: 7 schedules (SOR(omega*), GS, omega -> 2, fixed 1.5,
Chebyshev-oscillating, random-omega, leaf-heavy): every finishing schedule
has `N_c >= LB` and `W >= m LB`, every cell, 0 failures; tightest member
`N_c/LB = 1.77-1.99`. i4c's fuller battery adds asymmetric partial-leaf
blocks and Gauss-Southwell, 104 runs, 0 violations.)*

**Theorem B.5 (matching member upper bound; Proved-draft via I2-D T3.3 +
Measured).** On the same instance, SOR at
`omega* = 1 + lambda^2`, `lambda = (1-sqrt(alpha))/(1+sqrt(alpha))`,
alternating centre/leaf blocks, satisfies the *exact* block law
`x_j = (j+1) lambda^j` (I2-D Lemma 3.1) and stops — under the residual
certificate `max_u |r_u|/d_u <= eps`, which implies `err <= eps` by F4+F5 —
within

```text
W_SOR <= m * ceil( (1/sqrt(alpha)) ln( 2/(sqrt(alpha) eps m) ) )  =  O( log(1/alpha) / (sqrt(alpha) eps) ).
```

Under the semantic stop the `log(1/alpha)` disappears: measured
`N_blocks(err) * sqrt(alpha) = 1.35-1.50`, flat over `alpha in [2^-12, 2^-4]`
(check C10 asserts the proved ceiling; the flat semantic constant is printed
per cell), and the `omega -> 2` alternating member achieves
`W * sqrt(alpha) * eps = 0.083-0.094` for `alpha <= 2^-5` (at `alpha = 2^-4`
the near-2 member no longer converges; `omega*` does). Hence on the star

```text
W_{R+-} = Theta( 1/(sqrt(alpha) eps) ),
```

pinned from both sides with ratio `3.5-4.0`, and the `log(1/alpha)` of the
certificate-stopped bound is a stopping-rule artifact (i4c §6.3), consistent
with the manuscript's `Theta(log(1/alpha)/(sqrt(alpha) eps_ppr))` star bound
for certificate-stopped CF-Push/SOR (`subsec:cf-star-lower`) — same method,
different stopping semantics, no contradiction.

**Proposition B.6 (residual-mass cap and output maps; Proved-draft, new).**
Along every `R+-` path on any graph, at every time,

```text
||r||_1 <= sqrt(vol) * sqrt(2 (1+c_alpha) Phi_0);      star:  ||r||_1 <= 2 sqrt(alpha/(1+alpha)).
```

*Proof.* `D^{-1/2} r = H_sym y`, so
`||r||_1 = sum_u sqrt(d_u) |(H_sym y)_u| <= sqrt(vol) ||H_sym y||_2` and
`||H_sym y||_2^2 = y^T H_sym^2 y <= mu_max y^T H_sym y = 2 mu_max Phi
<= 2 mu_max Phi_0`. Star numbers: `vol = 2m`, `mu_max = 2/(1+alpha)`,
`Phi_0 = alpha/(2m)`. ∎ *(Check C12: never violated, utilization
0.975-1.000 — the cap is essentially attained.)*
Consequently Theorem B.4 extends to outputs `z + Mr`, `M in O_B`: the
guarantee at `c` gives `z_c^T >= pi_c - eps m - (Mr)_c` and
`(Mr)_c <= B ||r||_1 <= 2B sqrt(alpha/(1+alpha))`, so for
`B <= (1/16) sqrt((1+alpha)/alpha)` the travel is `>= 1/4` and

```text
N_c >= 1/(8 sqrt(alpha(1+alpha))),        W >= m/(8 sqrt(alpha(1+alpha))).
```

Note the admissible `B` *grows* as `alpha -> 0` (the signed class cannot park
much mass in `r`: energy forbids it); sharpness of this threshold is not
claimed — only the universal `W = 0` escape at
`B >= (1 - eps vol)/gamma_alpha` bounds it from above.

**Proposition B.7 (general graphs; Proved-draft, from i4c Prop 3.4).** For
any connected `G`, seed `v`, let `P_{>=mu0}` project onto `H_sym`-eigenspaces
with eigenvalue `>= mu0` and `kappa_v := max_{mu0} ||P_{>=mu0} ehat_v||
sqrt(mu0)`. Then every seed relaxation has
`|Delta z_v| <= 2 sqrt(gamma_alpha pi_v)/kappa_v`, so if `eps d_v <= pi_v/2`,

```text
N_v >= (kappa_v/4) sqrt(pi_v/gamma_alpha),        W >= d_v N_v.
```

The deciding instance parameter is the seed's self-return amplification
`pi_v/gamma_alpha`: it is `Theta(1/alpha)` on the star (one-step mass
reflection at a degree-`Theta(1/eps)` seed) but only `Theta(1/sqrt(alpha))`
on paths, spiders, caterpillars, trees, grids — where the bound honestly
degrades to `Omega(alpha^{-1/4})` seed ops (measured, 11 graphs). ∎

---

## 5. Proposition C: elimination pays `Theta(1/eps)`

**Proposition C (exact elimination on the star; Proved-draft).** On the
centre-seeded `K_{1,m}`: scan `c` (work `m`, discovering `d_c = m` and the
leaves), scan each leaf (work `1` each) to certify `d_l = 1`, and write

```text
zhat_c = gamma_alpha/(1 - c_alpha^2),        zhat_l = c_alpha zhat_c / m.
```

Then `zhat = pi` exactly (`err = 0`) and `W = 3m + 1 <= 3/(8 eps) + 1`.
*Proof.* Row `l` of `H zhat`: `zhat_l - c_alpha zhat_c/m = 0 = (gamma e_c)_l`.
Row `c`: `zhat_c - c_alpha sum_l zhat_l = zhat_c (1 - c_alpha^2) =
gamma_alpha`. Uniqueness: `H` nonsingular. Work: `m` (centre scan) + `m`
(leaf scans) + `m+1` (output writes). ∎ *(Checks C1, C11: exact to 1e-11,
work bound holds, every cell.)*

Combined with the universal output floor `W >= m` (§2), elimination is
`Theta(1/eps)` on this instance — and it beats every member of `R+-` by
`Theta(1/sqrt(alpha))` (Theorem B.4). Within the one-hop state framework,
what elimination gives up is the axiom `delta = omega r_u, omega in (0,2)`
(its writes are non-dissipative one-hop updates — on a radius-1 instance
one-hop locality itself never binds); on general graphs elimination also
gives up one-hop locality. Theorem B.4 is therefore a **class** bound, not an
information barrier, and gives no support to `1/(sqrt(alpha) eps)` as a
*necessary* cost of the semantic problem (I4-D's `O~(1/eps)` target stands).

---

## 6. The ladder

**Corollary 6.1 (three classes, one instance; Proved-draft).** Fix
`eps <= 1/16`, `alpha in (0, 3/4)`, and the centre-seeded star `K_{1,m}`,
`m = floor(1/(8 eps))`. All classes use the identical primitive, work charge,
output map `z`, and guarantee `err <= eps`. Then:

| rung | class | axiom dropped vs. previous | star work | LB / UB source |
|---|---|---|---|---|
| 1 | `M+` monotone push | — | `Theta(1/(alpha eps))` | Thm A.4 / APPR itself (`prop:appr-upper-bound`) |
| 1′ | `M+-` signed step | step positivity | `Theta(1/(alpha eps))` — **no gain** | Thm A.4 / same |
| 2 | `R+-` signed residual | `r >= 0` | `Theta(1/(sqrt(alpha) eps))` | Thm B.4 / Thm B.5 |
| 3 | elimination (unrestricted one-hop writes) | `delta = omega r_u`, `omega in (0,2)` (dissipativity) | `Theta(1/eps)` | §2 floor / Prop C |

Each rung from 1 to 3 drops exactly one axiom and buys exactly one factor of
`sqrt(alpha)`; the step-sign axiom (rung 1 to 1′) buys nothing. Explicit
constants on the dyadic grid, `alpha <= 1/16`:

```text
M+-:  W alpha eps           >= 0.0397   (members reach 0.087; this battery 0.130)
R+-:  W sqrt(alpha) eps     >= 3/(128 sqrt(1+alpha)) >= 0.0227   (members reach 0.083-0.094)
elim: W eps                 <= 3/8 + eps   vs. the universal floor  W eps >= m eps = 1/8
```

Separation ratios on the single instance: `M+-`/`R+-` `= Theta(1/sqrt(alpha))`
(no log, by the semantic-stop upper bound), `R+-`/elimination
`= Theta(1/sqrt(alpha))`. *(Both rows of constants re-measured by
`verify_ladder.py`; the crossover of the R+- member over the M+- lower bound
is at `alpha ~ 2^-6`, as in I2-D T3.d.)*

**Reading the axioms.** `r >= 0` is the **anti-acceleration axiom**: it is
what forces settling to be paid at the seed's own multiplicative rate
`kappa_+ = Theta(alpha)` (Lemma A.2) instead of the additive fast-mode rate
`Theta(sqrt(alpha))` (Lemma B.3). Dissipative one-hop relaxation is the
**anti-output-linearity axiom**: it is what stops the algorithm from simply
writing a linear functional of what it has seen (the eliminator's closed
form); its price is the fast-mode cap, and its output-side shadow is the
column-mass threshold `B = (1 - eps vol)/gamma_alpha`, beyond which even a
one-hop *output* map is linear-powerful enough to print the answer at
`W = 0` (I2-D Lemma 1.2/Prop 1.3: on radius-1 instances the entire output-map
question collapses to the single scalar `B`).

---

## 7. Relation to the manuscript, and two Opens

**APPR star theorem.** The manuscript's `thm:appr-star-lower-bound`
(`W > 3/(128 alpha eps_appr)` for literal lazy APPR under every legal
ordering, with the matching `prop:appr-upper-bound`) is the literal-APPR
anchor of rung 1: lazy APPR is the `M+` member `push(u, ((1+alpha)/2) r_u)`,
its termination rule implies `err <= eps_appr` (F4, the manuscript's
`eq:appr-accuracy` route), and Theorem A.4 applied with `eps := eps_appr`
reproduces the `Theta(1/(alpha eps_appr))` conclusion with constant
`0.0397-0.0433 > 3/128` while extending it to arbitrary step sizes, signed
steps, batching, `O_B` outputs, and arbitrary stopping rules. The manuscript
theorem should be **cited as the special case that fixed the instance and
the mechanism** (its Steps 1-2 are the mass-scale ancestors of Lemmas
A.2-A.3); the namespaces `eps_appr` and `eps_ppr` remain distinct, and the
bridge above is the only identification used.

**CF-Push / SOR star bound.** The manuscript's
`Theta(log(1/alpha)/(sqrt(alpha) eps_ppr))` star result for
certificate-stopped CF-Push(`omega*`) (`subsec:cf-star-lower`,
`eq:cf-opt-sor-identities`) is one member of `R+-` under one stopping rule.
Theorem B.4 supplies the missing *class* lower bound `Omega(1/(sqrt(alpha)
eps))`, and the `log(1/alpha)` gap between them is exactly the certificate
artifact (i4c §6.3): the same member under the semantic stop runs in
`Theta(1/sqrt(alpha))` blocks. Cite, do not subsume: the manuscript statement
is about the method-plus-certificate; ours is about the class-plus-semantics.

**CF-Push long spider.** The manuscript's long-spider `Omega(1/(alpha eps))`
obstruction for fixed-`omega*` FIFO CF-Push is a statement about a specific
`R+-` member under the `gamma_alpha eps d`-activation certificate on a
*different* instance — one whose semantic content is empty in the relevant
regime (`S_eps = emptyset` for `alpha <= 2^-8`; i4c §6.1, and the dedicated
audit in `findings/i5a_manuscript_spider.md`). It is therefore a certificate
lower bound, fully compatible with Theorem B.5, and it is the reason this
package's hard instance is the star, which is semantically nontrivial
(`S_eps = V`, §2). Again: cite, do not subsume.

**Open 1 (general-graph `O_B` terminal bound; the constant `Phi`).**
Consolidation removed the instance constant
`Phi = max_u d_u pi_u / (d_v pi_v)` from every main statement: Theorem A′ and
the `B = 0` case of Theorem A.4 use only the seed coordinate of the
guarantee. What remains open is the general-graph version of Lemma A.3(ii) —
the terminal `Psi` bound for outputs `z + Mr` with `B` near the escape
threshold — where the old route `Psi_T <= Phi ||r_mass||_1` re-enters and is
sharp only if `Phi = 1`. Conjecture (Measured on 10 zoo graphs x 3 alpha,
i2d): `Phi = 1` whenever the seed maximizes `d_u pi_u`; equivalently
`pr(e_u)_v <= pr(e_v)_v` for all `u`. Until proved (or a counterexample
found), general-graph statements should use Theorem A′ / A.3(i), which are
`Phi`-free but cover a smaller `B` range.

**Open 2 (does anything besides the star force `1/(sqrt(alpha) eps)` on
`R+-`?).** Theorem B.4 is star-specific through one number: the seed's
self-return amplification `pi_v/gamma_alpha = Theta(1/alpha)`, achieved by a
degree-`Theta(1/eps)` seed that reflects its mass back in one step. Prop B.7
shows bounded-degree 1-D-like families amplify only `Theta(1/sqrt(alpha))`
and yield just `Omega(alpha^{-1/4})` seed ops, and i4c §6.1 closes the spider
route. Open, in falsifiable form: exhibit a family with
`vol(S_eps) = Theta(1/eps)` and *bounded* seed degree on which every `R+-`
member needs `Omega(1/(sqrt(alpha) eps))` work — or prove that
`pi_v/gamma_alpha = Theta(1/alpha)` (hence a `Theta(1/eps)`-degree seed, hence
essentially the star) is *necessary*, making the star the unique hard
instance shape for one-hop relaxation. A positive resolution of either branch
would decide whether the class barrier is a local anomaly of reflecting seeds
or a graph-uniform phenomenon. (Related but distinct known gap: one-hop
*block* relaxations escape Lemma B.3 by construction — the centre-plus-leaves
block solves the star in `O(m)` — so the block question is about the cheapest
implementable primitive that is spectrally aligned with the slow mode, i4c
§8; it is a design question, not part of this Open.)

---

## 8. Verification appendix

Script: `/home/claude/work/overnight/i5d/verify_ladder.py` (single file;
imports `lib/zoo.py`, `w1_monotone_lb/gpush.py`, `i4c/core.py`; the 2-dim
block reduction is the one validated against the full simulator in i2d/i4c
and re-reconciled here against the full `(m+1)`-dimensional state every 64
blocks and at every stop). Checks C1-C13 map to the numbered statements as
listed in the script header (C1 closed forms + Prop C exactness; C2-C3
Lemmas A.1-A.2; C4-C5 Theorem A.4/Corollary A.5 on three member policies +
pump adversary; C6 Lemma B.1 + reduction reconciliation; C7-C8 Lemmas
B.2-B.3; C9 Theorem B.4 over a 7-schedule battery; C10 Theorem B.5 both
forms; C11 Proposition C; C12 Proposition B.6; C13 the scale dictionary).
Full output (45 cells x 13 checks, **0 failures**; rerun ~2 min):

```text
======================================================================================================================
I5-D  verify_ladder  --  star K_{1,m}, m = 1/(8 eps);  checks C1-C13 (see header);  . = pass, X = FAIL
======================================================================================================================
  alpha    eps   m |   C1   C2   C3   C4   C5   C6   C7   C8   C9  C10  C11  C12  C13 |  NcA/LB  W*ae>=  NcB/LB  W2*sae  N(w*)sa   maxY   maxD  max|r|1
2^-4    2^-4     2 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.557  0.1328   3.806     nan    1.500  1.000  0.970    1.000
2^-4    2^-5     4 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.557  0.1328   3.806     nan    1.500  1.000  0.970    1.000
2^-4    2^-6     8 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.557  0.1328   3.806     nan    1.500  1.000  0.970    1.000
2^-4    2^-7    16 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.557  0.1328   3.806     nan    1.500  1.000  0.970    1.000
2^-4    2^-8    32 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.557  0.1328   3.806     nan    1.500  1.000  0.970    1.000
2^-5    2^-4     2 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.500  0.1328   1.838  0.0884    1.414  1.000  0.854    1.000
2^-5    2^-5     4 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.500  0.1328   1.838  0.0884    1.414  1.000  0.854    1.000
2^-5    2^-6     8 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.500  0.1328   1.838  0.0884    1.414  1.000  0.854    1.000
2^-5    2^-7    16 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.500  0.1328   1.838  0.0884    1.414  1.000  0.854    1.000
2^-5    2^-8    32 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.500  0.1328   1.838  0.0884    1.414  1.000  0.854    1.000
2^-6    2^-4     2 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.516  0.1309   1.974  0.0938    1.375  0.999  0.940    0.999
2^-6    2^-5     4 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.516  0.1309   1.974  0.0938    1.375  0.999  0.940    0.999
2^-6    2^-6     8 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.516  0.1309   1.974  0.0938    1.375  0.999  0.940    0.999
2^-6    2^-7    16 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.516  0.1309   1.974  0.0938    1.375  0.999  0.940    0.999
2^-6    2^-8    32 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.516  0.1309   1.974  0.0938    1.375  0.999  0.940    0.999
2^-7    2^-4     2 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.502  0.1309   1.873  0.0884    1.414  0.997  0.940    0.997
2^-7    2^-5     4 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.502  0.1309   1.873  0.0884    1.414  0.997  0.940    0.997
2^-7    2^-6     8 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.502  0.1309   1.873  0.0884    1.414  0.997  0.940    0.997
2^-7    2^-7    16 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.502  0.1309   1.873  0.0884    1.414  0.997  0.940    0.997
2^-7    2^-8    32 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.502  0.1309   1.873  0.0884    1.414  0.997  0.940    0.997
2^-8    2^-4     2 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.506  0.1304   1.994  0.0859    1.375  0.991  0.979    0.991
2^-8    2^-5     4 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.506  0.1304   1.994  0.0859    1.375  0.991  0.979    0.991
2^-8    2^-6     8 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.506  0.1304   1.994  0.0859    1.375  0.991  0.979    0.991
2^-8    2^-7    16 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.506  0.1304   1.994  0.0859    1.375  0.991  0.979    0.991
2^-8    2^-8    32 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.506  0.1304   1.994  0.0859    1.375  0.991  0.979    0.991
2^-9    2^-4     2 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.503  0.1301   1.883  0.0829    1.370  0.980  0.969    0.980
2^-9    2^-5     4 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.503  0.1301   1.883  0.0829    1.370  0.980  0.969    0.980
2^-9    2^-6     8 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.503  0.1301   1.883  0.0829    1.370  0.980  0.969    0.980
2^-9    2^-7    16 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.503  0.1301   1.883  0.0829    1.370  0.980  0.969    0.980
2^-9    2^-8    32 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.503  0.1301   1.883  0.0829    1.370  0.980  0.969    0.980
2^-10   2^-4     2 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.501  0.1300   1.832  0.0859    1.375  0.986  0.966    0.986
2^-10   2^-5     4 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.501  0.1300   1.832  0.0859    1.375  0.986  0.966    0.986
2^-10   2^-6     8 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.501  0.1300   1.832  0.0859    1.375  0.986  0.966    0.986
2^-10   2^-7    16 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.501  0.1300   1.832  0.0859    1.375  0.986  0.966    0.986
2^-10   2^-8    32 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.501  0.1300   1.832  0.0859    1.375  0.986  0.966    0.986
2^-11   2^-4     2 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.500  0.1300   1.767  0.0829    1.348  0.975  0.958    0.975
2^-11   2^-5     4 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.500  0.1300   1.767  0.0829    1.348  0.975  0.958    0.975
2^-11   2^-6     8 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.500  0.1300   1.767  0.0829    1.348  0.975  0.958    0.975
2^-11   2^-7    16 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.500  0.1300   1.767  0.0829    1.348  0.975  0.958    0.975
2^-11   2^-8    32 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.500  0.1300   1.767  0.0829    1.348  0.975  0.958    0.975
2^-12   2^-4     2 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.500  0.1300   1.833  0.0840    1.359  0.978  0.974    0.978
2^-12   2^-5     4 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.500  0.1300   1.833  0.0840    1.359  0.978  0.974    0.978
2^-12   2^-6     8 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.500  0.1300   1.833  0.0840    1.359  0.978  0.974    0.978
2^-12   2^-7    16 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.500  0.1300   1.833  0.0840    1.359  0.978  0.974    0.978
2^-12   2^-8    32 |    .    .    .    .    .    .    .    .    .    .    .    .    . |   1.500  0.1300   1.833  0.0840    1.359  0.978  0.974    0.978
----------------------------------------------------------------------------------------------------------------------
cells: 45   checks per cell: 13   FAILED cell-checks: 0
ALL PASS: every numbered inequality holds on every grid cell.
```

Column reading: `NcA/LB` = tightest member's `N_c^+` over Theorem A.4's bound
(min over the 3-policy + pump battery; always `>= 1`, so the bound holds with
1.5x member headroom here; I2-D's larger zoo closes it to 1.015);
`W*ae>=` = smallest `W alpha eps` observed (floor 0.0397 dyadic);
`NcB/LB` = tightest schedule over Theorem B.4's bound (1.77-1.99 for
`alpha <= 2^-5`; the bound is tight to <2x); `W2*sae` = the `omega -> 2`
member's `W sqrt(alpha) eps` (flat 0.083-0.094; `nan` at `alpha = 2^-4`
where that member stalls and SOR(`omega*`) is the witness);
`N(w*)sa` = SOR(`omega*`) semantic-stop blocks x `sqrt(alpha)` (flat 1.35-1.50:
no `log(1/alpha)`); `maxY`, `maxD`, `max|r|1` = utilization of the caps in
Lemmas B.2, B.3 and Prop B.6 (all `<= 1`, all nearly attained — the
inequalities are the right ones, with no slack to spare).

Not re-verified here (covered by the source packages): asymmetric /
partial-leaf / Gauss-Southwell schedules and the 60-digit energy identity
(i4c E3, E4: 104 runs, 0 violations), the 14-policy member zoo and the LP
output-map thresholds to 4 decimals (i2d member_check / outmap_lp), the
general-graph zoo sweeps (i2d P1-P3, i4c E4.a).

---

## 9. Honesty pass: status of every step, and what an auditor should check first

**Proved-draft (complete arguments above, unaudited):** Lemmas A.1-A.3,
Theorem A.4, Corollary A.5, Theorem A′; Lemmas B.1-B.3, Theorem B.4,
Proposition B.6, Proposition B.7; Proposition C; Corollary 6.1's lower/upper
pairings except as noted next.

**Proved-draft with an imported proof not re-derived here:** Theorem B.5's
certificate-stopped upper bound (I2-D Theorem 3.3: the `x_j = (j+1)lambda^j`
block law and the log-bearing ceiling; its proof is 10 lines in the source
and was verified to 1.4e-13 over 40 blocks); the W1 characterization lemma
("every invariant-exact one-hop update is `push(u, delta)`"), on which the
*definition* of the classes leans — its star-closure extension (multi-base
ops when the `z`-changes-only-at-base axiom is dropped) is proved only on
the star.

**Verified numerically, not proved:** the semantic-stop flatness
`N(omega*) sqrt(alpha) in [1.35, 1.50]` and the `omega -> 2` member constant
`W sqrt(alpha) eps in [0.083, 0.094]` (45 cells here + i4c's 15-cell sweep;
these calibrate Theta-tightness of Theorem B.4 but the *proved* upper bound
carries a `log(1/alpha)`); `Phi = 1` on the 10-graph zoo (Open 1);
`pi_v/gamma_alpha` scalings of Prop B.7 beyond closed-form families.

**Open (labelled):** Open 1 (general-graph `O_B` terminal bound / `Phi = 1`);
Open 2 (`R+-` beyond the star). Known class-scope limits, not Opens: one-hop
*block* relaxations are outside `R+-` and defeat Lemma B.3 by design (i4c
§8); `M+-` bounds assume the invariant-exact primitive, so inexact/rounded
arithmetic is outside the model.

**Auditor's checklist, in order of leverage.**
1. **Lemma A.2's two uses of `r >= 0`** (feasibility `delta <= r_c`, and
   `e_c >= (pi_c/gamma_alpha) r_c` via F2/F3). This is the entire monotone
   bound; it is 5 lines and either it survives audit or rung 1 falls.
2. **Lemma B.3's before/after application of Lemma B.2** (the factor 2 in
   the displacement cap) and the claim that the leaf-difference modes vanish
   at `c` (so only `q_-` caps the centre). Check the eigendecomposition by
   hand for `m = 2`.
3. **Theorem A.4's handling of batched ops**: Lemma A.1 covers any
   invariant-preserving update, but the *feasibility cap* `delta <= r_c` is
   per-op; confirm a simultaneous batch cannot settle more at `c` than
   sequential ops with the same intermediate states (W1 Lemma 1′ does this on
   the star; its scope is star-specific — flagged above).
4. **The `O_B` fairness scoping in §2**: the claim "`B >= (1-eps vol)/gamma`
   escapes for every class at `W = 0`" is I2-D Prop 1.3; re-check its LP
   witness or the two-line Hall argument, since the whole ladder's "same
   output map" framing rests on choosing `B` below it.
5. **Dyadic vs general-`eps` constants** (`m = 1/(8 eps)` exact vs
   `>= 1/(16 eps)`): every displayed constant states which case it is; the
   verification grid is dyadic only.
6. Rerun `verify_ladder.py` (2 min) and, for the pieces this script inherits,
   `i4c/verify.py` + `w9_i2d/member_check.py` (~13 min total).

**Supersession note.** This package supersedes: W1 Lemmas 3-5 and Theorem 6
(replaced by Theorem A.4 with better constants and wider scope); I2-D §2's
mass-scale potential presentation (replaced by the z-scale Psi, which also
retires the `Phi` constant from Prop 2.6's role in the main line); i4c's
`3/128` display (now stated with its dyadic scope explicit, general-`eps`
constant `3/256`). It leaves standing: I2-D §1 (output-map LP/transport
characterization), I2-D T3.3 (certificate-stopped SOR upper bound), i4c §6
(spider/stopping-rule calibrations), and all general-graph zoo measurements.
