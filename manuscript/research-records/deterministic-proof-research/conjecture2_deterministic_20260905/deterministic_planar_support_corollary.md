# Deterministic OP2 when the optimal induced support graph is planar

Status: a positive restricted-case theorem, obtained by composing the
fresh certified batch-stage theorem with an explicitly deterministic
planar SDDM solver. This is not a proof for arbitrary induced supports.
The full graph and its boundary need not be planar, and neither the
optimal support nor an embedding is supplied to the algorithm.

## 1. Primary-source audit

The following sources were checked directly; no prior manuscript notes
or old research directions were consulted.

* Elkin, Emek, Spielman, Teng, *Lower-Stretch Spanning Trees*,
  [primary paper](https://arxiv.org/pdf/cs/0411064), Theorem 3.4
  (printed pp. 8--10), BallCut (p. 13), ConeCut and StarDecomp
  (pp. 14--16). The basic
  weighted construction takes `O(m log n+n log^2 n)` and has total
  stretch `O(m log^3 n)`. Its choices are deterministic; in particular,
  BallCut advances through shortest-distance breakpoints. The paper
  separately discusses a randomized variant in its closing section.
* Spielman and Teng, *Nearly-Linear Time Algorithms for Preconditioning
  and Solving Symmetric, Diagonally Dominant Linear Systems*,
  [primary paper](https://arxiv.org/pdf/cs/0607105), diagonal handling
  in Section 3.1 (p. 7), Proposition 4.1 (p. 9), Lemmas 5.3--5.4
  and the planar paragraph after Theorem 5.5 (pp. 14--17),
  Theorem 10.5 (pp. 34--35), and Lemma C.1 (pp. 56--57).
  Their planar augmentation and
  recursive Chebyshev analysis accept the deterministic tree above.
  The general randomized sparsifier is unnecessary. Appendix C requires
  tree children in embedding order.
* Boyer and Myrvold, *On the Cutting Edge: Simplified O(n) Planarity by
  Edge Addition*, [primary paper](https://jgaa.info/index.php/jgaa/article/view/paper91),
  JGAA 8(3), 241--273 (2004),
  gives deterministic linear-time embedding and obstruction detection.

The conclusion below is an explicit composition of these ingredients,
rather than an assertion that every algorithm called a nearly-linear
planar solver is deterministic. The faster tree routine mentioned in
later versions of Spielman--Teng is not needed here.

## 2. A deterministic planar SDDM solve really costs n times polylogarithms

Here is the parameter check for that composition. Let A be positive
definite, symmetric, diagonally dominant, with nonpositive off-diagonals,
and planar off-diagonal graph. Handle connected components separately.
For one component write

    A=L_G+D0, D0>=0 diagonal.

Keep D0 in every preconditioner. Do not introduce a common ground apex:
that would change the planarity question.

Let N bound the starting dimension. The deterministic tree construction
supplies a tree T with

    eta(G)=sum_e max(stretch_T(e),1) <= s*m,
    s=C*(1+log N)^3,

for an absolute C, enlarged to cover all smaller recursive graphs.
All ties may be resolved by labels. The planar augmentation procedure,
with an integer parameter r, gives a subgraph U satisfying

    U <= L_G <= (12*eta(G)/r)*U,
    |E(U)| <= n-1+3*r.

Here and below inequalities between matrices mean Loewner order.
The augmentation, its tree decomposition, and its selected connecting
edge for every cluster pair are deterministic. Its planar size estimate
uses the computed cyclic embedding order.

Choose `kappa=C1*s^2`, with a sufficiently large absolute C1, and
`r=max(2,ceil(12*eta(G)/kappa))`. If r is too large for a reduction,
or the component dimension is `O(s^2)`, stop and use a dense direct
solve on this polylogarithmic-sized component. Otherwise put

    B=U+D0.

The explicit sandwiches give

    B <= A <= kappa*B.

For r=2 this remains valid because that branch means
`12*eta(G)/kappa<=2`. Adding D0 preserves the sandwich because
`D0<=kappa*D0`; no claim about an unscaled condition-number ratio is
needed. Since `m>=n-1`, and nonterminal n exceeds a sufficiently large
multiple of s^2, rounding r adds only a constant-factor term. Thus

    |E(U)|-(n-1) = O(m/s).

Eliminate vertices with off-diagonal degree at most two from B. This
uses linear arithmetic, creates only O(n) factor entries, and leaves
a planar SDDM system with `O(m/s)` nonzeros. Positive definiteness
ensures that every pivot is positive. Grounding diagonals do not count
as off-diagonal edges in this step.

The recursive Chebyshev construction uses `O(s)` calls to the next
level for a fixed-factor inverse approximation. By increasing C1, its
recursion branching factor times the graph-size reduction factor is
less than a fixed number below one. Consequently the full hierarchy,
all sparse factor applications, and the outer iterations cost

    (n+m)*polylog(N)*log(2/zeta)                       (1)

to obtain relative A-energy error zeta. Dense work at terminal systems
of dimension `O(s^2)` changes only this fixed polylogarithmic exponent.
This is `m*polylog(n)`, not an `m^(1+o(1))` substitution.

Planarity can be recognized and an embedding recomputed at each level
in `O(n_i+m_i)` time. These sizes decrease geometrically, so all such
calls are included in (1). The tree construction takes the reciprocal
of conductance as edge length; weighted shortest paths and all radius
choices are deterministic. No sparsifier sampling, random initial
vector, randomized spectral test, or randomized retry is used.

The statement concerns the arithmetic/state-word model of the problem
definition. The source also analyzes finite-precision recursive solves;
this note does not claim a new implementation or an optimized practical
logarithmic exponent.

## 3. Applying the solver to the actual RPPR principal matrix

Use the fresh notes `inexact_batch_decay.md`, `batch_pivot_decay.md`,
`batch_pivot_audit.md`, and `certified_envelope.md`. Let
`S*=supp(x*_rho)` and assume only that `G[S*]` is planar. Put
`M=vol(S*)<=1/rho`.

Every safely admitted set S is contained in S*. Thus every principal
off-diagonal graph G[S] is planar even if the full input graph is not.
The normalized matrix Q_SS need not be diagonally dominant in its raw
coordinates. Use the congruence

    H_S=D_S^(1/2)*Q_SS*D_S^(1/2)
       =c*L_(G[S])
          +diag(alpha*d_i+c*(d_i-deg_(G[S])(i))),
    c=(1-alpha)/2.                                   (2)

This is a positive-definite grounded SDDM matrix with exactly the
off-diagonal graph G[S]. The degrees in (2) are the original graph
degrees. They are already obtained and charged when the admitted
vertices are read. The diagonal contribution of outside neighbors is
kept numerically; those neighbors are not joined to an artificial apex.

For the principal right-hand side `h_S=b_S-alpha*rho*sqrt(d_S)`, solve

    H_S*y=D_S^(1/2)*h_S, x=D_S^(1/2)*y.

The energy errors agree exactly under this congruence:

    ||x-X(S)||_(Q_SS)=||y-y_exact||_(H_S).             (3)

The fresh safe-principal estimate gives `||X(S)||_(Q_SS)<=sqrt(alpha)`.
Choose

    delta=sqrt(epsilon*alpha*rho/8),
    zeta=min(1/2,sqrt(alpha)*delta).

A relative-energy solve of accuracy zeta has, by (3),

    ||Q_SS*x-h_S||_2
       <= ||x-X(S)||_(Q_SS)
       <= zeta*sqrt(alpha) <= alpha*delta,            (4)

because `Q_SS<=I`. Thus it meets exactly the residual certificate
required by the inexact batch theorem. Evaluate (4) explicitly with
one additional sparse product, and construct the lower vector

    ell_i=max(0,x_i-delta*sqrt(d_i)).

The precision factor is only logarithmic in `1/epsilon`, `1/alpha`,
and `1/rho`: when the minimum does not choose 1/2,
`zeta=alpha*sqrt(epsilon*rho/8)`.
Moreover `alpha*D_S<=H_S<=D_S`, so

    kappa(H_S)<=max_(i in S)d_i/[alpha*min_(i in S)d_i]
       <= M/alpha <= 1/(alpha*rho).

Any condition-number logarithm in implementing or certifying the
numerical solve is therefore local and polynomially bounded by the
allowed parameter logarithms. No degree bound on an inactive boundary
vertex is used.

## 4. Fully charged algorithm and locality

Run the explicit certified batch algorithm, with

    T=1+ceil[ (1/(2*sqrt(alpha)))*log_+(8*alpha/epsilon) ].

At each stage:

1. Form the induced principal graph from cached active incidences.
   Test its planarity and compute an embedding. This costs
   `O(vol(S))` times deterministic dictionary logarithms.
2. Build (2), solve to (4) by the deterministic planar solver, evaluate
   the residual certificate, and materialize ell.
3. Scan the cached active incidences to accumulate every boundary
   residual and admit all strict violations of ell. Query each newly
   exposed degree once; scan a vertex's adjacency list only after its
   safe admission.
4. At the stage budget, or an empty boundary screen, emit ell.

The inexact batch theorem guarantees objective gap below epsilon and
keeps all admitted sets inside S*. At each stage, recognition,
embedding, matrix assembly, solver arithmetic, certificate evaluation,
boundary work, and vector materialization cost at most

    vol(S)*polylog(M,1/alpha,1/rho,1/epsilon).

The exposed boundary has at most O(M) labels, regardless of the sum of
their degrees. Their adjacency lists are not recursively scanned.
Each admitted adjacency list is first obtained once, and final output
has at most M coordinates. Rebuilding a fresh planar hierarchy every
stage is fully paid; no persistent factorization or support oracle is
being presumed.

Summing the stage cost proves

    total work = O_tilde(1/(rho*sqrt(alpha))),         (5)

with the stated logarithmic dependence on objective accuracy. Storage
is M times polylogarithmic factors. Both recognition and solver input
are confined to exposed data; the algorithm never tests planarity of
the unknown full graph or of the unknown final support.

If a discovered principal graph is nonplanar, the algorithm can switch
to the deterministic Chebyshev baseline from the fresh batch note.
This preserves correctness on all graphs; guarantee (5) is asserted
only on instances whose optimal induced support is planar.

## 5. Scope

This proves the requested deterministic OP2 bound on the planar-induced-
support class, including instances with nonplanar unvisited regions or
arbitrarily large inactive boundary volume. It does not provide the
missing nearly-linear deterministic restricted solver for general
cyclic supports. The result is a mathematical corollary with a checked
dependency chain, not a claim that a production planar solver was
implemented in this session.
