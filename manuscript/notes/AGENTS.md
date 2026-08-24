# Research-note agent instructions

These instructions refine the repository-root `AGENTS.md` for work under
`manuscript/notes/`. The root scientific conventions and required checks still
apply.

## Read before working

Every direction agent reads, in order:

1. [`_shared/problem_definition/README.md`](_shared/problem_definition/README.md);
2. [`_shared/related_work/README.md`](_shared/related_work/README.md);
3. [`_shared/results/README.md`](_shared/results/README.md);
4. [`_shared/coordination/BROADCAST.md`](_shared/coordination/BROADCAST.md);
5. the target direction's `README.md`, `STATUS.md`, registry entry, and relevant
   parts of `main.tex`;
6. the required project context and literature files named by the root
   `AGENTS.md`.

Reading the shared summaries does not replace checking a theorem in its source
paper or proof file.

## Ownership and concurrent work

- A **direction agent** owns one named note directory for one task. It may edit
  that directory only unless the controller explicitly expands the scope.
- The **controller agent** owns `_shared/`, the root note index, the registry,
  and cross-direction synchronization.
- Do not rename, merge, split, or delete a direction while other work is
  present. Propose such changes to the controller instead.
- Inspect the working tree before editing. Preserve unrelated or concurrent
  changes and never replace a dirty file with a regenerated copy.
- Cross-reference another direction; do not copy its proof into the local
  note. A dependency is not a proved local lemma until its exact assumptions
  have been checked.
- Treat `registry.toml`'s `depends_on` array as the **formal proof/import
  graph**: add an edge only when the consuming direction invokes a result from
  the provider as part of a claim or construction.  Empirical ancestry,
  motivating siblings, comparison baselines, and companion notes belong in
  `STATUS.md` under a separate **Context/provenance** label; they are not
  missing registry edges and must not be added when doing so would merely
  encode narrative history or create a provenance cycle.

## Independent-direction contract

Each direction must remain resumable without reading chat history. Its
`README.md` explains the mathematical idea and build command. Its `STATUS.md`
is the operational handoff and must state:

- the exact question, model, accuracy namespace, and charged work;
- source, proved, conditional, measured, open, and refuted claims separately;
- the central blocker and the next falsifiable target;
- formal registry dependencies, context/provenance, and reusable outputs;
- where a new agent should resume and which checks were last run.

`STATUS.md` is a navigation aid, not proof authority. `main.tex` and cited
sources remain authoritative for mathematical statements. Resume pointers use
stable LaTeX labels, section names, test names, or source anchors whenever
possible; a bare line range is too fragile under concurrent edits.

## Update and broadcast loop

At the end of a direction task:

1. reconcile the note with project notation and claim labels;
2. update that direction's `STATUS.md`;
3. send the controller a compact handoff using
   [`_shared/coordination/STATUS_TEMPLATE.md`](_shared/coordination/STATUS_TEMPLATE.md);
4. identify any result that should enter the cumulative ledger, any refuted
   route that other agents must stop using, and any new dependency;
5. run the focused note build and the inventory audit.

The controller verifies handoffs, updates the shared results and literature
maps, refreshes `BROADCAST.md`, and redistributes only source-backed or
proof-backed conclusions. Unverified ideas stay attached to their direction.

## Claim and work discipline

Use the repository vocabulary exactly: **Source**, **Proved here**,
**Conditional**, **Measured**, **Open**, and **Refuted**. Every complexity
statement names its graph/access model, accuracy namespace, support evolution,
inverse primitive, preprocessing, and all charged operations. Never turn an
algorithm-specific obstruction into a universal lower bound.

Generated PDFs and LaTeX auxiliaries are not research state and must not be
used as the only record of a result.
