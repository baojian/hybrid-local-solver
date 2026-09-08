# LCP, obstacle, and active-set solvers for the OP2 route

Last source audit: 2026-09-08 (second-night OP3 dynamic-flow, curve and cograph-structure checks)

This map asks a narrow question: does a primary-source theorem already give
the fully charged, graph-uniform, output-sensitive solver required by OP2 after
the exact RPPR-to-obstacle reduction?  Search-engine snippets and secondary
surveys were used only for discovery.  Every claim below was checked in the
linked primary paper or author manuscript.  PDF page numbers count from the
first page of the downloaded PDF; journal page numbers are stated separately
when useful.

The short answer for an existing published theorem is **no**.  The closest local result is Wei--Yang's growing
active-set method, but its proof solves every principal SDD system from scratch
and scans the current boundary in every outer iteration.  Fast SDD solvers
remove the condition-number dependence on a *supplied* face, while classical
LCP/obstacle methods give finite termination or global/asymptotic convergence.
None of the audited source theorems by itself pays for local support discovery, cumulative
boundary maintenance, changing-face numerical state, and output within
`O_tilde(vol(S*) / sqrt(alpha))`.

The project note `manuscript/notes/active_edge_lcp/` now supplies the missing
wrapper by a new threshold-batch Cholesky decay theorem.  It bounds the number
of complete exposed-face rebuilds by
`O(alpha^(-1/2) log(1/eps_obj))`, uses Koutis--Miller--Peng only on each
already exposed degree-scaled SDD face, and certifies every randomized solve
before any new adjacency list is exposed.  This is a proved-here result, not a
claim attributed to the audited literature.

## Verdict table

| Source | Exact theorem or algorithm | Runtime/iteration statement | Access and preprocessing | OP2 verdict |
| --- | --- | --- | --- | --- |
| Wei--Yang (2026) | Theorems 1.2 and 1.3; Algorithm 2 and Lemmas 4.2--5.2 | ACL `O_tilde(1/lambda^2)`; RPPR `O_tilde(|S*| vol(S*))`; logarithmic numerical accuracy | Local adjacency access, but one SDD solve and one current-boundary inspection per active-set round | **Closest local result, not sufficient.** True-support activation is usable; repeated faces remain. |
| Foniok--Fukuda--Gärtner--Lüthi (2009) | Theorem 5.6 and Corollary 5.10 for K-matrix LCPs | At most `n` pivots from cube vertex zero; at most `2n` from an arbitrary vertex | A vertex-orientation oracle evaluates all `n` incident cube orientations using a principal basis solve | **Usable with a global pivot oracle.** Linear pivot count is not local work. |
| Bokanowski--Maroso--Zidani (2009) | Howard obstacle iteration, Theorem 4.3 | At most `N+1` iterations, or `N` from the all-obstacle policy | Each iteration solves a global policy system and evaluates the policy over all `N` coordinates | **Global-only.** The iteration bound does not charge local support discovery or solve work. |
| Schmelzer--Stoll (2026) | Algorithm 1, Theorem 4.1, Lemma 4.1, Table 2 | Finite active-set loop; each matrix-free CG solve has `O(sqrt(kappa))` iterations; total table entry is `s O(sqrt(kappa))` inner iterations | Full free-set products; inexact sign decisions require a positive trajectory-wide decision margin `mu`; changing-face preconditioner setup is discussed but not amortized | **Global-only / support-oracle primitive.** It exposes the desired square-root factor but leaves outer steps and discovery unbounded. |
| Koutis--Miller--Peng (2011) | Theorem 4.6 | Expected `O_tilde(m log n log(1/eta))` for a supplied SDD system | Builds a global preconditioning chain from the entire supplied matrix | **Usable on a supplied face; global-only for discovery.** |
| Durfee--Gao--Goranci--Peng (2019) | Lemma 1.1 and Theorem 1.2 | Terminal additions are amortized after `O_tilde(m beta^-2 epsilon^-4)` initialization; bounded-degree coordinate solve queries cost `O_tilde(n^(11/12) epsilon^-5)` | Full-graph random-walk/Schur preprocessing, rebuilds, oblivious-adversary guarantee, and polynomial numerical-accuracy dependence | **Dynamic but global-only.** It is not an exposed-volume changing-face primitive. |
| van den Brand--Nanongkai--Saranurak (2019) | Theorems 4.1 and 4.2 | Ambient-polynomial column/element update and row/element inverse-query time | Dense `n x n` algebra with `O(n^omega)` preprocessing over a field | **Dynamic but assumption/access mismatch.** No graph locality; its lower bounds are not OP2 lower bounds. |
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

