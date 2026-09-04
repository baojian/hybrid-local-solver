# Stopped masked input residual: exact high-beta chronology cells

Date: 2026-09-04

This is an unregistered companion result.  It records canonical
single-source, zero-start graphs whose exact chronology cells overlap to
reach finite endpoint `0.4897911787...`.  Exact eight- through twenty-two-leaf
zero-root audits extend the overall open endpoint slightly farther to
`0.4897917473...`.

## Verdict

There are finite simple connected undirected unit-weight graphs on at most 49
vertices and rational PageRank parameters for which the full
one-push-maximal method violates `MaskedInputResidual` for every

```text
beta in [0.41484025995950213..., 0.4897917473484638...).
```

Thirty-two mutually overlapping positive-root exact chronology cells give the
finite part of the interval:

```text
bridge:     [0.41484025995950213..., 0.44133838123915387...),
dense 0.45: [0.4408297580358625...,  0.4533049942090682...),
structured: [0.4479198414314383...,  0.4589730192979452...).
near-half:   [0.45884213201521634..., 0.4661958263074981...).
beta 0.47:   [0.4609588674518746...,  0.4703618507638715...).
beta 0.473:  [0.4646822972411101...,  0.4735482533062691...).
beta 0.477:  [0.4666344039005332...,  0.47705539637312866...).
beta 0.478:  [0.4744989324730002...,  0.4784561594666679...).
beta 0.48:   [0.47690551924253965..., 0.4812222006674521...).
beta 0.482:  [0.47872710640348143..., 0.4829077331583215...).
beta 0.484:  [0.48279941351905725..., 0.4841421563464968...).
beta 0.4845: [0.481398830294878...,   0.4845459054785884...).
beta 0.4847: [0.48454563245614596..., 0.48534205790336427...).
beta 0.485:  [0.4848047623241312...,  0.48593238121846255...).
beta 0.486:  [0.485054219345981...,   0.48613378881118563...).
clock swap:  [0.48576853645024953..., 0.486397917190983...).
clock rewire: [0.4863082635746538...,  0.48646664846402143...).
branch bound: [0.48639969150013823..., 0.48650854880991756...).
bound retime: [0.4864956188167256...,  0.48658118062184946...).
two leaf:     [0.4861893592528099...,  0.4870256869778903...).
four leaf:    [0.4868820271518755...,  0.48767016032436117...).
six leaf:     [0.48729045390469944..., 0.48820216764353663...).
eight entry:  [0.48806839433893695..., 0.4884019576618608...).
eight middle: [0.48824932214123595..., 0.4885632177154518...).
eight extend: [0.4883929965053578...,  0.48868006133662073...).
twelve leaf:  [0.4886718252465223...,  0.4888994588075898...).
14-leaf entry: [0.48889773743687115..., 0.48898059857589404...).
14-leaf extend: [0.4889577783804475..., 0.48903788718422087...).
sixteen leaf: [0.48897261203974246..., 0.4891365074011953...).
eighteen leaf: [0.48846738177898996..., 0.4893806599606024...).
twenty leaf: [0.48907818585092405..., 0.4895138464285235...).
twenty-two leaf: [0.48869803978352204..., 0.48979117875734753...).
```

All thirty-two lead to strict failures.  Each right endpoint is open because
equality would stop a continued product; each left endpoint is closed because
stopping uses `<=`.  Three exact eight-leaf zero-root cells overlap through
`0.488691166865773...`, and the twelve-leaf zero-root audit gives the cell
`[0.4886720900294752...,0.48889876186669784...)`.  These corroborate the
finite-prefix mechanism.  The fourteen-leaf zero-root relay reaches
`0.489037149172748...`, while its final positive-root cell is slightly
stronger and proves the full verdict above directly.
The sixteen-leaf zero-root audit reaches `0.48913580953910807...`, while its
positive-root cell is again slightly stronger.
The retimed eighteen-leaf zero-root audit reaches `0.4893830355111828...`,
slightly beyond its finite endpoint.  The twenty-leaf zero-root audit reaches
`0.48951378405604035...`; its positive-root cell is slightly stronger and
supplies the E20-stage endpoint directly.  The equioscillated twenty-two-leaf
finite cell reaches `0.48979117875734753...`, and its exactly audited
zero-root family extends the overall result to `0.4897917473484638...`.

