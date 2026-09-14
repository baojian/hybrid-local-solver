# Portable validation artifact audit

**Passed.** The standalone source bundle now contains `validation/cases.json`,
`validation/run_full.py`, and `validation/README.md`. Numerical modules, existing
tests, and the default backend are unchanged.

The case data exactly equals the existing serialized `make_manifest()` output
and the manifest saved with the independent adaptive integration run. Its
canonical SHA-256 is
`e02485273de4bc1b615530518ac9db60ae5d7beee0140e0e787f6f4320ed0434`, identical to
the saved fast validation. The on-disk JSON hash differs only because it includes
intentional readable formatting; both identities are recorded in the audit JSON.

The new runner imports only the bundled package, bundled independent
`tests.test_solver` KKT/objective/source helpers, and the standard library. It
contains no research path or manifest-generator import. Its exact problem/oracle
helpers, serializer, source observer, and alarm handler have matching ASTs with
the independently completed adaptive validator. The wrapper checks branch
explicitly: fast uses `max(rho, previous_r/2)`, while adaptive uses the exact full
source maximum and its separate additional ledger. Both preserve the original
objective target; no cross-backend output equality is assumed.

Read-only transcription checks used the new manifest parser and problem helpers
to verify **366 saved final outputs** (183 per backend) and **344 saved adaptive
stages**, including exact source maxima and actual candidate/repaired gaps.
There was no full-suite solver rerun.

For the new import/parser/CLI boundary only, a temporary standalone directory
contained copies of just `deterministic_rppr/`, `tests/`, and `validation/`.
Python `-I` ran the fixed five-case smoke subset once per backend: **10 complete
smoke solver cases** total. These passed and matched their respective already
saved backend outputs; the adaptive smoke records matched all saved result
fields. The subset includes label/reversed-row invariance, both direct branches,
and the analytic million-leaf star. A separate forced guard test completed zero
solver cases and executed zero numerical steps; it saved `status: incomplete`
and a nonzero process exit as required.

The five-case smoke is explicitly marked `complete_subset`, with
`full_manifest_completed: false`. The complete CLI uses `complete`; failures and
guards preserve completed records with `incomplete`. The evidence records fixed
resource guards, runtime and source hashes, full outputs/stages/candidates,
independent exact checks, and local ledgers. No new timing comparison is claimed.

From the unpacked source bundle, users can run the full suite with:

```sh
python3 -I validation/run_full.py --backend fast --output fast-validation.json
python3 -I validation/run_full.py --backend adaptive --output adaptive-validation.json
```

Adding `--smoke` runs only the five-case subset. `--check-data` validates the
manifest/parser without running a solver. The adjacent validation README explains
the computational checks, exact fraction format, guards, and output statuses.

Reproducibility artifacts in the research directory are
`audit_portable_validation.py`, `portable_validation_transcription_audit.json`,
`portable_validation_fast_smoke.json`, `portable_validation_adaptive_smoke.json`,
and `portable_validation_forced_guard.json`. The audit JSON records matching
before/after hashes of all bundled numerical Python modules and existing tests.
