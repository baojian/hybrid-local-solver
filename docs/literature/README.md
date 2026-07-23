# Literature Map

This directory is the curated entry point to the project's source literature.
PDFs are evidence; these notes explain why each source matters and where its
relevant material appears.

The [`index.md`](index.md) catalog organizes the current paper library by
research area. Paper titles are the primary labels; year, venue, and BibTeX key
provide stable lookup metadata.

## Topic map

| Topic | Notes | Current focus |
| --- | --- | --- |
| Paper catalog | [`index.md`](index.md) | Research areas, reading paths, and library status |
| Local solvers | [`local-solvers.md`](local-solvers.md) | APPR, evolving sets, AESP, LocGD, LocCH, LocSOR |
| Acceleration | [`acceleration.md`](acceleration.md) | Catalyst and accelerated/local interactions |
| Graph optimization | [`graph-optimization.md`](graph-optimization.md) | Local PageRank formulation, locality, and work models |

The candidate methods above come from the current project scope. Their exact
citations and technical relationships remain to be verified from source
papers.

## Required annotation for each paper

Add an entry to the relevant topic file with:

- full citation and BibTeX key;
- DOI, arXiv identifier, or canonical URL;
- local PDF path;
- why the paper matters to this project;
- relevant theorem, algorithm, or experiment;
- exact page, theorem, equation, or section pointers;
- differences from this project's formulation;
- unresolved questions or possible failure modes.

Do not summarize a theorem from memory. Check the source and make clear when a
statement is an inference rather than a claim made by the paper.

## Intake workflow

1. Install and initialize Git LFS in the clone.
2. Save the PDF directly under `papers/` using
   `<year>-<venue>-<first-author>-<short-title>.pdf`; do not create subfolders.
3. Add the paper to [`index.md`](index.md).
4. Add a source-grounded annotation to the relevant topic file.
5. Add or correct the BibTeX entry in `manuscript/references.bib`.
6. Commit the LFS pointer, catalog entry, annotation, and bibliography update
   together.

## Annotation template

```md
## Citation key: `authorYYYYshort`

- Citation:
- DOI/arXiv/URL:
- Local PDF:
- Relevance:
- Exact pointers:
- Formulation differences:
- Open questions:
```
