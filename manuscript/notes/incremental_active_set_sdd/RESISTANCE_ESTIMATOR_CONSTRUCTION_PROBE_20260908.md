# Cycle solves, resistance estimates and the weighted constructor

**Fifth-block update:** The ordinary-solve resistance sketch and bounded
core sparsifier now have implemented constructions and note-local proof
drafts in `sec:op3-ordinary-solve-resistances` and
`sec:op3-bounded-core-sparsifier`. The final full runs pass, including large relative-weight stress cases. The corrected one-cycle
base now passes 72 exact solves; the nine general prescribed solve
fixtures use 2,643 total updates. Earlier checkpoint counts below are
historical.

The constructor conclusion is now `cor:op3-weighted-constructor-contract`:
quality O(m L^2/j), O(j L) core edges, and paid word work
O(m[L^6+log(weight_ratio)]) for arbitrary positive input weights. It uses the
explicitly checked Abraham--Neiman source tree. The code does not
implement that source tree algorithm. The final full supplied recurrence
still requires explicit failed-execution cap reconciliation; general
OP3 and potential-driven local discovery remain Open.

The completed design text below records the derivation. For current
claims and hashes, use the new proof sections and final audit JSONs.

**Fourth-block update:** Fair-bit sampling and the heavy-path cycle backend
are now implemented and have note-local proofs in
`sec:op3-fair-bit-sampling` and `sec:op3-weighted-cycle-solver`. The sampler
passes 140,860 terminal-interval checks. The cycle backend passes 276
state cases, 3,488 exact sampled-cycle identities, 3,456 large-tree
path/work checks, and nine fixed-budget solves with 2,808 total updates.
Its input error/failure budget also passes 27 scalar stress cases.
Read the current audit JSONs for source/backend hashes. The design below
is retained; the remaining unimplemented target is the ordinary-solve
resistance sketch and its complete core-sparsifier composition.

**Historical design below; the constants have now been proved and audited.**
The supplied-tree weighted constructor is now proved and audited in
`sec:op3-weighted-corridor-routing`. Its 27,961 constructions and 55,706
exact PSD checks match source SHA-256
`2042b6b2666bedbc78480454e754fec3224878d756d9ec33cf8a000b50b22581`.
The remaining source obligations are an arbitrary-weight low-stretch tree
and a core sparsifier with requested failure probability and charged work.

## Source review and choice

Abraham–Neiman's Theorem 1 and weighted extension supply a tree with
W=O(m log n loglog n) in that work, with no expectation qualifier. Their
shortest-path denominator only strengthens our original-edge denominator.

KLP arXiv:1209.5821v3 has a global footnote on PDF p.1: all sparsification
algorithms are randomized, with inverse-n failure, and displayed running
times omit output generation. Lemma 3.4 uses a symmetric approximate
inverse operator. The current notes must not silently turn ordinary
right-hand-side solves into that stronger interface. KMP's chain source
is independent of the right-hand side, but its explicit failure/cap and
small-core restrictions would still need reconciliation. This route is
available but is no longer the only candidate.

Kelner, Orecchia, Sidford and Allen Zhu, *A Simple, Combinatorial Algorithm
for Solving SDD Systems in Nearly-Linear Time*, STOC 2013, provides a
simpler alternative. Primary source:
https://arxiv.org/pdf/1301.6628v1 (only arXiv version, Jan.28,2013).
PDF cache `/tmp/op3-kosz13.pdf`, SHA-256
`bd78a2436636c41e27a34803dc1d4efa9929c7c2a0a534e1366ce646b9a0d669`.
Theorem 3.2 on p.7 gives expected energy and potential-norm error;
Algorithm 1 and Theorem 4.1 on p.8 give the fixed iteration count and
geometric energy contraction. Lemmas 6.1/6.2 on pp.13–14 connect the
tree-supported initial flow and final tree potentials to the optimum.
Pages 7,8,14 have been rendered and visually checked. This is a supplied
graph source; it does not discover a local support.

## Implemented target: a simple paid cycle-update backend

This backend is now implemented. It uses a heavy-path decomposition and
a lazy segment tree, accepting O(log^2 n) per cycle instead of the
source's O(log n). That extra logarithm is harmless for the intended
supplied polylogarithmic recurrence and is easier to audit directly.

Orient stored tree flow t_v from child v toward its parent. For demand b
with sum b=0, initialize t_v to the sum of b in v's subtree. Root
potential is zero and v_u=sum_{f on root-to-u} r_f*t_f. An off-tree edge
e=(u,v), oriented u to v, has separately stored flow f_e and cycle
resistance R_e=r_e+r(T(e)). Let

    Delta = r_e*f_e - (v_u-v_v), a=Delta/R_e.

Update f_e -= a, add a to the tree root path of u, and subtract a on the
root path of v. This preserves divergence and zeros the sampled cycle's
voltage sum. Tree queries store sum(r_f*t_f); a range flow increment a
adds a*sum(r_f) using a static resistance sum and a lazy coefficient.
Every input array, heavy-path index, segment-tree cell, traversal, query,
update, call frame, copy, sample and final potential record is charged.

