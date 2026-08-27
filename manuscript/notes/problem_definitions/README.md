# Problem definitions

This standalone reference note collects the exact PageRank and regularized
PageRank (RPPR) problems used by the project, their equivalent lazy,
non-lazy, symmetric, mass-coordinate, and degree-coordinate formulations, and
standard source-backed properties of those problems.

The note deliberately contains no algorithm, new theorem, experiment,
complexity target, or open conjecture. In particular, it does not adopt a
repository-wide residual or stopping rule. It distinguishes the semantic PPR
output error, a sufficient document-scoped residual certificate, the RPPR
regularization scale, objective error, and algorithm-specific diagnostics.

Build with `make`. The reference text is in `main.tex`; its source and scope
ledger is in `STATUS.md`.
