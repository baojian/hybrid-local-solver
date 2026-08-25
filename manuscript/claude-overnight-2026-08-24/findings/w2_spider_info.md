# W2 — Information lower bound on spider ensembles: exact sensitivities, the forced-probe theorem, and the Theta(1/eps) ceiling

**Direction:** information-theoretic (adjacency-probe) lower bound of order
1/(sqrt(alpha)*eps) on center-seeded spider ensembles.

**VERDICT (headline).** The spider/truncation ensemble certifies a clean,
honest **Omega(1/eps)** probe lower bound (deterministic and randomized), with
the structural refinement that the probes must reach **depth Theta(1/sqrt(alpha))
in Theta(sqrt(alpha)/eps) separate arms**. It **cannot** certify
Omega(1/(sqrt(alpha)*eps)): the forced product k*j* has an exact ceiling
Theta(1/eps) over the entire ensemble family (measured max 0.066/eps,
alpha-independent), consistent with and matching the killed-capacity ceiling
`thm:corridor-capacity` (32/tau). **Refuted-draft:** the W2 target statement
"Omega~(1/(sqrt(alpha)*eps)) is information-theoretically necessary, witnessed
by spiders". Any Omega(1/(sqrt(alpha)*eps)) necessity must come from
non-corridor interference (a counterexample to `conj:influence-packing`) or be
computational rather than informational.

Access model used throughout: **adjacency-list scan** (scanning a discovered
vertex u reveals its full neighbor list; probes restricted to the seed and
previously revealed ids). Bounds are stated in #scans; they hold unchanged in
#revealed-edges and vol(scanned) currency up to a factor 2 (+k for the center
scan), and per-edge probing only increases the count. The blind-probe caveat
is in "Gaps" below.

Code: `/home/claude/work/overnight/w2_spider_info/{formulas,sensitivity,validate,theorem_constants}.py`.

---

## 1. Exact closed forms (Proved-draft; sympy-verified identities + exact-Fraction equality against `ExactModel.solve_pi` on unequal-arm spiders for alpha in {1/16, 1/64, 1/256})

Work in the semantic scale u_i = pi_i/d_i (output eps-valid iff
|pi_hat_i/d_i − u_i| <= eps coordinatewise). The lazy degree-scaled system
H pi = gamma e_v becomes symmetric: **(D − cA) u = gamma e_v**, with
c = (1−alpha)/(1+alpha), gamma = 2 alpha/(1+alpha). Write s = sqrt(alpha),
lambda = (1−s)/(1+s); then c = 2 lambda/(1+lambda^2), gamma = 1−c =
(1−lambda)^2/(1+lambda^2), and gamma/(1−c lambda) = s.

For the spider with center seed (degree k) and arm lengths L_1..L_k:

- Arm transfer ratio (m vertices strictly below the current one; free end):
  **psi(m) = lambda (1+lambda^{2m}) / (1+lambda^{2m+2})**, psi(0) = c,
  psi(m) − lambda = lambda^{2m+1}(1−lambda^2)/(1+lambda^{2m+2}) > 0
  (truncation = reflection ⇒ psi > lambda, decaying at the **round-trip** rate
  lambda^{2m}).
- Center: **u_0 = gamma / (k − c Σ_a psi(L_a − 1))**, and
  **u_0 > s/k for every finite arm configuration** (since psi > lambda);
  u_0 → s/k as all L_a → ∞ (recovers pi_center = sqrt(alpha), the path kernel).
- Arm profile: **u_j = u_0 (lambda^j + lambda^{2L−j}) / (1+lambda^{2L})**,
  j = 1..L. (pi: center k u_0, arm interior 2 u_j, arm end u_L.)

### (a) Center impedance of one truncated arm (exact)
One arm truncated at depth j, others long:
**Delta u_0(j) = (2 + o(1)) (s/k^2) lambda^{2j}**, monotone decreasing in j;
the limiting constant is exactly 2 (symbolic identity
gamma·c·(1−lambda^2)/(lambda(1−c·lambda)^2·s) ≡ 2). Measured normalized
constants: 1.57→2.000 (alpha=1/16, j=1..16), 1.26→2.000 (alpha=1/256,
j=1..64). Center effect decays at the round-trip rate lambda^{2j} — the arm's
"impedance mismatch" seen from the seed.

