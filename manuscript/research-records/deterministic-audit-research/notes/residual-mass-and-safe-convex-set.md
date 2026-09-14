# A residual-mass sufficient condition for the proved-rate coupling

This concerns the **unrepaired**, mass-capped averaged coupling. Its root
energy contraction is proved. Its cumulative row-volume bound is open.

In original coordinates its prethreshold score satisfies the exact identity

\[
h=qz+s y+(b-Qy)/s.
\]

Consequently, for nonnegative x,z and hence y,

\[
H:=w^T[-h]_+\le \frac1s w^T[Qy-b]_+.
\]

Combining this with the existing signed score ledger shows that

\[
\sum_{k<T}w^T[Qy_k-b]_+
\le C\alpha T
\quad\Longrightarrow\quad
\rho\sum_{k<T}\operatorname{vol}(\operatorname{supp}z_{k+1})
\le (1+C)T.
\]

Polylogarithmic C would suffice for OP2. This is a sufficient condition,
**not an established trajectory estimate**. It is stronger than controlling
the original signed score debit, so it may fail even when that debit is small.

There is a related useful convex-set observation. Let

\[
\mathcal C=\{x\ge0:Qx\le b\}.
\]

The desired regularized optimum belongs to C: on its positive coordinates,
`Qx*=b-alpha rho w`; on its zero coordinates the Stieltjes off-diagonal
signs give `Qx*<=0<=b`. If both x,z belong to C, their convex combination y
does too, and the displayed score identity gives `h>=qz+s y>=0`.

This does not supply a cheap projection onto C or show that the accelerated
update preserves C. Projecting onto it is a nonlocal constraint problem.
The existing repository safe-box and positive-barrier rounding notes already
warn against treating such one-sided repairs as a free primitive; see
`manuscript/notes/spectral_balance_threshold_batch/POSITIVE_BARRIER_SAFE_SUPERSOLUTION_ROUNDING.md`.
This observation is therefore an interface reduction, not a new solver proof.
