# Paired-leaf ladder: exact finite pattern and missing induction

Date: 2026-09-04

This is an unregistered structural companion for the canonical zero-start,
one-push-maximal stopped masked-input-residual recurrence.  It does not edit
the beta atlas.  It separates the exact E2--E20 certificates from bounded
search evidence and explains why the observed ladder is not yet an induction
to `1/2`.

## The exact ladder

Let `B` be `BETA_04865_BRANCH_BOUNDARY_EDGES`, the 27-vertex simple unit
core.  The successive graphs are

~~~text
E2  = B   + {(4,27),(15,28)}
E4  = E2  + {(2,29),(13,30)}
E6  = E4  + {(4,31),(21,32)}
E8  = E6  + {(1,33),(23,34)}
E10 = E8  + {(4,35),(18,36)}
E12 = E10 + {(1,37),(19,38)}
E14 = E12 + {(2,39),(20,40)}
E16 = E14 + {(5,41),(22,42)}
E18 = E16 + {(4,43),(17,44)}
E20 = E18 + {(2,45),(18,46)}.
~~~

Vertex `19` in the last line may be replaced by its graph twin `22`.
Every displayed graph is connected, simple, undirected, and unit weighted.
The source remains vertex `0`.

The following table uses Fraction-exact zero-root traces.  The E8 row is the
last case of its three-rho relay.  “p3” and “p7” refer to the two competing
continued products in the failure phase.

| graph | rho scale | failure | lower endpoint | upper endpoint | upper row |
|---|---:|---|---:|---:|---|
| E2 | `14701198001/10^12` | ph24/p8/v28 | `.48618996153896166...` | `.4870260368530394...` | p7/v25 |
| E4 | `7053/500000` | ph24/p8/v28 | `.48688202715538775...` | `.4876701546689488...` | p3/v26 |
| E6 | `6943/500000` | ph25/p8/v28 | `.4872906952446029...` | `.4882140103628501...` | p7/v25 |
| E8 | `544839/40000000` | ph26/p8/v28 | `.4883941377364695...` | `.488691166865773...` | p7/v25 |
| E10 | `133419/10000000` | ph26/p8/v28 | `.4880924862240161...` | `.4886562754407511...` | p3/v26 |
| E12 | `26191/2000000` | ph27/p8/v28 | `.4887692904770463...` | `.4889861328877012...` | p3/v26 |
| E14 | `629919/50000000` | ph26/p8/v28 | `.4889579986044299...` | `.4890371491727480...` | p3/v26 |
| E16 | `6243/500000` | ph27/p8/v28 | `.4889728568308515...` | `.4891358095391081...` | p3/v26 |
| E18 | `6120857/500000000` | ph27/p8/v28 | `.4884673976143190...` | `.4893830355111828...` | p3/v26 |
| E20 | `11781/1000000` | ph26/p8/v28 | `.4890781866971157...` | `.4895137840560404...` | p3/v26 |

E10 is deliberately retained in the table although its cell is contained
in the E8 relay.  It is the necessary intermediate topology from which the
E12 extension was found.  Thus endpoint improvement is nonmonotone under a
single paired addition.

The E8 relay has three exact overlapping zero-root cells:

~~~text
rho_scale = 1363/100000:
  [.4880686430540822..., .4884011060182894...)
rho_scale = 109/8000:
  [.4882495694723176..., .4885623702605307...)
rho_scale = 544839/40000000:
  [.4883941377364695..., .488691166865773...).
~~~

The first overlaps E6, and adjacent E8 cells overlap each other.  E12 itself
uses the original cell at `rho_scale=6549/500000` followed by the retimed
cell in the table; their intervals overlap.  The two exact E14 rows are

~~~text
rho_scale = 1260037/100000000:
  [.4888979580659025..., .4889798590424537...)
rho_scale = 629919/50000000:
  [.4889579986044299..., .4890371491727480...).
