# Research Notes

## Hybrid Local Solver

Working hypotheses, proof ideas, and experimental observations should be recorded here.

Important topics:

- Catalyst acceleration;
- AESP;
- LocSOR;
- hybrid switching rules;
- complexity bounds.

## 2026-08-21: Round 013 reaches one local checkpoint and quarantines two tempting shortcuts

Two independently reviewed exact-real results sharpen the response and hybrid
directions. A third attempted path lower bound was withdrawn after independent
audits. None of these statements is a graph-uniform accelerated solver theorem.

First, fix the notched-double-sun face containing all `n` cycle/chord anchors
and all source petals, together with its rank-`n` anchor--report cut and shifted
ladder. For fixed `n` and sufficiently near-one `alpha`, let
`vartheta=(1-alpha)/2`. A unit first-rung fragment has matching response
`Theta(vartheta^2)` and off-matching response `O_n(vartheta^3)`. At gate
`g=vartheta^(5/2)` and band `g/2`, the exact fixed-face trace emits one new
delta label per event, yet every response increment is dense. Consequently the
named separately addressed exact-vector representation `EagerExactSlack`
performs `Theta(p n^2)` response/control/materialization work for
`Theta(r n)` delta/certificate output, with `p=r` for nonnegative columns and
`p=2r` for signed certification. Its full ledger is
`eq:notched-sun-eager-eleven-vector`:

```text
(Theta(n), 2, n, Theta(n+J),
 Theta(C_frag^Sigma+p n^2+pJ), 0, Theta(p n^2),
 Theta(pn+n+J), O(n+p), Theta(p n^2), Theta(rn)).
```

This is a fixed-face debt/query representation STOP only. The trace is not an
RPPR load or admission chronology, and the proposition does not constrain
implicit cyclic transfer, packed coded queries, scale-truncated state,
on-demand validation, or a general output-sensitive partial reporter.

Second, on the fixed `m>=2`, branch-seeded caterpillar with `alpha<1/2` and
`rho<rho_can`, the response-native `FirstLayer-BC_1` policy supplies an actual
local checkpoint at `k=1`. It scans exactly
`Uhat_1={b_1,b_2,a_1,r_1}`, commits the canonical first batch
`{b_2,a_1,r_1}`, settles the restricted point exactly, and retains the native
response state. Admitted support, numerical support, and scanned rows are all
`Uhat_1`; only the next layer's labels are known without row exposure or
admission. The prefix ledger is

```text
(9, 2, 1, 0, O(1), 0, O(1), O(1), O(1), Theta(1), Theta(1)),
```

and `eq:branch-caterpillar-first-layer-post-eleven-vector` charges the
remaining `J_+=m-1` batches and terminal return as

```text
(vol(S*\Uhat_1), J_+, J_++1, 0, O(C(S*)), 0,
 O(C(S*)+J_+ log(2+m)), Theta(C(S*)), O(C(S*)), Theta(|S*|),
 |S*\Uhat_1|+|S*|+Theta(J_++1)).
```

Extending the retained response in place gives exact total
`O(C(S*) log(2+C(S*)))`, with no hidden `log(1/(1-2 alpha))`. This is an
exact-real, canonical delta-interface, response-native RPPR comparator, not a
useful accelerated burn-in.

The companion signed-gate proposition identifies the missing accelerated
interface. At checkpoint `k`, a boundary demand changes exactly by
`beta_(k,v)(z_parent-x_parent)`, so the sharp symmetric radius is
`mu_k=min_v g_(k,v)/beta_(k,v)`. Strong convexity makes
`Delta<alpha mu_k^2/2` sufficient. The imported relative-gap route has
zero-stage success when `Delta_(k,0)=0`; for positive initial gap it provides
only

```text
T > (2/sqrt(alpha/(1-alpha)))
    log_+(4 Delta_(k,0)/(alpha mu_k^2)),
```

and each relative-oracle stage still contains the explicit
`log(1/(1-2 alpha))` factor. The previous constant half-gap does not establish
the required comparison. This is a sharp norm-ball/gap-interface barrier, not
a lower bound against exact settlement or a new one-sided local certificate.

Finally, the proposed constant-ratio endpoint-path terminal logarithmic lower
theorem was removed. Conditional on inactive projection, its full-face
recurrence has the derived damped-cosine roots, but those roots do not supply
the actual entry coefficients or an anti-cancellation bound for the moving
residual range. The finite exact runs remain direction-local scaffolding only.
There is no terminal logarithmic block, asymptotic lower eleven-vector, or
refutation of `K_face=O(q^-1)`. The Round-012 moving-maximum theorem remains
the authoritative one-log upper bound; whether that logarithm can be removed
or is necessary remains open.

## 2026-08-21: Round 012 charges flushing, caps one Phase I, and bounds the moving maximum

Three independently reviewed exact-real results repair the provisional
response summary, supply one fully paid caterpillar prefix witness, and give
the first uniform constant-ratio path chronology upper bound. None is a
graph-uniform solver theorem.

First, aggregate shifted debt is closed only on one frozen `(A,F)` partition,
exposed cut, and ladder. The scalar recurrence costs
`O_tilde(cvol(T)/sqrt(alpha)+C_frag)`, where every fragment-coordinate event is
charged. For `r` nonnegative columns the actual product count is the sum of
the `r` runs; signed columns use `p=2r` nonnegative streams without
pre-certificate cancellation. The energy certificate gives simultaneous
mathematical exterior intervals, not materialized replies. The named
non-output-sensitive `AllBoundaryFlush` pays cut scans, interval computation,
classification, validation, materialization, memory, rounds, and every
emission in a complete eleven-vector. With fixed column count, geometrically
growing fixed-decision faces retain the product scale only with those charges
and `C_frag` included. On ambient-degree endpoint paths, a family-dependent
`rho_n` forces canonical singleton batches while charged-volume ratios tend to
one. The linear exact-real comparator has `R_int=n`; this refutes geometric
sleep only as a schedule, not by a path work or round lower bound.

Second, “any finite valid burn-in” cannot bound caterpillar Phase I: an
arbitrary number `N` of valid exact-inner Catalyst stages may preserve the
pre-gate checkpoint `Uhat_0={b_1}` while adding `Omega(N)` control work. The
named `Full-BC-AESP_0` policy gives one capped comparator on the promised
fixed-`m`, branch-seeded family for `alpha<1/2` and `rho<rho_can`. It pays full
exposure, certifies `U=V=S*`, runs
`T_*=ceil(2 log(4)/sqrt(alpha/(1-alpha)))` AESP-CD stages, and hands off at
`k=0`. Its authoritative prefix bound is `O(H_*)`, and the separately charged
response gives exact output in `O(H_*+C_* log(2+C_*))`. The soft product
notation hides `log(1/(1-2 alpha))` and is not uniform near `alpha=1/2`. This
is a full-realized-support fixed-family witness, not adaptive locality, a
general prefix theorem, graph-uniform work, finite precision, or PPR accuracy.

Third, for the exact-real zero-start, internally gated transported-center
endpoint path at `rho=tau=q/5`, set
`K_q=ceil(log(50(1+q^2)^2 q^(-10))/(-log(1-q)))`. Every visited face admits
or certifies within `K_q` consecutive steps, independently of where the global
correction maximizer moves. Therefore
`T<=(J+1)K_q=O(q^(-2) log(1/q))` and
`mathfrak V_T=O(q^(-3) log(1/q))`; the literal implementation charges all
eleven coordinates as
`(Theta(q^-1),Theta(q^-1),1,0,O(q^-3 log(1/q)),O(q^-3 log(1/q)),`
`O(q^-3 log(1/q)),Theta(q^-1),O(q^-1),O(q^-3 log(1/q)),Theta(q^-1))`.
These are one-log upper bounds, not matching `Theta` laws, lower bounds,
logarithm removal, a product separation, a zero-padded or nonpath theorem, or
a finite-precision result.

## 2026-08-21: Round 011 retires one cyclic family and closes a growing-core handoff

Three independently reviewed exact results close the relay-seed audit, add a
paid branch-caterpillar switch, and establish the rigorous part of the
constant-ratio path chronology. None is a graph-uniform product theorem.

First, the relay seed supplies no escape on the even double-cycle feed. For
every even `n>=4`, site `j`, `0<alpha<1`, and `rho>0`, let
`t=(1+alpha)/(1-alpha)`,
`rho_W=1/(2(2t+1))`, and `rho_B=1/(2(4t+1))`. The exact canonical
all-violations gate has the exhaustive first-step split: no initialized face
for `rho>=1/2`; a terminal relay singleton for `rho_W<=rho<1/2`; first batch
`{w_j}` for `rho_B<=rho<rho_W`; and first batch `{w_j,b_j}` for
`0<rho<rho_B`, with equality inactive under the strict gate. Thus every
relay-seeded trace that propagates reports in its first batch, before any
petal. Together with the backbone and anchor seed stops, this retires the
double-cycle family only for the prescribed canonical long report-free
later-petal witness. It does not retire all cyclic witnesses, cover arbitrary
positive-subset policies or post-report behavior, or prove a response,
reporter/work, stability, or finite-precision lower bound. The next candidate
needs a different coupling or bounded-degree settlement gadget.

Second, the strict-range canonical branch caterpillar now has a paid hybrid
handoff. Fix `m>=2`, branch seed `s=e_(b_1)`, `0<alpha<1`, and
`0<rho<rho_can(m,alpha)<=rho_cat(m,alpha)<=1/3`. Any fully charged Phase-I
prefix ending after `k` actual canonical layers may discard all signed
numerical, momentum, queue, and uncommitted state. One direct support-only
pass builds the current arm/leaf absorptions, tridiagonal branch cells, and
balanced transfer tree, then continues with `CaterpillarCanonicalLayerDelta`
without replaying or querying any prior face. The exact-real total is

```text
B_J^full + O(C(S*) log(2+C(S*))).
```

The prefix and suffix ledgers charge all eleven resource coordinates,
including prior and remaining delta/certificate emissions, recovery,
validation, terminal materialization, exact output, and peak memory. Product
work follows only if an independent theorem bounds the fully charged prefix
`B_J^full`; the result does not transport estimate-sequence energy or cover
the remaining parameter range, other seeds or policies, repeated full lists,
finite precision, PPR conversion, or arbitrary graphs.

Third, the constant-ratio endpoint path yields exact floors rather than the
numerically suggested separation. For `0<q<=1/4`, `alpha=q^2`,
`rho=tau=q/5`, and
`L_q=floor(log(5/3)/(-log((1-q)/(1+q))))`, the zero-start transported-center
execution on a long enough ambient-degree path satisfies

```text
J, nu_fin = Theta(1/q),   T >= J,
mathfrak V_T = Omega(q^(-2)) = Omega(nu_fin/q).
```

This is the realized product scale. It does not prove
`T=Theta(q^(-2))`, `mathfrak V_T=Theta(q^(-3))`, or any product separation.
An exact `q=1/5` trace also gives a decisive gate-locality STOP: a
seed-attained global safe-envelope correction suppresses a raw stage-6
frontier violation, and after the next admission its maximizer moves to old
interior vertex `v_2` by stage 9. Neither the raw frontier coordinate nor a
correction pinned to one old vertex determines the chronology. The next exact
target at Round 011 was the time-varying global correction over all old
coordinates. Round 012 above now controls it up to one logarithm; matching
lower powers or logarithm removal remain open.

## 2026-08-21: Round 010 closes the anchor rescue and isolates an accuracy-log sweep

Three independently reviewed exact results advance the cyclic-legality,
reporting, and expanding-face ledgers without promoting a graph-uniform
solver theorem.

First, the apparent anchor-seed escape on the double-cycle feed is not a long
canonical witness. For every even `n>=6`, `0<alpha<1`, and
`0<rho<(1-alpha)/8`, the exact-real canonical all-violations continuation has
at most the three report-free petals at the seed and its two neighboring
sites. If the first `j+/-2` petal batch occurs, it co-admits `w_j` unless a
report entered earlier. This retires the anchor-seeded rescue only. At Round
010 the relay seed remained unaudited; Round 011 above now closes that orbit
and retires the graph family only for the prescribed witness. The anchor
theorem itself makes no claim for arbitrary positive-subset policies,
post-report behavior, finite-band reporting, response directions,
reporter/work lower bounds, stability, or finite precision.

Second, the actual canonical policy is positive on a smaller fixed-family
caterpillar range. Fix `m`, branch seed `s=e_(b_1)`, `0<alpha<1`, and
`0<rho<rho_can(m,alpha)<=rho_cat(m,alpha)<=1/3`. The canonical trace has
exactly `m` strict three-label distance-layer batches.
`CaterpillarCanonicalLayerDelta` changes one branch load/diagonal cell for an
early side leaf; a long-arm append adds one arm-transfer cell and updates its
induced `b_1` absorption cell; and a backbone append adds one tridiagonal cell.
Balanced transfers answer the parent-coordinate queries. Its exhaustive
resource vector is

```text
(Theta(m), Theta(m), m+1, 0, Theta(m), 0,
 O(m log(2+m)), Theta(m), O(m), Theta(m), Theta(m)).
```

Every exact demand test, delta/certificate exchange, retained and scratch
cell, terminal recovery, validation, candidate write, and exact output is
charged. Total work is `O(m log(2+m))` with `O(m)` state. The result is
fixed-`m`, branch-seeded, family-dependent, exact-real, canonical, and
delta-only. It excludes `rho_can<=rho<rho_cat`, other seeds or policies,
pre-backbone interleavings, repeated full lists, `kappa=1`, finite precision,
PPR conversion, and graph-uniform product work. Those are the next reporter
extensions; no positive `rho` range uniform in `m` is claimed.

Third, a zero-start endpoint path forces an exact accuracy-driven swept-prefix
separation for the literal implementation. Use the endpoint seed and ambient
path degrees on a finite path with exactly `N=L+1` edges. Put `q=1/n` for
integer `n>=2`, `L=n^2`, and
`rho=tau=(q/3)((1-q)/(1+q))^L`, with `eps_ppr=2rho`. The terminal certificate
forces the first `L+1` path vertices into the support; only one outside
successor can enter per fixed-face step. Hence `L<=J<=L+1`, `T>=J`,
`nu_fin=Theta(q^(-2))`, and

```text
mathfrak V_T >= sum_(j=1)^L (1+2(j-1)) = L^2 = q^(-4).
```

The named literal full-prefix implementation therefore exceeds its realized
`nu_fin/q=Theta(q^(-3))` scale by a certified factor `1/q`. That certified
factor is only `Theta(log(q/rho))`; no matching upper bound on actual swept
volume is proved. This refutes a log-free accounting statement only. It does
not refute soft order or an implicit implementation, extend beyond endpoint
paths, or give a finite-precision result. Round 011 above proves only
product-scale constant-ratio floors and a moving-global-correction STOP; the
observed stage and swept exponents remain open.

## 2026-08-21: Round 009 stops the double-cycle trace and sharpens two implicit ledgers

Three independently reviewed exact results refine the current chronology,
reporting, and expanding-face targets.

