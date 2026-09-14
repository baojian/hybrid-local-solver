# Independent audit of the optional source-driven schedule

This audit was derived independently from the proposed rule, using the
consolidated proof's current-stage and repair invariants. It changes no
algorithm, implementation, or proof file. The rule is sound under those
invariants, including for the bounded dyadic realization. The arithmetic
statement below is conditional on keeping its existing dyadic baseline
repair; an arbitrary unrounded rational history is not silently given the
same bit bound.

## 1. Source maximum and progress

After repair at `r_old<1/d_seed`, suppose

`0<=bar<=x*_(r_old)`,  `0<=s=b-Qbar<=2*alpha*r_old*w`.

Let `M=max_i s_i/w_i`. Then

`alpha*r_old <= M <=2*alpha*r_old`.

The upper bound is the repair interface. If `M<alpha*r_old`, the
nonnegative baseline would satisfy `Qbar>=b-alpha*r_old*w` and hence
dominate its least nonnegative supersolution, the optimizer. Baseline
safety would force equality. But the nontrivial optimizer has a positive
seed coordinate and source density exactly `alpha*r_old` there, a
contradiction. In fact `M=alpha*r_old` forces `bar=x*_(r_old)` as well.

The optional next parameter is

`r_next=max(rho, M/(4*alpha))`.

It preserves the diffuse stage interface by construction:
`0<=s<=4*alpha*r_next*w`. Optimum monotonicity preserves baseline safety.
Unless the target clamp is active, it obeys

`r_old/4 <=r_next<=r_old/2`.

If the target clamp is active, it may decrease by less than a factor two,
but that stage is terminal. It still satisfies `r_next>=r_old/4` and
`r_next<r_old` because the rule is called only when `rho<r_old`.

Initially `bar=0` at `r0=1/d_seed`. Although the old optimum then has empty
support, the maximum is known directly: `M=alpha/d_seed`. The first stage
is therefore `max(rho,r0/4)`, and its source satisfies the same factor-four
interface. No nonempty-support argument is being applied at that endpoint.
The global zero and alpha-one branches remain direct cases.

## 2. The stronger deficit bound needs no predecessor ratio

At any current valid stage `r`, put `e=x*_r-bar>=0` and assume
`s<=4*alpha*r*w`. If `e_i>0`, the optimum is positive at that coordinate,
so `(Qe)_i=s_i-alpha*r*w_i<=3*alpha*r*w_i`. If `e_i=0`, Stieltjes signs
give `(Qe)_i<=0`. Inverse positivity consequently gives

`Qe<=3*alpha*r*w`,  `e<=3*r*w`.

The error is supported inside `S_r=supp(x*_r)`, and the KKT mass identity
gives `r*vol(S_r)<=eta_*(r)`. Therefore

`eta_bar-eta_*(r)=w^T e<=3*r*vol(S_r)<=3*eta_*(r)`.

Thus the proposed factor five is valid, and the sharper statement is
`eta_bar<=4*eta_*(r)`. Concavity of `eta_*` and `eta_*(0)=0` give, at
every adaptive stage with `r>=rho`,

`eta_bar/r <=4*eta_*(rho)/rho`.

This uses only the current diffuse-source contract and baseline safety.
It includes the initial zero baseline and does not need a factor-two
predecessor. The separately proved final repaired-deficit approximation
within `1+alpha` is unchanged.

## 3. Complete local accounting

The maximum must be recomputed from the **actual repaired baseline**. The
preceding corrector's fixed source corresponds to its old baseline, and
the rounded primal neighbor response is approximate; neither can simply
be reused as this exact new source.

The source is supported on the seed, the repaired support, and its immediate
boundary. One exact baseline-neighbor accumulation and a maximum pass cost
`O((1+vol(supp bar))*log(N+2))` local word operations. A helper supplied
fresh or partial graph caches may need first reads of retained rows; all
such reads are charged to the repaired support volume. In the actual
cached wrapper, the certified candidate and PG point are each within
`delta/2` of the optimum, so truncation cannot retain a coordinate absent
from the candidate. Its repaired rows are therefore already cached, but
their repeated reads are still paid. There is no recursive boundary-row
scan. If the next
corrector rebuilds the source or rereads cached rows, those are additional
paid operations; neither duplication nor probe setup is free.

