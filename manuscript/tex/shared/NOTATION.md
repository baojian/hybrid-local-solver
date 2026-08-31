# Manuscript notation registry

The symbol tables now live in [`notation.tex`](notation.tex), which is the
single source of truth and is directly includable:

```latex
\input{tex/shared/notation}         % from manuscript/main.tex
\input{../../tex/shared/notation}   % from manuscript/notes/<name>/main.tex
```

`notation.tex` renders two tables — reserved scientific symbols (Tier 1) and
registered scoped notation (Tier 2/3) — and carries the layering and
maintenance rules as source comments. The scoped table is repository-internal;
declare `\newif\ifnotationscoped \notationscopedfalse` before the `\input` to
print only the reserved table.

This directory remains the only declaration point for reusable LaTeX notation
in the active paper and standalone research notes.

## Layers

1. `math_commands.tex` defines generic typography, delimiters, operators, and
   named tolerances.
2. `source_aligned_problem.tex` is the Tier 1 source-aligned PageRank and RPPR
   reference model imported by the active paper and every research-direction
   note. The controller-owned `notes/problem_definitions/main.tex` is the sole
   expanded-reference exception and must keep its shared equations and symbols
   synchronized with this file.
3. Algorithm-specific notation in Tier 2 is registered in `notation.tex` and
   introduced only in documents that use that algorithm. Proof-local indexed
   quantities form Tier 3: their scope must be stated where they first occur,
   but their base symbols may not collide with Tier 1 or Tier 2.
4. `research_commands.tex` defines algorithm names and claim-status labels;
   `research_note_preamble.tex` supplies the common standalone-note shell.

The archived arXiv macro files are evidence only and must never be imported by
the active paper or notes.

## Adding notation

Any new recurring symbol or LaTeX command is added to `notation.tex` and to the
appropriate shared `.tex` file before use; individual sections and note entry
points do not declare commands. Algorithm- or proof-scoped symbols may narrow
the registered definitions or introduce indexed local quantities only after
stating their scope, and must not reuse a reserved symbol for an incompatible
role.
