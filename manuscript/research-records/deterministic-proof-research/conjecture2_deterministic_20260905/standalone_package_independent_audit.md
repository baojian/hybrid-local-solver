# Independent audit of the standalone AVL-backed package

Audited `deliverables/deterministic-rppr` in the fresh research directory
without modifying any package source. The audit covers extraction,
graph-state containers, locality/reclamation costs, and bounded exact
comparisons against `practical_dyadic_rppr_solver.py`.

## Result

No package-transcription or container-semantics defect was found. All
graph-indexed point maps and sets on the public solve path are AVL-backed.
Remaining runtime dictionaries hold a fixed number of diagnostic fields.
The exact numerical outputs and stage summaries agree with the verified
prototype in the tested cases. The package passes an additional check
using integer graph labels whose `__hash__` method raises an exception.

The independent script is `audit_standalone_package.py`, and its report is
`standalone_package_independent_verification.json`. The script does not
regenerate or edit the package and does not invoke a randomized test.

## Extraction and imports

The seven component source hashes in `TRANSCRIPTION.json` matched their
fresh sources. The recorded package hashes matched the generated modules;
the copied `_avl.py` matched the container source byte for byte.

An independent AST pass undid only the graph-container constructors in
the generated modules, then compared the complete bodies of all selected
definitions against the source. All 27 extracted class/function definitions
matched exactly after that restoration. This includes decorators, method
bodies, annotations, defaults, and class docstrings. No numerical update
was silently changed by AST unparsing.

The package imports only standard-library modules and its own relative
components. The selected weighted-tree and reporter definitions retain
their needed helper functions; unused research solver classes are not
imported at runtime. Dataclass/Fraction imports and the aliases needed by
the extracted types are preserved. Import filtering therefore does not
create a missing global dependency on an omitted prototype module.

## Graph state and metadata

In `_dyadic.py`, the baseline, degrees, adjacency cache, lazy keys, X, L,
kinetic z, exact kinetic neighbor sums M, source, emitted projection,
neighbor-sum builders, and changed-coordinate maps use `AVLMap`.
Exception sets, touched-coordinate sets, source unions, and output unions
use `AVLSet`. The weighted projection reporter remains its original
deterministic augmented AVL tree.

In `solver.py`, both scalar-rebase replacement maps, rounded repair maps,
the monotone-maximum support union, the continuation baseline, and the
retained next baseline are likewise AVL-backed. In `_repair.py`, the
candidate-value and incoming PG maps use AVLMap; the public solve path
passes its AVL degree and adjacency caches into that helper. If the private
helper is called separately with arbitrary externally supplied caches,
those remain caller-owned objects. The package's public solve path does
not supply a hash table there.

The remaining explicit `dict(...)` call has exactly four named repair
counter fields. The two `asdict` uses convert fixed-field metric dataclasses;
their keys are fixed strings and their values are scalar counters. The
`dict` annotations in summary types refer to those same diagnostic maps.
They are not graph-indexed state. Python instance/global dictionaries
also have a fixed set of program field names, independent of the exposed
graph size. No worst-case graph lookup bound relies on them.

Cached adjacency rows are lists, not point maps. Their sequential creation
and inspection are already counted per entry. Emission/output lists,
per-iteration histories, and stage-summary lists are also sequential
containers with explicitly bounded lengths. Replacing point dictionaries
does not require converting these paid lists into trees.

## Changed iteration order and arithmetic semantics

AVLMap/AVLSet iteration is sorted by integer label. This can change the
order of source aggregation, key insertion, and exception updates from
the prototype's insertion/hash order. All involved arithmetic is exact
rational arithmetic, so the sums are unchanged. The projection tree's
logical ordering is already `(raw_key, vertex_id)`; changing insertion
order changes tree shape, not sorted ranks or threshold outputs.

The old exception set is traversed and completely removed before a new
one is assigned. The scalar rebase reads old X/L maps into separate new
maps and then replaces them, so sorted live iteration does not invalidate
the input iterator. Refreshing exposed keys iterates the degree map while
mutating a different key map and reporter tree. The PG accumulation loops
over candidate values while updating a separate incoming map. Thus the
AVL iterator's structural-mutation checks do not conceal an incompatible
in-place update pattern.

## Clearing, discarding, and actual charge

Dropping a balanced map is not free node reclamation. The current package
does not call an uncharged global clear in an ordinary iteration, but
reassigning temporary maps can reclaim their old nodes. Those costs are
bounded as follows:

- Old kinetic and kinetic-neighbor maps, old exception sets, changed/touched
  maps, and intermediate unions have sizes bounded by the already charged
  old/new kinetic volume and fixed source-record count.
- A scalar rebase explicitly visits the old X and L records before
  replacing them. It refreshes all exposed keys. Reclaiming those old
  maps adds only a constant multiple of this charged record pass.
- Final PG temporary maps and monotone-repair maps are bounded by the
  candidate scan and its exposed neighbors, plus the old baseline.
- At a stage transition, all discarded point-tree nodes and cached row
  entries are bounded by that stage's accumulated exposure and emitted
  work. Stage summaries retain only already charged output tuples and
  fixed-size metadata.

AVL point operations add their worst-case logarithmic comparison factor.
The existing diagnostic counters are still structural counters, not a
literal count of every point-tree rotation, interpreter instruction, or
reference-count reclamation. The proof's charged operation bound includes
those factors; interpreting the metrics as an exhaustive instruction count
would be incorrect.

## Independent exact comparisons

A direct 20-step stage comparison used a three-vertex path with signed
2,049-bit labels and a nonzero two-coordinate dyadic baseline. The graph
labels were instances of an integer subclass whose `__hash__` raises.
After every step, the package's X, L, z, M, source, baseline, degree map,
scale, history entry, and objective certificate agreed with the prototype.
Every graph-state map/set had the expected AVL type. This fixture had
10 scalar rebases and 9 steps with nonzero primal neighbor-sum error,
so it genuinely exercised the approximate-response path. All rebase
adjacency counts were zero and total selected volume was 80.

Four full-solver comparisons also used hash-forbidden integer labels:

| Case | Stages | Iterations | Output records |
| --- | ---: | ---: | ---: |
| Asymmetric cyclic graph | 4 | 328 | 3 |
| Path with huge signed labels | 5 | 188 | 3 |
| Constant-time zero regime | 0 | 0 | 0 |
| Alpha equal to one | 0 | 0 | 1 |

The exact outputs, certificates, parameters, grid choices, mass caps,
kinetic volumes, baseline statistics, repaired outputs, and repair counts
matched stage by stage. Degree-query and adjacency-query multiplicities
also matched. Weighted-reporter rotation/visit counts need not match,
because balanced insertion order can change its shape; they were not
incorrectly required to be identical.

## Scope

This is a bounded audit rather than a new broad solver test suite. It
verifies the package transcription and the intended balanced-container
replacement on relevant actual execution paths. The mathematical
convergence/locality proof and the previously documented rational-arithmetic
scope remain the basis for the general theorem. It does not claim that
ordinary floating-point execution is certified.
