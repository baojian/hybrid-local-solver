# Optional constant-pivot global trial — proved design, not implemented

This observation is separate from the delivered solver. The implemented
exact branch requires a completed component of at most sixteen vertices.
The following bounded global trial could also recognize a small exact
support inside a much larger component. It does not change the delivered
algorithm or its verification claims.

Work in degree densities with symmetric Stieltjes energy matrix
H=D^(1/2)QD^(1/2), and q=alpha e_seed-alpha rho d. A face solution on S
satisfies H_SS f_S=q_S and is zero elsewhere. Start from S empty and f=0.
On any inactive coordinate with positive violation

    v_j=q_j-H_jS f_S>0,

append j and solve the enlarged face using incremental exact LDL factors.
The new Schur pivot is positive. Consequently its new coordinate is
v_j divided by that pivot, hence positive. The old face values increase by
-H_SS^(-1)H_Sj f_j>=0. All active values stay strictly positive.

Every such face solution is below the full obstacle optimum f*. Indeed,
write the full optimum's nonnegative slack as omega=Hf*-q. On S,

    H_SS(f*_S-f_S)=omega_S-H_S,outside f*_outside>=0.

Inverse positivity implies f*_S>=f_S. A positive inactive violation can
therefore occur only where f*_j>0: otherwise the full optimum's KKT
inequality, off-diagonal signs and f*>=f would imply v_j<=0. Thus every
opened row lies in the unknown true support, and the total original
degree-volume of distinct opened rows is at most 1/rho. This support is
not supplied to or computed by an uncharged oracle.

For any face, an inactive violation can occur only at the seed or a neighbor
of the active rows. Scan those rows to construct the exact response and
enumerate this finite boundary. Query every newly exposed original degree
and charge all repeated incidences and balanced-tree state operations.
If no inactive violation remains, the face solution is the exact global
optimum, and it may be returned with gap bound zero.

Fix an absolute pivot limit p0, such as sixteen. After at most p0 additions,
either certify the exact optimum or discard the trial's numerical state
and use the existing proved algorithm. Recomputing the boundary response
after each pivot costs O_tilde(p0/rho), all factorization work costs
O(p0^3), and storage is O(1/rho+p0^2). With p0 fixed, this trial plus a
complete fallback preserves OP2. Exact rational growth in the small factors
also remains a constant multiple of encoded input lengths. No randomized
pivoting or large exact face factorization is required.

An implementation must keep its trial row cache separate from the bounded
pilot's definition of C. The current pilot takes C to be the prepass-scanned
region. Silently replacing C by a union with earlier trial rows could
invalidate its asserted volume<=1/rho budget. Reusing cached rows is valid,
but the original pilot region and all extra trial charges must remain
explicit. This interface issue is why the optional design has not been
inserted into the otherwise finalized implementation during this audit.

This is an elementary bounded use of the previously explored safe active-set
direction. It does not supply a support-linear implementation for an
unbounded number of exact pivots, and it is not a claim of historical novelty.
