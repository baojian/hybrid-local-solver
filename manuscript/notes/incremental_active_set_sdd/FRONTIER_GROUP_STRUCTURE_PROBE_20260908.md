# Structural type bound and branching test for response groups

**Next targets, awaiting implementation audits and formal proof.** The
general paid grouped producer is already proved as a draft and implemented
in `sec:op3-frontier-response-groups` / `FRONTIER_GROUPS_AUDIT.json`.
General OP3 remains Open. Do not infer a small response-group count from
the star example.

## A type-count promise that does not supply preprocessing

For an uncolored original graph, global twins satisfy
N(u) minus {v} = N(v) minus {u}. A partition into k such types is the
standard neighborhood-diversity parameter. The checked primary source is
Michael Lampis, *Algorithmic Meta-Theorems for Graphs of Bounded Vertex
Cover*, arXiv:0910.0582v2, 4 November 2009,
https://arxiv.org/pdf/0910.0582v2. Definitions 1-2 are on PDF p.4;
Theorem 5 on pp.12-13 gives the clique/independent-set and complete/empty
inter-type description. The source's global partition computation and
logical model-checking algorithms are not local PageRank algorithms and
are not imported here. The older author-hosted URL returned 404; use the
verified arXiv version and its title, rather than merging publication metadata.

Proposed invariant: after the seed is admitted, all remaining members of
each global type are either undiscovered together or contained in a single
live response group. The first admitted neighbor of any type exposes all
its remaining members in one original row. Every subsequent partition
refinement treats those members identically, because their adjacencies to
the newly admitted vertex agree. Existing groups can combine types but
cannot split a still-unadmitted type. Therefore completed-state groups
are at most k, and transient groups including empty parents are at most
2k+1. This would give O((1+V)(k+1)^2 log(2+V)) local work, without the
algorithm knowing k or its global partition. Check the source type
exception at the initial seed and true-twin clique types carefully.

Test arbitrary quotient graphs, mixtures of clique and independent types,
unequal type multiplicities, all source types and original degrees.
The type partition is validator-only information. Large ambient types
must still obey the pre-row original-volume guard. The final structural
claim should be distinguished from the earlier multipartite and tree
results, which already cover special cases.

Optional subsequent extension: allow kappa=0 with the same positive-pivot
rule to return the exact lambda obstacle. It needs its own parameter
contract and exact KKT audit before an exact RPPR statement is made.
Current implemented default is kappa=lambda/2 and remains ACL-only.

## Candidate cubic obstruction for this live-list group order

Use a finite complete binary tree of depth D=4R+8, root seed, R>=1.
Its actual leaves have degree one; all reached nonroot vertices in the
following prefix have original degree three. Put

    lambda = 1/(64*2^R), eps_appr=2*lambda,
    t=1-gamma = 1/(64*8^R), alpha=t/(2-t).

For the complete admitted ball S_r of depth r<=R-1, its original volume
is v_r=3*2^(r+1)-4. In the conservative Dirichlet face, radial edge flux
across level k is 1-lambda*v_(k-1)>0. The outside frontier residual is

    x_r = (1-lambda*v_r)/2^(r+1) >= 61/(64*2^R).

The whole conservative face is positive and its maximum is below one,
since its root potential is bounded by the sum of 2^(-k-1) through r.
Let L be this proper Dirichlet matrix and x0 its face solution.
With M=L+t*A, the vector v=x0-t*L^-1*A*x0 satisfies
M*v=b-t^2*A*L^-1*A*x0<=b. The Dirichlet torsion bound
||L^-1*d||_infty <= vol(S_r)^2 <=9*4^R therefore gives

    x0-9/(64*2^R) <= x_gamma <= x0,
    gamma*x_gamma(r) >=51/(64*2^R).

This is well above the degree-three admission threshold
(lambda+kappa)*3=9/(128*2^R). The lower comparison is positive and hence
also proves positivity of these damped face solutions. Verify every sign
and the original-degree boundary mapping in a formal argument.

If correct, every vertex through depth R is eligible by the time the
previous complete level has been admitted. Monotonicity and the producer's
first-eligible-group rule then force breadth-first order through that
prefix. Each original row adds two fresh children and no old-member split.
While processing the 2^R vertices of level R, at least 2^(R-1) nonempty
groups remain, each encoding siblings. Thus the implementation explicitly
makes at least 2^(3R-3) shared matrix-entry updates in this prefix alone.
Its eventual admitted volume is between v_R and 1/lambda, so is Theta(2^R)
and Theta(1/eps_appr). The ambient graph volume exceeds 4/eps_appr.

Audit with a private lazy finite-tree oracle and an explicit prefix cap;
do not materialize its enormous ambient graph or label a capped nonterminal
prefix as a completed ACL solve. Check independent radial Dirichlet
solutions and group/ordering/count identities at modest R. Symbolic large-R
inequalities are proof checks, not executed large local solves. Such a
result would refute the cubic-to-linear inference for this particular
group representation and order, while leaving depth-first, low-rank,
persistent tree and general OP3 methods available.
