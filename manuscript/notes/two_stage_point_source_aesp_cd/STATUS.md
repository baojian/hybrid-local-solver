# Direction status: two_stage_point_source_aesp_cd

Last reviewed: 2026-08-30

State: proved-open

## Exact question and contract

- **Question:** Can the long changing-face AESP-CD argument be replaced by an
  at-most-two-stage point-source algorithm that returns a certified numerical
  checkpoint immediately, or else screens a set and accelerates only once on
  that fixed set?
- **Model:** Finite simple undirected unweighted no-isolate graphs, one seed
  `s=e_v`, source-aligned `Q`, a declared split
  `rho+delta+tau<=eps_ppr`, adjacency-list access, and nested or fixed Stage-I
  envelopes.
- **Accuracy namespace:** The output satisfies the note-scoped semantic PPR
  target `||D^(-1/2)(x_hat-x^0)||_infinity <= eps_ppr`. RPPR regularization
  and ordinary restricted-PPR error consume declared parts of the semantic
  budget; no APPR-threshold equality is assumed except inside the declared
  APPR envelope engine.
- **Access and charged work:** Every exposure, repeated row scan, coordinate or
  batch update, response/reporter operation, certificate query, matrix
  application, state write, and output write is charged in degree work.
- **Intended result:** A concise screen-or-solve theorem: return immediately
  when Stage I has a certified numerical point, and otherwise pay
  `W_disc + O_tilde(vol(E)/sqrt(alpha))` for a set-only screen, or publish a
  lower-safe mass checkpoint and pay
  `O(mu(z)/(alpha eps_ppr))` for APPR/SOR cleanup; plus a fair certified
  portfolio and a precise reduction of the arbitrary-graph target to
  output-sensitive screening or mass capture.
- **Reduced artifacts:** the proof-oriented standalone note is 36 pages, the
  complete short paper is 10 pages, and the strict support-first theorem core
  is 4 pages.  The last version removes mass continuation and every
  changing-face Lyapunov/Perron argument.

## Claim ledger

- **Source:** RPPR nonnegativity, support volume, comparison to PPR, APPR
  support containment, AESP and SOR framework facts.
- **Proved here:** The approximate RPPR-envelope linearization lemma,
  the direct PPR boundary-leakage certificate and its residual-error-bar
  implementation,
  gap-to-output-sized-envelope conversion, mass-capped positive-batch bound,
  one-heap lower-safe positive-key handoff, direct positive-residual-mass
  contraction, unconditional priority-SOR Stage-I and direct-PPR bounds,
  the numerical-handoff early-return theorem, the adaptive hard-capped
  Green-ball set-only screen, tuned error-budget
  rule, three-budget composition theorem, exact-support-not-needed corollary,
  fair interruptible certificate race, the exact residual-mass cleanup
  identity, the mass-capturing-envelope AESP--APPR theorem, its unconditional
  hard-capped screen-or-fallback wrapper, the point-source rooted-ball mass
  bound, and the support-versus-potential handoff dichotomy.
  The APPR-snapshot exact-face race and the support-safe positive-residual
  SOR-to-one-solve lane give unconditional factor-two wrappers for literal
  exact-support attempts.  A successful Green envelope with a certified
  fixed-width order is solved in $O(w^3B)$ work; implemented tree and
  unicyclic elimination realizes the fixed-width claim rather than merely
  estimating it.
- **Conditional:** The arbitrary-graph target under a dynamic obstacle/reporter
  oracle with `W_DS(B)=O_tilde(B/sqrt(alpha))`; strict-margin exact-face
  identification; AESP-burn-in locality bounds.
