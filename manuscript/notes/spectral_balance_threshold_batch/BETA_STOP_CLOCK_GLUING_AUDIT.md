# Beta-stopped input cone: clock gluing and its exact missing synchronization

Date: 2026-09-04

This is an unregistered companion audit.  It studies only the deterministic
single-source retained-prox chronology with pre-gradient input admission, one
simultaneous active diagonal push, and maximal append-with-immediate-push
closure.  It does not update the shared integration summary.

## Verdict

The proposed repair

```text
stop a shifted phase as soon as inner_width <= beta * old_width,
for one fixed beta < 1/2,
```

is not proved for any universal `beta`.  The exact canonical witnesses in
`STOPPED_MASKED_INPUT_RESIDUAL_BETA_CELL_ATLAS.md`, including the structured
double- and triple-clock grafts and an edge-retimed extension, now
give a finite positive-root cover through

```text
0 < beta < 0.4897917473484638....
```

Exact eight- through twenty-two-leaf zero-root audits independently
corroborate the finite leaf-ladder mechanism.  The final E22 zero-root cell
extends slightly beyond the last finite row.

Thus any surviving universal threshold would have to lie in
`[0.4897917473484638...,1/2)`.  The present construction does not prove or
disprove the existence of a threshold in that remaining interval.

Three exact structural conclusions are proved here.

1. A canonical two-vertex first-product clock has residual-width ratio
   tending to `1/2` as the retained root and source threshold tend to zero.
2. A dormant `k`-leaf star released by one input-residual crossing leaves a
   rigorously quantified residual packet whose ratio also tends to `1/2`
   under explicit local conditions.
3. Replicated source wedges give a rigorous way to make the feedback of a
   clock branch vanish while its pointwise normalized residual stays order
   one.  This same fact explains why naive perturbative gluing is invalid:
   the max-residual stopping schedule can change at order one even when the
   clock's feedback into the source is `o(1)`.

Together these reduce a counterexample for every fixed `beta<1/2` to one
precise open synchronization statement: release a fresh star clock one
product before a strict input-cone failure, while keeping every earlier clock
residual below the core's strict stopping margins.  No canonical construction
of that synchronization is asserted here.

There is also a finite exact relay of structured clock witnesses.  Its last
thirty-one chronology cells are

```text
double: [0.4479198414314383..., 0.4589730192979452...),
triple: [0.45836356321468646...,0.46201574441162896...),
retimed: [0.45884213201521634...,0.4661958263074981...),
rho-retimed: [0.4609588674518746...,0.4703618507638715...).
beta-0.473: [0.4646822972411101...,0.4735482533062691...).
beta-0.477: [0.4666344039005332...,0.47705539637312866...).
beta-0.478: [0.4744989324730002...,0.4784561594666679...).
beta-0.48: [0.47690551924253965...,0.4812222006674521...).
beta-0.482: [0.47872710640348143...,0.4829077331583215...).
beta-0.484: [0.48279941351905725...,0.4841421563464968...).
beta-0.4845: [0.481398830294878...,0.4845459054785884...).
beta-0.4847: [0.48454563245614596...,0.48534205790336427...).
beta-0.485: [0.4848047623241312...,0.48593238121846255...).
beta-0.486: [0.485054219345981...,0.48613378881118563...).
clock-swap: [0.48576853645024953...,0.486397917190983...).
clock-rewire: [0.4863082635746538...,0.48646664846402143...).
branch-boundary: [0.48639969150013823...,0.48650854880991756...).
boundary-retimed: [0.4864956188167256...,0.48658118062184946...).
two-leaf: [0.4861893592528099...,0.4870256869778903...).
four-leaf: [0.4868820271518755...,0.48767016032436117...).
six-leaf: [0.48729045390469944...,0.48820216764353663...).
eight-entry: [0.48806839433893695...,0.4884019576618608...).
eight-middle: [0.48824932214123595...,0.4885632177154518...).
eight-extension: [0.4883929965053578...,0.48868006133662073...).
twelve-leaf: [0.4886718252465223...,0.4888994588075898...).
fourteen-entry: [0.48889773743687115...,0.48898059857589404...).
fourteen-extension: [0.4889577783804475...,0.48903788718422087...).
sixteen-leaf: [0.48897261203974246...,0.4891365074011953...).
eighteen-leaf: [0.48846738177898996...,0.4893806599606024...).
twenty-leaf: [0.48907818585092405...,0.4895138464285235...).
twenty-two-leaf equioscillation: [0.48869803978352204...,0.48979117875734753...).
```

These are proved cells, not evidence for smaller beta by monotonicity.  Their
overlap with each other and with the independently Fraction-verified atlas is
what proves the finite continuous cover through
`0.48979117875734753...`.  The audited E18, E20, and E22 limiting families
independently corroborate the mechanism, with the E22 zero-root endpoint
`0.4897917473484638...` just beyond the finite endpoint.  The remaining target
is the interval from that open endpoint to `1/2`.

## Exact double-clock graft

**Proved here.**  Start with the 24-vertex edge set in
`STOPPED_MASKED_INPUT_RESIDUAL_ONE_THIRD_COUNTEREXAMPLE.md` and add

```text
(2,24), (24,25), (7,26).
```

Equivalently, on vertices `0,...,26` the complete edge set is

```text
{
  (0,1), (0,12), (1,2), (1,6), (1,11), (2,3), (2,4),
  (2,5), (2,8), (2,10), (2,11), (2,24), (3,4), (3,5),
  (4,5), (4,6), (4,8), (5,6), (5,9), (6,7), (7,8),
  (7,26), (8,9), (8,10), (9,10), (10,11), (12,13),
  (13,14), (13,17), (13,18), (14,15), (15,16), (15,17),
  (15,20), (16,17), (16,20), (17,18), (18,19), (18,20),
  (18,22), (18,23), (19,20), (20,21), (20,23), (21,22),
  (22,23), (24,25)
}.
```

Take

```text
s=1/224,              alpha=1/100351,
d_source rho=11/500,  rho=11/1000,
relative width=1/1000, beta=9/20.
```

At one-based phase `19`, product `8`, the already active failure row `16`
has

```text
xi_16/old_width=-4.14393151046928...e-8 < 0.
```

