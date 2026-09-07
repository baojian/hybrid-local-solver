# Overnight probe: exact live-frontier Schur elimination

Date: 6 September 2026. **Proved here:** algebraic draft. **Open:** compressed
fill implementation with a near-linear total work bound. This is a baseline
for the main OP3 investigation, not a new general solver theorem.

Use `M=D-gamma*A` and `b=e_v-lambda*d`, with
`lambda=eps_appr/2` and `kappa=eps_appr/4`. Suppose the admitted set `A`
has been eliminated exactly. On its exposed exterior frontier retain the
Schur diagonal `s_i`, nonnegative effective conductances `w_ij`, and
transformed load

\[
\boldsymbol h=\boldsymbol b_{\bar A}
-\boldsymbol M_{\bar A,A}\boldsymbol M_{AA}^{-1}\boldsymbol b_A.
\]

For an exterior label, `h_i=r_i^A-lambda*d_i`. It is therefore safe to admit
any `i` with `h_i>kappa*d_i`. When no such label exists, the exact face
solution has exterior ACL residual at most `3*eps_appr*d_i/4`; the active
residual is `eps_appr*d_i/2`.

An admitted pivot has `s_i>0` and `h_i>0`. Write `z_i=h_i/s_i` for its
temporary eliminated value. Its elimination performs

\[
h_j\leftarrow h_j+w_{ij}z_i,\qquad
s_j\leftarrow s_j-w_{ij}^2/s_i,
\qquad
w_{jk}\leftarrow w_{jk}+w_{ij}w_{ik}/s_i.
\]

The surplus changes are positive. Check a vertex's gate whenever its surplus
changes, enqueue it once on crossing, and keep it queued until admission.
There is no need for a separate all-frontier quietness scan: every changed
gate was evaluated, and undiscovered labels have no adjacent admitted row.
One reverse traversal of stored elimination records supplies the final
solution. Old solution coordinates need not be written during discovery.

Original edges between two unexposed vertices are unknown. Store only fill
corrections between exposed frontier labels. When a pivot is admitted,
expose its original adjacency row, query degrees for newly encountered
labels, and add its original conductances to its retained fill row. Do not
preprocess the ambient graph or scan rows of inactive neighbors.

If `p_i` is the number of live effective neighbors at elimination, the
explicit implementation costs

\[
\widetilde O\!\left(V+\sum_{i\text{ admitted}}(p_i+1)^2\right)
\]

including fill updates, load changes, gate checks, stored records and final
back substitution. This gives a falsifiable work ledger, with **no** claim
that the sum is near-linear. The older chronological Cholesky calculation
in `spectral_balance_threshold_batch/README.md` retains admitted-face
factors; this alternative carries the unadmitted frontier and its loads.

The central-star control is already severe. Eliminating a center adjacent
to `m` leaves creates a positive clique among all leaves. If all leaves are
subsequently admitted, explicit pair updates number
`Theta(sum_(k=1)^m k^2)=Theta(m^3)`, although the original graph volume is
`2m`. For example, lazy `alpha=1/3`, `eps_appr=1/(8m)` and a center seed
give a strictly positive leaf surplus above the chosen gate after the first
pivot; all leaves are queued and every later update is positive. This is a
representation-specific obstruction. Rank-one clique compression makes the
star easy, and no universal lower bound follows.

The next cyclic-family experiment must separately meter original row
exposure, fill storage/updates, surplus/gate updates, unsuccessful searches,
and final reconstruction. An implicit clique is useful only if its effect
on future gates can also be produced without visiting every member after
each pivot. No implementation or measured fill experiment has yet been
claimed for this baseline.
