# Independent literature review: semantic PPR and local RPPR

Checked 9 September 2026. This is a targeted novelty review, not a proof verification or a guarantee that no unpublished or unindexed work exists. The original repository and synced project sources were read only.

## Scope and assessment

The relevant project questions are OP1, an explicit sparse vector with degree-normalized semantic PPR error at most epsilon in graph-uniform work `O_tilde(1/(epsilon sqrt(alpha)))`; and OP2, additive objective approximation of the weighted l1-regularized PPR problem in `O_tilde(1/(rho sqrt(alpha)))`, with the objective tolerance and its logarithms stated separately. Both use point sources and connected simple undirected graphs in the canonical project model. ISTA lower bounds are outside the present scope.

**Assessment:** there is substantial prior research on these problems and their underlying geometry. This search did not identify an additional paper that, by its stated theorem alone, establishes either exact project contract uniformly over graphs and parameters. A publishable novelty claim should identify the joint dependence on teleportation, locality/accuracy, and fully charged graph access. Claims of being the first accelerated sparse method, the first local numerical solver, or the first M-matrix obstacle formulation would be incorrect. The two directly competing 2026 RPPR papers are being audited in a separate report.

The original COLT 2022 note, Section 3 (PDF p.3), discusses an acceleration question and motivates the inverse-square-root teleportation target. It does not present the project's later numbered list of three questions. Cite the project numbering as an organizational choice. [Fountoulakis–Yang, COLT 2022](https://proceedings.mlr.press/v178/open-problem-fountoulakis22a/open-problem-fountoulakis22a.pdf).

## Directly relevant predecessor omitted from the active prose