This interval result is necessary because the trajectory is not monotone in
`beta`: changing the threshold can change an earlier phase endpoint and hence
all later outer centers.  A predecessor ratio above one chosen beta does not
automatically refute every larger beta below that ratio.

## Exact 48-edge anchor instance

Let `V={0,...,23}`, source `v=0`, and

```text
E = {
  (0,1), (0,12), (1,2), (1,6), (1,11), (2,3), (2,4),
  (2,5), (2,6), (2,8), (2,10), (2,11), (3,4), (3,5),
  (3,11), (4,5), (4,6), (4,8), (5,6), (5,7), (5,9),
  (5,10), (6,7), (7,8), (7,11), (8,9), (8,10), (9,10),
  (10,11), (12,13), (13,14), (13,17), (13,18), (14,15),
  (15,16), (15,17), (16,17), (16,20), (17,18), (18,19),
  (18,20), (18,21), (18,22), (18,23), (19,20), (20,21),
  (20,23), (22,23)
}.
```

The source degree is two.  Take

```text
s = 1/224,
alpha = s^2/(2-s^2) = 1/100351,
d_source rho = 201/10000,
rho = 201/20000,
relative terminal width = 1/1000.
```

For a representative rational point inside the cell, use

```text
beta = 221393/500000 = 0.442786.
```

At one-based outer phase 18, product 7, after 23 completed products, the
input batch is empty and the active face is `{0,...,18}`.  The already active
vertex `16` has the exact strict failure

```text
xi_16 / phase_old_width = -1.282876738804886...e-7 < 0.
```

The preceding completed product has width ratio
`0.4427864623679597...`, so the chosen beta requires the failing product.

## Exact chronology cell

Fix the graph and rational parameters above.  First replay at the
representative high beta and collect every successful product before the
failure.  Preserving the same stop decisions is equivalent to

```text
beta >= max{ratio of every stopped product},
beta <  min{ratio of every continued product}.
```

Fraction arithmetic gives

```text
cell lower = 0.42000073390629883...  (phase 17, product 1),
cell upper = 0.4427864623679597...   (phase 18, product 6).
```

The dedicated verifier prints the exact numerator and denominator of both
endpoints and asserts

```text
cell_lower <= 221393/500000 < cell_upper.
```

Because every beta in this half-open cell produces identical prior stop and
continue decisions, it produces the identical negative input at phase 18,
product 7.

A second exact replay at `beta=419/1000` fails at phase 18, product 8, vertex
`15`, with

```text
xi_15 / phase_old_width = -1.4893069372461688...e-7 < 0.
```

Its exact chronology cell is

```text
[0.41853039720816443..., 0.42000073390629883...).
```

The upper endpoint of this middle cell is exactly equal, as a rational
number, to the inclusive lower endpoint of the high cell.  Their union is
therefore the single covered interval stated in the verdict.

For comparison, the earlier 24-vertex witness has exact cells

```text
one-third trace: [0.3276043827054206..., 0.3732141756300159...),
two-fifths trace: [0.3892860721428367..., 0.4151107187959626...).
```

The 48-edge anchor alone does not overlap either earlier cell.  The bridge
instance below closes its upper gap with the two-fifths cell, however.

## Bridge cell

The first additional graph has 24 vertices and 51 edges.  Its full exact edge
list is the constant `BRIDGE_EDGES` in the verifier.  With the same root and
relative width as above, take

```text
d_source rho = 12/625,
rho = 6/625,
beta = 417/1000.
```

The exact trace fails at phase 18, product 7, vertex 16 after 23 completed
products, with empty input batch and

```text
xi_16 / phase_old_width = -6.633971285688295...e-8.
```

Its exact cell is

