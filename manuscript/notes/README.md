# Standalone research notes

Each subdirectory is an independently buildable research document.  The
inventory in `manifest.toml` is exhaustive: adding or removing a note requires
updating that manifest in the same change.

All notes import the common shell in
`../tex/shared/research_note_preamble.tex` and the source-aligned PageRank/RPPR
model in `../tex/shared/source_aligned_problem.tex`.  Reusable commands and
scientific notation are declared only under `../tex/shared/`; a note may state
stronger assumptions and introduce explicitly proof-scoped indexed variables,
but it may not redefine a reserved object.  The registry is
`../tex/shared/NOTATION.md`.

| Note | Role | Current boundary |
| --- | --- | --- |
| `aspr23_bound_audit` | COLT 2023 ASPR correctness and tightness audit | Bound is tight for literal ASPR; no local-oracle lower bound is claimed. |
| `aesp_cd_l1_rppr` | Composite AESP with local coordinate descent | Fixed-envelope and trajectory-sensitive accelerated work are proved; safe centers give oracle-free `1/rho` inner locality, while safe accelerated continuation remains open. |
| `aesp_locgd_star_lower_bound` | Center-star stress test | Lower bound is specific to the literal AESP--LocGD loop. |
| `hybrid_aesp_locsor` | Accelerated burn-in plus local refinement | Graph-uniform early-AESP locality is open. |
| `hybrid_local_solver_complete_note` | Proof history and failed routes | Several safeguard/flux directions remain open. |
| `hybrid_local_solver_synthesis` | Broad theory and experiment synthesis | Strong uniform work claims remain conditional. |
| `volume_gated_acceleration` | RPPR support gate and continuation | Expanding-subspace work lemma remains open. |

Build every note from the repository root with:

```bash
make notes
```

Or build one note with `make -C manuscript/notes/<note-id>`.  Generated PDFs
and LaTeX auxiliaries are ignored.
