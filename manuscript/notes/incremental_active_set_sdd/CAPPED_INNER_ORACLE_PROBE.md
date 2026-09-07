# The remaining inner oracle after explicit certified restarts

Block 9 update: the corrected Lift, persistent derivative-integral forest,
canonical export and one-pass range claims below are now implemented and
proved drafts in `sec:op3-persistent-vwf-forest`. Resume the new
`ADDITIVE_RECURSION_PROBE.md` for mixed relative/additive budgets and the
actual recursive graph schedule. The block-8 and earlier probes below
remain as historical derivations. General OP3 remains **Open**.

Second-night block 8 checkpoint, 8 September 2026. **General OP3 remains
Open.** The outer reductions retain every inner-oracle cost. Continue
the active-time campaign without repeating completed audits.

## Resume here: generic tolerance and canonicalization are now proved drafts

`sec:op3-generic-proximal-geometry` formalizes the earlier highest-priority
probe. The exact audit `GENERIC_PROXIMAL_GEOMETRY_AUDIT.json` passes 112
trajectories and 3,584 complete model/range certificates, including 11
zero-gap runs, four zero-total-tail runs, 80 signed-domain runs and two
exact common-energy-scale invariance checks. The script hash is
`4c5995f3fe6b154bec982ce9e4d714d79a82fe3398ea39efa36371ddb7b446fc`.
The policy is `delta=1/(33*2^30*kappa^3)`, with no algorithmic use of the
unknown gap. Residual translation gives restarts on signed lower domains.

The canonical shift `q-max(0,min(q)-U)*1` never increases model or original
energy, even when the total terminal slope is zero. For a connected supplied
graph, finite infimum is equivalent to nonnegative total terminal slope,
and the minimum is attained. With A=sum|f_i'(0)|, B0=max(U,max(-L_i)),
K=(n-1)/c_min, the initial gap is at most `A*B0+K*A^2/2`. Canonical APG
outputs have absolute coordinates at most `B0+sqrt(12*kappa*K*gap)`;
centers have at most three times that radius. These statements are draft
proofs awaiting independent review, not a recursive OP3 theorem.

**Next bounded target:** implement and audit the corrected Lift and a
persistent derivative-integral curve for valid supplied forest elimination.
Start with the two sections below named "Remaining numerical and local-work
obligations" and "A possible implemented replacement". Preserve validated
backends and old snapshots. Handle general child and parent lower endpoints:
the child endpoint L maps to L+F'(L)/c; before that point the lifted derivative
is c*(x-L). At parent lower P, use the boundary value if P is before this
point, otherwise y=P-g_lift(P)/c and F_lift(P)=F(y)+g_lift(P)^2/(2*c).
This gives exact constants and permits signed residual domains.

For the augmented area tree, override both node construction and lazy apply;
do not recompute a tagged aggregate from children still in old coordinates.
Read-only prefix integrals must carry transformations without allocating
nodes. A prefix deletion may be paid by removed event lineages, provided
the full small-to-large copying argument is proved. Do not repeat the
23-minute completed original driver audit unless its code or assumptions
change. The earlier derivation below is historical, now superseded where
the labeled generic proof applies.

## Established outer interface

`sec:op3-capped-proximal-budget` proves an explicit policy for the original
capped objective Phi and supplied Laplacians G<=H<=kappa*G. CPW Algorithm 9
and Theorem 8.3 (PDF p. 44) supply the convergence inequality. The scale
induction and certified restart driver are note-local proof drafts.
Source pp. 44 and 50–52 were visually checked; no fast inner solver is imported.

For feasible a with Phi(a)<=0 and a known lower bound d0>0 on its gap, use

    C0=1/(2*bar_alpha), R=kappa/(bar_alpha*lambda),
    e0=d0/(2^30*kappa^4), B=(9/2)*kappa*m*R^2+C0, delta_rel=e0/B.

The least dyadic T with T^2>=256*kappa suffices. Normalize every oracle as
E_x(y)=Phi_x(y)-Phi_x(0), where
Phi_x(y)=Phi(y)+(y-x)'(H-G)*(y-x)/2. The (1+delta_rel)-relative guarantee
forces model error <=e0. Previously bounded feasible iterates give the next
center in [-R,2R] through the exact coefficient (k-1)/(k+2); the source
prefix estimate proves the next feasible radius. Every run contracts gap
by at least 32, without a circular range assumption.

