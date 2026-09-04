# Stopped masked input residual: exact chronological reduction

Date: 2026-09-04

This is an unregistered companion note.  It first derives the exact cone map
and separates arbitrary supplied states from canonical point-source history.
The final section records a later exact canonical zero-start counterexample
to the literal quarter-stopped claim.

## Verdict

**The literal quarter-width `StoppedMaskedInputResidual` statement is
refuted.**  The exact one-push recurrence reduces to a
residual/physical-velocity system, and the maximal append chronology gives a
necessary-and-sufficient row shield.  Two genuinely history-specific facts
still follow:

1. every row appended after the gradient/push has nonnegative input residual
   at the next product automatically; and
2. every outer phase starts with zero velocity and with residual equal to the
   preceding phase's final chronological flux plus a nonnegative diagonal
   progress injection.

Thus a first canonical failure can occur only on a row already active during
the preceding gradient product and carrying positive retained velocity.  The
five-vertex supplied-state obstruction below first showed that one or two
successful flux images plus the quarter stop were insufficient.  A later
16-vertex rational trace reaches the same failure from the prescribed single
source and zero initialization, with every active and append push enabled.

The quarter counterexample has preceding inner-width ratio `0.258389...`.
Moreover, one 24-vertex canonical zero-start graph fails under both the
one-third and two-fifths outer chronologies, at predecessor ratios
`0.373214...` and `0.415110...`, respectively.  A different 24-vertex graph
gives exact higher failing chronology cells.
Since any fixed stop
`inner_width<=beta old_width` with `beta<1/2` still contracts the outer
bracket, the sharpened positive question is whether the cone can be proved
for even one fixed `beta<1/2`.  The negative question is cellwise rather than
monotone: changing beta changes earlier phase endpoints.  A Fraction-exact
atlas now overlaps forty-four failing cells through
`0.48979117875734753...`.  Exact eight- through twenty-two-leaf zero-root
audits independently corroborate the leaf-ladder mechanism; the E22 zero-root
equioscillation extends the overall open endpoint to
`0.4897917473484638...`.  Thus
the only surviving threshold-only candidates lie between that endpoint and
`1/2`.

## Exact reduced recurrence

Work on one shifted proximal phase, with

```text
B = Q + alpha I = b I - C,    C >= 0,
mu I <= B <= L I,             s = sqrt(mu/L),
theta = (1-s)/(1+s).
```

For the retained shift `sigma=alpha`,

```text
mu=2 alpha,  L=1+alpha,
b=L(1+s^2)/2.
```

Put

```text
A=B/L=a I-K,       a=(1+s^2)/2,
K=C/L,             delta=(1-s^2)/2,
I-A=delta I+K.
```

In symmetric normalized coordinates, `K=delta N`, where `N` is normalized
adjacency.  The equivalent random-walk degree coordinates are related by a
positive diagonal similarity, so every coordinate sign below is unchanged.

Assume the input cone has held through the start of product `t`.  Let `u_t`
be the certified lower/current state after the preceding push and append
closure.  Let `d_t` be the physical velocity encoded by the clamped NAG
current/previous pair.  The post-clamp state has

```text
d_t >= 0,    q_t=u_t+theta d_t.
```

For shifted load `h`, define the scaled certified and input residuals

```text
e_t=(h-Bu_t)/L,
xi_t=(h-Bq_t)/L=e_t-theta A d_t.
```

Input-frontier admission adds every exterior row with positive `xi_t` at zero
state.  Let `A_t` denote the resulting gradient face.  Under the input-cone
premise, `xi_t>=0` on `A_t`.  The raw gradient current is

```text
v_t=q_t+xi_t.
```

Its active residual is `L(I-A)xi_t>=0`; hence the uniform retraction shave is
zero and `v_t>=q_t>=u_t`.  Therefore the pre-push lower is exactly `v_t`.
The simultaneous active diagonal push is

```text
p_t^(0)=((delta I+K)xi_t)/a.                    (1)
```

After clamping the raw auxiliary state above the pushed lower, the physical
velocity is exactly

