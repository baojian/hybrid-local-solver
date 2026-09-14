# A deterministic reporter for a stronger weighted cap

This note proves a local exact weighted-projection implementation with only
polylogarithmic overhead. It also identifies a useful integer-degree exception
that avoids weakening the cap near equality. Accelerated convergence and the
existing late-phase work theorem survive. The initial-phase cumulative support
bound, and hence general deterministic Conjecture 2, remain open.

## 1. Valid caps and the near-equality issue

Use the fixed allowed face from `guarded_monotone_capped_acceleration.md`:

    c_s=1-rho*d_s,
    c_i=1-rho*(d_s+d_i) for i!=s,
    Allowed={i:c_i>0}.

If rho*d_s>=1, the optimum is zero and no weighted reporter is needed.
Otherwise 0<rho<1, since the graph has positive integer degrees. Put q_i=1/c_i
on Allowed. The exact optimum satisfies

    sum_i q_i*w_i*x*_i <= 1.                            (1)

For completeness, if S=supp(x*) is nonempty, it contains the seed and
mass(x*)+rho*vol(S)<=1. Each c_i for i in S is at least
c_S=1-rho*vol(S)>0. Therefore the left side of (1) is at most
mass(x*)/c_S<=1. Coordinates outside Allowed are zero. The zero optimum also
satisfies (1). This establishes a convex containing set, not a requirement
that arbitrary iterates satisfy the original nonconvex support identity.

Any fixed weights 1<=qbar_i<=q_i retain the optimum and imply the ordinary
unit-mass cap. In particular, define

    qbar_i = largest power of two <= min(q_i,1/rho).      (2)

There are at most 1+floor(log_2(1/rho)) weights in (2). Thus the requested
clipped, downward-rounded cap is valid. It may coincide with the ordinary
mass cap; strict strengthening is not guaranteed.

A near-equality pitfall is that c_i need not be at least rho. For example,
if 1/rho is just above an integer k and the relevant degree sum equals k,
then c_i=1-rho*k can be arbitrarily smaller than rho. Clipping q_i at 1/rho
can therefore lose an arbitrarily large factor relative to the exact weight.
The graph's degrees are integers, but rho need not be a reciprocal integer.
No near-equality coordinate may be rounded into the allowed face: test c_i>0
exactly before assigning any weight. Equality is rejected.

There is a simple stronger option that costs only one additional class:

    if 0<c_i<rho, retain qbar_i=q_i exactly;
    otherwise round q_i downward to a power of two.      (3)

To see why this creates at most one extra class, write c_i=1-rho*k_i with
k_s=d_s and k_i=d_s+d_i otherwise. Each k_i is an integer. The condition
0<c_i<rho requires

    1/rho-1 < k_i < 1/rho,

an open interval of length one, so there is at most one possible integer k_i.
All such vertices consequently have the same c_i and the same exact q_i.
Every other allowed coordinate has q_i<=1/rho. Formula (3) has
B<=2+floor(log_2(1/rho)) classes, and q_i/2<qbar_i<=q_i everywhere; the
exceptional class retains equality qbar_i=q_i. It contains the optimum and
loses at most a factor two from the exact convex cap. More precisely,
C_exact subset C_rounded subset 2*C_exact, on the same allowed face.

No floor or logarithm oracle is required: construct the dyadic table by
repeated doubling up to 1/rho and classify each exposed allowed coordinate
by comparisons with c_i. The exceptional test is just c_i<rho; it does not
require knowing the maximum allowed degree in advance. This integer argument
uses the problem's unit-edge graph assumption and must not be applied to
arbitrary real weighted degrees. For such graphs, (2) still gives the stated
number of classes and a valid cap, but (3) may have many exceptional weights.

The following reporter works for any fixed B positive weight classes. Write
q_b for a class weight, whether dyadic or exceptional.

## 2. Projection as a root among B sorted sets

The unchanged lazy mirror state gives, in degree coordinates,

    zraw_i/w_i = sigma*K_i-h,   h=theta*rho>0,

