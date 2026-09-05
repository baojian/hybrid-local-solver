# Master Notation Inventory — 8 Reference Papers
*Compiled 2026-08-27 from the per-paper notes ([ACL06], [FRS+19], [MWP23], [Che+23], [ZSB+24], [HLX+25], [FM26], [WY26]) and the overview note §11. Organized: shared notation first, then convention dictionaries, then paper-specific symbols.*

---

## 0. Repository problem-statement notation (this project's canonical layer)

| Symbol | Meaning |
|---|---|
| $G=(V,E)$, $A$, $d_i$, $D$ | simple undirected unweighted graph, adjacency, degrees $>0$, degree matrix |
| $s$, $\mathrm{nnz}(s)$ | seed distribution ($1^\top s=1$), sparse; default $s=e_v$ |
| $\alpha\in(0,1]$ | teleportation parameter (lazy convention) |
| $\mathcal L = I-D^{-1/2}AD^{-1/2}$ | normalized Laplacian, $0\preceq\mathcal L\preceq 2I$ |
| $Q=\alpha I+\tfrac{1-\alpha}{2}\mathcal L$ | canonical system matrix, spectrum $[\alpha,1]$, PD M-matrix |
| $b=\alpha D^{-1/2}s$ | right-hand side |
| $x^0=Q^{-1}b$, $\pi=D^{1/2}x^0$ | source-aligned solution; PPR vector |
| $P=AD^{-1}$ | non-lazy column walk operator |
| $\varepsilon_{\mathrm{ppr}}$ | **semantic output accuracy**: $\max_i|\hat\pi_i-\pi_i|/d_i\le\varepsilon_{\mathrm{ppr}}$ |
| certificate | $\lVert D^{-1/2}(Q\hat x-b)\rVert_\infty<\alpha\varepsilon_{\mathrm{ppr}}\Rightarrow\lVert D^{-1}(\hat\pi-\pi)\rVert_\infty<\varepsilon_{\mathrm{ppr}}$ |
| $f,g_\rho,F_\rho,x^\star(\rho)$ | RPPR surrogate: $f=\tfrac12x^\top Qx-b^\top x$, $g_\rho=\alpha\rho\lVert D^{1/2}x\rVert_1$; $x^\star(\rho)\ge0$, $\mathrm{vol}(\mathrm{supp})\le1/\rho$ |
| target scale | $\widetilde O\big(1/(\sqrt\alpha\,\varepsilon_{\mathrm{ppr}})\big)$ (aspirational, open) |

## 1. Shared graph / set notation (all papers)

| Symbol | Meaning | Notes |
|---|---|---|
| $n=|V|$, $m=|E|$ | node/edge counts | sublinear access assumed |
| $\mathcal N(v)$ or $N(v)$, $j\sim i$ | neighbors | |
| $\mathrm{vol}(S)=\sum_{i\in S}d_i$ | volume; $\mathrm{vol}(V)=2m$ | **[MWP23] adds $+|S|$** (self-loop from $\alpha I$) |
| $\widetilde{\mathrm{vol}}(S)=|S|+\#E(S)=\mathrm{nnz}(Q_{S,S})$ | internal volume | [MWP23], [WY26]; $\le\mathrm{vol}(S)$, $\le|S|^2$ |
| $\widehat{\mathrm{vol}}(S)$ | edge-endpoint count | [FRS+19] only; ≠ $\widetilde{\mathrm{vol}}$! |
| $\overline{\mathrm{vol}}(S)=\min(\mathrm{vol}(S),2m-\mathrm{vol}(S))$ | in [ACL06] Thm 3 | ⚠ clashes with run-average $\overline{\mathrm{vol}}(\mathcal S_T)$ below |
| $\partial(S)$ | edge boundary [ACL06] / **vertex** boundary $\{v\notin S: N(v)\cap S\ne\emptyset\}$ [WY26] | two meanings |
| $\Phi(S)$ or $\phi(S)$ | conductance $=|\partial(S)|/\min(\mathrm{vol}(S),2m-\mathrm{vol}(S))$ | |
| $\mathrm{supp}(x)$, $\mathrm{Supp}(p)$ | support | |
| $S^\star=\mathrm{supp}(x^\star)$ | optimal support; $\mathrm{vol}(S^\star)\le1/\rho$ | [FRS+19] Thm 2 |
| $e_v$, $\chi_v$, $\mathbf 1$ | indicator / all-ones vectors | $\chi_v$ is [ACL06]'s row form |
| $I_S$, $Q_S$, $\nabla_S f$, $d_S$ | column-selection restriction operators | [FRS+19], [MWP23], [WY26] |
| $\psi_S(x)=d(x)/\mathrm{vol}(S)$ on $S$ | degree-weighted distribution | [ACL06] |