The preceding ratio is `0.4611320804565953...>9/20`.  Intersecting every
earlier weak stop comparison and strict continuation comparison gives the
exact half-open cell

```text
[0.4479198414314383..., 0.4589730192979452...).
```

The lower endpoint is attained at phase `18`, product `1`; the upper endpoint
is attained at phase `19`, product `3`.  The failure phase's seven completed
products have residual maxima

```text
product:   1       2       3       4       5       6       7
ratio:   .46691  .46479  .45897  .46433  .47314  .47114  .46113
row:        9      26      26      25      25      25      25
```

Thus the original branch supplies the first clock, the leaf at `26` covers
the early dip, and the delayed endpoint `25` covers the late products while
the disjoint branch fails at row `16`.  The Fraction-exact verifier
`beta_stopped_input_cone_double_clock_exact.py` asserts the graph, failure,
cell equality, endpoint-attaining products, and complete maximum-row sequence.

## Exact triple-clock extension

**Independently replayed here.**  Add one more leaf `(2,27)` to the preceding
double-clock graph, and take

```text
s=1/224,              alpha=1/100351,
d_source rho=21/1000, rho=21/2000,
relative width=1/1000, beta=23/50.
```

The same remote row `16` has its first negative active input residual at
one-based phase `19`, product `8`.  Its predecessor ratio is
`0.46663673977815245...`, and the full exact chronology cell is

```text
[0.45836356321468646...,0.46201574441162896...).
```

The endpoints occur at phase `18`, product `1` and phase `19`, product `3`.
The failure phase maximum rows are

```text
26, 26, 26, 25, 25, 25, 25,
```

so the single-leaf clock carries the first three products and the delayed
two-edge clock carries the final four.  The Fraction-exact wrapper
`stopped_masked_input_residual_triple_clock_counterexample_exact.py` asserts
the graph, failure, endpoint-attaining products, maximum-row relay, and exact
agreement with the general tracer's chronology-cell field.

## Exact edge-retimed extension

**Independently replayed here.**  Starting from the 27-vertex double-clock
edge set, add chord `(3,8)` and delete edges `(16,20)` and `(21,22)`.  The
result is still a finite simple connected undirected unit graph.  Take

```text
s=1/224,                alpha=1/100351,
d_source rho=109/5000,  rho=109/10000,
relative width=1/1000,  beta=23/50.
```

The exact run first violates the input cone at row `16`, one-based phase
`22`, product `7`, after `27` completed products.  The input batch is empty,
and

```text
xi_16/old_width=-2.8575496720229401...e-8,
preceding width/old_width=0.4839445758158437....
```

The complete exact chronology cell is

```text
[0.45884213201521634...,0.4661958263074981...).
```

The lower endpoint occurs at phase `21`, product `1`; the upper endpoint at
phase `22`, product `3`.  The six completed products in the failure phase
have maximum rows

```text
26, 26, 26, 25, 25, 25
```

and width ratios

```text
.4776226, .4733420, .4661958, .4731186, .4842652, .4839446.
```

The `NEAR_HALF_*` block of
`stopped_masked_input_residual_high_beta_counterexample_exact.py` asserts
the exact failure and cell overlap; direct exact recomputation identifies the
endpoint-attaining products and clock relay.

The same topology admits a stronger exact cell after changing only the scalar
threshold to

```text
d_source rho=21509/1000000,  rho=21509/2000000,
beta=47/100.
```

This run fails at phase `21`, product `7`, row `16`, after `26` completed
products, with

```text
xi_16/old_width=-3.77703407800628...e-9,
preceding width/old_width=0.4711665774508539....
```

Its exact cell is

```text
[0.4609588674518746...,0.4703618507638715...).
```

The endpoints occur at phase `20`, product `1` and phase `21`, product `3`.
In the failure phase the first clock supplies ratios `.4784477`, `.4751671`,
`.4703619`, followed by the delayed clock at `.4719187`, `.4746035`, and
`.4711666`.  This one-parameter retiming is important: the topology need not
change to move the chronology cell, but the third-product dip remains the
present finite bottleneck.

A further 27-vertex, 50-edge retiming is exported as `BETA_0473_EDGES` in the
same exact wrapper.  With

```text
d_source rho=393/20000,  rho=393/40000,
beta=473/1000,
```

it fails at phase `21`, product `8`, row `16`, after `27` completed products.
The active input batch is empty and

```text
xi_16/old_width=-5.420669446553434...e-8,
preceding width/old_width=0.4738287015513679...,
same-chronology cell=
[0.4646822972411101...,0.4735482533062691...).
```

This cell overlaps the rho-retimed one and rigorously refutes
`beta=473/1000`.  Its detailed maximum-row relay and endpoint-attaining
products are best read from the Fraction trace; the present finite upper
endpoint remains strictly below `1/2`.

The 27-vertex, 54-edge graph exported as `BETA_0477_EDGES` uses
`d_source rho=187/10000` and `beta=477/1000`.  It fails at phase `25`,
product `8`, row `15`, after `31` completed products, with an empty active
input batch and

```text
xi_15/old_width=-8.126468540210927...e-9,
same-chronology cell=
[0.4666344039005332...,0.47705539637312866...).
```

This cell directly overlaps the beta-0.473 cell and advances the exact finite
relay past `beta=0.477`.

Adding the single edge `(18,21)` to `BETA_0477_EDGES` gives the 55-edge graph
`BETA_0478_EDGES`, with the same root, source threshold, and representative
beta.  The exact failure remains at phase `25`, product `8`, row `15`, but
the cell advances to

```text
[0.4744989324730002...,0.4784561594666679...).
```

The failure-phase width ratios and maximum rows are

```text
product:  1        2        3        4        5        6        7
ratio:   .486146  .483495  .479762  .483012  .487140  .485162  .478456
row:       26       26       26       25       25       25       25
```

Thus product `7` at the delayed endpoint `25` is the exact current bottleneck;
product `3` at the early leaf `26` is next.  Direct pendant additions at
vertices `25` or `26` changed an earlier outer stop and removed the failure.
The successful move instead retimes the still partly dormant failure branch:
vertex `21` is outside the certified face at the failing phase start, while
the new edge changes the active boundary degree at vertex `18`.  Numerically,
the clock residual numerator actually decreases; the ratios rise because the
phase width decreases more.  This is a phase-synchronization effect, not a
free extra residual packet.

