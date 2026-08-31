# Research graph working strategy

**Status and scope**

This document defines the intended research-working strategy for standalone
notes under `manuscript/notes/`. It specifies how research questions split,
how agents work on them, how proofs and counterexamples are reviewed, and how
results propagate toward the root objective.

This is not the migration plan for the 27 existing notes. Parent assignments,
note dispositions, compatibility judgments, renames, merges, and new skeleton
nodes belong in a separate migration document after the revised problem
definition and this strategy are accepted.

**Existing repository mechanisms**

The strategy extends the existing system rather than replacing it:

- [`registry.toml`](registry.toml) remains the machine-readable note inventory.
- Its existing `depends_on` field remains the formal proof/import graph.
- Each note's status handoff remains the current claim ledger and resume point.
- [`_shared/coordination/rounds/`](_shared/coordination/rounds/) remains the
  sole durable history of controller-managed agent attempts.
- [`active_assignments.toml`](../../docs/coordination/active_assignments.toml)
  remains a temporary write-ownership ledger for genuinely concurrent work.
- [`_shared/results/README.md`](_shared/results/README.md) and
  [`_shared/coordination/BROADCAST.md`](_shared/coordination/BROADCAST.md)
  remain controller-maintained shared summaries.
- Reproducible proof-audit programs remain under `experiments/proof_audits/`.

The strategy does not introduce a second registry, per-note chat archive, or
duplicate attempt-history directory.

**Root and graph semantics**

`problem_definitions` is the unique root. It is a versioned scientific
contract, not a speculative direction. It defines the input, output, accuracy
namespace, computational model, and acceptance criteria against which every
research node is interpreted.

The intended first child is an end-to-end research question. Its exact name
and statement will be fixed after the revised problem definition is accepted.
It should permit both a constructive resolution and a mathematically valid
impossibility or lower-bound resolution when both are scientifically relevant.

The graph is logical rather than filesystem-nested. Note directories remain
flat, because a result may have several consumers even though it has only one
primary exploration parent.

Every ordinary research-direction node has one primary `parent`. The primary
edge records why the node was opened and gives an agent a unique path back to
the root. It does not replace `depends_on`, which records exact theorem or
construction imports.

Each primary edge has one of three roles:

- `required`: the child is a declared obligation in the parent's current
  formulation. Refuting it flags the parent for reformulation; it does not
  automatically refute or close the parent.
- `alternative`: the child is one competing route. Refuting it closes only
  that route while siblings remain available.
- `probe`: the child is an audit, lower-bound test, counterexample search,
  structured-family study, or experiment that informs the parent's blocker
  without satisfying or refuting the parent automatically.

The registry should eventually carry the minimal fields

```toml
parent = "<note-id>"
parent_role = "<required | alternative | probe>"
direction = "<strategic state>"
built_against = "<problem-contract version>"
```

The root omits `parent` and `parent_role`. Existing `depends_on` entries remain
unchanged unless a separate proof-import audit justifies a change.

The first implementation need not encode several independent OR groups below
one parent. If a real decomposition later requires `(A or B) and (C or D)`, an
optional grouping field may be introduced then. Schema complexity should be
driven by an actual mathematical need.

**Node identity and authority**

A node represents a stable, falsifiable mathematical question, claim,
construction, algorithmic route, or diagnostic probe. A node is not an agent
session and is not defined by its current status.

Each node must state:

- its exact question and intended contribution to its parent;
- its graph, access, seed, accuracy, and charged-work contract;
- the result that would count as success;
- the observation or counterexample that would falsify the route;
- its formal `depends_on` imports;
- its proved, conditional, measured, open, and refuted claims;
- its central blocker and next concrete action;
- stable pointers to proofs, counterexamples, source evidence, and checks.

The note's `main.tex` and cited sources remain mathematical authority. The
status handoff is a concise operational view. Round records index attempts and
adjudications but never replace proofs or counterexamples.

Full chat transcripts are not repository proof state. Agent work is preserved
through concise round handoffs, mathematical edits, failed-route explanations,
and reproducible evidence.

**Three independent status dimensions**

Mathematical evidence, strategic value, and temporary assignment state remain
separate.

The existing evidence vocabulary is retained:

```text
source | proved-open | conditional | measured | synthesis | refuted
```

It summarizes the mathematical evidence profile without claiming independent
verification of every local proof.

The proposed strategic `direction` vocabulary is:

