"""I4-B tables: comparison, ledger, alpha-exponents, triage economics."""
import json
import math
import os
import sys

import numpy as np

OUT = "/home/claude/work/overnight/i4b_composed/out"
I3A = "/home/claude/work/overnight/i3a_amg/out/zoo_main.json"

METHODS = ["comp", "comp_E", "comp_A", "comp_pull", "comp_nb", "wy", "push"]
ORDER = ["star", "path", "caterpillar", "comb", "spider", "theta",
         "decoy_hub", "double_cycle", "binary_tree", "rrt", "grid2d",
         "rand_reg3", "rand_reg4", "grid3d"]


def load(tag="main"):
    with open(os.path.join(OUT, f"i4b_{tag}.json")) as fh:
        rows = json.load(fh)
    ref = {}
    if os.path.exists(I3A):
        with open(I3A) as fh:
            for r in json.load(fh):
                ref[(r["fam"], r["alpha"], r["eps"])] = r
    for r in rows:
        k = (r.get("fam"), r.get("alpha"), r.get("eps"))
        if k in ref:
            for tag2 in ("amg", "direct"):
                d = ref[k].get(tag2)
                if d and d.get("W"):
                    r.setdefault(tag2, dict(W=d["W"], status=d.get("status"),
                                            err_eps=d.get("err_eps"),
                                            approx_map=True, C_adj=d.get("C_adj"),
                                            R_adj=d.get("R_adj"),
                                            C_rec=d.get("C_rec"),
                                            C_resp=d.get("C_resp"),
                                            C_mat=d.get("C_mat")))
    return [r for r in rows if r.get("volS")]


def wv(r, k):
    d = r.get(k) or {}
    w = d.get("W")
    if not w or d.get("status") in ("cap", "err", "maxed", "stuck", "fail"):
        return float("nan")
    return w / max(r["volS"], 1)


def f(x, w=9, p=1):
    return ("nan".rjust(w) if (x is None or (isinstance(x, float) and
            math.isnan(x))) else f"{x:{w}.{p}f}")


def table1(rows):
    print("\n=== TABLE 1: W / vol(S_eps) -- composed vs every baseline "
          "(nan = capped / not certified) ===")
    hdr = (f"{'family':13s}{'alpha':>6s}{'eps':>7s}{'volS':>9s}"
           f"{'COMPOSED':>10s}{'comp_E':>9s}{'comp_A':>9s}{'pull':>9s}"
           f"{'WY':>10s}{'push':>10s}{'AMG_i3a':>9s}{'DIR_i3a':>9s}"
           f"{'rd':>4s}{'fl':>3s}{'reg/S':>7s}{'e/eps':>7s}")
    print(hdr)
    for fam in ORDER:
        for r in rows:
            if r["fam"] != fam:
                continue
            C = r.get("comp", {})
            print(f"{fam:13s}{int(round(math.log2(r['alpha']))):>6d}"
                  f"{r['eps']:>7.0e}{r['volS']:>9.0f}"
                  f"{f(wv(r,'comp'),10)}{f(wv(r,'comp_E'))}{f(wv(r,'comp_A'))}"
                  f"{f(wv(r,'comp_pull'))}{f(wv(r,'wy'),10)}{f(wv(r,'push'),10)}"
                  f"{f(wv(r,'amg'))}{f(wv(r,'direct'))}"
                  f"{C.get('rounds',0):>4}{C.get('flips',0):>3}"
                  f"{(C.get('volReg',0) or 0)/max(r['volS'],1):>7.2f}"
                  f"{C.get('err_eps',float('nan')):>7.3f}")


