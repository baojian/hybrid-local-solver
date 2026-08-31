# Handoff: original-score-quartic

- Agent family: codex
- Role: direction
- Branch: `agent/codex/original-score-quartic`
- Base commit: `88a3c36591e17e3aa2a216998d4574675185e860`
- Assignment state: ready_for_review
- Write scope: the `volume_gated_acceleration` note, one exact scalar audit and
  its registry entry, the coordination assignment, and this handoff.

## Outcome

- Requested result: close or sharpen the original all-coordinate
  consumed-reserve coefficient under arbitrary projection for the declared
  zero-start point-seed recurrence and complete gate; the follow-up asks for
  the next rigorous convergence or recovery consequence.
- Implemented result:
  - Proved that the support-positive score's projected decrement is valid
    along the original gate chronology and remains invariant under frozen
    genuinely violating admissions.
  - Proved a first-admission energy floor.  If the initial singleton seed face
    is interior and the first boundary vertex is admitted, then
    `E_0 > c_0(q) q^5`, with
    `c_0(q)=4(1+q^2)/(5(1-q^2)(3+q^2))`, and the already consumed reserve at
    that gate is larger than `c_0(q) q^6`.
  - Every clipped positive-residual row is a nonseed row and contributes at
    most `q^2/25` to the original score.  The first-admission reserve floor
    pays this contribution with the same coefficient
    `(1-q^2)/q^4` that pays positive-support rows.
  - Therefore the original all-coordinate score is causally solvent under
    arbitrary projection with `(1-q^2)/q^4`.  Combined with the exact
    `K_{2,r}` lower family, its graph-uniform coefficient order is exactly
    `Theta(q^-4)`.
  - The separate total transported-energy identity satisfies
    `E_0+D_k <= q^2` on every graph.  Residual-to-energy control at
    `E_gate=q^12/(50(1+q^2)^2)` makes every active envelope row
    certificate-safe.  The complete gate must therefore admit or certify
    after at most `O(q^-1 log(1/q))` consecutive steps on any face.
  - Consequently every finite execution terminates with PPR error at most
    `2q/5`, total fixed-face steps `O(q^-2 log(1/q))`, and swept active volume
    `O(q^-3 log(1/q))`.  A dense incremental Cholesky implementation charges
    every exact optimum displacement in the same exact-real arithmetic order
    with `O(q^-2)` persistent storage.
- Deliberately unchanged:
  - The theorem requires `0<q<1`, `rho=tau=q/5`, a point seed whose initial
    singleton restricted optimum is interior, the named post-step genuinely
    violating gate, frozen zero-padding, exact transport, and exact-real
    support decisions.  Without singleton interiority the statement is false.
  - The quartic theorem itself is scalar all-history solvency only.  The
    separate total-energy theorem supplies convergence and a charged dense
    fallback; it does not infer them from scalar solvency.
  - The fallback is still a factor `O_tilde(q^-1)` above the desired
    product-scale work and proves no finite-precision, bit-complexity,
    stability, sparse-fill, or intermediate-emission bound.
  - The projection-normal identity and reachable 30-vertex projection witness
    remain useful local diagnostics; they no longer constitute a scalar-order
    gap.

## Evidence

- Added `volume_gated_acceleration.original_score_quartic`, an exact rational
  regression audit for the constant identity, first-admission minimization,
  clipped-row reserve comparison, total-energy cap, envelope threshold, and
  hold exponent.  It passes 4,860 integer-degree and eight horizon cells
  across eight rational `q` values.
- An independent read-only equation audit rederived the singleton gate,
  energy minimization, reserve chronology, and score split.  It also supplied
  the necessary noninterior counterexample: at `q=1/2`, the center-seeded
  `K_{1,11}` has zero singleton optimum and reserve but a positive seed score.
  The theorem explicitly excludes this case.
- All 13 full-tier `volume_gated_acceleration` audits pass in 40.7 seconds,
  including the graph-atlas enumeration and the reachable-projection screen.
- The 77-page note builds with no undefined reference or citation.  The note
  inventory/target check, global coordination audit, focused Ruff
  lint/format, and `git diff --check` pass.
- All 210 repository tests pass with 15 known temporary-directory cleanup
  warnings.  Repository-wide `make lint` reproduces exactly the 1,345
  pre-existing findings under `manuscript/claude-overnight-2026-08-24/`; none
  is in a changed file.

## Review notes

- Provider-owned paths changed: none.
- Shared paths changed: the proof-audit registry and coordination metadata
  listed in the assignment.
- Open decisions or follow-up: remove the per-face logarithm, avoid repeated
  full active scans, or replace dense optimum transport with a response whose
  total charged work is `O_tilde(q^-2)`.  Every uncached optimum, energy,
  support, and gate query remains charged.
