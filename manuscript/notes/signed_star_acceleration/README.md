# Signed star acceleration

This standalone note proves that optimal signed SOR reaches the project’s
degree-normalized semantic PPR accuracy on a center-seeded star in
`Theta(1 / (sqrt(alpha) * eps_ppr))` charged work.  The upper bound uses an
exact cancellation in the two-mode star dynamics and removes the
`log(1 / alpha)` incurred by the usual residual certificate.

The note also separates four different ways in which “local acceleration” can
fail:

- for `0 < alpha <= 1/16`, nonnegative-residual one-hop methods need
  `Omega(1 / (alpha * eps_ppr))` work on the same center-star;
- standard FISTA can activate an arbitrarily high-degree center even when the
  RPPR optimum is supported only on its seed leaf;
- literal ASPR can pay for repeatedly solving every growing path prefix;
- a certificate-stopped signed method can appear logarithmically slower even
  when its semantic error has already reached the target.

These are algorithm- and model-specific results.  They do not prove the
project’s graph-uniform accelerated local-solver target.

Build and verify from this directory:

```bash
make
python3 verify_star.py
```