First, the independent double-cycle feed still fails for the intended
backbone-`B`-seeded canonical all-violations chronology. Before the first
report or petal, every active anchor has its relay. If the next batch remains
report-free, report quietness caps every active anchor below the petal
threshold; when an inactive anchor is admitted, its relay is already active or
is co-admitted in the same batch. Consequently every report-free canonical
prefix is petal-free and the first petal batch contains a report. This rules
out only the prescribed backbone-seeded report-free petal/attachment trace and
makes no claim after `W` enters. The seed qualifier cannot be removed: with an
anchor seed and `0<rho<(1-alpha)/8`, the first petal batch is exactly
report-free. Arbitrary positive-subset policies, reporter/work lower bounds,
response-direction conclusions, finite precision, and stability remain open.
The next attempt first follows that anchor-seeded counterrange through its full
canonical chronology. If it does not yield the required epoch, the next
feed/gadget must escape the anchor--relay maximum principle or the canonical
cyclic-witness route should be deprioritized; chronology and changing response
directions still precede reporter analysis.

Second, the implicit route succeeds for one explicit growing-core policy and
delta interface. Fix `m`, branch seed `s=e_(b_1)`, `0<alpha<1`, and
`0<rho<rho_cat(m,alpha)<=1/3`. After the exact-KKT positive-subset policy
commits backbone singletons `b_2,...,b_m`, it may commit arbitrary nonempty
subsets of currently known strict-positive pendant tips.
`CaterpillarKineticDelta` uses the separable last Green column and a strict
crossing-key heap to retain the exact all-positive live-tip set; equality stays
in the heap and every label is emitted only when it first becomes strictly
positive. Its full vector is

```text
(Theta(m), Theta(m), J+1, 0, O(m log(2+m)), 0,
 O(m log(2+m)), Theta(m), O(m), Theta(m), Theta(m)),
```

for `2m-1<=J<=3m`. This charges every transfer update/query, heap operation,
membership and proposed-batch check, retained/scratch cell, delta/certificate
label, terminal recovery, validation, materialization, and exact output. The
result is fixed-`m`, exact-real, family-dependent in `rho`, backbone-first, and
delta-only. It is not canonical all-violations, arbitrary pre-backbone
interleaving, repeated full-list reporting, `kappa=1`, finite precision, or a
graph-uniform accelerated theorem. The next reporter target is precisely one
of those broader policy/interfaces, with full-list output charged separately.

Third, weighted Schur shocks admit an exact analytical decomposition but not
the hoped-for unweighted shortcut. With `q=sqrt(alpha)`, `theta=1-q`, and
`H_t` the remaining restricted-face optimum gain,

```text
sum_t theta^(T-1-t) Delta_t
  = theta^(T-1) H_0
    + q sum_(t=1)^(T-1) theta^(T-1-t) H_t.
```

The right object is therefore discounted remaining-gain occupancy. A terminal
gate-compatible endpoint edge has `T=2`, one admission, final volume two,
swept volume three, and weighted-to-`q`-unweighted ratio `(1-q)/q`. This
refutes only a universal `C q sum_t Delta_t` packing. It does not lower-bound
stage count or swept work and leaves terminal-floor terms, occupancy-based
potentials, other potentials, and zero-initialized growing-path executions
open. The endpoint-path continuation target is now to control or refute the
occupancy term together with the terminal floor, `T`, and every charged
old-prefix sweep.

## 2026-08-21: Round 008 retires a fourth cyclic trace and separates transport from reporting

Three independently reviewed exact results sharpen the chronology,
representation, and expanding-face acceleration frontiers.

First, raising the exterior petals to degree three reverses the local
petal/relay threshold but still does not produce the required canonical
relay-first epoch. On the even petal-cycle relay graph, for every
`0<alpha<1`, `rho>0`, and seed orbit, a `W`-free canonical face containing
all relays whose next all-violations batch is also `W`-free has at most one
inactive petal. If a report enters with or before the last relay, or in the
first post-last-relay batch, the report-free epoch has already failed. Thus
the degree-three petal-cycle candidate is retired. This is an exact KKT
chronology stop for the canonical all-violations policy only: arbitrary
positive-subset policies remain outside it, and it is not a reporter,
response-rank, work, scan, output, stability, or finite-precision lower bound.
The next legal witness must feed relays from an independent active backbone or
use a different bounded-degree gadget, with all seed cases and genuinely
changing response directions proved before reporter analysis.

Second, a growing branch core does force quadratic maintenance in one named
eager state, but not in implicit response generally. Fix `m`, branch seed
`s=e_(b_1)`, `0<alpha<1`, and the family-dependent exact range
`0<rho<rho_cat(m,alpha)<=1/3`. One legal KKT positive-subset singleton order
first admits the branch backbone, then a length-`m` endpoint arm, and finally
the deferred leaves. Each arm append strictly changes all `m+1` deferred
positive leaf demands. The literal `EagerTipKey` representation, which keeps
one separately addressed exact cell per live tip and refreshes every changed
cell without lazy indirection, therefore performs at least `m(m+1)` old-key
writes. The chronology is not the canonical all-violations batch, and no
positive range for `rho` uniform in `m` is claimed. Lazy affine keys,
sign-persistence flags, kinetic/group structures, on-demand queries, arbitrary
RPPR algorithms, and finite precision are not lower-bounded. Indeed, a
balanced affine-transfer tree supports one named append/update or tip query in
`O(log(2+m))` exact operations with `O(m)` retained cells. The open target is
a charge-comparable dynamic all-positive reporter for every legal order, with
every internal query and external emission charged.

Third, exact center transport closes the one-expansion analytical identity on
endpoint paths without closing total work. If `d` is the restricted-optimum
shift for a safe expansion `U` to `U+`, then

```text
E_(U+)(x, v+d) = E_U(x, v) + Delta_B.
```

The nonnegative Schur gains telescope over nested faces. An append-only exact
`LDL^T` response stores centered momentum `v-x_U*`, appends zero state at an
admission, and thereby represents the dense optimum shift without rewriting
the old prefix. Factor, Schur, gate, admission, and state-append work is
charged to newly admitted volume. The full eleven-coordinate ledger still
charges every old-face recurrence read and response application through the
swept volume, as well as validation, materialization, memory, and terminal
sparse output. The stated path execution is internally gated and uses one
terminal external certificate/output stage; intermediate external emissions
are not covered. This modifies the center recurrence rather than proving the
literal zero-padded conjecture. It supplies no bound on the step count, late
weighted shocks, or total swept volume, and does not cover branching/cyclic
responses, floating point, or bit complexity. PPR conversion still requires
the terminal one-sided certificate with `rho=tau=eps_ppr/2`. The next proof
must pack the signed zero-padding defect or control those late shocks and
old-prefix sweeps, then test whether centered-state transport survives the
first branching core.

## 2026-08-21: Round 007 closes the double-Y handoff and rejects two stronger witnesses

Three independently reviewed exact results sharpen the cyclic-legality,
hybrid-composition, and recurrence-model frontiers.

First, inserting a relay does not create the desired preloaded cyclic epoch.
On the two-edge active-relay matched sun, at every `W`-free canonical face, a
canonical all-violations batch that admits a nonseed relay `r_i` must find its
degree-one petal `f_i` already active or admit it in the same batch. The proof
exhausts the seed orbits and holds for every `0<alpha<1` and `rho>0`; the raw
anchor--relay and relay--report cuts are nevertheless full rank. Hence a
common face containing all relays already contains at least all but one petal
and cannot precede a linear petal-only epoch. This is a KKT chronology stop,
not a reporter, response-rank, scan, output, or finite-precision lower bound.
Paired petal--relay batches remain possible, and arbitrary positive-subset
policies are outside the canonical-all-violations theorem. This motivated the
degree-three petal-cycle and independent-backbone tests. Round 008 above
retires the petal-cycle option; the independent-backbone or different-gadget
route still needs its all-seed chronology proved before reporter analysis.

Second, the branch-seeded double-Y response now has a paid common-state hybrid
handoff. For `s=e_o`, `0<alpha<1`, and `0<rho<1/3`, every finite fully charged
gate-compatible Phase-I prefix discards its signed numerical state and, in one
common outward pass, reconstructs the four actual pendant prefixes together
with the scalar core before `h` enters or the SPD rank-two core afterward.
There is no private order replay. The prefix and post-handoff statements each
give the full eleven-coordinate vector. In particular, the post phase charges
adjacency, conversion/control, affine and core response work, recovery,
validation, persistent and scratch cells, terminal materialization, exact
output, and one constant-size certificate emission per declared external
stage. The total is

```text
B_J^full + O(C(S*(rho))).
```

Product scale follows only from an independent bound on the fully charged
prefix `B_J^full`; no signed estimate-sequence energy is transported. Other
seeds, growing branch cores, arbitrary trees or cycles, finite precision, and
graph-uniform continuation remain open.

Third, full-support accuracy still does not rescue the broad endpoint-path
supported-prefix lower-bound candidate. At `n>=8`, `alpha=n^(-2)`, and
`eps_ppr=1/(10n)`, the actual residual certificate implies normalized solution
error at most `1/(10n)`, while the exact path solution exceeds that value at
every coordinate. Every valid sparse list therefore has all `n` coordinates
and `nu_fin=2(n-1)`. Yet exact sparse row actions and scalar cancellations
generate singleton coordinate directions `e_1,...,e_n`; a fixed degree-six
spatial profile is then synthesized, verified, and emitted in `Theta(n)`
charged work with no intermediate full current vector. A same-task append-only
`LDL^T` response also costs `Theta(n)`, while
`nu_fin/sqrt(alpha)=Theta(n^2)`. This refutes the product lower bound only for
the broad exact-cell `CertPrefixPoly` task. Ordinary CG's literal trajectory
and the exact full-vector `DiagSpecPoly(r)` theorem remain unchanged. A next
candidate must defeat both constant-prefix residual-slack spreading and
singleton-basis delayed synthesis, or justify a narrower trajectory or
materialization invariant.

## 2026-08-21: Round 006 closes a fixed rank-two response and rejects two candidate witnesses

Three independently reviewed exact results sharpen the legality, composition,
and lower-bound queues.

First, breaking source/report degree symmetry does not by itself create a
legal long cyclic admission trace. On the even matched-report sun, every
anchor has degree four, every source petal degree one, and every matched report
vertex degree two, so the raw anchor--report block has full rank `n`. Yet on a
canonical face and next batch that both avoid the report set `W`, exact report
quietness, with `vartheta=(1-alpha)/2`, gives

```text
x_(u_i) <= 4 * alpha * rho / vartheta,
```

whereas a positive source-petal demand gives

```text
x_(u_i) > 2 * alpha * rho / vartheta.
```

For a nonseed anchor, its active KKT equation and the same upper bounds on its
two cycle neighbors make this interval impossible. Exhausting anchor, petal,
report, and nonpositive seed cases shows that every `W`-free canonical prefix
contains at most one `F` petal, for every `0<alpha<1` and `rho>0`. This is a
KKT-legality obstruction despite full raw cut rank. It is not a reporter,
response-rank, scan, output, or finite-precision lower bound. The then-next
candidate used an active relay with an unadmitted report endpoint; Round 007
above records why that repair also fails its canonical chronology test.

Second, common irreversible response state survives the first two-branch
core. On the double-Y seeded at branch vertex `o`, `s=e_o`, exact affine
records for the four actual pendant prefixes couple through one scalar before
the adjacent branch `h` is admitted and through a fixed-size SPD `2 x 2` Schur
core afterward. Every legal certified batch order updates only this common
state; there is no private replay or eager global rekey. For `0<alpha<1` and
`0<rho<1/3`, the activation-token countdown has `kappa=1` and the fully charged
exact-real ledger is

```text
O(C(S*(rho))) = O(1 / rho),
```

including adjacency, gate/control, response construction, updates and
queries, state, recovery, validation, and exact output. With
`zeta=(1-alpha)/(1+alpha)` and
`rho_link(alpha):=zeta/[3(3+zeta)]`, the condition
`rho<rho_link(alpha)` forces every legal order to admit `h` and enter the
rank-two phase. This theorem fixes only one two-vertex branch core. The
response direction next tests growing branch-core backbones and cycles. At
Round 006 the hybrid composition was still open; Round 007 above closes that
fixed-core handoff while leaving the Phase-I budget independent.

Third, the actual sparse residual certificate defeats the first named
supported-prefix product candidate. On the endpoint path with `n>=8`,
`alpha=n^(-2)`, and `eps_ppr=1/10`, a five-coordinate vector supported inside
the first six exposed vertices lies in `K_5(Q,b)` and passes the strict
degree-normalized residual certificate. A degree-four `CertPrefixPoly`
execution uses four constant-prefix row actions and `O(1)` exact cells; a
fully charged five-row append-only `LDL^T` response emits the identical sparse
output in `O(1)` exact cells. The realized final degree volume is `11`, so the
named class/task does not have a product lower bound. This does not alter the
ordinary-CG theorem that its Galerkin trajectory first certifies at step `n`,
and it does not weaken the distinct exact full-vector `DiagSpecPoly(r)`
obstruction. The next lower-bound family must prevent constant-prefix
residual-slack spreading or explicitly justify a stronger accuracy or
trajectory requirement.

## 2026-08-21: Round 005 validates one handoff and rejects two unsafe generalizations

Three independently reviewed results sharpen the current trajectory,
recurrence, and composition boundaries.

First, the prescribed notched-double-sun `F`-only epoch is not a canonical
single-seed RPPR trace. At any positive face containing the anchor and no
report leaf, every unseeded matched pair `f_i,w_i` has exact normalized demand

```text
-alpha * rho + (1-alpha) * x_(u_i) / (2 * sqrt(d_(u_i))).
```

The canonical all-violations gate therefore co-admits the two labels. One seed
can make at most one pair exceptional, so no parameter choice realizes
linearly many distinct `F` admissions while all report leaves remain outside.
The finite-band corollary is narrower still: for one simultaneous uniform
point-estimate call at one common face, both labels lie on the same side of
the robust band. It says nothing about separately scheduled interval
refinement. The existing structural rank and explicit dense-table audits are
still valid representation audits, but neither is a reporter lower bound for
a legal RPPR trajectory. The next cyclic witness must break the pair symmetry
and prove its single-seed KKT admission chronology before any reporter claim.

Second, literal supported exact CG has an exact product-scale calibration. On
the endpoint-seeded unweighted path, use ambient degrees,
`alpha_n=n^(-2)`, `eps_ppr=1/10`, and start ordinary CG from zero. Before
termination, the residual is a positive singleton at the next frontier while
the search direction is positive on the full visited prefix. The actual
degree-normalized residual certificate first holds at `K=n`. Consequently,

```text
sum_(k=0)^(n-1) vol(supp(p_k)) = n^2 - 1,
total literal work including verification = Theta(n^2)
                                         = Theta(nu_n / sqrt(alpha_n)).
```

The complete eleven-coordinate ledger charges the chosen sequential
supported-row rereads, recurrence and control, explicit materialization,
memory, validation, and output. This is an algorithm- and
implementation-specific exact-algebraic result. It is not a lower bound for
arbitrary supported polynomials or recurrences, implicit or rational response,
prefetching adaptivity, or finite precision. Those broader representations
remain the next recurrence/model tests.

