# path_terminal_modal_block

This note isolates the open terminal-face mechanism in the short endpoint-path
candidate from `volume_gated_acceleration`. It proves the exact weighted cosine
decomposition, the scalar damped-wave formula, the literal global-correction
range implication, explicit prefix optima/transports, the exact entry-velocity
quadrature, and pointwise nonpositivity of the ideal packet evolution.
Conditional on an explicit proper-prefix chronology---inactive projection,
zero safe correction, and one next-singleton admission at every prefix---it
also proves the exact three-frontier changing-face source and its factored
Fourier transform.
The chronology itself is now reduced exactly to one shared-coordinate sign:
if `D_n(j)=-r_n(p_n)(j)+(1-q)r_(n-1)(p_(n-1))(j)/2 >= 0`, then raw
positivity, nonpositive post-step residual, zero correction, and strict next
admission all follow with explicit rational slack. The uniform proof of this
sign remains open.
It also gives exact nonnegative position/velocity propagators, isolating the
remaining factor-`k` velocity-cancellation obstruction. It then proves a conditional
anti-cancellation theorem: two quantified entry
position/velocity profile bounds plus projection/envelope regime preservation
would force `Omega(q^-1 log(1/q))` terminal steps for the named
transported-center execution.

The shared-coordinate sign (and hence the full proper-prefix chronology), the
two entry profiles, and the terminal projection/envelope regime are not
proved. A deterministic NumPy screen reconstructs
the actual admission trajectory, measures the packet and modal defects, checks
the sharpened profiles and projection/envelope margins, verifies the exact
velocity identity, and reports both the first range crossing and the first
literal safe-envelope certificate. A rational-arithmetic preflight separately
checks the source support, every displayed boundary entry, and the formal
Laurent-polynomial transform identity at representative prefixes, conditional
on the replayed chronology. A second rational preflight checks the new
frontier constants, shared/frontier residual identities, post-residual
identity, and finite shared-sign replay at `m=8,12`, while explicitly printing
`uniform_shared_sign=open`. Subject to the open chronology, the remaining
entry-profile problem is a sharp signed summation of those source traces, not
their support calculation. Numerical observations are labeled
**Measured**, not promoted to an asymptotic theorem or a lower bound for other
algorithms.

Build with `make`. Run the screen with:

```bash
python3 verify.py 128 256 512 1024
```
