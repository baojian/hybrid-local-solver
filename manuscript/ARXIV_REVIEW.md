# ArXiv manuscript preparation and review

## Current revision: 10 September 2026 title alignment correction

Both title lines are now centered. A one-command line-break correction fixes the first line's 38-point left offset. The paper remains 48 pages with six main sections, three appendices, 75 numbered equations, and 31 references. All text, pages 2–48 drawing streams, named destinations, and links are unchanged.

The [title-alignment review](ARXIV_TITLE_ALIGNMENT_20260910.md) records the measured alignment, visual check, and successful independent archive build. Current PDF SHA-256 is `5bdc837bedd323beedd674f5b0e28d5b39730bfd8dede83aa5ed4873730aa5db`; current source-archive SHA-256 is `227b68679f8648f3c19165b6fb20bdf08ba133cfd697fcbd6195bf23ba2765db`. The previous version is preserved in the task's `publication-20260909/before-title-alignment-20260910/`. No upload was attempted.

---

## Historical revision: 10 September 2026 editorial and proof-exposition review

The current release has **six main sections, three appendices, 75 numbered equations, 48 pages, 31 references, and a 27-member source archive**. Equation numbering is selective: 78 unneeded numbers were removed while all displayed mathematics is accounted for. The confirmed author details and CC BY 4.0 choice remain unchanged.

The [editorial review](ARXIV_EDITORIAL_20260910.md) records the structure, equation policy, notation cleanup, primary-source comparisons, and proof qualifications clarified during independent reading. All 191 display blocks, inline-formula changes, and three algorithm blocks were compared against the preserved 47-page baseline. The same 34 theorem-family statements and 33 proof environments remain; their prose is intentionally clarified, so this is not a claim of byte-identical proof text.

The final PDF and fresh extracted archive compile with identical extracted PDF text. All 48 pages were visually reviewed; equation, theorem, citation, bookmark, and hyperlink targets were checked. Focused notation tests pass. No full solver-suite rerun or new numerical experiment was performed for this manuscript-only revision; the test/lint results below remain historical.

- PDF SHA-256: cb923662bec5fead954da6b05ad8ca808df06ced9d37d6c9be57fc7132860d8a
- Source archive SHA-256: b6faa803e39200dbf9bba63ca5e10e16b54201e94b3a537699b16c0386389dcb
- PDF-text SHA-256: 5e34787ab96c67147850fd731d101b74f683ed732f084eeb049d0fc1e4dfb07f

Current files are under `dist/`. The preceding 47-page release is preserved in the task's `publication-20260909/before-editorial-20260910/`. No upload was attempted in this editing pass. ArXiv submission remains pending after the previously recorded administrative security-policy verification block.

---

## Historical revision: 9 September 2026 COLT formatting

The current release has **47 pages, 31 references, and a 27-member source archive**. The title page contains the author-confirmed Fudan affiliation and contact email. The paper uses the official JMLR/PMLR class with COLT-style Times typography, running headers, and global theorem numbering, without proceedings or acceptance claims.

The [COLT formatting review](ARXIV_COLT_FORMAT_20260909.md) records content preservation, all-page visual inspection, font/link checks, and a successful isolated archive build with identical extracted PDF text. Five focused notation checks and the coordination audit passed. The full repository run again has 231 passes and the same 3 historical failures; the same 2 older-note lint findings remain.

- PDF SHA-256: 623f43c325ea80519fafb7428856cf3dee3fb7f5b913d46d440fa2d00d7aa099
- Source archive SHA-256: 003852e60973f4b409d3a5ec55e05008e8e5963656a247e76a1c41bc2b6f0f24
- PDF-text SHA-256: 182e79dab40548522f974b7c489e7a51e6c84ba2eda71d85364892c9649f0f26

The current files are under dist/. The prior 43-page release is preserved in the task's publication-20260909/before-colt-format/. No article was uploaded. The author selected CC BY 4.0. A fresh browser access check was again blocked because the administrative security policy could not be verified; no upload occurred.

---

## Historical revision: 9 September 2026 author-style revision

