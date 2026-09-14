# A deterministic lazy reporter for capped one-projection acceleration

Status: a proved accelerated iteration and a fully charged implementation
reduction. The cumulative support-work bound in the last section is open.
This is not an OP2 proof.

No existing manuscript note other than the requested problem definition
was consulted. No algorithm or experiment here uses randomness.

## 1. Iteration

Use the orthant quadratic

    J(x)=0.5*x^T Qx-b^T x+alpha*rho*w^T x,  w=sqrt(d).

Its minimizer belongs to

    C={x>=0 : w^T x<=1},

because the RPPR solution is dominated by unregularized PPR in mass.
Write `theta=sqrt(alpha)`, `a=1-theta`, and `L0=Q-alpha*I`.
For `0<alpha<1`, start `x_0=z_0=0` and iterate

    y_k=(x_k+theta*z_k)/(1+theta),
    z_raw=a*z_k+theta*y_k-grad J(y_k)/theta,
    z_(k+1)=Proj_C(z_raw),
    x_(k+1)=a*x_k+theta*z_(k+1).

At alpha=1 the one-seed diagonal problem is solved directly.

Both x and z stay in C. The support of x is the union of the previous
nonzero z supports. This union need not be rescanned at every iteration.

## 2. Accelerated convergence

Let `p=y_k-grad J(y_k)`. Elementary algebra gives

    theta*z_raw = p-a*x_k.

Thus `x_(k+1)` is the Euclidean projection of p onto
`a*x_k+theta*C`, a subset of C. For

    E_k=J(x_k)-J(x*)+alpha/2*||z_k-x*||_2^2,

smooth descent for x and the projection inequality for z cancel exactly:
the former's additional squared distance is
`||x_(k+1)-p||²/2=alpha*||z_(k+1)-z_raw||²/2`, which the latter removes.
The remaining strong-convexity calculation gives

    E_(k+1) <= (1-theta)*E_k
       - alpha*theta*(1-alpha)/2*||z_k-y_k||_2^2.

In particular `J(x_K)-J(x*) <= a^K E_0`. The standard initial bound
`E_0 <= alpha/d_v` gives a deterministic sufficient iteration count
`O(alpha^(-1/2)*log(alpha/(d_v*epsilon)))`, with the usual nonnegative
interpretation when the zero vector already meets the requested gap.

This proof holds for the displayed convex-combination update. It must not
be silently substituted for an arbitrary other clipped momentum rule.

## 3. Exact lazy state

Maintain

    r_k=L0*x_k,    t_k=L0*z_k.

The x update gives

    r_(k+1)=a*r_k+theta*t_(k+1).

Thus both x and r receive one global multiplicative decay and sparse
updates. Put `sigma_k=a^k`, and store normalized entries

    X_i=x_(k,i)/sigma_k,    R_i=r_(k,i)/sigma_k.

After producing z_(k+1), update `sigma <- a*sigma` and add
`theta*z_(k+1,i)/sigma` to X_i, only on its support. Forming
`t_(k+1)=L0*z_(k+1)` costs one scan of that support, including each
adjacency entry and each repeated neighbor contribution. Add
`theta*t_(k+1,i)/sigma` to R_i on the resulting sparse support.

The degree of a newly encountered neighbor is obtained and charged once.
At most `O(vol(supp z_(k+1)))` vertices occur in this sparse update,
because all graph degrees are at least one. No neighbor's adjacency list
is recursively scanned.

## 4. The mirror query has one shared affine ordering

The raw mirror value is

    z_raw = a*z - r/[theta*(1+theta)]
                    - t/(1+theta) + b/theta - theta*rho*w.

Dividing coordinate i by w_i gives

    z_raw_i/w_i = sigma*K_i - theta*rho,

where the ordered key is

    K_i = -R_i/[theta*(1+theta)*w_i] + e_i/sigma,
    e_i = a*z_i/w_i - t_i/[(1+theta)*w_i] + b_i/(theta*w_i).

Only `supp(z) union supp(t) union {seed}` has a nonzero exception e_i.
This is at most the scanned support and its nonrecursively exposed
neighbors. In particular it is not the whole old x support.

Maintain a deterministic balanced binary search tree of K_i for exposed
vertices. It stores, for every subtree, the sum of weights `d_i` and the
sum of weighted keys `d_i*K_i`. Tied keys can be grouped, with a
deterministic list of labels for enumeration. Every key insertion,
deletion, or change costs O(log E), where E is the exposed word count.

At an iteration transition:

1. Revert the previous explicitly stored exception list to base keys.
2. Change the global scale sigma; unexceptional key order is unchanged.
3. Apply the sparse R updates, changing their base keys.
4. Install the new exceptions from z, t, and the seed.

These changes cost
`O((vol(supp z_k)+vol(supp z_(k+1))+1)*log E)`.
The order of the four steps can be rearranged while preserving the
displayed invariant; no query is made in the middle of the transition.

All unexposed vertices have x=z=r=t=b=0 and raw mirror value
`-theta*rho*w_i<0`. They cannot be selected. They need no record until a
charged adjacency scan first exposes them.

## 5. Weighted simplex projection without scanning all records

Euclidean projection onto C has the form

    z_(k+1,i)=w_i*[z_raw_i/w_i-zeta]_+,

where `zeta>=0`; zeta is zero if the unshrunk nonnegative vector has
mass at most one, and otherwise it makes the mass exactly one.
Set

    tau=(theta*rho+zeta)/sigma,
    tau_0=theta*rho/sigma.

Then

    z_(k+1,i)=sigma*w_i*(K_i-tau)_+,
    w^T z_(k+1)=sigma*sum_(K_i>tau) d_i*(K_i-tau).

The augmented tree evaluates this weighted tail in O(log E). If its
value at tau_0 is at most one, take tau=tau_0. Otherwise find the unique
threshold tau>tau_0 with tail mass one. A standard weighted water-filling
search uses the stored tail weight W and weighted-key sum T; within a
key interval the solution is `tau=(T-1/sigma)/W`. Descending the balanced
tree finds the correct interval in O(log E).

Enumerate only keys strictly larger than tau. Their number is exactly
the nonzero z support size; equality produces zero and is not emitted.
Consequently both projection and support discovery cost
`O(log E+|supp z_(k+1)|)` after the key updates. There is no scan of all
candidate positives rejected by the cap.

## 6. Complete work reduction and the one remaining theorem

Let `Z_k=supp(z_k)` and

    B_K=sum_(k=1)^K vol(Z_k).

All arithmetic, comparisons, adjacency inspections, degree replies,
ordered-tree changes, mirror threshold evaluations, sparse materialization,
and final output are bounded by

    O((B_K+K+1)*log(E+2)).

Storage is O(E), with `E=O(B_K+1)`. To emit x_K, traverse its stored
nonzero normalized entries once and multiply by sigma_K. Their number
is at most `sum_k |Z_k|<=B_K`. The old x support therefore contributes
neither an uncharged terminal scan nor repeated full gradient work.

This establishes the implementation reduction; it does **not** bound B_K.
An estimate such as

    B_K <= O((K/rho + 1/(rho*sqrt(alpha)))
                     * polylog(1/alpha,1/rho,E))

would prove deterministic OP2 with the displayed accelerated K. That
support estimate remains open. Capped tree experiments motivate it but
are not a proof.
