# Additive budgets through compressed recursive diffusion

**Block 10 update:** Sections 1–4 and the dense forward-piece policy below
are now proved drafts and exact-audited in `sec:op3-mixed-additive-oracles`.
The original candidate derivation is retained as dated development history.
Resume `COARSE_GRAPH_RANGE_PROBE.md` for the still-conditional graph/range
work. The source constructor and local-work obligations remain open.


Second-night block 9 continuation, 8 September 2026. **General OP3 remains
Open.** The persistent exact forest primitive is implemented and audited in
`sec:op3-persistent-vwf-forest`. Its code is `persistent_vwf_forest.py`,
final hash `8977f6a2a361b7a203422e6f140d52af32aa8bfaa24ba6d493c60a122274b911`.
The complete audit passes 192 trees, 15 retained-root field assignments,
nine structured cases through 512 vertices, complete old-curve integrals,
canonical export and original KKT. Do not repeat completed full audits
unless code or a new concern changes their validity.

## Highest-priority new target: mixed relative and additive contracts

Everything below is a **Conditional derivation to formalize and audit**,
not a proved result of block 9. The universal exact-relative tolerance and
the one-pass forest range results are already proved drafts. A remaining
compression difficulty is that an arbitrary normalized inner model may
have an arbitrarily small negative optimum: choosing an additive compression
budget from a positive lower bound on that optimum reintroduces a precision
margin. Instead carry a requested absolute error through the recursion.

Let a supplied oracle on Phi, Phi(0)<=0, return a feasible q satisfying

    Phi(q) <= Phi*/beta + eta,  beta>=1, eta>=0.

Call this a beta-relative guarantee with additive eta; do not silently
replace it by a pure relative guarantee. Maintain feasible states and
charge objective evaluations/failed improvement guards.

### 1. Compression and exact forest recovery

The proved global compressor gives E>=Ehat>=2*E(x/2)-2*Xi. If an oracle
returns Ehat(w)<=Ehat*/beta+zeta, then

    E(w/2) <= E*/(2*beta) + zeta/2 + Xi.

Scaling w/2 preserves a domain [L,infinity) because L<=0. Exact forest
recovery M preserves this energy exactly. No division by |E*| is needed
for this mixed contract. Implement this pipeline using exported persistent
root VWFs, the unchanged global moment compressor, and an explicitly
charged coarse reference oracle. Certify all scalar polynomial intervals,
compression constants, coarse energy and recovered original energy.

Use a common tau for all root functions. If C_total is their summed largest
curvature and target Xi0>0, tau=min(1,Xi0/C_total) is a conservative rational
choice (affine C_total=0 is exact). The existing bound Xi<=C_total*tau^2/8
then gives Xi<=Xi0. The exact pass bounds the largest split and curvature;
it must precede compression. Source Algorithm 6, PDF p.31, has that order.

### 2. Refinement with an additive budget

At current feasible a form the exact residual objective
R_a(z)=Phi(a+z)-Phi(a), with shifted vertex functions/domain as in
`cor:op3-generic-residual-restart`. Its optimum is -gap(a) and R_a(0)=0.
A beta-relative oracle with additive xi yields

    gap(a+z) <= (1-1/beta)*gap(a)+xi.

An optional paid guard keeps a if the actual energy would increase. It
preserves this inequality, makes all accepted energies nonincreasing, and
does not discard the failed call's work. After J calls,

    gap(a_J) <= (1-1/beta)^J * |Phi*| + beta*xi,

because initial gap Phi(0)-Phi*<=|Phi*|. For desired relative delta>0 and
additive zeta, take xi=zeta/beta and the least J with
(1-1/beta)^J<=delta/(1+delta). This gives

    Phi(a_J) <= Phi*/(1+delta)+zeta.

J=O(beta*log((1+delta)/delta)); it does not depend on the absolute error
or on an unknown objective-gap floor. The zero-gap case must be included.
All residual translations, domains, constants, graph products and guards
are charged. A canonical common shift may be applied after each accepted
iterate to bound coordinates without increasing energy.

### 3. Accelerated mixed-contract induction

For one source APG invocation let Delta=Phi(0)-Phi*, and give the algorithm
a requested eta>0. Set D=Delta+eta for analysis only, and choose

    T = least dyadic integer with T^2>=256*kappa,
    delta_rel = 1/(66*2^30*kappa^3),
    zeta = eta/(2^32*kappa).

Require each normalized model oracle to satisfy

    E_x(q) <= E_x*/(1+delta_rel)+zeta.

The candidate induction is the generic block-8 proof with D in place of
Delta. Its internal absolute target is e0=D/(2^30*kappa), which is not
used by the algorithm. Previous gap bounds give center norm squared
<=64*kappa^2*D and model range Phi_x(0)-Phi_x(q)<=33*kappa^2*D.
The mixed contract rearranges to

    e_x <= delta_rel*(Phi_x(0)-Phi_x(q))+(1+delta_rel)*zeta <= e0.

