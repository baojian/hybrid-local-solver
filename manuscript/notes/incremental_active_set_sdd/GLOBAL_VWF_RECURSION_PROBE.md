# Global compression: recursive scales and absolute proximal errors

Second-night block 6 checkpoint, 8 September 2026. **General OP3 remains
Open.** The global scalar primitive below supersedes the bounded-domain
route as the primary numerical probe. All new proofs are drafts awaiting
independent review. Supplied graph algorithms and local graph discovery
remain separate obligations.

## Completed results; do not repeat the audits

`sec:op3-global-vwf-compression` implements signed curvature-event
compression on the entire VWF domain. For a tiny split s with r=|s|<tau,
distribute curvature q between zero and sign(s)*tau with weights
q*(1-r/tau), q*r/tau. For a negative split subtract q*r*(tau-r)/2 from
the constant. The regularized function is a global lower approximation
with error at most

    xi = sum_tiny q*r*(tau-r)/2 <= C*tau^2/8, C=sum q.

Its derivative at zero and final derivative are preserved. Then round
each nonzero split away from zero to a dyadic grid and multiply its weight
by old_split/new_split. Handle zero separately. The global result is

    F(x) >= F_hat(x) >= 2*F(x/2)-2*xi.

The proof uses B_(a*s)(x)=a^2*B_s(x/a) and convexity, valid for both signs.
The operation takes O(k+1+log(R/tau)) word work, where R is the largest
input split magnitude or tau, and O(1+log(R/tau)) newly allocated words.
Two event scans, monotone grid pointers and all bins/output are counted.
The smallest split and the evaluation radius no longer enter the size
bound. **The largest split and a curvature/error bound still do.**
Tiny nonzero curvature weights remain possible: s=2^-2048, q=1,
tau=2^-10 creates weight 2^-2038. Do not claim all-number range.

For a graph objective, summing xi_i to Xi gives

    E(x) >= E_hat(x) >= 2*E(x/2)-2*Xi.

A beta-relative candidate for E_hat gives
E(w/2)<=E*/(2*beta)+Xi. If Xi<=|E*|/(4*beta), this is a
4*beta-relative original candidate. This is one embedding, not the
recursive approximation and runtime analysis.

`GLOBAL_VWF_COMPRESSION_AUDIT.json` records 1,212 functions, 23,000 full
overlay intervals, 87,152 finite-interval inequalities, 4,848 infinite-ray
inequalities and exact preservation of 1,212 terminal derivatives. The
weaker bounded baseline has 1,206 functions and 18,616 full intervals.
Deleting a tiny negative split was refuted; retaining its curvature matters.

`sec:op3-capped-sublevels` proves and implements the one-degree-query
shortcut: return zero if eps_appr*d_seed>=1; otherwise, if
gamma<=eps_appr*d_seed, return physical u=e_seed/d_seed, ACL output
bar_alpha*e_seed. No adjacency read is needed. Remaining cases have
gamma>eps_appr, controlling the logarithm of 1/gamma by log(1/eps_appr).
The original capped energy satisfies, for x>=0,

    E_cap(x) >= lambda*sum(x)-1/(2*bar_alpha).

The audit checks 1,644 original graph cases and three implicit stars with
up to 10^30 leaves. These statements control original feasible points;
they do not automatically bound every recursive or accelerated input.

## Next bounded target A: an elimination-pass upper-split contract

Source: Chen–Peng–Wang arXiv:2105.14629v2, Section 7.2, PDF pp. 39–42.
For Lift(c), a breakpoint s moves to s+F'(s)/c, with derivative at the
new breakpoint still F'(s). Its curvature r maps to c*r/(c+r)<=c.
The lower-domain boundary creates one additional transition with the
boundary derivative. Addition merges breaks and adds derivatives.

Investigate a **single supplied tree-elimination pass** first. Along a
chain the same derivative contribution produces additive shifts
g*sum(1/c), rather than a multiplicative recurrence. If initial upper
splits are at most U, all edge weights at least c_min, and positive final
derivative mass is bounded by S, a candidate upper bound is
U+n*S/c_min. Prove the exact induction, domain-boundary contribution and
sign requirements before promoting it. Addition of a linear proximal
term can make individual final derivatives negative, so their positivity
must never be assumed to survive a source call. Track positive parts or
absolute masses if necessary. Compression preserves final derivatives,
which may make this charge usable.

## Next bounded target B: replace one use of the all-number assumption

