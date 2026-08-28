# AESP-CD RPPR note

This standalone note develops a composite AESP outer loop with local proximal
coordinate descent for the shared regularized PageRank model. The proof source
is `main.tex` and its included sections; [`STATUS.md`](STATUS.md) is the
current claim ledger and handoff.

The note proves the local KKT-mass and relative-oracle interfaces, safe lower
centers and retraction, fixed-envelope locality, finite residual identities,
several exact trajectory calibrations, and an unconditional accelerated result
on the a-posteriori high-Dirichlet class. It also records sharp failures of
raw correction counting, Euclidean-only collateral packing, black-box
shadowing, and the simplest unsplit lagged energy bank.
The finite-inner comparison is now sharp at the root-potential level:
`sqrt(Phi_(t+1)) <= sqrt((1-q) gamma_t Phi_t) + sqrt(kappa_A) xi_t`.
This removes the artificial `xi_t <= 1` restriction and improves the
conditional absolute polish from a `theta` scale to a `sqrt(theta)` scale;
it does not prove the missing net packing inequality.
On the exact settled optimal face, a new cross-normalized error/velocity bank
contracts by `1-q` on every correction-free stage and by a constant after a
`Theta(1/q)` post-full window. It passes the previous K2 low-mode STOP; its
unpaid term is now the explicit correction forcing in a `Q_A^(-1)` norm. A
reachable complete-graph family proves that no graph-uniform constant can pay
that forcing from net high-band decrease alone: the required ratio is
`>(N-1)/23`. The surviving exact fixed-face interface is instead a
contract-or-spend window: after `Theta(1/q)` stages the bank contracts by a
constant unless it spends a telescoping low Euclidean endpoint drop.
A fully rational-interval `P24` trajectory additionally proves that paying
the low forcing by net high-band drop plus `6/5` times the starting low bank
still fails; its certified required coefficient is greater than
`1.206959416`. This narrows the viable interface to the unsplit endpoint
spend or an adaptive event allowance.
An alternative Moreau-Hessian bank has a correction-event forcing metric with
condition number below `4(1+q^2)`.  For an explicit nested-face epoch protocol
that expands only at boundaries and restarts momentum at the unchanged primal
point, it gives a geometric root-potential ledger: face-optimum gains and
correction masses are injected once and earlier events are automatically
discounted.  This is not yet an event-packing theorem for the automatic
per-stage admission trajectory.
Keeping the correction cross term gives a sharper signed increment `Xi_t`.
Only `[Xi_t]_+` enters the refined epoch ledger, and its fixed-face sum has a
telescoping Stieltjes payment without the former geometric `1/q` loss. A
reachable `P3` event proves that `Xi_t` can nevertheless be positive and can
increase the bank, while the reachable `K8` family makes the telescoping
payment asymptotically tight.  An exact settled `S5` trajectory has adjacent
positive partial/full events and grows the bank across the pair, so even a
mandatory one-step quiet gap is false.  On the positive side, every graph
family with a proved clipped-master inequality has a mean-free Moreau bank
that contracts by a factor at most `3/8` in `ceil(log(2)/q)` exact fixed-face stages,
independently of event density.  The remaining pulse obstruction is therefore
concentrated in the constant low mode.  This high-bank estimate now has a
finite-inner root perturbation with a discounted residual budget.  For the
low mode there is an exact dichotomy: mean overshoot contracts its Moreau bank
by `1-q` in one step, while every non-overshoot correction is forced by the
infinity norm of the mean-free trial residual.  Combining the master high
root with the exact forced mean recurrence gives a two-scale epoch potential:
a quiet `ceil(2/q)` same-point-restart epoch contracts it below `0.407`, and
an epoch whose observable weighted mean deficit is at most one quarter still
contracts by `3/4`.  A sharper arbitrary-history low-root gate halves the
two-scale potential on every accepted `ceil(2/q)` window, and it retains an
explicit finite-inner residual allowance.  Independently, an observable
pure-prox alignment warmup reduces the high/mean residual ratio by
`(1+q)^(-J)`; once its computable threshold is crossed, the entire exact
global-momentum tail is permanently correction-free.  This gives a genuine
fixed-full-face accelerated route with `O(1/q)` warmup up to logarithms,
without lower eigendata.  A reachable `K_N` family proves that high-to-low
transfer cannot be paid by a graph-uniform high-bank coefficient: even after
a `1/q` rescaling the required coefficient is greater than `(N-1)/15`.
Thus a local, infinity-norm, or volume-sensitive payment for the weighted
mean deficit is still needed.
On a fixed certified face, the inner-work obstruction is now removed:
Chebyshev semi-iteration may use signed scratch vectors, after which a
Stieltjes retraction and coordinatewise maximum with the old safe checkpoint
publish a monotone lower certificate. A small shift therefore costs
`O_tilde(vol(A)/sqrt(lambda_lower))`, and a certified final RPPR face can be
solved directly in `O_tilde(1/(rho*sqrt(alpha)))` work. Requiring every
scratch residual to remain nonnegative provably loses this acceleration, and
fixed-rank low-mode deflation is blocked by arbitrarily high multiplicity
near-ground clusters. The remaining end-to-end issue is face discovery,
certification, and replay rather than the terminal linear solve.
That boundary is now sharper. Full-graph Chebyshev scratch can carry constant
`l2` mass on an exponentially large regular-tree frontier at degree
`Theta(1/sqrt(alpha))`, so unrestricted signed scratch is not automatically
local even when the final obstacle support is one vertex. Conversely, if
every restricted face exposes a margin-certified boundary batch of volume at
least `gamma*vol(A)`, safe restricted solves and scans geometrically sum to
`O_tilde(vol(S*)/(gamma*sqrt(alpha)))`. Endpoint paths give the matching
structural STOP: a boundary-only protocol may expose one vertex per batch and
pay quadratic cumulative face volume. Across an explicit same-point face
replay, the sharp graph-uniform Moreau root-shock coefficient is `2` (energy
coefficient `4`), so the existing root convolution has optimal scale.
The singleton path STOP is not informational.  An append-only scalar
`LDL^T` message evaluates each new boundary key in constant time and performs
only one terminal back substitution, giving output-linear discovery work.
The block Schur identity shows what must replace this message on a general
graph: an implicit dynamic response applying the old inverse to every new
coupling block and refreshing affected boundary queries.  Fixed-rank Krylov
recycling does not suffice for arbitrary new coupling directions.
On forests this interface can be realized by top-tree Schur summaries:
each link, active/pinned toggle, or named KKT query changes only logarithmically
many two-port quadratic messages.  A supplied width-`w` junction tree gives
the analogous `O((w+1)^3 log B)` update.  This is not yet an end-to-end
frontier oracle: the number `Q` of named pinned-coordinate queries remains an
explicit charge and can be quadratic under repeated full-frontier rescans.
For a stable fixed separator of dimension one or two, a kinetic threshold
heap or planar extreme-point reporter closes this query term in near-linear
work; the general fixed-dimensional statement is an explicit dynamic
extreme-point interface. Balanced forest messages also have a certified
finite-precision implementation under a nonzero KKT gap. Exact rational
messages do not have polylogarithmic bit size in general: a constant-condition
tridiagonal family already produces endpoint fractions with linearly many
bits.
Speculative coordinate-envelope doubling gives a second conditional route:
its solves geometrically sum to
`O_tilde(vol(U_final)/sqrt(lambda_floor))`, but `U_final` includes inactive
halo and need not be controlled by `vol(S*)`.  Under strict primal/dual active
margins, accelerated projected-gradient scratch identifies the face and the
safe Chebyshev publisher implements the required obstacle primitive.  Without
those margins, support discontinuity and high-degree inactive decoys remain.
The RPPR support cap nevertheless gives a universal retained-volume result:
by keeping at most `1/rho` inactive halo volume in addition to the true active
support, an exact dynamic obstacle protocol never retains more than `2/rho`
volume. This is a partial affirmative answer, not an accelerated solver: all
serial updates and frontier reports remain charged to the explicit quantity
`W_DS(2/rho)`. A subcubic exact audit shows that naive factor-two speculation
can already explore `26/9` times the final support volume. Once discovery has
certified the final positive face, carrying no momentum through admissions
and restarting only once gives the q-free bridge
`C_rst <= 4(F(z)-F(x*))`; the accelerated fixed-face tail can then start from
this certified root budget.
The common-cap truncation ledger is also joint: correction and surviving
momentum `Q`-energies share one copy of the telescoping energy drop.