where sigma>0 is a shared scale and K_i is the existing local key. The convex
set is C_q={z>=0:sum_i q_i*w_i*z_i<=1}, restricted to Allowed. Euclidean
projection has the exact form

    zplus_i = w_i*[sigma*K_i-h-mu*q_i]_+,   mu>=0.       (4)

For each class define its ordered breakpoints

    t_i=(sigma*K_i-h)/q_b,

and the decreasing continuous function

    Phi(mu)=sum_i d_i*q_i^2*[t_i-mu]_+.                 (5)

If Phi(0)<=1, take mu=0. Otherwise there is a unique positive root Phi(mu)=1;
Phi is strictly decreasing wherever it is positive. Equation (4) then gives
the unique projection. The original regularization offset h remains unchanged;
it must not be replaced by h*q_i.

Within a class, the order of t_i is the order of K_i because sigma/q_b>0.
Cross-class orders may change with sigma, but no cross-class order is stored.
Maintain one deterministic balanced search tree per nonempty class, keyed by
K_i with deterministic tie handling. Its subtree aggregates are

    number of vertices, sum_i d_i, sum_i d_i*K_i.

The count supports rank selection. The other aggregates support exact tail
sums. One insertion, deletion, or key change costs O(log(N+2)), where N is the
number of exposed records. Weights and class memberships are fixed for the
entire solve. Forbidden exposed vertices keep their charged degree and sparse
response records but need no entry in a projection tree.

At a candidate mu, query class b at K>(h+q_b*mu)/sigma. If the corresponding
tail moments are M0=sum d_i and M1=sum d_i*K_i, its contribution is

    Phi_b(mu)=q_b*sigma*M1-q_b*h*M0-mu*q_b^2*M0.        (6)

Ranks strictly below, equal to, and above the threshold are obtainable in the
same asymptotic time (two ordinary prefix queries suffice for ties). Thus a
full evaluation of Phi and all class ranks costs O(B*log(N+2)). It reads only
search paths and aggregate words, not all tail records.

## 3. Exact pruning algorithm for the water-fill root

Assume Phi(0)>1. Maintain a lower bound ell=0 and initially no finite upper
bound. In each class keep the rank interval of breakpoints strictly between
the current bounds. Initially this consists of t_i>0. Let n_b be its size and
n=sum_b n_b. Boundaries and ties are excluded consistently.

Repeat while n>0:

1. In each nonempty interval select its middle breakpoint m_b by subtree
   counts, and attach the integer weight n_b to m_b.
2. Compute a weighted median p of these at most B middle values. Sorting the
   B values deterministically and adding their integer weights suffices.
   Thus classes with m_b<=p have total weight at least n/2, and classes with
   m_b>=p also have total weight at least n/2.
3. Evaluate Phi(p) and the per-class ranks using (6).
   If Phi(p)=1, return mu=p. If Phi(p)>1, the root is strictly greater than p:
   set ell=p and discard every candidate breakpoint <=p. If Phi(p)<1, set
   the upper bound to p and discard every candidate breakpoint >=p.

Every nonterminating iteration discards at least n/4 candidates. Indeed,
when the root exceeds p, each class whose middle is <=p loses at least half
its interval; these classes have total size at least n/2. The reverse case
uses classes with middle >=p. This works for singleton intervals, even sizes,
and duplicate breakpoints. A lower middle has at least half the class on
either inclusive side. Hence at most O(log(N+2)) iterations occur.

When no candidate breakpoint remains, the root lies in an interval on which
the active set is constant. Query tails at the lower bound ell, excluding
breakpoints equal to ell. Sum their affine coefficients

    A=sum_b (q_b*sigma*M1_b-q_b*h*M0_b),
    C=sum_b q_b^2*M0_b.

Then C>0 because Phi(ell)>1, and the exact answer is

    mu=(A-1)/C.                                       (7)

