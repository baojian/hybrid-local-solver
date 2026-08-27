# Handoff: psi-master-inequality

- Branch: `agent/codex/psi-master-inequality`
- Base commit: `4a979a6907880fb2dc76d1c51dbb7d12dc8bd5b3`
- Write scope: `manuscript/notes/psi_master_inequality/` and this handoff.
- Shared files changed: this explicitly permitted handoff only.

## Current result

The exact positive-face recurrence and the full algebraic cap domain have
been reconstructed independently.  Lemma `lem:psi-master-identity` proves the
master identity and `eq:psi-slack-decomposition` exposes the clipping term.
Under `mu_2>=2q`, the all-positive and all-negative sign channels are
analytically nonpositive.  Mixed clipping is the only remaining functional
obstruction.

## Evidence boundary

- **Source:** Fable iteration-6/7 files are read-only exploratory evidence.
- **Proved here:** recurrence, master identity, slack decomposition, and the
  two unmixed sign channels.
- **Open:** mixed-sign nonpositivity, proper faces, finite shifted solves,
  work, locality, and terminal accuracy.

## Resume target

Derive the mixed-clipping positive-association condition and prove it on an
infinite graph family, beginning with complete bipartite graphs.

## Checks

- `make -C manuscript/notes/psi_master_inequality`: pass.
- `git diff --check`: pass.
