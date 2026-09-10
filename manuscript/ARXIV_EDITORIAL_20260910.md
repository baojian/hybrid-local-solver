# Editorial and proof-exposition review — 10 September 2026

The author requested a two-hour improvement pass, with approximately six main sections and selective equation numbering. The current manuscript has **six main sections, three appendices, 75 numbered equations, 48 pages, and 31 cited references**. It retains the requested COLT-style JMLR/PMLR layout, the confirmed Fudan affiliation and email, and the author's CC BY 4.0 choice.

This pass combines structural editing, notation cleanup, independent mathematical reading, source comparisons, and PDF/source-package verification. It is not a formal verification of every theorem or a new exhaustive literature search. The dated September 9 literature review and August–September search evidence remain the records for the earlier novelty review.

## Structure and equation numbering

The eight previous main sections are now grouped as follows:

1. Introduction, including a concise related-work subsection.
2. Problem Formulation and Main Results.
3. Stieltjes Geometry and Local Certificates.
4. Deterministic Accelerated Continuation: algorithm, analysis, and implementation.
5. Randomized Threshold Batching: algorithm, depth, and total-work analysis.
6. PPR Consequences and Discussion.

Appendix A retains the detailed related-work and normalization comparisons. Appendix B contains the bounded-arithmetic implementation; Appendix C contains the explicit-seed extensions. All previous section labels remain valid. The organization paragraph and PDF bookmarks follow the new hierarchy. A page break separates the bibliography from Appendix A.

Equation numbering is explicit and selective: **153 numbers became 75**. Of the 75 retained numbered displays, 66 are referenced in the active manuscript. Nine further displays retain numbers because they define the central graph, PageRank, RPPR, or obstacle problems, or state the principal deterministic work guarantee. Seven of these are canonical definitions in the shared formulation. Unreferenced intermediate algebra uses unnumbered display environments. There are no labels attached to unnumbered displays, no manual equation tags, and no broken equation references.

The nine intentionally unreferenced numbered labels are `eq:shared-volume`, `eq:shared-seed`, `eq:shared-pagerank-matrices`, `eq:shared-pagerank-objective`, `eq:shared-ppr-solution`, `eq:shared-rppr-objective`, `eq:shared-rppr-kkt`, `eq:deterministic-main-work`, and `eq:shifted-obstacle`.

## Exposition and notation

- The opening sections define Stieltjes matrices and safe subsolutions, expand SDD and the names of CDPR/ASPR, and state the three contributions without internal OP1/OP2 labels. The table distinguishes objective accuracy, original graph volume, matrix sparsity, and probability qualifications.
- Algorithm descriptions now introduce their inputs, zero extension, stopping variable, output transformation, and proof dependencies before use. The two deterministic energies and their different comparator roles are explained at the point where they enter the analysis.
- The implementation describes the initial common scale, zero response records, record disposal at stage handoff, and the density representation of the output. The appendix states what contributes to the rational input length and treats the diagonal and zero-output cases explicitly.
- Vector components, a local Schur-complement name, and complement notation are consistent. Obsolete roman-font commands were replaced in active prose; the shared mathematical macro and formulation files remain unchanged.
- The table and its following discussion are kept together. Proposition 14's hyperlink now lands at its heading rather than at the foot of the preceding page. The theorem numbering remains global and unchanged.

## Mathematical qualifications clarified during review

These changes are more than typography and should not be described as literal preservation of every proof sentence. The main numerical work bounds and algorithm recurrences are unchanged.

1. **Reachable-face regime.** The active-face discussion now explicitly assumes the nonzero point-source regime. The actual algorithms already handle the zero optimum separately. This avoids invoking initial strict positivity when the optimum is zero.
2. **Finite threshold sequences.** The definition now requires the residual threshold for every optimum coordinate outside the current face, including coordinates not yet listed in a future block. The previous wording was ambiguous for a finite prefix. The numerical algorithm already certifies all unreported coordinates, so it satisfies the clarified hypothesis. The analytical completion is used in the proof and does not require the algorithm to know the optimum support.
3. **Depth interpretation.** The text states when the decaying term becomes at most half the requested absolute objective tolerance; it no longer suggests a relative constant-factor contraction from an arbitrary intermediate face. The padded block-zero vector and the matrix identity used in the Chebyshev argument are explicit.
4. **Deterministic flow and repair.** The raw mass is explicitly defined before the signed-flow charge. The selected signed sum is retained through the telescope. The repair proof separates the stronger inequality on retained positive coordinates from the nonpositive residual on zero coordinates, which follows from the Stieltjes signs. The rounded repair uses the same distinction.
5. **Explicit-seed accounting.** Input records and the diagonal case are charged explicitly. The superposition comparison discards sufficiently small weights, charging their error, before constructing constant-factor dyadic square-root estimates. This removes a hidden dependence on the smallest positive source weight from the stated logarithmic factors.

