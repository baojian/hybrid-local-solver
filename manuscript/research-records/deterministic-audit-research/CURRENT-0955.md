# Current handoff — September 5, 2026, about 09:55 UTC

**Goal active. Ten-hour request is not complete.** Started01:41:57 UTC;
wall minimum11:41:57. At09:44, get_goal reported27,243 work seconds (7h34m).
Require>=36,000 work seconds too, likely around12:10. No token budget.
All algorithms/experiments deterministic. References stay read-only. No
private explorations disclosed to other tasks. No subagents/automation made.
Send meaningful commentary about every60sec; avoid long reasoning silences.

## Main proof

Parallel task **Prove conjecture 2 deterministically** developed the core.
Its ID01a06f28-982b-7fb2-835e-8494fb69d338 and source directory
`../research/conjecture2_deterministic_20260905/`. Full main TeX and practical
appendix were independently audited; no gap found in first complete pass.
Not machine-checked. Credit the other task. First-read hashes in
`notes/independent-proof-audit.md`; later snapshot hashes differ because its
owner kept editing. Recheck final version if relying on that file.

Core: diffuse-source safe continuation, Euclidean box/mass projection,
special M-metric sector at t=M^{-1}s, second energy, selected signed flow.
Repeated kinetic volume148K/r exact,360K/r bounded dyadic. Deterministic
ordered reporters and scalar-only rebases close fully charged OP2.

## Latest private code: pruned_rppr/, version0.3.0

Attributed copied core, PROVENANCE.json records source hashes; originals
unchanged. AVL graph-state maps, standard-library runtime, exact rational
inputs and bounded dyadic state. Public exports: solve_fast (recommended),
solve (slow rational reference), solve_integer, solve_with_source_energy.
Last two retain early_certificate=False by default for trajectory comparison.
solve_fast defaults to early_certificate=True and bounded_pilot=True.

Proved/implemented refinements:
- Fixed final degree cutoff1/rho, original degrees retained. M=Q_AA has
  Mw>=alpha w, |M|w<=w. Use second linear term lambda(Mw)^T xi. Restricted
  source mass inequality, not identity. Tighter box max(h,max source/alpha).
  A decreasing cutoff is proved but NOT implemented.
- Integer-state continuation and shorter source-energy schedule. Squared
  source sums round upward on common denominator; no degree LCM growth.
- Bounded component discovery (original scan volume<=1/rho), direct component
  acceleration with boundary-forest lower bound beta>=alpha. Root distance
  1/k_root, unit path edges, L=max_root sum d_i*distance, beta=alpha+c/L.
- Geometric PG checkpoints in continuation, scanning only candidate rows.
  Test(1-alpha)^2 U2<=alpha^2 delta^2/4, reuse successful PG in clipping.
  Summary certified_point distinguishes candidate vs projected-gradient.
  Failed scans and norm arithmetic are separately counted.
- A single bounded pilot on the incomplete prepass region C. Accelerate on
  Q_CC using beta_C, but accept only with a FULL-A PG certificate using alpha.
  On rejection discard iterate and fall back to continuation from zero with
  charged oracle cache. Local tolerance alpha^2 delta^2/16 and additional
  grid h<=alpha delta rho/16 guarantee acceptance by horizon if C contains
  the full optimum, without a strict complementarity margin. Worst-case OP2
  remains unchanged. Notes: bounded-region-pilot.md, checkpoint-certificates.md.

An optional bit-complexity issue was found and fixed: exact Fraction sums of
PG displacement squares can accumulate degree LCMs. Now use
sum ceil(a_i^2/d_i)/C^2, a certified upper bound. Component helper
displacement_norm_upper; sparse helper _integer._projected_gradient.

## Completed exact checks

- Main stages576cases/18,432steps; sector16,100cases.
- Pruned continuation72cases/17,652steps/216stages.
- Sorted projection5,184cases; full fast solver54cases, repeated after
  integer fallback, forest and checkpoint changes. Last run8sec.
- Special branches5, including fixed horizon.
- Integer/rational12cases/768full-trajectorysteps,32wrappercases; rerun after
  PG refactor, all passed47.14sec.
- Forest5,652exactPSDchecks +6longerpaths.
- Checkpoints875normcases,576exactPGpoints,126fullsolvercases/294stages/
  1,746checks. All294early. All actual graph replies reconciled with counters.
  Virtual star activates degree2^100 PG vertex while scanning one old entry.
- Bounded pilot144cases,74accepted,4rejected; both early/fixed-horizon modes.
  Misleading branch intentionally omits part of optimum; rejection/fallback
  correct. All order, gap, volume, degree reply and incidence audits pass.
Results and scripts have matching descriptive names in results/experiments/.

## Virtual benchmarks, all exact symbolic full-graph KKT audits

- Path32 with excluded2^100-leaf hubs: fast64steps,94entries,.07-.09sec over
  alpha1e-2..1e-10. Atalpha1e-4 rational continuation192sec, integer source20.3sec.
- One-boundary paths16/64:1024/4096steps,31/127entries acrossalpha1e-4/1e-8/1e-12;
  forest L=n^2. Six cases passed.
- Billion-vertex retained leaky path, prepass254entries: checkpoint-only
  continuation1.37sec atalpha1e-4,190.91sec at1e-8. Third1e-12 case deliberately
  stopped; no result. Valid rows preserved in virtual-checkpoint-fast-before-pilot.jsonl
  and stop notice virtual-checkpoint-fast-stopped.md.
- Same billion-path with bounded pilot:64/128/128steps,.193/.378/.393sec for
  alpha1e-4/1e-8/1e-12,254entries,171degree replies. virtual-checkpoint-pilot.jsonl.
  Structured Python measurements, not general runtime predictions.

## Deliverables and remaining work

deliverables/deterministic_op2_audit.tex is now a substantial self-contained
restatement with all refinements, prior-obstruction comparison and OP1
corollary (distinct epsilons). OP3 explicitly not claimed. **PDF IS STALE**:
last compiled first7-page draft. Recompile twice, inspect log, render every
page with Poppler and inspect images under the already-read PDF skill.
LaTeX/Library/TeX/texbin/pdflatex; Poppler/opt/homebrew/bin.

Still needed: portable solver package, README/pyproject, concise independent
tests, virtual graph example, provenance/verification manifests, final paper
and code review, PDF QA. No final ZIP/README yet. Consider one huge plain path
pilot benchmark to complement leaky hubs, but keep experiments bounded.

No known live experiment. Recent90201/19264/60352/50431/11781 complete.
4677/PID1536 stopped during third benchmark. pdflatex53387 may be unclosed
but completed. Do not restart old candidate campaigns: mass-preserving repair
still has an OPEN rate; keep it separate from the proved method.

Use login:false and absolute job paths. .venv configured. Backup
/Users/baojian/.codex/research/deterministic-op2-20260905 is stale since07:54;
refresh notes/code/artifacts and hashes without huge logs. Disk about4.6GiB
free at07:43. Continue until all deliverables AND both time conditions pass.
