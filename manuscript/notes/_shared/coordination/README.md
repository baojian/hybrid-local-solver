# Multi-agent coordination protocol

The notes workspace uses a controller/worker model that preserves independent
directions and makes cross-direction communication explicit.

## Roles

- The **controller** maintains the shared problem, literature map, accumulated
  results, broadcast, manifest, taxonomy, and dependency graph. It verifies
  before propagating.
- A **direction agent** works in exactly one note directory per assignment,
  keeps that note self-contained, and returns a structured handoff.
- A **review agent** may audit a direction without editing it. Its findings are
  proposals until reconciled with the proof and source material.
- `hybrid_local_solver_complete_note` is the proof-bearing consolidated
  theorem-attempt and archive. Its direction owner maintains derivations,
  counterexamples, and the historical proof record.
- `hybrid_local_solver_synthesis` is the integration- and controller-facing
  synthesis and gap map. It cross-references proof owners and must not duplicate
  or silently become authoritative for their proofs.

Roles are per task, not permanent identities.

## Coordination loop

```text
shared contract + broadcast
          -> direction assignment
          -> independent proof/experiment/audit
          -> local STATUS.md + controller handoff
          -> controller verification
          -> results/literature/taxonomy update
          -> new BROADCAST.md read by all directions
```

This is how updates are collected and redistributed without allowing one
worker to rewrite every other note.

Every parallel cycle also gets a durable record under [`rounds/`](rounds/),
created from [`ROUND_TEMPLATE.md`](ROUND_TEMPLATE.md). The live broadcast says
what all agents should know now; the round ledger records why the controller
accepted and routed each conclusion.

## Direction handoff

Every handoff uses [`STATUS_TEMPLATE.md`](STATUS_TEMPLATE.md) and includes:

- exact claim-status changes;
- proof, counterexample, source, code, or experiment pointers;
- which shared lemma is now reusable;
- which old route is refuted or narrowed;
- dependencies created or discharged;
- the single next falsifiable target;
- commands run and remaining verification gaps.

Only direct formal proof or construction imports change `taxonomy.toml`'s
dependency graph. Source prerequisites, empirical ancestry, sibling
comparisons, and companion-note provenance are still redistributed, but they
remain separately labeled and do not create graph edges.

The controller rejects a broadcast item that has no precise evidence pointer,
mixes accuracy namespaces, hides work, or overgeneralizes an algorithm-specific
result.

## Collision avoidance

- Direction agents do not edit `_shared/`, `manifest.toml`, `taxonomy.toml`, or
  the root note `README.md` unless assigned as controller.
- The controller does not rewrite a dirty direction file while its worker is
  active; it communicates a requested change instead.
- Each agent inspects current diffs immediately before applying a patch and
  again before handing off.
- Folder renames and mass rewrites are deferred until the working tree is
  quiet and all references can be updated atomically.

## Suggested research cadence

1. Controller selects a small set of independent, high-value targets from the
   taxonomy and broadcast.
2. Direction agents work in parallel and report even negative results.
3. Controller performs a claim and dependency audit.
4. Verified shared results and refutations are broadcast.
5. The next round may reuse an existing direction or open a materially new
   note; speculative variants do not multiply folders prematurely.

This cadence scales to more directions than can run simultaneously because
the persistent state is in the repository rather than in agent memory.
