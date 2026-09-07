# Growing branching cores: scalar physical-flux reporting

Date: 7 September 2026. **Proved here:** implemented construction and proof
draft awaiting independent review. **General OP3 remains Open.**

The two-retained-vertex result extends in a useful direction without a
higher-dimensional hull. Retain the seed and every admitted vertex of
original degree at least three. Eliminate the other admitted vertices.
Every unfinished path then has exactly one retained endpoint, so its
physical flux into an inactive vertex is a stable affine function of one
retained potential. A scalar queue reports its geometric increases.
Several paths reaching the same vertex contribute to one shared gate.

The complete bound is

\[
 O\left(|U|r^2+rV+VL\log(2+V)\right),\qquad
 V=\operatorname{vol}(U),\quad
 L=1+\log_+\frac1{\bar\alpha\varepsilon_{\rm appr}},
\]

with `O(V+r^2)` working storage. Here `r` counts retained vertices in the
returned support. There is no supplied support, separator, topology, core
size or inactive-component size. The algorithm reads precisely positive
output rows, and may query degrees of their inactive neighbors.
Since `V<=2/eps_appr`, the bound is `O_tilde((1+r^2)/eps_appr)`.
It reaches OP3's soft-O scale for a polylogarithmic number of retained
branching vertices. The explicit core factor remains on general graphs.

The proof is `sections/op3_branch_core_flux.tex`, especially
`lem:op3-scalar-flux-arms`, `lem:op3-scalar-flux-work`, and
`thm:op3-branch-core-flux`. All arithmetic is exact-real word arithmetic;
coefficient-bit complexity and floating-point certification are outside
the claim. The implementation uses exact fractions, a dense retained inverse,
and ordinary scalar heaps. Comparison dictionaries give the conservative
word bound; the Python implementation uses dictionaries for bookkeeping.

## Why these scalar events avoid the Schur cancellation failure

An original boundary edge `ij` carries

\[
 F_{ij}=\gamma u_i=a_{ij}u_{c(ij)}+b_{ij},
 \qquad a_{ij}>0,\quad b_{ij}\leq0.
\]

The path, coefficients and retained label stay fixed until target `j`
activates. Keep a lower publication `ell_ij` and queue the next threshold
`u_c > ((5/4) ell_ij + eps_appr/16 - b_ij)/a_ij`.
At a due event, publish the actual physical flux. Settled queues certify

\[
 \ell_{ij}\leq F_{ij}\leq\tfrac54\ell_{ij}
                 +\varepsilon_{\rm appr}/16.
\]

The shared sum `L_j=sum_i ell_ij` admits `j` when
`L_j>(11/20) eps_appr*d_j`, safely for the obstacle at
`lambda=eps_appr/2`. At termination the exterior original residual is at
most `(3/4) eps_appr*d_j`; active residuals equal `lambda*d_i`.
The final exact restricted solution therefore already gives an ACL witness.
It need not equal the global obstacle optimum: the tolerance permits this
different stopping support.
Evaluate `r` on this new trace at `lambda=eps_appr/2`; the earlier exact
two-port theorem uses the obstacle support at its own chosen lambda.

Each arm corresponds to one scanned original edge. Its physical flux is
monotone and bounded by `gamma/bar_alpha`; a first publication exceeds
`eps_appr/16`, and later publications grow by more than `5/4`. This pays
for all publications, queue entries and stale removals. Visiting every
retained queue each round is explicitly charged as `O(|U|r)`.

The failed normalized-Schur reporter instead allowed error proportional to
the accumulated negative Schur load. This construction retains the large
negative intercept in an exact threshold calculation and bounds error in
physical flux. It does not assume that cancellation is numerically harmless.

## What the implementation actually verifies

`BRANCH_CORE_FLUX_AUDIT.json` records **27,120 exact comparisons** on all
connected atlas representatives through seven vertices, every seed and four
parameter pairs. Each output is compared with a separate exact solve on its
returned face, bounded above by the full obstacle optimum, and checked
against the original graph's ACL residual inequalities.

