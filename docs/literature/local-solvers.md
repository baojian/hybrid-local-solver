# Local Solvers

## Scope

This note covers algorithms designed to exploit locality in PageRank or
related graph problems. Candidate areas from the current research plan include
APPR, evolving-set methods, AESP, LocGD, LocCH, and LocSOR.

## Questions for comparison

- What mathematical problem and `alpha` convention does the method use?
- What residual, normalization, and stopping criterion does it use?
- How is the active or local set selected and updated?
- What convergence guarantee is proved?
- How are work, volume, and edge operations counted?
- Which assumptions are needed for locality?
- Can accuracy and work be compared directly with this project, or is an
  explicit conversion required?

## Source annotations

## Citation key: `huang2025accelerated`

- Citation: Binbin Huang, Luo Luo, Yanghua Xiao, Deqing Yang, and Baojian
  Zhou. “Accelerated Evolving Set Processes for Local PageRank Computation.”
  *Advances in Neural Information Processing Systems 39*, 2025.
- DOI/arXiv/URL: <https://doi.org/10.48550/arXiv.2510.08010>;
  arXiv `2510.08010v4`.
- Local PDF:
  `papers/2025-neurips-huang-accelerated-evolving-set-processes-local-pagerank.pdf`.
- Relevance: The paper defines the AESP outer process and two localized inexact
  proximal maps, including batched LocGD. It is the source algorithm for the
  standalone center-star lower-bound note and fixes the active-volume work
  measure, inexact gap schedule, activation threshold, momentum, and PPR
  accuracy used there.
- Exact pointers:
  - PDF pages 1-3, Equation (1), (P1), and Equation (3): define lazy-walk PPR,
    the symmetrized quadratic, and the degree-normalized infinity-error target.
  - PDF pages 4-5, Equations (4)-(10), condition (C1), and Lemma 3.2: define
    nested active-volume work, the inexact proximal set, the inner threshold,
    the batched LocGD update, and the scaled-gradient progress ratio.
  - PDF pages 6-7, Algorithms 1-2 and Theorems 3.3-3.6: specify the AESP-PPR
    schedule, `eta = 1 - 2 * alpha`, constant momentum, early stopping, inner
    gap guarantee, outer iteration count, and source upper bound.
  - PDF pages 16-21, Appendix A.2-A.3: prove the inner objective-gap certificate
    and LocGD convergence statement used to include initially empty calls.
  - PDF pages 26-27, Appendix A.5-A.6: prove the AESP and AESP-PPR complexity
    theorems and expose the run-dependent scaled-gradient constant `R`.
  - PDF page 29, Algorithms 3-4: distinguish the batched LocGD queue from the
    sequential LocAPPR queue. This distinction is essential to the star scan
    lower bound.
- Formulation differences: The source uses its own PPR accuracy `epsilon` and
  dominated active-volume cost. The repository-wide residual convention is
  still open, so the standalone note treats both definitions as note-scoped
  and asserts no conversion to RPPR, APPR, or implementation-wide stopping.
- Use in this repository: `manuscript/notes/aesp_locgd_star_lower_bound/`
  proves a new, source-compatible lower bound for the literal AESP-PPR plus
  batched LocGD algorithm. On a center-seeded star it gives
  `Omega(1 / (sqrt(alpha) * epsilon))` active-volume work, and under an edge
  budget it gives `Omega(min(m, 1 / epsilon) / sqrt(alpha))`. These are new
  repository results, not claims made by the source paper.
- Open questions: Determine whether a different graph forces transient volume
  beyond `O(1 / epsilon)`; extend the lower-bound mechanism to sequential
  LocAPPR or a wider local-oracle model; and reconcile AESP accuracy with the
  eventual repository residual convention.

## Citation key: `morris2003evolving`

- Citation: Ben Morris and Yuval Peres. “Evolving Sets and Mixing.”
  *Proceedings of the 35th Annual ACM Symposium on Theory of Computing*,
  pages 279-286, 2003.