Third, the three-arm structural response now composes with a fully charged
Phase-I prefix without replay. On the center-seeded unweighted three-arm
spider with `0<alpha<1` and `0<rho<1/3`, any finite gate-compatible prefix records the actual
irreversible common arm prefixes and charges initialization, excess exposure,
old-row reads, recurrence and gate work, exact canonical settlement/response,
checkpoint materialization and recovery, and state. At the handoff it discards
all signed trial and momentum state, reconstructs the affine records in one
pass over the committed prefixes, and finishes with exact response, validation,
recovery, and output. Thus

```text
W_total <= B_J^full + O(C(S*(rho))).
```

The suffix is common-state and accepts every legal certified bulk order; it
does not privately replay a canonical history. The product scale is only the
conditional corollary obtained from an independent fully charged bound on
`B_J^full`. No numerical estimate-sequence energy survives, so the theorem
does not provide shock-free acceleration. It is exact-real, one-branch, and
RPPR-only; the note's particular composite Catalyst/AESP prefix is covered
only for `alpha<1/2`. The next tests are the smallest tree with two branching
vertices and a separate Phase-I budget theorem.

## 2026-08-21: Round 004 transports structure, but only on the first composable families

Three independently reviewed results identify the smallest settings where
the current composition interfaces succeed or fail.

First, exact RPPR activation tokens extend from an endpoint path to one true
branch. On a center-seeded unweighted three-arm spider with `0 < rho < 1/3`,
one affine transfer product per actual common arm prefix and two scalar root
aggregates represent every canonical checkpoint. Stieltjes violation
persistence serializes any legal certified boundary batch, so every policy
updates only the actual committed common prefixes without an arm-private
trajectory. Exposure, forward response, all three tip tests, state writes and
resident cells, terminal recovery, and exact output are separately charged. In exact
real-cell arithmetic the resulting activation-token countdown has
`kappa = 1` and standalone work

```text
O(C(S*)) = O(1 / rho).
```

This is not a graph-uniform accelerated solver and has no finite-precision or
bit-complexity consequence. The next falsifiable family is the smallest tree
with two branching vertices, where the number of transported response
directions can grow.

Second, a fixed-attachment cyclic reporter is now completely charged. Let a
simple cycle be the settled core, let supplied certified closed pendant trees
all attach at one core vertex `p`, and keep still-exterior coordinates fixed
at zero during absorption. Sherman--Morrison confines every core correction
to one Green column, so each boundary key is affine in one nondecreasing
scalar. `FACR(p)` sorts the two gate-crossing lists once and advances two
pointers. Its exact-cell ledger is

```text
work   = O(V_fin + |R| log(2 + |R|) + Z),
memory = O(V_fin),
```

including verification and scans for the supplied closure certificates,
forest elimination and recovery, Green-column construction/application,
queries, exact validation, state, and output. No current boundary-key array is
materialized or globally rekeyed. The result is absorption-only: online
closure discovery, varying attachment vertices, growing response rank, a
post-repair terminal queue, and finite precision remain open.

Third, zero-padding alone cannot transport an accelerated face energy. For
`0 < alpha < 1` and `rho=tau=r<(1-alpha)/(3+alpha)`, start the exact
safe-gated recurrence on one endpoint edge at a zero-momentum exact restricted
optimum. The gate safely admits the other endpoint, but the first
enlarged-face step retains the positive objective gap

```text
alpha * eta^2 * m^2 = (2 eta^2 / a) * Delta_B,
```

where `Delta_B` is the exact Schur expansion gain. Every fixed-face-exact old
energy is zero, so a shock-free pointwise contraction is impossible. This
does not refute the global zero-start rate, an inequality with an explicit
Schur or transported-state term, cumulative shock packing, or a
newly-admitted-volume work bound. The next proof must carry that term and
charge old-face recurrence, gate/admission work, persistent state,
validation, and output cumulatively.

## 2026-08-21: Round 003 closes three tempting implementations, not the parent targets

Three independently reviewed exact results narrow the live proof routes.

First, the safeguarded AESP-CD collateral charge cannot be packed by simply
normalizing the monotone Euclidean-error telescope. On an exact full-support
single-edge family with `alpha=q^2/(1+q^2)` and fixed `rho=9/20`, stage two is
a harmful full collateral correction with

```text
C_2^col = (44/9) q + o(q),
log(||e_1||_2^2 / ||e_2||_2^2) = (88/9) q^2 + o(q^2).
```

The same separation holds on the first two-stage prefix. Hence no
`o(1/q)` coefficient, including an `alpha`-uniform or polylogarithmic one,
charges the analytical collateral fraction to Euclidean log-progress. This
does not refute a cumulative bound for the actual log-inflation `I_T`, a
multistep collapse-history potential, or another one-sided surrogate. The
next AESP target is exactly one of those alternatives.

Second, on the prescribed notched-double-sun structural epoch, a literal
adaptive coded-bank implementation that rebuilds and stores a fresh explicit
dense harmonic table at every event writes at least

```text
n (L_n + 1) * sum_k c_k
```

table cells, leaving an unsuppressed anchor-size factor above charged volume
plus all candidate caps. This is an implementation audit, not an RPPR
trajectory or reporter lower bound. Fresh implicit multi-right-hand-side
solves, batched or compressed row access, predeclared charged block pools,
dynamic terminal sparsifiers, cyclic transfer state, and sparse recovery all
remain open. The next response target is an aggregate epoch charge for one of
those representations, including anchor solves, old-face reads, adaptive
random blocks, workspace, validation, and output.

Third, the fully exposed endpoint path survives the exact-system dimension
test at `alpha=n^(-2)` only under a named execution class. For every positive
diagonal `M`, the transformed load is cyclic for
`T=M^(-1/2) Q_n M^(-1/2)`. Exact full-vector `DiagSpecPoly(r)` therefore needs
polynomial degree at least `n-r-1`; the named spectral-atom charge gives
`r<=floor(sqrt(nu_n))`, and the defining full-vector application rule yields

```text
C_rec = Omega(n * nu_n) = Omega(nu_n / sqrt(alpha)).
```

This is exact algebraic-cell work for the named full-vector subclass only.
It does not cover supported growing-prefix Krylov, arbitrary nonlinear,
adaptive, rational, or implicit response, or finite precision. Polynomial
preconditioning is included only when every underlying `T` application is
counted. The next model target is a separately named supported-prefix or
response subclass; killed-Green influence packing remains an independent
information route.

## 2026-08-21: positive shifted resolvents turn whitening into exact debt

The frontier inverse square root has a monotone representation that connects
the spectral proof directly to delayed push. Starting from

```text
x^(-1/2) = (2/pi) * integral_0^infinity 1/(x+t^2) dt,
```

a geometric right-endpoint quadrature gives positive weights `omega_j` and
shifts `sigma_j` with

```text
(1-4*eta) * x^(-1/2)
    <= sum_j omega_j/(x+sigma_j)
    <= x^(-1/2)
```

uniformly on `[alpha,1]`. The key ledger is not merely the logarithmic rung
count: `sum_j omega_j/(alpha+sigma_j) <= 1/sqrt(alpha)`. A residual-coordinate
settlement argument strengthens this to an `O(1/sqrt(alpha))` total
Schur-coordinate work factor for nonnegative sources. Signed Gaussian sources
are handled by their positive and negative parts.

Every shifted frontier resolvent is exactly a sparse shifted face solve. If
`K_F` is the frontier Schur complement and `E_F` embeds the frontier, then

```text
(Q_TT + sigma_j E_F E_F^T)^(-1) E_F
    = U_F (K_F + sigma_j I)^(-1).
```

An unfinished sparse solve has a nonnegative residual debt `d_j`, and the
exact rational lift is the current sparse state plus
`sum_j M_j^(-1) d_j`. Settling the anchor part later changes the frontier debt
by exactly `-Q_FA Q_AA^(-1) d_A`, which is the shifted Schur residual and
remains nonnegative. Thus delayed anchor debt is not a heuristic: it is an
exact invariant for a positive inverse-square-root ladder.

This removes target harmonic-row construction as an algebraic necessity and
explains why the empirical delayed-rung idea can carry the accelerated
`1/sqrt(alpha)` scale. Literal nonnegative row-by-row settlement is not enough:
the first rung on one edge needs `Omega(1/alpha)` alternating exact pushes for
a fixed residual reduction.

The fixed-face escape is now proved in a frozen exact-real model. Keep one
partition `(A,F)`, its exposed cut, and the complete shifted ladder fixed while
additive nonnegative debt fragments arrive. Sum the fragments rung by rung,
run signed Chebyshev semi-iteration on each sparse shifted face matrix, and
allocate residual tolerances so that the sum of the `Q`-energy errors is at
most `delta`. Since `alpha I <= M_j <= (1+sigma_j) I` and
`sum_j sqrt(1+sigma_j) <= J+(1+eta)^2/eta^2`, the scalar sparse-recurrence
work is

```text
O_tilde_eta(cvol(T)/sqrt(alpha) + C_frag),
```

where `C_frag` charges every incoming fragment-coordinate read, write, and
aggregation event. For `r` nonnegative columns, the authoritative product
count is the sum of the `r` column runs. Signed columns are split into
`p=2r` nonnegative streams with no cancellation credit before certification.
The universal boundary-leverage bound converts each final energy certificate
into simultaneous mathematical one-sided exterior intervals; that quantifier
does not materialize any interval or implement `BoundaryBounds`.

The named `AllBoundaryFlush` supplies the stronger implementation only by
paying for it. It scans the exposed cut, contracts every requested output
column, computes and materializes both endpoints of every current boundary
interval, classifies and validates them against the gate/band, and emits every
interval plus one certificate record per output column. Its eleven-vector
also charges fragment and ladder control, Chebyshev recurrence work,
persistent debt, sequential workspace, full-face writes, adjacency and
interaction rounds, and output. It is non-output-sensitive and exact-real;
face or ladder mutation, refinement of ambiguous labels, finite precision,
bit complexity, and terminal PPR/RPPR output are separate.

With fixed column count, geometrically growing fixed-decision faces and one
fully charged all-boundary flush each retain the final-volume product bound,
including the summed fragment, cut, memory, materialization, round, and
emission coordinates. Pure geometric sleep is nevertheless false for the
literal exact gate. On every fixed sufficiently long ambient-degree endpoint
path, one may choose a family-dependent positive `rho_n` so canonical
all-violations batching admits exactly the next singleton; no positive lower
bound on `rho_n` uniform in path length is asserted. The charged append-only
exact-real comparator has a complete linear ledger with `R_int=n`. Thus the
result is a scheduling obstruction, not a path work or interaction-round lower
bound. The remaining operation is an output-sensitive partial flush on
high-cut-rank cores, unless a separately proved support-safe trace bypasses
the literal batches.

The coded-bank route has simultaneously removed two other apparent
multipliers. Exact validation plus a first-failure coupling reuses one target
hash/sign bank per doubling capacity throughout the adaptive epoch, so the
total target-row count is controlled by the largest packed query rather than
the sum over events. The same harmonic product has exact target and source
orientations. An online rent-or-buy rule uses at most twice the smaller of the
target-row count and cumulative source width in anchor right-hand sides. The
remaining charge is no longer measurement dimension, adaptive target
randomness, or the number of anchor solves; it is repeated source-side
anchor-cut scanning versus target-side stored-response reads and applications.

## 2026-08-20: low-cut-rank harmonic queries close, but not universally

The remaining scalar harmonic-query interface is exact in a useful structural
regime. For a fixed anchor `A`, factor the normalized cut
`Q_AU D_U^(-1/2) = B*C` with rank `s` and precompute
`Y = Q_AA^(-1) B`. Every target harmonic extension is then `Y*(C*a)`.
The normalized exterior response is a sparse direct vector minus `C^T` times
an `s`-vector. Its squared norm on every hierarchy node is therefore an exact
quadratic of an additive `s`-by-`s` Gram matrix, an additive `s`-vector, and an
additive scalar. These summaries are updated only on hierarchy paths touched
by the frontier. Source-only Gaussian probes, prepared by Chebyshev whitening,
then give the complete packed reporter. Thus bounded or polylogarithmic cut
rank closes the group-query side after explicitly charged anchor solves,
storage, and touched-incidence work.

This route is not graph-universal. On the comb tree formed by an active
`n`-vertex path with one exterior leaf per path vertex, the normalized cut is
a nonsingular diagonal matrix. Its harmonic bank is dense and rank `n`, and
the smallest energy-scaled singular value is at least
`(1-alpha)/(2*sqrt(3))`. Hence every rank-deficient bank has constant operator
error while the active charged volume is only `4*n-2`. This is a
representation lower bound only: path/tree message passing can still exploit
order. It rules out precomputing a universal low-rank harmonic bank and leaves
the high-cut-rank nonequitable core as the precise dynamic-sparsification or
sparse-recovery target.

## 2026-08-20: two telescopes give a square-root response scheduler

The source-aware Schur-diagonal-loss telescope and the orthogonal
correction-energy telescope combine by Cauchy--Schwarz. For any exterior label
`v` and any epoch `I`, the normalized response accumulated during that epoch
is at most

```text
sqrt((sum_{j in I} diagonal_loss_j(v) / d_v)
     * (sum_{j in I} correction_energy_j)).
```

Across disjoint wake-up epochs, the sum of their certified margins is at most
the geometric mean of the label's total diagonal loss and the trace's total
correction energy. A unit-seed RPPR trace from the zero face has total
correction energy at most `alpha`, while a still-exterior label has normalized
diagonal loss at most `(1-alpha)/(2*d_v)`. At margin
`Theta(alpha*tau)`, this proves at most
`O(1/(tau*sqrt(alpha*d_v)))` wake-ups per label. This is the first proved
response-side occurrence of the desired `1/sqrt(alpha)` scale. It is not yet a
total-work theorem: a naive sum over the live boundary can still be large, and
the loss ledger itself must be maintained without touching every label.

The operator needed for that implementation has an exact graph form. With
`H = D^(1/2) Q D^(1/2)`, one has
`H = ((1-alpha)/2)*(D-A) + alpha*D`, the grounded Laplacian obtained by
scaling original graph edges by `(1-alpha)/2` and adding a ground edge of
conductance `alpha*d_v` at every vertex. Principal Schur complements and
degree-normalized response coordinates respect the same congruence. The
dynamic spectral vertex-sparsifier/electrical-flow locator of van den Brand et
al. is therefore a concrete construction blueprint, but its ambient-graph
preprocessing and locator costs do not transfer as a local theorem.

The full exterior graph is nevertheless unnecessary. For a fixed face, every
response row, source leverage, and diagonal loss is determined by the face's
internal edges, its exposed cut incidences, and the degrees of the boundary
labels. Thus the static operator record has size linear in charged active
volume. More strongly, Chebyshev inverse-square-root probes construct
simultaneous one-sided estimates of every exposed boundary diagonal loss in
`O_tilde(cvol(S)/sqrt(alpha))` work. Geometric full checkpoints therefore fit
the final-volume product ledger. Approximation-stable Chebyshev whitening also
prepares every within-epoch Gaussian source from a constant-factor spectral
frontier in `O_tilde(T_mv/sqrt(alpha))` work; no exact frontier square root is
needed. The next proof target is target-side maintenance of requested
harmonic rows or a shared sparse-recovery bank whose queries use the
two-ledger wake-up schedule.