The revised manuscript has **43 pages, 31 references, and a 25-member source archive**. The abstract and introduction now present three contributions; Sections 5 and 6 group each algorithm with its analysis; the detailed literature comparisons are retained in Appendix A. The main results, proof bodies, algorithm steps, and mathematical conventions are preserved.

The [style-revision review](ARXIV_STYLE_REVISION_20260909.md) records the changes and checks. All 69 formal environments and 150 retained labeled formulas passed the preservation comparison. Five focused notation checks passed. The fresh extracted source archive compiles and produces identical PDF text. All 43 pages passed visual inspection, with embedded fonts and no unresolved references/citations or overfull boxes.

- PDF SHA-256: 15c97ecfaa1d8ea515e81e9cd7f16f5dafa7e085f08836b2414e8984299655ea
- Source archive SHA-256: 74c6602d6b4a6396833bf82c6b6bcd9c0118e9bf5b8eaf46aa70ca2ad0c46b0c
- PDF-text SHA-256: 662a4d42873540b1cb7b6016351d1480bfa775a399f8c0396530ef7da5b65076

The updated PDF, source archive, and submission metadata are under dist/. The previous 42-page delivery is preserved in the task's publication-20260909/before-style-revision/ directory. No new literature search or numerical experiment was performed for this exposition revision; the earlier dated evidence is retained below. ArXiv submission remains pending following the previously recorded browser security-policy block.

---

## Historical revision: 9 September 2026 literature sweep

Prepared **Accelerated Local Algorithms for Personalized and Regularized PageRank**, by Baojian Zhou: 42 pages, 31 cited references, and a self-contained 23-member source archive. The full deterministic and randomized proof files are preserved. The title, abstract, introduction, result overview and discussion now explicitly cover both project-defined contracts: OP1 semantic PPR and OP2 RPPR objective approximation. OP1 follows from the existing regularization-bias conversion, not an additional independent algorithm.

The related-work review now covers same-accuracy ICDT 2024 results, local diffusion, the two closest 2026 papers and their latest versions, newer PPR estimation/centrality and asymmetric-system results, global flow/M-matrix optimization and constrained sparsity identification. No additional earlier theorem matching the full joint parameter/access/output contract was found in the searched public sources. This is not an exhaustive absence guarantee. The dated [literature review](../docs/literature/publication-review-20260909.md) retains primary URLs, exact pointers and search limits; `ARXIV_SOURCES.json` indexes the cited sources.

The subsequent [August–September arXiv sweep](../docs/literature/arxiv-aug-sep-audit-20260909.md) retrieved 3,775 distinct records across the specified keyword/category queries and screened every title, with selected abstracts and targeted full-text comparisons. It adds Thorup–Wang's August revision and Li–Yang's September regularized-resistance paper. The query scope and reading-depth limits are explicit; this is not an all-arXiv full-text absence guarantee.

### Validation recorded for the 42-page release

- Main PDF and bibliography compile; no undefined references/citations or overfull boxes. One harmless underfull bibliography paragraph was visually checked.
- Extracted source archive independently compiles. Extracted and active PDF text are identical.
- Focused exact proof checks: 21 passed. Full existing suite: 231 passed, the same three historical failures below; 15 warnings.
- Coordination audit passed. Changed package builder passes Ruff. Full lint reports the same two older-note errors below.
- Main PDFs use embedded fonts. All 42 pages passed visual inspection; see [the dated QA report](ARXIV_VISUAL_REVIEW_20260909_WINDOW.md).
- No solver code, algorithm recurrence, benchmark result or original synced project source changed. No commit, push or arXiv upload was performed.

### Fingerprints of the 42-page release

- PDF SHA-256: `56b67deb467975d50c6ab4f547029e39219fe7059fa8924b8386a6a27e1a4f74`.
- Source archive SHA-256: `54f43bbf050ba13cd76eed950551536df504af7b9627063e7480ed348fd8dd77`.
- Active/extracted PDF text SHA-256: `bd60682327bb3b2acfc7b245cd5d9dea08fff02494408a00332942d929f4ca2b`.

### Submission status

