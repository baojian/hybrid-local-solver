# Current research status and open problems

Verified snapshot: 2026-08-29.

This file is a routing summary. The current
[controller broadcast](../../manuscript/notes/_shared/coordination/BROADCAST.md),
the [`registry.toml`](../../manuscript/notes/registry.toml), and each
direction's `STATUS.md` are authoritative for live research state. The cited
proof in the owning note is authoritative for a mathematical claim.

## Bottom line

The desired graph-uniform canonical point-source PPR solver with fully charged

```text
O_tilde(1 / (sqrt(alpha) * eps_ppr))
```

work is not proved. The project has useful local convergence results,
support and volume controls, exact structured handoffs, response identities,
finite-trace counterexamples, and algorithm-specific lower bounds. The
missing step is a graph-uniform composition that preserves accelerated
progress while paying for every local and response operation.

The shared problem remains defined for a sparse source distribution, but this
is now a deliberately broader extension.  Linear point-source superposition
gives the factor `(sum_v sqrt(s_v))^2`, and RPPR active supports do not
superpose.  Claims must therefore be tagged `point-seed` or `general-seed`.
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
- The RPPR minimizer is nonnegative and has support volume at most `1 / rho`.
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

The latest accepted AESP-CD boundary is Round 027. The actual finite-inner
recurrence now has a lagged Euclidean reserve, but its graph-uniform drift is
only order `q^2`. The simplest lagged unsplit `q^(-1) Q` reserve cannot both
contract uniformly in one step at the accelerated rate and carry enough
coefficient for the reachable K8 pulse. This does not rule out accelerated
decay over windows or with a different decomposition.

The live AESP route is therefore a windowed, spectrally split, nonlinear, or
differently normalized low-Dirichlet transfer that retains every finite
residual and correction. Round 027 does not provide a graph-uniform net
exponent, end-to-end solver theorem, complete work vector, or
finite-precision result.

## Active open directions

All directions below are currently `proved-open`: they contain proved scoped
results and a central unresolved target.

| Direction | Exact unresolved target | Resume source |
| --- | --- | --- |
| AESP coordinate descent for RPPR | Prove a finite windowed, spectral, nonlinear, or differently normalized low-Dirichlet net exponent that retains all residual and correction charges. | [`aesp_cd_l1_rppr/STATUS.md`](../../manuscript/notes/aesp_cd_l1_rppr/STATUS.md) |
| AESP--LOCSOR hybrid | Build a nonadditive or logarithmic reset ledger across multiple actual nonsettled admissions, or prove another graph-independent prefix bound. | [`hybrid_aesp_locsor/STATUS.md`](../../manuscript/notes/hybrid_aesp_locsor/STATUS.md) |
| Volume-gated acceleration | Establish all-history causal solvency under a declared structural condition, or exhibit debt that survives enough admissions to stop that route. | [`volume_gated_acceleration/STATUS.md`](../../manuscript/notes/volume_gated_acceleration/STATUS.md) |
| Response-preconditioned hybrid | Find sparse collision-sensitive refresh state or a geometrically paid replay/rebuild theorem for changing high-rank cores. | [`response_preconditioned_hybrid/STATUS.md`](../../manuscript/notes/response_preconditioned_hybrid/STATUS.md) |
| Propagate--settle framework | Construct a different legal cyclic coupling or bounded-degree settlement gadget with seed chronology proved before reporter analysis. | [`propagate_settle_framework/STATUS.md`](../../manuscript/notes/propagate_settle_framework/STATUS.md) |
| Local-solver oracle hierarchy | Define and justify a same-task lower-bound model that defeats residual-slack spreading and sparse-basis delayed synthesis, or narrow the claimed class. | [`local_solver_oracle_hierarchy/STATUS.md`](../../manuscript/notes/local_solver_oracle_hierarchy/STATUS.md) |

The full registry currently tracks 18 notes across iterative, mixed,
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
