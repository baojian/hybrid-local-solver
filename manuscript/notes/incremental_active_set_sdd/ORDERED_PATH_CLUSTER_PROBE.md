# Ordered path clusters: implemented primitive and next integration audit

Date: 7 September 2026. The backend is **Proved here**, as a draft awaiting
independent review, and **Measured** by exact audits. The end-to-end local
tree bound is now **Proved here** as a draft in `thm:op3-local-top-tree`. Arbitrary-graph OP3 remains **Open**.
Proof authority: `sec:op3-ordered-path-clusters` in `main.tex`.

## Completed construction

Use the finite homogeneous chart `(X,Y,W)=(a_L,c,a_L+a_R)`, with
`0<=X/W<=1`, `Y/W<0`. It includes both endpoint strata. The upper chain
maximizes the normalized original gate; signs, rather than unnormalized
magnitudes, are preserved. The full positive projective pullback, orientation
proof and exact tie handling are in `lem:op3-compact-projective-pullback`.

Adjacent compression gives `u_M=eta*u_L+zeta*u_R+shift`, with positive
multipliers and negative shift. In the new chart, the right child occupies
`[0,eta/(eta+zeta)]`, and the left child occupies
`[eta/(eta+zeta),1]`. They therefore admit a separated merge, in right/left
order. One-port side clusters contribute one endpoint threshold; forgetting
the farther port uses an exact fractional extreme query. Original diagonal
and load are stored at cluster ports, subtracting one duplicate at a join.

`projective_hull_rope.py` implements immutable AVL sequences, whole-chain
homogeneous tags, exact orientation tests, separated bridges, splits, joins,
queries and retained versions. `lem:op3-persistent-projective-chain` charges
O(1) work and one root for a whole map; conservative O(log^3 N) work and
O(log^2 N) new nodes for a separated merge; and O(log^2 N) for a gate or
one-port query. The model counts exact real word operations, not rational
bit lengths or floating-point stability. Historical copies and unsuccessful
searches are included.

`path_cluster_reporter.py` implements edge, compress, one/two-port rake,
forget and final recovery records. Its driver supplies hierarchies and
rebuilds them for comparison; it is not an online local tree implementation.
All full-graph metadata, materialized reference hulls and dense solves live
in the audit driver and are excluded from algorithmic complexity claims.

Boundary ownership matters: keep one heap of inactive-child thresholds at
each active vertex and home only its minimum row on that vertex's permanent
parent edge. Home the seed's minimum on its first admitted edge. An admission
then changes one old edge payload and creates one new payload. Do not copy
a vertex's row to every incident edge. Original degrees remain fixed.

## Exact evidence

- `PROJECTIVE_HULL_ROPE_AUDIT.json`: 516 static-chain comparisons, 43,906
  retained-point checks, 360 extreme queries, 360 one-port queries, 96
  adjacent separation checks and 130 retained versions. Every tested whole
  map allocates exactly one root. Final audit: 45.204 seconds.
- `PATH_CLUSTER_REPORTER_AUDIT.json`: 423 source instances, every tree
  through seven vertices, every seed, three parameter pairs; 1,512 actual
  positive faces/admissions, 18,819 independent full Schur comparisons,
  29,278 boundary rows, 31,590 two-port queries, 8,289 one-port checks,
  74,400 recovered coordinates, 5,265 retained reparenthesized versions and
  1,040 one-port/one-port rakes. Final audit: 27.484 seconds.
- Five implicit canonical path/private-star cases through 128 positive
  vertices retain every boundary row on the upper chain. Report adjacency
  access is forbidden. Three parenthesizations agree exactly. At length
  128, balanced construction allocates 924 hull nodes, versus 3,585 for
  left association and 3,045 for right association. This measures supplied
  builds, not an online update theorem or an OP3 lower bound.

Final backend SHA-256:
`9efde237937cd5e37f46061d3d2ebeaa474f336e1131c81bc5bb5932a3e91d03`.
Cluster audit SHA-256:
`37411b1b5bcdd77db21e200522d0636a0ca369691a2d0e936429f234f0a19ab4`.

