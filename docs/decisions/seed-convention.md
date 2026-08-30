# Seed Convention

- **Status:** Accepted for the canonical research target
- **Last updated:** 2026-08-29
- **Applies to:** The controller-level end-to-end PPR/RPPR problem and any
  theorem described as solving that target

## Decision

The canonical computational input is one seed vertex `v`, represented by the
standard basis vector

```text
s = e_v.
```

The desired graph-uniform exact-real work scale is therefore

```text
O_tilde(1 / (sqrt(alpha) * eps_ppr)),
```

with constant seed-input cost. A theorem for a general sparse unit-mass seed
distribution is a stronger extension and must state its additional dependence
on the seed support and weights.

## Boundary of the decision

The shared source-aligned algebra continues to allow
`s >= 0` and `1^T s = 1`. This preserves source results and standard facts
that are genuinely valid for every probability seed. It does not make the
general distribution part of the central complexity contract.

For the unregularized PPR map, linearity gives

```text
pi(s) = sum_v s_v pi(e_v).
```

This identity does not preserve the desired work bound for free: separately
solving every point source can multiply the principal work by the number or
effective mixture size of the sources. The RPPR minimizer and its active-set
chronology are nonlinear in `s`; no analogous superposition rule is assumed.

## Consequences

- Core theorem statements and research targets say `s=e_v` explicitly.
- General-seed source facts, lower bounds, and proved stronger theorems keep
  their original scope.
- Point-source counterexamples remain valid against any algorithm claimed for
  all sparse seeds, because point sources are a subclass.
- A general-seed corollary must include input, merging, output, and any
  per-source or mixture-dependent work.
