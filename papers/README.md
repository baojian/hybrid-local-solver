# Shared Paper Library

This directory holds source papers that may legally be shared through the
project's GitHub repository. PDFs support the curated notes in
`docs/literature/`; they do not replace those notes.

## Can I add papers directly?

Yes. Copy each permitted PDF directly into `papers/`; do not create
subfolders. Use filenames such as:

```text
papers/2024-neurips-author-short-title.pdf
papers/2023-colt-author-short-title.pdf
papers/2026-arxiv-author-short-title.pdf
```

Then annotate it in `docs/literature/` and add its BibTeX entry to
`paper/references.bib`.

Use a local Git clone for PDF uploads. GitHub's browser upload does not provide
a reliable Git LFS workflow, and storing large PDFs as ordinary Git objects
permanently enlarges repository history.

## Git LFS setup

PDFs under `papers/` are tracked by rules in the repository's
`.gitattributes`. Each computer that adds or checks out PDFs should have Git
LFS installed and initialized:

```bash
git lfs install
git lfs pull
```

Before committing a new PDF, verify that it is LFS-managed:

```bash
git check-attr filter -- papers/example.pdf
git lfs ls-files
```

The first command should report `filter: lfs`. This machine did not have Git
LFS installed initially; Git LFS 3.7.1 has now been installed and initialized
for this repository.

## Redistribution policy

Commit only PDFs whose licenses or permissions allow redistribution, such as
appropriately licensed open-access or author-posted versions. A paper being
free to read does not necessarily mean it may be redistributed.

For a paper that cannot be committed:

- record its full citation and canonical URL in `docs/literature/`;
- keep any personal copy outside this repository;
- do not add the personal copy to Git history.

## Naming and organization

- Keep all PDFs directly under `papers/`; do not use subfolders.
- Use `<year>-<venue>-<first-author>-<short-title>.pdf`.
- Use lowercase conference or journal abbreviations for `<venue>`, such as
  `colt`, `icml`, `kdd`, `neurips`, or `tkde`.
- For a paper that has not been formally published, use `arxiv` as the venue:
  `<year>-arxiv-<first-author>-<short-title>.pdf`.
- When an arXiv preprint is formally published, rename its PDF with the formal
  venue and update its BibTeX entry in `paper/references.bib`.
- Prefer stable author manuscripts or official open-access versions.
- Do not store multiple unexplained versions of the same paper.
- Record the PDF path and exact page or section pointers in its annotation.
