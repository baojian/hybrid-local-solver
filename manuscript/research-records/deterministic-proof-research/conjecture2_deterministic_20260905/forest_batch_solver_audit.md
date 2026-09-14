# Exact forest-preconditioned batch prototype: audit and validation

Status: implemented and tested using rational arithmetic only. The general
OP2 conjecture remains open. Files are fresh task artifacts outside the
manuscript; no other manuscript notes were read.

## Algorithm and structural guarantee

`forest_batch_solver.py` is self-contained apart from the Python standard
library. The source graph belongs to an adjacency oracle. The solver can
request one degree or one adjacency list; it never enumerates source vertices
or requests the source graph size. Admitted adjacency lists are cached once.

Each batch materializes the current induced graph, builds a deterministic
spanning forest, and factors

    T=alpha*D+c*diag(d-d_S)+c*L(F),  c=(1-alpha)/2.

The external-degree grounding term is included. Leaf elimination stores
positive rational pivots kappa_i and factors c/kappa_i. A backward pass and
a forward pass apply T^(-1) without square roots. Both construction and each
application take O(vol(S)) logical work.

The principal matrix satisfies `H=T+c*sum_chords b_e*b_e^T`. Consequently
exact PCG terminates within `min(|S|,r(S)+1)` iterations, where r(S) is the
induced cyclomatic number. The code checks this limit and recomputes the
actual principal residual after termination. It warm-starts with the
preceding principal solution, extended by zero, but the rank bound does not
depend on that choice.

Every strictly positive outside residual is admitted in the next batch.
Exact Stieltjes comparison therefore keeps every admitted coordinate inside
the true optimal support and every restricted solution coordinatewise below
the optimum. Boundary accumulation scans cached active rows, queries only
previously unknown boundary degrees, and never recursively scans a boundary
vertex. Positivity of every solved admitted coordinate is also checked.

Per batch the work is O((r(S)+1)vol(S)). With r* the cyclomatic number of the
unknown final optimal support, the proved batch-decay theorem gives

    tilde O((r*+1)/rho *
        [1+alpha^(-1/2)*log_+(2alpha/epsilon)]).

This meets the requested form on supports with polylogarithmic cycle rank.
The prototype does not assume that this holds on a general graph.

## Fully rational stopping

The code computes two independent exact objective certificates.

First, for outside degree-coordinate residuals r_i>0, the minimum-norm
original-objective subgradient has entries `-r_i/sqrt(d_i)`. Inside the
principal support it is zero. Strong convexity therefore certifies

    objective gap <= sum_(outside r_i>0)r_i^2/d_i/(2alpha).

All nonzero terms are on the accumulated boundary. If there are none, the
current answer is the exact optimum.

Second, the exact batch theorem bounds stage-T gap by
`2alpha*q^(2(T-1))`, where `q=(2-sqrt(alpha))/(2+sqrt(alpha))`.
To avoid irrational arithmetic and floating-point logarithms, the code finds
a dyadic ell with `sqrt(alpha)/2<ell<=sqrt(alpha)` using rational square
comparisons. It uses `q_bar=(2-ell)/(2+ell)>=q` and updates
`2alpha*q_bar^(2(T-1))` rationally. This gives the same accelerated stage
count within a factor two: `q_bar<=exp(-ell)`. Either certificate can end the
run. The diagonal alpha=1 case is solved from the seed degree without any
adjacency query. The zero regime and a sufficient zero-vector objective
certificate also avoid adjacency queries.

The canonical output consists of pre-materialized triples `(i,y_i,d_i)`;
each represents the exact requested coordinate `x_i=y_i*sqrt(d_i)`.

## What the counters mean

The reported counters instrument graph replies, first adjacency entries,
repeated cached and internal neighbor visits, boundary tests, factor builds,
tree applications, PCG iterations, arithmetic, comparisons, selected explicit
state accesses, control events, and output materialization. Numeric operands
and results are charged by the arithmetic wrappers. Repeated neighbor visits
also incur state and control charges; their diagnostic tallies are not added
again to the total. Batch-history records and final radical records are
materialized and charged.

`total_logical_work` is the sum of these instrumented exact-real events. It is
not a complete count of Python bytecodes, allocations, hashing internals,
test-oracle work, or Fraction bit operations. The Python maps use integer
keys; the mathematical implementation can substitute deterministic balanced
maps with the stated logarithmic overhead. No worst-case constant-time hash
claim is made. Exact Fraction operation costs can grow substantially with
numerator and denominator bit length.

## Independent deterministic validation

Command from the task research directory:

    python3 test_forest_batch_solver.py --report forest_batch_verification.json

The final run passed all five test methods:

* 1,028 exact obstacle batch cases, checked against the existing independent
  exhaustive support-enumeration/dense rational KKT oracle.
* 420 arbitrary principal systems, including disconnected principal sets,
  checked against independent dense Gaussian elimination; each tree inverse
  was separately checked against its explicitly formed grounded forest matrix.
* Every connected labeled graph through four vertices (43 graphs), multiple
  seeds and rational parameters; paths, stars, binary trees, cycles, a wheel,
  two joined triangles, and a clique.
* A wrapper rejects global graph enumeration and graph-size queries. A
  degree-100 unadmitted hub receives a degree query but no adjacency scan.
  Zero and diagonal cases issue no adjacency queries.

Maximum observed values were 9 batches, 5 PCG iterations in a batch, induced
cycle rank 10, and 18,798 instrumented logical work units in an obstacle run.
Every forest principal solve used at most one PCG iteration. The JSON report
contains the fixture details. All graph choices, arithmetic, and independent
oracles are deterministic; there is no floating-point or randomized mode.
