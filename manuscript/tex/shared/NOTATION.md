# Manuscript notation registry

This directory is the only declaration point for reusable LaTeX notation in
the active paper and standalone research notes.

## Layers

1. math_commands.tex defines generic typography, delimiters, operators, and
   named tolerances.
2. source_aligned_problem.tex is the Tier 1 source-aligned PageRank and RPPR
   reference model imported by the active paper and every note.
3. Algorithm-specific notation in Tier 2 is registered below and introduced
   only in documents that use that algorithm. Proof-local indexed quantities
   form Tier 3: their scope must be stated where they first occur, but their
   base symbols may not collide with Tier 1 or Tier 2.
4. research_commands.tex defines algorithm names and claim-status labels;
   research_note_preamble.tex supplies the common standalone-note shell.

The archived arXiv macro files are evidence only and must never be imported by
the active paper or notes.

## Reserved scientific symbols

| Symbol | Reserved meaning |
| --- | --- |
| \(G=(V,E)\), \(A,D,I,\mathcal L,Q\) | Source-aligned graph and PageRank matrices. |
| \(s\in\mathbb R_+^n\) | Unit-mass seed distribution; a single seed is \(s=e_v\). |
| \(b=\alpha D^{-1/2}s\) | PageRank right-hand side. |
| \(f\), \(g_\rho\), \(F_\rho=f+g_\rho\) | Smooth quadratic, weighted l1 regularizer, and RPPR objective. |
| \(x^0\), \(\pi=D^{1/2}x^0\) | Unregularized solution and PPR vector. |
| \(x^\star(\rho),S^\star(\rho),I^\star(\rho)\) | RPPR minimizer, support, and inactive set. |
| \(\beta\) | FISTA momentum in source-aligned comparisons. |
| \(\eta\) | FISTA/ISTA proximal-gradient step size. |
| \(q=1-\sqrt{\mu/L}=1-\sqrt{\alpha}\) | FISTA contraction factor in source-aligned comparisons. |
| \(R\) | Source FISTA iterate-distance bound; AESP run-dependent ratios explicitly map to this same role. |
| \(\varepsilon_{\rm appr},\varepsilon_{\rm obj},\varepsilon_{\rm pg},\varepsilon_{\rm ppr}\) | Distinct accuracy namespaces; no implicit conversions. |

## Registered scoped notation

| Symbol | Scope and meaning |
| --- | --- |
| \(\kappa_{\rm A}=1-2\alpha\) | AESP/Catalyst quadratic shift; never written as \(\eta\). |
| \(\beta_{\rm A}\) | AESP outer momentum; distinct from source FISTA \(\beta\). |
| \(\vartheta_{\rm A}=\alpha/(\alpha+\kappa_{\rm A})\) | Effective strong-convexity ratio for the AESP proximal subproblem. |
| \(\varpi_{\rm A}=0.9\sqrt{\vartheta_{\rm A}}\) | AESP outer geometric-decay parameter; distinct from RPPR regularization \(\rho\). |
| \(q_{\mathrm{sc}}(x)\), \(q_{\mathrm{in},t}\) | Scaled PPR gradient and an inner-loop version; bare \(q\) remains reserved for FISTA. |
| \(\xi_t=r_t(u_t)\) | Residual mass processed by APPR push \(t\). |
| \(\theta_{\mathrm{sp}}\), \(J_{\mathrm{blk}}\), \(L_{\mathrm{sp}}\) | Fixed mass fraction and proof cutoffs in the CF-Push star/spider constructions. |
| \(\sigma=r_u\), \(\tau_{\mathrm{act}}\) | Proof-local CF-Push residual amount and generic activation threshold. |
| \(\beta_{\mathrm{sp}}\) | Spider/path spectral ratio used in a conditioning proof. |
| \(\beta_{\mathrm F}\) | FISTA momentum inside the volume-gated continuation proposal. |
| \(q_{\mathrm{fc}}\) | Proof-local contraction in the changing-face Bregman obstruction. |
| \(\kappa_\rho(x)\) | A note-scoped KKT-violation vector. |
| \(R_{\mathrm{kkt},\rho}(x)\) | Scalar KKT diagnostic used by the AESP-CD proposal. |
| \(T_{\alpha,\rho}(x)\), \(R_{\mathrm{fp},\alpha,\rho}(x)=x-T_{\alpha,\rho}(x)\) | Source-aligned proximal map and note-scoped vector fixed-point residual; neither silently chooses a repository stopping rule. |
| \(\zeta_\rho\) | RPPR-to-PPR load/error vector in the volume-gated note. |
| \(\varepsilon_{\rm in},\varepsilon_{\rm kkt}\) | Explicit inner and KKT diagnostic targets. |
| \(\varepsilon_{\rm burn},\varepsilon_{\rm sol}\) | Note-scoped burn-in and solution-diagnostic targets; neither aliases a final PPR target. |
| \(\varepsilon_{\mathrm{ppr},i}\) | Instance-indexed PPR target, written with `\epspprinst{i}`. |
| \(w=D^{1/2}\mathbf1\) | Proof-scoped Perron weight in the complete RPPR note. |
| \(J_{\mathrm{path}}(\rho)\) | Proof-scoped admission radius on the path instance. |
| \(N_{\mathrm{rst}}\) | Number of certified restarts in an adaptive-work target. |

The letter \(W\) is not a shared graph matrix: normalized adjacency is always
written explicitly as \(D^{-1/2}AD^{-1/2}\). Cumulative cost uses
\(\operatorname{Work}\) or a locally indexed work quantity. The symbols
\(r_\rho\) and \(g\) are not aliases for a regularizer or gradient;
\(g_\rho\) is reserved for the shared regularizer and smooth gradients are
written \(\nabla f\) (or \(\nabla f_t\)).

Algorithm- or proof-scoped symbols may narrow these definitions or introduce
indexed local quantities only after stating their scope. They must not reuse a
reserved symbol for an incompatible role. Any new recurring symbol or LaTeX
command is added here and to the appropriate shared .tex file before use;
individual sections and note entry points do not declare commands.
