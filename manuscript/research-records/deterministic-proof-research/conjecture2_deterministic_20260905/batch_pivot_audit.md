# Independent audit of the fresh batch-pivot decay proof

Audited file: `batch_pivot_decay.md` in this same newly created research directory. No other manuscript notes or historical work were read. Status: no substantive proof error found. This audit does not assert the missing fully charged arithmetic result.

1. **Safe pivots and completion.** The Schur complement is a positive-definite M-matrix. Its inverse is nonnegative and has positive diagonal, so a strictly positive new residual makes every new coordinate positive; old coordinates increase. The comparison to the global obstacle optimum is correct. Empty strict-violation set gives KKT, including degenerate zero margins.

2. **Energy orthogonality.** Both consecutive exact solves have zero residual on the older support, hence `(Q Delta_t)_{S_{t-1}}=0`. An earlier increment is supported there, proving pairwise Q-orthogonality. The objective-gap identity is valid because `x^(T)-x*` is supported in `S*`, on which the global KKT multiplier vanishes. It would need an extra linear term for arbitrary supports; the safe-support property supplies exactly the missing condition here.

3. **Cholesky signs and energy coordinates.** Scalar Cholesky of an SPD Z-matrix has positive diagonal and nonpositive strict lower entries by the stated recurrence. Its inverse, and the inverses of its diagonal admission blocks, are nonnegative. The diagonal Schur block equals `L_tt L_tt^T`; consequently `z_t=L_tt^(-1)r_t` is nonnegative and the increment energy equals `||z_t||²`.

4. **All-violations recurrence.** A vertex admitted at stage `t` had nonpositive residual at stage `t-2` because every strict violation was admitted in the intervening batch. Subtracting the intervening update, eliminating older variables, and using `C_{t,t-1}=L_{t,t-1}L_{t-1,t-1}^T` gives exactly `r_t<=-L_{t,t-1}z_{t-1}`. Multiplying by `L_tt^(-1)>=0` is legitimate. The proof correctly avoids multiplying an inequality by a sign-indefinite transpose.

5. **Bidiagonal comparison.** Dropping long-range nonpositive lower blocks gives `L<=B`. Both inverses are nonnegative, and `L^(-1)-B^(-1)=L^(-1)(B-L)B^(-1)>=0`. Entrywise domination of nonnegative matrices implies 2-norm domination. The block diagonal and first block subdiagonal each have norm at most `||L||`; therefore `||B||<=2` and `||B^(-1)||<=alpha^(-1/2)`. This proves the claimed spectrum of `BB^T`. The comparison recurrence `z_t<= (B^(-1))_{t1}r_1` follows by induction.

6. **Chebyshev and indices.** `H=BB^T` is block tridiagonal and `B^(-1)=B^T H^(-1)`. A degree `ell-1` polynomial in `H`, premultiplied by `B^T`, has block bandwidth at most `ell`. At `ell=t-2`, its `(t,1)` block vanishes since its distance is `t-1`. The resulting bound `4 alpha^(-1) q^(t-2)` is correct; the separate `t=2` bound is loose but valid.

7. **Tail and constants.** Squaring the increment bound, summing the orthogonal tail, and dividing by two gives `8 q^(2(T-1))/(1-q²)`. For `q=(2-sqrt(alpha))/(2+sqrt(alpha))`, the displayed inequalities imply the stated `9 alpha^(-1/2) exp(-2 sqrt(alpha)(T-1))`. The ceiling formula therefore yields additive objective error epsilon. `alpha=1` is harmless because the algorithm actually finishes after the seed solve.

8. **Cost boundary.** The exact support is not supplied or scanned for free; it appears only in the analysis. Boundary records are obtained from adjacency lists of safely admitted vertices. The proof charges exposed adjacency entries and repeated explicit boundary evaluation correctly. It explicitly does not charge the successive exact restricted solves as free in its final claim, so it does not establish OP2.

9. **Terminology refinement.** The result bounds the number of exact-solve stages sufficient for a given objective tolerance. It is not a margin-independent bound on the number of stages required for exact support identification or exact termination. Wording such as “exact batch depth” should always retain this accuracy qualification.

10. **Star obstruction.** The inverse formula in the final section is correct, as is strict activation of every leaf for the displayed regularization. It rules out the proposed decay with arbitrary singleton admission order and eager updates, not batching or OP2 generally.
