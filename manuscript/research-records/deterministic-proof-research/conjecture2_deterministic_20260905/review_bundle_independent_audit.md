# Independent final review-bundle audit

The corrected final bundle passed. No unresolved defect remains in the audited integrity, navigation, provenance, or extracted data/help checks.

- Archive: `deliverables/conjecture2_proof_and_solver.zip`, 2,172,725 bytes.
- SHA256: `ed47aa350f4e42d7683040aea98b777ac4e479a1260b6e67d28a71740ed1fd6b`.
- Bundle manifest SHA256: `fa11ac4235c6adde7f38de74bd258e2ca626fdf361f7a72b466a7bbe176ccbf6`.
- Auditor: `audit_review_bundle.py`.
- Detailed results: `review_bundle_independent_audit.json`; extracted copy and command logs: `review_bundle_final_audit/`.

## Integrity and packaging

The archive has 108 regular files: 107 artifacts covered by `BUNDLE_MANIFEST.json`, plus the manifest itself. All recorded byte counts and SHA256 values match; every ZIP CRC passes; the ZIP, final source-bundle directory, and freshly extracted files are byte-identical. The uncompressed total is 18,243,300 bytes.

All archive paths have the single expected bundle prefix, contain no traversal, absolute paths, backslashes, colon ambiguity, or NUL, and have no duplicate or case-insensitive-colliding names. There are no symlinks, encrypted entries, or nonregular entries. Extraction was performed only after these checks, into the new audit directory. Manifest provenance points only to the fresh research directory or the explicitly generated start document; the original manuscript source was not copied into the bundle.

The bundled package manifest equals the current finalized package manifest. Its 20 numerical/library module hashes and all 7 referenced validation-artifact hashes match the current sources and included evidence. The default is still `solve_fast`. The bundled wheel has SHA256 `536d1b99a9855388b10f2be6294b98ce328955ba3ddc4610734142169d437437`, identical to the independently audited final wheel. Its exact 20 Python modules match the source package, and all 23 non-self `RECORD` checksums and lengths pass. No library, wheel, or bundle content was edited by this auditor.

## Proof and navigation

The three TeX files match both their current source hashes and the compile manifest. The main TeX includes exactly the two adjacent appendix files. The PDF matches the compilation and visual-review manifests: SHA256 `4780f6a3edaa015afa52f5f790e8f6969d4b9068bd6088b7f0f9a58b462b6e20`, 426,555 bytes, and 20 pages. The fresh research compile log matches its recorded hash, and all 20 rendered-page hashes match `proof_visual_review.json`.

This last check verifies provenance of the already compiled and visually reviewed artifact; it is not a new compilation or a second visual-quality judgment. The bulky compile log and rendered pages need not be present in the review ZIP to read the included PDF and its recorded audit.

All 31 explicit Markdown file links resolve within the extracted bundle, including the start document, proof-to-code map, and worked figure. All 35 mathematical labels referenced by the proof-to-code map exist in the included TeX. The start document distinguishes historical research-workspace reproduction commands from the bundled portable validation and benchmark commands. Historical evidence references therefore do not masquerade as runtime dependencies.

One actual portability defect was found in the original `conjecture2_review_bundle.zip` (SHA256 `088c006e6f3812c41a02c696bd009f48042664b903c03cbf802365121559b3a2`): the worked-example Markdown used an absolute research path for its image. Root changed the source link to `worked_three_vertex_example.png` and generated the final archive under a new name. This audit verified the relative link and adjacent PNG in the final bundle, and verified that the original archive remains unchanged. The defect and its resolution are preserved in the JSON history.

## Extracted commands only

Using the already installed bundled Python 3.12.14, a subprocess launched from `/` with `-I -S -B` ran:

```text
validation/run_full.py --check-data --output <audit-directory>/manifest-check.json
validation/run_full.py --help
benchmarks/run.py --help
```

The wrapper allowed only standard-library imports plus the extracted `deterministic_rppr` and bundled `tests` package. All imported package/test origins were checked inside the extraction. A profile guard rejected any numerical `solve_*` or `step` call. All three commands exited successfully.

The data-only result is `data_verified`, with the expected 183-case canonical manifest SHA256 `e02485273de4bc1b615530518ac9db60ae5d7beee0140e0e787f6f4320ed0434`, unchanged before/after source hashes, an empty completed-case list, and **zero solver cases run**. No solver test suite or timing study was repeated. This audit checks the review delivery and its standalone entry points; the mathematical argument and earlier exact implementation validations retain their separately stated scope.
