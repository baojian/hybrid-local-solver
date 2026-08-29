# LCP, obstacle, and active-set solvers for the OP2 route

Last source audit: 2026-08-29

This map asks a narrow question: does a primary-source theorem already give
the fully charged, graph-uniform, output-sensitive solver required by OP2 after
the exact RPPR-to-obstacle reduction?  Search-engine snippets and secondary
surveys were used only for discovery.  Every claim below was checked in the
linked primary paper or author manuscript.  PDF page numbers count from the
first page of the downloaded PDF; journal page numbers are stated separately
when useful.

The short answer is **no**.  The closest local result is Wei--Yang's growing
active-set method, but its proof solves every principal SDD system from scratch
and scans the current boundary in every outer iteration.  Fast SDD solvers
remove the condition-number dependence on a *supplied* face, while classical
LCP/obstacle methods give finite termination or global/asymptotic convergence.
None of the audited theorems pays for local support discovery, cumulative
boundary maintenance, changing-face numerical state, and output within
`O_tilde(vol(S*) / sqrt(alpha))`.

## Verdict table

| Source | Exact theorem or algorithm | Runtime/iteration statement | Access and preprocessing | OP2 verdict |
| --- | --- | --- | --- | --- |
| Wei--Yang (2026) | Theorems 1.2 and 1.3; Algorithm 2 and Lemmas 4.2--5.2 | ACL `O_tilde(1/lambda^2)`; RPPR `O_tilde(|S*| vol(S*))`; logarithmic numerical accuracy | Local adjacency access, but one SDD solve and one current-boundary inspection per active-set round | **Closest local result, not sufficient.** True-support activation is usable; repeated faces remain. |
| Foniok--Fukuda--Gärtner--Lüthi (2009) | Theorem 5.6 and Corollary 5.10 for K-matrix LCPs | At most `n` pivots from cube vertex zero; at most `2n` from an arbitrary vertex | A vertex-orientation oracle evaluates all `n` incident cube orientations using a principal basis solve | **Usable with a global pivot oracle.** Linear pivot count is not local work. |
| Schmelzer--Stoll (2026) | Algorithm 1, Theorem 4.1, Lemma 4.1, Table 2 | Finite active-set loop; each matrix-free CG solve has `O(sqrt(kappa))` iterations; total table entry is `s O(sqrt(kappa))` inner iterations | Full free-set products; inexact sign decisions require a positive trajectory-wide decision margin `mu`; changing-face preconditioner setup is discussed but not amortized | **Global-only / support-oracle primitive.** It exposes the desired square-root factor but leaves outer steps and discovery unbounded. |
| Koutis--Miller--Peng (2011) | Theorem 4.6 | Expected `O_tilde(m log n log(1/eta))` for a supplied SDD system | Builds a global preconditioning chain from the entire supplied matrix | **Usable on a supplied face; global-only for discovery.** |
| Júdice--Pires (1994) | Finite block principal-pivoting algorithm for strictly monotone LCPs | Finite termination, with a guarded single-pivot fallback | Global complementary-basis/residual evaluation and principal solves | **Global-only.** No output-sensitive or condition-number work theorem. |
| Moré--Toraldo (1991) | GPCG: projected-gradient identification plus face CG; finite termination under nondegeneracy | Convergence and finite termination, not a local output-sensitive complexity bound | Full-vector projections, gradients, and reduced systems | **Global-only / assumption mismatch.** |
| Dostál--Domorádová--Sadowská (2011) | MPRGP projected-gradient/CG working-set method; Theorems 6.1 and 7.6 in the author manuscript | R-linear rate in the Hessian condition number; finite termination with a proportioning parameter at least `3 sqrt(kappa)+4` | Full bound-QP vectors and products; no graph discovery model | **Global-only.** Rate is useful for supplied-face comparison, not OP2 locality. |
| Kornhuber (1994) | Extended underrelaxation and monotone multigrid, Theorems 2.1, 2.2, and 3.1 | Global convergence; under strict complementarity, an *asymptotic* 2D contraction `1-c(j+1)^(-2)` | Full finite-element hierarchy, restrictions/prolongations, shape-regular meshes | **Assumption mismatch / global-only.** Not a graph-uniform active-edge theorem. |
| Kärkkäinen--Kunisch--Tarvainen (2003) | Primal-dual active-set algorithms A1/A2; rate and multilevel implementations | Convergence/rate results for Stieltjes discretizations; mesh-independent behavior is numerical for multigrid-PCG implementations | Two- and three-dimensional FEM obstacle problems, full active/inactive partitions and reduced solves | **Assumption mismatch / global-only.** Stieltjes structure matches, access model does not. |

