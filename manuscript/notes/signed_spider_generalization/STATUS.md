# Direction status: signed_spider_generalization

Last reviewed: 2026-08-28
State: proved-open

## Exact question and contract

- **Question:** In what mathematically legitimate sense are optimal signed SOR
  and standard RPPR FISTA comparable, and how far can the proved star
  acceleration mechanism be extended through spiders, trees, and cyclic
  graph classes?
- **Model:** The shared source-aligned undirected PageRank matrix `Q`.  SOR is
  analyzed on a fixed exposed bipartite principal face.  End-to-end structural
  corollaries use single-seed RPPR and ordinary adjacency-list access.
- **Accuracy namespace:** The final PPR target is
  `||D^(-1/2)(x_hat-x^0)||_infinity <= eps_ppr`.  RPPR regularization `rho`,
  fixed-face solve error `tau`, and objective gap `eps_obj` are kept distinct
  and connected only by proved conversion inequalities.
- **Access and charged work:** Every active adjacency scan costs degree, repeated sweeps
  are charged, support discovery and certification are charged when claimed,
  and final output writes are included.
- **Intended result:** Establish the exact comparison bridge, prove log-free
  plain SOR on the symmetric spider, carry its signed numerical state across
  a controlled sequence of bipartite faces, identify the strongest imported
  structural algorithms, and leave only the unpaid large-core interface open.

## Claim ledger

- **Source:** The standard strongly-convex FISTA recurrence and leaf-star
  locality obstruction are from Fountoulakis--Martínez-Rubio (2026).  The
  RPPR support-volume bound is part of the shared source-aligned formulation.
- **Proved here:** RPPR bias is at most `rho` in semantic PPR norm; objective
  gap `delta` contributes at most `sqrt(2 delta / alpha)`; on a known positive
  RPPR face, the problem is an ordinary shifted PageRank linear system.  On
  any supplied fixed face, a two-sided normalized residual at most
  `alpha*tau` implies semantic error at most `tau`; exact CG and interval
  Chebyshev therefore give the charged dispatch
  `O(vol(U) min{|U|, alpha^(-1/2) log(2/tau)})` under the stated single-seed
  load normalization.  Exact CG's dimension cap is an exact-real-arithmetic
  statement; the theorem does not discover or amortize changing faces.  For
  every fixed bipartite face, optimal red--black SOR has exact spectral factor
  `(1-t)/(1+t)` with `t=sqrt(1-rho_J^2)` and a finite Euclidean/semantic
  convergence bound when the face-specific tuning is supplied.  One
  graph-global parameter gives the generic fully charged fixed-face bound
  without computing `rho_J`.  A certified upper bound on `rho_J` gives a
  fully charged face-specific bound after adding `C_spec(U)`; constant-relative
  tuning through this rule needs squared-radius accuracy on the `t^2` scale,
  which can be `Theta(alpha)`.  A raw lower Rayleigh estimate is not a safe
  substitute.  Componentwise Collatz iterations provide a concrete safe
  upper certificate: their lower bounds rise and upper bounds fall, the
  aggregate relative-gap check licenses a frozen face parameter, and every
  iteration is charged as a full face scan.  Each fixed face eventually
  certifies for every fixed relative factor below one, but there is no
  graph-uniform scan count; a budget expiry safely falls back to the global
  parameter.  A complete face has spectral value one, so this estimator gives
  exactly the global parameter and no sweep benefit.  On every finite
  equal-arm hub-seeded spider,
  source-color-first plain SOR obeys the exact dimension-free envelope
  `zeta^k(1+2k(1-zeta))`, yielding log-free output-scale work.  A layered
  bipartite funnel proves that no graph-independent constant extends the
  corresponding exponential maximum-semantic envelope to all bipartite
  graphs.  Its seed output is
  `Theta(1/vol(G))`, so it also rules out graph-uniform
  `O(1/(sqrt(alpha) eps_ppr))` charged work for the literal complete-face
  source-first full-sweep plain-SOR schedule.  The propagation and work stop
  is uniform over arbitrary finite adaptive scalar relaxations that preserve
  the source-first color blocks, including exact eigenvalue advice.  A second
  source-distance theorem covers zero-start Chebyshev, CG/Krylov, heavy-ball,
  and variable Richardson recurrences whose vector operations are scalar
  combinations and complete sparse PageRank matvecs.  Dense eigenvector,
  inverse, Green-response, global-warm-start, and nonlocal-preconditioner
  operations are outside that theorem.  For nested
  fixed-load faces, zero-padding any nonsettled old iterate gives exact
  Pythagorean error splitting.  Combining this identity with the fixed-face
  power bound proves a supplied geometrically-growing-face continuation
  theorem at soft product scale.
- **Imported:** The exact spider-prefix spectrum comes from
  `volume_gated_acceleration`.  Exact kinetic response on hub-rooted spiders and
  exact aggregate response on rooted trees come from
  `propagate_settle_framework`.  The representation-free bounded-block
  response theorem comes from `delayed_reflection_ladder`.  The accelerated
  radial two-rung and finite-spider deflation theorems come from
  `two_rung_direct_theory` under their residual-gate namespace and parameter
  hypotheses `1 < B_rung < B_edge`, `B_rung R eps_ppr < 1`.
- **Conditional:** The continuation theorem assumes supplied nested bipartite
  faces and geometric volume growth.  An end-to-end SOR-only local theorem
  still requires a charged support-discovery, finite-band reporting, and
  semantic-stopping interface without repeated-prefix scans.
- **Measured:** None of the main claims is inferred from measurement.  The
  verifier audits the block-SOR algebra, radial wave recurrence, semantic
  envelope, bias bridge, and face-shock identity numerically, and audits the
  layered funnel transition, hitting time, discounted Green ratio,
  inverse-volume seed scale, and finite propagation in exact rational
  arithmetic.