The independent 59-edge graph in
`stopped_masked_input_residual_beta_048_counterexample_exact.py` retimes the
same relay once more.  At `d_source rho=171/10000` and `beta=12/25`, its
failure remains product `8`, row `15`, and its exact cell is

```text
[0.47690551924253965...,0.4812222006674521...).
```

The failure-phase maximum rows again are `26,26,26,25,25,25,25`; the exact
ratios are `.4874557,.4849087,.4813478,.4847608,.4891352,.4875039,.4812222`.
Thus product `7` is still the exact bottleneck, with product `3` only
`0.00012557...` higher.  This confirms that the finite search is converging
to a two-point minimax synchronization of the early and delayed clocks.

The 62-edge retiming in
`stopped_masked_input_residual_beta_0482_retimed_exact.py` adds clock-branch
chords `(3,9)` and `(4,9)` and the dormant-edge admission shield `(20,22)` to
the beta-`0.48` graph.  At `d_source rho=162618685/10000000000`, its exact
cell is

```text
[0.47872710640348143...,0.4829077331583215...).
```

The same phase-`23` two-clock relay is now

```text
product:  1        2        3        4        5        6        7
ratio:   .488413  .486154  .482907  .486160  .490382  .488869  .482908
row:       26       26       26       25       25       25       25
```

Product `3` is the cell upper endpoint, only `1.83e-9` below product `7`.
Vertices `20` and `22` are never admitted in this prefix; nevertheless their
edge changes their outside residuals and prevents an admission-history
change.  Deleting that edge does not preserve the failure.  The next finite
search target is therefore sharply two-sided: raise the early row-`26`
product `3` without lowering the delayed row-`25` product `7`.

The next exact retiming adds `(8,11)`.  At the original root it already gives
the diagnostic cell

```text
[0.47865117954737074...,0.4830073888985141...),
```

with product `3` still the bottleneck and product `7` equal to
`0.48310614849913197...`.  More importantly, keeping that edge and decreasing
the retained root to `s=1/1792`, with
`d_source rho=1592357/100000000`, moves the strict failure to phase 24 and
gives

```text
[0.48279941351905725...,0.4841421563464968...).
```

Here the upper endpoint has switched to product `7`, row `25`.  Thus root
scaling is a genuine third retiming parameter in addition to graph edges and
`rho`; on this fixed topology it passes through the same product-3/product-7
equioscillation bottleneck.  The exact certificate is
`stopped_masked_input_residual_beta_0484_counterexample_exact.py`.

Adding `(3,6)` and retiming to `s=1/672`,
`d_source rho=313/20000`, gives the wider bridge cell

```text
[0.481398830294878...,0.4845459054785884...).
```

It has the same failure-phase clock relay.  Product `7`, row `25`, is the
upper endpoint `0.4845459054785884...`, while product `3`, row `26`, is
`0.4846255603238848...`.  Its exact certificate is
`stopped_masked_input_residual_beta_04845_bridge_exact.py`.

A separate 64-edge graph makes the root dependence especially explicit.  On
the same topology, three exact parameter triples yield the overlapping cells

```text
s=1/240, beta=.4847: [0.48454563245614596...,0.48534205790336427...),
s=1/320, beta=.485:  [0.4848047623241312..., 0.48593238121846255...),
s=1/4096, beta=.486: [0.485054219345981..., 0.48613378881118563...).
```

The relay is not a monotonicity inference: all three full histories are
replayed exactly.  Their common wrapper is
`stopped_masked_input_residual_beta_0486_relay_exact.py`.

Finally, replacing clock-side edge `(5,8)` by `(4,10)` and rho-retiming at
`s=1/896` yields

```text
[0.48576853645024953...,0.486397917190983...).
```

Its upper endpoint is product `3`, row `26`, with product `7`, row `25`, only
`7.46e-9` larger.  This is an exact degree-preserving clock-side change; see
`stopped_masked_input_residual_beta_0486_clock_swap_exact.py`.

Replacing `(4,8)` by `(3,5)` on the swap graph and rho-retiming at
`s=1/4096` yields the next overlapping cell

```text
[0.4863082635746538...,0.48646664846402143...).
```

The product-3/product-7 gap is only `2.14e-9`; see
`stopped_masked_input_residual_beta_04864_clock_rewire_exact.py`.

Replacing `(1,11)` by `(1,4)` and choosing rho immediately above a prior-phase
stop boundary gives

```text
[0.48639969150013823...,0.48650854880991756...).
```

Here product `3`, row `26`, is the upper endpoint, while product `7` is much
larger (`0.48664161157750385...`).  The constrained optimum is therefore at a
chronology boundary rather than at p3/p7 equioscillation.  This warns that a
coarse rho grid can miss the useful branch entirely; see
`stopped_masked_input_residual_beta_04865_branch_boundary_exact.py`.

Retiming the same boundary graph to `s=1/262144` and
`rho_scale=756368731/50000000000` gives the overlapping positive-root
extension

```text
[0.4864956188167256...,0.48658118062184946...).
```

The two-case exact overlap certificate is
`stopped_masked_input_residual_beta_04865_branch_boundary_retimed_exact.py`.

The same fixed boundary topology has a stronger exact scaled `s=0` cell at
`rho_scale=756368559/50000000000`:

```text
[0.48649576806397526...,0.48658126877289976...).
```

It fails strictly at phase 25, product 8, row 14.  The exact comparison audit
finds no exterior-input, closure, pre-push, maximum-row, or stop tie.  The 39
zero comparisons are three copies of 13 structurally forced coordinates:
closure diagonal cancellation, next-phase active-input inheritance, and the
corresponding zero raw velocity.  At a small positive root, if an inherited
active zero turns negative then failure occurs earlier; otherwise continuity
of the max/clamp recurrence carries the state to the strict limiting failure.
Consequently every beta strictly inside this limit cell has a positive-root
counterexample.  The topology and rho stay fixed, while the sufficiently
small positive root `s=s(beta)` may depend on beta.  Together with the
then-current finite atlas, this gives the intermediate bound
`0<beta<0.48658126877289976...`.  See
`STOPPED_MASKED_INPUT_RESIDUAL_BETA_04858_ZERO_ROOT_LIMIT.md` and
`stopped_masked_input_residual_beta_04858_zero_root_limit_audit_exact.py`.

