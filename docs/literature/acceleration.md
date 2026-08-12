# Acceleration

## Scope

This note covers outer acceleration frameworks and accelerated local graph
methods relevant to the proposed hybrid solver. Catalyst and AESP are current
starting points, but their applicability has not yet been established.

## Questions for comparison

- What objective, operator, or monotonicity assumptions are required?
- What inner-solver accuracy schedule is assumed?
- How is inexactness measured and propagated?
- Does acceleration require global work or dense state?
- Can warm starts and local active sets be preserved?
- What condition number or `alpha` dependence is improved?
- Does the theoretical accuracy measure match the implemented stopping rule?

## Source annotations

## Citation key: `martinezrubio2023accelerated`

- Citation: David Martínez-Rubio, Elias Wirth, and Sebastian Pokutta.
  “Accelerated and Sparse Algorithms for Approximate Personalized PageRank and
  Beyond.” *Proceedings of the 36th Conference on Learning Theory*, PMLR
  195:2852-2876, 2023.
- DOI/arXiv/URL: <https://doi.org/10.48550/arXiv.2303.12875>;
  arXiv `2303.12875v1`;
  <https://proceedings.mlr.press/v195/martinez-rubio23b.html>.
- Local PDF:
  `papers/2023-colt-martinez-rubio-accelerated-sparse-algorithms-approximate-personalized-pagerank-beyond.pdf`.
- Source-faithful reader archive:
  `manuscript/archive/colt-2023-accelerated-sparse-appr/`.
- Relevance: The paper proposes an exact conjugate-directions PageRank method
  (CDPR) and an accelerated sparse active-set method (ASPR) for nonnegative
  quadratics with symmetric positive-definite M-matrix Hessians. Its geometry
  and retraction arguments are directly relevant to safe support expansion,
  while its repeated full-gradient scans expose a locality cost that a hybrid
  solver must account for explicitly.
- Exact pointers:
  - arXiv v1 PDF pages 4-5, Section 2 and Equations (1)-(6): define the graph
    volumes, PageRank matrix, ℓ1-regularized objective, nonnegative quadratic
    reformulation, and KKT conditions. The printed expansion in Equation (4)
    is algebraically inconsistent with its defining equality and must not be
    reused without correction and documentation.
  - arXiv v1 PDF pages 6-7, Proposition 2: establish monotone restricted
    minimizers, strict positivity of exposed coordinates, and support
    containment for M-matrix quadratics.
  - arXiv v1 PDF pages 8-9, Algorithm 2 and Theorems 3-4: define CDPR and state
    exact correctness plus
    `O(|S*|^3 + |S*| vol(S*))` time and `O(|S*|^2)` space.
  - arXiv v1 PDF pages 9-11, Algorithm 3, Proposition 5, Lemma 6, Algorithm 4,
    and Theorems 7-8: define the accelerated inner solve and ASPR, prove
    support containment and an objective-gap guarantee, and state the sparse
    accelerated complexity.
  - arXiv v1 PDF pages 18-23, Appendix A: give the deferred proofs; the proof
    of Lemma 6 on pages 19-20 prints a degree denominator inconsistent with
    Equation (1), although that step uses only the off-diagonal sign.
  - arXiv v1 PDF page 23, Appendix B: compare the stated CDPR, ASPR, and ISTA
    complexities. The paper contains no computational experiments.
- Formulation differences: The source uses ε for objective gap and exact sign
  tests for active-set expansion; it specifies no residual-based stopping
  criterion or finite-precision tolerance. Its volume includes selected-set
  cardinality and its algorithms inspect full gradients. `ASPR` in this paper
  is not AESP. The active project uses a corrected source-aligned RPPR
  objective and distinct accuracy namespaces.
- Open questions: Reverify Equation (4) and the cited support-volume result;
  translate the objective-gap guarantee into any adopted residual convention;
  determine whether negative-gradient discovery can be localized without the
  full-gradient volume charge; and audit the sparse operation counts under an
  executable access model.

## Citation key: `fountoulakis2026complexity`

- Citation: Kimon Fountoulakis and David Martínez-Rubio. “Complexity of
  Classical Acceleration for \(\ell_1\)-Regularized PageRank.” arXiv
  `2602.21138v2`, 2026.
- DOI/arXiv/URL: <https://doi.org/10.48550/arXiv.2602.21138>;
  <https://arxiv.org/abs/2602.21138>.
- Local PDF:
  `papers/2026-arxiv-fountoulakis-complexity-classical-acceleration-l1-regularized-pagerank.pdf`.
- Source-faithful reader archive:
  `manuscript/archive/arxiv-2026-classical-acceleration-rppr/`.
- Relevance: The paper gives a source-compatible RPPR objective, classical
  FISTA iteration, degree-weighted work model, conditional locality bound
  under boundary confinement, and a star-graph lower bound showing that
  standard FISTA can be asymptotically worse than ISTA.
