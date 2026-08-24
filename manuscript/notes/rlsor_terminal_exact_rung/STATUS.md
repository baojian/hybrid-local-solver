# Direction status: rlsor_terminal_exact_rung

Last reviewed: 2026-08-20
State: measured

## Exact question and contract

- **Question:** Which ranked-local-SOR relaxation/rung schedules reduce charged
  work on the fixed 24-cell benchmark, and which measured mechanism survives
  matched controls?
- **Model:** The shared source-aligned PageRank quadratic with
  `r = b - Q x_hat`, on six real graphs, two seeds per graph, and
  `alpha in {0.025, 0.04}`.
- **Accuracy namespace:** The note-scoped verifier gate is
  `||D^(-1/2) r||_infinity <= alpha * eps_ppr`, with
  `eps_ppr in {1/n, 0.1/n}`. It is not the repository-wide stopping decision.
- **Access and charged work:** Every executed row operation on `u` costs
  `c(u) = 1 + d_u`; repeats are charged and a live-guarded skip is free. The
  reported score is this service meter, not wall-clock or a complete charge for
  client-side frontier handling.
- **Intended result:** Preserve reproducible empirical arms and falsifiable
  mechanism hypotheses; do not promote them to graph-uniform theorems.

## Claim ledger

- **Source:** `main.tex:56-77` imports the shared problem and states the exact
  benchmark contract. The R-LSOR reference and frontier artifact are benchmark
  records, not literature theorems.
- **Proved here:** A coordinate SOR push satisfies
  `r_u <- (1 - omega) r_u` (`main.tex:95-100`). No accelerated complexity
  theorem is proved here.
- **Conditional:** The no-reactivation inequalities
  `omega <= 1 + 1/b` and `omega <= 1 + 1/b^2` are in-band heuristics that ignore
  new neighbor arrivals (`main.tex:241-267`).
- **Measured:** R-LSOR totals 84,071,471; the independently found frontier run
  totals 69,351,213 and was reproduced; the graft totals 64,564,398 but is a
  single measurement not independently reproduced; the eleven-arm campaign's
  best tested arm is the two-rung `B = 2.5` schedule at 60,741,237, certified
  24/24 (`main.tex:82-84,137-183,269-302,344-356`). The constructed cross-cell
  selector was never run as one declared policy (`main.tex:214-227`).
- **Refuted:** The predicted base-2 eight-rung alternating ladder does not beat
  base 3 (`main.tex:304-312`).
- **Open:** Independent graft reproduction, a fine per-alpha `B` sweep, and a
  declared test combining cross-cell relaxation choice with rung scheduling.

## Central blocker

The next falsifiable target is a preregistered fine sweep over
`B in [2.2, 2.8]`, reported separately for each alpha, together with an
independent rerun of the graft. Treat `B = 2.5` as best tested, not optimal.

## Dependencies and reusable outputs

- **Formal registry dependencies:** none.
- **Source/shared prerequisites:** the shared problem contract and benchmark
  artifacts.
- **Context/provenance:** `frontier_adaptive_ladder` preserves the frontier
  comparison run; it is not a proof-import edge.
- **Supplies to:** `two_rung_sor` (distilled measured family),
  `delayed_reflection_ladder` (reflection-debt motivation), and empirical arms
  used by adaptive/propagate-settle controllers.

## Resume here

- **Exact pointer:** `main.tex:269-356` for the campaign, open sweep, and
  provenance; `main.tex:214-227` for the unrun selector.
- **Next action:** Reproduce the graft, then run the per-alpha fine sweep under
  the identical verifier and work meter.
- **Stop/go test:** Continue tuning only if held-out or independently rerun
  cells preserve a material valley; otherwise freeze the schedule as an
  empirical portfolio arm.

## Verification

- **Source pointers checked:** `docs/research-context.md`,
  `docs/mathematical-conventions.md`, relevant acceleration/local-solver
  literature notes, this README/main file, and sibling measured notes.
- **Checks last run:** `make note-audit` passed on 2026-08-20; focused LaTeX
  build not rerun because no theorem source was changed.
- **Known gaps:** The former claim that 1.9 and 2.3 bracket 2.5 has been
  corrected to match `two_rung_sor/main.tex:130-137`: both lie below the
  best-tested point. README line 10's “everything is a measurement” should not
  be read as labeling the exact residual identity or conditional heuristic as
  measurements.
