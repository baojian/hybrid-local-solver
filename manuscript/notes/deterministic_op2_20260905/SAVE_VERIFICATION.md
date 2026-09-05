# Repository archive verification

Saved on 2026-09-06. The original mathematical/experimental checks remain in
VERIFICATION.md; this record concerns faithful storage and independent reuse.

No historical experiment result is changed or relabeled by this import.

## Successful checks

- The standalone `main.tex` builds to a 10-page PDF with the shared preamble.
  Final compilation has no overfull/underfull boxes or unresolved references.
  All ten rendered pages were visually inspected for layout and clipping.
- All 448 archived source/evidence members were read and checked against the
  manifest: 504,508,899 uncompressed bytes. Every archive and split-part
  SHA-256 and ZIP CRC check passed. Archive 08 was reassembled in memory for
  verification. Every saved file is below 10 MB.
- `proof-audit.pdf` and `archive/solver-package.zip` are byte-identical to the
  original report and portable package. The original source workspace remains
  intact. Third-party downloads, environments and redundant build copies are
  explicitly excluded in the manifest.
- The portable archive was extracted outside the repository. Its
  `python -m unittest discover -s tests -v` rerun passed all 17 tests
  (Python 3.13.13, 0.305 seconds). Full output: `PORTABLE_TEST_RERUN.txt`.
- `git diff --check` passed. The direction has its own registry entry,
  README, status, Makefile, four section sources and shared notation import.
- `make agent-audit` passed during the initial save verification.

## Existing or concurrent broader-check failures

The broader checks are not claimed to pass. Their failures do not originate
in this note, and other directions were not modified to hide them.

- Initial notation/inventory test run: 23 passed, 4 failed. Existing causes:
  unit-seed `e_s` in `manuscript/sections/related_work.tex`; reserved
  regularizer alias in `aesp_cd_l1_rppr/sections/body/02_eq_aesp_cd_target.tex`;
  and two sources over the 1,000-line inventory limit:
  `06b_prop_aesp_cd_dynamic_reporters.tex` (1,237 lines) and
  `06d_cor_aesp_cd_obstacle_primitives.tex` (4,361 lines), both in that
  direction's `sections/body/`. These files were verified unchanged from HEAD.
- During final verification, a concurrent directory named
  `deterministic_op2_independent_20260905` appeared without a registry entry.
  The final test snapshot therefore reported 22 passed, 5 failed: the same
  existing causes plus that registry mismatch. This concurrent directory was
  left untouched. The inventory reported no issue in this note's files.
- Existing repository lint failures: an unused import in
  `problem_definitions/verify_exact_batch_cholesky.py` and an assigned lambda
  in `spectral_balance_threshold_batch/green_band_stress_exact.py`.
  The global format check also reports 101 existing files requiring formatting.
  This save adds no live Python implementation; solver code is archived intact.

The checks establish reproducible storage and successful compilation, not
formal verification of the theorem or a practical speed advantage over FISTA.
