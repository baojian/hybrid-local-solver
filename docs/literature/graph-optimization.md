# Graph Optimization

## Scope

This note covers the local PageRank problem formulation and broader graph
optimization concepts needed to define locality, accuracy, and work.

## Questions for comparison

- Is the graph directed, undirected, weighted, or assumed to have no isolated
  vertices?
- Are probability and solution vectors rows or columns?
- How is the transition operator normalized?
- What seed distribution and PageRank equation are used?
- What graph volume, conductance, or locality quantities are defined?
- Which residual or error norm supports the stated guarantee?
- What constitutes a local update or edge operation?

## Source annotations

## Citation key: `spielman2004nearly`

- Citation: Daniel A. Spielman and Shang-Hua Teng. “Nearly-Linear Time
  Algorithms for Graph Partitioning, Graph Sparsification, and Solving Linear
  Systems.” *Proceedings of the 36th Annual ACM Symposium on Theory of
  Computing*, pages 81-90, 2004.
- DOI/arXiv/URL: <https://doi.org/10.1145/1007352.1007372>; preprint
  <https://arxiv.org/abs/cs/0310051>.
- Local PDF:
  `papers/2004-stoc-spielman-nearly-linear-graph-partitioning-sparsification-linear-systems.pdf`.
- Relevance: This extended abstract links approximate graph partitioning,
  spectral sparsification, ultra-sparse preconditioners, and preconditioned
  Chebyshev iteration into a nearly-linear-time framework for symmetric
  diagonally dominant linear systems. It provides historical context for the
  graph-diffusion systems and work models used by this project.
- Exact pointers:
  - Page 81, Abstract and Section 1: state the SDD solver objective and the
    roles of graph partitioning, sparsification, and preconditioning.
  - Pages 81-82, Sections 1.1-1.3: describe preconditioned Chebyshev iteration,
    spectral approximation of graph Laplacians, and the truncated-random-walk
    partitioning strategy.
  - Page 85, Theorem 5.4: gives the spectral preconditioning guarantee for the
    sampling construction.
  - Page 87, Theorems 7.5 and 7.8: state the guarantees for `Sparsify` and
    `UltraSparsify`.
  - Pages 87-89, Section 8 and Theorems 8.1, 8.2, and 8.4: connect the
    preconditioners to one-shot and recursive linear-system solvers.
- Formulation differences: The paper solves global SDD systems and measures
  approximation through Laplacian quadratic forms, condition numbers, and
  energy-norm error. This project seeks local PageRank-type solutions with
  residual-based stopping and locality-sensitive work, so neither its error
  bounds nor its total-work guarantees transfer directly.
- Open questions: Determine which spectral-approximation bounds are useful for
  hybrid local preconditioning, and whether the recursive solver analysis can
  accommodate active-set truncation without losing a local work bound.

## Citation key: `spielman2010algorithms`

- Citation: Daniel A. Spielman. “Algorithms, Graph Theory, and Linear
  Equations in Laplacian Matrices.” In *Proceedings of the International
  Congress of Mathematicians 2010*, Volume IV, pages 2698-2722, 2010.
- DOI/arXiv/URL: <https://doi.org/10.1142/9789814324359_0164>; author
  manuscript <https://www.cs.yale.edu/homes/spielman/PAPERS/icm10post.pdf>.
- Local PDF:
  `papers/2010-icm-spielman-algorithms-graph-theory-linear-equations-laplacian-matrices.pdf`.
- Relevance: This survey provides a unified explanation of how graph
  Laplacians, spectral approximation, preconditioned iteration, low-stretch
  spanning trees, sparsifiers, ultra-sparsifiers, and local clustering fit into
  fast Laplacian solvers. Its overview is useful for locating the hybrid local
  solver relative to the broader Laplacian-solver pipeline.
- Exact pointers:
  - Postprint pages 1-5, Section 1: define graph Laplacians, conductance,
    condition number, and the graph primitives used throughout the survey.
  - Postprint pages 7-10, Section 3: review direct and iterative Laplacian
    solvers, including preconditioned conjugate gradient.
  - Postprint pages 11-14, Sections 4-5: introduce spectral approximation,
    sparse graph approximation, and support-theory preconditioners.
  - Postprint pages 15-18, Sections 6-7 and Theorem 6.1: connect low-stretch
    spanning trees and ultra-sparsifiers to nearly-linear Laplacian solvers.
  - Postprint pages 18-19, Section 8: summarize local clustering via truncated
    random walks, personalized PageRank, and evolving sets.
- Formulation differences: This is a global survey rather than a new local
  numerical method. Its solver guarantees use Laplacian-system accuracy,
  condition numbers, and global sparse-matrix work; the project uses a
  PageRank-type system, residual-based termination, and locality-sensitive
  edge work.
