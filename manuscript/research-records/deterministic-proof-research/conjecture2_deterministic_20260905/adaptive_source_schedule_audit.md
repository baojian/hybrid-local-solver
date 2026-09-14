# Adaptive continuation from the exact repaired-source maximum

This is a mathematical audit of a proposed scheduling refinement. It does not change the current code or the main theorem. It uses the graph, objective, stage, repair, and arithmetic hypotheses already stated in `deterministic_conjecture2.tex` and its practical appendices. All choices and arithmetic are deterministic.

**Verdict.** The proposed schedule is valid. It preserves the proved objective accuracy, local-work bounds, default-grid bit bounds, and optional certified stage shortenings. Nonfinal stages reduce regularization by a factor between two and four. Moreover, the proposed predecessor-independent estimate `eta <= 5 eta_*(r)` can be strengthened to `eta <= 4 eta_*(r)` for every valid cap-four diffuse baseline.

## 1. Source maximum after repair

Write `w_i=sqrt(d_i)`, `lambda_r=alpha*r`, and `s=b-Q bar`. Suppose a completed nontrivial stage at `r` has been repaired so that

\[
0\le\bar x\le x_r^*,\qquad 0\le s\le2\alpha r w,
\qquad 0<r<1/d_v.
\]

Define the exact scalar

\[
M(\bar x)=\max_i s_i/w_i.
\]

Then

\[
\boxed{\alpha r\le M(\bar x)\le2\alpha r.}
\tag{1}
\]

The upper bound is the repair guarantee. For the lower bound, suppose `M < alpha*r`. Then `Q bar >= b-alpha*r*w`, so `bar` is a nonnegative supersolution of the obstacle problem at `r`. The least-supersolution property gives `x*_r <= bar`. Combined with the assumed reverse inequality this gives equality. The nontrivial point-source regime has a positive optimum coordinate (in fact the seed is positive), and on every such coordinate its source equals `alpha*r*w_i`. This contradicts `M < alpha*r`. Equality in (1) is possible and causes no difficulty.

Only `supp(bar)`, its immediate neighbors, and the seed can have nonzero source. Therefore the maximum is obtained by a finite, exact source assembly and scan over those records; no unknown outside vertex participates.

At the initial threshold `r_0=1/d_v`, use `bar=0=x*_{r_0}`. Here the positive-support argument is inapplicable, but the source is explicit:

\[
M(0)=\alpha/d_v=\alpha r_0.
\tag{2}
\]

## 2. Complete adaptive schedule

First perform the existing direct branches: if `rho*d_v >= 1`, return zero; if `alpha=1`, return the exact seed-only optimum. In the remaining regime initialize `r_old=1/d_v` and `bar=0`. While `r_old>rho`, assemble its exact source and set

\[
r_{\rm next}=\max\{\rho,M(\bar x)/(4\alpha)\}.
\tag{3}
\]

At `r_next`, use the existing correction algorithm and its chosen proved stage certificate, followed by the existing repair. Intermediate stages take the ordinary shift `delta=alpha*r_next/2`; the final stage additionally halves the shift until `2*delta^2/rho <= epsilon`. Use the existing appropriate tolerance for the chosen repair: `alpha^3*delta^2/2` for the main exact repair, or `alpha*delta^2/8` for the bounded rounded PG repair. Replace `r_old` and `bar` by the completed stage and its repaired output. Stop immediately after the target stage; no next-source scan is required then.

The first stage is `max(rho,r_0/4)` by (2). At every subsequent transition, (1) gives

\[
r_{\rm old}/4\le M/(4\alpha)\le r_{\rm old}/2.
\tag{4}
\]

Thus every **nonfinal** stage has `r_old/4 <= r_next <= r_old/2`. A target-clamped final stage can be closer to `r_old`; it instead satisfies `r_old/4 <= r_next=rho < r_old`. It would be incorrect to assert the upper-half bound for that final stage.

At each new stage, directly from (3),

\[
0\le s\le4\alpha r_{\rm next}w.
\]

Since `r_next <= r_old`, optimum monotonicity also gives `0 <= bar <= x*_{r_next}`. These are precisely the diffuse-source stage hypotheses. No factor-two predecessor condition is required: it is replaced by the measured source maximum. The ordinary mass cap or the exact source-mass cap remains feasible. The repair restores (1)'s upper bound and safety at the new regularization. This closes the induction.

