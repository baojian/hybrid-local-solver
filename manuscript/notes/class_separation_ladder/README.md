# class_separation_ladder

A three-rung class-complexity ladder for local PageRank on a single instance,
the centre-seeded star `K_{1,m}` with `m = floor(1/(8 eps_ppr))`.

| Class | Axiom dropped | Star work |
|---|---|---|
| monotone push `M_+` | --- | `Theta(1/(alpha eps_ppr))` |
| signed step `M_pm` | step positivity | `Theta(1/(alpha eps_ppr))`, no gain |
| signed relaxation `R_pm` | `r >= 0` | `Theta(1/(sqrt(alpha) eps_ppr))` |
| elimination | dissipativity `omega in (0,2)` | `Theta(1/eps_ppr)` |

Each rung drops exactly one axiom and buys exactly one factor of
`sqrt(alpha)`, except the step-sign axiom, which buys nothing. All four rows
share one primitive, one work charge, one output map and one semantic
guarantee, so the only difference between the compared classes is the class
axiom.

The note is deliberate about what this does **not** show: elimination beats
every member of `R_pm` on the same instance, so the rung-two bound is a class
statement rather than an information barrier, and it gives no support to
`1/(sqrt(alpha) eps_ppr)` as a necessary cost of the semantic problem.

Build with `make`. Claim status, provenance, the verification appendix and an
auditor's checklist are in the final section of the note; the direction's
ledger and open items are in `STATUS.md`.
