# Independent audit of the exact box/cap corrector

Reviewed `capped_box_corrector.py` and the AVL routines it imports from the
fresh current-task `lazy_capped_solver.py`. The implementation and its
owner's tests were not edited. This audit checks the code independently of
the owner's dense-projection comparison tests.

## Verdict

The exact projection root selection, sparse baseline/source initialization,
general-mu response update, and lazy key refresh pass static mathematical
audit and the independent exact tests below. No correctness defect was found.
The implementation is an exact-arithmetic prototype; its structural
counters do not assert a bound on Python bit operations or all map accesses.

## 1. Exact clipped waterfilling

`tail_moments(q)` uses a strict tail. The formula in `box_mass` is exactly

    sum_i d_i min(U,max(0,sigma*K_i-shift-eta)).

The returned slope is the magnitude of the RIGHT derivative in eta.
Coordinates exactly at zero are excluded. Coordinates exactly at the upper
box boundary are included, because increasing eta releases them into the
linear region. This makes the affine solve valid when its lower endpoint
is itself a breakpoint.

If the zero-multiplier mass exceeds cap, `high` is the largest raw density
and has mass zero. For cap>0, low and high therefore bracket the root.
The first binary search removes all interior breakpoints of the unshifted
sequence from the bracket. The second search only shrinks the bracket,
so it cannot reintroduce any; it also removes the upper-shifted sequence's
interior breakpoints. At exit the interval is affine. Low has mass strictly
above cap, so its right slope must be positive, and

    eta=low+(mass(low)-cap)/slope

is the exact root. Encountering a breakpoint with mass exactly cap returns
immediately, including a whole plateau of possible multipliers. Cap zero
is handled by the largest raw density. An empty tree exits through the
zero-mass branch before any rank query.

The two searches each have logarithmically many iterations, with logarithmic
rank and mass queries. Thus this implementation's root search is O(log²N)
tree work, comfortably inside the proof's conservative O(log³N) bound.
Only the strictly positive projected output is enumerated.

## 2. AVL order statistics

The subclass's refreshed `count` includes both child counts. A newly
allocated leaf uses the fallback count one before its first refresh.
Rotations dispatch to the subclass refresh, and deletion either returns a
previously valid child or refreshes its remaining ancestors. Consequently
rank selection remains valid after rotations, key replacement, and deletion.
Duplicate numeric keys are ordered by vertex ID; strict numerical tail
queries correctly exclude every tie at the threshold.

## 3. Sparse source construction

All stored values are degree densities. `_response(f)` computes

    D^(-1/2)(Q-mu I)D^(1/2) f
      = (alpha-mu+c)f-c D^(-1)A f.

Its scatter coefficient into neighbor i is `-c*f_j/d_i`, as required.
Adding `mu*baseline` in the constructor reconstructs Q's density response,
so its source is exactly

    s_i/w_i = alpha*1_(i=seed)/d_i-(Qbar)_i/w_i.

Every possibly nonzero coordinate occurs in the response support, baseline
support, or seed. A filtered zero response does not hide a needed diagonal
source coordinate because the baseline support is included separately.
Every outside coordinate has zero baseline and no baseline neighbor, hence
zero source. The constructor's local checks therefore establish its
claimed global source interval for a valid undirected input graph.

The weighted source identity is checked using only this sparse source list.
Baseline adjacency scans are charged; exposed source neighbors receive
degree queries without recursive adjacency scans. Being below the unknown
RPPR optimum remains the documented analytical precondition supplied by the
outer repair scheme; the constructor does not incorrectly claim to verify it.

## 4. Lazy state and stopping certificate

Before changing sigma, old sparse exceptions are removed. Updating X on
new emissions and R by their scattered response preserves

    xi_density=sigma*X,
    (Q-mu I)xi_density=sigma*R.

New source, kinetic, and kinetic-response exceptions are then installed.
Only sparse exception supports are iterated; a source key is explicitly
refreshed each step, as needed for its division by the changing sigma.
First exposure initializes zero prior state, which is justified because a
previously nonzero primal neighbor would already have exposed the vertex.

The code's initial bound differs from the proof's simpler bound one but is
valid: strong convexity gives `E0<=2 gap(0)`, and
`gap(0)<=||(s-lambda*w)_+||²/(2mu)<=C lambda*m_s/(2mu)`.
Its bound is therefore `C lambda*m_s/mu`, and the returned
`sigma*initial_energy_bound` is a valid objective certificate. Since
mu>alpha/4 and m_s<=alpha, this is at most `4C alpha*rho`, so it does not
change the asymptotic iteration count. A caller using `max_iterations`
must still inspect the resulting bound; that optional early stop is not a
separate accuracy certificate.

## 5. Independent exact checks

`audit_capped_box_corrector.py` produced
`capped_box_independent_verification.json` with all checks passing:

- 6,250 exact projection cases, including 3,694 binding caps, with degree
  weights 1, 2, 101, and 10,007. Verification used the KKT formula, exact
  cap/complementarity, and independently summed mass/right derivatives.
- Seven deterministic sequences of AVL insertions, deletions, and value
  replacements, followed by 28 projection checks and complete rank checks.
- Eighteen exact-source cases on an asymmetric cyclic seven-vertex graph,
  including repaired baselines and three nonsquare alpha choices.
- 198 exact subsequent sparse-key versus dense-raw identities, checking
  every vertex and explicitly requiring negative raw density at vertices
  not yet exposed.

No random values, random graph construction, or randomized tests were used.
Arbitrary raw projection tests validate that primitive only; they are not
presented as reachable-trajectory evidence for the work theorem.

## 6. Implementation/model distinction

The AVL breakpoint reporter is deterministic with worst-case logarithmic
operations. The Python prototype also uses builtin dict/set containers for
vertex state. For its tested integer labels the numerical trajectory uses
no RNG, but these containers are not the deterministic balanced dictionary
implementation used in the theorem's worst-case word bound. Nor do the
reported structural metrics count every Python operation or rational bit.
The proof permits replacing these maps by balanced dictionaries at the
already allowed logarithmic cost. Production code should retain this
explicit distinction until that replacement or a separately justified
runtime model is supplied.