### (b) Local effect near the truncation (exact)
Truncation at j vs continuation: at common vertex i < j,
**u_i^{trunc}/u_i^{full} = 1 + lambda^{2(j−i)}** up to an O(lambda^{2j}/k)
center-shift; gap |Delta u_i| = (1+o(1)) (s/k) lambda^{2j−i}, maximized at the
frontier i = j−1, where the value is boosted by the factor 1+lambda^2 ≈ 2
(measured 1.9963 at alpha=1/256). The truncation vertex j itself is a **bad**
distinguisher in this metric: its pi barely moves (only its degree changes,
and the metric divides by the instance's own degree). Verified argmax of the
distinguishability statistic is always the deepest common arm vertex, never
the center.

### (c) Forced-distinguish predicate and critical depth (exact)
Two graphs sharing the probed portion admit no common eps-valid output iff
some common vertex i has |pi^G_i − pi^{G'}_i| > eps (d^G_i + d^{G'}_i)
(per-coordinate interval overlap; ids unseen by the algorithm are
adversary-controlled, so one-sided vertices impose no joint constraint).
For equal-degree-2 vertices this is |Delta u_i| > 2 eps. Consequences,
verified exactly and on float-solved graphs (agreement to all printed digits;
flip location exact):

**j*(alpha, eps, k) = ln( s/(2 k eps) ) / ln(1/lambda) + Theta(1)
= (1/(2s))·ln( s/(2 k eps) )·(1 + O(s)) + Theta(1).**

A truncation (or any passive completion change) hidden at depth j is
output-relevant iff j <= j*. Measured vs predicted (alpha=1/256, eps=s/512):
k=2: 37 vs 38.8; k=25: 17 vs 18.6; k=51: 9−10 vs 12.9. Degree gadgets do not
beat the eps·d slack: the widest passive two-sided range at a hidden port
(reflecting leaf vs heavy star-sink, exact small-graph computation) widens the
one-sided gap by factor 1.77 — constants only. The extreme passive loads are
psi ∈ (0, c] (absorbing ↔ reflecting), and the exponential envelope lambda^j
is unbreakable by any passive completion.

## 2. The theorem the ensemble supports (Proved-draft)

**Ensemble E(alpha, eps):** alpha <= 1/16, s = sqrt(alpha), **eps <= s/80**
(the live wedge; k >= 2 requires it). J = ceil(1/s), k = floor(s/(40 eps)).
Spiders with k arms, each arm's depth in {J, 2J}; n <= 2kJ+1 finite.

**Theorem A (deterministic).** Any deterministic algorithm that outputs an
eps-valid degree-normalized PPR vector on every instance of E must make at
least k·J + 1 >= **1/(80·eps)** scans on the all-2J instance.
*Proof (adversary):* answer all probes as in the all-2J spider. If arm a gets
no probe at depth >= J, both depth-J and depth-2J completions of arm a are
transcript-consistent, and at arm a's vertex J−1 (degree 2 in both) the exact
gap is |Delta u| >= 2 eps · 1.43 > 2 eps — verified exactly for
alpha ∈ {1/16, 1/64, 1/256, 1/1024} across eps ∈ [s/20480, s/80], with margin
increasing as alpha decreases (1.43 → 2.40); uniform in the rest-arms
configuration because u_0 > s/k always. So every arm needs a probe at depth
>= J, and reaching depth J requires probing depths 1..J−1 first (probes
restricted to discovered ids), i.e., >= J scans per arm plus the center.

