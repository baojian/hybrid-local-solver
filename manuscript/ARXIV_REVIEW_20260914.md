> Historical pre-release record. The original private repository remains subject to the hold described below. The replacement public-history copy excludes the uncleared materials; see [the release guide](../docs/public-release/README.md) for its current scope and validation.

# Manuscript proof, chronology, and publication audit

Date: September 14, 2026. Starting manuscript commit:
`92a9f78bd94a4b7f1058ad1463ef3fbfe6b233fe`.
This record supplements, rather than rewrites, the September 6-10 audits.

## Findings and disposition

1. **Novelty framing required correction.** Cui--Wei--Yang,
   arXiv:2609.12076v1, directly overlaps the randomized accelerated RPPR
   theorem. Its proof also implies the support-adaptive minimum. The
   abstract, introduction, comparison table, detailed related work, and
   conclusion now emphasize deterministic polylog-only acceleration and
   distinguish proof mechanisms without claiming randomized exclusivity.
2. **Earlier development is supported, not earlier public disclosure.**
   Historical proof text was inspected at `3fa8455` and `0f0ac32`;
   GitHub-hosted run/PR records corroborate their existence before the
   competing preprint. The manuscript now links the complete hashes and
   distinguishes original proofs from subsequent refinements.
3. **No fatal mathematical gap was identified in this review of the
   active theorem chain.** This is a manual audit plus finite checks,
   not a machine-checked proof, external peer review, or assurance that
   every exploratory note is correct.
4. **Public-release clearance is incomplete.** Archived reviews/rebuttals,
   source-paper redistribution, author consent, and omitted history/log
   content require clearance. The repository remains private by design.
5. **Repository-wide checks have pre-existing failures.** The baseline
   suite reports 229 passed, 5 failed; lint reports two existing errors.
   No failing test was removed or weakened and no research-note history
   was rewritten to manufacture a clean result.

## Active proof chain examined

| Component | Checked reasoning and important boundary |
| --- | --- |
| Problem and obstacle geometry | Lazy/non-lazy mapping; nonnegativity; least-supersolution order; original-degree mass and support volume; bias and objective-to-PPR conversion |
| Deterministic correction domain | Both analytical comparators are feasible; residual source is diffuse; continuation does not assume an exact old optimum |
| Accelerated comparison | Squared-distance identity and gradient cancellation; comparator need not minimize the auxiliary quadratic |
| PageRank-metric projection | Lower/upper normal signs and the mass-normal pairing; no general matrix-metric nonexpansiveness claim is used |
| Second energy | Initial diffuse-source energy and the squared-response constant 18; potentially negative comparison energy is handled correctly |
| Local work | Selected signed forcing, rather than all positive forcing; telescoping and weighted Cauchy--Schwarz; repeated kinetic scans included |
| Sparse implementation | Shared scale, response keys, source/kinetic exceptions, box/mass threshold search, discovery and final materialization charges |
| Bounded arithmetic | Downward errors, neighbor-record rebase induction, closed-tail enumeration, grid tolerances, coefficient encodings, and final safe repair |
| Randomized depth | Stieltjes Cholesky signs; inverse ordering; block-row norm bound; spectrum in [alpha,2]; causal forcing; Chebyshev propagation and threshold floor |
| Randomized numerical wrapper | Energy-to-residual conversion, deterministic acceptance, boundary-error threshold, empty/capped stopping cases, orthant repair and fresh retries |
| Source solver import | Koutis--Miller--Peng PDF pp. 10-11: Lemma 4.5 and Theorem 4.6; supplied-matrix expected work is distinct from local discovery |
| PPR consequences | ACL residual representation, degree-normalized error, approximate-envelope comparison, CG and certified-SDD completion, trivial branches |
| Seed and flow appendices | Explicit source-input costs, randomized initial block, deterministic repeated source refreshes, mixture budget, and grounded-flow dual signs |

The exact-real and specified bounded-arithmetic algorithms must not be
identified with arbitrary floating-point code. The standalone AESP--LOCSOR
universal locality gate remains open and is not a dependency of these
manuscript theorems. No solver implementation, mathematical convention,
or reported experiment was changed in this update.

## Baseline verification performed

- `make agent-audit`: passed.
- `make test`: **229 passed, 5 failed**; all **21** tests in
  `tests/test_arxiv_proof_identities.py` passed.
- `make lint`: two existing diagnostics: unused `pagerank_matrix` import
  in `manuscript/notes/problem_definitions/verify_exact_batch_cholesky.py`,
  and assigned lambda in
  `manuscript/notes/spectral_balance_threshold_batch/green_band_stress_exact.py`.
- Three failing tests concern manuscript/shared-notation rules: the active
  paper's inlined model, a table-local `arraystretch` declaration, and a
  regularizer alias in the AESP--CD research note. Two failures concern
  oversized research-note sections. These are not failed numerical proof
  identities, but they remain repository acceptance failures.
- GitHub's latest workflow fails at the note-registry check, before its
  test and lint steps. A failed workflow is used only as chronology
  evidence, never as a successful proof check.

The first local check attempt was blocked by sandbox access to the existing
uv cache; the results above are from the authorized rerun. Detailed logs
are `/private/tmp/hybrid-release-agent-audit.log`,
`/private/tmp/hybrid-release-tests.log`, and
`/private/tmp/hybrid-release-lint.log`.

## Publication evidence and remaining gate

See [the September literature comparison](../docs/literature/publication-review-20260914.md)
for source PDF pointers and normalization, and
[the release audit](../docs/public-release-audit-20260914.md) for exact
commit links, hosted timestamps, and permission checks.

Preserve all historical commits. Before describing this as a publicly
available repository or declaring an unconditional submission-ready
release, clear the disclosure/redistribution questions and address or
explicitly accept the remaining repository-check failures. The author
retains final responsibility for the theorem statements and submission.
