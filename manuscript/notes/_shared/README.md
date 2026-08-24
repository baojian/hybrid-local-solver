# Shared research control layer

This directory is the controller-owned entry point for all standalone research
directions. It contains shared navigation and status, not duplicate proofs.

Read in this order:

1. [`problem_definition/README.md`](problem_definition/README.md) — the exact
   working PPR/RPPR target, output guarantee, and work ledger;
2. [`related_work/README.md`](related_work/README.md) — the comparison map and
   current source-paper boundary;
3. [`results/README.md`](results/README.md) — reusable proved facts, important
   obstructions, and common open interfaces;
4. [`coordination/README.md`](coordination/README.md) — the multi-agent update
   and redistribution protocol;
5. [`coordination/BROADCAST.md`](coordination/BROADCAST.md) — the latest
   verified cross-direction message;
6. [`coordination/rounds/README.md`](coordination/rounds/README.md) — the
   durable assignment, adjudication, and redistribution history.

The build inventory and machine-readable research map are unified in
`../registry.toml`; every ordinary sibling directory remains
an independently buildable direction note. Files here are deliberately not
registered as standalone LaTeX notes.

## Authority boundary

This layer summarizes the current working tree. It does not override the
repository-root `AGENTS.md`, accepted decisions, mathematical conventions,
source PDFs, or proofs in a direction's `main.tex`. If a summary and a proof
disagree, stop propagation, mark the discrepancy, and repair the summary only
after checking the authoritative source.
