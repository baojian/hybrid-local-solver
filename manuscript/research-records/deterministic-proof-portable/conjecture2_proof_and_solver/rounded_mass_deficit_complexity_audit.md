# Mass-deficit complexity for the actual default rounded solver

Independent mathematical audit of the same implemented algorithm. No code,
grid, projection, schedule, stopping rule, or repair is changed. The result
applies to the default wrappers with the actual correction cap
`eta=1-mass(baseline)`, scalar-only rounded rebases, and the audited final
PG/grid/maximum repair. It includes the integer, source-energy, binomial,
early-stop, combined, direct-exception, and trajectory-equivalent fast
variants. It does not automatically apply to older experimental correctors
that retained a unit correction cap or used different state updates.

The strengthening is sound. In the nontrivial case put

`M_* = eta_*(rho)/rho`,  `eta_*(q)=1-w^T x*_q`.

The default implementations have deterministic local word/arithmetic work
`O(L^4 M_*/sqrt(alpha))`, and conservative bit work
`O(B^3 L^4 M_*/sqrt(alpha))`, with the same `L` and `B` as the existing
integer/source complexity corollary. The logarithmic fourth power below is
a conservative stage sum, not a claim of a constant geometric sum for the
mass-weighted quantities. Since `eta_*(rho)<=1`, the earlier bounds also
remain available; one may take the smaller of the two proved estimates.

## 1. Exact deficit and its lower bound

For any regularization `q>0`, let `v_q=b-Qx*_q`. Obstacle KKT and the
Stieltjes signs give

`0<=v_q<=alpha*q*w`, and `v_(q,i)=alpha*q*w_i` on `supp(x*_q)`.

Using `Qw=alpha*w` and `w^T b=alpha` gives

`w^T v_q=alpha*eta_*(q)`,
`q*vol(supp x*_q)<=eta_*(q)`.

When `q*d_seed<1`, the optimum is nonzero and its seed coordinate is
positive. Indeed at a zero seed coordinate its gradient would be at most
`-alpha/sqrt(d_seed)+alpha*q*sqrt(d_seed)<0`, contradicting KKT.
Consequently

`eta_*(q)/q >= vol(supp x*_q) >= d_seed >= 1`.

At a continuation stage `r`, the safe baseline obeys `0<=bar<=x*_r`, so

`eta=1-w^T bar >= eta_*(r) >= r*d_seed >= r`.

Every actual nontrivial stage has `r<1/d_seed<=1`. Thus its mass cap is
strictly positive and `eta/r>=1`. These facts absorb otherwise additive
seed, scalar, and zero-step setup charges. The zero and `alpha=1` global
branches remain direct constant-word cases.

## 2. Retaining the source mass in the perturbed auxiliary energy

The source is `s=b-Qbar`, with
`0<=s<=4*lambda*w`, `lambda=alpha*r`, and
`m_s=w^T s=alpha*eta`. The analytical comparator
`t=Q^{-1}s` lies in the actual box/mass cap:

`0<=t<=4*r*w`,  `w^T t=eta`.

The true correction `e*=x*_r-bar` also lies in that set. At a binding mass
face the auxiliary projection-normal contribution is
`gamma*(alpha*eta-m_s)=0`. Lower and upper normal signs are the same as in
the original proof. Hence both perturbed comparison recurrences remain
valid. The existing error estimates used only mass at most one, so they
remain valid unchanged when the cap is the smaller `eta<=1`.

Write

`A(xi)=0.5||Qxi-s||^2+alpha*lambda*w^T xi`,
`B_k=A(xi_k)-A(t)+(mu/2)||z_k-t||_Q^2`, `mu=theta^2<=alpha`.

From `||s||^2<=4*lambda*m_s`, `A(t)=lambda*m_s`, and
`t^T s<=4*r*m_s`, one obtains

`B_0<=3*lambda*m_s`.

The proved perturbation recurrence gives
`B_k<=a^k B_0+Gamma<=3*lambda*m_s+Gamma`.
This argument does not assume `B_0` or `B_k` is nonnegative. Dropping the
nonnegative mirror term and the nonnegative linear penalty in `A` yields

`A(xi_k)<=4*lambda*m_s+Gamma`,
`||Qxi_k-s||^2<=8*lambda*m_s+2*Gamma`.

For `v=s-Qe*=b-Qx*_r`, KKT gives
`0<=v<=lambda*w`, `w^T v<=m_s`, and hence `||v||^2<=lambda*m_s`.
The elementary squared triangle bound therefore proves for every prefix

`||Q(xi_k-e*)||^2 <= 18*lambda*m_s+4*Gamma`
`                         =18*alpha^2*r*eta+4*Gamma`.