- Open questions: Use the survey's common spectral-approximation language to
  separate global preconditioning cost from local update cost, and determine
  which graph primitives remain useful when only a seed-local subgraph is
  explored.

## Citation key: `spielman2011spectral`

- Citation: Daniel A. Spielman and Shang-Hua Teng. “Spectral Sparsification of
  Graphs.” *SIAM Journal on Computing*, 40(4):981-1025, 2011.
- DOI/arXiv/URL: <https://doi.org/10.1137/08074489X>; preprint
  <https://arxiv.org/abs/0808.4134>.
- Local PDF:
  `papers/2011-sicomp-spielman-spectral-sparsification-graphs.pdf`.
- Relevance: This paper isolates and fully develops the spectral
  sparsification component announced in the 2004 STOC extended abstract. It
  defines graph approximation through Laplacian quadratic forms, constructs
  nearly-linear-size sparsifiers in nearly-linear time, and explains their
  role as preconditioners for graph Laplacian systems.
- Exact pointers:
  - Preprint pages 2-3, Sections 1-2 and Equations (1)-(2): define spectral
    approximation and connect its factor to the relative condition number of
    a Laplacian preconditioner.
  - Preprint pages 8-18, Section 6 and Theorem 6.1: give the random-sampling
    sparsifier for high-conductance graphs.
  - Preprint pages 19-23, Section 7 and Theorem 7.1: develop graph and spectral
    decompositions used to establish sparsifier existence.
  - Preprint pages 24-35, Section 8 and Theorem 8.1: build the approximate-cut
    routine from the earlier local partitioning algorithm.
  - Preprint pages 36-48, Sections 9-10, Lemma 9.2, and Theorem 10.5: assemble
    the algorithms for unweighted and weighted spectral sparsification.
- Formulation differences: Spectral sparsification is a global
  matrix-approximation problem on undirected weighted graph Laplacians. The
  hybrid solver instead targets a seed-local PageRank-type solution and uses
  residual-based stopping, so a sparsifier can only serve as a possible
  computational tool; it does not by itself provide a locality guarantee.
- Open questions: Test whether sparsifying only the explored subgraph can
  improve hybrid-solver work while preserving the repository's residual
  convention, and identify an error composition bound between truncation,
  sparsification, and iterative-solve errors.

## Citation key: `brand2022faster`

- Citation: Jan van den Brand, Yu Gao, Arun Jambulapati, Yin Tat Lee, Yang P.
  Liu, Richard Peng, and Aaron Sidford. “Faster Maxflow via Improved Dynamic
  Spectral Vertex Sparsifiers.” *Proceedings of the 54th Annual ACM Symposium
  on Theory of Computing*, pages 543-556, 2022.
- DOI/arXiv/URL: <https://doi.org/10.1145/3519935.3520068>; extended version
  <https://arxiv.org/abs/2112.00722>.
- Local PDF:
  `papers/2022-stoc-brand-faster-maxflow-dynamic-spectral-vertex-sparsifiers.pdf`.
- Relevance: The paper supplies an existing construction pattern for the
  hybrid project's heavy-change reporter. It combines sparse ℓ2 heavy-hitter
  sketches, harmonic extension, and a dynamically maintained spectral Schur
  complement to locate large electrical-flow coordinates without evaluating
  every edge. The grounded-Laplacian reduction in
  `manuscript/notes/response_preconditioned_hybrid/` shows algebraic
  compatibility with the shared PageRank operator.
- Exact pointers:
  - PDF pages 1-4, Abstract and Section 1.1: identify dynamic Schur
    complements, operator heavy hitters, and adaptivity as the three main
    data-structural ingredients.
  - PDF page 13, Theorem 4.1: states the informal dynamic-Schur interface and
    its initialization, terminal-addition, update, and query costs.
  - PDF pages 21-22, Section 4.2 and Theorem 4.10: give the precise dynamic
    spectral Schur-complement interface, including `InitialSC`, the terminal
    budget, and the oblivious-adversary qualification.
  - PDF pages 23-25, Section 5.1 and Lemmas 5.2-5.3: express inverse action
    through harmonic extension and a terminal Schur complement.
  - PDF pages 32-34, Section 5.4, Theorem 5.10, and Algorithm 5: construct the
    sparse-projection locator and state its candidate-size and running-time
    guarantees.
  - PDF pages 35-42, Section 6: develop the nontrivial reduction from
    oblivious to adaptive queries.
