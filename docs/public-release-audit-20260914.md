> Historical pre-release record. The original private repository remains subject to the hold described below. The replacement public-history copy excludes the uncleared materials; see [the release guide](public-release/README.md) for its current scope and validation.

# Public-release and development-history audit

Audit date: September 14, 2026. Repository:
<https://github.com/baojian/hybrid-local-solver>.
Audited starting commit: `92a9f78bd94a4b7f1058ad1463ef3fbfe6b233fe`.
The initial worktree was clean. No commit, push, history rewrite, visibility
change, release, or arXiv submission was performed by this audit.

## Release decision: hold public visibility pending clearance

The author selected **preserve the existing repository and commit links,
but review permissions before exposing the full history**. The repository
remains private. This report does not authorize publication of historical
review correspondence, third-party PDFs, or unchecked hosted records.
Deleting a file at the tip would not remove it from public history.
Do not rewrite history merely to strengthen a chronology claim.

The following decisions remain necessary:

| Material | Finding | Required clearance |
| --- | --- | --- |
| `manuscript/archive/neurips-2024-locch/review.tex` and corresponding PDF | Contains quoted reviewer questions and author responses | Confirm this correspondence may be made public |
| `manuscript/archive/neurips-2025-aesp/review.tex` and corresponding PDF | Contains reviewer identifiers, ratings, questions, and rebuttal text | Confirm disclosure permissions; do not assume ownership of the paper covers every review |
| Historical source papers under `papers/` | 40 distinct LFS pointer blobs were found; upstream licensing varies | Establish redistribution permission for each retained PDF and historical version |
| Archived manuscripts and proof/research bundles | Include earlier drafts, working records, and other authors' contributions | Confirm author/coauthor consent and absence of confidential imported material |
| GitHub hosted history | 44 closed PRs, two issue comments, 99 workflow runs; no releases, artifacts, Pages site, wiki, or open issues reported | Review PR bodies and retained Actions logs before public exposure; metadata is not a content audit |
| License | No root license; GitHub reports no recognized repository license | Author chooses licensing if reuse is intended; do not invent permission for third-party material |
| Commit identities and local environment references | Email addresses and local filesystem references are present in the scanned history | Author accepts this disclosure or chooses another release strategy |

The two hosted issue comments were inspected and concern branch/merge
housekeeping. No PR review comments or non-PR issues were returned by the
checked endpoints. This does not clear PR bodies, old attachments, or all
Actions logs. The latest workflow fails at the research-note registry check;
its failure is not evidence of a failed mathematical proof.

## Earliest located proof-bearing snapshots

The following are the earliest located commits in the relevant theorem
lineages, not a claim about all private work or all possible earlier drafts.
Dates are shown in both UTC and the author's Shanghai timezone.

