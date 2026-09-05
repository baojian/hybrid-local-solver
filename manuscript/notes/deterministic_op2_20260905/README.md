# Deterministic local RPPR by constrained accelerated continuation

Saved into the repository on 2026-09-06. The research and verification were
completed on 2026-09-05; this directory preserves that work independently of
the active manuscript. It also records the subsequent algorithm explanation,
2026 literature comparison, and limits of the current practical evidence.

The audited theorem gives deterministic, fully charged work
`O_tilde(1/(rho*sqrt(alpha)))` for additive RPPR objective accuracy on finite,
simple, connected, undirected unit-weight graphs with one seed. The algorithm
uses regularization continuation, box/mass-constrained accelerated updates,
and deterministic sparse threshold reporting. It uses no randomized primitive.

## Read in this order

1. [STATUS.md](STATUS.md): exact contract, claim classes, and resume pointers.
2. [main.tex](main.tex), built with `make`: standalone algorithm and pseudocode,
   accelerated stage convergence proof, cumulative local-work proof, safe
   continuation, implementation ledger, and 2026 comparison. The four proof
   and discussion sections live in [sections/](sections/).
3. [proof-audit.pdf](proof-audit.pdf): the complete original 11-page proof audit
   and practical-refinement report, preserved byte for byte.
4. [DISCUSSION.md](DISCUSSION.md): pseudocode, relation to the user's earlier
   notes, 2026 comparisons, and the unproved practical comparison with FISTA.
5. [research-notes/](research-notes/): all 18 original mathematical notes,
   including failed, open, and optional directions.

## Reproducible source and full history

- [archive/solver-package.zip](archive/solver-package.zip) is the portable
  source package: solver, 17 standard-library tests, examples, extended audits,
  proof-to-code map, selected result snapshots, and original report TeX/PDF.
  Extract it outside `manuscript/notes/` to keep archived TeX declarations and
  bundled experimental code separate from the repository's live source tree.
- [archive/research-source.zip](archive/research-source.zip) preserves the
  remaining research source and historical handoffs, including the original
  standalone TeX and proof-source snapshots. Historical `STATUS` and `CURRENT`
  files retain their original dates and may describe unfinished candidates.
- `archive/raw-results-*.zip` preserves the complete remaining experimental
  records, including intentionally stopped campaigns. These records do not
  turn the earlier failed or open algorithms into proved methods.
  Archive 08 is split into two parts to keep each repository file below 10 MB.
  Reconstruct it outside the repository before extraction:

  ```sh
  cat archive/raw-results-08.zip.part1 archive/raw-results-08.zip.part2 > /tmp/deterministic-op2-raw-results-08.zip
  ```
- [ARCHIVE_MANIFEST.json](ARCHIVE_MANIFEST.json) maps each preserved source file
  to an archive/member and its SHA-256. It also identifies excluded environment,
  build, extracted-copy, and third-party download files. No source workspace
  file was removed.
- [RESEARCH_DURATION.md](RESEARCH_DURATION.md) records the completed research
  duration. [VERIFICATION.md](VERIFICATION.md) records the original checks.
  [SAVE_VERIFICATION.md](SAVE_VERIFICATION.md) records compilation, archive
  integrity, portable tests, and the existing broader repository-check failures.

For the portable tests, extract `archive/solver-package.zip` into a temporary
directory and, from its `deterministic-op2-solver` subdirectory, run:

```sh
python -m unittest discover -s tests -v
```

The runtime needs Python 3.10+ and the standard library; extended mathematical
audits use the dependency recorded in the package. All experiments in this
research task were deterministic (random seed: not applicable).

## Attribution and scope

The continuation and two-energy proof originated in the parallel task
**Prove conjecture 2 deterministically**. This task independently audited it
and developed degree pruning, boundary-forest/component certificates,
bounded pilots, integer implementations, early certificates, and the tiny
exact-component shortcut. Package provenance and original source hashes are
preserved. Independent work here means an independently resumable audit and
refinement record; it does not mean independent invention of the core proof.

The completed audit found no gap in the stated theorem. This is not a
machine-checked formal proof or external peer review. Practical superiority
over optimized FISTA, AESP, or active-set solvers has not been established.
This directory does not promote other algorithms' open claims into the active
manuscript or change the repository's implementation-wide residual decision.
