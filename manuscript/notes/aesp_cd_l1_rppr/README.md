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
actually explored stage volume.  This raw analysis initially leaves the task
of proving $V_{\max}^{\rm exp}=O(1/\rho)$ or enforcing that cap.
For a certified lower center, the cap is automatic: the shifted minimizer,
proximal warm start, and every greedy coordinate iterate stay between the
center and the RPPR optimum.  Thus each safe-centered proximal call is
oracle-free and costs $\widetilde O(1/\rho)$.  A local retraction converts any
signed finite-support trial point into such a lower certificate.  For the
resulting safeguarded recurrence, the
stage-start KKT masses telescope to at most $1-\alpha$, with no
$1/\alpha$ loss.  The note also derives the exact correction term in the
Nesterov potential and a Euclidean progress telescope for it.  A three-vertex
path refutes pointwise momentum nonexpansion, so the remaining proof obligation
is the sharper amortization that combines this defect formula with the
proximal-displacement collapse identity.  A multiplicative potential ledger
now reduces that obligation further to bounding cumulative log-inflation;
each correction inflates the classical potential by at most a factor two.  An
exact single-edge family with a singleton optimal support has a full
correction every other stage, and hence logarithmically many charged
correction/rekey calls for logarithmic terminal accuracy after only one
support discovery.  Every such correction has $\gamma_t<1$, however, so the
family has $\mathcal I_T=0$.  It refutes raw correction-count amortization,
not the still-open bound on harmful normalized inflation.  The note now
upper-bounds that positive part: every $\log\max\{1,\gamma_t\}$ is bounded by a
normalized collateral-clipping charge supported only on coordinates that the
common retraction clips while their extrapolates remain below the optimum.
The charge may be positive on a benign collateral round.  For $t\geq2$, its
clipping amplitude is written exactly through the proximal-displacement
collapse identity.  This is an a posteriori proof charge because it uses the
unknown optimum.  A second exact single-edge family, now with full optimal
support, has a harmful full collateral correction at stage two for which the
charge is asymptotic to $(44/9)q$ while the same-step Euclidean log-error
decrease is asymptotic to $(88/9)q^2$.  It rigorously refutes an
$\alpha$-independent packing of the collateral charge by monotone Euclidean
log-error, even over the first two stages; the same family rules out every
$o(1/q)$ coefficient, including polylogarithmic dependence on $1/\alpha$.
It does not refute packing by a different potential or the collapse history.  Such a cumulative
accelerated-scale packing, or a locally checkable one-sided surrogate,
remains open.

Build with:

```bash
make -C manuscript/notes/aesp_cd_l1_rppr
```
