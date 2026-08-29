# Research notes

This file is the current project-level map of exploratory results, blockers,
and promotion gates. It is not a chronological lab notebook. Detailed proof
state belongs in each note's `STATUS.md`; accepted historical handoffs are
preserved in the immutable
[`research-round archive`](../manuscript/notes/_shared/coordination/rounds/).
The machine-readable note map is
[`registry.toml`](../manuscript/notes/registry.toml).

Last synchronized: 2026-08-29, after the point-source envelope and dynamic
event-interface audit.

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
The RPPR support is also not merely the positive connected component of the
ordinary shifted PPR vector: a three-vertex exact point-source instance has a
strictly active obstacle coordinate whose unconstrained shifted coordinate is
negative.  Any successful reduction must retain nonlinear obstacle/Schur
information.

The classical APPR support sandwich makes the surviving gap especially
precise.  At threshold `rho`, every terminal APPR support contains
`S*(rho)` and is contained in `S*((1-alpha)rho/2)`.  Hence for
`alpha<1/2` it is a certified containing envelope of volume below `4/rho`,
and the point-source radius lemma puts the same envelope within
`O_tilde(1/sqrt(alpha))` hops of the root,
although classical APPR takes tightly `Theta(1/(alpha*rho))` work to build
it.  If this envelope is supplied, accelerated proximal gradient on the
fixed envelope reaches semantic PPR error `eps_ppr` for a general sparse
source in
`nnz(s)+O_tilde(1/(sqrt(alpha)*eps_ppr))` work, without an exact-support
margin.  The square-root radius itself extends to distance from a general
source set; point-source structure makes the construction a single rooted
trace, rather than a collection of components that can merge.  It is not
needed for the terminal oracle solve.
The ordering-independent APPR star already has envelope radius at most one
and volume `Theta(1/rho)` while spending `Omega(vol(E)/alpha)` work, so the
gap is repeated state processing rather than distant or oversized output.
The universal point-source problem is therefore exactly accelerated
construction or dynamic reuse of an output-sized envelope, not an
output-volume existence question.

A point-source rho-homotopy still reveals useful extra structure.  On a fixed
face every boundary key is affine in rho, and after admitting one vertex each
surviving critical rho becomes a nonnegative weighted average of its previous
value and the admitted maximum.  This monotone mixing is exact, but the
weights differ by boundary row: a six-vertex rational instance reverses two
candidates' order.  Homotopy therefore replaces the fully arbitrary rekey
problem by dynamic maxima under row-dependent rank-one mixtures, not by an
ordinary lazy heap.

There is, however, an exact positive algorithm behind this identity.  If the
current exterior Schur complement is kept explicitly, admitting a largest
critical ratio is exactly one Stieltjes pivot; each support coordinate enters
once, and the first largest ratio below the target rho is the global KKT
certificate.  With delta_v denoting the realized Schur-fill degree at the
pivot, discovery costs

```text
O_tilde(vol(S*) + sum_v (1+delta_v)^2).
```

Thus bounded homotopy elimination width gives a genuine point-source
product-scale solver after the existing final-face Chebyshev step.  This is a
structural breakthrough, not yet a general-graph one: explicit fill can be
quadratic even when an implicit tree or separator reporter would be linear.
For finite accuracy, the homotopy does not require exact breakpoint
separation: every exterior affine-key slope lies between `alpha*d_v` and
`(1+alpha)*d_v/2`.  A certified additive upper error `eta` on the largest
remaining ratio therefore contributes at most `(1+alpha)*eta/2` to the
degree-normalized KKT diagnostic.  This is the correct interface for an
approximate or sparsified Schur implementation.

The finite reporter now has an alternative harmonic formulation.  Every
exact singleton pivot adds a killed hitting-probability column; these columns
are pairwise orthogonal in the principal Hessian energy, have a telescoping
total-energy budget, and can trigger only logarithmically many finite
coordinate levels.  Chebyshev decay confines each such level event to
`O_tilde(1/sqrt(alpha))` graph distance from its pivot.  Consequently a
dynamic locator charged once per emitted level plus its pivot-to-event route
would close discovery in `O_tilde(vol(S*)/sqrt(alpha))` work.  Ball scans do
not instantiate this interface because ball volume and repeated overlap are
uncontrolled; existing named-coordinate dynamic inverse structures likewise
do not enumerate all one-sided events.

Response accuracy itself is now separated from event location: a
degree-weighted residual norm gives simultaneous certified intervals for all
coordinates of an approximate killed-harmonic response. Choosing summable
per-pivot residual budgets changes only logarithmic solve accuracy and fits
inside the finite KKT hysteresis. The open operation is therefore exhaustive
event-coordinate reporting, not exact response evaluation.

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
