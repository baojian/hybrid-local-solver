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
face error with unit coefficient. The
ledger also does not control nonpath response growth. The results use exact
real cells and prove no
finite-precision or automatic RPPR-to-PPR conversion;
the existing PPR guarantee applies only after the terminal one-sided
certificate with `rho = tau = epsilon / 2`.
