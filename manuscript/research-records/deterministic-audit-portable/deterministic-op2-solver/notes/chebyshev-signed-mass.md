# Chebyshev propagation does not have a uniform signed-mass bound

2026-09-05. This is an exact obstruction to one literature assumption, not
a lower bound against deterministic OP2 algorithms.

Let G be the finite rooted b-ary unit tree of depth at least k, with b>=2,
and let P=A D^{-1} act on probability-mass columns. Write r=e_root. Every
vertex of distance k from the root has zero coordinate in P^j r for j<k.
The leading coefficient of the Chebyshev polynomial T_k is 2^(k-1), for
k>=1. Therefore, on the distance-k level, T_k(P)r equals
2^(k-1) P^k r and is nonnegative.

The total probability mass of P^k r on that level is (b/(b+1))^(k-1):
the first step always goes outward, and each of the next k-1 steps goes
outward with probability b/(b+1). Hence

    ||T_k(P)e_root||_1 >= (2b/(b+1))^(k-1).

This grows exponentially in k for every b>=2. Also 1^T T_k(P)r=T_k(1)=1,
so the total negative mass is at least (2b/(b+1))^(k-1)-1. Boundary degrees
do not affect this calculation because an outward k-step trajectory does
not depart from a depth-k vertex.

The primary paper [Scaling Up Graph Propagation Computation on Large
Graphs: A Local Chebyshev Approximation Approach](https://arxiv.org/abs/2412.10789)
assumes a uniform l1 bound on these polynomial propagators in its local
analysis (Assumption 1). Its local complexity statement also has a K^2
dependence on truncation length. Neither that assumption nor the stated
complexity supplies the graph-uniform root-condition local bound required
by OP2. Its error-feedback recurrence remains a potentially useful algebraic
idea, but would need an independently valid work analysis in this setting.
