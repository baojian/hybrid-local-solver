# arXiv audit: 1 August–9 September 2026

The earlier review was a targeted literature search, not an enumeration of this entire date window. This follow-up performs a reproducible metadata sweep and staged screening. It found two additional papers worth adding to the manuscript: Thorup–Wang's August revision on instance-optimal scalar PageRank estimation, and Li–Yang's September paper on regularized resistance. Both are now cited, with explicit differences from project OP1/OP2.

**Assessment:** no additional source theorem matching the full OP1 or OP2 parameter, graph-access, and output contract was identified among the screened records. This is a qualified result of the stated search, not a guarantee that no overlapping work exists.

## What was enumerated

Observation window: **2026-08-01 00:00 UTC through 2026-09-09 14:11 UTC** (22:11 China time on 9 September), using the metadata publicly retrievable during this audit. Later announcements are outside this snapshot.

The official arXiv API supplied **3,775 distinct paper records** after deduplication: **2,644 first submissions within the window** and **1,131 papers first submitted earlier with a latest revision in the window**. Every title was screened. Relevant-looking records then received abstract screening; the closest candidates received targeted full-text checks of definitions, theorem statements, algorithms, and access costs. Most excluded papers were screened only by title. This is not a claim that 3,775 full papers were read.

The search included all new submissions and latest updates in **cs.DS, math.OC, math.NA and cs.NA**, without a keyword restriction within those categories. Cross-category searches used PageRank/page rank, graph diffusion, local clustering, Laplacian solvers, diagonally dominant matrices, M-matrices, graph/quadratic active sets, random walks with restart, and related synonyms. Thus relevant work outside the four core categories could enter through keyword matching, including ISO-RAG and quantum PageRank.

The query interface documents pagination, total-result counts, lastUpdatedDate sorting, and the distinction between a paper's first publication timestamp and its latest-update timestamp. [Official arXiv API manual](https://info.arxiv.org/help/api/user-manual.html).

| Query family | Date basis | Reported hits in window | Retrieval verification |
|---|---|---:|---|
| PageRank / page rank, all categories | First submission | 10 | All 10 of 10 query hits retrieved |
| Broad diffusion / graph / optimization terms | First submission | 749 | All 749 of 749 query hits retrieved in three pages |
| Four core categories, no keyword filter | First submission | 1,942 | All 1,942 of 1,942 query hits retrieved in seven pages |
| Restart-walk / local-partition / diffusion synonyms | First submission | 6 | All 6 of 6 query hits retrieved |
| PageRank / page rank, all categories | Latest update | 18 | Sorted 300-record prefix passes below August1 |
| Narrow adjacent solver/diffusion terms | Latest update | 29 | Sorted 300-record prefix passes below August1 |
| Synonyms | Latest update | 7 | Entire 202-record all-date query retrieved |
| Four core categories, no keyword filter | Latest update | 3,059 | Sorted 3,500-record prefix passes below August1 |

Rows overlap and must not be added to obtain the distinct-paper count. All update prefixes were checked to be in descending timestamp order. Both old identifiers and identifiers whose month differs from the original submission timestamp were retained correctly. The counts establish complete retrieval for these specific API queries and this indexed snapshot, not complete coverage of every possible description of the research problem.

## Project comparison contract

OP1 returns an explicit sparse approximation to point-seed PPR on the original finite, connected, simple, unit-weight undirected graph, with degree-normalized maximum error at most epsilon_ppr, and soft-O(1/(epsilon_ppr sqrt(alpha))) total locally charged work.

OP2 returns an additive objective approximation for the project's degree-weighted l1-regularized PageRank quadratic, with soft-O(1/(rho sqrt(alpha))) work and logarithmic objective-accuracy factors. Graph exploration, repeated row scans, and support discovery are charged. General fixed-point or first-order oracle iteration counts do not by themselves supply that local-work guarantee. The manuscript's OP1 result follows from its regularization-bias and objective-error conversion for OP2.

## Material findings

### Li and Yang: regularized resistance, September3; version2 September4