- `live`: the node can still advance its parent and has a viable next target.
- `blocked`: a named unresolved lemma, interface, or counterexample search
  prevents progress, but the route is not known to be false or useless.
- `parked`: the route remains meaningful but is not worth current resources.
- `closed`: the node's local question is answered and no further work is
  planned there; its output may remain reusable.
- `dead-end`: even a correct surviving result cannot advance the parent. The
  note must explain why and identify the supporting proof or counterexample.
- `superseded`: another node replaces this formulation; `superseded_by` names
  the replacement.
- `promoted`: verified outputs have been imported into a parent, shared result,
  or manuscript claim, with an exact destination pointer.

`refuted` and `dead-end` are not synonyms. The first is mathematical; the
second is strategic. An unsuccessful session establishes neither.

Temporary concurrent assignment state remains

```text
active | ready_for_review
```

An idle node normally has no assignment record. Sequential single-agent work
may remain on the current branch; simultaneous writers use isolated worktrees
and disjoint scopes.

**Independent verification gate**

A statement labeled **Proved here** is a proof draft until an independent
review accepts that exact claim. Compilation, tests, numerical agreement, a
`ready_for_review` assignment, or a review-ready round do not by themselves
constitute mathematical verification.

Verification records identify claim labels rather than implicitly covering an
entire note:

```text
Verified claims: `lem:example`, `thm:example`
Verified by: <different agent family/model or human reviewer>
Verification round: <NNN>
Verification result: <accepted | rejected | partial>
```

The reviewer checks the displayed assumptions, proof steps, imported results,
problem-contract compatibility, and the consequence claimed by the parent.
A claim cannot be promoted or imported as unconditional merely because its
author marked it **Proved here**.

Historical verification may be backfilled only when an existing round names
the exact reviewed claim, independent reviewer, evidence checked, and result.
Ambiguous historical checks remain unverified until the claim becomes a live
dependency or critical-path input.

No model or agent session certifies its own mathematical result. For a
high-value claim, an author and an adversarial reviewer should come from
different model families when possible. A third reviewer resolves material
disagreement.

**Problem-contract versioning**

The root declares a `contract_version`. Every ordinary node declares
`built_against`.

`built_against` means that the named problem contract is the node's declared
formulation baseline. It does not mean every theorem has already received an
independent compatibility review.

When the root changes:

- a notation-only change may be handled by an explicit, stable `mapping`
  pointer in the node's status handoff;
- a change to the graph, access model, seed model, accuracy namespace,
  residual certificate, output contract, or charged work requires a real
  compatibility audit;
- a node remains stale until that audit or mapping is recorded;
- old proofs are never silently reinterpreted under the new contract.

Version names, mappings, and compatibility results must be source-controlled
and human-readable. A Git commit may support provenance, but it does not
replace the semantic contract version.

**Candidate children and split admission**

A possible branch first enters the parent's **Candidate children queue** in
its status handoff. It becomes a registered node only when it has:

1. one exact, falsifiable question or claim;
2. a clear consequence for the parent;
3. a success criterion;
4. a falsification or stop criterion;
5. nonduplicative scope relative to existing nodes; and
6. a bounded context package and a concrete first task.

By default, admit at most three alternative children in one split. More
alternatives require a written controller justification. A mathematically
natural set of required obligations may exceed three when necessary.

Agents may propose children but do not register them unilaterally. The
controller checks duplication, graph placement, context cost, and expected
information value before admission.

**Agent work cycle**

One writing session leases one node, not an entire path. Its context package
contains only what the task needs:

- the current root contract;
- concise summaries along the primary-parent path;
- exact `depends_on` providers being imported;
- the node's status handoff and relevant proof sections;
- necessary project conventions and source literature; and
- the assigned success and falsification tests.

At the end of a session, the agent returns exactly one primary exit type:

```text
proof | counterexample | conditional | weaker-target |
split-proposal | blocker | no-change
```

The direction handoff records the exact changed claims, stable evidence
pointers, failed arguments worth preserving, implications for the parent, and
the next action. A blocker names the missing statement and attempted routes;
it is not a declaration of a dead end.

Each direction entry in a controller round should record:

```text
Agent family/model: <family/model>
Exit type: <exit type>
Nodes touched: `<note-id>`, ...
```

These fields make model performance and per-node attempt history recoverable
from the existing round records without introducing another history system.

Only the controller edits shared topology, shared summaries, or cross-note
promotion records during parallel work. Direction agents make node-local
changes and propose graph updates in their handoffs.

**Using heterogeneous model families**

