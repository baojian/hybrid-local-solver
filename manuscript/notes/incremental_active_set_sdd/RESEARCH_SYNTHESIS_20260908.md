# Conjecture 3: tightness, new results, and the next direction

**The inverse-accuracy target is supported by a matching worst-case output
lower bound. The arbitrary-graph upper bound remains Open.** This is the
correct distinction behind the decision to continue the additional
research campaign.

This report covers **600.770027 NEW actual active minutes** in the third
campaign, completed on 8 September 2026. Its final active-time record
is in [the work ledger](OVERNIGHT_20260908_WORK_LOG.json); both earlier
campaigns and unverified intervals are excluded. New proofs below are
**Proved here, as drafts awaiting independent review**. Exact finite
checks support the formulas and implementations; they do not replace
review of an asymptotic proof.

## What “tight” means here

OP3 in `problem_definitions` asks whether successive nested SDD systems
can be reused to obtain nearly linear work in `1/eps_appr`, charging
updates, boundary searches, materialization and output. The known
Wei–Yang source bound is nearly quadratic in that accuracy parameter,
with only logarithmic dependence on inverse teleportation. The parameter
is the original ACL residual tolerance, not automatically the project's
semantic PPR tolerance or RPPR objective tolerance.

For the original certificate

    0 <= e_v - (D-gamma*A)x <= eps_appr*d,
    gamma = (1-alpha)/(1+alpha),
    p = (1-gamma)*D*x,

an omitted coordinate is interpreted as zero. The existing star argument,
with the checked parameter conversion, forces at least
`1/(16*eps_appr)` positive output coordinates on a hard family when
`eps_appr <= 1/16` and `0 < alpha <= 1/3`. A four-type double-star version
keeps this requirement while allowing arbitrarily large ambient graphs.
Thus a bound of nearly `1/eps_appr` would have the optimal accuracy power.
At `alpha=1`, the exact distribution is just the seed, so the lower bound
must not be asserted for every teleportation parameter.

The [primary-source transfer audit](LOWER_BOUND_LITERATURE_AUDIT_20260908.md)
checks the degree-normalized SSPPR literature, recent undirected query
bounds, and directed SSPPR lower bounds. Their graph, error, preprocessing
and fixed-alpha assumptions differ. In particular, their lower bounds
do not establish OP3's proposed upper bound or an unavoidable inverse-alpha
factor. The audit also refutes an **instancewise** mass-over-error reading:
some inputs have much cheaper valid local outputs. The existential
worst-case lower bound survives.