At a boxed candidate, C(a)>t, t=bar_alpha*(eps_appr/8)^2/2, supplies
d0=bar_alpha*t/(1+gamma). Run the same original capped objective again,
box at 1/bar_alpha and repeat. At most min{j:C0/32^j<=d0} runs are needed.
The actual original certificate stops the driver. This avoids shifted
residual domains at the outer level. All inner work, sparse construction,
failed guards, graph scans and boxing passes remain charged.

Use `CAPPED_PROXIMAL_BUDGET_AUDIT.json` and `CAPPED_RESTART_DRIVER_AUDIT.json`.
Dense capped KKT-piece solves and perturbed oracle candidates are validators.
Large final rationals use explicit binary-hash/bit-size metadata rather
than decimal expansion; every comparison remains exact. Rational runtime
is not the claimed exact-real word complexity.

## Historical block-7 derivation: a universal relative proximal tolerance

The following sharper induction emerged after writing the original-capped
policy. It has now been formalized and exact-audited as described above;
retain this derivation as provenance, with the labeled TeX proof authoritative.

For any convex diffusion objective Phi=g+h with g=x'G*x/2, 0 feasible,
an attained finite optimum u and G<=H<=kappa*G, write
Delta=Phi(0)-Phi(u). Start source Algorithm 9 at zero. Convex optimality
gives, for every feasible y,

    ||y-u||_H^2 <= 2*kappa*(Phi(y)-Phi(u)),
    ||u||_H^2 <= 2*kappa*Delta.

Use the same dyadic T, 256*kappa<=T^2<1024*kappa. Consider the **universal**
relative tolerance

    delta_rel = 1/(33*2^30*kappa^3).

The proof's internal absolute target can be e0=Delta/(2^30*kappa), even
though Delta is unknown to the algorithm. If earlier errors <=e0, the source
prefix estimate gives gaps <=2*kappa*Delta, using
3*sum_{j<=T}j*sqrt(2*e0)<=sqrt(kappa*Delta)/8.
Hence ||y-u||_H<=2*kappa*sqrt(Delta). The exact extrapolation coefficient
in [0,1) gives ||x-u||_H<=6*kappa*sqrt(Delta), so

    ||x||_H^2 <= 64*kappa^2*Delta,
    Phi_x(0)-Phi_x(q) <= ||x||_H^2/2+Delta <= 33*kappa^2*Delta.

The normalized relative oracle then forces error <=e0, closing the
induction with a tolerance depending only on kappa. The final gap is
<=Delta/32. Check the Delta=0 case explicitly: normalized model optimum
is zero, every relative output is optimal, and all relevant seminorms vanish.
This argument would replace the numerical-range appeal in source Claim 8.21
for a generic zero-start invocation, without needing capped coercivity,
minimum nonzero energy scale, number of vertices, alpha or epsilon.

For a restart from a nonzero a, one can use the standard shifted residual
objective with variable z=y-a, lower bound L-a, and zero value at z=0.
The same universal policy would then use its current gap internally.
This does require signed lower domains at inner refinement levels; the
completed fixed-original-capped driver avoids those domains by its explicit
gap floor. Preserve that distinction. The source theorem's seminorm form,
normalization constants, finite-optimum assumptions and all error inequalities
must be independently checked before claiming this sharper result.

### Candidate canonicalization for generic coordinate bounds

For source VWFs with a constant final derivative, finite objective infimum
requires the sum of terminal derivatives to be nonnegative: otherwise
shifting all coordinates to positive infinity makes energy unbounded below.
Let U>=0 bound all final breakpoints. If every coordinate of a feasible
candidate q exceeds U, subtract min(q)-U from every coordinate. All
coordinates remain >=U>=0>=their lower bounds, graph Laplacian energy
is unchanged, and all vertex terms are in their final rays with nonnegative
total slope. Thus energy cannot increase. This is also valid for a proximal
model: the added Laplacian linear shift has sum zero. It costs one paid
O(n) scan and can be applied to every oracle output without weakening its
relative guarantee. Afterwards min(q)<=U.

Combine this normalization with the seminorm bounds and an input edge
floor c_min. On a connected n-vertex graph,
diam(q)<=sqrt((n-1)/c_min)*||q||_G, by a simple path and Cauchy–Schwarz.
The initial lower bounds control the negative side, while min(q)<=U controls
the positive side. This suggests generic coordinate and shifted-breakpoint
bounds without an original capped coercivity constant. Test zero total
terminal slope, zero gap, shifted negative lower bounds and candidate
normalization during the actual accelerated state updates.

