# Handoff: signed-spider-global-semantic-stop

- Agent family: codex
- Role: direction
- Branch: `agent/codex/signed-spider-global-semantic-stop`
- Base commit: `1ff1bf43346dced88da96a8045dcbbeef511c627`
- Assignment state: ready_for_review
- Write scope:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/signed-spider-global-semantic-stop.md`
  - `manuscript/notes/signed_spider_generalization/`
- Permitted shared files: the same three paths above.

## Outcome

- Constructed a finite simple connected layered bipartite family with red
  vertices `r_0,...,r_n` and `3^(n-1-i)` parallel two-edge channels between
  consecutive red layers.
- Proved that the red two-step semantic chain stays with probability `1/2`,
  moves left with probability `3/8`, and moves right with probability `1/8`.
  Its hitting time from `r_n` to the seed has expectation at most `4n`, so the
  far-to-seed discounted Green ratio is at least `c_alpha^(8n)`.
- Proved exact finite propagation for zero-start, source-color-first SOR with
  graph-global `omega_alpha`: after `k` complete sweeps only coordinates
  within distance `2k-1` can have changed.  The far red coordinate therefore
  stays unchanged through sweep `n`.
- Taking `alpha=(T/n)^2` shows that no graph-independent finite constant can
  extend the spider envelope
  `C(1+k sqrt(alpha)) exp(-4k sqrt(alpha))` to every finite connected
  bipartite graph, and no graph-uniform fixed relative reduction is guaranteed
  through any fixed multiple of `1/sqrt(alpha)` full sweeps.
- Proved the narrowly scoped absolute-work consequence.  Reversibility and
  the exact PSD incidence Gram factor give
  `1/((1+c)(3^n-1)) <= y_seed <= 1/((1+c)3^(n-1))`; hence
  `y_seed=Theta(1/vol(G_n))`.  With `eps=y_seed/2`, the failed `n` sweeps have
  work-to-`1/(sqrt(alpha) eps)` ratio greater than `T/2`.  Arbitrary `T`
  rules out graph-uniform product work for this literal complete-face
  full-sweep plain-SOR primitive.
- Kept the boundary explicit: this is not a lower bound for other local
  algorithms, support discovery, response composition, the supplied-face
  logarithmic SOR solve, or the Euclidean fixed-face spectral theorem.

## Evidence

- `verify_spider.py` now checks the layered transition rows, incidence
  Gram/PSD identity, hitting-time increments, discounted Green ratio,
  stationary diagonal Green bounds, inverse-volume seed scale, and finite
  propagation in exact rational arithmetic for seven depths.  Its complete
  audit passes 80 SOR-mode cells, 144 spider cells, 14,616 radial-semantic
  cells, one sweep-order witness, seven exact funnel cells, 522 RPPR-bias
  cells, and 132 face-shock cells.
- `verify_fixed_face.py` independently passes all 570 cells.
- The 28-page note builds with no undefined references, citations, or
  overfull boxes.  The four pages containing the new theorem and corollary
  were rendered and visually inspected.
- Focused Ruff checks, `make note-audit`, `make agent-audit`, `git diff
  --check`, and all 210 tests pass.  The test warnings are the known temporary
  directory cleanup warnings.
- Repository-wide `make lint` remains red on the same 1,345 pre-existing Ruff
  findings under `manuscript/claude-overnight-2026-08-24/`; the focused note
  verifier lint is clean.

## Review notes

- The full graph and bipartition are supplied for free in the work corollary;
  one completed full sweep is charged exactly by graph degree volume.
- The source normalization is `h=(1-c_alpha)/d(r_0)`.  The stationary Green
  contribution supplies the lower seed bound; the return-probability sum
  supplies the upper bound.
- The work contradiction quantifies over arbitrary fixed `T` before taking
  `n` large.  For a claimed constant `C_W`, choose `T>2C_W`.
- The smaller unequal-arm graph that refutes the sharp coefficient was not
  included because the layered family proves the stronger universal-constant
  and full-sweep-work stops.