There is also an exact fixed-anchor implementation identity. Let `Pi` be any
linear sketch on degree-normalized exterior dual demands and precompute
`Z = Q_AA^{-1} Q_AU D_U^{-1/2} Pi^T`. For a frontier vector `y`, the complete
sketch of its lifted dual signature is

```text
Pi D_U^{-1/2} q_U
  = Pi D_U^{-1/2} Q_UF y - Z^T Q_AF y.
```

Both right-hand-side products are generated by scanning frontier incidences.
For an exact Schur-frontier solve, `q_F` is the known frontier source, so its
sketch can be subtracted to leave only exterior coordinates. This eliminates
both dense old-face materialization and an ambient boundary scan. It does not
hide the hard costs: the sketch dimension, anchor solves, storage and reads of
`Z`, and epoch-internal updates remain the quantitative obligations.

A two-sided Gaussian reduction now fixes the group-measurement side of that
interface. Random normalized frontier sources and random targets supported on
one reached hierarchy node estimate its complete leverage mass using only
polylogarithmically many scalar transposed harmonic measurements. The packed
hierarchical locator therefore tests only output-sensitive nodes and never
forms a dense exterior response or an all-leaf squared update. The remaining
problem is narrower: produce or maintain each requested harmonic target row,
or one shared sparse-recovery family covering those rows, within the local
epoch ledger. The reduction is Monte Carlo; deterministic validation remains
separate.

## 2026-08-20: orthogonal frontier lifts close mixed no-restart repair

The response-preconditioned direction has a stronger orthogonality invariant
than the earlier exact-correction telescope. For an expansion from `S_j` by a
batch `B_j`, lift any frontier vector `y` by placing `y` on `B_j` and
`-Q_{S_j S_j}^{-1} Q_{S_j B_j} y` on the old face. Multiplying this lift by
`Q` annihilates `S_j`. Since every earlier lift is supported inside `S_j`, the
entire lifted frontier spaces—not only their exact minimizers—are pairwise
`Q`-orthogonal.

Consequently, independently approximated frontier solves have a final energy
error equal to the sum of their individual Schur-energy errors. This removes
the need to restart or re-optimize any old face in the mixed architecture. It
does not make the lift cheap: every application of the old-face response,
boundary report, and old-coordinate read remains in the explicit response
charge. A second reduction shows that logarithmically many source-normalized
Gaussian response sketches simultaneously approximate all fixed hierarchy
group traces. Fresh sketches drawn after each adaptive batch can be accumulated
through their nonnegative squared masses with a summable conditional failure
budget. Mutual frontier orthogonality makes every prefix valid, and newly
exposed boundary labels have zero response to all earlier frontier bases, so
past probes are never replayed. The two-sided harmonic reduction further
removes the all-leaf range-add. Chebyshev full-boundary sketches separately
close geometric anchor initialization at the product scale, while spectral
Chebyshev whitening removes exact source solves between checkpoints. The
decisive third-direction target is now a target-side dynamic local harmonic
row or shared sparse-recovery interface on a large nonequitable cyclic core.
The
separate response-free expanding-subspace acceleration problem remains open.

## 2026-08-20: source-aware boundary leverage narrows the cyclic reporter

The response-preconditioned direction remains useful after the repository's
large solver-family update, but the universal claim is now concentrated in one
data-structural primitive. The new lemma in
`manuscript/notes/response_preconditioned_hybrid/` uses the dual support of an
exact nested correction. If the correction is generated by a frontier batch
`B`, then its source-aware squared exterior leverages sum to at most `|B|`.
For a declared normalized interval margin, this gives an a priori
degree-volume bound on all rows that can be ambiguous without materializing
the dense old-face correction.

This is stronger than the existing uniform leverage and complementary to the
energy-packing lemma: energy packing bounds the coordinates that actually
move, while source-aware leverage bounds the coordinates whose certified
intervals can be wide before their values are computed. A matched-edge
construction proves that source-oblivious intervals are insufficient. A
single-coordinate correction can make every boundary interval appear
ambiguous at every round, causing quadratic refresh, although only one exact
boundary value changes.

The remaining P0 theorem is now precise: maintain a hierarchy that locates
large source-aware leverage rows and exact threshold crossings with total
`O_tilde(V / sqrt(alpha))` work. A rank-sensitive search lemma now proves the
locator combinatorics: constant-factor subtree leverage masses reduce the
number of hierarchy probes to the packed batch-rank/energy budget times the
hierarchy depth. What is still missing is the dynamic group-trace oracle that
supplies those masses without materializing all response rows. Therefore the
third direction should continue, but work on uniform global energy clocks or
eager boundary arrays should stop.

## 2026-08-20: solver-family organization and response-preconditioned bridge

The project now records its solver classification in
`docs/solver-family-roadmap.md` and the machine-readable
`manuscript/notes/taxonomy.toml`. The classification uses three independent
axes: graph access, support evolution, and inverse realization. In particular,
nested active sets do not imply an SDD method, and adjacency access does not
imply a first-order restriction.

Two new standalone notes isolate the resulting research program:

- `manuscript/notes/response_preconditioned_hybrid/` proves the generic
  bordered-Schur correction, energy-to-boundary interval, and geometric rebuild
  lemmas, then states an exhaustively charged conditional composition theorem;
- `manuscript/notes/local_solver_oracle_hierarchy/` separates adjacency access,
  materialized restricted solves, local-linear-span recurrences, and persistent
  response, and formulates a same-instance recurrence-versus-response
  separation target.

The current judgment is deliberately narrower than universal optimality. A
mixed settled-response/frontier-repair architecture is the strongest
risk-adjusted project design because it interpolates between two unresolved
endpoints. A graph-uniform output-sensitive incremental SDD/Schur solver would
make iterative repair asymptotically unnecessary, while a graph-uniform
no-restart expanding-subspace theorem could attain the product scale without a
nontrivial response representation.

The immediate common target is certified finite-band boundary response on
nonequitable cyclic cores. The response layer must report every safe violation
and certify all unreported boundary coordinates outside the declared band;
spectral energy accuracy or single-coordinate query access alone is
insufficient. The complementary iterative target is acceleration over safely
expanding faces without restarting a complete solve after every support event.

Use `make note-audit`, `make note-report`, and `make note-graph` to validate and
inspect the inventory. These tools do not rewrite research sources.

### Dense response--frontier reference implementation

`src/hybrid_solver_codex/response_hybrid.py` now realizes the proposed
heavy/light controller exactly on small graphs. It maintains a dense inverse on
the settled anchor, warm-starts CG on the exact frontier Schur complement, and
absorbs the frontier after geometric degree-volume growth. Rebuild factors one,
two, and infinity expose the pure-response, mixed, and fixed-anchor iterative
endpoints behind the same support and verification controller.

The experiment `make response-hybrid` keeps adjacency scans, global boundary
reads, dense response-update arithmetic, Schur construction, frontier CG,
materialization, and output writes separate. At `alpha = 0.05`, note-scoped
`eps_ppr = 1e-6`, and random seed 7, factor two reduced the diagnostic response
update arithmetic relative to rebuilding every batch by approximately `77%`
on the path, `88%` on the binary tree, `68%` on the spider, and `66%` on the
random 4-regular graph. Relative to never rebuilding, it reduced frontier CG
iterations by approximately `53%`, `78%`, `54%`, and `34%`, respectively.

An immediate factor-two rebuild fails on the center-seeded star: its single
heavy batch would trigger the full dense response although the frontier solves
in one CG step. The implemented mixed arm therefore gives each new frontier
one converged iterative probe before permitting a volume-triggered rebuild.
This makes the star collapse to the fixed-anchor endpoint with one iteration
and no post-initial response update. These measurements establish a
reproducible tradeoff surface, not a combined work bound or universal hybrid
advantage. The implementation deliberately materializes the full matrix and
performs global boundary reads; replacing those two operations remains the
graph-local P0 obligation.

## 2026-08-20: repeated active-set SDD factor isolated

The new standalone note
`manuscript/notes/incremental_active_set_sdd/` audits the August 2026
Wei--Yang growing-active-set PageRank/RPPR result and resolves the first reuse
questions without overstating the arbitrary-graph case.

Closed statements:

- the source degree-form system is exactly the shared lazy RPPR system after
  the parameter change `alpha_bar = 2 * alpha / (1 + alpha)` and the variable
  change `x = D^(1/2) z`; `rho` is unchanged;
- successive exact restricted states have an explicit block-Schur correction,
  and the sum of their squared correction energies telescopes to at most
  `alpha_bar` along a source-valid trajectory;
- this energy identity is not a work amortization: on endpoint paths the
  active set can grow through every prefix, so any implementation that writes
  the full active vector or performs one full active-set matrix pass per round
  pays `Omega(|S*|^2) = Omega(|S*| vol(S*))`;
- the same endpoint paths admit an exact append-only tridiagonal `LDL^T`
  representation. Two scalars per admitted vertex determine the next boundary
  gate, and one terminal reverse pass materializes the answer. Total charged
  work is linear in the final active volume, with no polynomial dependence on
  `1 / alpha`;
- the exact path replacement inherits deterministic ACL approximation and
  RPPR support-containment/additive-objective guarantees from the source
  active-set proof.

The arbitrary-graph claim remains conditional. The needed primitive must
jointly maintain an implicit nested restricted solution and the complete set
of boundary violations. A conventional SDD warm start is insufficient because
the block correction can be dense and a changed old coordinate alters its
outside neighbors' residues. If a graph-uniform output-linear interface is
proved, Wei--Yang's outer argument would give `O_tilde(1 / rho)` RPPR work,
strictly stronger than the current `O_tilde(1 / (rho * sqrt(alpha)))` project
target. Existing product lower bounds do not rule this out because they use
narrower persistent-support or repeated-row access models.

## 2026-08-19: the orthogonal-locality proof program is closed

The remaining terminal-envelope question for `evolving_support_cg` has a
sharp negative answer. Fixing `alpha` and the note-scoped `eps_ppr`, a
four-vertex core can place one low-degree violating leaf beside a
nonviolating hub of arbitrary degree. Literal violation-only principal
expansion admits the leaf and terminates at degree volume `5`; factor-two
halo growth must also admit the hub to reach its doubling target, ending at
volume at least `M + 5` and performing at least `M` graph work.

The complementary positive statement is also proved: exact violation-only
expansion from a point seed has terminal degree volume at most
`d_source + (1 + alpha) / (2 * alpha * eps_ppr)`. Thus orthogonality itself
does not eliminate spatial locality, and geometric envelopes really do
amortize restart work, but nonviolating look-ahead cannot have a uniform
locality guarantee. The complete algorithmic conclusion is to use
frontier-sparse exact CG as the honest orthogonal baseline, retain
violation-only restricted CG as the support-safe reference, and allow
geometric halo growth only behind a hard degree-volume cap with a certifying
fallback.

The executable decoy sweep uses hub degrees `16, 64, 256, 1024, 4096` at
`alpha = 0.01` and `eps_ppr = 0.25`. Literal work stays `33`; factor-two work
is exactly `4M + 37`. All runs pass the verifier-owned residual certificate.

## 2026-08-18: geometric-envelope CG closes the restart ledger

The `evolving_support_cg` note and prototype now include factor-two envelope
growth after a failed restricted-CG solve.

Closed statements:

- exact line-minimizing CG preserves a nonpositive quadratic objective across
  warm starts and support expansion, so every restricted call retains the
  standard `O(1 / sqrt(alpha))` iteration scale;
- every nonexhausting failed envelope doubles in degree volume, giving at
  most logarithmically many restarts and total revisited envelope volume at
  most three times the terminal envelope volume;
- explicitly charged boundary and breadth-first halo discovery preserves the
  output-sensitive bound
  `O_tilde(vol(U_final) / sqrt(alpha))`;
- certification remains verifier-owned, and all direction recurrences stay
  inside a fixed envelope between restarts.

Measured boundary at `alpha = 0.01` and note-scoped `eps_ppr = 1e-7`:

- factor-two envelopes reduce literal restart work from `278090` to `25676`
  on the 511-path and from `815040` to `89460` on the long spider;
- restarts fall from `76` to `7` and from `64` to `7`, respectively;
- the factor-two method remains `2.1` and `2.6` times more expensive than exact
  frontier-sparse CG and explores `192` rather than `153` path vertices.

The restart-amortization question is therefore closed in terms of the final
explored envelope. The 2026-08-19 decoy theorem resolves the remaining
locality question negatively for unconditional factor-two halo growth.

## 2026-08-16: direct theory of the literal two-rung policy

Recorded as the standalone note
`manuscript/notes/two_rung_direct_theory/`.

Closed statements:

- one relaxation-`omega` coordinate push decreases the unregularized
  quadratic by exactly
  `omega * (2 - omega) * r_u^2 / (1 + alpha)`;
- with charge `1 + d_u`, the empirical key
  `|r_u| * sqrt(d_u) / (1 + d_u)` is a graph-universal factor-two
  approximation to exact objective decrease per charge; the same factor
  holds for a top-`k` residual snapshot, without a band or sign assumption;
- the exact key is `|r_u| / sqrt(1 + d_u)`, giving a concrete ranking
  ablation;
- a fully refreshed score maximizer has a fixed-region charged-work
  contraction, while the literal top-fraction batching still needs a live
  staleness amortization;
- every literal two-rung run terminates under the note-scoped residual, with
  explicit nonaccelerated fallback bounds;
- on the single-edge graph, the complete ranked optimal-SOR trajectory is
  available in closed form and alternates signs with a critically damped
  linear transient;
- the asymptotic one-push settlement ratio is at most `0.3002831060...`
  uniformly over `alpha`; hence every fixed band factor below
  `3.3301906768...` has eventual one-push exact settlement;
- in particular, band factor `B = 2.5` needs at most one exact push after
  twenty spreading pushes on the one-edge model. This rigorously shows why
  neighbor cancellation can validate a band rejected by the
  self-reflection-only rule;
- on a sufficiently long endpoint-seeded path, the normalized optimal-SOR
  residual has an exact parity-wave event representation. Fully refreshed
  absolute-residual ranking executes exactly the events above the spreading
  gate and never charges a negative waiting packet: every such packet has a
  strictly larger enabled positive certificate on its northeast dependency
  chain;
- if `L` is the first depth with `lambda^L <= B * eps_ppr`, the spreading
  phase makes exactly `floor((L + 1)^2 / 4)` pushes and reaches an explicit
  two-level signed plateau. Its charged work is exactly three times that
  count minus `ceil(L / 2)`;
- for every `B < 3.3301906768...`, the path terminal phase pushes each
  high-parity coordinate at most once and possibly one outer coordinate.
  Hence its work is
  `O(V_exp * (1 + log(1 / (B * eps_ppr)) / sqrt(alpha)))`;
- strengthening the live batch guard with the condition `r_u > 0` extends
  the exact path theorem to snapshot batches of arbitrary size. It adds no
  charged coordinate work under the note's meter, though it can add service
  round trips;
