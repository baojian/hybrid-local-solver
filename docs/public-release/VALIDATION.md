# Public release validation

Date: September 14, 2026. This record covers the filtered release copy and the current manuscript edits supplied in the author's working tree. No numerical solver, proof claim, reported experiment, or test expectation was changed by release preparation.

## History and disclosure checks

- 505 original research commits retained; 235 historical paths excluded with a reason for each.
- Author/committer identity and date fields, full messages, all parent relationships, and retained file contents/modes verified against the originals. Empty commits are retained. Original signatures on 43 commits cannot be preserved after filtering.
- Full commit mapping and an explicit exclusion inventory accompany the release.
- 1,010 original research text files exported from four archives; each exported payload is checked against its original member SHA-256. The manifest documents 97 omitted members. Original opaque bundles and raw-result archives remain private.
- Downloaded source papers, imported publication workspaces, reviewer correspondence, private hosted discussions/logs, and LFS payloads are not transferred.
- Gitleaks 8.30.1 scans the retained history and working tree. The initial 34 history and 33 working-tree findings are bibliographic citation labels, reviewed in `secret-scan-review.json`; no confirmed credentials were found in those scans. Final scan results are recorded alongside the history verification report.

## Build and repository checks

| Check | Result |
| --- | --- |
| `make agent-audit` | Passed |
| Reconstructed portable solver excerpt | All 17 original tests passed |
| `make test` | 229 passed, 5 failed; same failures as the pre-release audit |
| `make lint` | Two existing diagnostics; the formatting stage is not reached because `ruff check` fails |
| `make note-audit` | Two existing oversized note sections |
| `make paper` | Passed; 50-page PDF, with no undefined references/citations or overfull boxes in the final LaTeX log |

The five test failures concern the active paper's shared-model import count, a table-local LaTeX declaration, a research note's regularizer alias, and two checks of oversized research-note sections. They are not numerical proof-identity failures. The lint diagnostics are the unused `pagerank_matrix` import in `verify_exact_batch_cholesky.py` and a lambda assignment in `green_band_stress_exact.py`. The 1,237-line and 4,361-line sections remain intact rather than being reorganized during disclosure preparation.

The required checks were run in the filtered checkout with the existing locked Python environment. No test was removed, skipped, weakened, or marked expected-failure to make the release appear clean. A green status is not claimed. Passing finite computational checks does not establish a theorem or constitute external peer review.

The original repository, its old GitHub records, and all private backups must remain private. The replacement is prepared for the author to change visibility in GitHub; readiness of this copy does not clear the original repository for public disclosure.

The final pre-commit scan of the filtered history reported 34 bibliographic-label matches; the working-tree scan reported 33. Each was individually classified, with no confirmed credentials. The four retained PNG figures were visually inspected; they contain research plots. The two corresponding PDF figures were retained unchanged. The updated development-record page was visually checked after compilation.

The release-preparation commit `01d0801` was scanned separately after committing. Its single scanner match was another explicit citation key; no confirmed credentials were found. The exact commit and classification are recorded in `release-commit-scan-review.json`. The Git object-integrity check passed; no excluded historical paths or LFS pointer blobs were reachable.

A fresh GitHub clone caught six text package-metadata files omitted by the repository-wide `*.egg-info/` ignore rule. Their exported bytes were verified against the research-record manifest and explicitly added. This keeps all 1,010 declared exported payloads present in the Git checkout.