~~~

The first E14 row overlaps the retimed E12 row, and the two E14 rows overlap
each other.  All upper endpoints are open.

## Admission roles

The leaves do not form a sequence of late one-shot triggers.  Their first
closure admissions in the representative exact traces are:

| graph | first admissions of leaves | dormant through failure |
|---|---|---|
| E2 | `27@ph3`, `28@ph9` | none |
| E4 | `30@ph1`, `27,29@ph3`, `28@ph9` | none |
| E6 | `30@ph1`, `29@ph3`, `27,31@ph4`, `28@ph9` | `32@21` |
| E8 | `30,33@ph1`, `29@ph3`, `27,31@ph4`, `28@ph9` | `32@21`, `34@23` |
| E10 | `30,33@ph1`, `29@ph3`, `27,31,35@ph4`, `36@ph5`, `28@ph9` | `32,34` |
| E12 | `30,33,37@ph1`, `29@ph4`, `27,31,35,36@ph5`, `28@ph9` | `32,34,38` |
| E14 | `30,33,37@ph1`, `29,39@ph4`, `27,31,35,36@ph5`, `28@ph8` | `32,34,38,40` |
| E16 | `30,33,37@ph1`, `27,29,31,35,39@ph4`, `36@ph5`, `28@ph8`, `41@ph14` | `32,34,38,40,42` |
| E18 | `30,33,37@ph1`, `29,39,44@ph4`, `27,31,35,36,43@ph5`, `28@ph9`, `41@ph14` | `32,34,38,40,42` |
| E20 | `30,33,37@ph1`, `29,39,44,45@ph4`, `27,31,35,36,43,46@ph5`, `28@ph8`, `41@ph13` | `32,34,38,40,42` |

Here `leaf@port` in the last column names the attachment port, not an
admission time.  The roles are distinct:

1. Leaf `28` at port `15` is the eventual negative active-input row.
2. Early clock-side leaves change degrees and the phase clock.  Once port
   `4` has multiple twins, leaves `27,31,35` become the maximum row in the
   product-1 lower-endpoint phases.
3. Some failure-side leaves never enter the active face.  They still change
   their parent's degree and therefore retime the failure branch whenever
   that parent is active.  Leaves attached to a parent that itself stays
   inactive are completely inert on the finite prefix.
4. Successful rungs alternately rebalance p3/v26 and p7/v25.  E2, E6, E8,
   and E10 are nearly equioscillating; E4 and E12 leave visible slack in p7.

In particular, “two more leaves” is not a scalar recurrence.  One leaf can
act on the clock branch while the other acts only through a dormant-degree
perturbation on the failure branch.

## Exact quotient formula and a multiplicity obstruction

At zero root, suppose a core port `p` has base degree `d0`, `k` symmetric
degree-one leaves with common state `y`, parent state `z`, and sum `S` of the
states of its core neighbors.  With nonsource load `-rho`, its residuals are

\[
 R_p=-\rho-\frac z2+\frac{S+k y}{2(d_0+k)},
 \qquad
 R_{\rm leaf}=\frac{z-y}{2}-\rho.
\]

Thus a dormant batch is admitted exactly when `z>2 rho`; its diagonal push
sets

\[
 y^+=z-2\rho.
\]

On every fixed comparison branch, the symmetric leaves therefore reduce to
a rational recurrence in `rho` and the quotient coefficient

\[
 \frac{k}{d_0+k}.
\]

This explains why p3--p7 balancing in `rho` can be solved exactly on a fixed
topology.  It does not supply a recurrence between different attachment
ports.

There is also a strict obstruction to unlimited multiplicity at one fixed
parent.  If an active leaf has nonnegative residual, then
`y <= z-2 rho`.  Requiring the parent residual to remain nonnegative gives

\[
 0\le 2(d_0+k)R_p
 \le S-d_0z-2d_0\rho-4k\rho.
\]

