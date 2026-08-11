# Hybrid Local Solver: Complete Independent Research Note

This directory contains an independent LaTeX research note reconstructed from the project discussions.

The note is intentionally separate from the active manuscript. It consolidates:

- APPR worst-case lower bounds;
- locally evolving-set methods;
- AESP and Catalyst acceleration;
- the AESP--LocSOR hybrid framework;
- SOR relaxation corrections;
- trajectory-dependent complexity bounds;
- early-locality and confinement open problems;
- l1-regularized PageRank extensions;
- proof audits and research directions.

The note distinguishes:

1. proved statements;
2. source results from cited papers;
3. conditional theorems;
4. empirical observations;
5. open conjectures.

Build:

```bash
make
```

The note is not included by `manuscript/main.tex` because the repository-wide residual convention and final theorem statements are still under development.
