# AESP--LOCSOR hybrid research note

This directory contains a standalone LaTeX research note that reconstructs the
project discussion on an AESP burn-in followed by a local SOR cleanup. It is a
curated mathematical synthesis rather than a verbatim chat transcript:
source theorems, new derivations, conditional statements, empirical
observations, corrections, and open claims are labeled separately.

Build from this directory with:

```bash
make
```

The note embeds its three-item bibliography so that it can compile without a
BibTeX executable. It deliberately does not modify the active manuscript or
adopt a repository-wide residual convention. Its PageRank normalization and
stopping certificate are scoped to the note and follow the symmetric
quadratic used in the AESP paper.

The main proved results in the note are:

- finite convergence of the AESP-to-LOCSOR hybrid after every finite handoff;
- an `O(1/(sqrt(alpha) * epsilon))` LOCSOR tail after a certified
  objective-gap or weighted-gradient-mass handoff;
- a trajectory-dependent end-to-end work theorem;
- a confinement-based corollary that yields the target total work under an
  explicit early-stage locality condition.

The graph-uniform early-AESP locality lemma remains open and is stated as such.
