# Positivity and conservation literature checked 2026-09-05

These sources inform possible proof techniques; neither is being imported as
an OP2 algorithm or an accelerated convergence theorem.

## Botchev and Zhukov: positivity of LIM

[Primary institute PDF](https://keldysh.ru/papers/2025/prep2025_70.pdf),
2025 preprint 70, sections 3.1-3.2, printed pages 8-13. A local snapshot is
`results/positivity-lim-2025.pdf`. Printed page 9 was visually checked.

The authors explicitly explain that the Chebyshev-based local iteration
modified time scheme is not positivity preserving for every symmetric
M-matrix. Their four-by-four tridiagonal example has diagonal 7 and
off-diagonal -3; its update matrix has negative entries. The positive behavior
discussed for the standard one-dimensional heat equation therefore cannot
be transferred to all canonical graph instances. Their discussion invokes
the Bolley-Crouzeix absolute-monotonicity criterion. No general positive
accelerated polynomial primitive is obtained from this source.

## Cheng and Shen: mass-preserving multiplier corrections

[Author-hosted published PDF](https://www.math.purdue.edu/~shen7/pub/CS_CMAME22.pdf),
CMAME 391 (2022), 114585, especially sections 2.3 and 3, Theorems 3.2 and 3.4.
A local snapshot is `results/positivity-mass-cheng-shen-2022.pdf`.

The paper uses positivity multipliers and a scalar mass multiplier in
prediction/correction schemes. The scalar correction is related to a weighted
simplex threshold. Its first- and second-order stability arguments concern
their specified time discretizations and mass-conserving operators; the
second-order bound includes a multiplier norm. This suggests tracking a
repair multiplier as part of an energy, but it does not establish the
root-condition-number optimization rate or local graph-work ledger needed
here. In particular, their implicit prediction stage is not a free local
matrix operation. Theorem 3.4 and the neighboring proof were read, and its
statement was visually checked on printed page 9.
