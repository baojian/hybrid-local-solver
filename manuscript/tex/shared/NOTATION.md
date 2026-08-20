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
| \(\lambda_\alpha=(1-\sqrt\alpha)/(1+\sqrt\alpha)\) | Optimal-SOR reflection factor in the delayed-reflection ladder note. |
| \(b_{\rm self}(\alpha)=\lambda_\alpha^{-2}\), \(b_{\rm next}(\alpha)=\lambda_\alpha^{-1}\) | Alpha-scaled ladder bases for current- and next-rung self-reactivation control. |
| \(\varphi,h\) | Fresh residual and delayed reflection-debt components in the split-residual note, with \(r=\varphi+h\). |
| \(\mathcal M(r)=\sum_i\sqrt{d_i}|r_i|\) | Note-scoped weighted absolute residual mass for exact-rung cleanup. |
| \(B\), \(B_{\mathrm{edge}}\) | Band factor in the direct two-rung note and its universal one-edge settlement ceiling; lowercase \(b\) remains the PageRank right-hand side. |
| \(c_u=1+d_u\) | Per-operation service charge in the direct two-rung note; the shared adjacency-scan work remains \(d_u\). |
| \(p_u(r)\), \(h_u(r)\) | Empirical rank key and exact objective-decrease-per-charge score in the direct two-rung note. |
| \(\chi_{\mathrm{set}}(r;\mathcal O)\) | Trajectory-specific exact-rung settlement factor in the direct two-rung note. |
| \(\ell,\ell_\rho,\mathcal E_U^\ell\) | Note-scoped fixed loads and exact Dirichlet settlement map in the propagate--settle framework. |
| \(\operatorname{cvol}(U),\mathfrak R_{\rm set}\) | Empirical-charge volume and cumulative settled-volume revisit factor in the propagate--settle framework. |
| \(\mathcal F_m,\vartheta_0,\psi_d(\vartheta)\) | Tailed-fan obstruction, its critical gate scaling, and limiting degree-\(d\) shifted demand in the propagate--settle framework. |
| \(\tau(v),\eta_d^{(j)}\) | Activation time in a nested settled trace and the live degree-\(d\) fan-boundary violation demand in the propagate--settle framework. |
| \(\varrho_{\rm rev}\) | Charge-weighted mean paid-visit multiplicity in the adaptive-revisit note. |
| \(\mathsf{Rev}_{a\to b}\), \(a,b\in\{\mathrm e,\mathrm s\}\) | Note-scoped causal revisit charge, classified by previous and current exact/spreading modes. |
| \(\mu_k,\overline\mu\) | Within-epoch charged-work multiplier and its settled-volume-weighted mean in the adaptive-revisit factorization. |
| \(\mathsf{Bank}_t(\Gamma)=\Gamma C(S_t)-W_t\) | Online adaptive-revisit work slack for declared factor \(\Gamma\). |
| \(x[U],\mathcal B(U)\) | Canonical shifted RPPR settlement on region \(U\) and its exact boundary-violation set in the adaptive-revisit note. |
| \(\Phi_j\), \(\Phi_{\rm en}\), \(\Phi_{\rm path}\) | Work-valued mergeable policy countdown, its common energy-based safety instance, and its endpoint-path activation-token instance in the adaptive-revisit note. |
| \(f_i,b_i\) (adaptive-revisit note only) | Forward Schur-record and reverse-recovery tokens for the endpoint-path mergeable countdown; these local token labels are unrelated to the shared PageRank load \(b\). |
| \(\mathcal E(\widehat x)=f(\widehat x)-f(x^0)\) | Note-scoped unregularized quadratic error energy for adaptive-relaxation safety. |
| \(\mathsf V_{\rm loc}(I)\) | Placeholder for an explicitly defined instance-local degree-volume ledger in an accelerated policy-arm theorem; never the vertex set \(V\). |
| \(y^0=D^{-1/2}x^0=D^{-1}\pi\), \(U_\tau^0=\{i:y_i^0>\tau\}\) | Degree-normalized exact PPR potential and its exact superlevel core in the volume-gated and local-oracle notes. |
| \(H_\alpha=D^{1/2}QD^{1/2}=\alpha D+(1-\alpha)(D-A)/2\) | Note-scoped killed degree-form PageRank matrix used for capacity and Green-function arguments. |
| \(\operatorname{cap}_\alpha(v)\) | Killed seed capacity in the local-solver oracle hierarchy note; defined variationally from \(H_\alpha\). |

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
