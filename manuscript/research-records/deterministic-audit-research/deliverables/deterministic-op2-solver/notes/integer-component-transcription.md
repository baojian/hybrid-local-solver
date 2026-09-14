# Integer component transcription and a certified inactive-cap shortcut

The known-region solver stores density x_i=X_i/H and z_i=Z_i/H, with integer
counts and theta=1/T. Write alpha=A/D and Y_i=T X_i+Z_i. Direct substitution
in the exact averaged-coupling formula gives raw projected density

    q_i/w_i = n_i/(G d_i) - alpha rho T,
    G = 2 D H T(T+1),

    n_i = 2D(T^2-1)d_i Z_i
          + [2D-(D+A)T^2]d_i Y_i
          + (D-A)T^2 sum_{j~i, j in C} Y_j
          + 2A H T^2(T+1) 1{i=seed}.

Thus all per-coordinate raw-key work uses integers and original degrees.
Projection is the same box U=1/d_seed and mass cap1. Once the projected
density has been rounded downward to count Z_i^+, the primal count is

    X_i^+ = floor(((T-1)X_i+Z_i^+)/T).

This is exactly the rational component trajectory, not an approximate
replacement or a different convergence claim. Densities are materialized
only at PG certificate checks and termination.

To avoid unnecessary ordered-tree updates on a known bounded region, clear
the common shift into q_i/w_i=a_i/(B d_i). Let free indices have
0<a_i/(B d_i)<U and upper indices have raw density>=U. Then the exact box
projection mass equals

    sum_free a_i/B + U sum_upper d_i.

An integer comparison decides whether it is already <=1. If so, direct
integer floors give the exact rounded projection. If the cap is active,
install all current integer keys in the deterministic clipped reporter and
perform its exact finite-breakpoint search. Any reporter keys retained from
an earlier active-cap step are refreshed before use. This shortcut is only
for the known region of volume<=1/rho, where a full region pass is charged;
it is not used to scan the accumulated history in local continuation.

Correctness checks: 96 complete-trajectory cases / 6,144 exact iterations,
including 323 active-cap steps, passed before and after the shortcut. An
additional 32 full solver comparisons covered completed components, accepted
and rejected pilots, geometric checks and fixed horizons; final output,
route, iteration count, certificates and original graph replies matched
the rational implementation exactly. Result files have prefix
`component-integer-`. The public fast solver enables integer component state
by default; `integer_component=False` retains the rational reference.
