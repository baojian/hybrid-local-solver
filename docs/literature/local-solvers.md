# Local Solvers

## Scope

This note covers algorithms designed to exploit locality in PageRank or
related graph problems. Candidate areas from the current research plan include
APPR, evolving-set methods, AESP, LocGD, LocCH, and LocSOR.

## Questions for comparison

- What mathematical problem and `alpha` convention does the method use?
- What residual, normalization, and stopping criterion does it use?
- How is the active or local set selected and updated?
- What convergence guarantee is proved?
- How are work, volume, and edge operations counted?
- Which assumptions are needed for locality?
- Can accuracy and work be compared directly with this project, or is an
  explicit conversion required?

## Source annotations

No source has been annotated yet. Add each paper using the template in
[`README.md`](README.md), with exact page or section pointers.