## 2. The three PPR conventions (overview §11, corrected)

| | Lazy: [FY22, FRS+19, MWP23, FM26, **HLX+25**] | Rescaled lazy: [ZSB+24] | Non-lazy: [WY26], ([Che+23] mass coords) |
|---|---|---|---|
| Walk | $W=\tfrac12(I+AD^{-1})$ | same walk | $AD^{-1}$ (Che: $P=A^\top D^{-1}$, directed OK) |
| Matrix | $Q=\alpha I+\tfrac{1-\alpha}2\mathcal L$ | $Q'=I-\tfrac{1-\alpha}{1+\alpha}D^{-1/2}AD^{-1/2}=\tfrac2{1+\alpha}Q$ | $L_\alpha=D-(1-\alpha)A$; Che: $M=I-(1-\alpha)P$ |
| System | $Qx=\alpha D^{-1/2}e_v$ | $Q'x=\tfrac{2\alpha}{1+\alpha}D^{-1/2}e_s$ | $L_\alpha x=\alpha e_s$; Che: $Mx=\alpha e_s$ |
| Spectrum | $[\alpha,1]$ ($\mu=\alpha$, $L=1$) | $[\tfrac{2\alpha}{1+\alpha},\tfrac2{1+\alpha}]$ | $\alpha D\preceq L_\alpha\preceq 2D$; Che sym.: $[\alpha,2-\alpha]$ |
| Variable | $x=D^{-1/2}\pi$ | same | $x=D^{-1}p$ (WY); $x=\pi$ (Che mass) |
| Recovery | $\pi=D^{1/2}x^\star$ | same | $p=Dx$ |
| Regularizer | $\rho\alpha\lVert D^{1/2}x\rVert_1$ | $\hat\epsilon\,\alpha\lVert D^{1/2}x\rVert_1$ | $\alpha\rho\lVert Dx\rVert_1$ (WY); none (Che) |
| Teleport map | — | same $\alpha$ | $\alpha_{\text{lazy}}=\tfrac{\alpha}{2-\alpha}$; conversely $\alpha'=\tfrac{2\alpha}{1+\alpha}$ |

*Correction retained: [HLX+25] uses the plain lazy $Q$ (identity map), not [ZSB+24]'s rescaling; only its regularizer/stop rule match the middle column. [WY26]: $D^{-1/2}L_\alpha D^{-1/2}=(2-\alpha)Q(\alpha_L)$ and $\psi(x)=(2-\alpha)F_\rho(D^{1/2}x)$.*

## 3. Accuracy / tolerance namespace (do not conflate!)