def table2(rows):
    print("\n=== TABLE 2: ELEVEN-COORDINATE LEDGER of the composed solver "
          "(units; M_pers/M_tmp are cells, not summed into W) ===")
    K = ["C_adj", "R_adj", "R_int", "C_pre", "C_ctl", "C_rec", "C_resp",
         "C_mat", "C_emit"]
    print(f"{'family':13s}{'a':>4s}{'eps':>7s}" +
          "".join(f"{k:>10s}" for k in K) +
          f"{'W':>11s}{'M_pers':>9s}{'M_tmp':>9s}"
          f"{'tri%':>6s}{'gate%':>6s}{'cert%':>6s}{'swtch%':>7s}{'pig%':>6s}")
    for fam in ORDER:
        for r in rows:
            if r["fam"] != fam:
                continue
            C = r.get("comp")
            if not C or not C.get("W"):
                continue
            W = C["W"]
            print(f"{fam:13s}{int(round(math.log2(r['alpha']))):>4d}"
                  f"{r['eps']:>7.0e}" +
                  "".join(f"{C.get(k,0):>10.3g}" for k in K) +
                  f"{W:>11.4g}{C.get('M_pers',0):>9.3g}"
                  f"{C.get('M_tmp',0):>9.3g}"
                  f"{100*C.get('ctl_triage',0)/W:>6.1f}"
                  f"{100*C.get('ctl_gate',0)/W:>6.1f}"
                  f"{100*C.get('ctl_cert',0)/W:>6.1f}"
                  f"{100*C.get('resp_switch',0)/W:>7.1f}"
                  f"{100*C.get('piggy',0)/W:>6.1f}")


def fit_alpha(rows, key):
    """Fit log(W/volS) ~ q * log(1/alpha) per (family, eps), then median."""
    out = {}
    for fam in ORDER:
        qs = []
        for eps in (1e-6, 1e-8):
            pts = []
            for r in rows:
                if r["fam"] != fam or r["eps"] != eps:
                    continue
                y = wv(r, key)
                if y and not math.isnan(y) and y > 0:
                    pts.append((math.log(1.0 / r["alpha"]), math.log(y)))
            if len(pts) >= 2:
                x = np.array([p[0] for p in pts])
                yv = np.array([p[1] for p in pts])
                qs.append(float(np.polyfit(x, yv, 1)[0]))
        if qs:
            out[fam] = float(np.median(qs))
    return out


def table3(rows):
    print("\n=== TABLE 3: alpha-exponent of W/vol(S_eps)   "
          "(W/vol ~ alpha^-q; q=0 is alpha-free) ===")
    fits = {k: fit_alpha(rows, k) for k in
            ("comp", "comp_E", "comp_A", "wy", "push", "amg", "direct")}
    print(f"{'family':13s}" + "".join(f"{k:>10s}" for k in fits))
    for fam in ORDER:
        if not any(fam in fits[k] for k in fits):
            continue
        print(f"{fam:13s}" +
              "".join(f(fits[k].get(fam), 10, 2) for k in fits))
    print(f"{'MEDIAN':13s}" +
          "".join(f(float(np.median(list(fits[k].values())))
                    if fits[k] else None, 10, 2) for k in fits))


def table4(rows):
    print("\n=== TABLE 4: TRIAGE ECONOMICS -- cost of the test vs the cost "
          "of the wrong route ===")
    print(f"{'family':13s}{'a':>4s}{'eps':>7s}{'route':>16s}"
          f"{'tri_cost':>10s}{'tri%W':>7s}{'W_comp':>11s}{'W_best1':>11s}"
          f"{'W_wrong1':>11s}{'save_x':>8s}{'net_x':>8s}")
    for fam in ORDER:
        for r in rows:
            if r["fam"] != fam:
                continue
            C = r.get("comp")
            if not C or not C.get("W"):
                continue
            we, wa = (r.get("comp_E") or {}).get("W"), (r.get("comp_A") or {}).get("W")
            se = (r.get("comp_E") or {}).get("status")
            sa = (r.get("comp_A") or {}).get("status")
            we = we if se == "cert" else None
            wa = wa if sa == "cert" else None
            cand = [w for w in (we, wa) if w]
            if not cand:
                continue
            best = min(cand)
            worst = max(cand) if len(cand) > 1 else float("nan")
            tri = C.get("ctl_triage", 0)
            rts = C.get("routes", "")
            print(f"{fam:13s}{int(round(math.log2(r['alpha']))):>4d}"
                  f"{r['eps']:>7.0e}{rts[:16]:>16s}"
                  f"{tri:>10.4g}{100*tri/C['W']:>7.1f}{C['W']:>11.4g}"
                  f"{best:>11.4g}{worst:>11.4g}"
                  f"{(worst/best if best else float('nan')):>8.2f}"
                  f"{(best/C['W']):>8.2f}")


