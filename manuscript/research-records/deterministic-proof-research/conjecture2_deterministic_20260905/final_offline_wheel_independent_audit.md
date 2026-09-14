# Final offline wheel audit

The finalized 20-module distribution passed build, archive, installed-file, and isolated-example checks. No packaging defect was found. This audit is separate from the historical 18-module `distribution_readiness/` artifacts, which remain untouched.

## Exact snapshot and runtime

- Manifest: `deliverables/deterministic-rppr/PACKAGE_MANIFEST.json`, SHA256 `27a637c3e569a78a2775c20f824b98134be5754b28072a92f8ce9c27770cdc30`.
- Wheel: `distribution_final/wheels/deterministic_rppr-0.1.0-py3-none-any.whl`, 45,923 bytes, SHA256 `536d1b99a9855388b10f2be6294b98ce328955ba3ddc4610734142169d437437`.
- Existing runtime: `/Users/baojian/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`, Python 3.12.14, setuptools 84.0.0, wheel 0.48.0, pip 26.2.1.
- Reproducible driver: `audit_final_offline_wheel.py`; results: `final_offline_wheel_independent_verification.json` and the identical `distribution_final/verification.json`.

The driver first verifies every current manifest module hash and every referenced validation-artifact hash. It copies only the 20 modules, unchanged project metadata, and README into a clean build directory. The package source, metadata, examples, and manifest are rechecked after all operations. The finalizer, numerical modules, and global Python installation were not changed.

## Offline commands

The exact argv arrays, working directories, return codes, and wall times are saved in the verification JSON. With `PYTHON` denoting the runtime above and `FINAL` denoting the absolute `distribution_final/` path, the operations were:

```text
cd FINAL/build_source
PYTHON -m pip wheel --no-deps --no-build-isolation --no-index . -w FINAL/wheels

cd FINAL
PYTHON -m pip install --no-deps --no-index --no-compile --target FINAL/installed FINAL/wheels/deterministic_rppr-0.1.0-py3-none-any.whl

cd /
PYTHON -I -S -B FINAL/isolated_example_runner.py FINAL/installed FINAL/isolated_examples
```

The environment disables pip indexes, pip version checks, pip configuration files, and cache use; build isolation and dependency resolution are disabled. The only build tools used were already installed. `SOURCE_DATE_EPOCH=315532800` fixes archive timestamps. No network request or global installation is part of this procedure. Build and install logs are retained in the fresh audit directory.

## Distribution inspection

The archive contains exactly the 20 manifest Python files plus `METADATA`, `WHEEL`, `top_level.txt`, and `RECORD`. Every Python file matches its manifest hash. All 23 non-self wheel `RECORD` hashes and lengths match, with no duplicate or missing records. After local-target installation, all 20 module hashes still match; all 26 non-self installed `RECORD` hashes and lengths match, including pip's installation metadata. Every installed-record path resolves inside the local target.

Metadata declares `deterministic-rppr` version `0.1.0`, Python `>=3.10`, no runtime dependencies, and a pure-Python `py3-none-any` wheel. No tests or research modules are unexpectedly bundled. No installed bytecode files were generated. This execution audit covers Python 3.12.14; the metadata's broader Python-version claim is not a cross-version test result.

## Isolated examples

The examples are unchanged copies of the four public package examples. A fresh subprocess starts in `/` with `-I -S -B`. Its absolute imports permit only the Python standard library and `deterministic_rppr`; all 20 loaded package module origins must resolve into the locally installed wheel. The copied examples cannot import any research implementation. The default binding is checked as `solve is solve_fast`, from `deterministic_rppr._fast`.

| Example | Output records | Correction steps | External degrees | External adjacency entries | Independent certificate |
|---|---:|---:|---:|---:|---|
| `path.py` | 2 | 48 | 9 | 7 | Pass, gap below `10^-6` |
| `star.py` | 1 | exact singleton | 2 | 1 | Exact zero gap |
| `adaptive_path.py` | 5 | 56 | 20 | 26 | Pass, gap below `10^-6` |
| `mass_grid_path.py` | 4 | 48 | 21 | 22 | Pass, gap below `10^-6` |

The adaptive example records its additional 15 cached source adjacency visits separately, with zero additional external degree replies. The mass-grid example records 10 additional incoming-baseline records and 10 cached degree lookups. Full outputs, exact rational certificates, stage parameters, grids, and additive ledgers are retained in the JSON rather than replaced by decimal approximations. Independent certificate adjacency visits are recorded separately from solver work.

This is a bounded distribution-readiness audit. It confirms the final wheel contains the audited source snapshot and executes all four public examples without the research files. It does not substitute for the mathematical proof, independent component audits, or broader graph-case validation already recorded by the final manifest.