| Symbol | Meaning | Home papers |
|---|---|---|
| $\varepsilon_{\mathrm{ppr}}$ (repo) $\approx\epsilon$ | degree-normalized PPR error $\lVert D^{-1}(\hat\pi-\pi)\rVert_\infty$ | [ACL06] Lemma 5 (one-sided), [ZSB+24], [HLX+25], [WY26] |
| $\varepsilon_{\mathrm{appr}}$ = ACL's $\varepsilon$ = push tolerance | activation threshold $r(v)\ge\varepsilon d(v)$ | [ACL06], [Che+23] ($\epsilon$), [ZSB+24] |
| $\rho$ | $\ell_1$-regularization weight ≡ push tolerance ≡ inverse locality budget | [FRS+19], [FY22], [MWP23], [FM26], [WY26] |
| $\hat\epsilon$ | [ZSB+24]/[HLX+25] regularizer weight ($=\epsilon$); [FRS+19] termination slack $\epsilon^2\rho^2\alpha^2\min_j d_j/2$; [MWP23] nested-APGD tolerance | ⚠ three uses |
| $\varepsilon$ (opt.) | objective gap $F(\hat x)-F(x^\star)\le\varepsilon$ | [FY22], [MWP23], [FM26] |
| $\xi$ | additive objective error in $\psi$ | [WY26] |
| $\lambda$, $\kappa$, $\tau$ | retained residue level; expansion slack; $\tau=\min\{\rho,\xi/(2\alpha)\}$ | [WY26] (⚠ $\kappa$ ≠ condition number here) |
| $\mu$ | strong convexity $=\alpha$ (opt. papers) / SDD-solver relative accuracy $0.01\alpha\min\{\lambda,\kappa\}$ [WY26] | ⚠ two uses |
| $\kappa=L/\mu=1/\alpha$ | condition number | [MWP23], [FM26] |
| $\delta$ | failure probability [WY26]; mass excess [ACL06] Thm 2; retraction $\delta_t$ [MWP23] | ⚠ three uses |
| stop rules | $\lVert D^{-1/2}\nabla f\rVert_\infty\le\alpha\epsilon$ (lazy) $\Leftrightarrow\lVert D^{-1/2}\nabla f\rVert_\infty\le\tfrac{2\alpha\epsilon}{1+\alpha}$ (rescaled) | [ZSB+24], [HLX+25] |

## 4. Cost model notation

| Symbol | Meaning | Home |
|---|---|---|
| $\mathrm{work}_k=\mathrm{vol}(\mathrm{supp}(y_k))+\mathrm{vol}(\mathrm{supp}(x_{k+1}))$ | per-iteration degree-weighted work | [FM26] Def 3.1 |
| $T_{\mathcal A}=\sum_t\mathrm{vol}(\mathcal S_t)$ | evolving-set runtime | [ZSB+24] |
| $\overline{\mathrm{vol}}(\mathcal S_T)=\tfrac1T\sum_t\mathrm{vol}(\mathcal S_t)$ | run-average active volume | [Che+23] ($\overline{\mathrm{vol}}(\mathcal S_{1:T})$), [ZSB+24], [HLX+25] |
| $\gamma_t$, $\overline\gamma_T$ ($\bar\gamma_{1:T}$) | residual-mass concentration ratio and its run average | [Che+23], [ZSB+24], [HLX+25] |
| $\Delta_i$ | sub-epoch index (sequential vs parallel solvers) | [ZSB+24] |
| $\mathcal T$, $\mathcal T^{\mathcal M}_t$, $K_t$ | total / per-stage work, stage iteration count | [HLX+25] |
| local | total work a function of $(\rho,\alpha,\varepsilon)$ only, no $n,m$ | [FY22] |

---

## 5. [ACL06] — paper-specific

Row vectors, acting from the left. $W=\tfrac12(I+D^{-1}A)$ (lazy, row form); $\mathrm{pr}_\alpha(s)$ solves $\mathrm{pr}_\alpha(s)=\alpha s+(1-\alpha)\mathrm{pr}_\alpha(s)W$; $R_\alpha=\alpha\sum_{t\ge0}(1-\alpha)^tW^t$ (resolvent); $M=D^{-1}A$, $\alpha'=\tfrac{2\alpha}{1+\alpha}$ (non-lazy dictionary). Approximation pair $(p,r)$ with invariant $p+\mathrm{pr}_\alpha(r)=\mathrm{pr}_\alpha(s)$, i.e. $p=\mathrm{pr}_\alpha(s-r)$; `push(u)`; $s^+$ positive part. Sweep: $N_p$, ordering $p(v_j)/d(v_j)$, sweep sets $S^p_j$, $\Phi(p)=\min_j\Phi(S^p_j)$; LS curve $p[x]$ on $[0,2m]$; directed-edge sets $\mathrm{in}(S),\mathrm{out}(S)$; $p(u,v)=p(u)/d(u)$. Mixing/clustering: $\delta$ (mass excess), $\phi,\gamma,t$ (Thm 3 dichotomy), $C_\alpha\subseteq C$ (good-seed set), $\Phi_G$, $C_{\mathrm{opt}}$. PageRank-Nibble: scale $b$, $B=\lceil\log m\rceil$, ladder $\gamma_b=\tfrac5{12}(\tfrac9{10}+\tfrac1{10}\tfrac bB)$, $\alpha=\phi^2/(225\log(100\sqrt m))$, $\varepsilon\le(2^b\cdot48\lceil\log m\rceil)^{-1}$.

