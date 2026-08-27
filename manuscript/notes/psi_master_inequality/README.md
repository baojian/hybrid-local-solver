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
```

The second command is an independent exact-rational audit of the master
identity and the full algebraic cap representation.  Its committed output is
[`verify_master_identity.json`](verify_master_identity.json).