```text
d_(t+1)=[theta d_t+xi_t-s p_t^(0)/(1-s)]_+     (2)
```

on `A_t`.  Every row appended later in the product is initialized with zero
velocity.

Now run maximal exact-positive append closure and label its batches
`1,...,m`.  Write `p_t^(k)` for the diagonal increment of batch `k`, and put
`tau(i)=0` for `i in A_t`, while `tau(i)=k` for a row first appended in batch
`k`.  Direct cancellation of the diagonal residual at first push gives

```text
e_(t+1),i = sum_(k>=tau(i)) (K p_t^(k))_i.      (3)
```

Equation (3) is the chronological flux decomposition in the normalized
variables.  Earlier batches disappear from a newly appended row because its
own diagonal increment cancels the whole residual accumulated before its
admission; only same and later batches remain.

Combining (2)--(3), the next input residual is

```text
xi_(t+1),i
 = sum_(k>=tau(i)) (K p_t^(k))_i
   +theta(K d_(t+1))_i-theta a d_(t+1),i.       (4)
```

For a post-gradient appended row, `tau(i)>=1` and `d_(t+1),i=0`; every term
in (4) is nonnegative.  For a row in `A_t`, (4) becomes

```text
xi_(t+1),i
 = [K(sum_(k=0)^m p_t^(k)+theta d_(t+1))]_i
   -theta a d_(t+1),i.                          (5)
```

Consequently, preservation of `MaskedInputResidual` is exactly the local
chronological shield

```text
[K(sum_k p_t^(k)+theta d_(t+1))]_i
   >= theta a d_(t+1),i                         (6)
```

on old/input-admitted gradient rows.  Later admission batches contribute
only positive credit to (6).  There is no hidden residual or projection term.

### Proof of the recurrence

The raw gradient displacement from `u_t` is `theta d_t+xi_t`.  The usual NAG
auxiliary is above the raw current by `(1-s)/s` times this displacement.
Raising the current by `p_t^(0)` and clamping the auxiliary above it therefore
leaves physical velocity

```text
[(1-s)(theta d_t+xi_t)/s-p_t^(0)]_+ * s/(1-s),
```

which is (2).  The active raw residual is
`L(I-A)xi_t`, and division by the diagonal `La` gives (1).  At the first push
of row `i`, its diagonal contribution cancels every residual contribution
that arrived earlier.  A simultaneous same-batch neighbor increment and
every later neighbor increment remain, proving (3).  Finally substitute (3)
in `xi_(t+1)=e_(t+1)-theta A d_(t+1)` to obtain (4)--(6).

## The outer phase injection omitted by arbitrary-state examples

Let `ell_k` be the retained lower center at the start of phase `k`, and let
`ell_(k+1)` be the lower returned by that phase.  Its final shifted residual
and the original residual at the next phase start satisfy the exact identity

```text
r_k^shift
 = c+alpha ell_k-(Q+alpha I)ell_(k+1),

c-Q ell_(k+1)
 = r_k^shift+alpha(ell_(k+1)-ell_k).             (7)
```

Both terms on the right are nonnegative on the certified support.  The first
is the chronological flux (3); the second is a diagonal progress injection.
The new phase resets `d=0`, so its first input residual is automatically
nonnegative.  Identity (7) is the precise extra ancestry that the known
embedded arbitrary-center counterexample, and the obstruction below, do not
demonstrate.

The injection itself has a lossless expansion in the reduced variables.  If
`u_t` is the lower before product `t`, its exact increase in that product is

```text
u_(t+1)-u_t
 = 1_(A_t) (theta d_t+xi_t) + sum_(k=0)^m p_t^(k).   (8)
```

The first term is the gradient displacement from `u_t` to the raw current;
the remaining terms are the active and append diagonal increments.  Every
term in (8) is nonnegative under the input cone.  Since
`alpha/L=s^2/2`, consecutive phases therefore obey the normalized nested
history identity

```text
e_(k+1),0
 = e_k,T + (s^2/2) sum_(t<T)
     [1_(A_t)(theta d_t+xi_t)+sum_j p_t^(j)].       (9)
```

