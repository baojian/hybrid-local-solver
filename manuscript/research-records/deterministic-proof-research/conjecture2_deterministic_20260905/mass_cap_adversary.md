# A deterministic tree–clique test for capped acceleration

Status: exact graph reduction, a conditional long-activity lemma, and
reproducible floating-point observations. The arrival conditions in the
lemma have not yet been proved uniformly from the zero initialization.
Therefore this is not yet an asymptotic counterexample, and is never a
counterexample to OP2 itself. No randomness is used.

## 1. The graph and parameter scales

Let L be a power of two, `theta=1/L`, `alpha=1/L^2`,
`h=16*log2(L)`, `W=2^h=L^16`, and `R=L^2`.
Take a complete rooted binary tree of depth h. To each of its W leaves
attach, by one edge, a separate clique on R vertices. Call the attachment
vertex of each clique its port, and the other R-1 vertices its bulk.
The seed is the tree root. The degrees are exactly:

* root: 2;
* other nonleaf tree vertices: 3;
* tree leaves: 2;
* clique ports: R;
* clique bulk vertices: R-1.

The total clique volume, including the external degree at each port, and
the total bulk volume are respectively

    Cvol=W*(R^2-R+1),    B=W*(R-1)^2.

Set `gamma0=1/16` and `rho=gamma0*L/Cvol`. Then

    rho*B=gamma0*L*(B/Cvol),
    1/rho=Theta(L^19),
    maximum degree=L^2,
    number of vertices=Theta(L^18).

All logarithms of graph size and inverse parameters are O(log L). The
degree guard `d_i<=1/rho`, or any constant multiple thereof, removes
none of this graph. The target work scale is
`1/(rho*theta)=Theta(L^20)`.

The graph automorphisms are transitive on all W(R-1) bulk vertices:
binary-tree automorphisms move the leaves, and each clique permits all
permutations of its nonport vertices. The minimizer is unique and hence
constant on this orbit. If any bulk coordinate of the rho/2 minimizer
were positive, every bulk coordinate would be positive. For L>=64,
`rho*B>2`, contradicting its support-volume bound `2/rho`. Thus:

    every bulk vertex lies outside supp(x*_(rho/2)).       (1)

This conclusion is exact and does not rely on a numerical principal
solve. Every iteration with positive bulk auxiliary state really scans
B vertices' incident-edge volume outside the comparison support.

## 2. Exact equitable quotient and the bulk recurrence

For analysis only, the graph has h+3 orbits: the tree levels, the ports,
and the bulk. Aggregate mass variables sum the mass over every vertex
of an orbit; they are not per-vertex values. Let

    q=sum_ports u_i,       r=sum_bulk u_i,
    v=sum_ports V_i,       z=sum_bulk V_i,
    u=D^(1/2)x,            V=theta*D^(1/2)z_aux.

The column-stochastic operator `P=A D^(-1)` satisfies

    (P*u)_bulk=(R-1)/R*q+(R-2)/(R-1)*r.

The within-bulk term is essential. Edges between two bulk vertices
are represented by a quotient diagonal; omitting it would give the
wrong graph and the wrong recurrence.

With `a=1-theta`, `lambda=alpha*rho`, the sum of the uncapped raw
auxiliary mass over the bulk is exactly

    Zraw=a*(1-1/[2(R-1)])*z
          +a*(R-1)/(2R)*(q+v)
          -a/(2(R-1))*r-lambda*B.                        (2)

All bulk vertices have the same raw density. The weighted simplex
projection therefore either rejects the entire bulk or leaves every
bulk vertex positive. If its common mass-coordinate multiplier is eta,

    znew=[Zraw-eta*B]_+.                                 (3)

Let Araw be the sum of all positive raw auxiliary masses outside the
bulk. The projection alone gives

    znew>=min(Zraw, theta-Araw)                            (4)

whenever `Zraw>=0` and `Araw<=theta`. If the cap is inactive, (4) is
immediate. If active, the projected outside mass is at most Araw and
the total projected mass is theta.

## 3. A conditional half-L persistence lemma

