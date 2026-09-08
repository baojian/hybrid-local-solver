# Can a spectral approximation itself guide conservative discovery?

Next proof target, **Open until checked**. This is an obstruction to using
the approximate matrix's obstacle support directly as an envelope. It is
not an objection to iterative refinement with a spectral preconditioner,
and is not a computational lower bound for OP3.

## Candidate exact family

Use the same original path 0,...,8N, seed N, N>=4, and
lambda=2N/(8N^2+1), e=2lambda, delta=e/8=lambda/4.
Its conservative obstacle has endpoint u0_0=lambda/2=2delta, as proved in
`thm:op3-fourth-power-support-obstruction`.

Increase conductances on exactly the right-hand edges (N,N+1),...,
(2N-1,2N) by eta=1/N^2. Write L_R for the unit Laplacian of those
edges and L_hat=L+eta L_R. Keep the load b=e_N-lambda*d with the
ORIGINAL unweighted degrees d. Then L <= L_hat <= (1+eta)L.

On T={1,...,2N-1}, impose zero endpoints 0,2N. Let c_i be the
conductance of edge (i-1,i): 1 for i<=N, 1+eta for i>N. An exact
Dirichlet solution z can be computed using flux increments

j_i = j_1 + 2lambda(i-1)                 i<=N,
j_i = j_1 - 1 + 2lambda(i-1)             i>N,
z_i = sum_(k<=i) j_k/c_k,

where

j_1 = [1-lambda*(4N-2+eta*(N-1))]/(2+eta),
j_1-lambda = [1-2eta*N^2]/[(2+eta)*(8N^2+1)] < 0.

Check independently from the generic weighted Dirichlet prefix solve:
the final potential z_(2N) is exactly zero. j_1>0; all left increments
are positive, and all right increments are negative, so z>0 on T.
The omitted original endpoint has incoming weighted flux j_1<lambda.
At 2N the incoming flux is 1-j_1-2lambda*(2N-1), which lies in [0,2lambda]
provided j_1>=1/(8N^2+1). Verify this inequality for all N>=4.
Thus z is the exact obstacle for L_hat and the original-degree load.
It omits the significant endpoint 0.

## Positive definite version and quantitative consequence

Choose the SAFE original comparison t=e^4/128 and lazy a=t/(2-t).
Let M_t=L+tA=(1-t)L+tD and M_hat_t=M_t+eta L_R.
Then

M_t <= M_hat_t <= (1+eta/(1-t)) M_t <= (1+2/N^2) M_t.

M_hat_t z = L_hat z+t A z >= b because A and z are nonnegative.
Both matrices are strictly diagonally dominant M-matrices (row sums t*d).
Hence the exact perturbed obstacle u_hat_t <= z and u_hat_t,0=0.
The earlier safe comparison gives u_t,0 > 2delta-delta/2=3delta/2.
Thus the support of the perturbed obstacle omits a coordinate that is
significant even for the ORIGINAL positive-target obstacle, despite a
relative spectral error at most 2/N^2=O(e^2), tending to zero.

Consequently any general spectral-only sufficient tolerance must be at
most order e^2 (up to constants) for this support-containment rule. Do
not assert that e^2 is sufficient without a separate proof. In particular,
a constant-quality approximate factorization cannot be substituted
directly for the obstacle matrix to find a safe envelope. It remains
valid as a preconditioner for a proved sufficiently accurate computation.

## Candidate matching sufficient stability theorem

There may also be a matching sufficient accuracy power, under explicit
M-matrix and nonnegative-row-sum assumptions. Let vol(G)>4/e, lambda=e/2,
M=M_t for t in [0,1], and let M_hat be a symmetric M-matrix with
nonnegative row sums and (1-eta)M <= M_hat <= (1+eta)M, eta<=1/2.
Let u,v be their same-load obstacle minimizers (check existence at t=0).

Both outputs have residuals r>=0, active residual lambda*d, and total
residual at most one, since matrix row sums are nonnegative. Thus each
original support volume is at most 2/e and their union W has volume
at most 4/e < vol(G), hence is proper. The Dirichlet original matrix
M_W is positive definite, even at t=0.

Write z=v-u and E=M_hat-M. The two variational inequalities give
z^T M z <= -z^T E v <= eta ||z||_M ||v||_M, hence
||z||_M <= eta/(1-eta) ||u||_M.

For t<=1/2, M_W >= L_W/2, and each Dirichlet inverse diagonal is at
most twice a simple path length to W's outside, at most 2vol(W)<=8/e.
Prove this path bound directly by Cauchy--Schwarz along that path; no
effective-resistance source theorem is required. For t>=1/2,
M_W >= D_W/2, giving the same coarse bound. The original potential
maximum is at most 2vol(supp u)<=4/e by the earlier proper-support
superlevel bound, or by mass when t>=1/2. Hence u^T M u=b^T u<=4/e.

Together, ||u-v||_infty <= sqrt(32) eta/[e(1-eta)] <12eta/e.
Therefore eta<=e^2/192 implies error at most e/16 and guarantees that
supp(v) contains {u>e/8}. Empty-support cases are immediate. Check all
inequalities, including the union properness and the original-degree
volume accounting for M_hat. The weighted-path family above has relative
spectral error asymptotic to 4e^2, so the POWER TWO would be sharp up to
constants for this matrix-replacement support rule.

Do not claim arbitrary spectral approximations preserve M-matrix signs
or nonnegative row sums; those are explicit premises. The factorization
product in an arbitrary source is not automatically such a matrix. The
result would concern a same-load matrix replacement, not a lower bound
on preconditioned iterative work.

## The sign condition is not automatic from a spectral guarantee

For a physical star with m leaves, center first, let gamma=1-t. The
center elimination decomposes M into one positive rank-one pivot term,
leaf grounding (1-gamma^2)I, and the leaf clique
C=gamma^2(I-J/m). Set Z=M-eta*C (zero-extend C at the center).
Since 0<=C<=M, (1-eta)M<=Z<=M and Z is positive definite for eta<1.
Its row sums are the original nonnegative row sums. However, every
off-diagonal leaf pair of Z equals eta*gamma^2/m>0, violating the
M-matrix sign condition. Thus an abstract spectral-factorization theorem
cannot supply that condition without a separate argument.

For a degree-one leaf seed and sufficiently large lambda (e.g. 3/4,
m=3 and gamma=1/2), its Z-obstacle should have only that leaf positive.
At another zero leaf the Z-residual is negative. Verify this small
certificate before claiming that the usual active-volume proof is
unavailable without the sign condition. This does not claim that a
particular random source execution returns this Z.

## Source transfer to check

Kyng--Sachdeva, arXiv:1605.02353v1 (May 2016), primary PDF downloaded to
`/tmp/op3-ks16-approx-elimination.pdf`. Theorem 1.1 PDF p.2 supplies a
constant-quality approximate Cholesky factorization; Theorem 1.2 p.3 uses
iterative refinement. Theorem 3.1 p.5 gives explicit relative-accuracy
dependence; Algorithm 1 p.6 uses a uniformly random permutation of the
supplied vertices. Remark 3.2 and Appendix B allow sampling among the
vertices of at most twice the average multi-edge degree, not among a
positivity-constrained active frontier. Verify these page pointers against
the rendered pages. The PDF's printed page number is one less than its
one-based PDF page number.

Its clique sampler uses only the pivot row, an attractive local feature.
Its complete theorem still starts from all supplied graph edges. Neither
its vertex-order analysis nor its spectral conclusion automatically supplies
a local positivity-constrained discovery algorithm. Record a compact source
map and synchronized bibliography/index if this direction is formalized.