- Exact pointers:
  - PDF page 3, Section 3 and equation (RPPR): define graph/set notation,
    \(Q\), \(f\), \(F_\rho\), the optimal support, and coordinatewise KKT
    conditions.
  - PDF page 4, Section 3.1 and equations (FISTA), (2), and (3): define
    \(L,\mu,\eta,\beta\), the FISTA iterates, weighted soft thresholding, and
    degree-weighted per-iteration work.
  - PDF pages 4-5, Sections 4.1-4.2 and equations (4)-(6): define the
    over-regularized A/B problems, spurious active sets, complementarity
    margins, and the work decomposition.
  - PDF pages 5-6, Theorems 4.3-4.4: state the conditional total-work bound
    and the boundary no-percolation condition.
  - PDF pages 18-23, Appendix D: construct the star-graph lower bound where
    FISTA activates a high-degree center while ISTA remains local.
  - PDF page 24, Appendix E, “Stopping criterion”: define the unit-step
    proximal fixed-point residual used in all experiments.
- Formulation differences: The paper uses plain italic vector/matrix symbols
  and studies undirected unweighted graphs with \(s=e_v\). It overloads
  \(\varepsilon\): theory uses an objective-gap target while experiments use a
  proximal fixed-point residual tolerance. The active manuscript now
  distinguishes these as \(\varepsilon_{\mathrm{obj}}\) and
  \(\varepsilon_{\mathrm{pg}}\). Neither residual nor its conversion to the
  project's PageRank error has yet been adopted implementation-wide.
- Open questions: Prove a conversion between the proximal fixed-point
  residual and the project's eventual PageRank accuracy convention; determine
  whether the hybrid method preserves boundary confinement; and compare the
  paper's degree-weighted work with edge-operation accounting for local inner
  solves.

## Citation key: `lin2018catalyst`

- Citation: Hongzhou Lin, Julien Mairal, and Zaid Harchaoui. “Catalyst
  Acceleration for First-order Convex Optimization: From Theory to Practice.”
  *Journal of Machine Learning Research*, 18(212):1-54, 2018.
- DOI/arXiv/URL: <https://jmlr.org/papers/v18/17-748.html>; preprint
  <https://arxiv.org/abs/1712.05654>.
- Local PDF:
  `papers/2018-jmlr-lin-catalyst-acceleration-first-order-convex-optimization.pdf`.
- Relevance: Catalyst is the principal generic outer-acceleration framework in
  the project's research plan. It approximately solves a sequence of
  regularized auxiliary problems, using explicit inner stopping criteria and
  warm starts to accelerate a base method with linear convergence on strongly
  convex objectives.
- Exact pointers:
  - Pages 5-6, Section 1.2 and Algorithm 1: give the two-loop Catalyst overview,
    auxiliary objective, extrapolation, and outer momentum.
  - Pages 7-10, Section 2 and Proposition 1: interpret Catalyst through the
    Moreau envelope and formulate approximate proximal subproblem solutions.
  - Pages 10-13, Section 3 and Algorithm 2: state the full method, its two inner
    accuracy criteria, warm starts, and parameter choices.
  - Pages 14-20, Section 4.1 and Theorems 3 and 7: analyze outer-loop
    convergence under the two inexactness criteria.
  - Pages 20-29, Sections 4.2-4.3, Corollaries 13 and 16, and Propositions
    17-18: analyze warm-started inner work and combine it with outer
    convergence into global complexity bounds.
  - Pages 30-49, Section 5: compare stopping criteria, warm starts, and Catalyst
    variants experimentally.
- Formulation differences: Catalyst assumes a convex composite objective and
  a base method with a global linear-convergence model on strongly convex
  subproblems. The hybrid local solver must also preserve sparse support,
  locality-sensitive work, and the repository's residual convention; these
  properties are not guaranteed by Catalyst's function-gap or duality-gap
  criteria.
- Open questions: Derive a valid conversion from the hybrid solver's residual
  to Catalyst's inner accuracy criteria, determine whether warm starts preserve
  the active set, and account for outer-loop extrapolation and auxiliary
  regularization without introducing global dense work.

## Citation key: `uschmajew2022note`

- Citation: André Uschmajew and Bart Vandereycken. “A Note on the Optimal
  Convergence Rate of Descent Methods with Fixed Step Sizes for Smooth Strongly
  Convex Functions.” *Journal of Optimization Theory and Applications*,
  194(1):364-373, 2022.
- DOI/arXiv/URL: <https://doi.org/10.1007/s10957-022-02032-z>; preprint
  <https://arxiv.org/abs/2106.08020>.
- Local PDF:
  `papers/2022-jota-uschmajew-optimal-convergence-descent-fixed-step-smooth-strongly-convex.pdf`.
