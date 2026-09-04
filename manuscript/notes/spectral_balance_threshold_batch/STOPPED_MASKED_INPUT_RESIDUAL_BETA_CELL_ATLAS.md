# Stopped masked input residual: an exact beta-cell atlas

Date: 2026-09-04

This is an unregistered companion theorem.  It combines finitely many exact
canonical traces, with exact zero-root limiting-family audits, only after
accounting for the nonmonotone dependence of the outer chronology on the
stopping constant.

## Verdict

**Every fixed stopping constant**

```text
0 < beta < 0.4897917473484638...
```

**is refuted.**  For each beta in that interval, at least one finite simple
connected undirected unit-weight graph, with a single point source and the
prescribed zero initialization, reaches a strictly negative active masked
input residual before its beta stop.

This is an interval theorem, not an inference from a rising list of
predecessor ratios.  Forty-four Fraction-exact positive-root chronology cells
give a finite cover through `0.48979117875734753...`.  Exactly audited
twenty-two-leaf zero-root equioscillation extends this by a small amount to the
displayed endpoint.  The endpoint is open.  No claim is made here for

```text
0.4897917473484638... <= beta < 1/2.
```

## Why cells, not isolated beta values

For a fixed graph and rational parameters, every completed product before a
failure contributes exactly one beta constraint:

```text
stopped product:    inner_width/old_width <= beta,
continued product: beta < inner_width/old_width.
```

All previous stop decisions, hence the entire outer history leading to the
failure, are identical on the half-open cell

```text
[max ratio at stopped products,
 min ratio at continued products).              (ChronologyCell)
```

Changing beta outside this cell can move a phase endpoint and alter every
later center, so a single predecessor ratio has no monotone implication.

## Exact finite-cell cover and limiting lift

The exact wrapper replays the following cells in the displayed order.  Only
decimal renderings are shown here; it prints and compares their full rational
endpoints.

| Trace | Exact-cell decimal rendering |
| --- | --- |
| 48-edge anchor, first phase | `[0, 0.17722931342278156...)` |
| 48-edge anchor, low chronology | `[0.17722931342278156..., 0.19627983329174967...)` |
| 44-edge base at `beta=1/5` | `[0.19239784137647384..., 0.227826568209582...)` |
| 44-edge base at `beta=6/25` | `[0.227826568209582..., 0.24690525143060324...)` |
| 48-edge anchor at `beta=6/25` | `[0.2369488184693511..., 0.270878279688796...)` |
| 44-edge base at `beta=7/25` | `[0.2665782789729732..., 0.31271501202935376...)` |
| 48-edge anchor at `beta=31/100` | `[0.30432398528876614..., 0.33020840075859764...)` |
| 44-edge one-third trace | `[0.3276043827054206..., 0.37321417563001585...)` |
| 48-edge anchor at `beta=3/8` | `[0.3688605042855399..., 0.3800754993316571...)` |
| 48-edge anchor at `beta=77/200` | `[0.3800754993316571..., 0.41085090892619697...)` |
| 44-edge two-fifths trace | `[0.38928607214283667..., 0.41511071879596256...)` |
| 51-edge bridge | `[0.41484025995950213..., 0.44133838123915387...)` |
| 63-edge dense trace | `[0.4408297580358625..., 0.4533049942090682...)` |
| 27-vertex structured graft | `[0.4479198414314383..., 0.4589730192979452...)` |
| 28-vertex triple-clock graft | `[0.45836356321468646..., 0.46201574441162896...)` |
| 27-vertex edge-retimed graft | `[0.45884213201521634..., 0.4661958263074981...)` |
| Same edge-retimed graph, rho retimed | `[0.4609588674518746..., 0.4703618507638715...)` |
| 27-vertex beta-0.473 graph | `[0.4646822972411101..., 0.4735482533062691...)` |
| 27-vertex beta-0.477 graph | `[0.4666344039005332..., 0.47705539637312866...)` |
| 27-vertex dormant-edge retiming | `[0.4744989324730002..., 0.4784561594666679...)` |
| 27-vertex beta-0.48 graph | `[0.47690551924253965..., 0.4812222006674521...)` |
| 27-vertex beta-0.482 retiming | `[0.47872710640348143..., 0.4829077331583215...)` |
| 27-vertex beta-0.484 small-root retiming | `[0.48279941351905725..., 0.4841421563464968...)` |
| 27-vertex beta-0.4845 bridge | `[0.481398830294878..., 0.4845459054785884...)` |
| 27-vertex beta-0.4847 relay bridge | `[0.48454563245614596..., 0.48534205790336427...)` |
| Same graph at beta 0.485 | `[0.4848047623241312..., 0.48593238121846255...)` |
| Same graph at beta 0.486 | `[0.485054219345981..., 0.48613378881118563...)` |
| 27-vertex beta-0.486 clock swap | `[0.48576853645024953..., 0.486397917190983...)` |
| 27-vertex beta-0.4864 clock rewire | `[0.4863082635746538..., 0.48646664846402143...)` |
| 27-vertex beta-0.4865 branch boundary | `[0.48639969150013823..., 0.48650854880991756...)` |
| Same boundary graph, root/rho retimed | `[0.4864956188167256..., 0.48658118062184946...)` |
| 29-vertex beta-0.487 two-leaf extension | `[0.4861893592528099..., 0.4870256869778903...)` |
| 31-vertex beta-0.4875 four-leaf extension | `[0.4868820271518755..., 0.48767016032436117...)` |
| 33-vertex beta-0.4881 six-leaf extension | `[0.48729045390469944..., 0.48820216764353663...)` |
| 35-vertex eight-leaf relay entry | `[0.48806839433893695..., 0.4884019576618608...)` |
| Same graph, rho-retimed middle | `[0.48824932214123595..., 0.4885632177154518...)` |
| Same graph, rho-retimed extension | `[0.4883929965053578..., 0.48868006133662073...)` |
| 39-vertex beta-0.4889 twelve-leaf extension | `[0.4886718252465223..., 0.4888994588075898...)` |
| 41-vertex fourteen-leaf relay entry | `[0.48889773743687115..., 0.48898059857589404...)` |
| Same graph, rho-retimed extension | `[0.4889577783804475..., 0.48903788718422087...)` |
| 43-vertex beta-0.48905 sixteen-leaf extension | `[0.48897261203974246..., 0.4891365074011953...)` |
| 45-vertex beta-0.48935 eighteen-leaf retiming | `[0.48846738177898996..., 0.4893806599606024...)` |
| 47-vertex beta-0.48935 twenty-leaf extension | `[0.48907818585092405..., 0.4895138464285235...)` |
| 49-vertex beta-0.48979 twenty-two-leaf equioscillation | `[0.48869803978352204..., 0.48979117875734753...)` |

