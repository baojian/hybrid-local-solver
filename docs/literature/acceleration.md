# Acceleration

## Scope

This note covers outer acceleration frameworks and accelerated local graph
methods relevant to the proposed hybrid solver. Catalyst and AESP are current
starting points, but their applicability has not yet been established.

## Questions for comparison

- What objective, operator, or monotonicity assumptions are required?
- What inner-solver accuracy schedule is assumed?
- How is inexactness measured and propagated?
- Does acceleration require global work or dense state?
- Can warm starts and local active sets be preserved?
- What condition number or `alpha` dependence is improved?
- Does the theoretical accuracy measure match the implemented stopping rule?

## Source annotations

No source has been annotated yet. Add each paper using the template in
[`README.md`](README.md), with exact theorem, equation, or section pointers.
