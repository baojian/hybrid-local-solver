# Independent audit of virtual benchmark graphs and output verification

This bounded audit did not run the practical wrapper or any long benchmark.
It read only the fresh benchmark and its fresh exact-test dependencies.
The separate harness is `audit_virtual_graphs_and_verifier.py`; exact results
and the audited benchmark SHA-256 are in
`virtual_graph_and_verifier_audit_results.json`.

## Results

All 43 small structural instances passed an independent edge-set comparison,
connectivity traversal, positive-degree check, degree/row-length agreement,
absence of loops and duplicate neighbors, reciprocal adjacency, and the
one-based vertex range. The families and valid domains are:

| Family | Small audited parameters | Interpretation |
|---|---|---|
| path | n=2,...,9 | consecutive path, endpoints degree one |
| cycle | n=3,...,9 | one simple cycle |
| star | n=2,...,9 | vertex 1 is the center |
| grid | side=2,3,4 | square grid with row-major labels |
| cube | dimension=1,...,4 | labels are one plus the bit vector |
| barbell | clique size=1,...,4 | two cliques joined by one edge |
| tree_clique | height=1,2,3; clique size 2^h,2^h+1,2^(h+1) | one binary tree attached to one shared clique |

The tree-clique construction has tree labels `1,...,2^(h+1)-1`, root 1,
and leaves `2^h,...,2^(h+1)-1`. Every leaf has one edge to a distinct port
of the same clique. Root and leaves have degree two, other internal tree
vertices degree three, ports degree `clique_size`, and other clique vertices
degree `clique_size-1`. This is not the earlier hypothetical graph with a
private chamber at every leaf.

All 12 declared benchmark seeds are valid positive one-based labels. The
large-label star seed is its last leaf; the grid seed has zero-based row
and column 5000; the cube seed is the all-zero bit vector; both tree-clique
and path seeds are their roots/endpoints; barbell seed 1 is in its first
clique. No large graph was expanded to check these facts.

The small verification suite covered all seven families, three seeds,
alpha in `{1/4,1/7,1}`, and regularization densities equal to one-quarter,
three-quarters, and exactly the zero-solution threshold. It accepted:

- 189 exact optimal or zero answers;
- 126 nonzero-gap safe truncations with their independently computed exact
  objective gaps;
- and rejected all 126 corresponding false zero-gap claims.

The answers used to exercise the checker were generated with a separate
forward-elimination/back-substitution rational solver and exhaustive KKT
support enumeration. Objective values were independently evaluated in edge
form,

    alpha/2 * sum_i d_i f_i^2
      +(1-alpha)/4 * sum_{undirected edges ij}(f_i-f_j)^2
      -alpha*f_seed + alpha*rho*sum_i d_i f_i,

rather than by calling the benchmark's objective helper to construct the
expected answer.

## Source and objective verification scope

The sparse source formula is correct. For a density output `f_i=x_i/w_i`,
the dictionary called `source_numerator` contains exactly

    d_i*s_i/w_i = alpha*1_(i=seed)-q0*d_i*f_i+c*sum_(j~i)f_j.

Only the output support, its exposed neighbors, and the seed can have
nonzero source. Division by the original degree gives the correct density;
the sum identity is exactly `alpha*(1-mass(output))`. Positive output
entries, duplicate output labels, returned degrees, support volume, source
nonnegativity, and the `2*alpha*rho` density upper bound are checked.

For graphs with at most seven vertices, the exhaustive dense KKT oracle is
mathematically correct, and the independently assembled quadratic checks
both the actual gap and coordinatewise containment below the optimum.

For larger graphs, the returned objective bound is *not* independently
certified by the sparse checks. This is an explicit scope limit, consistent
with the existing `exact_optimum_comparison=False` flag. A concrete exact
witness is path(8), seed 1, alpha=1/4, rho=1/32. Its unregularized solution
has zero source, mass one, and volume 14<=32, so it passes all current sparse
checks when accompanied by a false objective certificate zero. Its actual
regularized objective gap is

    800525909 / 893841059840 > 1/1000000.

Accordingly, benchmark reporting must distinguish the exact sparse source
checks from the solver-returned objective certificate. The latter still
has the algorithm's theorem and implementation tests behind it; the sparse
checker alone does not establish it.

## Corrections identified and status

The initial read found two defects which were communicated immediately:

1. Constructor sizes below the valid domains admitted isolated vertices,
   duplicate cycle neighbors, or the height-zero tree degree mismatch.
2. Output-degree checks called `graph.degree` directly, bypassing the
   separate verification counter.

The parent corrected both before the recorded audit run. The recorded
version rejects all seven exercised invalid small parameter combinations,
and output-degree assertions now use the verification oracle.

Two remaining presentation/hardening points were also sent to the parent:

- On graphs above seven vertices, also require
  `0<=answer.objective_gap_bound<=epsilon`; the current upper-bound-only
  check accepts a negative claimed certificate.
- The dense small-graph reconstruction calls `graph.neighbors` directly,
  after the sparse verification snapshot is already taken. Thus the
  reported `verification_oracle` counts cover the sparse verification,
  not the optional dense reconstruction. Either label them explicitly as
  sparse-only or separately count the dense verification graph access.
  Neither operation contaminates the separately snapshotted solver counts.

The test harness and result record establish graph/checker correctness on
these finite fixtures. They do not certify the practical solver trajectory,
large-case objective accuracy, or a numerical running-time bound.
