# OP3: what the existing lower bounds establish

**Verdict:** the worst-case inverse-accuracy target is supported. The
conjectured upper bound, uniform in the teleportation parameter, remains
**Open**. This passes the user's condition for another 600 active minutes;
it is not a declaration that OP3 has been proved.

## Exact model and the direction of the comparison

OP3 takes a point seed on a finite connected simple undirected unweighted
graph. Its output is an explicit sparse vector; omitted entries mean zero.
All degree/adjacency queries, repeated arithmetic, stored and emitted words
are charged. No full-graph preprocessing or unrestricted ambient-size
logarithm is free. With the project's lazy alpha, write
`gamma=(1-alpha)/(1+alpha)` and `bar_alpha=1-gamma`. The original certificate
is `0 <= r=e_v-(D-gamma*A)u <= eps_appr*d`, with output
`p=bar_alpha*D*u`. Inverse positivity gives
`0 <= (pi-p)/d <= eps_appr`. Consequently a semantic output lower bound
also applies to this stronger ACL requirement. A semantic approximation
does not automatically supply the original residual certificate.

The existing [problem-definition proof attempt, Proposition 5](../problem_definitions/open_conjectures_proof_attempt.md)
already gives the fixed-parameter star output lower bound. The new note
section imports that result explicitly and audits the parameter mapping;
it does not present that proof as a new discovery. The original star has
leaf mass `(1-alpha)/(2*m)`. For `0<alpha<=1/3`, choosing
`m=floor(1/(8*eps_appr))`, `eps_appr<=1/16`, forces at least
`1/(16*eps_appr)` explicitly emitted leaves. The constant is uniform as
alpha tends to zero. At alpha=1 the PPR vector is the seed alone, so a
lower bound asserted for every alpha in `(0,1]` would be false.

## Primary-source transfer map

