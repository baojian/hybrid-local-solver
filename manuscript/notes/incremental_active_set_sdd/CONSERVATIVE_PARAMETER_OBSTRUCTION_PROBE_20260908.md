# Is the fourth-power comparison scale necessary?

This is the next proof/audit target, not yet a proved obstruction. It
concerns the rule that extracts an envelope from arbitrary ACL output at
one comparison parameter. It is not a computational lower bound for OP3.

## Exact conservative family

For an integer N>=4, take the original path on labels 0,...,8N, seed N.
Set lambda=2N/(8N^2+1), e=2lambda, delta=e/8=lambda/4. Its original
volume 16N exceeds 4/e. The conservative obstacle should have support
S0={0,...,2N-1} and explicit values

u0_i = N-lambda*(4N^2-i^2)                     for 0<=i<=N,
u0_i = (2N-i)*(1-lambda*(2N+i))               for N<=i<=2N,
u0_i = 0                                    for i>=2N.

In particular u0_0=lambda/2=2delta is significant. Check all original
KKT rows, including degree one at 0, seed degree two, and the first zero
coordinate at 2N. At the last positive coordinate,
u0_(2N-1)=lambda*(1+1/(2N))<=2lambda, so that zero boundary is legal.

## A positive-target ACL output that omits that significant endpoint

Let T={1,...,2N-1}, with Dirichlet zero values at 0 and 2N, and use
t=bar_a=1/N^4 (lazy a=t/(2-t)). All original degrees inside T equal two.
Write L_T for the original Dirichlet Laplacian and A_T for its adjacency.
The conservative UNCONSTRAINED solution on T is positive and symmetric:

v_i = min(i,2N-i)/2 - lambda*i*(2N-i).

Its torsion vector is w_i=i*(2N-i), and max(v)<=N/3. Define
h=L_T^-1 A_T v and k=L_T^-1 A_T h. Both are nonnegative. The candidate
z=v-t*h+t^2*k on T, with zero extension, obeys exactly

(L_T+t*A_T) z = b_T + t^3*A_T*k.

Use an actually charged or explicitly audit-only linear-time Dirichlet
path solve for h,k. These are simple prefix-sum solves with rational
polynomial-sized coefficients; do not run dense repeated obstacle solves
on thousands of vertices.

The following bounds appear sufficient for N>=4:
- v_i/w_i >= v_1/w_1 >= 1/(9N^2).
- h_i <= (N/3)*w_i, hence v-t*h>0.
- sum_i v_i = N^2*(8N^2+7)/(6*(8N^2+1)) >= N^2/6.
- By symmetry of the Dirichlet Green row, h_1=sum_i v_i-v_1.
  Since v_1<=3/(8N), h_1>=N^2/8 for N>=3.
- v_1-lambda=1/(2*(8N^2+1))<=1/(16N^2).
- max(h)<=N^3/3 and k_1<=2N^4/3.

Consequently z_1-lambda <= -1/(16N^2)+2/(3N^4)<0 for N>=4.
Symmetry gives the same bound at 2N-1. At the omitted original endpoint
0, target residual (1-t)*z_1 is therefore below lambda (degree one).
At 2N it is below lambda<=2lambda; every farther residual is zero.

Inside T, original target residual is 2lambda-t^3*(A_T*k)_i. Since
max(k)<=(N^3/3)*N^2=N^5/3, its subtractive term is at most 2/(3N^7),
which is smaller than 2lambda for N>=4. Thus z itself should be a genuine
nonnegative original ACL output at accuracy lambda, of volume 4N-2,
yet its support omits the conservative significant endpoint 0.

## Interpretation to prove carefully

t/e^4=(8N^2+1)^4/(256N^8) tends to 16. The existing safe comparison
t=e^4/128 is smaller by a fixed factor. The family would show that the
FOURTH POWER is necessary, up to constants, for uniform containment based
only on arbitrary accuracy-lambda ACL output at the same obstacle load.
Because the exact target obstacle is below the supersolution z, it also
omits endpoint 0. Same-load monotonicity then preserves that omission for
larger t, so a universally larger asymptotic scale t=omega(e^4) cannot
replace the safe comparison in this particular reverse reduction.

Do not infer a lower bound on algorithm work, or rule out a producer that
deliberately includes extra envelope coordinates. Verify every displayed
identity and inequality exactly, including the original outside rows and
the zero endpoint's smaller degree, before promoting the claim.
