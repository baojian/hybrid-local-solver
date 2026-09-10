# Author-style manuscript revision: 9 September 2026

Revised *Accelerated Local Algorithms for Personalized and Regularized PageRank*, by Baojian Zhou. The current PDF has 43 pages and 31 cited references; the submission archive contains 25 files.

## Editorial changes

- Rewrote the abstract around the two algorithms, their RPPR guarantee, and the PPR consequence. Kept the expected-work qualification for both randomized guarantees.
- Replaced the introductory proof inventory with a three-part contribution list and a short explanation of why each method remains local.
- Grouped deterministic construction, analysis, and sparse implementation in Section 5. Introduced the complete procedure before its stage-handoff proof.
- Grouped the randomized procedure, batch-depth analysis, and total-work proof in Section 6. Named the delayed proof explicitly and kept its required definitions before it.
- Kept a concise related-work overview and comparison table in Section 3, with the full existing comparison text and normalization maps in Appendix A. The table now states the Wei–Yang high-probability qualification directly.
- Shortened the discussion and added interpretations after the main work bounds. Retained the canonical notation, graph and source assumptions, accuracy distinctions, arithmetic model, and research-assistance disclosure.

The layout follows the explanatory order found in the author's KDD 2023 and NeurIPS 2024/2025 papers. The existing article template remains appropriate for the arXiv version.

## Content and build checks

All 69 theorem, lemma, proposition, corollary, proof, and algorithmic environments are unchanged after ignoring whitespace and optional environment headings. All 150 retained labeled formulas are unchanged after ignoring whitespace and terminal sentence punctuation. The removed introductory duplicate of the kinetic-volume bound remains stated in the technical equation eq:det-kinetic-work; its obsolete introductory label had no references.

All 31 citation keys are retained, and each is covered by ARXIV_SOURCES.json. That literature-provenance file and the bibliography were not edited in this style revision. The source archive retains every previous member and adds related_work_overview.tex and threshold_batch_analysis.tex.

- Active PDF and fresh extracted archive both compile.
- Extracted PDF text is identical to the active PDF text.
- No undefined references or citations, duplicate labels, overfull boxes, or pending rerun warnings.
- All fonts embedded; no Type 3 fonts.
- Focused manuscript notation checks: 5 passed, 3 deselected.
- All 43 pages rendered and inspected individually. The final citation cleanup changed only pages 1–2; both were re-rendered and inspected again. Algorithm 1 is complete on page 13 and Algorithm 2 on page 21.
- One underfull bibliography paragraph remains readable and has no missing or overlapping content.
- No solver implementation or experimental result was changed. Earlier numerical and repository-wide test results remain dated historical evidence.

Evidence directory: /Users/baojian/.codex/.chatgpt-projects/g-p-6a61903d8df88191b0fa11a0ff57a7e1/style-revision-20260909

Previous 42-page delivery: /Users/baojian/.codex/.chatgpt-projects/g-p-6a61903d8df88191b0fa11a0ff57a7e1/publication-20260909/before-style-revision

## Fingerprints

- PDF SHA-256: 15c97ecfaa1d8ea515e81e9cd7f16f5dafa7e085f08836b2414e8984299655ea
- Source archive SHA-256: 74c6602d6b4a6396833bf82c6b6bcd9c0118e9bf5b8eaf46aa70ca2ad0c46b0c
- Active and isolated PDF-text SHA-256: 662a4d42873540b1cb7b6016351d1480bfa775a399f8c0396530ef7da5b65076

The source archive and submission metadata have been refreshed. No arXiv upload was performed.
