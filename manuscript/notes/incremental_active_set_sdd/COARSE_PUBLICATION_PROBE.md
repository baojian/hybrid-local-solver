# Completed probe: the coarse response as a geometric publication producer

Date: 7 September 2026. **Proved here, awaiting independent review.**
The proposal below is completed in `sections/op3_coarse_publications.tex`,
`thm:op3-coarse-publication-acl`, with the exact audit in
`COARSE_PUBLICATION_AUDIT.json`. The implemented state machine uses the
metadata hook, paid parent buffers and cached deliveries described here.
It removes q from ACL work and can stop before the obstacle optimum.
The prospective wording below preserves the block-12 design checklist;
its proof authority is the completed theorem, not this historical plan.
The next Open composition is `CERTIFIED_COARSE_SDD_PROBE.md`.

## Exact constants and accuracy namespace

Use the existing recipient constants, without silently changing the gate:

- lambda = eps_appr/2;
- h = eps_appr/(16*gamma);
- publication ratio eta = 5/4 (not q, which now denotes revealed cycle rank);
- candidate readiness threshold theta = 11*eps_appr/20.

Maintain exact active-face physical values implicitly. Each active vertex
has a lower publication ell_i, initially zero. Its producer row is

`u_i - (eta*ell_i + h)`.

If positive, obtain u_i by a named old-current component query and publish
ell_i := u_i. This first publishes above h and later increases by more than
eta, so it satisfies the original recipient's h/2 and 11/10 growth rules.
At producer quietness, ell_i <= u_i <= eta*ell_i+h holds for all active i.

On publication, scan the **cached** original row of i and add
gamma*(ell_new-ell_old) to the lower signal of every still-inactive neighbor.
Count every cached incidence read, including neighbors already active.
A boundary vertex enters a ready queue once its signal exceeds theta*d_j.
The signal is monotone until admission, so one queued flag per vertex is
enough. Exhaust the producer before each admission decision. If the ready
queue is empty afterward, stop. Otherwise admit a queued candidate using
the exact maintained inverse transaction with all its active parents.

The final point can differ from the exact lambda-obstacle optimum. Do not
reuse the previous audit's final equality or exact RPPR claims. Instead
verify positivity, monotonicity, containment below that optimum, active
residual lambda*d, and final exterior residual <=3*eps_appr*d/4. The output
is bar_alpha*D*u. This direction improves **OP3 ACL** only; it is not an
exact-RPPR algorithm or an OP2 conclusion without another argument.

## Producer representation

Place exactly one reporter row per active vertex on its permanent insertion
home edge. Use the existing one/two-port component hull with scalar key
`eta*ell_i+h-C`, C=1/bar_alpha. Arbitrary signs of this key are already
allowed by the uniform-shift implementation. At each producer search,
query every component at its current exact port values. A positive selected
row identifies an actual due active coordinate; retrieve its physical value
through the existing named query. Do not interpret a normalized hull score
as the physical coordinate difference.

After publication, change only this one home-edge payload and restore that
piece's source exposure. The matrix, physical port means and current coarse
inverse do not change. Thus there must be **no dense inverse update or
refactorization at a publication**. Admission changes the inverse exactly
as in the completed algorithm. All components are checked again as needed;
the cost of these failed searches is included below.

The reference audit may rebuild hierarchies at every producer search, but
must label that cost separately from the imported source's paid home-edge
updates. It must not use a scan of all physical values to find due rows.

## Local metadata obligations

Retain the original row after its one allowed scan for later deliveries.
Initialize an inactive candidate's signal to zero on first discovery.
This misses no past publication: any edge to an earlier active vertex would
already have discovered that candidate when that active row was scanned.
The newly admitted vertex starts with ell=0.

Use appendable incidence lists with explicitly charged geometric capacity
growth. The old cycle audit uses tuple concatenation and charges its copies
to q*V; that implementation choice cannot be carried into a q-free bound.
Copy or reverse an admitted parent list only once, with total cost bounded
by the scanned active incidences. No scan of the exceptional dictionary is
permitted at a checkpoint. Tracking q for validation is harmless if each
new repeated boundary incidence changes it in constant dictionary work.

The current inverse implementation has three calls to its parent metadata
admission routine. Prefer a small explicit overridable metadata hook if
reusing it; rerun the complete existing inverse audit after that refactor.
Avoid dynamic global monkey-patching or a hidden reference solve. Preserve
old roots, port means and home maps through every cycle promotion as before.

## Candidate work and space to prove after implementation

Let U be the actual final published-policy support, V=cvol(U), L=log(2+V),
r its active cycle rank, b the number of cycle-birth admissions, and p the
final retained-port count. Define

`K = 1 + log_+(32*gamma/(bar_alpha*eps_appr))`.

