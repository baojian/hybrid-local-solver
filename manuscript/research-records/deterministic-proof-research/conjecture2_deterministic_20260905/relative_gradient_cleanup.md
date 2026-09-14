# Relative-gradient cleanup with charged local maintenance

Fresh deterministic construction. It preserves accelerated convergence and
adds only a polylogarithmic factor to the kinetic-support implementation
cost when beta is a fixed constant. A general initial kinetic-work bound
for the resulting algorithm is still OPEN. No OP2 proof is asserted.

Use the existing monotone capped step, with theta=sqrt(alpha), q0=(1+alpha)/2,
lambda=alpha*rho, f_i=x_i/sqrt(d_i). After that step, fix beta in (0,1) and
tau>0 (the proposed default is beta=1/4, tau=lambda/8). Repeatedly report
all coordinates satisfying

    f_i>0 and grad J(x)_i/sqrt(d_i)>beta*q0*f_i+tau.

For the reported set, simultaneously replace

    f_i <- max(0, f_i-grad J(x)_i/(q0*sqrt(d_i))).

All other coordinates remain unchanged. Continue until there is no reported
coordinate. All comparisons are strict; equality can remain unprocessed.

## Each cleanup batch decreases the objective

Every changed normalized coordinate has delta_i<=0. Its diagonal quadratic
and linear contribution equals the improvement from exact coordinate
minimization. Off-diagonal cross terms between different changed coordinates
are Q_ij*delta_i*delta_j<=0, because Q is Stieltjes. Therefore the simultaneous
batch decreases J at least as much as the sum of the separate diagonal
coordinate improvements. This observation does not require the changed
vertices to be independent in the graph.

The cleanup preserves nonnegativity and decreases weighted mass. It does not
change z. Consequently replacing the monotone step's primal point by the
cleaned point only decreases

    E=J(x)-J(x*)+alpha*||z-x*||^2/2.

The same accelerated energy contraction remains valid, as does monotonicity
of J. The general-state late-phase support recurrence applies; the stronger
invariant theta*z<=x is not claimed.

## Finite cleanup and arithmetic accounting

If a cleanup leaves f_i positive, then

    f_i_new <= (1-beta)*f_i_old-tau/q0.

If f_i_old<=tau/((1-beta)*q0), the next eligible cleanup sets it to zero.
Weighted mass at most one implies f_i<=1. Between two positive additions to
the same coordinate by the accelerated primal update, global scaling only
decreases its actual value. Thus each such interval has at most

    O(1+log_+(q0/tau)/(-log(1-beta)))

cleanup events at that coordinate, including its possible final zeroing.
The number of intervals is bounded by its number of kinetic-support
emissions, plus one for an externally supplied initial nonzero coordinate.

For constant beta and tau=lambda/8, the extra adjacency and scalar work is
therefore O(log(1/(alpha*rho))) times the already charged cumulative kinetic
volume and initial support volume, apart from balanced-tree logarithms.
No numerical complementarity-margin logarithm is introduced. This is an
amortized count, not a claim that every individual cleanup batch is cheap.

## Second lazy reporter

As in the existing implementation, maintain x=sigma*X and L0*x=sigma*R,
where L0=Q-alpha I; here X and R are in degree coordinates. On x_i>0,
cleanup eligibility is

    sigma*(R_i+(alpha-beta*q0)*X_i-b_i/(sigma*w_i))
           +lambda > tau.

Only the seed has the displayed b exception. A second deterministic
augmented ordered tree on the positive X coordinates stores this key, with
one common threshold (tau-lambda)/sigma. Positive primal additions and
sparse response changes update its keys. Global decay changes only the
common scale and the seed exception. Zeroed coordinates leave the tree.

For a reported cleanup delta, scan those changed coordinates once to form
L0*delta, update X and R sparsely, and update the affected entries in both
trees. The kinetic reporter must retain its current z,t exceptions; it
must not revert and reinstall the entire exception list after every cleanup
batch. Its affected key can be recomputed directly from local X,R,z,t data.
The quadratic scalar changes by 2 delta^T Qx+delta^T Q delta; both terms use
only the changed coordinates and their charged sparse response. Mass and
seed-linear terms also update locally. There is no repeated scan of the
old primal support, or an uncharged final materialization.

## Stronger cleanup is safe but has an extra cost

If beta*q0<alpha and tau<lambda, a terminated primal state is a subsolution
of the modified Stieltjes obstacle problem with matrix Q-beta*q0 I and
forcing b-(lambda-tau)w. Comparison therefore places its support inside the
modified optimizer's support, of volume at most alpha/(lambda-tau).
Moreover L0*x has positive weighted mass at most alpha when beta*q0<=alpha,
so c*||(I-P)D^(1/2)x||_1<=2alpha.

This stronger invariant would fund the kinetic-support flow ledger.
However choosing beta=Theta(alpha) in the elementary geometric cleanup
count incurs an inverse-alpha factor. A separate mass-drop accounting is
better but still does not achieve OP2: every cleanup leaving the coordinate
positive removes at least tau*d_i/q0 weighted mass; the cumulative positive primal additions
are at most theta*K, and zeroing events can be charged to kinetic additions.
This gives O(theta*K/tau) cleanup volume, or approximately
O(1/(alpha*rho)) at K=O(1/theta), before logarithms.

Thus the strong variant currently reproduces a nonaccelerated work scale;
the constant-beta variant has the desired cheap implementation but still
needs a new cumulative kinetic-support theorem. Neither fact is omitted
from the status of this construction.