## 3. The existing grid is already sufficiently fine

The actual default stage sets

`tau=alpha*delta^2/8`, `delta<=alpha*r/2`,
`h<=theta*tau/256`, `Gamma=29*h/theta`.

These are upper bounds, so any extra refinement caused by an inherited
baseline denominator only helps this argument. They imply

`Gamma<=29*tau/256<=29*alpha^3*r^2/8192`.

Since `eta>=r` and `alpha<=1`,

`Gamma/(alpha^2*r*eta) <= (29/8192)*alpha*(r/eta) <=29/8192<1`.

Thus, without changing a bit of the implemented grid rule,

`||Q(xi_k-e*)||^2 <=22*alpha^2*r*eta`.

The adverse raw-flow coefficient is also unchanged:
`nu=theta*kappa_raw<=2*h<=lambda/4`. For example
`2*h<=tau/256<=alpha^3*r^2/8192<=lambda/4` suffices.
All inequalities include final stages whose shift was halved further for
epsilon. No extra inverse-eta precision or parameter is needed.

## 4. The rounded selected-flow bound retains eta

Choose the analytical core `C=supp x*_(r/2)`. It is not supplied to the
algorithm. Monotonicity gives `bar<=x*_r<=x*_(r/2)`, so

`vol(C)<=2*eta_*(r/2)/r<=2*eta/r`.

The outside-core gradient margin remains `lambda*w/2`. In the notation of
the perturbed selected-flow proof, let `D_out` be cumulative emitted volume
outside `C`, let `B_vol=K*vol(C)`, and put `Y=D_out+B_vol`.
The response bound just proved gives

`H2<=22*alpha^2*r*eta*K`.

The same selected signed-flow inequality and `nu<=lambda/4` yield

`lambda*D_out/2 <= sqrt(Y*H2)+nu*Y`,
`Y <=2*B_vol+4*sqrt(Y*H2)/lambda`,
`Y <=4*B_vol+16*H2/lambda^2`.

The final line follows from
`4*sqrt(Y*H2)/lambda<=Y/2+8*H2/lambda^2`.
The total actual stored kinetic volume is at most `Y`. Therefore

`W_K=sum_{k<K}vol(supp z_(k+1)) <=360*eta*K/r`.

This counts all appearances of all emitted vertices. It applies to every
prefix and to rounded support decisions; it makes no smallest-positive
entry assumption. The fact that the reporter omits sub-grid positive
projection coordinates remains essential. Both scalar-response rounding
and downward primal/kinetic rounding have already been included in `Gamma`
and `nu` rather than discarded from this strengthened estimate.

## 5. Every implementation charge

Write `m=eta/r>=1` for a fixed stage and let `K` be its actual executed
steps, possibly zero. The following are the existing charge bounds with
the stronger parameter retained:

- Baseline support volume is at most `vol(supp x*_r)<=m`.
- Source initialization inspects at most that baseline volume; source
  records lie in its support, boundary, and seed, so there are `O(m)`.
- At most `N<=1+2m+W_K<=363*(K+1)*m` vertex records are exposed.
  The cache contains at most `m+W_K` adjacency entries.
- Current/old kinetic and boundary updates cost `O(W_K)` point operations;
  repeated fixed-source exception refresh costs `O(K*m)`. This includes
  direct-exception retirement/replacement and temporary-set reclamation.
- Source-energy statistics add one `O(m)` pass, including upward squared
  statistic rounding. The original and refined setup loops cost `O(L)`.
- Every candidate support volume is at most `m+W_k`; materialization,
  exact terminal PG, immediate grid truncation, and maximum with the old
  baseline cost `O((K+1)*m)` entries/records before AVL logarithms.
- Scalar rebases number `O(theta*K+1)` and each visit at most `O(N)`
  historical records. Their complete state/key reconstruction and old-map
  reclamation are charged. They read no adjacency.
- The two-tree root costs `O(log^2(N+2))` per step. Point operations add
  `O(log(N+2))` per charged record. Label/degree encodings are unchanged.
- Early checkpoints run only at geometrically spaced `k=T,2T,4T,...`.
  Each reads at most `(1+360k)*m` cached candidate entries/records.
  Their geometric sum is `O((K+1)*m)`, including failed tests, independent
  certificate work, and all temporary materialization/reclamation.

The zero-step case has no kinetic, rebase, or checkpoint work, but its
`O(m)` setup, source pass, output, and terminal repair remain counted.
The claimed bound therefore does not silently replace `(K+1)` by `K`.

Source/binomial schedules only shorten the prior prescribed horizon.
Early stopping checks the original objective directly and still satisfies
the same repair tolerance. Its checks leave all states unchanged, so the
auxiliary prefix bound holds even on an accepted prefix. Representation
and exact-arithmetic adapters preserve the actual rounded trajectory.

