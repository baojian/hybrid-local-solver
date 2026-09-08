# A deterministic replacement for the alpha-floor full-graph solve

The seventh-block conditional floor theorem used a complete supplied solver
when the native positive support was the whole graph. A stronger reduction
was found while exploring proper-envelope ranges. It needs only arithmetic.

For every nonnegative-residual potential at gamma_eff, the existing edge
bound gives global oscillation at most `(n-1)/gamma_eff`, EVEN ON FULL
SUPPORT. On a graph fully materialized by the volume/closure pass, put

    rho_i = (e_v - M_target*x)_i / d_i,
    m = min_i rho_i,
    c = m / bar_alpha_target,
    y = x + c*1.

On the native good event m>=0. The neighborhood average `(Ax)_i/d_i` lies
between min(x) and max(x); hence its oscillation is at most that of x.
The width of rho is at most native_accuracy plus
`(gamma_target-gamma_eff)*B/gamma_eff <= eps/2 + eps/2`.
Adding c subtracts exactly m from every normalized original residual.
Thus y>=0 and its original target residual lies in `[0,eps*d]`.

The full-support repair reads no outside rows, calls no numerical solver,
and costs O(B log B) comparisons/arithmetic/copied words after the same
paid volume/closure pass. The exact constant can be very large as target
alpha tends to zero; this is one exact-real word, not a floating-point or
bit-complexity assertion. The native production work remains explicit.

`small_alpha_constant_shift.py` implements and exactly checks this repair,
with native obstacle, seed-perturbed and constant-shifted validators. Full
runs include alpha=2^-1024 and verify the final normalized output mass.
This strengthens the earlier reduction; it still does not supply a fast
native producer at the accuracy-squared floor.

## A further supplied-envelope consequence under development

Keep the ORIGINAL obstacle lambda=eps/2 and envelope tolerance delta=eps/8.
The numerical/clip bridge actually guarantees native residual at most
`lambda+3delta=7eps/8`, leaving margin eps/8. Its support volume is below
B=2/eps. Therefore use the smaller floor

    a0 = (eps/8)/(2B+eps/8) = eps^2/(32+eps^2).

The target-lambda obstacle decreases coordinatewise when alpha increases.
Thus an envelope for the target-alpha obstacle also contains every
significant coordinate of the SAME-lambda effective-alpha obstacle.
Use a seed shortcut at accuracy 7eps/8 while keeping lambda unchanged;
otherwise run the supplied solver with the original delta. The parameter
floor bounds every inverse-alpha numerical range by a polynomial in 1/eps.
The new arithmetic support wrapper handles target alpha afterward.

This would give `(1+V) polylog(2+V+1/eps+1/p)` supplied-envelope work,
including output and all failures, independent of target alpha even in
logarithms. The constant shift still uses one division by target bar_alpha
in exact-real arithmetic. It remains a SUPPLIED result, with no finder.
Do not silently change lambda to half of the 7eps/8 native error budget.
