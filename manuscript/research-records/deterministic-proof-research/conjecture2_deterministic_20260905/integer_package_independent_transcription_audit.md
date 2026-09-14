# Independent audit of the additive integer package transcription

Status: passed. This audit did not invoke the builder or modify package
source files. It covers transcription and finite integration behavior;
the source-energy schedule's mathematical argument is audited separately.

The recorded `INTEGER_TRANSCRIPTION.json` SHA-256 is
`04bf0a1f0ec3645a4b6d1e9b716a20874d1c6fc6a0d60f32550cac3158ca6034`.
The package is the fresh `deliverables/deterministic-rppr/deterministic_rppr`
directory. Evidence is in:

- `audit_integer_package_transcription.py` and
  `integer_package_independent_transcription_results.json`;
- `audit_integer_package_isolated.py` and
  `integer_package_isolated_import_results.json`.

## 1. AST and hash equivalence

All four new manifest records match their actual package hashes, and all
three recorded original-source hashes match the audited source files.
The original integer source hash is the same snapshot that passed
`integer_solver_independent_end_to_end_audit.md`.

Independent AST comparisons found exact equivalence of eight classes and
their 42 methods across the reporter, integer core, and source-energy
module. Ten imported dataclass definitions were separately matched through
their inheritance chain, including solver results, stage summaries, and
repair/corrector metrics. This checks that import relocation preserves
their fields and defaults, not just their names.

For the reporter, the entire non-import module AST is identical. The
integer module differs only by the declared optional keyword:

    solve_rppr_integer(..., *, corrector_class=IntegerDyadicCorrector)

and the single constructor call changed to `corrector_class(...)`.
Undoing precisely those two AST changes makes its full non-import AST
identical to the original. Every relocated import was independently
compared with the expected relative package import and alias. The audit
did not simply rerun or trust the builder's transformation functions.

All seven pre-existing package module hashes still match the older
`TRANSCRIPTION.json`. In particular, `.solver` was not replaced or edited.
At runtime `solve is solve_reference is solver.solve_rppr_practical`.
The original Fraction implementation therefore remains the default, and
the two added backends are explicit exports.

## 2. Wrapper semantic equivalence

With the default class, the copied integer wrapper has the same ordinary
behavior: it passes the same constructor arguments, executes the same
repair, summaries, zero and alpha-one branches, and returns the same data.
The new keyword only makes the class choice explicit.

The original source-energy helper is a FunctionType clone of the exact
integer wrapper code, using a copied globals dictionary in which only
`IntegerDyadicCorrector` is replaced. The audit checked actual code-object,
defaults, closure, and global-binding identity for that clone. The packaged
source-energy wrapper calls the copied integer wrapper with exactly that
replacement class as its new keyword. The source-energy class itself is
AST-identical. Thus the replacement removes the private globals clone
without changing ordinary numerical behavior.

This equivalence assumes normal unchanged module bindings. A private
monkeypatch of the original module's class or helper globals after import
is not a promised compatibility behavior: the old clone captured globals,
whereas the new API supplies an explicit class argument. The class-injection
keyword is the supported way to choose a replacement in the package.

## 3. Exact fixture comparisons

Five bounded fixtures covered a path, leaf-seeded star, triangle, alpha-one
shortcut, and exact zero-solution threshold. For each, both new backends
were compared against their corresponding original function, giving ten
exact backend pairs. The comparison included the complete normalized
dataclass result, every nested metric, and the full degree-query and
adjacency-row query sequences. All pairs were identical.

The checker also independently enumerated exact KKT supports and used the
edge-form objective to verify actual gap and coordinatewise containment.
It did not rely only on matching two implementations' returned certificates.
These finite comparisons confirm transcription behavior, not a substitute
for the separate general source-energy proof.

## 4. No-hash graph-label tests

All three package backends were run with vertex labels
`2^100+37*i`, represented by an integer subclass whose `__hash__` raises
an exception. The oracle itself used only a short label list and linear
comparisons, so a hidden graph-label hash operation in a solver would fail.
After inverse relabeling, outputs, certificates, source/access data, and
operation counts matched the ordinary-label runs.

The measured Fraction backend correctly reported a 101-bit label encoding
instead of the smaller ordinary-label maximum, and its derived internal
bit bound increased correspondingly. Only those two explicit encoding
diagnostics were allowed to differ; this is required accounting for the
larger labels, not a numerical discrepancy. The integer backends' complete
normalized results matched without that exception.

This test addresses graph-state hashing. It does not claim that Python's
module namespaces, classes, or fixed string-keyed diagnostic dictionaries
are implemented without internal hash tables.

## 5. Package-only isolated import

A further three-backend fixture ran under Python isolated mode, with the
research directory absent from the import path and only the standalone
package parent explicitly added. Each backend used hash-forbidden
100-bit labels on a two-vertex path and passed the exact known-optimum
and objective-gap checks.

No original research module was loaded, including the original integer,
source-energy, practical, bounded-corrector, AVL, or reporter modules.
This rules out successful integration tests caused by an accidentally
available unrelocated research import.

## Conclusion

The additive package transcription preserves the audited integer core and
the existing default implementation. The explicit class-injection wrapper
is semantically appropriate, and the package passes bounded exact and
no-hash integration checks without original-module imports. No packaging
correction was required. Optional source-energy mathematics and broader
packaged-solver validation remain distinct evidence, as intended.
