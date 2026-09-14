# Optional adaptive package transcription and focused checks

**Passed.** The package adds `_adaptive.py` and the named `solve_adaptive`
export. `solve` remains the identical `solve_fast` function. The optional
export was added only after the independent implementation audit in
`adaptive_source_implementation_independent_audit.md` passed for the exact
source snapshot below. No existing numerical module or finalizer was
modified, and no final wheel was rebuilt.

## Exact transcription

`build_adaptive_solver_package.py` parses the complete source module and
relocates exactly six imports:

| Research source | Package destination |
| --- | --- |
| `combined_certified_dyadic_rppr` | `._combined` |
| `direct_exception_integer_rppr` | `._direct` |
| `deterministic_avl_containers` | `._avl` |
| `deterministic_rppr_solver` | `._types` |
| `integer_dyadic_rppr_solver` | `._integer` |
| `practical_dyadic_rppr_solver` | `.solver` |

All imported names remain the same. Reversing these six relocations makes
the entire module AST identical, including every class body, default,
dataclass field, function body and corrector dispatch. There is no wrapper
code extraction or `FunctionType` substitution in this transcription.
`ADAPTIVE_TRANSCRIPTION.json` records the changes and snapshots all
preexisting module hashes.

- Research source SHA-256:
  `af33cb41872eb834aeabb14f5ec5cc1a45cda7400482884da5576e0358c633ea`.
- Packaged `_adaptive.py` SHA-256:
  `76d302149c5a6ffb859ee850d6b5ef497e2a89d38377ad43945589e7ec9ff51b`.

The builder itself does not edit exports. After independent audit approval,
`__init__.py` received only the optional function import and its `__all__`
entry. All 17 preexisting non-initializer modules still match their hashes
recorded before packaging. Root's finalizer may subsequently include the
adaptive result/metrics classes among the final named exports and refresh
the current package manifest; this audit has not modified that finalizer.

## Source/package and isolation evidence

`audit_adaptive_package.py` produces `adaptive_package_verification.json`
with both `passed=true` and `successful=true`. Six source/package calls
match by their complete recursively materialized dataclass records, not
just the final output. They cover 12 stages, rational stage jumps, final
clamps, an actual zero-iteration stage, alpha-one and zero direct branches,
and a singleton-support problem adjoining a degree-`10^30` inactive hub.
Actual degree/row sequences and entry counts match too. All fixtures use
integer labels whose hash operation raises. The hub's row is forbidden and
never read. Independent sparse certificates pass for every final output.

The isolation check copies only the package directory and starts a fresh
Python process using `-I -S -B`, working directory `/`, and only the copied
package added to its import path. Research module imports are additionally
guarded against. Its four-stage adaptive path solve, extra source scans,
and independent objective-gap certificate pass with hash-forbidden large
labels. Thus the relative import boundary is exercised without research
files available as implementation dependencies.

## Self-contained package checks and documentation

`tests/test_adaptive.py` adds four focused groups covering dense exact KKT
stage comparisons, adaptive source maxima and clamping, separate external
query accounting, zero-step terminal repair, direct branches, fresh/cached
source-helper behavior, and a huge inactive boundary with no hashing.
All four groups pass using:

```
python3 -B -m unittest tests.test_adaptive -v
```

During test preparation, the independent verifier's test oracle initially
treated only the seed as a supplied vertex. The verifier also receives all
output vertex identifiers as inputs. Initializing that test oracle's known
set with these output labels resolved the harness assertion; no solver or
certificate implementation changed.

`examples/adaptive_path.py` runs independently from the package source tree.
Its billion-vertex virtual path uses four adaptive stages and 56 correction
iterations; it reports 15 additional retained-row source scans separately
from the inner result. Its independent certificate is below the requested
`1/1000000`. This is an example execution, not a timing comparison.

The README documents `outer.result`, `outer.adaptive_metrics`, the exact
schedule records and convenience output properties. It explicitly says
to add the adaptive ledger to the unchanged inner ledgers, explains the
different stage path and possible different output, and states that the
internal terminal source helper may extend caches without updating an old
reporter, so that corrector must not be resumed afterward. The public
wrapper respects this automatically.

The default remains fast with the halving schedule. The adaptive option
has the same proved guarantees but no claim of uniform speed improvement;
the separately performed paired study included a slower grid fixture.
The broad stable/183-case suites were not rerun for this additive import
boundary, and wheel rebuilding is deferred until package finalization.