The source's Algorithm 9 and Theorem 8.3 are on PDF p. 44;
Claims 8.18–8.21 and the actual proximal-instance mapping are pp. 50–52.
The text was reread in block 6; visually check these pages before citing
precise formulas in a new proof. The cache is `/tmp/op3-cpw2021v2.pdf` and
`/tmp/op3-cpw2021v2.txt`. The source's scalar compression proof, pp. 37–39,
was visually checked in block 6.

Take a **supplied original capped graph**, G<=H<=kappa*G in Laplacian
order, and Phi(y)=y'G*y/2+h(y). Its proximal model obeys exactly

    Phi_x(y) = Phi(y) + (y-x)'(H-G)*(y-x)/2 >= Phi(y).

The source normalizes its oracle objective by subtracting Phi_x(0), not
by silently discarding arbitrary vertex constants:

    E_x(y) = Phi_x(y)-Phi_x(0).

Claim 8.19 constructs this using vertex terms
((G-H)x)_i*y_i+f_i(y_i)-f_i(0). A (1+delta)-relative oracle therefore has
additive model error at most delta*(Phi_x(0)-Phi_x(q)). This mapping must
be preserved in any absolute-error replacement.

For the original nontrivial ACL objective, with x0=0, the known initial
gap Delta obeys eps_appr/8<Delta<=1/(2*bar_alpha). Claim 8.20 gives
||x*||_H^2<=2*kappa*Delta. Theorem 8.3 gives, at step k>1,

    gap(y_k) <= 2/(k+1)^2 *
        (||x0-x*||_H + 3*sum_{j<=k} j*sqrt(2*error_j))^2.

A proposed bootstrap sets a known absolute proximal error well below
eps_appr/(160000*kappa^4), and runs T=ceil(10*sqrt(kappa)) steps.
Use conservative exact rational constants and check rounding; do not just
reuse a printed asymptotic value. Then prove a uniform polynomial bound
on feasible y_k energies from this theorem, and convert it to a coordinate
bound R_y using the new original capped coercivity. This has to be an
induction that justifies each oracle tolerance before its call.

Algorithm 9 uses z_k as well as y_k. Algebraically, for k>=1,
z_k=alpha_k*y_k-(alpha_k-1)*y_(k-1), and its next center is

    x_(k+1)=y_k + (k-1)/(k+2)*(y_k-y_(k-1)).

Thus bounded nonnegative feasible iterates imply x coordinates in
[-R_y,2*R_y]. Verify this identity against the actual source indices.
For an original graph with m edges of weight gamma<=1, one then has
||x||_H^2<=9*kappa*m*R_y^2. Since
Phi_x(0)<=||x||_H^2/2+Phi(0) and Phi_x(q)>=Phi*, the relative-oracle
gap scale is at most this known norm bound plus Delta. Choosing delta
from that upper bound should force the required absolute model error
without a minimum encountered-number assumption **for this one supplied
original-capped APG invocation**. Validate exact small graphs, infeasible
centers, original-model constants and the error inequalities.

This is a falsifiable candidate, not a proved replacement for the entire
source solver. Recursive residual instances have shifted domains and
different coercivity constants; their relative starting gap can be small.
The computable original gap certificate supplies a positive scale while
further original refinement is needed, but does not automatically price
all nested calls. Propagate the actual call graph and budgets explicitly.

## Further synthesis and local-work obligation

One global compression transfers E(x)>=lambda*sum(x)-C0 to
E_hat(x)>=lambda*sum(x)-2*C0-2*Xi. A logarithmic depth would preserve
polynomial scale; the actual recursion must establish that depth and sum
all additive errors. A long sequence of compressions cannot be charged
as one call. Edge pruning, its grounding assumption, linear shifts,
compressed curvature masses and largest breakpoints need compatible
invariants. Tiny curvature weights alone are not an obstruction if no
operation divides by them; audit actual uses.

Even a complete parameter-uniform near-linear **supplied-graph** solver
leaves the general OP3 local problem open. Unknown support discovery and
cumulative graph construction, certificate scans, failed calls and output
must be paid. Return to this requirement after the two bounded probes;
do not infer a local runtime from final support size.

Continue the 480-new-active-minute campaign in the actual-time ledger,
excluding prior-night and idle gaps. Commit and push verified blocks.
Keep all unreviewed claims out of the active manuscript and shared ledger.
No further account reset or subagent work is authorized or needed.
