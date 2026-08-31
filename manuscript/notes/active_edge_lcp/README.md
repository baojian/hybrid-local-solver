# active_edge_lcp

This standalone note proves OP2 through the obstacle/LCP formulation in the
canonical RPPR normalization.  The reduction is exact:
`c=b-alpha*rho*D^(1/2)1`, `x>=0`, `w=Qx-c>=0`, and `x_i w_i=0`.

The decisive result is a threshold-batch energy-depth theorem.  Order the
unknown optimal support by its safe admission batches and block-factor its
principal Stieltjes matrix.  Retaining only the diagonal and first block
subdiagonal of the Cholesky factor gives a block-bidiagonal M-matrix with
singular values in `[sqrt(alpha),sqrt(2)]`.  Chebyshev inverse decay on that
block chain proves

```text
face_gap(J) <= 8 q_alpha^(2J) + threshold^2/(alpha*rho),
q_alpha = (sqrt(2/alpha)-1)/(sqrt(2/alpha)+1).
```

The distributed threshold term pays every delayed or numerically ambiguous
release once.  It requires no strict-complementarity or sign-separation
margin.

With `threshold=(1/8)*sqrt(alpha*rho*eps_obj)`, only
`O(alpha^(-1/2) log(1/eps_obj))` batches are needed.  Each batch constructs
and solves the currently exposed degree-coordinate SDD face from scratch in
nearly-linear local work.  An exact active-row residual test certifies each
randomized solve; capped independent retries supply the declared failure
probability without attributing an unsupported probability interface to the
SDD black box.  The accepted face is scanned once more and every certified
boundary residual above threshold is admitted.  Every admitted row lies in the true
support, so each phase has volume at most `1/rho`.  The resulting randomized
high-probability algorithm has fully charged expected work

```text
O_tilde(1/(rho*sqrt(alpha)) * log(1/eps_obj)),
```

including discovery, degree and adjacency access, fresh solver state,
candidate accumulation, repeated scans, numerical accuracy, materialization,
orthant projection, and output.  There is no supplied support or global
preprocessing.  The theorem is in the exact-real algebraic word model with a
declared certified-retry failure probability; deterministic bit complexity and a
specific floating-point stability theorem remain separate.

The note retains earlier reusable results: safe batched pivots, the
margin-free approximate-face dichotomy, the exact energy/slack telescope, an
activation-once endpoint-path `LDL^T` solver, the fully charged resource
ledger, and the exact four-vertex counterexample to coordinatewise-monotone
ordinary/projected face CG.

Run the focused audits with:

```bash
python3 verify_counterexample.py
python3 verify_threshold_dichotomy.py
python3 verify_path_ldl.py
python3 verify_batch_depth.py
python3 verify_batch_depth_high_precision.py
make
```

The primary-source map is `docs/literature/lcp-solvers.md`.
