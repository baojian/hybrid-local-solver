# Related work and state-of-the-art map

**Last primary-source check:** 2026-08-21.

There is no single scalar ranking of these methods: they solve different PPR,
RPPR, local-clustering, point-query, or linear-system tasks and use different
accuracy and access models. “State of the art” below therefore means the
current comparison frontier for this project's canonical connected,
unit-weight, single-source sparse-vector local PPR and RPPR questions. General
seed distributions and broader graph classes are stronger extensions, not a
claim that one method dominates every regime.

Detailed theorem/page annotations live in
[`../../../../docs/literature/`](../../../../docs/literature/). This page is a
routing map, not a substitute for those source notes.

## Core comparison frontier

| Family | Best source-level message relevant here | Critical boundary for this project | Project route |
| --- | --- | --- | --- |
| ACL/APPR push (2006/2007) | Canonical strongly local approximate-PPR baseline with `O(1 / (alpha * eps_appr))` degree work. | Its activation threshold is not automatically the project's `eps_ppr` solution error. | `docs/literature/local-solvers.md`; active APPR lower-bound ledger. |
| Locally evolving-set iterative methods (NeurIPS 2024) | Localizes standard iterative solvers through evolving active sets and supplies the residual/gradient normalization used by current AESP notes. | Locality depends on the evolving-set work measure and the exact certificate. | `hybrid_local_solver_synthesis`, `hybrid_aesp_locsor`. |
| AESP (NeurIPS 2025) | Accelerated outer process with `O_tilde(1 / sqrt(alpha))` local subproblems and source bound `O_tilde(R^2 / (sqrt(alpha) * eps_ppr^2))` in its stated model. | The desired `1 / eps_ppr` dependence and graph-uniform early-stage locality are not supplied. | `hybrid_aesp_locsor`, `aesp_locgd_star_lower_bound`. |
| ASPR/CDPR (COLT 2023) | Sparse accelerated active-set and conjugate-direction algorithms for the RPPR obstacle formulation. | Literal repeated restricted solves and discovery can incur repeated-prefix work; published formulas require the recorded audit repairs. | `aspr23_bound_audit`. |
| Classical FISTA for RPPR (arXiv 2026) | Conditional accelerated work under confinement, plus a star construction showing that acceleration can destroy locality through transient activation. | Small optimal support alone does not control the active trajectory; the general product-scale theorem remains conditional. | `aesp_cd_l1_rppr`, `volume_gated_acceleration`. |
| Growing-active-set SDD method (Wei--Yang, arXiv 2608.16339v1, 2026) | ACL-approximate PPR in `O_tilde(1 / eps_appr^2)` time with only polylogarithmic dependence on inverse teleportation, plus an RPPR result. | Re-solving and materializing nested active systems can hide a repeated-active-set factor; its accuracy tradeoff differs from the product target. | `incremental_active_set_sdd`. |
| Local SOR / accelerated push | Practical and structural improvements over forward push, including relaxation and momentum-based variants. | Fixed relaxation or measured schedules do not by themselves prove graph-uniform accelerated local work. | `rlsor_terminal_exact_rung`, `two_rung_sor`, `two_rung_direct_theory`. |
| Global SDD, sparsification, and dynamic Schur methods | Nearly-linear global inverse machinery and dynamic spectral vertex-sparsifier/heavy-hitter architectures. | Published preprocessing and update bounds are ambient-graph, not exposure-local; importing them requires a charged local reporter. | `incremental_active_set_sdd`, `response_preconditioned_hybrid`. |

Primary links for the newest comparison boundary:

- [A Simple Active-Set Method for PageRank-Based Local Graph Clustering](https://arxiv.org/abs/2608.16339), posted 2026-08-17;
- [Complexity of Classical Acceleration for l1-Regularized PageRank](https://arxiv.org/abs/2602.21138);
- [Accelerated Evolving Set Processes for Local PageRank Computation](https://openreview.net/forum?id=zDOo34mbpl);
- [Accelerated and Sparse Algorithms for Approximate Personalized PageRank and Beyond](https://proceedings.mlr.press/v195/martinez-rubio23b.html).

## Comparison rules

Every related-work claim records:

- the paper's exact `alpha` convention;
- output task and accuracy measure;
- graph and seed assumptions;
- local access, preprocessing, and work unit;
- whether the result is worst-case, conditional, structural, expected,
  high-probability, or empirical;
- the exact theorem, equation, page, or section pointer.

Do not place `1 / eps_appr`, `1 / eps_ppr`, `1 / rho`, objective gap, or
point-query relative error on one complexity plot without an explicit
conversion theorem.

## Reading routes

- PPR definition and local push: `docs/literature/graph-optimization.md`, then
  `docs/literature/local-solvers.md`.
- Acceleration and RPPR: `docs/literature/acceleration.md`.
- Persistent response and preconditioning: `docs/literature/graph-optimization.md`.
- Complete bibliography and local PDFs: `docs/literature/index.md` and
  `papers/README.md`.

## Literature maintenance

Before calling a new method state of the art, verify the primary paper rather
than a search snippet. Adding a paper or changing publication metadata also
updates `docs/literature/index.md`, the relevant detailed topic file, and the
paper library according to the root instructions. A direction note records
only the source facts it actually uses.
