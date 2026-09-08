# Next local targets after the supplied solver

The sixth third-campaign block proves a complete source-backed supplied
VWF recursion in `thm:op3-complete-supplied-recursion`. General OP3 is
still Open. Continue with the tasks below, distinguishing new proposals
from proved results and keeping every graph query and repeated operation
charged.

## 1. Make the supplied-envelope work reduction explicit

Use the existing significant-envelope theorem with lambda=eps_appr/2,
delta=eps_appr/8. Given U containing all exact obstacle coordinates
above delta, with original volume V, show that the now-complete supplied
solver produces original ACL output in

    (1+V) polylog(2+V+1/alpha+1/eps_appr+1/p).

Read every original row in U and obtain its original degree. Construct
the induced graph by paid sorting/membership maps, preserving full degrees
in the diagonal. No outside adjacency list is read. All components away
from the physical seed have zero restricted optimum; process the seed
component and directly handle the scalar/empty cases. The restricted
matrix is gamma*L_induced + diag(d_i-gamma*d_i_induced), so grounding
is at least bar_alpha*d_i. Use B=1, mu=bar_alpha and the size-two capped
VWF embedding with U_B=1/bar_alpha. Target absolute energy gap
bar_alpha*delta^2/2, box, then clip downward by delta. The existing
envelope/ACL corollary supplies the full original residual certificate.

Start with the sharp seed-only gate. If it fails, then

    eps_appr*d_v < gamma/(1+gamma), hence gamma > eps_appr.

This prevents a hidden log(1/(1-alpha)) in the edge-weight scale as
alpha approaches one. Alpha=1 is already covered by the gate. On the
remaining supplied component, original degrees, total grounding, edge
weight sum, terminal slopes, cap radius, energy bound and inverse target
are polynomial in V, 1/alpha and 1/eps_appr. Check each initial Z
quantity explicitly. A finder costing ~O(1/eps_appr) and returning
V=O(1/eps_appr) would then leave no separate supplied-solver hypothesis.
It still would not constitute a fast finder or literal reuse of every
exact nested face.

## 2. Potential cap and a small-alpha reduction: proposed, not yet audited

A possibly useful new direction emerged during cap verification.
For ANY nonnegative ACL potential x with r=e_v-M_gamma*x >= 0,
sum over a strict superlevel set H of x. Its boundary gradients have
one sign, and

    bar_alpha*sum_H d_i*x_i + gamma*sum_cut(x_i-x_j)
      = 1_{v in H} - sum_H r_i <= 1.

This appears to imply gamma*|x_i-x_j| <= 1 on every edge. If the
positive support is proper in the connected ambient graph, a path from
a maximum coordinate to a zero has at most |supp(x)| edges, giving

    max(x) <= |supp(x)|/gamma.

For the exact lambda-obstacle, support volume <1/lambda then gives
max(x) <= 1/(lambda*gamma), independent of alpha. Verify the proof,
including ties, disconnected claimed positive sets and the full-support
exception, with exact original-graph tests.

If gamma_target >= gamma_eff (target alpha smaller), the SAME candidate
has target residual

    r_target = r_eff + (gamma_target-gamma_eff)*A*x.

Thus an eps_appr/2 ACL candidate at an effective alpha on the order of
eps_appr/B transfers to target accuracy eps_appr whenever its proper
support has at most B vertices (a known volume bound is stronger). For
an exact lambda-obstacle with lambda on the order of eps_appr, this
suggests an effective-alpha floor on the order of eps_appr^2. If the
support is the entire connected graph, a supplied solve at the original
alpha may be affordable WHEN the materialized original support volume
is already O(1/eps_appr). Detecting that case requires charging its rows.

Do not silently assume a generic sparse ACL algorithm has an original
support-volume bound: output word count and degree volume are different.
State the needed output/access contract explicitly, or first prove an
appropriate wrapper. This reduction would isolate the hard regime near
alpha~eps_appr^2; it would not itself give the target local algorithm.
A same-vector substitution with a much larger floor may fail on paths;
check a precise witness rather than claiming a general lower bound.

## 3. Concrete finder/event directions

The prior FIFO-BFS binary-branch/path family already rules out a purely
radial finder, including degree-three filters. Dense core/clique-leaf
examples already obstruct simplistic repeated refresh charging. Reuse
those saved audits; do not rerun them without a changed claim.

Potential-driven discovery should be tested against both families. A
restricted solve followed by all violating-boundary admissions is already
known to risk many repeated phases; no near-linear cumulative bound has
been proved. A final local residual certificate can reject an inadequate
U, but each failed solve and boundary scan must still be charged.

The alpha-floor calculation also suggests comparing the alpha->0
problem with a dissipative divisible-sandpile/odometer obstacle. This is
only a proposed literature direction; check primary sources before citing
any algorithm or complexity result. Dynamic-flow literature was already
reviewed in docs/literature/lcp-solvers.md; avoid repeating that review
without a concrete new theorem or interface to test.
