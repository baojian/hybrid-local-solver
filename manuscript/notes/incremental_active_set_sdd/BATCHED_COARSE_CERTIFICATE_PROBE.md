# Sparse residual epochs and a forced-refresh family

Date: 7 September 2026. **Proved here**, draft awaiting independent review;
the residual-epoch state and exact audit are complete. **Open:** an amortized
coarse response mechanism beyond the linear-rank ACL theorem. Proof authority
is `sections/op3_coarse_residual_epochs.tex`.

`COARSE_RESIDUAL_EPOCH_AUDIT.json` passes 4,866 complete original ACL checks,
including 26 accepted reuse events on targeted paths and six clique-leaf
forced-refresh families. `COARSE_GEOMETRIC_SUPERSOLUTION_AUDIT.json` checks
16,446 independent Schur systems and records an exact triangle on which a
true geometric upper envelope fails the sufficient supersolution test.
These refute particular shortcuts, not OP3. The actual scalar clique solver
in `LOCAL_CLIQUE_PENDANT_PROBE.md` solves the forced-refresh family efficiently.

The audit specification below is retained as development history; its
required checks have now been run. Counts, source hashes and scope are in
the two named audit files and `OVERNIGHT_BLOCK14_AUDIT.json`.

## A cheap ordinary-admission certificate update

Retain a certified coarse port vector t during an epoch with fixed ports P.
Let g=f-K*t be its current physical coarse residual, with
`|g_i|<=B_i=delta*bar_alpha*d_i`.
For an ordinary new leaf j with unique active parent i, use the old exact
conditional response `u_i=zeta+a^T*u_P` and conditional variance g_ii.
The vector a has at most two nonzero coordinates, all nonnegative. Let

`tau=d_j-gamma^2*g_ii`, `c=-lambda*d_j+gamma*zeta`.

The completed sparse-downdate identities imply

`K_new=K-(gamma^2/tau)*a*a^T`,
`f_new=f+(gamma*c/tau)*a`,
`g_new=g+(gamma/tau)*(gamma*t_i-lambda*d_j)*a`,

where `t_i=zeta+a^T*t` is the old approximate physical parent value.
This last formula updates at most two residual coordinates. It requires a
paid selected conditional query, not a full inverse. Since a publication
admission has true gate excess >eps_appr*d_j/20 and |t_i-u_i|<=delta,
the multiplier is positive: delta<=eps_appr/64 and d_j>=1 suffice.
Thus g increases coordinatewise during an ordinary-admission epoch while
the port vector is fixed. Only the upper certificate bounds at the changed
coordinates need checking. The lower bounds persist.

An implementation may update K/f sparsely, keep this residual, and reuse t
until one upper budget is crossed. A cycle birth can fall back to the full
certified sparse assembly/solve. This saves some repeated work, but neither
the number of refreshes nor the remaining component scans/cycle rebuilds
is bounded by the identity alone.

## Why a fixed absolute residual budget can refresh at every leaf

Suppose j is an original degree-one leaf whose active parent i is retained.
Then a is the coordinate unit vector at i, g_ii=0 and tau=1. The residual
increase at i is

`Delta g_i=gamma*(gamma*t_i-lambda)`.

If gamma>=1/2, delta=eps_appr/(256*gamma), and bar_alpha*d_i<=1, then
the publication gate and the error bound give

`Delta g_i>gamma*eps_appr*(1/20-1/256)
          =59*gamma*eps_appr/1280`,
`2*B_i<=eps_appr/(128*gamma)`.

Their ratio is greater than `59*gamma^2/10>=59/40>1`.
Hence Delta g_i>2*B_i. Regardless of the signed residual left by the previous
certified solve, g_i>=-B_i implies g_new_i>B_i. Every such admitted leaf
forces a refresh of this fixed-absolute-budget representation.
This is an algorithm-specific certificate obstruction, not an OP3 lower bound.

## A canonical clique with pendant leaves

Take a clique on k>=3 core vertices. Attach t>=k original degree-one leaves
to each core vertex. All core degrees are d=k-1+t. Use core seed 0, list
core neighbors before leaves in the seed adjacency order, and use FIFO
readiness with the first-discovered spanning parent. Choose

`bar_alpha=1/(4*d)`, `alpha=1/(8*d-1)`,
`gamma=1-1/(4*d)`,
`eps_appr=1/(8*d^2)`, `lambda=1/(16*d^2)`.

The initial seed value is 1/d-lambda. Its first certified lower publication
is at least this value minus 2*delta, hence exceeds 1/(2*d). Because
gamma>=19/20, it queues all core neighbors at threshold
theta*d=11/(160*d), and also the seed leaves. The core neighbors enter the
FIFO queue first. Every remaining core vertex is therefore admitted before
any leaf; later publications append additional leaves only at the back.

On the core-only face let L=d-gamma*(k-1). Every nonseed core value is

`u_core=[gamma/(d+gamma)-lambda*d]/L`.

Since d>=5, gamma>=19/20, L<=d and d/(d+1)>=5/6,
this is at least `35/(48*d^2)>1/(2*d^2)=4*eps_appr`.
At producer quietness its lower publication is therefore greater than
3*eps_appr. Every pendant leaf is consequently queued. Monotonicity keeps
all of them ready, so the algorithm reaches the entire finite graph.

The first-discovered insertion parent of each core vertex is the seed.
After the first triangle closes, all three core vertices are marked; each
further core admission is an endpoint of an extra edge. Thus every core
vertex is a permanent retained port when the leaves are admitted. Here
bar_alpha*d=1/4 and gamma>=19/20. The preceding obstruction forces a
refresh at all k*t pendant admissions, after the full k-port core exists.
Merely writing a complete refreshed port vector costs Omega(k^2*t).
With V=cvol(G)=Theta(k*t) for t>=k, this is Omega(k*V).

This is a repetition cost relative to explored volume, not yet an OP3-scale
counterexample: 1/eps_appr=8*d^2 can be much larger than V. For t=k,
V=Theta(k^2) while the mandatory refresh writes are Omega(k^3), so they
also exceed the proposed O_tilde(1/eps_appr) scale as k grows. Teleportation
is alpha=Theta(1/k), and logarithmic factors cannot hide that extra k.
This still refutes only this explicit global-vector refresh policy; other
representations, delivery policies or local push on other parameter regimes
are not lower-bounded.

## Required exact audit

Implement a separate residual-epoch state, keeping the completed certified
per-face solver intact. At ordinary admissions, compute the selected
conditional row and variance from old current tree records; update only
the affected sparse K/f/g entries; verify the upper bounds. Reuse the old
port vector only when the certificate remains valid. Otherwise call the
same explicitly labelled reference provider and reset the exact residual.
At cycle births use the existing full sparse assembly and certified solve.

Check every sparse update and reused certificate against independent
original-matrix Schur elimination, exact faces and original ACL residuals.
Track certificate generation separately from face count. Include all small
atlas graphs, both queue policies, gamma near zero and one, accepted reuse
events, rejected epochs, and the canonical clique family with t=k.
Verify its exact admission prefix, full support, retained core ports,
one forced refresh per leaf, and charged vector writes. Do not replace
matrix/response checks by an assumed symbolic recurrence in the validator.

The open alternatives are an adaptive original-coordinate error certificate,
an implicit coarse solve that does not rewrite all ports, a multilevel
response scheme, and incremental partition/reporting that removes the
separate cycle-rebuild and all-component-query costs. A successful source
import must cover every one of these charges, not just sparse matrix updates.