Let tau=sum_{off-tree e}(R_e/r_e)=W+m-2n+2. For a tree graph tau=0 and
the initial potentials are exact. Otherwise tau>1. Source contraction
and voltage rounding imply

    E ||v_K-L^+b||_L^2 <= tau*W*(1-1/tau)^K * ||L^+b||_L^2.

The squared-error form follows from the pointwise voltage-rounding
lemma before taking expectations; it is stronger than merely squaring
the source's expected-norm statement (which would be invalid).
For relative norm error eta and failure delta, choose at least
tau*log(2*tau*W/(delta*eta^2)) updates and allocate delta/2 to Markov
failure. Compute a conservative integer budget by paid doubling and
comparisons. With an AN tree, this is m times polylogarithmic factors.

## Remove an exact random-real / huge-integer sampling assumption

The existing confidence audit uses a common-denominator integer CDF as
a labelled reference. Add a production fair-bit sampler for arbitrary
positive real-word probabilities. Store their cumulative sums explicitly.
Generate a dyadic interval [a/2^k,(a+1)/2^k) for a uniform point by fair
bits. Binary-search which CDF intervals contain its endpoints. Once the
whole dyadic interval lies in one category, return that category.

After k bits, at most m-1 CDF boundaries can leave ambiguity, of total
probability at most (m-1)/2^k. Thus expected bits are O(log(2+m)).
For N known draws, cap each at B>=log2(2*m*N/delta) and return FAIL if
still ambiguous. A union bound allocates at most delta/2 additional
failure. Returned draws couple to exact independent categorical samples;
do not claim their distribution conditional on successful termination
is unchanged. Bounded work is O(N*B*log(2+m)), with all fair bits and
dyadic arithmetic counted. Handle CDF endpoints and dyadic ties exactly.

## Resistance estimates from ordinary approximate solves

No symmetric or fixed linear inverse operator is needed for this route.
Normalize c'_e=c_e/c_min, and call the corresponding Laplacian L'.
For each c'_e>=1, find a power-of-two bracket for its square root by
doubling, then use eight bisections. The upper endpoint s_e satisfies

    sqrt(c'_e) <= s_e <= h*sqrt(c'_e), h=257/256.

This uses only arithmetic and comparisons, O(1+log(c_max/c_min)) per
edge, not an exact square-root primitive. Generate q=512 independent
Rademacher rows a. For each, form b=B^T diag(s) a in O(m+n) work and
obtain an approximate solution x_hat with relative energy error
eta=1/(128*m). Use a supplied-solve failure delta_s<=1/(16*q), so all
q solves in a group are good with probability at least 15/16.

For a fixed queried original edge e, the exact sketch value has second
moment R'_e <= E Z_e^2 <= h^2 R'_e and fourth moment at most three
times the squared second moment. Therefore its q-row mean square is
within 1/8 of that second moment with probability at least 3/4.
For every sign row, ||L'^+b||_L' <= h*sqrt(m). Energy Cauchy–Schwarz
bounds the Euclidean sketch error by eta*h*sqrt(m)*sqrt(R'_e), even
when solver error depends on its right-hand side and is nonlinear.
The deliberately conservative rational bounds to check are

    (7/8-h/128)^2 >= 3/4,
    h^2*(17/16+1/128)^2 <= 5/4.

Thus each group estimates a fixed edge within 1/4 with failure at most
1/4+1/16=5/16, without needing independence between its good-solve and
good-sketch events. Independent groups and coordinatewise medians turn
this into joint probability >=3/4 for every original edge. For example,
with g odd and g>=32*ceil(log2(4*m)), the elementary majority bound
(sqrt(55)/8)^g <= exp(-g/16) is sufficient. Verify these constants,
including the choice of Markov and sampler budgets, before formalizing.
Rescale resistance estimates by 1/c_min, then use the existing median
and matrix-Chernoff wrapper with the new bounded fair-bit sampler.

## Required audits and completion gate

1. Exact heavy-path query/update comparisons against explicit tree flows,
   including long paths, shared roots, signs and extreme positive weights.
2. Exact one-step divergence, cycle-voltage and expected-energy identities;
   compare final potentials to dense grounded solves on small graphs.
3. Fair-bit sampler interval partition, boundary ties, capped failure
   counts and coupling on exhaustive short bit strings.
4. Square-root brackets, Rademacher second/fourth moments, all-edge sketch
   perturbation bounds and adversarial but admissible nonlinear solve errors.
5. Actual error/failure/work composition for the core sparsifier and AN
   constructor. Preserve Conditional status until all of this is reconciled.

No full general local-discovery claim follows from any of these supplied
primitives. Return to potential-driven discovery after this separate
constructor obligation is closed or a specific obstruction is found.
