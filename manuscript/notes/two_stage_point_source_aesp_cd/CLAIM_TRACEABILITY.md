# Claim-to-evidence map

This file is the review index for the reduced two-stage paper.  It separates
mathematical claims, executable certificates, measurements, and open
interfaces so that the four-page core does not inherit the scope of the
100-page companion audit by accident.

| Claim | Scope | Proof source | Executable evidence |
|---|---|---|---|
| RPPR is a `rho`-accurate PPR screen and has volume at most `1/rho` | any probability source | `sections/02_problem_and_certificates.tex` | exact obstacle cases in `two_stage_composition.py` |
| A containing RPPR envelope may be linearized by one ordinary principal PPR solve | any source; any containing set | strict Lemma 1.1 and `sections/04_composition.tex` | all 192 subsets in three exact rational instances |
| A set-only certificate composes with a fixed accelerated tail in `W_disc + O_tilde(vol(E)/sqrt(alpha))` | fixed certified envelope | strict Theorem 1.2 | exact rational accelerated tail and semantic check |
| An exact structural tail uses the full screening budget (`rho=epsilon`) | exact fixed solve | strict Theorem 1.2 | tree/unicyclic semantic columns in all literal tables |
| A verifier factorization can be reused for the ordinary-PPR right-hand side | tree/unicyclic or supplied bounded-width factors | strict Theorem 1.2 | reusable factors on path, broom, cycle, and 80 randomized structural systems |
| A point-source exact support is connected and rooted | one positive source load | strict Section 1 | exact obstacle enumeration and tree traces |
| On a rooted support candidate, exact KKT needs only a boundary scan | one source already in the candidate | strict Section 2 | residual-error intervals; 8,096 exhaustive randomized candidate-face checks with no false certificate |
| Positive residual rows from a lower-safe SOR/AESP point are true support rows | Stieltjes obstacle and lower checkpoint | strict Section 2 | exact positive-batch audit; 90-row SOR sweep |
| Repeated exact positive-boundary refits are correct but can be serial | structural refits | strict Section 2 | 38 singleton path rounds in the large batch table |
| APPR snapshots plus one verifier are an unconditional optional lane | fair race with direct APPR | short Theorem 2 | 28 certified rows; fresh/reused fair counts `2/2` |
| SOR/AESP support discovery plus one verifier is an unconditional optional lane | fair race with direct APPR | strict Section 2 | 75 certified rows; fresh/reused fair counts `5/5` |
| Tree threshold messages give product-scale exact Stage I | exact-real, one source, promised tree | strict Section 2 | 60 large rows and 1,890 randomized small-tree traces |
| A Green ball is an exact-support-free set-only screen | one source; hard volume cap | strict Section 2 | 90-row CG and 75-row structural-tail tables |
| Direct boundary leakage certifies a PPR envelope | fixed principal approximation plus residual error bar | strict Section 2 | exact rational leakage audit and high-accuracy sweep |
| Threshold batches solve RPPR in graph-uniform product work | point source; exact-real randomized word model | imported `active_edge_lcp`, Theorems `thm:batch-depth` and `thm:op2` | source audits: 1,152 floating cases, 216 high-precision cases, exact residual/path checks |
| A low-energy safe inner face certifies omitted RPPR amplitude | any reachable face, including a strict subset of `S*` | `sections/09_randomized_op2_transfer.tex`, Lemma `lem:two-stage-inner-face-energy` | 171 positive inner faces on 40 exact rational instances; 4 incomplete cap-exit paths |
| Randomized Stage I plus an independent ordinary-PPR Stage II meets the target product bound | point source; exact-real randomized word model | strict randomized-closure section and Theorem `thm:two-stage-randomized-completion` | 67-case accepted-error prototype; all direct and literal Stage-II outputs pass |
| Ordinary sparse-source PPR superposes but RPPR discovery does not | ordinary PPR versus obstacle RPPR | strict Section 4 | exact weighted P3 superposition and separate/joint KKT keys `-1/48`, `1/24` |

## Measured columns

The conservative table in the strict paper uses a fresh Stage-II solve:

- APPR proposal: `4/2` standalone/fair;
- SOR proposal: `5/5`;
- exact positive batches: `33/8`;
- tree messages: `27/14`;
- structural Green: `50/35`.

The retained-factor model changes the first three to `6/2`, `7/5`, and
`37/9`.  `strict_two_stage_summary.py` recomputes every count from the saved
CSVs, checks every finite semantic-error column, audits strict APPR verifier
intervals on 36 randomized small structural systems and all 8,096 of their
candidate faces, and independently tests the reusable factors.

## Claims deliberately not made

- The randomized closure does not identify all of `S*`; it proves that a
  low-energy inner face suffices.
- The exact-real randomized theorem is not a deterministic floating-point or
  coefficient-bit theorem, and it is not an implementation benchmark of the
  Koutis--Miller--Peng solver.
- Threshold-batched active-set discovery is an AESP-CD portfolio lane, not a
  proof that the original momentum recurrence survives face changes.
- A numerical RPPR/APPR checkpoint is not forced through a redundant second
  solve when it already meets the PPR target.
- Exact support is not required for PPR accuracy.
- The single-source theorem is not promoted to an additive `nnz(s)` theorem.
- Floating equality is not treated as an exact support decision; the
  executable verifier requires separated residual-derived intervals.
- Fresh and reused Stage-II work are reported separately.