Every lower endpoint after the first is at most the largest preceding upper
endpoint.  The union is therefore the single interval

```text
[0, 0.48979117875734753...).
```

On the final 35-vertex eight-leaf graph, three exact scaled `s=0` retimings
give the overlapping relay

```text
[0.4880686430540822...,0.4884011060182894...),
[0.48824956947231757...,0.4885623702605307...),
[0.4883941377364695...,0.488691166865773...).
```

Each terminal active input residual is strictly negative.  A complete exact
comparison audit finds only structurally forced closure/inheritance
equalities and harmless twin-leaf maximum ties; all stop decisions and all
other relevant comparisons are strict.  For small positive `s`, a negative
perturbation at a forced active zero is already an earlier counterexample;
otherwise continuity carries the run to the strict terminal failure.  Hence
every beta strictly inside the limiting relay has a positive-root
counterexample.  The graph is fixed, while the source threshold and the
sufficiently small positive choice `s=s(beta)`, hence `alpha`, may depend on
the relay cell and on beta; this is not one positive-alpha trace covering the
whole interval.  The limiting relay overlaps the finite cover.  A separate
exact audit on the 39-vertex twelve-leaf topology gives the corroborating
zero-root cell `[0.4886720900294752...,0.48889876186669784...)`, with only
classified structural equalities.  On the 41-vertex fourteen-leaf topology,
two audited zero-root cells overlap through `0.489037149172748...`; its two
positive-root cells are slightly stronger.  Adding `(5,41)` and `(22,42)`
gives a 43-vertex sixteen-leaf graph whose zero-root audit has cell
`[0.48897285683085145...,0.48913580953910807...)`; its positive-root cell
extends slightly farther.  Finally, the 45-vertex eighteen-leaf graph has
retimed positive-root cell shown in the table and the audited zero-root cell
`[0.48846739761431895...,0.4893830355111828...)`.  The latter overlaps the
finite cover and supplies the final small continuity extension.  Its phase-27
failure is the first ladder row with a
nonempty simultaneous input batch, namely `[19,22,23]`; the failing row `28`
was already active, so this is a genuine input-admission/active-failure
interaction rather than the earlier empty-input mechanism.  Its full
comparison audit satisfies the same earlier-failure-or-continuity dichotomy;
for each fixed beta strictly inside its zero-root cell, the sufficiently
small positive `s=s(beta)` may again depend on beta.  Adding `(2,45)` and
`(18,46)` gives a 47-vertex, 84-edge twenty-leaf zero-root family with cell
`[0.48907818669711567...,0.48951378405604035...)`.  Its failure returns to
phase 26, product 8, active leaf `28`, with an empty input batch.  The exact
audit classifies 40 forced groups over 27 coordinates plus six structural
twin-maximum ties; its tightest non-forced margin is
`2.6944...e-8`.  Thus the E20 lift is not an extrapolation from E18's
nonempty-batch mechanism.  At positive root `s=1/65536`, the same topology
and rho have the slightly stronger exact cell
`[0.48907818585092405...,0.4895138464285235...)`, so the final theorem
endpoint is now furnished directly by a finite certificate.  See
`STOPPED_MASKED_INPUT_RESIDUAL_BETA_04885_EIGHT_LEAF.md` and
`stopped_masked_input_residual_beta_04890_twelve_leaf_zero_root_limit_audit_exact.py`,
and `stopped_masked_input_residual_beta_04891_fourteen_leaf_zero_root_relay_exact.py`.
The sixteen-leaf audit is
`stopped_masked_input_residual_beta_04892_sixteen_leaf_zero_root_limit_audit_exact.py`.
The retimed eighteen-leaf audit is
`stopped_masked_input_residual_beta_04894_eighteen_leaf_zero_root_retimed_exact.py`.
The twenty-leaf audit is
`stopped_masked_input_residual_beta_04896_twenty_leaf_zero_root_limit_audit_exact.py`.
The finite twenty-leaf certificate is
`stopped_masked_input_residual_beta_04896_twenty_leaf_exact.py`.

