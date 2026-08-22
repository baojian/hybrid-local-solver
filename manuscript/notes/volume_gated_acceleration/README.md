# Volume-gated acceleration research note

This directory contains a standalone LaTeX note reconstructing the project
discussion on active-volume flattening, spider obstructions, RPPR-based safe
support gates, and accelerated continuation across expanding subspaces. It is
a curated mathematical synthesis rather than a verbatim transcript.

Build from this directory with:

```bash
make
python3 check_round013.py
python3 check_round014.py
python3 check_round015.py
python3 check_round016.py
python3 check_round017.py
python3 check_round018.py
python3 check_round019.py
python3 check_round020.py
```

The note embeds its bibliography and deliberately uses note-scoped
normalizations while the repository-wide residual convention remains open.
It separately labels source results, new proofs, conditional implications,
refuted claims, and open conjectures.

The main closed statements are:

- every principal PageRank system has condition number at most `1 / alpha`,
  and a depth-`L` spider prefix has condition number
  `Theta(1 / (alpha + L^(-2)))`;
- an exact PPR core of volume `1 / tau` exists;
- fixed RPPR regularization gives support volume at most `1 / rho` and PPR
  error at most `rho`;
- signed accelerated candidates can be corrected to safe lower envelopes,
  yielding safe support admission and a one-sided KKT error certificate;
- choosing `rho = tau = epsilon / 2` proves peak working volume at most
  `2 / epsilon` and final PPR error at most `epsilon`;
- an endpoint-source path refutes the claim that support changes require only
  `O(log(1 / epsilon))` ordinary restarts uniformly in `alpha`;
- an exact endpoint-edge run refutes shock-free transport of a zero
  fixed-face estimate-sequence energy across one safe admission, while leaving
  cumulative shock and newly admitted-volume amortization open;
- a modified estimate-center recurrence has an exact face-change identity:
  transporting the center by the restricted-optimum displacement adds exactly
  the Schur gain, and the nonnegative gains telescope;
- the geometrically weighted Schur tail has an exact summation-by-parts form:
  it charges discounted occupancy of the remaining face-optimum gain, not a
  `sqrt(alpha)` fraction of the unweighted telescope; a terminal one-edge
  family makes the ratio to that proposed scaled charge unbounded;
- on endpoint paths, an append-only exact `LDL^T` response stores centered
  momentum so that each transport append is charged to newly admitted volume
  without materializing the dense old-prefix shift; its full response
  applications, recurrence reads, state writes, validation, memory, and output
  remain charged in the displayed eleven-coordinate ledger;
- an exact rational zero-start endpoint-path family with
  `q=1/n`, discovery radius `L=n^2`, and
  `rho=tau=(q/3)((1-q)/(1+q))^L` forces at least `L` singleton admissions and
  swept full-prefix work `Omega(L^2)=Omega(q^(-4))`; this certifies a factor
  `1/q` above its realized `nu_fin/q` product, but the certified lower-bound
  factor is only logarithmic in the deliberately tiny accuracy and therefore
  does not refute a soft-order product theorem;
- at the constant ratio `rho=tau=q/5`, the exact radius
  `L_q=floor(log(5/3)/(-log((1-q)/(1+q))))` gives
  `J,nu_fin=Theta(1/q)`, `T>=J`, and
  `mathfrak V_T=Omega(1/q^2)=Omega(nu_fin/q)` for the literal full-prefix
  implementation; this is only a product-scale floor and does not prove the
  observed `T=Theta(1/q^2)` or `mathfrak V_T=Theta(1/q^3)` scaling;
- an exact `q=1/5` zero-start trace refutes frontier-only admission logic:
  the safe-envelope correction is seed-attained and suppresses a raw
  frontier violation at stage 6, then its maximizer switches to the old
  interior vertex `v_2` by stage 9;
- the same actual projected trace gives a narrower pointwise STOP
  (`prop:path-monotone-correction-potential-fails`): on the held face `U_3`,
  the full moving correction increases strictly from stage 6 to stage 7, and
  at stage 7 it exceeds `q^(-1)` times the normalized error to the restricted
  optimum. The complete run has `J=4`, `T=16`, final volume `9`, swept volume
  `114`, no intermediate emission, one terminal return, and the specialized
  eleven-vector `eq:path-monotone-correction-stop-eleven-vector`. This
  refutes only monotone correction debt and that coefficient-one pointwise
  bound, not a nonmonotone or phase-aware aggregate proof;
