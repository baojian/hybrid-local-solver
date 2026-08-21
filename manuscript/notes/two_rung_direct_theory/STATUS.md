# Direction status: two_rung_direct_theory

Last reviewed: 2026-08-21
State: proved-open

## Exact question and contract

- **Question:** On which graph classes is the literal charge-aware two-rung
  policy accelerated, what exactly breaks graph-uniform acceleration, and what
  minimal response operation removes that obstruction?
- **Model:** Shared source-aligned PageRank quadratic with note-scoped
  `r = b - Q x`; literal schedule
  `[(B*tau, omega_star), (tau, 1)]`.
- **Accuracy namespace:** `tau = alpha * eps_ppr` and
  `||D^(-1/2) r||_infinity <= tau`. No identification with RPPR `rho` or an
  objective tolerance (`main.tex:112-128`).
- **Access and charged work:** Executed coordinate `u` costs `1 + d_u`; the
  literal policy uses charge-aware top-`1/32` live snapshots. Forest
  elimination/recovery charges every forest vertex and incident edge; dense
  core work and storage are stated separately. The fixed-attachment reporter
  additionally charges verification/scanning of supplied closure certificates,
  boundary-row reads, cyclic response construction/application, sorting and
  queries, memory, validation, and output. Its bounds use exact
  real/algebraic-cell arithmetic and make no bit-complexity, finite-precision,
  or stability claim (`main.tex:130-143,233-262,2470-2552,2710-2880,2890-2911`).
- **Intended result:** A structural theorem/counterexample map for the literal
  method plus a certified pendant-forest response repair, not an unrestricted
  positive theorem.

## Claim ledger

- **Source:** The measured `B = 2.5` policy comes from `two_rung_sor`; the
  shared RPPR/PageRank operator supplies spectral bounds.
- **Proved here:** Factor-two score optimality per charge and finite-work
  fallback (`main.tex:256-482`); exact one-edge and endpoint-path dynamics,
  including literal measured-regime batching for `alpha > 1/49`
  (`main.tex:490-1020`); accelerated theorems under radial or persistent
  expansion (`main.tex:1395-2219`); linear closed-pendant-forest deflation,
  spectral lift, 2-core reduction, and finite-spider repair
  (`main.tex:2470-3060`). On a cycle core, same-attachment forest absorptions
  admit the exact `FACR(p)` affine crossing state with
  `O(V_fin + |R| log(2 + |R|) + Z)` total work and no global boundary rekey
  (`main.tex:2710-2880`).
- **Conditional:** A general positive solver requires an online certificate for
  closed decorations and a charged varying-attachment cyclic-core reporter;
  the fixed-attachment structural pieces do not yet compose into an
  arbitrary-graph product theorem.
- **Measured:** The note imports the best-tested `B = 2.5` campaign point; it
  does not prove or independently measure optimality.
- **Refuted:** Arbitrary unguarded batching and static parent closure fail
  (`main.tex:1095-1227`). More decisively, the fixed center-seeded `P3` has
  literal spreading work at least `alpha^(-3/2)/1408` for the stated regime,
  despite explored volume four (`main.tex:2252-2264`); the unrestricted
  graph-uniform accelerated theorem is false.
- **Open:** Literal top-`1/32` endpoint paths for `alpha <= 1/49`; online
  closure scheduling beyond the certificate assumed here; no-global-rekey
  2-core reporting when absorption vertices vary; a charged splice of corridor
  waves, persistent expansion, and boundary deflation.

## Central blocker

The fixed-attachment case is closed by `FACR(p)`: one static Green direction
gives monotone affine crossing times and no global rekey. Integrate certified
online 2-core peeling with a response-preconditioned finite-band reporter when
successive closed components attach at different core vertices. The exact
test is whether the resulting growing set of Green directions can be queried
without scanning/rekeying the whole core boundary.

## Dependencies and reusable outputs

- **Formal taxonomy dependencies:** `two_rung_sor` for the literal arm and
  `delayed_reflection_ladder` for the imported reflection/backflow response.
- **Supplies to:** `response_preconditioned_hybrid` and
  `propagate_settle_framework` through exact forest deflation, spectral lift,
  the 2-core reduction, and the fixed-attachment affine crossing reporter;
  supplies the literal-arm counterexample to every controller direction.

## Resume here

- **Exact pointer:** `main.tex:2460-2708` for the forest response repair,
  `main.tex:2710-2880` for `FACR(p)`, and the ordered next steps near the end.
- **Next action:** Test the first varying-attachment cycle trace, retaining
  implicit/kinetic state and charging each new Green direction.
- **Stop/go test:** Continue the composition only if varying-attachment
  reporter updates are final-volume/output sensitive; otherwise name the exact
  reporter representation and construct a sequence forcing its global rekey.

## Verification

- **Source pointers checked:** Required context/conventions, measured sibling,
  relevant response literature, README, claim ledger, lower bound, deflation,
  and next-step sections.
- **Checks last run:** Focused `make` passed with resolved references on
  2026-08-21; `make note-audit` passed with 18 notes across 5 tracks. An
  independent read-only audit verified the cumulative Sherman--Morrison
  algebra, monotone affine crossings including ties, exact-once output,
  factorization/work/memory ledger, and structural scope. Its review fixes now
  distinguish supplied-certificate verification from online closure discovery
  and state the exact-cell/finite-precision boundary explicitly.
- **Known gaps:** The README now states `1 < B < B_edge`,
  `B*q*eps_ppr < 1`, `h >= 0`, and `b_C >= 0` where the finite-spider and
  nonnegative Green-column results use them. `FACR(p)` reports absorption-only
  upward crossings while exterior coordinates are held fixed; it does not
  maintain a post-repair terminal queue, and it does not cover varying
  attachment vertices or finite-precision stability. The manifest, taxonomy,
  and root index already include the reviewed exact-cell fixed-attachment
  `FACR(p)` reporter; no controller metadata promotion remains pending.
