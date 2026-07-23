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
└── jmlr2e.sty
```

Build the active paper from the repository root with:

```bash
make paper
```

Project-wide mathematical definitions and research decisions belong in
`docs/`. Keep the active manuscript consistent with those documents, the
implementation, and the tests.

## Archived manuscripts

Complete previous-paper projects live under `manuscript/archive/`:

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