The two terms are each at most D/(2^31*kappa). At the first step,
Phi(q)<=Phi(0)+zeta, so gap(q)<=D. The source prefix inequality then
closes the induction and gives final gap <=(Delta+eta)/32.
The model energy difference need not be nonnegative now; use only its
upper bound. Canonicalization still preserves every mixed model contract.
Zero gap with positive eta permits nonzero errors and must be stress-tested.

Since Phi(0)<=0, this final bound implies the weaker but convenient
Phi(output)<=Phi*/2+eta. Thus this invocation can implement the same
2-relative-plus-additive interface requested recursively, if its preconditioner
and inner oracles meet their stated contracts. This does not itself build them.

### 4. Suggested recursive budget schedule

For an APG call with additive eta and quality kappa, each inner forest
problem requests relative delta_rel above and additive zeta=eta/(2^32*kappa).
Exactly eliminate its forest once, then refine the resulting coarse problem.
Each refinement residual is compressed with total error Xi<=zeta/8 and
sent to a recursive 2-relative oracle with additive eta_child=zeta/4.
The compression embedding yields a 4-relative coarse oracle with additive
xi=zeta/4. Refinement with beta=4 yields the requested
(1+delta_rel)-relative guarantee plus zeta. Recovery is exact.

There are O(log(kappa)) refinement calls per inner solve, with no extra
factor log(1/eta). Along a recursion path the additive budget decreases by

    eta_child = eta_parent / (2^34*kappa_parent).

Thus log(1/eta_leaf) increases only by O(depth + sum log(kappa)), not by
the number of calls in the recursion tree. Formalize why the geometric
refinement sum and the accelerated source bound pay for these reused
per-call budgets; do not divide by a guessed total number of future calls.

## Remaining source and local-work obligations

### A practical dense exact coarse validator to try

Avoid exponential piece enumeration if possible. For convex VWFs whose
derivatives are concave, a forward quadratic-piece policy may give a useful
exact validator. Start at the vector of original lower endpoints. Keep
the current piece at each coordinate. Solve the bound quadratic formed by
those pieces plus the graph Laplacian, with the previous candidate as the
new lower bound. Advance each piece index to the piece containing its new
coordinate (including right-side ties), and repeat until no index advances.
There are at most the total number of input split advances, but prove the
invariant before using that as a theorem.

The intended invariant: the new piece's derivative at the previous point
is at most the old extrapolated derivative, because curvature decreases
to the right. At a previously interior coordinate the new gradient is
therefore nonpositive. Holding such a coordinate at its temporary lower
bound cannot create a positive gradient: neighbor increases contribute
nonpositively through Laplacian off-diagonals. Thus its final bound-QP
gradient must be zero, so the temporary lower bound creates no spurious
original KKT constraint. At termination all original scalar pieces and
original lower-bound KKT conditions should agree exactly.

Use unchanged `geometric_value_events.obstacle` only as a dense reference.
The matrix is a connected Laplacian plus nonnegative diagonal curvature.
If any curvature is positive it is SPD. If all are zero, the total linear
slope is the nonnegative total terminal slope. The strict positive-face
growth cannot activate every vertex in this case: inactive residuals sum
to the nonpositive total load, while active residuals are zero. Proper
principal submatrices are SPD, so the singular full Laplacian need not be
solved. Check this carefully for zero total slope and arbitrary signed
lower endpoints, and certify full original KKT independently. Compare tree
instances with the already validated persistent forest solver. This is a
candidate dense validator, not a fast coarse numerical oracle.

### Actual recursive graph and locality questions

Read actual CPW Sections 4–5 and the preconditioner construction. The new
forest pass keeps edge weights unchanged; that fact alone does not bound
weights of newly constructed recursive preconditioners. Trace lower edge
weights, vertex domain shifts, total terminal mass, largest curvature,
constants and largest split through the real schedule. The earlier exact
Schur example is not a CPW execution. Keep input size n,m,S explicit, and
derive the actual recurrence with compression size depending on log(R/tau).
Do not import Assumption 3.15 under another name.

One-pass constants are in [Phi*,0]; generic canonicalization gives an
explicit input-gap upper bound. Normalized proximal terminal mass is at
most original positive tail mass plus 32*kappa*sqrt(kappa*W_G*Delta).
These may control upper scales without lower bounds on curvature drops.
Preserve the old validated helper hashes and create separate audit modules.

Even a repaired supplied global solver does not prove OP3. Unknown-support
graph discovery and repeated supplied-graph work must still be charged.
Finish with an honest synthesis separating implemented structural solvers,
the repaired global numerical interface, and this remaining local question.
