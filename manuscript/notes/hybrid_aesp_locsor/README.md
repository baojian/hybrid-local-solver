# AESP--local-refinement hybrid research note

This directory contains a standalone LaTeX research note that reconstructs the
project discussion on an AESP/Catalyst burn-in followed by momentum-free local
refinement. It is a curated mathematical synthesis rather than a verbatim chat
transcript: source theorems, new derivations, parameterized results,
conditional statements, empirical observations, corrections, and open claims
are labeled separately.

Build from this directory with:

```bash
make
```

The note embeds its bibliography so that it compiles without a BibTeX
executable. It deliberately does not modify the active manuscript or adopt a
repository-wide residual convention. Its PageRank normalization and stopping
certificates are scoped to the note.

The main established results are:

- finite convergence of AESP-to-LOCSOR after every finite signed handoff;
- objective-gap and weighted-gradient-mass LOCSOR tail bounds;
- a master handoff inequality for arbitrary Phase-I methods;
- an unconditional, run-dependent
  `O(R / (alpha^(3/4) * epsilon))` AESP-plus-LOCSOR bound;
- a trajectory-dependent theorem and a confinement-based
  `O_tilde(1 / (sqrt(alpha) * epsilon))` corollary;
- weighted contraction and residual-to-solution certificates for the RPPR
  proximal map, proving convergence of a composite Catalyst-to-ISTA hybrid.

The graph-uniform early-AESP locality lemma and the graph-independent RPPR
local-work theorem from an arbitrary accelerated warm start remain open and
are stated as such.
