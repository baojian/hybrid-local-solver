# AESP-LocGD center-star lower-bound note

This directory contains a standalone LaTeX research note that reconstructs
the complete center-star lower-bound discussion for AESP-PPR with the batched
LocGD inner solver. It is a curated mathematical synthesis rather than a
verbatim transcript: source statements, new proofs, conditional arguments,
refuted proof routes, scope limitations, and open directions are labeled
separately.

Build from this directory with:

```bash
make
```

The note embeds its bibliography and deliberately does not adopt a
repository-wide residual convention. Its `epsilon` is the note-scoped AESP
PPR error `||D^{-1}(pi_hat - pi)||_infinity`, and its work is cumulative
active degree volume.

The central proved statements are:

- unconditional work `Omega(B / sqrt(alpha))` on the center-seeded star
  `K_{1,B}` whenever `B * epsilon <= 1/4`;
- `Omega(1 / (sqrt(alpha) * epsilon))` after choosing
  `B = floor(1 / (4 * epsilon))`;
- the graph-budget refinement
  `Omega(min(m, 1 / epsilon) / sqrt(alpha))`;
- a separate first-activation logarithmic delay when unit outer-loop overhead
  is counted.

The result applies to the literal AESP-PPR outer loop and batched LocGD inner
solver. It does not claim a lower bound for arbitrary AESP inner maps,
sequential LocAPPR, RPPR, or every hybrid local method.
