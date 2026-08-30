# Current research status and open problems

Verified snapshot: 2026-08-29.

This file is a routing summary. The current
[controller broadcast](../../manuscript/notes/_shared/coordination/BROADCAST.md),
the [`registry.toml`](../../manuscript/notes/registry.toml), and each
direction's `STATUS.md` are authoritative for live research state. The cited
proof in the owning note is authoritative for a mathematical claim.

## Bottom line

The desired graph-uniform single-source sparse PPR solver with fully charged

```text
O_tilde(1 / (sqrt(alpha) * eps_ppr))
```

work is not proved. The project has useful local convergence results,
support and volume controls, exact structured handoffs, response identities,
finite-trace counterexamples, and algorithm-specific lower bounds. The
missing step is a graph-uniform composition that preserves accelerated
progress while paying for every local and response operation.

The canonical input is one seed vertex `v`, equivalently `s=e_v`. General
unit-mass distributions remain a stronger extension: linear PPR
superposition can multiply work, and RPPR support discovery requires a
separate merge-aware argument.

The canonical graph is finite, simple, undirected, connected, has at least
two vertices, and has unit edge weights. This is without loss for the
point-source solution: on a disconnected positive-degree graph both PPR and
RPPR restrict exactly to the seed component. Intermediate active faces may
still be disconnected.

On the positive side, rootedness has now closed the complete exact reporter on
promised cactus graphs through an online two-hysteretic heavy--light rebuild
ledger; the next structural gap is a genuinely variable two-port
series--parallel block.

The repository-wide residual convention also remains open. The controller
contract supplies a precise semantic target and sufficient certificate for
direction comparison, but implementations and experiments must still state
their actual stopping rule.

## Stable foundations

The following facts can be reused with their recorded assumptions and source
pointers:

- The shared PPR matrix satisfies `alpha I <= Q <= I`.
- The normalized Laplacian has a simple zero mode, and point-source PPR is
  strictly positive everywhere when `0 < alpha < 1`.
- The RPPR minimizer is nonnegative and has support volume at most `1 / rho`.
- Every RPPR optimal-support component contains a source; with `s=e_v`, the
  support is either empty or connected and contains `v`.
- The degree-normalized gradient certificate in the problem contract implies
  its stated degree-normalized PPR solution bound.
- Literal lazy single-seed APPR has a tight
  `Theta(1 / (alpha * eps_appr))` degree-work bound under its own activation
  rule and stated parameter range.
- Several trajectory-dependent, structural, and graph-family-specific
  response and handoff results are proved. Their qualifiers are part of the
  theorem and cannot be dropped.
- Exact counterexamples have eliminated several simple correction banks,
  restart rules, reporter states, and path lower-bound candidates. Each stop
  applies only to the named mechanism and scope.

Reusable results are indexed in the
[shared results ledger](../../manuscript/notes/_shared/results/README.md).
That ledger routes to proofs; it does not replace them.

## Central AESP--LOCSOR promotion gate

The universal end-to-end claim must remain open until either

```text
Lambda_J = max_(1 <= t <= J) overline_vol(S_t) / gamma_t
         = O(1 / epsilon)
```

is proved with a graph-independent hidden constant, or a correct weaker
structural condition or alternative burn-in work argument is sufficient for
the desired theorem.

Until then, the
[`hybrid_aesp_locsor`](../../manuscript/notes/hybrid_aesp_locsor/STATUS.md)
direction may use its proved trajectory-dependent theorem and explicitly
conditional confinement corollaries, but may not promote a universal
`O_tilde(1 / (sqrt(alpha) * epsilon))` claim into the active manuscript.

## Current frontier

The active endpoint is now the canonical point-source problem `s=e_v`.
Several formerly separate obstructions have been reduced to one online
discovery primitive.  The exact point-source homotopy admits every support
row once by a Stieltjes Schur pivot, the candidate universe is output-linear,
and an APPR envelope of volume `O(1 / rho)` exists within the proved support
radius.  If such an envelope is supplied, fixed-envelope accelerated
projected gradient closes the semantic PPR target.  What is not yet proved on
an arbitrary graph is an output-sensitive online event locator that builds or
reuses that envelope without materializing high-rank inverse responses.

The structural boundary has moved as well.  A two-hysteretic online
heavy--light ledger now closes the exact single-source reporter on every
cactus graph without a supplied final support or decomposition.  The
smallest remaining graph family exposed by the current proof interfaces is a
genuinely variable two-port series--parallel block: ordinary dynamic planar
hulls do not support the required bulk projective pullback and meld.  A
supplied balanced parse has an exact `O_tilde(N+J sqrt(N))` static-hull epoch
fallback and is product-scale when the charged block radius is at least
`sqrt(N)`; the shallow variable-port case remains open.  On any
certified connected proper face, the homotopy slope also gives a canonical
diagonal normalization with a known ground eigenpair at `alpha`; this removes
proper-face eigendata estimation, but not the clipping-direction hypothesis
of the unchanged full-face momentum master.  If the proper-face primitive is
modified to use that diagonal mass and its positive ground-state cap, an exact
diagonal conjugacy restores the normalized full-face algebra.  Its high-gap
and master-sign certificates remain separate conditions.