```text
[0.41484025995950213..., 0.44133838123915387...).
```

The lower endpoint is below the upper endpoint
`0.4151107187959626...` of the earlier two-fifths cell.

## A strict beta=0.45 failure

A denser 24-vertex, 63-edge member of the same two-lobe family is stored as
`DENSE_EDGES` in the verifier.  Take

```text
d_source rho = 77/5000,
rho = 77/10000,
beta = 9/20.
```

The exact trace fails at phase 18, product 8, vertex 14 after 24 completed
products, with empty input batch and

```text
xi_14 / phase_old_width = -3.867802490794967...e-7.
```

Its exact cell is

```text
[0.4408297580358625..., 0.4533049942090682...).
```

Thus `beta=0.45` itself is rigorously refuted, not merely approached by a
predecessor ratio from a different chronology.

## Structured extension

There is also a sparser, more structured 27-vertex witness.  Start with the
44-edge graph in `stopped_masked_input_residual_one_third_counterexample_exact.py`
and add three new vertices and edges

```text
(2,24), (24,25), (7,26).
```

Take

```text
d_source rho = 11/500,
rho = 11/1000,
beta = 9/20.
```

This exact trace fails at phase 19, product 8, vertex 16 after 25 completed
products, again with an empty input batch.  Here

```text
xi_16 / phase_old_width = -4.14393151046928...e-8,
same-chronology cell =
[0.4479198414314383..., 0.4589730192979452...).
```

The cell overlaps the dense cell and extends the right endpoint.

## Near-half extension

Retiming the 27-vertex structured graph gives a strict `beta=0.46` witness.
Starting from `STRUCTURED_EDGES`, add `(3,8)` and delete `(16,20)` and
`(21,22)`.  The resulting graph is still simple and connected and has 46
edges.  Take

```text
d_source rho = 109/5000,
rho = 109/10000,
beta = 23/50.
```

The exact trace fails at phase 22, product 7, vertex 16 after 27 completed
products, with an empty input batch.  It has

```text
xi_16 / phase_old_width = -2.85754967202294...e-8,
preceding width ratio = 0.4839445758158437...,
same-chronology cell =
[0.45884213201521634..., 0.4661958263074981...).
```

The cell overlaps both the structured and independently verified triple-clock
cells.

The same 46-edge graph also has a second rational parameter cell.  Keep the
root and relative width fixed, and take

```text
d_source rho = 21509/1000000,
rho = 21509/2000000,
beta = 47/100.
```

The exact trace fails at phase 21, product 7, vertex 16 after 26 completed
products, with an empty input batch and

```text
xi_16 / phase_old_width = -3.77703407800628...e-9,
same-chronology cell =
[0.4609588674518746..., 0.4703618507638715...).
```

Thus changing only the rational source threshold retimes the same finite graph
and carries the exact cover across `beta=0.47`.

A second 27-vertex graph with 50 edges, exported as `BETA_0473_EDGES`, takes

```text
d_source rho = 393/20000,
rho = 393/40000,
beta = 473/1000.
```

Its exact trace fails at phase 21, product 8, vertex 16 after 27 completed
products.  The input batch is empty, and

```text
xi_16 / phase_old_width = -5.420669446553434...e-8,
same-chronology cell =
[0.4646822972411101..., 0.4735482533062691...).
```

A third 27-vertex graph with 54 edges, exported as `BETA_0477_EDGES`, takes

```text
d_source rho = 187/10000,
rho = 187/20000,
beta = 477/1000.
```

Its exact trace fails at phase 25, product 8, vertex 15 after 31 completed
products.  The input batch is empty, and

```text
xi_15 / phase_old_width = -8.126468540210927...e-9,
same-chronology cell =
[0.4666344039005332..., 0.47705539637312866...).
```

Finally, add the single edge `(18,21)` to `BETA_0477_EDGES`, retaining all
parameters.  The resulting 55-edge graph is exported as `BETA_0478_EDGES`.
Vertex `21` is still outside the certified face at the failing phase start,
so this is a dormant-boundary retiming rather than an extra active clock.
The exact trace again fails at phase 25, product 8, vertex 15 after 31
completed products, with