The prior AESP-CD `lem:aesp-cd-two-port-projective-pullback` and
`cor:aesp-cd-slope-separated-projective-meld` were read for provenance.
The present finite chart and implemented conservative bridge are proved
locally; no logarithmic meld black box is silently imported. The earlier
alternating-fan interleaving obstruction does not apply to adjacent-path
separation. Root-threshold stale-order obstructions remain valid.

## Source callback contract, now discharged

The published version was also checked in block 9: Theorem 2.1, journal
p. 247, interface pp. 245–248 and implementation pp. 259–260. The final
tree theorem imports that height-bounded version. The source pointers below
retain the original preprint audit history.

Primary source: Alstrup, Holm, de Lichtenberg and Thorup,
[Maintaining Information in Fully-Dynamic Trees with Top Trees](https://arxiv.org/pdf/cs/0310065v2),
TALG 1(2):243–264 (2005). Checked version: arXiv v2, 21 November 2003.
Read PDF pp. 4–8, Theorem 1 p. 6, exposure p. 25 and arbitrary-degree
implementation pp. 25–26. Definition, Figure 1, theorem and exposure were
also visually inspected. Source PDF/text are temporarily in
`/tmp/op3-top-trees-source.pdf` and `.txt`.

**Source:** edge-induced clusters meet at one vertex and have at most two
boundary vertices; logarithmic height and O(log n) joins/splits per link,
cut or expose, linear structural space. Link/cut reset external boundaries.
Source summary and publication metadata are recorded together in
`docs/literature/index.md` and `docs/literature/lcp-solvers.md`.

The following six obligations were discharged in
`sec:op3-local-top-trees` and `TOP_TREE_CALLBACK_AUDIT.json`. They are
retained here as the precise import checklist and original audit design:

1. Maintain only one active component plus the newly allocated isolated
   vertex. Root the mathematical tree permanently at the seed; store depth
   on admission. A source-free two-port cluster's ports must be comparable
   in this rooted tree: otherwise the exit toward the seed would be a third
   boundary. A valid one-port cluster has its rootward vertex as its port.
2. Store `contains_seed` in O(1) per cluster. If a temporary cluster has the
   seed in its interior, mark its algebraic summary unavailable; retain its
   structural children. Do not eliminate the positive source load. Source
   exposure splits all such clusters. A valid parent cannot contain an
   invalid child: an interior vertex of a child cannot become a boundary of
   its parent without a boundary-changing update, whose old clusters must
   first be split. Verify this formally against the source discipline.
3. Match every Figure 1 case. Two path children compress. A point/path join
   either rakes or rakes then forgets the farther shared port. Two point
   children either rake or create a zero-port whole-tree cluster, which is
   unavailable until seed exposure. A base edge may need immediate farther-
   port forgetting. All final exposed-seed clusters should be valid.
4. The source gives parent/child pointers and logarithmic height. A home-edge
   payload change can refresh its leaf and ancestors without changing the
   hierarchy, charging O(log n) summary recomputations. Confirm that
   boundary changes during the following link are separately recreated by
   source callbacks. Do not use a cut/relink shortcut that creates an extra
   source-free edge component and silently changes the rooting invariant.
5. Allocate vertex identifiers and incidence records only as discovered;
   structural high-degree handling must not add PageRank vertices or scan
   inactive rows. Singleton initialization is direct. Final recovery walks
   only the current hierarchy, not all retained historical roots.
6. Implement an exhaustive callback adapter audit: enumerate connected edge
   clusters and every legal binary join under exposed and unexposed seed,
   check the unavailable-state invariant, compare each valid summary with
   an independent Schur/boundary oracle, and test exposure/payload changes.
   This audits the application contract without claiming to implement the
   published balancing algorithm. A later genuine online implementation
   should be clearly distinguished from this adapter audit.

If every integration obligation is discharged, O(log |U|) changed cluster
records per admission times the O(log^3 |U|) primitive would give
O(cvol(U) log^4(2+cvol(U))) word work, with all old versions costing at most
O(cvol(U) log^3(2+cvol(U))) space. Exact positive-face locality gives
vol(U)<=2/eps_appr. This condition is now discharged for trees as a proof draft.
The source balancing algorithm is imported, not implemented by the exhaustive
audit. The next Open target is `UNICYCLE_TOP_TREE_PROBE.md`. A tree theorem
does not resolve arbitrary-graph OP3.
