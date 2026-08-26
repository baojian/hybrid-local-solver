# Direction status: bounded_seed_return

Last reviewed: 2026-08-27
State: proved-open
Agent family: codex
Role: direction
Branch: `agent/codex/bounded-seed-return`
Base commit: `a02b39a2bb12e8e9d528ae1f011f8f041f98bed3`
Allowed write scope: `manuscript/notes/bounded_seed_return/` plus the
registered controller files.

## Exact question and contract

- **Question:** Can a finite connected graph family have simultaneously
  `vol(S_eps_ppr) = Theta(1 / eps_ppr)`, bounded ordinary seed degree, and
  seed self-return amplification `pi_v / gamma_alpha = Theta(1 / alpha)`?
- **Model:** The shared source-aligned single-seed PPR system on finite simple
  undirected unweighted connected graphs without isolated vertices, with
  `c_alpha = (1-alpha)/(1+alpha)` and
  `gamma_alpha = 2 alpha/(1+alpha)`.
- **Accuracy namespace:** `S_eps_ppr = {u : pi_u/d_u > eps_ppr}` uses the
  semantic degree-normalized PPR threshold.  No identification with
  `eps_appr`, objective gap, a KKT tolerance, or a residual certificate.
- **Access and charged work:** The theorem is structural and charges no
  algorithm.  The degree `d_v` is the ordinary adjacency-list degree.  The
  algorithmic discussion retains the project's one-hop charge `d_u` but
  derives no end-to-end work upper or lower bound.
- **Intended result:** Rule out the star-scale self-return mechanism at a
  bounded-degree seed, quantify the degree necessary to retain it, and keep
  this conclusion separate from any distributed signed-relaxation lower
  bound.

## Claim ledger

- **Source:** Only the shared source-aligned PPR definition and elementary
  normalized-Laplacian spectral decomposition are used.
- **Proved here:** The local spectral-measure bound
  `F_v(t) <= 4 d_v sqrt(t)`; the explicit discounted Green-diagonal bound;
  impossibility of simultaneous support saturation, bounded seed degree, and
  `Theta(1/alpha)` self-return in the joint local limit; the exact necessary
  degree `Omega(1/(eps_ppr + sqrt(alpha)))`; and its
  `Omega(1/eps_ppr)` specialization when `alpha = O(eps_ppr^2)`.
- **Conditional:** The upper delimiter `d_v = O(1/eps_ppr)` uses the separate
  semantic-nontriviality assumption `eps_ppr d_v <= pi_v/2`; combining it
  with the preceding specialization gives `Theta(1/eps_ppr)` seed degree.
- **Measured:** A deterministic verifier screens paths, caterpillars,
  fixed-degree hub ladders, finite binary trees, and a three-regular
  cycle-plus-antipode gadget.  Every family has vanishing
  `alpha pi_v/gamma_alpha`; the one-dimensional families have
  `Theta(alpha^{-1/2})` amplification while their best semantic thresholds
  keep `eps_ppr vol(S_eps_ppr)` bounded away from zero.
- **Refuted:** Bounded seed degree cannot realize the star's simultaneous
  support and self-return scalings.  The stronger unqualified inference
  "self-return amplification forces `Theta(1/eps_ppr)` seed degree" is not
  proved: without `alpha = O(eps_ppr^2)`, the graph-uniform conclusion is only
  `Omega(1/(eps_ppr + sqrt(alpha)))`.
- **Open:** A lower bound for every signed one-hop relaxation member may still
  be forced through operations distributed away from the seed.  The theorem
  neither constructs such a family nor supplies an algorithmic upper bound.

## Central blocker

The bounded-degree self-return question is closed.  The remaining lower-bound
question requires a mechanism other than large seed diagonal response, such
as a distributed collection of mode-coupled displacements whose total charged
work is large even though no single bounded-degree seed operation is forced
`Theta(alpha^{-1/2})` times.

## Dependencies and reusable outputs

- **Formal registry dependencies:** none.
- Source/shared prerequisites: the shared source-aligned PPR definition.
- Context/provenance: the open bounded-seed-degree screen in the separately
  owned class-separation ladder motivated the question; no proof is imported
  from that direction.
- Supplies to: any class lower-bound argument using the seed diagonal of the
  discounted Green kernel, and graph-zoo screening of reflecting gadgets.

## Resume here

- Exact file/section/lemma: `main.tex`, Lemma
  `lem:bounded-return-spectral-measure`, Theorem
  `thm:bounded-return-diagonal`, and Corollary
  `cor:bounded-return-support`.
- Next concrete action: search for a distributed signed-relaxation obstruction
  in which charged work is spread over `Theta(1/eps_ppr)` bounded-degree
  vertices rather than certified by seed travel.
- Stop/go test: reject any proposed bounded-seed self-return witness if
  `alpha*pi_v/gamma_alpha` tends to zero; do not reject a distributed class
  lower bound merely because this scalar tends to zero.

## Verification

- Source pointers checked: `docs/mathematical-conventions.md`, the shared
  source-aligned problem, and `docs/literature/local-solvers.md` for accuracy
  and lower-bound scope discipline.
- Focused checks: the note builds to an eight-page PDF with no LaTeX warnings;
  the registry reports 20 consistent notes; `verify.py` passes 4,176 rooted
  spectral/resolvent cells, all nine closed-form truncation cells, and the
  five-family support screen; all 210 repository tests pass; the coordination
  audit passes; and focused Ruff lint passes.  Repository-wide `make lint`
  remains red only on 1,345 pre-existing findings under
  `manuscript/claude-overnight-2026-08-24/`, outside this assignment.
- Known gaps: no finite-precision claim, no weighted-graph extension, no
  directed-graph extension, and no theorem for the total work of signed
  relaxation or a stronger response primitive.