For graphs through five vertices, all 2,112 intermediate faces receive
additional independent checks: 9,717 retained-inverse entries, 4,345
physical fluxes and 3,253 shared boundary sums. These full-state checks are
audit-only; the solver never calls a dense full-face oracle or loops over
the ambient graph.

Seventeen larger or targeted diagnostics also pass full-graph residual
checks. They include unequal subdivisions of cyclic cores, many shared
inactive reports, threshold equality, large stars, and the three previous
Schur cancellation examples.

| Family | Ambient vertices | Positive rows | Retained vertices | Scanned entries |
|---|---:|---:|---:|---:|
| Unequal subdivided core | 222 | 222 | 16 | 460 |
| Shared reports from four retained vertices | 6,445 | 35 | 4 | 90 |
| Shared reports from eight retained vertices | 51,372 | 136 | 8 | 376 |
| Shared reports from sixteen retained vertices | 102,707 | 271 | 16 | 878 |
| Large star | 4,097 | 4,097 | 1 | 8,192 |

Publication equality leaves the event pending; admission equality leaves
the candidate inactive. Both exact ties are audited. On the previous
cancellation examples of 135, 265 and 524 vertices, the new solver returns
valid full-support ACL solutions; it does not reproduce the approximate
normalized reporter's false quietness certificate.

## The remaining cost is real for this representation

`prop:op3-dense-core-binary-tree` proves a simple diagnostic. On a complete
binary tree of height h, take `alpha=1/1009` and
`eps_appr=alpha/(10*6^h)`. A single-path term in the PPR Neumann series
forces every ACL output coordinate to be positive. There are
`r=2^h-1` retained vertices. At their successive births, every entry of
the existing inverse increases, forcing at least

\[
 \sum_{k=1}^{r-1}k^2=\Omega(r^3)
\]

explicit inverse writes. `BRANCH_CORE_COST_AUDIT.json` verifies this family:

| Vertices | Retained vertices | Mandatory writes at retained births | Actual inverse-entry updates |
|---:|---:|---:|---:|
| 15 | 7 | 91 | 483 |
| 31 | 15 | 1,015 | 4,615 |
| 63 | 31 | 9,455 | 40,207 |
| 127 | 63 | 81,375 | 335,391 |

These are easy balanced trees for other representations. This is an
explicit-inverse obstruction, not a graph-access lower bound or evidence
against OP3. Even explicitly rewriting all retained potentials retains a
quadratic repeated-write cost when the core grows proportionally to support.

## Provenance and the next falsifiable target

**Context/provenance**, not formal cross-note imports:

- `propagate_settle_framework`, `thm:kinetic-scalar-gate` and
  `thm:rooted-spider-kinetic`, already give scalar threshold queues and
  exact arrowhead elimination. The new work is the physical-edge arm
  decomposition, original-residual bands, shared gates and growing-core
  accounting; no new generic heap theorem is claimed.
- `aesp_cd_l1_rppr`, `cor:aesp-cd-stable-port-reporter` and
  `thm:aesp-cd-tree-singleton-threshold`, supply the existing fixed-port
  and ancestor-route context. Its
  `thm:aesp-cd-cactus-online-hysteretic-hld` remains radius-paid, rather
  than a polylogarithmic dynamic hull-meld implementation.
- The Chan three-dimensional source contract is now reconciled in
  `docs/literature/lcp-solvers.md`. Its backend is not implemented here.
  The scalar physical-flux construction makes that bounded extension less
  urgent than paying for an unbounded retained core.

The next target is an implicit retained response that delivers due scalar
thresholds and certifies all other queues quiet. Low-degree admissions
change a core diagonal/load or a rank-one block on at most two coordinates;
branching admissions border the system. A cheap named solve does not pay
for finding all changed queue certificates. Start on long asymmetric trees
or a cycle with interleaved branch changes, and charge every hierarchy
transformation, rebuild, failed query and output write. Keep the verified
physical-flux residual contract when testing approximate responses.