The PDF is `dist/accelerated-local-rppr.pdf`; the upload archive is `dist/arxiv-source.tar.gz`, with `main.tex` as its entry point. Submission metadata is in `dist/submission-metadata.txt`. Browser access to arXiv was blocked because the administrator-enforced security policy could not be verified. No alternate route was used and no article was uploaded. The package is prepared for the author's submission; author details and licensing remain the author's choices.

The review below describes the earlier 39-page release. Its historical fingerprints and counts are preserved for provenance and do not describe the current files.

---

# Historical review: 6 September 2026

Status: local submission package prepared on 2026-09-06. The author will
submit to arXiv; no upload, publication, commit, or push was performed.
Work began from clean `main` at
`529be09beca95dadc87143cf4af90be46a6e08d2`.

## Deliverables and build

- Title: **Accelerated Local Algorithms for Regularized PageRank**.
- Author: Baojian Zhou. Standard article format, 39 pages, 19 cited sources.
- Editable entry point: [`main.tex`](main.tex).
- Release PDF: [`dist/accelerated-local-rppr.pdf`](dist/accelerated-local-rppr.pdf).
- Submission sources: [`dist/arxiv-source.tar.gz`](dist/arxiv-source.tar.gz).
- Per-file release hashes: [`dist/arxiv-source-manifest.json`](dist/arxiv-source-manifest.json).
- Cited-source versions, checksums, and exact pointers:
  [`ARXIV_SOURCES.json`](ARXIV_SOURCES.json).

From the repository root:

```bash
make paper
make -C manuscript arxiv
```

The source archive contains 23 files, including the active transitive LaTeX
inputs, `references.bib`, generated `main.bbl`, and a short build README.
It requires standard TeX Live packages and no research-note archive, source
paper, numerical package, generated research figure, or network access.
The bundle is generated by `tools/build_arxiv_bundle.py` from the TeX
recorder's actual input graph. It rejects imports from `notes/` and
`archive/`. Generated release files live in the Git-ignored `dist/` directory;
their editable sources remain in the worktree.

## Scope and proof authority

The main contract is OP2 from `notes/problem_definitions/`: a point source,
original graph degrees, additive RPPR objective accuracy, and fully charged
local access in the exact-real algebraic word model. The paper distinguishes
this algorithm-existence target from the COLT 2022 speculation about the
supports of standard accelerated proximal iterates. It does not assert that
standard FISTA satisfies that conjecture.

The complete randomized proof is in **`notes/active_edge_lcp/`**.
`notes/evolving_support_cg/` contains relevant obstructions and conditional
CG routes; it is not the source of the complete randomized OP2 theorem.
The deterministic development is preserved in
`notes/deterministic_op2_independent_20260905/original_sources/deterministic_conjecture2.tex.txt`,
with the audit and implementation evidence in
`notes/deterministic_op2_20260905/`. These are development and audit records
of the same core argument, not two unrelated algorithmic discoveries.

The active paper now contains the proofs itself. The original proof archives and
provider implementations were left unchanged. Shared formulation prose and
notation, including the expanded problem-definition reference, were reconciled without changing the graph operator, objective,
normalization, or implementation-wide stopping convention. The standalone
AESP–LOCSOR graph-uniform locality gate remains open and was not promoted.

## Final theorem chain

