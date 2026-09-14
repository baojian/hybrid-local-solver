# A paid-interface reduction for lazy homotopy boundary reporting

This note isolates a concrete missing numerical primitive. The algebra and
event budgets below are proved. A procedure that computes the required
pending harmonic boundary fluxes within that budget has **not** been proved.

## 1. A tolerant stationary prefix is enough for coarse support discovery

Let `S` have an exact positive restricted solution at regularization `rho`:

\[
 y_S=Q_{SS}^{-1}(b-\alpha\rho w)_S>0,\qquad y_{S^c}=0.
\]

The comparison principle gives `0<=y<=xstar_rho`, so
`vol(S)<=1/rho`. If the boundary certificate

\[
 (Qy-b+\alpha\rho w)_j\ge-\alpha\tau w_j
 \qquad(j\notin S)
\]

holds, then `y` is a supersolution at `rho+tau`, and hence

\[
 S(\rho+\tau)\subseteq S\subseteq S(\rho).
\]

Taking, for example, `rho=rho_target/2` and `tau=rho_target/2` produces a
support superset for the target problem with volume at most
`2/rho_target`. The final restricted accelerated solve can then be paid
normally. This criterion does not require reconstructing all exact
homotopy breakpoints.

The same certificate also gives

\[
 x^*_{\rho+\tau}\le y\le x^*_\rho,\qquad
 0\le x^*_\rho-y\le\tau w,
 \qquad
 J_\rho(y)-J_\rho(x^*_\rho)\le\frac{\alpha\tau^2}{2\rho}.
\]

For the last inequality, put `e=xstar_rho-y`. The exact quadratic gap is
`e^TQe/2`. The vector `Qe` is zero on `S` and is at most `alpha*tau*w` on
every coordinate outside `S` where `e` is positive. Thus
`e^TQe<=alpha*tau*w^Te<=alpha*tau^2/rho`.

## 2. Affine response pairs and boundary keys

For a current support `S`, write

\[
 p_S=Q_{SS}^{-1}b_S,\qquad
 g_S=\alpha Q_{SS}^{-1}w_S,\qquad y(\rho)=p-\rho g.
\]

For every outside vertex define

\[
 D_j=\alpha w_j-Q_{jS}g_S>0,\qquad
 N_j=b_j-Q_{jS}p_S,\qquad \kappa_j=N_j/D_j.
\]

Its residual is `D_j*(rho-kappa_j)`. Thus a negative-boundary pivot is
precisely a vertex with `kappa_j>rho`.

When one such vertex `i` is admitted, let `h=Delta g` denote the derivative
response for the enlarged support. Schur-complement algebra gives

\[
 \Delta p=\kappa_i h,\qquad
 \Delta y=(\kappa_i-\rho)h\ge0.
\]

The enlarged restricted solution remains positive and below `xstar_rho`.
This identity does not require selecting the largest key or following the
exact homotopy order.

For a vertex `j` still outside the enlarged support, set

\[
 \Delta D_j=-(Qh)_j\ge0.
\]

The key update is the weighted average

\[
 D_j^+=D_j+\Delta D_j,\qquad
 \kappa_j^+=\frac{D_j\kappa_j+\Delta D_j\kappa_i}
                  {D_j+\Delta D_j}.
\]

In exact homotopy order every remaining key increases toward the current
pivot key. With arbitrary negative pivots a key need not increase, but it
stays between its old value and the selected pivot key. In particular, an
upper bound `kappa_j<=rho_upper` is invariant.

## 3. The total boundary-coefficient budget

For any nested admission order, derivative responses `h_l` are positive,
pairwise `Q`-orthogonal, and satisfy

\[
 \|h_\ell\|_Q^2=\alpha w^Th_\ell.
\]

Let `B_l` be the newly admitted block and
`R_l=w^T[Qh_l]_+`. The positive part is supported on `B_l`, and the fresh
residual-source ledger proves

\[
 \sum_\ell R_\ell\le\sqrt\alpha\,\operatorname{vol}(S_{\rm final}).
\]