- the explicit face-local correction--error bank
  `Phi_t^bank = delta_t + q^(-1) e_t` survives that reviewed stage-6--7
  correction spike, but the same literal chronology refutes its held-pair
  monotonicity at the earliest later pair: stages 9 and 10 both hold on
  `U_4`, while `Phi_10^bank > Phi_9^bank` even though the correction itself
  decreases. The full run and charged vector remain
  `(Theta(9), Theta(5), 1, 0, Theta(114), Theta(114), Theta(114), Theta(9),
  O(9), Theta(114), Theta(9))`. More strongly, the full fixed-coefficient
  family `delta_t + c q^(-1) e_t`, `c >= 0`, has incompatible exact local
  constraints: the held `U_3` pair 6--7 requires
  `c >= 2978273417354 / 42112483166425`, while the held `U_4` pair 9--10
  requires `c <= 95554102960761584 / 1567701294665491845`. Their intervals
  are disjoint. This finite pairwise STOP assumes the literal face-local
  reset and event order; it neither defines a global block horizon nor
  refutes time- or face-dependent coefficients, longer phase blocks,
  coordinatewise monotone lower-point invariants, or aggregate potentials;
- the unique tight endpoints of those two feasible half-lines define the
  named finite `TightPair-Schur_(3->4)` bank. Its values are exactly flat on
  held pairs 6--7 and 9--10. At the frozen literal stage-8 candidate, the
  face reset leaves the correction unchanged, changes the old/new normalized
  face errors to
  `101253632777792 / 25604026220703125` and `13229 / 1501825`, and has exact
  Schur/optimum drop `175006441 / 6398713140625`. The raw linear-bank jump is
  larger than that objective drop, but the dimension-consistent squared-bank
  jump is strictly smaller. Thus `bank^2 + H_j`, with
  `H_3=Delta_8` and `H_4=0`, strictly decreases across the isolated reset.
  The tight endpoints maximize that reset jump over every locally feasible
  pair. This is a finite switch-charge GO only: held evolution and admission
  reset are separate, and no global stagewise potential, coefficient rule,
  block horizon, logarithm removal, asymptotic bound, or spectral statement
  follows. The fully charged vector is unchanged;
- extending that exact account through the four-state chain
  `7 -> 8^- -> 8^+ -> 9` gives
  `prop:path-tight-pair-local-chain-stop`. The fixed-`U_3` production step is
  the first STOP:
  `Psi_8^- - Psi_7 =
  4798070852000000223973860697504672676758942656 /
  1000717813631998065466639280969584524631500244140625 > 0`.
  The frozen-candidate reset still decreases by the Round-017 exact slack, but
  the first fixed-`U_4` follow-up rises by
  `185418883451039233414483427688468628491104384871211336448 /
  2666939846939373614068372111818330675602595627307891845703125`,
  and at the tight endpoints the complete stage-7--9 net change is positive.
  The two adjacent failures (not the net sign) are robust over the earlier
  held-pair-feasible rectangle: production nonincrease would
  require
  `c_3 <= 2103479690463 / 41819574955745 < c_3^tight`, while follow-up
  nonincrease would require
  `c_4 >= 2617155474971384896 / 14508305905763575885 > c_4^tight`.
  Held evolution, production, reset, and follow-up remain separate. The
  complete vector is
  `(Theta(9), Theta(5), 1, 0, Theta(114), Theta(114), Theta(114), Theta(9),
  O(9), Theta(114), Theta(9))`; this is a finite local-chain STOP, not a
  global, multi-admission, asymptotic, logarithmic, nonpath, or
  finite-precision claim;
- the first explicit longer repair uses no invented production credit.
  `prop:path-tight-pair-recovery-block` defines the analytical post-reset
  reserve `R_(9:k)^post = Psi_9-Psi_k` as the exact telescope of realized
  later fixed-`U_4` squared-bank decreases. At the canonical tight pair, it
  is insufficient through stage 12 and first pays the stage-7--9 deficit at
  stage 13, so `Psi_12>Psi_7>Psi_13`. Because the tight pair maximizes the
  stage-13 minus stage-7 endpoint change, the `7->13` GO holds throughout
  the held-pair-feasible rectangle. The earlier positive `7->9` net remains
  tight-pair-only and nonuniform over that rectangle. The reserve has the
  same squared-bank/objective units as `Psi` and is a realized proof
  telescope, not free state known in advance. Auditing it uses one scalar
  accumulator and does not change the full eleven-vector. This is one finite
  exact-real, single-admission block, not a pointwise potential, online
  closing rule, multi-admission telescope, global block horizon, logarithm
  removal, asymptotic result, nonpath theorem, or finite-precision claim;