For first admission from a dormant batch, `y=0` and `z>2 rho`, so the
stronger necessary condition is

\[
 S>4\rho(d_0+k).
\]

Consequently, repeatedly stacking leaves on a fixed parent cannot be a free
amplifier: unless the feeding core sum `S` grows linearly with `k`, the
admissible multiplicity is bounded.  An infinite near-half family would
need fresh parents, a growing feeding module, or a changed chronology.

## Exact comparison audits

For E12 at

~~~text
rho_scale = 6549/500000,
beta = 12217/25000,
relative_width = 1/1000,
~~~

the full Fraction audit certifies

~~~text
cell       [.4886720900294752..., .4888987618666978...)
failure    phase 27, product 8, vertex 28
input batch at failure = empty
lower      phase 26, product 1, twin leaf 27
upper      phase 27, product 3, row 26
normalized failure residual = -.00257198938271977...
p7 - p3 = .0001867688753673204...
~~~

There are 44 inherited zero/clamp equality groups coming from 11 forced
post-closure groups, involving 22 coordinates per equality kind.  There are
also six maximum ties: twins `33,37` in phases 22--23 and twins `27,31,35`
in phases 24--27.  The audit certifies each maximum tie by identical graph
neighborhoods.  There are no exterior-input zeros, pre-push zeros, closure
test zeros, or stop ties.

The minimum exact strict margins, shown in decimal only for readability,
are

| comparison | margin |
|---|---:|
| active input | `1.2713490735e-6` |
| exterior input | `5.1155461480e-5` |
| closure test | `1.3933998382e-5` |
| pre-push | `5.5862814044e-6` |
| post-closure active | `5.7742503757e-6` |
| lower clamp / raw velocity | `3.3138499452e-5` |
| maximum to next distinct | `1.1719250948e-7` |
| unique maximum | `2.5693672921e-7` |
| stop decision | `7.9099705248e-6` |

The exact zero-root audit is
`stopped_masked_input_residual_beta_04890_twelve_leaf_zero_root_limit_audit_exact.py`.
The stronger same-topology retiming is audited by
`stopped_masked_input_residual_beta_04899_twelve_leaf_zero_root_retimed_exact.py`;
it has cell

~~~text
[.4887692904770463..., .4889861328877012...)
~~~

and normalized failure `-.0023936328511867...`.
The explicit positive-root certificate uses `s=1/4096` and has the exact
finite cell

~~~text
[.4886718252465223..., .4888994588075898...).
~~~

Its phase-27/product-8/vertex-28 normalized failure is strictly negative,
about `-6.462e-11`.  It is checked by
`stopped_masked_input_residual_beta_04890_twelve_leaf_exact.py`.

For E14, both zero-root relay rows pass the same complete audit.  There are
44 inherited zero/clamp groups involving 25 coordinates per equality kind,
plus six structural twin-maximum ties: `33,37` in phases 21--22 and
`27,31,35` in phases 23--26.  The exact zero-root wrapper is
`stopped_masked_input_residual_beta_04891_fourteen_leaf_zero_root_relay_exact.py`.

The explicit `s=1/4096` replay is also strict and gives

~~~text
entry      [.4888977374368712..., .4889805985758940...)
extension  [.4889577783804475..., .4890378871842209...).
~~~

Both failures are phase 26, product 8, vertex 28, with empty input batch.
Their normalized residuals are respectively about `-4.738e-11` and
`-4.084e-11`.  The exact finite wrapper is
`stopped_masked_input_residual_beta_04891_fourteen_leaf_exact.py`.

E16 has zero-root cell

~~~text
[.4889728568308515..., .4891358095391081...)
~~~

and a normalized limiting failure `-.00493636918556...`.  Its 40 inherited
zero/clamp groups involve 23 coordinates per kind.  Five maximum ties are
again certified by graph twins.  The complete audit is
`stopped_masked_input_residual_beta_04892_sixteen_leaf_zero_root_limit_audit_exact.py`.
At `s=1/4096`, the exact finite cell is slightly stronger,