The live target is to batch and certify face discovery, pack failed
proper-face windows, and charge changing-face replays.
No graph-uniform exact accelerated solver or unconditional
`O_tilde(1/(rho*sqrt(alpha)))` end-to-end theorem is claimed. In particular:

- the abstract ledger witness is not an RPPR instance or an exact-proximal
  trajectory;
- the finite P4/P7 traces prove no infinite periodicity and no finite-inner
  work theorem;
- the fixed-P4 theorem refutes a horizon-uniform inflation bound while its
  primal error still converges geometrically, so it is not a net-exponent
  counterexample;
- the retraction discontinuity is a STOP for black-box shadowing, not a
  counterexample to direct finite-sequence packing or a graph-uniform solver
  theorem;
- entry-dominated stages and persistent-row energy now have explicit charges,
  but converting the event-level low-progress spend into a changing-face
  accelerated net exponent remains open.

An exact settled `P96` trajectory also shows why the new gate cannot be
replaced by a raw half-contraction assertion: its total Moreau bank retains
more than `0.54` after exactly `1/q` transitions, with the low component
retaining more than `2/3`.

Build the note from the repository root with:

```bash
make -C manuscript/notes/aesp_cd_l1_rppr
```

Run all seventeen exact audits with:

```bash
uv run python -m experiments.proof_audits.runner \
  --tier full --note aesp_cd_l1_rppr
```

