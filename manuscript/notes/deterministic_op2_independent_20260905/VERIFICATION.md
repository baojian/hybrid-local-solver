# Repository integration verification

Date: 2026-09-06. Base commit: `e83d996e7e61534ba5f3724ea3df3e25778a7ba9`.

## Passed for this note

- The new overview compiled to six pages; the final build has no overfull,
  underfull, or unresolved-reference warning. All six rendered pages were
  visually inspected.
- Four note-only notation checks passed: shared declarations, core-definition
  reuse, seed/accuracy names, and semantic aliases.
- The note registry contains the new entry and dependency, and the generated
  index is synchronized. The note has a complete status handoff and build rule.
- The coordination audit passed.
- All 736 retained research-archive files match their original SHA-256 hashes.
  The manifest records 456 exclusions: bytecode caches, downloaded reference
  copies, and duplicate extracted bundles. No substantive original root-level
  research file is omitted.
- The portable 108-file ZIP passed CRC and safe-path checks. Its hash and the
  original 20-page proof hash are unchanged. Three browsable original TeX
  sources are byte-identical copies; only their filename suffix differs.

## Repository-wide baseline failures

`make test` ran all 213 tests: 209 passed and four failed. A focused rerun after
correcting this note's initial notation warning left only existing failures:

- `test_reserved_seed_and_accuracy_names_do_not_regress`: seed notation in
  `manuscript/sections/related_work.tex`.
- `test_known_semantic_aliases_do_not_regress`: an existing regularizer alias in
  `aesp_cd_l1_rppr/sections/body/02_eq_aesp_cd_target.tex`.
- The inventory audit and source-size test: two existing sections in
  `aesp_cd_l1_rppr` exceed the 1,000-line limit (1,237 and 4,361 lines).

`make note-audit` reports those same two source-size violations. The new note
passes its registration, status, dependency, and size checks.

`make lint` reports two pre-existing Python issues: an unused import in
`problem_definitions/verify_exact_batch_cholesky.py` and a lambda assignment in
`spectral_balance_threshold_batch/green_band_stress_exact.py`. The separately
run format check reports 101 existing files needing formatting. This change
adds no active Python files. The cited failure-source files are byte-identical
to the base commit, as recorded in `FOCUSED_VERIFICATION.json`.

These unrelated files were preserved. The branch is saved for review; this
record does not claim that the complete repository test or lint suite passed.
Original numerical results were archived unchanged rather than regenerated.