~~~text
[.4889726120397425..., .4891365074011953...),
~~~

with normalized failure about `-1.354e-10`; see
`stopped_masked_input_residual_beta_04892_sixteen_leaf_exact.py`.

E18 introduces a qualitatively new strict failure: at phase 27, product 8,
rows `19,22,23` are newly admitted by the input test, while the already
active leaf `28` has negative input residual.  Thus its input batch is
nonempty but the same product still strictly fails before its candidate
update is executed.  The original exact zero row is audited by
`stopped_masked_input_residual_beta_04894_eighteen_leaf_zero_root_limit_audit_exact.py`.
The stronger rho retiming is audited by
`stopped_masked_input_residual_beta_04894_eighteen_leaf_zero_root_retimed_exact.py`
and has cell

~~~text
[.4884673976143190..., .4893830355111828...).
~~~

Its p3 and p7 upper constraints differ by only `1.9852e-8`.  The explicit
finite certificates are
`stopped_masked_input_residual_beta_04894_eighteen_leaf_exact.py` and
`stopped_masked_input_residual_beta_04894_eighteen_leaf_retimed_exact.py`.
The latter uses `s=1/16384` and gives

~~~text
[.4884673817789900..., .4893806599606024...)
~~~

with normalized failure about `-6.10e-12`; at this positive root p7/v25,
rather than p3/v26, is the upper endpoint.

E20 returns to an empty failure input batch.  Its complete zero-root audit is
`stopped_masked_input_residual_beta_04896_twenty_leaf_zero_root_limit_audit_exact.py`.
At `rho_scale=11781/1000000` and `beta=9787/20000`, it certifies

~~~text
cell       [.4890781866971157..., .4895137840560404...)
failure    phase 26, product 8, vertex 28
input batch at failure = empty
lower      phase 25, product 1, twin leaf 27
upper      phase 26, product 3, row 26
normalized failure residual = -4.545169895e-5...
~~~

The audit has 40 forced zero/clamp groups involving 27 coordinates per
equality kind and six structural maximum-tie certificates.  It finds no
unclassified equality.  Direct exact checks at `s=1/4096` and `s=1/16384`
are passes rather than counterexamples; this is consistent with the small
limiting failure margin and is not an obstruction to lifting the strict
zero-root branch.  At `s=1/65536`, the exact finite replay is a strict
counterexample with cell

~~~text
[.4890781858509241..., .4895138464285235...)
~~~

and normalized failure about `-2.0741e-15`.  It has the same phase-26,
product-8, vertex-28 failure and empty input batch.  The exact finite wrapper
is `stopped_masked_input_residual_beta_04896_twenty_leaf_exact.py`.  All cell
upper endpoints here are open; no claim is made at the endpoint itself.

E22 adds the pair `(5,47)` and `(19,48)`, giving 49 vertices and 86 edges.
Retiming the source scale to the exact fixed-branch minimax value
`0.011690271999265797...` equioscillates the zero-root phase-27 product-3
row-41 and product-7 row-25 clocks.  They occur at distinct products, so this
is not an algorithmic maximum or stop tie.  The complete zero-root audit
certifies

~~~text
cell       [.48869804073544294..., .4897917473484638...)
failure    phase 27, product 8, vertex 28
input batch at failure = empty
lower      phase 26, product 1, twin leaf 27
upper      phase 27, product 3/row 41 = product 7/row 25 exactly
normalized failure residual = -.00220340799079279...
~~~

It classifies 41 forced zero/clamp groups and eight structural twin-maximum
ties, with every other comparison strict.  The same source scale at
`s=1/65536` gives the direct finite cell

~~~text
[.48869803978352204..., .48979117875734753...)
~~~

