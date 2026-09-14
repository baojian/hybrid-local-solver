# Standalone reader and dependency review

Scope: the authorized `problem_definitions/main.tex`,
`deterministic_conjecture2.tex`, `practical_refinements_appendix.tex`, and
`practical_schedules_appendix.tex`. This is a presentation review for an
expert reader, following the completed correctness audits. No TeX was
edited, and no other manuscript note was inspected.

**Conclusion:** the proof has no newly identified circular dependency,
unstated support oracle, or mathematical correctness gap. Three specific
presentation corrections should be made; a few short bridge equations
would further improve independent readability.

**Follow-up:** root applied all three corrections, and a fresh inspection
passes. The new two-tree paragraph supplies the common-integer
decomposition, disjoint registry, four physical breakpoint sequences, and
sequential rank-exclusion search. The optional direct-exception transition
is restricted to intervals with no query and retains its record charges.
The new geometric-checkpoint subsection agrees with the independently
audited current-candidate certificate, cache completeness, geometric work,
temporary disposal, H-squared encoding, and manual invalidation arguments.
The items below are retained as the record of the review; only the optional
explanatory bridges remain suggestions.

## Corrections needed for a standalone exposition

1. **Explain the two-tree reporter before using its sharper complexity.**
   The main text constructs one ordered tree with two translated breakpoint
   lists and conservatively charges O(log^3 N). The final arithmetic
   subsection invokes two trees, four sequences, and O(log^2 N), but the
   intervening appendix does not construct this variant. The refined
   cubic-log bound therefore depends on an implementation detail that the
   reader cannot recover from the TeX alone.

   A sufficient addition after `app:weighted-key` is one paragraph and a
   display: write `W_i=B_i+E_i/sigma`. The physical pre-shift density is
   `(sigma*B_i+E_i)/d_i`. Put exactly the E_i=0 records in a base tree ordered
   by B_i/d_i, and all other records in a disjoint exception tree ordered
   by `(sigma*B_i+E_i)/d_i`. Degree-weighted moments have common integer
   denominators by the preceding argument. The base order survives a
   positive scale change; only the charged exception set is refreshed.
   Evaluate clipped mass using both trees' lower and upper tails. Binary
   search each of the four sorted breakpoint sequences for the crossing,
   using O(log N) rank/tail work per test; their predecessor/successor
   brackets locate the final affine interval in O(log^2 N) total work.
   Closed-tail emission remains as in `app:closed-tail`.

2. **Do not reuse E_k for energy and a selected-coordinate set.** In the
   main signed-flow section, rename `{i:V_(k+1,i)>V_i*}` to a distinct set
   symbol such as I_k. E_k already denotes the accelerated energy and is
   used in later references to the two-energy proof.

3. **Do not reuse the regularization r as an output residual vector.**
   The independent-certificate subsection currently sets
   `r=Qx-b+alpha*rho*w`, while the appendix declares r to be stage
   regularization and the next checkpoint subsection divides by r.
   Rename this residual to `r^{out}` or `g^{out}` throughout that subsection.
   The earlier omega change correctly resolved the distinct seed-v collision.

These are local additions/renamings; none changes the algorithm or proof.

## Short bridge equations worth adding

The existing lemma proofs are largely detailed enough for an expert. The
following small additions eliminate the main remaining implicit steps:

- At the first use of the correction objective, state
  `J(xi)=J_r(bar+xi)-J_r(bar)` and
  `Q xi* -s+lambda*w=r*`, `r*^T xi*=0`. Thus the displayed stage gap is
  exactly the original objective gap, and xi* is its feasible minimizer.
  The appendix already gives the objective identity, but the core theorem
  uses it before the appendix is reached.
- Define metric notation once:
  `<u,v>_M=u^T Mv`, `||u||_M^2=u^TMu`, and
  `grad_M f=M^{-1}grad f`. Then the auxiliary identity can be checked from
  `grad_Q A=Q^{-1}[Q(Qxi-s)+alpha*lambda*w]=Qxi-s+lambda*w` using
  `Q^{-1}w=w/alpha`. This makes explicit which gradient the general
  comparison lemma uses.
- Before the selected-flow inequality, insert its direct intermediate
  bound on I_k:
  `e_(k+1,i)+R_i* <= beta0(K0 e_k)_i-beta0(K0 n_k^-)_i+H_(k,i)`.
  Summing, dropping the nonpositive term, and using column stochasticity
  proves the displayed inequality. This also explains the currently
  introduced but otherwise unused n^- and why unselected positive forcing
  cannot replace the selected signed sum.
- In the reporter section, state the exposure invariant explicitly: every
  row that acquires positive primal or kinetic state has been scanned, so
  each neighbor is exposed. Hence an unexposed vertex has not only zero own
  state/source but also zero response from such neighbors. This is the
  exact reason its raw value is negative; zero own coordinate alone would
  not suffice.

These are recommended explanatory bridges, not repairs to invalid algebra.
For example, the comparison lemma already supplies the required weighted
strong-convexity cancellation and the projection-sector proof already
checks the three normal types separately; neither needs to be replaced by
an appeal to an external acceleration theorem.

## Dependency and model check

The logical chain is acyclic:

    canonical spectral/KKT facts -> monotonicity and analytical core margin
    diffuse baseline -> feasible analytical comparators and both energies
    second energy -> uniform squared response -> repeated kinetic-volume bound
    approximate repair -> next diffuse baseline and final safe objective gap
    local reporter + the preceding volume bound -> fully charged implementation.

The dense mathematical trajectory may be defined before its local
implementation is described; this is not a free-support assumption. The
reporter subsequently realizes that trajectory through discovered records.
Neither the analytical core nor either comparison optimum is queried.
Source construction, newly exposed degrees, repeated edge reads, historical
primal materialization, and discarded state all have stated charges.
The final reporter volume bound also controls its own exposed-record
logarithm, rather than leaving an unrestricted dependence on graph size.

The original theorem matches canonical OP2's point seed, additive objective
accuracy, charged exact-real word model, and permitted local logarithms.
The rational appendix separately pays floors, coefficient lengths, and
encoded graph replies. Scalar rebasing has its own perturbation proof;
it is not inferred merely from exact-real convergence. The optional
checkpoint proof checks the actual full candidate, keeps the same dynamics,
and charges unsuccessful checks and reclamation geometrically. Zero-step
initialization and final repair remain present.

One optional reading aid is a three-row repair-budget table distinguishing
the main exact clipping repair (`tau=alpha^3*delta^2/2`), exact terminal-PG
repair (`tau<=alpha*delta^2/2`), and rounded terminal-PG construction
(`tau=alpha*delta^2/8`). These are separate sufficient budgets, not
inconsistent definitions. No new hypothesis is needed to reconcile them.

The verification/status paragraphs are supporting context rather than
premises. An expert can verify the theorem without obtaining the separate
research audits or running code, after the two-tree construction above is
made explicit.
