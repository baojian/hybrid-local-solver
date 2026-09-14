# A deterministic bounded-region pilot with global acceptance

Private refinement, September 5, 2026. The main continuation theorem remains
the fallback and is not modified by this optional preliminary solve.

Let A={original degree <=1/rho}. Run the existing seed-component discovery,
stopping before total original scanned degree-volume would exceed 1/rho.
If it stops early, let C be precisely the scanned vertices. C is connected,
contains the seed, and vol(C)<=1/rho. All of its original adjacency rows and
all neighboring degree replies have been charged. Form M_C=Q_CC with the
original degrees. Edges to A\C are Dirichlet boundary edges for this pilot;
they are not silently treated as absent from the full problem.

## One restricted accelerated solve

The restricted optimum u_C is nonnegative, has mass at most one, and obeys
u_C<=Q_CC^{-1}b_C<=w_C/d_seed. Hence the existing component algorithm's box
and unit mass cap contain it. The boundary-forest construction, now counting
every original edge leaving C, certifies beta_C>=alpha for Q_CC.

Use its deterministic accelerated iteration and downward grid rounding.
For the same final clipping delta as continuation, choose local objective
tolerance tau_C=alpha^2 delta^2/16 and grid

    h <= min(theta tau_C/16, delta/2, alpha rho/4,
             1/d_seed, alpha delta rho/16).

Run only its prescribed horizon O(beta_C^{-1/2} log(1/tau_C)). There is
exactly one pilot attempt. It uses O_tilde(vol(C)/sqrt(beta_C)) work,
which is at most O_tilde(1/(rho sqrt(alpha))).

## Acceptance is global on A

At geometric checkpoints, and at the final pilot horizon if needed, regard
the pilot candidate as zero on A\C and compute its **full A projected-gradient
point**. Scan only positive candidate rows in C. Compute the common-denominator
upper bound U2 on ||x-p||^2 described in checkpoint-certificates.md, including
new PG coordinates in A\C. The stopping test is

    (1-alpha)^2 U2 <= alpha^2 delta^2/4.

It deliberately uses alpha, not the pilot's larger beta_C. A local spectral
bound alone is not a global accuracy certificate.

If the test passes, the global subgradient certificate proves distance
||p-x_rho||<=delta/2, so the established global clipping/grid repair returns
0<=output<=x_rho with objective gap <=2 delta^2/rho<=epsilon. Any retained
PG coordinate outside C is returned without scanning its row. Its safety and
output-volume bound follow from the certificate, not from a free support test.

If no test passes by the pilot horizon, discard the pilot iterate and invoke
the proved continuation from zero, retaining only the charged local oracle
cache. In particular, the pilot does not supply an unverified diffuse source
or an unverified continuation baseline.

## Why the pilot succeeds when C already contains the optimum

This is not required for worst-case correctness, but explains its utility.
If supp(x_rho)<=C, the restricted objective gap is the full objective gap.
At the fixed pilot horizon, it is less than tau_C. PG descent gives
||x-p||^2<=2 tau_C=alpha^2 delta^2/8.

The number of affected records is at most 1+2 vol(C)<=3/rho (rho<1).
The component state is on denominator H=1/h. Even the coarser valid common
denominator 2 denom(alpha) H denom(rho) makes the norm rounding excess at
most 3 h^2/(4 rho)<=3 alpha^2 delta^2/1024. The implementation reuses the
integer PG helper with H^2, yielding an even finer bound. Consequently the
global test passes by the prescribed horizon, without a complementarity
margin assumption.

## Charged total work

The prepass, induced-region assembly, all pilot products/projections,
geometric global certificate scans, scalar state updates, final certificate,
and either output or discarded pilot state are charged. Global certificate
scans cost O_tilde(vol(C) log K), with no row scan of newly positive PG points.
Adding one fallback continuation preserves O_tilde(1/(rho sqrt(alpha))).

## Status

Implemented and enabled by default in `solve_fast`; it can be disabled with
`bounded_pilot=False`. Exact checks in `results/bounded-pilot-audit.json`
covered 144 full-solver cases, including 74 accepted pilots and four rejected
pilots that correctly fell back. Both geometric checks and fixed-horizon-only
pilot modes were tested. All output orders, objective gaps, original graph
replies, and scan budgets passed. The misleading-branch graph deliberately
places part of the optimum outside the pilot region.

On a virtual retained path of one billion vertices, each attached to an
excluded hub with 2^100 leaves, all three alpha values 10^-4, 10^-8, 10^-12
passed exact symbolic full-graph KKT audits. The pilot used 64, 128, 128 steps,
254 original incidences, and about 0.19, 0.38, 0.39 seconds. The earlier
checkpoint-only continuation needed 191 seconds at alpha=10^-8. These are
structured-instance Python measurements, not general runtime predictions.