- the sign guard is necessary for arbitrary batch sizes: with the original
  absolute live guard, full-frontier batching reaches a two-entry third
  snapshot, pushes a positive coordinate at distance two, and then charges a
  still-negative endpoint;
- for `alpha > 1/49`, including the measured values `0.025` and `0.04`, a
  partial-layer invariant proves that the actual unguarded top-`1/32`
  snapshots preserve the exact spreading and terminal path counts,
  independently of equal-rank tie breaking;
- static top-`1/32` parent closure is nevertheless false: an explicit
  dependency-closed 34-corner interface uniquely selects a distant positive
  event and then a still-negative endpoint. The smaller-`alpha` actual path
  trajectory therefore needs a stronger history invariant;
- on a symmetric `q`-arm spider, refreshed ranking has an exact center-only
  prefix. For fixed `q >= 3` and small `alpha`, it performs
  `Theta(1 / sqrt(alpha))` consecutive center pushes, about half on negative
  residual, with `Theta(q / sqrt(alpha))` charged work;
- this single-branch echo saturates but does not exceed the desired
  explored-volume acceleration budget. Persistent expansion can pay this
  echo, whereas the fixed `P_3` lower bound below shows that a reached leaf
  can turn it into a genuinely slower macrocycle;
- grouping every depth of a symmetric spider into a radial block reduces both
  the optimal-SOR and exact rungs identically to the endpoint-path recurrence
  scaled by `1 / q`. This proves the same accelerated explored-volume bound
  for the complete radial-block spider method;
- on every level-regular rooted tree, shell-energy coordinates
  `z_i = sqrt(n_i d_i) y_i` reduce both radial block rungs to an exact
  symmetric tridiagonal chain. Its edge impedance is
  `2 sqrt(phi_i / (d_i d_(i+1)))`, and its squared shell coordinate is the
  aggregate residual-energy numerator for one-step objective decrease;
- in a homogeneous `g`-ary bulk, a translation-invariant two-level parity
  wave exists only for `g = 1`. The exact uncancelled branch debt is
  `lambda^2 ((g - 1) / (g + 1))^2`, identifying the path as the unique
  homogeneous critical match;
- for every fixed `g >= 2`, refreshed radial ranking performs
  `Theta_g(1 / sqrt(alpha))` consecutive root pushes before selecting level
  one. Thus the common shell-visit factor cannot be constant;
- if a homogeneous expanding tree visits shell `i` at most
  `K (L - i + 1)` times, geometric shell volume absorbs the triangular
  revisits and total charged work is `O_g(K V_L)`;
- more strongly, every finite explored ball of the homogeneous `g`-ary tree,
  `g > 1`, has Dirichlet gap at least
  `(sqrt(g) - 1)^2 / (2(g + 1))`, independent of depth and `alpha`;
- applying refreshed block contraction retrospectively to the final explored
  ball pays all revisits without a per-shell estimate. Both the optimal-SOR
  spreading rung and exact terminal rung terminate with explicit work bounds,
  giving `O-tilde_g(V_exp / sqrt(alpha))` total radial work for every fixed
  band factor;
- a positive Jacobi supersolution with ratio `rho < 1` extends the same
  result to variable level-regular profiles. If every offspring count is at
  least `g > 1`, the homogeneous gap constant remains valid;
- a unary corridor of length `ell` has gap at most
  `alpha + pi^2 / (4 (ell + 1)^2)`, proving that the persistent-expansion
  condition cannot be removed inside the same spectral argument;
- the test vector `sqrt(d_u) g^(-depth(u)/2)` removes level symmetry:
  refreshed individual-coordinate two-rung SOR has
  `O-tilde_g(V_exp / sqrt(alpha))` work on every rooted tree with at least
  `g > 1` children per vertex;
- the unrestricted graph-uniform target is false. On the center-seeded
  three-vertex path, the literal top-`1/32` batches are singletons yet
  `W_spread >= alpha^(-3/2) / 1408` for `B = 2.5`, `eps_ppr = 0.01`, and
  `alpha <= 1e-4`, while `V_exp = 4`. The exact reflecting-leaf macrocycle
  combines `Theta(1 / sqrt(alpha))` center echoes with a
  `1 - Theta(alpha)` slow mode;
- permanent Schur deflation of a certified closed pendant forest costs linear
  forest work, creates no core fill, and erases the reflecting trajectory. It
  gives an `O(V)` exact reached-star solve and closes the accelerated radial
  theorem on every finite symmetric spider;
- the lifted forest-response preconditioner has exactly one generalized
  eigenvalue per eliminated forest coordinate. Every nonunit eigenvalue is
  precisely a preconditioned eigenvalue of the Schur core, so tree decorations
  do not multiply the remaining condition factor;
- repeated degree-one peeling gives the canonical maximal reduction to the
  graph `2`-core. A fully exposed graph with a `k`-vertex core has an exact
  `O(cvol(V) + k^3)` dense-core solve;
- absorbing one newly certified pendant component is one Sherman--Morrison
  update along the attachment Green column. Its exterior demand change is one
  nonnegative range-add vector, directly matching the current finite-band
  response-reporter primitive.

Open boundary:

- extend the actual top-`1/32` endpoint-path invariant to
  `alpha <= 1/49`, or find an actual-run counterexample;
- integrate certified online forest peeling with the response-preconditioned
  controller. Forest algebra is closed; the remaining obligation is to locate
  the finite-band crossings of the implicit Green-column update on a large
  nonequitable cyclic core;
- charge live stale operations inside larger measured batches on the
  resulting positive graph classes;
- do not compare the note-scoped unregularized `eps_ppr` bound with the
  persistent-support RPPR `rho` lower bound without an explicit accuracy and
  oracle mapping.

## 2026-08-16: propagate--settle absorption and revisit-volume framework

Recorded as the standalone note
`manuscript/notes/propagate_settle_framework/`. It extracts a common theory
from `two_rung_sor`, `rlsor_terminal_exact_rung`, and
`frontier_adaptive_ladder`.

Closed statements:

- exact Dirichlet settlement on a region is an affine idempotent map, and
  settlement maps on nested regions satisfy a two-sided absorption law;
- every propagation trajectory supported inside the next settled region is
  erased exactly, so two methods with the same nested discovered regions have
  identical exactly settled iterates and boundary residuals;
- the only possible benefit of over-relaxation in an exactly settled method is
  changing region discovery, discovery time, or discovery work; it cannot
  improve the terminal point of a fixed region;
- repeated unit-relaxation delivery has an exact defect certificate: if its
  remaining interior residual is `e_U`, its quadratic objective excess above
  exact settlement is `e_U^T Q_UU^(-1) e_U / 2`, at most
  `||e_U||_2^2 / (2 alpha)`;
- empirical charge volume `cvol(U) = sum_{u in U} (1 + d_u)` is within a
  factor two of degree volume, so the benchmark and theoretical work units
  can share one amortization;
- the trajectory-sensitive work quantity is the settled-volume revisit factor
  `R_set = sum_k cvol(U_k) / cvol(U_K)`, not the raw batch count;
- under constant scans and width-`w` settlement, work is
  `O((w + 1)^2 R_set cvol(U_K))`;
- condition-free exact RPPR boundary expansion admits only true-support
  vertices and has the sharper bound
  `O((w + 1)^2 sum_k vol(U_k)) = O((w + 1)^2 R_set / rho)`;
- hence the intended product scale needs only
  `R_set = O_tilde(1 / sqrt(alpha))`, a strictly weaker target than bounding
  the number of nonempty batches by the same order;
- a four-vertex tailed triangle refutes activation by root-distance layer: two
  vertices at distance one enter in consecutive exact-gate batches;
- a width-two tailed fan extends the obstruction to any prescribed number
  `L` of singleton batches among distance-one vertices and forces
  `R_set > (L + 1) / 5`, even though the graph has root radius two;
- quantifying the fan's limiting tridiagonal response gives
  `R_set = Omega_alpha(log(1 / rho))`; therefore a log-free revisit theorem is
  false for the literal fresh-refactor-and-rescan gate, while the
  polylogarithmic accelerated target remains viable;
- cumulative settled volume has an exact activation-age dual: every vertex is
  charged once for every fresh settlement after it enters, so the fan lower
  bound is caused by the long paid lifetime of its degree-`m` root;
- seven exact stop rules across five cyclic graph families hold in their stated
  scopes. On the independent double-cycle feed, every backbone-seeded
  report-free prefix is petal-free and the first petal batch contains a report.
  In the anchor-seed counterrange `0<rho<(1-alpha)/8`, the exact continuation
  permits at most the three report-free petals at the seed and its neighbors;
  the first next-layer petal batch co-admits the seed report unless one entered
  earlier. From every relay seed, the initialized singleton either terminates
  or its first propagating batch contains the incident report. The graph family
  is therefore retired only for this prescribed canonical long report-free
  later-petal witness. These are not arbitrary-positive-subset results,
  reporter lower bounds, or claims after reports enter;
- a lazy block-Schur update represents the correction to old coordinates and
  updates all remaining violation demands through one signed Schur
  block-column, without algebraically resettling the old region;
- on the same tailed fan, retaining the exact two-coordinate separator
  `{o, v_j}` reproduces the identical first `L` batches and restricted
  solution in `O(m + L) = O(cvol(U_L))` work, versus `Omega(m L)` for fresh
  settlement; hence the logarithmic fan lower bound is not an
  information-theoretic barrier to an output-linear exact local method;
- more generally, a charged online activation-aligned trace with live frontal
  size `zeta` and at most `nu` exact boundary-demand signatures reproduces
  every gate batch and the terminal solution in
  `O((1 + zeta^2 + nu zeta) cvol(S) + T_sep)` work, with the separator-update
  charge and exact metadata/access model now explicit;
- kinetic scalar threshold reporting removes the `nu` factor when distinct
  demands have stable one-dimensional crossings; rooted spiders admit an
  exact `O(cvol(S) log(2 + R))` online solver even if all `R` frontier
  responses differ;
- stable low-dimensional affine demands reduce exactly to dynamic
  extreme-point reporting; response-rank examples on sparse path cores show
  that bounded state dimension or bounded rekeying is a genuine hypothesis;
- certified low-rank response trees replace exact signature equality by
  rigorous KKT-sign intervals and charge only visited nodes, ambiguous exact
  leaves, factor maintenance, frontal algebra, and separator updates;
- constant-degree expanders with full RPPR support force
  `zeta, nu = Omega(n)` in every activation-aligned flat presentation, so the
  structural condition cannot be removed graph-uniformly within that
  framework; this is not a lower bound against all local solvers;
- the exact cutoff `zeta_0 = ceil(alpha^(-1/4))` caps pre-overflow dense Schur
  work at `O(cvol(S) / sqrt(alpha))`;
- an explicit RPPR tree refutes per-event shock-only continuation under
  explicit batch output, and a block argument separately proves that
  full-sweep accelerated-gradient, Chebyshev, and CG repair require one old-
  face pass even when the event shock tends to zero;
- aggregate numerical repair is nevertheless closed: with an exhaustively
  charged exact-response oracle, leave the iterate unchanged through an epoch
  and perform one final accelerated solve; telescoping charges its work by the
  total face shock and one scan ceiling;
- once an independent exact-response mechanism certifies the groups, heavy
  shocks require only a constant number of numerical repairs per epoch;
  `||q_B||_2^2 >= 2 theta E` is a sufficient repair-frequency condition, not
  an exact-sign certificate;
- lazy inverse-response recursion bypasses the literal gate and computes the
  exact support and solution on every rooted tree in
  `O_tilde((1 + cvol(S*)) / sqrt(alpha))` work; a conditional hierarchical
  route-charge lemma identifies the exact higher-rank interface;
- original-basis multifrontal or Cholesky response hierarchies require
  `Omega(n^2)` explicitly stored numerical entries on bounded-degree
  expanders, and eager exact-demand arrays require `Omega(n^2)` updates on a
  sparse cyclic Stieltjes light cascade; these are representation lower
  bounds, not lower bounds against compressed or matrix-free algorithms;
- relative to a stable exposed block--cut presentation, exact response
  recursion on blocks of size `b` has route work quadratic in `b`; for
  polylogarithmic `b` it reaches the product scale when the presentation can
  be maintained within the same budget, while online response recourse under
  cycle-closing block merges remains open;
- finite-resolution RPPR continuation needs no exact zero-sign decisions in
  an `alpha * tau` normalized KKT band: certified demand error
  `alpha * tau_gate / 4` gives support safety and terminal normalized error
  at most `tau_gate`, and one final accelerated solve yields total error
  `rho + tau_gate + tau_sol`;
- consequently, a graph-uniform finite-band response oracle would imply
  `O_tilde(1 / (epsilon * sqrt(alpha)))` work for degree-normalized PageRank
  error `epsilon`; this is strictly weaker than exact light-sign maintenance;
- accumulating backward packets into one net right-hand side makes a typed
  one-scan causal epoch output-linear on forests and width-sensitive on sparse
  cyclic regions, independent of how many causal paths contributed packets.

Open item:

- within the exact boundary-gate hybrid route, prove graph-uniform response
  maintenance for consecutive light-shock events on nonequitable cyclic
  cores. Numerical amortization is no longer open: one final accelerated
  repair suffices. The missing theorem must build an online response hierarchy
  whose event-route ranks and rekeys total
  `O_tilde(cvol(S*) / sqrt(alpha))`, including initialization, all old-face
  reads, exact sign queries, explicit output, and no future-support advice.
  Root radius, constant flat width, and one global low-rank factor are each
  insufficient on their own. For the approximate target it is enough to prove
  the strictly weaker finite-band certificate bound, charging only the
  transition-band refinements and finite-accuracy response maintenance. Before
  that reporter analysis, a new legality candidate must use a different
  coupling or bounded-degree settlement gadget: the backbone, anchor, and
  relay seed orbits retire the double-cycle family for the prescribed witness.
  The new trace must still prove every seed orbit and genuinely changing
  response directions before reporter algebra begins.

## 2026-08-16: adaptive revisit control and safe policy portfolios

Recorded as the standalone note
`manuscript/notes/adaptive_revisit_control/`. The note isolates the
cross-instance revisit-memory idea from the measured frontier ladder and asks
what it can support without assuming that task difficulty transfers between
graphs or seeds.

Closed statements:

- the stored revisit ratio is exactly the charge-weighted mean number of paid
  visits to a touched coordinate, and its excess over one is the realized
  revisit work divided by touched-support charge;
- a four-way ledger indexed by the previous and current exact/spreading modes
  decomposes all revisit work exactly;
- every paid revisit after an exact push certifies intervening
  neighbor-generated backflow, because the exact push left zero residual on
  that coordinate;
- on a nested propagate--settle trace, the empirical ratio factors exactly as
  the settled-volume revisit factor times the settled-volume-weighted mean
  within-epoch multiplier;
- a causal revisit bank admits all first touches and only affordable repeated
  touches, enforcing `Work_t <= Gamma C(S_t)` at every prefix; applied to the
  propagate--settle ledger, this removes the assumed bounded-propagation
  multiplier and leaves the cross-epoch settled-volume factor as the
  structural obligation;