**Theorem B (randomized, Yao).** Arm depths iid uniform{J, 2J}. Any algorithm
correct with probability >= 2/3 makes >= kJ/8 = **Omega(1/eps)** expected
scans (needs k >= 4, i.e., eps <= s/160).
*Proof sketch:* for a deterministic algorithm, "arm a unresolved" (no probe at
depth >= J) is transcript-measurable, and unresolved depths stay iid uniform
given the transcript. The key **per-arm dictatorship** step: the two intervals
of possible u_{(a,J−1)} values, [u_0^{min|l_a=J}·g_J, u_0^{max|l_a=J}·g_J]
and the l_a=2J analogue (extremes over ALL rest configurations), are separated
by > 2 eps (measured separation margin 1.29–2.44 across the grid). Hence for
any fixed output, at most one value of l_a is compatible **regardless of the
other arms**, so P(valid | transcript) <= 2^{−#unresolved}. Markov on probes
+ 2^{−k/2} finishes.
*This separation is the overlap subtlety that killed the earlier killed-Green
corridor packing:* with the natural J = ceil(1/(2s)) it genuinely FAILS
(separation ratio −0.67 at alpha=1/16, large k) because the cross-arm coupling
through u_0 has relative range ~lambda^{2J} ≈ e^{−2}, comparable to the
per-arm signal. Doubling to J = ceil(1/s) shrinks the coupling to e^{−4} and
restores it. The spider is rescuable because each arm's influence on the
shared u_0 is O(1/k) of its own local signal; general overlapping-corridor
ensembles have no such factor.

## 3. The ceiling: why 1/(s·eps) is impossible here (Measured + matches proved capacity bound)

Maximizing the forced product over the whole family (k free, J free, exact
Fraction predicate): max_k k·j*_yao(k) ≈ **0.05–0.07 / eps for every alpha**
(1/16, 1/64, 1/256) and every eps tested — alpha-independent as a multiple of
1/eps; as a multiple of 1/(s·eps) it vanishes like s (0.0125 → 0.0086 →
0.0044). Mechanism: distinguishability at depth J needs per-arm signal
(s/k)·lambda^J > 2 eps, i.e., k <= (s/(2eps))·lambda^J, so
k·J <= (s/(2 eps))·J·e^{−2sJ(1+O(s))}, maximized at J = Theta(1/s) with value
Theta(1/eps) — the arm count and the log trade off exactly. The short-arm
resistive corner (J << 1/s, signal ~ alpha·J/k) obeys the same ceiling
(alpha·J^2/eps <= Theta(1/eps)); the measured optimum sits near that corner
but never exceeds 0.07/eps. This is the extremal realization of
`thm:corridor-capacity` (sum_j min(alpha L_j, s) < 32 alpha/tau ⇒ corridor
exposure < 32/tau): our floor 0.066/eps and that ceiling 32/eps bracket the
spider information complexity to Theta(1/eps) within a constant factor ~500.

**Depth necessity (separate resource, Proved-draft):** on a k=O(1) spider
(path), probes must reach depth (1/(2s))·ln(s/(2eps)) − O(1) = Theta(log(s/eps)/s)
— a radius lower bound **with** the log; but total probes there are only
Theta(log(s/eps)/s). Combined honest statement:
**Omega( 1/eps + log(s/eps)/s )** probes, where 1/eps always dominates in the
wedge; the product 1/(s·eps) is NOT forced.

## 4. Gaps and caveats (honest ledger)

1. **Constant certification is exact-at-grid, not yet symbolic:** det/Yao
   margins verified by exact rational computation at alpha ∈ {1/16, 1/64,
   1/256, 1/1024}, eps grid to s/20480, with monotone-in-alpha margins; the
   all-(alpha, eps) statement needs a routine monotonicity lemma on elementary
   rational functions of lambda (Open, mechanical).
2. **Probe-model fine print:** the per-arm depth-J requirement uses
   discovery-restricted probing. Under blind probing of arbitrary ids
   (adversarial random id assignment), the Omega(1/eps) total survives via an
   output-listing argument on this same ensemble (≈1.8k/s = Omega(1/eps)
   coordinates have u_i > eps, must be output nonzero, each scan reveals <= 2
   new ids off-center) — but the structural "depth J per arm" claim does not.
3. **Adaptivity** is fully handled (adversary/transcript arguments); the
   subtle step was cross-arm coupling in Yao, resolved by interval separation
   at J = ceil(1/s).
4. The ceiling argument (Section 3) is a measured maximization over the
   truncation-ensemble family plus the proved capacity theorem for all
   corridor families; it is not a new impossibility beyond
   `thm:corridor-capacity` — it confirms the spider sits at that ceiling's
   scale and cannot pass it.
5. Degree-vs-probe accounting: all bounds stated in scans; vol currency
   multiplies by ~2; no hidden d_u charges (max degree in ensemble is k at
   the center, scanned once).

## 5. Next target

The information complexity of spiders (and, by `thm:corridor-capacity`, all
disjoint-corridor families) is Theta~(1/eps). Therefore: (i) the
Omega(1/(s·eps)) *necessity* question is now squarely a choice between a
**non-corridor interference family** — stress `conj:influence-packing` with
overlapping corridors / hidden degree-preserving swaps behind shared exposure
regions, where the Yao-separation failure mode we isolated (coupling range
lambda^{2J} vs per-arm signal, un-divided by k) is exactly the effect to
amplify rather than avoid — or (ii) accepting that the product scale is
**computational**, and proving the matching O~(1/eps)-probe information upper
bound (capacity-guided best-first exploration with a passive-completion
envelope, sec. 18 program), for which this ensemble (plus the leaf-vs-sink
extremes psi ∈ (0, c]) supplies both the extremal test family and the exact
envelope endpoints. Recommendation: (ii) first — the envelope certificate on
trees is within reach using u_0 > s/k monotonicity and the psi-interval, and
it would cleanly split information Theta~(1/eps) from computation
Theta(1/(s·eps)), turning the project's product lower bound into a provably
computational statement.

---
*Labels: Sec.1 Proved-draft (symbolic + exact-rational cross-checks); Sec.2
Proved-draft (adversary arguments complete; constants exact-at-grid, see Gap
1); Sec.3 Measured (+ proved ceiling via thm:corridor-capacity); Sec.5 Open.*
