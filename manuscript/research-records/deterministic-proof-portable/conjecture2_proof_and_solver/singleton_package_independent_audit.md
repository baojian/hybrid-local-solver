# Independent singleton package transcription audit

**Passed; no defect found.** The package implementation in
`deliverables/deterministic-rppr/deterministic_rppr/_singleton.py` agrees
with the separately audited optional helper. No package or source solver
file was edited for this audit.

## Transcription and exports

The complete module AST is identical to `singleton_precheck_rppr.py` after
reversing exactly the documented two changes: its one import now refers
to `._fast.solve_rppr_fast`, and the one function-default name now binds
`solve_rppr_fast`. All function/dataclass bodies, branch ordering, metrics,
validation and result construction are unchanged. Source and package
hashes match `SINGLETON_TRANSCRIPTION.json`:

- Source: `54d4f30160034f27aac40d947353919b4c41d7163d820ab096d20bc1087efcbc`.
- Package: `faac5194c6945c45ca6dd6dc55bf204cbaf2754a97c698eafa418b042cb54864`.

At runtime, the helper's default fallback is the identical exported
`solve_fast` function and its cutoff remains 32. The exported `solve` is
still identical to `solve_fast`; it does not invoke a singleton trial.
`solve_with_singleton`, `SingletonPrecheckResult`, and
`SingletonTrialMetrics` are exported separately. Hash checks against the
latest applicable transcription records confirm all 16 existing numeric,
container, reporter, certificate and result modules are unchanged.

## Behavioral and accounting checks

`audit_singleton_package.py` independently compares the packaged helper
with the audited source helper explicitly supplied the package fast
fallback. Five cases cover exact-threshold singleton success, a genuine
failed trial, an explicit cutoff skip, exact-threshold zero, and alpha one.
All complete results and actual graph-query sequences match. Every label
in these cases forbids hashing and exceeds 2051 bits in magnitude.

The failure and skip cases run the actual fast solver. Both the explicitly
captured fallback and the helper's bound default are exercised. The helper
retains the identical returned fallback object, output tuple, and
objective-gap object. The fast result, including all nine stages across
these two cases, matches a separate fresh fast solve exactly. Removing the
trial's measured degree/row prefix leaves the fresh fallback's query
sequence; total streamed entries equal trial entries plus fallback entries.
Thus the package relocation has not hidden the failed trial in numeric or
repair ledgers. The explicit skip has no row prefix and adds one seed
degree reply. The failed trial consumes precisely one seed entry and two
degree replies in its fixture.

Every output is checked by the package's independent sparse certificate.
The singleton, zero and alpha-one outputs have exact zero subgradient norm
and zero certified gap. Both fallback outputs satisfy the requested
`epsilon=1/100000`. The original helper's independent mathematical/bit-cost
audit continues to apply unchanged; this audit does not infer general
correctness from the finite cases.

## Standalone isolation

The test copies only `deterministic_rppr/` to a temporary directory, then
starts a fresh Python process with `-I -S -B`, working directory `/`, and
only that copy added to the import path. An import guard additionally
rejects known research-source module names. A hash-forbidden, huge-label
leaf adjacent to a degree-`10^30` hub returns the exact singleton using two
degree replies and one seed entry; querying the hub row raises. The copied
package independently certifies its gap as zero. A second isolated case
performs a genuine four-stage fast fallback on an edge and independently
certifies its final accuracy. Both pass without access to research files.

Reproduce from the research directory with
`python3 -B audit_singleton_package.py`. Complete structured evidence is in
`singleton_package_independent_verification.json`. The bounded audit
finished in about two seconds and did not rerun the broad package manifest
or perform a timing study.
