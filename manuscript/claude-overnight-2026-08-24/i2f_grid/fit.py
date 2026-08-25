"""Digest out/map.json: parameter map, W/vol ratios, fitted exponents."""
import json
import math
import sys

import numpy as np

OUT = "/home/claude/work/overnight/i2f_grid/out"
rows = [r for r in json.load(open(f"{OUT}/map.json")) if "error" not in r]
rows = [r for r in rows if not r.get("trivial")]


def g(r, k, d=float("nan")):
    v = r.get(k, d)
    try:
        return float(v)
    except (TypeError, ValueError):
        return d


def l2(x):
    return math.log2(x)


CANDS = [("push", "W_push"), ("cheb", "W_cheb"), ("hyb", "W_hyb"),
         ("nd", "W_nd"), ("mg", "W_mg"),
         ("nd_or", "W_nd_or"), ("mg_or", "W_mg_or")]


def section(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


section("A. PARAMETER MAP (measured output vs the classic target)")
print(f"{'alpha':>7} {'eps':>7} {'w':>4} {'nS':>7} {'volS':>8} {'Rsem':>5} "
      f"{'Rpred':>6} {'1/(sqrt(a)e)':>12} {'/volS':>8} {'1/(a e)':>10} "
      f"{'/volS':>8}")
for r in sorted(rows, key=lambda r: (-r["eps"], -r["alpha"])):
    a, e = r["alpha"], r["eps"]
    Rp = max(1 / math.sqrt(a), math.log(a / e) / (2 * math.sqrt(a))) if a > e \
        else 1 / math.sqrt(a)
    tc, tp = r["target_classic"], r["target_push"]
    print(f"2^{l2(a):>5.0f} {e:>7.0e} {r['w']:>4} {r['nS']:>7} "
          f"{r['volS']:>8.0f} {r['R_sem']:>5} {Rp:>6.1f} {tc:>12.3g} "
          f"{tc/r['volS']:>8.1f} {tp:>10.3g} {tp/r['volS']:>8.1f}")

section("B. CHARGED WORK W (self-certified) and W / vol(S_eps)")
hdr = f"{'alpha':>7} {'eps':>7} {'volS':>8} " + " ".join(
    f"{n:>10}" for n, _ in CANDS)
print(hdr)
for r in sorted(rows, key=lambda r: (-r["eps"], -r["alpha"])):
    vals = " ".join(f"{g(r, k):>10.3g}" for _, k in CANDS)
    print(f"2^{l2(r['alpha']):>5.0f} {r['eps']:>7.0e} {r['volS']:>8.0f} {vals}")
print()
print("W / vol(S_eps):")
print(hdr)
for r in sorted(rows, key=lambda r: (-r["eps"], -r["alpha"])):
    vals = " ".join(f"{g(r, k)/r['volS']:>10.1f}" for _, k in CANDS)
    print(f"2^{l2(r['alpha']):>5.0f} {r['eps']:>7.0e} {r['volS']:>8.0f} {vals}")

section("C. ALPHA-EXPONENTS of W/vol(S) at fixed eps  "
        "(W/vol ~ C * alpha^-s ; s=0 <=> alpha-free / output-linear)")
print(f"{'eps':>8} {'cand':>7} {'s':>7} {'C':>9} {'rms':>6}  points")
fits = {}
for eps in sorted({r["eps"] for r in rows}, reverse=True):
    sub = [r for r in rows if r["eps"] == eps and r["volS"] > 20]
    if len(sub) < 3:
        continue
    for name, key in CANDS:
        pts = [(r["alpha"], g(r, key) / r["volS"]) for r in sub
               if np.isfinite(g(r, key))]
        if len(pts) < 3:
            continue
        X = np.array([[1.0, -math.log(a)] for a, _ in pts])
        y = np.array([math.log(v) for _, v in pts])
        c, *_ = np.linalg.lstsq(X, y, rcond=None)
        rms = float(np.sqrt(np.mean((X @ c - y) ** 2)))
        fits[(eps, name)] = (c[1], math.exp(c[0]), rms)
        print(f"{eps:>8.0e} {name:>7} {c[1]:>7.3f} {math.exp(c[0]):>9.3g} "
              f"{rms:>6.3f}  {len(pts)}")

section("D. ALPHA- and EPS-EXPONENTS of RAW W  (log W = c + p log(1/a) "
        "+ q log(1/eps))")
print(f"{'cand':>7} {'p(alpha)':>9} {'q(eps)':>8} {'rms':>6}  n")
sub = [r for r in rows if r["volS"] > 20 and r["eps"] <= 1e-4]
for name, key in [("volS", None)] + CANDS:
    pts = [(r["alpha"], r["eps"],
            r["volS"] if key is None else g(r, key)) for r in sub]
    pts = [p for p in pts if np.isfinite(p[2]) and p[2] > 0]
    if len(pts) < 4:
        continue
    X = np.array([[1.0, -math.log(a), -math.log(e)] for a, e, _ in pts])
    y = np.array([math.log(v) for _, _, v in pts])
    c, *_ = np.linalg.lstsq(X, y, rcond=None)
    rms = float(np.sqrt(np.mean((X @ c - y) ** 2)))
    print(f"{name:>7} {c[1]:>9.3f} {c[2]:>8.3f} {rms:>6.3f}  {len(pts)}")

section("E. MG cost decomposition (region inflation x search x cycles)")
print(f"{'alpha':>7} {'eps':>7} {'Rsem':>5} {'m_mg':>5} {'m_or':>5} "
      f"{'volO/volS':>9} {'cyc':>4} {'W/volO':>7} {'W/volS':>7} "
      f"{'Wor/W':>6} {'adj%':>5} {'resp%':>6} {'mat%':>5}")
for r in sorted(rows, key=lambda r: (-r["eps"], -r["alpha"])):
    v = r.get("mg_vec")
    if isinstance(v, str):
        v = json.loads(v.replace("'", '"'))
    tot = g(r, "W_mg")
    adj = (v["C_adj"] + v["R_adj"]) / tot * 100 if v else float("nan")
    resp = v["C_resp"] / tot * 100 if v else float("nan")
    mat = v["C_mat"] / tot * 100 if v else float("nan")
    vo = g(r, "volOmega_mg")
    print(f"2^{l2(r['alpha']):>5.0f} {r['eps']:>7.0e} {r['R_sem']:>5} "
          f"{g(r,'m_mg'):>5.0f} {g(r,'m_mg_or'):>5.0f} {vo/r['volS']:>9.2f} "
          f"{g(r,'cyc_mg'):>4.0f} {tot/vo:>7.1f} {tot/r['volS']:>7.1f} "
          f"{g(r,'W_mg_or')/tot:>6.2f} {adj:>5.1f} {resp:>6.1f} {mat:>5.1f}")

section("F. WINNER per cell (self-certified bracket) and MG speedup")
print(f"{'alpha':>7} {'eps':>7} {'winner':>8} {'W_win':>10} "
      f"{'mg/push':>8} {'mg/cheb':>8} {'mg/nd':>7}")
for r in sorted(rows, key=lambda r: (-r["eps"], -r["alpha"])):
    cs = [(g(r, k), n) for n, k in CANDS[:5] if np.isfinite(g(r, k))]
    wv, wn = min(cs)
    mg = g(r, "W_mg")
    print(f"2^{l2(r['alpha']):>5.0f} {r['eps']:>7.0e} {wn:>8} {wv:>10.3g} "
          f"{mg/g(r,'W_push'):>8.3f} {mg/g(r,'W_cheb'):>8.3f} "
          f"{mg/g(r,'W_nd'):>7.3f}")

section("G. semantic error / eps (verification) — must all be <= 1")
mx = {}
for r in rows:
    for k in ("err_push", "err_cheb", "err_nd", "err_mg", "err_hyb"):
        v = g(r, k)
        if np.isfinite(v):
            mx[k] = max(mx.get(k, 0.0), v / r["eps"])
print("  max err/eps over all cells:", {k: round(v, 4) for k, v in mx.items()})
sts = {}
for r in rows:
    for k in ("push_status", "cheb_status", "nd_status", "mg_status"):
        sts.setdefault(k, {}).setdefault(r.get(k), 0)
        sts[k][r.get(k)] += 1
print("  statuses:", sts)
