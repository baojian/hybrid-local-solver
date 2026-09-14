# Public research history

Prepared September 14, 2026, with the author's authorization to remove materials that could not be cleared for public redistribution. This is a filtered research history. The original private repository is retained as `baojian/hybrid-local-solver-private-history` after migration.

## What readers can inspect

The public copy retains all 505 selected research commits, including 44 pull-request head snapshots and an otherwise unmerged local research branch. Empty commits and merge parents are retained. The filtering preserves every retained file's exact Git blob ID and mode, and preserves author/committer identities, dates, commit messages, and parent order. [The verification report](history-verification.json) records the checks. New release-preparation commits are dated when they were made. Original signatures on 43 commits cannot survive rewriting; they were removed, and the public counterparts do not inherit their original Verified status. The signed originals remain in the private archive.

The notes include failed proof paths, corrections, conditional results, open problems, AI-assisted development, and limitations of computational checks. Publishing a historical claim does not make it correct. The active manuscript and each note's status record identify the intended current scope.

## Proof reading guide

Start with the two historical proof milestones cited in the [manuscript's development record](../../manuscript/sections/development_record.tex). Each source link below is pinned to the indicated commit, so later edits do not change the text it opens. The commit page shows the change; the source links show the complete argument at that revision.

### Randomized threshold batching

[Public commit `9ebb285da402`](https://github.com/baojian/hybrid-local-solver/commit/9ebb285da402e0ddf3cdc621240b5502a822b61f), originally `3fa8455`, committed August 30, 2026 at 01:22:06 UTC+8: **research: prove OP2 via threshold-batch LCP decay**.

Read the `active_edge_lcp` note in this order:

1. [Safe batched pivots](https://github.com/baojian/hybrid-local-solver/blob/9ebb285da402e0ddf3cdc621240b5502a822b61f/manuscript/notes/active_edge_lcp/sections/body/note_part1.tex#L324-L410), `thm:safe-pivots`: why admitted vertices belong to the optimal support.
2. [Threshold-batch Cholesky decay](https://github.com/baojian/hybrid-local-solver/blob/9ebb285da402e0ddf3cdc621240b5502a822b61f/manuscript/notes/active_edge_lcp/sections/body/note_part1.tex#L673-L860), `thm:batch-depth`: the block-Cholesky/Chebyshev argument bounding the number of batches.
3. [Algorithm, guarantee, and total-work proof](https://github.com/baojian/hybrid-local-solver/blob/9ebb285da402e0ddf3cdc621240b5502a822b61f/manuscript/notes/active_edge_lcp/sections/body/note_part2.tex#L1-L213), `alg:threshold-batch` and `thm:op2`: certified randomized SDD calls on discovered principal systems, objective accuracy, and the fully charged expected-work bound.

The later conditional persistent-continuation contract in the same note is a separate, stronger interface; it is not a premise of `thm:op2`. For the current exposition, read the manuscript's [algorithm](../../manuscript/sections/threshold_batch_algorithm.tex), [batch-depth proof](../../manuscript/sections/threshold_batch_depth.tex), and [correctness/work analysis](../../manuscript/sections/threshold_batch_analysis.tex).

### Deterministic accelerated continuation

[Public commit `d97d280560ba`](https://github.com/baojian/hybrid-local-solver/commit/d97d280560ba8dd085813d11737dad96c2552221), originally `0f0ac32`, committed September 6, 2026 at 00:42:47 UTC+8: **Add independent deterministic OP2 acceleration note and proof archive**.

Read the preserved original proof in `deterministic_op2_independent_20260905/original_sources/deterministic_conjecture2.tex.txt`:

1. [Statement and model](https://github.com/baojian/hybrid-local-solver/blob/d97d280560ba8dd085813d11737dad96c2552221/manuscript/notes/deterministic_op2_independent_20260905/original_sources/deterministic_conjecture2.tex.txt#L52-L97), `thm:main`: the deterministic local-work and safe-output guarantees in the exact-real arithmetic model.
2. [Two comparison energies](https://github.com/baojian/hybrid-local-solver/blob/d97d280560ba8dd085813d11737dad96c2552221/manuscript/notes/deterministic_op2_independent_20260905/original_sources/deterministic_conjecture2.tex.txt#L151-L288), including `lem:comparison`, `lem:sector`, and `eq:response`.
3. [Selected signed flow and cumulative work](https://github.com/baojian/hybrid-local-solver/blob/d97d280560ba8dd085813d11737dad96c2552221/manuscript/notes/deterministic_op2_independent_20260905/original_sources/deterministic_conjecture2.tex.txt#L290-L337), `eq:work`: the bound that charges repeated support scans.
4. [Certified repair and continuation schedule](https://github.com/baojian/hybrid-local-solver/blob/d97d280560ba8dd085813d11737dad96c2552221/manuscript/notes/deterministic_op2_independent_20260905/original_sources/deterministic_conjecture2.tex.txt#L339-L393), `lem:repair` and `sec:schedule`.
5. [Exact sparse reporter and complete work ledger](https://github.com/baojian/hybrid-local-solver/blob/d97d280560ba8dd085813d11737dad96c2552221/manuscript/notes/deterministic_op2_independent_20260905/original_sources/deterministic_conjecture2.tex.txt#L395-L463): the implementation argument completing the core theorem.

The `.tex.txt` suffix preserves the readable original TeX source. The separately scoped [bounded-arithmetic refinements](https://github.com/baojian/hybrid-local-solver/blob/d97d280560ba8dd085813d11737dad96c2552221/manuscript/notes/deterministic_op2_independent_20260905/original_sources/practical_refinements_appendix.tex.txt) are also present at this commit. For the current exposition, read the manuscript's [algorithm](../../manuscript/sections/deterministic_algorithm.tex), [energy and work analysis](../../manuscript/sections/deterministic_analysis.tex), and [sparse implementation](../../manuscript/sections/deterministic_implementation.tex).

Both arguments appear together in the [integrated manuscript snapshot](https://github.com/baojian/hybrid-local-solver/tree/cb67f5fd258e039fe931a1c99f6d98ec3ec3141f/manuscript) at public commit `cb67f5fd258e` (originally `7e1b4e7`, September 6, 2026). Later revisions refine the exposition and guarantees; the links above identify the historical proof records rather than asserting that every current statement already appeared there.

## Mapping the paper's original commit references

Filtering changes commit IDs. The identifiers printed in the submitted manuscript refer to the original private history; use the links below to inspect their public counterparts. These copies preserve the retained research source bytes.

| Milestone | Original commit | Public counterpart | Original committer date |
| --- | --- | --- | --- |
| Randomized threshold-batch proof | `3fa84552e6582604a214021f20310df1c6290c9e` | [9ebb285da402](https://github.com/baojian/hybrid-local-solver/commit/9ebb285da402e0ddf3cdc621240b5502a822b61f) | August 30, 2026 (UTC+8) |
| Deterministic continuation proof | `0f0ac32d70290f2c6877b4cf1faa7da85e2835ee` | [d97d280560ba](https://github.com/baojian/hybrid-local-solver/commit/d97d280560ba8dd085813d11737dad96c2552221) | September 6, 2026 (UTC+8) |
| Both proofs integrated in the manuscript | `7e1b4e77351b361e0c700ce3186c1534d2023f0e` | [cb67f5fd258e](https://github.com/baojian/hybrid-local-solver/commit/cb67f5fd258e039fe931a1c99f6d98ec3ec3141f) | September 6, 2026 (UTC+8) |

[Complete original-to-public commit mapping](commit-map.txt). An unchanged date in a filtered commit records the original development metadata, not an earlier public release. Git timestamps and the exported GitHub records support a development chronology; they do not establish an earlier public disclosure or certify a proof.

## What was excluded and why

The [235-path inventory](excluded-paths.json) lists every excluded historical path and its reason. The excluded classes are:

- downloaded third-party source-paper payloads;
- imported publication workspaces, coauthored historical manuscripts, and reviewer correspondence whose redistribution was not cleared;
- opaque source/data bundles, nested environments, executables, raw session exports, and local build/editor artifacts;
- two unused legacy `jmlr2e.sty` paths without an explicit redistribution license in the retained distribution;
- compiled PDFs outside the retained project figure directory. The active manuscript and standalone note sources remain available for rebuilding.

The removal criteria concern redistribution and inspection scope. They are not findings that the excluded material was unlawful, nor judgments about which research attempts succeeded. Originals remain privately preserved.

To retain readable evidence from the research bundles, [1,010 original text files](../../manuscript/research-records/README.md) are published separately with unchanged content bytes, archive/member paths, and SHA-256 checksums. That manifest explicitly records 97 omitted archive members. The bulky `raw-results-*.zip` bundles remain private; the public excerpts include available source code, original proof drafts, notes, and selected measurement records.

## Hosted records and previous links

Original GitHub PR discussions, Actions logs, artifacts, and attachments stay with the private original repository and are not transferred to this replacement. Public branches under `history/pr/` preserve filtered commit snapshots, not the GitHub discussion threads. [Workflow metadata](workflow-metadata.json) and [pull-request metadata](pull-request-metadata.json) retain selected dates, commit IDs, and outcomes, including failed workflows. These exported records are not independently signed timestamp attestations.

Old deep links using an original commit ID at `hybrid-local-solver` will not resolve after the replacement. This page and the full mapping are the public lookup. A future manuscript revision can link this page; the already submitted arXiv version is not changed by repository preparation.

## Inspection and limitations

The history was scanned with Gitleaks 8.30.1. The initial 34 matches were reviewed as author-year-title citation identifiers, not credentials; [the review record](secret-scan-review.json) identifies them. The extracted working tree is scanned separately. Scanner output is evidence of the stated checks, not a guarantee against every possible disclosure issue. See [validation](VALIDATION.md) for final results and known repository test failures.

The original implementation paths under `src/` and provider experiments/tests were not modified by the release filtering. Historical snapshots may have missing optional external archives or fail modern tests. This release does not add a blanket reuse license; existing licenses remain applicable. See [rights and third-party notices](../../RIGHTS.md).

## Maintainer instructions

Continue development from a fresh clone of this public-history repository. Do not merge or push the unfiltered private repository's branches into it. Keep the original repository private, including its Actions logs and LFS objects. Obtain redistribution clearance before adding imported papers or correspondence. The local-only `papers/` convention is documented in [the paper library guide](../../papers/README.md).
