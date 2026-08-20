# local_solver_oracle_hierarchy

This standalone note separates adjacency access from the computational and
representation restrictions used in local-solver lower bounds. It proposes a
capability hierarchy covering unrestricted computation on the exposed graph,
materialized repeated restricted solves, local linear-span recurrences, and
persistent Schur/response state.

For degree-normalized additive PPR error, the note now proves:

- seed-connectedness and degree volume at most `1 / epsilon` for the exact
  superlevel core;
- a matching `Theta(1 / epsilon)` explicit-output bound using a center star;
- an alpha-killed capacity packing theorem for internally disjoint seed
  corridors;
- the resulting `M * L = O(1 / epsilon)` obstruction at diffusion depth
  `L = Theta(1 / sqrt(alpha))`;
- an exact finite-path completion sensitivity formula showing that this
  indistinguishability construction also stays within the output scale; and
- the constant-rank Woodbury formula governing degree-preserving hidden-edge
  swaps.

The optimal variable-alpha adjacency-query complexity remains open. The note
states killed-Green influence packing as the central information-level
conjecture and recurrence-versus-response separation as the central
computational-model target. It does not claim a universal
`Omega(1 / (epsilon * sqrt(alpha)))` lower bound.

Build from this directory with:

```bash
make
```
