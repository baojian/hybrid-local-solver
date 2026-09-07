# Relative Schur-key accuracy is not an ACL quietness certificate

Date: 7 September 2026. **Refuted:** replacing an exact normalized extreme
query by a constant-relative approximate extreme query, and accepting its
nonpositive returned gate as a global ACL quietness certificate.
This is a specific oracle-contract failure. It does not refute approximate
solvers or the geometric publication interface on original vertex values.

The two-port frontier record has original boundary surplus

\[
 g_j=h_j+\boldsymbol a_j^T\boldsymbol u_C,
 \qquad \boldsymbol p_j=\boldsymbol a_j/(-h_j),\quad h_j<0.
\]

An exact query checks `max p_j·u_C>1`. If an approximate query returns an
actual stored point with value within a factor `1+eta` of the maximum,
a returned value at most one implies only

\[
 g_j\leq\eta(-h_j) \quad\hbox{for every boundary vertex j}.
\]

The relevant error scale is the original `lambda*d_j`. Eliminated negative
loads accumulate in `-h_j`, so the ratio `(-h_j)/(lambda*d_j)` can grow
with an active path length. This is why a constant relative key error is
different from the permitted finite band on original vertex values.

## A source-valid two-arm witness

Use a degree-two seed and two ordinary path arms. Admit L vertices on one
arm and M on the other. The full finite arm lengths are L+2 and M+2,
so both next inactive tips have actual degree two.
Keep the seed and eliminate the admitted arm vertices. In the limit
gamma=1, an arm of length k has

\[
 a_k=\frac1{k+1},\qquad -h_k=\lambda(k+2),\qquad
 \frac{-h_k}{\lambda d_{\rm tip}}=\frac{k+2}{2}.
\]

The retained seed matrix and load are

\[
 H=\frac1{L+1}+\frac1{M+1},\qquad
 f=1-\lambda(L+M+2).
\]

Choosing `lambda=(L+1)/((L+M+2)(L+M+3))` puts the M-tip exactly at its
threshold in this limit. The L-tip's normalized value is
`(M+1)(M+2)/((L+1)(L+2))`. For M only slightly larger than L, this is
above one but below 1.1. The gamma=1 calculation motivates the construction;
the actual falsification uses strictly admissible gamma<1 and exact fractions.

The registered `schur_relative_reporter_probe.py` uses

\[
 M=L+\lceil L/40\rceil,\qquad
 \gamma=1-(L+M+3)^{-4},\qquad
 \alpha=\frac{1-\gamma}{1+\gamma},\qquad
 \varepsilon_{\rm appr}=2\lambda.
\]

Every preceding admission is checked to have a strict positive gate and to
be a permitted 1.1-approximate normalized extreme return. The trace first
balances the arms, then advances the slightly longer arm through permitted
approximate returns. It finally permits the quiet M-tip to be returned
while the L-tip still violates the original ACL tolerance. Thus this is
an endogenous legal approximate-reporter trace, not an externally imposed
pair of port values.

| L, M | True normalized maximum | Permitted quiet return | Original residual / requested degree tolerance |
|---|---:|---:|---:|
| 64, 66 | 1.0619947 | 0.9999905 | 1.5229109 |
| 128, 132 | 1.0627285 | 0.9999976 | 2.5386757 |
| 256, 263 | 1.0551075 | 0.9999994 | 4.0544327 |

Displayed values are rounded; all inequalities were checked with fractions.
The smallest witness uses `alpha=1/625801441`, `lambda=65/17556` and
`eps_appr=65/8778`. An independent full tridiagonal face solve, with the
seed in the interior of the ordered path, verifies its positive coordinates
and both original tip residuals. The three cases contain 909 strict
admission checks and 912 independently reconstructed active coordinates.
The final source hash and parameters are in
`SCHUR_RELATIVE_REPORTER_AUDIT.json`.

An initial attempt to grow one whole arm before the other failed the strict
gate check. That chronology is invalid and is not used in the witness.
The final audit checks the approximate-return contract at every step.

## Consequence for the next direction

The exact planar reporter remains valid. An approximate higher-dimensional
replacement needs an error guarantee at the original degree-residual scale,
or an additional bound on accumulated Schur loads. A constant relative
maximum guarantee by itself is insufficient. This does not rule out a
different terminal repair; it invalidates the claimed quietness certificate
needed to invoke the existing terminal-completion proof.
