# Independent audit of the direct-transition package addition

Result: **no transcription, composition, or locality defect found** in the current `_direct.py`, `_fast.py`, and additive exports. The default remains `solve_source_energy` at the audited snapshot. No package file was edited, and the broad 183-case manifest was not rerun.

The independent script is `audit_fast_package.py`; its exact results and transcription hashes are saved in `fast_package_independent_verification.json`.

## Static transcription and unchanged prior code

The audit verifies the three hashes in `DIRECT_TRANSCRIPTION.json`, the independently audited direct-source hash, and the source-composition benchmark hash. It also combines the earlier transcription manifests and verifies that all **14 preexisting package modules** are unchanged. The prefix of `__init__.py` before the new direct-transition export block matches its previous hash exactly.

For `_direct`, the audit reverses only the documented relative-import rewrites, removal of the `FunctionType` continuation helper and its two bindings, and replacement of the two wrappers by explicit `corrector_class` calls. Each new call is checked against the exact expected class. After that normalization the entire module AST agrees with `direct_exception_integer_rppr.py`. This includes every integer state update, partition-membership condition, rebase branch, registry update, counter, and class base list; no numerical or transition logic was rewritten.

The generated `_fast` contains only its documentation, three expected package imports, the composed class, and one explicit class-injection wrapper. Its two base classes exactly match the audited `DirectCombinedCorrector` in `benchmark_direct_exception_transition.py`. The added class documentation has no operational effect. There is no extra executable state or research-module import.

## Composition and update boundaries

The actual package method-resolution order is:

`Fast -> Combined -> EarlyStop -> Binomial -> SourceEnergy -> DirectExceptionInteger -> Integer -> object`.

It matches the source composition apart from the outer class name. Cooperative initialization constructs integer state and direct-transition metrics before the higher-level schedules and checkpoint fields finish initializing. During a step, early-stop bound invalidation and the binomial wrapper surround the direct integer update. The binomial power update occurs after the direct transition is complete; checkpoints occur afterward in the inherited run loop. Thus the reporter is not queried midway through a partially replaced exception representation.

The direct implementation removes old records by their stored registry keys. Its non-rebase update partitions retired exceptions, ordinary touched records, and new exceptions; its rebase resets every exposed base key before reinstalling exceptions. Those exact bodies were independently audited in `direct_exception_independent_audit.md` and are unchanged in the package. This package audit does not substitute a new numerical argument for that earlier mutation-level proof.

All graph-state collections remain the existing AVL maps and sets. The new transition metrics are a fixed-size dataclass; their diagnostic dictionary has fixed string keys. The representation optimization changes reporter mutation counts while preserving numerical states and graph/checkpoint work.

## Exact source/package comparisons

The bounded checks compare record contents and exact numeric fields across the distinct source/package dataclass types. They passed:

- 48 direct-integer steps and 20 composed-fast steps, including 22 scalar rebases.
- At every compared step: scale/grid, baseline, degrees, cached adjacency, X/L/z/M/source maps, exception membership, reporter registry records, projection values, last-step data, objective bound, diagnostics, and external query histories.
- Six complete fast-backend output comparisons covering 18 stages and 40 checkpoints.
- A positive-error zero-iteration stage, the immediate zero-solution case, and the alpha=1 direct branch with no adjacency reads.
- Nonsquare alpha, an asymmetric cyclic graph, labels larger than 2,048 bits, and a billion-degree hub boundary.

All numerical solver labels in these checks are integer subclasses whose `__hash__` raises. The hub oracle asserts if its high-degree row is requested; only leaf rows are scanned. Complete source and package results, including direct-transition and checkpoint metrics, match exactly. Each final package output also passes the independent sparse norm certificate at its requested tolerance.

## Isolated fast execution

The package alone was copied to a temporary directory without bytecode caches. A fresh process ran with `-I -S -B`, working directory `/`, and only that package path added. Research-module imports were explicitly forbidden. `solve_fast` completed and independently certified the hub-boundary case using hash-forbidden labels, without inspecting the hub row. The process also verified that loaded package sources contain no `FunctionType` use. The temporary copy was removed afterward.

## Scope

This audit approves the additive package transcription and composition at the saved hashes. It does not change the default, claim an independently reproduced timing improvement, run the broader KKT manifest, or perform a release. The previously measured speedup remains evidence from `benchmark_direct_exception_transition.py`; the work here establishes exact transcription, state agreement, deterministic container use, and standalone locality.
