# New-agent research brief

Last reconciled: 2026-08-29.

This is a numerical optimization repository. It studies local algorithms for
personalized PageRank (PPR) and closely related regularized graph
optimization problems. The main research objective is to determine whether
acceleration, sparse local exploration, and persistent restricted-system
response can be combined in one fully charged algorithm.

The desired graph-uniform end-to-end complexity is open. The repository has
proved components, conditional theorems, exact counterexamples, and measured
evidence, but it does not currently contain a theorem establishing the full
target.

## Read this package in order

1. Read [`problem-definition.md`](problem-definition.md) for the exact input,
   PPR operator, output requirement, certificate, accuracy namespaces, work
   model, and RPPR surrogate.
2. Read [`research-status.md`](research-status.md) for what is established,
   what remains open, the central promotion gate, and the current direction
   owners.
3. Read [`contribution-workflow.md`](contribution-workflow.md) before choosing
   or accepting an assignment.
4. Read the [`root agent instructions`](../../AGENTS.md), then the `STATUS.md`
   file for the one research direction named by the assignment.

Do not begin with historical round files. They preserve provenance, but the
current controller broadcast and direction status files already incorporate
accepted corrections.

## The project in one paragraph

Given adjacency-list access to a finite simple connected graph with unit edge
weights and at least two vertices, one seed vertex `v` (`s=e_v`), a PageRank
parameter `alpha`, and a target degree-normalized error `eps_ppr`, return a
sparse PPR approximation and a valid terminal certificate.
Every graph read, repeated local operation, response update, state access,
validation step, materialized value, and output write must be charged. The
aspirational work bound is
`O_tilde(1 / (sqrt(alpha) * eps_ppr))`. The central difficulty is
that global acceleration can lose locality, while strictly local iterations
can lose the accelerated dependence on `alpha`.

## Working vocabulary and candidate architecture

| Term | Role in this project |
| --- | --- |
| PPR | Personalized PageRank, the primary semantic output problem. |
| APPR | A classical approximate PPR push method and local-work baseline. |
| RPPR | An L1-regularized PPR optimization surrogate used to obtain sparse, support-safe active cores. |
| Catalyst | An outer acceleration framework for convex optimization. |
| AESP | Accelerated Evolving Set Process, the principal source model for accelerated local graph exploration. |
| LocSOR | Localized successive over-relaxation, used for momentum-free local refinement. |
| Persistent response | Reusable factor, Schur, harmonic, or related state for answering repeated restricted-system changes without rebuilding every prefix. |
| Gate | A proved admission, stopping, or support-safety test based only on information the algorithm has paid to obtain. |

The candidate hybrid has four conceptual jobs: discover a sparse active
region, make accelerated progress on that region, preserve or hand off useful
restricted-system state as the region changes, and return one certified sparse
answer. Existing directions explore different orderings and interfaces among
these jobs. This is an architecture hypothesis, not a fixed algorithm or a
proved optimal design. The current family map is
[`docs/solver-family-roadmap.md`](../solver-family-roadmap.md).

## Authority map

These files have different roles and must not be silently merged into a new
convention:

| Question | Authoritative file |
| --- | --- |
| Repository scope and working rules | [`AGENTS.md`](../../AGENTS.md) |
| Project-wide notation | [`docs/mathematical-conventions.md`](../mathematical-conventions.md) |
| Canonical graph class | [`docs/decisions/graph-convention.md`](../decisions/graph-convention.md) |
| Canonical seed input | [`docs/decisions/seed-convention.md`](../decisions/seed-convention.md) |
| Repository-wide residual decision | [`docs/decisions/residual-convention.md`](../decisions/residual-convention.md) |
| Controller-level exact comparison contract | [shared problem definition](../../manuscript/notes/_shared/problem_definition/README.md) |
| Current cross-direction boundary | [controller broadcast](../../manuscript/notes/_shared/coordination/BROADCAST.md) |
| Direction ownership and dependencies | [`manuscript/notes/registry.toml`](../../manuscript/notes/registry.toml) |
| Detailed claim status | Each direction's `STATUS.md` |
| Proof source | The cited theorem or proposition in the owning note |

The shared problem definition is a precise controller-level contract for
comparing research directions. It does not close the repository-wide choice
of implementation residual or stopping schedule. This package summarizes
that contract; if wording diverges, follow the authoritative file and repair
this package in the same change.

## Choose one contribution route

### Theory or algorithm design

Select one registered direction and its next falsifiable target. Read its
`README.md`, `STATUS.md`, main note, declared dependencies, relevant
literature note, and only the source papers needed for a theorem check. Keep
new proved statements, conditional claims, experiments, conjectures, and
refuted paths explicitly separated.

### Implementation or experiments

Obtain a provider identity and an owned directory before writing solver code.
Use the shared solver contract for comparisons. Record graph, `alpha`, target
accuracy, random seed, stopping rule, solver parameters, code version, and
work measurements for every experiment.

### Read-only review

Audit a named claim against its proof source, assumptions, evidence type,
and charged-work scope. Report exact section, equation, theorem, experiment,
or counterexample pointers. A review must not broaden a direction's stated
scope.

## Five non-negotiable facts

1. The graph-uniform target is open.
2. `eps_ppr`, `eps_appr`, objective error, proximal residuals, and RPPR
   regularization are different quantities unless a theorem explicitly
   converts them.
3. RPPR is a useful sparse-support surrogate, not automatically the final PPR
   answer.
4. A failure of one recurrence, state representation, graph family, or finite
   trace is not a lower bound for all local solvers.
5. A fast tail does not establish an end-to-end bound when exploration,
   burn-in, repeated reads, certification, memory, materialization, or output
   is uncharged.
