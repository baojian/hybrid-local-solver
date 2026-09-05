# Ordinary rational output without a square-root primitive

The density triple (i,f_i,d_i) already specifies x_i=sqrt(d_i)f_i exactly
using a constant number of words. To remove any dependence on that output
convention, `solve_explicit` produces ordinary rational x-coordinates using
only arithmetic and comparisons.

Run the proved density solver with tolerance epsilon/4, obtaining gap bound
B<=epsilon/4 and 0<=x_hat<=x_star. Choose dyadic eta>0 with eta^2<=epsilon/2.
For each emitted vertex, bisect the rational interval [1,d_i] using squared
midpoint comparisons, until its width is at most eta. Its lower endpoint
l_i satisfies 0<=sqrt(d_i)-l_i<=eta. Return x'_i=l_i f_i.

Then 0<=x'<=x_hat<=x_star. Since d_i>=1 and sum_i d_i f_i<=1,

    ||x_hat-x'||_2^2 <= eta^2 sum_i f_i^2 <= eta^2.

Both output supports lie in supp(x_star), so their KKT linear terms vanish.
Using Q<=I and ||a+b||_Q^2<=2||a||_Q^2+2||b||_Q^2 gives

    F(x')-F(x_star) <= 2B + eta^2 <= epsilon.

This bound is rational and needs no square root to evaluate. Empty output
needs no conversion and keeps the density solver's certificate directly.

Every emitted degree is at most 1/rho. Bisection therefore costs
O(log(1/rho)+log(1+1/epsilon)) arithmetic/comparison steps per output record,
with no additional graph query. All endpoints are dyadic rationals with
polylogarithmic bit length. The OP2 work bound and safe order are preserved.

Independent checks: 384 deterministic small-graph parameter cases, 780
converted records and 11,792 bisection steps passed exact rational interval
enclosures of the true objective gap. The test computes full-graph KKT optima
and uses integer square-root enclosures independently of the solver's
bisection. The runtime solver itself uses no square-root primitive and
performs no extra graph queries during conversion. Portable tests also
cover a rejected preliminary pilot, zero output and the diagonal case.