- Formulation differences: The source begins with the full `m`-edge graph,
  locates edge-current coordinates relative to a global ℓ2 norm, and charges
  global preprocessing and periodic rebuilding. Its parameters give
  initialization `O_tilde(m beta^-2 xi^-2)`, terminal/update cost
  `O_tilde(beta^-2 xi^-2)`, and locator cost
  `O_tilde(beta m xi^-2)`, with only `O(beta m)` updates before rebuilding.
  The local PageRank target instead exposes a seed-local graph online, reports
  degree-normalized vertex boundary demands at an absolute finite-band scale,
  and requires total work in the final active volume. Therefore the source
  architecture transfers, but its complexity theorem does not.
- Use in this repository: The response-preconditioned note proves that the
  PageRank Stieltjes matrix is diagonally congruent to a grounded graph
  Laplacian and maps normalized boundary response to a degree-scaled vertex
  divergence. It uses the paper as a concrete implementation blueprint while
  retaining dynamic local sketch maintenance as an open lemma.
- Open questions: Replace full-graph initialization by exposure-charged
  geometric epochs, adapt the edge-flow locator to degree-scaled vertex
  divergence, exploit monotone terminal additions and killed walks, and use
  the note's two-ledger square-root scheduler to target total
  `O_tilde(V / sqrt(alpha))` or `O_tilde(V)` work.

## Citation key: `rubinfeld2011sublinear`

- Citation: Ronitt Rubinfeld and Asaf Shapira. “Sublinear Time Algorithms.”
  *SIAM Journal on Discrete Mathematics*, 25(4):1562-1588, 2011.
- DOI/arXiv/URL: <https://doi.org/10.1137/100791075>; ECCC report
  <https://eccc.weizmann.ac.il/report/2011/013/>.
- Local PDF: `papers/2011-sidma-rubinfeld-sublinear-time-algorithms.pdf`.
- Relevance: This survey clarifies what sublinear computation can promise when
  an algorithm inspects only a small portion of its input. Its emphasis on
  explicit access models, randomized approximation, and robust
  characterizations is useful when stating what “local” means for a graph
  solver.
- Exact pointers:
  - Report pages 1-4, Sections 1-2: motivate sublinear computation through
    property testing and a monotonicity example.
  - Report pages 5-8, Section 3: formalize the approximation and oracle-access
    concepts used by the survey.
  - Report pages 12-25, Section 5: survey dense- and sparse-graph property
    testing and show how the graph representation changes attainable bounds.
  - Report pages 25-29, Section 6: discuss sublinear approximation algorithms
    for optimization problems.
- Formulation differences: This is a broad survey of property testing and
  approximation rather than a numerical graph-diffusion solver. Its query
  models and distance-to-property guarantees are not interchangeable with
  residual accuracy or edge-operation counts.
- Open questions: State the hybrid solver's graph oracle and output promise
  explicitly, identify which global residual quantities can be certified
  without scanning the graph, and distinguish sublinear input access from
  output-sensitive local work.

## Citation key: `alon2012space`

- Citation: Noga Alon, Ronitt Rubinfeld, Shai Vardi, and Ning Xie.
  “Space-Efficient Local Computation Algorithms.” *Proceedings of the
  Twenty-Third Annual ACM-SIAM Symposium on Discrete Algorithms*, pages
  1132-1139, 2012.
- DOI/arXiv/URL: <https://doi.org/10.1137/1.9781611973099.89>; full version
  <https://arxiv.org/abs/1109.6178>.
- Local PDF:
  `papers/2012-soda-alon-space-efficient-local-computation-algorithms.pdf`.
- Relevance: This paper formalizes local computation as answering online
  queries to a single consistent global solution without constructing or
  storing that solution. Its polylogarithmic-space, query-oblivious, and
  parallelizable constructions provide a useful contrast to numerical graph
  locality, where the solver stores a sparse approximation and residual.
- Exact pointers:
  - Pages 1132-1134, Sections 1.1-1.2 and Theorems 1.1-1.2: state the
    polylogarithmic-time-and-space guarantees and explain query obliviousness,
    parallel consistency, bounded independence, and random query trees.
  - Pages 1134-1135, Sections 1.3-2: distinguish LCAs from related local and
    sublinear models and establish notation and pseudorandom primitives.
  - Pages 1135-1137, Section 3 and Theorem 3.1: prove the high-probability
    polylogarithmic bound on random query-tree size using branching processes.
  - Pages 1137-1139, Section 4 and Theorem 4.1: construct compact
    pseudorandom orderings that avoid storing all vertex ranks.
- Formulation differences: The LCA output is a queried bit of a combinatorial
  solution, and correctness means consistency with some legal global output.
  The hybrid solver produces numerical values, maintains residual state, and
  requires an explicit approximation norm and graph-edge work model.
- Open questions: Decide whether coordinate requests to the hybrid solution
  should be supported independently of a full solve, determine what
  cross-query consistency means under numerical tolerance, and assess whether
  bounded-independence or recomputable random priorities can reduce active-set
  storage.

