# From the proof to the implementation

Read `report/deterministic_op2_audit.pdf` for the complete argument and
`README.md` for the graph contract and public API. The recommended call is
`solve_fast`; `solve_explicit` additionally returns ordinary rational
x-coordinates. Function names below can be searched directly in the code.

| Mathematical responsibility | Implementation | Work that must be charged |
|---|---|---|
| Fixed final degree restriction with original degrees | `component.py: CachedOracle`, `_integer.py: _expose, _row` | Degree replies, every original incidence including excluded neighbors, cache access |
| Bounded seed-region discovery | `component.py: discover_component` | Original scanned volume at most `1/rho`, queue and tree records |
| Exact solve on at most sixteen completed vertices | `_tiny_obstacle.py: solve_tiny_obstacle` | Matrix assembly, all LDL updates, face solves and violation scans; enforced constant size |
| Boundary-forest spectral lower bound | `component.py: forest_spectral_bound` | Deterministic heap operations, every internal relaxation, root-load accumulation |
| Component/pilot acceleration and global acceptance | `component.py: solve_fast` | Region products, projections, failed and successful certificates, discarded pilot and fallback |
| Integer component recurrence | `_component_integer.py: IntegerComponentCoupling.step` | Every region record, internal incidence, integer floor and active-cap tree update |
| Diffuse-source continuation | `_integer.py: solve_rppr_integer`, `IntegerDyadicCorrector` | Stage initialization, baseline scans, exact source construction and every executed step |
| Source-dependent initial-energy schedule | `_source_energy.py: SourceEnergyDyadicCorrector` | Full source pass, common-denominator upper square sum, schedule comparisons |
| Finite box/cap threshold reporter | `_integer_reporter.py: IntegerClippedReporter` | AVL point updates, weighted tails, rank/breakpoint searches and emitted records |
| Bounded rounding and scalar rebases | `_integer.py: step, _rebase` | State floors and every retained scalar record at each rebase; no free history sweep |
| Full-problem PG checkpoints | `_integer.py: _projected_gradient, _run_with_checkpoints` | Candidate materialization, repeated candidate-row scans, degree lookups, norm aggregation |
| Safe terminal clipping | `_integer.py: _terminal_repair` | Exact PG unless reused, downward grid rounding, monotone baseline merge and output |
| Ordinary rational coordinate output | `explicit.py: solve_explicit` | Tolerance reservation, square-root interval comparisons and every emitted coordinate |

The core acceleration proof uses **two** potentials. The ordinary energy
proves the objective rate. The second energy bounds the actual squared
matrix response; its selected signed-flow argument pays the cumulative
kinetic-support volume. The code does not compute the analytical inverse
source comparator or the larger optimum support at half the regularizer.

The degree-pruned matrix is a fixed Dirichlet restriction. Its degrees are
never recomputed from the inspected subgraph. The second energy therefore
uses `lambda * (M w)^T xi` in the proof. Replacing this with the full-graph
identity after pruning would be incorrect.

A successful partial pilot is accepted using the original strong-convexity
bound `alpha` and a full-problem PG certificate. The stronger local forest
bound controls only the restricted iteration. Likewise, a continuation PG
checkpoint certifies its PG point; the stage summary identifies that point
explicitly. These distinctions are part of the correctness argument.

The persistent graph maps and threshold structures are deterministic AVL
trees. Fixed-schema diagnostic dictionaries are not the graph-state data
structure. Runtime decisions use exact rational/integer comparisons; there
is no sampled sparsifier, randomized solve, randomized pivot or retry.

The counters expose meaningful work categories but are not a complete Python
instruction trace. The report supplies the asymptotic full ledger, including
temporary storage and repeated inspections. `VERIFICATION.md` and `audits/`
separate proof obligations from finite checks and measured examples.