and the same phase-27/product-8/vertex-28 empty-input failure.  Its normalized
failure is `-2.532016659799247e-13...`; the finite product-7 clock is uniquely
limiting and lies `6.38216185637119e-7...` below product 3.  The exact wrappers
are
`stopped_masked_input_residual_beta_04898_twenty_two_leaf_zero_root_equioscillation_exact.py`
and
`stopped_masked_input_residual_beta_04898_twenty_two_leaf_equioscillation_exact.py`.
The finite-prefix earlier-failure-or-continuity lemma turns each fixed beta
strictly inside the zero-root cell into a sufficiently small positive-root
counterexample.

## Bounded search evidence and the missing induction

The following statements are empirical finite-search facts, not graph
nonexistence theorems.

- Starting from E8, all 351 unordered pairs of core ports `1,...,26` were
  tested at beta `.48865` on the 1001-point grid
  `rho_scale in [.0128,.0138]`.  The only non-inert hit was E10.  Six other
  hits attached only to parents inactive on the prefix and reproduced the
  E8 trace exactly.
- E10 was then tested with all 351 further port pairs at beta `.48868` on
  the 1001-point grid `[.0125,.0135]`.  The pair `(1,19)` and its twin form
  `(1,22)` produced E12, which was then independently replayed exactly.
- Starting from E12, all 351 core-port pairs were tested at beta `.4890` on
  the 1401-point grid `[.0118,.0132]`.  The unique hit was `(2,20)`, giving
  E14.  A separate coarser search used 151 rho values in `[.012,.0135]` and
  reported zero hits.  The exact E14 witness therefore supplies a second
  explicit coarse-grid false negative; the coarse result is not an
  obstruction.
- Starting from E14, all 351 pairs were tested at beta `.48905` on the
  1001-point grid `[.0118,.0128]`.  Four pairs hit; `(5,22)` gave E16 and
  the largest observed upper endpoint.  This candidate was then replayed
  and audited exactly.
- Starting from E16, all 351 pairs were tested at beta `.48915` on the
  1101-point grid `[.0115,.0126]`.  Six pairs hit.  `(4,17)` gave E18 and
  the strongest endpoint, then passed exact zero- and positive-root replay.
- Starting from E18, all 351 pairs were tested at beta `.48935` on the
  1101-point grid `[.0112,.0123]`.  Sixteen pairs hit.  `(2,18)` gave E20
  and the strongest observed endpoint, then passed the complete exact
  zero-root audit and a positive-root replay at `s=1/65536`.  Most other
  high-ranking hits used an attachment whose parent was inactive on the
  tested prefix and simply reproduced the E18 trace.

The observed upper endpoints are

~~~text
E2  .4870260368530
E4  .4876701546689   gain .0006441178159
E6  .4882140103629   gain .0005438556939
E8  .4886911668658   gain .0004771565029
E10 .4886562754408   (negative step; contained)
E12 .4889861328877   gain over E8 .0002949660219
E14 .4890371491727   gain .0000510162850.
E16 .4891358095391   gain .0000986603664.
E18 .4893830355112   gain .0002472259721.
E20 .4895137840560   gain .0001307485449.
E22 .4897917473485   gain .0002779632924.
~~~

These numbers do not support a proved scalar recurrence.  A valid induction
toward `1/2` would still have to establish, uniformly in the rung:

1. a supply of attachment ports satisfying the exact parent-admission
   inequality above;
2. preservation of the negative input at leaf `28` after the topology grows;
3. overlap of consecutive cells, `lower(E_{m+1}) < upper(E_m)`;
4. an increasing upper bottleneck tending to `1/2`, with p3 and p7 both
   controlled; and
5. uniform classification of all equality events so the zero-root branch
   lifts to positive root.

The exact finite chain proves a reproducible *design principle*--paired
clock/failure retiming plus rho relays--but not a parametric near-half
family.  The fixed-parent multiplicity inequality is the precise point at
which the naive induction fails.
