# Local paper library

Source papers support the curated notes in `docs/literature/`. The public repository provides citations, links, version metadata, checksums, and page pointers; it does not redistribute the downloaded paper PDFs.

Obtain a paper from its publisher or arXiv record in `../docs/literature/index.md` or `../manuscript/references.bib`, then save a local copy directly in this directory using the filename recorded in the literature note. `papers/*` is ignored except for this README. Historical PDF paths are provenance pointers, not promises that the PDF is included in this public checkout. Exact-version checksums can be found in the corresponding source manifests where available.

Do not use `git lfs pull` to retrieve the private library: the replacement repository contains no source-paper LFS objects. Do not force-add downloaded PDFs. A future redistribution needs an explicit license/permission review and a documented change to this policy.

Use names such as `2024-neurips-author-short-title.pdf`. Keep literature metadata and source-page pointers synchronized if a source version changes. Public links and bibliographic information, rather than an imported archive, should be the default way to share a source with readers.