Assume L>=64. Suppose at some iteration t0:

    q_t0>=theta,             z_t0>=theta/2.                (5)

For the ordinary averaging primal update and for the monotone segment
variant, coordinatewise `u_(t+1)>=a*u_t`. Consequently for
`0<=j<=floor(L/2)`,

    q_(t0+j)>=a^j*q_t0>=theta/2.                          (6)

Suppose additionally that throughout these `floor(L/2)` steps,

    Araw_t<=theta/2.                                      (7)

Then every one of those iterations leaves all bulk coordinates positive,
and in fact `z_(t+1)>=theta/2`.

Here is an explicit induction with generous constants. Both primal
variants preserve the mass cap, so `r<=1`; also `v>=0`. For L>=16,

    a*(1-1/[2(R-1)]) >= (15/16)^2,
    a*(R-1)/(2R)     >= (15/16)^2/2,
    a*r/[2(R-1)]     <= theta/16,
    lambda*B          <= theta/16.

Using `z>=theta/2`, (6), and (2),

    Zraw>=(547/1024)*theta>theta/2.

Equations (4) and (7) therefore give `znew>=theta/2`, completing the
induction. No line-search lower bound is needed: (6) holds for every
segment fraction in [0,1].

The kinetic adjacency work on this interval is at least

    floor(L/2)*B.

After normalization by the target `1/(rho*theta)`, its size is

    rho*theta*floor(L/2)*B=Theta(L).                       (8)

Thus a uniform zero-start proof of the arrival and outside-raw conditions
(5)-(7) would refute the proposed ordinary/monotone capped algorithm's
OP2 work bound by a polynomial factor. It would not refute OP2 or rule
out other deterministic algorithms. Condition (7) is substantive and
must not be granted from a cap on projected auxiliary mass.

### A polynomial objective tolerance forces the charged interval

For the monotone variant the conditional work statement is not an
artifact of unnecessarily continuing after convergence. Write q* for
the total port mass at the true rho minimizer. The bulk is inactive by
(1). Summing the active KKT equations and keeping just the edges from
active ports to their inactive bulk gives

    c*(R-1)/R*q*<=alpha,

so `q*<=4*alpha` for the stated parameter range. During the interval
in section 3, `q>=theta/2`. For L>=64 this implies
`q-q*>=theta/4`. Cauchy-Schwarz on the ports, whose total volume is WR,
and alpha-strong convexity yield

    J(x)-J(x*) >= alpha/2*||x-x*||_2^2
                >= alpha*theta^2/(32*W*R)
                 = alpha^2/(32*W*R).                     (9)

Thus choose `epsilon=alpha^2/(64*W*R)`. Its inverse logarithm is only
`(p+6)*log L+O(1)` when h=p log2 L. The objective is nonincreasing for
the monotone segment variant (and after any objective-decreasing
cleanup), so every earlier iterate has at least the gap in (9) as well.
It cannot meet this tolerance before the charged interval has elapsed.
This argument remains conditional on the arrival and raw-mass
hypotheses, but it supplies the required tolerance without hiding a
polynomial overhead in an unusually small requested accuracy.

## 4. Deterministic floating-point diagnostics

`capped_tree_cube_probe.py --clique` implements the exact quotient
geometry above in double precision. It includes the within-bulk
adjacency term, weighted simplex projection, and the monotone segment
minimizer. The root has independently begun auditing the quotient and
finite arithmetic certificates. The values below are observations,
not interval certificates or a uniform asymptotic proof.

For h=16 log2 L, R=L^2, gamma0=1/16, and the first 4L iterations:

| L | Iterations with positive bulk V | Normalized outside kinetic work | Maximum outside position mass |
|---:|---:|---:|---:|
|128|275|17.18645|0.87586|
|512|1343|83.93718|0.90944|
|2048|5179|323.68742|0.91140|
|8192|20413|1275.81248|0.91287|

Because bulk activity is an all-or-nothing orbit event, the second
column directly counts how often the full bulk volume B is scanned.
The third column is exactly `rho*theta*B` times that count, up to
floating-point summation. Equation (1) justifies excluding all bulk
from the comparator support without any numerical support decisions.

