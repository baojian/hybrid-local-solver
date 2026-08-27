# psi_master_inequality

This note studies the exact one-step Lyapunov master form for the clipped
accelerated proximal recurrence.  It independently reconstructs the identity,
makes the admissible algebraic cap domain explicit, and separates the two
unmixed sign channels from the genuinely mixed clipping obstruction.  It
seeks analytic nonpositivity proofs on infinite graph families, structural
sufficient conditions, or exact counterexamples.

Build from the repository root with:

```bash
make -C manuscript/notes/psi_master_inequality
python3 manuscript/notes/psi_master_inequality/verify_master_identity.py
python3 manuscript/notes/psi_master_inequality/verify_complete_bipartite.py
python3 manuscript/notes/psi_master_inequality/verify_complete_multipartite.py
```

The second command is an independent exact-rational audit of the master
identity and the full algebraic cap representation.  Its committed output is
[`verify_master_identity.json`](verify_master_identity.json).
The third command checks the closed resolvent and squared-kernel formulas for
all `K_{a,b}` with `1<=a,b<=8` in exact rational arithmetic; its committed
output is
[`verify_complete_bipartite.json`](verify_complete_bipartite.json).
The fourth command exactly checks the unequal complete-multipartite block
inverse, the continuous simplex-Bernstein certificate used in the analytic
theorem, and all 493 unordered part vectors through 14 vertices.  Its
committed output is
[`verify_complete_multipartite.json`](verify_complete_multipartite.json).
