# Coarse local solution followed by certified accelerated refinement

This is a deterministic reduction of general OP2 to a single coarse solve.
It is not a construction of that coarse solve at the conjectured cost.
Only the designated manuscript source and fresh current-task work are used.

## Warm-start theorem

Assume a sparse nonnegative point x0 satisfies

    w^T x0 <= 1,
    F_rho(x0)-F_rho(x*) <= G0 <= alpha^2*rho/2.

The bound G0 must be certified by the coarse solver; it is not an oracle
available for free. Set z0=x0. Strong convexity gives

    alpha/2*||x0-x*||^2 <= F_rho(x0)-F_rho(x*),
    E0 <= 2*G0 <= alpha^2*rho.

Initialize the lazy capped reporter by reading the adjacency lists of the
explicit support of x0 and forming (Q-alpha I)x0. This costs
O(vol(supp x0)) graph and arithmetic work, up to deterministic-map logs.
No other adjacency lists need to be read for initialization. Since z0=x0,
the invariant theta*z0<=x0 holds for theta=sqrt(alpha).

The independently audited late-phase theorem now applies at every step:

    vol(supp z_(k+1)) < 13/rho.

Energy contracts by 1-sqrt(alpha). Thus, including lazy initialization and
final output, the refinement costs

    tilde O(vol(supp x0)
            + (1/(rho*sqrt(alpha)))*log_+(2*G0/epsilon)).

In particular, if the coarse solver costs tilde O(1/(rho*sqrt(alpha)))
and emits a point of support volume at most that budget, general OP2 follows.
All dependence on arbitrarily fine final accuracy has been isolated in this
already-proved refinement. The unresolved accuracy target is only
alpha^2*rho/2.

## A useful proved parameter-dependent implementation

The forest-preconditioned safe batch solver returns x0<=x*, so its mass
cap and support-volume bound are automatic. Run it to G0<=alpha^2*rho/2,
then apply the preceding refinement. If r* is the final support's cycle
rank, the resulting bound separates the costs as

    tilde O( (r*+1)/(rho*sqrt(alpha))*log_+(1/(alpha*rho))
             +1/(rho*sqrt(alpha))*log_+(alpha^2*rho/epsilon) ).

The structural factor r* therefore need not multiply the final-accuracy
logarithm. This is a practical refinement of the proved restricted-class
solver; arbitrary r* still prevents it from proving general OP2.

## Exact implementation and tests

`LazyCappedSolver.initialize_from_primal` accepts sparse degree coordinates
and a supplied certified objective-gap bound, initializes z=x, checks the
mass cap exactly, and charges its initial adjacency scans. It explicitly
does not certify the supplied objective bound itself. The prototype uses
rational theta with alpha=theta^2.

An independent exact test obtains the coarse certificate from
`forest_batch_solver`, refines to objective tolerance 10^(-12), and compares
against an exhaustive dense KKT optimum on a path, a tree, and a star.
All three cases passed; the path starts with a nonzero certified gap, so
the actual refinement loop is exercised. Per-step scans equal the recorded
kinetic support volume, and the proved 13/rho bound is checked. These small
tests validate implementation details, not the missing coarse-work theorem.
