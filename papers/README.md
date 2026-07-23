# Shared Paper Library

This directory holds source papers that may legally be shared through the
project's GitHub repository. PDFs support the curated notes in
`docs/literature/`; they do not replace those notes.

## Can I add papers directly?

Yes. Copy a permitted PDF into a topic directory such as:

```text
papers/local-solvers/2024-author-short-title.pdf
papers/acceleration/2019-author-short-title.pdf
papers/graph-optimization/2020-author-short-title.pdf
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
git check-attr filter -- papers/local-solvers/example.pdf
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

- Organize papers by research topic.
- Use `<year>-<first-author>-<short-title>.pdf`.
- Prefer stable author manuscripts or official open-access versions.
- Do not store multiple unexplained versions of the same paper.
- Record the PDF path and exact page or section pointers in its annotation.