`S*` denotes the optimum support and `vol(S*)` its graph volume.  The
classification “usable with a support oracle” means that the linear algebra
can be invoked after the relevant principal matrix and its rows have already
been exposed; it does not mean that the source supplies such an oracle.

## Primary-source audit

### Wei and Yang, 2026: the closest local primitive

**Source.** Zhewei Wei and Mingji Yang, [*A Simple Active-Set Method for
PageRank-Based Local Graph Clustering*](https://arxiv.org/abs/2608.16339),
arXiv:2608.16339v1.

- PDF pp. 2--3, Theorems 1.2--1.3 state the ACL and regularized-PageRank
  guarantees.  The latter has work
  `O_tilde(|supp(x*)| vol(supp(x*)))` and logarithmic dependence on its
  accuracy and failure parameters.
- PDF pp. 7--9, Theorem 4.1 and Algorithm 2 solve the current principal SDD
  system and then inspect the outer boundary.  Lemma 4.2 gives monotonicity of
  exact restricted solutions under active-set expansion.
- PDF p. 10, proof of Lemma 4.4 charges `O(vol(S))` for inspecting the current
  boundary and uses up to `1/lambda` active-set iterations.
- PDF p. 13, Lemma 5.2 proves that an exact residue violation outside a current
  subset of `S*` can only occur in `S*`.  The proof of Theorem 1.3 on PDF
  pp. 13--14 therefore maintains `S subseteq S*`.
- PDF p. 14 explicitly says that each SDD system is solved from scratch and
  names incremental or warm-started reuse as the route toward nearly linear
  target-volume dependence.

**Audit.** This paper supplies the strongest source-backed support-safety fact
for the present direction.  It does not supply the amortized continuation and
boundary reporter needed for OP2.  Its approximation margins also differ from
the canonical objective-gap stopping rule, so the conversion must be restated
in the shared normalization.

### Foniok et al., 2009: short K-LCP pivot paths, expensive oracle

**Source.** Jan Foniok, Komei Fukuda, Bernd Gärtner, and Hans-Jakob Lüthi,
[*Pivoting in Linear Complementarity: Two Polynomial-Time
Cases*](https://arxiv.org/abs/0807.1249), *Discrete & Computational Geometry*
42(2):187--205, 2009, doi:10.1007/s00454-009-9182-2.

- PDF p. 7, equation (4) defines the P-LCP-induced cube orientation.  The
  stated vertex-evaluation oracle returns the orientations of **all** incident
  cube edges from `A_B(v)^(-1) q`; this is a principal-system computation, not
  a graph-boundary query.
- PDF pp. 15--16, Proposition 5.3 through Theorem 5.6 prove that every directed
  path from cube vertex zero to a K-USO sink has Hamming length at most `n`.
- PDF p. 17, Theorem 5.9 and Corollary 5.10 extend the bound to `2n` pivots from
  an arbitrary cube vertex.

**Audit.** The canonical PageRank obstacle matrix is a K-matrix, so the pivot
count applies.  It does not charge the numerical and access cost of a vertex
evaluation.  Starting from zero is especially favorable and agrees with the
nested true-support path proved in the active-edge note, but the local work
question remains untouched.

### Schmelzer and Stoll, 2026: matrix-free face CG with a margin

**Source.** Thomas Schmelzer and Martin Stoll, [*Non-Negative Conjugate
Gradients*](https://arxiv.org/abs/2607.22121), arXiv:2607.22121v1.

- PDF p. 7, Algorithm 1 and Theorem 4.1 wrap exact principal-block solves in a
  guarded block-pivot loop.  Finite termination is inherited from
  Júdice--Pires/Murty; the paper itself notes a crude `2^n` basis ceiling rather
  than a useful work bound.
- PDF pp. 8--9, Lemma 4.1 transfers the exact sequence to inexact CG only when
  the residual is smaller than a trajectory-wide decision margin `mu`.  The
  margin is the minimum nonzero primal or dual test value on the unknown exact
  active-set trajectory.
- PDF pp. 13--14, Proposition 5.2 gives the standard
  `O(sqrt(kappa_P) log(1/eta))` PCG count.  The discussion says a changing free
  set can require rebuilding nontrivially restricted preconditioners.
- PDF p. 14, Table 2 records `s O(sqrt(kappa))` inner iterations and full
  matrix-free products for `s` active-set outer steps.  Neither `s` nor the
  product cost is tied to output volume.

**Audit.** The square-root condition-number factor is exactly the desired
fixed-face rate.  The source begins with a global free set, scans global primal
and dual tests, and hides a potentially arbitrarily small sign-decision margin.
It therefore cannot be used as an OP2 theorem without a local wrapper and a
margin-free, fully charged reporter.

### Koutis, Miller, and Peng, 2011: nearly-linear supplied SDD solves

**Source.** Ioannis Koutis, Gary L. Miller, and Richard Peng, [*A Nearly-
`m log n` Time Solver for SDD Linear Systems*](https://arxiv.org/abs/1102.4842),
FOCS 2011.

- PDF pp. 9--10, Definition 4.2 and Lemmas 4.3--4.5 construct and analyze a
  global preconditioning chain.
- PDF p. 10, Theorem 4.6 gives expected
  `O_tilde(m log n log(1/eta))` work for an input SDD matrix with `m` nonzeros
  and relative energy error `eta`.

**Audit.** Applied to `Q_UU`, this is nearly linear in the nonzeros of a
*supplied* active face and has only logarithmic accuracy dependence.  Rebuilding
the chain on every growing face repeats work; building it once on the full
graph is forbidden global preprocessing.  The theorem neither discovers `U`
nor maintains boundary violations.

### Júdice and Pires, 1994: finite block pivots

**Source.** Joaquim Júdice and Faustino Pires, [*A Block Principal Pivoting
Algorithm for Large-Scale Strictly Monotone Linear Complementarity
Problems*](https://doi.org/10.1016/0305-0548(94)90106-6), *Computers &
Operations Research* 21(5):587--596, 1994.

The abstract and algorithm give a finite block strategy safeguarded by a
single-pivot rule.  Schmelzer--Stoll, PDF pp. 7--8, explicitly identify their
exact outer loop as this construction and isolate their new contribution as
the inexact-CG sign-transfer lemma.  The 1994 paper's “large-scale” label is a
numerical implementation claim: its theorem is not an adjacency-oracle or
output-sensitive bound.

### Moré and Toraldo, 1991: projected identification plus face CG

**Source.** Jorge J. Moré and Gerardo Toraldo, [*On the Solution of Large
Quadratic Programming Problems with Bound
Constraints*](https://doi.org/10.1137/0801008), *SIAM Journal on
Optimization* 1(1):93--113, 1991.

The GPCG framework alternates projected-gradient steps, which identify a
face, with CG on the associated reduced quadratic.  Theorem 5.2 (journal
p. 102) proves finite termination for strictly convex, nondegenerate problems.
The operations are global projected gradients and reduced-system products;
there is no graph exploration, active-edge reporter, or output-sensitive work
statement.  In particular, objective decrease and eventual face
identification do not imply the coordinatewise one-sided invariant needed for
safe local discovery.

### Dostál, Domorádová, and Sadowská, 2011: MPRGP rates

**Source.** Zdeněk Dostál, Marta Domorádová, and Marie Sadowská,
[*Superrelaxation and the Rate of Convergence in Minimizing Quadratic
Functions Subject to Bound
Constraints*](https://doi.org/10.1007/s10589-009-9237-6), *Computational
Optimization and Applications* 48(1):23--44, 2011.

The author manuscript's Theorem 6.1 (PDF p. 11) gives an R-linear projected-
gradient rate, and Theorem 7.6 (PDF p. 17) gives finite termination of the
MPRGP working-set method under an explicit proportioning choice at least
`3 sqrt(kappa)+4`.  The method interleaves reduced CG, projected-gradient, and
expansion steps over full bound-QP vectors.  It supplies neither a local
support-volume access model nor cumulative active-edge maintenance.

### Kornhuber, 1994: monotone multigrid for FEM obstacles

**Source.** Ralf Kornhuber, [*Monotone Multigrid Methods for Elliptic
Variational Inequalities I*](https://publications.imp.fu-berlin.de/1914/),
*Numerische Mathematik* 69(2):167--184, 1994,
doi:10.1007/BF03325426.

- PDF p. 7, Theorem 2.1 proves global convergence of extended
  underrelaxation.
- PDF pp. 9--10, Theorem 2.2 requires strict complementarity for eventual
  reduction to a linear extended relaxation.
- PDF p. 14, Theorem 3.1 proves global convergence and, under strict
  complementarity in the two-dimensional finite-element setting, an
  a-posteriori asymptotic contraction `1-c(j+1)^(-2)`.  The constant depends on
  ellipticity and coarse-mesh shape regularity.
- PDF p. 3 says global rate estimates are left for future work; the method
  operates through the full multilevel nodal hierarchy.

**Audit.** Monotone refers to energy-preserving underrelaxation, not to a
coordinatewise lower envelope below the obstacle solution.  The finite-element
hierarchy and shape assumptions do not hold for arbitrary input graphs, and
the theorem does not charge discovery of an unknown local active region.

### Kärkkäinen, Kunisch, and Tarvainen, 2003: Stieltjes active sets

**Source.** Tommi Kärkkäinen, Karl Kunisch, and Pasi Tarvainen,
[*Augmented Lagrangian Active Set Methods for Obstacle
Problems*](https://doi.org/10.1023/B:JOTA.0000006687.57272.b6), *Journal of
Optimization Theory and Applications* 119(3):499--533, 2003.

- Journal p. 501 assumes the discretization matrix is Stieltjes (symmetric
  nonsingular M-matrix), the same matrix class obtained in the OP2 reduction.
- Journal pp. 503--504, Algorithm A1 forms a global active/inactive partition
  and solves the corresponding reduced system.
- Journal pp. 506--510 analyze monotone phases and rates.  Journal
  pp. 520--530 develop multilevel/PCG realizations and report mesh-independent
  behavior numerically for two- and three-dimensional model problems.

**Audit.** The matrix-class match is genuine.  The solver's mesh hierarchy,
full-domain partition, and reduced-system work are not graph-local, and the
paper does not state an output-sensitive theorem for an unknown support.

## Consequences for the active-edge direction

1. **The LCP label does not itself buy locality.**  K-matrix pivot paths have
   only linearly many pivots, but the standard vertex oracle performs a
   principal solve and returns a global sign vector.
2. **The square-root factor belongs to a fixed face.**  CG/PCG supplies
   `sqrt(kappa)=O(1/sqrt(alpha))` only after the face is represented and its
   operator applications are charged.
3. **Terminal support volume is not a cumulative ledger.**  Existing local
   active-set proofs pay for every principal solve and boundary scan.  A path
   can expose nested prefixes with final volume `Theta(s)` and cumulative
   prefix volume `Theta(s^2)`.
4. **Numerical sign decisions require an explicit policy.**  A theorem that
   assumes a hidden minimum complementarity margin is not polylogarithmic in
   only the requested objective accuracy.  A usable OP2 primitive must return
   certified sign intervals, refine ambiguous tests within the total ledger,
   or avoid exact sign decisions.
5. **The remaining theorem is dynamic.**  It must amortize changing-face
   solves, warm starts or response updates, boundary-key changes, state
   materialization, and final certification over distinct explored volume.

The theorem-level formulation and the exact projected-CG obstruction are in
`manuscript/notes/active_edge_lcp/`.