On the carried certified face, `e_k,T` already has the admission-time
decomposition (3), and the new phase again starts with zero velocity.  Thus
(9), rather than membership in the post-push flux cone alone, is the smallest
exact predecessor interface exposed by this reduction.

There is also a point-source identity not shared by a generic Stieltjes
right-hand side.  In random-walk degree coordinates let `P` be the walk
matrix, so `K=((1-s^2)/2)P`, and let `v` be the source.  The original
operator and load normalized by `L` are exactly

```text
Q/L=(1/2)I-K,
c_i/L=(s^2/2)(1_(i=v)/d_v-rho).                  (10)
```

Consequently every canonical phase `k` with outer center `ell_k` satisfies

```text
e_(k),0
 = (s^2/2)(1_v/d_v-rho 1)-[(1/2)I-K]ell_k.      (11)
```

More generally, if `u>=ell_k` is any certified lower during that shifted
phase, nonnegativity of its shifted residual gives, on a non-source row,

```text
(P u)_i-u_i
 >= s^2(2u_i-ell_(k),i+rho)/(1-s^2) > 0.         (12)
```

The same inequality holds with `u` replaced by the input extrapolate `q`
whenever its cone premise is true.  Hence every nonsource certified row has
a neighbor with strictly larger lower value, yielding a strictly ascending
path to the source.  Equation (12) also quantifies why an
`alpha`-independent pointwise buffer is implausible: its mandatory margin is
only order `s^2`.  This maximum-principle structure is necessary but is not
sufficient by itself--the known arbitrary positive phase-center embedding
already has the same point-source affine form.  The still-unproved content is
the joint recursive compatibility of (3), (8), and (11) all the way back to
the zero start.

## Exact two-step stopped flux obstruction

The script
`stopped_input_cone_two_step_flux_counterexample_exact.py` uses the connected
simple unit graph

```text
E={02,03,04,13,23,24,34},   d=(3,1,3,4,3),
s=1/20.
```

In random-walk degree coordinates, start a supplied full-face phase with

```text
xi_0=(0,800,0,500,0),   d_0=0,
W=max(xi_0)/s^2=320000.
```

Apply (1)--(5) with a single full-face active push batch and no append batch.
The first next-input residual is strictly positive.  The exact post-product
width ratios are

```text
max(e_1)/(s^2 W)=1114407/2566400 > 1/4,
max(e_2)/(s^2 W)=330779369823/1317281792000 > 1/4.
```

Thus products two and three are both executed by the literal quarter rule,
but the input to product three has

```text
xi_(2),1=-4389594301/864466176 < 0.
```

This proves that all of the following together are still insufficient:

- a connected graph-derived PageRank matrix;
- a nonnegative zero-momentum phase input;
- one already successful next-input cone step;
- two exact chronological active-push flux identities; and
- the literal stopped continuation rule.

It is not by itself a counterexample to `StoppedMaskedInputResidual`: the full
face and `xi_0` are supplied rather than generated by the minimal single-source
outer chronology.  Its role is to rule out a finite one-step-image induction
and to show why (7), or an equivalent source-ancestry invariant, could not be
dropped.  The next result shows that even the complete ancestry is not enough
for the literal quarter rule.

## Exact canonical zero-start counterexamples

For the literal quarter stop, take vertices `0,...,15`, source `0`, and the
simple unit-edge graph

```text
E={(0,1),(0,10),(1,2),(2,3),(3,4),(4,5),(5,6),(7,12),
   (8,9),(9,10),(9,11),(10,15),(11,12),(12,13),(12,14),
   (13,14),(14,15)}.
```

Put

```text
s=1/224,       alpha=s^2/(2-s^2)=1/100351,
d_0 rho=481/8000,       rho=481/16000.
```

Run the canonical retained-prox outer loop from zero, with relative terminal
width `1/1000`.  Within every phase use exactly the chronology derived above:
pre-gradient input-frontier admission, one active diagonal push, maximal
immediate append-push closure, and the literal quarter stop.

At one-based phase 20, product 10, the active face is