[Improved algorithm for counting spanning trees by l1-regularized resistance, 2609.03574v2](https://arxiv.org/abs/2609.03574v2) is a relevant methodological follow-on that the earlier targeted review missed. Definition3 uses an unshifted Laplacian obstacle with an unweighted penalty. Section3.1/Theorem13 states soft-O(lambda^-3) per-source potential approximation after soft-O(m) global preprocessing. Algorithm1 uses nested SDD solves and Lemma14 supplies a preprocessed boundary oracle. Its objective, preprocessing and parameter guarantee differ from OP2; its output is not the OP1 PPR vector. Added as `li2026resistance` in the manuscript and literature index. [Primary theorem and algorithm](https://arxiv.org/html/2609.03574v2#S3.SS1).

### Thorup and Wang: older paper revised August3

[Instance-Optimality of Bidirectional PageRank Estimation, 2512.16087v6](https://arxiv.org/abs/2512.16087v6) was first submitted in December2025 and revised August3,2026; the record says it will appear in FOCS2026. Section1 defines a single vertex's global PageRank, averaged over uniform starting vertices, and fixes alpha. Section2 specifies neighbor, degree and random-jump access; Theorem4.1 bounds expected adaptive bidirectional estimation work. Its probabilistic relative-error scalar guarantee and graph classes differ from OP1/OP2. Added as `thorup2026instance`. Version5 already contains the scalar upper-bound contract; an August version date does not mean a new OP1 theorem appeared then. [Primary model and theorem](https://arxiv.org/html/2512.16087v6).

### Wei and Yang: August17, already included

[A Simple Active-Set Method for PageRank-Based Local Graph Clustering, 2608.16339v1](https://arxiv.org/abs/2608.16339v1) remains the closest directly relevant August predecessor. It provides soft-O(epsilon^-2) ACL approximation and soft-O(k*V*) regularized-PageRank work with nearly-linear principal SDD solves. Its deterministic-solver remark must also be retained. The earlier source-level comparison remains applicable; this sweep found no later revision. The current manuscript explains the parameter tradeoff rather than claiming that prior acceleration or deterministic active sets did not exist.

### Two additional September PageRank uses

[ISO-RAG, 2609.00513v1](https://arxiv.org/abs/2609.00513v1), first submitted September1, solves a PageRank fixed point on a selected, edge-pruned, renormalized graph. Its methods do not supply a transfer guarantee to original-graph PPR or the OP2 objective. Its exact-convergence wording therefore is not an OP1 certificate. The method equations, rather than broad abstract language, determine this classification. [Primary methods](https://arxiv.org/html/2609.00513v1).

[Quantum algorithm for PageRank computation through multistep quantum resonant transitions, 2609.08140v1](https://arxiv.org/abs/2609.08140v1), submitted September8, prepares a quantum state. Its computational/output model and Hamiltonian-simulation costs do not establish the classical explicit sparse-vector OP1 or RPPR guarantee. [Primary full text](https://arxiv.org/html/2609.08140v1).

## Every PageRank-keyword first-submission hit

Dates below are first-submission timestamps; latest versions are in the links. Omega-N's arXiv identifier begins2609 but the official history gives August21 as its first submission. This is why identifier prefixes alone were not used as a date filter.

| First submitted | Record | Screening disposition |
|---|---|---|
| 2026-08-08 | [eIRWR: Enhanced Iterative Random Walk with Restart for Scalable Root Cause Analysis in Microservices](https://arxiv.org/abs/2608.08073v1) | Modified restart/transition model for fault localization; methods checked. |
| 2026-08-11 | [A Graph Approach to the Academic Publishing Network: A Heterogeneous Model and Structural Screening over OpenAlex Open Data](https://arxiv.org/abs/2608.10774v1) | Academic-publishing network application; abstract screened. |
| 2026-08-13 | [Power in Liquid Democracy: A Network Centrality Approach](https://arxiv.org/abs/2608.13188v1) | Liquid-democracy centrality and representative selection; abstract screened. |
| 2026-08-17 | [A Simple Active-Set Method for PageRank-Based Local Graph Clustering](https://arxiv.org/abs/2608.16339v1) | Known direct predecessor; existing full theorem comparison retained. |
| 2026-08-21 | [Advanced Linear Algebra with Applications - Part I (Numerical linear algebra for PDEs, machine learning, and data assimilation)](https://arxiv.org/abs/2608.21234v1) | Numerical linear algebra lecture notes; PageRank section checked. |
| 2026-08-21 | [Omega-N: Interpretable Structural Node Descriptors and Their Applicability Domain](https://arxiv.org/abs/2609.01633v2) | PPR neighborhoods used as node descriptors; abstract screened. |
| 2026-08-25 | [PhysicsBench: A Unified Leaderboard for Generative and Predictive Models in Engineering Design and Simulation](https://arxiv.org/abs/2608.24056v1) | Benchmark-ranking application; abstract screened. |
| 2026-08-28 | [Structural Change and Random Graph Models in Global Oil Trade Networks](https://arxiv.org/abs/2608.28474v1) | Oil-trade network application; abstract screened. |
| 2026-09-01 | [ISO-RAG: Isoperimetric Noise Control for Retrieval-Augmented Generation](https://arxiv.org/abs/2609.00513v1) | Modified-subgraph retrieval PageRank; targeted full text checked. |
| 2026-09-08 | [Quantum algorithm for PageRank computation through multistep quantum resonant transitions](https://arxiv.org/abs/2609.08140v1) | Quantum-state output; targeted full text checked. |

## Other candidate checks and limits

Broader screening examined sparse least-squares condition-number lower bounds, general active-set QP methods, nonnegative conjugate gradients, accelerated Frank–Wolfe methods with sparsity/strict-complementarity assumptions, global spectral sparsifiers, PDE obstacle solvers, and recent matrix-computation open-problem updates. None of the inspected statements supplies the complete OP1/OP2 contract. The supporting reports distinguish these different problems instead of rejecting them merely because their titles omit PageRank.

There are four residual limitations:

1. **Coverage:** all-arXiv keyword matches and four core categories are not every submission in every category. A relevant paper using different terminology outside those categories can be missed.
2. **Reading depth:** most records were title screened, a smaller set abstract screened, and the closest were theorem/method screened. A consequence hidden in a generic paper may be missed. No claim of a complete proof audit is made.
3. **Timing:** metadata reflects publicly retrievable records at the stated cutoff. Not-yet-announced, private, unpublished, unindexed, and later work are not excluded.
4. **Versions:** the API returns latest records. Older-paper latest updates within the window were included, but the sweep is not an enumeration of every historical version event or a line-by-line comparison of every revision.

The appropriate novelty language remains: **“To our knowledge, no previous work establishes this joint parameter bound under the stated graph-access and output guarantees.”** Avoid “no other sources work on this problem,” “first accelerated PageRank method,” or universal optimality claims.

## Reproducibility

The full query strings, URLs, result counts, UTC timestamps, unique record set, and source abstracts are retained in the metadata snapshot. Raw paginated Atom responses and the collection scripts are in the same evidence directory. Supporting screening reports and ledgers retain excluded titles and inspection depth. All evidence resides outside the read-only synced `sources/` directory.

- [Complete metadata snapshot](/Users/baojian/.codex/.chatgpt-projects/g-p-6a61903d8df88191b0fa11a0ff57a7e1/publication-20260909/arxiv-window-evidence/audit-metadata.json).
- [New-title part0](/Users/baojian/.codex/.chatgpt-projects/g-p-6a61903d8df88191b0fa11a0ff57a7e1/publication-20260909/arxiv-window-evidence/screen-part-0-review.md).
- [New-title part1](/Users/baojian/.codex/.chatgpt-projects/g-p-6a61903d8df88191b0fa11a0ff57a7e1/publication-20260909/screen-part-1-review.md).
- [New-title part2](/Users/baojian/.codex/.chatgpt-projects/g-p-6a61903d8df88191b0fa11a0ff57a7e1/publication-20260909/arxiv-window-evidence/screen-part-2-review.md).
- [New-title part3](/Users/baojian/.codex/.chatgpt-projects/g-p-6a61903d8df88191b0fa11a0ff57a7e1/publication-20260909/arxiv-window-evidence/screen-part-3-review.md).
- [Older-revision part0](/Users/baojian/.codex/.chatgpt-projects/g-p-6a61903d8df88191b0fa11a0ff57a7e1/publication-20260909/arxiv-window-evidence/revisions-part-0-review.md).
- [Older-revision part1](/Users/baojian/.codex/.chatgpt-projects/g-p-6a61903d8df88191b0fa11a0ff57a7e1/publication-20260909/revisions-part-1-review.md).
- [Older-revision part2](/Users/baojian/.codex/.chatgpt-projects/g-p-6a61903d8df88191b0fa11a0ff57a7e1/publication-20260909/arxiv-window-evidence/revisions-part-2-review.md).
- [Older-revision part3](/Users/baojian/.codex/.chatgpt-projects/g-p-6a61903d8df88191b0fa11a0ff57a7e1/publication-20260909/arxiv-window-evidence/revisions-part-3-review.md).
- [Official history checks](/Users/baojian/.codex/.chatgpt-projects/g-p-6a61903d8df88191b0fa11a0ff57a7e1/publication-20260909/arxiv-revision-audit.md).
- [August keyword audit](/Users/baojian/.codex/.chatgpt-projects/g-p-6a61903d8df88191b0fa11a0ff57a7e1/publication-20260909/arxiv-august-audit.md).
- [September keyword audit](/Users/baojian/.codex/.chatgpt-projects/g-p-6a61903d8df88191b0fa11a0ff57a7e1/publication-20260909/arxiv-september-audit.md).

## Manuscript update

The two new theoretical citations and their contract distinctions were added to related work. The resulting manuscript has **42 pages and 31 cited references**. Only related-work prose, the bibliography, and its generated bibliography changed inside the submission archive; all other TeX members, including the proofs, are byte-identical to the earlier package. The 23-member archive independently recompiles with text identical to the active PDF. All 42 rendered pages were checked for layout, with detailed checks of the changed related-work and bibliography pages. One underfull bibliography paragraph remains visually acceptable; no undefined citations or overfull boxes were reported. No numerical or proof test rerun was needed for this bibliography/prose-only follow-up; the earlier proof checks remain separately documented.

No arXiv submission was made during this follow-up.
