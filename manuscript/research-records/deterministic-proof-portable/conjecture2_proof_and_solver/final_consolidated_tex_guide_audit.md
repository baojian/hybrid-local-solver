# Final consolidated TeX and reading-guide audit

Status: no theorem/model gap found in the current main proof and both
included appendix files. The new A.14 mass-grid transcription passes.
The one nonblocking abstract qualification found during review has been
corrected by the author and checked, as below.

Scope: reread deterministic_conjecture2.tex,
practical_refinements_appendix.tex, practical_schedules_appendix.tex
(including A.13 and the newly appended A.14), and proof_reading_guide.md.
The only manuscript source used is the authorized
problem_definitions/main.tex. Prior audits from this same fresh task were
available. No proof files were edited, and no numerical tests or external
research were undertaken in this review.

## Core dependency check

The claimed optimization problem matches canonical OP2: a finite connected
simple unweighted undirected graph, a point seed, positive alpha/rho and
additive objective accuracy. The theorem preserves the exact-real charged
word model and explicitly includes scalar/state operations, degrees,
repeated adjacency entries, and sparse output words. General source
mixtures, weighted graphs, and floating-point correctness are not smuggled
into its scope. The zero/direct branches and the additive constant for
unrestricted rho are present.

The graph/Stieltjes/KKT foundations imply inverse positivity, nonnegative
optima, source bounds, mass/support bounds, optimizer monotonicity, and the
strict outside-core slack used later. The stage's diffuse source supplies
both analytical comparators without computing them.

The comparison lemma is valid for a single comparator that need not
minimize its function. Applying it in the Q metric is justified by the
specific lower-box, upper-box, and mass-face sector signs. This does not
assert pairwise Q nonexpansiveness of Euclidean projection. The auxiliary
energy may be negative; its contraction still gives the stated positive
upper bound and the response estimate.

The selected signed-flow argument uses only emitted coordinates, charges
every repeated degree-volume appearance, and telescopes from zero positive
kinetic error. The analytical core and exact optima are never queried.
Source refreshes and cached response updates are separately covered, so
the iteration count is not substituted for the locality proof.

The exact reporter has a finite ordered-breakpoint root search, including
ties and flat intervals. Its unexposed-state invariant makes raw values
strictly negative outside known records. Repair/output/source formation
and obsolete-record disposal are charged to the baseline and emitted
history. Tiny epsilon enters only the allowed logarithmic iteration
schedule; no support-margin search or hidden terminal full-graph scan is
needed.

## Appendix qualifications and A.14

The three stage tolerances correctly correspond to three different repairs:
the original exact clipping, the exact terminal PG refinement, and the
bounded dyadic PG/grid/max repair. The downward perturbation interface and
scalar-only rebase control both actual stored energies. Closed-tail
emission prevents repeated adjacency work on discarded sub-grid values.
The two-tree reporter removes degree denominators from weighted moments,
and the source statistics and output certificate use upward integer
square sums. Quotient/remainder costs are explicitly separate from an
unadvertised floor primitive in the arbitrary-real theorem.

The source-energy, binomial, cached-checkpoint, singleton, and adaptive
refinements use only their stated current-stage assumptions. Zero-step
setup/repair is charged. The adaptive final clamp is distinguished from
nonfinal factor-two-to-four decreases. Its parameter is rebuilt from
current bounded dyadic counts, so no historical denominator product is
introduced. The mass-deficit comparison uses the current diffuse baseline,
not an unsupported geometric sum of mass-weighted stages.

A.14 matches mass_scaled_rounding_precision_audit.md:
both perturbation recurrences acquire exactly one factor eta; the raw,
primal, and mirror error coefficients remain unchanged; the effective
floor is at most 29*eta*h/theta. The proposed ceiling implies all old raw
and terminal guards, response and selected-work bounds retain their eta
factor, and every schedule uses actual tau. Zero-step certificates do not
add a fictitious rounding floor. The nontrivial assumption eta>=r>0
excludes division by zero.

Exact reduced-baseline representation is sufficient in A.14. The displayed
h_new>=min(h_old,g_num)>theta*tau_new/512 induction is correct even when a
final clamp permits coarsening. The old bit envelope therefore remains
valid; the text does not claim a smaller graph-read count or runtime on
every input.

## Guide and remaining wording

The guide now distinguishes the fixed schedule described in the main
argument from optional adaptive source selection and mass-scaled precision.
It preserves the actual stage tolerance and final repair, and explains
that unused baseline grid bits need not be retained. Its claims about
the optional methods are no stronger than the appendix theorems.
The nontrivial/unrestricted complexity distinction and the rational-versus-
floating-point distinction are both explicit. It also distinguishes
paired backend checks from different graph instances and finite testing
from a mathematical proof or external peer review.

The abstract initially omitted the nontrivial-regime qualifier on the bare
soft-O(1/(rho*sqrt(alpha))) bound. The author has now added
0<rho<1/d_seed, matching the main theorem and guide; this correction was
checked. The running header was also updated from Working proof to Proof
and implementation. Neither edit changes a lemma or theorem equation.
The final frontmatter also now states explicitly that the audits occurred
within this research task and are not external peer review; that wording
was checked.

No additional unresolved analytical hypothesis was identified. The
bounded-bit extension still assumes rational inputs, explicitly encoded
oracle replies, and the charged deterministic integer arithmetic model;
computation internal to an arbitrary user-supplied oracle is extra.
This is an internal proof audit, not a claim of outside peer review.

## Reviewed final hashes

- deterministic_conjecture2.tex:
  d5425bc5aec84166adf6ffbda7bb1738bed26eab458df1b1b40e565410a3f2fa
- practical_refinements_appendix.tex:
  dfa059bf8ab9631d4881818f5e10ac1511b5877daa3dd8af0e65547f4431d4e8
- practical_schedules_appendix.tex:
  3fb6d6d901d5c7c3e2105bb31e94e2827d031d1c27b5d610324a4cca2a25b559
- proof_reading_guide.md:
  7c5ac64a4a1a153e9efe4109504d30bfa08ac47ceeead942e25b900f2ab07751