```text
xi_15 / phase_old_width = -6.63521631786637...e-9,
same-chronology cell =
[0.4744989324730002..., 0.4784561594666679...).
```

The failure-phase maximum rows are `26` for products 1--3 and `25` for
products 4--7.  The cell upper endpoint is the product-7 row-`25` ratio.

A separate 27-vertex, 59-edge graph at `beta=12/25` has the same maximum-row
relay and the exact cell

```text
[0.47690551924253965...,0.4812222006674521...).
```

It fails at phase 22, product 8, row 15.  The graph, parameters, and full
Fraction certificate are in
`STOPPED_MASKED_INPUT_RESIDUAL_BETA_048_COUNTEREXAMPLE.md` and
`stopped_masked_input_residual_beta_048_counterexample_exact.py`.

From that graph, add `(3,9)`, `(4,9)`, and `(20,22)`.  At
`d_source rho=162618685/10000000000` and `beta=241/500`, the resulting 62-edge
graph fails at phase 23, product 8, row 15 and has exact cell

```text
[0.47872710640348143...,0.4829077331583215...).
```

Its standalone Fraction certificate is
`stopped_masked_input_residual_beta_0482_retimed_exact.py`.

Adding `(8,11)`, decreasing the retained root to `s=1/1792`, and taking
`d_source rho=1592357/100000000` gives a 63-edge graph whose `beta=121/250`
trace fails at phase 24, product 8, row 15.  Its exact cell is

```text
[0.48279941351905725...,0.4841421563464968...).
```

The last cell's upper endpoint is attained at product 7 by clock row 25.  Its
standalone certificate is
`stopped_masked_input_residual_beta_0484_counterexample_exact.py`.

Adding `(3,6)` to that graph and retiming to `s=1/672` and
`d_source rho=313/20000` gives the overlapping bridge cell

```text
[0.481398830294878...,0.4845459054785884...).
```

It fails at phase 25, product 8, row 15.  Its exact certificate is
`stopped_masked_input_residual_beta_04845_bridge_exact.py`.

A different 27-vertex, 64-edge graph then supplies three overlapping root/rho
retimings:

```text
s=1/240, beta=.4847: [0.48454563245614596...,0.48534205790336427...),
s=1/320, beta=.485:  [0.4848047623241312..., 0.48593238121846255...),
s=1/4096, beta=.486: [0.485054219345981..., 0.48613378881118563...).
```

Each first fails at phase 25, product 8, after 31 completed products.  Their
shared exact wrapper is
`stopped_masked_input_residual_beta_0486_relay_exact.py`.

Replacing clock-side edge `(5,8)` by `(4,10)` and retiming rho gives one more
overlapping cell

```text
[0.48576853645024953...,0.486397917190983...).
```

It first fails at phase 25, product 8, row 14; see
`stopped_masked_input_residual_beta_0486_clock_swap_exact.py`.

On that graph, replacing `(4,8)` by `(3,5)` and retiming rho produces

```text
[0.4863082635746538...,0.48646664846402143...).
```

It has the same phase-25, product-8, row-14 strict failure; see
`stopped_masked_input_residual_beta_04864_clock_rewire_exact.py`.

Replacing `(1,11)` by `(1,4)` and moving rho just across a prior-phase stop
boundary gives the next overlapping cell

```text
[0.48639969150013823...,0.48650854880991756...).
```

See `stopped_masked_input_residual_beta_04865_branch_boundary_exact.py`.

The same boundary graph at `s=1/262144`,
`d_source rho=756368731/50000000000`, and `beta=973/2000` gives

```text
[0.4864956188167256...,0.48658118062184946...).
```

The two boundary cells are jointly checked by
`stopped_masked_input_residual_beta_04865_branch_boundary_retimed_exact.py`.

Adding pendant leaves `(4,27)` and `(15,28)` to the boundary topology and
retiming at `s=1/65536` gives the next positive-root cell

