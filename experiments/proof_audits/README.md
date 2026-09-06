# Research-note proof audits

This directory owns executable checks for claims developed in standalone
research notes. The note source remains under `manuscript/notes/`; keeping the
executables here prevents round-specific scripts from becoming part of a
note's document structure.

[`registry.toml`](registry.toml) gives every audit a durable mechanism-based
identifier, its owning note, exact or numerical status, and its historical
round of origin. Round numbers are provenance only. Renaming or adding an
audit requires updating the registry in the same change.

An audit developed outside a coordinated research round records an ISO
`provenance_date` instead. Exactly one of the date or historical round is
required; this records new work without inventing a research-round history.

From the repository root, run:

```bash
make research-audit-fast   # representative deterministic checks used by CI
make research-audit        # every audit, including extended exact sweeps
make research-audit-list   # registry, tier, provenance, and script path
```

The full tier deliberately includes the optional P7 exact trace for
`aesp_cd_l1_rppr.safeguarded_outer_ledger` and exhaustive small-graph search
for `volume_gated_acceleration.nonpath_causal_stop`. Numerical audits retain
their recorded seeds and trial counts in the individual scripts. Passing an
audit corroborates only the scoped claim named by that script and its owning
note; it does not promote an open end-to-end complexity statement.