The next construction shows that pendant leaves can move both the failure
row and the limiting clock.  Add `(4,27)` and `(15,28)` to the boundary graph.
At `s=1/65536`, an exact rho retiming gives the positive-root cell

```text
[0.4861893592528099...,0.4870256869778903...),
```

with a strict phase-24, product-8 failure at new leaf `28`.  See
`STOPPED_MASKED_INPUT_RESIDUAL_BETA_048659_TWO_LEAF.md`.

Adding two more leaves, `(2,29)` and `(13,30)`, and taking the exactly audited
scaled zero-root limit at `rho_scale=7053/500000` gives

```text
[0.48688202715538775...,0.4876701546689488...).
```

The lower endpoint overlaps the finite two-leaf cell.  The exact comparison
ledger has no exterior-admission, closure, pre-push, maximum-row, or stop tie;
every equality is a structurally forced closure cancellation or its
next-phase active/raw-velocity/clamp inheritance.  The same
earlier-failure-or-continuity argument therefore lifts every beta strictly
inside the limiting cell to a positive-root counterexample, with `s=s(beta)`.
This establishes the intermediate bound `0<beta<0.4876701546689488...`; see
`STOPPED_MASKED_INPUT_RESIDUAL_BETA_04877_FOUR_LEAF_ZERO_ROOT_LIMIT.md` and
`stopped_masked_input_residual_beta_04877_four_leaf_zero_root_limit_audit_exact.py`.

The exact positive-root ladder continues.  Adding `(4,31)` and `(21,32)`
gives the six-leaf cell

```text
[0.48729045390469944...,0.48820216764353663...),
```

and then adding `(1,33)` and `(23,34)` gives an eight-leaf topology.  At
`s=1/4096`, three exact rho retimings on that fixed graph give

```text
[0.48806839433893695...,0.4884019576618608...),
[0.48824932214123595...,0.4885632177154518...),
[0.4883929965053578...,0.48868006133662073...).
```

The corresponding exactly audited scaled zero-root rho relay is

```text
[0.4880686430540822...,0.4884011060182894...),
[0.48824956947231757...,0.4885623702605307...),
[0.4883941377364695...,0.488691166865773...).
```

Its forced closure/inheritance equalities and automorphic twin-leaf maximum
ties satisfy the same earlier-failure-or-continuity hypotheses.  The upper
endpoint remains open and the sufficiently small positive root may depend on
beta.  This establishes the intermediate bound
`0<beta<0.488691166865773...`; see
`STOPPED_MASKED_INPUT_RESIDUAL_BETA_04882_SIX_LEAF.md` and
`STOPPED_MASKED_INPUT_RESIDUAL_BETA_04885_EIGHT_LEAF.md`.

The present ten-leaf parent pair does not improve the E8 fixed-branch
optimum, but adding one more pair at parents `1` and `19` produces a
39-vertex twelve-leaf topology.  At `s=1/4096` it has the exact finite cell

```text
[0.4886718252465223...,0.4888994588075898...),
```

with a strict phase-27, product-8 failure at leaf `28`.  Its exactly audited
zero-root cell is
`[0.4886720900294752...,0.48889876186669784...)`.  The latter corroborates
the forced-tie/continuity mechanism, while the finite cell is slightly
stronger and establishes the current bound
`0<beta<0.4888994588075898...`.  Adding leaves `(2,39)` and `(20,40)` gives
a 41-vertex fourteen-leaf topology.  At `s=1/4096`, two exact rho retimings
give the overlapping finite cells

```text
[0.48889773743687115...,0.48898059857589404...),
[0.4889577783804475...,0.48903788718422087...).
```

Their exactly audited zero-root analogues reach `0.489037149172748...`, just
below the stronger finite endpoint.  Hence the current bound is
`0<beta<0.48903788718422087...`.  See
`stopped_masked_input_residual_beta_04890_twelve_leaf_exact.py` and its
zero-root audit wrapper, together with
`stopped_masked_input_residual_beta_04891_fourteen_leaf_exact.py` and its
zero-root relay wrapper.

Adding `(5,41)` and `(22,42)` gives a 43-vertex sixteen-leaf topology with
exact finite cell

```text
[0.48897261203974246...,0.4891365074011953...).
```

It has a strict phase-27, product-8 failure at leaf `28` and overlaps the E14
relay.  Its audited zero-root cell ends at `0.48913580953910807...`, just
below the finite endpoint.  Thus the current bound is
`0<beta<0.4891365074011953...`; see
`stopped_masked_input_residual_beta_04892_sixteen_leaf_exact.py` and its
zero-root audit wrapper.

Adding `(4,43)` and `(17,44)` gives a 45-vertex eighteen-leaf topology with
exact finite cell

```text
[0.48846738177898996...,0.4893806599606024...).
```

The first failure remains phase 27, product 8, at already active leaf `28`,
but its input batch is `[19,22,23]` rather than empty.  This is a qualitative
mechanism change: fresh admissions coexist with the active-row failure and
do not restore the input cone.  Its audited retimed zero-root cell is
`[0.48846739761431895...,0.4893830355111828...)`, slightly exceeding the
finite endpoint.  Thus the E18-stage bound was
`0<beta<0.4893830355111828...`;
see `stopped_masked_input_residual_beta_04894_eighteen_leaf_retimed_exact.py`
and its retimed zero-root audit wrapper.

Adding `(2,45)` and `(18,46)` gives a 47-vertex, 84-edge twenty-leaf topology.
At root `s=1/65536` and `rho_scale=11781/1000000`, its exact finite cell is

```text
[0.48907818585092405...,0.4895138464285235...).
```