```text
[0.4861893592528099...,0.4870256869778903...).
```

It fails at phase 24, product 8, at new leaf `28`; see
`STOPPED_MASKED_INPUT_RESIDUAL_BETA_048659_TWO_LEAF.md`.

Successively adding two further leaf pairs gives exact positive-root
four-, six-, and eight-leaf relays.  The final eight-leaf topology uses 35
vertices and 72 edges; at fixed `s=1/4096`, three rho retimings give cells

```text
[0.48806839433893695...,0.4884019576618608...),
[0.48824932214123595...,0.4885632177154518...),
[0.4883929965053578...,0.48868006133662073...).
```

See `STOPPED_MASKED_INPUT_RESIDUAL_BETA_04882_SIX_LEAF.md` and
`STOPPED_MASKED_INPUT_RESIDUAL_BETA_04885_EIGHT_LEAF.md`.

Adding four further leaves at parents `4`, `18`, `1`, and `19` gives a
39-vertex, 76-edge twelve-leaf graph.  At `s=1/4096` and
`d_source rho=6549/500000`, its exact positive-root cell is

```text
[0.4886718252465223...,0.4888994588075898...).
```

It overlaps the last E8 finite cell and is checked by
`stopped_masked_input_residual_beta_04890_twelve_leaf_exact.py`.

Adding `(2,39)` and `(20,40)` gives a 41-vertex, 78-edge fourteen-leaf graph.
Two exact positive-root rho retimings give

```text
[0.48889773743687115...,0.48898059857589404...),
[0.4889577783804475...,0.48903788718422087...).
```

They overlap each other and the E12 row; see
`stopped_masked_input_residual_beta_04891_fourteen_leaf_exact.py`.

Adding `(5,41)` and `(22,42)` gives a 43-vertex, 80-edge sixteen-leaf graph.
Its exact positive-root cell is

```text
[0.48897261203974246...,0.4891365074011953...).
```

It overlaps the E14 relay; see
`stopped_masked_input_residual_beta_04892_sixteen_leaf_exact.py`.

Adding `(4,43)` and `(17,44)` gives a 45-vertex, 82-edge eighteen-leaf graph.
At retimed root `s=1/16384`, its exact positive-root cell is

```text
[0.48846738177898996...,0.4893806599606024...).
```

The failure remains phase 27, product 8, at active leaf `28`, but its input
batch is now `[19,22,23]`, rather than empty.  Thus this row uses a new
mechanism: simultaneous fresh admissions coexist with, but do not repair, the
strict residual failure on an already active row.  See
`stopped_masked_input_residual_beta_04894_eighteen_leaf_retimed_exact.py`.

Adding `(2,45)` and `(18,46)` gives a 47-vertex, 84-edge twenty-leaf graph.
At root `s=1/65536` and `rho_scale=11781/1000000`, its exact positive-root
cell is

```text
[0.48907818585092405...,0.4895138464285235...).
```

It overlaps the E18 finite cell.  The strict failure is phase 26, product 8,
at already active leaf `28`, with empty input batch, so the mechanism returns
from E18's simultaneous-admission case to an already-active empty-input
failure.  See `stopped_masked_input_residual_beta_04896_twenty_leaf_exact.py`.

Adding `(5,47)` and `(19,48)` gives a 49-vertex, 86-edge twenty-two-leaf
graph.  At root `s=1/65536` and the exact zero-root equioscillation source
scale, its exact finite cell is

```text
[0.48869803978352204...,0.48979117875734753...).
```

The strict phase-27, product-8 failure is again at already active leaf `28`
with empty input batch.  Product 7 continues after its append closure admits
and pushes `{22,23}`; its row-25 leaf clock attains the open upper cell
endpoint.  At zero root the competing product-3 row-41 clock is exactly
equal to it.  This is a designed equality between distinct products, not an
algorithmic tie.  Hence this row combines a fresh closure one product earlier
with an empty-input failing product.  See
`stopped_masked_input_residual_beta_04898_twenty_two_leaf_equioscillation_exact.py`.

