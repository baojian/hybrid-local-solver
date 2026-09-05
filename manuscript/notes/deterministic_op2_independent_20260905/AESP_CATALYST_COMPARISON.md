# Relation to AESP and Catalyst

This comparison was requested after the independent proof was completed. It is
context, not a claim that generic acceleration was invented in this task.

**Source.** Catalyst approximately minimizes
`F(x) + kappa*||x-y||^2/2`, then extrapolates between successive solutions.
It balances an inner solver, improved subproblem conditioning, warm starts, and
inexactness tolerances. Deterministic inner solvers are allowed. See
[Lin, Mairal, and Harchaoui, Algorithm 1 and Sections 1.2–2](https://jmlr.org/papers/volume18/17-748/17-748.pdf).

**Source.** AESP explicitly instantiates localized Catalyst-style updates with
LocGD or LocAPPR inner solves. Its local analysis uses weighted residual decrease
and evolving active sets. Its principal PPR theorem concerns degree-normalized
infinity error and a bound involving `R^2/eps_ppr^2`; Section 3.4 discusses
unresolved localization for the regularized formulation. See
[AESP v4, Sections 2.2–3.4, Eq. (5), and Theorem 3.6](https://arxiv.org/html/2510.08010v4#S2.SS2).

| Feature | Catalyst / AESP | This algorithm |
| --- | --- | --- |
| Acceleration location | Between approximate proximal solves | Direct projected correction updates within each stage |
| Quadratic curvature | The proximal term changes Q to Q + kappa I | Q is unchanged |
| Continuation parameter | Quadratic proximal regularization | Sparsity penalty r decreases toward rho |
| Projection | Full-objective proximal computation | Box and mass-cap projection through a scalar threshold |
| Local-work argument | AESP supplies a specialized local inner-solver analysis | Second energy and cumulative repeated support-volume accounting |

**Comparison/inference.** The methods share Nesterov acceleration, auxiliary
states, and controlled approximation. The extra content in this proof is the
particular feasible correction set, diffuse-source invariant, sector inequality,
and complete local-work ledger. Projection is itself a proximal map of a
constraint indicator, but it is not the full-objective proximal solve used by
Catalyst. Changing `r` does not improve Q's condition number.

The distinction is not randomized versus deterministic. Neither generic
Catalyst convergence nor a PPR infinity-error theorem automatically supplies
the OP2 objective-gap/support guarantee. A direct runtime comparison must match
the target and accuracy; no empirical superiority or literature-wide novelty
claim is made here.