**Bai, Zhou, Yang, Xiao, _Faster Local Solvers for Graph Diffusion Equations_, NeurIPS 2024; arXiv:2410.21634v2, 22 December 2024.** Theorem 3.3 (PDF p.5) establishes semantic degree-normalized PPR accuracy using LocalSOR with `omega=1`, zero initial estimate, point-source residual, and `0<epsilon<=1/d_s`. Work is bounded by the minimum of `1/(alpha epsilon)` and a trajectory-sensitive active-volume/residual-ratio expression. Corollary 3.6 (p.6) supplies the analogous LocalGD bound. Theorems rely on nonnegative monotone residuals; this is not an unconditional accelerated-alpha result. Section 6 (p.10) explicitly records that the accelerated LocalSOR and LocalCH bounds remain unproved. Thus the paper supports local diffusion, implementation, and empirical acceleration precedents, but does not establish OP1 or optimize the RPPR objective of OP2. Its nonlazy teleportation convention must be converted before a numerical comparison. The existing bibliography contains `bai2024faster`, but the active related-work prose should cite and distinguish it. [Primary PDF](https://arxiv.org/pdf/2410.21634v2), [HTML](https://arxiv.org/html/2410.21634v2).

## Other close algorithmic predecessors

**Martínez-Rubio, Wirth, Pokutta, COLT 2023.** Table 1 (p.3), Theorems 4 and 8 distinguish an exact conjugate-direction solver, `O(k^3+kV)`, from accelerated approximate optimization, `O_tilde(k V_internal sqrt(L/alpha)+kV)`. Here `k=|supp(x*)|`, `V=nnz(Q_:,S*)`, and `V_internal=nnz(Q_S*,S*)`. These methods apply to symmetric positive-definite M-matrix quadratics over the nonnegative orthant. They already demonstrate accelerated sparse RPPR computation in useful parameter regimes. The extra support-cardinality factor means the displayed theorem is not the uniform OP2 target. The active manuscript already makes this distinction correctly. [Published paper](https://proceedings.mlr.press/v195/martinez-rubio23b/martinez-rubio23b.pdf).

**Zhou et al., _Iterative Methods via Locally Evolving Set Process_, NeurIPS 2024; arXiv:2410.15020.** The primary record states an APPR bound via average active volume and residual ratio and a Local Chebyshev acceleration result conditional on a trajectory's geometric mean residual reduction having square-root-alpha scale. This is a close precedent for cumulative active-volume accounting. The conditional trajectory quantity must not be silently treated as graph independent. The paper does not, from this guarantee, settle either project contract. [Primary record](https://arxiv.org/abs/2410.15020), [conference PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/fffe5a7804c40465ef2432386850c2c7-Paper-Conference.pdf).

**Huang, Luo, Xiao, Yang, Zhou, _Accelerated Evolving Set Processes for Local PageRank Computation_, NeurIPS 2025; arXiv:2510.08010v4.** Theorem 3.6 requires connected simple undirected graphs, `alpha<1/2`, point source, and `0<epsilon<1/d_s`; LocGD or LocAPPR inner solvers produce semantic degree-normalized error at most epsilon in `O_tilde(min(m/sqrt(alpha), R^2/(sqrt(alpha) epsilon^2)))`. The discussion immediately following the theorem says `R` is not universally bounded across configurations. It proposes simplex constraints or restart as possible controls. Consequently it supplies accelerated outer iterations and a closely related PPR guarantee, but not OP1's uniform inverse-linear epsilon work. It is also not an additive RPPR minimization theorem. Credit its mass-constraint suggestion where the new argument uses constrained acceleration. [Primary HTML, Theorem 3.6 and discussion](https://arxiv.org/html/2510.08010v4), [published record](https://proceedings.neurips.cc/paper_files/paper/2025/hash/946ecab300b0695fe24b53a92e632935-Abstract-Conference.html).

**Lin and Deng, _Faster Accelerated First-order Methods for Convex Optimization with Strongly Convex Function Constraints_, NeurIPS 2024.** Pages 1–3 introduce accelerated primal-dual methods and finite sparsity identification for minimizing an l1 objective subject to a strongly convex quadratic constraint, with PageRank as an application. Their displayed bounds concern iterations, objective/constraint error, and last-iterate convergence. Finite identification does not bound the cumulative adjacency work before identification. This is relevant constrained-optimization literature, but those statements do not give OP1/OP2. [Primary conference PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/8d8e060d9a3312ae12f42adf0da6ec7c-Paper-Conference.pdf).

## Same optimization geometry: important additional citations

**Chen, Peng, Wang, _2-norm Flow Diffusion in Near-Linear Time_, FOCS 2021; arXiv:2105.14629v2.** Equation (3) minimizes `x^T L x/2+d^T x` under `x>=0` on a weighted undirected graph, with total capacity nonnegative. Theorem 1.1 (arXiv PDF p.5; Theorem I.1 in the conference version) gives high-accuracy randomized work `O(m log^8(n) log(1/epsilon))`. The methods include constrained elimination, graph sparsifiers, and accelerated inexact proximal operations. This is a genuine obstacle-quadratic and flow-duality precedent. Its bound uses the whole input graph. Section 1.4 explicitly identifies strong locality with near-linear output-cluster dependence as a further direction. Mapping a grounded RPPR quadratic into this geometry does not supply the missing local discovery and boundary-accounting theorem. Add this source to the obstacle/flow discussion; do not claim that the optimization formulation or accelerated handling of inequality-constrained diffusion is new. [Primary arXiv PDF](https://arxiv.org/pdf/2105.14629v2), [conference PDF](https://ieee-focs.org/FOCS-2021-Papers/pdfs/FOCS2021-5stbVHiOp5jRHWlSl41FkR/205500a540/205500a540.pdf).

**Vladu, _Breaking the Barrier of Self-Concordant Barriers: Faster Interior Point Methods for M-Matrices_, STOC 2025; arXiv:2504.20619v1.** Theorem 2 (PDF p.4) gives additive objective approximation of `min_{x>=0} x^T A x/2-b^T x` for symmetric M-matrices using `O_tilde(n^(1/3))` predictor-corrector iterations. Corollary 3 (p.5) gives `O_tilde(n^(1/3) nnz(A) log(1/epsilon))` work, with additional condition-number and norm logarithms. RPPR's nonnegative formulation falls within this algebraic class. The algorithm initializes and maintains a full-dimensional positive interior point and invokes global matrix solvers. There is no stated support-sensitive discovery guarantee, so this theorem does not imply OP2. It should be acknowledged as a recent general M-matrix optimization result; the new local bound can coexist with this different global work/depth tradeoff. [Primary record](https://arxiv.org/abs/2504.20619), [Theorem 2 and Corollary 3](https://arxiv.org/html/2504.20619v1).

## Additional 2025–2026 sublinear linear-system and PageRank results

**Kwok, Wei, Yang, _On Solving Asymmetric Diagonally Dominant Linear Systems in Sublinear Time_, ITCS 2026; arXiv:2509.13891v2, 25 January 2026.** The published paper's Section 1.2 (physical p.4) asks for a scalar `t^T x*`, assumes known dimension and matrix/vector access, and permits theorem-specific sampling access. Theorem 4 (p.7) gives scalar error normalized by `||D_M^-1 b||_infinity` with constant success probability. Theorem 11 (p.9) gives an inverse-accuracy lower bound for estimating one coordinate of a well-conditioned SDD system under a different relative-to-solution-norm error. These results extend local linear-system estimation but neither enumerate a sparse PPR vector nor solve a nonnegative RPPR optimization. One cannot turn a scalar oracle into OP1 by uncharged calls over unknown targets. A short related-work distinction is sufficient. [Published PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/LIPIcs.ITCS.2026.89/LIPIcs.ITCS.2026.89.pdf), [latest full-version record](https://arxiv.org/abs/2509.13891).

**Feng, Li, Peng, _Sublinear-Time Algorithms for Diagonally Dominant Systems and Applications to the Friedkin–Johnsen Model_, arXiv:2509.13112v1, 16 September 2025.** The primary abstract specifies randomized estimation of a supplied coordinate under additive or solution-norm-relative error. For positive diagonal-dominance slack delta, one displayed additive bound is proportional to `||b||_infinity^2 S_max/(delta^3 epsilon^2)` with a logarithm. This is a further alternative-label hit for sublinear solvers, not a whole sparse vector or obstacle optimization result. Only the primary abstract was screened; no detailed theorem comparison is needed for the manuscript unless this line is discussed substantially. [Primary record](https://arxiv.org/abs/2509.13112).

**Thorup, Wang, Wei, Yang, _PageRank Centrality in Directed Graphs with Bounded In-Degree_, SODA 2026; arXiv:2508.01257v2, 3 January 2026.** The target is one node's PageRank centrality from a uniform initial source, in a directed graph, with constant relative error and constant success probability. The abstract fixes the stopping probability alpha as a constant, parameterizes graph degree limits, and assumes relevant sizes/bounds known. It develops a randomized backward propagation method. This is current PageRank complexity research, but neither the graph model, output, nor alpha-uniform contract matches OP1/OP2. [Primary record](https://arxiv.org/abs/2508.01257).

**Two additional 2026 PPR frontiers found and handed to the main reviewer:** Bertram–Jensen, [Personalized PageRank Estimation in Undirected Graphs, 2602.10843v1](https://arxiv.org/abs/2602.10843), and Jiang et al., [Near-Optimality for Single-Source Personalized PageRank, 2507.14462v5](https://arxiv.org/abs/2507.14462). Their current records were checked. Detailed graph/error/access reductions are assigned to the main reviewer to avoid duplicate work.

## Novelty language and action items

1. Include `bai2024faster` in the active comparison, explaining its proved unaccelerated bounds and open accelerated bound.
2. Add Chen–Peng–Wang and Vladu to the mathematical lineage. Grounded electrical-flow duality and M-matrix obstacle minimization are established geometry; the candidate novelty is local discovery, projection/energy arguments, and total charged work.
3. Keep the two new 2026 scalar-estimation papers in a short broader-frontier paragraph or the audit bibliography. They should not inflate the central comparison table as though their output contracts matched.
4. State precisely whether the new theorem concerns a custom accelerated method or standard FISTA. The original question's broad algorithmic target and its narrower classical-method motivation are distinct.
5. Use qualified wording such as: "We are not aware of an earlier theorem giving this joint graph-uniform dependence under the stated sparse-output and access model." The search cannot justify "no one else works on this problem."
6. The manuscript's proposed proof remains subject to independent verification. Literature novelty is not proof correctness, and an empirical result is not an unconditional work theorem.

## Search coverage and limits

Web search was performed on 9 September 2026 with primary-source follow-up on PMLR, arXiv, NeurIPS/OpenReview, ACM's STOC proceedings listing, Dagstuhl's ITCS proceedings, and the official FOCS paper server. Author publication pages were used as discovery aids. Secondary aggregators, social posts, and automatically generated descriptions were not used as evidence for mathematical conclusions. Obvious topic false positives (multilinear PageRank, centrality applications, M-matrix estimation, unrelated obstacle avoidance) were excluded.

Representative exact queries:

- `Fountoulakis Yang Running Time Complexity Accelerated l1 Regularized PageRank open problems 2022 conjecture`
- `"Accelerated Evolving Set Processes for Local PageRank Computation"`
- `"Iterative Methods via Locally Evolving Set Process"`
- `"PageRank" "2025" "accelerated" sparse complexity`
- `"regularized PageRank" "2026" -site:researchgate.net -site:reddit.com`
- `"PageRank" "local" "acceleration" "2026"`
- `"sparse" "M-matrix" optimization accelerated active set`
- `"PageRank" "lower bounds" "2026"`
- `"PageRank" "SODA 2026"`
- `"obstacle" "local" "nearly linear" algorithm graph`
- `"M-matrix" "output-sensitive" optimization`
- `"PageRank" "linear complementarity"`
- `"sublinear" "diagonally dominant" "2019"`
- `"accelerated" "regularized" "PageRank" after:2025-01-01`
- `"PageRank" "obstacle problem"`
- `"minimizing a quadratic function" "hard non-negativity"`
- `"2-norm flow diffusion" "near-linear"`

The initial remit included ISTA-specific lower bounds; after the user's scope clarification that branch was stopped and the review concentrated on semantic PPR/RPPR upper bounds. Search-result dates were not treated as publication dates; arXiv histories and venue records were preferred. No citation database offers complete coverage; recent preprints, differently named formulations, non-English work, private manuscripts, and changes after the check date remain possible. This review inspected statements and assumptions, not every proof in every paper.

Local evidence copies for the three most important newly classified predecessors are in `literature-evidence/`: `bai2024.pdf`, `chen2021.pdf`, and `vladu2025.pdf`, with extracted text for page checking. These are reference copies, not intended for the arXiv source package.
