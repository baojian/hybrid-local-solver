# Independent audit of the lazy capped acceleration reduction

Root audit, 2026-09-05. This verifies the convergence and implementation
reduction in `lazy_capped_acceleration.md`. It does not prove the missing
cumulative support bound and therefore is not a proof of OP2.

Only the user-designated problem definition and work freshly produced in
this task were used. No randomized procedure is involved.

## Convergence

Put theta=sqrt(alpha), a=1-theta, g=grad J(y), p=y-g, and
zraw=a z+theta y-g/theta. The identity

    theta*zraw=p-a*x

follows from (1+theta)y=x+theta z and alpha=theta^2. Hence for the
one-projection update xplus=a*x+theta*zplus,

    ||xplus-p||^2=alpha*||zplus-zraw||^2.

Smoothness bounds J(xplus) by J(y)-||g||^2/2 plus half the left side.
The Euclidean projection inequality against x* in C removes half alpha
times the right side from the auxiliary-distance potential. Thus these
terms cancel exactly. Expanding the remaining square and applying alpha
strong convexity from y to x and x* gives

    Eplus <= a*E
             -alpha*a/2*||x-y||^2
             -alpha*a*theta/2*||z-y||^2.

Using x-y=-theta(z-y) gives the displayed dissipation coefficient
alpha*theta*(1-alpha)/2. Feasibility of xplus follows by convexity of C.
The proof uses neither coordinatewise monotonicity of x nor safety relative
to x*. It is valid for arbitrary positive definite Q with the same spectral
bounds when the optimum belongs to C.

At the optimum, complementarity gives J(x*)=-x*^T Qx*/2. Since
Qx*=h on its support, x*<=Q^{-1}b and ||b||^2=alpha^2/d_v imply

    x*^T Qx* <= b^T Q^{-1}b <= alpha/d_v,
    alpha*||x*||^2 <= alpha/d_v.

Consequently E0<=alpha/d_v, as claimed. The alpha=1 case is diagonal and
must be handled directly because the lazy scale a vanishes.

## State and ordering

L0=Q-alpha I=c(I-D^{-1/2} A D^{-1/2}). The update
rplus=a*r+theta*L0*zplus is exact. Computing L0*zplus touches only its
support and one adjacency scan per supported vertex. Repeated neighbor
contributions are charged separately, including contributions read from
the cache. Every newly encountered neighbor needs its degree, but not its
adjacency list. Diagonal terms cost one operation per support vertex.

Substituting g=alpha*y+L0*y-b+alpha*rho*w verifies

    zraw=a*z-r/[theta*(1+theta)]
               -L0*z/(1+theta)+b/theta-theta*rho*w.

Only current z, the support of L0*z, and the seed have a nonzero exception
to a common scale and shift of the stored base key. Reverting old exceptions
before changing the common scale is necessary. Processing both the old and
new exception lists costs the sum of the corresponding support volumes;
this does not cause an additional union-of-all-history scan.

Any vertex never exposed by an adjacency scan has zero x,z,r,L0*z,b and
negative raw mirror value. Therefore the ordered tree contains every vertex
that could enter the next z support. Exposure and storage are charged to
the scans that generated those records.

## Projection and complete accounting

The weighted simplex projection is

    zplus_i=sigma*w_i*(K_i-tau)_+.

The active constraint is a weighted tail sum with weights d_i. A balanced
ordered tree augmented with subtree weight and weighted-key sums supports
deterministic water filling. Descending the tree locates the interval
containing tau; arithmetic within that interval uses its affine tail-sum
formula. Strictly positive entries are then enumerated in time proportional
to their count. Vertices rejected by the cap need not be individually
visited during that query.

Each iteration has O(log(E+2)) overhead and O(log(E+2)) per sparse record
change. Since d_i>=1, supported vertices, exposed neighbors, degree replies,
and all repeated edge contributions are bounded by the charged support
volume. Final x output visits the stored union once, whose size is bounded
by the sum of z support sizes. Therefore the asserted work reduction

    O((K+1+sum_k vol(supp z_k))*log(E+2))

is valid in the source's exact-real algebraic word model. Finite precision
and bit growth of sigma^{-1} require a separate analysis; they are outside
that model and cannot be inferred from this audit.

## Remaining obligation

Mass(z)<=1 bounds values but does not bound the degree volume of its
strictly positive support. Positivity without a quantitative lower value
is insufficient. The required cumulative support estimate remains open.
Exact tree experiments and favorable finite cap behavior cannot replace it.