- every terminal support-safe RPPR trace has the a posteriori certificate
  `Work <= 2 rho_rev / rho`; a global bank with
  `Gamma = O_tilde(1 / sqrt(alpha))` therefore certifies the intended
  `O_tilde(1 / (rho sqrt(alpha)))` fast path without a structural graph
  condition, while a first overdraw caps the prefix before canonical fallback;
- the literal fixed-band two-rung continuation cannot make that bank
  graph-uniform: on one edge, an RPPR-certified support-safe handoff lies
  strictly below the spreading threshold and its exact-delivery tail takes
  `Omega(1 / alpha)` work at fixed `rho` and fixed `eps_ppr`;
- the scalar ratio does not order total work because its touched-support
  denominator is policy dependent, and one historical scalar cannot identify
  which of two future policies is better over unrestricted task sequences;
- immediate quadratic-objective decrease per charge is uniquely maximized by
  `omega = 1`, so any advantage of over-relaxation must arise over a
  multi-operation transport block rather than from a myopic descent score;
- every causal controller clamped to `omega in [1, 2 - delta]` terminates from
  the zero iterate when every paid operation satisfies the live note-scoped
  degree-normalized residual gate, with charged work at most
  `(1 + alpha) / (delta * (2 - delta) * alpha * eps_ppr^2)`;
- a budgeted adaptive prefix can switch irreversibly to exact Gauss--Seidel on
  the same state; its energy decrease is credited against the tail, giving
  `Work_total <= H_0 + (1 - delta * (2 - delta)) Work_prefix` and a hard
  near-baseline ceiling without branching or reset;
- a branchable weighted portfolio of finitely many certifying local policies
  has work `min_j Work_j / nu_j`, up to one scheduling chunk; uniform shares
  are therefore `K`-competitive with the best of `K` arms on every instance;
- a geometric restart portfolio uses one live policy state at a time and costs
  less than `4 K max(Work_best, B_0)`, so simultaneous branches are not needed
  when a clean instance reset is available;
- for single-seed RPPR, every exact restricted settlement is a canonical
  absorption checkpoint: a history-dependent controller may change policy and
  admit any nonempty subset of exact boundary violations while preserving true
  support containment, positivity, and finite termination; combining this gate
  with the revisit bank gives a genuine work-capped no-reset switch theorem;
- a finite simple unweighted single-seed RPPR tree, consisting of an
  independent length-`L` path and one heavy branch, has two legal exact
  boundary-batch orders with the same terminal canonical point and
  `R_set(early) / R_set(late) >= (L + 1) / 5`; hence checkpoint absorption,
  nested support, persistence, and even treewidth one cannot imply best-arm
  work competitiveness or policy-blind accelerated-bank success;
- if each policy has a work-valued countdown decreased by its own certified
  blocks and never increased by blocks of other policies, a fair scheduler
  committing every block to one shared state costs at most
  `min_j Phi_j / nu_j` plus scheduling discrepancy; `kappa`-tight countdowns
  make the uniform shared-state portfolio `K kappa`-competitive;
- irreversible common-state activation tokens give a general construction of
  such countdowns; on endpoint paths, one forward Schur-record token and one
  reverse-recovery token per true-support vertex give `kappa = 1`, exact
  declared work at most `2 C(S*) <= 4 / rho`, and a no-reset shared-state
  portfolio bound `4K / rho + Delta`;
- on the fixed-`m`, branch-seeded caterpillar, literal separately addressed
  `EagerTipKey` storage has `m(m+1)` changed old-key writes along one legal
  positive-subset order, but this is only a representation obstruction;
- for the explicit backbone-first positive-subset policy on that same family,
  `CaterpillarKineticDelta` maintains the exact all-positive live-tip set with
  strict crossing keys, emits each newly positive label once, and charges
  `O(m log(2+m))` exact-cell work and `O(m)` retained state. The result is
  delta-only and family-dependent in `rho`; canonical all-violations,
  pre-backbone interleavings, repeated full lists, finite precision, and a
  graph-uniform reporter remain open;
- on the smaller fixed-family range
  `0<rho<rho_can(m,alpha)<=rho_cat(m,alpha)`, the actual canonical
  all-violations caterpillar trace has exactly `m` strict three-label layers.
  `CaterpillarCanonicalLayerDelta` charges every localized absorption/transfer
  update, demand query, certificate exchange, recovery, validation,
  materialization, and output in `O(m log(2+m))` exact work and `O(m)` state.
  It remains branch-seeded, fixed-`m`, delta-only, and exact-real;
  `rho_can<=rho<rho_cat`, other seeds or policies, repeated full lists, finite
  precision, and graph-uniform work remain open;
- on a two-vertex RPPR breakpoint, a legal activation of fixed charge two has
  a vanishing state jump and energy drop; therefore no jointly continuous
  numerical-state countdown can pay activation uniformly, and the necessary
  energy multiplier diverges as the breakpoint is approached;
- the quadratic energy budget is an unconditional mergeable countdown for
  clamped live updates, but it has the nonaccelerated safety scale and does not
  distinguish the empirical arms;
- arbitrary revisit-based predicted shares remain distribution-free safe
  after adding an exploration floor, and the portfolio inherits any
  `O_tilde(V_loc / sqrt(alpha))` bound already held by one of its constant-many
  arms.

Boundary and open items:

- the safety bound is not accelerated and has quadratic tolerance dependence;
- the finite portfolio removes the need to know the best policy in advance,
  but the one-edge theorem refutes a graph-uniform accelerated work bound for
  the literal fixed-band two-rung continuation; adaptive SOR remains only a
  certified empirical arm unless separately analyzed;
- safe switching no longer requires branchable state, reset, or an assumed
  cross-policy state-transfer map at exact RPPR checkpoints; what remains is
  an order-independent activation-once transport representation for general
  branching and cyclic fronts, or a quantitatively forced-spreading arm; raw
  delayed-reflection and causal-backflow magnitudes are not themselves
  interference monotone;
- structured extensions now cover the center-seeded three-arm spider and the
  branch-seeded double-Y fixed core, while the backbone-first and strict
  canonical-layer caterpillar results supply delta reporting on one growing
  core. They still do not give an
  arbitrary-tree, order-independent response: the existing lazy tree-response
  iterator follows a sorted homotopy order, and another legal boundary policy
  can admit a different positive branch first. The next tests are the
  remaining canonical range `rho_can<=rho<rho_cat`, arbitrary pre-backbone
  behavior, and the separate full-list interface;
- a continuous relaxation family cannot be reduced safely to a finite grid
  without a regularity theorem for thresholded SOR work as a function of
  `omega`.

## 2026-08-16: finite-propagation CG and evolving principal systems

Recorded as the standalone note
`manuscript/notes/evolving_support_cg/`, with executable prototypes in
`src/hybrid_solver_codex/evolving_cg.py`.

Closed statements:

- exact ordinary CG from a seed-supported right-hand side has one-hop finite
  propagation; its cumulative direction envelope is a valid locally evolving
  set sequence, while each matrix product scans only the current direction;
- the resulting graph work through iteration `K` is bounded by the sum of
  the degree volumes of the visited seed balls, without changing the CG
  recurrence or its `1 / sqrt(alpha)` spectral iteration scale;
- the note-scoped degree-infinity residual certificate implies the matching
  degree-scaled solution-error guarantee;
- masking or thresholding a live direction destroys conjugacy on a
  three-coordinate path, whereas full reorthogonalization remains spatially
  confined but becomes dense in the accumulated support;
- exact principal-subsystem solutions are nonnegative, grow coordinatewise
  under support expansion, and expose nonnegative residual only on the
  boundary, giving a correct restarted evolving-set scaffold.

Measured boundary:

- frontier-sparse exact CG certified all five synthetic graph families;
- restart-after-every-boundary-expansion cost `1.6` to `23.4` times more
  graph work, so that literal policy is refuted as the primary solver;
- fast-growth graphs still make exact CG global quickly. Geometric growth
  amortizes restarts in terms of the terminal envelope, but the 2026-08-19
  high-degree decoy refutes any `alpha`/`eps_ppr`-only bound on that envelope.

## 2026-08-15: alpha-scaled exact rungs and delayed reflection debt

Recorded as the standalone note
`manuscript/notes/delayed_reflection_ladder/`.  The note turns the measured
alternating exact-rung R-LSOR mechanism into a proof program and audits it
against the active long-spider obstruction.

Closed statements:

- with `lambda = (1 - sqrt(alpha)) / (1 + sqrt(alpha))`, optimal SOR has
  `omega_star = 1 + lambda^2` and leaves signed self-reflection
  `-lambda^2 * r_u`;
- an immediate over-relaxed push followed by an exact push is exactly one
  unit-relaxation push, so delay is mathematically load-bearing;
- current-rung no-self-reactivation requires
  `b <= lambda^(-2)`, and missing the next rung requires
  `b <= lambda^(-1)`;
- both admissible bases are `1 + Theta(sqrt(alpha))`, giving
  `Theta(log(R) / sqrt(alpha))` rungs over dynamic range `R`;
- every fixed base `b > 1`, including two and three, eventually violates the
  optimal-SOR no-self-reactivation window as `alpha -> 0`;
- exact unit-relaxation cleanup contracts degree-weighted absolute residual
  mass from arbitrary signed states;
- a fresh/debt residual split preserves `r = b - Qx` exactly while allowing
  self-reflection to be delayed;
- on a spider arm, the neighbor-generated backward packet has magnitude
  `lambda * |r_u|`, larger than the self-debt `lambda^2 * |r_u|`, so delaying
  self-reflection alone cannot remove the triangular traversal.

Conditional target:

- if a causal spreading/exact-cleanup pair costs `O(V_loc)` work and reduces
  the live threshold by an admissible alpha-scaled factor, the total is
  `O(V_loc * log(R) / sqrt(alpha))`; this yields the intended accelerated
  scale under an `O(1 / eps_ppr)` PPR volume bound or the proved safe RPPR
  `O(1 / rho)` support bound.

Open item:

- the exact-debt half of causal pair locality is now closed: a restricted
  block correction zeros all residual in a discovered region; leaf
  elimination computes the correction and boundary residual in `O(vol(S))`
  work on forests, while a width-`w` elimination order costs
  `O((w + 1)^2 vol(S))`;
- exact block cleanup erases all SOR relaxation and scheduling history within
  a fixed region, returning the unique restricted Dirichlet point; therefore
  the only possible accelerated role of the ladder is online region discovery;
- given the exact RPPR support, a shifted Dirichlet solve plus boundary KKT
  check returns the RPPR optimum and an unregularized residual certificate;
  on a forest support with a single seed its cost is `O(1 / rho)`;
- RPPR support components must contain seed coordinates, so single-seed
  support is connected and boundary expansion is complete;
- on an endpoint path, a forward Schur recurrence discovers the exact RPPR
  boundary at the first nonpositive transformed demand; one reverse pass
  solves the support in `O(1 + vol(S*))` work;
- arm symmetry reduces the lower-bound path-bundle spider to the same radial
  recurrence, giving `Theta(1 / rho)` actual scan work on that instance;
- therefore the existing `Omega(1 / (rho sqrt(alpha)))` persistent-support
  product is oracle-specific rather than universal: it charges all resident
  volume at every exposure round, whereas directed Schur messages scan only
  the frontier and then back-substitute once;
- on a rooted tree, every child subtree response as a function of its parent
  value is continuous, monotone, and piecewise affine with nested supports;
  it is zero exactly below the one-edge threshold
  `alpha * rho * sqrt(d_child) / (-Q_parent,child)` and has at most one new
  affine piece per activated subtree vertex;
- the exact tree recursion sums child responses into a strictly increasing
  inverse map `H_u`; its slope is the local Schur complement divided by the
  parent coupling and is at least `alpha / (-Q_parent,child)`, so child
  breakpoints are merged and monotonically transformed without combinatorial
  proliferation;
- explicit bottom-up materialization of these response lists gives an exact
  `O(n^2 log(1 + max_degree))` solver on every finite tree, with no exponential
  active-set enumeration;
- lazy response iterators request only realized activation events, scan an
  active vertex's adjacency once, and never inspect descendants of an inactive
  boundary vertex;
- Chebyshev approximation of `Q^(-1)` gives exponential graph-distance decay
  with ratio `(1 - sqrt(alpha)) / (1 + sqrt(alpha))`; on every graph, the
  exact support radius is
  `O(1 + log(1 / (alpha rho)) / sqrt(alpha))`;
- charging each realized activation through its active ancestors proves an
  exact, support-oracle-free
  `O~(1 / (rho sqrt(alpha)))` degree-work solver on every finite tree, with
  `O(vol(S*))` storage;
- fixing the root value on an arbitrary graph gives one scalar
  piecewise-affine obstacle homotopy with nested supports and at most one
  activation event per nonseed vertex; cyclicity therefore does not obstruct
  exact support discovery;
- an exact block-inverse identity shows that one activation updates every
  remaining slack by one nonpositive Schur-complement column times the new
  coordinate; the unresolved event data structure is therefore a kinetic
  minimum under successive signed low-rank updates, not a correctness issue;
- for block-incidence graphs with biconnected blocks of size at most `q`, lazy
  block responses give an exact, condition-free
  `O~(q^3 / (rho sqrt(alpha)))` solver;
- on a single-seed cycle, reflection symmetry reduces the whole biconnected
  core to a radial tridiagonal Stieltjes system; one forward Schur recurrence
  and one reverse solve discover and return the exact solution in
  `O(1 + vol(S*))` work;
- this output-linear result extends from cycles to every
  root-distance-equitable graph.  Orthogonal shell averaging commutes with the
  RPPR matrix, so the full nonnegative obstacle problem reduces exactly to a
  tridiagonal quotient.  Scanning a certified active shell reveals the next
  shell's size, backward incidence, and degree before that next shell is
  scanned; its Schur demand therefore supplies a lazy KKT stopping test.  The
  resulting exact solver costs `O(1 + vol(S*))` without support, radius, or
  confinement advice, even with arbitrarily thick shells.  Examples include
  cliques, complete bipartite graphs, hypercubes, Hamming and Johnson graphs,
  and all distance-regular graphs;
- the shell method no longer requires a trusted global promise.  On an
  arbitrary graph, each active scan audits the degree and three shell-incidence
  counts.  The last active scan also gives every coordinatewise boundary
  violation before those boundary lists are scanned.  An empty positive set
  is a full KKT certificate; a partial set or failed uniformity check is a
  concrete witness and is handed unchanged to the safe exact boundary gate;
- one cell per distance shell is not necessary.  For an equitable partition
  whose distinct-cell interaction graph is a tree,
  orthogonal cell averaging gives an exact tree-sparse Stieltjes quotient.
  Lazy cell responses reveal the first child event before scanning that cell,
  and the full solver costs
  `O(vol(S*) + log(1 + Delta_P) sum_active_cells quotient_depth)` =
  `O~(1 / (rho sqrt(alpha)))`.  This permits several inequivalent thick cells
  in one shell and original graphs with unbounded treewidth and arbitrarily
  large biconnected cores;
