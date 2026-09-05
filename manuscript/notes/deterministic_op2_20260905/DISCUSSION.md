# Algorithm explanation, provenance and practical position

Recorded 2026-09-06 from the follow-up discussion. Source papers were checked
in their primary online versions during that discussion; the attached
notation inventory was a reference, not an instruction source.

## What is the algorithm?

At fixed regularizer r, let w_i=sqrt(d_i), lambda=alpha*r, and let
s=b-M*baseline be the source residual. Here s is not the seed vector.
The original-degree-pruned principal matrix M is discovered locally.
Choose theta of order sqrt(alpha), and optimize the correction over
K={0<=u<=4*r*w, w^T*u<=w^T*s/alpha}:

```text
xi = z = 0
repeat the predetermined accelerated horizon:
    y = (xi + theta*z)/(1 + theta)
    q = (1-theta)*z + theta*y - (M*y-s+alpha*r*w)/theta
    p = project q onto K
    xi = (1-theta)*xi + theta*p
    z = p
candidate = baseline + xi
certify candidate and clip downward to obtain the next safe baseline
```

The projection is p_i/w_i=min(4*r,max(0,q_i/w_i-eta)). A deterministic
breakpoint search finds eta for the mass cap. Shared scales, persistent
matrix-response records and ordered trees implement the vector operations
implicitly. A dense or historical-support-scanning transcription would not
inherit the local-work theorem.

Continuation halves r to the requested rho. The additional energy controls
the squared matrix response by O(alpha^2*r); selected signed-flow accounting
then bounds cumulative emitted row volume by O(K/r). No general SDD solver,
randomized retry, sampling algorithm, or AESP inner process is used.

## How the earlier notes and prompts helped

The Stieltjes/obstacle and subsolution notes supplied positivity and order
certificates. Safe-box audits distinguished mathematical acceleration from
a cheaply implemented projection. Overshoot and boundary-counterexample
notes identified cumulative transient work as the real obstacle. The
threshold-reporter and support-discovery-ledger hints directed attention to
actual data structures and all first/repeated work.

The instructions to check explored directions, prohibit randomness, and keep
the algorithm practical shaped the audit and refinements. The duration
requirement allowed deeper verification; it is not mathematical evidence.
The core continuation/two-energy argument originated in the parallel task
**Prove conjecture 2 deterministically**. This session independently audited
it and supplied the refinements identified in README and the package
provenance. No private directions were sent to the parallel task.

## Closest 2026 comparisons

All RPPR comparisons use additive objective accuracy eps_obj, suppress
polylogarithmic accuracy factors, and convert lazy/non-lazy conventions.

**Fountoulakis--Martinez-Rubio (FM26), arXiv 2602.21138v2, April 8 revision.**
Theorem 4.3 analyzes standard FISTA on F_(2*rho), with the smaller-regularizer
optimum as comparison core. Under confinement to B, its work includes
1/(rho*sqrt(alpha)) plus sqrt(vol(B))/(rho*alpha^(3/2)); Theorem 4.4 gives a
structural sufficient condition. Proposition 4.7 gives a star on which FISTA
incurs Omega(m) work. The paper already analyzes cumulative spurious work
and removes a global minimum-margin dependence using two regularization
levels. Our added mechanism removes the external boundary-volume term for
a different, constrained continuation algorithm. It does not establish that
ordinary FISTA has unconditional accelerated locality.
[Primary source](https://arxiv.org/html/2602.21138v2).

**Wei--Yang (WY26), arXiv 2608.16339v1, August 17.** Theorem 1.3 uses growing
active sets and repeated SDD solves, with work
O_tilde(|S*| vol(S*)) <= O_tilde(1/rho^2), polylogarithmic inverse-alpha
dependence, additive RPPR accuracy, and an ACL residual-witness guarantee.
The headline bound is randomized; its deterministic-solver remark adds a
|S*|^o(1) factor. Our core uses deterministic local updates and threshold
reporting, retaining 1/sqrt(alpha) while achieving linear inverse-rho
dependence. This is a tradeoff: comparing the worst-case envelopes favors
ours when rho<sqrt(alpha), ignoring logs, but their support-sensitive bound
can be better on an instance. Objective error and an ACL witness must be
compared explicitly rather than conflated.
[Primary source](https://arxiv.org/html/2608.16339v1).

## Relation to the user's 2024--2025 work

The 2024 locally evolving-set framework foregrounds cumulative active
volume. AESP (2025), Theorem 3.6, obtains a PPR work bound
O_tilde(min(m/sqrt(alpha),R^2/(sqrt(alpha)*eps_ppr^2))) using nested local
proximal solves. Its discussion explicitly states that R lacks a universal
input-parameter bound and suggests simplex constraints as a possible remedy.
Our mass cap, degree-scaled box and diffuse-residual continuation develop a
related constraint-based direction into a proved work estimate for the new
algorithm. They do not establish bounded R for the existing AESP trajectory.
[2024 paper](https://arxiv.org/abs/2410.15020),
[2025 paper, Section 3.3](https://arxiv.org/html/2510.08010#S3.SS3).

## Is it practically better than FISTA?

**Open.** The current exact-arithmetic implementation has continuation,
tree-maintenance, projection and certificate overhead. A simple optimized
FISTA implementation may be faster where temporary supports remain small.
Small alpha and costly spurious activations are plausible favorable regimes
for this design, but that expectation has not been established by a fair
head-to-head benchmark. The completed tests verify correctness and selected
structured timings, not practical superiority.

The next experiment should compare optimized implementations at the same
certified objective gap, recording wall-clock time, every scanned adjacency
incidence, state-maintenance work and memory. Do not report iteration counts
alone or equate an exact-rational prototype with a production floating-point
solver.
