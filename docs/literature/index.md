# Research Paper Index

This index organizes the project's paper library by research role. Use the
paper title as the main identifier and the BibTeX key for citations. A paper
may support several areas even though the catalog assigns one primary area.

## Research areas

### PageRank foundations and formulations

These papers establish the PageRank-based local partitioning problem, its
optimization interpretation, and broader algorithmic context.

- *Local Graph Partitioning Using PageRank Vectors* (Andersen, Chung, and
  Lang, 2006) - APPR and local partitioning foundation.
- *Variational Perspective on Local Graph Clustering* (Fountoulakis et al.,
  2019) - variational and optimization formulation.
- *Efficient Algorithms for Personalized PageRank Computation: A Survey*
  (Yang et al., 2024) - PPR algorithms and comparison framework.

### Heat-kernel PageRank

These papers develop heat-kernel PageRank and its use in local graph
partitioning.

- *The Heat Kernel as the PageRank of a Graph* (Chung, 2007).
- *A Local Graph Partitioning Algorithm Using Heat Kernel PageRank* (Chung,
  2009).

### Evolving-set methods

These papers use evolving sets or locally evolving-set processes for local
clustering and local PageRank computation.

- *Evolving Sets and Mixing* (Morris and Peres, 2003).
- *Finding Sparse Cuts Locally Using Evolving Sets* (Andersen and Peres,
  2009).
- *Almost Optimal Local Graph Clustering Using Evolving Sets* (Andersen et
  al., 2016).
- *Iterative Methods via Locally Evolving Set Process* (Zhou et al., 2024).
- *Accelerated Evolving Set Processes for Local PageRank Computation* (Huang
  et al., 2025).

### Local graph solvers and diffusion

These papers develop local iterative solvers or related graph-diffusion
methods whose work is intended to depend on local structure.

