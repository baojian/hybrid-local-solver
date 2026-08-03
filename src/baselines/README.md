# Baselines

This package contains shared reference implementations used in experiments.
Baselines will be added one at a time.

All agents may import, run, test, and benchmark this code. Existing baseline
behavior should be modified only to correct a verified defect or in response to
an explicit request. Keep corrections narrow and protect them with focused
tests so comparisons remain reproducible.

## Classical APPR

[`appr.py`](appr.py) is the explicit reference implementation of the lazy
Andersen--Chung--Lang push algorithm. It uses the degree-normalized activity
test `r[u] >= eps_appr * d[u]` and charges `d[u]` adjacency-list work per push.
FIFO, LIFO, maximum-residual-ratio, and seeded-random legal orderings are
available so ordering-independent theory can be checked without changing the
update rule. During the cross-check, the older Numba kernel in `sdd_solver.py`
was found not to re-enqueue a pushed vertex whose retained residual remained
active and to omit the final partial round from its reported work. Its frontier
and accounting paths were repaired narrowly, and its FIFO output and total
work are now checked against the reference implementation in the test suite.