At the old regularization, the repaired support has volume at most
`1/r_old`, and at most `eta_*(r_old)/r_old` in the stronger estimate. Thus
the probe's added work fits the old or next stage ledger, including its
materializations, degree replies, point records, and discarded temporaries.
The initial empty-baseline probe needs only the known seed degree and
constant scalar work. A final unnecessary diagnostic probe, if performed,
must likewise be charged rather than omitted from the ledger.

Before the final clamped stage, inverse parameters grow by at least two.
Consequently there are `O(1+log(1/rho))` stages and the same bound
`sum_j 1/r_j<3/rho` holds. Clamping cannot introduce an additional
non-geometric tail because it immediately terminates continuation.
The source, binomial, or early-stop schedule still needs at most `T*L`
iterations at each stage. Its candidate accuracy and final repair proof
depend on the current diffuse source, not a predecessor-ratio assumption.

If a stage takes zero accelerated steps, its initialization, source probe,
source-energy statistics, candidate, and exact terminal repair still cost
the existing `(K+1)/r` charge. Progress of the next regularization follows
from the post-repair source bound, independently of how many accelerated
steps were used. The last clamped stage stops without requesting another
parameter. Hence neither zero steps nor an unchanged numerical baseline
is treated as permission for an uncharged repeated stage.

The unweighted `O(L^3/(rho*sqrt(alpha)))` word and
`O(L/(rho*sqrt(alpha)))` adjacency estimates are preserved. With the
direct deficit comparison, the conservative stronger bounds remain
`O(L^4*eta_*(rho)/(rho*sqrt(alpha)))` word work and the corresponding
`L^2` adjacency estimate. Probe work is absorbed by these bounds.

## 4. Exact-word and bounded-bit realizations

In the exact-real word model, source formation, maximum comparisons, and
division by `4*alpha` are allowed charged scalar operations. No root,
logarithm, randomization, or unknown activation margin is used.

For the bounded implementation, write `alpha=A/D` and the repaired
baseline densities as `B_i/H`, with the common dyadic `H`. If
`J_i=sum_(j~i) B_j`, its source density is

`s_i/w_i=N_i/(2*D*H*d_i)`,
`N_i=2*A*H*1_(i=seed)-(D+A)*d_i*B_i+(D-A)*J_i`.

Find the largest `N_i/d_i` by integer cross multiplication, retaining one
maximizing index. If it is `i0`, the proposed unclamped parameter is

`M/(4*alpha)=N_(i0)/(8*A*H*d_(i0))`.

In particular the original denominator `D` cancels. This expression
contains the current dyadic grid and one degree, not a product or least
common multiple of degree denominators accumulated over past stages.
The source numerators are nonnegative and sum to
`2*A*H*(1-mass(bar))<=2*A*H`; their intermediate products also have the
prior bounded parameter/degree/grid bit envelope. Maxima, final reduction,
and comparison with the original target are exact bounded scalar operations.

All current parameters remain at least the requested rho. Ordinary stage
tolerances are still `alpha^3*r^2/32`, and an epsilon-forced final shift
retains the same lower tolerance bound as before. They decrease along the
new continuation, so the minimal next dyadic grid represents the preceding
baseline automatically and has the same logarithmic `H` bound. The adaptive
parameter's own encoding is `O(b_parameter+b_graph+L)` bits by the explicit
formula above, without history growth. Thus all prior scalar bounds remain
`B=O(b_parameter+b_graph+L)`, and multiplying the word estimate by the same
conservative `B^3` gives the bit bound. This does not make the original
unrounded exact-real scalar trajectory a bounded-bit algorithm.

## 5. Transcription check

The new `app:diffuse-deficit` paragraph in
`practical_refinements_appendix.tex` correctly transcribes the global
`Qe<=3*alpha*r*w` proof and the factor-four conclusion. The replacement
reference in `practical_schedules_appendix.tex` correctly uses that
current-stage comparison and concavity. It changes neither the algorithm
nor its constants and is valid for both the previous fixed schedule and
this optional adaptive one. No correction is required.
