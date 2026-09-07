# Certified sparse coarse solves for linear-rank ACL work

Date: 7 September 2026. **Proved here**, completed construction and exact
audit, draft awaiting independent review. General OP3 remains **Open**.
Proof authority is `sections/op3_certified_coarse_sdd.tex`, especially
`thm:op3-certified-linear-rank`. The source solver and online top-tree
balancing are explicit **Source** imports; the exact audit substitutes a
dense coarse candidate provider and separately charged hierarchy rebuilds.

The correct random-support statement is
`E[W]=O_tilde((1+E[r])/eps_appr)`. A fixed sufficient rank bound `R` on the
containing exact obstacle support gives `O_tilde((1+R)/eps_appr)`.
`CERTIFIED_COARSE_PUBLICATION_AUDIT.json` contains 67,856 complete original
ACL checks, 223,514 independent faces, and 3,228,290 original uniform-error
and due-row checks. Rejected signed perturbations and accepted nonzero
errors exercise the exact certificate and downward repair. This is ACL-only;
it does not establish exact RPPR, OP2, or fast source-solver performance.

The following development specification is retained as **historical proof
obligations now resolved by the cited section**. Its prospective wording
is not the current completion status. See the theorem for the final
random-support expectation, source-retry and workspace statements.

## Why approximate ports may suffice

The permanent-port decomposition has p=O(1+r) ports, O(p) tree pieces and r
extra edges. Each piece has at most two ports. Its physical Schur matrix K
therefore has O(p+r) nonzeros, even though K inverse is dense. Geometric
publication needs certified coordinate bands, not an exact inverse.

Try assembling K and its physical load f once per admitted face, then using
a supplied sparse SDD solver with a checked residual. Publication changes
only reporter payloads, so the same certified port vector can be reused
until the next admission. Paying O_tilde(p+r) per face would replace the
current quadratic rank factor by a linear one. This still does not resolve
general OP3, because r can grow with the explored support.

## Exact error certificate to prove and audit

Let I=U\P. The conditional physical response is

`u_I = zeta + A*u_P`, `A=-M_II^{-1}*M_IP`.

Inverse positivity gives A>=0. Since the row sums of M_UU are at least
bar_alpha*d, the maximum principle gives A*1<=1. A row in one piece has
at most two nonzero coefficients. Thus a port error bounded by delta in
every coordinate produces an interior error bounded by delta, with no
tree-depth factor.

Moreover,

`K*1 = M_PP*1 + M_PI*A*1 >= M_PP*1 + M_PI*1 >= bar_alpha*d_P`.

K is therefore SDDM, not merely spectrally bounded below by bar_alpha*D_P.
Check a proposed physical port vector t using the sparse residual:

`|f-K*t| <= delta*bar_alpha*d_P`.

The positive inverse and K*1>=bar_alpha*d_P imply
`|t-u_P|<=delta*1`. The certificate costs O(p+r) exact-word operations.
Rejected candidates cannot affect publication or admission decisions.

## Source solver and accuracy budget

**Source to import after verification:** Koutis--Miller--Peng (2011),
arXiv:1102.4842v4, Theorem 4.6, PDF p11; Lemma 4.3 and the SDD reduction on
p9, and LowStretchTree/BuildChain on p10. The supplied weighted SDD theorem
gives relative energy error eta in expected O_tilde(m log n log(1/eta))
work. The paper is already in the local library and literature index.
Do not invent a high-probability parameter in Theorem 4.6. Verify the
constant-success construction and use independent retries with the exact
certificate; account for failed attempts. Fresh randomness is needed after
an adaptively chosen face. This is an exact-real word model source import,
not a rational-bit or numerical-stability claim.

The physical seed v is always retained. Interior physical loads are
negative, so f has no positive entry except possibly f_v<=1. For a positive
face, `||u_P||_K^2=f^T*u_P<=u_v<=1/bar_alpha`. Also K_ii<=d_i. Relative
energy error eta therefore implies

`|(K*(t-u_P))_i| <= sqrt(d_i)*eta/sqrt(bar_alpha)`.

