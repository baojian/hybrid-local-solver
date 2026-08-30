# Two-stage point-source AESP-CD

This standalone note develops a shorter, at-most-two-stage
**screen, complete, or solve** architecture
for canonical single-source local PageRank:

1. run an interruptible local screen or fixed-envelope AESP scratch;
2. return immediately, clean a lower-safe checkpoint by APPR/SOR, or discard
   changing-face history and solve ordinary PPR once on a certified set.

```text
direct APPR ------------------------------- numerical certificate -> return
Green / leakage screen ----\
AESP-CD / SOR / APPR face --+-- first certified set -> discard history
tree threshold messages ----+                         -> solve Q_E u = b_E once
random threshold batches ---/
```

The direct lane makes the portfolio unconditional.  The speculative lanes
are allowed to lose; their work is interrupted and charged rather than hidden.

If Stage 1 returns the numerical RPPR/APPR checkpoint used to certify the set,
the note proves that checkpoint is already accurate enough for the requested
PPR target and should be returned immediately.  This screen-or-solve
dichotomy is the main simplification: the fixed-face tail is optional polishing
unless a future engine finds the set substantially more cheaply than it finds
the values.

The original containing-envelope composition is

```text
W_total = W_discovery + O_tilde(vol(E) / sqrt(alpha)),
```

where `E` contains the RPPR support. Exact support is optional, and Stage 2 is
a linear system rather than another obstacle problem. With an iterative tail,
one may split the tolerance between `rho` and the terminal residual. With an
exact structural tail, the correct choice is `rho = eps_ppr`: the tail
replaces Stage-I recovery, uses no numerical error budget, and
`vol(E) = O(1 / eps_ppr)`.

The companion `active_edge_lcp` note now supplies the arbitrary-graph
randomized Stage 1.  Its threshold batches solve only
`O_tilde(1 / sqrt(alpha))` complete exposed faces, certify every accepted
randomized SDD call by an exact residual scan, and never activate outside the
true RPPR support.  Crucially, the final face `U` may be a strict subset of
`S*`.  A new transfer lemma proves

```text
max_{i outside U} x*_rho(i) / sqrt(d_i)
    <= sqrt(2 * face_gap / alpha),
PPR_error(Q_U^{-1} b_U) <= rho + sqrt(2 * face_gap / alpha).
```

Thus a low-energy inner face is already a set-only Stage-1 certificate.  With
`face_gap = alpha * eta^2 / 2`, an independent ordinary-PPR Stage 2 gives a
literal two-stage algorithm with expected fully charged work
`O_tilde(1 / (eps_ppr * sqrt(alpha)))` on every graph.  The shorter execution
returns the certified RPPR point directly at the same scale.  This is an
exact-real randomized word-model theorem; deterministic finite-precision and
coefficient-bit complexity remain open.

The cleanest set-only lane does not solve RPPR at all.  Point-source Green
decay gives an explicit rooted ball on which one principal CG solve suffices.
The ball is exposed under a hard cap and raced against direct APPR, so a
successful branch has the target product scale while cap failure costs only a
constant-factor fallback.  In a 90-case high-accuracy sweep the standalone
lane wins 22 cases across stars, binary trees, a grid, a path, and a cycle;
15 remain strict wins after charging the simultaneous APPR lane.

The most literal exact-support lane is also implemented.  Coarse priority
APPR snapshots or a positive-residual SOR/AESP discovery state propose a
face; one tree/unicyclic solve and one complete KKT scan either certify
`S*` or reject it.  The verifier is raced against the continuing direct APPR
state, so failure costs at most a factor two.  Returning the exact verifier
point gives five SOR and four APPR fair-race wins.  Charging a separate fresh
ordinary-PPR Stage 2 leaves all five SOR wins and two APPR wins.
If the exact verifier retains its tree/unicyclic factors, the charged
backsolve model raises the standalone counts from 4 to 6 for APPR and from 5
to 7 for SOR; the fair counts remain 2 and 5.

The repeated exact positive-boundary baseline certifies 75 of 90 cases.  Its
exact RPPR point wins 43 standalone and 13 after the fair charge; charging a
fresh ordinary-PPR Stage 2 leaves 33 standalone and 8 fair wins.  A path still
needs 38 singleton refits, so this is a useful portfolio lane rather than a
universal work proof.
Retaining the last structural factors improves those literal counts to 37
standalone and 9 fair wins.

