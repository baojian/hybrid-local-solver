# Exact dyadic warm starts: forcing structure and a confinement theorem

This is fresh deterministic work for Conjecture 2. It does not prove the
conjecture on arbitrary graphs. It uses exact old optimizers only to state
and analyze a continuation stage; computing those optimizers is not free.
The final section distinguishes a proved family result from floating
trajectory diagnostics.

## 1. Every exact dyadic correction has two-sided small forcing

Let `Q=alpha*I+c*D^(-1/2)(D-A)D^(-1/2)`,
`c=(1-alpha)/2`, `w=sqrt(d)`, and
`b=alpha*D^(-1/2)e_s`. Fix `rho>0`, and write

\[
 x_o=x^*_{2\rho},\quad r_o=Qx_o-b+2\alpha\rho w,
 \quad h=b-\alpha\rho w-Qx_o=\alpha\rho w-r_o.
\]

Then, globally and coordinatewise,

\[
 \boxed{|h|\le\alpha\rho w.}
\]

Indeed, on the old positive support complementarity gives `r_o=0`.
On every old zero coordinate, off-diagonal nonpositivity gives
`(Qx_o)_i<=0`; since `b>=0`, KKT gives
`0<=r_o,i<=2*alpha*rho*w_i`. This proof also covers an old zero optimizer.

The true correction `e*=x*_rho-x_o` satisfies

\[
 0\le e^*\le\rho w,\quad w^Te^*\le1,
 \quad \operatorname{supp}e^*\subseteq S=\operatorname{supp}x^*_\rho,
 \quad \operatorname{vol}(S)\le1/\rho.
\]

On `S`, new stationarity yields `Q_SS e*_S=h_S`. Consequently,

\[
 \|Q_{SS}e^*_S\|_2^2\le\alpha^2\rho^2\operatorname{vol}(S)
 \le\alpha^2\rho,
 \qquad
 \|e^*\|_Q^2=h_S^Te^*_S\le\alpha\rho w^Te^*\le\alpha\rho.
\]

The global strengthening `||Qe*||^2<=2*alpha^2*rho` is proved in
`warm_spectral_incremental_lemma.md`. Thus the initial error is in a substantially smaller **restricted gradient**
class than a generic error of energy `alpha*rho`. The restriction to the
unknown true support matters: the global vector `h` has a negative
regularization entry at almost every unvisited vertex, so its global
Euclidean norm need not be local. Nor has the displayed small-gradient
bound been proved invariant under the constrained accelerated trajectory.

## 2. Box-constrained lazy acceleration

Set `theta=sqrt(alpha)`, `a=1-theta`, `P=A D^(-1)`. For a correction `xi`
and mirror correction `z`, use mass coordinates

\[
 u=D^{1/2}\xi,\qquad v=\theta D^{1/2}z.
\]

Initialize `u=v=0`. The ordinary lazy accelerated stage has raw update

\[
 q=\frac a2\{P(u+v)-(u-v)\}+D^{1/2}h.
\]

Project the corresponding mirror point onto
`{0<=z<=rho*w, w^Tz<=1}`. In these coordinates this gives

\[
 v_i^+=\min\{\theta\rho d_i,[q_i-\eta d_i]_+\},
 \quad\eta\ge0,\qquad
 u^+=a u+v^+.
\]

The multiplier enforces `sum vplus<=theta`. This is precisely a Euclidean
projection in the original mirror coordinates, so the ordinary convex
constraint acceleration proof applies. It also preserves

\[
 0\le u_i\le\rho d_i,\quad 0\le v_i\le\theta\rho d_i,
 \quad v\le u,\quad\sum u_i\le1.
\]

The following support result needs only these coordinate bounds and the
nonnegative cap multiplier; it does not charge a projection oracle for free.

## 3. A general sufficient box-confinement condition

Let `T` contain the old support, and let `d_T(j)` count neighbors of `j` in
`T`. Suppose that, for every `j outside T`,

\[
 \boxed{\quad (D^{1/2}h)_j+c\rho d_T(j)\le0.\quad}                 \tag{C}
\]

Then every initialized boxed lazy iterate is supported in `T`.

For induction, suppose `u,v` vanish outside `T`. At `j outside T`,

\[
 q_j\le\frac a2\rho(1+\theta)d_T(j)+(D^{1/2}h)_j
      =c\rho d_T(j)+(D^{1/2}h)_j\le0.
\]

The projection therefore leaves `vplus_j=0`, and `uplus_j=0` follows.

Condition (C) also implies that `x_o+rho*w_T` is a global supersolution
for the new obstacle problem. On `T`, its residual is
`r_o+c*rho*D^(-1/2)*(number of edges leaving T)`, hence nonnegative;
outside `T`, nonnegativity is exactly (C). Thus the least-supersolution
principle independently certifies `supp x*_rho subseteq T`.

This is a sufficient condition, not a universal continuation theorem.
In particular, enlarging `T` by every violation of (C) can propagate
through a large graph: it is not currently justified to assume that the
resulting closure has volume `O(1/rho)`.

## 4. Exact application: tree prefixes feeding large cliques