- Relevance: This note derives sharp function-value contraction factors for
  fixed-step descent methods by viewing variable-metric, gradient-related, and
  inexact-gradient steps in suitable inner products. The results offer compact
  tools for analyzing hybrid updates whose directions or gradients differ from
  exact Euclidean gradient descent.
- Exact pointers:
  - Pages 364-366, Section 1 and Equations (1.1)-(1.4): state the optimal
    fixed-step contraction factor for smooth strongly convex objectives and
    motivate function-value analysis.
  - Pages 366-367, Section 2 and Theorem 2.1: give the variable-metric rate in
    terms of objective and metric condition numbers.
  - Pages 368-371, Section 3, Lemma 3.1, and Theorems 3.2 and 3.4: treat
    gradient-related directions under angle and scaling conditions.
  - Pages 371-372, Section 4, Lemma 4.1, and Theorem 4.2: derive the sharp
    fixed-step rate for gradients with bounded relative error.
  - Page 373, Section 5: summarizes the metric-change proof strategy and its
    scope.
- Formulation differences: The analysis assumes a globally smooth,
  strongly-convex objective and measures function-value contraction. The
  project uses graph-structured PageRank objectives, residual stopping, sparse
  active sets, and locality-sensitive work, so smoothness, strong convexity,
  and error bounds must be translated into the repository's normalization and
  residual conventions.
- Open questions: Express local truncation or stale-coordinate effects as the
  relative gradient error in Theorem 4.2, determine whether active-set updates
  satisfy the angle/scaling conditions of Section 3, and compare the resulting
  sharp rate with Catalyst and coordinate-local convergence bounds.

## Citation key: `tseng2009coordinate`

- Citation: Paul Tseng and Sangwoon Yun. “A Coordinate Gradient Descent Method
  for Nonsmooth Separable Minimization.” *Mathematical Programming*,
  117(1-2):387-423, 2009.
- DOI/arXiv/URL: <https://doi.org/10.1007/s10107-007-0170-0>.
- Local PDF:
  `papers/2009-mp-tseng-coordinate-gradient-descent-nonsmooth-separable-minimization.pdf`.
- Relevance: This paper develops block coordinate gradient descent for a
  smooth objective plus a separable convex term. It provides a foundational
  convergence framework for local block choices, Gauss-Seidel or
  Gauss-Southwell selection, and error-bound-based linear convergence.
- Exact pointers:
  - Manuscript pages 4-9, Section 2: define the composite problem, block
    quadratic model, coordinate update, and admissible block-selection rules.
  - Manuscript pages 10-15, Section 3: characterize stationarity through the
    block displacement and establish the core comparison lemmas.
  - Manuscript pages 16-19, Section 4: prove global convergence of the method.
  - Manuscript pages 19-27, Section 5: use a local Lipschitzian error bound to
    derive local linear convergence.
  - Manuscript pages 27-31, Section 6: give error-bound conditions covering
    polyhedral regularizers and structured smooth terms.
- Formulation differences: The method permits general separable regularizers
  and block rules but does not impose a graph-local access model or count
  explored edges. Its linear rate is asymptotic and error-bound based, whereas
  this project uses an explicit PageRank residual and locality-sensitive work.
- Open questions: Express the hybrid solver's update as the paper's block
  model, determine whether its active-set rule satisfies the generalized
  Gauss-Southwell condition, and translate the local error bound into the
  repository's residual convention.

## Citation key: `tu2017breaking`

- Citation: Stephen Tu, Shivaram Venkataraman, Ashia C. Wilson, Alex Gittens,
  Michael I. Jordan, and Benjamin Recht. “Breaking Locality Accelerates Block
  Gauss-Seidel.” *Proceedings of the 34th International Conference on Machine
  Learning*, PMLR 70:3482-3491, 2017.
- DOI/arXiv/URL: <https://proceedings.mlr.press/v70/tu17a.html>; preprint
  <https://arxiv.org/abs/1701.03863>.
- Local PDF:
  `papers/2017-icml-tu-breaking-locality-accelerates-block-gauss-seidel.pdf`.
- Relevance: The paper shows that random coordinate blocks can outperform any
  fixed partition even without acceleration, then analyzes accelerated random
  block Gauss-Seidel through data-dependent parameters. This directly exposes
  the tradeoff between computational locality, block selection, and momentum.
- Exact pointers:
  - Preprint pages 1-4, Sections 1-2: define fixed-partition and random-block
    sampling and their convergence parameters.
  - Preprint pages 4-6, Section 3.1 and Propositions 3.1-3.3: construct
    instances where breaking the fixed partition gives an arbitrarily better
    rate.
  - Preprint pages 6-9, Section 3.2, Algorithm 1, and Theorems 3.4-3.7: give
    the Lyapunov analysis for accelerated block Gauss-Seidel and Kaczmarz.
  - Preprint pages 9-11, Section 3.3 and Lemma 3.8: specialize the accelerated
    rate to random coordinate sampling and well-conditioned sub-blocks.
  - Preprint pages 14-20, Section 5: compare sampling strategies,
    conjugate-gradient, and block sizes empirically.
