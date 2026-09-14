# Comparison with previously explored manuscript directions

2026-09-05. This audit concerns the separately reported complete continuation
proof. It does not retroactively validate the failed or conditional algorithms.

| Earlier issue | What the reported proof actually uses |
|---|---|
| Repeated deterministic CG on newly exposed faces adds another square-root condition factor. | No restricted linear-system solve occurs. Each stage uses local matrix-vector updates and ordinary scalar waterfilling. |
| Exact safe-box / residual-metric projection has an unresolved cheap implementation. | The computed projection is Euclidean onto a density box and mass cap. A special projection-normal inequality supplies only the analytical comparison needed for the second energy. |
| Euclidean projection is not generally nonexpansive in a matrix metric. | No such general assertion is made. The signs are checked against one unregularized response comparator, using the diffuse source, upper box, and mass cap. |
| Projected accelerated iterates can leave the true support. | Iterates may leave it. A margin outside the larger analytical support at r/2 and a squared-response estimate bound cumulative repeated volume. |
| Raw signed residual mass and Chebyshev l1 propagation can grow too much. | The proof keeps the selected signed flow and uses Cauchy-Schwarz with a separately proved squared residual bound for the actual constrained trajectory. |
| A mass cap alone does not prove a root local-work bound. | The box and diffuse-source continuation are also essential to the second-energy argument. The theorem is not asserted for an arbitrary point-source mass-capped run at the final regularizer. |
| Approximate face solutions may not preserve exact feasibility or support. | Objective-controlled terminal PG/clipping yields a safe baseline without a strict-complementarity margin; bounded rounding has an explicit perturbation analysis. |
| Persistent exact Schur response can require expensive broad updates. | Only the sparse matrix response to emitted kinetic increments is maintained. Old primal values share a scalar decay; no Schur complement or inverse response is stored. |
| Boundary discovery and final materialization can be hidden in a nominal iteration count. | The reporter, degree replies, every first/repeated incidence, fixed source refreshes, retained state, materialization and output have explicit charges. |

In particular, the existing
`spectral_balance_threshold_batch/DETERMINISTIC_HALO_INTEGRATION.md` (dated
2026-09-04) distinguishes valid exact safe-box acceleration from its still
unimplemented support-linear oracle. Its `ResidualAPG` uses a Q^{-1}-metric
projection. The complete continuation proof reviewed here does not call that
oracle. The earlier masked-input and peeling counterexamples therefore do
not directly contradict it.

The global Chebyshev signed-mass assumption is separately disproved by the
finite-tree calculation in `chebyshev-signed-mass.md`. That obstruction also
does not apply to the new second-energy argument, whose diffuse source and
box constraints explicitly control the nonlinear residual trajectory.

This comparison is an interface audit, not a historical-priority claim. It
does not establish that no earlier paper contains a related proof technique.

The later optional exact component branch is limited to at most sixteen
completed vertices. It explicitly charges all small factorizations and face
solves. This does not introduce an unbounded supplied-face solver into the
core continuation proof or assert that its earlier large-face obstruction
has disappeared.