```text
{0,1,2,3,4,5,6,8,9,10,11,12,14,15}.
```

The input residual at vertex `11` is strictly negative.  In random-walk
degree coordinates,

```text
xi_11=-8.939445218207715...e-12,
xi_11/old_width=-1.533358898199047...e-8.
```

This is not a post-stop artifact.  The preceding completed product has

```text
inner_width/old_width=0.2583894607814098...>1/4,
```

so product 10 is required by the stated rule.  Both this comparison and the
negative residual sign are exact rational statements, not floating
tolerances.  The first failure also occurs on a row with retained positive
velocity, as predicted by (4).

`retained_prox_input_cone_trace_exact.py` replays both the weakened
input-frontier-only chronology and this `one-push-maximal` chronology with
`fractions.Fraction`, records every admission/stop branch, and stops before
executing the first illegal product.  The counterexample proves that the
complete point-source identities (7)--(12) do not imply the quarter-stopped
cone.  The dedicated theorem statement and wrapper are
`STOPPED_MASKED_INPUT_RESIDUAL_ZERO_START_COUNTEREXAMPLE.md` and
`stopped_masked_input_residual_zero_start_counterexample_exact.py`.

The failure is not confined to the quarter constant.  On a different
24-vertex graph, still with `s=1/224`, the exact one-push-maximal zero-start
trace with `beta=1/3` reaches a negative input residual at one-based phase 13,
product 7, while

```text
inner_width/old_width=0.3732141756300159...>1/3,
xi_16/old_width=-9.274461320341061...e-8.
```

See `STOPPED_MASKED_INPUT_RESIDUAL_ONE_THIRD_COUNTEREXAMPLE.md` and
`stopped_masked_input_residual_one_third_counterexample_exact.py` for the
44-edge graph and the full exact trace assertions.

Changing the same graph's stop to `beta=2/5` changes its outer chronology but
does not cure the invariant.  At one-based phase 14, product 7, the exact
trace has

```text
inner_width/old_width=0.4151107187959626...>2/5,
xi_16/old_width=-4.846557184187879...e-9.
```

The exact wrapper is
`stopped_masked_input_residual_two_fifths_counterexample_exact.py`; its
statement is `STOPPED_MASKED_INPUT_RESIDUAL_TWO_FIFTHS_COUNTEREXAMPLE.md`.

For a fixed graph and parameters, a failing trace is stable exactly on a
half-open chronology cell.  Every product at which a phase stopped imposes
`inner_width/old_width<=beta`; every product which continued imposes the
strict reverse inequality.  Thus the identical prior history, and hence its
strict failure, persists for

```text
max{ratios at stopped products} <= beta
  < min{ratios at continued products}.          (BetaChronologyCell)
```

The first three named witnesses occupy cells containing the quarter,
one-third, and two-fifths constants.  Further chronologies of the same two
24-vertex graph families, a 51-edge bridge, a dense beta-`0.45` graph, and a
structured double/triple-clock grafts, several edge-retimed 27-vertex graphs,
and a two- through twenty-two-leaf ladder give forty-four
pairwise-overlapping cells whose
union is

```text
[0,0.48979117875734753...).
```

See `STOPPED_MASKED_INPUT_RESIDUAL_BETA_CELL_ATLAS.md` and
`stopped_masked_input_residual_beta_cell_atlas_exact.py`.  The atlas prints
every rational endpoint, validates every canonical graph and failure, and
checks every overlap.  The upper endpoint is open, and a predecessor ratio
alone must not be interpreted as refuting beta outside its chronology cell.