It overlaps the E18 cell.  The strict failure occurs in phase 26, product 8,
at already active leaf `28`, and the input batch is empty.  Thus the chronology
returns from E18's simultaneous-admission mechanism to the earlier
already-active empty-input mechanism.  The corresponding zero-root cell is
`[0.48907818669711567...,0.48951378405604035...)`.  Its complete comparison
audit classifies 40 forced equality groups over 27 coordinates plus six
structural twin-maximum ties; every other relevant comparison is strict, with
tightest strict margin about `2.6944e-8`.  It corroborates rather than extends
the slightly stronger positive-root row.  See
`stopped_masked_input_residual_beta_04896_twenty_leaf_exact.py` and
`stopped_masked_input_residual_beta_04896_twenty_leaf_zero_root_limit_audit_exact.py`.

Adding `(5,47)` and `(19,48)` gives a 49-vertex, 86-edge twenty-two-leaf
topology.  At root `s=1/65536` and the exact zero-root product-3/product-7
equioscillation source scale, its exact finite cell is

```text
[0.48869803978352204...,0.48979117875734753...).
```

The strict phase-27, product-8 failure is at active leaf `28` with empty input
batch.  Crucially, product 7 first performs append closure on `{22,23}` and
then continues; its row-25 clock attains the finite open upper endpoint.  On
the zero-root fixed branch, the competing product-3 row-41 clock and this
product-7 clock are linear-fractional in the source scale with a common
denominator.  Equating their numerators gives an exact rational source scale
and the stronger limiting cell
`[0.48869804073544294...,0.4897917473484638...)`.  The equality is between
distinct products and is not an algorithmic tie; all within-product branch
comparisons remain strict or structurally certified.  See
`stopped_masked_input_residual_beta_04898_twenty_two_leaf_equioscillation_exact.py`
and
`stopped_masked_input_residual_beta_04898_twenty_two_leaf_zero_root_equioscillation_exact.py`.

### Pendant-batch quotient recurrence

The leaf ladder has a small exact quotient.  Attach `k_p` symmetric pendant
leaves to a nonsource core row `p`; let its core degree be `d_p^0`, its new
degree `D_p=d_p^0+k_p`, its state `z_p`, and the common leaf state `y_p`.
In the scaled zero-root recurrence their residuals are

```text
R_p   = -rho-z_p/2
        +(sum_(j in N_core(p)) z_j+k_p y_p)/(2D_p),
R_leaf=(z_p-y_p)/2-rho.                         (LeafQuotient)
```

Permutation symmetry of the leaf batch is invariant under gradients,
positive-part velocity clamps, and simultaneous diagonal pushes.  A dormant
batch has `y_p=0`, so it is admitted exactly when `z_p>2rho`.  Its immediate
diagonal push satisfies the exact reset

```text
y_p^+ = y_p+2R_leaf = z_p-2rho,
```

and cancels its own residual at the frozen parent value.  Therefore, on any
fixed comparison branch, the full graph trace reduces to the core plus one
scalar per pendant batch.  Every state and stop ratio is a rational function
of `rho` and the multiplicity coefficients `k_p/(d_p^0+k_p)`.  This is an
exact deterministic recurrence, not a sampling heuristic, and provides a
route to symbolic analysis of a growing leaf family.

There is also an exact obstruction to putting unbounded multiplicity on one
fixed parent.  Write `S_p=sum_(j in N_core(p))z_j`.  If the batch residual is
nonnegative, then `y_p<=z_p-2rho`; simultaneous nonnegativity of the parent
therefore requires

```text
0 <= 2D_p R_p
   <= S_p-d_p^0 z_p-2d_p^0 rho-4k_p rho.         (LeafLoadNecessary)
```

At first dormant admission, where `y_p=0` and `z_p>2rho`, the sharper direct
form is `S_p>4rho(d_p^0+k_p)`.  Hence if the core-neighbor state sum stays
bounded, the allowable multiplicity at a fixed parent is bounded as well.
Repeated leaves are not a free clock amplifier: a family approaching `1/2`
must also grow the feeding core state, distribute leaves over fresh parents,
or alter the admission chronology.

The first-admission clocks and endpoint constraints at representative
zero-root parameters are listed below.  The E8 rows use the earlier central
choice `rho_scale=136261/10000000`; the optimized three-cell relay is stated
above.

| rung/batch | first closure admission | maximum row and ratio after that product |
| --- | --- | --- |
| E2: leaf `27` at `p=4` | phase 3, product 1 | row 0, `0.06768705538...` |
| E2: leaf `28` at `p=15` | phase 9, product 1 | row 12, `0.15173579738...` |
| E4: leaf `30` at `p=13` | phase 1, product 1, closure round 3 | row 0, `0.16784608690...` |
| E4: leaves `27,29` at `p=4,2` | phase 3, product 1 | row 0, `0.06631059228...` |
| E4: leaf `28` at `p=15` | phase 9, product 1 | row 12, `0.16288294177...` |
| E6: leaf `30` at `p=13` | phase 1, product 1, closure round 3 | row 0, `0.16795923189...` |
| E6: leaf `29` at `p=2` | phase 3, product 1 | row 0, `0.06620703999...` |
| E6: twin leaves `27,31` at `p=4` | phase 4, product 1 | row 12, `0.07076933641...` |
| E6: leaf `28` at `p=15` | phase 9, product 1 | row 12, `0.16340902529...` |
| E8: leaves `33,30` at `p=1,13` | phase 1, product 1, closure rounds 2 and 3 | row 0, `0.15975949891...` |
| E8: leaf `29` at `p=2` | phase 3, product 1 | row 0, `0.06611366956...` |
| E8: twin leaves `27,31` at `p=4` | phase 4, product 1 | row 12, `0.07132528221...` |
| E8: leaf `28` at `p=15` | phase 9, product 1 | row 12, `0.17009137758...` |

E2 is essentially equioscillating in its failure phase: product 7, row 25 is
the upper endpoint `0.4870260368530394...`, while product 3, row 26 is only
`2.27e-11` larger.  E4 raises product 3 to the new upper endpoint
`0.4876701546689488...`, but product 7 becomes
`0.4882266791919638...`, leaving slack `0.000556524523015...`.  Thus the next
leaf rung must preferentially raise the product-3/row-26 clock; merely raising
the product-7 branch cannot improve the minimum continued ratio.

