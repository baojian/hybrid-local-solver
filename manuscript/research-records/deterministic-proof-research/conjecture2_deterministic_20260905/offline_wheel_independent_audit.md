# Offline distribution readiness audit

**Passed.** The failed Homebrew build was an unavailable build-backend
dependency in that interpreter. The existing package metadata builds
successfully using an already installed bundled runtime. No metadata,
numerical module, or source material was changed, and no network access or
global installation was used.

## Build runtime and artifact

Runtime:
`/Users/baojian/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`

Installed versions: Python 3.12.14, setuptools 84.0.0, wheel 0.48.0, and
pip 26.2.1. All were present before this task.

Wheel:
`distribution_readiness/wheels/deterministic_rppr-0.1.0-py3-none-any.whl`

Size: 39,328 bytes. SHA-256:
`8e01540737c1fc8510985c7bac2252daccfe2bd0f64683054fe6bfb32678daed`.

The build used a clean copy of the 18 modules listed in the current
`PACKAGE_MANIFEST.json`, plus the unchanged `pyproject.toml` and README.
This keeps generated egg-info and build files out of the deliverable source
directory. The checked manifest snapshot SHA-256 is
`740a72ee452110a5bdb5b2a9e5a9399852806877b048cab1f46eb5dc05ef42e9`.
The manifest and every original module were rechecked unchanged afterward.

## Exact operations

The reproducible driver is `audit_offline_wheel.py`. It records complete
absolute argument vectors and working directories in
`offline_wheel_independent_verification.json`. The three substantive
commands were, using the runtime above as `PYTHON`:

```
PYTHON -m pip wheel --no-deps --no-build-isolation --no-index . -w WHEEL_DIRECTORY
PYTHON -m pip install --no-deps --no-index --no-compile --target ISOLATED_DIRECTORY WHEEL_FILE
PYTHON -I -S -B ISOLATED_RUNNER ISOLATED_DIRECTORY COPIED_EXAMPLES_DIRECTORY
```

The build command ran in `distribution_readiness/build_source`, the target
installation command in `distribution_readiness`, and the last command
with working directory `/`. The environment additionally set
`PIP_NO_INDEX=1`, `PIP_DISABLE_PIP_VERSION_CHECK=1`, and
`SOURCE_DATE_EPOCH=315532800`. The latter fixes wheel timestamps; no claim
of cross-toolchain byte-for-byte reproducibility is needed here.

The driver preserves its artifact directory and refuses to overwrite an
existing installation or wheel directory. For a repeat build, use a fresh
scratch artifact directory. Full build/install/example logs are retained
under `distribution_readiness/`.

## Contents and installation checks

The wheel contains exactly the 18 manifest-listed Python modules and four
standard distribution metadata files: `METADATA`, `WHEEL`, `top_level.txt`,
and `RECORD`. Every module's bytes match the current manifest. All 21
hashed `RECORD` entries have the correct SHA-256 and size; `RECORD` itself
has the standard empty self-hash/size. There are no extra Python modules,
compiled extensions, research imports, tests, or build artifacts in the
wheel.

Metadata identifies `deterministic-rppr` version `0.1.0`, Python `>=3.10`,
no runtime dependencies, and the pure-Python tag `py3-none-any`. The wheel
is the installable library; examples, proof documents, validation reports,
and manifests remain in the accompanying source deliverable. Their absence
from the library wheel is expected under the current package configuration.

Installation went only into the audit's isolated target directory. Its
18 installed module hashes match the wheel and source manifest. Pip added
only its normal installation metadata (`INSTALLER`, `REQUESTED`, and
`direct_url.json`, with an updated installed `RECORD`). No global site
packages were modified.

## Isolated example results

The examples were copied to a separate directory. The fresh process used
`-I -S -B`, explicitly added only the isolated installed library location,
and rejected known research-source import names. After running both
examples, every imported `deterministic_rppr` module was asserted to reside
inside the installed target. Neither the original source package nor the
research modules supplied executable solver code.

- The billion-vertex path example completed 48 correction iterations,
  returned two density records, and used nine degree replies and seven
  first adjacency entries. Its independent objective-gap bound was
  `415034168512853483/12089258196146291747061760`, below `1/1000000`.
- The billion-leaf star example returned the exact singleton density
  `63/3232` at its leaf seed. It used two degree replies and one adjacency
  entry, and its independent objective-gap certificate was exactly zero.

These are installation and readiness checks on Python 3.12.14, not a new
runtime benchmark or a test of every supported Python version. No packaging
defect or necessary metadata fix was found.