Independent reviews covered obstacle geometry, deterministic comparison and response energies, cumulative signed-flow charging, finite threshold depth, the certified randomized wrapper, PPR conversion and set completion, bounded arithmetic and rebasing, and explicit-seed extensions. Small exact-arithmetic and finite-sequence diagnostics supplement the proof reading; they are diagnostics rather than proofs over all inputs.

## Current theorem map

| Claim | Current location and dependencies |
|---|---|
| Deterministic local acceleration | Theorem 2; Lemmas 11–13, Proposition 14, Lemmas 15–16, Theorem 17, and Lemma 18 in Section 4 |
| Randomized support-adaptive acceleration | Theorems 3 and 19; safe pivots and boundary discovery in Theorem 8 and Corollary 9; Lemma 20 and Theorem 21; certified completion and Corollary 23 in Section 5 |
| Semantic PPR and positive residual | Proposition 1, Corollary 4, and Corollary 24 |
| Set-only PPR completion | Lemmas 25–26 and Theorem 27 in Section 6 |
| Bounded-arithmetic implementation | Lemmas 28–30 and Theorem 31 in Appendix B |
| Explicit seed distributions | Theorem 32 and Propositions 33–34 in Appendix C |

## Related-work checks

The main comparison table was checked against the primary ISTA, CDPR, ASPR, and 2026 sources. In particular, the ISTA objective-rate pointer is Theorem 3 after equation (23) in the 2019 paper. The equality between external matrix sparsity and original support volume plus cardinality is explicitly restricted to `0 < alpha < 1`; the diagonal case is separate.

The AESP comparison uses exactly the same lazy PageRank parameter and semantic degree-normalized error as its source: the primary paper's equation (1), problem (P1), equation (3), and Theorem 3.6/equation (13) confirm this. Its `alpha < 1/2` qualification needs no parameter conversion. The separate AESP–LOCSOR locality question is not promoted to a proved result.

Bibliographic corrections protect “Lagrangian” capitalization, identify the full version containing the cited ICDT 2024 theorem, and update the 2026 proceedings page range and preprint wording. All 31 cited keys are retained. No new claim of an exhaustive absence of competing work is made in this revision.

## Content accounting and validation

The baseline is the 47-page release preserved in the task's `publication-20260909/before-editorial-20260910/` directory. The comparison follows all 22 active TeX inputs.

- All **191 display blocks** are accounted for: 183 match under layout, numbering, and font normalization; seven have individually checked notation changes; one duplicate point-source display was removed while one display stating the complete-support threshold condition was added. No unexplained display or numerical-bound change was found.
- All inline-formula differences were reviewed: 954 formulas before and 1,015 after, with 927 unchanged sequence matches, two exact relocations, and 60 reviewed edit groups. All three pseudocode blocks were compared separately.
- The same 34 theorem-family statements, in the same order and with the same titles and numbers, and 33 proof environments remain. Together with the three algorithms, these are the same 70 formal blocks. Their prose is intentionally revised as described above.
- All 132 active labels and 175 concrete reference uses resolve. The 75 printed equation tags and 34 theorem-family headings are consecutive and match the source labels. All 31 citation keys resolve.
- The final active manuscript and extracted 27-member source archive compile. The isolated build disables shell escape and produces byte-identical extracted PDF text. Final logs have no undefined references or citations, no overfull boxes, and no outstanding rerun request. The remaining script-font size substitution and three underfull bibliography lines were visually checked.
- All 48 pages were visually reviewed. The final PDF has embedded fonts, no Type 3 fonts, 298 valid named destinations, 297 valid internal links, and 38 correctly nested section/appendix bookmarks. Author, affiliation, email, title metadata, and submission abstract were checked.

Focused notation checks pass. The broader code suite was not rerun for this manuscript-only revision. The previous run's 231 passes and three research-note/notation failures, together with two older-note lint findings, are historical results; the current delivery's `build-verification.json` labels them accordingly. No solver implementation or experiment result was changed in this pass.

Detailed review ledgers and immutable rendered candidates are retained in the task's `editorial-20260910/` directory. They include formula, inline/pseudocode, reference, primary-source, mathematical, visual, and isolated-build records.

## Release fingerprints and submission status

- PDF SHA-256: `cb923662bec5fead954da6b05ad8ca808df06ced9d37d6c9be57fc7132860d8a`.
- Source archive SHA-256: `b6faa803e39200dbf9bba63ca5e10e16b54201e94b3a537699b16c0386389dcb`.
- Extracted PDF-text SHA-256: `5e34787ab96c67147850fd731d101b74f683ed732f084eeb049d0fc1e4dfb07f`.

The release files are in `dist/`; the archive entry point is `main.tex`. Confirmed author details and CC BY 4.0 are retained in `dist/submission-metadata.txt`. The source archive is self-contained for compilation with its stated standard TeX Live dependencies.

No article has been uploaded. The previously recorded arXiv access block remains: the administrator-enforced security policy could not be verified. This editing pass made no upload attempt. The final review does not extend the PageRank-specific work guarantees to arbitrary sparse matrices.
