# AESP-CD RPPR note

This standalone note proposes a composite AESP outer loop with local proximal
coordinate descent for the shared regularized PageRank model.  The weighted
KKT-mass decrease, diagnostic-to-solution-error conversion, and local
inner-oracle work bound are proved for arbitrary signed iterates.  The
contraction and error certificate are also stated for any separable
$\ell_1$-regularized Stieltjes quadratic with a positive supersolution.  The
note gives the resulting cumulative inner-work interface for a composite AESP
outer loop, with no sign restriction on its extrapolated centers.  The raw
absolute-gap interface is shown to be intrinsically too coarse at an
$\ell_1$ kink.  Using the relative Catalyst criterion, a proximal warm start,
and greedy coordinate selection gives $\widetilde O(V/\sqrt\alpha)$ total
work on any fixed certified envelope of degree volume $V$.  An optimal-support
oracle gives $V\leq1/\rho$ and the target
$\widetilde O(1/(\rho\sqrt\alpha))$ bound.  Without an oracle, the same local
heap implementation has a trajectory-dependent
$\widetilde O(V_{\max}^{\rm exp}/\sqrt\alpha)$ bound in terms of the maximum
actually explored stage volume.  The remaining graph-uniform task is to prove
$V_{\max}^{\rm exp}=O(1/\rho)$ or enforce that cap without repeated restarts.
For a certified lower center, the cap is automatic: the shifted minimizer,
proximal warm start, and every greedy coordinate iterate stay between the
center and the RPPR optimum.  Thus each safe-centered proximal call is
oracle-free and costs $\widetilde O(1/\rho)$; preserving the accelerated
outer rate while keeping all centers lower is the remaining continuation
problem.  A local retraction converts any signed finite-support trial point
into such a lower certificate, but a proof that repeated retraction preserves
the accelerated outer rate is not asserted.

Build with:

```bash
make -C manuscript/notes/aesp_cd_l1_rppr
```