def table5(rows):
    print("\n=== TABLE 5: TRIAGE FLIPS and the refactorisation tax ===")
    print(f"{'family':13s}{'a':>4s}{'eps':>7s}{'rounds':>7s}{'flips':>6s}"
          f"{'routes':>26s}{'switch_cost':>12s}{'%W':>6s}"
          f"{'rd_nobatch':>11s}{'W_nb/W':>8s}")
    for fam in ORDER:
        for r in rows:
            if r["fam"] != fam:
                continue
            C = r.get("comp")
            if not C or not C.get("W"):
                continue
            NB = r.get("comp_nb") or {}
            print(f"{fam:13s}{int(round(math.log2(r['alpha']))):>4d}"
                  f"{r['eps']:>7.0e}{C.get('rounds',0):>7}"
                  f"{C.get('flips',0):>6}{C.get('routes','')[:26]:>26s}"
                  f"{C.get('resp_switch',0):>12.4g}"
                  f"{100*C.get('resp_switch',0)/C['W']:>6.1f}"
                  f"{(NB.get('rounds') or 0):>11}"
                  f"{f((NB.get('W')/C['W']) if NB.get('W') else None, 8, 2)}")


def table6(rows):
    print("\n=== TABLE 6: correctness -- semantic error / eps and certificate "
          "===")
    bad = []
    for r in rows:
        for k in METHODS + ["amg", "direct"]:
            d = r.get(k)
            if not d or "err_eps" not in d:
                continue
            if d.get("status") == "cert" and d["err_eps"] > 1.0:
                bad.append((r["fam"], r["alpha"], r["eps"], k, d["err_eps"]))
    tot = 0
    mx = {}
    for r in rows:
        for k in METHODS:
            d = r.get(k)
            if d and d.get("status") == "cert" and "err_eps" in d:
                tot += 1
                mx[k] = max(mx.get(k, 0), d["err_eps"])
    print(f"certified runs verified against the exact solve: {tot}")
    for k, v in sorted(mx.items()):
        print(f"   {k:10s} max err/eps = {v:.4f}")
    print(f"VIOLATIONS (err > eps on a certified run): {len(bad)}")
    for b in bad:
        print("   ", b)


def dominance(rows):
    print("\n=== TABLE 7: does the composition dominate? "
          "(ratio W_comp / W_baseline; <1 means composed wins) ===")
    base = ["comp_E", "comp_A", "wy", "push", "amg", "direct"]
    print(f"{'family':13s}" + "".join(f"{b:>10s}" for b in base) +
          f"{'best_base':>11s}{'comp/best':>10s}")
    agg = {b: [] for b in base}
    allr = []
    for fam in ORDER:
        rs = [r for r in rows if r["fam"] == fam and wv(r, "comp") ==
              wv(r, "comp") and not math.isnan(wv(r, "comp"))]
        if not rs:
            continue
        row = {}
        for b in base:
            v = [wv(r, "comp") / wv(r, b) for r in rs
                 if not math.isnan(wv(r, b)) and wv(r, b) > 0]
            row[b] = float(np.median(v)) if v else float("nan")
            if v:
                agg[b] += v
        bb = []
        for r in rs:
            cands = [wv(r, b) for b in base if not math.isnan(wv(r, b))]
            if cands:
                bb.append(wv(r, "comp") / min(cands))
        med = float(np.median(bb)) if bb else float("nan")
        allr += bb
        print(f"{fam:13s}" + "".join(f(row[b], 10, 2) for b in base) +
              f"{'':>11s}{f(med,10,2)}")
    print(f"{'MEDIAN(all)':13s}" +
          "".join(f(float(np.median(agg[b])) if agg[b] else None, 10, 2)
                  for b in base) +
          f"{'':>11s}{f(float(np.median(allr)) if allr else None,10,2)}")


if __name__ == "__main__":
    tag = sys.argv[1] if len(sys.argv) > 1 else "main"
    rows = load(tag)
    print(f"loaded {len(rows)} non-degenerate cells")
    table1(rows); table2(rows); table3(rows); table4(rows)
    table5(rows); table6(rows); dominance(rows)