The fixed-horizon, source-energy, binomial-block, and geometric-checkpoint stage options are valid here because their certificates and work bounds require only the current stage hypotheses. They do not require the regularization to have arisen by literal dyadic halving. A zero-iteration stage still pays source initialization and terminal repair, whose guarantees supply the next invariant. Since regularization strictly decreases and nonfinal transitions at least halve it, zero-iteration stages cannot prevent termination.

For the actual stages `r_1,...,r_J=rho`,

\[
J=O(1+\log(1/\rho)),\qquad
\sum_{j=1}^J1/r_j<3/\rho.
\tag{5}
\]

Indeed the reciprocals of all prefinal stages grow by at least a factor two; their sum is less than twice the last prefinal reciprocal, which is less than `2/rho`. Add the final reciprocal. This also covers the one-stage case.

## 3. Paid local access and arithmetic work

Assemble `s` from the repaired baseline, never from an approximate lazy neighbor-response record. If its support volume is `V_bar`, scanning its rows, exposing/querying boundary degrees, forming exact source values, and taking the maximum costs

\[
O((1+V_{\rm bar})\log(N+2))
\]

deterministic word/arithmetic operations and `O(V_bar)` adjacency inspections. The number of possible source records is at most `1+2V_bar`. A maximum comparison retains one selected value and its vertex; it does not sum degree denominators. One may reuse the assembled source for the next corrector. If the implementation instead assembles it again, both passes are charged and only a constant factor changes. Repeated cached reads are charged as reads. The initial zero-baseline maximum uses only the seed degree and constant arithmetic.

At the new stage, `V_bar <= 1/r_next`; alternatively the stronger bound below is available. Therefore this additional pass is absorbed by the existing stage ledger, including at zero iterations. The cumulative kinetic bound and reporter costs are unchanged because the numerical stage and all its hypotheses are unchanged. Equation (5) and the existing iteration bound prove the same

\[
\widetilde O(1/(\rho\sqrt\alpha))
\]

exact-real local work. This includes source evaluation, schedule comparisons, state updates, materialization, terminal repair, and output. The schedule uses no new real-arithmetic primitive beyond arithmetic and comparison.

For the bounded integer realization with its default grids, the explicit conservative bounds remain

\[
O(L^3/(\rho\sqrt\alpha))\ \text{word/arithmetic operations},
\qquad O(L/(\rho\sqrt\alpha))\ \text{adjacency inspections},
\tag{6}
\]

with the same logarithmic scale `L` as the practical schedules appendix, up to harmless absolute constants. Per-stage setup scans, zero-step stages, paid scalar rebases, checkpoint temporary-state creation/disposal, and terminal source/PG scans remain covered by the existing ledger. This conclusion concerns one complete default continuation call; extra manual stepping or output requests still require additional charges.

## 4. Rational schedule encoding does not compound

Let `alpha=A/D` and suppose the repaired baseline densities share the dyadic denominator `H`:

\[
\bar x_i/w_i=P_i/H,\qquad B_i=\sum_{j\sim i}P_j.
\]

The exact source density is

\[
\frac{s_i}{w_i}
=\frac{n_i}{2DHd_i},\qquad
n_i=2AH\mathbf1_{i=v}-(D+A)d_iP_i+(D-A)B_i.
\tag{7}
\]

The repaired-source guarantee makes all these numerators nonnegative. To choose a maximum, compare `n_i*d_j` with `n_j*d_i`; the common `2DH` cancels. If `i_*` attains the maximum, the non-clamped proposed parameter has the exact representation

\[
\frac{M}{4\alpha}=\frac{n_{i_*}}{8AHd_{i_*}}.
\tag{8}
\]

Reduction is optional for correctness. Only one degree denominator is retained, and `D` cancels. Formula (8) depends on the current **dyadic baseline** and the original `alpha`, not on an accumulated product of earlier regularization denominators. The target-clamped branch simply retains the input `rho`.

The stage values strictly decrease and stay at least `rho`. With the same default shift rules, `tau=alpha*delta^2/8` is nonincreasing and still obeys