- the partition representation is no longer an oracle condition.  Starting
  from root and degree colors, online equitable refinement uses only counts
  from already scanned adjacency lists.  Every visible class is a union of
  hidden true cells, and indistinguishable boundary cells have one common
  affine slack, so they activate as an exact tied bundle.  Once scanned, a
  bundle may split and fork only its future response.  Smaller-half refinement
  costs `O(vol(S*) log(1 + vol(S*)))`; all response forks retain the
  `O~(vol(S*) R_*)` ancestor charge.  Hence the exact
  `O~(1 / (rho sqrt(alpha)))` bound needs no supplied cell identifiers and
  remains a certifying fast path on arbitrary graphs;
- the supplied-support assumption is removable on arbitrary graphs: exact
  boundary-violation batches admit only true RPPR-support vertices, terminate
  at the exact optimum in at most `|S*|` batches, cost
  `O(1 / rho^2)` with fresh forest elimination, and cost
  `O((w + 1)^2 / rho^2)` with supplied width-`w` intermediate orderings;
- retaining the realized nonempty-batch count `J` sharpens the latter bound to
  `O((w + 1)^2 (J + 1) vol(S*))`; if at most `chi_*` support vertices occupy
  each root-distance shell, then `J + 1 <= chi_* (R_* + 1)` and the
  graph-universal radius lemma gives
  `O~((w + 1)^2 chi_* / (rho sqrt(alpha)))`;
- this radial-width result closes arbitrarily long cycles and fixed-width
  cyclic strips without assuming bounded biconnected blocks; the direct cycle
  recurrence is stronger and output-linear;
- a tied activation batch has an exact block-Schur update: the new block is
  solved with its principal Schur complement, the old active solution receives
  one inverse-positive correction, and every remaining KKT slack changes by
  one nonpositive Schur block-column;
- every exact-gate expansion dominates one unit proximal-gradient step, so the
  RPPR objective gap contracts by `1 - alpha`; if `delta_*` is the smallest
  positive optimum coordinate, the gate terminates within
  `O(1 + alpha^(-1) log_+(1 / (d_o delta_*^2)))` batches, in addition to the
  finite-support bound;
- a three-vertex endpoint path proves that this energy route cannot become a
  graph-uniform accelerated contraction: as `rho -> 0`, its first-batch gap
  ratio is
  `(1 - alpha)^2 / (1 + 6 alpha + alpha^2) = 1 - 8 alpha + O(alpha^2)`;
  this refutes a `1 - Theta(sqrt(alpha))` per-batch gap argument but does not
  refute an accelerated combinatorial batch-count theorem, since that path
  terminates in two batches;
- this condition-free bound already meets `O(1 / (rho sqrt(alpha)))` for
  `rho >= sqrt(alpha)`; the lazy-response theorem closes the fine regime on
  trees as well;
- on the alpha-scaled path `rho[k + 1] = lambda^s rho[k]`, the supplied-
  support exact-rung volume ledger is geometric and costs
  `O((w + 1)^2 / (rho_final sqrt(alpha)))`, without an extra dynamic-range
  logarithm;
- the remaining open structural item is compressed event maintenance, or a
  universal batch-count argument, inside a large biconnected core with
  neither bounded articulation blocks, an equitable tree quotient, nor thin
  radial support.  Exact support discovery, cycles, thick
  equitable cells, fixed-width strips, and bounded-size cyclic blocks are
  closed.

## 2026-08-14: active lower-bound ledger and first tight local hybrid

The active manuscript now separates six algorithm-specific statements under
their native accuracy conventions.

Closed statements:

- the classical APPR proof was rechecked against Andersen, Chung, and Lang
  (2007), Definition 3.3, Lemma 3.4, Algorithm 1, and Theorem 3.2. The lazy
  update, column-vector invariant, mass identity, ordering-independent star
  lower bound, and RPPR bridge are correct;
- a new numerical regression test solves the PageRank and RPPR systems
  directly and verifies `p + pr(r) = pi` for every implemented active ordering;
- full-batch RPPR ISTA retains its previously proved tight general-seed work
  `Theta((1 + log(1 / (delta * rho))) / (alpha * rho))`;
- residual-thresholded coordinate ISTA has a new ordering-independent star
  lower bound `Omega(1 / (alpha * rho))`. Together with its existing potential
  upper bound, this proves exact worst-case work
  `Theta_delta(1 / (alpha * rho))` for every fixed relative accuracy `delta`;
- the coordinate-to-batch coarse-to-fine hybrid inherits the same lower bound
  from its first phase and therefore has the same exact fixed-accuracy
  worst-case order. This is the first active-manuscript hybrid with matching
  upper and lower work bounds;
- the coarse forward-push star proof was strengthened from a scheduled-cycle
  argument to an ordering-independent flow proof, giving an explicit matching
  lower bound for Phase I;
- the full fixed-relaxation FIFO CF-Push hybrid still has only the spider lower
  bound `Omega(1 / (alpha * eps_ppr))` and the weaker energy upper bound. Its
  exact worst-case order remains open.

Scope boundary:

- these statements do not identify `eps_appr`, `rho`, `delta`, and `eps_ppr`;
- tightness is for the stated algorithms and work models, not for every local
  graph oracle;
- the graph-uniform accelerated `O_tilde(1 / (rho * sqrt(alpha)))` target
  remains open and the AESP--LOCSOR publication gate is unchanged.

## 2026-08-12: ASPR 2023 correctness and path tightness audit

Recorded as a standalone note in `manuscript/notes/aspr23_bound_audit/`.
The note reconstructs the intended exact-arithmetic ASPR theorem after
repairing the source's quadratic normalization, RPPR linear term, and the
APGD-output distance display.

Closed statements:

- the support-safety and objective-gap argument is valid for the corrected
  Stieltjes quadratic contract;
- on an endpoint-seeded RPPR path with full optimal support, every proper
  active prefix exposes exactly its next vertex;
- for sufficiently small objective-gap tolerance, literal ASPR makes exactly
  `|S*|` APGD calls and has restricted-solve work
  `Omega(|S*|^2 / sqrt(alpha))`;
- literal fresh-gradient discovery separately costs `Omega(|S*|^2)` on the
  same family;
- these bounds match the two structural products in the published ASPR upper
  bound up to logarithms;
- the quantitative scaling `alpha = |S*|^{-2}`, `rho = alpha / 100`, and
  `eps_obj = 10^{-4} alpha^2` gives
  `Omega(|S*|^3 log |S*|)` ASPR work versus
  `O(|S*|^2 log |S*|)` FISTA work at the same tolerance, while the 2026
  leaf-star lower bound gives the opposite separation when FISTA activates a
  high-degree center;
- the post-COLT official Julia repository generally plots default ASPR faster
  than its FISTA and ISTA baselines, with CASPR fastest, so those plots are not
  evidence that default ASPR is empirically slow;
- in official commit `3a169eb`, the periodic boundary-gradient option deletes
  the active-to-boundary cross block before evaluation. Its early-discovery
  flag is therefore inert on RPPR and the periodic variants only add work;
- the same implementation's in-place retraction fails to clip entries in
  `(0, delta)`, and the baseline support filter performs an `O(n)` complement
  allocation outside the stated local work model;
- a corrected early-discovery method still needs one successful event per path
  layer and `Omega(|S*|^2)` work under fresh-prefix scans, although the current
  proof does not retain the per-stage `1 / sqrt(alpha)` inner lower bound for
  that variant.

Scope boundary:

- the lower bound is for literal ASPR, not every accelerated local solver;
- the sufficiently small accuracy is an objective-gap target and is not
  identified with APPR, PPR infinity error, or the experimental proximal
  fixed-point residual;
- an algorithm-independent local-oracle lower bound remains open.

## 2026-08-13: composite AESP-CD inner oracle proved

The standalone note `manuscript/notes/aesp_cd_l1_rppr/` uses the shared RPPR
objective and analyzes a local proximal-coordinate inner method with
degree-weighted update cost.

Closed statements:

- the minimum-magnitude composite KKT map is one-Lipschitz in each untouched
  coordinate's smooth gradient;
- every exact proximal coordinate update decreases weighted KKT mass by the
  factor `2 * (alpha + kappa_A) / (1 + alpha + 2 * kappa_A)` times the updated
  violation, including zero hits and sign crossings;
- the degree-normalized KKT diagnostic divided by the shifted strong-convexity
  constant certifies degree-normalized solution error;
- both results extend to any separable `l1`-regularized Stieltjes quadratic
  `H` that admits a positive supersolution `H v >= mu v`, with coordinate
  contraction factor `(H v)_i / (H_ii v_i)`;
- thresholded sequential updates have work at most
  `C_t(z_0) / (tau_cd * eps_in)` and give an explicit objective-gap inner
  oracle; for `kappa_A = 1 - 2 * alpha`, `tau_cd = 2/3`;
- consequently, composite AESP can use this oracle from its signed
  extrapolated centers, with cumulative inner work at most
  `3 / (4 * (1 - alpha)) * sum_t C_t(y_(t-1))^2 / phi_t`;
- the raw absolute-gap functional cannot be controlled pointwise by outer
  objective error: minimum KKT mass is discontinuous when a nonzero coordinate
  approaches an `l1` kink;
- the standard composite Catalyst proximal warm start smooths this
  discontinuity, and greedy normalized-KKT coordinate selection contracts
  mass exponentially in degree work on a fixed envelope of volume `V`;
- with Catalyst's relative criterion C2, every inner stage costs
  `O_tilde(V)`, so a certified envelope gives total
  `O_tilde(V / sqrt(alpha))`; an optimal-support oracle specializes this to
  `O_tilde(1 / (rho * sqrt(alpha)))`;
- the actual full-graph heap implementation needs no support oracle and has
  trajectory-dependent work
  `O_tilde(V_exp_max / sqrt(alpha))`, where `V_exp_max` is the largest degree
  volume explored by one stage; every newly nonzero KKT key is locally exposed
  by a touched coordinate or one of its neighbors;
- if a proximal center is a certified lower solution, Stieltjes comparison
  traps its exact shifted minimizer, proximal warm start, and every greedy
  coordinate iterate below the RPPR optimum; no KKT key outside the optimal
  support activates, so that entire safe-centered call costs
  `O_tilde(1 / rho)` without a support oracle;
- any signed finite-support trial point can be converted locally into a lower
  certificate by subtracting its maximum normalized negative one-sided
  residual and clipping at zero; this makes the safe-center result directly
  applicable to accelerated trial points;
- the resulting safeguarded outer recurrence remains inside the optimal
  support, its stage-start KKT masses telescope to at most `1-alpha`, and its
  total correction mass has no hidden `1/alpha` loss;
- the exact Nesterov-potential defect is identified. A three-vertex path
  refutes pointwise momentum nonexpansion, while the multiplicative potential
  ledger reduces the remaining accelerated-continuation question to bounding
  positive cumulative correction log-inflation under the
  proximal-displacement collapse identity;
- an exact single-edge family with singleton optimal support has a full
  correction every other stage but zero normalized log-inflation. Thus raw
  correction count cannot be charged only to support additions or substituted
  for the positive-inflation ledger;
- every `log max(1,gamma_t)` is now upper-bounded by a normalized
  collateral-clipping fraction. The fraction uses the unknown optimum, may
  overcharge a benign collateral round, and has the exact collapse amplitude
  for stages `t >= 2`;
- an exact full-support single-edge family has a harmful stage-two collateral
  charge of order `q` but only order-`q^2` Euclidean log-progress. Thus no
  `o(1/q)` coefficient packs the analytical charge by that logarithmic
  telescope. This does not refute actual cumulative log-inflation or another
  potential;
- zero-start coordinate descent for unshifted RPPR recovers the standard
  `O(1 / (alpha * eps_kkt))` degree-work scale.

Scope boundary:

- the diagnostic remains note-scoped and is not identified with the source
  proximal fixed-point residual or a repository stopping rule;
- the result closes the composite inner-locality conjecture but not the
  oracle-free graph-uniform accelerated theorem: start-mass interaction is now
  closed both on a fixed certified envelope and in terms of realized explored
  volume; safe lower centers also enforce `V_exp_max <= 1 / rho` for each
  inner call, and the safeguarded recurrence retains this order safety. What
  remains open is the quantitative outer amortization: cumulatively pack the
  proved collateral fractions using multistep collapse information or a
  different potential, or replace them by a locally checkable surrogate,
  tightly enough to retain the
  `O_tilde(1 / sqrt(alpha))` accelerated stage scale.

## 2026-08-12: volume-gated RPPR acceleration and expanding-subspace lemma

Recorded as a standalone note in
`manuscript/notes/volume_gated_acceleration/`. The note reconstructs the
active-volume flattening discussion and separates the spider's spectral
behavior from support-growth and repeated-scan work.

Closed statements:

- every principal restricted PageRank system has condition number at most
  `1 / alpha`; on a depth-`L` spider prefix the exact scale is
  `Theta(1 / (alpha + L^(-2)))`, so the spider obstruction is geometric
  rather than a local condition number of order `1 / alpha^2`;
- exact PPR has a degree-volume-`1 / tau` superlevel core whose Dirichlet
  restriction is `tau`-accurate in degree-normalized infinity norm;
- fixed RPPR regularization gives support volume at most `1 / rho` and PPR
  error at most `rho`;
- an arbitrary signed restricted candidate can be corrected to a safe lower
  envelope; one-sided KKT violations then admit only true-support vertices,
  and the absence of such violations certifies normalized infinity error;
- choosing `rho = tau = epsilon / 2` proves peak working volume at most
  `2 / epsilon` and final PPR error at most `epsilon`;
- an endpoint-source path forces
  `Omega(log(sqrt(alpha) / rho) / sqrt(alpha))` one-vertex expansions,
  refuting the claim that support changes can always be grouped into only
  `O(log(1 / epsilon))` ordinary restarts;
- the exact expansion gain is a Schur-complement quadratic. Its elementary
  bound is a lower bound, not the upper perturbation bound required for
  accelerated stability;
- transporting the estimate center by the exact restricted-optimum shift adds
  exactly one Schur gain, and these nonnegative gains telescope. On an endpoint
  path, centered momentum plus an append-only exact `LDL^T` response realizes
  each transport append in newly admitted volume while every old-prefix pass
  remains separately charged;
- with `q=sqrt(alpha)`, the weighted Schur tail is exactly
  `(1-q)^(T-1) H_0 + q sum_(t=1)^(T-1) (1-q)^(T-1-t) H_t`, where `H_t` is
  remaining face gain. A terminal-edge execution has ratio
  `W_T/(q sum_t Delta_t)=(1-q)/q`, refuting only a universal
  `C q sum_t Delta_t` shortcut;
- the exact zero-start endpoint-seeded ambient-degree path family with
  `q=1/n`, integer `n>=2`, `L=n^2`, exactly `N=L+1` edges, and
  `rho=tau=(q/3)((1-q)/(1+q))^L` forces `J>=L`, `T>=L`, and literal
  full-prefix swept work `mathfrak V_T>=L^2=q^(-4)`, while
  `nu_fin/q=Theta(q^(-3))`. This refutes only a log-free charge for that named
  exact-real implementation: the certified extra factor is
  `Theta(log(q/rho))`, no matching swept-volume upper bound is proved, and
  soft order and implicit implementations remain open;