There are O(|U|*K) publications and O(V*K) cached incidence deliveries.
Every publication changes one payload in O(L^4) source work and uses at
most O(p*L^2) total component-query work. There are at most |U| admissions
and one extra quiet producer search per face. Original row scans cost V;
all ready-queue/dictionary work is covered by O(V*K*L).

The proposed fully charged word bound is

`O(1 + V*((1+b)*L^4 + (1+p)^2 + K*(L^4 + (1+p)*L^2)))`.

Selected covariance promotion work is still absorbed as in the completed
inverse theorem. Since b<=r and p<=4r for r>=1 (p=1 if r=0), this would
give `O_tilde((1+r^2)/eps_appr)`, **without a revealed-rank factor**.
The q dependence is removed from this representation's work, not bounded
by a false assumption that inactive cycles are few.

If all historical application versions are retained, a safe candidate
space bound is

`O(1 + V*(1+b+K)*L^3 + (1+p)^2)`.

Only current dense inverse matrices are retained. Historical piece root
values require O(V*K*p) words if saved after every publication; that is
NOT automatically within the smaller bound above. Even saving them only
at admission checkpoints requires O(V*p), which is also not automatically
covered by the refined b-based bound. For that bound, release old port-value
snapshots and retain only changed immutable cluster/hull records. Otherwise
add V*p or V*K*p explicitly, according to the retained snapshot frequency.
A fresh whole list of every unchanged component root and old port value
must not be silently allocated at each producer search. Exact audits may
retain extra snapshots as separately charged reference state.

## Falsifiable checks

1. All connected atlas graphs through seven vertices, every seed, four
   alpha/epsilon pairs, FIFO/LIFO ready queues and first/last tree parents.
2. Independent original-matrix J*K=I at each admission; full physical-face
   comparison and every producer decision checked independently. Verify
   that selected positive rows really are due and every producer-quiet
   state satisfies the entire coordinatewise band.
3. Independently recompute every boundary lower signal from current ell,
   every ready-queue condition, final original ACL residual and support
   volume. Include traces stopping strictly before the obstacle optimum.
4. Count all repeated cached incidence reads, first discoveries, parent
   buffer copies, queue inserts/deletions, payload changes, failed producer
   queries, root/value histories and coarse inverse writes. Assert that
   the inverse is untouched by publication-only transitions.
5. Include the existing implicit private-star families with no inactive
   hub scans. Add a family with tree-shaped actual support but arbitrarily
   many shared inactive candidates, so r=0 while q grows, and verify no
   per-face exceptional scan. Derive parameters rather than filtering for
   favorable finite behavior.
6. If any producer or metadata cost cannot be paid, leave the result
   Conditional and preserve the exact failed trace; do not claim OP3 from
   the recipient theorem alone.

## Explicit growing-q family for the next audit

Take an active star with seed center 0 and k>=2 core leaves. For each pair
of distinct core leaves introduce an inactive shared hub adjacent to that
pair, and give it D-2 private degree-one neighbors. Every shared hub has
full degree D; each core leaf has full degree k and the center has degree k.
There are H=binom(k,2) hubs, and the finite ambient graph has
(k+1)+H*(D-1) vertices. Define

`lambda = gamma/(4*k*(k+gamma))`, `eps_appr=2*lambda`,
`D = ceil(4/(bar_alpha*lambda))`.

The exact full-core face has

`u_0 = (1-lambda*k*(1+gamma))/(k-gamma^2)`,
`u_leaf = 3*gamma/(4*k*(k-gamma^2)) > 0`.

No hub can violate the original lambda gate because its residual is at
most 2*gamma/bar_alpha < lambda*D. The private vertices see only zero hubs.
Thus this full star is the unique lambda-obstacle positive support.

Already on the singleton seed face, its first exact publication queues
every core leaf: gamma*(1-lambda*k)/k > (11/10)*lambda*k. After multiplying
by 40*k*(k+gamma)/gamma, this inequality is 40*k+30*gamma>11*k.
The singleton value exceeds h, so that publication really occurs. All
core leaves remain queued, and no hub can enter the readiness queue.
Therefore the proposed publication policy also reaches exactly this star,
under either FIFO or LIFO and regardless of the chosen leaf order.

Its final active cycle rank is r=0, revealed cycle rank q=H, scanned
volume k*(k+1), and charged volume V=(k+1)^2. A direct exceptional-gate
checker visits exactly binom(t,2) shared hubs after t core leaves have been
admitted, hence sum_{t=0}^k binom(t,2)=binom(k+1,3) exceptional gates.
This is an algorithm-specific superlinear repeated-search cost on a
source-valid family, not a lower bound for all local algorithms. The new
producer must demonstrate cached incidence delivery and logarithmic
publication counts while making zero such exceptional scans.

These algebraic parameters are a derivation to verify in the next exact
audit. Use an implicit oracle that refuses every shared-hub row scan;
do not materialize the private vertices.
