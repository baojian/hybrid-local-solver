"""I3-A analysis: per-family tables, alpha-exponents, setup/solve split."""
import json
import math
import sys

import numpy as np

OUT = "/home/claude/work/overnight/i3a_amg/out"


def load(tags):
    rows = []
    for t in tags:
        try:
            rows += json.load(open(f"{OUT}/zoo_{t}.json"))
        except Exception:
            pass
    return [r for r in rows if r.get("amg") and r.get("volS", 0) > 0]


def wv(r, key):
    d = r.get(key)
    if not d or d.get("W") is None:
        return float("nan")
    return d["W"] / r["volS"]


def slope(xs, ys):
    """least squares slope of log y vs log(1/x)."""
    xs = np.array(xs, float)
    ys = np.array(ys, float)
    m = np.isfinite(ys) & (ys > 0)
    if m.sum() < 2:
        return float("nan")
    lx = np.log(1.0 / xs[m])
    ly = np.log(ys[m])
    A = np.vstack([lx, np.ones_like(lx)]).T
    return float(np.linalg.lstsq(A, ly, rcond=None)[0][0])


def main():
    tags = sys.argv[1].split(",") if len(sys.argv) > 1 else ["main", "g3d"]
    rows = load(tags)
    fams = []
    for r in rows:
        if r["fam"] not in fams:
            fams.append(r["fam"])

    print("\n=== TABLE 1: W / vol(S_eps) ===")
    hdr = (f"{'family':13s} {'a':>6s} {'eps':>6s} {'volS':>9s} {'vOm/vS':>7s} "
           f"{'AMG':>9s} {'AMGorc':>8s} {'push':>10s} {'cheb':>9s} "
           f"{'direct':>9s} {'set%':>5s} {'rate':>6s} {'opcx':>5s} "
           f"{'cyc':>4s} {'e/eps':>6s}")
    print(hdr)
    for f in fams:
        for r in [x for x in rows if x["fam"] == f]:
            A = r["amg"]
            print(f"{f:13s} 2^{int(round(math.log2(r['alpha']))):>4d} "
                  f"{r['eps']:>6.0e} {r['volS']:>9.0f} "
                  f"{A['volOmega']/r['volS']:>7.2f} "
                  f"{wv(r,'amg'):>9.1f} {wv(r,'amg_oracle'):>8.1f} "
                  f"{wv(r,'push'):>10.1f} {wv(r,'cheb'):>9.1f} "
                  f"{wv(r,'direct'):>9.1f} "
                  f"{100*A['setup']/A['W']:>5.0f} "
                  f"{(A.get('allrate') or float('nan')):>6.3f} "
                  f"{(A.get('opcx') or float('nan')):>5.2f} "
                  f"{A.get('tot_cycles') or 0:>4d} "
                  f"{A['err_eps']:>6.3f}"
                  + ("  MAXED" if A["status"] != "cert" else ""))

    print("\n=== TABLE 2: alpha-exponent s of  W/vol(S) ~ C * alpha^-s ===")
    print(f"{'family':13s} {'eps':>7s} {'AMG':>7s} {'AMGorc':>7s} "
          f"{'push':>7s} {'cheb':>7s} {'direct':>7s} {'vOm/vS':>7s}")
    for f in fams:
        for e in sorted({r["eps"] for r in rows if r["fam"] == f}):
            sub = sorted([r for r in rows if r["fam"] == f and r["eps"] == e],
                         key=lambda r: -r["alpha"])
            al = [r["alpha"] for r in sub]
            print(f"{f:13s} {e:>7.0e} "
                  f"{slope(al,[wv(r,'amg') for r in sub]):>7.2f} "
                  f"{slope(al,[wv(r,'amg_oracle') for r in sub]):>7.2f} "
                  f"{slope(al,[wv(r,'push') for r in sub]):>7.2f} "
                  f"{slope(al,[wv(r,'cheb') for r in sub]):>7.2f} "
                  f"{slope(al,[wv(r,'direct') for r in sub]):>7.2f} "
                  f"{slope(al,[r['amg']['volOmega']/r['volS'] for r in sub]):>7.2f}")

    print("\n=== TABLE 3: V-cycle rate (median over all cycles) by alpha ===")
    als = sorted({r["alpha"] for r in rows}, reverse=True)
    print(f"{'family':13s} " + " ".join(
        f"{'a=2^'+str(int(round(math.log2(a)))):>10s}" for a in als)
        + "   max-rate")
    for f in fams:
        cells = []
        mx = 0.0
        for a in als:
            v = [r["amg"].get("allrate") for r in rows
                 if r["fam"] == f and r["alpha"] == a
                 and r["amg"].get("allrate")]
            cells.append(f"{np.median(v):>10.3f}" if v else f"{'-':>10s}")
            for r in rows:
                if r["fam"] == f and r["alpha"] == a:
                    mx = max(mx, r["amg"].get("rmax_rate") or 0.0)
        print(f"{f:13s} " + " ".join(cells) + f"   {mx:>6.3f}")

    print("\n=== TABLE 4: setup / solve split, operator complexity, locality ===")
    print(f"{'family':13s} {'a':>6s} {'eps':>6s} {'setup%':>7s} {'solve%':>7s} "
          f"{'W_seq/W':>8s} {'opcx':>5s} {'nlev':>5s} {'volS/volG':>10s} "
          f"{'volOm/volG':>11s} {'attempts':>8s}")
    for f in fams:
        for r in [x for x in rows if x["fam"] == f]:
            A = r["amg"]
            print(f"{f:13s} 2^{int(round(math.log2(r['alpha']))):>4d} "
                  f"{r['eps']:>6.0e} {100*A['setup']/A['W']:>7.1f} "
                  f"{100*A['solve']/A['W']:>7.1f} "
                  f"{A.get('W_seq',A['W'])/A['W']:>8.3f} "
                  f"{(A.get('opcx') or float('nan')):>5.2f} "
                  f"{A.get('nlev') or 0:>5d} "
                  f"{r['volS']/r['volG']:>10.4f} "
                  f"{A['volOmega']/r['volG']:>11.4f} "
                  f"{A.get('attempts') or 0:>8d}")

    print("\n=== TABLE 5: winner map (lowest W/vol among certified) ===")
    for f in fams:
        for r in [x for x in rows if x["fam"] == f]:
            cand = {}
            for k in ("amg", "push", "cheb", "direct"):
                v = wv(r, k)
                st = (r.get(k) or {}).get("status", "cert")
                if np.isfinite(v) and st in ("cert", None):
                    cand[k] = v
            if not cand:
                continue
            best = min(cand, key=cand.get)
            amgv = cand.get("amg", float("nan"))
            print(f"{f:13s} 2^{int(round(math.log2(r['alpha']))):>4d} "
                  f"{r['eps']:>7.0e}  best={best:7s} {cand[best]:>9.1f}  "
                  f"AMG/best={amgv/cand[best]:>7.2f}")


if __name__ == "__main__":
    main()
