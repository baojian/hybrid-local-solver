"""I5-F E1: soundness battery for lib/cert.py + E2: the radius question."""
import json, math, sys
import numpy as np
sys.path.insert(0, "/home/claude/work/overnight/lib")
sys.path.insert(0, "/home/claude/work/overnight/i3a_amg")
sys.path.insert(0, "/home/claude/work/overnight/i4f")
import zoo, cert
from amglib import GModel
import core  # i4f iterate producers

OUT = "/home/claude/work/overnight/i5f/out"
import os; os.makedirs(OUT, exist_ok=True)


def fam_models(alpha):
    out = {}
    for name, (adj, seed) in dict(
        path=zoo.path(4000, seed_end=False),
        spider=zoo.spider(6, 700),
        caterpillar=zoo.caterpillar(1800, 1),
        grid2d=zoo.grid(101, 101),
        rand_reg3=zoo.random_regular(2000, 3),
        star=zoo.star(2000),
        decoy_hub=zoo.decoy_hub(600, 200),
    ).items():
        if name == "grid2d":
            seed = 50 * 101 + 50
        out[name] = GModel(adj, alpha, seed)
    return out


def iterates(m):
    """A spread of iterate types: region solves (2 radii), push, chebyshev,
    zero, and a noise-contaminated region solve (signed residual)."""
    sh, dist = core.bfs_shells(m)
    x0 = m.solve_exact()
    pid = x0 / m.sqd
    idx = np.flatnonzero(pid >= 1e-6)
    Rsem = int(dist[idx].max()) if idx.size else 1
    its = {}
    for f, lab in ((0.4, "ball40"), (0.75, "ball75")):
        R = max(1, int(Rsem * f))
        S = np.flatnonzero((dist >= 0) & (dist <= R))
        its[lab] = core.xh_restricted(m, S) / m.sqd
    p, r, _ = core.push_run(m, 1e-5)
    its["push"] = p / m.sqd / m.sqd * m.sqd  # pi scale -> x scale: x = pi/sqd
    its["push"] = p / m.sqd
    its["cheb"] = core.cheb_iterate(m, max(4, int(1.5 / math.sqrt(m.alpha)))) / m.sqd
    its["zero"] = np.zeros(m.n)
    rng = np.random.default_rng(3)
    xb = its["ball75"].copy()
    nz = np.flatnonzero(xb)
    xb[nz] *= (1 + 1e-3 * rng.standard_normal(nz.size))
    its["noisy"] = xb
    return its


def e1_soundness():
    rows = []
    for alpha in (2**-2, 2**-4, 2**-6, 2**-8):
        for fname, m in fam_models(alpha).items():
            x0 = m.solve_exact()
            for iname, xh in iterates(m).items():
                for ext in ("pessimistic", "sc"):
                    for om in ("ball", "multiscale"):
                        o = cert.certify_eprime(m, xh, exterior=ext, omega=om)
                        err = cert.assert_sound(
                            m, xh, o, x0,
                            tag=f"{fname}/{iname}/{ext}/{om}/a={alpha}")
                        rows.append(dict(
                            fam=fname, it=iname, ext=ext, om=om, alpha=alpha,
                            err=err, bound=o["err_bound"],
                            tier0=o["err_tier0"], K=o["K"],
                            volO=o["volOmega"], cost=o["cost"]["total"],
                            tight=o["err_bound"] / max(err, 1e-300),
                            t0_over=o["err_tier0"] / max(err, 1e-300)))
        print(f"alpha={alpha}: checks so far {cert.SOUND_CHECKS}, "
              f"violations {len(cert.VIOLATIONS)}", flush=True)
    json.dump(rows, open(f"{OUT}/sound.json", "w"))
    tt = np.array([r["tight"] for r in rows])
    print(f"E1 done: {cert.SOUND_CHECKS} checks, {len(cert.VIOLATIONS)} "
          f"violations; tightness bound/err: median {np.median(tt):.2f} "
          f"p90 {np.percentile(tt, 90):.2f} max {tt.max():.2f}")


# ---------------------------------------------------------- E2: radius -----
def green_center(m, v):
    """G = (I-cP)^-1 psi at v with psi = point profile from x_hat = 0."""
    import scipy.sparse as sp, scipy.sparse.linalg as spla
    c, ga = cert.push_consts(m.alpha)
    K = (sp.diags(m.d) - c * m.A).tocsc()
    rhs = np.zeros(m.n); rhs[v] = ga  # d_v * psi_v = |r_v| = ga
    return spla.spsolve(K, rhs)


