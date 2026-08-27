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

The mixed obstruction is now also closed under the entrywise `(HK)` kernel
condition by a symmetric-coupling positive-association lemma.  A closed-form
calculation of `N=(3D-A)^-1D` proves `(HK)` on every `K_{a,b}`: the normalized
off-diagonal ratios are exactly `13/36` within a part and `3/4` across the
cut.  Since `mu_2>=1`, `sup Psi=0` for all `a,b>=1` and `0<q<=1/2`.  This is
an infinite non-scalar-high-space family and includes every star.

## Evidence boundary

- **Source:** Fable iteration-6/7 files are read-only exploratory evidence.
- **Proved here:** recurrence, master identity, slack decomposition, the two
  unmixed sign channels, structural `(HK)` nonpositivity, and the complete
  bipartite family theorem.
- **Open:** mixed-sign nonpositivity beyond `(HK)`, proper faces, finite
  shifted solves, work, locality, and terminal accuracy.

## Resume target

Test complete multipartite graphs symbolically and either prove the block
kernel condition or preserve its first exact failure.  A complementary target
is an analytic family beyond `(HK)`, where clipping complementarity rather
than entrywise domination must supply the sign.

## Checks

- `make -C manuscript/notes/psi_master_inequality`: pass.
- `python3 manuscript/notes/psi_master_inequality/verify_master_identity.py`:
  21/21 exact-rational trials pass on `C5`, `K2,3`, and `K3,4`; committed
  output is `verify_master_identity.json`.
- `python3 manuscript/notes/psi_master_inequality/verify_complete_bipartite.py`:
  64/64 closed resolvents and 5280/5280 off-diagonal squared-kernel formulas
  pass exactly; maximum `(HK)` ratio is `3/4`; committed output is
  `verify_complete_bipartite.json`.
- `git diff --check`: pass.
