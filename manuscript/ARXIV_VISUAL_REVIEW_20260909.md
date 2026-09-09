# Final manuscript visual and citation-scope QA

Checked 2026-09-09, after the build recorded in `/tmp/ppr-publication-build-20260909-final.log` completed.

**Result: pass for visual presentation and the audited citation comparisons. No mandatory fixes identified.** This record is not a new proof audit, test-suite result, or arXiv submission confirmation.

## Exact artifact

- File: `/Users/baojian/git/hybrid-local-solver/manuscript/main.pdf`
- Title: *Accelerated Local Algorithms for Personalized and Regularized PageRank*
- Author metadata and displayed author: Baojian Zhou
- Length: 41 A4 pages; 685,739 bytes
- SHA-256: `4cbc8e8906b21ce025153bd36b39957a394bbfeff22bf00034b2e6910cf4764d`

## Visual review performed

All 41 pages rendered successfully into `page-01.png` through `page-41.png`, each at 900-pixel page width. All pages were first inspected in seven overview sheets. A second readable-size pass used individual pages 1, 7--11, and 32--34 plus sixteen two-page sheets covering every other page. These readable sheets are `readable-01.png` through `readable-16.png`; each retains a 900-pixel width per page without downscaling the page images.

No clipping, overlap, cropped equation numbers, blank replacement glyphs, broken tables, truncated algorithms, or missing page content was observed. The long comparison formulas on pages 9--11, the algorithms on pages 17, 26, and 30, and the long rounded-arithmetic formulas in Appendix A stay inside the margins. The title is legible on two lines. References wrap cleanly across pages 32--34, including long linked URLs. Page numbering is continuous through page 41.

## Build and citation resolution

The final `main.log` contains no undefined citations, undefined references, or overfull boxes. It records one underfull line warning in the bibliography; the corresponding reference-page layouts are visually acceptable. Earlier passes in the aggregate build log contain undefined-citation warnings that were resolved by subsequent bibliography and LaTeX passes; they are not present in the final log or final PDF.

Full text extraction succeeded. Searches of the extracted PDF found no `??`, `[?]`, or `(?)` placeholders. The new citations are present as linked author-year references, with bibliography entries for Bertram--Jensen, Jiang et al., Kwok--Wei--Yang, Lin--Deng, Chen--Peng--Wang, Vladu, Wei--Wen--Yang, and Thorup et al.

An optional Poppler bounding-box extraction mode aborted internally with `std::out_of_range`. It was not used as evidence. Ordinary full-text extraction, all 41 raster renders, and both visual passes completed successfully. No PDF was edited or re-exported during this audit.

## Citation-scope checks

The revised introduction, main-result framing, related work, and references were read together with `literature_2026.md`, `literature_independent.md`, and the consolidated novelty review. The following potentially misleading comparisons have been handled correctly:

1. OP1 and OP2 are explicitly project-defined contracts. The text attributes the COLT 2022 running-time target to RPPR and states that semantic PPR follows through the explicit conversion.
2. Fountoulakis--Martínez-Rubio is identified as v2, submitted April 8, 2026. Its upper bound retains both over-regularization and confinement, and the standard-FISTA negative result is not presented as a barrier for every local accelerated algorithm. The two-regularizer idea is credited.
3. Wei--Yang is identified as v1, submitted August 17, 2026. The support-cardinality factor, additional ACL certificate, caller-set probability, and deterministic almost-linear-solver variant are retained. No claim that deterministic active-set methods were absent remains.
4. The comparison table distinguishes exact CDPR optimization from additive objective approximation. Its SDD and new randomized rows preserve their probability qualifications in the surrounding text.
5. The ICDT 2024 SSPPR-D result is recognized as matching the degree-normalized error criterion; the discussion distinguishes its fixed-teleportation convention, preprocessing, and Monte Carlo output instead of dismissing it as a different norm.
6. Bertram--Jensen and Jiang et al. are discussed with their graph/error/access regimes. Their lower bounds are not imported as universal lower bounds with variable alpha for the manuscript's task. Thorup et al. is correctly treated as a directed single-node, fixed-teleportation result.
7. Kwok et al.'s scalar query is distinguished from discovering and returning an entire sparse vector. Lin--Deng's constrained formulation and identification/iteration guarantees are not presented as a cumulative local-work theorem.
8. Chen--Peng--Wang and Vladu receive credit for the established optimization geometry and global algorithms; their whole-input costs are distinguished from local discovery and boundary accounting.
9. The text makes no universal optimality, uniformly-faster, empirical speedup, or ordinary floating-point stability claim. It preserves the support-adaptive minimum and separates exact-real work from the specified rounded implementation.

The directly competing 2026 source contracts were independently checked against their exact PDFs in the earlier focused audit. For newly added broader sources, this pass checked consistency with the separate primary-source audit and inspected the resulting comparisons; it did not reconstruct every original source proof.

## Scope preserved

The repository was read only during this QA. Only new images, extracted text, and this QA record were written under the publication-review workspace. Tests were not rerun. Parent-agent archive rebuilding and independent checks are recorded separately.
