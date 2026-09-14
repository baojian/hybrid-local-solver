# Independent audit of the standalone acceleration transcription

Result: **no defect found** in the current standalone package's `_binomial`, `_early_stop`, `_combined`, and revised `_certificate` modules. The optional exports `solve_binomial`, `solve_early_stop`, and `solve_combined` match their audited research implementations on the bounded exact cases. The package default remains `solve_source_energy` at this audit snapshot.

The audit script is `audit_accelerated_package.py`; exact results are in `accelerated_package_independent_verification.json`. Package sources were read only. The broader 183-case manifest was deliberately not rerun.

## Independent transcription checks

The audit first verifies all five package hashes in `ACCELERATED_TRANSCRIPTION.json`, together with the four source hashes. It then parses both versions and reverses only the documented changes, independently of the builder:

1. Package-relative imports are mapped back to their authorized research-module names. The obsolete `FunctionType` import and isolated-wrapper namespace assignments are removed from the research comparison.
2. Each package wrapper is required to make exactly the corresponding call to `solve_rppr_integer(..., corrector_class=...)`. Its preserved docstring and all other syntax are checked. The three corrector classes are respectively `BinomialBlockDyadicCorrector`, `EarlyStopSourceEnergyCorrector`, and `CombinedDyadicCorrector`.
3. The certificate function has exactly two new keyword-only arguments, `_map_factory=AVLMap` and `_set_factory=AVLSet`. Exactly five map constructor calls and one set constructor call are restored for comparison; no arithmetic, branch, validation, or result expression is changed.
4. The package metered checker retains both nested AVL classes identically at the AST level. Its new forwarding function must pass those exact factories to the independent certificate and then return the function. Only this explicitly checked forwarding code replaces the former cloned namespace.

After those changes are reversed, the complete ASTs of all four modules agree. This comparison includes class bodies, constants, decorators, stopping inequalities, bound invalidation, cleanup paths, schedules, arithmetic expressions, and result fields; it is not merely a list of matching function names.

The audit also checks the preexisting package `_integer.solve_rppr_integer` class-injection interface independently. Removing its one keyword-only class parameter and restoring its single class-construction call yields the exact original continuation AST. Consequently the new wrappers reuse the same special cases, baseline schedule, terminal PG/grid repair, summaries, and output behavior.

## Explicit factories and deterministic containers

The certificate's normal path still constructs the package AVL maps and set. The metered path passes the unchanged `MeteredMap` and `MeteredSet`, including the set's internally metered map, through explicit factories. The six temporary map instances and their reclamation retain the original counters and semantics. Defaults are evaluated from the package's own AVL imports; no research-module globals or dynamically cloned functions are required.

The private factory arguments permit instrumentation. The deterministic complexity claim applies to the default AVL factories and the package's metered AVL factories; it is not a promise about an arbitrary caller-supplied data structure. This is an interface scope observation, not a defect in the supported package paths.

The three new acceleration modules add only fixed-size scalar state, counters, and class/function bindings. They do not introduce a new graph-indexed hash container. Existing graph state, reporter records, and independent-checker temporary maps retain the audited AVL implementations. Fixed string-key diagnostic dictionaries remain separate from graph-indexed state.

## Exact behavioral checks

All three package backends were compared with their respective research backends. The audit compares the complete `asdict` result, including exact outputs, certificates, every stage field, continuation metrics, checkpoint metering, and source/binomial diagnostics. It also compares the exact sequence of external degree and adjacency queries.

The bounded study passed:

- 18 complete backend comparisons and 54 stage comparisons.
- 81 checkpoint events with matching metered factory/reclamation counts and zero cache misses.
- Two genuine fallback stages after rejected checkpoints.
- Three positive-error zero-iteration stages and the zero-solution special branch.
- Three alpha=1 direct solves with no adjacency queries.
- All 18 comparisons using integer label objects whose `__hash__` raises.

Fixtures include a five-vertex path with alpha=1/100, an asymmetric cyclic graph with alpha=13/97, labels exceeding 2,048 bits in magnitude, and a billion-degree hub boundary. The hub oracle asserts if the hub row is requested; all three package backends scan only the leaf row and match the research source exactly. Each final package output also passes its independently recomputed norm certificate at the requested tolerance.

These are meaningful transcription checks, not another broad algorithmic benchmark. They complement the existing exact trajectory/KKT audits of the source implementation.

## Isolated execution

For an additional dependency check, the package directory alone was copied into a temporary directory, excluding `__pycache__`. A fresh Python process ran with `-I -S -B`, working directory `/`, and only that temporary package path explicitly added. An import guard rejected research-module imports. All three public acceleration backends solved and independently certified a nontrivial two-vertex case with hash-forbidden labels.

The process confirms that no research or test module was imported. It also checks that no loaded package Python source contains `FunctionType`. The package default remains identically the `solve_source_energy` function, and the six new function/class exports are present. The temporary copy was removed afterward; the source package was not modified.

## Scope and remaining integration work

This audit approves the current transcription and explicit-factory replacement. It does not change the public default, perform a release, rerun the broad manifest, or claim a new mathematical convergence result. The source proofs still provide the numerical and work guarantees; the independent AST and exact-isolation checks establish that the standalone acceleration paths preserve those implementations.
