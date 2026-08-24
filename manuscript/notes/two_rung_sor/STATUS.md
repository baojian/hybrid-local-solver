# Direction status: two_rung_sor

Last reviewed: 2026-08-20
State: measured

## Exact question and contract

- **Question:** For the fixed schedule
  `[(B*tau, omega_star), (tau, 1)]`, which tested band factor minimizes charged
  work on the 24-cell R-LSOR benchmark, and which matched variants explain the
  observed valley?
- **Model:** Shared source-aligned PageRank quadratic and the unchanged R-LSOR
  charge-aware ranked chassis.
- **Accuracy namespace:** `tau = alpha * eps_ppr`, with verifier gate
  `||D^(-1/2)(b - Q x_hat)||_infinity <= tau`; note-scoped, not RPPR `rho`.
- **Access and charged work:** Each executed row operation costs `1 + d_u`;
  the top `ceil(|F|/32)` snapshot prefix is capped at 8,192 and every operation
  has a live threshold guard (`main.tex:40-101`). Reported totals are benchmark
  service work, not a complete wall-clock ledger.
- **Intended result:** Preserve the best-tested fixed propagation arm and its
  ablations. Do not claim continuous or graph-uniform optimality.

## Claim ledger

- **Source:** The chassis and mechanism come from
  `rlsor_terminal_exact_rung`; the frontier artifact is a measured comparator.
- **Proved here:** The algorithm is specified exactly. No convergence-rate or
  graph-uniform accelerated theorem is proved in this empirical note.
- **Conditional:** `B ~= 1/(omega_star - 1)` is a self-reflection heuristic for
  a possible per-alpha optimum, not an optimizer theorem (`main.tex:122-137`).
- **Measured:** Among `B in {2, 2.5, 3, 4, 5, 9}`, `B = 2.5` is best tested at
  60,741,237 charged operations, 24/24 certified (`main.tex:103-137`). Matched
  nulls and loser pairs identify alternation and band placement as the useful
  ingredients (`main.tex:139-186`). The campaign is one harness campaign; no
  independent second reproduction is claimed.
- **Refuted:** The base-2 eight-rung alternating ladder prediction is false
  (`main.tex:188-195`).
- **Open:** Fine `B in [2.2, 2.8]` sweep, per-alpha band choice, held-out graph
  validation, and independent campaign reproduction.

## Central blocker

The immediate falsifiable target is the fine, separately reported per-alpha
band sweep. `B = 2.5` must remain “best among tested campaign points” until
that sweep and independent validation exist.

## Dependencies and reusable outputs

- **Formal registry dependencies:** none.
- **Context/provenance:** `rlsor_terminal_exact_rung` and
  `frontier_adaptive_ladder` supply the chassis, history, and comparators; they
  are not proof-import edges.
- **Supplies to:** `two_rung_direct_theory`, `adaptive_revisit_control`, and
  `propagate_settle_framework` as a fixed measured propagation arm.

## Resume here

- **Exact pointer:** `main.tex:103-137` for the valley and open sweep;
  `main.tex:139-214` for variants and provenance.
- **Next action:** Run a preregistered per-alpha fine sweep with unchanged
  ranking, guard, verifier, and 24-cell schedule, then reproduce the winning
  point independently.
- **Stop/go test:** Promote a per-alpha choice only if it improves independently
  rerun totals without per-cell tuning; otherwise freeze `B = 2.5` as a tested
  portfolio arm.

## Verification

- **Source pointers checked:** Required context/conventions, measured sibling
  notes, README, algorithm, valley, variants, and provenance sections.
- **Checks last run:** `make note-audit` passed on 2026-08-20; focused LaTeX
  build not rerun because no theorem source was changed.
- **Known gaps:** The registry evidence remains `measured`, matching
  the six-point campaign. The former contradictory bracketing sentence in
  `rlsor_terminal_exact_rung` has also been corrected; this note's
  `main.tex:130-135` remains the precise interpretation.
