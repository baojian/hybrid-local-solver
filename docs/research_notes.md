# Research notes

This file is the current project-level map of exploratory results, blockers,
and promotion gates. It is not a chronological lab notebook. Detailed proof
state belongs in each note's `STATUS.md`; accepted historical handoffs are
preserved in the immutable
[`research-round archive`](../manuscript/notes/_shared/coordination/rounds/).
The machine-readable note map is
[`registry.toml`](../manuscript/notes/registry.toml).

Last synchronized: 2026-08-24, after the Round-027 review and repository
organization audit.

## Fixed end-to-end target

The primary audit target is an exact-real algorithm on a finite simple
undirected unweighted graph with no isolated vertices and adjacency-list
access. Its canonical source is one vertex, `s=e_v`. Let

```text
x0     = Q^-1 b,
pi     = D^1/2 x0,
pi_hat = D^1/2 x_hat.
```

The algorithm must return sparse `x_hat` with

```text
max_i |pi_hat_i-pi_i| / d_i <= eps_ppr,
```

one complete terminal certificate, and one terminal return. The charged work
includes seed input, discovery, every repeated row read, inner update,
correction/rekey, response operation, certificate query, materialization,
state read/write, and output write. The desired point-source bound is

```text
O_tilde(1/(sqrt(alpha) eps_ppr)).
```

The shared problem definition continues to allow a general sparse
distribution. By linearity, a proved point-source PPR solver gives the
general-seed corollary

```text
nnz(s) + O_tilde((sum_v sqrt(s_v))^2/(sqrt(alpha) eps_ppr)).
```

This is not the formerly requested additive `nnz(s)` bound: for a uniform
`k`-point source the extra factor is `k`. RPPR obstacle solutions are
nonlinear in `s`, so their point-source runs cannot be superposed before the
final unregularized PPR approximation is formed. Claims that use connected
support, rooted exploration, or the support-radius bound are therefore
point-source claims.

The point-source restriction is a genuine simplification, but it does not by
itself close dynamic support discovery.  A proved fan family has every graph
vertex adjacent to the source while the exact rule that solves the current
face and admits every positive exterior key still takes a linear number of
nonempty batches.  Thus radius controls route length, not the number of
response changes or restricted-face rebuilds around one root.

An RPPR route must state its regularization conversion, such as
`rho=tau=eps_ppr/2`, and its terminal certificate. Exact-real means algebraic
cell arithmetic, not exact-minimizer output or a floating-point/bit result.
For `alpha` bounded below by a constant, monotone coordinate descent remains
an allowed fallback. This is a target contract, not a proved theorem.

## AESP--LOCSOR promotion gate

Keep
[`hybrid_aesp_locsor`](../manuscript/notes/hybrid_aesp_locsor/)
as a standalone rigorous research note. Do not promote its graph-uniform
end-to-end complexity claim into the active manuscript until either:

1. the central early-AESP locality lemma

   \[
   \Lambda_J
   := \max_{1\leq t\leq J}
      \frac{\overline{\operatorname{vol}}(S_t)}{\gamma_t}
   = O(1/\epsilon)
   \]

   is proved with a graph-independent hidden constant; or
2. a correct weaker structural condition or alternative burn-in work argument
   sufficient for the stated manuscript theorem is proved.

Until then, the proved trajectory-dependent theorem and explicitly
conditional confinement corollaries may be developed, but the universal
`O_tilde(1/(sqrt(alpha)*epsilon))` work bound is open.

## Current proof fronts

