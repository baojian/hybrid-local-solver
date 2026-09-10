# Title alignment correction — 10 September 2026

The first title line was displaced approximately 38 points (13.4 mm) to the left. The second title line was centered. The class defines `\titlebreak` as `\newline`, which adds unwanted right-side stretch in this centered title. Replacing that one break with `\\` in `main.tex` centers both lines while retaining the same wording and line division. The official class is unchanged.

The corrected first page was rendered and visually inspected. The two title lines now have glyph-bound centers at 306.157 and 306.201 points on a page centered at 306 points. Their vertical positions are unchanged.

Validation:

- The paper remains 48 pages, with six main sections, three appendices, 75 numbered equations, and 31 references.
- All paper text is unchanged. The decoded PDF drawing streams for pages 2–48 are byte-identical to the preceding release.
- All 298 named destinations and all link annotations are unchanged.
- The active build and freshly extracted source archive compile without undefined references/citations, overfull boxes, or outstanding rerun requests. The isolated build disables shell escape and produces identical extracted PDF text.
- The author details, plain PDF title metadata, submission abstract, and license choice are unchanged.

Current fingerprints:

- PDF: `5bdc837bedd323beedd674f5b0e28d5b39730bfd8dede83aa5ed4873730aa5db`.
- Source archive: `227b68679f8648f3c19165b6fb20bdf08ba133cfd697fcbd6195bf23ba2765db`.
- Extracted PDF text: `ad41d511d521b573b83404ca91e7ae9e8eadc6f1dc0df5637bc3e0909a70c7b4`.

The preceding release is preserved in the task's `publication-20260909/before-title-alignment-20260910/`. Detailed coordinate and build evidence is in `title-alignment-20260910/`. This is a layout-only correction; no mathematical claim or algorithm changed. No arXiv upload was attempted.
