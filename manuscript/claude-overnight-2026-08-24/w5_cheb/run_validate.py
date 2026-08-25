"""Phase 0: validate untruncated Chebyshev + the error-propagation identity."""
import sys
import math
import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/w5_cheb")
sys.path.insert(0, "/home/claude/work/overnight/lib")
from cheb import consts, cheb_sweep, VecMeter, measure_amp, A_bar  # noqa
from model import Model  # noqa
import zoo  # noqa

np.set_printoptions(precision=3)

# --- 1. rate check on a path ---
adj, seed = zoo.path(300)
for alpha in (2 ** -4, 2 ** -8):
    mod = Model(adj, alpha, seed)
    x0 = mod.solve_exact()
    theta, delta, sigma, lam = consts(alpha)
    m = VecMeter(mod)
    out = cheb_sweep(mod, 1e-10, mode="none", stop="K", K_max=120, meter=m,
                     record=True)
    # rerun capturing err trajectory
    errs = []
    x_prev = np.zeros(mod.n)
    r0 = mod.b - mod.Q @ x_prev
    x = x_prev + r0 / theta
    t_prev, t_cur, ucoef = 1.0, sigma, 1.0 / sigma
    e0 = float(np.linalg.norm(-x0))
    for k in range(1, 100):
        errs.append(float(np.linalg.norm(x - x0)))
        r = mod.b - mod.Q @ x
        ucoef = 1.0 / (2.0 * sigma - ucoef)
        rho = 2.0 * sigma * ucoef
        x, x_prev = rho * (x + r / theta) + (1.0 - rho) * x_prev, x
        t_prev, t_cur = t_cur, 2.0 * sigma * t_cur - t_prev
    ks = [10, 30, 60, 90]
    print(f"alpha=2^{int(math.log2(alpha))} lam_cheb={lam:.5f}")
    for k in ks:
        bound = 2 * lam ** k * e0
        tk = math.cosh(k * math.acosh(sigma))
        print(f"  k={k:3d} ||e_k||2={errs[k-1]:.3e}  (1/t_k)||e0||="
              f"{e0/tk:.3e}  ratio={errs[k-1]*tk/e0:.3f}")

# --- 2. propagation identity check: injected perturbation vs U-poly formula ---
alpha = 2 ** -6
mod = Model(adj, alpha, seed)
theta, delta, sigma, lam = consts(alpha)
K = 60
k0 = 25
i_site = 40
d = 1e-6
# run A: plain; run B: perturb y_{k0} by -d*e_i; diff at K vs formula
def run(perturb):
    x_prev = np.zeros(mod.n)
    x = mod.b / theta
    ucoef = 1.0 / sigma
    for k in range(1, K):
        if perturb and k == k0:
            x = x.copy()
            x[i_site] -= d
        r = mod.b - mod.Q @ x
        ucoef = 1.0 / (2.0 * sigma - ucoef)
        rho = 2.0 * sigma * ucoef
        x, x_prev = rho * (x + r / theta) + (1.0 - rho) * x_prev, x
    return x

diff = run(False) - run(True)   # should equal d * (t_k0/t_K) U_{K-k0}(M) e_i
# formula via dense eigendecomposition
Qd = mod.Q.toarray()
w, V = np.linalg.eigh(Qd)
mu = (theta - w) / delta
mrem = K - k0
U = np.zeros_like(mu)
Um1, Um0 = 0.0 * mu, np.ones_like(mu)
for j in range(mrem):
    Um1, Um0 = Um0, 2 * mu * Um0 - Um1
U = Um0  # U_mrem with U_0=1
t = [1.0, sigma]
for k in range(1, K + 1):
    t.append(2 * sigma * t[-1] - t[-2])
e = np.zeros(mod.n)
e[i_site] = 1.0
pred = d * (t[k0] / t[K]) * (V @ (U * (V.T @ e)))
print(f"identity check: ||diff - pred||/||pred| = "
      f"{np.linalg.norm(diff-pred)/np.linalg.norm(pred):.2e}  "
      f"(||pred||={np.linalg.norm(pred):.3e})")
env = (t[k0] / t[K]) * (mrem + 1)
print(f"measured A2 = {np.linalg.norm(diff)/d:.4f}  envelope={env:.4f}  "
      f"A_bar={A_bar(alpha):.3f}")

# --- 3. ledger-certified sweep sanity on path ---
for alpha in (2 ** -6, 2 ** -10):
    mod = Model(adj, alpha, seed)
    x0 = mod.solve_exact()
    for eps in (1e-2, 1e-3):
        m = VecMeter(mod)
        out = cheb_sweep(mod, eps, mode="cert", stop="ledger", meter=m)
        err = mod.semantic_err(out["x"], x0)
        cr = mod.cert_resid(out["x"])
        print(f"a=2^{int(math.log2(alpha))} eps={eps:g} status={out['status']}"
              f" k={out['k']} err/eps={err/eps:.3g} cert/(a*eps)="
              f"{cr/(alpha*eps):.3g} W_scan={m.scan_work():.0f} "
              f"ntrunc={out['n_trunc']}")
