# Handoff: signed-spider-generalization

- Agent family: codex
- Role: direction
- Branch: `agent/codex/signed-spider-generalization`
- Base commit: `15702d5cafd51f4a2175e93ceb154c3afa9bbe92`
- Assignment state: ready_for_review
- Write scope:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/signed-spider-generalization.md`
  - `manuscript/notes/README.md`
  - `manuscript/notes/registry.toml`
  - `manuscript/notes/signed_spider_generalization/`
- Permitted shared files: the same five paths above.

## Outcome

- Proved an exact PPR--RPPR semantic bias bridge and a conservative
  objective-gap conversion, so SOR and FISTA can be compared only under a
  matched objective/accuracy contract.
- Proved the optimal red--black SOR spectral factor and a finite power bound
  on every supplied bipartite face.  The sharp face-specific rate requires
  supplied spectral tuning; one graph-global parameter gives the generic
  fully charged rate without an eigenvalue computation.
- Proved a dimension-free maximum-norm Chebyshev-wave envelope for plain
  source-color-first SOR on every complete equal-arm hub-seeded spider.  It
  removes the logarithm on the output-scale family and yields
  `O(1 / (sqrt(alpha) eps_ppr))` charged work.  An exact `P2` witness shows
  why the source-first order is a real theorem hypothesis.
- Specialized the factor to depth-`L` spider prefixes, giving sweep scale
  `Theta(1 / sqrt(alpha + L^-2))` up to logarithms and fully charged repeated
  face scans; derived the exact hub-seeded radial PPR profile.
- Distinguished the new log-free plain-SOR theorem from the already-proved
  radial two-rung finite-spider algorithm: both are accelerated, but only the
  latter performs adaptive prefix exploration and optional Schur deflation.
- Kept support discovery separate and imported, without relabeling, the
  stronger exact-response results for hub-rooted spiders, arbitrary rooted
  trees, and bounded biconnected blocks.
- Proved exact face-shock Pythagoras for an arbitrary nonsettled old iterate
  and a windowed global-parameter SOR continuation theorem for supplied
  geometrically growing bipartite faces.  This closes numerical state
  transport under the gate and narrows the open interface to repeated scans
  and output-sensitive boundary reporting in large nonequitable cyclic cores.

## Evidence

- The 24-page note builds with no undefined references, citations, or
  overfull boxes, and all pages were rendered and visually inspected.
- `verify_spider.py` passes 80 deterministic SOR-mode cells, 144 exact-formula
  spider cells, 14,616 radial-semantic cells, one sweep-order witness, 522
  small-graph RPPR-bias cells, and 132 face-shock cells.
- `verify_fixed_face.py` independently passes 570 exact/formula/power cells.
- Focused lint, note inventory, coordination, branch-scope checks, diff
  checking, and all 210 tests pass.  The test run reports only the known
  temporary-directory cleanup warnings.

## Review notes

- Provider-owned paths changed: none.
- Shared paths changed: assignment/handoff, note registry, and generated note
  index only.
- Scope boundary: fixed-face SOR does not discover or certify a changing face;
  imported response solvers use stronger, separately charged primitives.
- The supplied-face continuation theorem does not pay for arbitrary singleton
  admissions or the boundary reporter; geometric volume growth is an explicit
  condition, not hidden in the notation.
- Independent equation-level review restored the source hypotheses on the
  imported radial two-rung theorem and separated oracle spectral tuning from
  the generic globally tuned fixed-face bound.