- at the constant ratio `rho=tau=q/5`, with `0<q<=1/4`, the exact support
  radius gives `J,nu_fin=Theta(1/q)`, `T>=J`, and
  `mathfrak V_T=Omega(q^(-2))=Omega(nu_fin/q)`. An exact `q=1/5` run refutes
  frontier-only gate logic: the global correction suppresses a raw stage-6
  frontier violation while maximized at the seed, then moves to old interior
  vertex `v_2` by stage 9. These are a product-scale floor and a gate-locality
  STOP, not the observed `q^(-2)` stage or `q^(-3)` swept laws;
- for that same exact-real zero-start, internally gated transported-center
  path execution, a moving-maximum energy argument controls the correction
  without locating its maximizer. With
  `K_q=ceil(log(50(1+q^2)^2 q^(-10))/(-log(1-q)))`, every visited face admits
  or certifies within `K_q` consecutive fixed-face steps. Hence
  `T<=(J+1)K_q=O(q^(-2) log(1/q))` and
  `mathfrak V_T=O(q^(-3) log(1/q))`. The literal full-prefix upper vector
  charges all eleven coordinates and has exactly one terminal external return.
  It proves neither matching lower bounds nor removal of the logarithm, and it
  does not cover the zero-padded recurrence, nonpath graphs, intermediate
  emissions, or finite precision;
- a Round-013 attempt to prove a terminal logarithmic block from the
  conditional full-face spectral recurrence was withdrawn. The damped-cosine
  roots are correct under inactive projection, but they do not determine the
  actual entry coefficients or prevent cancellation in the moving residual
  range. The finite exact runs are scaffolding, not an asymptotic theorem;
- continuous restricted re-solving costs telescope to
  `O(log(1 / epsilon) / sqrt(alpha)) + N_exp` full iterations.

Open item:

- the graph-uniform `O_tilde(1 / (rho * sqrt(alpha)))` work theorem remains
  open. The accuracy-driven family separates only log-free literal accounting.
  At constant ratio, the product-scale floor and one-log upper bounds do not
  match: `Omega(q^(-2))` stages, `Omega(q^(-3))` swept volume, and removal of
  the logarithm remain unproved. The quarantined root calculation supplies no
  terminal lower block, asymptotic lower ledger, or refutation of
  `K_face=O(q^-1)`. The next falsifiable target is an exact space--time lower
  potential with explicit entry coefficients and anti-cancellation, or a
  logarithm-free moving-maximum analysis, with every old-prefix pass charged.
  Endpoint-path implicit transport still does not cover branching, finite
  precision, or the literal zero-padded recurrence. The note does not close
  the separate AESP--LOCSOR promotion gate or promote the universal bound into
  the active manuscript.

## 2026-08-12: rigorous AESP--LocGD center-star lower bound

Recorded as a standalone note in
`manuscript/notes/aesp_locgd_star_lower_bound/`. The note reconstructs the
complete proof development for the literal AESP-PPR outer loop with the
batched LocGD inner solver and uses the AESP paper's cumulative active-volume
work measure.

Closed statements:

- on the center-seeded star `K_{1,B}`, every nonempty batched LocGD call costs
  at least `B`, and every `epsilon`-accurate output requires
  `Omega(B / sqrt(alpha))` work whenever `B * epsilon <= 1/4`;
- choosing `B = floor(1 / (4 * epsilon))` gives the unconditional lower bound
  `Omega(1 / (sqrt(alpha) * epsilon))` for this literal algorithm;
- under an edge budget `m`, the construction gives
  `Omega(min(m, 1 / epsilon) / sqrt(alpha))`;
- if unit outer-loop overhead is counted in addition to active volume, the
  first nonempty call contributes a separate
  `Omega(log(B / alpha^2) / sqrt(alpha))` delay in the small-`alpha` regime.

Proof correction and scope:

- leaf symmetry rigorously forces a full center or leaf-block scan, but it does
  not imply the proposed signed residual cone;
- the unconditional proof instead uses the first nonempty activation to bound
  every later subproblem's slow-mode error, followed by a positive
  Green-function calculation for the critically damped outer recurrence;
- the theorem does not apply to arbitrary AESP inner maps, sequential
  LocAPPR, RPPR, or every hybrid local method, and therefore does not by itself
  close the AESP--LOCSOR publication gate above;
- no polynomially larger AESP-LocGD lower bound is currently proved. A
  multiscale spider, star-of-stars, or clustered lollipop would have to force
  transient explored volume beyond the `O(1 / epsilon)` significant-output
  scale.

## 2026-08-12: black-box tradeoff and composite RPPR extension

The standalone note in `manuscript/notes/hybrid_aesp_locsor/` now includes the
latest parts of the project discussion rather than treating the 2026 RPPR paper
only as structural evidence.

New closed statements:

- for every finite handoff, total work is bounded by Phase-I work plus the
  smaller of the objective-gap and weighted-gradient-mass LOCSOR tails;
- using the direct AESP inner amortization and optimizing the objective handoff
  gives an instance-wise
  `O(R / (alpha^(3/4) * epsilon))` inner-plus-tail bound;
- this Path-I result is unconditional with respect to graph structure,
  confinement, and residual signs, but remains parameterized by the realized
  AESP ratio `R` and excludes uncharged outer initialization work;
- the RPPR unit-step proximal map is a `(1 - alpha)` contraction in
  degree-weighted infinity and one norms;
- its fixed-point residual divided by `alpha` certifies solution error;
- a finite composite Catalyst burn-in followed by full ISTA is therefore
  unconditionally convergent from every handoff.

The three proof paths are now separated explicitly:

1. black-box AESP/SOR balancing: closed and `R`-parameterized;
2. early locality/support confinement: conditionally gives
   `O_tilde(1 / (sqrt(alpha) * epsilon))`;
3. KKT-slack cumulative boundary charging: the abstract charge is proved, but
   a shifted-subproblem margin and a localized inner path-length lemma are
   still missing for AESP.

For RPPR, correctness is no longer the open point. The open point is the
`O_tilde(1 / (rho * sqrt(alpha)))` degree-work theorem from an arbitrary
accelerated warm start. Zero-start support monotonicity cannot be silently
reused after Catalyst overshoot.

## 2026-08-12: rigorous AESP--LOCSOR synthesis

Recorded as a standalone note in
`manuscript/notes/hybrid_aesp_locsor/`. The note reconstructs the project
conversation in a common PageRank normalization and separates source results,
new proofs, conditional statements, empirical observations, corrections, and
open claims.

Closed statements:

- after any finite valid AESP handoff, local SOR with fixed
  `0 < omega < 2` terminates under the final degree-normalized gradient
  certificate;
- with the proof-safe tail `omega = 1`, an objective-gap handoff
  `f(x_J)-f* <= alpha^(3/2) * eps / (1+alpha)` gives tail work
  `O(1/(sqrt(alpha) * eps))`;
- the weighted-gradient-mass handoff
  `||D^(1/2) grad f(x_J)||_1 = O(alpha^(3/2))` gives the same tail order and
  bounds every tail active-set volume;
- the complete hybrid has a trajectory-dependent bound
  `O~(Lambda_J/sqrt(alpha)) + O(1/(sqrt(alpha) * eps))`.

Corrections and open item:

- the universal signed weighted-`l1` monotone SOR range is
  `0 < omega < 1+alpha`, not all of `(0,2)`; objective descent still holds on
  `(0,2)`;
- the graph-uniform target total work follows if the early AESP locality
  factor satisfies `Lambda_J = O(1/eps)`;
- that early-locality statement is not proved for every graph. The note gives
  a support-envelope lemma and an explicit no-percolation condition under
  which it does hold, and explains why the 2026 RPPR/FISTA support results do
  not transfer automatically to unregularized AESP.

The note is intentionally not input by the active manuscript while the
repository-wide residual convention remains open.

### Publication gate

Keep `manuscript/notes/hybrid_aesp_locsor/` as a rigorous standalone research
note; do not promote its graph-uniform end-to-end complexity claim into the
active paper until one of the following is established:

1. the central early-AESP locality lemma
   \[
   \Lambda_J
   := \max_{1\leq t\leq J}
      \frac{\overline{\operatorname{vol}}(S_t)}{\gamma_t}
   = O(1/\epsilon),
   \]
   with a graph-independent hidden constant; or
2. a correct weaker structural condition or alternative burn-in work argument
   that is sufficient for the paper's stated theorem.

Until this gate is closed, paper-facing statements may use the proved
trajectory-dependent theorem and explicitly conditional confinement
corollaries, but must continue to label the universal
`O~(1/(sqrt(alpha) * epsilon))` work bound as open.

The reviewed three-arm RPPR handoff does not close this gate. It proves only
`B_J^full + O(C(S*))` after a fully charged gate-compatible prefix, discards
the prefix's signed numerical energy, and obtains product work only from an
independent theorem bounding `B_J^full`. Its exact-real one-branch response is
therefore a structural composition result, not the missing graph-uniform PPR
or RPPR burn-in bound.

The branch-seeded double-Y now also has a fully charged common-state handoff,
including complete prefix and post-handoff eleven-coordinate vectors and the
external certificate emissions. It proves the same scoped total
`B_J^full + O(C(S*))`, with scalar response before the second branch enters
and fixed SPD rank two afterward. It still does not bound `B_J^full`, retain
signed numerical energy, cover a growing branch core, or imply graph-uniform
continuation. The independent prefix-budget obligation therefore remains and
the publication gate is unchanged.

The fixed-`m` branch caterpillar now closes the next structural handoff only
on its strict canonical range. For `m>=2`, branch seed `s=e_(b_1)`,
`0<alpha<1`, and `rho<rho_can(m,alpha)`, any paid actual canonical checkpoint
converts in one support-only pass to `CaterpillarCanonicalLayerDelta`, without
historical replay. Its total is
`B_J^full + O(C(S*) log(2+C(S*)))`, and product work still requires an
independent theorem for that particular `B_J^full`. The result discards signed
numerical energy and does not cover the remaining canonical range, other
policies, finite precision, PPR conversion, or arbitrary graphs.

One response-native policy now reaches a local actual checkpoint without
promised full-support exposure. In the narrower composite range
`alpha<1/2`, `FirstLayer-BC_1` scans exactly
`Uhat_1={b_1,b_2,a_1,r_1}`, commits one canonical interaction, settles that
face exactly, and retains the native response state. Its prefix vector is
`(9,2,1,0,O(1),0,O(1),O(1),O(1),Theta(1),Theta(1))`; the separately displayed
post vector charges the remaining `m-1` batches and terminal return. The exact
total is `O(C(S*) log(2+C(S*)))`. This closes one local `k=1` RPPR comparator,
not a useful accelerated prefix.

The signed-state interface remains quantitatively different. At checkpoint
`k`, the exact sharp radius is `mu_k=min_v g_(k,v)/beta_(k,v)`. Zero initial
gap is exact and runs zero stages. For positive initial gap, the imported
relative-gap route supplies only the sufficient cap
`T>(2/sqrt(alpha/(1-alpha))) log_+(4 Delta_(k,0)/(alpha mu_k^2))`, while its
relative oracle retains `log(1/(1-2 alpha))`. The earlier constant half-gap
does not imply the required comparison. A future accelerated local splice
must pay this interface or prove a stronger charged one-sided certificate.

Validity and finiteness alone cannot supply the missing prefix theorem. In the
composite range `alpha<1/2`, any reachable pre-gate prefix may be extended by
an arbitrary finite number `N` of valid exact-inner Catalyst stages while the
common canonical checkpoint remains `Uhat_0={b_1}`. Each stage adds at least
one outer-control operation, so the added `C_ctl=Omega(N)`. This is an
algorithm-specification obstruction to the uncapped phrase “any finite valid
burn-in,” not a lower bound for a capped policy.

One capped fixed-family witness does close its own prefix obligation. For the
promised branch caterpillar with `m>=2`, `alpha<1/2`, and `rho<rho_can`,
`Full-BC-AESP_0` pays a complete traversal and uses the strict-range support
theorem to certify the full envelope `U=V=S*`. It then runs exactly
`T_*=ceil(2 log(4)/sqrt(alpha/(1-alpha)))` relative-accuracy AESP-CD stages,
invokes no canonical gate, and hands off at the unchanged checkpoint `k=0`.
Its full prefix vector is
`(O(D_*),O(D_*),0,O(C_*),O(H_*),O(D_*),0,O(C_*),O(C_*),O(D_*),0)`, and the
authoritative bound is `B_env^full=O(H_*)`. The separately charged response
returns exact output with total `O(H_*+C_* log(2+C_*))`. The soft product
notation hides `log(1/(1-2 alpha))` and is not uniform as `alpha` approaches
`1/2`. The proved half-gap is discarded at handoff. This is a
full-realized-support, promised-family, zero-checkpoint witness, not adaptive
locality, a general prefix theorem, graph-uniform continuation, finite
precision, or PPR accuracy. It therefore leaves the publication gate
unchanged while adding a precise positive comparator.

## 2026-08-02: APPR worst-case work is `Theta(1/(alpha * eps))`

Recorded in `manuscript/sections/appr_lower_bound.tex`. The classical ACL
upper bound `O(1/(alpha * eps))` is worst-case tight, witnessed by the
center-seeded star `K_{1,m}` with `m = floor(1/(8 * eps_appr))`, for every
legal active-vertex ordering. This fixes the baseline that the hybrid solver
must beat and identifies the two obstructions to attack:

1. the `1/alpha` factor, from settling only an `alpha`-fraction of pushed
   residual per push;
2. the `1/eps_appr` factor, from repeatedly rescanning a
   `Theta(1/eps_appr)`-degree vertex.

Any hybrid or accelerated method claiming a better worst-case bound must break
at least one of these; a `sqrt(alpha)`-type acceleration attacks (1) only.

Implementation status and open items:

- `src/baselines/appr.py` now provides a controlled reference implementation
  with exact degree-weighted work accounting and four legal active-vertex
  orderings. `tests/test_appr_lower_bound.py` makes the star a regression test
  and cross-checks FIFO output against the Numba kernel after repairing its
  missing self-reactivation queue step. The reproducible diagnostic entry
  point is `uv run python -m experiments.check_appr_lower_bound`; it records
  graph, `alpha`, `eps_appr`, source, random seed, stopping rule, ordering, and
  code version. Its path and long-spider rows are explicitly not theorem
  checks.
- Whether a path or long spider is tight in the coupled regime
  `L = Theta(1/eps)` with `alpha * L^2 = O(1)` is left open; the star needs no
  such coupling.
- The lower-bound checker enforces the theorem regime
  `0 < eps_appr <= 1/16`; out-of-regime values are rejected rather than
  reported as theorem checks. The figure generator validates the complete
  `(alpha, eps_appr, ordering)` grid before plotting actual or scaled work.
- The relation between `eps_appr` and the RPPR sparsity parameter `rho` is
  deliberately not asserted. Both bound support volume, and settling it is a
  prerequisite for a fair APPR-versus-RPPR work comparison.