Since d_i>=1, choosing
`eta=min(1/2, delta*bar_alpha^2/2)` suffices for the checked residual.
Only logarithmic dependence on alpha and eps_appr enters the source work.
Check source runtime/success assumptions explicitly before claiming this.

## Finite-width publication rule

Keep lambda=eps_appr/2, h=eps_appr/(16*gamma), publication ratio 5/4 and
ready threshold theta=11*eps_appr/20. Choose

`delta=min(h/16, eps_appr/64)`.

For current certified approximate physical value t_i, use the reporter row

`t_i - ((5/4)*ell_i+h-delta)`.

At a positive selected row obtain the named value t_i and publish
`ell_new=t_i-delta`. Then ell_new<=u_i, while

`ell_new>(5/4)*ell_old+h-2*delta >= (5/4)*ell_old+7*h/8`.

This satisfies the original recipient's h/2 first-publication and 11/10
growth rules. After publication the current upper endpoint is at most
ell_new+2*delta<=(5/4)*ell_new+h. At a quiet reporter search, the true
values satisfy u_i<=t_i+delta<=(5/4)*ell_i+h. Port values may be slightly
negative or exceed C; the projective reporter must support these arbitrary
query values. The structural positive denominators must not rely on an
unproved approximate-port sign.

Use the same cached original-incidence delivery and monotone ready queue.
No exact full-face solve may select a publication. Exact coarse solves are
permitted only as separately labelled reference providers for testing the
source interface. The fast source solver is not implemented by such a
reference oracle.

## Final downward repair, without another full SDD solve

At termination recover the current approximate physical vector t once from
the tree pieces and return `bar_alpha*D*max(0,t-delta)` on U. Its difference
e from the exact positive face u obeys 0<=e<=2*delta. For an active row,

`r_repaired = lambda*d + M_UU*e`,
`(lambda-2*gamma*delta)*d <= r_repaired <= (lambda+2*delta)*d`.

These bounds lie inside [0,eps_appr*d]. Exterior residuals only decrease
under downward repair and are already <=3*eps_appr*d/4 at quietness.
Thus clipping seems sufficient; audit all original residuals independently.

For literal support-local accounting, use the initial zero test
`eps_appr*d_v>=1`, which directly certifies ACL without reading the seed
row. Otherwise the first seed value exceeds eps_appr/2. Every later
admitted vertex has old gate excess >(theta-lambda)*d=eps_appr*d/20 and
admission pivot <=d, so its new exact value exceeds eps_appr/20. Monotone
face growth and 2*delta<=eps_appr/32 then ensure the repaired output stays
strictly positive on every admitted vertex. Check these inequalities and
the changed zero test explicitly; do not silently inherit the old
lambda*d_v>=1 obstacle-only zero condition.

## Charged target and falsifiable implementation

With V=cvol(U), L=log(2+V), b cycle-birth admissions, p final ports and
K_pub=1+log_+(32*gamma/(bar_alpha*eps_appr)), the intended work is

`O_tilde(V*(1+b+p+r+K_pub*(1+p)))`.

As b<=r and p=O(1+r), this would give expected
`O_tilde((1+r)/eps_appr)` ACL work. Account for sparse assembly and duplicate
port corrections, solver preprocessing/retries/certification, every failed
producer query, named-coordinate query, cached delivery, source callback,
cycle rebuild, parent buffer and final recovery. Do not retain whole old
port snapshots at every publication. Audit source space separately before
stating a sharper space theorem. This is ACL only, not exact RPPR or OP2.

Implement a separate approximate-port state machine using paid metadata
and tree-piece assembly, without maintaining J. Test deliberately bad
coarse candidates, certified nonzero perturbations of both signs, changing
port sets, all existing cyclic structured families, high-q tree supports,
the initial zero boundary and the final repair. Independently check every
certificate against the full original face; compare due rows, quiet bands,
lower signals, growth counts, positive admissions and final original ACL.
Record source hashes and keep reference-only dense work separate. If a
certificate or source-cost premise fails, preserve the trace and leave the
linear-rank statement Conditional.