For point-source trees, exact support identification no longer needs a
proposal race.  The implemented threshold-message reporter performs scalar
Schur updates only along the newly admitted root path, then makes one
fixed-face leaf solve.  A separate global KKT scan audits the implementation.
It certifies all 60 path/star/binary/broom
instances (1,024--2,047 vertices).  Among 51 nontrivial direct-APPR
comparisons, returning its already accurate RPPR point wins 27 standalone and
14 after the one-for-one race.  A literal Stage 2 ordinary-PPR solve has the
same counts because it replaces RPPR recovery instead of being appended to
it; its exactness permits $\rho=\varepsilon$ rather than an unnecessary
half split.  All Stage 2 outputs pass the semantic PPR target; 1,890 additional
randomized small-tree traces also passed the independent KKT verifier.

An even shorter direct composition does not use RPPR: a coarse principal PPR
solve plus a residual error bar bounds every exterior boundary leakage. If
all upper bounds are below `alpha * delta`, the envelope is already a
`delta`-accurate truncation and one fixed refinement completes it. This gate
is local, observable, and exact-support-free.

A second proved composition does not identify `S*` at all. If a local
envelope's principal PPR solution captures `1 - O(sqrt(alpha))` total mass,
signed Chebyshev/AESP scratch plus an a-posteriori Stieltjes retraction
publishes a global lower checkpoint with the same mass guarantee. APPR/SOR
then completes it in `O_tilde(1 / (eps_ppr sqrt(alpha)))` work. The handoff
test is observable.  A star-family barrier proves that no uniformly
output-volume mass certificate exists for the $\ell_\infty$ target, so this is
an instance-selective portfolio opportunity rather than a replacement for
the numerical early-return lane.

A hard-capped version is unconditional: try geometrically growing envelopes
up to `B`, take the mass handoff on success, and otherwise restart direct
APPR. With `B=O(1/eps_ppr)`, a successful trace has the target accelerated
scale, while a failed trace preserves the classical APPR bound.

The point-source assumption also yields an explicit universal test: a rooted
radius-`R` ball has principal-PPR mass deficit at most
`((1-alpha)/(1+alpha))^(R+1)`. This guarantees eventual mass capture, though
its worst-case radius is `O(log(1/alpha)/alpha)` and its volume need not be
local. The hard cap is therefore essential.

The note compares APPR, monotone SOR/Gauss--Seidel, safe AESP-CD obstacle
batches, structural response reporters, and a hard-capped dynamic-obstacle
interface. It also proves a fair certificate-race wrapper and explains how the
complementary AESP-burn-in--SOR lane fits the same portfolio.

A fully computable priority-GS discovery lane stops on a maximum positive-key
certificate, with unconditional
`O_tilde(min(1 / delta, log(1 / delta) / rho) / alpha)` work. A mass-cap lemma proves that
every positive-violation batch is output-sized; the remaining acceleration
gap is specifically signed scratch and repeated exposure, not final support
size or a single high-degree positive batch.

The new benchmark includes fair direct APPR and priority-SOR baselines.  On
the deterministic sweep, forcing the optional tail costs about five times the
direct APPR work at equal accuracy; this rules out presenting the current
numerical discovery lanes as an end-to-end two-stage speedup.
At intermediate accuracy the adaptive mass lane has two strict wins on a
source-centered star (`570/3610` and `570/950` charged work). The direct
leakage implementation reproduces both wins but is expensive on general BFS
balls, confirming that proposal/reuse work is the remaining issue.

The arbitrary-graph existence theorem is therefore closed by randomized
threshold batches.  A deterministic/practical set-only reporter and a
persistent implementation that avoids fresh face rebuilding remain open,
while mass-envelope growth is still used only under a hard cap. The long
`aesp_cd_l1_rppr` note is preserved as
the proof audit and companion; it is not copied or shortened in place.
For review, [`CLAIM_TRACEABILITY.md`](CLAIM_TRACEABILITY.md) maps every strict
claim to its proof, executable audit, saved measurement, and scope exclusion.

Build with:

```bash
make -C manuscript/notes/two_stage_point_source_aesp_cd
```

The current full proof note is 40 pages. A separate 12-page short core
contains the randomized closure, the two continuation
theorems, the Green--CG lane, algorithm, experiments, and remaining
finite-precision problem is built with:

```bash
cd manuscript/notes/two_stage_point_source_aesp_cd
latexmk -pdf short_main.ltx
```

For the most aggressive reduction, the six-page strict support-first paper
removes the mass continuation entirely and keeps only Stage-I set certificates
plus one ordinary-PPR Stage II, including the randomized inner-face theorem:

```bash
cd manuscript/notes/two_stage_point_source_aesp_cd
latexmk -pdf strict_main.ltx
```
