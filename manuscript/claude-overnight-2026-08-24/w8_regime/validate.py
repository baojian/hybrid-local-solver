"""Validation: (1) C push == lib appr_lazy (identical W, p to 1e-12);
(2) push one-sided semantic error <= eps; (3) WY certificate correctness
and one-sidedness vs exact solve; (4) two-sided vs one-sided certificate
gap for push (shows the one-sided bound is what does the work)."""
import sys
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "lib"))
from model import Model, appr_lazy   # noqa: E402
from meter import Meter              # noqa: E402
import contenders as C               # noqa: E402

cases = []
for name in ["star", "spider", "caterpillar", "btree", "grid"]:
    for alpha in [2**-2, 2**-6, 2**-10]:
        for eps in [2**-3, 2**-5, 2**-7]:
            if 1.0 / (alpha * eps) <= 2**18:
                cases.append((name, alpha, eps))

print(f"{len(cases)} validation cells")
max_pdiff = 0.0
w_mismatch = 0
max_err_ratio_push = 0.0
max_err_ratio_wy = 0.0
min_onesided_push = 0.0
min_onesided_wy = 0.0
cert_gap = []
for name, alpha, eps in cases:
    (kind, args), n_est, m_edges = C.family_params(name, alpha, eps)
    adj, seed = C.build_graph(kind, args)
    model = Model(adj, alpha, seed)
    x0 = model.solve_exact()
    pi0 = model.sqd * x0

    # lib push with Meter
    met = Meter(adj)
    p_lib, r_lib = appr_lazy(adj, alpha, seed, eps, meter=met)
    W_lib = met.C_adj + met.R_adj
    # C push
    res = C.push_c(model, eps, seed)
    if res["W"] != W_lib:
        w_mismatch += 1
        print(f"  W MISMATCH {name} a={alpha} e={eps}: C={res['W']} lib={W_lib}")
    max_pdiff = max(max_pdiff, float(np.max(np.abs(res["p"] - np.array(p_lib)))))

    err_push = float(np.max(np.abs(res["p"] - pi0) / model.d))
    max_err_ratio_push = max(max_err_ratio_push, err_push / eps)
    min_onesided_push = min(min_onesided_push, float(np.min(pi0 - res["p"])))
    # two-sided certificate value (the eps it would certify = cert/alpha)
    x_push = res["p"] / model.sqd
    cert2 = model.cert_resid(x_push) / alpha
    cert_gap.append(cert2 / max(err_push, 1e-300))

    wy = C.wy_active_set(model, eps, seed, x0=x0)
    err_wy = model.semantic_err(wy["x"], x0)
    max_err_ratio_wy = max(max_err_ratio_wy, err_wy / eps)
    min_onesided_wy = min(min_onesided_wy, float(np.min(x0 - wy["x"])))
    n_tighten_total = globals().setdefault("_NT", [0])
    n_tighten_total[0] += wy["tightenings"]
    assert wy["status"] == "ok"
    assert err_wy <= eps * (1 + 1e-9), (name, alpha, eps, err_wy / eps)
    assert err_push <= eps * (1 + 1e-9), (name, alpha, eps, err_push / eps)

print(f"W mismatches C-vs-lib: {w_mismatch}")
print(f"max |p_C - p_lib|: {max_pdiff:.2e}")
print(f"push: max err/eps = {max_err_ratio_push:.4f}  "
      f"(one-sided min(pi0-p) = {min_onesided_push:.2e})")
print(f"WY:   max err/eps = {max_err_ratio_wy:.4f}  "
      f"(one-sided min(x0-x) = {min_onesided_wy:.2e})")
cg = np.array(cert_gap)
print(f"push two-sided cert eps / actual err: median {np.median(cg):.1f}, "
      f"max {cg.max():.1f}  (>1 => one-sided bound is the sharp one)")
print(f"WY adaptive tightenings total: {globals().get('_NT', [0])[0]}")
print("VALIDATION OK" if w_mismatch == 0 and max_err_ratio_push <= 1 + 1e-9
      and max_err_ratio_wy <= 1 + 1e-9 else "VALIDATION ISSUES")
