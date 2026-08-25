"""Fits for I5-B: alpha-exponents of W/vol(S_eps), rounds, region, per family."""
import json, math
import numpy as np


def fit(alphas, ys):
    A = np.vstack([np.log2(alphas), np.ones(len(alphas))]).T
    q, _c = np.linalg.lstsq(A, np.log2(ys), rcond=None)[0]
    return -q          # W ~ alpha^-q -> report q  (positive = grows as a->0)


def sp3():
    rows = json.load(open("/home/claude/work/overnight/i4e/out/sp3.json"))
    fams = {}
    for r in rows:
        fams.setdefault(r["tag"].split()[0], []).append(r)
    print("family    | mech-exponent q of W/vol(S_eps)      | rounds-exp | region-exp")
    print("          |  vgf    v3    v3E   v3O              | vgf  v3 v3E| v3 (vol_S3/volSe)")
    for f, rs in fams.items():
        al = np.array([r["alpha"] for r in rs])
        vol = np.array([r["volS"] for r in rs])
        line = f"{f:9s} |"
        for m in ("vgf", "v3", "v3E", "v3O"):
            W = np.array([r[m]["W"] for r in rs])
            line += " %+0.3f" % fit(al, W / vol)
        Rv = np.array([r["vgf_R"] for r in rs], float)
        R3 = np.array([r["v3_R"] for r in rs], float)
        RE = np.array([r["v3E_R"] for r in rs], float)
        reg = np.array([r["v3_vol"] for r in rs], float) / vol
        line += " | R: %+0.2f %+0.2f %+0.2f | reg %+0.3f" % (
            fit(al, Rv), fit(al, R3), fit(al, RE), fit(al, reg))
        print(line)
        print("   rounds vgf:", [int(r["vgf_R"]) for r in rs],
              " v3:", [int(r["v3_R"]) for r in rs],
              " v3E:", [int(r["v3E_R"]) for r in rs])


def zoo():
    rows = json.load(open("/home/claude/work/overnight/i4e/out/zoo3.json"))
    fams = {}
    for r in rows:
        fams.setdefault(r["tag"].split()[0], []).append(r)
    mechs = ("push", "composed", "vgf", "v3", "v3E", "v3O")
    print("\nfamily    volSe  | We at a=2^-4/-8/-12 (v3E)        | q: push comp  vgf   v3    v3E   v3O | ok?")
    qs = {m: [] for m in mechs}
    nbad = 0
    for f, rs in fams.items():
        al = np.array([r["alpha"] for r in rs])
        vol = np.array([r["volS"] for r in rs])
        line = f"{f:9s} {vol[-1]:7.0f}|"
        We = [r["v3E"]["We"] for r in rs]
        line += "/".join("%.3g" % w for w in We) + " |"
        for m in mechs:
            W = np.array([r[m]["W"] for r in rs])
            q = fit(al, W / vol)
            qs[m].append(q)
            line += " %+0.3f" % q
        bad = sum(0 if r[m].get("ok") else 1 for r in rs for m in mechs)
        nbad += bad
        line += " | bad=%d" % bad
        print(line)
    print("MEDIAN q: " + "  ".join("%s %+0.3f" % (m, np.median(qs[m]))
                                   for m in mechs))
    print("MAX    q: " + "  ".join("%s %+0.3f" % (m, np.max(qs[m]))
                                   for m in mechs))
    print("total not-ok cells (incl. wall-capped):", nbad)
    # best-of counts and ratios vs push
    for m in ("vgf", "v3", "v3E"):
        ratios = []
        for f, rs in fams.items():
            for r in rs:
                ratios.append(r[m]["W"] / r["push"]["W"])
        ratios = np.array(ratios)
        print("%s/push: median %.3g  max %.3g  min %.3g" % (
            m, np.median(ratios), ratios.max(), ratios.min()))


if __name__ == "__main__":
    import sys
    if "zoo" in sys.argv:
        zoo()
    else:
        sp3()
        try:
            zoo()
        except Exception as e:
            print("zoo pending:", e)
