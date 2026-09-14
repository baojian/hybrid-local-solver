# Independent audit of direct exception replacement

Audited `direct_exception_integer_rppr.py`,
`direct_exception_transition_proof.md`, the stable integer corrector, and
the reporter registry/removal implementation. No production changes or
correctness corrections are required. This is a representation optimization
of the already proved rounded recurrence, not a new numerical iteration.

## Registered keys and the transition boundary

`IntegerClippedReporter._set` obtains the immutable old triple
`(kind, numerator, degree)` from `records[vertex]`. It removes that exact
numerical key from the corresponding old tree before inserting the new key.
It never reconstructs the old numerator from the current `S`, `X`, or `L`.
Consequently, changing those state variables cannot invalidate subsequent
removal of an old exception. A mixture of old and new exception keys remains
a valid AVL tree, with exact integer moments, throughout the transition.
It temporarily ceases to represent the complete new raw vector; the code
does not query it in that interval.

The only `project_counts` call in `step` precedes every state change.
`_row`, `_expose`, `_set_base`, `_finish_direct_transition`, `_rebase`, and
`_install_exceptions` perform no reporter projection or threshold query.
The step returns only after finishing the full representation update.
Checkpoint code runs outside that completed step. This includes cooperative
composition with the early-stop and binomial scheduling classes.

Write `E_old` and `E_new` for the old and new exception sets. In a non-rebase
step, the code covers every vertex as follows:

1. Every vertex of `E_old \ E_new` is replaced by its current base key.
2. A touched vertex outside both sets receives its current base key.
3. Every member of `E_new` receives its complete new exception numerator,
   replacing its registered old record directly.
4. Every remaining base record has unchanged `X_i` and `L_i`, and hence
   unchanged unscaled base numerator. Its changed physical scaling is
   supplied globally by the new `S` at the next query.

The first and second loops cannot overwrite a completed new exception:
both explicitly exclude `E_new`. The third loop completes every exception,
including previously unexposed or previously ordinary base vertices.
Newly exposed neighbors start with a zero base key. If their primal
response changes they are touched; if only their kinetic response changes
they belong to the new `M` support. Thus new exposure is covered.

There is a stronger invariant for actual steps: `touched` is contained in
`supp(z_new) union supp(M_new)`, hence in `E_new`. Every positive primal
increment belongs to an emitted coordinate; every neighbor-sum increment
belongs to a neighbor of such a coordinate, whose new kinetic neighbor sum
is positive. The ordinary-base-update loop is therefore redundant on the
actual recurrence, although retaining it is correct and inexpensive. The
synthetic partition test below exercises its defensive branch separately.

On a rebase, the inherited `_rebase` rescales and rounds `X` and `L`, resets
`S=H`, and resets the base key of **every exposed vertex**. Registered old
exceptions are removed using their stored old keys during that pass. The
following `_install_exceptions` completes the new state. No preliminary
old-exception pass is necessary, and no adjacency is read by the rebase.

## Trajectory, graph order, and accounting

Inductively the two disjoint record sets at each query boundary equal those
of the stable implementation. The ordered trees may have different shapes,
but each tree's emitted order depends only on its numerical key and vertex
tie-breaker. The projection result, including its multiplier, emitted tuple,
and cap status, is identical. The integer arithmetic and subsequent sorted
`p.items()` traversal are unchanged. Therefore numerical states, the order
of graph queries, graph counts, block counters, and materialized outputs
agree exactly. Reporter operation counts and representation-transition
counters need not agree.

If `V_b` is baseline support volume and `V_k` is kinetic support volume,
then the source record count is at most `1+2 V_b` by the union of the seed,
baseline support, and its neighbors, and
`|E_k| <= 1+2 V_b+2 V_k`. The touched set has at most `2 V_new` members.
Thus the new membership passes, temporary set construction/reclamation,
retirement, and direct installation cost
`O(K(1+V_b)+sum_k V_k)` deterministic AVL point operations over a stage.
Since `V_b=O(1/r)`, this is the stated `O(K/r+W)` charge. The pre-existing
full rebase work and reporter query costs remain charged as before.
No sum over the full historical exposed state has been introduced outside
the already paid full rebases. The extra diagnostic counters are logical
operation counters; they do not purport to instrument every Python-level
allocation, comparison, or reclamation instruction.

The cooperative class order for the optional combined adapter is
`DirectCombined -> Combined -> EarlyStop -> Binomial -> SourceEnergy ->
DirectExceptionInteger -> Integer`. Initialization installs direct metrics
before later scheduling initialization completes. Binomial `super().step`
selects the direct step, and early-stop invalidation and checkpoint timing
remain unchanged. The independent checker exercises this actual MRO.

## Independent exact evidence

`audit_direct_exception_transition.py` and
`direct_exception_independent_verification.json` are separate from the
production module and the author's existing suite. All four test groups
passed. There were:

- 284 exact reference trajectory steps, including 64 combined-schedule
  prefixes, and 45 scalar rebases;
- 1,194 completed reporter point-mutation checks inspecting 3,321 nodes;
- 768 independently recomputed query-boundary raw-vector checks;
- 380 projection calls, each checked to occur at the expected completed
  iteration and with the complete exact raw vector;
- seven new vertex exposures during reference trajectories;
- a binding-cap initialized fixture;
- 96 steps with a degree `10^30` boundary vertex: only the degree-one seed
  adjacency was read, exactly once;
- a separate synthetic representation transition exercising a retired
  exception, a persistent exception, an ordinary touched base record, and
  newly installed exceptions with no graph or projection calls.

After every reporter point mutation the checker independently validates
BST order, AVL balance/heights, subtree sizes, degree/numerator moments,
disjointness, and agreement with the stored registry. It recomputes raw
densities from the rational `alpha`, `theta`, `sigma`, and state values
rather than reusing `_base`. Every compared step has identical projections,
state maps, record triples, certificates, last-step data, and external graph
query sequences. Real reference trajectories in this bounded suite did not
retire exceptions; retirement is covered by the explicitly synthetic unit
fixture and the set-partition proof, rather than claimed as cold-start
trajectory evidence.

Source hashes are saved in the verification JSON. The independently audited
production hash is
`61e04500b459042822c9724bfb9d549a2e71ec2248126d40651dfc60ee8ee06b`.
The author's separate exact suite and timed comparison are additional
evidence; this independent audit does not reclassify their measurements as
independently reproduced timings.
