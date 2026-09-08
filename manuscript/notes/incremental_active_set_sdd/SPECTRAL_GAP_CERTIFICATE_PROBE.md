# A computable nongrounded VWF gap certificate

**Completed in block 12.** The spectral residual certificate, computable stopping rules and upward rounding are proved in `sections/op3_spectral_vwf_certificate.tex`. The generic audit passes 1,440 mixed and 240 exact-tree certificates. The independently implemented certified nested variant passes three full profiles. See the morning synthesis and durable audit JSON files. The older proposal below records the starting question.

Block 12 candidate, 8 September 2026. **Conditional until formalized and
audited.** The fixed-length genuinely nested audit is running separately;
do not edit its source while it runs or repeat that audit without a reason.

For any feasible state a of Phi=.5*x'G*x+sum f_i(x_i), form its residual

    R_G(z)=Phi(a+z)-Phi(a)=.5*z'G*z+h_a(z), h_a(0)=0,
    R_H(z)=.5*z'H*z+h_a(z), G<=H<=kappa*G.

The shifted domain contains zero, and h_a is convex. Consequently

    R_G(z)<=R_H(z),
    R_H(z/kappa)<=R_G(z)/kappa.

Taking minima gives kappa*R_H*<=R_G*<=R_H*<=0. If a supplied oracle
returns q with R_H(q)<=R_H*/beta+xi, beta>=1,xi>=0, then

    C = kappa*beta*(xi-R_H(q))
    gap(a) <= C <= kappa*beta*(gap(a)+xi).

C is nonnegative and computable. It does not need positive grounding,
known optimum, nonzero initial gap or a coordinate box. A complete sparse
residual construction, oracle call and energy evaluation are charged.
Exact tree elimination gives beta=1,xi=0 when H is a supplied tree.
The spectral comparison is a short independent proof; do not claim this
standard comparison idea is novel.

For desired absolute gap t, use xi<=t/(2*kappa*beta). If the actual gap
is at most t/(2*kappa*beta), C<=t, so a guarded convergence driver has an
explicit stopping target. For Phi(0)<=0, the check

    Phi(a)+C <= 2*eta

certifies Phi(a)<=Phi*/2+eta. This can stop the coarse accelerated oracle
before its fixed worst-case iteration count without using the dense
reference optimum. For a normalized model with desired relative delta
and additive zeta, it also suffices that C<=zeta; the resulting absolute
guarantee implies the mixed one because the model optimum is nonpositive.

Audit signed endpoints, zero gap, positive objective states, non-edgewise
spectral order, positive additive oracle errors, threshold ties, and exact
tree certificates. Keep dense minima only in the validator. A follow-up
coarse APG wrapper may query this certificate using one extra tree solve
at each candidate, paying all residual/curve work and returning only after
the displayed computable stopping condition passes. Do not silently change
the pending fixed-length nested audit to use a dense-optimum stopping rule.
