# Removing the ancestor walk: the next tree/cycle interface

Date: 7 September 2026. **Open**, with elementary algebra and explicit
prior-note pointers. This is a continuation target, not another fast solver
claim. Read `TREE_AFFINE_PROBE.md`, `LOCAL_CYCLE_PROBE.md`, and the exact
length-two-attachment witness first.

## What existing notes already supply

`delayed_reflection_ladder`, `thm:lazy-tree-response`, is the natural local
baseline. A child's first activation threshold uses only its edge and degree.
Its adjacency row is scanned only after the activation is consumed. Each
vertex maintains its current response piece and one lookahead per child;
a heap chooses the next child event. Thus no whole ambient tree is read.

Its work contains `sum_{v in S} dist(seed,v)`: each event is propagated
through all ancestors. The support-radius estimate converts this into the
existing `1/sqrt(alpha)` product scale. Recreating that lazy iterator would
not establish OP3. The new persistent ACT proves a near-linear supplied-tree
bound, but knows the full descendant curves and subtree sizes in advance.

`aesp_cd_l1_rppr`, `prop:aesp-cd-sp-meld-hull-reduction`, already identifies
a persistent affine-pullback-and-meld threshold-hull interface for supplied
series-parallel parses. Its following epoch construction is a slower
unconditional substitute. Do not treat a normal dynamic hull as implementing
the bulk interface. These are contextual obstacles, not dependencies used to
prove the two new solver drafts.

## Why compressing a heavy chain is plausible

On a fixed response piece, collect the light-child responses at an active
chain vertex into `c_i*u_i + e_i`. Its current equation is

\[
 \beta_i u_i-\gamma u_{i-1}-\gamma u_{i+1}=h_i,
 \qquad \beta_i=d_i-c_i,\quad h_i=b_i+e_i.
\]

Consequently the transfer from one adjacent pair to the next is the affine map

\[
 \begin{pmatrix}u_{i+1}\\u_i\\1\end{pmatrix}
 =
 \begin{pmatrix}
 \beta_i/\gamma&-1&-h_i/\gamma\\
 1&0&0\\0&0&1
 \end{pmatrix}
 \begin{pmatrix}u_i\\u_{i-1}\\1\end{pmatrix}.
\]

A balanced tree of products supports a named light-response change or a
named coordinate query in logarithmic word work on a supplied chain.
This is the same fixed-factor mechanism already discussed in
`aesp_cd_l1_rppr`; no new bound for aggregate event location follows.

Each pending light-child event gives a threshold `u_i=tau_i`. Pulling it
through the chain yields an affine inequality in the chain's two endpoint
potentials. Updating one interior response changes the affine pullback of
whole groups of old thresholds. A solver must locate the first crossing
among all those groups, including an unsuccessful search certificate.
The length-two-attachment witness shows that these old events really can
occur after the advancing cycle frontier has left their centers.

## The precise distinction from static ACT merging

In the supplied-tree construction, all knots of a smaller child are known.
They can be merged into the larger curve, with the cost paid by subtree-size
doubling. Lazy discovery has not revealed future child knots. A response
change at an old light branch must change the chain state and its future
event certificate while preserving all other undiscovered branches.

Within a single off-path subtree, a change in its articulation's affine
potential transforms all root-parameter event times by a common affine map.
Across different articulations on a long path, these transforms differ.
Treating their union as one scalar affine heap is unjustified. A balanced
two-port hierarchy or a stronger source-specific certificate is needed to
avoid walking every articulation.

The arbitrary-two-port counterexample in
`prop:aesp-cd-two-port-direction-stop` does not settle the source-specific
question: its two port motions are externally chosen, whereas a single-seed
obstacle continuation follows one endogenous monotone trajectory. This is a
potential place to weaken the required interface, provided the restriction
is proved along actual local admissions.

## Next falsifiable experiments and proof targets

1. Implement a charged exact continuation on a cycle with length-two
   attachments. Separate named transfer updates from all-threshold event
   location. Start with the saved 15-vertex witness; then vary attachment
   lengths and locations asymmetrically.
2. Test whether actual single-source Schur updates induce a bounded number
   of common affine event-time transformations. Count distinct transforms
   and their member degrees. An unbounded count rejects that representation,
   not OP3 itself.
3. Try a balanced hierarchy whose quietness certificates tolerate the
   geometric publication bands from `thm:op3-geometric-recipient`. Charge
   failed certificates, hierarchy rebuilding, and all changed light-child
   pieces. An exact arbitrary-direction hull may be stronger than necessary.
4. If pursuing a local heavy decomposition, include its discovery and
   changes as the support grows. Final-support subtree sizes are unavailable
   advice. The static ACT's size-doubling proof cannot be imported unchanged.

The useful outcome of this probe is either a paid interface with explicit
state operations or a small source-valid failure of one of these restricted
certificates. Repeating an exact global solve or a full old-boundary scan
after every activation is only a reference oracle.
