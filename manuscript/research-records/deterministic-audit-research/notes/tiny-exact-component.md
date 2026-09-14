# Exact deterministic solving on a fixed-size completed component

The default wrapper now treats a completed retained component with at most
sixteen vertices by exact monotone active-set LDL elimination. This addresses
a practical weakness of generic acceleration on a tiny closed graph when
alpha is extremely small. The size limit is fixed, enforced in the routine,
and independent of all problem parameters. `tiny_exact=False` disables it.
An incomplete pilot is never accepted merely by this restricted solver.

Use degree densities f=x/sqrt(d). The component energy has symmetric matrix

    H_ii=(1+alpha)d_i/2, H_ij=-(1-alpha)/2 on internal edges,
    q_i=alpha 1_(i=seed)-alpha rho d_i.

H is a positive definite Stieltjes matrix; the original degrees include all
edges leaving the retained region. Start with the empty active set and f=0.
If an inactive coordinate j has violation q_j-H_jS f_S>0, append j, extend
the exact LDL factorization of H_SS, and solve the enlarged face system.
Choose the first violating coordinate in the sorted component order.

The new Schur pivot is positive. The new coordinate equals its positive
violation divided by that pivot. On old coordinates the change is

    -H_SS^(-1) H_Sj f_j >= 0.

Thus all active coordinates stay positive and every coordinate is appended
at most once. Termination after at most |C| additions gives nonnegative
slack off the active set and zero slack on it, hence the unique exact
obstacle optimum. A completed degree-pruned seed component contains the full
optimum, so this exact result can be returned directly, with gap bound zero.
It is a final output; no rational-to-dyadic warm-start assumption is made.

Building the small matrix costs O(|C|^2), and incremental LDL updates plus
triangular solves cost O(|C|^3) in total. Original discovery and assembly are
charged separately. Since |C|<=16 is an enforced absolute constant, this
additional work preserves O_tilde(1/(rho sqrt(alpha))) in the nonzero regime.
The finite elimination uses rational arithmetic and comparisons only, with
no square roots and no random pivoting. Constant matrix size also bounds
all intermediate rational encoding lengths by a constant multiple of the
input-word encoding length. The separate bounded-arithmetic result is
therefore preserved; no general large-face exact-solve shortcut is claimed.

The general continuation and boundary-forest algorithms remain available for
larger components and incomplete discovery. Their independent trajectory
audits explicitly disable this optional tiny-component branch so that the
new fast path does not dilute their coverage.

Verification completed: 3,699 exact comparisons against independent active
face enumeration, across every connected graph on two through five vertices,
three boundary-degree patterns, all seed vertices, three regularization
ratios, and three alpha values. All passed. Eight complete path cases of
size 2, 4, 8 and 16 at alpha=1e-20 and 1e-80 matched independent exact full
linear solutions. At size 16 and alpha=1e-80 the solve took about 0.19 seconds,
used 16 pivots and inspected 30 original incidences. These are structured
measurements, not a general wall-clock guarantee.