## 6. Relating every stage deficit to the final optimum

The executed repair satisfies
`bar_new<=x*_r`, `0<=x*_r-bar_new<=2*delta*w`, and
`2*delta<=alpha*r`. Thus

`eta_*(r)<=eta_new`
`   <=eta_*(r)+2*delta*vol(supp x*_r)`
`   <=(1+alpha)*eta_*(r)`.

This reuses the pointwise repair estimate and the support-volume identity;
it does not presume monotonicity of the Q-norm under coordinatewise error
reduction. It remains valid after the maximum with the old baseline and
after an epsilon-forced final shift reduction.

The optimizer is the least nonnegative supersolution of
`Qx>=b-alpha*r*w`. Convex combinations of supersolutions at two parameters
are supersolutions at their interpolated parameter, so each coordinate of
`x*_r` is convex in `r`. Therefore `eta_*(r)` is concave and nondecreasing.
At zero regularization `x*_0=Q^{-1}b` has mass one, hence `eta_*(0)=0`.
Concavity gives

`eta_*(R)/R <= eta_*(r)/r` for `0<r<=R`.

For a stage parameter `r_j` with previous parameter `r_prev`,
`r_j<=r_prev<=2*r_j`. Except initially, its baseline was the preceding
repaired output. Consequently

`eta_j/r_j <=2*(1+alpha)*eta_*(r_prev)/r_prev <=4*M_*`.

Initially `r_prev=1/d_seed`, the baseline and optimum there are zero, and
`eta_j=1`; since `r_j>=1/(2*d_seed)`,
`eta_j/r_j<=2*d_seed<=2*M_*`. Thus no initial-stage exception is needed.
There are `J=O(L)` stages, so

`sum_j eta_j/r_j <=4*J*M_*=O(L*M_*)`.

This is the appropriate weighted sum; it is not asserted to be a constant
multiple of `M_*`. Monotone baselines also give decreasing actual deficits,
but that alone is not used to erase the stage-count logarithm.

## 7. Explicit logarithms, bits, and optional prefix

Retain the prior definitions

`a0=ceil log2(1/alpha)`, `r0=ceil log2(1/rho)`,
`e0=ceil log2(max(1,1/epsilon))`,
`L=16+4*a0+3*r0+e0`, `T=1/theta<2/sqrt(alpha)`.

The unchanged default grids have `log2 H<L`; the original block bound is
`K<=T*L`, and all refined schedules are no longer. Since `eta<=1`, the old
exposed-size bound still ensures `log(N+2)=O(L)`. A stage consequently costs

`O(L+K log^2(N+2)+(K+1)*m*(1+theta*K)*log(N+2))`
`   =O(T*L^3*m)`.

Summing the weighted stage estimates gives

`O(L^4*M_*/sqrt(alpha))` word/arithmetic work,
`O(L^2*M_*/sqrt(alpha))` total adjacency-entry inspections.

The earlier geometric bounds remain simultaneously valid, giving the
optional tighter combined forms

`O((L^3/sqrt(alpha))*min(1/rho, L*M_*))` word work,
`O((L/sqrt(alpha))*min(1/rho, L*M_*))` adjacency inspections.

The earlier bounded-denominator argument is entirely unchanged. No new
stored scalar, denominator, or numerical operation is introduced by this
analysis. All stored and temporary values retain
`B=O(b_parameter+b_encountered_graph+L)` bits, and conservative naive
exact rational operations cost `O(B^3)`. This proves the bit bound stated
at the top. The sharper peak exposed state is `O(T*L*M_*)` words. Retained
stage outputs also fit it: each support has volume at most `M_*`, and
there are `O(L)` such summaries. Optional uncharged diagnostics or
arbitrarily expensive user-defined oracle internals are not included.

The observable final output deficit lies between `eta_*(rho)` and
`(1+alpha)*eta_*(rho)`. Also `M_*>=d_seed>=1`, so no inverse-deficit
logarithm exceeds the already allowed inverse-rho logarithm.

For interpretation only, summing the KKT upper bound over the whole graph
also gives `M_*<=vol(V)`. Thus
`vol(supp x*_rho)<=M_*<=min(1/rho,vol(V))`; equality with `vol(V)` holds
when the optimizer has full support. No graph-wide quantity is queried or
needed by the implementation to obtain this analytical improvement.

Finally, the separate optional singleton precheck has prefix word cost
`O(d_seed+1)<=O(M_*)` in this nontrivial regime. Its own trial ledger stays
separate from the fallback ledgers. Therefore it also preserves the
strengthened total bound, whether it succeeds, fails, or skips the row.