Their durable IDs are:

- `aesp_cd_l1_rppr.safeguarded_outer_ledger` (Round 022 provenance);
- `aesp_cd_l1_rppr.fixed_operator_p4_tail` (Round 023);
- `aesp_cd_l1_rppr.retraction_and_fixed_face` (Round 024);
- `aesp_cd_l1_rppr.boundary_shielding_filter` (Round 025);
- `aesp_cd_l1_rppr.persistent_q_energy` (Round 026);
- `aesp_cd_l1_rppr.weighted_reserve_boundary` (Round 027);
- `aesp_cd_l1_rppr.windowed_cross_normalized` (Round 028);
- `aesp_cd_l1_rppr.p24_low_start_stop` (Round 029);
- `aesp_cd_l1_rppr.signed_event_stop` (Round 030);
- `aesp_cd_l1_rppr.adjacent_signed_event_stop` (Round 031).
- `aesp_cd_l1_rppr.p96_full_face_window_stop` (Round 032).
- `aesp_cd_l1_rppr.safe_chebyshev_face` (Round 034).
- `aesp_cd_l1_rppr.singleton_face_batches_stop` (Round 035).
- `aesp_cd_l1_rppr.s5_face_shock_sharp` (Round 036).
- `aesp_cd_l1_rppr.rppr_speculative_decoy` (Round 037).
- `aesp_cd_l1_rppr.dynamic_schur_forest` (Round 038).
- `aesp_cd_l1_rppr.bounded_degree_speculative_stop` (Round 039).

The full tier includes the optional P7 corroborating trace. These audits check
the scoped exact identities and source guardrails; they do not promote the
open graph-uniform theorem.
