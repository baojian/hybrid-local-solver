# AESP--local-refinement hybrid research note

This standalone note studies an AESP/Catalyst burn-in followed by
momentum-free local refinement or a structured exact response. The proof
source is `main.tex` and its included sections; [`STATUS.md`](STATUS.md) is the
current claim ledger and operational handoff.

The note proves finite correctness after any finite signed handoff,
trajectory-dependent work bounds, conditional confinement corollaries, and
fully charged response constructions on several fixed graph families. The
branch-caterpillar sequence develops response-free lower gates, transported
lower states, an implicit residual heap, incremental face carry, sparse
auxiliary appends, and two genuine nonsettled continuations. The latest exact
`reset_budget_obstruction` audit separates three facts:

- the declared observable settled reset budget cannot be paid by an
  alpha-uniform or `O(1/sqrt(alpha))` multiple of face-optimum drops;
- the actual analytical settled shock is still within a constant multiple of
  the drop and the inner stage uses its initial budget only logarithmically;
- the quadratic no-sharing product count belongs only to that literal
  representation and is not a class lower bound.

The central early-AESP locality lemma

```text
max_{1 <= t <= J} overline_vol(S_t) / gamma_t = O(1/epsilon)
```

with a graph-independent hidden constant remains open. Therefore the
graph-uniform `O_tilde(1/(sqrt(alpha)*epsilon))` end-to-end work claim remains
open and must not be promoted to the active manuscript. The proved
trajectory-dependent theorem and explicitly conditional confinement
corollaries remain valid in their stated scopes.

Build and audit from the repository root with:

```bash
make -C manuscript/notes/hybrid_aesp_locsor
uv run python -m experiments.proof_audits.runner \
  --tier full --note hybrid_aesp_locsor
```

The nine mechanism-based audit IDs are listed by `make research-audit-list`;
their provenance spans Rounds 014--022. Passing them does not establish a
speedup, an arbitrary-graph locality lemma, or a finite-precision theorem.
