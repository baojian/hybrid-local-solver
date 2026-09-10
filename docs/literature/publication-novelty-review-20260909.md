> Supplement: the later [August–September arXiv sweep](arxiv-aug-sep-audit-20260909.md) records explicit enumeration and adds two cited theoretical papers. The assessment below describes the earlier targeted review.

# Novelty review for local PageRank acceleration

## 1. Finding and publication recommendation

The searched literature contains substantial work on local PageRank, sparse accelerated optimization, active-set methods, graph diffusion, and M-matrix obstacle problems. This review did **not identify an earlier theorem with the same unconditional, graph-uniform work guarantee and the same output and access contracts** as the manuscript's proposed results. That finding supports proceeding with a carefully positioned preprint. It is not a guarantee that no equivalent work exists, a priority certificate, or a proof of mathematical correctness.

This review covers two project questions: OP1 asks for a sparse personalized PageRank (PPR) vector with degree-normalized solution error; OP2 asks for additive objective approximation of regularized personalized PageRank (RPPR). OP1 is established as a corollary of OP2 through a regularization-bias and objective-error conversion. These are two output guarantees from the RPPR algorithms, not two independently developed algorithmic breakthroughs. The labels OP1 and OP2 belong to this project; the COLT 2022 source poses an acceleration question without this numbered pair. [1: COLT 2022, Section 3](https://proceedings.mlr.press/v178/open-problem-fountoulakis22a/open-problem-fountoulakis22a.pdf)

The reviewed manuscript, *Accelerated Local Algorithms for Personalized and Regularized PageRank*, contains 41 pages and 29 cited references. It presents deterministic and randomized RPPR algorithms and explicitly derives the PPR guarantee. The title and introductory framing distinguish both contracts while preserving their mathematical dependency and stated graph scope.

### The precise contribution to assess

| Result | Manuscript guarantee | Important qualification |
|---|---|---|
| Deterministic RPPR | O~(1/(ρ√α)) fully charged work | Custom continuation and constrained accelerated recurrence |
| Randomized RPPR | O~(V* min{k*, α^(-1/2)}) expected work | Las Vegas; every accepted support admission is certified |
| Semantic PPR | O~(1/(ε√α)) work | Degree-normalized maximum error; follows by explicit conversion |
| Bounded arithmetic | Same soft local operation count; explicit encoding factors | A specified directed-rounding implementation |

Here α is teleportation, ρ is regularization, ε is PPR accuracy, k* is optimal-support cardinality and V* is its original-degree volume. Objective accuracy is a separate RPPR parameter, entering logarithmically. O~ hides permitted polylogarithms, not an arbitrary subpolynomial overhead.

**Recommendation:** retain the combined manuscript and its explicit predecessor comparisons, state the novelty as a joint work-and-model result, and avoid broad “first accelerated method” or “uniformly optimal” language. The updated local submission package is ready. Upload was blocked by an administrative browser-security verification failure, so no arXiv submission was completed during this preparation.

<!-- pagebreak -->

## 2. Contracts that make comparisons meaningful

The main graph is finite, connected, simple, undirected and unweighted, with at least two vertices. The input seed is one vertex v. Let A be adjacency, D the diagonal matrix of original degrees, and L the symmetric normalized Laplacian. The manuscript uses the lazy operator and objective

> Q = αI + (1−α)L/2; b = αD^(-1/2)e_v; Fρ(x) = x^TQx/2 − b^Tx + αρ‖D^(1/2)x‖₁.

For 0 < α ≤ 1, Q has spectrum in [α,1]. Write xρ* for the RPPR minimizer, x0* = Q⁻¹b for the unregularized solution, and π = D^(1/2)x0* for its probability vector. Original degrees must remain in every principal system: replacing them with induced-subgraph degrees changes the target.

**OP2.** Given ρ and a separate objective tolerance εobj, return a sparse xhat satisfying Fρ(xhat) − Fρ(xρ*) ≤ εobj in O~(1/(ρ√α)) work. The nonzero regime is ρ < 1/d_v. The deterministic theorem also gives 0 ≤ xhat ≤ xρ* and output support volume at most 1/ρ. If ρ ≥ 1/d_v, the exact zero optimum is recognized using one degree query.

**OP1.** Return a sparse probability-vector approximation πhat with ‖D⁻¹(πhat−π)‖∞ ≤ ε in O~(1/(ε√α)) work. This is an absolute error per unit target degree. It differs from ordinary absolute error, relative error on significant coordinates, one-node estimation, and a residual stopping tolerance.

**Conversion.** The RPPR KKT conditions and inverse positivity give 0 ≤ x0*−xρ* ≤ ρD^(1/2)1. Strong convexity bounds the optimization contribution by √(2εobj/α). Thus choosing ρ = ε/2 and εobj = αε²/8 establishes OP1, with output support volume at most 2/ε. This implication is explicitly proved in the manuscript; it is not obtained by identifying two tolerance symbols.

### Access, randomness and numerical work

The graph is learned from the seed through degree replies and adjacency entries. Every first or repeated row scan, scalar operation, state access, boundary update, certificate, materialization and output word is charged. The algorithm receives no containing region, optimal support, inverse oracle, or graph-wide preprocessing. Iteration count and output sparsity alone do not establish the desired work bound.

The baseline model is exact-real algebraic word work. A separate rational-input result controls integer lengths and gives bit cost O~(B²/(ρ√α)), with B including parameter, precision, encountered-label and degree encodings. This does not assert stability of an arbitrary floating-point implementation. Randomized bounds must retain their expected-work and failure qualifications.

For comparison with a nonlazy parameter a, use a = 2α/(1+α) and x = D^(1/2)y. Then Fρ(D^(1/2)y) = (1+α)ψρ(y)/2. The regularizer is unchanged; objective tolerances change by a constant factor. An ACL nonnegative-residual certificate implies semantic degree-normalized error, but a general two-sided semantic error bound does not imply the ACL residual representation. These distinctions control the comparisons on the next pages.

<!-- pagebreak -->

## 3. The two closest 2026 RPPR papers

### Fountoulakis and Martínez-Rubio: classical acceleration

*Complexity of Classical Acceleration for l1-Regularized PageRank*, arXiv 2602.21138. The latest version listed at review was **v2, submitted 8 April 2026**; v1 was submitted 24 February. The 29-page v2 adds the negative FISTA development absent from the 23-page v1. Version dates come from arXiv history, not a generated PDF or HTML date. [2: Record and history](https://arxiv.org/abs/2602.21138)

Theorem 4.3, physical PDF page 6, studies FISTA on the over-regularized objective F₂ρ. It assumes that all spurious activations lie in a fixed boundary set B and gives

> O((1/(ρ√α)) log(α/εobj) + √vol(B)/(ρα^(3/2))).

Theorem 4.4 supplies a graph-structural sufficient condition for this confinement. Proposition D.4, page 22, gives fixed-α star examples with FISTA work at least 2m at sufficiently small objective tolerance, while ISTA work is independent of m. The negative result concerns a particular classical recurrence, not the existence of any accelerated local algorithm. [2: v2, Theorems 4.3-4.4 and Appendix D](https://arxiv.org/pdf/2602.21138v2)

The manuscript should credit the two-regularizer comparison: using a less regularized optimum as an analytical core gives a uniform margin outside it without assuming a global minimum slack. The candidate new step is the diffuse-source constrained recurrence, its second metric comparison and its unconditional cumulative-work estimate. The new theorem does not overturn the FISTA counterexample or show that standard FISTA maintains small supports.

### Wei and Yang: nearly-linear solves on growing active sets

*A Simple Active-Set Method for PageRank-Based Local Graph Clustering*, arXiv 2608.16339. The latest listed version at review was **v1, submitted 17 August 2026**, 17 pages. Theorem 1.2, page 3, gives randomized ACL ε approximation in O~(ε⁻²) work, with numerical and failure logarithms and support volume at most 2/ε. [3: Record](https://arxiv.org/abs/2608.16339)

Theorem 1.3, pages 3-4, gives additive RPPR objective accuracy with an ACL 2ρ certificate and work O~(k*V*) ≤ O~(ρ⁻²). Each growing active set is processed with an SDD solver. The stated success probability is at least 1−δ. The deterministic-solver remark on page 4 allows deterministic substitution with an additional k*^(o(1)) factor. Therefore deterministic predecessors exist, and the new paper must not claim mere determinism as its novelty. Section 6 identifies reuse across nested systems as a further direction. [3: v1, Theorems 1.2-1.3](https://arxiv.org/pdf/2608.16339v1)

The manuscript's randomized bound O~(V* min{k*,α^(-1/2)}) retains their small-support branch while adding an accelerated depth branch. The new contribution is the number of locally discovered systems requiring a solve, not the underlying supplied-face SDD primitive. The deterministic construction uses a different route and avoids the almost-linear deterministic-SDD overhead.

Neither 2026 theorem, as stated, supplies the same unconditional joint target. Neither is uniformly dominated: ignoring logarithms, ρ⁻² is smaller than 1/(ρ√α) when ρ > √α. The support-adaptive minimum is the appropriate comparison, rather than a universal speed or optimality claim.

<!-- pagebreak -->

## 4. Closely related algorithms and optimization geometry

**Sparse acceleration already exists.** Martínez-Rubio, Wirth and Pokutta's COLT 2023 paper gives an exact conjugate-direction algorithm with O(k*³+k*V*) work and an accelerated approximate method with O~(k*Vinternal/√α+k*V*) work in the normalized RPPR case. Internal matrix nonzeros and original-degree volume are distinct. These results establish accelerated sparse optimization in useful regimes; the extra support-discovery factor prevents their stated worst-case bound from giving OP2. [4: Theorems 4 and 8](https://proceedings.mlr.press/v195/martinez-rubio23b/martinez-rubio23b.pdf)

**Local diffusion precedents should be named.** Bai, Zhou, Yang and Xiao's *Faster Local Solvers for Graph Diffusion Equations* (NeurIPS 2024) proves semantic PPR bounds for LocalSOR with ω=1 and LocalGD, with an inverse-α envelope and a trajectory-sensitive alternative. Theorem 3.3 is on page 5 and Corollary 3.6 on page 6. Section 6, page 10, explicitly leaves the accelerated LocalSOR/LocalCH work bounds unproved. It provides direct implementation and local-diffusion precedents but no unconditional OP1 acceleration theorem. [5: 2410.21634v2](https://arxiv.org/pdf/2410.21634v2)

Zhou et al.'s *Iterative Methods via Locally Evolving Set Process* (NeurIPS 2024) makes cumulative active-volume accounting central and analyzes accelerated local recurrences using trajectory-dependent residual reduction. Such a quantity cannot silently be treated as a graph-independent constant. Its role is methodological lineage and a distinct conditional guarantee. [6: Primary record](https://arxiv.org/abs/2410.15020)

Lin and Deng's NeurIPS 2024 constrained-optimization paper uses PageRank as an application and proves accelerated iteration and finite sparsity-identification guarantees. Its strongly convex constraint and l1 objective differ from the RPPR presentation, and finite identification does not bound total adjacency work before identification. [7: Primary paper, pages 1-3](https://proceedings.neurips.cc/paper_files/paper/2024/file/8d8e060d9a3312ae12f42adf0da6ec7c-Paper-Conference.pdf)

**AESP is particularly close to OP1.** Huang et al.'s *Accelerated Evolving Set Processes for Local PageRank Computation* (NeurIPS 2025), Theorem 3.6, gives semantic error ε with work O~(min{m/√α, R²/(√α ε²)}), for its stated point-source and parameter regime. The following discussion says that R is not universally bounded and proposes simplex constraints or restarts. The manuscript should credit both accelerated local outer iterations and this mass-control suggestion; the candidate contribution is a different proof of the inverse-linear locality scale. [8: Theorem 3.6 and discussion](https://arxiv.org/html/2510.08010v4)

### The nonnegative quadratic and flow viewpoint are established

Chen, Peng and Wang's *2-Norm Flow Diffusion in Near-Linear Time* (FOCS 2021) gives randomized high-accuracy optimization for a graph-Laplacian obstacle quadratic using constrained elimination, sparsification and accelerated proximal ideas. Theorem 1.1, page 5, has whole-graph work O(m log⁸(n) log(1/ε)). Section 1.4 lists strong locality as a further direction. A grounded RPPR formulation does not by itself inherit local discovery or boundary-accounting guarantees from that global solver. [9: 2105.14629v2](https://arxiv.org/pdf/2105.14629v2)

Vladu's *Breaking the Barrier of Self-Concordant Barriers: Faster Interior Point Methods for M-Matrices* (STOC 2025) treats the same algebraic class of nonnegative symmetric M-matrix quadratics. Theorem 2 and Corollary 3 give a global algorithm with work O~(n^(1/3) nnz(A) log(1/ε)), including further norm/condition logarithms. It maintains full-dimensional numerical state and has no stated optimal-support discovery bound. This is an important general optimization predecessor, not an OP2 solution. [10: Theorem 2 and Corollary 3](https://arxiv.org/html/2504.20619v1)

These citations prevent novelty from being assigned to established obstacle geometry, flow duality, acceleration, or sparse active sets. The candidate novelty lies in the stated combination of certified local discovery, the new inequalities and the resulting total work.

<!-- pagebreak -->

## 5. Broader PPR complexity, including further 2026 work

**Degree-normalized SSPPR predates this manuscript.** Wei, Wen and Yang's *Approximating Single-Source Personalized PageRank with Absolute Error Guarantees* (ICDT 2024) includes SSPPR-D sparse output. Appendix D, Theorem 20, displays O~(√(Σt π(s,t)/d(t))/εd) query work. However, Section 1.4's parameter remark restores linear dependence on 1/α when α varies, and Appendix D's RBS setup assumes Θ(m) preprocessing. This is a relevant accuracy-match predecessor, but its stated preprocessing and α dependence do not give OP1's fully charged graph-uniform target. Cite it rather than implying that degree-normalized sparse PPR itself is new. [11: Primary full text](https://arxiv.org/html/2401.01019v1), [11: published record](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICDT.2024.9)

**Undirected estimation frontier.** Bertram and Jensen's *Personalized PageRank Estimation in Undirected Graphs*, arXiv 2602.10843v1 (11 February 2026), fixes α as a constant and uses thresholded relative/additive error for per-target PPR estimates. Equation (2) does not divide error by target degree. Theorem 4.2.2 gives an Ω(min{m,1/δ}) lower bound averaged over a uniform source, in a query model permitting optional stronger access. The hard instances and accuracy contract require a separate reduction before they constrain this paper's connected, degree-normalized task. It is relevant current work, but does not assert OP1 or OP2. [12: Primary full text](https://arxiv.org/html/2602.10843v1)

**Near-optimal SSPPR lower bounds.** Jiang, Liu, Luo and Xiao's *Near-Optimality for Single-Source Personalized PageRank* is listed as PACMMOD 4(2), Article 110 (2026), DOI 10.1145/3801906, and associated with PODS 2026. The checked arXiv v5 is dated 12 April 2026. Definitions 1.1-1.2 fix α and error/failure constants; the main lower-bound table concerns directed graphs and ordinary maximum absolute or thresholded relative error. These are substantial whole-vector lower bounds, but they do not directly establish an inverse-α or degree-normalized lower bound for OP1. [13: v5](https://arxiv.org/html/2507.14462v5), [13: publication DOI](https://doi.org/10.1145/3801906)

**Scalar estimation is a different output task.** Kwok, Wei and Yang's *On Solving Asymmetric Diagonally Dominant Linear Systems in Sublinear Time* (ITCS 2026; 2509.13891v2) estimates a scalar t^Tx*, under stated matrix/vector and sometimes sampling access. Its error norms and constant success probabilities are explicit. Repeated calls over unknown targets do not produce a sparse whole-vector guarantee for free. [14: Published paper, Section 1.2 and Theorem 4](https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/LIPIcs.ITCS.2026.89/LIPIcs.ITCS.2026.89.pdf)

Thorup, Wang, Wei and Yang's *PageRank Centrality in Directed Graphs with Bounded In-Degree* (SODA 2026; 2508.01257v2) studies one node's global centrality, with fixed stopping probability and directed degree parameters. Wang et al.'s *Revisiting Local Computation of PageRank: Simple and Optimal* (STOC 2024) studies contribution and single-node tasks. Both belong in a broader frontier discussion, not the same-output RPPR comparison table. [15: SODA 2026 record](https://arxiv.org/abs/2508.01257), [16: STOC 2024 record](https://arxiv.org/abs/2403.12648)

Feng, Li and Peng's 2025 sublinear diagonally dominant solver was also screened at abstract level; it targets supplied-coordinate estimates. That limited screening is recorded as such, rather than presented as a full proof comparison. [17: 2509.13112](https://arxiv.org/abs/2509.13112)

<!-- pagebreak -->

## 6. Contribution map and proof-review boundary

The active manuscript's deterministic result is supported by a full proof chain, not just promising experiments. This review read the main deterministic recurrence, the two comparison energies, cumulative volume, stage repair and the exact threshold reporter; it also read the randomized block-depth proof. No gap was identified in that bounded internal review. A fresh run of the existing independent proof-identity suite passed 21 tests. These checks are neither external peer review nor a formal proof certificate, and not every auxiliary appendix argument was reconstructed afresh.

### Deterministic method: the candidate new chain

Regularization continuation maintains a safe baseline x̄ and diffuse source h = b−Qx̄ with 0 ≤ h ≤ 4αrω, where ω = √d. The correction optimum and the analytical comparator Q⁻¹h both lie in an explicit box and mass cap. The algorithm does not query either unknown comparator.

The same accelerated recurrence has a Euclidean energy controlling objective gap and a Q-metric comparison controlling its squared matrix response. The second projection inequality is valid for one specific analytical comparator; it is not a claim that arbitrary Euclidean projections are nonexpansive in the Q metric. The signs of the box normals and the identity Qω = αω make the comparison work.

The support of the less regularized optimum at r/2 supplies an analytical core of volume at most 2/r. A selected signed-flow telescope, retaining forcing only on actually selected coordinates, bounds cumulative repeated kinetic volume by 76K/r for K exact iterations. A deterministic finite breakpoint reporter, charged source exceptions and final materialization then turn that estimate into actual local work. Certified downward repair closes the continuation induction. Earlier unsuccessful FISTA, CG or AESP hybrid routes are not premises of this proof.

### Randomized method: the candidate new chain

Support-safe active sets and supplied-matrix SDD solvers have clear predecessors. The additional depth proof orders the unknown optimum support into threshold batches, truncates an analytical Cholesky factor to adjacent blocks, and obtains a well-conditioned block chain. Chebyshev inverse decay and causal threshold forcing bound the number of full numerical faces. The algorithm does not construct that full unknown-support factorization. Each accepted admission is locally certified; failed numerical calls are retried. The paper's expected-work statement counts rebuilding rather than assuming a free persistent inverse.

### What should remain outside the claim

No universal lower bound or joint optimality theorem is established. The standard-FISTA locality counterexample remains intact. The main result is restricted to unit-weight, single-seed graphs; separate multi-source extensions have explicit input costs. The paper asserts no matched empirical speed advantage and no ordinary floating-point stability theorem. The stopped weighted-prototype polishing regression is not needed for the complete theorem and should not be described as fully audited.

The two deterministic development records document development plus independent review of one core argument, not two independent discoveries. The original randomized proof is in the active-edge/LCP note. Preserving this provenance and the human-author/AI-assistance disclosure avoids overstating independence. OP3 and further questions about reuse of nested SDD systems remain outside this publication's two-question scope.

<!-- pagebreak -->

## 7. Defensible wording, search coverage and release status

### Suggested manuscript language

“We give deterministic and randomized local algorithms attaining the stated accelerated work target for regularized PageRank. An explicit regularization-bias argument yields the corresponding degree-normalized PPR guarantee. To the best of our knowledge, no earlier theorem gives this same joint graph-uniform dependence under the stated sparse-output and fully charged local-access model.”

This wording should be tied to the displayed formulas, point-source graph class and numerical model. The strongest defensible conclusion is about the reviewed theorem contracts. Avoid “nobody else has worked on this problem,” “first accelerated sparse PageRank method,” “first deterministic active-set method,” “all classical acceleration conjectures are solved,” and “optimal in all regimes.” Those statements exceed the evidence or conflict with identified precedents.

### Coverage of the present search

The review combined a focused audit of the two principal 2026 papers, an independent broader literature search, a check of recent SSPPR lower-bound/estimation work, and a local claims audit. Primary-source follow-up covered arXiv version histories, PMLR/COLT, NeurIPS, Dagstuhl/ITCS/ICDT, official FOCS proceedings and ACM venue metadata. Author publication pages were discovery aids. Substantive comparisons used papers and their explicit theorem assumptions, not secondary summaries or citation counts.

Query families included exact paper titles and identifiers; local or regularized PageRank with acceleration, active sets, support safety and 2026; sparse M-matrix optimization; obstacle and flow diffusion with near-linear or output-sensitive work; sublinear diagonally dominant systems; and recent PageRank lower bounds. Representative recency searches included “PageRank local acceleration after:2026-08-01 before:2026-09-10” and “accelerated regularized PageRank after:2025-01-01.” Exact search logs and version fingerprints are preserved in the companion audits.

Version identity and the main contracts of the closest papers have strong primary-source support. Coverage of every possible equivalent antecedent is necessarily less certain. Recent unindexed uploads, private manuscripts, differently named formulations, accepted but unavailable papers, non-English work and changes after 9 September remain possible. Some citation API and publisher-page requests failed; no verified citation-count claim is made. Abstract-only screening is explicitly distinguished from theorem-level review.

### Release and verification record

The final manuscript has **41 pages and 29 references**. Its 23-member source archive compiled independently and produced identical extracted PDF text. Final SHA-256 fingerprints are PDF `4cbc8e8906b21ce025153bd36b39957a394bbfeff22bf00034b2e6910cf4764d` and archive `ed146f90157872814e9427f558467cf099280a8ef73e5bcc7bf9a2af2f61bfd0`. The build record and all-page visual review passed.

The repository suite reported **231 passes and the same three historical failures** in unchanged older notes. Two pre-existing lint issues remain in older scripts. The focused mathematical identity suite passed all 21 tests. These checks support reproducibility; they do not replace proofs.

**The local package is ready; no upload was completed.** The browser reported that an admin-enforced security policy could not be verified before arXiv access. This access blocker is separate from manuscript readiness. The human author retains responsibility for the mathematics and submitted text.

Detailed records: *claims_audit.md*, *literature_2026.md*, *literature_independent.md* and *build-verification.json*. Reference PDFs are research evidence and are excluded from the source archive.

<!-- pagebreak -->

## 8. Sources

Primary sources are numbered in order of discussion. Page and theorem pointers appear beside the substantive comparisons above; URLs below resolve to the original publication or versioned preprint. The report's search cutoff is 9 September 2026.

1. K. Fountoulakis and S. Yang (2022). *Open Problem: Running Time Complexity of Accelerated l1-Regularized PageRank*. COLT. [https://proceedings.mlr.press/v178/open-problem-fountoulakis22a.html](https://proceedings.mlr.press/v178/open-problem-fountoulakis22a.html)

2. K. Fountoulakis and D. Martínez-Rubio (2026). *Complexity of Classical Acceleration for l1-Regularized PageRank*. arXiv 2602.21138v2. [https://arxiv.org/abs/2602.21138v2](https://arxiv.org/abs/2602.21138v2)

3. Z. Wei and M. Yang (2026). *A Simple Active-Set Method for PageRank-Based Local Graph Clustering*. arXiv 2608.16339v1. [https://arxiv.org/abs/2608.16339v1](https://arxiv.org/abs/2608.16339v1)

4. D. Martínez-Rubio, E. Wirth and S. Pokutta (2023). *Accelerated and Sparse Algorithms for Approximate Personalized PageRank and Beyond*. COLT. [https://proceedings.mlr.press/v195/martinez-rubio23b.html](https://proceedings.mlr.press/v195/martinez-rubio23b.html)

5. J. Bai, B. Zhou, D. Yang and Y. Xiao (2024). *Faster Local Solvers for Graph Diffusion Equations*. NeurIPS; arXiv 2410.21634v2. [https://arxiv.org/abs/2410.21634v2](https://arxiv.org/abs/2410.21634v2)

6. B. Zhou, Y. Sun, R. Babanezhad Harikandeh, X. Guo, D. Yang and Y. Xiao (2024). *Iterative Methods via Locally Evolving Set Process*. NeurIPS. [https://arxiv.org/abs/2410.15020](https://arxiv.org/abs/2410.15020)

7. Z. Lin and Q. Deng (2024). *Faster Accelerated First-order Methods for Convex Optimization with Strongly Convex Function Constraints*. NeurIPS. [Primary conference PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/8d8e060d9a3312ae12f42adf0da6ec7c-Paper-Conference.pdf)

8. B. Huang, L. Luo, Y. Xiao, D. Yang and B. Zhou (2025). *Accelerated Evolving Set Processes for Local PageRank Computation*. NeurIPS; arXiv 2510.08010v4. [https://arxiv.org/abs/2510.08010v4](https://arxiv.org/abs/2510.08010v4)

9. L. Chen, R. Peng and D. Wang (2021). *2-Norm Flow Diffusion in Near-Linear Time*. FOCS; arXiv 2105.14629v2. [https://arxiv.org/abs/2105.14629v2](https://arxiv.org/abs/2105.14629v2)

10. A. Vladu (2025). *Breaking the Barrier of Self-Concordant Barriers: Faster Interior Point Methods for M-Matrices*. STOC. [https://arxiv.org/abs/2504.20619v1](https://arxiv.org/abs/2504.20619v1)

11. Z. Wei, J.-R. Wen and M. Yang (2024). *Approximating Single-Source Personalized PageRank with Absolute Error Guarantees*. ICDT. [https://doi.org/10.4230/LIPIcs.ICDT.2024.9](https://doi.org/10.4230/LIPIcs.ICDT.2024.9); checked full version [2401.01019v1](https://arxiv.org/abs/2401.01019v1).

12. C. Bertram and M. V. Jensen (2026). *Personalized PageRank Estimation in Undirected Graphs*. arXiv 2602.10843v1. [https://arxiv.org/abs/2602.10843v1](https://arxiv.org/abs/2602.10843v1)

13. X. Jiang, H. Liu, S. Luo and X. Xiao (2026). *Near-Optimality for Single-Source Personalized PageRank*. PACMMOD 4(2), Article 110; PODS 2026. [https://doi.org/10.1145/3801906](https://doi.org/10.1145/3801906); checked full version [2507.14462v5](https://arxiv.org/abs/2507.14462v5).

14. T. C. Kwok, Z. Wei and M. Yang (2026). *On Solving Asymmetric Diagonally Dominant Linear Systems in Sublinear Time*. ITCS. [https://doi.org/10.4230/LIPIcs.ITCS.2026.89](https://doi.org/10.4230/LIPIcs.ITCS.2026.89); full version [2509.13891v2](https://arxiv.org/abs/2509.13891v2).

15. M. Thorup, H. Wang, Z. Wei and M. Yang (2026). *PageRank Centrality in Directed Graphs with Bounded In-Degree*. SODA. [https://arxiv.org/abs/2508.01257v2](https://arxiv.org/abs/2508.01257v2)

16. H. Wang, Z. Wei, J.-R. Wen and M. Yang (2024). *Revisiting Local Computation of PageRank: Simple and Optimal*. STOC. [https://arxiv.org/abs/2403.12648](https://arxiv.org/abs/2403.12648)

17. Feng, Li and Peng (2025). *Sublinear-Time Algorithms for Diagonally Dominant Systems and Applications to the Friedkin-Johnsen Model*. Abstract-level screening only. [https://arxiv.org/abs/2509.13112v1](https://arxiv.org/abs/2509.13112v1)
