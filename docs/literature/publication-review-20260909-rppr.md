# Audit of the two 2026 PageRank papers

Checked 2026-09-09. Scope: exact versions, theorem contracts, their relation to the project's OP1/OP2, and public follow-on searches. This is a literature audit, not an independent validation of the project's proofs.

## Finding

Neither examined paper states the same unconditional, graph-uniform, deterministic bound with only polylogarithmic overhead and inverse-linear accuracy/regularization dependence that the project claims. This supports a carefully qualified novelty claim for that precise combination. It does **not** support saying that nobody else works on the problem, that local acceleration was previously unavailable, or that the inverse-square-root dependence is an unconditional lower bound.

The project names OP1 (degree-normalized semantic PPR error) and OP2 (regularized objective error). These are project-defined contracts. The original [COLT 2022 paper, Section 3, p. 3](https://proceedings.mlr.press/v178/open-problem-fountoulakis22a/open-problem-fountoulakis22a.pdf) presents one acceleration question, not a numbered pair of conjectures.

## Fountoulakis--Martínez-Rubio

**Primary records:** [arXiv abstract/history](https://arxiv.org/abs/2602.21138), [v1 PDF](https://arxiv.org/pdf/2602.21138v1), [v2 PDF](https://arxiv.org/pdf/2602.21138v2).

Latest listed: v2, submitted 2026-04-08; v1: 2026-02-24. PDF lengths: 29 versus 23 pages. The new v2 Section 4.4/Appendix D gives the negative FISTA result absent from v1; the conditional upper-bound architecture remains.

Theorem 4.3 (v2 p. 6) concerns FISTA on **F_{2rho}**, assumes every spurious activation stays in a fixed boundary set B, and bounds work by

\[
O\!\left(\frac{1}{\rho\sqrt\alpha}\log\frac\alpha\varepsilon
+\frac{\sqrt{\operatorname{vol}(B)}}{\rho\alpha^{3/2}}\right).
\]

Theorem 4.4 (same page) supplies a sufficient graph condition for confinement. Assumptions include undirected unweighted graphs, positive degrees, and a single-vertex seed (§3, p. 3). Proposition D.4 (p. 22) gives fixed-alpha star instances requiring at least 2m FISTA work for sufficiently small objective error, whereas ISTA work is independent of m.

**Comparison:** neither the confinement-dependent upper bound nor an algorithm-specific FISTA obstruction establishes the project's unconditional OP1/OP2 theorem. Cite the negative result to motivate a different constrained recurrence.

**Date caution:** HTML rendering displays August 24; the PDFs display February 25/April 10. Bibliographic version dates above come from arXiv submission history, not generated title dates.

## Wei--Yang

**Primary records:** [arXiv abstract/history](https://arxiv.org/abs/2608.16339), [v1 PDF](https://arxiv.org/pdf/2608.16339v1).

Latest listed: v1, 2026-08-17, 17 pages. Theorem 1.2 (p. 3): randomized ACL epsilon approximation, support volume <= 2/epsilon, work O(epsilon^-2 polylog(1/(alpha epsilon delta))).

Theorem 1.3 (pp. 3--4), with k*=|S*|, V*=vol(S*), gives

\[
O\!\left(k_*\widetilde{\operatorname{vol}}(S_*)
\operatorname{polylog}\frac1{\alpha\rho\xi\delta}+k_*V_*\right)
=\widetilde O(k_*V_*)\le\widetilde O(\rho^{-2}).
\]

Outputs have additive objective gap <= xi and an ACL 2rho certificate; support volume <= 1/rho. Success probability >= 1-delta. Assumptions: connected, simple, undirected, unweighted graph; adjacency-list access (§1.1, p. 2). Growing active sets use SDD solves (Algorithm 2, pp. 8--10; proof p. 14).

The p. 4 deterministic-solver remark incurs an extra k*^{o(1)} factor for RPPR. Thus deterministic predecessors exist. Section 6 (pp. 14--15) leaves reuse across nested systems open.

**Comparison:** quadratic locality dependence gives a tradeoff, not a uniform solution to inverse-linear OP1/OP2. The project's randomized minimum matches this branch when k* <= alpha^-1/2 and improves its displayed bound in the opposite regime, up to logarithms.

## Mathematical comparison checks

These are algebraic deductions used for manuscript positioning, not additional published theorems.

The lazy/non-lazy normalization dictionary is

\[
a=\frac{2\alpha}{1+\alpha},\qquad x=D^{1/2}y,
\qquad F_{\alpha,\rho}(D^{1/2}y)
=\frac{1+\alpha}{2}\psi_{a,\rho}(y).
\]

Therefore regularization rho is unchanged, and objective tolerances differ by a factor between 1/2 and 1. Original graph degrees must be retained on restricted systems.

For an ACL certificate p=pr_a(e_s-r), 0<=r<=epsilon d, positivity and pr_a(d)=d imply 0<=pr_a(e_s)-p<=epsilon d. The converse does not follow from a two-sided degree-normalized error certificate. A manuscript claiming compatibility with ACL clustering must actually establish the positive-residual representation.

Ignoring logarithms, compare the generic ACL rates epsilon^-2 and (epsilon sqrt(alpha))^-1: the former is smaller when epsilon>sqrt(alpha), and the latter when epsilon<sqrt(alpha). Consequently, a new accelerated inverse-linear theorem should not be described as uniformly faster than every existing algorithm. A combined minimum can cover both regimes.

The claimed randomized RPPR envelope V* min{k*,alpha^-1/2} should credit the existing active-set/SDD branch; its novelty depends on the new accelerated branch and the correctness and accounting of the combination.

## Recency coverage and uncertainty

**High confidence:** version identities and main theorem contracts above. The relevant PDF pages were read; Theorem 4.3, Proposition D.4, and the continuation of Theorem 1.3 were also rendered and visually inspected.

**Moderate confidence:** no additional publicly indexed paper matching the exact joint OP1/OP2 target was located in this focused search. A search cannot rule out unpublished work, unindexed uploads, accepted-but-not-public papers, or work using distant terminology. No verified citation-count claim is made: Semantic Scholar API requests failed in the browsing tool. Some OpenReview PDF URLs presented browser verification challenges; their available search extracts concerned RAG diffusion or spectral clustering oracles, and were not treated as proof of solver-theorem scope.

[Mingji Yang's publication page](https://kyleyoung-ymj.github.io/) still lists the active-set result as an August 2026 preprint and also identifies adjacent ITCS/SODA 2026 papers on asymmetric linear systems and directed single-node PageRank estimation. Those are different output/access regimes. [WatCL's publication page](https://watcl.ca/publications/) lists the classical-acceleration paper, without an additional solution to the same target in its public list. Author-page lists are corroboration, not exhaustive registries.

Recommended manuscript phrasing: “To the best of our knowledge, this is the first deterministic graph-uniform bound of [precise displayed rate and certificate] with only polylogarithmic overhead.” Use this only after the separate proof audit succeeds and the broader literature audit is reconciled.

## Search log

All queries executed 2026-09-09. Search results were discovery aids; substantive comparisons above use original papers.

1. Exact identifiers: `2602.21138`, `2608.16339`; exact full titles; title plus `citations`.
2. `PageRank "local" "acceleration" after:2026-08-01 before:2026-09-10`.
3. `"PageRank" "regularized" "2026" "algorithm"`.
4. `"PageRank" "regularized" "2026" site:arxiv.org/abs/`.
5. `"PageRank" "local" "acceleration" "2026" site:proceedings.mlr.press`.
6. `"PageRank" "local" "2026" site:epubs.siam.org`.
7. `"PageRank" "confinement" acceleration`.
8. `"PageRank" "support-safe"`; `"PageRank" "local" "linear coupling"`; `"PageRank" "active-set" acceleration`; `"PageRank" "rho" "2609"`.
9. `site:openreview.net "ICLR 2026" "local graph clustering"` and exact identifiers of two returned PDF versions.
10. Primary author pages and the arXiv histories were opened directly; both classical-acceleration versions and the active-set PDF were downloaded.

Additional discovery sent to the broad-literature audit: [NeurIPS 2024 constrained optimization paper](https://papers.nips.cc/paper_files/paper/2024/file/8d8e060d9a3312ae12f42adf0da6ec7c-Paper-Conference.pdf), whose motivating constrained sparse-PageRank example and support identification require distinguishing from total local RPPR work. This focused audit does not independently close that comparison.

## Reproducibility

Downloaded reference files are under `publication-20260909/references/`. No original repository or synced project source was changed.

| PDF | SHA-256 |
|---|---|
| 2602.21138v1.pdf | 039226c625e26c2d49d4e4555b244eb47e10c75f9e94418bca0293c1d5a9db52 |
| 2602.21138v2.pdf | ddbbe15cddf8f8c129304a6f34a8ecaeaba205f9dca763882a1b937b40484dcd |
| 2608.16339v1.pdf | fb0a4d4887b2f3f916e440a6a6f9800b9a4dffcefe48e5ee04e0662df25193bb |
