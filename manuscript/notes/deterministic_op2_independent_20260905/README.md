# Deterministic local acceleration for regularized PageRank

This independent note records the algorithm and proof developed in **Prove
conjecture 2 deterministically** on September 5, 2026. It solves the second
conjecture in the authorized problem-definition source in its exact-real model.
Internal audits found no remaining gap; external peer review is still open.

The algorithm combines a decreasing regularization schedule, accelerated
projected corrections, a degree-scaled box and mass cap, deterministic sparse
threshold reporting, and certified stage repair. Its stage energy decreases by
`1 - theta`, with `theta` comparable to `sqrt(alpha)`. A separate second-energy
and signed-flow argument bounds **all repeated support scans** by `O(K/r)`.
Together these yield fully charged `Otilde(1/(rho sqrt(alpha)))` work, with
polylogarithmic dependence on objective accuracy.

## Read and reuse

- [New independent note](main.pdf): model, update equations, continuation,
  accelerated rate, locality proof chain, and evidence scope.
- [Original complete 20-page proof](proof.pdf): unchanged audited proof.
- [Browsable original TeX sources](original_sources/README.md): byte-identical
  historical sources with a `.txt` suffix and independent build instructions.
- [Algorithm explanation](ALGORITHM.md): concise mathematical pseudocode.
- [AESP and Catalyst comparison](AESP_CATALYST_COMPARISON.md).
- [Current claim and verification status](STATUS.md).
- [Complete portable proof and solver bundle](archives/conjecture2_proof_and_solver.zip):
  original TeX sources, solver package, wheel, exact validation runners, benchmark
  runners, reading guide, and curated audits. Start at its `START_HERE.md`.
- [Substantive research archive](archives/research_record.tar.gz): original
  working notes, corrected attempts, programs, measurements, audits, and final
  records. Use the final status and proof when an earlier attempt disagrees.
- [Archive inventory](ARCHIVE_MANIFEST.json): every retained file and exclusion.
- [Completion record](COMPLETION.json) and [checksums](SHA256SUMS).

The original work is preserved in archives because it is a historical standalone
document and code snapshot, not an alternate repository-wide notation system or
a replacement for the production solver under `src/`. Original source bytes and
archived hashes are retained. Historical absolute paths in audit logs describe
the original run; use the portable bundle's runners for a fresh checkout.

## Build and check

From this directory:

```sh
make
make verify-archives
```

To work with the original proof or solver, extract the portable archive **outside
`manuscript/notes`**, for example into repository `tmp/`, then follow `START_HERE.md`.
This avoids registering a second standalone historical TeX document as a new
active note. The bundle is self-contained; the overview note uses the shared
repository preamble and problem definition.

## Notation and status

The new note follows the shared bold-vector notation. Archived plain `Q,D,b,x*`
map to their bold counterparts; archived `epsilon` is `eps_obj`. The archived
stage source `s = b - Q bar_x` is called **h** in the new note, since the shared
symbol **s** is the seed distribution. No PPR-error/objective-error equivalence
is assumed. No randomized primitive is used by the algorithms or exact fixtures.

The fresh research did not consult other manuscript directions. The later
user-requested comparison established that **Prove deterministic Conjecture 2**
audited and extended this same core proof. It is not a formal dependency of this
note. AESP and Catalyst were compared only after the proof was completed.