Combining the two-fifths, bridge, dense, structured, near-half, beta-0.47,
beta-0.473, beta-0.477, beta-0.478, beta-0.48, beta-0.482, beta-0.484,
beta-0.4845, beta-0.4847, beta-0.485, beta-0.486, clock-swap, clock-rewire,
both branch-boundary cells, and the leaf ladder gives the
continuous exact cover

```text
[0.3892860721428367..., 0.48979117875734753...).
```

Together with separately verified lower-beta cells, the atlas companion
extends this finite cover down to zero.  On the eight-leaf topology, three
exact zero-root rho retimings overlap through
`0.488691166865773...`.  Their only equalities are structurally forced
closure/inheritance events and harmless twin-leaf maximum ties.  The
earlier-failure-or-continuous-clamp dichotomy therefore lifts every beta
strictly inside the limiting relay to a positive-root counterexample.  The
twelve-leaf zero-root audit gives the corroborating cell
`[0.4886720900294752...,0.48889876186669784...)`; the finite twelve-leaf row
extends slightly farther.  The exact fourteen-leaf zero-root relay reaches
`0.489037149172748...`, just below the finite endpoint.  See
`STOPPED_MASKED_INPUT_RESIDUAL_BETA_04885_EIGHT_LEAF.md` and the twelve- and
fourteen-leaf audit wrappers.  The sixteen-leaf zero-root audit similarly
reaches `0.48913580953910807...`, just below its finite endpoint.  The
retimed eighteen-leaf audit reaches `0.4893830355111828...` and retains the
nonempty input-batch mechanism, thereby extending the overall theorem beyond
the old E18 finite endpoint.  The twenty-leaf zero-root audit gives cell
`[0.48907818669711567...,0.48951378405604035...)`, with 40 forced equality
groups over 27 coordinates, six structural twin-maximum ties, and no other
tie; its tightest strict margin is about `2.6944e-8`.  It returns to an empty
input batch and robustly corroborates the slightly stronger finite E20 row.
The equioscillated twenty-two-leaf zero-root audit then reaches the slightly
stronger open endpoint `0.4897917473484638...`; it preserves the product-7
`{22,23}` closure followed by the empty-input product-8 failure.  Its two
bottleneck clocks occur at distinct products, while all within-product
comparisons are strict or structurally certified.

The triple-clock construction remains useful
structural evidence and overlaps the near-half cell; see
`STOPPED_MASKED_INPUT_RESIDUAL_TRIPLE_CLOCK_COUNTEREXAMPLE.md`.  Reaching all
the way to `1/2` still needs additional witnesses or a parametric construction.

## Exact verification

Run:

```bash
.venv/bin/python manuscript/notes/spectral_balance_threshold_batch/stopped_masked_input_residual_high_beta_counterexample_exact.py
```

The wrappers invoke the graph validator and execute all thirty-two full canonical
one-push-maximal outer chronologies using `fractions.Fraction` for every
value, publication decision, and stopping comparison.  It independently
recomputes every stop/continue cell, asserts equality with the general
tracer's exact cell field, and checks the graphs, parameters, failures,
endpoint overlaps, and exact adjacency of the two anchor cells.
The separate beta-`0.48`, beta-`0.482`, beta-`0.484`, beta-`0.4845`, and
beta-`0.486` relay, clock-swap, clock-rewire, branch-boundary, and leaf-ladder
wrappers apply the same exact checks to the high-beta cells.  The limiting
audits are independently checked by the eight- through twenty-two-leaf zero-root
wrappers.

## Consequence

The threshold-only repair is now known to fail at `beta=0.45` and on a
substantial contiguous interval around it.  The finite portion remains
cellwise because of beta-dependent outer history; the finite endpoint is a
direct positive-root certificate, and the final small extension comes from
the audited E22 continuity family.  Analytically, a complete negative result
must either cover
`[0.4897917473...,1/2)` by further cells or give a parametric graph family
whose chronology cells approach `1/2`.