## 6. [FRS+19] — paper-specific

Variable $q$ ($=$ project's $x$), objective $\psi$ ($=F_\rho$), output $p=D^{1/2}q$. $f(q)=\tfrac12\langle q,Qq\rangle-\alpha\langle s,D^{-1/2}q\rangle$; general seed $s\ge0$, $\langle e,s\rangle=1$. APPR-as-coordinate-descent: residual $r=(I-(1-\alpha)W)p-\alpha s$ (note sign: $r_0=-\alpha s$; $\tilde r=-r/\alpha\ge0$ recovers ACL). Key identity: residual $=$ scaled gradient, $r=-\tfrac1\alpha D^{1/2}\nabla f(q)|$-type. Restriction operators $I_S,\nabla_Sf,Q_S,d_S$; $\widehat{\mathrm{vol}}$; termination slack $\hat\epsilon=\epsilon^2\rho^2\alpha^2\min_jd_j/2$ (Thm 3). ISTA iterates from 0: nonnegative, coordinatewise nondecreasing, $\mathrm{supp}\subseteq S^\star$.

## 7. [MWP23] — paper-specific

Abstract class: $\min_{x\ge0}g(x)=\langle x,Qx\rangle-\langle b,x\rangle$, $Q$ PD M-matrix (note: no $\tfrac12$; PageRank instantiation carries $\tfrac12$). $L,\alpha$ eigenvalue bounds, $\kappa=L/\alpha$; **good/bad** coordinates ($\in/\notin S^\star$). $\mathrm{vol}(S)=\sum d_i+|S|=\mathrm{nnz}(Q_{:,S})$; $\widetilde{\mathrm{vol}}(S)=\mathrm{nnz}(Q_{S,S})$. Certified chain $S^{(-1)}=\emptyset\subsetneq S^{(0)}\subsetneq\cdots\subseteq S^\star$; subspace optimum $x^{(\ast,t)}$ (also $x^{(\ast,C)}$ over cone $C^{(t)}$); certificate set $N=\{i:\nabla_ig<0\}$ (no false positives); slack decomposition $x=x^{(\ast,C)}-\sum\omega_ie_i$, $\omega\ge0$. Algorithms **CDPR** (conjugate directions, exact) and **ASPR** (restarted APGD); retraction $x^{(t+1)}=\max\{0,\bar x^{(t+1)}-\delta_t\mathbf 1\}$; per-stage accuracy $\hat\varepsilon_t\asymp\varepsilon\alpha^2/(L^2|S^{(t)}|)$. Headline: $\widetilde O(|S^\star|\widetilde{\mathrm{vol}}(S^\star)/\sqrt\alpha)$.

## 8. [Che+23] — paper-specific

Non-lazy, mass coordinates, directed allowed. $P=A^\top D^{-1}$ (column-stochastic, out-degrees), $M=I-(1-\alpha)P$; PPV $x=\alpha M^{-1}e_s$; symmetrized $\tilde P=D^{-1/2}AD^{-1/2}$, $y=D^{-1/2}x$, matrix $\alpha I+(1-\alpha)\mathcal L$, spectrum $[\alpha,2-\alpha]$; $\alpha_\ell=\alpha/(2-\alpha)$. FwdPush = Gauss–Seidel ("linear invariant property"); $\ell_1$ identity $\lVert x-x^\star\rVert_1=\lVert r\rVert_1$. **SOR**: relaxation $\omega\in(0,2)$, optimal $\omega^\ast=1+\big(\tfrac{1-\alpha}{1+\sqrt{1-(1-\alpha)^2}}\big)^2$, Jacobi radius $\mu_J=1-\alpha$; FwdPushSOR, PwrPushSOR. Epoch machinery: dummy marker $\ddagger$; $\mathcal S_t$ (active), $\mathcal U_t$ (inactive with $0<r<\epsilon d$), $\mathcal I_t=\mathcal S_t\cup\mathcal U_t$; $\gamma_t$, $\bar\gamma_{1:T}$, $C_{\alpha,T}$; bound $\sum_t\mathrm{vol}(\mathcal S_t)\le\tfrac{\overline{\mathrm{vol}}}{\alpha\bar\gamma}\log\tfrac C\epsilon$; comparison bounds $B_1,B_2$; heuristic FwdPush-Mean ($\bar r$ mean ratio). Momentum: $\theta$, $\beta=\tfrac{1-\theta}{1+\theta}$, three-term HB/NAG recurrences; global NAG $O(\tfrac m{\sqrt\alpha}\log(\cdot))$.

## 9. [ZSB+24] — paper-specific

Calligraphic $\mathcal G(\mathcal V,\mathcal E)$; $W=D^{-1/2}AD^{-1/2}=V\Lambda V^\top$, $\lambda_1\ge\cdots\ge\lambda_n$ (⚠ $W$ = normalized adjacency here, not lazy walk). System $Qx=b$, $Q=I-\tfrac{1-\alpha}{1+\alpha}W$, $b=\tfrac{2\alpha}{1+\alpha}D^{-1/2}e_s$; residual $r^{(t)}=b-Qx^{(t)}=-\nabla f$; degree-scaled $\tilde r^{(t)}=D^{1/2}r^{(t)}$; shorthand $\tilde\alpha=\tfrac{1-\sqrt\alpha}{1+\sqrt\alpha}$; standing $\epsilon\le1/d_s$. Active: $\tilde r_u\ge\tfrac{2\alpha}{1+\alpha}\epsilon d_u$ ($|\cdot|$ for signed methods). **Locally evolving set process**: $(\mathcal S_{t+1},x^{(t+1)},r^{(t+1)})=\Phi_\theta(\mathcal S_t,x^{(t)},r^{(t)},\mathcal A)$, $\theta=(\alpha,\epsilon,s,\mathcal G)$; locality $\mathcal S_{t+1}\subseteq\mathcal S_t\cup N(\mathcal S_t)$; FIFO with `*` epoch marker; $T_{\mathcal A}$, $\overline{\mathrm{vol}}$, $\overline\gamma_T$, $\gamma_t$ (with $\Delta_i$), $I_T=\mathrm{supp}(r^{(T)})$; $\mathcal S_{j:t}=\mathcal S_j\cap\cdots\cap\mathcal S_t$, $\overline{\mathcal S}_t=\mathcal V\setminus\mathcal S_t$; $1/\epsilon$ inequality $\overline{\mathrm{vol}}/\overline\gamma_T\le1/\epsilon$ (monotone solvers only). Solvers: LocGD, LocSOR ($\omega$; $\omega^\ast=\tfrac{2(1+\alpha)}{(1+\sqrt\alpha)^2}$), LocCH, LocHB; accelerated bound $\widetilde O\big(\overline{\mathrm{vol}}(\mathcal S_T)/((2-c)\sqrt\alpha)\big)$ conditional on geometric-mean residual decay; $\delta_{k+1:j}$ residual-reduction products.

## 10. [HLX+25] — paper-specific

Lazy $Q$ (identity to project). $\Pi_\alpha=\alpha(\tfrac{1+\alpha}2I-\tfrac{1-\alpha}2AD^{-1})^{-1}$, $\lVert\Pi_\alpha\rVert_1=1$; target set $P(\epsilon,\alpha,b,G)=\{x:\lVert D^{-1/2}(x-x^*_f)\rVert_\infty\le\epsilon\}$; (P1) unregularized, (P2) $\ell_1$ with $\hat\epsilon$. **AESP / Catalyst**: shift $\eta=1-2\alpha$ (needs $\alpha<1/2$); $\widetilde Q=Q+\eta I$, spectrum $[1-\alpha,2-2\alpha]$, condition number $2$; stage objective $h_t(z)=f(z)+\tfrac\eta2\lVert z-y^{(t-1)}\rVert^2$, $x^*_t=(Q+\eta I)^{-1}b^{(t-1)}$, $b^{(t-1)}=\alpha D^{-1/2}b+\eta y^{(t-1)}$; inner system is PPR with effective damping $\tilde\alpha=\tfrac12$; momentum $\beta=\tfrac{1-\sqrt q}{1+\sqrt q}$, $q=\mu/(\mu+\eta)=\tfrac\alpha{1-\alpha}$; tolerances $\varphi_t$ (criterion C1, set $\mathcal H_t(\varphi_t)$) converted to checkable $\epsilon_t$: $S^{(k)}_t=\{u:|\nabla_uh_t(z^{(k)}_t)|\ge\epsilon_t\sqrt{d_u}\}$; $\nabla h^{1/2}_t=D^{1/2}\nabla h_t$; $\tau=\tfrac23$ dissipation constant; stage counts $K_t$, $T_{\max}$; per-stage costs $C^0_{h_t},C^{K_t}_{h_t}$; run-dependent constant $R$ (inflation of stage initial mass). Headline $\widetilde O(\min\{m/\sqrt\alpha,\ R^2/(\sqrt\alpha\,\epsilon^2)\})$.

## 11. [FM26] — paper-specific

Project convention verbatim. FISTA: $\eta=1$, $\beta=\tfrac{1-\sqrt\alpha}{1+\sqrt\alpha}$, extrapolation $y_k$, prox = weighted soft-threshold at $\eta\alpha\rho\sqrt{d_i}$. Absolute constants: $\Delta_0=F_\rho(0)-F_\rho(x^\star)\le\alpha/2$; rate $q=1-\sqrt\alpha$; path constant $M\le20$, $\lVert y_k-x^\star\rVert_2\le\sqrt{20}$. KKT margin $\gamma_i=(\lambda_i-|\nabla_if(x^\star)|)/\sqrt{d_i}$, threshold levels $\lambda_i$; breakpoint $\rho_0$ (star/path counterexamples). **Over-regularization (A/B)**: run on $F_{2\rho}$ ($g_B=2\alpha\rho\lVert D^{1/2}x\rVert_1$); $S_A=\mathrm{supp}(x^\star(\rho))$, $S_B=\mathrm{supp}(x^\star(2\rho))\subseteq S_A$, $I_B=[n]\setminus S_B$; margin $\gamma^{(B)}_i\ge\rho\alpha$ outside $S_A$ (Lem 4.2, via $I_B^{\mathrm{small}}$); forward map $u(x)=x-\eta\nabla f(x)$; spurious sets $A(y)$, $\widetilde A_k=\mathrm{supp}(x_{k+1})\cap S_A^c$; confinement set $B$ ($\widetilde A_k\subseteq B$; $B'=\{i\in B:\gamma^{(B)}_i\ge\rho\alpha\}$; Thm 4.4: $B=\partial S$). Bounds: $\Omega(m)$ worst-case FISTA; conditional $O\big(\tfrac1{\rho\sqrt\alpha}\log\tfrac\alpha\varepsilon+\tfrac{\sqrt{\mathrm{vol}(B)}}{\rho\alpha^{3/2}}\big)$; never-activate degree threshold $d_i\ge20\alpha^{-2}\rho^{-2}$.

## 12. [WY26] — paper-specific

Non-lazy $L_\alpha=D-(1-\alpha)A$; $\mathrm{pr}_\alpha(s)$ with walk $AD^{-1}$; lazy map $\alpha_L=\alpha/(2-\alpha)$. ACL $\epsilon$-approx as **witness pair** $p=\mathrm{pr}_\alpha(e_s-r)$, $0\le r\le\epsilon d$. Objective $\psi(x)=\tfrac12x^\top L_\alpha x-\alpha e_s^\top x+\alpha\rho\lVert Dx\rVert_1$; $\xi$-additive accuracy. **Residue map** $r(x)=e_s-\tfrac1\alpha L_\alpha x$; mass identity $\mathbf 1^\top Dx+\mathbf 1^\top r(x)=1$; boundary formula on $\partial S$ (vertex boundary); subgradient $\nabla\psi=\alpha(\rho d-r(x))$. Restricted matrix $L_{\alpha,S}=D_S-(1-\alpha)A_S$ (full degrees on diagonal), SDD M-matrix, $\alpha D_S\preceq L_{\alpha,S}\preceq2D_S$. Algorithm state: active set $S$ (grown from $\{s\}$), restricted solve $L_{\alpha,S}x_S=\alpha(e_s|_S-\lambda d_S)$; retained residue level $\lambda$ ($=0.5\epsilon$ PPR; $=\rho$ for $\ell_1$), expansion slack $\kappa$ ($=0.5\epsilon$; $=\tau=\min\{\rho,\xi/(2\alpha)\}$), activation above $(\lambda+\kappa)d$; SDD solver accuracy $\mu=0.01\alpha\min\{\lambda,\kappa\}$ (energy norm), failure prob. $\delta$. Headlines: $\widetilde O(1/\epsilon^2)$ PPR; $\widetilde O(|S^\star|\,\mathrm{vol}(S^\star))\le\widetilde O(1/\rho^2)$ for $\ell_1$.

---

## 13. Symbol-collision watchlist (highest-risk overloads)

1. **$\varepsilon/\epsilon$** — at least five meanings (ACL push tolerance, opt. gap, PPR error, [FRS+19] slack, [HLX+25] inner $\epsilon_t$). Always namespace: $\varepsilon_{\mathrm{appr}},\varepsilon_{\mathrm{ppr}},\varepsilon_{\mathrm{obj}}$.
2. **$W$** — lazy walk ([ACL06], overview) vs. normalized adjacency ([ZSB+24]).
3. **$Q$** — three scalings (lazy, rescaled $\tfrac2{1+\alpha}Q$, and Che's $(2-\alpha)Q(\alpha_\ell)$); [WY26] uses $L_\alpha$ instead.
4. **$\alpha$** — same letter, different walks; conversions $\alpha'=\tfrac{2\alpha}{1+\alpha}$, $\alpha_L=\tfrac\alpha{2-\alpha}$, $\alpha_\ell=\tfrac\alpha{2-\alpha}$.
5. **$x$** — normalized variable $D^{-1/2}\pi$ (lazy papers), mass $\pi$ ([Che+23]), degree-normalized reserve $D^{-1}p$ ([WY26]).
6. **$r$** — nonnegative ACL residual vs. signed $b-Qx=-\nabla f$ ([FRS+19]: $r_0=-\alpha s$!); scaled versions $\tilde r$.
7. **$\kappa$** — condition number ([MWP23], [FM26]) vs. residue slack ([WY26]).
8. **$\mu$** — strong convexity vs. SDD solver accuracy ([WY26]) vs. Jacobi radius $\mu_J$ ([Che+23]).
9. **$\delta$** — mass excess ([ACL06]) vs. retraction ([MWP23]) vs. failure probability ([WY26]).
10. **$\overline{\mathrm{vol}}$** — $\min$-volume ([ACL06]) vs. run-average ([Che+23], [ZSB+24], [HLX+25]).
11. **$B$** — Nibble scale bound ([ACL06]) vs. confinement set ([FM26]).
12. **$\beta$** — momentum ([FM26], [HLX+25], [Che+23]) — different formulas ($\tfrac{1-\sqrt\alpha}{1+\sqrt\alpha}$ vs. $\tfrac{1-\sqrt q}{1+\sqrt q}$ vs. $\tfrac{1-\theta}{1+\theta}$).
13. **$\mathrm{vol}$** — with/without $+|S|$ ([MWP23]); vs. $\widetilde{\mathrm{vol}}$ vs. $\widehat{\mathrm{vol}}$.
14. **$\partial S$** — edge boundary ([ACL06]) vs. vertex boundary ([WY26], [FM26]'s confinement).
15. **$\hat\epsilon$** — regularizer weight ([ZSB+24]/[HLX+25]) vs. termination slack ([FRS+19]) vs. nested tolerance ([MWP23]).