Adding `(5,47)` and `(19,48)` gives the 49-vertex, 86-edge twenty-two-leaf
topology.  Retiming its source scale to the exact fixed-branch
product-3/product-7 equioscillation gives, at root `s=1/65536`, the finite
cell `[0.48869803978352204...,0.48979117875734753...)`.  It overlaps E20 and
extends the finite atlas.  Its phase-27, product-8 failure is again at active
leaf `28` with empty input batch.  Product 7 first performs append closure on
`{22,23}` and then continues; its row-25 leaf clock attains the finite upper
endpoint.  At `s=0`, the row-41 product-3 clock and row-25 product-7 clock
are exactly equioscillated at distinct products.  This is a designed
cross-product equality, not an algorithmic maximum or branch tie.  The full
comparison audit leaves every within-product comparison strict or
structurally certified and gives the stronger limiting cell
`[0.48869804073544294...,0.4897917473484638...)`.  See
`stopped_masked_input_residual_beta_04898_twenty_two_leaf_equioscillation_exact.py`
and
`stopped_masked_input_residual_beta_04898_twenty_two_leaf_zero_root_equioscillation_exact.py`.

The first twenty-two traces use retained root `s=1/224`, hence
`alpha=1/100351`; the final twenty-two use the displayed wrappers' roots
`1/1792`, `1/672`, `1/240`, `1/320`, `1/4096`, `1/16384`, `1/65536`, and
`1/262144`, together with the four-leaf root `1/1048576`.
All use relative terminal width `1/1000`.  Their rational source thresholds
and complete edge sets are imported from the dedicated exact wrappers.

## Exact verification

Run

```bash
uv run python \
  manuscript/notes/spectral_balance_threshold_batch/stopped_masked_input_residual_beta_cell_atlas_exact.py
```

For every row of the table, the wrapper validates the graph, replays the full
canonical one-push-maximal history with `fractions.Fraction`, asserts the
strict negative input residual, reads the general tracer's exact chronology
cell, checks that the representative beta belongs to it, and verifies the
overlap with the already covered interval.  A zero residual is never
published or pushed.

The limiting-family comparison audits are separately replayed by
`stopped_masked_input_residual_beta_04885_eight_leaf_zero_root_limit_audit_exact.py`
and `stopped_masked_input_residual_beta_04890_twelve_leaf_zero_root_limit_audit_exact.py`.
The fourteen-leaf comparison relay is checked by
`stopped_masked_input_residual_beta_04891_fourteen_leaf_zero_root_relay_exact.py`.
The sixteen-leaf comparison audit is checked by
`stopped_masked_input_residual_beta_04892_sixteen_leaf_zero_root_limit_audit_exact.py`.
The retimed eighteen-leaf comparison audit is checked by
`stopped_masked_input_residual_beta_04894_eighteen_leaf_zero_root_retimed_exact.py`.
The twenty-leaf comparison audit is checked by
`stopped_masked_input_residual_beta_04896_twenty_leaf_zero_root_limit_audit_exact.py`.
The twenty-two-leaf comparison audit is checked by
`stopped_masked_input_residual_beta_04898_twenty_two_leaf_zero_root_equioscillation_exact.py`.
They verify all exact strict margins, classify every structurally forced
equality, and certify the hypotheses of the lifting dichotomy.

## Remaining proof target

The constant-stop repair has now been eliminated for every beta below the
displayed endpoint.  The only threshold-only candidates are in

```text
[0.4897917473484638..., 1/2).
```

The exact two-vertex and dormant-star clock calculations show why `1/2` is a
natural limiting barrier, but they do not yet synchronize that clock with a
strict canonical failure.  Closing the route negatively requires extending
the cell cover through the remaining interval or proving a uniform
parametric construction.  A positive completion would require proving
`BetaStoppedMaskedInputResidual` at one fixed beta in this remaining interval.
