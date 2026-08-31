# seed_maximum_principle

This note proves a degree-normalized maximum principle for personalized
PageRank.  If `pi` is seeded at `v`, then `pi_u / d_u <= pi_v / d_v` for
every vertex `u`.  Reversibility therefore gives the exact response-row
identity

```text
pr(e_u)_v / pi_v = (pi_u / d_u) / (pi_v / d_v) <= 1.
```

The result corrects an inverted degree ratio in an earlier proof-campaign
transcription and closes the associated general-graph terminal-potential
question: every nonnegative residual obeys

```text
(H^-1 r)_v / pi_v <= ||r||_1 / gamma_alpha.
```

Consequently, monotone one-hop lower bounds extend to nonnegative output maps
of column mass `B` on every connected graph, with terminal potential at most
`eps_ppr * vol(V) / (1 - gamma_alpha B)` whenever
`gamma_alpha B < 1`.

Build with `make`.  The proof and scope limits are in `main.tex`; the
operational handoff is in `STATUS.md`.