Primary references include
[Wei, Wen and Yang, ICDT 2024](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICDT.2024.9),
[Bertram and Jensen, 2026](https://arxiv.org/pdf/2602.10843v1), and
[Jiang et al., PODS 2026, checked v5](https://arxiv.org/pdf/2507.14462v5).
The transfer audit records exact pages and limitations rather than treating
these formulations as interchangeable.

## The most useful advances from this campaign

| Result | What it establishes | What it does not establish |
| --- | --- | --- |
| Complete supplied weighted recursion | A source-backed near-linear supplied computation, with weighted routing, resistance estimation, sampling, recursion, failure and allocation budgets reconciled. | It does not discover a local support. The whole asymptotic recursion and imported low-stretch tree algorithm are not implemented experiments. |
| Supplied significant-envelope repair | Given a set of original volume V containing obstacle values above eps_appr/8, ACL repair costs `(1+V)*polylog(2+V+1/eps_appr+1/p)`, independent of target alpha in exact-real arithmetic. | The suitable envelope is input; its discovery remains unpaid until a separate finder is proved. |
| Conservative-envelope equivalence | With explicit original-volume and all-branch work caps, the algorithmic ACL target is equivalent to finding a small significant envelope for a proper conservative obstacle. | It is a reduction, not the missing finder, and does not by itself implement literal reuse of the source's exact nested systems. |
| Complete batches of original twins | Under an unsupplied k-type promise, local exact/ACL work is `O((1+V+(1+k)^3)*log(2+V))`. Full original rows identify types only after their admission is paid. | The additive type term can be cubic; an induced-batch type partition can discard a real Schur contrast. |
| Sparse twin-quotient trees | When the canonical original-type quotient is a tree, a full local proof gives `O((1+V)*log^4(2+V))` work and `O((1+V)*log^3(2+V))` retained words, with V below 1/lambda. | This is a structural graph class. Fast tree balancing is a published source algorithm; the numerical driver in the audit is an explicitly slow reference. |

The last result handles dense original graphs as well as ordinary trees:
a large clique or independent type can be represented by one weighted
quotient node. The local algorithm does not receive that partition. Its
new obligations are the physical seed's contrast within its type, ordinary
degree heaps, a special gate for missing source twins, and the once-only
update when the source class grows. Those operations now have explicit
proofs and separate exact audits.

The latest state-machine audit has **5,129 complete outputs**, **58,047
original residual checks**, and **10,161 independently checked positive
prefixes**. The weighted primitives have a separate audit. The combined
source-growth/new-leaf update order was checked in **1,298 transactions**.
Private huge-hub oracles reject any remote hub-row query and still obtain
valid original certificates. These are exact correctness and operation
checks, not floating-point speed measurements.

The exact physical solvers also admit a separate canonical RPPR
consequence: direct dyadic output achieves the requested objective gap
with output precision independent of target teleportation. This does not
supply an internal bit-complexity bound, and those canonical dyadic values
are not advertised as rounded ACL output.

## What the unsuccessful directions taught us

Several tempting shortcuts fail for specific reasons.

- A larger teleportation parameter can omit significant conservative
  coordinates. The proved comparison needs a fourth-power accuracy scale
  for the particular reduction; a path family shows why that power cannot
  simply be relaxed in the same rule.
- A constant-factor spectral approximation need not preserve significant
  obstacle support. Reducing the obstacle penalty by a fixed or
  polylogarithmic factor does not generally repair that support rule.
- Dense Schur updates, individual response groups and dense batch
  quotients can all incur cubic work on explicit branching families.
  These are obstructions to those representations, not universal OP3
  lower bounds.
- The new teleportation-independent cubic local references are useful
  debugging and comparison tools. They do **not** improve the known
  nearly quadratic general upper bound.

This is why faster supplied solves alone are not enough. The remaining
problem is to discover or certify the useful local region without paying
for repeated inspection of a growing collection of coordinates.

## Recommended next steps

**For the main conjecture, prioritize conservative significant-envelope
discovery.** It now has a precise, parameter-free target: at penalty
`lambda=eps_appr/2`, find a set containing every conservative potential
above `eps_appr/8`, with original volume `O(1/eps_appr)` and total work
`(1/eps_appr)*polylog(2+1/eps_appr+1/p)` on every execution. A successful
finder would compose with the supplied repair already proved. Require a
charge for every failed boundary check and every copied state; a support
existence statement alone does not meet this target.

**For a bounded next theorem, pursue a single cycle in the original-type
quotient.** The tree construction provides most of the local machinery.
The new cycle-budget lemma bounds multi-parent response groups by the
remaining quotient cycle rank, plus one possible incomplete source type.
It also identifies when a large parent count certifies a missing source
twin. A five-cycle shows that two parents alone are insufficient: the
source-twin residual formula is then wrong even on a legal positive prefix.
The next construction must maintain the small exceptional groups, weighted
cycle correction and source contrast with all costs charged. This is still
**Open**, not an automatic corollary of the unweighted unicyclic result.

Before promotion, independently review the supplied recurrence's source
contracts and the complete twin-tree composition, particularly the
root-before-links update and failure-branch accounting. Consolidating these
proofs is more valuable than adding more finite tests that merely repeat
the same identities.

## Where to read and reproduce

- [Lower-bound audit](LOWER_BOUND_LITERATURE_AUDIT_20260908.md): source assumptions, quantifiers and exact parameter transfer.
- [Complete twin-tree proof](sections/op3_local_twin_quotient_tree.tex): `thm:op3-local-twin-quotient-tree`.
- [Supplied-envelope proof](sections/op3_supplied_envelope_alpha_floor.tex): `thm:op3-alpha-independent-supplied-envelope`.
- [Conservative reduction](sections/op3_conservative_envelope_equivalence.tex): `thm:op3-conservative-envelope-equivalence`.
- [Bounded-cycle next target](sections/op3_quotient_cycle_frontier.tex): the proved combinatorial quota and the exact five-cycle obstruction; the numerical extension remains Open.
- [Current status](STATUS.md), [campaign ledger](OVERNIGHT_20260908_WORK_LOG.json), and the numbered campaign checkpoint audits: provenance, checks and continuation details.

The standalone note builds with `make -C manuscript/notes/incremental_active_set_sdd`.
The experiment registry records each exact audit's full invocation. Generated
JSON records include parameters, source/dependency hashes and separate
reference-work counters. Historical audits remain snapshots of their
recorded revisions; the final provenance review identifies two unchanged
prior-campaign records with older primary hashes and no recorded basename
dependency mismatch. The relevant code and results are committed and
pushed under the user's continuing authorization. The active manuscript
has not been changed by this campaign.

Repository-wide checks retain the documented pre-existing failures: three
tests, two unrelated lint findings and two oversized note sources. Their
five source hashes have been checked against the campaign baseline.
`make reproduce` stops at the same failed test prerequisite; its later
stages do not run. Focused checks for this direction pass.