Model roles should be assigned from observed repository performance rather
than permanent assumptions about Fable, Opus, or GPT-5.6-sol.

At important branch points, several model families may independently propose
decompositions or falsification routes. The controller admits a small set of
nonduplicative children. One model develops a node, a different model attacks
its proof or searches for counterexamples, and a third is used only for
high-value disagreement or final adjudication.

Round records should support a lightweight performance history based on:

- accepted proof rate and later correction rate;
- useful counterexamples and narrowed claims;
- quality of split proposals;
- verification accuracy;
- progress per context and compute budget; and
- ability to produce resumable handoffs.

The objective is verified information gain, not generated prose, note count,
or the number of sessions marked successful.

**Propagation and controller adjudication**

Graph consequences are flagged for review rather than applied automatically:

- a refuted `required` child flags its parent as needing reformulation;
- a refuted `alternative` child closes only that route;
- a `probe` updates the parent's blocker, evidence, or candidate queue without
  satisfying the parent automatically;
- an unverified imported proof keeps the consuming claim conditional;
- a verified result is promoted only after checking assumptions and contract
  compatibility at the consuming node;
- a weaker replacement is recorded in the claim ledger before the old route
  is closed or superseded.

The controller decides whether to weaken a formulation, admit new children,
park a direction, mark a dead end, or promote a verified output. Mathematical
research is not closed through automatic status propagation.

**Terminal-state evidence**

Terminal strategic states require durable evidence:

- `closed` identifies the answered local question and reusable output;
- `dead-end` explains why the result cannot advance its parent even if true;
- `superseded` names `superseded_by` and maps any retained results;
- `promoted` names the verified claims and exact consuming destination;
- a mathematical `refuted` state points to an analytic counterexample,
  impossibility proof, or registered reproducible proof audit.

Failed proof attempts are preserved when they identify a false step, missing
assumption, counterexample family, or useful weaker target. Repetition without
new evidence is summarized rather than accumulated as transcript history.

**Scheduling and progress**

The active frontier should favor nodes that are central to the root question,
falsifiable, likely to remove uncertainty, and affordable to investigate.
Alternative high-risk routes and adversarial probes remain in the portfolio,
but uncontrolled branching is avoided.

Priority judgments should consider:

- consequence for the root objective;
- dependency centrality;
- probability of obtaining a decisive proof or counterexample;
- expected information gain even on failure;
- verification and context cost; and
- availability of independent reviewers.

Progress is measured by verified claims, resolved dependencies, informative
counterexamples, correctly closed routes, and narrowed blockers. It is not
measured by the number or length of notes.

**Graph and audit invariants**

The eventual registry and template audit should enforce at least:

- exactly one root contract;
- one valid primary parent for every ordinary non-root direction;
- reachability from the root;
- no cycle in primary-parent ancestry;
- valid parent roles, strategic states, and contract versions;
- continued acyclicity and exact semantics of `depends_on`;
- evidence pointers for `dead-end`, `refuted`, `superseded`, and `promoted`;
- claim-level independent-review metadata before promotion; and
- a valid compatibility record for nodes used across contract versions.

During migration, strict graph checks begin only after a complete proposed map
has been reviewed. Partial migration must not force agents to invent parent
edges or strategic states merely to satisfy an audit.

**Separation from the migration plan**

The later migration document should contain:

- the v1 snapshot and revised-contract transition;
- the proposed top-level skeleton;
- a 27-row note triage table;
- proposed parent, role, direction, compatibility, and confidence per note;
- explicit human decisions for ambiguous edges;
- historical-verification evidence that is safe to backfill;
- staged audit and renderer changes; and
- validation and rollback criteria.

The migration must not rename, merge, split, delete, or edit mathematical note
bodies merely to make the graph look tidy. Scientific judgments are reviewed
before topology is written.

**Decisions required before migration**

The following choices remain deliberately open until the revised problem
definition is fixed:

1. the exact statement and identifier of the root's first research-question
   child;
2. the contract-version naming scheme;
3. whether a valid independent reviewer must be a different agent family, a
   different underlying model, or a human reviewer;
4. whether the two synthesis notes participate in primary-parent propagation
   or remain controller views outside it; and
5. whether any real parent requires more than one group of alternative
   children in the first schema version.

Recommended defaults are `end_to_end_question`, semantic versions such as
`problem-v1`, a reviewer from a different underlying model family or a human,
synthesis notes as nonpropagating controller views, and no alternative-group
field until a concrete decomposition requires it.
