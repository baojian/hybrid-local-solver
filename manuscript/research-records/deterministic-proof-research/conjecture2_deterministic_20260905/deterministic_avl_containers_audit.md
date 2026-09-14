# Deterministic point-container component

`deterministic_avl_containers.py` is a separate implementation of the
integer point maps and sets needed to replace the solver prototypes'
hash tables. It does not change an active solver. It uses no random
procedure and no hash-table operation internally.

## Interface

`AVLMap` implements `collections.abc.MutableMapping`. Construction and
`update` accept another mapping or an iterable of key/value pairs.
Integer keys may be negative or arbitrarily large. It supports ordinary
item lookup, insertion/replacement, deletion, membership, length, `get`,
`setdefault`, `pop`, `popitem`, `clear`, and `copy`. Iteration is in sorted
integer-key order. The key, item, and value views are live; item and value
iteration walks the tree directly rather than performing another point
lookup per emitted record.

`AVLSet` implements `MutableSet` using the same map. It supports
construction, `add`, `discard`, membership, sorted iteration, length,
`clear`, `copy`, `update`, `union`, and `|`/`|=`. Other standard abstract-set
operations provided by the mixin use these deterministic primitives.

Structural changes invalidate an outstanding iterator; changing the
value stored under an existing key is permitted. `popitem` currently
removes the smallest key, which is allowed by the MutableMapping
contract. It intentionally does not reproduce dict insertion order.
Keys must be integers; membership of another type returns false, while
attempting an item operation with a noninteger key raises TypeError.

## Complexity and bookkeeping

Every node stores exact subtree height and size. Insertion and deletion
recompute those fields along one search path and use single or double
rotations to maintain height difference at most one. For height h the
minimum possible nonempty node count satisfies

    N(h) >= 1 + N(h-1) + N(h-2).

Thus height is `O(log(n+1))`. Point reads, writes, membership, and deletion
use `O(log(n+1))` integer comparisons in the worst case. Length reads the
root's cached size. A complete iterator costs O(n) work and a logarithmic
stack. Copying, construction, and repeated update currently cost
O(n log(n+1)); no unproved linear bulk-construction claim is needed.

The bit cost of comparing a very large graph label remains separate from
the number of comparisons, just as in the graph input model. Calling
`clear` drops the root in constant explicit work, but reclaiming its nodes
can cost O(n). Solver accounting must charge that reclamation; the
component does not describe it as free memory destruction.

## Deterministic verification

The independent test file `test_deterministic_avl_containers.py` passed
all five test groups. Its report is
`deterministic_avl_containers_verification.json`.

- All 15,018 insertion/deletion order pairs for labeled sizes zero through
  five were checked, including intermediate states and repeated value
  replacement.
- Mapping behavior, defaults, missing-key errors, pop operations, update,
  equality, copies, live views, and iterator invalidation were checked.
- Set construction, duplicate insertion, discard, copy, update, unions,
  and equality were checked over all insertion orders of sizes through
  five.
- Four structured insertion orders on 4,096 signed 2,049-bit keys were
  followed by alternating minimum/maximum deletion.
- Across 180,199 validated states and 726,197 visited nodes, every ordering,
  value, subtree size, stored height, and AVL balance check passed. The
  largest observed height was 15.

Reference dictionaries and sets are used only by the test oracle, not
by the production container implementation. No random test cases were
generated. Integrating the containers requires replacing point-map/set
construction sites as well as ordinary lookups; leaving a builtin set
union or dictionary comprehension on a critical path would retain that
prototype hash-table dependency.
