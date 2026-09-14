# Independent proof and implementation audit of relative-gradient cleanup

`MonotoneCappedCleanupSolver` is a separately versioned exact prototype. Its
simultaneous cleanup is safe, preserves accelerated energy contraction, and
has the claimed local work reduction. The initial cumulative kinetic-support
bound remains unproved. The default parameters do not eliminate the known
difficult initialized examples. Original parent solvers are unchanged.

## 1. Exact batch descent and termination

Write f_i=x_i/sqrt(d_i), g_i=grad J(x)_i/sqrt(d_i), q0=(1+alpha)/2, and
lambda=alpha*rho. The configured parameters satisfy 0<beta<1 and tau>0;
defaults are beta=1/4 and tau=lambda/8. A reported coordinate has

    f_i>0 and g_i>beta*q0*f_i+tau.

Its simultaneous replacement is f'_i=max(0,f_i-g_i/q0), so every change is
strictly negative. For each coordinate separately,

    d_i*(g_i*delta_i+q0*delta_i^2/2)
       <= -q0*d_i*delta_i^2/2.

The additional joint off-diagonal terms are nonpositive because all changes
have the same sign and the Hessian is Stieltjes. Therefore the whole batch
satisfies the stronger checked descent inequality

    J(f+delta)-J(f) <= -q0/2*sum_i d_i*delta_i^2.

Nonnegativity and any downward-closed mass cap are preserved. The kinetic
vector z is unchanged by cleanup, so the accelerated energy only decreases.
The parent's monotone step retains its factor 1-sqrt(alpha) contraction, with
exactly the same energy multiplier. Cleanup does not change the lazy sigma.

For a cleanup whose result is positive,

    f'_i <= (1-beta)*f_i-tau/q0.

A final clamp to zero can have a smaller drop; count that event separately.
Between positive additions by the accelerated update, global scaling can only
decrease f_i. With starting density f0<=1/d_i, the number of cleanup events in
such an epoch is bounded by

    1+ceil(log(1+beta*q0*f0/tau)/(-log(1-beta))),

up to harmless endpoint slack. A zero coordinate cannot reenter the cleanup
reporter until a new positive kinetic addition. Thus, if V is total kinetic
support volume and V_init is the explicitly supplied warm-support volume,

    total cleanup volume <= C*(V+V_init),
    C=O(1+beta^(-1)*log(1+beta*q0/tau)).

For fixed beta and tau=lambda/8, C is logarithmic in 1/(alpha*rho), with the
usual positive-part convention. For beta of order alpha, the extra factor
must remain explicit. This verifies the distinction drawn in
`relative_gradient_cleanup.md`; it does not improve that stronger variant's
known work bound.

## 2. The second reporter is truly lazy

The implementation stores f=sigma*X and its degree-coordinate L0 response
as sigma*R. On strictly positive X coordinates only, the cleanup key is

    R_i+(alpha-beta*q0)*X_i-alpha*1{i=seed}/(sigma*d_i),

with common threshold (tau-lambda)/sigma. The tree deliberately contains no
zero-X coordinates: this threshold is negative for the default parameters,
so assigning zero keys to absent primal coordinates would be incorrect.
The production code instead deletes a zeroed coordinate from this AVL.

An ordinary monotone transition changes normalized X and R only at the new
kinetic support and its sparse Laplacian response. Global sigma changes only
the common threshold and the seed's key exception. These entries suffice to
refresh the cleanup tree after the parent step; no old-X scan is needed.

Within a cleanup batch all gradients and changes are computed from the old
state before any coordinate is changed. One charged scan of the changed
coordinates forms L0*delta. The quadratic scalar updates by

    xQx <- xQx+2*delta^T Qx+delta^T Qdelta,

using only changed-coordinate values and their sparse response. The mass
change is the directly accumulated sum d_i*delta_i. Both terms use degree
coordinates consistently; the source and regularization linear terms are
then reflected by the existing objective property.

The changed X coordinates and changed R entries refresh the second tree.
For the original kinetic tree, each changed R entry is refreshed directly
with its CURRENT z,t exception and source term. The code never reverts or
reinstalls the whole kinetic exception list during a cleanup batch. z,t and
sigma remain unchanged. This is essential when cleanup affects a small set
while the previous kinetic support is large.

## 3. Paid work and state

One cleanup batch reports only eligible positive entries and scans their
adjacency lists once. Every repeated adjacency entry and boundary contribution
is counted by the parent's metrics. The added cleanup metrics identify the
subset of these scans caused by cleanup, eligible emissions, AVL visits and
rotations, key changes, gradient evaluations, and sparse response updates.
They are structural logical events, not exhaustive Python/bit-operation counts.

Each changed adjacency list was already cached when its coordinate entered the
primal support through a kinetic addition or the warm initializer. No new
adjacency list is required by cleanup in those supported initialization modes;
this fact is checked. Even without this observation, charging a list by its
cleanup volume would give the stated reduction.

If N is the exposed state size, the total implementation work is bounded by

    O((1+K+(1+C)*(V+V_init))*log(N+2)),

with final output charged to the initial support and previous kinetic supports.
Reporter queries with no eligible output still cost logarithmic time; there
is one per completed batch and one per outer step. Their count is paid by the
number of changed coordinates and outer iterations. Cached graph state,
current reporter state, and retained histories are charged to the same events.
Neither a preexisting warm support nor the final primal materialization is free.

## 4. Exact independent verification

`test_monotone_capped_cleanup_solver.py` independently forms full dense matrices,
recomputes every gradient, finds eligible coordinates by a full reference scan,
and applies exact simultaneous Fraction batches. This reference uses neither
production tree nor cached response/scalar updates.

It checks all connected labeled two- and three-vertex graphs, every seed, two
theta values, two rho values, and two cleanup parameter settings. Comparisons
include primal and kinetic vectors, each batch's eligible set and objective,
both reporter keys at every exposed record, the full response, quadratic and
mass scalars, terminal eligibility, line-search fractions, accelerated energy,
and stopping certificates. Per-step scans equal kinetic volume plus the exact
sum of cleanup batch volumes.

A warm three-vertex fixture produces the cascade {2}, {1}, {2}, testing a
positive intermediate coordinate reduction followed by final clamping. Another
warm trajectory invokes nonempty cleanup after actual monotone steps. A 32-vertex
warm fixture tests a simultaneous batch of adjacent vertices while guarded
objects reject full iteration over X,R,z,t,degree, and the old kinetic exception
set. It passes without invoking any forbidden full scan. These are feasible
warm-state tests, not reachability claims from the zero initialization.

Results are saved in `monotone_capped_cleanup_verification.json`. The exact
Fraction prototype is a small-instance verification tool; no floating numeric
certificate, general bit-complexity bound, or practical large-instance runtime
is claimed. No randomized algorithm or test is used.

The completed run passes all five test methods: 112 zero-initialized
trajectories, 563 exact step comparisons including three warm steps, eight
nonempty cleanup batches, and 38 coordinate-cleanup events. The small default
zero-start trajectories in this suite require no cleanup; the nonempty-batch
coverage comes from the explicitly identified feasible warm fixtures.