- **Measured:** A new exact Fraction audit checks the PPR--RPPR comparison,
  linear sparse-source superposition and the joint-source RPPR obstruction,
  support-volume and face/envelope certificates on paths, cycles, stars, and
  brooms; all 192 coordinate subsets on three point-/multi-source cases; a
  rational proper-envelope linear tail; the gap-threshold envelope and its
  early numerical output;
  mass-capped positive exposure; positive-residual contraction on four graph
  families; direct priority-PPR; a signed-scratch Stieltjes lower retraction
  and its mass accounting; and fair scheduler accounting. A 252-lane
  deterministic diagnostic compares direct APPR/priority-SOR, a hard-capped
  set-only Green-ball lane, and four optional-tail envelope lanes on six graph
  families.  A separate 36-row oracle diagnostic measures the smallest rooted
  ball satisfying the exact and half-slack mass-capture triggers.  A second
  36-row executable benchmark runs the full hard-capped AESP/CG-retraction to
  priority-APPR lane and validates every final semantic error.  A third
  36-row adaptive variant uses priority-APPR-shaped envelopes and warm starts,
  reducing median overhead substantially.  A 54-row higher-accuracy extension
  gives two strict source-centered-star wins: `570/3610` at
  `(alpha,epsilon)=(0.01,0.005)` and `570/950` at `(0.04,0.005)`, while its
  median ratio remains one.  The star's source belongs to a two-dimensional
  invariant subspace, so the successful fixed solve takes exactly two matrix
  applications and no cleanup.  A separate 54-row direct boundary-leakage
  implementation certifies 44 envelopes and reproduces the two star wins,
  but has median ratio `7.52`; repeated geometric-ball solves are therefore
  correct but not competitive without response reuse.  The APPR-shaped
  two-heap leakage implementation switches in only 4 of 54 cases, has median
  ratio `1.061`, and preserves the two strict wins at `572/3610` and
  `572/950`; it is the literal monotone-discovery/fixed-CG two-stage lane.
  With the exact-tail split $\rho=\varepsilon$, the 90-row coarse-APPR
  exact-face race completes 19 nontrivial exact-support certificates before
  direct APPR and has four early-return fair wins (best ratio `0.132`); a
  separately charged fresh ordinary-PPR Stage II leaves two fair wins.  The
  positive-residual SOR support-discovery lane finishes before APPR in eight
  cases and has five strict fair-race wins, with best ratio `0.088`; all five
  survive a separately charged fresh ordinary-PPR Stage II.  The
  factor-reuse charge raises APPR and SOR standalone counts from 4 and 5 to 6
  and 7 while retaining the same 2 and 5 fair wins.  Reusable tree/unicyclic
  factors are now executable rather than only counted: one factorization is
  applied to both RPPR and PPR right-hand sides and checked against sparse
  direct solves on three named and 80 randomized structural systems.
  The large floating verifier now propagates its principal residual error bar
  through active-coordinate and boundary-KKT intervals; all three 90-row
  APPR/SOR/batch count tables remain unchanged under this stricter guard.
  An exhaustive randomized check enumerates 8,096 candidate faces on 36
  small tree/unicyclic systems: every false face is rejected and every exact
  support is certified.
  A 75-row
  large structural-tail sweep uses actual leaf peeling and
  cyclic-core elimination with the exact-tail budget tuned: 56 Green balls
  fit the cap, 50 beat direct PPR as standalone lanes, 35 remain strict wins
  with the fair APPR charge, and the median successful standalone ratio is
  `0.302`.
  A separate implementation of the exact rooted-tree threshold-message
  reporter certifies all 60 large path/star/binary/broom traces.  Of the 51
  cases with a nonzero direct-APPR baseline, the RPPR early-return version
  wins 27 standalone and 14 after a one-for-one APPR charge.  The literal
  set-only-then-PPR version has the same counts because its fixed solve
  replaces RPPR recovery and permits the full split $\rho=\varepsilon$.
  A further 1,890 randomized small-tree traces pass the independent global
  KKT verifier.
  A three-way promised-tree race between direct APPR, threshold messages, and
  structural Green retains 23 wins among 51 nontrivial cases even after the
  conservative three-way charge.
  The repeated exact positive-boundary baseline certifies 75 of 90 structural
  cases and finishes before APPR in 43; 13 early-return wins survive the fair
  charge.  Charging a fresh ordinary-PPR Stage II leaves 33 standalone and 8
  fair wins; retaining the final structural factors raises these to 37 and 9.
  Its 38 singleton path rounds record why this correct baseline is not a
  universal work theorem.
- **Refuted:** Treating APPR's output-sized envelope as an accelerated
  construction; transporting unguarded momentum across admissions; blind
  radius expansion; and repeated full restricted solves after singleton
  admissions as a universal product-scale proof.
- **Open:** General-graph output-sensitive point-source set-only screening or
  accelerated numerical discovery itself; exact-face
  identification without a finite KKT margin, and a larger implementation
  study of the certified portfolio. Exact zero-key decisions are unnecessary
  for the approximate-envelope main line.

## Central blocker

Construct or rule out an adjacency-local set-only boundary reporter with total
`O_tilde(B/sqrt(alpha))` work on every retained envelope of volume `B`.
Separately, improve the hard-capped mass lane on instances where a small
mass-capturing envelope exists; the star barrier rules out making that second
condition universal for the $\ell_\infty$ target.
The numerical fixed-envelope tail is no longer the blocker.  All current
concrete APPR, SOR, AESP-gap, and exact-response engines return enough values
to meet the PPR target already; forcing Stage II on them is redundant.
The Green-ball screen is a genuine set-only exception and is adaptively safe.
It had no win in the initial coarse 252-lane sweep, but the dedicated
high-accuracy sweep has 22 standalone and 15 fairly charged wins.  The
adaptive mass screen supplies two further high-accuracy star wins through a
different low-minimal-polynomial mechanism.  Neither observation is an
arbitrary-graph discovery theorem.

## Dependencies and reusable outputs

- **Formal registry dependencies:** `aesp_cd_l1_rppr` and
  `hybrid_aesp_locsor`.
- Source/shared prerequisites: the canonical source-aligned problem and the
  acceleration/local-solvers literature maps.
- Supplies to: a future short main paper, point-source solver prototypes, and
  any direction implementing the dynamic discovery oracle.
- Reusable outputs: the two certificate interfaces, envelope-linearization
  lemma, composition theorem, certificate-race wrapper, and paper-reduction
  map.

## Resume here

- Exact file/section/lemma: `main.tex`, especially
  `thm:two-stage-composition`, `thm:two-stage-certificate-race`, and
  `prob:two-stage-general-discovery`.
- Next concrete action: seek a genuinely cheaper set-only screen; separately,
  improve the adaptive mass lane using APPR-shaped rather than blind
  envelopes; replace the benchmark's offline lane
  selection by an interruptible shared-adjacency race for direct APPR and
  priority-SOR.
- Stop/go test: go if a new Stage-I engine returns a valid face/envelope
  certificate with every reporter charge explicit. Narrow or stop if the
  argument assumes the final support, hides global preprocessing, or treats a
  containing-radius ball as output-sensitive volume.

## Verification

- Source pointers checked: shared problem definition; acceleration,
  local-solvers, and graph-optimization literature notes; provider README,
  STATUS, and proof labels named in the manuscript.
- Focused build/checks run: all three standalone artifacts build; the exact
  audit and saved-result/semantic-error audit, their targeted fast-tier runner
  entries, registry consistency, Ruff, and
  `git diff --check` pass.  The repository-wide note inventory still reports
  two pre-existing provider sections above its source-line cap; neither file
  is in this direction's edit scope.
- Known gaps: no new arbitrary-graph accelerated screening theorem; the SOR
  lane is a direct nonaccelerated solver rather than an accelerated support
  engine; the fair race is exact-real unless each engine supplies its own
  finite-precision certificate.