| Result | Proof components in the paper |
| --- | --- |
| Deterministic `O_tilde(1/(rho sqrt(alpha)))` local work, Theorem 2.2 | Diffuse correction domain (Lemma 5.1); safe stage repair (Lemma 5.2); accelerated comparison identity (Lemma 6.1); Euclidean convergence (Proposition 6.2); second projection comparison (Lemma 6.3); PageRank-metric response energy (Lemma 6.4); cumulative kinetic volume (Theorem 6.5); finite sparse reporter and full accounting (Section 7) |
| Randomized support-adaptive Las Vegas work, Theorem 2.3 | Safe Stieltjes batches (Theorem 4.4); local certificate (Lemma 4.6); self-contained Chebyshev approximation (Lemma 8.1); block-Cholesky depth (Theorem 8.2); fresh certified SDD calls and conditional failure accounting (Theorem 9.1); final repair (Corollary 9.3) |
| Semantic PPR and ACL residual guarantees | Bias and objective conversion (Proposition 2.1); direct PPR consequence (Corollary 2.4); positive-residual certificate (Corollary 10.1) |
| Set-only PPR handoff | Maximum-principle envelope comparison (Lemma 10.2); sparse objective certificate (Lemma 10.3); deterministic PCG or certified randomized SDD completion (Theorem 10.4) |
| Bounded-arithmetic deterministic implementation | Two perturbed energies, rounded-volume charge, closed-tail reporting, controlled neighbor records, scalar rebasing, integer key encodings, and rounded repair (Appendix A, Theorem A.4) |
| Explicit multi-source extensions | Block-source randomized depth with additive input work (Theorem B.1); deterministic repeated source-record work (Proposition B.2); comparison with superposition (Proposition B.3) |

The exact-stage volume proof gives `76 K/r`; the rounded-stage proof gives
`360 K/r`. Both charge repeated kinetic visits, and neither assumes a
containing region or a positive minimum activation margin. The second
energy uses a comparator that need not minimize that auxiliary quadratic;
the comparison identity explicitly permits this. The selected signed-flow
sum is retained until the telescope, rather than replaced by all positive
forcing. These are essential proof points.

The randomized method has expected work
`O_tilde(V* min{|S*|, alpha^(-1/2)})`, not merely its worst-case envelope.
Every admitted support coordinate is deterministically certified before its
adjacency list is scanned. Fresh SDD preconditioner construction, boundary
updates, residual certification, state disposal, and output are charged.
Restarting an explicitly failed run gives the stated Las Vegas guarantee.
The final projected-gradient/downward repair supplies the stronger
subsolution and ACL residual output without changing the soft work bound.

The bounded-arithmetic result is separate from the exact-real theorem and
specifies the rounding scheme; it is not a stability claim for arbitrary
floating-point code. The general-seed appendix also states its input
interface separately. It does not identify a mixture of regularized optima
with the optimum for a mixture.

## Related-work checks and attribution

The paper's comparisons were checked against primary papers, with pointers
recorded in `docs/literature/acceleration.md`, `local-solvers.md`, and
`lcp-solvers.md`. The source manifest pins the 18 local PDFs used and records
the primary online obstacle-paper text for the nineteenth citation. Twenty
selected theorem/formulation pages were additionally rendered and inspected.

- COLT 2022: equation (3), physical p. 2, matches the canonical objective;
  Section 3, p. 3, explicitly names FISTA and linear coupling.
- COLT 2023: the local 25-page PMLR version has its volume definitions on
  p. 4, CDPR Theorem 4 on p. 9, and ASPR Theorem 8 on p. 11. Its internal
  and external nonzero counts are kept distinct in the comparison table.
- Fountoulakis–Martínez-Rubio 2026 v2: Theorems 4.3–4.4 and the informal
  star counterexample are on physical p. 6. The two-regularizer comparison
  and its removal of a global minimum slack are credited to that work.
- Wei–Yang 2026 v1: Theorem 1.3 is on pp. 3–4. The deterministic SDD
  substitution remark on p. 4 is explicitly discussed. Their
  `O_tilde(rho^(-2))` regime can be smaller than the accelerated envelope;
  the paper makes no blanket optimality or first-deterministic-method claim.
- AESP 2025: equation (7), p. 5, defines the gradient-mass ratio; Theorem
  3.6, p. 7, retains it; p. 8 proposes a simplex constraint. The paper
  credits this precedent and identifies the additional box, source cap,
  projection comparison, and cumulative work proof.
- Ha et al. 2021: monotonicity is Lemma 4, p. 6; the stagewise path result
  is in Section 5, pp. 13–14. The paper includes its own normalized order
  argument while citing that prior result.
- Koutis–Miller–Peng: Lemma 4.5 is on p. 10 and Theorem 4.6 on p. 11 of
  the pinned local PDF. The caller-specified failure wrapper is proved in
  this paper; it is not attributed as a direct API of Theorem 4.6.