- a simpler observable score gives the first causal face-general recovery
  condition tested across two admissions.  Put `Xi_t = delta_t^2`; after each
  transition, credit only an already observed score decrease and an exact
  restricted-optimum drop only after its charged admission query, while
  debiting every score increase.  The resulting one-scalar identity is
  face-general but conditional.  On the actual `q=1/5` trace, starting from
  held stage 3, its balance stays nonnegative through the consecutive
  canonical stage-4 and stage-8 admissions and through stage 12.  The
  smallest positive carried balance occurs at stage 9.  If the unused
  stage-4 credit is discarded, the restarted stage-8 block is negative
  through stage 11 and first closes at stage 12.  Thus the earlier realized
  Schur credit supplies an exact cross-state cancellation; no future
  decrease is borrowed.  The complete run and eleven-vector remain
  `(Theta(9), Theta(5), 1, 0, Theta(114), Theta(114), Theta(114), Theta(9),
  O(9), Theta(114), Theta(9))`.  This is a finite exact-real two-admission
  scalar-ledger GO and local stage-11 ledger STOP/stage-12 ledger GO, not a
  convergence, objective-decrease, or work certificate, pointwise potential,
  uniform recovery horizon, all-admission telescope, logarithm removal,
  nonpath theorem, or finite-precision result;
- a moving-maximum energy bound controls the full old-face correction without
  locating its maximizer: every constant-ratio path face admits or certifies
  within `O(q^(-1) log(1/q))` steps, giving
  `T=O(q^(-2) log(1/q))` and
  `mathfrak V_T=O(q^(-3) log(1/q))` for the named literal full-prefix
  implementation, together with a complete eleven-coordinate upper ledger;
- for the candidate family `q=1/(16m)`, `rho=tau=q/5` on the full path
  `P_m`, the conditional fixed-full-face residual recurrence has exact damped
  cosine roots (`lem:path-full-face-linearized-roots`). Exact rational runs at
  `m=2,4,8` verify finite admission and terminal prefixes only. Independent
  audit rejected the proposed asymptotic packet/range lower bound, so this is
  non-theorem scaffolding and proves no logarithmic terminal block;
- under the displayed fixed-subspace accelerated-contraction premise,
  continuous restricted re-solving costs telescope to an accelerated term
  plus one discrete term per support expansion.

The graph-uniform
`O_tilde(1 / (rho * sqrt(alpha)))` work theorem remains open. Its precise
missing ingredient is now beyond the path-specific transport append: the
signed cross-defect of the literal zero-padded momentum has no cumulative
packing, while the exact weighted-shock identity leaves a remaining-gain
occupancy term that is not controlled by the unweighted telescope.  The
transported-center ledger still does not give product-scale total work in the
constant-ratio regime.  The moving-maximum theorem bounds the stage count and
old-prefix swept volume only up to an additional logarithm.  Removal of that
logarithm by a uniform `K_face=O(1/q)` proof or an aggregate
`T=O(1/q^2)`, `mathfrak V_T=O(1/q^3)` potential remains open, as does a
rigorous logarithmic fixed-face lower bound.  The
observed `T=Theta(1/q^2)` and `mathfrak V_T=Theta(1/q^3)` exponents still lack
matching global lower bounds.  The exact gate requires a nonlocal correction
rather than a frontier-only scalar, and any future upper or lower proof must
retain its moving global correction. The correction itself also cannot simply
be declared decreasing on held faces or bounded by `q^(-1)` times normalized
face error with unit coefficient. Nor can that same face error simply be
added as a coefficient-one decreasing bank: `delta_t + q^(-1) e_t` fails
from literal held stage 9 to held stage 10, despite passing the earlier
correction spike. Indeed, no nonnegative constant coefficient works on both
reviewed held pairs. This does not conflict with a monotone state invariant
that restarts its accelerated auxiliary state; scalar-bank monotonicity and
such coordinatewise preservation are different claims. The tight two-phase
squared bank shows that the one literal stage-8 reset can be paid by its exact
optimum-drop reserve. The complete local-chain audit now proves that the same
account rises on the candidate-producing step, falls at the reset, rises on
the first follow-up, and at the tight endpoints has positive net stage-7--9
change. Every held-pair-feasible coefficient pair fails both adjacent steps,
but the net sign is not uniform over that rectangle. It therefore cannot
supply a pointwise local telescope. The exact analytical post-reset recovery
telescope does close the one literal `7->13` block, first at stage 13 and
uniformly at that endpoint over the feasible rectangle, but gives no online
face-general or multi-admission closing rule. The new `delta^2`
realized-credit identity is face-general as an accounting condition and its
finite path balance survives the next canonical admission by carrying unused
stage-4 credit; without that carry the stage-8 account first recovers at stage
12. This establishes one exact cross-state cancellation, but gives no uniform
closing time or all-admission telescope. Extending or stopping this causal
balance on another graph, face, or order remains open.
The ledger also does not control nonpath response growth. The results use exact
real cells and prove no
finite-precision or automatic RPPR-to-PPR conversion;
the existing PPR guarantee applies only after the terminal one-sided
certificate with `rho = tau = epsilon / 2`.
