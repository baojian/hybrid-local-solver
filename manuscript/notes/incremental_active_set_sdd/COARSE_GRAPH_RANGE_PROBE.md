# Recursive graph floors and numerical ranges

Second-night block 10 continuation. **Conditional derivations to formalize
and audit**, not yet proved claims. General OP3 remains **Open**. Block 10's
mixed additive recursion is proved and audited separately in
`sec:op3-mixed-additive-oracles`; the following is the next bounded target.

## Spectral pruning of a preconditioner

Given connected G on n>=2 with minimum positive edge c, supplied H with
G <= H <= kappa G and m_H positive edge records, set

    tau = c / (2*m_H*(n-1)).

Delete H edges of weight strictly below tau (retain ties), then double all
retained weights. For K=(n-1)/c, any endpoint difference satisfies
(x_i-x_j)^2 <= K*x'G*x. The deleted Laplacian P therefore satisfies
P <= K*W_deleted*G <= G/2. Consequently

    G <= H_new=2*(H-P) <= 2*kappa*G,
    min_positive_weight(H_new) >= c/(m_H*(n-1)).

This changes only the preconditioner, not the original objective, so it
uses no objective-error budget. Charge scans of G/H and every retained
copy/scaling/deletion check. If H is a valid forest plus retained-root core,
each forest edge is an H bridge. Applying H>=G to its cut gives its weight
at least c; hence none is deleted. The root core stays connected because
H_new>=G. Exact elimination creates no new graph edges. A child core has
c_child>=c_parent/(m_H*(n-1)), W_child<=2*kappa*W_parent.

Audit exact PSD inequalities, threshold ties, original bridge preservation,
all copied weights and common scales 2^-80,1,2^80. A useful family is unit
complete G, H=n times a star plus one tiny edge between retained roots;
G<=H<=(n+1)G. Also test weighted graph families with independently certified
spectral order. Dense PSD checks are validator work, not construction cost.

## Propagate energy bounds without repeatedly squaring coordinate bounds

Track B>=-Phi*, positive final-slope mass S, total largest curvature C,
R=max(1, largest positive split, largest negative lower endpoint), graph
weight W, minimum edge c, n,m, and requested eta. All graph/VWF quantities
are for the current supplied problem, not an unexamined local neighborhood.

1. Mixed APG: D=Delta+eta<=B+eta. Centers have squared H norm at most
   64*kappa^2*(B+eta), and a normalized inner model has negative optimum
   at most 33*kappa^2*(B+eta). Its positive final-slope mass is at most
   S+32*kappa*sqrt(kappa*W*(B+eta)). Domains/splits/curvatures are unchanged.
2. Exact forest: B is unchanged, individual root values at zero lie in
   [-B,0], positive tail mass does not increase, C_root<=C+W_H, and
   U_root<=U+n*S/c_H. Lower endpoints are a subset of the inputs.
3. Coarse refinement: the paid nonincrease guard keeps Phi(a)<=Phi(0)<=0.
   Thus ||a||_G^2<=8B and ||G*a||_1<=4*sqrt(2*W*B). Each residual is
   formed from the original coarse problem, so S_res<=S+4*sqrt(2*W*B)
   does not accumulate over refinement rounds. Its negative optimum is
   <=B. With K=(n-1)/c and paid canonicalization,
   R_res<=2*R+sqrt(8*K*B). Curvature is unchanged and every residual
   vertex function equals zero at its zero anchor.
4. Compression: final slopes are preserved, total curvature does not
   increase, R_child<=2*max(R_res,tau), and choose tau<=1. The global
   embedding yields B_child<=2*B+2*Xi. Negative zero-anchor shifts total
   at most Xi. Tiny positive curvature weights may remain.
5. Mixed recursion: eta_child=eta_parent/(2^34*kappa). With the spectral
   wrapper use its adjusted quality consistently in every formula.

These updates are additive/multiplicative by controlled graph/quality
factors and square roots. They avoid applying the generic A^2 gap bound
afresh at every depth. Prove a simultaneous logarithmic range induction
under explicit depth, size and quality assumptions, then check the actual
CPW construction and shrink recurrence. Do not claim Assumption 3.15 for
every encountered nonzero; show which primitive depends on which range.

Original capped diffusion starts with B=1/(2*bar_alpha), U=1/bar_alpha,
C=bar_alpha*sum(degrees), S<=(1+lambda)*sum(degrees), W=gamma*m,
c=gamma. The proved degree-only shortcut leaves gamma>eps_appr. Scales
polynomial in 1/bar_alpha are acceptable only when work depends on their
logarithms. A supplied global theorem would still leave local discovery
and cumulative supplied-face work open.

## Optional precision target

For feasible x with |x|_infinity<=R, total graph weight W, total maximum
curvature C and A=sum|f_i'(0)|, upward coordinate rounding by at most h<=1
preserves feasibility and raises energy by at most

    h*(A+(4*W+C)*R) + (W+C)*h^2/2
    <= h*(A+(4*W+C)*(R+1)).

An explicit dyadic grid could reserve additive error without the validator's
unbounded trial policy. This is a candidate lemma, not a bit-complexity
claim. Audit it only if useful after the graph/range argument.
