# ASPR 2023 correctness and tightness audit

This standalone research note audits the accelerated sparse PageRank method
(ASPR) of Martinez-Rubio, Wirth, and Pokutta (COLT 2023). It separates the
intended theorem from formula-level defects in the published text, gives a
corrected exact-arithmetic contract, and proves an algorithm-specific path
lower bound.

Build from this directory with:

```bash
make
```

The central conclusions are:

- the ASPR support-safety and objective-gap proof is valid after three
  essential formula repairs;
- endpoint-seeded RPPR paths force exactly one active-set expansion per outer
  stage;
- for sufficiently small objective tolerance, literal ASPR has work
  `Omega(|S*|^2 / sqrt(alpha))` on those paths, matching its leading published
  upper bound up to logarithms;
- repeated full-gradient discovery separately costs `Omega(|S*|^2)` under
  literal recomputation;
- the concrete scaling `alpha = |S*|^{-2}`, `rho = alpha / 100`, and
  `eps_obj = 10^{-4} alpha^2` gives same-tolerance work
  `Omega(|S*|^3 log |S*|)` for literal ASPR versus
  `O(|S*|^2 log |S*|)` for standard FISTA;
- the later official Julia plots generally show default ASPR faster than the
  included FISTA and ISTA baselines, with CASPR fastest, so they do not support
  a blanket claim that ASPR is empirically slow;
- the official periodic-gradient option deletes the active-to-boundary matrix
  block and therefore cannot trigger early RPPR discovery; its extra work and
  the in-place retraction defect are documented in the note;
- even a corrected early-discovery variant needs `|S*|` successful path-layer
  discoveries and `Omega(|S*|^2)` work if it freshly scans every active prefix;
- none of these algorithm-specific statements is a lower bound for every
  local PageRank solver.

The note uses objective-gap accuracy only. It does not identify that accuracy
with APPR's degree-normalized residual, the 2026 experimental proximal
fixed-point residual, or a repository-wide stopping rule.