For completeness, if `r_l=(Qh_l)_(B_l)`, then
`0<r_l<=h_l` coordinatewise because `Q_ii<=1` and the off-diagonals are
nonpositive. Therefore
`||r_l||^2<=r_l^T h_l=alpha*w^T h_l`. Cauchy gives
`R_l<=sqrt(alpha*vol(B_l)*w^T h_l)`. Sum over the disjoint admission blocks
and use `sum_l w^T h_l<=vol(S_final)`.

Since `w^TQh_l=alpha*w^T h_l`, the total outside coefficient increase in
one admission is

\[
 \sum_{j\notin S_{\rm new}}w_j\Delta D_j
 =R_\ell-\alpha w^Th_\ell\le R_\ell.
\]

Consequently all outside coefficient increments have total weighted mass
at most `sqrt(alpha)*vol(S_final)`.

## 4. Lazy omission gives a controlled residual overestimate

Consider a phase with fixed current `rho` and pivot keys in
`[rho,rho_upper]`. Suppose some outside updates are pending rather than
delivered to the boundary reporter. Its stored `Dhat,Nhat` omit the
corresponding positive pairs `(Delta D, kappa_pivot*Delta D)`.
The stored residual obeys

\[
 \widehat r_j-r_j
 =\sum_{\text{pending }\ell}
       (\kappa_\ell-\rho)\Delta D_{\ell,j}
 \in[0,(\rho_{\rm upper}-\rho)\,P_j],
\]

where `P_j=sum_pending Delta D_(l,j)`.

A reported negative stored residual is therefore a valid negative pivot.
However, the response coefficient in `Delta p=kappa_i*Delta g` is the
**true current** pivot ratio, not its stale reporter ratio. Recovering or
certifying that ratio, including pending contributions at the pivot, is
also part of the paid numerical interface.
If `P_j<=eta*alpha*w_j` for every outside vertex and no stored residual is
negative, the true boundary certificate is

\[
 r_j\ge-\eta\alpha(\rho_{\rm upper}-\rho)w_j.
\]

Thus bounded pending coefficient mass gives exactly the tolerant stationary
certificate in Section 1. Constant-factor regularization phases make the
allowed slack a constant multiple of `alpha*rho`.

## 5. Why the reporter event count has the desired scale

Suppose a numerical primitive can detect and deliver a vertex's pending
updates whenever `P_j` reaches `eta*alpha*w_j`. Each such event consumes
at least `eta*alpha*d_j` of the total weighted coefficient budget. Hence

\[
 \sum_{\text{threshold events at }j}d_j
 \le\frac{\operatorname{vol}(S_{\rm final})}{\eta\sqrt\alpha}.
\]

Dictionary work per delivered event and per actual admission can therefore
fit the conjectured scale. New admitted adjacency lists also total at most
`vol(S_final)`. This is a genuine potential-event bound, not yet an
implementation bound.

## 6. The unresolved numerical primitive

The quantity `Delta D=-(Q Delta g)_outside` is a harmonic boundary response.
It is not supplied explicitly by a pivot. Computing it by materializing
every old coordinate of `Delta g` can exceed the event budget; declaring
it pending in an implicit record does not reveal which vertices have
crossed their pending threshold.

Ordinary monotone coordinate propagation is also insufficient by itself:
its cost has an additional absorption factor `1/alpha`, as proved in
`homotopy_residual_source_ledger.md`. A successful implementation must
compute or certify these thresholded cumulative boundary fluxes with a
paid persistent representation. The preceding reduction makes the required
primitive explicit, but does not assume it exists.

Initialization and phase-boundary treatment must also be paid. In
particular, an old pending update's pivot key can be much larger than a
later phase's `rho_upper`; it cannot simply be assigned the later,
smaller error multiplier. One must deliver it, retain its true age, or
recompute a certified phase state. A claim of a free phase flush would
reintroduce the same unresolved harmonic-response cost.
