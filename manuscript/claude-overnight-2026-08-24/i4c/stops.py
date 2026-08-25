"""E6: on the star, oracle(semantic) stop vs residual(certificate) stop for SOR(w*).
Confirms the log(1/alpha) in I2-D T3 is a STOPPING-RULE artefact (cf. I4-D sec 5)."""
import math
from core import params, omega_star
print(f"{'alpha':>11s} {'eps':>9s} {'m':>5s} {'N_err':>7s} {'N_res':>7s} "
      f"{'N_err*sqa':>10s} {'N_res*sqa':>10s} {'N_res*sqa/log(1/a)':>19s}")
for e in (6, 8, 10, 12, 14, 16):
    alpha = 2.0**-e; sa = math.sqrt(alpha); om = omega_star(alpha)
    c, g = params(alpha); pic = (1+alpha)/2
    for ee in (5,):
        eps = 2.0**-ee; m = int(1/(8*eps)); tm = eps*m
        ec, EL = pic, c*pic
        Ne = Nr = None
        for N in range(1, 2_000_000):
            # residuals: r_c = e_c - c E_L ;  R_L = E_L - c e_c ; per-leaf r_l = R_L/m
            rc = ec - c*EL; RL = EL - c*ec
            if Nr is None and max(abs(rc)/m, abs(RL/m)) <= g*eps: Nr = N-1
            if Ne is None and max(abs(ec), abs(EL)) <= tm: Ne = N-1
            if Ne is not None and Nr is not None: break
            if N % 2 == 1: ec = (1-om)*ec + om*c*EL
            else:          EL = (1-om)*EL + om*c*ec
        print(f"{alpha:11.3e} {eps:9.5f} {m:5d} {Ne:7d} {Nr:7d} {Ne*sa:10.3f} "
              f"{Nr*sa:10.3f} {Nr*sa/math.log(1/alpha):19.4f}")