- DOI/arXiv/URL: <https://doi.org/10.1145/780542.780585>
- Local PDF: `papers/2003-stoc-morris-evolving-sets-mixing.pdf`.
- Relevance: This paper supplies the evolving-set Markov-chain construction
  underlying later evolving-set local clustering methods. It connects the
  process to conductance profiles and mixing bounds rather than presenting a
  PageRank linear solver.
- Exact pointers:
  - Page 279, Introduction, “Definition: Evolving sets”: defines the random
    threshold update
    \(S'=\{y:Q(S,y)\geq U\pi(y)\}\), with the one-step inclusion probability
    in Equation (9).
  - Pages 279-280, Theorem 1 and Equations (6)-(8): bound uniform mixing time
    using the conductance profile \(\Phi(u)\).
  - Page 280, Section 2, Lemma 2: relates the evolving-set boundary gauge
    \(\psi(S)\) to conductance under a holding-probability assumption.
- Formulation differences: The state is a random subset generated from a
  Markov chain, and the target guarantee concerns mixing. This project studies
  deterministic or hybrid local updates for a PageRank-type solve, with
  residual-based accuracy and an explicit local-work model.
- Open questions: Determine precisely which evolving-set identities are used
  by LocESP and AESP, and whether their randomized set evolution has a useful
  analogue for the hybrid solver’s active-set or switching rule.

## Citation key: `andersen2009finding`

- Citation: Reid Andersen and Yuval Peres. “Finding Sparse Cuts Locally Using
  Evolving Sets.” *Proceedings of the 41st Annual ACM Symposium on Theory of
  Computing*, pages 235-244, 2009.
- DOI/arXiv/URL: <https://doi.org/10.1145/1536414.1536449>
- Local PDF:
  `papers/2009-stoc-andersen-finding-sparse-cuts-locally-evolving-sets.pdf`.
- Relevance: This paper turns the volume-biased evolving-set process into the
  local partitioning algorithm EvoCut. It explicitly analyzes work relative to
  output volume, making it a key predecessor for LocESP, AESP, and this
  project’s locality-aware work model.
- Exact pointers:
  - Pages 235-236, Introduction and Table 1: compare EvoCut with Nibble and
    PRNibble using both approximation quality and work/volume ratio.
  - Page 236, Theorem 1: states EvoCut’s expected work/volume bound and its
    local conductance guarantee for starting vertices in a low-conductance
    target set.
  - Page 237, Sections 2.2 and 2.4: define the evolving-set transition in
    Equation (1) and the volume-biased transition kernel in Equation (2).
  - Pages 239-240, Section 4: construct the local simulation procedure and
    EvoCut, then connect its sampled-path cost to the work/volume guarantee.
- Formulation differences: EvoCut is randomized, returns a vertex set, and
  measures accuracy through conductance. The hybrid solver targets a
  PageRank-type numerical solution with residual-based termination; its local
  work and output must therefore be compared through an explicit conversion,
  not treated as the same guarantee.
- Open questions: Identify whether the boundary-update implementation and
  sampled-path cost can inform an active-set work bound for LocESP or AESP,
  and determine which randomness-dependent guarantees can be compared fairly
  with deterministic solver stopping rules.

## Citation key: `andersen2007localcontributions`

- Citation: Reid Andersen, Christian Borgs, Jennifer T. Chayes, John E.
  Hopcroft, Vahab S. Mirrokni, and Shang-Hua Teng. “Local Computation of
  PageRank Contributions.” In *Algorithms and Models for the Web-Graph: 5th
  International Workshop, WAW 2007*, LNCS 4863, pages 150-165, Springer,
  2007.
- DOI/arXiv/URL: <https://doi.org/10.1007/978-3-540-77004-6_12>
- Local PDF:
  `papers/2007-waw-andersen-local-computation-pagerank-contributions.pdf`
  was extracted from physical pages 159-174 of the supplied proceedings
  volume.
- Relevance: The paper gives a backward local-push algorithm for approximating
  the contribution of all source vertices to one target vertex’s PageRank. Its
  explicit push-count and support bounds are relevant to local update
  accounting, although its target-column problem differs from the project’s
  seed-based PageRank solve.
- Exact pointers:
  - Page 150, Abstract and Introduction: define the contribution-vector and
    significant-contributor problems and state the local \(O(1/\epsilon)\)
    exploration objective.
  - Pages 153-154, Sections 2-3: define personalized PageRank contributions,
    the contribution vector, and the approximation criterion.
  - Pages 156-158, Section 3.2, Theorem 1 and Corollary 1: specify
    `ApproxContributions`, its pushback invariant, and its push-count bound.
  - Pages 160-162, Section 4, Theorems 2-6: derive local algorithms for top
    contributors and significant supporting sets from the approximate
    contribution vector.
  - Page 164, Theorem 7: relates PageRank contributions in a Markov chain to
    personalized PageRank in its time-reversed chain.
- Formulation differences: The method explores edges backward from a target
  vertex on a directed web graph and approximates a column of the personalized
  PageRank matrix. The hybrid solver begins from a seed distribution and
  targets a PageRank-type solution under the repository’s residual and work
  conventions.
- Open questions: Determine whether the pushback invariant or time-reversal
  relation provides a useful dual view of local residual propagation, and
  whether the support bounds can be translated to the hybrid solver’s active
  set without imposing directed-web assumptions.

## Citation key: `spielman2013local`

- Citation: Daniel A. Spielman and Shang-Hua Teng. “A Local Clustering
  Algorithm for Massive Graphs and Its Application to Nearly Linear Time Graph
  Partitioning.” *SIAM Journal on Computing*, 42(1):1-26, 2013.
- DOI/arXiv/URL: <https://doi.org/10.1137/080744888>; preprint
  <https://arxiv.org/abs/0809.3232>.
- Local PDF:
  `papers/2013-sicomp-spielman-local-clustering-massive-graphs-nearly-linear-partitioning.pdf`.
- Relevance: The paper introduces Nibble, an output-sensitive local clustering
  method based on truncated random walks, and uses repeated local calls to
  obtain a nearly linear-time graph partitioning algorithm. Its support
  truncation and work-versus-output analysis are relevant precedents for
  locality control in the hybrid solver.
- Exact pointers:
  - Preprint pages 1-2, Abstract and Section 1.1: state the local-clustering
    objective and explain why truncating random-walk distributions controls
    support growth.
  - Preprint pages 4-8, Section 2.1 and Theorem 2.1: define Nibble and state its
    running-time, conductance, volume, and seed-set guarantees.
  - Preprint Section 2.3, Lemma 2.13: bounds the error introduced by truncated
    random walks.
  - Preprint pages 18-20, Section 3, `RandomNibble`, and Theorem 3.2: assemble
    local calls into the nearly linear-time `Partition` algorithm.
- Formulation differences: Nibble returns a low-conductance vertex set and
  measures approximation through conductance and overlap. The hybrid solver
  targets a numerical PageRank-type solution with residual-based accuracy, so
  truncation error and work bounds require an explicit translation before
  comparison.
- Open questions: Determine whether Nibble’s degree-scaled truncation threshold
  suggests a principled active-set threshold for the hybrid solver, and compare
  its support/work accounting with LocESP, AESP, and residual-based local
  updates under a common edge-operation model.

## Citation key: `wang2024revisiting`

- Citation: Hanzhi Wang, Zhewei Wei, Ji-Rong Wen, and Mingji Yang. “Revisiting
  Local Computation of PageRank: Simple and Optimal.” *Proceedings of the 56th
  Annual ACM Symposium on Theory of Computing*, pages 911-922, 2024.
- DOI/arXiv/URL: <https://doi.org/10.1145/3618260.3649661>; full version
  <https://arxiv.org/abs/2403.12648>.
- Local PDF:
  `papers/2024-stoc-wang-revisiting-local-computation-pagerank-simple-optimal.pdf`.
- Relevance: This paper gives a modern worst-case analysis of the
  `ApproxContributions` backward local-push algorithm introduced by Andersen et
  al. (2007), proves its optimality for detecting significant contributors,
  and combines it with Monte Carlo sampling to improve single-node PageRank
  estimation. It is directly relevant to local work accounting and lower
  bounds for PageRank computations.
- Exact pointers:
  - Pages 911-913, Sections 1.1-1.2 and Theorems 1.1-1.6: define the local
    graph-access problems and summarize the upper and lower bounds.
  - Pages 914-915, Section 2 and Algorithm 1: specify
    `ApproxContributions`, its approximation invariant, and prior
    output-sensitive complexity bounds.
  - Pages 916-917, Section 4: prove the new worst-case complexity bound for
    `ApproxContributions` and derive the contributing-set result.
  - Pages 917-918, Section 5: analyze the bidirectional
    `ApproxContributions` plus Monte Carlo estimator for single-node PageRank.
  - Pages 919-922, Sections 6-7: establish lower bounds for contributor
    detection and single-node PageRank estimation.
- Formulation differences: The target is a column-oriented contribution vector
  or one node’s global PageRank score on a directed graph under an oracle
  access model. The hybrid solver starts from a seed distribution, produces a
  PageRank-type solution vector, and measures residual-based accuracy and
  concrete edge work, so the lower bounds do not transfer without a reduction.
- Open questions: Determine whether the paper’s degree-sensitive lower bounds
  constrain the hybrid solver’s backward or dual operations, translate its
  query model into the repository’s edge-operation model, and compare its
  output-sensitive term with active-set volume and residual support.

## Citation key: `macgregor2021local`

- Citation: Peter Macgregor and He Sun. “Local Algorithms for Finding Densely
  Connected Clusters.” *Proceedings of the 38th International Conference on
  Machine Learning*, PMLR 139:7268-7278, 2021.
- DOI/arXiv/URL: <https://proceedings.mlr.press/v139/macgregor21a.html>;
  preprint <https://arxiv.org/abs/2106.05245>.
- Local PDF:
  `papers/2021-icml-macgregor-local-algorithms-finding-densely-connected-clusters.pdf`.
- Relevance: This paper uses approximate personalized PageRank and a new
  double-cover reduction to find two seed-local vertex sets that are densely
  connected to each other but weakly connected to the rest of an undirected
  graph. It is a concrete example in which local PageRank is a computational
  primitive for a richer clustering objective rather than the final output.
- Exact pointers:
  - Preprint pages 2-3, Section 2 and Equation (1): define personalized
    PageRank, its random-walk interpretation, approximate PageRank, and the
    residual invariant.
  - Preprint pages 3-5, Sections 3.1-3.2 and Lemmas 1-3: introduce the
    double-cover reduction, simplify operator, and local algorithm design.
  - Preprint pages 6-8, Algorithms 1-3 and Theorem 1: specify
    `LocBipartDC`, its paired-coordinate PageRank push, and its local
    conductance, volume, and running-time guarantees.
  - Preprint pages 9-11, Section 4, Algorithm 4, and Theorem 2: replace
    PageRank with an evolving-set process for the directed-graph objective.
  - Preprint pages 11-15, Section 5: evaluate the methods on interstate
    disputes, migration flows, and synthetic graphs.
- Formulation differences: The PageRank routine is applied to a doubled graph
  and followed by sweep cuts to return a pair of clusters. Its guarantee is
  expressed through bipartiteness ratio, conductance, target volume, and
  randomized seed quality rather than numerical residual accuracy alone.
- Open questions: Compare the paired `dcpush` operation with the hybrid
  solver's update kernels, determine whether the double-cover structure can be
  handled without explicitly duplicating graph state, and translate its
  output-sensitive running time into the repository's edge-operation model.

## Citation key: `andersen2007using`

- Citation: Reid Andersen, Fan R. K. Chung, and Kevin J. Lang. “Using
  PageRank to Locally Partition a Graph.” *Internet Mathematics*,
  4(1):35-64, 2007.
- DOI/arXiv/URL: <https://doi.org/10.1080/15427951.2007.10129139>.
- Local PDF:
  `papers/2007-im-andersen-using-pagerank-locally-partition-graph.pdf`.
- Relevance: This paper gives the detailed PageRank-Nibble framework:
  personalized PageRank from a seed, a residual-push approximation whose work
  depends on output scale, degree-normalized sweep cuts, and a local
  partitioning guarantee. These are central precedents for the project's
  residual convention and locality-sensitive work model.
- Exact pointers:
  - Pages 38-41, Section 2: define lazy-walk PageRank, conductance,
    degree-normalized sweeps, and mixing curves.
  - Pages 41-44, Section 3, Algorithm 1, and Theorem 3.2: define
    `ApproximatePR`, its push invariant, residual threshold, support bound, and
    running time.
  - Pages 44-51, Section 4 and Theorems 4.1 and 4.5: derive the PageRank
    mixing result that links excess mass to a low-conductance sweep cut.
  - Pages 51-55, Section 5 and Theorems 5.1 and 5.3: show that many seeds
    inside a target set retain enough PageRank mass to expose a nearby cut.
  - Pages 55-60, Section 6, Algorithm 2, and Theorems 6.1-6.2: specify
    PageRank-Nibble and its output-sensitive local guarantee.
- Relationship to other library entries: The 2006 FOCS paper
  `andersen2006local` is the conference version. This journal article is
  retained as the expanded treatment with full PageRank approximation,
  mixing, and local-partitioning analysis.
- Later terminology: Zhou et al. (2024), PDF page 1, Abstract, and page 3,
  Section 2.1 and Lemma 2.1, write the APPR dependence as
  `Theta(1/(alpha * eps))`. The displayed lemma is nevertheless a one-sided
  upper inequality, and the accompanying argument derives only
  `sum_u d_u <= 1/(alpha * eps)` from residual-mass decrease. It gives no hard
  instance or lower-bound proof. The new star theorem below supplies that
  missing direction rather than treating the later `Theta` notation itself as
  evidence of tightness.
- Use in this repository: `manuscript/sections/appr_lower_bound.tex` restates
  the push operation (Definition 3.3), the push invariant (Lemma 3.4), and the
  work bound of Theorem 3.2 / Equation (3.3) in the repository's column-vector
  and degree-weighted work conventions, and adds a matching lower bound. The
  source proves only the upper bound `O(1/(alpha * eps))`; the paper does not
  state whether it is worst-case tight. The manuscript closes this by a
  center-seeded star `K_{1,m}` with `m = floor(1/(8 * eps_appr))`, giving
  `3/(128 * alpha * eps_appr) < W <= 1/(alpha * eps_appr)` for every legal
  active-vertex ordering, hence
  `W_appr^worst(alpha, eps_appr) = Theta(1/(alpha * eps_appr))`. The two
  mechanisms are: termination on a graph of volume `Theta(1/eps_appr)` forces
  `Omega(1/alpha)` cumulative pushed residual, and a leaf-flow identity routes
  a constant fraction of it through a vertex of degree `Theta(1/eps_appr)`.
  The manuscript also records that `x = D^{-1/2} pi` is the unique minimizer of
  the RPPR objective at `rho = 0`, which is what makes APPR and the
  `l1`-regularized formulation comparable at all.
- Formulation differences: The algorithm returns a low-conductance set after
  a sweep and tunes PageRank accuracy from a target volume scale. The hybrid
  solver primarily targets a numerical solution under a prescribed residual
  tolerance, so cut quality and volume guarantees are downstream rather than
  its sole correctness criteria.
- Open questions: Align the paper's row-vector, lazy-walk, and teleportation
  conventions with the implementation, reproduce the push invariant exactly,
  and compare PageRank-Nibble's volume-indexed work bound with the hybrid
  solver's residual-driven stopping and edge-operation accounting.
