# Manuscript workspace

This directory separates the active hybrid-local-solver paper from complete
archives of earlier papers.

## Active manuscript

The files at the root of `manuscript/` form the active paper:

```text
manuscript/
├── main.tex
├── appendix.tex
├── references.bib
├── sections/
├── tex/
│   └── shared/
│       ├── preamble.tex
│       ├── math_commands.tex
│       └── writing_commands.tex
└── jmlr2e.sty
```

`main.tex` contains document structure only. Shared package configuration and
notation live under `tex/shared/`. The active command set preserves the
author's recurring NeurIPS 2024 and 2025 writing conventions without importing
archived scientific claims or the unrelated machine-learning boilerplate in
those older command files:

- `math_commands.tex` defines the canonical `\v...` vector, `\m...` matrix,
  `\g...` calligraphic, and `\s...` blackboard-bold families, together with
  common graph operators and helpers such as `\mc`, `\eps`, and `\grad`;
- `writing_commands.tex` contains figure-panel labels, reference wrappers,
  drafting colors, checkmarks, and pseudocode assignment symbols;
- `preamble.tex` owns package loading and theorem-environment setup.

Add reusable notation to these shared files rather than defining commands
inside individual sections. Archived macro files remain read-only references
and are never input by the active manuscript.

Build the active paper from the repository root with:

```bash
make paper
```

Project-wide mathematical definitions and research decisions belong in
`docs/`. Keep the active manuscript consistent with those documents, the
implementation, and the tests.

## Archived manuscripts

Complete previous-paper projects live under `manuscript/archive/`:

- [`archive/kdd-2023-appr-sor/`](archive/kdd-2023-appr-sor/) contains the
  standalone KDD 2023 APPR-SOR paper.
- [`archive/neurips-2024-locch/`](archive/neurips-2024-locch/) contains the
  standalone NeurIPS 2024 LocCH paper and reviewer response.
- [`archive/neurips-2025-aesp/`](archive/neurips-2025-aesp/) contains the
  standalone NeurIPS 2025 AESP paper and author response.

Archived projects are historical, read-only references. They are not included
in the root `make paper` or `make reproduce` targets. Before inspecting,
building, or explicitly changing an archive, read its own `README.md` and
`AGENTS.md`; preserve its internal structure and use its documented build
commands.

Do not automatically copy archived prose, claims, bibliography entries,
macros, or experimental results into the active manuscript. Verify any reused
material against the current project documentation and cited sources.