## Citation key: `anikin2022efficient`

- Citation: Anton Anikin, Alexander Gasnikov, Alexander Gornov, Dmitry
  Kamzolov, Yury Maximov, and Yurii Nesterov. “Efficient Numerical Methods to
  Solve Sparse Linear Equations with Application to PageRank.” *Optimization
  Methods and Software*, 37(3):907-935, 2022.
- DOI/arXiv/URL: <https://doi.org/10.1080/10556788.2020.1858297>; preprint
  <https://arxiv.org/abs/1508.07607>.
- Local PDF:
  `papers/2022-oms-anikin-efficient-numerical-methods-sparse-linear-equations-pagerank.pdf`.
- Relevance: This paper reformulates stationary-distribution PageRank as
  simplex-constrained residual minimization and develops three algorithms that
  exploit bounded row and column sparsity: ℓ1-proximal gradient, sparse
  Frank-Wolfe, and randomized-projection mirror descent. It provides useful
  global sparse-update baselines for distinguishing matrix sparsity from
  seed-local computation.
- Exact pointers:
  - Preprint pages 1-4, Sections 1-1.2: define the simplex residual problems,
    summarize the three algorithms, and compare their complexity bounds.
  - Preprint pages 5-10, Section 2, Algorithm 1, and Theorem 2.2: derive the
    `NL1` method and its sparse gradient and objective updates.
  - Preprint pages 10-13, Section 3, Algorithm 2, and Theorem 3.1: present the
    sparse-update Frank-Wolfe method and its complexity.
  - Preprint pages 13-18, Section 4, Algorithms 3-4, and Theorem 4.1: formulate
    the ℓ∞ residual problem as a saddle point and analyze randomized
    projection.
  - Preprint pages 18-25, Section 5: discuss implementation and compare the
    methods on real and simulated PageRank instances.
- Formulation differences: The target is a global stationary distribution on
  a transition matrix with bounded row and column degrees. The hybrid solver
  uses personalized seeds and seeks work tied to a local support; sublinear
  access to known sparse matrix structure is not by itself a seed-local
  guarantee.
- Open questions: Implement the three methods as global sparse baselines,
  normalize their residual criteria to the repository convention, and test
  whether their sparse update data structures can accelerate active-set work
  without requiring global simplex maintenance.

## Citation key: `kariotakis2026fairrari`

- Citation: Emmanouil Kariotakis and Aritra Konar. “FairRARI: A Plug and Play
  Framework for Fairness-Aware PageRank.” *Forty-Third International
  Conference on Machine Learning (ICML)*, 2026.
- DOI/arXiv/URL: <https://openreview.net/forum?id=Z2axjFEPH3>; preprint
  <https://doi.org/10.48550/arXiv.2602.08589>; project page
  <https://ekariotakis.github.io/projects/fairrari_project_page/>.
- Local PDF:
  `papers/2026-icml-kariotakis-fairrari-fairness-aware-pagerank.pdf`.
- Relevance: This is a substantive application of PageRank to fairness-aware
  ranking. It expresses the PageRank vector as the minimizer of a strongly
  convex quadratic objective, adds convex group-fairness constraints, and
  alternates an ordinary PageRank update with a projection onto the fairness
  set. It therefore illustrates how a PageRank solver can become the numerical
  core of a constrained graph-learning application.
- Exact pointers:
  - Pages 1-2, Abstract and Introduction: motivate biased allocation of
    PageRank mass and state the fairness, optimality, and complexity goals.
  - Pages 3-4, Section 3, Proposition 3.1, and Equations (4)-(7): derive the
    variational PageRank objective and the projected PageRank fixed-point
    iteration.
  - Page 4, Theorems 3.2-3.3: establish geometric fixed-point convergence and
    equivalence with the fairness-constrained optimum.
  - Pages 5-6, Section 4, Theorems 4.1-4.3, and Algorithm 1: instantiate three
    group-fairness criteria and their projection routines.
  - Pages 7-12, Section 6: compare score utility, ranking utility, and achieved
    fairness against existing fair-PageRank baselines on real graphs.
  - Appendix B.2: relates the paper's random-walk-Laplacian objective to the
    earlier variational PageRank formulation used elsewhere in this project.
- Formulation differences: FairRARI computes a global centrality vector with a
  uniform teleportation vector and group-wide fairness constraints. Its
  projection step can touch all vertices and can destroy sparse support, so the
  claimed linear-time iteration is not a local-work guarantee and does not
  directly exploit a personalized seed.
- Open questions: Determine whether the fairness projection can be maintained
  incrementally over a local active set, whether a hybrid local solver can
  preserve feasibility without global scans, and how projection error should
  combine with the repository's residual stopping rule.