The following theorem rules out the earlier cold-start chamber mechanism
for this boxed, exact-warm-start variant.

Let `L>=64`, `theta=1/L`, `alpha=1/L^2`, and `R=L^2`. Start with any rooted
complete binary tree of depth at least one, with `W` leaves. Attach to each
leaf a separate clique of order `R` by one edge to a designated clique
port. Put

\[
 \gamma=1/16,\quad B=R^2-R+1,\quad
 \rho=\frac{\gamma L}{WB}.
\]

Let `T` consist of the tree and all ports; the other clique vertices are
called bulk vertices. Their degree is `R-1`; a port has degree `R`.
Then all exact optimizers at `2rho`, `rho`, and `rho/2` vanish on the bulk.
Moreover, every ordinary lazy accelerated correction from the exact
`2rho` optimizer, with the box in Section 2, vanishes on the bulk.

### Restricted optimum certificate

For any regularization `r>=rho/2`, solve the nonnegative obstacle problem
restricted to `T`, and extend by zero. Symmetry gives a common port density
`f_p=x_p/sqrt(d_p)`. It can be zero. Summing degree-weighted stationarity
over the positive restricted support gives

\[
 \alpha\sum_i d_i f_i+\alpha r\operatorname{vol}(S_r)
 +c\sum_{i\in S_r,j\notin S_r}A_{ij}f_i=\alpha
\]

when the seed is active; when the optimizer is zero the needed conclusion
is immediate. In particular,

\[
 cW(R-1)f_p\le\alpha.                                      \tag{1}
\]

At every bulk coordinate, the degree-scaled gradient is
`alpha*r*(R-1)-c*f_p`. It is nonnegative whenever
`r*W*(R-1)^2>=1`. Here

\[
 rW(R-1)^2\ge\frac{L}{32}\frac{(R-1)^2}{R^2-R+1}>1,
\]

because `L>=64` and `(R-1)^2/(R^2-R+1)>1/2` for `R>=3`.
The restricted optimizer consequently satisfies every full KKT condition.
This proves the asserted true-support confinement, without presupposing it
in the cut estimate.

### Trajectory confinement

Apply (1) to the old regularization `2rho`. At a bulk vertex,

\[
 (D^{1/2}h)_j=-\alpha\rho(R-1)+c f_{o,p},
 \qquad d_T(j)=1.
\]

Therefore (C) follows from

\[
 c\left(1+\frac{f_{o,p}}\rho\right)\le\alpha(R-1).             \tag{2}
\]

The cut estimate proves

\[
 \frac{c f_{o,p}}\rho
 \le\frac{\alpha}{\rho W(R-1)}
 =\frac{16}{L}\left(1+\frac1{R(R-1)}\right).
\]

The right side is less than `0.251` for `L>=64`, while `c<1/2`.
Thus the left side of (2) is less than `0.751`, whereas its right side is
`1-1/L^2>0.999`. Condition (C) holds with a fixed margin.

The volume of `T` is `W(R+5)-4`. In particular,

\[
 \rho\operatorname{vol}(T)
 <\frac{L(R+5)}{16(R^2-R+1)}=O(1/L).
\]

Thus `K=O(L*polylog)` iterations on this family cost
`O(K*vol(T)*polylog)`, which is within the conjectured target. No support
oracle is required for this upper bound: ordinary adjacency scans from the
old support and the evolving correction expose at most the incident edges
of `T`. Bulk degrees may be queried when first exposed, but bulk adjacency
lists are never needed because those coordinates never activate. Explicit
sorting for the capped box projection costs only a logarithmic factor in
the exposed coordinate count. This charges the stage once the exact old
solution has been obtained; it does not supply that old solution for free.

## 5. Barriers and diagnostics

The pointwise forcing bound alone does not make the free accelerated
linear recurrence order preserving. At `alpha=0`, its constant-forcing step
response has polynomials

\[
 p_0=0,\quad p_1=1,\quad
 p_{k+1}(t)=(1+t)p_k(t)-\tfrac12(1+t)p_{k-1}(t)+1.
\]

An exact rational expansion gives coefficient `-7/4` on `t^3` in `p_10`.
By continuity this coefficient remains negative for sufficiently small
positive `alpha`. Thus comparison by nonnegative Markov-polynomial
coefficients is unavailable. This is an algebraic proof-method barrier,
not a graph trajectory counterexample.

`dyadic_warm_corrector_probe.py` implements deterministic floating radial
diagnostics for the actual old principal optimum and this boxed recurrence.
The old solution is numerically approximated, so these runs are not exact
or interval certificates. The clique runs in
`dyadic_warm_clique_diagnostic.json`, with tree depth `16*log2(L)` and
`L=128,512,2048`, had zero kinetic activity outside the half-rho core over
`8L` iterations, as the theorem predicts. Their normalized kinetic work
`rho*theta*sum vol(Z_k)` was approximately `0.00380,0.000950,0.000237`.

A general proof still needs to control discovery outside a suitably small
set when condition (C) fails. The exact small-forcing and restricted-gradient
facts in Section 1 appear useful, but neither a preserved spectral bound
nor a general support-work theorem has been established here.
