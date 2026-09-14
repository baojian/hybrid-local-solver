# Independent audit: two integer-moment reporter trees

Status: the proposed formulas, exact threshold search, and local update
charge are valid under the conditions below. No implementation or speedup
measurement is claimed. This is a representation change for the fresh
bounded-dyadic solver, with no randomized operation and no new mathematical
direction or manuscript source consulted.

## 1. Notation and the raw-density identity

Use integer representations

    alpha=A/D, theta=1/T, h=1/H, sigma=S/H,
    X_i=M_i/H, L_i=J_i/H,
    z_i/w_i=Z_i/H, sum_(j~i)z_j/w_j=W_i/H,
    baseline_i/w_i=P_i/H, sum_(j~i)baseline_j/w_j=B_i/H.

Here `D` is the positive denominator of alpha, not the degree matrix.
The original degree is `d_i`. Within a stage A,D,T,H are fixed; S is
positive, and current-kinetic and baseline neighbor sums are exact.
The primal neighbor record J may carry the already audited scalar-rebase
error. The identities below are exact for the *computed* raw point with
that record; they do not remove its existing analytical error budget.

Set `q0=(1+alpha)/2`, `c=(1-alpha)/2`, `mu=theta^2`, and `a=1-theta`.
Starting directly from ordinary acceleration, the raw density is

    raw_i/w_i
      = -sigma * [(q0-mu)X_i-c*L_i/d_i]/[theta*(1+theta)]
        + c/(1+theta)*(Z_i/H+W_i/(H*d_i))
        + (s_i/w_i)/theta - lambda/theta.             (1)

The kinetic coefficient simplifies because

    a-(q0-mu)/(1+theta)=c/(1+theta).

The source density has the exact numerator

    sN_i = 2*A*H*1_(i=seed)-(D+A)*d_i*P_i+(D-A)*B_i,
    s_i/w_i=sN_i/(2*D*H*d_i).                        (2)

Define the proposed integers

    C0 = 2*D*H*(T+1),
    b_i = (D-A)*T^2*J_i-((D+A)*T^2-2*D)*d_i*M_i,
    e_i = (D-A)*T*(d_i*Z_i+W_i)+T*(T+1)*sN_i.

Substitution in (1) gives exactly

    raw_i/w_i = (S*b_i+H*e_i)/(d_i*H*C0)-lambda*T.    (3)

In particular, the factor H multiplying the exception and the T^2 in the
base are both necessary. No extra theta, degree, or source denominator is
missing. The proposed formulas are valid for arbitrary represented
rational alpha; alpha need not equal theta^2.

## 2. Disjoint trees and integer moments

Let E be the exception set and maintain exactly one tree record for every
exposed vertex:

    Base tree, i notin E: key b_i/d_i,
                          integer moments sum b_i and sum d_i.
    Exception tree, i in E: key N_i/d_i, N_i=S*b_i+H*e_i,
                             integer moments sum N_i and sum d_i.

Subtree cardinality can also be stored. Compare ratios by integer cross
multiplication, with the integer vertex label as the secondary tie key.
There is no need to normalize b_i/d_i or N_i/d_i by gcd, and equal ratios
at distinct vertices must remain distinct records.

The exact choice E={i:e_i!=0} is valid. For 0<alpha<1 and a certified
nonnegative source, all terms in e_i are nonnegative, and hence

    E = supp(z) union N(supp(z)) union supp(s).        (4)

Thus its cardinality is at most `2*vol(supp z)+|supp s|`. It is also safe
to keep a superset of this union as exceptions, with some zero e_i, if
the same cardinality bound holds. Every vertex still belongs to exactly
one tree. Alpha=1 is already a separate direct-solution case.

It is useful to absorb the common raw shift. Put

    L0=H*C0,
    q=L0*(gamma+lambda*T),
    q_min=L0*lambda*T,
    U=4*r, U0=L0*U.

Here gamma>=0 is the original projection's mass multiplier. Define the
physical numerator N_i=S*b_i on a base vertex and N_i=S*b_i+H*e_i on an
exception. Projection density is

    p0_i/w_i = min(U, (N_i/d_i-q)_+/L0).             (5)

For a threshold q, the combined positive tail is

    G(q)=sum_i (N_i-d_i*q)_+
        = S*sum_(base: S*b_i>d_i*q)b_i
          +sum_(exception: N_i>d_i*q)N_i
          -q*sum_(the same two tails)d_i.           (6)