| Direction | Established boundary | Next falsifiable target |
| --- | --- | --- |
| [`aesp_cd_l1_rppr`](../manuscript/notes/aesp_cd_l1_rppr/) | Safe centers, finite residual interfaces, persistent `Q`-energy banks, and high-Dirichlet acceleration are proved. The lagged Euclidean reserve has only `q^2` drift; the simplest unsplit weighted bank fails a stagewise `cq` contraction. | Prove a windowed, spectrally split, nonlinear, or differently normalized low-Dirichlet Lyapunov for the actual finite sequence. |
| [`hybrid_aesp_locsor`](../manuscript/notes/hybrid_aesp_locsor/) | Structured response handoffs and two nonsettled continuations are proved. A settled path makes the observable reset/drop ratio `Theta(1/alpha)`, without yielding a work lower bound. | Pay multiple actual nonsettled reset budgets with a nonadditive/logarithmic ledger, or prove a weaker structural burn-in theorem. |
| [`volume_gated_acceleration`](../manuscript/notes/volume_gated_acceleration/) | The support cap and exact finite path/nonpath causal ledgers are proved in scope. Restarted credit need not recover before the next admission. | Prove all-history solvency under an explicit structural condition or find debt surviving several admissions. |
| [`response_preconditioned_hybrid`](../manuscript/notes/response_preconditioned_hybrid/) | Fixed-face response packing and structured delta reporters are proved. One pivot repairs a three-label reweight collision; general explicit Gram state is quadratic. | Find sparse collision-sensitive state or a geometrically paid replay/rebuild theorem under repeated reweighting. |
| [`propagate_settle_framework`](../manuscript/notes/propagate_settle_framework/) | Several exact settlement/absorption rules are proved on named graph families; the latest double-cycle candidate is retired in its prescribed scope. | Find a different cyclic coupling or bounded-degree settlement gadget with seed chronology proved first. |
| [`local_solver_oracle_hierarchy`](../manuscript/notes/local_solver_oracle_hierarchy/) | Output/capacity bounds and resource separations are proved. Broad supported-prefix product lower bounds are defeated by constant-prefix or sparse-basis counteralgorithms. | Defeat both residual-slack spreading and delayed sparse-basis synthesis, or state a narrower justified model. |

All remaining direction targets, evidence classes, and formal dependencies are
kept in `registry.toml`; use `make note-targets` and `make note-graph` rather
than duplicating them here.

## Reusable conclusions

- The classical APPR upper bound `O(1/(alpha*eps_appr))` is worst-case tight
  on the center-seeded star in the theorem regime. The baseline implementation
  and ordering-independent regression remain in `src/baselines/`,
  `tests/test_appr_lower_bound.py`, and
  `experiments.check_appr_lower_bound`. Path/spider diagnostic rows are not
  theorem checks.
- Fixed RPPR regularization gives a support-volume cap, and safe lower centers
  make local proximal calls oracle-free on certified envelopes. This settles
  local call correctness, not expanding-face accelerated amortization.
- Persistent response state can eliminate repeated solves on paths and other
  structured families, but a graph-uniform output-sensitive boundary
  interface is still missing.
- Orthogonality and energy packing explain why mixed response/frontier methods
  are promising. Dense response application or boundary materialization must
  remain explicit in every claimed work bound.
- Several exact witnesses close tempting proof templates without establishing
  broad solver lower bounds. A STOP for a recurrence, representation, or
  scalar bank must retain that qualifier.

## Round-027 boundary

Round 027 proves an actual-finite lagged Euclidean reserve whose unconditional
comparison yields only `Theta(q^2)` drift. It also proves that direct payment
of the reachable K8 pulse forces a positive coefficient in the lagged unsplit
`q^-1 Q` bank, while a reachable persistent K2 stage then has only `O(q^2)`
relative decrease. The K2 trajectory nevertheless has accelerated global
decay after a logarithmic startup normalization, and the K8 high-band payment
ratio tends to `14641/32256`. Therefore the result stops one stagewise unsplit
template; it is not a net-rate obstruction, an additive-resistant
counterexample, or a solver theorem. Full equations and review provenance are
in [`Round 027`](../manuscript/notes/_shared/coordination/rounds/2026-08-23-round-027.md).

## Evidence and promotion discipline

- `main.tex` plus included section files are proof authority for a direction;
  `STATUS.md` records its current operational state.
- Exact and seeded numerical proof audits live in
  [`experiments/proof_audits/`](../experiments/proof_audits/) and are indexed
  by mechanism, with round number retained only as provenance.
- Numerical tables and graph searches remain measured scaffolding unless a
  theorem explicitly promotes them.
- Promote material to the active manuscript only after its dependencies are
  proved or the claim is narrowed to a correct conditional statement.
- Preserve refuted routes and corrections in the owning note and round record;
  do not keep copying their full history into this current-state file.
