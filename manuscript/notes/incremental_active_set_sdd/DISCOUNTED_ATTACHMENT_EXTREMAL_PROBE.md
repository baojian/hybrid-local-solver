# A possible sharper saturation bound

Date: 7 September 2026. **Open.** This strengthening is not used by
`thm:op3-bounded-attachments`, which retains its proved conservative bound.

For a tree attachment with q vertices and discounted center-hitting time
`p_i=E_i[gamma^tau]`, the endpoint of a q-vertex attached path has

\[
 p_{\rm path}=\frac1{T_q(1/\gamma)},
 \qquad T_q(\cosh\theta)=\cosh(q\theta).
\]

The recurrence follows from the path harmonic equations and the reflecting
degree-one endpoint. Test the stronger conjecture

\[
 p_i\geq\frac1{T_q(1/\gamma)}
 \quad\text{for every q-vertex tree attachment and every starting vertex.}
\]

All 2,247 exact rooted-tree/parameter cases through q=9 pass; equality occurs
on endpoint-rooted paths. The registered audit
`discounted_attachment_extremal.py` records the individual coordinate counts
and source hash. This is measured evidence, not a proved comparison.

Why it matters: the sharp minimal backward cycle recurrence has

\[
 y_k+\frac{\lambda}{1-\gamma}
 \geq \frac{\lambda}{1-\gamma}
       \frac{\cosh((k+1/2)\theta)}{\cosh(\theta/2)},
 \qquad \cosh\theta=1/\gamma.
\]

This exceeds `lambda*T_k(1/gamma)/(1-gamma)` for k>0. The conjectured
attachment bound would therefore settle every q-vertex attachment by q
cycle steps behind the active end, replacing the current `2q^2` window.
It would improve the event-processing factor without changing the solver.

The existing mean-hitting result does not prove this Laplace-transform
comparison. The primary online manuscript
[*Reversible Markov Chains and Random Walks on Graphs*, §5.3](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch5.S3.html)
gives the exact edge mean in Theorem 5.20, equation (5.81), and the maximal
mean bound in Proposition 5.24(b). These justify the familiar mean facts,
not the stronger discounted inequality.

A possible algebraic route is to set `s=1/gamma>=1` and
`K=s*D-A` on the attachment. Then `p_i=(K^{-1})_{i,r}` for the attachment
root r. The desired inequality becomes
`T_q(s)*cofactor_{r,i}(K)-det(K)>=0`. Both determinant and cofactors admit
tree/forest expansions. Testing coefficient positivity after `s=1+z` could
identify a stronger inductive claim. The exact integer-polynomial audit now
checks this coefficient positivity for all 6,155 rooted-tree/start pairs
through q=9. It passes, and its determinant/cofactor evaluations agree with
every independent rational hitting solve. Thus the finite enumerated graph
cases cover all `0<gamma<1`, while the statement for arbitrary q remains
**Open**. A general coefficient induction is still missing. A mean bound
or a few moments cannot be substituted for it.