def e2_radius():
    res = dict(lower=[], upper=[])
    print("\n-- E2a LOWER: cycle adversary (indistinguishable from path on "
          "B_K; frontier degrees equal) --")
    for alpha in (2**-4, 2**-6, 2**-8, 2**-10, 2**-12):
        sa = math.sqrt(alpha)
        lam = (1 - sa) / (1 + sa)
        # true err of x_hat=0 on a long path (proxy for infinite)
        N = min(120000, int(80 / sa))
        mp = GModel(zoo.path(N, seed_end=False)[0], alpha, N // 2)
        Gp = green_center(mp, N // 2)
        errp = float(Gp[N // 2])
        Kmin_meas = None
        rows = []
        for Kb in sorted(set(
                [max(1, int(x / sa)) for x in
                 (0.05, 0.1, 0.2, 0.27, 0.35, 0.5, 0.75, 1.0, 1.5)])):
            L = 2 * Kb + 4
            mc = GModel(zoo.cycle(L)[0], alpha, 0)
            Gc = green_center(mc, 0)
            ratio = float(Gc[0]) / errp
            pred = (1 + lam ** L) / (1 - lam ** L)
            rows.append((Kb, ratio, pred))
            if ratio <= 2.0 and Kmin_meas is None:
                Kmin_meas = Kb
        Kpred = math.log(3.0) / (4 * math.atanh(sa)) - 2
        res["lower"].append(dict(alpha=alpha, rows=rows, Kmin=Kmin_meas,
                                 Kpred=Kpred))
        print(f"a=2^{int(math.log2(alpha))}: K_min(C=2) measured "
              f"{Kmin_meas} vs pred ln3/(4 artanh sqrt(a))-2 = {Kpred:.1f}; "
              f"K_min*sqrt(a) = {(Kmin_meas or 0) * sa:.3f}; "
              f"formula err {max(abs(r / p - 1) for _, r, p in rows):.1e}")

    print("\n-- E2b UPPER: K needed by (e') for tightness 2 on the path: "
          "pessimistic vs self-consistent exterior --")
    for alpha in (2**-4, 2**-6, 2**-8, 2**-10, 2**-12):
        sa = math.sqrt(alpha)
        N = min(160000, int(100 / sa))
        m = GModel(zoo.path(N, seed_end=False)[0], alpha, N // 2)
        xh = np.zeros(m.n)
        x0 = m.solve_exact() if m.n <= 30000 else None
        Gp = green_center(m, N // 2)
        err = float(Gp[N // 2])
        row = dict(alpha=alpha)
        for ext in ("pessimistic", "sc"):
            Kst = None
            for Kb in sorted(set([max(1, int(x / sa)) for x in
                                  (0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0,
                                   2.5, 3.0, 4.0)])):
                o = cert.certify_eprime(m, xh, K=Kb, exterior=ext)
                if x0 is not None:
                    cert.assert_sound(m, xh, o, x0, tag=f"e2b/{ext}/{alpha}")
                if o["err_bound"] <= 2 * err:
                    Kst = Kb
                    break
            row[ext] = Kst
            row[ext + "_x_sqrta"] = None if Kst is None else Kst * sa
        res["upper"].append(row)
        print(f"a=2^{int(math.log2(alpha))}: K*(pess) = {row['pessimistic']}"
              f" ({row['pessimistic_x_sqrta']:.2f}/sqrt a), K*(sc) = "
              f"{row['sc']} ({row['sc_x_sqrta']:.2f}/sqrt a)")
    json.dump(res, open(f"{OUT}/radius.json", "w"))


def e3_adaptive():
    print("\n-- E3: adaptive/multiscale Omega on decaying residuals --")
    rows = []
    for alpha in (2**-6, 2**-8):
        for fname in ("path", "grid2d"):
            m = fam_models(alpha)[fname]
            x0 = m.solve_exact()
            # rapidly decaying residual: a few push steps leave r ~ geometric
            p, r, _ = core.push_run(m, 3e-4)
            xh = p / m.sqd
            o_b = cert.certify_eprime(m, xh, exterior="sc", omega="ball")
            o_m = cert.certify_eprime(m, xh, exterior="sc", omega="multiscale")
            eb = cert.assert_sound(m, xh, o_b, x0, tag=f"e3b/{fname}")
            em = cert.assert_sound(m, xh, o_m, x0, tag=f"e3m/{fname}")
            rows.append(dict(alpha=alpha, fam=fname,
                             vol_ball=o_b["volOmega"], vol_ms=o_m["volOmega"],
                             tb=o_b["err_bound"] / eb,
                             tm=o_m["err_bound"] / em))
            print(f"a=2^{int(math.log2(alpha))} {fname}: vol(ball) "
                  f"{o_b['volOmega']:.0f} vs vol(multiscale) "
                  f"{o_m['volOmega']:.0f} ({o_m['volOmega']/o_b['volOmega']:.2f}x)"
                  f"; tightness {o_b['err_bound']/eb:.2f} -> "
                  f"{o_m['err_bound']/em:.2f}")
    json.dump(rows, open(f"{OUT}/adaptive.json", "w"))


if __name__ == "__main__":
    e1_soundness()
    e2_radius()
    e3_adaptive()
    print(f"\nTOTAL soundness checks {cert.SOUND_CHECKS}, violations "
          f"{len(cert.VIOLATIONS)}: {cert.VIOLATIONS[:5]}")