- Formulation differences: The paper solves global positive-definite linear
  systems and treats locality primarily as cache locality. The project seeks
  seed-local graph diffusion with sparse state and edge-local work, so random
  blocks that touch the full coordinate universe may violate its locality
  objective.
- Open questions: Separate cache locality from graph locality in the work
  model, test whether random blocks can be sampled inside an evolving active
  set, and determine whether the paper's acceleration parameters can be
  bounded using local graph structure.

## Citation key: `odonoghue2015adaptive`

- Citation: Brendan O'Donoghue and Emmanuel Candès. “Adaptive Restart for
  Accelerated Gradient Schemes.” *Foundations of Computational Mathematics*,
  15(3):715-732, 2015.
- DOI/arXiv/URL: <https://doi.org/10.1007/s10208-013-9150-3>; preprint
  <https://arxiv.org/abs/1204.3982>.
- Local PDF:
  `papers/2015-focm-odonoghue-adaptive-restart-accelerated-gradient-schemes.pdf`.
- Relevance: This paper introduces function-value and gradient-based restart
  tests that reset momentum when observable behavior indicates overshoot. It
  is directly relevant to a hybrid solver that must decide online when
  acceleration is helping without knowing a global or local condition number.
- Exact pointers:
  - Pages 716-719, Sections 1-2 and Algorithms 1-2: review accelerated
    gradient schemes, their momentum parameters, and sensitivity to an
    inaccurate strong-convexity estimate.
  - Pages 719-722, Section 3 and Algorithm 3: derive the fixed restart scale
    and introduce the function and gradient adaptive restart conditions.
  - Pages 722-727, Section 4: analyze quadratic dynamics, observable
    oscillations, and convergence under adaptive restart.
  - Pages 727-731, Section 5 and Algorithms 4-6: demonstrate restart with
    log-sum-exp, FISTA for sparse regression, and projected acceleration for
    quadratic programming.
- Formulation differences: The adaptive rules are heuristic for general
  objectives, use global objective or gradient information, and do not track
  graph support or edge-local work. A local implementation may not have enough
  information to evaluate the published restart tests exactly.
- Open questions: Develop a restart signal from the repository's local
  residual, determine whether a restricted active-set objective is a reliable
  proxy for the global function test, and measure whether restart preserves
  sparse support while improving edge-operation complexity.

## Citation key: `lin2015universal`

- Citation: Hongzhou Lin, Julien Mairal, and Zaid Harchaoui. “A Universal
  Catalyst for First-Order Optimization.” *Advances in Neural Information
  Processing Systems 28*, pages 3384-3392, 2015.
- DOI/arXiv/URL:
  <https://proceedings.neurips.cc/paper/2015/hash/c164bbc9d6c72a52c599bbb43d8db8e1-Abstract.html>;
  preprint <https://arxiv.org/abs/1506.02186>.
- Local PDF:
  `papers/2015-neurips-lin-universal-catalyst-first-order-optimization.pdf`.
- Relevance: This is the original conference presentation of Catalyst. It
  wraps a linearly convergent base method around approximately solved,
  quadratically regularized subproblems and accelerates their outer sequence
  through extrapolation.
- Exact pointers:
  - Preprint pages 1-2, Section 1: define the composite objective and motivate
    acceleration of batch, coordinate, and finite-sum base methods.
  - Preprint pages 3-4, Section 2 and Algorithm 1: specify the auxiliary
    objectives, extrapolation, and inner accuracy schedule.
  - Preprint pages 4-7, Section 3, Theorems 3.1 and 3.3, and Propositions 3.2
    and 3.4: give outer convergence and inner-loop complexity for strongly
    convex and convex objectives.
  - Preprint pages 7-9, Section 4: instantiate Catalyst for existing methods
    and introduce proximal MISO.
- Relationship to other library entries: The 2018 JMLR paper
  `lin2018catalyst` is the expanded journal treatment, with more complete
  stopping-criterion, warm-start, and experimental analysis. This NeurIPS
  article is retained separately as the original formal publication.
- Formulation differences: Catalyst assumes globally defined composite
  subproblems and global inner accuracy certificates. The hybrid local solver
  also requires sparse support, seed locality, residual-based termination, and
  an edge-local work bound.
- Open questions: Determine whether the local solver supplies the required
  linear inner rate, translate its residual into the conference paper's
  function-gap schedule, and bound the work added by extrapolation and
  regularized auxiliary solves.