The library additions are the FISTA 2009 primary paper, KMP 2011 primary
paper, and the publisher's linear-coupling ITCS 2017 paper. Their retrieval
URLs and SHA-256 hashes are in the source manifest. Bibliographic entries,
`docs/literature/index.md`, and the relevant topic notes were updated
together. All three PDF paths use the repository's Git LFS filter.

## Verification and limitations of the checks

These are mathematical development and regression checks, not a formal proof
certificate or external peer review. The paper makes no benchmark speed
claim. No reported experimental dataset or result was changed, so
`make reproduce` was not required.

| Check | Result |
| --- | --- |
| Active paper build and bibliography | Passed; no undefined references/citations or overfull boxes |
| Extracted source archive build | Passed in `tmp/arxiv-review/isolated-arxiv-build-release/`; extracted PDF text is byte-identical to the active PDF text |
| PDF visual QA | All 39 pages inspected; every changed page was re-rendered and rechecked; no clipping or overlapping material |
| PDF fonts | All fonts embedded; no Type 3 fonts |
| Four source-note builds | `problem_definitions`, `active_edge_lcp`, and both deterministic OP2 notes compile; the tracked note PDF regenerated by this check was restored to preserve the archive |
| New proof checks | 21 passed: independent exact rational KKT/projection checks, two comparison metrics, signed-flow identity, perturbation inequalities, safe/rounded repair, and 216 multi-source block-Cholesky cases |
| Existing threshold-depth checks | 1,152 ordinary cases and 216 cases at 100-digit precision passed |
| Extracted deterministic package tests | 17 audit-package tests and 16 development-package tests passed |
| Full deterministic fast validation manifest | All 183 cases passed; 12,068 iterations, 2,760 oracle entries, 2,156 degree replies, and 520 stages; source hashes unchanged |
| `make agent-audit` | Passed |
| `make test` | 231 passed, 3 pre-existing failures, 15 warnings |
| `make lint` | Two pre-existing errors in older note scripts; new Python files pass Ruff and formatting |
| `git diff --check` | Passed |

The initial suite had 209 passes and four failures. Rewriting the active
related-work text removed its reserved-seed-notation failure. The remaining
three failures all concern unchanged older note sources:

1. `test_known_semantic_aliases_do_not_regress`: `r_\rho(` in
   `notes/aesp_cd_l1_rppr/sections/body/02_eq_aesp_cd_target.tex`.
2. `test_note_inventory_audit_passes` and
   `test_note_sources_stay_within_reviewable_size_limits`: the same note's
   `06b_prop_aesp_cd_dynamic_reporters.tex` has 1,237 lines and
   `06d_cor_aesp_cd_obstacle_primitives.tex` has 4,361 lines, above the
   1,000-line limit.

The two unchanged lint findings are F401 in
`notes/problem_definitions/verify_exact_batch_cholesky.py:14` and E731 in
`notes/spectral_balance_threshold_batch/green_band_stress_exact.py:248`.
The active PDF has one harmless underfull bibliography paragraph, visually
checked; there is no missing text. Logs and development reruns are under
`tmp/arxiv-review/`; they are deliberately excluded from the submission.

## Release fingerprints and elapsed window

- PDF SHA-256: `64525f7e6edbf1ff84c1e1d271a38f79ae5cc810446def6b0f55fa7a736d27a9`.
- Source archive SHA-256: `7fc704ff22954ddf62f66fdc1b7da4a1fdaba3d3bc25c8480445dd8fb82ac66e`.
- Active and isolated PDF-text SHA-256: `0bd914a2932b525995a156bb9e1502b525cc853147851a11fecf7d31f2599c4e`.
- Started: 2026-09-05 17:19:19 UTC (2026-09-06 01:19:19 Asia/Shanghai).
- Completion record: 2026-09-06 02:48:22 UTC.
- Elapsed preparation window at this record: 9 hours,
  29 minutes; exceeds the requested four-hour minimum.

The document includes a research-assistance disclosure. Baojian Zhou remains
the human author and controls the final submission.