- [*The Divisible Sandpile at Critical Density*](https://arxiv.org/abs/1501.07258)
  (Levine, Murugan, Peres and Ugurcan, *Annales Henri Poincaré*
  17(7):1677–1711, 2016; DOI 10.1007/s00023-015-0433-x) —
  least action, with the conservative physical mapping in `lcp-solvers.md`.
- [*Fast Simulation of Large-Scale Growth Models*](https://arxiv.org/abs/1006.1003)
  (Friedrich and Levine, *Random Structures & Algorithms* 42:185–213,
  2013) — supplied odometer correction; no OP3 runtime import.
- [*p-Norm Flow Diffusion for Local Graph Clustering*](https://proceedings.mlr.press/v119/fountoulakis20a.html)
  (Fountoulakis, Wang and Yang, ICML 2020, PMLR 119:3222–3232) —
  support-local coordinate descent with explicit curvature and degree factors;
  the OP3 parameter check is in `lcp-solvers.md`.
- [*Weighted Flow Diffusion for Local Graph Clustering with Node Attributes: an Algorithm and Statistical Guarantees*](https://proceedings.mlr.press/v202/yang23d.html)
  (Yang and Fountoulakis, ICML 2023, PMLR 202:39252–39276) —
  weighted local push; the stated runtime parameter needs reconciliation
  before an OP3 import.
- [*Local Graph Clustering with Noisy Labels*](https://proceedings.iclr.cc/paper_files/paper/2024/file/a4d991d581accd2955a1e1928f4e6965-Paper-Conference.pdf)
  (Back de Luca, Fountoulakis and Yang, ICLR 2024) — application context;
  its introductory linear-support runtime summary is checked against the
  original theorem in `lcp-solvers.md`.

- [*Maintaining Information in Fully-Dynamic Trees with Top Trees*](https://arxiv.org/pdf/cs/0310065v2)
  (Alstrup, Holm, de Lichtenberg and Thorup, *ACM Transactions on
  Algorithms* 1(2):243–264, 2005) — logarithmically many cluster changes
  per dynamic-tree update. The checked application contract supports the
  local-tree proof draft in `incremental_active_set_sdd`; the balancing
  algorithm is an explicit source import. Journal
  Theorem 2.1 and Sections 2/6 were checked in the published PDF.
- [*Dynamic Planar Convex Hull*](https://arxiv.org/abs/1902.11169)
  (Jacob and Brodal, arXiv:1902.11169v1, 2019; full version of earlier work)
  — individual point updates and extreme queries for stable two-port
  boundary records. It does not provide bulk affine pullback and meld.
- [*Dynamic Geometric Data Structures via Shallow Cuttings*](https://arxiv.org/abs/1903.08387)
  (Chan, arXiv:1903.08387v1, 2019) — Theorem 4.2 supplies dynamic
  three-dimensional extreme queries; a candidate for a bounded third
  retained coordinate, not a general local-solver theorem.
- [*Reversible Markov Chains and Random Walks on Graphs*, Chapter 5, §5.3](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch5.S3.html)
  (online manuscript section dated 23 April 1996) — exact tree edge-hitting
  means and maximal mean bounds. These do not establish the discounted
  path-extremal conjecture in the bounded-attachment OP3 probe.
- *Local Computation of PageRank Contributions* (Andersen et al., 2007).
- *Using PageRank to Locally Partition a Graph* (Andersen, Chung, and Lang,
  2007) - journal treatment of approximate PageRank push, sweep cuts, and
  output-sensitive local partitioning.
- *A Local Clustering Algorithm for Massive Graphs and Its Application to
  Nearly Linear Time Graph Partitioning* (Spielman and Teng, 2013).
- *Local Algorithms for Finding Densely Connected Clusters* (Macgregor and
  Sun, 2021) - personalized-PageRank local clustering for paired,
  densely-interconnected vertex sets.
- *Revisiting Local Computation of PageRank: Simple and Optimal* (Wang et al.,
  2024).
- [*Approximating Single-Source Personalized PageRank with Absolute Error Guarantees*](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICDT.2024.9)
  (Wei, Wen and Yang, ICDT 2024, LIPIcs 290:9:1–9:19;
  DOI 10.4230/LIPIcs.ICDT.2024.9) — degree-normalized sparse-output
  comparison; fixed-alpha and preprocessing assumptions are audited in
  `local-solvers.md` against arXiv:2401.01019v1.
- [*Personalized PageRank Estimation in Undirected Graphs*](https://arxiv.org/abs/2602.10843)
  (Bertram and Jensen, arXiv:2602.10843v1, 11 February 2026 preprint) —
  undirected thresholded-relative estimation and graph-access lower bounds;
  its error, source-average and fixed-alpha scope are in `local-solvers.md`.
- [*Near-Optimality for Single-Source Personalized PageRank*](https://arxiv.org/pdf/2507.14462v5)
  (Jiang, Liu, Luo and Xiao, Proc. ACM Manag. Data 4(2), Article 110,
  May 2026, 55 pages; DOI 10.1145/3801906) — directed SSPPR absolute/relative
  bounds. Checked v5 replaces the earlier title *Tighter Lower Bounds for
  Single Source Personalized PageRank*; see `local-solvers.md` for the
  accuracy/access barriers to OP3 transfer.
- *Fast Online Node Labeling for Very Large Graphs* (Zhou, Sun, and
  Babanezhad Harikandeh, 2023).
- *Faster Local Solvers for Graph Diffusion Equations* (Bai et al., 2024).
- *A Simple Active-Set Method for PageRank-Based Local Graph Clustering* (Wei
  and Yang, 2026) - growing active sets with nearly-linear SDD solves and
  polylogarithmic dependence on the inverse teleportation parameter.

### Spectral graph optimization

These papers connect graph partitioning, spectral sparsification,
preconditioning, and fast solution of graph-structured linear systems.

- [*Algorithmic Meta-Theorems for Graphs of Bounded Vertex Cover*](https://arxiv.org/pdf/0910.0582v2)
  (Lampis, arXiv:0910.0582v2, 2009) — neighborhood-type definitions and
  structural comparison for local frontier response groups; source scope
  in `lcp-solvers.md`. No local PageRank work theorem is imported.
- [*Approximate Gaussian Elimination for Laplacians: Fast, Sparse, and Simple*](https://arxiv.org/abs/1605.02353)
  (Kyng and Sachdeva, arXiv:1605.02353v1, 2016) — source map in `lcp-solvers.md`.
- [*Using Petal-Decompositions to Build a Low Stretch Spanning Tree*](https://www.cs.bgu.ac.il/~neimano/spanning-full1.pdf)
  (Abraham and Neiman, SIAM J. Comput. 48(2):227–248, 2019) —
  arbitrary positive-weight low-stretch trees; checked 2012 author full
  version and precise source scope in `lcp-solvers.md`.
- [*Faster spectral sparsification and numerical algorithms for SDD matrices*](https://arxiv.org/pdf/1209.5821v3)
  (Koutis, Levin and Peng, ACM Trans. Algorithms 12(2), Article 17, 2015;
  DOI 10.1145/2743021) — fixed-precision general spectral sparsification;
  checked source version and recursive-constructor limits in `lcp-solvers.md`.
- [*A Simple, Combinatorial Algorithm for Solving SDD Systems in Nearly-Linear Time*](https://arxiv.org/pdf/1301.6628v1)
  (Kelner, Orecchia, Sidford and Allen Zhu, STOC 2013) — fixed-budget
  random cycle updates and explicit expected error; source scope and the
  supplied resistance-estimation probe are recorded in `lcp-solvers.md`.
- [*User-Friendly Tail Bounds for Sums of Random Matrices*](https://users.cms.caltech.edu/~jtropp/papers/Tro11-User-Friendly-FOCM.pdf)
  (Tropp, Found. Comput. Math. 12:389–434, 2012;
  DOI 10.1007/s10208-011-9099-z) — matrix Chernoff bounds for the
  explicitly charged resistance-sampling confidence wrapper; see `lcp-solvers.md`.

- *Nearly-Linear Time Algorithms for Graph Partitioning, Graph
  Sparsification, and Solving Linear Systems* (Spielman and Teng, 2004).
- *Algorithms, Graph Theory, and Linear Equations in Laplacian Matrices*
  (Spielman, 2010) - survey connecting the main algorithmic primitives.
- *Spectral Sparsification of Graphs* (Spielman and Teng, 2011).
- *Faster Maxflow via Improved Dynamic Spectral Vertex Sparsifiers* (van den
  Brand et al., 2022) - dynamic Schur complements and operator heavy-hitter
  location for electrical flows.

### Complementarity, obstacle, and active-set solvers

The theorem-level OP2 audit, including exact PDF pointers and locality
verdicts, is in [`lcp-solvers.md`](lcp-solvers.md).  No audited source states
the full local theorem; the project note `manuscript/notes/active_edge_lcp/`
now proves OP2 by combining a new threshold-batch Cholesky depth bound with
certified supplied-face SDD solves.

- *On the Solution of Large Quadratic Programming Problems with Bound
  Constraints* (Moré and Toraldo, 1991) - projected-gradient identification
  followed by reduced conjugate gradients.
- *Monotone Multigrid Methods for Elliptic Variational Inequalities I*
  (Kornhuber, 1994) - globally convergent monotone multigrid for finite-element
  obstacle problems.
- *A Block Principal Pivoting Algorithm for Large-Scale Strictly Monotone
  Linear Complementarity Problems* (Júdice and Pires, 1994) - finite guarded
  block pivots.
- *Augmented Lagrangian Active Set Methods for Obstacle Problems*
  (Kärkkäinen, Kunisch, and Tarvainen, 2003) - Stieltjes obstacle active sets
  and multilevel implementations.
- [*A Fully Dynamic Algorithm for Modular Decomposition and Recognition of Cographs*](https://www.cs.tau.ac.il/~roded/articles/cmd.pdf)
  (Shamir and Sharan, Discrete Applied Mathematics 136(2–3):329–340, 2004) -
  degree-paid graph-structure maintenance; response-update obligations are
  separately audited in `lcp-solvers.md`.
- *Pivoting in Linear Complementarity: Two Polynomial-Time Cases* (Foniok et
  al., 2009) - linear pivot-path bounds for K-matrix LCPs.
- *Some Convergence Results for Howard's Algorithm* (Bokanowski, Maroso, and
  Zidani, 2009) - at most linearly many global obstacle-policy solves.
- [*Lipschitz Unimodal and Isotonic Regression on Paths and Trees*](https://www.cs.toronto.edu/~sadri/publications/regression.pdf)
  (Agarwal, Phillips, and Sadri; author manuscript, 2010) - affine composition
  trees for implicit scalar response curves; OP3 import audit in `lcp-solvers.md`.
- [*Total Generalized Variation on a Tree*](https://epubs.siam.org/doi/10.1137/23M1556915)
  (Kuric, Ahmetspahic, and Pock, 2024) - explicit piecewise-quadratic tree
  messages; comparison for the affine-response probe.
- *A Nearly-m log n Time Solver for SDD Linear Systems* (Koutis, Miller, and
  Peng, 2011) - nearly-linear solution of a supplied SDD system; the OP3
  note applies it to a locally assembled sparse coarse system with explicit
  residual certification (application audit in `lcp-solvers.md`).
- *Superrelaxation and the Rate of Convergence in Minimizing Quadratic
  Functions Subject to Bound Constraints* (Dostál, Domorádová, and Sadowská,
  2011) - projected-gradient/CG working-set convergence rates.
- [*ℓ2-Norm Flow Diffusion in Near-Linear Time*](https://arxiv.org/pdf/2105.14629v2)
  (Chen, Peng, and Wang, 2021) - global constrained diffusion; an OP3
  localization candidate with a numerical-range obligation, audited in
  [`lcp-solvers.md`](lcp-solvers.md#chen-peng-and-wang-2021-constrained-diffusion-and-the-op3-alternative).
- [*Almost-Linear Time Algorithms for Incremental Graphs: Cycle Detection,
  SCCs, s-t Shortest Path, and Minimum-Cost Flow*](https://arxiv.org/pdf/2311.18295v1)
  (Chen, Kyng, Liu, Meierhans, and Probst Gutenberg, 2023 preprint) -
  thresholded incremental flow; subpolynomial overhead and no direct OP3
  coordinate certificate. Scoped audit in `lcp-solvers.md`.
- [*Almost-Linear Time Algorithms for Decremental Graphs: Min-Cost Flow and
  More via Duality*](https://arxiv.org/pdf/2407.10830v1)
  (van den Brand, Chen, Kyng, Liu, Meierhans, Probst Gutenberg, and Sachdeva,
  FOCS 2024 preprint) - decremental thresholded flow and approximate value
  maintenance; scoped OP3 comparison in `lcp-solvers.md`.
- *Non-Negative Conjugate Gradients* (Schmelzer and Stoll, 2026) - inexact
  matrix-free CG inside a guarded active-set loop.
- *Fully Dynamic Spectral Vertex Sparsifiers and Applications* (Durfee, Gao,
  Goranci, and Peng, 2019) - dynamic terminal additions and Laplacian queries
  after full-graph Schur preprocessing.
- *Dynamic Matrix Inverse: Improved Algorithms and Matching Conditional Lower
  Bounds* (van den Brand, Nanongkai, and Saranurak, 2019) - dense dynamic
  inverse maintenance with ambient preprocessing/update/query costs.

### Acceleration and sparse PageRank

These papers study accelerated, sparse, or complexity-improved methods for
PageRank and related local problems.

- *A Fast Iterative Shrinkage-Thresholding Algorithm for Linear Inverse
  Problems* (Beck and Teboulle, 2009) - FISTA and its composite convergence
  analysis; a motivating algorithm in the COLT 2022 question.
- *Linear Coupling: An Ultimate Unification of Gradient and Mirror Descent*
  (Allen-Zhu and Orecchia, 2017) - coupling primal and auxiliary progress;
  another explicit motivation in the COLT 2022 question.
- *Catalyst Acceleration for First-order Convex Optimization: From Theory to
  Practice* (Lin, Mairal, and Harchaoui, 2018) - general outer acceleration
  framework.
- *A Universal Catalyst for First-Order Optimization* (Lin, Mairal, and
  Harchaoui, 2015) - original NeurIPS presentation of the Catalyst framework.
- *A Note on the Optimal Convergence Rate of Descent Methods with Fixed Step
  Sizes for Smooth Strongly Convex Functions* (Uschmajew and Vandereycken,
  2022) - sharp rates for variable-metric and inexact-gradient methods.
- *Open Problem: Running Time Complexity of Accelerated
  ℓ1-Regularized PageRank* (Fountoulakis and Yang, 2022).
- *Accelerated and Sparse Algorithms for Approximate Personalized PageRank
  and Beyond* (Martínez-Rubio, Wirth, and Pokutta, 2023).
- *Accelerating Personalized PageRank Vector Computation* (Chen et al.,
  2023).
- *Efficient Numerical Methods to Solve Sparse Linear Equations with
  Application to PageRank* (Anikin et al., 2022) - sparse simplex
  optimization methods for global PageRank.
- *Complexity of Classical Acceleration for ℓ1-Regularized PageRank*
  (Fountoulakis and Martínez-Rubio, 2026).
- *A Coordinate Gradient Descent Method for Nonsmooth Separable
  Minimization* (Tseng and Yun, 2009) - block coordinate updates for composite
  objectives.
- *Adaptive Restart for Accelerated Gradient Schemes* (O'Donoghue and Candès,
  2015) - observable restart rules for accelerated first-order methods.
- *Breaking Locality Accelerates Block Gauss-Seidel* (Tu et al., 2017) -
  acceleration under random block sampling.
- *A Simple Active-Set Method for PageRank-Based Local Graph Clustering* (Wei
  and Yang, 2026) - an alternative accuracy/locality tradeoff whose repeated
  nested-SDD factor is the subject of a project reuse note.

### Sublinear algorithms and access models

These papers provide general query-model and approximation foundations for
algorithms whose work is smaller than the full input size.

- *Sublinear Time Algorithms* (Rubinfeld and Shapira, 2011).
- *Space-Efficient Local Computation Algorithms* (Alon et al., 2012) -
  consistent query-local computation with polylogarithmic time and storage.

### Statistical guarantees

These papers analyze recovery or statistical behavior rather than only
worst-case algorithmic complexity.

- *Statistical Guarantees for Local Graph Clustering* (Ha, Fountoulakis, and
  Mahoney, 2021).

### PageRank applications and fairness

These papers adapt PageRank scores or PageRank-based optimization models to
downstream ranking requirements.

- *FairRARI: A Plug and Play Framework for Fairness-Aware PageRank*
  (Kariotakis and Konar, 2026) - fairness-constrained PageRank optimization.

## Master catalog

| Year | Venue | Paper | BibTeX key | Primary area |
| --- | --- | --- | --- | --- |
| 1991 | SIOPT | *On the Solution of Large Quadratic Programming Problems with Bound Constraints* | `more1991solution` | Bound-constrained optimization |
| 1994 | Numer. Math. | *Monotone Multigrid Methods for Elliptic Variational Inequalities I* | `kornhuber1994monotone` | Obstacle solvers |
| 1994 | COR | *A Block Principal Pivoting Algorithm for Large-Scale Strictly Monotone Linear Complementarity Problems* | `judice1994block` | Complementarity solvers |
| 2003 | STOC | *Evolving Sets and Mixing* | `morris2003evolving` | Evolving-set foundations |
| 2003 | JOTA | *Augmented Lagrangian Active Set Methods for Obstacle Problems* | `karkkainen2003augmented` | Obstacle solvers |
| 2004 | STOC | *Nearly-Linear Time Algorithms for Graph Partitioning, Graph Sparsification, and Solving Linear Systems* | `spielman2004nearly` | Spectral graph optimization |
| 2006 | FOCS | *Local Graph Partitioning Using PageRank Vectors* | `andersen2006local` | PageRank foundations |
| 2007 | PNAS | *The Heat Kernel as the PageRank of a Graph* | `chung2007heat` | Heat-kernel PageRank |
| 2007 | WAW | *Local Computation of PageRank Contributions* | `andersen2007localcontributions` | Local PageRank computation |
| 2007 | IM | [*Using PageRank to Locally Partition a Graph*](../../papers/2007-im-andersen-using-pagerank-locally-partition-graph.pdf) | `andersen2007using` | Local graph clustering |
| 2009 | SIIMS | [*A Fast Iterative Shrinkage-Thresholding Algorithm for Linear Inverse Problems*](../../papers/2009-siims-beck-fast-iterative-shrinkage-thresholding-linear-inverse-problems.pdf) | `beck2009fast` | Acceleration |
| 2009 | MP | [*A Coordinate Gradient Descent Method for Nonsmooth Separable Minimization*](../../papers/2009-mp-tseng-coordinate-gradient-descent-nonsmooth-separable-minimization.pdf) | `tseng2009coordinate` | Coordinate optimization |
| 2009 | DCG | *Pivoting in Linear Complementarity: Two Polynomial-Time Cases* | `foniok2009pivoting` | Complementarity solvers |
| 2009 | IM | *A Local Graph Partitioning Algorithm Using Heat Kernel PageRank* | `chung2009local` | Heat-kernel PageRank |
| 2009 | STOC | *Finding Sparse Cuts Locally Using Evolving Sets* | `andersen2009finding` | Evolving-set methods |
| 2010 | ICM | *Algorithms, Graph Theory, and Linear Equations in Laplacian Matrices* | `spielman2010algorithms` | Spectral graph optimization |
| 2011 | FOCS | [*A Nearly-m log n Time Solver for SDD Linear Systems*](../../papers/2011-focs-koutis-nearly-m-log-n-time-solver-sdd-linear-systems.pdf) | `koutis2011nearly` | Spectral graph optimization |
| 2011 | COAP | *Superrelaxation and the Rate of Convergence in Minimizing Quadratic Functions Subject to Bound Constraints* | `dostal2011superrelaxation` | Bound-constrained optimization |
| 2011 | SICOMP | *Spectral Sparsification of Graphs* | `spielman2011spectral` | Spectral graph optimization |
| 2011 | SIDMA | [*Sublinear Time Algorithms*](../../papers/2011-sidma-rubinfeld-sublinear-time-algorithms.pdf) | `rubinfeld2011sublinear` | Sublinear algorithms |
| 2012 | SODA | [*Space-Efficient Local Computation Algorithms*](../../papers/2012-soda-alon-space-efficient-local-computation-algorithms.pdf) | `alon2012space` | Local computation algorithms |
| 2013 | SICOMP | *A Local Clustering Algorithm for Massive Graphs and Its Application to Nearly Linear Time Graph Partitioning* | `spielman2013local` | Local graph clustering |
| 2015 | FoCM | [*Adaptive Restart for Accelerated Gradient Schemes*](../../papers/2015-focm-odonoghue-adaptive-restart-accelerated-gradient-schemes.pdf) | `odonoghue2015adaptive` | Acceleration |
| 2015 | NeurIPS | [*A Universal Catalyst for First-Order Optimization*](../../papers/2015-neurips-lin-universal-catalyst-first-order-optimization.pdf) | `lin2015universal` | Acceleration |
| 2016 | JACM | *Almost Optimal Local Graph Clustering Using Evolving Sets* | `andersen2016almost` | Evolving-set methods |
| 2017 | ICML | [*Breaking Locality Accelerates Block Gauss-Seidel*](../../papers/2017-icml-tu-breaking-locality-accelerates-block-gauss-seidel.pdf) | `tu2017breaking` | Acceleration |
| 2017 | ITCS | [*Linear Coupling: An Ultimate Unification of Gradient and Mirror Descent*](../../papers/2017-itcs-allen-zhu-linear-coupling-gradient-mirror-descent.pdf) | `allenzhu2017linear` | Acceleration |
| 2018 | JMLR | [*Catalyst Acceleration for First-order Convex Optimization: From Theory to Practice*](../../papers/2018-jmlr-lin-catalyst-acceleration-first-order-convex-optimization.pdf) | `lin2018catalyst` | Acceleration |
| 2019 | MP | *Variational Perspective on Local Graph Clustering* | `fountoulakis2019variational` | PageRank formulations |
| 2021 | JMLR | [*Statistical Guarantees for Local Graph Clustering*](../../papers/2021-jmlr-ha-statistical-guarantees-local-graph-clustering.pdf) | `ha2021statistical` | Statistical guarantees |
| 2021 | ICML | [*Local Algorithms for Finding Densely Connected Clusters*](../../papers/2021-icml-macgregor-local-algorithms-finding-densely-connected-clusters.pdf) | `macgregor2021local` | Local graph clustering |
| 2022 | COLT | [*Open Problem: Running Time Complexity of Accelerated ℓ1-Regularized PageRank*](../../papers/2022-colt-fountoulakis-running-time-complexity-accelerated-l1-regularized-pagerank.pdf) | `fountoulakis2022open` | Acceleration |
| 2022 | JOTA | [*A Note on the Optimal Convergence Rate of Descent Methods with Fixed Step Sizes for Smooth Strongly Convex Functions*](../../papers/2022-jota-uschmajew-optimal-convergence-descent-fixed-step-smooth-strongly-convex.pdf) | `uschmajew2022note` | First-order convergence |
| 2022 | OMS | [*Efficient Numerical Methods to Solve Sparse Linear Equations with Application to PageRank*](../../papers/2022-oms-anikin-efficient-numerical-methods-sparse-linear-equations-pagerank.pdf) | `anikin2022efficient` | Sparse PageRank optimization |
| 2022 | STOC | [*Faster Maxflow via Improved Dynamic Spectral Vertex Sparsifiers*](../../papers/2022-stoc-brand-faster-maxflow-dynamic-spectral-vertex-sparsifiers.pdf) | `brand2022faster` | Dynamic spectral graph optimization |
| 2023 | COLT | [*Accelerated and Sparse Algorithms for Approximate Personalized PageRank and Beyond*](../../papers/2023-colt-martinez-rubio-accelerated-sparse-algorithms-approximate-personalized-pagerank-beyond.pdf) | `martinezrubio2023accelerated` | Acceleration |
| 2023 | ICML | [*Fast Online Node Labeling for Very Large Graphs*](../../papers/2023-icml-zhou-fast-online-node-labeling-very-large-graphs.pdf) | `zhou2023fast` | Local graph solvers |
| 2023 | KDD | *Accelerating Personalized PageRank Vector Computation* | `chen2023accelerating` | Acceleration |
| 2024 | NeurIPS | [*Faster Local Solvers for Graph Diffusion Equations*](../../papers/2024-neurips-bai-faster-local-solvers-graph-diffusion-equations.pdf) | `bai2024faster` | Local graph solvers |
| 2024 | NeurIPS | [*Iterative Methods via Locally Evolving Set Process*](../../papers/2024-neurips-zhou-iterative-methods-locally-evolving-set-process.pdf) | `zhou2024iterative` | Evolving-set methods |
| 2024 | STOC | [*Revisiting Local Computation of PageRank: Simple and Optimal*](../../papers/2024-stoc-wang-revisiting-local-computation-pagerank-simple-optimal.pdf) | `wang2024revisiting` | Local PageRank computation |
| 2024 | TKDE | *Efficient Algorithms for Personalized PageRank Computation: A Survey* | `yang2024efficient` | PageRank foundations |
| 2025 | NeurIPS | [*Accelerated Evolving Set Processes for Local PageRank Computation*](../../papers/2025-neurips-huang-accelerated-evolving-set-processes-local-pagerank.pdf) | `huang2025accelerated` | Evolving sets and acceleration |
| 2026 | ICML | [*FairRARI: A Plug and Play Framework for Fairness-Aware PageRank*](../../papers/2026-icml-kariotakis-fairrari-fairness-aware-pagerank.pdf) | `kariotakis2026fairrari` | PageRank applications and fairness |
| 2026 | arXiv | [*Complexity of Classical Acceleration for ℓ1-Regularized PageRank*](../../papers/2026-arxiv-fountoulakis-complexity-classical-acceleration-l1-regularized-pagerank.pdf) | `fountoulakis2026complexity` | Acceleration |
| 2026 | arXiv | *A Simple Active-Set Method for PageRank-Based Local Graph Clustering* | `wei2026simple` | Local graph solvers |
| 2026 | arXiv | *Non-Negative Conjugate Gradients* | `schmelzer2026nonnegative` | Complementarity solvers |

## Suggested reading paths

### Local PageRank foundations

1. Andersen, Chung, and Lang (2006).
2. Fountoulakis et al. (2019).
3. Yang et al. (2024).

### Evolving sets toward AESP

1. Morris and Peres (2003).
2. Andersen and Peres (2009).
3. Andersen et al. (2016).
4. Zhou et al. (2024).
5. Huang et al. (2025).

### Acceleration toward the hybrid solver

1. Tseng and Yun (2009).
2. Lin, Mairal, and Harchaoui (2015).
3. O'Donoghue and Candès (2015).
4. Tu et al. (2017).
5. Lin, Mairal, and Harchaoui (2018).
6. Uschmajew and Vandereycken (2022).
7. Fountoulakis and Yang (2022).
8. Martínez-Rubio, Wirth, and Pokutta (2023).
9. Chen et al. (2023).
10. Huang et al. (2025).
11. Fountoulakis and Martínez-Rubio (2026).

### Local solver comparisons

1. Andersen et al. (2007).
2. Andersen, Chung, and Lang (2007).
3. Spielman and Teng (2013).
4. Macgregor and Sun (2021).
5. Zhou, Sun, and Babanezhad Harikandeh (2023).
6. Wang et al. (2024).
7. Bai et al. (2024).
8. Zhou et al. (2024).
9. Huang et al. (2025).

### Spectral graph optimization foundations

1. Spielman and Teng (2004).
2. Spielman (2010).
3. Spielman and Teng (2013).
4. Spielman and Teng (2011).
5. van den Brand et al. (2022).

### Obstacle/LCP route to OP2

1. Moré and Toraldo (1991).
2. Kornhuber (1994).
3. Júdice and Pires (1994).
4. Kärkkäinen, Kunisch, and Tarvainen (2003).
5. Foniok et al. (2009).
6. Bokanowski, Maroso, and Zidani (2009).
7. Koutis, Miller, and Peng (2011).
8. Durfee et al. (2019).
9. van den Brand, Nanongkai, and Saranurak (2019).
10. Wei and Yang (2026).
11. Schmelzer and Stoll (2026).

### PageRank applications

1. Kariotakis and Konar (2026).

### Sublinear and local computation foundations

1. Rubinfeld and Shapira (2011).
2. Alon et al. (2012).

## Maintenance

- Add each new paper to one primary area and cross-list it only where useful.
- Keep detailed theorem, equation, and experiment notes in the topic files,
  not in this index.
- Use the formal venue after publication; use `arXiv` while a paper remains a
  preprint.
- Update the Fountoulakis and Martínez-Rubio 2026 arXiv entry, filename, and
  BibTeX record after formal publication.

## Publication review, 9 September 2026

[OP1/OP2 novelty comparison](publication-review-20260909.md) integrates additional local-diffusion, SSPPR, scalar-query, flow-diffusion and M-matrix predecessors into the active paper. [Focused 2026 review](publication-review-20260909-rppr.md) and [broader search](publication-review-20260909-broad.md) retain source and search details. These sources are also indexed in `manuscript/ARXIV_SOURCES.json`.
