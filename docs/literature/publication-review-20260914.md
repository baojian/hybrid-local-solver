# Publication comparison: September 14, 2026

## Decision

Cui, Wei, and Yang, **Accelerating the Local Push Primitive for PageRank
Computation**, arXiv:2609.12076v1, is directly overlapping work, not merely
an adjacent PageRank estimator. Its official submission timestamp is
2026-09-10 18:05:23 UTC. The active manuscript must cite it and must not
claim absence of a randomized solution of the COLT 2022 running-time target.

Primary sources: <https://arxiv.org/abs/2609.12076v1> and
<https://arxiv.org/pdf/2609.12076v1>. The inspected PDF has 32 pages and
SHA-256 `328c0f9e11d27a5ffd3b9b9abdb43fe66da97b22533e444184b3286f019136c6`.
It was inspected outside the repository; no additional redistribution of
the source PDF is part of this change. Page numbers below are physical PDF
pages, coinciding with the printed numbers in the inspected passages.

## Normalization and theorem comparison

Let `a` denote this project's lazy alpha and let `beta = 2a/(1+a)`.
With `x = D^(1/2)y`, our objective satisfies

```text
F_(a,rho)(D^(1/2)y) = (1+a)/2 * psi_(beta,rho)(y).
```

Thus rho is unchanged, beta is Theta(a), and their requested objective
gap is `2 eps_obj/(1+a)`. The point-source, undirected unweighted graph
and local degree/neighbor-access assumptions coincide (Section 1.1, p. 2).
Theorem 1.2 (p. 3) supplies the ACL residual certificate; Theorem 1.3 (p. 4)
supplies RPPR objective accuracy and an ACL certificate. An ACL certificate
also implies the project's degree-normalized solution-error criterion by
inverse positivity and preservation of the degree vector by PageRank.
Different normalization or a weaker semantic error criterion is not a
novelty distinction.

In the proof of Theorem 1.3 (p. 18), their phase count is bounded by the
minimum of optimal-support cardinality and an inverse-square-root-alpha
factor times logarithms. Multiplying by the local nonzero and boundary
cost per phase, and using internal nonzeros at most twice original-degree
volume, gives `softO(V_* min{k_*, a^(-1/2)})`. This is an inference from
their proof. The same support-adaptive expression in our theorem is
therefore not, by itself, a novel separation.

Lemma 3.10 (pp. 18-19) gives sparse-source ACL approximation with additive
source-input work. Our general-source appendix should not be presented as
the first sparse-source accelerated PPR result.

## What remains distinct

Our deterministic theorem has only polylogarithmic overhead in the stated
local word model. Their deterministic-substitution remark (p. 4) incurs
an additional subpolynomial factor. A subpolynomial factor is not in
general polylogarithmic. Our two-energy continuation, projection-sector
inequality, and cumulative selected-flow accounting do not invoke an SDD
solver. The separately specified bounded-arithmetic realization also
belongs to our deterministic proof, not to arbitrary floating-point code.

Our randomized proof uses block-Cholesky signs, a block-bidiagonal inverse
comparison, and Chebyshev decay. Their proof uses consecutive-block
potential decrease (Lemma 3.7, p. 13; Lemma 3.9, p. 16). Both algorithms
use thresholded safe active sets. Our residual-certified Las Vegas wrapper
is explicit, but no impossibility of adapting certification to their
algorithm is claimed. Neither algorithm's upper bound establishes an
optimality lower bound.

## Chronology and scope

The earliest proof-bearing commits located in the relevant recorded
lineages are `3fa8455` for randomized RPPR and `0f0ac32` for deterministic
RPPR. See [the release audit](../public-release-audit-20260914.md) for full
hashes, proof locations, timezone conversions, GitHub-hosted evidence,
and disclosure limitations. Historical files and commit dates are preserved.
These records support development chronology, not prior public disclosure.

The September search triaged the fresh cs.DS, math.OC, and math.NA monthly
listings through September 14: 695 distinct IDs after deduplication.
This was title/abstract triage followed by targeted source inspection, not
695 full-paper reviews or an exhaustive absence guarantee. The decisive
overlap was found despite an earlier stale search-engine listing. The
previous September 9 literature verdict is historical and is superseded
by this comparison for current novelty claims.