| Result | Immutable commit | Git committer time, UTC | Shanghai time |
| --- | --- | --- | --- |
| Randomized RPPR: threshold-batch depth and fully charged solver | [3fa8455](https://github.com/baojian/hybrid-local-solver/commit/3fa84552e6582604a214021f20310df1c6290c9e) | 2026-08-29 17:22:06 | 2026-08-30 01:22:06 |
| Deterministic RPPR: original continuation proof archive | [0f0ac32](https://github.com/baojian/hybrid-local-solver/commit/0f0ac32d70290f2c6877b4cf1faa7da85e2835ee) | 2026-09-05 16:42:47 | 2026-09-06 00:42:47 |
| Consolidated active manuscript with both proofs | [7e1b4e7](https://github.com/baojian/hybrid-local-solver/commit/7e1b4e77351b361e0c700ce3186c1534d2023f0e) | 2026-09-06 03:05:19 | 2026-09-06 11:05:19 |

### What the historical content actually contains

At `3fa8455`, inspect
`manuscript/notes/active_edge_lcp/sections/body/note_part1.tex`, section
**Threshold-batch Cholesky decay**, labels `thm:batch-depth`,
`eq:chain-domination`, and `eq:seed-tail-bound`; and `note_part2.tex`,
section **A fully charged OP2 algorithm**, label `thm:op2`. These contain
the proof, numerical residual wrapper, and local work ledger, not just a
claim in a commit message. The preceding version explicitly left OP2 open.
The August 30 active manuscript at `49313f3` subsequently restated this
argument. Do not attribute every later safe-output refinement to the
earliest note.

At `0f0ac32`, inspect
`manuscript/notes/deterministic_op2_independent_20260905/original_sources/deterministic_conjecture2.tex.txt`.
The source contains the main exact-real theorem, accelerated comparator
lemma, PageRank-metric projection inequality, response estimate, selected
signed-flow volume bound, repair, continuation schedule, and exact sparse
reporter. The early proof uses mass cap one, volume constant 148, and a
more conservative repair tolerance. The active manuscript uses a tighter
mass cap and refined repair/implementation. These differences must not be
erased by saying that the early snapshot is identical to the final paper.
The original draft's typeset September 5 date is author-supplied; the
commit and hosted evidence are recorded separately above and below.

At `7e1b4e7`, both algorithms and their proofs, including the deterministic
bounded-arithmetic appendix, are present in the active paper. Comparing
this snapshot with the pre-audit tip shows subsequent exposition,
notation, organization, and certificate refinements. The historical
objects and archived files were not edited.

### GitHub-hosted corroboration

Git timestamps alone are insufficient to establish a trusted publication
date. The checked server records provide additional evidence that the
specified objects were already present on GitHub:

- [Workflow 33293616342](https://github.com/baojian/hybrid-local-solver/actions/runs/33293616342), created **2026-08-30 04:57:24 UTC**, names head `f5f999e4b47c3ca28f76428c48ab90d43a72c9d8`; `3fa8455` is its ancestor. This is the earliest such run found in the checked August 29-September 6 window, not an asserted exact push time for `3fa8455`.
- [Workflow 33304804003](https://github.com/baojian/hybrid-local-solver/actions/runs/33304804003), created **2026-08-30 09:44:59 UTC**, names the randomized active-manuscript commit `49313f37bb0354703613c91738fde337944255fe` directly.
- [Pull request 44](https://github.com/baojian/hybrid-local-solver/pull/44), created **2026-09-05 17:04:57 UTC**, records head `0f0ac32d70290f2c6877b4cf1faa7da85e2835ee`; merged **17:07:34 UTC**. [Workflow 33979970723](https://github.com/baojian/hybrid-local-solver/actions/runs/33979970723) records its merge commit one second later.
- [Workflow 34008135248](https://github.com/baojian/hybrid-local-solver/actions/runs/34008135248), created **2026-09-06 03:05:52 UTC**, directly names `7e1b4e77351b361e0c700ce3186c1534d2023f0e`.
- [Workflow 34444811673](https://github.com/baojian/hybrid-local-solver/actions/runs/34444811673), created **2026-09-10 06:21:05 UTC**, names the pre-audit tip `92a9f78bd94a4b7f1058ad1463ef3fbfe6b233fe`.

These workflows have failure conclusions. They corroborate chronology,
**not passing tests or proof correctness**. The checked consolidated commit
is unsigned. GitHub-hosted timestamps are supporting platform evidence,
not independent mathematical certification or a claim that the repository
was public on those dates.

For comparison, the [official competing preprint record](https://arxiv.org/abs/2609.12076v1)
states **2026-09-10 18:05:23 UTC** for v1. The records above support earlier
development of the inspected proofs. They do not establish earlier public
disclosure and do not remove the obligation to cite overlapping work.

## Credential and container inspection

The read-only custom pattern scan covered **8,379 reachable objects**
across all locally available refs, **4,292 text blobs**, and approximately
177 MB of blob content. It checked private-key headers, common service and
GitHub token formats, AWS access-key IDs, credential-bearing URLs, literal
credential assignments, and selected sensitive-identifier phrases. It
reported **no matches**. No blob exceeded its 32 MiB outer-blob limit.

A separate in-memory container pass examined **22 archives**, **1,794
text members**, and extracted text from **87 PDF blobs**, expanding about
123 MB. It reported no matches for its narrower credential patterns.
There were **83 skipped entries** covering binary/nested material,
split archives, and oversized members. LFS pointers were identified, not
treated as the PDF payloads. Neither images nor executable binaries were
certified safe by a text scan. `gitleaks` and `trufflehog` were unavailable;
this is a scoped heuristic audit, not a comprehensive secret-scanner
attestation or a redistribution-rights audit.

Redacted detailed scan inventories remain outside the repository at
`/private/tmp/hybrid-public-release-scan-20260914.json` and
`/private/tmp/hybrid-public-release-container-scan-20260914.json`.
Complete the omitted content checks and permission review before changing
visibility. In particular, absence of a credential-pattern match does not
clear confidential correspondence or author consent.

## Submission readiness

The current scientific comparison and commit-linked development record
are incorporated into the manuscript. The scope and verification results
are in [the manuscript audit](../manuscript/ARXIV_REVIEW_20260914.md).
The proof-identity tests pass; broad repository checks are not all green.
The public repository links will remain inaccessible to unauthenticated
readers until the release hold is resolved. Do not describe the repository
as publicly available in an arXiv submission while it remains private.
