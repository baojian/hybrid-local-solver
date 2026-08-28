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
that contracts by at least `3/8` in `ceil(log(2)/q)` exact fixed-face stages,
independently of event density.  The remaining pulse obstruction is therefore
concentrated in the constant low mode.  This high-bank estimate now has a
finite-inner root perturbation with a discounted residual budget.  For the
low mode there is an exact dichotomy: mean overshoot contracts its Moreau bank
by `1-q` in one step, while every non-overshoot correction is forced by the
infinity norm of the mean-free trial residual.  Combining the master high
root with the exact forced mean recurrence gives a two-scale epoch potential:
a quiet `ceil(2/q)` same-point-restart epoch contracts it below `0.407`, and
an epoch whose observable weighted mean deficit is at most one quarter still
contracts by `3/4`.  A reachable `K_N` family proves that this high-to-low
transfer cannot be paid by a graph-uniform high-bank coefficient: even after
a `1/q` rescaling the required coefficient is greater than `(N-1)/15`.
Thus a local, infinity-norm, or volume-sensitive payment for the weighted
mean deficit is still needed.
The common-cap truncation ledger is also joint: correction and surviving
momentum `Q`-energies share one copy of the telescoping energy drop.

The live target is to pack the weighted face-gain and correction-event terms
in the epoch ledger, then transfer the explicit restart protocol to the actual
finite safeguarded sequence.
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

Build the note from the repository root with:

```bash
make -C manuscript/notes/aesp_cd_l1_rppr
```

Run all ten exact audits with:

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

The full tier includes the optional P7 corroborating trace. These audits check
the scoped exact identities and source guardrails; they do not promote the
open graph-uniform theorem.