For a nonpositive-relative-energy candidate a, the same energy geometry
gives ||a||_G<=2*sqrt(2*Delta). A residual linear shift changes total positive
terminal-slope mass by at most
||(G*a)||_1<=2*sqrt(W_G)*||a||_G. This may avoid squaring a coordinate bound
at every recursive level. Trace the actual source graph construction and
call depth: leaf elimination creates VWFs, whereas the earlier exponential
Schur edge witness was explicitly not a source execution. Do not assume
that witness's tiny edges are generated by the source's j-tree procedure.

## Source formula correction before implementing Lift (details)

CPW arXiv:2105.14629v2 PDF pp. 40–42 was visually checked. Its printed
constant update for f(y)=r*y^2/2+a*y+b has a plus sign. Direct minimization
of c*(x-y)^2/2+f(y) on the corresponding interior piece gives

    y=(c*x-a)/(c+r),
    lifted(x)=c*r*x^2/(2*(c+r))+c*a*x/(c+r)+b-a^2/(2*(c+r)).

The breakpoint and derivative/curvature transformations are unaffected.
The valid VWF f(y)=-y on y>=0, c=1, x=0, has minimizer y=1 and value
-1/2; the printed plus sign gives +1/2. This is a specific coefficient
mismatch, not a refutation of the full runtime theorem. Corrected maps
remain associative under harmonic composition of c by infimal convolution.
Independently prove and audit the corrected whole-interval map before use.
The source also prints `arg max` where the following stationarity argument
uses minimization; follow the explicit minimizing definition.

## Next exact target: one supplied forest-elimination pass

The new outer driver's inner inputs all have domain y_i>=0, cap
U=1/bar_alpha, curvature h_i=bar_alpha*d_i and shifted linear loads
b_i^x=b_i+((H-G)x)_i. Individual terminal slopes may be negative even
though the full normalized model is coercive.

For exact graph elimination, require that the forest components attach
at retained roots and that every other graph edge joins retained roots.
An arbitrary spanning forest of a general graph does not meet this contract:
discarding nonforest incidences at eliminated vertices changes the problem.

Formalize and audit this **candidate induction** for exact leaf elimination:
F_v=f_v+sum_child Lift(c_child,F_child) on y>=0. Write t_i for each input
terminal derivative, T_v=sum_subtree t_i, S=sum_i max(t_i,0), assume initial
nonnegative breakpoints <=U and every forest edge >=c_min>0.

1. Lift preserves the terminal derivative, and addition adds it, so the
   subtree derivative is exactly T_v even when it is negative.
2. A split s maps to s+F'(s)/c. Since F'(s)<=T_v, each new nonnegative
   split is <=max(0,s)+max(T_v,0)/c. The domain boundary at zero gives
   split F'(0)/c with the same bound. Restrict to the parent's [0,infinity)
   and discard nonpositive events. The path recurrence suggests every
   retained breakpoint is <=U+n*S/c_min; prove all boundary cases.
3. Lift curvature is <=c. Thus the initial curvature at v is at most
   h_v+sum_child c_child, independently of the child event count. Summed
   over one pass it is <=sum h_i+sum_forest c_e.
4. Original unshifted slopes (1+lambda)*d_i-1_{i=v} are nonnegative.
   For centers in [-R,2R],

       ||(G-H)x||_1 <= 6*R*(W_G+W_H),
       W_G=gamma*m, W_H<=kappa*W_G,
       S <= (1+lambda)*2*m+6*(kappa+1)*gamma*m*R.

   The weight-sum bound follows from trace comparison. It does not
   require H-G to have nonnegative individual Laplacian edge weights.

An exact pass grows total events through original pieces and eliminated
boundaries. Do not silently compress after every leaf: doubling a maximum
split at linear depth could itself create an exponential range. Inspect
the actual source schedule and event/reconstruction charge before claiming
that one final compression, or only logarithmic compression depth, suffices.

## Remaining numerical and local-work obligations

### A possible implemented replacement for the source coefficient tree

The existing `persistent_affine_tree.py` has immutable AVL nodes, general
affine point maps, suffix hinges, readonly brackets and streaming iteration.
`module_curve_removal.py` provides immutable deletion. Preserve both files
and their established hashes; implement an augmented subclass/new module
for this new curve type rather than changing old validated backends.

Store the piecewise linear **derivative** curve as knots (x,g), including
the domain endpoint x=0, together with F(0). Add to each subtree its first
and last point and the trapezoid integral A=int g dx between them. Node
construction combines two child integrals and the connecting trapezoids.
For an affine point map

    x'=a*x+b*g+tx, g'=c*x+d*g+tg,

