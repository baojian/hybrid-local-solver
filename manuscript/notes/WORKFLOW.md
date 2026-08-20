# Research-note workflow

This directory is a theorem and experiment ledger, not a collection of drafts
with interchangeable claims. A new note should isolate a materially distinct
algorithm, oracle model, lower-bound family, proof mechanism, or experimental
question. Extend an existing note when the new result shares its mathematical
object and central proof obligation.

## Claim discipline

Every major statement should be visibly one of:

- **Source:** a result attributed to a cited paper, with assumptions preserved.
- **Proved here:** a complete argument under the note's stated model and work
  accounting.
- **Conditional:** a composition whose hypotheses include every unresolved
  data-structure or continuation obligation.
- **Measured:** a reproducible observation, never promoted to a theorem.
- **Open:** a named target with a falsifiable interface or bound.
- **Refuted:** a former conjecture accompanied by its counterexample or failed
  proof step.

Algorithm-specific lower bounds must name the algorithm. Oracle lower bounds
must define the oracle's access, allowed computation, persistent state, output
representation, and charged work. Adjacency access by itself is an input model,
not a first-order restriction.

## Adding or changing a note

1. Read `docs/research-context.md`, `docs/mathematical-conventions.md`, and the
   relevant literature summary before changing a theorem statement.
2. Use `tex/shared/research_note_preamble.tex` and
   `tex/shared/source_aligned_problem.tex`; do not create a private PageRank
   normalization or redefine reserved notation.
3. Give the note its own directory containing `main.tex`, `README.md`, and a
   `Makefile` that includes `../note.mk`.
4. Register the note in `manifest.toml`, `taxonomy.toml`, this directory's
   `README.md`, and `Makefile`. The taxonomy entry must state its primitive,
   support evolution, evidence level, dependencies, and next target.
5. Add focused automated tests for executable tools or implementations. Keep
   experiment orchestration in `experiments/` and reusable logic in `src/`.
6. Run the inventory audit, tests, lint, and the changed note build.

```bash
make note-audit
make note-targets
make test
make lint
make -C manuscript/notes/<note-id>
```

## Before promoting a bound

Check that the work ledger charges adjacency discovery, old-face reads,
restricted solves, factor or response updates, boundary reports, rekeys,
materialization, certificate verification, and output writes. State whether
active sets are fixed, nested, or nonnested and whether the inverse is realized
by iteration, persistent response, or a mixture.

For the current response--iterative program, a graph-uniform near-output-linear
claim still requires both a charged finite-band response reporter on general
cyclic cores and safe accelerated continuation on an expanding subspace.