There are no breakpoints between ell and the root, so (7) solves the correct
affine piece. A breakpoint at the upper bound remains in this tail, as it
should; a breakpoint at ell is excluded. If an evaluated breakpoint is the
root exactly, the equality branch already returned it. No numeric bisection,
separation bound, accuracy parameter, or randomized selection is used.

Rank selection and tail queries cost O(B*log(N+2)) per pruning round; the
weighted median costs O(B*log(B+2)) by sorting. Total threshold work is

    O(B*log(N+2)*(log(N+2)+log(B+2))).                  (8)

After finding mu, enumerate only K_i>(h+mu*q_b)/sigma in each class tree and
compute (4). This costs O(B*log(N+2)+|supp zplus|). Ties produce zero and are
not emitted. The cap-inactive case has the same output bound and needs only
one tail evaluation. In particular, even a huge set of positive raw candidates
removed by the cap does not have to be scanned or materialized.

## 4. Complete locality charge

The normalized response and exception formulas are identical to the ordinary
cap. Revert old exceptions, change sigma, apply sparse response changes, and
install new exceptions within each affected coordinate's fixed class tree.
This costs O((1+vol Z_old+vol Z_new)*log(N+2)). Only the new Z is scanned to
form L0*zplus, including charged repeated edge contributions, neighbor-degree
replies, and sparse writes. Unexposed vertices have raw value -h*w_i<0 and
cannot be selected under any positive q_i, so no global graph access occurs.

Classifying a newly exposed coordinate costs O(log(B+2)) comparisons after
the dyadic table is constructed. The table has O(log(1/rho)+1) entries and
costs that much to build. The exact exceptional weight in (3) requires one
additional division on its first use, with subsequent equality of that class
guaranteed by the integer-degree argument. Large exact weights remain one
word in the specified exact-real model; rational bit complexity and numerical
conditioning are separate issues and are not hidden as practical guarantees.

For K iterations, put V=sum_(k=1)^K vol Z_k and let V_init be any explicitly
charged warm-support volume. With N the final number of exposed records, the
total paid work, including degree replies, scans, arithmetic, comparisons,
state updates, reporter work, and output, is bounded by

    O((1+V_init+V+K)*log(N+2)
       + (1+V_init+V)*log(B+2)
       + K*B*log(N+2)*(log(N+2)+log(B+2))
       + log(1/rho)+1),                               (9)

Here B may be the full class-table bound; root queries visit only nonempty
classes, whose number is at most min(B,N). The output support is contained
in the warm support and the union of auxiliary supports. Its materialization
is therefore charged to V_init+V. The state has O(1+V_init+V+K+B) words,
including cached adjacency, all exposed rejected boundary records, and any
stored iteration history. This is a deterministic polylogarithmic overhead
on the same cumulative support-work quantity as before.

## 5. What changes in the mathematical theorem

The weighted cap is fixed, closed, convex, and contains x*. Therefore the
one-projection accelerated-energy proof applies without changing theta,
regularization, or the gradient. The monotone segment search also remains
valid: both endpoints lie in C_q, and decreasing the objective preserves the
same energy contraction. The objective coefficients continue using ordinary
mass w^Tx, not the new weighted-cap mass. The lazy scale still differs from
the energy contraction when the segment search is used.

Because q_i>=1, C_q is contained in the ordinary mass cap. Positivity of an
emitted coordinate implies positivity of its original raw mirror coordinate;
the new projection subtracts the nonnegative term mu*q_i*w_i. Thus the audited
outside-core and late-phase support estimates remain valid. Formula (9) proves
that this stronger feasible set does not require a full-record scan.

This is an algorithmic strengthening of the feasible-set and reporter results,
not a proof that the early cumulative support volume is small. For example,
when every relevant rho*(d_s+d_i)<1/2, downward dyadic rounding gives qbar_i=1,
so the method agrees with the ordinary cap on those coordinates. No claimed
improvement on bounded-degree early waves follows from this cap alone.
