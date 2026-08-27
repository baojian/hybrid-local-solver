# Handoff: psi-master-inequality

- Branch: `agent/codex/psi-master-inequality`
- Base commit: `4a979a6907880fb2dc76d1c51dbb7d12dc8bd5b3`
- Write scope: `manuscript/notes/psi_master_inequality/` and this handoff.
- Shared files changed: this explicitly permitted handoff only.
- Integration readiness: ready; the remaining items are explicitly scoped
  research questions rather than missing support for the proved claims.

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
an infinite non-scalar-high-space family and includes every star.  Fable's
source evidence already listed `K_{a,b}` as an `(HK)` subclass, so that
calculation is recorded as an independent analytic closure rather than a new
class discovery.

The strict extension is now proved for every complete multipartite graph
`K_{n_1,...,n_k}` with arbitrary positive, unequal part sizes.  The part
chain has a rank-one resolvent, and its cross-part squared-kernel ratio
reduces to a two-variable inequality.  An exact degree-eight
simplex-Bernstein certificate has 45/45 nonnegative coefficients; same-part
pairs are controlled by the nonpositive nontrivial spectrum.  There is no
part-size threshold: `(HK)` and therefore `sup Psi=0` hold universally in
this family for `0<q<=1/2`.

The note now also leaves `(HK)`.  Exact maximization over the high variable
rewrites `sup_h Psi` as two negative quadratic energies plus a single cross
term.  If the zero-row-sum cross kernel has nonpositive off-diagonal entries
(`(CL)`), clipping complementarity makes that cross term nonpositive.  Exact
six-cycle spectral formulas prove `(CL)` for every balanced independent-set
blow-up `C6[Kbar_a]`, all `a>=1`, throughout the high-gap range
`0<q<=1/4`.  Every graph in this infinite family strictly fails `(HK)` with
the same adjacent ratio `5211/4900>1`, so this is a genuinely different
proof route.

The route has a precise limit: on `C10` at `q=1/20`, the `(CL)` adjacent
entry is the exact positive rational
`6998345705403423/396849260156782400`.  This refutes universal `(CL)` on
cycles but is not a counterexample to `Psi<=0`.

## Evidence boundary

- **Source:** Fable iteration-6/7 files are read-only exploratory evidence.
- **Proved here:** recurrence, master identity, slack decomposition, the two
  unmixed sign channels, structural `(HK)` nonpositivity, and the complete
  bipartite and complete-multipartite family theorems; exact high-variable
  elimination, structural `(CL)` nonpositivity, and the infinite
  `(HK)`-failing balanced-six-cycle-blow-up theorem.
- **Refuted:** universal `(CL)` coverage of cycles, by the exact `C10`
  positive kernel entry above.
- **Open:** mixed-sign nonpositivity beyond `(HK)` and `(CL)`, proper faces,
  finite shifted solves, work, locality, and terminal accuracy.

## Resume target

Start from `eq:psi-eliminated-form` on `C10`: pay the positive adjacent cross
entries with the two negative diagonal energies, or find an exact
sign-feasible positive direction.  This is now the smallest explicit
boundary of the two structural routes.

## Checks

- `make -C manuscript/notes/psi_master_inequality`: pass.
- `python3 manuscript/notes/psi_master_inequality/verify_master_identity.py`:
  21/21 exact-rational trials pass on `C5`, `K2,3`, and `K3,4`; committed
  output is `verify_master_identity.json`.
- `python3 manuscript/notes/psi_master_inequality/verify_complete_bipartite.py`:
  64/64 closed resolvents and 5280/5280 off-diagonal squared-kernel formulas
  pass exactly; maximum `(HK)` ratio is `3/4`; committed output is
  `verify_complete_bipartite.json`.
- `python3 manuscript/notes/psi_master_inequality/verify_complete_multipartite.py`:
  exact continuous rational identity; 45/45 nonnegative degree-eight
  numerator Bernstein coefficients and 10/10 nonnegative degree-three
  denominator coefficients; 87 direct block-inverse comparisons, 493 part
  vectors through 14 vertices, and 64094 off-diagonal `(HK)` checks pass.
  The maximum census ratio is `2981/3969<1`; committed output is
  `verify_complete_multipartite.json`.
- `python3 manuscript/notes/psi_master_inequality/verify_cycle_blowup.py`:
  six exact rational-function cycle-kernel identities, 24 exact
  eliminated-`h` checks, strict signs on 36 blow-up matrices and 68796
  off-diagonal entries; exact `(HK)` failure ratio `5211/4900`; exact `C10`
  `(CL)` obstruction.  Committed output is `verify_cycle_blowup.json`.
- `git diff --check`: pass.
