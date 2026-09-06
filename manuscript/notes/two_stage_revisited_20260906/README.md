# Two-stage algorithms revisited, September 6, 2026

This note revisits `aesp_cd_l1_rppr`, `two_rung_sor`, and
`hybrid_aesp_locsor` using the newer deterministic and randomized RPPR
proofs. The most direct answer to the original hybrid question is the
new deterministic prefix / signed-GS construction in `sections/13_deterministic_signed_handoff.tex`.

## Main findings

**A provable accelerated prefix.** Project only the kinetic vector onto the
nonnegative orthant, keep the source fixed, and decrease the regularizer
at every accelerated step. The new cooling energy and weighted signed-flow
telescope give

    sum_k vol(supp z_(k+1)) <= 44 sum_k 1/r_k.

A lazy threshold reporter charges every local operation. The algorithm has
no box, mass projection, intermediate repair, or restart. A separately
specified directed-rounding construction uses bounded integer encodings
and replaces 44 by 60. Exact primal support is nested; rounded coordinates
can disappear, while the stored exposure history remains nested.

**A literal deterministic accelerated-prefix / coordinate-tail algorithm.**
Let sigma=eps_ppr/3, rho=sigma/2, and r_*=rho/2. Cool to r_* and accelerate
only until the RPPR objective gap is at most `alpha^2 theta rho`. The
thresholded absolute residual potential

    M_rho(x) = sum_i sqrt(d_i) (|b-Qx|_i-alpha rho sqrt(d_i))_+

is then at most `alpha theta`. Signed coordinate updates that retain the
reserve `alpha rho sqrt(d_i)` spend this potential and finish with accelerated
total work. One final downward clipping gives an output below the RPPR
optimum at `eps_ppr/3`, with nonnegative PPR residual and volume at most
`3/eps_ppr`. Its semantic PPR error is at most `eps_ppr`.

The exact-real incidence bound is
`O((1+log(2/alpha))/(eps_ppr sqrt(alpha)))`; only label-map logarithms remain
in the full operation count. The frozen prefix needs no logarithm of
`1/eps_ppr`. A direct residual test permits an earlier handoff. A separately
rounded version has the same soft work scale. This final output is certified
for semantic PPR; an ACL certificate is a distinct claim.

The gap-to-excess bound also accepts signed composite-AESP endpoints.
They can enter the coordinate tail without a lower retraction, though the
charged work of reaching that certificate remains an AESP-specific question.

**Other valid completions.** Freezing the same recurrence to a finer tolerance
and clipping once solves point-source OP1, independent RPPR objective
accuracy (OP2), and optionally the stronger positive-residual target.
For an arbitrary explicit sparse source, discard source entries of density
at most rho/2, solve the retained source at regularizer rho/2, and use the
resulting approximate support for the original objective at rho. This gives
fully charged `O_tilde(|T|+1/(rho sqrt(alpha)))` work. The compensated
source reduction is new here; approximate inner faces already occur in the
older point-source note.

**A coarser randomized handoff.** The existing randomized theorem exposes
faces inside the optimal support. Clip relative to the exact face solution,
then use an RPPR-relative mass deficit or a directly computed residual-excess
certificate to pay for a reserve-preserving GS tail. The composition retains
the accelerated expected work scale. Its objective target is coarser than
the direct semantic conversion when `eps_ppr < theta^2`. The SDD primitive is imported;
these audits do not implement or time it.

**A reason to keep a completion phase.** Exact unit-tree counterexamples
refute monotonicity, PPR lower order, and nonnegative intermediate residuals
for the new ramp. A separate separated-front limit and stable cascade proof
show that no graph-uniform constant bounds ramp error by its current
regularizer, even at alpha=1/4096. This is an accuracy obstruction for
omitting the completion phase, not a work lower bound against the full
algorithm or other local algorithms.

**A separate warning about the old AESP mass proof.** For the ideal
unregularized AESP recurrence with exact shifted solves, the normalized
weighted residual mass is unbounded over finite unit trees and stages,
even at alpha=1/4097. A complex-frequency argument and finite-tree limit
prove this; an exact finite example exceeds `1.38e11`. Thus a universal
constant `R_J` cannot follow from outer convergence and inner accuracy
alone. This does not refute the actual thresholded inner solver or its
early `Lambda_J` conjecture. See `thm:revisit-exact-aesp-mass`.

## What remains open

| Older attempt | Reusable new idea | Remaining limit |
| --- | --- | --- |
| `aesp_cd_l1_rppr` | A signed composite-gap endpoint can enter the reserved coordinate tail without a lower retraction. The new orthant prefix has its own work proof. | The original retracted AESP recurrence does not inherit that proof. |
| `hybrid_aesp_locsor` | Thresholded absolute residual excess pays for the tail; a proved deterministic or certified randomized prefix supplies it. | Unchanged AESP still needs a charged prefix theorem. The ideal exact-inner mass obstruction concerns `R_J`, not a proof against its actual inner policy. |
| `two_rung_sor` | The new accelerated batch recurrence offers a different prefix/tail construction. | The existing ranked-SOR obstruction keeps its original scope; changing the interpretation of its relaxation parameter does not remove it. |

The note contains complete written proofs of the stated new constructions
and obstruction, subject to independent review. It does **not** establish
the original early-AESP quantity `Lambda_J=O(1/eps_ppr)` or an unchanged
AESP/FISTA/SOR theorem. The old ranked-SOR obstruction retains its original
scope. For unchanged AESP, reaching the new thresholded residual budget
with accelerated prefix work is a precise alternative research target.
Practical comparisons under a common work contract remain open; an earlier
handoff can save face solves while adding many coordinate updates.

## Reading and verification

`main.tex` and its included sections are the mathematical authority.
`STATUS.md` is the resumable claim ledger. `RESEARCH_LOG.md` records the
investigation of more than six hours, rejected routes, and corrections.
`RAMP_ASYMPTOTICS.md` preserves the earlier open limit argument and its
resolution. `VERIFICATION.md` and `COVERAGE.json` record the final audit
coverage and provenance. Finite computations are checks, not substitutes
for asymptotic proofs.

The local model is a finite connected simple unit graph with positive
original degrees, a point source or the explicitly stated sparse-source
extension, and no graph-wide preprocessing. Every input read, degree reply,
first and repeated incidence, scalar update, threshold report, materialization,
principal-face build, and output is charged. Dense references and equitable
quotients are offline verification instruments, never free solver primitives.

Formal dependencies are `deterministic_op2_20260905`,
`two_rung_direct_theory`, and `two_stage_point_source_aesp_cd`.
Build and run the representative audits from the repository root with:

```sh
make -C manuscript/notes/two_stage_revisited_20260906
uv run python -m experiments.proof_audits.runner --note two_stage_revisited_20260906
```