That prediction is borne out by E6: product 3, row `26` is
`0.4882161189654068...`, while product 7, row `25` is the limiting upper
endpoint `0.4882140103628501...`, only `2.1086025566...e-6` smaller.  E8 then
raises product 3 to `0.48852701108289587...`; at its base rho, product 7 is
`0.48887148474014525...`.  Rho retiming restores the relay balance and moves
the exact open endpoint to `0.488691166865773...`.

The “paired-leaf” ladder is not pure multiplicity at one parent.  In E6 the
new leaf `31` at parent `4` is admitted together with its twin `27`, while
leaf `32` at parent `21` remains dormant through the failure.  In E8 the new
leaf `33` at parent `1` is admitted in phase 1, whereas leaf `34` at parent
`23` remains dormant.  Thus each rung combines an early active load/degree
perturbation with a late dormant clock-side degree perturbation.  This is why
the one-parent obstruction `(LeafLoadNecessary)` does not by itself bound the
ladder.

### Fixed-branch rho equioscillation

There is an exact deterministic optimization principle behind the retimings.
Fix a zero-root graph, a finite horizon, and every discrete choice in the
trace: admissions, closure batches, clamp arms, maximum rows, and phase-stop
history.  On that branch, induction through the linear gradient, momentum,
and diagonal-push maps shows that every scaled state, velocity, residual, and
phase endpoint is affine in `rho_scale`.  Consequently every width ratio is
linear-fractional in `rho_scale`, with a denominator of fixed positive sign
on the branch.  The open chronology-cell endpoint is the lower envelope of
finitely many such functions.

In particular, two continued products in the same phase have the same old
width denominator.  Equalizing their ratios is therefore one affine equation,
not a nonlinear search.  On the optimized E8 extension branch, exact
equalization of product 3, row `26`, and product 7, row `25` occurs at a
large rational

```text
rho_scale = 0.013620975272999141...,
```

and gives common ratio `0.4886911764288346...`, while the terminal normalized
failure remains `-0.00237119...`.  The smaller rational used by the audited
relay sacrifices only about `9.56e-9` in the endpoint.  This establishes a
local fixed-chronology optimum; it does not rule out a different rho branch
or a new topology with a larger cell.

The same exact calculation diagnoses the presently tested ten-leaf rung,
obtained by adding leaves at parents `4` and `18`.  Its fixed-branch
equioscillation occurs at `rho_scale=0.013341870570450089...` and has common
product-3/product-7 ratio only `0.48865735113656616...`, below the E8 optimum,
while the failure stays strict.  Thus that E10 chronology cannot extend the
current endpoint by rho retiming alone; a useful next rung must change the
parent pair or the discrete chronology.

As a diagnostic only, the exact zero-root tracer on the preceding clock-rewire
graph, before the branch-boundary `(1,11)->(1,4)` change, at
`rho_scale=15143/1000000` gives limiting product-3 and product-7 ratios
`0.4864670065311669...` and `0.48646700838689544...`.  The positive-root
certificate at `s=1/65536` is therefore already within `3.7e-7` of this
fixed-topology minimax limit.  This does not add an atlas row or justify a
zero-root counterexample; it shows that another topology change is needed for
a material improvement.

A systematic zero-root neighborhood audit of that preceding graph reinforces
that diagnosis.  Among
all 1,959 one-delete/one-add moves inside clock vertices
`{1,...,11,24,25,26}` at `beta=.48645` and the limiting rho, the only move
retaining a failure is `(2,24)->(2,25)`, which merely relabels the two-vertex
tail.  A coarser scan of 50,934 graph/rho pairs at `beta=.4865`, with rho in
`[.0149,.0154]`, found no failure.  This is finite search evidence, not a
local-optimality theorem over continuous rho; it rules out the most immediate
single clock-side repair and motivates multi-edge or growing-clock families.

## 1. Normalized recurrence and beta stopping

Use random-walk degree coordinates and divide the shifted operator by its
smoothness constant.  Put

```text
A = a I-delta P,
a=(1+s^2)/2,
delta=(1-s^2)/2,
theta=(1-s)/(1+s).
```

Thus `a+delta=1`, `P` is row stochastic, and the normalized shifted gap is
`s^2`.  If `e=h-Au` is the nonnegative certified lower residual after a
product, its observable inner width is

```text
w=max_i e_i^+ / s^2.
```

For the retained shift, a phase starting with outer width `W` returns the
valid outer width

```text
W^+ = W/2+w.
```

Consequently any fixed `beta<1/2` would retain geometric outer contraction:
stopping at `w<=beta W` gives

```text
W^+ <= (1/2+beta)W.
```

The only issue audited here is whether every product actually executed before
that stop has nonnegative active input residual.

### Finite-prefix small-root continuity

**Conditional lemma.**  Fix a finite unit graph, a finite number of phases
and products, and a source threshold `rho(s)` analytic at `s=0`.  Prescribe a
canonical branch pattern (input admissions, clamp arms, positive-residual
pushes, closure batches, maximum rows, and stop decisions).  If every
non-forced comparison in the `s=0` scaled recurrence is strict, then for all
sufficiently small positive `s` the same branch pattern is followed.  Every
scaled state and every stop ratio is analytic at `s=0`, so the chronology-cell
endpoints have finite limits.

To see the removable limit exactly, use the tracer's unnormalized variables
and write every state as `x=alpha z`, where

```text
alpha=s^2/(2-s^2),
b=(1+3 alpha)/2=(1+s^2)/(2-s^2),
c=(1-alpha)/2=(1-s^2)/(2-s^2),
L=1+alpha=2/(2-s^2).
```

The shifted load has the form `alpha(h+alpha ell)`, and hence every residual
has the form

```text
r = alpha R_s,
R_s = h+alpha ell-(b I-cP)z.
```

Gradient and push updates of `z` divide `R_s` only by `L` and `b`, whose
limits are nonzero.  The apparent singularity is the auxiliary scale
`k=(1-s)/s`.  Eliminate the stored auxiliary after each chosen clamp arm.  If
`u=z+k(z-p)`, `zhat=max(z,ell)`, and `uhat=max(u,ell)`, then

```text
phat = zhat-(uhat-zhat)/k,
1/k = s/(1-s).
```

On either fixed arm `uhat=u` or `uhat=ell`, this is analytic at zero; the
factor `1/k` cancels the only singular term.  The remaining finite sequence
of updates is therefore branchwise analytic.  Finally,