For example, at L=8192 and iteration 512 the aggregate port position
mass is about `1.413*theta`, its auxiliary mass is zero, and the bulk
auxiliary mass is theta. For many following iterations the port remains
stopped and its stored position decays by a. The bulk auxiliary mass is
continually refilled from this stored boundary potential; the bulk
position mass grows close to one. The constant gamma0 bulk penalty is
overcome until the reservoir becomes small.

The dedicated `certificate` fields in subsequent probe outputs measure
the margins needed for (5)-(7), but still use floating point. At L=512,
the interval starting `t0=3h=432` and of length L/2 has minimum port
position mass about `0.671*theta`, minimum bulk auxiliary mass about
`0.9997*theta`, and maximum outside positive raw mass about
`0.000251*theta`. These margins are wide enough to motivate an exact
certificate; they do not replace one.

## 5. The aligned-primal variation must pay for its own support work

The same probe also supports the cap-aligned update

    p=a/2*(I+P)*(u+V)+alpha*e_seed-lambda*d,
    unew=min([p]_+, a*u+Vnew).

This changes the stored-position mechanism, so the persistence argument
in section 3 does not apply: `unew>=a*u` can fail. The diagnostic reports
both kinetic and primal support volumes for this variant. Positive
primal entries that remain after kinetic coordinates vanish cannot be
ignored unless a separate implementation pays for their management.
No general locality theorem or counterexample for this variant is
asserted here.

## 6. The proposed beta=1/4 relative-gradient cleanup

A further diagnostic applies repeated simultaneous Jacobi decreases
after the monotone primal step. In per-vertex degree-potential variables
`f_i=x_i/sqrt(d_i)`, put `q0=(1+alpha)/2` and

    g_i=grad J_i/sqrt(d_i),  beta=1/4,  tau=lambda/8.

An orbit is eligible when `f_i>0` and `g_i>beta*q0*f_i+tau`; all its
coordinates are replaced by `max(0,f_i-g_i/q0)`, then gradients are
recomputed. The original coordinate diagonal q0 is used, including in
the clique bulk; using the much smaller quotient diagonal would be a
different algorithm.

Simultaneous decreases are objective-decreasing for this Stieltjes
quadratic: every change is nonpositive, so every off-diagonal cross
term `Q_ij*delta_i*delta_j` is nonpositive. Thus the joint change is at
most the sum of the individual coordinate changes. This justifies a
symmetry-preserving diagnostic of the batched cleanup variant.

On all four clique instances in section 4, there were zero eligible
orbits in all 4L iterations. The kinetic support counts were identical
to those without cleanup. These are still floating-point observations,
but they caution against assuming that this threshold removes the
reservoir: its positive gradient can be less than one quarter of its
diagonal potential because nearby tree potential supports most of it.
The output files `capped_tree_clique_cleanup_L*.jsonl` record zero
cleanup passes and the unchanged work. No uniform lower bound for all
choices of cleanup threshold is claimed.

A smaller fixed threshold changes the transient, but a deeper fixed
prefix restores it in the floating-point diagnostics. At L=2048 and
the original depth factor 16, beta=1/64 reduces the bulk to 19 active
iterations and normalized kinetic-plus-cleanup work about 3.94.
With depth `h=64 log2 L` and the same beta=1/64, the observed numbers of
bulk-active iterations over the first 4L are 768, 4650, and 30733 for
L=512, 2048, and 8192. Their normalized outside kinetic work is about
48.0, 290.62, and 1920.81. The degree-weighted cleanup cost is tiny in
these examples. All size and inverse-parameter logarithms remain
O(log L) because 64 is fixed.

This is evidence that a fixed relative threshold can leave a sufficiently
smooth stored boundary potential. It is not an asymptotic proof for any
threshold, nor a result against thresholds that depend on graph/parameter
logarithms. Large orbit weights also increase the importance of an
independent interval or exact-arithmetic audit; the probe is not one.
