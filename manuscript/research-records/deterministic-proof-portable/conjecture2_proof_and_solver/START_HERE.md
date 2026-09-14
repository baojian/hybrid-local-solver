# Deterministic Conjecture 2: proof and implementation

The proof answers OP2 from the designated problem-definition note in its
exact-real algebraic word model. It gives a deterministic local algorithm
with additive objective accuracy and fully charged work
`Otilde(1/(rho sqrt(alpha)))` in the nontrivial regime. It also gives a
separate bounded-integer implementation for rational inputs.

Start with [the reading guide](proof_reading_guide.md), then read
[the complete proof](output/pdf/deterministic_conjecture2.pdf).
The main [TeX file](deterministic_conjecture2.tex) includes the two adjacent
appendix files. Compile it with a standard LaTeX installation.

The standalone [solver package](deliverables/deterministic-rppr/README.md)
contains code, examples, exact tests, and the package manifest. The wheel
in `install/` contains the identical library modules. Its default is the
fixed-stage fast solver; adaptive continuation, mass-scaled precision and the
singleton precheck are optional and have their own charged work records.
The [proof-to-code map](proof_to_implementation_map.md) identifies the actual
methods implementing each invariant and the accounting categories.
The [algebra walkthrough](core_algebra_walkthrough.md) expands the accelerated
comparison and the selected-flow calculation underlying the local work bound.
The package's `validation/` and `benchmarks/` directories provide standalone
commands that do not depend on the original research workspace.

[The three-vertex example](worked_three_vertex_example.md) provides an
exact regularization path and a worked numerical comparison. The included
audits and validation records are additional checks performed within this
research task. They are not claims of external peer review. Paired timings
are empirical results with runtime provenance, not substitutes for the
graph-uniform proof.
The historical timing reports preserve their original runtime and harness
scope. Their research-directory reproduction commands refer to that original
workspace; use the bundled portable runner for a new standalone comparison.

Only final proof, implementation, validation, and explanatory artifacts are
included here. The designated source note was not edited or copied into the
bundle, and other manuscript notes were not inspected. The proof supplies
its mathematical definitions and required standard properties directly.
`BUNDLE_MANIFEST.json` records the copied artifact hashes and source paths.
