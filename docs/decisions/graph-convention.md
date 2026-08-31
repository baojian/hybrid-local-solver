# Graph Convention

- **Status:** Accepted for the canonical research target
- **Last updated:** 2026-08-29
- **Applies to:** The controller-level end-to-end PPR/RPPR problem and every
  theorem described as solving that target

## Decision

The canonical input graph is finite, simple, undirected, connected, and has
unit edge weights. We also require `|V| >= 2`, so every degree is positive and
the normalized operators using `D^(-1/2)` are well defined.

Equivalently, the canonical graph is an unweighted connected simple graph
with at least one edge. The algorithm receives adjacency-list access; it is
not given a dense adjacency matrix or a free global connectivity scan.

## Why connectedness is without loss for the point-source target

Suppose a larger unit-weight simple graph has positive degrees but may be
disconnected, and the source is `s=e_v`. Let `C(v)` be the connected component
of `v`. After permuting vertices, the PageRank matrix is block diagonal and
the load is supported only on the `C(v)` block. Therefore:

```text
x^0_i = x^star_i(rho) = 0    for i outside C(v),
```

and both restricted solutions on `C(v)` are exactly the solutions obtained by
running the same PPR/RPPR definitions on the induced component. Vertex degrees
inside a connected component are unchanged. Thus restricting the canonical
point-source problem to connected graphs loses no solution behavior and does
not add a global preprocessing charge.

This reduction does not apply unchanged to a general seed distribution whose
mass lies in several components; that case remains a stronger extension under
the seed convention.

## Consequences and limits

- `d_i >= 1` follows from connectedness and `|V| >= 2`; a separate no-isolate
  assumption is unnecessary.
- For `0 < alpha < 1`, point-source PPR is strictly positive on every vertex.
- The normalized Laplacian has a simple zero eigenvalue, and normalized
  adjacency has a simple Perron eigenvalue `1`.
- Ambient connectedness does **not** imply that an explored, active, or
  restricted induced face is connected. Componentwise face analyses remain
  necessary.
- Combining ambient connectedness with the point-source support lemma does
  simplify the exact RPPR optimum: its support is either empty or connected
  and contains `v`.
- Results proved for all no-isolate or disconnected graphs remain valid in
  their stated stronger scope; historical records are not rewritten.
