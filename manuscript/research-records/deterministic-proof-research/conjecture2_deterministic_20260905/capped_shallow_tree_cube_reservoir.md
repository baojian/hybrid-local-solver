# A certified persistent cube-layer reservoir from zero

Status: a rigorous reservoir lemma for a modified tree-and-cubes graph
under the ordinary lazy capped iteration. It does not yet prove a lower
bound on auxiliary-support work. The long-prefix last-tree-level lemma
requested for the separate clique construction remains unresolved.

Only the authorized problem definition and fresh notes/code from this
research run were consulted. No randomized algorithm is used.

## 1. Construction and theorem

Let `L=2^n`, `n>=16`, `theta=1/L`, `alpha=1/L^2`, and
`a=1-theta`, `c=(1-alpha)/2`. Take a complete binary tree of depth
`h=n`. Attach **two separate d-dimensional cubes** to each tree leaf,
using one edge from that leaf to the distinguished corner of each cube,
where `d=192*n`. There are `W=L` tree leaves and `B=2*L` cubes.

The tree root has degree 2. Every other tree vertex, including a leaf,
has degree 3. Each cube corner joined to a tree leaf has degree d+1;
all other cube vertices have degree d. The total degree-volume of the
cubes, counting their attachment-edge incidences, is

    VolCube = B*(d*2^d+1).

Choose any `0<gamma0<=1`, and set

    rho=gamma0*L/VolCube, lambda=alpha*rho.

Start ordinary lazy capped acceleration at zero, in the notation of
`lazy_capped_acceleration.md`. There exist a time `k_*<=64*n` and a
cube Hamming layer `j_*<=64*n` such that the aggregate position mass
over layer j_* in all B cubes is at least

    theta/(130*n).                                    (1)

For every integer `0<=t<=L/2`, the mass of this same layer at time
`k_*+t` is at least

    theta/(260*n).                                    (2)

The chosen layer has degree-volume at most
`2*L^-12*VolCube`. Thus its position density is much larger than the
average density permitted by total position mass one on the cubes.

The position mass is a reservoir only; (1)-(2) do not assert that any
auxiliary coordinate on this layer, or on the rest of the cubes, remains
positive. Establishing such activity is a separate bootstrap problem.

## 2. The first theta-mass hitting time is early

Write mass coordinates `u=D^(1/2)x`, `V=theta*D^(1/2)z`. The ordinary
update is

    q=a/2*[P*(u+V)-(u-V)]+alpha*e_seed-lambda*dvec,
    Vnew=[q-eta*dvec]_+,
    unew=a*u+Vnew,

where eta is the simplex multiplier and `sum Vnew<=theta`. Thus
`u>=V>=0`, `sum u<=1`, and a binding cap produces position mass at
least theta immediately.

Rooted automorphisms preserve every iterate, so the tree levels and the
aggregate Hamming layers in all cubes form an exact equitable quotient.
Let ell denote graph distance from the tree root. Finite propagation
places time-k support at distances at most k-1.

Use the constants from `capped_total_flux_counterexample.md`:

    g=11/10, beta=57/55, h0=2/15, r=23/20,
    t0=a*r, b0=2*g=11/5.

For the radial weight `phi=g^ell`, every reached vertex through time
`k0=64*n` satisfies `P^T phi>=beta*phi`. The usual binary vertices
have backward probability 1/3. A cube's attachment corner has backward
probability `1/(d+1)<=1/3`. A reached noncorner cube vertex has Hamming
level at most `64*n<=d/3`, hence backward probability at most 1/3.
The root has only forward neighbors.

Let `D_ell` be the total degree on graph-distance layer ell. Up to
distance k0, successive values `g^ell*D_ell` grow by a factor at least
b0. For tree layers this follows from binary branching; at the cube
corner the degree increases; from that corner to cube level 1 the
degree-volume ratio is `d^2/(d+1)>=2`; and inside the cube the ratio
is `(d-j)/(j+1)>=2` throughout the reached levels.

Suppose total position mass stays below theta through k0. All preceding
caps are then nonbinding. With moments

    U_k=sum_i g^(ell_i)*u_(k,i),
    Z_k=sum_i g^(ell_i)*V_(k,i),
    m_k=min(U_k,Z_k/h0),

the same positive 2-by-2 cone calculation as in the total-flow note
gives

    m_(k+1)>=t0*m_k-15*lambda*g^k*D_k.                (3)

Indeed the weighted degree through distance k is at most
`2*g^k*D_k`, and division by h0 gives the coefficient 15. The cone
constants are exact: its two growth ratios are 952/825 and 127/110,
both greater than r. The initial moment satisfies `m_1>=alpha/2`.
Geometric growth of the weighted D layers allows the loss in (3) to
be summed, yielding the loose but convenient bound

    sum u_k >= alpha/(2*t0)*(t0/g)^k
                        -60*lambda*D_k.             (4)

Here we used `t0/b0<=23/44` and `U_k<=g^k*sum u_k`.

At distance k0, the corresponding cube Hamming level is at most d/3.
The binomial identity `(1+1/2)^d=sum_j binom(d,j)*2^-j` gives

    binom(d,j)/2^d <= (3/4)^d*2^j
       <= (27/32)^(64*n) <= L^-12.                  (5)

For the last inequality, `(27/32)^5<1/2` and `64*n>=60*n` suffice.
Consequently

    rho*D_k0 <= 2*L^-11,
    60*lambda*D_k0 <= 120*L^-13.                     (6)

