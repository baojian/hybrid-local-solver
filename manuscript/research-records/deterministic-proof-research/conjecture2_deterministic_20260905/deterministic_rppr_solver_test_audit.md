# Independent exact verification of the continuation wrapper

The fresh `deterministic_rppr_solver.py` was inspected and tested without
editing it. `test_deterministic_rppr_solver.py` instruments each constructed
corrector through a temporary test-only subclass, records its materialized
pre-repair output, and checks the wrapper's stage summaries and final output.
The production algorithm receives only a degree/adjacency oracle whose input
mapping prohibits global enumeration.

All five test groups passed. The saved
`deterministic_rppr_solver_verification.json` records 24 exact cases, 38
repaired stages, and 1,398 ordinary correction iterations.

## Mathematical checks

For every small-graph stage, an independent dense rational oracle exhaustively
enumerates candidate KKT supports and solves their principal systems by
Gaussian elimination. An independently assembled full quadratic checks:

* The materialized pre-repair objective gap is nonnegative and no larger
  than the stage's certified gap, which is no larger than its requested gap.
* The repair is exactly the positive part after subtracting the prescribed
  density shift. It is coordinatewise between zero and the exact optimizer.
* Its coordinate density error is at most `(1+alpha)*delta`, its objective
  gap is at most `2*delta^2/rho_stage`, and its support volume is at most
  `1/rho_stage`.
* The repaired source satisfies `0<=b-Qbar<=2*alpha*rho_stage*w` on every
  graph vertex, including inactive boundary coordinates.
* The next corrector's source is exactly the dense reconstruction and is
  bounded by `4*alpha*rho_next*w`. Its mass equals
  `alpha*(1-mass(baseline))`; its record count is at most twice the baseline
  support volume plus one.
* The final output is a safe under-approximation and its actual objective
  gap is at most the returned certificate, which is at most epsilon.

The dyadic schedule, exact requested gap `alpha^3*delta^2/2`, dyadic rational
momentum, and every epsilon-induced final halving are checked independently.
Five cases use alpha different from theta squared; six reach a final
regularization that is not half the preceding level. The suite includes
all connected graphs on two and three vertices with every seed, plus paths,
stars, and a small tree. Parameters include alpha `2/5`, `1/8`, `1/100`,
`17/19`, and `1/3`; zero-at-equality, zero-above-threshold, and alpha-one
branches are checked separately.

The wrapper's additional initial-energy cap of one is consistent with the
analytic interface: if `e=x*_rho-bar>=0`, then both vectors are supported
inside the optimum support, so `gap(bar)=e^TQe/2`. The initial mirror term
is at most this gap. Since `mass(e)<=1`, `w_i>=1`, and `Q<=I`,
`E0<=e^TQe<=||e||_2^2<=1`. Thus taking the smaller of this bound and the
source-based bound is justified.

## Graph and state accounting

Each stage's measured degree queries are distinct and equal its degree
counter. Each first adjacency query is distinct within that stage; its
entry count equals the saved first-read counter. The total repeated scatter
count is exactly

`baseline support volume + cumulative kinetic support volume`.

The source-refresh counter equals `(iterations+1)*source_records`; projection
emissions equal the sum of actual selected record counts. The test also
reconciles projection queries, materialized output words, repaired input and
output records, final output words, and all wrapper-level degree queries.

The large locality fixture is a 1,001-vertex star with a leaf seed, alpha
`1/4`, rho `1/10`, and epsilon `1/1000`. Its closed-form seed-only optimizer
is independently checked against all KKT inequalities, avoiding exponential
test-oracle enumeration on this deliberately large graph. All four stages
query only the seed and hub degrees. The hub has degree 1,000 and its
adjacency is never scanned. There are four adjacency queries in total, all
for the seed, and the final certificate is `1/1280`.

## Exact-arithmetic scope

There was no production-code defect detected. An initial test run failed
only while formatting a large exact gap for JSON; the mathematical assertions
had already passed. The test logger now records numerator and denominator
bit lengths for large fractions, while all comparisons remain exact.
For alpha `1/100`, the final gap denominator has 16,418 bits after 736
iterations across two stages. This illustrates why the prototype is finite
exact verification rather than a claim about practical rational bit cost.

The suite checks the implementation and its certificates on these inputs.
The general operation bound is the separate analytical theorem, with balanced
comparison maps in the exact-real word model; finite tests are not a proof
of that asymptotic statement.