**Source: Wei, Wen and Yang, ICDT 2024.**
[Published record](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICDT.2024.9),
[checked full version, arXiv:2401.01019v1](https://arxiv.org/pdf/2401.01019v1).
PDF pp.2–3 define undirected SSPPR-D with degree-normalized absolute error,
sparse output and simultaneous success probability `1-1/n`. Alpha is a
fixed nonlazy decay probability. Page 1 suppresses polylog(n); Appendix D,
p.22 assumes a Theta(m) preprocessing step for its RBS subroutine.
Theorem 20, p.24 gives the stated improved SSPPR-D query bound. The
output discussion on p.3 supports a worst-case accuracy comparison. We
do **not** import its mass-over-error expression as a lower bound on each
individual graph/seed; see the cycle counterexample below. Neither the
constant-alpha convention nor the prepaid index establishes OP3's local,
alpha-uniform upper bound. Publication: LIPIcs 290, 9:1–9:19,
14 March 2024, DOI 10.4230/LIPIcs.ICDT.2024.9.

**Source: Bertram and Jensen, 2026 preprint.**
[Personalized PageRank Estimation in Undirected Graphs](https://arxiv.org/pdf/2602.10843v1),
11 February 2026. PDF p.3 fixes alpha and gives discovered-label
degree/adjacency access, optionally strengthened by random jumps,
degree-sorted neighbors and adjacency tests. Equation (2), PDF p.7,
requires thresholded relative/additive error for each target with constant
failure probability. Theorem 4.2.2, PDF p.26 (printed p.24), gives
`Omega(min(m,1/delta))` even averaged over a uniform source and with all
three extra query types. Its proof chooses the error constant at most
`(1-alpha)^3*alpha/4`; its hard graph can be disconnected. This is a useful
undirected frontier, but degree normalization, connectedness and the
alpha-dependent constants require separate reductions. It does not
establish an inverse-alpha lower bound for OP3.

**Source: Jiang, Liu, Luo and Xiao, PODS 2026.**
[Near-Optimality for Single-Source Personalized PageRank](https://arxiv.org/pdf/2507.14462v5),
checked v5, 12 April 2026. This replaces the earlier title *Tighter Lower
Bounds for Single Source Personalized PageRank*. The primary PDF gives
Proc. ACM Manag. Data 4(2), Article 110, May 2026, 55 pages,
DOI 10.1145/3801906; the ACM page returned 403 during this audit.
Definitions 1.1–1.2, p.3 fix alpha and global failure probability.
Theorems 1.6/1.8, pp.5–6 give lower bounds
`Omega(min(m,log(1/delta)/delta))` for thresholded relative error and
`Omega(min(m,1/epsilon^2))` for absolute error. Section 2, p.6 uses
directed graphs and arc queries with random jumps. Section 5, pp.16–18
encodes a Bernoulli matrix in a directed hard family. These are genuine
generic bounds for the stated tasks, but neither the graph model nor
the accuracy is OP3's; no contradiction or direct upper-bound transfer
is inferred.

**Source: Wang, Wei, Wen and Yang, STOC 2024.**
[Revisiting Local Computation of PageRank: Simple and Optimal](https://arxiv.org/pdf/2403.12648v1).
The repository already records this paper in `docs/literature/local-solvers.md`.
The checked full version, p.2, uses directed graphs, fixed nonlazy alpha,
incoming/outgoing adjacency queries and optional uniform jumps. Its
contributor problem follows a target column, and its other task estimates
global PageRank centrality. The contributor lower bound is not a bound
for our undirected point-source row. Published in STOC 2024, pp.911–922,
DOI 10.1145/3618260.3649661. Keep it as model-comparison evidence unless a
valid degree/error/access reduction is supplied.

## A necessary quantifier correction

Let `H(G,v)=sum_i pi(v,i)/d_i`. The implication
`work(G,v,epsilon)=Omega(H(G,v)/epsilon)` on **every** instance does not
follow from the obligation to emit entries above epsilon. That obligation
only gives the actual count of those entries. Large total mass can be
concentrated in a few coordinates or spread below the threshold.

**Proved here:** a local truncated Neumann computation supplies a direct
counterexample to that pointwise interpretation. At lazy alpha=1/3,
gamma=1/2 and epsilon=2^-k, take a cycle with `n=2^(2*k+2)` vertices.
After k walk terms the original nonnegative residual has total mass
`2^-k`, hence is at most `epsilon*d` entrywise. There are O(k) exposed
vertices and O(k^3) fully charged word operations with simple deterministic
linear-search maps. Every seed behaves the
same, while `H=1/2` and `H/epsilon=2^(k-1)`. Here `1/epsilon=o(n)`, so
the distinction persists in a sublinear regime and after averaging over
sources on this particular graph. This does **not** disprove an
existential worst-graph bound, including a worst-graph average-source
bound. We make no broader claim about the source theorem's intended
quantifiers.

The sharper one-coordinate certificate also helps expose the issue. On
any original graph, a single seed-degree query permits
`u_v=max(0,1/d_v-epsilon)`, with all other coordinates zero, whenever
`epsilon*d_v >= gamma/(1+gamma)=(1-alpha)/2`. On center-seeded stars
this threshold is exact among outputs supported only at the seed. This
improves the sufficient shortcut already in our capped-sublevel section;
it does not establish an arbitrary-graph solver.

## Consequences for the next research blocks

1. Preserve the `O_tilde(1/eps_appr)` target as worst-case output-optimal
   in accuracy. Do not call the whole conjecture valid from a lower bound.
2. Treat polynomial inverse-alpha lower bounds for APPR, coordinate methods
   or FIFO exploration as restrictions on those algorithms or access rules.
3. Continue the weighted supplied-constructor audit and potential-driven
   local discovery. The lower-bound review has not supplied a reason to
   abandon either route, nor a proof that either succeeds.
4. Any new literature reduction must state graph direction/weights,
   connectedness, source distribution, output representation, error,
   failure probability, preprocessing and every alpha/ambient-size factor.

## Reproducibility

The local primary-PDF caches are temporary, not tracked paper-library files.
SHA-256 digests of the checked bytes:

| Version | SHA-256 |
| --- | --- |
| 2401.01019v1 | `25977e3c15a9d80eb30d67698fc6e1cc4deaccdcf763c0fcbe3de750784d4d87` |
| 2602.10843v1 | `5300afe8fae603256ec78b3cd3ec134a4f111b812cc1fbaaad0614f455817a02` |
| 2507.14462v5 | `6f1ef8548f0a7cb93a1a336b5e9128604aa9b6e727b58def64c8bdf9026e249e` |
| 2403.12648v1 | `fc15bdbba6cb9888a4acc1874b74671a01fb435c370b92a784213fd654fa7141` |

WWY PDF pp.2–3 and BJ PDF p.26 were rendered and visually checked.
Exact construction and operation evidence is recorded in
`LOWER_BOUND_QUANTIFIERS_AUDIT.json`: 44 independent star solves, 132
exact seed-only thresholds, 231 uniform-alpha output cases, 1,096
degree-gate inputs and 36 local cycle runs. All pass with exact fractions.
