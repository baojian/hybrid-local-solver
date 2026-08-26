# bounded_seed_return

This note proves a graph-uniform upper bound on the seed diagonal of the
discounted PageRank Green kernel.  If `d_v` is the ordinary degree of the
seed, `gamma_alpha = 2 alpha / (1 + alpha)`, and `V_G = vol(G)`, then

```text
pi_v / gamma_alpha
  <= d_v / (V_G gamma_alpha)
     + 1 / (1 + c_alpha)
     + 2 pi d_v / sqrt(c_alpha gamma_alpha).
```

Consequently, along any joint limit with `alpha -> 0`, `eps_ppr -> 0`,
bounded `d_v`, and `vol(S_eps_ppr) = Theta(1 / eps_ppr)`, one has
`alpha pi_v / gamma_alpha -> 0`.  Thus no bounded-seed-degree family can
combine support-volume saturation with the star's
`Theta(1 / alpha)` self-return amplification.

The note closes only this self-return mechanism.  It does not prove an upper
bound for signed one-hop relaxation and does not exclude a distributed class
lower bound whose work is forced away from the seed.

Build with `make`.  Run the deterministic formula and graph-zoo screen with
`python3 verify.py`.  The claim ledger and resume point are in `STATUS.md`.
