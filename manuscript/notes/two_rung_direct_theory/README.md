# two_rung_direct_theory

Direct theory for the literal charge-aware two-rung SOR policy. The note
proves that the empirical ranking key is a graph-universal factor-two
approximation to exact quadratic decrease per charged operation, gives
finite-work and refreshed-ranking bounds, and solves the complete two-vertex
dynamics. On a single edge, every band factor below 3.33019 has an eventual
one-push exact settlement property; in particular, the measured factor 2.5
is certified even when the self-reflection-only test rejects it. On a
sufficiently long endpoint-seeded path, the fully refreshed measured
absolute-residual rank is an exact parity-wave event schedule: through depth
L it uses
floor((L+1)^2/4) spreading pushes, reaches an explicit signed plateau, and
finishes with one no-repeat exact sweep plus at most one outer push. This
gives accelerated explored-volume work up to the attenuation logarithm.
Every negative waiting packet has a strictly larger positive dependency
certificate, so refreshed ranking never charges it. A live positive-sign
guard extends the same theorem to literal snapshot batches of arbitrary size
without additional charged coordinate work. The guard cannot be removed for
arbitrary batches: full-frontier batching provably charges a negative
endpoint in its third batch. For `alpha > 1/49`, including the measured
values `0.025` and `0.04`, a partial-layer invariant proves that the original
top-1/32 snapshots preserve the complete spreading and terminal path counts
without a sign guard. A separate 34-corner legal interface refutes static
top-1/32 parent closure, so the smaller-alpha path question requires a
trajectory-history invariant. On a symmetric q-arm
spider, refreshed ranking has an exact
center-echo prefix: it spends Theta(q/sqrt(alpha)) work in
Theta(1/sqrt(alpha)) consecutive center pushes, about half on negative
residual. This saturates the desired budget at one branch and isolates
repeated branching as the next obstruction. Grouping each symmetric radial
shell into one block removes the echo, reduces both rungs exactly to the path
recurrence, and proves the accelerated explored-volume bound on the complete
symmetric spider. More generally, every level-regular rooted tree has an
exact shell-energy quotient: radial block SOR becomes a symmetric
variable-coupling chain with edge impedance
`2 sqrt(phi_i / (d_i d_(i+1)))`. The homogeneous `g`-ary bulk is critically
matched to the path wave only for `g = 1`; for `g > 1` the exact mismatch
debt is `lambda^2 ((g - 1) / (g + 1))^2`. Persistent geometric branching
also produces a proved `Theta_g(1 / sqrt(alpha))` root echo, so a constant
visit factor is impossible. Geometric shell volume absorbs a triangular
visit profile with common factor `K` into `O_g(K V)` work. More decisively,
every finite explored ball for homogeneous `g > 1` has uniform Dirichlet gap
`(sqrt(g) - 1)^2 / (2(g + 1))`. A retrospective final-region contraction
therefore proves both rungs terminate with
`O-tilde_g(V_exp / sqrt(alpha))` work for every fixed band factor, without a
per-shell visit hypothesis. A positive Jacobi supersolution extends this
result to variable level profiles. In particular, arbitrary offspring
counts bounded below by `g > 1` have the same homogeneous gap, while an
explicit unary-corridor Rayleigh vector proves that unbounded unary runs have
no depth-independent gap. The vector
`sqrt(d_u) g^(-depth(u)/2)` further gives the same theorem on completely
nonsymmetric rooted trees with at least `g` children per vertex, for the
fully refreshed individual-coordinate policy.

The unrestricted graph-uniform target is false. On the three-vertex path
seeded at its center, the literal top-1/32 policy always has singleton
batches but, for `B = 2.5`, `eps_ppr = 0.01`, and `alpha <= 1e-4`, its
spreading work satisfies
`W_spread >= alpha^(-3/2) / 1408` while `V_exp = 4`. The exact macrocycle has
`Theta(1 / sqrt(alpha))` center echoes and a `1 - Theta(alpha)` slow mode.
Thus a positive general framework needs one of three certificates:
persistent expansion, a causal corridor wave, or a boundary operation that
eliminates the reflecting-leaf slow mode.

The note now proves the third certificate for closed pendant forests.
Permanent leaf-to-root Schur elimination changes only the attachment
diagonal, creates no fill between surviving core vertices, erases the
reflected trajectory, and costs linear forest work. On a reached q-star it
solves the full system in `O(q)` work uniformly in `alpha`; exact leaf
settlement with the old center pivot would still require
`Omega(1 / alpha)` steps. Splicing this operation into the radial parity
wave proves the accelerated volume bound on every finite symmetric spider,
including when the far leaves are reached.

In the repository's newer response-preconditioned language, the forest
operation has an exact spectral lift: every eliminated forest coordinate
becomes a unit generalized eigenvalue, and the remaining effective condition
number is exactly that of the Schur core. Repeated degree-one peeling gives
the canonical maximal reduction to the graph 2-core. A completely exposed
graph with a k-vertex 2-core therefore has an exact
`O(cvol(V) + k^3)` dense-core solve, while arbitrary core preconditioners and
response solvers lift with only linear forest construction and recovery.
Absorbing one newly certified pendant component is exactly a rank-one
attachment update: Sherman--Morrison shows that the entire core correction is
one Green-function column and that all exterior demand changes form one
nonnegative range-add vector. This pinpoints the remaining online task as
finite-band crossing reports on the cyclic core, rather than forest algebra.

Build with make (latexmk).