On the final 35-vertex eight-leaf topology, three exactly audited scaled
zero-root cells overlap from `0.4880686430540822...` through
`0.488691166865773...`.  All stop comparisons are strict; the only ties are
forced closure/inheritance events and harmless automorphic twin-leaf maxima.
A finite-prefix continuity dichotomy therefore produces a positive-root
failure for every beta strictly inside that limiting relay.  The twelve-leaf
zero-root audit gives the corroborating cell
`[0.4886720900294752...,0.48889876186669784...)`, while its positive-root cell
extends to `0.4888994588075898...`.  The fourteen-leaf zero-root relay reaches
`0.489037149172748...`, while its positive-root relay extends to
`0.48903788718422087...`.  The sixteen-leaf zero-root audit reaches
`0.48913580953910807...`, while its positive-root cell extends to
`0.4891365074011953...`.  The retimed eighteen-leaf finite cell reaches
`0.4893806599606024...`, while its audited zero-root family extends to
`0.4893830355111828...`.  This final failure has simultaneous input batch
`[19,22,23]`; unlike earlier leaf rows, fresh admissions occur in the failing
product while the negative residual remains on already active leaf `28`.  See
`STOPPED_MASKED_INPUT_RESIDUAL_BETA_04885_EIGHT_LEAF.md`.

Adding `(2,45)` and `(18,46)` gives a 47-vertex, 84-edge twenty-leaf graph.
At root `s=1/65536` its exact positive-root cell is
`[0.48907818585092405...,0.4895138464285235...)`, overlapping E18.  The
failure returns to phase 26, product 8, at already active leaf `28`, with an
empty input batch.  The corresponding zero-root audit gives the nearby cell
`[0.48907818669711567...,0.48951378405604035...)`; it classifies 40 forced
equality groups over 27 coordinates and six structural twin-maximum ties,
with every other relevant comparison strict and tightest strict margin about
`2.6944e-8`.  Thus E20 is both a direct finite extension and an independently
audited limiting-family corroboration.  See
`stopped_masked_input_residual_beta_04896_twenty_leaf_exact.py` and its
zero-root audit wrapper.

Adding `(5,47)` and `(19,48)` gives a 49-vertex, 86-edge twenty-two-leaf
graph.  Retiming the source scale to the exact fixed-branch equioscillation
value gives the positive-root cell
`[0.48869803978352204...,0.48979117875734753...)` at `s=1/65536`.  The
failure is phase 27, product 8, on already active leaf `28`, with empty input
batch.  Product 7 continues after its append closure admits and pushes
`{22,23}`.  At zero root, the product-3 row-41 and product-7 row-25 ratios are
exactly equal and jointly attain the open upper endpoint; because they occur
in distinct products, this is not an algorithmic branch tie.  The full audit
still classifies every within-product equality as forced, and its chronology
cell is `[0.48869804073544294...,0.4897917473484638...)`.  Applying the
finite-prefix earlier-failure-or-continuity lemma from the atlas supplies a
sufficiently small positive root for every fixed beta strictly inside that
cell; the limiting trace is not itself counted as a finite graph instance.

The numerical value `1/4` is not structurally necessary.  If a phase stops at
`inner_width<=beta old_width`, then (for the retained shift used here)

```text
new_width<= (1/2+beta) old_width.
```

Hence every fixed `beta<1/2` preserves a constant outer contraction.  The
exact remaining positive claim is therefore `BetaStoppedMaskedInputResidual`
for at least one beta in `[0.4897917473484638...,1/2)`.  Conversely, refuting
the threshold-only route requires extending the counterexample-cell cover
through that remaining interval.

## Evidence and honest boundary

The exact all-threshold audit in `retained_prox_parametric_rho_exact.py`
passes all 38 connected labelled four-vertex graphs at `s=3/10`, relative
width `1/32`: 1,353 exact rational trace cells, 12,841 product traces, and
424,661 comparisons.  The minimum is zero only on a tautological zero-history
row.  This is finite evidence, not a theorem.

Equation (12) independently shows that the source-forced pointwise buffer
degenerates with `s`.  Hence even if nonnegativity is true, a proof should be
exact-real and should not spend an `alpha`-independent numerical margin.

The unresolved statement is now sharply confined to (6) for rows active in
the preceding gradient product, with the complete zero-start ancestry (7)
and all earlier admission deposits retained, under some fixed stop threshold
in `[0.4897917473484638...,1/2)`.  Chronological flux by itself, or any
induction retaining only one preceding successful cone state, is provably
insufficient.  A global negative result must extend the exact chronology-cell
cover to `1/2` or replace the finite atlas by a uniform parametric family.
