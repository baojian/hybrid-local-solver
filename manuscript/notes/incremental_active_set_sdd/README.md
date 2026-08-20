# incremental_active_set_sdd

This standalone note audits the repeated-active-set factor in the August 2026
Wei--Yang PageRank/RPPR algorithm and asks exactly what is required to remove
it.  The note proves an exact block-Schur correction identity and a telescoping
energy law for nested restricted systems.  It also proves that warm starts
alone do not remove repeated-prefix work: any implementation that explicitly
materializes the whole active solution after every expansion has quadratic
write cost on endpoint paths.

The positive result is exact and stronger on the same graph class.  On an
endpoint-seeded path, a one-pass `LDL^T` message computes every active-set gate
in constant arithmetic per admitted vertex and materializes the solution only
once, in a final reverse pass.  Its total charged work is linear in the final
active volume, with no repeated factor and no polynomial dependence on
`1 / alpha`.  The source ACL and RPPR correctness arguments continue to hold
because the replacement uses exact restricted solutions.

For arbitrary graphs, the note gives a conditional plug-in theorem for an
implicit incremental solve-and-boundary interface.  Constructing that
interface with near-linear total local work remains open: the block correction
can be dense, and the energy telescope does not pay for full active-set matrix
passes or repeated vector output.

Build from this directory with:

```bash
make
```