- **Refuted:** The existing SOR and FISTA star examples cannot be used as a
  direct performance ranking.  A small final support does not control FISTA's
  transient work, and a favorable fixed-face SOR rate does not pay for finding
  or changing that face.  The sharp radial envelope fails on `P2` after one
  unswapped sweep when the source lies on the second color; swapping the color
  order restores the theorem.  Even with source-first order, the layered
  funnel refutes every graph-universal constant version of the radial
  maximum-semantic exponential envelope and stops product work for literal
  complete-face scalar-adaptive color-block SOR and source-polynomial
  complete-matvec recurrences.  An interleaved Gauss--Seidel permutation can
  reach the far layer in one coordinate pass, so the theorem counts color
  blocks or sparse-matvec dependency depth rather than an order-free word
  “sweep.”  It does not lower-bound nonlocal response methods.
- **Open:** A graph-uniform signed iterative solver on large biconnected cyclic
  cores with product-scale work and a local semantic certificate.

## Central blocker

Trees and bounded articulation blocks have scalar or bounded-dimensional
responses that can be maintained and charged.  Numerical SOR state can also
be transported across supplied geometrically growing bipartite faces.  What
remains is a large nonequitable cyclic core where singleton admissions can
force repeated old-face scans and change many boundary demands.  Neither a
fixed-face spectral rate nor exact final-support volume controls those
transient reports and state writes.  The layered funnel additionally closes
the simpler route that would repeatedly sweep the entire complete face and
hope for a graph-uniform maximum-semantic product bound.

## Dependencies and reusable outputs

- **Formal registry dependencies:** `signed_star_acceleration`,
  `volume_gated_acceleration`, `propagate_settle_framework`,
  `delayed_reflection_ladder`, and `two_rung_direct_theory`.
- **Context/provenance:** The user's SOR--FISTA comparability question and
  requested spider-first generalization motivate this note.
- **Reusable outputs:** The accuracy bridge, fixed-face equivalence, exact
  supplied-face CG/Chebyshev dimension--spectral dispatch with a two-sided
  semantic residual stop, bipartite SOR factor, log-free radial Chebyshev
  theorem, sweep-order witness,
  certified face-spectral cost and accuracy rule, charged a-posteriori
  Collatz certificate with safe fallback, layered graph-uniform
  envelope, adaptive scalar and source-polynomial work stops, nonsettled
  face-shock Pythagoras, conditional continuation theorem, graph-family
  ladder, and staged falsification plan.

## Resume here

- **Exact pointer:** `sec:comparison-bridge` for the objective/accuracy bridge;
  `thm:radial-semantic-damping` for the log-free spider theorem;
  `thm:global-semantic-sor-stop` and
  `cor:global-semantic-sor-work-stop` for the graph-uniform full-sweep stop;
  `prop:certified-face-spectral-cost` for paid face tuning and
  `prop:collatz-face-certificate` for its charged a-posteriori realization;
  `thm:supplied-face-dispatch` for the fixed-face CG/Chebyshev dimension--spectral
  rule and `lem:supplied-face-two-sided-stop` for its semantic certificate;
  `thm:adaptive-polynomial-propagation-stop` and
  `cor:adaptive-polynomial-work-stop` for the scalar-adaptive and
  Chebyshev/Krylov scope;
  `prop:windowed-sor-continuation` for supplied-face transport; and
  `sec:beyond-bounded-blocks` for the remaining interface.
- **Next action:** Build a finite-band KKT reporter on the smallest large
  bipartite core and prove that its events remove the geometric-volume gate,
  or preserve the first exact repeated-scan counterexample.
- **Stop/go test:** Continue the SOR route only if singleton face-change work
  is charged to new support, a packed finite-band crossing, or a compressed
  response event; stop any proof that treats boundary reports or repeated old
  rows as free.

## Verification

- **Focused checks:** `make` produced a 36-page PDF with no undefined
  references, citations, or overfull boxes.  `verify_spider.py` passed 80
  SOR-mode cells, 144 spider-spectrum cells, 14,616 radial-semantic cells, one
  exact sweep-order witness, seven exact layered-funnel cells, 522 small-graph
  RPPR-bias cells, and 132 face-shock cells.
  `verify_fixed_face.py` passed 570 cells: 60 exact rational parameter
  cells, 480 finite-power cells, and 30 spider-prefix cells.
  `verify_adaptive_spectral.py` passed 244 exact cells: 120 certified-tuning,
  98 componentwise Collatz/certification, 11 adaptive scalar-SOR, and 15
  Krylov/polynomial.  `verify_supplied_face_dispatch.py` passed 2,254 exact
  cells auditing the Chebyshev factor, shifted-load norm, M-matrix semantic
  conversion, and Krylov annihilator off-by-one.  Focused Ruff checking passed.
- **Repository checks:** `make note-audit`, `make agent-audit`, `git diff
  --check`, and all 210 tests passed on 2026-08-28.  Repository-wide `make
  lint` remains red on 1,345 pre-existing Ruff findings in checked-in
  `manuscript/claude-overnight-2026-08-24/` scripts; no reported finding is in
  this note or its verifier.
- **Known gaps:** The sharp radial theorem does not cover unequal arms,
  nonradial seeds, or online face discovery; the layered stop shows that no
  graph-universal constant-envelope extension can cover all bipartite graphs.
  The end-to-end tree and
  bounded-block corollaries inherit the exact-real arithmetic and single-seed
  scopes of their proof-owning response theorems.  Arbitrary singleton
  admissions, their finite-band reporter, and large biconnected cyclic cores
  remain open.
