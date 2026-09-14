# Independent audit of the optional mass-grid package

Status: passed, with no implementation change requested.

Audited package module: deliverables/deterministic-rppr/deterministic_rppr/_mass_grid.py.
Its SHA-256 is 94485eadc2fbbd1b2a9026e58e6c0bd19b792c3271130a12392463bd11da9402.
The research source remains 3b8cfa4a8f0161101147573007e5ac4cbabb4c64e348ec702f90d977a37d7d8f.

The builder and MASS_GRID_TRANSCRIPTION.json were inspected without executing
the builder. The manifest's source, package, and approving audit hashes match.
An independent reverse-AST comparison verifies that the complete module is
identical except for the three relative import relocations, removal of the
research FunctionType helper import, addition of the packaged integer-module
reference, and one explicit continuation call with corrector_class=factory.
The receiving packaged continuation independently matches the research
integer wrapper's complete AST after removing its private constructor
keyword and restoring its one constructor name. All numerical loops, stage
schedules, repair statements, return branches, and accounting bodies are
therefore unchanged by relocation.

The public exports resolve to the intended optional function and four public
types. The default remains solve_fast, and the fast module's hash is unchanged.
All eighteen preexisting numerical modules listed in the build manifest
retain their hashes. The only permitted public-initializer changes are the
optional imports and exports; no default dispatch is replaced.

The independent checker audit_mass_grid_package_independent.py copies only
the package to a temporary directory and starts Python in isolated (-I)
mode. A module finder rejects research-source imports, and the standalone
driver contains its own small exact dense KKT oracle. The isolated package
is compared against the independently audited research adapter on:

- Six complete calls, including two ordinary continuations, a positive
  zero-step case, alpha=1, the zero-solution branch, and a hash-forbidden
  large-label graph with an inactive degree-10^30 boundary.
- Eight repaired stages checked by exact dense KKT solutions, six separate
  final subgradient certificates, and every complete nested work ledger
  and external degree/adjacency call sequence.
- Nine same-grid state prefixes, complete diagnostic fields, and an exact
  zero-energy stage; inherited step, run, and scalar-rebase method identity
  is also checked against the packaged fast corrector.

All comparisons pass exactly. No inactive high-degree boundary row is read,
the final certificates meet their requested tolerances, and the copied
package imports only its own package modules and the standard library.
The complete result and metric comparisons also preserve the separate hint
pass ledger and the accumulated retargeting counter convention; they do
not silently combine those charges.

Saved gate: mass_grid_package_independent_verification.json (passed=true).
All package Python file hashes are recorded there and remained unchanged
during the check. The temporary isolated copy was removed on completion.
No numerical core, package, finalizer, or proof file was edited. The full
183-case suite was not rerun, and no performance claim is made here.

This packaging audit relies on the separately proved mass-scaled energy
lemma and implementation audit for uniform accuracy and work bounds. Its
role is to verify faithful relocation, optional public dispatch, and bounded
exact end-to-end operation without a research-workspace dependency.
