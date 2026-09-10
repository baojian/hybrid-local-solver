# COLT-style preprint conversion and verification

The active manuscript now uses the official JMLR/PMLR class in a COLT-style preprint layout: 47 pages, 31 cited references, and 27 files in the source archive. The mathematical scope remains the established PPR/RPPR results.

## Appearance and author block

The reference is [arXiv:2303.12875](https://arxiv.org/pdf/2303.12875). Its source uses a modified COLT2023 class, 11-point Times text, and NewTX mathematics. This conversion uses the official unmodified JMLR class v1.30 with explicit `pmlr,11pt,twoside`, US Letter paper, a 6-inch text width, and an 8.5-inch text height. The local `jmlr.cls` and `jmlrutils.sty` are included in the source archive with their original license notices.

- Times-style text and NewTX math; single-column COLT page geometry.
- Centered two-line title; native COLT author, email, and italic affiliation layout.
- Author: Baojian Zhou. Affiliation: School of Data Science, Fudan University, Shanghai, China. Email: bjzhou@fudan.edu.cn. These details were supplied by the author in this task.
- Alternating author/title running headers, centered page numbers, globally numbered statements, and bold proof headings.
- A plain first page suppresses proceedings, editor, acceptance, and conference copyright information. No conference publication is claimed.
- The native PMLR author-year `plainnat` bibliography is retained. The reference paper's custom alphabetic BibLaTeX/Biber modifications are not required for COLT layout.
- Existing named proof headings remain supported through `amsthm`, with the class's own theorem definitions disabled. The sole `tabularx` table was replaced by equivalent fixed-width columns to avoid the class's table-footnote incompatibility.

## Content checks and small corrections

The source comparison preserved every compared formal block and labeled display equation. Its explicit counting rule finds 70 outer statement/proof/algorithm blocks and 153 labeled displays in the baseline and revised sources, including the shared formulation. This count differs from the earlier editorial audit's extraction rule; no mathematical statement was added or removed. The only permitted formal-text normalization beyond whitespace is changing `cref` to `eqref` for the nontrivial-regime equation, so the rendered sentence reads naturally.

The introduction now says 'polylogarithmic dependence' to match the abstract and explicit work bound. The comparison-table caption was shortened to avoid a final line containing only a symbol. Algorithm steps, mathematical formulas, graph/source scope, probability qualifications, and all 31 cited keys are preserved. The general-matrix discussion from the separate audit has not been promoted into a theorem.

## Verification

- All 47 pages were inspected individually. After the final polish, only pages 8 and 9 changed; both were rendered and inspected again.
- No clipped or overlapping content, overfull boxes, missing glyphs, unresolved references/citations, duplicate labels, or unresolved internal PDF destinations.
- All 21 font records are embedded Type 1 fonts; no Type 3 fonts. PDF title/author metadata and the email link are correct. All 374 named destinations resolve.
- Five focused manuscript-notation checks passed. The coordination audit passed.
- The source archive was extracted into a fresh directory and compiled with shell escape disabled. Its extracted PDF text is identical to the active build.
- The broader repository suite again reports 231 passed and the same 3 previously documented research-note/notation-audit failures. Full lint again reports the same 2 old research-note findings. These are recorded in the verification JSON and were not changed by the formatting work.
- Nonblocking TeX diagnostics remain: legacy roman-font commands, a script-font size substitution from 5.5pt to 5pt, and three underfull bibliography lines. Their rendered output was inspected.

## Submission status

The local publication package is prepared; nothing has been uploaded. Author details are complete. The author explicitly selected Creative Commons Attribution 4.0 International (CC BY 4.0); it is recorded in the submission metadata. The browser access check was repeated after the license selection and again blocked because the administrative security policy could not be verified. No upload occurred and no alternative route was attempted.

Official references: [PMLR template guidance](https://proceedings.mlr.press/faq.html), [arXiv PDF requirements](https://info.arxiv.org/help/policies/format_requirements.html), [TeX submission requirements](https://info.arxiv.org/help/submit_tex.html), and [license choices](https://info.arxiv.org/help/license/index.html).

The prior 43-page PDF, sources, metadata, and manifests are preserved in `publication-20260909/before-colt-format/` in the task workspace. Build/render evidence is in `colt-style-20260909/`.

## Fingerprints

- PDF SHA-256: `623f43c325ea80519fafb7428856cf3dee3fb7f5b913d46d440fa2d00d7aa099`
- Archive SHA-256: `003852e60973f4b409d3a5ec55e05008e8e5963656a247e76a1c41bc2b6f0f24`
- Extracted-text SHA-256: `182e79dab40548522f974b7c489e7a51e6c84ba2eda71d85364892c9649f0f26`