Each tree tail query costs O(log(N+2)), using only integer subtree moments
and rational-threshold cross products. The clipped mass is exactly

    Mass(q)=[G(q)-G(q+U0)]/L0.                      (7)

Consequently one mass query costs O(log(N+2)); large positive-tail
cancellation is exact integer arithmetic, not a floating-point operation.
No support list is enumerated to evaluate this mass.

For the source-mass cap, write eta=Ecap/H, where

    Ecap=H-sum_i d_i*P_i

is a known nonnegative integer. Thus the scaled target in (7) is

    L0*eta=C0*Ecap,                                 (8)

which is an integer. The unit cap is the special case Ecap=H. Only q_min
and U0 need the represented regularization denominator; the common
lambda*T shift has disappeared from all other search operations.

## 3. Four ordered sequences give O(log^2 N) root search

If `Mass(q_min)<=eta`, set q=q_min and the mass cap is inactive. Otherwise
eta>0 in a valid nonzero continuation stage, and the desired q is strictly
larger than q_min. The only mass breakpoints are four sorted sequences:

    base zero points:       S*b_i/d_i,
    base upper points:      S*b_i/d_i-U0,
    exception zero points:  N_i/d_i,
    exception upper points: N_i/d_i-U0.             (9)

Each sequence has the order of its underlying AVL tree because S>0 and
the translations are common. Empty trees simply supply no sequence.

An O(log^2 N) search does not repeatedly rank-select in the implicit merged
array. Instead, binary-search *each of the four sequences directly* with
the monotone predicate `Mass(breakpoint)>eta`. At an equality, return that
breakpoint immediately; a flat segment at the target causes no ambiguity
in the projected vector. Otherwise, retain the last breakpoint with mass
greater than eta and the first with mass smaller than eta in each sequence.
One search can be performed as an AVL root-to-leaf walk. It visits
O(log N) nodes, and its mass evaluation at each node costs O(log N).
Four such walks therefore cost O(log^2 N), not O(log^3 N).

Let q_left be the maximum of q_min and the retained lower endpoints, and
q_right the minimum retained upper endpoint. An upper endpoint exists:
at the largest zero breakpoint the mass is zero<eta. If no equality has
already returned, then

    q_left<q_right,
    Mass(q_left)>eta>Mass(q_right),

and no breakpoint from either tree lies strictly between them. Hence the
mass is affine on this interval. Query the free and upper sets at any
interior point, for example its exact midpoint. The free degree sum is
positive, since otherwise the strict endpoint mass inequalities would
be impossible. With I the free coordinates and J the saturated ones,

    q = [sum_(i in I)N_i + U0*sum_(i in J)d_i
                         -C0*Ecap]/sum_(i in I)d_i. (10)

The required numerator sums are integer tree moments: base sums are
multiplied by S and combined with exception sums. Formula (10) is the
exact root on the interval. It adds only the denominator of the free
degree sum and the already known denominator of U0.

Duplicate ratios within a tree or ties across sequences are harmless.
The vertex secondary key ensures unique records, while the mass predicate
has the same value on every copy of a breakpoint. No smallest activation
margin, approximate bisection, or root-at-a-distinct-value assumption is
needed. A reporter accepting eta=0 can return the zero vector directly;
that degeneracy should not enter a free-degree division.

## 4. Correct emission and integer output rounding

For an exact, unrounded projection, positive outputs satisfy `N_i>d_i*q`
strictly. In the bounded-dyadic solver, emission is different. Since h=1/H
and h<=U, a stored projected density is positive exactly when

    N_i/d_i >= q+L0*h = q+C0.                       (11)

Thus enumerate two *closed* tails:

    base:      S*b_i >= d_i*(q+C0),
    exception: N_i  >= d_i*(q+C0).                 (12)

Equality must be included. Values in `(0,h)` remain represented only in
the aggregate ideal projection and incur no per-coordinate enumeration,
write, or adjacency scan. Upper clipping does not alter (11), because
U>=h. Searching a tail costs O(log N) and enumerating it costs its number
of returned records. The two lists need not be merged into a global order;
integer graph labels can supply a deterministic tie/order convention if
an implementation requires one.

If q=q_num/q_den with q_den>0, the stored numerator is computed entirely
with integer floor division:

    Pout_i=max(0,min(floor(H*U),
           floor((N_i*q_den-d_i*q_num)/(d_i*C0*q_den)))),
    p_i/w_i=Pout_i/H.                              (13)

