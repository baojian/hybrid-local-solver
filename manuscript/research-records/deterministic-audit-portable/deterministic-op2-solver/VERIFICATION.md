# Verification record

The main continuation proof was developed by the parallel task **Prove
conjecture 2 deterministically** and independently audited here. The audited
argument proves the requested OP2 work bound in the supplied exact-real word
model. The accompanying report supplies the Dirichlet restriction and
practical refinements used by this package, including a bounded-rational
implementation. This is a mathematical proof audit, not machine-checked
formal verification.

All inputs and experiments were deterministic. Exact rational verification
was used for the checks below. Full-graph optima used to verify outputs were
computed by external audit tools. The implemented tiny component branch
separately charges its own constant-size factorizations. No verification
computation is an uncharged subroutine of the local solver.

| Check | Completed scope |
|---|---:|
| Two energies, selected flow and every-prefix work bound | 576 stage cases; 18,432 iterations |
| Projection sectors, including upper faces and active mass cap | 16,100 cases |
| Both perturbed energies and selected flow, including Dirichlet matrices | 16,128 cases; 1,012 active caps; 266 upper-face cases |
| Fixed-degree-pruned continuation and safe stage baselines | 72 cases; 17,652 iterations; 216 stages |
| Independent exact box/cap projection comparison | 5,184 cases |
| Full fast-solver objective and support checks | 54 cases, repeated after major updates |
| Zero, diagonal, loose accuracy and fixed-horizon branches | 5 special cases |
| Integer/rational continuation trajectory equivalence | 12 cases; 768 iterations |
| Integer and source-energy continuation wrapper comparisons | 32 cases |
| Boundary-forest spectral bound | 5,652 exact PSD checks; 6 longer paths |
| Common-denominator PG norm upper bounds | 875 cases |
| Exact sparse PG point versus independent full product | 576 points |
| Checkpoint continuation and all original graph replies | 126 cases; 294 stages; 1,746 checks |
| Accepted and rejected bounded pilots | 144 cases; 74 accepted pilots; 4 rejected pilots |
| Integer/rational component trajectory equivalence | 96 cases; 6,144 iterations; 323 active-cap steps |
| Complete integer/rational fast-solver equivalence | 32 cases |
| Ordinary rational output, independent objective intervals | 384 cases; 780 converted records |
| Tiny exact obstacle versus independent active-face enumeration | 3,699 cases |
| Tiny completed paths at alpha=1e-20 and 1e-80 | 8 exact full-solver cases, up to 16 vertices |
| Portable standard-library test suite | 17 tests |

The integer component trajectory and full solver comparisons were repeated
after adding the certified inactive-cap shortcut. They still matched exactly.
Those trajectory comparisons disable the optional tiny exact solve, keeping
the intended accelerated-path coverage. The tiny branch has its own exact
face-enumeration and extreme-parameter checks.
The readability formatting pass was checked by comparing Python syntax trees;
all thirteen then-existing module syntax trees were unchanged. The later
rational-output module was checked separately against independent full
optima and exact rational objective intervals.

## Targeted difficult cases

- A PG step activates a vertex of original degree `2**100`, while the check
  scans only the old candidate's single adjacency entry.
- A misleading branch spends the discovery budget away from part of the
  optimum. The restricted pilot is rejected by its global certificate, and
  continuation completes the task correctly.
- Large integer labels, non-dyadic rational parameters, source-mass caps,
  permanent degree pruning, and original-degree normalization are exercised.
- Fixed-horizon modes are tested separately from early stopping, so the
  worst-case guarantee is not based on empirical early termination.

## Structured performance measurements

These are Python process measurements on the task host, with exact symbolic
KKT checks on all omitted vertex classes. They are examples, not uniform
wall-clock guarantees or comparisons with optimized third-party software.

| Instance | Result |
|---|---|
| Retained path32 with enormous excluded hubs | 94 original entries; 64 component iterations |
| One-boundary retained paths16/64 | 31/127 original entries; 1,024/4,096 iterations across three alpha values |
| Billion-vertex retained path with excluded hubs | 254 original entries; globally certified bounded pilot |
| Ordinary trillion-vertex path, rho=1/256, alpha=1e-8 | 255 original entries; 8,192 iterations; about 4.7 seconds with the final integer component loop |
| Complete path16, alpha=1e-80, strict objective target | Exact optimum in 16 pivots and about 0.19 seconds; 30 original entries |

On the last ordinary-path instance, the rational component loop took about
55 seconds and produced the exact same output. The pilot on the billion-path
example also passed at alpha=1e-12. An earlier checkpoint-only continuation
benchmark was intentionally stopped during its alpha=1e-12 case; no completed
result is claimed for that unfinished run.

## Scope

The guarantee applies to the unit, finite, simple, connected, undirected graph
and original-degree convention stated in the README and manuscript. The
provided OP2-to-semantic-PPR parameter conversion gives OP1 as described in
the report. This work does not claim the separate OP3 nested-SDD reuse bound,
weighted-graph extensions, or a convergence theorem for earlier abandoned
candidate algorithms.

The graph input contract matters. The solver validates encountered degree
values and row lengths but does not perform a global input-validation scan.
Ordinary unchecked floating-point execution is not the certified algorithm.
Decimals printed in examples and benchmark tables are display conversions
after exact decisions and checks.