```text
inner_width/W = max R_s^+/(2W),
```

because the unnormalized shifted gap is `2 alpha`.  Strict limiting signs and
maxima persist by continuity, proving the lemma.

**Earlier-failure-or-continuity extension.**  For a counterexample prefix,
strictness is not needed at an active input comparison whose limiting value is
zero.  Along any sequence `s -> 0`, a negative perturbation already proves an
earlier input-cone failure.  Conditional on nonnegativity, the coordinate
remains on the current face and every gradient, lower clamp, and positive-part
velocity update is continuous at zero.  Thus, if all exterior admissions,
positive-residual pushes, closure tests, maximum rows, and stop decisions are
strict, induction gives the dichotomy: either the positive-root run fails
earlier, or it converges through the entire finite prefix and inherits a
strict limiting terminal failure.  This is the form used by the audited
boundary family above.

This gives a precise limitation on root retiming.  On a fixed graph and fixed
finite branch pattern, sending `s` to zero does not automatically send a
bottleneck ratio to `1/2`; it sends it to the value of the explicit limiting
recurrence.  Thus a topology whose limiting minimum continued ratio is
`c<1/2` eventually remains bounded below `1/2`.  Root scaling can cross a
local product-3/product-7 equioscillation point, as the exact relay does, but
a proof up to every `beta<1/2` still needs either a topology family whose
limiting value tends to `1/2` or the dormant-star synchronization lemma.

The companion `retained_prox_input_cone_zero_root_limit_exact.py` evaluates
this limiting recurrence directly with `Fraction`.  It stores the surviving
scaled NAG velocity as `max(current-previous,0)`, which is exactly the limit
of the auxiliary clamp on a fixed strict arm.  On the 64-edge clock-swap graph
at `rho_scale=7569821/500000000`, it returns the same phase-25, product-8,
row-14 strict failure and the exact limiting cell rendered as

```text
[0.4857688439240337...,0.4863966765832388...).
```

The positive-root cell at `s=1/4096` is
`[0.48576853645024953...,0.486397917190983...)`, consistent with convergence
to that rational limit.  As with the lemma, a non-forced zero velocity or a
tied sign/maximum requires higher-order analysis; the limit tracer is a
branchwise exact diagnostic, not a replacement for a positive-root
certificate.

## 2. Exact canonical two-vertex clock

**Proved here.**  Consider one unit edge, source vertex `0`, zero lower state,
source-scale threshold `r=d_0 rho=rho`, and the first shifted phase.  In the
normalized variables the load is

```text
h_0=s^2(1-r)/2,       h_1=-s^2 r/2,
W=1-r.
```

The input face is initially `{0}`.  The gradient step and active diagonal
push set the source lower value to `h_0/a`.  The leaf residual then is

```text
g=-s^2 r/2 + delta h_0/a.
```

It is positive exactly when `r<delta`, because `a+delta=1`.  Maximal closure
therefore appends the leaf and pushes it by `g/a`.  The only remaining
positive residual is the returned source flux `delta g/a`.  Its exact width
ratio is

```text
C_s(r)
 = (delta/a) [delta/(2a)-r/(2(1-r))]
 = delta^2/(2a^2)-delta r/(2a(1-r)).             (TwoVertexClock)
```

Hence

```text
lim_(s->0,r->0) C_s(r)=1/2.
```

This is a canonical point-source, connected, simple, unit-edge calculation.
It is only a first-product clock; it has no input-cone failure and cannot be
silently replayed at an arbitrary later product.

## 3. Exact dormant-star release packet

The first-product restriction can be separated from the clock algebra.  Let
an already certified port `p` have degree `k+1`: one upstream neighbor and
`k` leaf neighbors `c_1,...,c_k`.  Immediately before a product suppose all
leaves are still uncertified and have zero state.  Write the active input
residual at the port as `xi_p>=0`.  Suppose every leaf crosses the input
frontier in this product with the same strict score

```text
xi_c=eta>0.
```

Because a leaf has only neighbor `p`, its raw-current residual after the
gradient is

```text
[(I-A)xi]_c=delta(eta+xi_p).
```

The simultaneous active diagonal push therefore increments each leaf by

```text
pi_c=delta(eta+xi_p)/a.
```

The port's own diagonal residual is cancelled by its push.  The `k` leaf
increments return the following nonnegative off-diagonal flux to the port:

```text
e_p^after
 >= delta/(k+1) sum_(j=1)^k pi_(c_j)
  = [k/(k+1)] [delta^2/a] (eta+xi_p).            (StarClockPacket)
```

Every later append batch contributes only more nonnegative chronological
flux, so the inequality survives maximal closure.  It follows that

```text
w/W
 >= [k/(k+1)] [delta^2/a]
      [(eta+xi_p)/(s^2 W)].                     (StarClockRatio)
```

In particular, if along a family

```text
k -> infinity,
s -> 0,
eta/(s^2 W) -> 0,
xi_p/(s^2 W) -> 1,
```

then the lower bound tends to `1/2`.  Thus, for every fixed `beta<1/2`, these
four strict quantitative conditions make the released star keep the next
product alive.

### Exact release threshold

For an inactive degree-one leaf, its input and lower residuals are

```text
xi_c=-g+delta q_p,
e_c =-g+delta u_p,
g=s^2 r/2
```

in variables obtained by multiplying every degree-coordinate state and width
by `d_source`, with `r=d_source rho`.  (Without this scaling,
`g=s^2 rho/2`.)  Under the input cone, `q_p>=u_p`.  Therefore the exact
delayed-release condition is

```text
q_p^(j) <= g/delta  for every earlier product j,
q_p^(t) >  g/delta  at the trigger product t.    (LeafTrigger)
```

The earlier input inequalities automatically imply `e_c<=0`, so neither the
input frontier nor the post-push append closure publishes the leaves early.
The port itself, however, has degree `k+1`; before release its input residual
is

```text
xi_p=h_p-a q_p+delta q_up/(k+1),                 (PortInput)
```

