# A weaker local envelope target for OP3

**Completed reduction and sharper obstruction in block 12.** The envelope and ACL repair statements are proved and exact-audited: 1,097 physical cases, 19,925 supplied envelopes and 751,993 original residual certificates. Three finite original-tree witnesses pass complete quotient KKT checks. A separate explicit positive subsolution proves an asymptotic obstruction to FIFO BFS discovered-label envelopes, even with degree filtering; 67 exact instances check all 10,138 positive subsolution rows. This is a rule-specific lower bound, not an OP3 lower bound. The source below is the historical starting proposal.

**Validator change.** The initial whole-forest response-curve computation was terminated without a completed result because inactive distant vertices made exact rational curves expensive. The final finite witness uses repeated exact positive-face tree solves and checks every original quotient row. It finishes all three cases in 5.587 seconds. The implicit quotient is still a validator convenience, never a free local oracle.

Block 12 continuation candidate. **Conditional until proved/audited.**
This is a useful final local-work direction after the supplied numerical
recursion, not a claim that the envelope can already be found cheaply.

Let u solve the full physical obstacle M u=b, u>=0 in KKT form, with
M=D-gamma A, b=e_v-lambda d, lambda=eps_appr/2. Let U be a supplied
vertex set containing every coordinate with u_i>delta. Let v be the
exact obstacle restricted to U with zero outside and original full
diagonal degrees. Then

    0 <= v <= u, and ||u-v||_infinity <= delta.

Proof candidate: monotone restriction gives v<=u. If e=u-v has maximum
strictly greater than delta, it occurs inside U. At that coordinate u_i>0.
Full KKT and restricted KKT give (M e)_i<=0, whereas the maximum principle
gives (M e)_i>=bar_alpha*d_i*e_i>0. Contradiction. This avoids requiring
U to contain arbitrarily tiny positive coordinates of the exact support.

If a feasible restricted numerical candidate w has ||w-v||_infinity<=delta,
set x=(w-delta)_+. Then 0<=x<=v<=u and ||u-x||_infinity<=3*delta.
At x_i>0 the full optimum has r_i*=lambda*d_i, so

    (lambda-3*gamma*delta)*d_i <= r_i(x)
       <= (lambda+3*delta)*d_i.

At x_i=0 the original residual is nonnegative directly, and the same
upper bound follows from full KKT. Taking delta=eps_appr/8 yields original
ACL residuals in [0,eps_appr*d], and output bar_alpha*D*x. Its positive
support lies inside the true obstacle support, whose original volume is
less than 1/lambda. Audit threshold ties, omitted positive coordinates,
extra inactive vertices, signed coordinate error at both endpoints, the
empty envelope and original full-degree boundary grounding.

Thus a sufficient open target is a local procedure that finds a supplied
U containing {u_i>eps_appr/8}, with vol(U)=O(1/eps_appr) and fully charged
O_tilde(1/eps_appr) work. Together with a validated supplied near-linear
obstacle solver this would imply OP3. Finding this approximate envelope
is weaker than recognizing every arbitrarily small positive coordinate.
The construction of U is not provided by the argument.

## Falsifiable warning: degree-filtered breadth-first search

A candidate counterexample is a seed joined to a long path and to two
large binary branches. All original degrees are at most three. For small
lambda, significant path potentials can extend to distance of order
lambda^-1/2, while breadth-first exploration spends its O(1/lambda) row
budget after only O(log(1/lambda)) layers in the binary branches. The
true obstacle support still has volume below 1/lambda. A degree threshold
does not remove these low-degree decoys. Prove or refute with exact data;
do not infer a general lower bound from failure of this exploration rule.

Use symmetry to audit an enormous finite original graph without building
it. Quotient vertices are the seed, binary levels k=1..H with multiplicity
2^k, and a path of length P. Binary edge multiplicity from k-1 to k is
2^k; the path edges have multiplicity one. Original weighted degree sums
are 3 at the seed, 3*2^k on nonleaf binary levels, 2^H on the final binary
level, 2 on interior path vertices and 1 on its endpoint. Quotient matrix
has these degree sums on the diagonal and -gamma times edge multiplicity
off-diagonal; its source is e_seed-lambda*degree_sums. Uniqueness and
tree automorphisms justify equal potentials within each level.

Suggested exact case: lambda=2^-12, eps_appr=2^-11, alpha tiny positive,
H=24, P=512. Original ambient tree has more than 2^24 vertices, but the
quotient is a supplied weighted tree with only 537 vertices. Use exact
persistent VWF tree elimination with grounding bar_alpha*degree_sums
and cap 1/bar_alpha. This is a validator exploiting supplied symmetry,
not a local algorithm allowed free quotient access. Count the hypothetical
breadth-first original rows/degree work via complete level multiplicities,
and exhibit a missed path coordinate above eps_appr/8 even for budget
16/lambda. Keep all huge rationals in compact binary records if needed.
The already proved local tree solver shows why this cannot be a universal
OP3 obstruction.
