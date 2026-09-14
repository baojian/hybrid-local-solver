# Independent audit of the sparse output certificate

Auditor: localization/regularization subtask. This audit reads only the
fresh certificate files and our fresh small-graph verification helpers.
No solver is called, no randomized test is used, and no implementation is
modified. The certificate source SHA-256 checked here is
`d4dd7147646e2a8a87f33877f7cd1bef8fce4eebacfb6d1093ad22c743ce98f1`.

**Finding: the mathematical certificate and its implementation pass.**
It is a sufficient, optionally inconclusive certificate for the original
objective, independent of the accelerated algorithm's analysis.

## 1. Subgradient and objective-gap argument

Let `w_i=sqrt(d_i)`, `lambda=alpha*rho`, and let the supplied vector be
nonnegative. On its positive coordinates the original absolute-value
objective has subgradient `g_i=(Qx-b)_i+lambda*w_i`. On a zero coordinate,
the Stieltjes signs and `b>=0` imply `(Qx-b)_i<=0`. The original subgradient
interval is therefore

    [(Qx-b)_i-lambda*w_i, (Qx-b)_i+lambda*w_i].

If its upper endpoint is negative, select that endpoint; otherwise the
interval contains zero. This gives exactly the implemented selection
`v_i=g_i` on positive coordinates and `v_i=min(g_i,0)` on zero coordinates.
Thus `v` is a valid subgradient of the original unconstrained objective,
not merely a certificate for a modified constrained problem.

The objective is alpha strongly convex. Its subgradient lower quadratic
model, minimized over all vectors, gives

    F(x)-F(x*) <= ||v||^2/(2*alpha).

This argument needs neither baseline safety nor an acceleration invariant.
The supplied nonnegative vector may be arbitrarily inaccurate.

## 2. Arithmetic formula and upward rounding

Writing densities `f_i=B_i/H`, parameters `alpha=A/D`, `rho=P/R`, and
neighbor sum `J_i=sum_{j~i}B_j`, direct expansion yields

    (g_i/w_i) = [(D+A)R*d_i*B_i-(D-A)R*J_i
                  -2AHR*1(i=seed)+2AHP*d_i] / (2DHR*d_i).

This agrees term by term with the code. For the selected integer numerator
`V_i` and `C=2DHR`, its squared contribution is `V_i^2/(C^2*d_i)`.
The implementation sums integer ceilings of `V_i^2/d_i` and divides by
`C^2` only once. Consequently the norm upper bound is rigorous and its
excess is strictly less than `M/C^2` when there are `M>0` nonzero terms;
both values are zero when `M=0`. No least common multiple of graph degrees
is constructed. Parameter/output conversion uses exact `Fraction`
arithmetic, and all neighbor accumulation and term sums are integers.

The implementation explicitly requires the largest reduced output
denominator to be divisible by every other reduced denominator. All dyadic
outputs, and all single-coordinate direct outputs, satisfy this. It is
intentionally not an unrestricted rational-vector API: for example reduced
denominators 2 and 3 are rejected instead of constructing their LCM.

## 3. Sparse access and scope of validation

Only output coordinates have adjacency lists scanned, exactly once each.
The degree of each affected coordinate is queried once, where affected
means output support, its immediate boundary, or the seed. Unaffected zero
coordinates have selected subgradient zero exactly. Hence the record and
access count is `O(1+vol(supp x))`, with one deterministic-map logarithm
for accumulation. The zero-output case queries the seed degree and scans
no adjacency list.

Claimed output degrees are checked against the oracle, and the scanned row
length is checked against the degree. The implementation does not attempt
to certify globally that the graph is simple and undirected, nor to prove
reciprocity by scanning every discovered neighbor. Those are graph-oracle
input assumptions, as stated in the note and the original problem. A
malicious or inconsistent oracle is outside this certificate's contract.
Arbitrary integer labels are accepted; requiring labels in `[n]` is not
necessary for the certificate once they consistently identify graph
vertices. There is no hidden total-graph enumeration.

`meets(epsilon)` returns false when its sufficient bound is larger than
epsilon. This is correctly documented as inconclusive. It must not be
interpreted as proof that the output is inaccurate. The saved-benchmark
driver uses the labels `CERTIFIED` and `INCONCLUSIVE`, and retains the
separate solver-reported bound without using it in the new computation.
The driver's one-million-entry verification limit is an explicit bounded
experiment setting, not an additional mathematical assumption.

## 4. Independent bounded evidence

`audit_independent_sparse_certificate.py` independently computes exact
density gradients without the integer numerator formula. An independent
support-enumeration/KKT oracle and edge-form objective supply the exact
optimum and actual gap. Its saved evidence is
`independent_sparse_certificate_audit_results.json`.

All checks passed:

- 84 graph/seed/parameter cases across path, cycle, star, grid, cube,
  barbell, and tree-clique families, including alpha=1 and the zero regime.
- 504 output vectors: zero, sparse seed-only, rounded exact optima,
  perturbed rounded optima, and deliberately inaccurate dense/sparse values.
  Each satisfies actual gap <= exact subgradient bound <= returned bound.
- Exact norm and access counts agree on every case; three cases exercise
  strict upward rounding rather than accidental exact divisibility.
- 305 cases explicitly demonstrate an accurate output for a tolerance at
  which this sufficient certificate is inconclusive.
- Twelve malformed-input cases are rejected, including wrong degrees,
  row-length disagreement, duplicate records, nonpositive explicit values,
  incompatible denominators, invalid parameters, and invalid tolerance.
- On a virtual star with `10^12` vertices and output only at one leaf, the
  certificate makes two degree queries and reads one adjacency entry; the
  hub adjacency routine is guarded to fail if called.
- A relabeled path with labels above `2^100` whose `__hash__` raises gives
  exactly the same certificate as its ordinary labeling. This independently
  exercises the deterministic AVL registries.

The existing saved-benchmark evidence reports eleven outputs checked and
eleven certified, with the same certificate source hash. The driver itself
does not rerun the solver. This audit independently checks its data flow;
the 504 fixtures above provide the new numerical evidence rather than
duplicating its larger saved-output scan.

No correction to the implementation is requested. The root derivation's
final status line may now refer to this completed independent audit.