**Dual-language audit.**  In Wei--Yang's non-lazy notation, equations (2) and
(4) and Lemmas 5.1--5.2 imply that the grounded-flow vertex slack is
`L_alpha x - alpha(e_s-rho d) = alpha(rho d-r(x))`.  Thus their test
`r(x^(S))(v) > rho d(v)` is exactly a violated dual vertex inequality.  The
paper uses this equivalent residual/KKT condition in the support-safety proof
on PDF pp. 13--14, but does not introduce a flow variable, a dual energy
objective, or the grounded electrical-flow optimization problem.  The active
manuscript now states that dual explicitly as a structural interpretation and
does not claim standard Fenchel duality as the new complexity ingredient.

### Chen, Peng, and Wang, 2021: constrained diffusion and the OP3 alternative

**Source.** [*ℓ2-Norm Flow Diffusion in Near-Linear Time*](https://arxiv.org/pdf/2105.14629v2), FOCS 2021, arXiv:2105.14629v2.

- Theorem 1.1 (PDF p. 5) gives randomized high-probability
  `O(m log^8(n) log(1/eta))` work on a supplied graph. Definitions 3.7--3.8
  (p. 15) specify the generalized diffusion objective and its approximation;
  Lemmas 4.1--4.2 (p. 17) give the generalized solver and refinement.
- Constrained elimination and vertex weighting functions are the relevant
  mechanisms (Sections 2.2--2.3). Section 1.4 (p. 8) leaves strongly local
  near-linear diffusion open.
- Assumption 3.15 (p. 17) restricts every encountered nonzero number to
  `[n^(-c), n^c]` for a universal constant. Numerical stability is outside
  the source's scope; Lemma 4.4 also uses polynomial weight ratio.

**Audit.** Global-only, with a parameter-range obligation. The OP3 face matrix
is algebraically a graph Laplacian plus positive diagonal vertex terms, but
this does not supply a local construction or unrestricted polylogarithmic
inverse-teleportation dependence. The exploration and proposed acceptance
criteria are in
[`OP3_DIRECTIONS_20260906.md`](../../manuscript/notes/incremental_active_set_sdd/OP3_DIRECTIONS_20260906.md).

**Objective-class correction and new local bridge.** Definition 3.2, PDF
p. 14 (visually checked), requires a VWF derivative that is constant on
its final ray. A positive quadratic grounding term does not directly meet
that condition. The note's `lem:op3-capped-grounding-vwf` supplies an
equivalent two-piece objective using a known potential bound and final
boxing; `thm:op3-local-gap-certificate` supplies a computable original
accuracy certificate. Both are note-local proof drafts, not source imports.
Fact 7.2 and the compression argument, PDF pp. 35–39, use breakpoint
range to bound the number of geometric bins. Lemma 7.7 and the proof of
Lemma 6.4 were visually checked on pp. 37–39. The note-local
`thm:op3-global-vwf-compression` adds moment regularization of tiny signed
splits, with a global additive budget and an unchanged final derivative.
It removes the smallest-split and evaluation-radius dependence for this
scalar operation. Largest-split, curvature and recursive error bounds
remain separate; tiny curvature weights can still occur. This does not
establish Assumption 3.15 or import the source's fast solver. The next
specific targets, including the actual normalized proximal objective in
Claim 8.19, are in
[`GLOBAL_VWF_RECURSION_PROBE.md`](../../manuscript/notes/incremental_active_set_sdd/GLOBAL_VWF_RECURSION_PROBE.md).

### Second-night check: curve primitives and dynamic flow

The further OP3 accuracy check is in
[`DIFFUSION_SOURCE_CERTIFICATE_PROBE.md`](../../manuscript/notes/incremental_active_set_sdd/DIFFUSION_SOURCE_CERTIFICATE_PROBE.md).
Chen--Peng--Wang's residual instance has full supplied-graph construction
cost (Definition 3.13 and Fact 3.14, PDF p. 16). Claim 8.21's proof
(p. 52) uses Assumption 3.15 when choosing a proximal tolerance. The new
note-local energy-to-ACL lemma supplies a known initial energy scale and
requested tolerance; it does not establish the source's intermediate
numerical-range assumption or a local construction.

**Explicit outer accuracy policy.** Algorithm 9 / Theorem 8.3 (p. 44)
and Claims 8.19–8.21 (pp. 50–52) were visually checked. The note's
`thm:op3-explicit-capped-proximal-budget` uses the source convergence
inequality with an explicit induction on original feasible sublevels and
accelerated centers. `cor:op3-capped-certified-restart-driver` supplies
the positive gap scale from the original certificate and restarts the same
capped objective. Every inner relative-oracle cost remains in its bound.
This replaces one outer accuracy obligation; it does not implement the
source's recursive inner solver or prove local OP3 work. The remaining
interface is recorded in
[`CAPPED_INNER_ORACLE_PROBE.md`](../../manuscript/notes/incremental_active_set_sdd/CAPPED_INNER_ORACLE_PROBE.md).

**Generic accuracy and canonical ranges, note-local drafts.**
`thm:op3-generic-relative-proximal` now gives the universal tolerance
`1/(33*2^30*kappa^3)` for a zero-start invocation of the same source
algorithm, including zero gap. Its energy-seminorm induction cancels the
unknown objective-gap scale; translated residual VWFs cover restarts.
`prop:op3-vwf-canonical-input-gap` and
`cor:op3-generic-canonical-ranges` give finite-minimum and coordinate
bounds for a connected supplied graph after a paid common terminal-ray
shift. They permit zero total final slope and signed lower domains.
These are new proofs using the already checked source convergence bound,
not claims attributed to CPW. They do not settle recursive coefficient
growth, fast inner-oracle work, or unknown-support discovery.

**Printed Lift coefficient check.** On visually checked PDF pp. 40–42,
the displayed constant update has a plus sign. Direct minimization of
`c*(x-y)^2/2+r*y^2/2+a*y+b` gives `b-a^2/(2*(c+r))`.
For the valid VWF `f(y)=-y`, `y>=0`, `c=1`, the value at x=0 is
`-1/2`; the printed coefficient gives `+1/2`. The note records this
specific correction before implementing Lift values, without treating
it as a refutation of the paper's entire complexity theorem.

**Implemented forest comparison, note-local draft.** PDF pp. 30–34 were
visually checked: Lemmas 6.1 and 6.6 already state fast degree-one VWF
elimination, and Algorithm 6 eliminates first and then compresses refinement
instances on the remaining core. The note's
`thm:op3-persistent-vwf-forest` implements a separate immutable
derivative-integral AVL representation with corrected constants, signed
domains, explicit all-allocation accounting and canonical export.
`prop:op3-vwf-forest-ranges` gives one-pass split, terminal-slope, curvature
and zero-value bounds. This is implementation and proof verification of a
known elimination approach, not a claim that the approach is new.
Reconstruction uses the saved lifted child derivative. Algorithm 7's printed
recovery line on p. 33 names the parent descriptor after Add, while Lemma 6.6
specifies OptimalX after Lift; the note states its own exact child recovery
contract to avoid this descriptor ambiguity. Fast recursive coarse work and
the source's numerical-range obligations remain separate.

### Local flow runtime parameters checked against primary formulas

**Source.** Fountoulakis, Wang and Yang,
[*p-Norm Flow Diffusion for Local Graph Clustering*](https://proceedings.mlr.press/v119/fountoulakis20a/fountoulakis20a.pdf),
ICML 2020, PMLR 119:3222–3232. Equation (10), PDF p. 7, retains a
weighted Dirichlet eigenvalue and bounds the strong-convexity parameter
below by `1/((p-1)*|Delta|^p)`. Theorem 6, PDF p. 8, gives at `p=q=2`
work `O(|Delta|*d_max^2/gamma_source*log(1/epsilon))`.
Here `gamma_source` is curvature, not this project's PageRank coupling.
Both pages were checked visually. **Audit:** locality is useful, but this
quantified theorem retains conditioning and degree factors.

**Source.** Yang and Fountoulakis,
[*Weighted Flow Diffusion for Local Graph Clustering with Node Attributes: an Algorithm and Statistical Guarantees*](https://proceedings.mlr.press/v202/yang23d/yang23d.pdf),
ICML 2023, PMLR 202:39252–39276. Algorithm 1 is on PDF p. 3.
Propositions 2.1–2.2 and the following paragraph, p. 4, give support
containment and work
`O(d_max*||Delta||_1*alpha_source/beta_source*log(1/epsilon))`.
The displayed statement identifies `alpha_source` with maximum weighted
degree and prints `beta_source >= min edge weight`; these symbols do not
denote the project's teleportation parameters. **Audit:** the exact path
diagnostic in `prop:op3-flow-path-curvature` rules out interpreting that
lower bound as a general Dirichlet-curvature bound. It does not refute an
unspecified parameter or establish an algorithmic lower bound. This
meaning must be reconciled before importing the runtime as an OP3 result.

**Source / context.** Back de Luca, Fountoulakis and Yang,
[*Local Graph Clustering with Noisy Labels*](https://proceedings.iclr.cc/paper_files/paper/2024/file/a4d991d581accd2955a1e1928f4e6965-Paper-Conference.pdf),
ICLR 2024. The paragraph after equation (2), PDF p. 4, describes linear
support-size work and cites the 2020 paper; the formula was checked in
the rendered page. Remark 3.3, p. 6, discusses support-neighborhood
locality. **Audit:** this introductory summary does not replace the
quantified original theorem or provide a uniform original-ACL certificate.

### Persistent curve and dynamic flow context

**Source / context, not a new solver import.** Chen--Peng--Wang,
[Section 7.2, Lemma 7.8 and Claim 7.9, PDF pp. 39--40](https://arxiv.org/pdf/2105.14629v2),
uses augmented search trees for predecessor, insertion, range updates and
order-preserving composite operators, with persistence. Their small-function
addition scans the smaller representation. This is relevant context for
persistent scalar responses; the OP3 recursive-module experiment reuses this
repository's independently implemented immutable affine AVL primitives.
Its response shear, nonnegative left ray, reconstruction versions and
small-child charge require their own proof. No novelty claim is made for
lazy affine transforms or merging a smaller piecewise function.

**Source.** Chen, Kyng, Liu, Meierhans and Probst Gutenberg,
[*Almost-Linear Time Algorithms for Incremental Graphs*](https://arxiv.org/pdf/2311.18295v1),
arXiv:2311.18295v1 (30 November 2023). Section 1.2, Theorem 1.4 and
Remark 1.5, PDF p. 5, address the first incremental update at which a
min-cost-flow threshold is attained, with polynomially bounded
capacities/costs. Remark 1.5 permits fixed-point arithmetic and an unknown
final edge count using doubling. Theorem 1.6 on that page gives
approximate flow maintenance with an inverse-accuracy factor. The displayed
runtime includes an exponential of a fractional power of log m.

**OP3 assessment (inference).** This is useful dynamic-flow context, not a
polylogarithmic-overhead obstacle-coordinate oracle. OP3's soft-O notation
does not hide the source's subpolynomial factor; a local graph exposure,
continuous quadratic reduction and original ACL certificate would also be
required. No lower bound for OP3 is inferred from the source's matching
comparison.

**Source.** van den Brand, Chen, Kyng, Liu, Meierhans, Probst Gutenberg and
Sachdeva, [*Almost-Linear Time Algorithms for Decremental Graphs*](https://arxiv.org/pdf/2407.10830v1),
arXiv:2407.10830v1 (15 July 2024), accepted to FOCS 2024 per the author
record. Section 1.2, Theorem 1.6, PDF p. 6, reports threshold feasibility
under edge deletion, capacity decrease or cost increase, with bounded
integral data. Theorem 1.7 maintains an approximate flow cost with an
inverse-accuracy factor; its guarantee handles adaptive adversaries.

**OP3 assessment (inference).** The explicit runtime has subpolynomial,
rather than polylogarithmic, overhead. Decremental flow feasibility does not
itself expose positive original obstacle coordinates under local graph
admissions. These are separate model and certificate obligations, not a
refutation of adapting a particular source mechanism.

The source check was scoped to these statements and curve primitives, not
an exhaustive literature review or a proof that no newer result exists.
No source PDF was added to the local paper collection. Stable versioned
links above identify the checked sources.

### Shamir and Sharan, 2004: dynamic cograph structure

**Source / context.** Ron Shamir and Roded Sharan, [*A Fully Dynamic
Algorithm for Modular Decomposition and Recognition of Cographs*](https://www.cs.tau.ac.il/~roded/articles/cmd.pdf),
*Discrete Applied Mathematics* 136(2–3):329–340, 2004,
[doi:10.1016/S0166-218X(03)00448-7](https://doi.org/10.1016/S0166-218X(03)00448-7).
Checked the author preprint, Section 3.1 (PDF p. 6), Section 3.3
(PDF p. 9), Proposition 7 and Theorem 8 (PDF p. 10), including rendered
pages where text extraction loses theorem numbers. Its representation
stores node types, child counts and linked parent/child records, with no
explicit module membership lists. Theorem 8 gives O(d) structural work
per modification involving d edges. Vertex insertion uses the earlier
Corneil–Perl–Stewart incremental algorithm; Section 3.1 describes linear
initial construction. Allow O(1+d) to include isolated-vertex operations.

**OP3 assessment (inference).** Starting from the discovered induced graph
and supplying only paid original-row incidences could address the structural
interface. The implementation and accounting of that wrapper are still
missing. This source does not maintain the obstacle-response curves,
original-coordinate targets, or their changed values. The separately proved
known-summand removal bound depends on the removed child's size. Thus cheap
structural edits cannot yet be charged as cheap response updates. No new
formal source import is used by the fixed-response or removal theorems.

### Alstrup, Holm, de Lichtenberg and Thorup: dynamic tree clusters

**Source.** [*Maintaining Information in Fully-Dynamic Trees with Top Trees*](https://arxiv.org/pdf/cs/0310065v2),
*ACM Transactions on Algorithms* 1(2):243–264, 2005; publication metadata
checked against the [University of Copenhagen record](https://researchprofiles.ku.dk/en/publications/maintaining-information-in-fully-dynamic-trees-with-top-trees/).
The checked theorem text is arXiv:cs/0310065v2 (21 November 2003).
Section 2, PDF pp. 4–8, defines edge-induced clusters with at most two
boundary vertices and application callbacks. Theorem 1, p. 6, gives
logarithmic height, linear structural space, and O(log n) joins/splits per
link, cut or expose. Composite k-operation bounds multiply by k.
Section 2.1 requires splitting every cluster whose edge set or boundary
set will change. Link/cut reset external boundaries. Section 6.1, p. 25,
implements exposure; Section 6.2, pp. 25–26, handles arbitrary degree
inside the data structure.

The [published PDF](https://www.cs.uoi.gr/~loukas/courses/grad/Data_Structures_and_Algorithms/papers/p243-alstrup.pdf)
was subsequently checked directly: Theorem 2.1, journal p. 247; definitions,
modification discipline and application pointers, pp. 245–248; exposure and
arbitrary-degree reduction, pp. 259–260. It retains the required height and
callback guarantees. Unlike the old preprint, the published interface does
not offer zero-argument expose; the application uses only one- or two-vertex
exposure. The final theorem imports this height-bounded published version.

**Import audit completed for trees.** The OP3 note proves
`thm:op3-local-top-tree`: the application stores an unavailable marker for
clusters with an interior seed, then uses source exposure to split/recreate
them. Every valid join is a constant number of implemented compress/rake/
forget operations. A home-edge payload refresh follows the logarithmic
ancestor path. Local indices and incidence records include only admitted
vertices. The resulting exact-real word work is O(cvol(U) log^4(2+cvol(U))),
with final recovery and all retained copies charged. This is a local proof
draft awaiting independent review, not a theorem attributed to the source.
The callback audit checks 167,384 legal joins and 650 exposure transitions;
its exhaustive hierarchy builder is not the published balancing algorithm.
Source height bounds, not the unbounded-height amortized variant of Section
6.3, are used for the payload walk. Uniform shifted loads now allow an
independent geometric anchor; the proposed unicyclic continuation remains
Open in `UNICYCLE_TOP_TREE_PROBE.md`.

### Jacob and Brodal: stable planar boundary records

**Source.** [*Dynamic Planar Convex Hull*](https://arxiv.org/pdf/1902.11169),
arXiv:1902.11169v1 (2019), Theorem 1 on PDF page 2, gives amortized
logarithmic insertion/deletion, logarithmic extreme-point queries, and
linear space. Section 2.2, PDF pages 5–6, specifies exact geometric
primitives and the real-RAM/pointer model.

**Audit.** This is enough for individual changes to stable planar frontier
records. The earlier `aesp_cd_l1_rppr` stable-port corollary already states
that reduction, while its series-parallel hull-meld interface remains open.
The new `thm:op3-two-port-frontier` verifies the required local work by
retaining the seed and at most one other admitted branching vertex. Its
separate AVL implementation uses a conservative fourth-power logarithm,
proved locally; it does not implement or import the source's optimal
construction. Changing many separator coordinates at once is not a single
point update in this source model.

### Chan: a verified three-coordinate source contract

**Source.** [*Dynamic Geometric Data Structures via Shallow Cuttings*](https://arxiv.org/pdf/1903.08387),
arXiv:1903.08387v1 (2019), Theorem 4.2 on PDF pp. 10–11, gives
three-dimensional extreme queries in `O(log^2 n)` time, amortized
`O(log^2 n)` insertion and `O(log^4 n)` deletion, with `O(n log n)`
preprocessing and `O(n log n)` space (p. 11). Lemma 4.1, PDF p. 9, uses
deterministic restricted shallow cuttings. The query proof on p. 11 checks
the static envelope and a recursively maintained exception set; its deletion
counter argument ensures a surviving extremizer is found.

**Import audit.** Theorem 4.2 has no general-position restriction; the
restriction in Theorem 2.1 concerns a different hull-size problem. Coincident
labeled points can be grouped in a comparison dictionary, storing a live
representative. Any exact maximizer suffices for a strict gate query.
Initialization from a constant-size set is paid by the stated insertion
bound; local frontier size is discovered online. This reconciles the source
contract for a fixed third coordinate, without implementing its backend.
It supplies individual updates, not bulk coordinate transformations.
The newer scalar physical-flux construction in `incremental_active_set_sdd`
handles growing core dimension with an explicit dense-core cost, so a
three-dimensional implementation is no longer the immediate research target.

### Tree hitting times and the bounded-attachment probe

**Source.** [*Reversible Markov Chains and Random Walks on Graphs*, Chapter 5, §5.3](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch5.S3.html), online section dated 23 April 1996. Theorem 5.20, equation (5.81), gives the mean time across a tree edge as twice the starting-side component size minus one. Proposition 5.24(b) bounds the maximal mean hitting time on an n-vertex tree by `(n-1)^2`.

**Audit.** These are mean-hitting statements, not an extremal comparison of
discounted hitting transforms. The new
[`BOUNDED_ATTACHMENT_PROBE.md`](../../manuscript/notes/incremental_active_set_sdd/BOUNDED_ATTACHMENT_PROBE.md)
rederives the needed edge identity and a conservative mean bound, then uses
Jensen's inequality to prove attachment saturation. The sharper Chebyshev
comparison in `DISCOUNTED_ATTACHMENT_EXTREMAL_PROBE.md` remains **Open**;
finite exact tests do not turn the source's mean bound into that claim.

### Agarwal, Phillips, and Sadri: an affine response data structure

**Source.** [*Lipschitz Unimodal and Isotonic Regression on Paths and Trees*](https://www.cs.toronto.edu/~sadri/publications/regression.pdf), author manuscript dated 2 January 2010. Section 3, Theorem 3.1 (PDF p. 7), gives affine composition trees: whole-curve affine maps cost constant time; evaluation, inverse evaluation, insertion and interval maps cost logarithmic time. The transformed curve must remain monotone in both coordinates.

**Audit.** This is a data structure for supplied scalar curves, not a local
RPPR solver. The new
[`TREE_AFFINE_PROBE.md`](../../manuscript/notes/incremental_active_set_sdd/TREE_AFFINE_PROBE.md)
gives a supplied-tree adaptation. Its persistent AVL implementation and
`O(n log^2 n)` word-work argument are now proof-drafted and exactly audited
in `thm:op3-persistent-tree`. Local discovery and multidimensional cyclic
responses remain separate obligations; these are our claims, not the
source's RPPR results.

For comparison, Kuric, Ahmetspahic and Pock's
[*Total Generalized Variation on a Tree*](https://epubs.siam.org/doi/10.1137/23M1556915)
(2024), Lemma 4.4, proves quadratic worst-case time and memory for its convex
piecewise-quadratic message implementation. This is an algorithm bound, not a
lower bound for implicit affine representations.

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

### Bokanowski, Maroso, and Zidani, 2009: linear obstacle policies, global solves

**Source.** Olivier Bokanowski, Stefania Maroso, and Hasnaa Zidani,
[*Some Convergence Results for Howard's
Algorithm*](https://www.ljll.fr/~bokanowski/recherche/Bokanowski_Maroso_Zidani_2009.pdf),
*SIAM Journal on Numerical Analysis* 47(4):3001--3026, 2009,
doi:10.1137/08073041X.

- Author-manuscript PDF p. 13 defines Algorithm (Ho-2) for
  `min(Ax-b, x-g)=0`.  Its policy update compares the two branches for every
  coordinate, and the fixed-policy step solves the corresponding `N x N`
  linear system.
- Theorem 4.3 on the same PDF page proves termination in at most `N+1`
  iterations under monotonicity of every policy matrix, and at most `N` when
  initialized with the all-obstacle policy.  The paragraph after the theorem
  explicitly interprets the latter count as `N` linear-system resolutions.

**Audit.** Taking `g=0` and `A=Q` matches the canonical obstacle equation.
The result is a global iteration theorem: it neither restricts policy changes
to the unknown local support nor prices the changing principal systems and
full policy tests by exposed volume.  It therefore reinforces, but does not
improve, the short-pivot/global-oracle verdict from Foniok et al.

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

- Local PDF:
  `papers/2011-focs-koutis-nearly-m-log-n-time-solver-sdd-linear-systems.pdf`,
  downloaded from <https://arxiv.org/pdf/1102.4842> on 2026-09-06. The PDF
  identifies arXiv `1102.4842v4`; its title page also has a later TeX date,
  which does not change the FOCS 2011 publication metadata.
- PDF pp. 9--10, Definition 4.2 and Lemmas 4.3--4.5 construct and analyze a
  global preconditioning chain.
- In this local PDF, p. 10 states Lemma 4.5 and p. 11 states Theorem 4.6,
  which gives expected
  `O_tilde(m log n log(1/eta))` work for an input SDD matrix with `m` nonzeros
  and relative energy error `eta`.

**Audit.** The normalized principal matrix `Q_UU` need not itself be
diagonally dominant on an irregular graph.  The applicable supplied system is
the degree-scaled matrix
`H_UU = D_U^(1/2) Q_UU D_U^(1/2)
      = ((1+alpha)/2) D_U - ((1-alpha)/2) A_UU`,
which is SDD and has `O(vol(U))` nonzeros.  Thus the theorem is nearly linear
in a *supplied* active face and has only logarithmic energy-accuracy
dependence.  Rebuilding the chain on every growing face repeats work; building
it once on the full graph is forbidden global preprocessing.  The theorem
neither discovers `U` nor maintains boundary violations.  Theorem 4.6 states
expected work but no arbitrary failure parameter.  BuildChain and Lemma 4.5
provide a constant-success event; the OP2 note obtains a declared failure
probability by exact local residual certification and capped independent
retries, not by attributing a `zeta` interface to Theorem 4.6.

**Note-scoped application audit, 7 September 2026.** The independent OP3
note `incremental_active_set_sdd`, `lem:op3-certified-sparse-solve`, imports
this supplied theorem on an already assembled coarse Schur system, not on
the ambient graph. PDF pp. 9--11 were reread, and pp. 10--11 rendered and
visually checked. Its K has O(p+r) nonzeros and K*1>=bar_alpha*d_P. The
exact residual test |f-K*t|<=delta*bar_alpha*d_P certifies a uniform physical
port error delta. With the physical seed retained, f has no positive entry
except f_v<=1 and the positive-face energy is at most 1/bar_alpha. Relative
energy accuracy eta=delta*bar_alpha^2/2 therefore suffices. Independent
constant-success retries are explicitly certified and charged; fresh
randomness is used after adaptive face selection. The note's expected
linear-rank ACL claim is a new proof draft, not a source theorem. Its exact
audit uses a labelled dense coarse provider and does not implement the
source solver. Source metadata is unchanged; no separate worst-case
workspace or finite-precision stability guarantee is imported.

### Durfee et al., 2019: dynamic Schur complements require global initialization

**Source.** David Durfee, Yu Gao, Gramoz Goranci, and Richard Peng,
[*Fully Dynamic Spectral Vertex Sparsifiers and
Applications*](https://arxiv.org/abs/1906.10530), STOC 2019,
pp. 914--925, doi:10.1145/3313276.3316379.

- PDF p. 2, Lemma 1.1 maintains an approximate Schur complement under edge
  updates and terminal additions.  Initialization costs
  `O_tilde(m beta^-2 epsilon^-4)` and the data structure supports only
  `O(beta m)` operations before rebuilding; the guarantee is expected
  amortized against an oblivious adversary.
- PDF p. 3, Theorem 1.2 gives coordinate-query access to an energy-norm
  approximate Laplacian solution on bounded-degree unweighted graphs in
  `O_tilde(n^(11/12) epsilon^-5)` expected amortized time per update or query.
- PDF p. 15 explains the accounting: terminal-addition work is charged
  against preprocessing that generated full-graph random walks, whose
  initialization cost is `O_tilde(m beta^-2 epsilon^-4)`.

**Audit.** Terminal addition and coordinate query are conceptually close to a
growing-face response.  The theorem nevertheless starts from the ambient
graph, pays global initialization/rebuilds, has polynomial rather than
polylogarithmic dependence on numerical accuracy, and does not report obstacle
boundary-threshold crossings.  It is not usable as-is under OP2's no-free-
preprocessing access contract.

### van den Brand, Nanongkai, and Saranurak, 2019: dynamic inverse is ambient algebra

**Source.** Jan van den Brand, Danupon Nanongkai, and Thatchaphol Saranurak,
[*Dynamic Matrix Inverse: Improved Algorithms and Matching Conditional Lower
Bounds*](https://arxiv.org/abs/1905.05067), FOCS 2019, pp. 456--480,
doi:10.1109/FOCS.2019.00036.

- Full-version PDF p. 17, Theorem 4.1 preprocesses an `n x n` matrix in
  `O(n^omega)` field operations, then supports a column update and inverse-row
  query in ambient-polynomial time; the optimized current-exponent bound
  reported there is about `n^1.529`.
- On the same page, Theorem 4.2 gives element updates and inverse-element
  queries after the same `O(n^omega)` preprocessing, with optimized exponent
  about `n^1.407`.

**Audit.** These are powerful changing-inverse primitives, but their unit is
the ambient dense dimension, not exposed graph volume, and their preprocessing
is explicitly global.  The paper's conditional lower bounds concern its
dynamic algebraic models; they do **not** imply a lower bound for the stronger
specialized Stieltjes/adjacency-list OP2 model and are not used that way here.

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
   only the requested objective accuracy.  The active-edge note proves that a
   known residual-derived threshold suffices; the data structure still has to
   report threshold crossings within the total ledger.
5. **Published dynamic inverse machinery is still global.**  Dynamic Schur
   complements and matrix inverse maintenance use ambient preprocessing and
   ambient-dimension update/query bounds.  They do not supply exposed-volume
   obstacle support discovery.
6. **A dynamic response theorem is no longer necessary for OP2.**  The active-
   edge note proves a threshold-batch depth bound and fully charges a bounded
   number of fresh local face solves and complete active-row scans.  A
   persistent changing-face response remains open only as a potentially
   sharper implementation.

The theorem-level formulation and the exact projected-CG obstruction are in
`manuscript/notes/active_edge_lcp/`.


### Second-night weighted constructor check (8 September 2026)

**Source.** Abraham and Neiman, [*Using Petal-Decompositions to Build a Low
Stretch Spanning Tree*](https://www.cs.bgu.ac.il/~neimano/spanning-full1.pdf),
SIAM J. Comput. 48(2):227–248 (2019). The checked author full version is
dated March 22, 2012. Theorem 1 is on PDF p.2; Sections 6–7, PDF pp.17–18
(printed pp.16–17), explicitly extend the construction to arbitrary positive
weights. Their scale contraction limits each edge's participating scales.
The stated stretch and work are O(m log n log log n). The weighted-extension
pages were rendered and visually checked. This is a supplied graph source
primitive; no local discovery is provided.

**Source.** Koutis, Levin and Peng, [*Faster spectral sparsification and
numerical algorithms for SDD matrices*](https://arxiv.org/pdf/1209.5821v3),
ACM Trans. Algorithms 12(2), Article 17 (2015), DOI 10.1145/2743021.
Checked arXiv v3: Sections 3.1/3.4 and 4.1–4.2, Theorem 4.2 on PDF p.9
(rendered and visually checked). General positive weights are permitted
with minimum weight scaled to one. The general sparsifier has O(n log n)
edges at constant approximation and uses fixed solver precision. The
solver interface is a symmetric approximate inverse operator. Later
integer-weight or dense-graph shortcuts are not needed here.

**Audit / inference.** These primitives are relevant to CPW's construction,
but CPW Lemma 4.4 itself explicitly retains a polynomial weight-ratio
hypothesis (PDF p.19); its recursive schedule is on p.20, both visually
checked. The new note-local edge-floor wrapper and simultaneous range
theorem do not by themselves establish that hypothesis for shrinking n.
A source-derived weighted constructor and global confidence allocation
must be reconciled before removing it. The candidate supplied recurrence,
with all vertex-piece work and nonconstant base costs, is saved in
`SUPPLIED_GLOBAL_RECURSION_PROBE.md` in the incremental note. It remains
Conditional at this checkpoint. General OP3 and local discovery remain Open.

### Second-night confidence wrapper (8 September 2026)

**Source.** Joel Tropp, [*User-Friendly Tail Bounds for Sums of Random
Matrices*](https://users.cms.caltech.edu/~jtropp/papers/Tro11-User-Friendly-FOCM.pdf),
Found. Comput. Math. 12:389–434 (2012), DOI 10.1007/s10208-011-9099-z.
Corollary 5.2, PDF p.29, was rendered and visually checked. Its independent
positive-semidefinite matrix Chernoff bounds give the two-sided sampling
failure bound used in the incremental note. The journal page confirms the
2012 volume; the online publication date was August 2, 2011.

**Proved here / inference.** Independent complete resistance estimates,
coordinatewise medians and charged sampling yield requested failure
probability p, assuming an explicit joint constant-probability estimator
contract. The audit checks 180 weighted cases and 565,178 exact sample
draws; this validates finite algebra and does not empirically establish
the probability theorem. No fast resistance estimator is implemented.
The full supplied near-linear recurrence is now formalized conditionally
on the actual positive-weight constructor contract. CPW's printed
polynomial weight-ratio hypothesis is still not silently removed.

**Final source review.** CPW Claim 5.14, PDF p.28, was rendered and
visually checked: its displayed case condition is reversed relative to
the proof below it. The proof and the affected-edge sum in equation (5)
on p.29 use the consistent condition. A small unit-path routing example
and the remaining constructor review map are recorded in
`WEIGHTED_CONSTRUCTOR_REVIEW_20260908.md` in the incremental note.
This display mismatch is not a claimed refutation of the final theorem.

### Third-campaign rooted-piece correction (8 September 2026)

**Source / Refuted intermediate claim.** CPW arXiv:2105.14629v2,
Definitions 5.4/5.7 and Lemma 5.9, PDF pp.22–23 (p.23 rendered and
visually checked), define local stretch over a whole forest component
and include original edges retained in the forest. On a unit star with
m leaves and at most j components, that maximum is at least m-j+1,
with equality obtainable by rooting at the center and isolated leaves.
Taking m=2^(2k), j=2^k contradicts the literal claimed
O(m log n log log n/j) intermediate bound. The source proof on PDF p.27
identifies a component with one decomposition piece; several pieces
meeting at the same root can remain in one component. This observation
does not refute the final spectral-constructor or diffusion theorem.

**Proved here.** The incremental note instead proves
`thm:op3-rooted-piece-spectral-comparison`: for edge-disjoint rooted
pieces that meet only at a shared component root and have individual
routed stretch at most kappa, scaling the forest by kappa and the
resulting forest-plus-core graph by 3 gives G <= Q <= 21*kappa*G.
It includes all original edges and explicitly charges core aggregation.
The weighted ownership theorem in `sec:op3-weighted-tree-ownership`
constructs pieces with at most two shared boundaries in linear supplied
tree work, including high-degree roots, heavy singleton owners and all
temporary allocations. The exact audits pass 19,854 spectral cases and
9,042 ownership cases. These are note-local drafts awaiting review.

**Open composition.** The global-congestion corridor choice needs a
common-offset argument for edges with neither endpoint owned by a piece;
the printed identification with restricted congestion should not be
treated as literal equality. The charged tree-path implementation and
corrected routed-load proof are the next target. The full weighted
constructor and supplied recurrence remain Conditional; general OP3
and local discovery remain Open. See the incremental note's
`WEIGHTED_DECOMPOSITION_DESIGN_20260908.md` for the exact obligations.