where `q_up` is its sole nonzero-neighbor contribution.  Equations
`(LeafTrigger)`, `(PortInput)`, and `(StarClockRatio)` are the exact local
constraints that a delayed clock construction must solve.  They expose the
tradeoff: large `k` improves the returned-flux factor but dilutes the upstream
forcing of `p` by `1/(k+1)`.  This is not an impossibility, since later-phase
`q_up/W` can be large, but it prevents treating the clock as a cost-free
leaf attachment.

## 4. Replicated source-wedge continuity lemma

**Proved here.**  Let a rooted core have `q` attachment edges incident to a
common source.  Form a simple unit graph from `m` disjoint copies of the core
by identifying their source vertices, and attach one additional rooted probe
by one source edge.  Then

```text
d_source=m q+1.
```

Take `rho=r/d_source` and scale every degree-coordinate state and every width
by `d_source`.  The original point-source load becomes exactly

```text
source:      alpha(1-r),
nonsource:  -alpha r,
```

independently of `m`.  All nonsource random-walk rows are independent of
`m`.  The source row is the only changing row: every core attachment type has
aggregate weight `m/(mq+1)`, while the probe root has weight `1/(mq+1)`.

Fix a finite number of phases and products and prescribe all strict
input-admission, active-push, append, clamp, and stop comparisons made in that
prefix.  On that branch of the execution tree, every state is obtained from
the preceding state using additions, multiplications, divisions by positive
diagonals, and coordinatewise choices whose winning arguments are fixed.
It is therefore a rational, hence continuous, function of

```text
lambda_m=1/(mq+1).
```

If the limiting `lambda=0` execution has positive margins for all prescribed
branches, a strictly negative input residual in the core, and predecessor
width ratio strictly above `beta`, then the same signs and inequalities hold
for all sufficiently large finite `m`.  Those finite objects are connected
simple unit-weight graphs with one point source.  This is the desired
perturbative lifting lemma, but its premise concerns the **full limiting
execution including the probe's stopping contribution**.

## 5. Why naive branch gluing does not preserve a failure

The source feedback of the probe is `O(lambda_m)`, but its own scaled
pointwise residual is not.  The scaled nonsource load is `-alpha r`, and the
probe receives an order-one scaled source state.  For example, the
two-vertex calculation above has limiting residual-width ratio `C_s(r)`, not
`O(lambda_m)`.

Therefore the full stopping statistic converges to

```text
max{core residual width, probe residual width},
```

not to the core statistic.  If the probe wins that maximum at an earlier
product, the phase ends at a different time.  Momentum then resets at a
different state and every later proximal center changes.  Continuity of the
within-product state map cannot repair this discrete chronology change.

This is exactly visible in the 24-vertex canonical witness: the two branches
meet only at source `0`; the predecessor maximum is at vertex `9` in the
branch through vertex `1`, while the negative input residual is at vertex
`16` in the branch through vertex `12`.  Thus the found counterexample already
uses a clock/failure separation.  Replicating the core while adding a fresh
leaf is not, by itself, a proof of ratios approaching `1/2`, because the leaf
can change earlier stops even as its source feedback vanishes.

## 6. The exact remaining synchronization target

A gluing proof against every fixed `beta<1/2` would follow from a family with
the following strict properties in the `lambda=0` wedge limit.

1. The failure core follows a canonical zero-start prefix and has its first
   negative active input residual at product `t+1` of some phase.
2. Through product `t-1`, every probe residual stays below the core's strict
   max-residual and stop margins, so the probe does not alter the outer
   chronology.
3. At product `t`, `(LeafTrigger)` releases the dormant star and the port
   satisfies `(StarClockRatio)>beta`.
4. The core's negative input residual at product `t+1` remains strict under
   the one-way limiting source history.

The copy-wedge lemma would then lift the limiting construction to a finite
canonical unit graph.  The exact algebra shows that the target is plausible,
and the finite clock relay and its retimed extensions demonstrate the
required branch separation at ratios above `0.48938`.  What is still open is
the simultaneous solution of the trigger, port-input, earlier-stop, and
core-failure inequalities.  Until that synchronization is supplied, the
statement that failure ratios approach `1/2` remains a conjecture rather
than a theorem.

## Reproduction scope

`beta_stopped_input_cone_search.py` is a floating-point falsification aid for
altered beta histories.  The accelerated heuristic evaluator in
`beta_stopped_input_cone_near_half_search.py` now returns the minimum ratio at
every continued product as its ninth field: this is the actual open upper
endpoint of the observed chronology cell.  Search ranking can therefore
optimize the true cell endpoint rather than only the failure predecessor
ratio.  Exact finite-root canonical witnesses must still be replayed with
`retained_prox_input_cone_trace_exact.py`.  The structured wrappers are exact
finite certificates; floating searches do not establish a universal beta or
the limiting gluing premise.  A generic zero-root trace is only a fixed-branch
diagnostic.  The four-leaf family use is stronger because
`stopped_masked_input_residual_beta_04877_four_leaf_zero_root_limit_audit_exact.py`
exhaustively classifies its zero/tied comparisons and verifies the hypotheses
of the earlier-failure-or-continuity extension.  The stronger eight-leaf
relay is audited by
`stopped_masked_input_residual_beta_04885_eight_leaf_zero_root_limit_audit_exact.py`;
its only extra maximum ties are between automorphic twin leaves and do not
change the scalar maximum used by the stop rule.  The twelve-leaf audit
`stopped_masked_input_residual_beta_04890_twelve_leaf_zero_root_limit_audit_exact.py`
provides an independent corroborating comparison ledger just below the
stronger finite twelve-leaf endpoint.  The fourteen-leaf zero-root relay
provides the analogous audit, and the sixteen-leaf zero-root wrapper supplies
the next corroborating audit.  The retimed eighteen-leaf audit
`stopped_masked_input_residual_beta_04894_eighteen_leaf_zero_root_retimed_exact.py`
verifies the new nonempty-input-batch mechanism and supplies the small
extension beyond the old E18 finite endpoint.  The twenty-leaf finite and
zero-root wrappers verify the return to an empty-input failure and the current
E20-stage endpoint.  The twenty-two-leaf wrappers verify the later
product-7 `{22,23}` closure and the current finite and limiting endpoints.
Every finite atlas row still
comes from a separate positive-root Fraction replay.