All emitted rows satisfy Pout_i>=1. This gives the same downward-rounded
projection as the Fraction representation. No new numerical error is
introduced by the reporter change.

## 5. Safe membership transitions and complete local charge

The following two-phase update is sufficient and easy to audit. All
projection queries occur only before it starts or after it finishes.

1. Save the old exception vertex list. Delete every old exception from
   the exception tree using its stored old numerator and degree, and
   insert it into the base tree using its stored b_i. It is now an
   intermediate all-base representation, not a valid complete raw query.
2. Change the scale and update primal M/J records using the actual
   rounded X changes. At each affected base record, remove its old key
   before changing b_i, then insert its new key. New exposed vertices
   receive their degree and one base record. Current-kinetic neighbor
   records can be rebuilt from the newly emitted sparse kinetic support.
3. If a scalar rebase occurs, apply the already audited independent M/J
   rounding, set S=H, and rebuild base keys over exposed records. The
   changed keys need not preserve their old order: charge a genuine
   O(N log N) tree rebuild, or another independently justified rebuild.
   Current-kinetic and baseline neighbor sums are not scaled.
4. Construct the new exception set from the new kinetic support, its
   neighbors, and the fixed source. For each, delete its current base
   record and insert `(S*b_i+H*e_i)/d_i` into the exception tree. Install
   all new exceptions only after their source/kinetic sums and final S
   are known.

At query boundaries the trees are disjoint and cover all exposed records.
Transient delete/insert gaps are allowed only while projection queries
are forbidden. A per-vertex owner flag and stored key numerator make this
invariant explicit.

Refreshing every exception after a scale change is necessary even for
an unchanged static source vertex: its numerator contains S*b_i. The
exception order may change when S changes, so multiplying old exception
keys by a common scale or preserving their old search order is unjustified.
The base tree, in contrast, is independent of S and stays valid when only
S changes.

The ordinary transition costs

    O((|E_old|+|E_new|+changed_base_records)*log(N+2)).

Equation (4) bounds exception-list cardinality by current/previous kinetic
volume and source-record count. Primal changes are scattered only from
newly emitted coordinates; affected-record count is charged by those
adjacency entries. Clearing old exception/neighbor lists uses their saved
sparse records and requires no old support adjacency scan. Fixed-source
refresh costs O(|supp s|) per iteration, already paid by the stage theorem.
There is no sum of degrees of unselected boundary vertices.

Scalar rebase passes add the already proved O(log(1/tau)) factor over the
exposed record count. Every floor and every tree rebuild remains charged.
Together with O(log^2 N) root search and output-only tail enumeration,
the two-tree structure preserves the proved local operation bound.

## 6. Bounded integer sizes and what is actually eliminated

The bounded realization has `|M_i|=O(H)`, `|Z_i|=O(H)`, `|P_i|=O(H)`,
and `|J_i|,|W_i|,|B_i|=O(H*d_i)`, including the certified primal neighbor
error. Therefore

    |b_i|, |e_i| = O(D*T^2*H*d_i),
    |N_i|       = O(D*T^2*H^2*d_i).

Integer subtree sums add at most the bit length of an exposed degree sum.
Ratio comparisons use cross multiplication of these bounded integers with
degrees, rather than reduced Fraction construction or gcd. In particular,
no subtree denominator contains an accumulated least common multiple of
vertex degrees.

Search candidates are a node ratio, that ratio minus U0, or the single
free-interval formula (10). Their rational denominators consist of a
represented regularization denominator, one or a fixed number of degrees,
and one free degree sum. They are recomputed directly; they are not
recursively retained products from all search iterations. Integer pairs
can be left unreduced if this direct representation discipline is kept.
The total bit size is therefore bounded by a constant multiple of

    input encoding bits + log H + log T
        +log(N+2)+log(d_max+2),

including the numerical parameters and vertex labels. Stage changes use
nested grids and rebuild their fresh constants and source, as in the
bounded-dyadic proof.

The improvement eliminates Fraction/gcd work from point-key construction,
subtree-moment updates, and ratio-key comparison. It does not eliminate
integer multiplication, exact comparison, integer division for rounding,
or all rational threshold calculations. Those remaining operations are
bounded and charged. Performance improvement needs implementation and
measurement; the mathematical conclusion here is equivalence to the same
computed raw projection and preservation of its certified error/work model.