Since `t0/g>33/32`, the first term of (4) at k0 exceeds 10/23.
Equations (4)-(6) contradict total mass below theta. There is therefore
a first time `k_*<=64*n` when total position mass is at least theta.

The argument stops at this first hitting time. It never makes an
entrywise comparison through a binding simplex cap.

## 3. Electrical comparison bounds all tree-only position mass

Put `Hmat=alpha*D+c*Lgraph`, so `Q=D^(-1/2)*Hmat*D^(-1/2)`.
This is a grounded network with conductance c on graph edges and a
ground conductance `alpha*d_i` at vertex i. Elementary energy
minimization for flows gives upper bounds on quadratic forms of
`Hmat^(-1)`; no graph algorithm is being assumed or run by this proof.

Send one unit from the root down the binary tree, split it equally
among the B cubes, then split it uniformly through cube Hamming layers
until level `m=d/2`, and send it to ground there. The energy is at most

    1/c + 1/(c*B)
       + 2/(c*B*d) + 1/[alpha*B*d*binom(d,m)] < 5.   (7)

The cube-edge bound follows from

    sum_(j=0)^(m-1) 1/[binom(d,j)*(d-j)]
       = (1/d)*sum_(j=0)^(m-1) 1/binom(d-1,j)
       <= 2/d.

The middle binomial coefficient is at least `2^d/(d+1)`, which makes
the ground term in (7) smaller than 1 for the stated parameters.
Thus `Hmat^(-1)_(seed,seed)<5` and
`b^T Q^(-1)b<5*alpha^2`.

The RPPR KKT equality gives
`||x*||_Q^2<=b^T Q^(-1)b`. Its zero-initialized acceleration energy is
at most this same quantity. Since the ordinary lazy capped iteration
decreases that energy, every iterate has `J(x)<=5*alpha^2`.
If `R=||x||_Q`, Cauchy-Schwarz gives

    J(x)>=R^2/2-sqrt(5)*alpha*R.

It follows that

    ||x||_Q <= (sqrt(5)+sqrt(15))*alpha < 7*alpha.    (8)

For the tree mass functional, inject physical source `d_i/T` at each
tree vertex, where `T=vol(tree)=6*W-4`, and send the resulting unit
flow outward to the same cube middle layers and then to ground. On a
tree edge leading to level j the flow is

    [vol(tree levels 0,...,j-1)/T]/2^j <= 3/T.

Its tree-edge energy is at most `18*W/(c*T^2)`. The attachment, cube,
and ground costs are those already used in (7). For `W=L>=2^16`,
their sum is at most `8/W`. If `q_i=d_i` on the tree and zero elsewhere,
we have therefore proved

    q^T Hmat^(-1)q <= T^2*(8/W) <= 288*W.            (9)

Applying Cauchy-Schwarz to (8)-(9) yields, at every iteration,

    sum_(i in tree) u_i
       <= sqrt(288*W)*||x||_Q
       < 120*alpha*sqrt(W)
       =120*L^(-3/2) <= theta/2.                    (10)

This is an analytical energy estimate. It does not scan or presume
access to the tree or to any optimum support.

## 4. Extracting and preserving one layer

At the first hitting time from section 2, the total position mass is
at least theta, while (10) places at most theta/2 on the tree. Thus
the cubes carry at least theta/2. Finite propagation allows at most
`64*n+1<=65*n` cube Hamming layers to be nonzero. One of them has
aggregate mass at least `theta/(130*n)`, proving (1).
The same binomial estimate (5), including the attachment corner's
degree d+1, bounds this layer's degree-volume by
`2*L^-12*VolCube`.

The lazy update is coordinatewise at least `a*u`. Hence the same
layer retains at least `a^t` times its mass after t more iterations.
For `t<=L/2`, Bernoulli's inequality gives

    a^t=(1-1/L)^t>=1-t/L>=1/2.

This proves (2).

## 5. Remaining interface to an actual-work lower bound

The theorem avoids the unpaid transport of a reservoir through a long
tree after caps begin binding. It produces a reservoir in an interior
Hamming layer, rather than at an attachment corner. A separate lemma
would have to convert that nonnegative persistent position mass into
many simultaneously positive auxiliary coordinates for many steps,
while accounting for cap subtraction, backward flow, and existing
auxiliary mass. Until then there is no support-work counterexample.

## 6. Exact barrier for the original long-prefix argument

For a general interval starting at s, dropping the nonnegative kinetic
term from the ordinary update gives the coordinatewise inequality

    u_(k+1)>=a*K*u_k-(lambda+eta_k)*dvec,
    K=(I+P)/2.

Since `K*dvec=dvec`, its exact iterated consequence is

    u_(s+t)>=a^t*K^t*u_s
       -dvec*sum_(r=0)^(t-1) a^(t-1-r)*(lambda+eta_(s+r)).

Without the cap multipliers, this is a useful deterministic transition-
matrix lower bound for spreading an existing reservoir. With the
simplex cap, however, no sufficiently small bound on the accumulated
eta terms has been proved. The weighted radial moment has the same
problem: its new loss is eta times the weighted degree of all included
layers. The cap constrains the sum of surviving auxiliary mass, rather
than this degree-weighted loss. Simplex projection is not coordinatewise
monotone, so an uncapped subsolution does not automatically survive it.

The first mass-hitting proof avoids these terms precisely because any
binding cap would itself complete the hitting event. It neither places
that mass at a prescribed distant tree level nor controls subsequent
transport through the capped long prefix. The shallow construction
above resolves the location issue using an independent energy bound,
not by assuming the missing cap-multiplier estimate.