\[
\tau\ge\min\{\alpha^3\rho^2/32,\alpha\epsilon\rho/64\}.
\]

Thus choosing the largest admissible dyadic grid preserves nested grids and `log H=O(L)`. It represents every preceding baseline exactly, even though the stage regularization itself is generally not dyadic. Source numerators (7), maximum cross products, the proposed parameter (8), and its comparisons with `rho` all have `O(b_par+b_graph+L)` bits. Inserting the represented new `r` into a stage's common denominators multiplies only a fixed number of quantities of this size. Rounded state updates again reset to the current dyadic grid, so there is no stage-count multiplication of coefficient lengths.

Consequently the same envelope `B=O(b_par+b_graph+L)` and conservative schoolbook/gcd bit-arithmetic bound `O(B^3 L^3/(rho sqrt(alpha)))` remain valid for the default complete algorithm. Integer quotient/remainder and encoded oracle replies are charged as in the existing appendix; any extra computation inside a user-supplied graph oracle is additional. These are rational-input claims, not a claim about unchecked fixed-precision floating point.

## 5. A sharper predecessor-independent mass lemma

The following lemma applies to **any** valid diffuse baseline at the current regularization, independent of how that stage was selected. Let `C>=1` and assume

\[
0\le\bar x\le x_r^*,\qquad 0\le b-Q\bar x\le C\alpha r w.
\]

Put `eta=1-w^T bar`, `eta_*(r)=1-w^T x*_r`, and `S=supp(x*_r)`. Then

\[
\boxed{\eta_*(r)\le\eta\le C\eta_*(r).}
\tag{9}
\]

To prove the upper bound, write `xi=x*_r-bar`. It is nonnegative and zero outside `S`. Stationarity on `S` gives

\[
Q_{SS}\xi_S=s_S-\alpha r w_S\le(C-1)\alpha r w_S.
\]

The Stieltjes principal matrix is inverse-positive. Moreover, its off-diagonal signs and `Qw=alpha*w` give

\[
Q_{SS}w_S=\alpha w_S-Q_{S,S^c}w_{S^c}\ge\alpha w_S,
\]

so `Q_SS^{-1} w_S <= w_S/alpha`. Therefore

\[
0\le\xi_S\le(C-1)r w_S,
\qquad
\eta-\eta_*(r)=w^T\xi
\le(C-1)r\operatorname{vol}(S)
\le(C-1)\eta_*(r).
\]

The last step is the standard KKT deficit-volume inequality. The zero-optimum case is immediate. This proves (9). All support matrices in this argument are analytical; no new restricted solve or support oracle is used.

For the actual stages `C=4`, so `eta <= 4 eta_*(r)`. This is sharper than the proposed `5` obtained using only `xi <= Q^{-1}s <= 4r*w`. Since `eta_*(r)/r` is nonincreasing as `r` increases,

\[
\eta_j/r_j\le4\eta_*(\rho)/\rho
\tag{10}
\]

at **every** stage, including the first adaptive stage and any target-clamped final stage. This uses no predecessor ratio. The seed positivity argument also gives `eta_j >= r_j`, funding constant setup and zero-step charges. The actual default-grid perturbation budget and cumulative stored kinetic bound remain

\[
\Gamma\le\alpha^2 r_j\eta_j,
\qquad \sum_{k<K}\operatorname{vol}(\operatorname{supp}z_{k+1})
\le360\eta_jK/r_j.
\]

Together with (10), all earlier baseline/source, historical record, rebase, checkpoint, terminal, and output charges yield the same stronger bounds

\[
O\!\left(\frac{\eta_*(\rho)L^4}{\rho\sqrt\alpha}\right)
\ \text{word/arithmetic operations},\qquad
O\!\left(\frac{\eta_*(\rho)L^2}{\rho\sqrt\alpha}\right)
\ \text{adjacency inspections}.
\]

The unchanged bit envelope supplies the same `B^3` multiplier. The ordinary bounds (6) remain valid simultaneously. Final repair still estimates the optimum deficit within the existing factor `1+alpha`; adaptation does not alter that output guarantee.

No claim is made that the adaptive schedule improves elapsed time on every input or reproduces the dyadic schedule's trajectory. It is a different deterministic continuation schedule with the same proved guarantees. No numerical experiment is used in this audit.
