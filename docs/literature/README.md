# Literature Map

This directory is the curated entry point to the project's source literature.
PDFs are evidence; these notes explain why each source matters and where its
relevant material appears.

## Topic map

| Topic | Notes | Current focus |
| --- | --- | --- |
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
- local PDF path, when redistribution is permitted;
- why the paper matters to this project;
- relevant theorem, algorithm, or experiment;
- exact page, theorem, equation, or section pointers;
- differences from this project's formulation;
- unresolved questions or possible failure modes.

Do not summarize a theorem from memory. Check the source and make clear when a
statement is an inference rather than a claim made by the paper.

## Intake workflow

1. Confirm that the PDF may legally be redistributed through this repository.
2. Install and initialize Git LFS in the clone.
3. Save the PDF under `papers/<topic>/` using
   `<year>-<first-author>-<short-title>.pdf`.
4. Add a source-grounded annotation to the relevant topic file.
5. Add or correct the BibTeX entry in `paper/references.bib`.
6. Commit the LFS pointer, annotation, and bibliography update together.

If redistribution is not permitted, do not commit the PDF. Record a canonical
link and citation instead; a private local copy may be kept outside the
repository.

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
