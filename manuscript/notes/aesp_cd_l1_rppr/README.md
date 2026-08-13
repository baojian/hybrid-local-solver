# AESP-CD RPPR note

This standalone note proposes a composite AESP outer loop with local proximal
coordinate descent for the shared regularized PageRank model.  The weighted
KKT-mass decrease, diagnostic-to-solution-error conversion, and local
inner-oracle work bound are proved for arbitrary signed iterates.  The
contraction and error certificate are also stated for any separable
$\ell_1$-regularized Stieltjes quadratic with a positive supersolution.  The
note gives the resulting cumulative inner-work interface for a composite AESP
outer loop, with no sign restriction on its extrapolated centers.  The
graph-uniform outer-locality theorem remains open because Catalyst
extrapolation can make the shifted subproblems' initial KKT masses large.

Build with:

```bash
make -C manuscript/notes/aesp_cd_l1_rppr
```
