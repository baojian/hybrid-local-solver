# Direction status: frontier_adaptive_ladder

Last reviewed: 2026-08-20
State: measured

## Exact question and contract

- **Question:** Precisely preserve the frontier agent's adaptive alternating
  SOR artifact and determine which of its three ingredients explains measured
  work reduction.
- **Model:** The shared source-aligned PageRank quadratic on the same 24-cell
  six-graph benchmark used by R-LSOR.
- **Accuracy namespace:** Verifier-owned
  `||D^(-1/2)(b - Q x_hat)||_infinity <= alpha * eps_ppr`; this is note-scoped.
- **Access and charged work:** Executed row operations cost `1 + d_u` and
  guarded settled repeats are free. A call can contain up to 24 sequential
  sweeps subject to 65,536-operation and 2,000,000-charge caps
  (`main.tex:123-140`). Network latency and client orchestration are not the
  reported charged-work objective.
- **Intended result:** A complete reproducible artifact specification and
  decisive ablations, not a worst-case adaptive-control theorem.

## Claim ledger

- **Source:** The optimal-SOR prior is classical; the concrete update map and
  implementation are an agent-authored 2026-08-13 artifact (`main.tex:87-121,
  208-214`).
- **Proved here:** The algorithm and transport/retry semantics are specified
  exactly (`main.tex:142-192`). No local accelerated-work theorem is proved.
- **Conditional:** Revisit memory might help only on a longer repeated-instance
  schedule; the current evidence supplies no stationarity or transfer theorem.
- **Measured:** The artifact totals 69,351,213, certifies 24/24, passes the
  stated audit, and was reproduced exactly (`main.tex:42-59`). A fixed two-rung
  schedule totals 60,741,237 and beats it by 12%, so alternation survives
  distillation while the full adaptive machinery does not pay on this schedule
  (`main.tex:194-206`).
- **Refuted:** No mathematical conjecture is refuted locally. The available
  campaign empirically rejects the claim that the complete adaptive artifact
  is the best of these measured arms.
- **Open:** Whether memory helps with many instances per graph, and separate
  ablations of instance-dependent omega versus stacked guarded sweeps.

## Central blocker

The next falsifiable target is a longer, order-controlled repeated-instance
schedule comparing memory on/off while holding the alternating ladder and
stacking fixed. Keying memory only by graph size `n` must be stress-tested on
nonisomorphic graphs with the same size.

## Dependencies and reusable outputs

- **Formal registry dependencies:** none.
- **Source/shared prerequisites:** the shared benchmark and model.
- **Context/provenance:** the R-LSOR reference recorded in
  `rlsor_terminal_exact_rung` supplies the preserved comparison run, not a
  proof import.
- **Supplies to:** `adaptive_revisit_control` (revisit signal), `two_rung_sor`
  (distillation baseline), and `propagate_settle_framework` (measured
  propagation arm).

## Resume here

- **Exact pointer:** `main.tex:87-140` for ideas 2-3, `main.tex:142-192` for
  executable pseudocode, and `main.tex:194-206` for the unresolved transfer
  experiment.
- **Next action:** Run memory on/off and stacking on/off factorial ablations on
  a schedule with repeated same-graph instances.
- **Stop/go test:** Retain adaptive memory only if it reduces independently
  verified charged work beyond the fixed alternating/two-rung controls without
  using dataset identity or order leakage.

## Verification

- **Source pointers checked:** Required project context, adaptive-restart
  literature, README/main, and both measured sibling notes.
- **Checks last run:** `make note-audit` passed on 2026-08-20; focused LaTeX
  build not rerun because no theorem source was changed.
- **Known gaps:** The README omits the memory admissibility test, caps, and
  order dependence. O'Donoghue-Candes restart is global motivation only and
  does not certify this local feedback rule. Taxonomy currently records no
  empirical dependencies.
