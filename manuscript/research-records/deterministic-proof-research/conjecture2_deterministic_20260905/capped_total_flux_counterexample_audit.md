# Independent audit of the initialized total-flow counterexample

The theorem in `capped_total_flux_counterexample.md` is correct for the ordinary
lazy capped recurrence. Its constants are valid for every integer n>=7. It is
an initialized deterministic counterexample to the stated total-flow sufficient
condition, not a counterexample to Conjecture 2 or cumulative selected-support
work. No experiment or other manuscript note is used in this audit.

## Recurrence and mass hitting time

In mass coordinates, the radial update is

    q=a/2*(P(u+V)-(u-V))+alpha*e_seed-lambda*d,
    Vplus=[q-eta*d]_+,  uplus=a*u+Vplus,

with nonnegative eta enforcing sum Vplus<=theta. It follows inductively that
u>=V>=0, mass(u)<=1, and mass(V)<=theta. Rooted automorphism invariance of the
unique projection preserves radial symmetry. Finite propagation gives depth
at most k-1 at step k. These facts do not depend on a claim that the cap binds.

If every position through step k0=64*n had mass less than theta, each cap used
to obtain it would be inactive: a binding cap gives mass(Vplus)=theta and
mass(uplus)>=theta. Since k0<H=132*n, weighted-moment propagation during this
contradiction argument only uses nonleaf transition rows.

For gamma=11/10, the nonroot nonleaf outward moment multiplier is
beta=(gamma^(-1)+2*gamma)/3=57/55. The root multiplier is gamma>beta. Thus the
moment matrix in the note is exactly

    M = [[56/55, 56/55], [1/55, 56/55]].

The weighted regularization charge must be restricted to layers at most k on
transition k to k+1. This is legitimate because these layers contain all old
support and all possible next support. Their weighted degree is exactly

    2+3*sum_(j=1)^k (11/5)^j = (11/2)*(11/5)^k-7/2,

which is at most 6*(11/5)^k. No negative penalty from unreachable vertices has
been silently dropped from a sum containing their positive mass: they have
zero next mass and are excluded from that sum on both sides.

For h=2/15, the two lower expansion ratios of M*(1,h) are 952/825 and 127/110,
both larger than r=23/20. With t=a*r, m_k=min(U_k,W_k/h), the forcing charge
is max(6,6/h)=45. The initial root mass is alpha*(1-2*rho)>=alpha/2, and it
is below theta, so the first cap is indeed inactive. Exact unrolling gives

    m_k >= (alpha/2)*t^(k-1)
           -45*lambda*((11/5)^k-(11/5)*t^(k-1))/(11/5-t).

Since 11/5-t>=21/20, the note's weaker error bound 60*lambda*(11/5)^k is
valid. Dividing by gamma^k is valid because depth is at most k-1. For L>=128,

    t/gamma >= (127/128)*(23/22) > 33/32,
    (33/32)^32 > 2.

At k=64*n the resulting mass lower bound exceeds 10/23-60*L^(-66)>1/3.
That contradicts mass<theta=1/L. Thus a hitting index k_*<=64*n exists.
This checks both alternatives: either a cap causes a crossing, or an entirely
uncapped prefix forces one. No prior cap event is assumed.

## Finite leaves and subsequent drift

The leaf degree sum is 2^H=L^132. At every actual state, the aggregate raw leaf
value is at most

    a*(mass(u)+mass(V))/2-lambda*2^H
       <=a*(1+theta)/2-L^2=c-L^2<0.

Here the leaf diagonal term is nonpositive by u>=V. Symmetry makes every leaf
raw coordinate equal, so aggregate negativity implies coordinatewise
negativity. The cap only decreases raw values. Starting from zero, leaves
therefore stay zero at every iteration, including after finite propagation
could otherwise have reached depth H. No leaf layer is deleted, and no
infinite-tree approximation is being used.

The distance function psi has drift 1 at the root, 1/3 at all interior vertices,
and -1 at leaves. Leaves have zero position mass. Consequently

    <psi,(P-I)u> >= mass(u)/3,
    ||(I-P)u||_1 >= mass(u)/(3*H).

After the hitting index, uplus>=a*u gives mass(u_(k_*+j))>=theta*a^j. The next
L terms have summed mass at least 1-a^L>1/2. Since c>=1/3,

    c*sum_(j=0)^(L-1)||(I-P)u_(k_*+j)||_1
        >1/(18*H)=1/(2376*n).

The last included index is at most 64*n+L-1<=8*L-1 for n>=7. All terms are
therefore inside the claimed horizon. Graph size is O(L^132); all logarithms
in the proposed total-flow bound are O(log L). The lower bound dominates
L^(-1) times any fixed polynomial in these logarithms asymptotically.

## Scope correction

The final scope sentence in the original note attributed nontransfer to line
search to loss of coordinatewise persistence. That particular explanation
needs correction. The monotone segment rule has

    uplus=(1-gamma)*u+(gamma/theta)*Vplus,
    0<=gamma<=theta,

so it still satisfies uplus>=a*u. What it loses is uplus>=Vplus, and, crucially
for the hitting-time proof, a binding auxiliary cap no longer implies primal
mass at least theta: gamma may be arbitrarily small or zero. The original
ordinary-lazy theorem is unaffected. The author was informed of this wording
correction; no extension to the line-search trajectory is asserted here.

The argument also supplies no large lower bound for the selected signed-flow
quantity or for rho*theta times cumulative auxiliary-support volume. Persistent
old position mass alone can pay the total-flow lower bound while auxiliary
coordinates are stopped. This distinction is essential to the theorem's scope.

## Audited extension: unselected positive-error forcing

The author's later extension is also correct. Let
f_k=[a*(P-I)*(u_k-u*)/2]_+. The vector (P-I)*(u_k-u*) has zero sum, so its
positive-part norm is half its full l1 norm. At the optimum, positive
c*(I-P)u* can occur only at the seed and is at most alpha there; all nonseed
active coordinates have negative divergence by KKT, and inactive coordinates
have divergence -c*P*u*<=0. Since divergence sums to zero,

    c*||(I-P)u*||_1<=2*alpha.

Using c=a*(1+theta)/2 and the reverse triangle inequality therefore gives

    ||f_k||_1 >= [c*||(I-P)u_k||_1/2-alpha]/(1+theta).

Summing the proved total-flow bound over 8*L steps yields

    sum_k ||f_k||_1 >= [1/(4752*n)-8/L]/(1+theta).

For n>=21, L=2^n>=76032*n; the right side is at least 1/(19008*n).
The unselected positive-forcing sufficient bound consequently fails as well.
This additional conclusion still does not contradict the selected signed-flow
ledger or establish a large cumulative selected-support lower bound.