On a face passing the high-gap certificate, every unweighted pivot response
now splits into an observable ground rank-one term plus a gray remainder
bounded by
`c*q*sqrt(s_v*s_w)/(alpha*(1+q))`.  Point-source unit mass turns all such
remainders into one observable pivot-mass clock.  Conditional on the charged
exact-row refresh primitive, its work is
`O_tilde(F+c^(3/2)*q*P_*F_1/2/(alpha*(1+q)*eta))`.  This meets the target if
the mixed clock--degree quantity is small; in particular, it closes either
the high-degree-row or high-degree-pivot branch `d>=alpha^(-2)`.  The precise
proper-face remainder is therefore the simultaneous low-degree row/pivot
lifetime reporter.  A terminal `K2` pulse shows that the global clock need
not be `O(alpha)`, but does not rule out a smaller per-row clock stopped at
that row's admission or certified rejection.

Thus the project has a graph-uniform terminal solver and complete online
reporters on several large structural classes, but still no graph-uniform
end-to-end accelerated local PPR theorem, complete general event locator, or
finite-precision realization of all exact-real response contracts.

## Active open directions

All directions below are currently `proved-open`: they contain proved scoped
results and a central unresolved target.

| Direction | Exact unresolved target | Resume source |
| --- | --- | --- |
| AESP coordinate descent for RPPR | Build the simultaneous low-degree row/pivot lifetime reporter (or another output-sensitive inverse-response locator) on arbitrary point-source supports, or close the variable two-port series--parallel reporter. | [`aesp_cd_l1_rppr/STATUS.md`](../../manuscript/notes/aesp_cd_l1_rppr/STATUS.md) |
| AESP--LOCSOR hybrid | Build a nonadditive or logarithmic reset ledger across multiple actual nonsettled admissions, or prove another graph-independent prefix bound. | [`hybrid_aesp_locsor/STATUS.md`](../../manuscript/notes/hybrid_aesp_locsor/STATUS.md) |
| Volume-gated acceleration | Establish all-history causal solvency under a declared structural condition, or exhibit debt that survives enough admissions to stop that route. | [`volume_gated_acceleration/STATUS.md`](../../manuscript/notes/volume_gated_acceleration/STATUS.md) |
| Response-preconditioned hybrid | Find sparse collision-sensitive refresh state or a geometrically paid replay/rebuild theorem for changing high-rank cores. | [`response_preconditioned_hybrid/STATUS.md`](../../manuscript/notes/response_preconditioned_hybrid/STATUS.md) |
| Propagate--settle framework | Construct a different legal cyclic coupling or bounded-degree settlement gadget with seed chronology proved before reporter analysis. | [`propagate_settle_framework/STATUS.md`](../../manuscript/notes/propagate_settle_framework/STATUS.md) |
| Local-solver oracle hierarchy | Define and justify a same-task lower-bound model that defeats residual-slack spreading and sparse-basis delayed synthesis, or narrow the claimed class. | [`local_solver_oracle_hierarchy/STATUS.md`](../../manuscript/notes/local_solver_oracle_hierarchy/STATUS.md) |

The full registry currently tracks 27 notes across iterative, mixed,
response, model, and synthesis tracks. A new idea should first be checked
against the registry and shared result ledger so it does not recreate a
settled failure under a new name.

## What is not established

Do not state any of the following without a new accepted proof:

- a graph-uniform end-to-end accelerated local PPR solver;
- the early-AESP locality lemma required by the promotion gate;
- a graph-uniform actual-finite accelerated net exponent for the current
  safeguarded AESP-CD recurrence;
- an output-sensitive dynamic high-rank response backend for arbitrary
  changing cores;
- a matching general lower bound for every local solver under adjacency-list
  access;
- a finite-precision or bit-complexity version of the current exact-real
  contracts;
- a universal identification of APPR, PPR, RPPR, objective, KKT, and
  proximal-residual accuracy parameters.

## How a new agent should select work

1. Check the controller broadcast. Its current active dispatch is `none`, so
   do not open a research round automatically.
2. Ask the controller to assign exactly one direction, role, branch, and
   disjoint write scope.
3. Read that direction's full `STATUS.md` and its exact “Resume here” and
   stop/go tests.
4. Reuse proved dependencies only with their graph, seed, parameter,
   accuracy, access, and evidence qualifiers.
5. If a route fails, record the smallest exact stopped claim. Do not convert
   it into a broader lower bound.
6. If a route succeeds, verify every item in the acceptance checklist in
   [`problem-definition.md`](problem-definition.md) before proposing
   manuscript promotion.
