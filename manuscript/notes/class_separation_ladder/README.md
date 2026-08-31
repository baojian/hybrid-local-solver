# Class-separation ladder

This note studies **Problem 1 (semantic PPR)** on the centre-seeded star
`K_{1,m}`, where `m = floor(1/(8 eps_ppr))`. It uses the current connected,
unit-weight graph model, the canonical point seed, the sparse `x_hat` output,
and the fully charged exact-real word model from `problem_definitions`.

The note works internally in mass coordinates `z_hat = pi_hat` and explicitly
returns `x_hat = D^(-1/2) z_hat`. The two outputs have identical support and
the same canonical degree-normalized semantic error.

| Class | Axiom dropped | Proved star work |
|---|---|---|
| monotone push `M_+` | — | `Theta(1/(alpha eps_ppr))` |
| signed step `M_pm` | step positivity | `Theta(1/(alpha eps_ppr))` |
| signed relaxation `R_pm` | residual nonnegativity | lower `Omega(1/(sqrt(alpha) eps_ppr))`; upper with `log(1/alpha)` |
| elimination | dissipativity | `Theta(1/eps_ppr)` |

The signed-relaxation row is **not yet an exact Theta result**. Removing its
logarithmic upper-bound factor is supported by measurements but remains
unproved. Elimination also shows that the signed lower bound is a restricted
class result, not an information lower bound for semantic PPR.

Auxiliary one-hop output maps are treated as an oracle extension only. A map
may avoid push operations above a column-mass threshold, but applying the map
and emitting the sparse answer are still charged by Problem 1.

Build with `make`. Claim status, source provenance, verification details, and
the two remaining open directions are recorded in the final section and in
`STATUS.md`.