the transformed subtree area is

    A'=(a*d-b*c)*A + b*c*Delta(x*g)
       + (a*c/2)*Delta(x^2) + (b*d/2)*Delta(g^2)
       + tg*(a*Delta(x)+b*Delta(g)).

Here each Delta is last endpoint minus first endpoint. This follows by
integrating g' dx'; tx disappears from the differential. The formula and
first/last endpoints update in constant word work under a lazy affine tag.
Check it on complete segments and compositions, including translations.
A prefix integral query can combine whole covered subtree aggregates and
one partial segment in logarithmic height. Thus F(y)=F(0)+int_0^y g dx
is available without scanning the curve. Preserve read-only old versions.

For Lift(c), apply the horizontal shear (x,g)->(x+g/c,g). If the old
initial derivative a0>=0, prepend (0,0) before its transformed endpoint
(a0/c,a0), with derivative c*x in between; F_lift(0)=F(0).
If a0<0, query the transformed derivative at x=0, call it g0. Its original
minimizer is y=-g0/c, so compute F_lift(0)=F(y)+g0^2/(2*c) using the old
curve's prefix integral. Trim transformed knots below zero and insert the
new endpoint (0,g0). This obtains the correct constant from minimization.
The domain endpoint at equality zero needs explicit tie handling.

An AVL split trims a prefix in logarithmic work. Alternatively, repeated
minimum deletion may be amortized against the actual removed event copies;
prove that accounting before claiming it. Old snapshots remain immutable
and queryable even after their events disappear in an ancestor response.

To add a smaller VWF, add its constant at zero separately. Its derivative
is a0+C*x-sum_s q_s*(x-s)_+. Apply one global vertical shear/translation,
then stream its genuine curvature drops and apply negative suffix hinges,
inserting a derivative point at each breakpoint as needed. During this
operation the temporary final derivative may be linear, so track its tail
curvature explicitly for extrapolation; it returns to zero at completion.
All intermediate curvatures remain nonnegative because only the smaller
function's remaining positive curvature is being removed from that tail.

Largest-child persistent sharing with a source-event/physical-vertex mass
charge suggests O((S+n)*log^2(S+n)) work and all allocated words for a
supplied forest with total input VWF size S. Each leaf elimination creates
at most one boundary transition; each small-child event copy is charged
to a doubling of its containing mass. Preserve reconstruction data and
count prefix deletions, zero-jump events, scans, all newly created versions
and complete final recovery. This is still a candidate implementation and
charge, not an established fast primitive. First obtain a correct explicit
whole-interval reference Lift, addition and forest audit, then validate the
persistent implementation against that reference and full original KKT.

Use weights proportional to each original vertex's event count plus two,
including its possible incoming-edge boundary event. Choose the largest
weighted input among the local vertex function and lifted child functions.
Zero-jump stored points may be retained if their record lineage is charged;
skip their zero curvature drops when exporting a VWF. After elimination,
recover a child value from its saved lifted derivative at parent field x:
y=x-g_lift(x)/c, including the y=0 boundary case. At a full-tree root with
positive total final derivative, minimize by the derivative's zero crossing
or the domain endpoint; do not assume an isolated component with a negative
terminal derivative has its own finite unconstrained optimum.

### Recursive range and locality still to establish

The global moment compressor preserves terminal derivatives and has size
depending on the largest split, curvature and absolute budget. The pass
candidate bounds two of these inputs without the smallest coefficient.
The edge floor c_min still needs a justified source construction or pruning
rule. The earlier grounded quadratic pruning lemma does not automatically
apply to a capped or already eliminated scalar objective.

Eliminated component functions have value <=0 at zero. If their sum at a
reduced zero potential is bounded below by the full inner optimum, each
component's zero value inherits that same lower bound. Establish this
carefully and include compressed constant shifts. For domain-zero VWFs,
bounded F(0), event locations <=U_max and total curvature C imply bounded
piece coefficients: F'(0)=T-sum q*s, and a later constant is
F(0)-(1/2)*sum_past q*s^2. Tiny nonzero curvature weights may still remain.
Audit actual divisions: Lift uses c+r>=c_min, whereas root extraction may
use tiny r. A bounded quotient does not justify separately materializing
an unbounded reciprocal 1/r under an all-number assumption.

Trace the actual inner call graph, divisions, source graph construction,
compression error and refinement tolerance at every level. The outer
restart proof does not automatically replace arbitrary inner refinements.
Even a completed supplied-graph oracle leaves OP3's paid local discovery
and cumulative support/graph work open. Preserve this separate acceptance
criterion through the remaining active-time campaign.
