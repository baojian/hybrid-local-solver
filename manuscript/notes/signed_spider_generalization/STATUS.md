# Direction status: signed_spider_generalization

Last reviewed: 2026-08-27
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
- **Intended result:** Establish the exact comparison bridge and fixed-face
  bipartite SOR theorem, identify the strongest already-proved spider/tree/
  bounded-block algorithms, and leave large cyclic cores explicitly open.

## Claim ledger

- **Source:** The standard strongly-convex FISTA recurrence and leaf-star
  locality obstruction are from Fountoulakis--Martínez-Rubio (2026).  The
  RPPR support-volume bound is part of the shared source-aligned formulation.
- **Proved here:** RPPR bias is at most `rho` in semantic PPR norm; objective
  gap `delta` contributes at most `sqrt(2 delta / alpha)`; on a known positive
  RPPR face, the problem is an ordinary shifted PageRank linear system.  For
  every fixed bipartite face, optimal red--black SOR has exact spectral factor
  `(1-t)/(1+t)` with `t=sqrt(1-rho_J^2)` and a finite Euclidean/semantic
  convergence bound.
- **Imported:** The exact spider-prefix spectrum comes from
  `volume_gated_acceleration`.  Exact kinetic response on hub-rooted spiders and
  exact aggregate response on rooted trees come from
  `propagate_settle_framework`.  The representation-free bounded-block
  response theorem comes from `delayed_reflection_ladder`.  The accelerated
  radial two-rung and finite-spider deflation theorems come from
  `two_rung_direct_theory` under their residual-gate namespace.
- **Conditional:** An SOR-only local theorem beyond a fixed face requires a
  charged support-discovery, state-transport, and semantic-stopping interface.
- **Measured:** None of the main claims is inferred from measurement.  The
  verifier checks the block-SOR algebra and spectral formulas numerically.
- **Refuted:** The existing SOR and FISTA star examples cannot be used as a
  direct performance ranking.  A small final support does not control FISTA's
  transient work, and a favorable fixed-face SOR rate does not pay for finding
  or changing that face.
- **Open:** A graph-uniform signed iterative solver on large biconnected cyclic
  cores with product-scale work and a local semantic certificate.

## Central blocker

Trees and bounded articulation blocks have scalar or bounded-dimensional
responses that can be maintained and charged.  A large nonequitable cyclic
core can change many boundary demands after one local update.  Neither a
fixed-face spectral rate nor exact final-support volume controls those
transient reports, state rewrites, or face changes.

## Dependencies and reusable outputs

- **Formal registry dependencies:** `signed_star_acceleration`,
  `volume_gated_acceleration`, `propagate_settle_framework`,
  `delayed_reflection_ladder`, and `two_rung_direct_theory`.
- **Context/provenance:** The user's SOR--FISTA comparability question and
  requested spider-first generalization motivate this note.
- **Reusable outputs:** The accuracy bridge, fixed-face equivalence, exact
  bipartite SOR factor, spider specialization, graph-family ladder, and staged
  falsification plan.

## Resume here

- **Exact pointer:** `sec:comparison-bridge` for the objective/accuracy bridge;
  `thm:fixed-bipartite-sor` for the new SOR theorem; and
  `sec:beyond-bounded-blocks` for the open general-graph interface.
- **Next action:** Prove or refute a windowed state-transport lemma on the
  smallest large-block family where one admitted coordinate changes many
  boundary demands, while retaining the fixed-face SOR energy bank.
- **Stop/go test:** Continue the SOR route only if face-change work is charged
  to new support, a telescoping energy shock, or a compressed response event;
  stop any proof that treats the next face as free or silently replaces
  semantic accuracy by a residual certificate.

## Verification

- **Focused checks:** `make` produced a 21-page PDF with no undefined
  references, citations, or overfull boxes; all pages were rendered and
  visually inspected.  `verify_spider.py` passed 80 SOR-mode cells, 144
  spider-spectrum cells, and 522 small-graph RPPR-bias cells.
  `verify_fixed_face.py` passed 570 cells: 60 exact rational parameter
  cells, 480 finite-power cells, and 30 spider-prefix cells.  Focused Ruff
  checking passed.
- **Repository checks:** `make note-audit`, `make agent-audit`, `git diff
  --check`, and all 210 tests passed on 2026-08-27.  Repository-wide `make
  lint` remains red on 1,345 pre-existing Ruff findings in checked-in
  `manuscript/claude-overnight-2026-08-24/` scripts; no reported finding is in
  this note or its verifier.
- **Known gaps:** Log-free radial semantic damping for plain optimal SOR is
  conjectural.  The end-to-end tree and bounded-block corollaries inherit the
  exact-real arithmetic and single-seed scopes of their proof-owning response
  theorems.  Large biconnected cyclic cores remain open.
