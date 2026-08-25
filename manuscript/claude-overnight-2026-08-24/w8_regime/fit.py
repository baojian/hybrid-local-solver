"""W8 analysis: winner tables, crossover fits eps*(alpha), constants,
expansion counts, prize map. Reads map.csv, writes findings markdown."""
import csv
import math
import os
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FAMS = ["star", "spider", "spider2", "caterpillar", "btree", "grid"]


def load():
    rows = []
    with open(os.path.join(HERE, "map.csv")) as f:
        for r in csv.DictReader(f):
            for k in r:
                if r[k] == "":
                    r[k] = None
                elif k not in ("graph", "status", "winner"):
                    r[k] = float(r[k])
            rows.append(r)
    cert = {}
    with open(os.path.join(HERE, "cert.csv")) as f:
        for r in csv.DictReader(f):
            if r["status_cert"] == "ok":
                cert[(r["graph"], float(r["alpha_log2"]),
                      float(r["eps_log2"]))] = dict(
                    W=float(r["W_WYcert"]), E=float(r["E_cert"]),
                    S=float(r["S_cert"]))
    po = {}
    with open(os.path.join(HERE, "push_oracle.csv")) as f:
        for r in csv.DictReader(f):
            if r["status_po"] == "ok":
                po[(r["graph"], float(r["alpha_log2"]),
                    float(r["eps_log2"]))] = float(r["W_push_oracle"])
    for r in rows:
        key = (r["graph"], r["alpha_log2"], r["eps_log2"])
        r["cert"] = cert.get(key)
        r["push_o"] = po.get(key)
    return rows


def crossing(pairs, key):
    """pairs: sorted list of (eps_log2 desc, value). Return interpolated
    eps_log2 where value crosses 0 (largest-eps stable crossing to <0),
    or +inf if always <0, -inf if never <0."""
    vals = [(e, v) for e, v in pairs if v is not None]
    if not vals:
        return None
    vals.sort(reverse=True)  # eps large -> small
    # stable crossover: last index from which value stays < 0 onwards
    neg_from = None
    for i in range(len(vals) - 1, -1, -1):
        if vals[i][1] < 0:
            neg_from = i
        else:
            break
    if neg_from is None:
        return -math.inf
    if neg_from == 0:
        return math.inf
    e1, v1 = vals[neg_from - 1]
    e2, v2 = vals[neg_from]
    if v1 == v2:
        return e2
    return e1 + (0 - v1) * (e2 - e1) / (v2 - v1)


def fit_line(xs, ys):
    """LSQ y = b + m x; returns m, b, rms residual."""
    x = np.array(xs)
    y = np.array(ys)
    A = np.vstack([x, np.ones_like(x)]).T
    (m, b), res, _, _ = np.linalg.lstsq(A, y, rcond=None)
    pred = A @ np.array([m, b])
    return float(m), float(b), float(np.sqrt(np.mean((pred - y) ** 2)))


def main():
    rows = load()
    ok = [r for r in rows if r["status"] == "ok"]
    by_fam = defaultdict(list)
    for r in ok:
        by_fam[r["graph"]].append(r)

    out = []
    say = out.append

    # ---------- 1. crossover fits ----------
    say("## Crossover eps*(alpha) where W_push = W_WY (dense grid)\n")
    say("Fit: log2 eps* = log2 kappa + (theta/2) * log2 alpha, i.e. "
        "eps* = kappa * alpha^(theta/2) = kappa * sqrt(alpha)^theta.")
    say("theta = 1 would be the sqrt(alpha) line; the constant-free "
        "algebra 1/(alpha*eps) = 1/eps^2 predicts theta = 2 (eps* = alpha).\n")
    say("| graph | theta | kappa | rms(log2) | #alphas | eps* range |")
    say("|---|---|---|---|---|---|")
    cross_pts = {}
    for fam in FAMS:
        pts = []
        per_alpha = defaultdict(list)
        for r in by_fam[fam]:
            if r["triv"]:
                continue          # degenerate cells excluded from fits
            per_alpha[r["alpha_log2"]].append(
                (r["eps_log2"], math.log2(r["W_push"] / r["W_WY"])
                 if r["W_push"] and r["W_WY"] else None))
        for la, pairs in sorted(per_alpha.items()):
            ec = crossing(pairs, None)
            if ec is not None and math.isfinite(ec):
                pts.append((la, ec))
        cross_pts[fam] = pts
        if len(pts) >= 3:
            m, b, rms = fit_line([p[0] for p in pts], [p[1] for p in pts])
            theta = 2 * m
            kappa = 2 ** b
            er = (min(p[1] for p in pts), max(p[1] for p in pts))
            say(f"| {fam} | {theta:.2f} | {kappa:.3g} | {rms:.2f} | "
                f"{len(pts)} | 2^{er[0]:.1f} .. 2^{er[1]:.1f} |")
        else:
            say(f"| {fam} | n/a ({len(pts)} crossings in-grid) | | | | |")
    say("")
    say("Crossing points (alpha_log2 -> eps*_log2): " + "; ".join(
        f"{fam}: " + ", ".join(f"{int(a)}->{e:.1f}" for a, e in pts)
        for fam, pts in cross_pts.items() if pts) + "\n")

    # ---------- 1b. crossover vs SELF-CERTIFIED WY (coarse grid) ----------
    say("### Crossover vs the self-certified WY bracket "
        "(cert < alpha*eps, deterministic guarantee)\n")
    say("| graph | theta | kappa | rms(log2) | #alphas | points |")
    say("|---|---|---|---|---|---|")
    for fam in FAMS:
        pts = []
        per_alpha = defaultdict(list)
        for r in by_fam[fam]:
            if r["triv"] or r["cert"] is None:
                continue
            per_alpha[r["alpha_log2"]].append(
                (r["eps_log2"],
                 math.log2(r["W_push"] / r["cert"]["W"])))
        for la, pairs in sorted(per_alpha.items()):
            ec = crossing(pairs, None)
            if ec is not None and math.isfinite(ec):
                pts.append((la, ec))
        if len(pts) >= 3:
            m, b, rms = fit_line([p[0] for p in pts], [p[1] for p in pts])
            say(f"| {fam} | {2*m:.2f} | {2**b:.3g} | {rms:.2f} | {len(pts)} |"
                f" " + ",".join(f"{int(a)}->{e:.1f}" for a, e in pts) + " |")
        else:
            say(f"| {fam} | n/a ({len(pts)} crossings) | | | | "
                + ",".join(f"{int(a)}->{e:.1f}" for a, e in pts) + " |")
    say("")

    # ---------- 2. empirical wedge boundary (target vs best incumbent) ----
    say("## Empirical wedge boundary eps_dagger(alpha) where "
        "min(W_push,W_WY) = W_target\n")
    say("Below this eps the target oracle beats both measured contenders "
        "(theory line: eps = sqrt(alpha), i.e. theta=1, kappa=1).\n")
    say("| graph | theta | kappa | rms(log2) | #alphas |")
    say("|---|---|---|---|---|")
    for fam in FAMS:
        pts = []
        per_alpha = defaultdict(list)
        for r in by_fam[fam]:
            if r["triv"]:
                continue
            per_alpha[r["alpha_log2"]].append(
                (r["eps_log2"], math.log2(1.0 / r["ratio_to_target"])
                 if r["ratio_to_target"] else None))
        # value < 0 <=> ratio > 1 <=> target wins (deep eps side)
        for la, pairs in sorted(per_alpha.items()):
            ec = crossing(pairs, None)
            if ec is not None and math.isfinite(ec):
                pts.append((la, ec))
        if len(pts) >= 3:
            m, b, rms = fit_line([p[0] for p in pts], [p[1] for p in pts])
            say(f"| {fam} | {2*m:.2f} | {2**b:.3g} | {rms:.2f} | {len(pts)} |")
        else:
            say(f"| {fam} | n/a ({len(pts)} crossings) | | | |")
    say("")

    # ---------- 3. constants ----------
    say("## Measured constants (non-trivial cells, eps <= 2^-5)\n")
    say("| graph | W_push*alpha*eps med [min,max] | W_WY*eps^2 med "
        "[min,max] | W_WY*eps^2 at eps=2^-13 (per alpha range) |")
    say("|---|---|---|---|")
    for fam in FAMS:
        sel = [r for r in by_fam[fam] if r["eps_log2"] <= -5 and
               r["triv"] == 0]
        cp = sorted(r["const_push"] for r in sel)
        cw = sorted(r["const_wy"] for r in sel)
        deep = [r["const_wy"] for r in sel if r["eps_log2"] == -13]
        say(f"| {fam} | {np.median(cp):.3f} [{cp[0]:.3f}, {cp[-1]:.3f}] | "
            f"{np.median(cw):.3g} [{cw[0]:.3g}, {cw[-1]:.3g}] | "
            f"{min(deep):.3g} .. {max(deep):.3g} |" if deep else
            f"| {fam} | {np.median(cp):.3f} [{cp[0]:.3f}, {cp[-1]:.3f}] | "
            f"{np.median(cw):.3g} [{cw[0]:.3g}, {cw[-1]:.3g}] | n/a |")
    say("")

    # ---------- 4. scaling exponents ----------
    say("## Fitted scaling exponents log2 W = c + pe*log2(1/eps) + "
        "pa*log2(1/alpha)  (non-trivial cells, eps<=2^-5, n>=30)\n")
    say("| graph | push: pe, pa, c | WY: pe, pa, c |")
    say("|---|---|---|")
    for fam in FAMS:
        sel = [r for r in by_fam[fam] if r["eps_log2"] <= -5 and
               r["triv"] == 0 and r["n"] >= 30]
        if len(sel) < 6:
            say(f"| {fam} | too few cells | |")
            continue
        X = np.array([[-r["eps_log2"], -r["alpha_log2"], 1.0] for r in sel])
        line = f"| {fam} |"
        for key in ("W_push", "W_WY"):
            y = np.array([math.log2(r[key]) for r in sel])
            coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
            line += (f" {coef[0]:.2f}, {coef[1]:.2f}, {coef[2]:.1f} |")
        say(line)
    say("")

    # ---------- 5. expansion counts ----------
    say("## WY expansion counts E (rounds incl. tightenings) vs the 1/eps "
        "pessimism\n")
    say("| graph | E at eps=2^-13 (over alpha) | fitted slope dlog2 E / "
        "dlog2(1/eps) (at alpha=2^-10) | tightenings max |")
    say("|---|---|---|---|")
    for fam in FAMS:
        deep = [int(r["E_expansions"]) for r in by_fam[fam]
                if r["eps_log2"] == -13]
        sl = [r for r in by_fam[fam] if r["alpha_log2"] == -10 and
              r["eps_log2"] <= -5]
        slope = "n/a"
        if len(sl) >= 3:
            m, b, _ = fit_line([-r["eps_log2"] for r in sl],
                               [math.log2(r["E_expansions"]) for r in sl])
            slope = f"{m:.2f}"
        tmax = max(int(r["tightenings"]) for r in by_fam[fam])
        say(f"| {fam} | {min(deep)} .. {max(deep)} | {slope} | {tmax} |"
            if deep else f"| {fam} | n/a | {slope} | {tmax} |")
    say("")

    # ---------- 6. prize map (two brackets) ----------
    say("## Prize map: potential speedup of the target oracle\n")
    say("LO bracket = min(W_push, W_WY_oracle)/W_target (oracle-stopped WY, "
        "generous incumbent); HI bracket = min(W_push, W_WYcert)/W_target "
        "(self-certified WY, conservative incumbent). Real WY with whp "
        "certification lies between.\n")
    def lo(r):
        """LO bracket: best oracle-stopped incumbent, dense on all cells
        (min of oracle-push and oracle-WY; the self-certified variants are
        never below these except star-deep cells with ratio << 1)."""
        if r["push_o"] == 0.0:
            return 0.0
        inc = min(r["W_push"], r["W_WY"],
                  r["push_o"] if r["push_o"] is not None else math.inf)
        return inc / r["W_target"]

    for lab, fn in (("LO", lo),
                    ("HI", lambda r: (min(r["W_push"], r["cert"]["W"])
                                      / r["W_target"])
                     if r["cert"] is not None else None)):
        for thresh in (10.0, 100.0):
            say(f"{lab} bracket, cells with speedup >= {thresh:g}:")
            any_hit = False
            for fam in FAMS:
                hits = []
                for r in by_fam[fam]:
                    v = fn(r)
                    if v is not None and v >= thresh:
                        hits.append((int(r["alpha_log2"]),
                                     int(r["eps_log2"]), v))
                if hits:
                    any_hit = True
                    hits.sort()
                    say(f"- {fam}: " + ", ".join(
                        f"(2^{a},2^{e}):{v:.0f}x" for a, e, v in hits))
            if not any_hit:
                say("- none in grid")
            say("")
    say("| graph | max LO speedup (at) | max HI speedup (at) |")
    say("|---|---|---|")
    for fam in FAMS:
        best = max(by_fam[fam], key=lo)
        ch = [(min(r["W_push"], r["cert"]["W"]) / r["W_target"], r)
              for r in by_fam[fam] if r["cert"] is not None]
        s = (f"| {fam} | {lo(best):.1f}x "
             f"(2^{int(best['alpha_log2'])},2^{int(best['eps_log2'])}) | ")
        if ch:
            bv, br = max(ch, key=lambda t: t[0])
            s += (f"{bv:.1f}x (2^{int(br['alpha_log2'])},"
                  f"2^{int(br['eps_log2'])}) |")
        else:
            s += "n/a |"
        say(s)
    say("")

    # certified constants
    say("### Self-certified WY: W_WYcert*eps^2 (coarse grid, non-triv, "
        "eps<=2^-5) and expansions\n")
    say("| graph | W_WYcert*eps^2 med [min,max] | E_cert at eps=2^-13 | "
        "E_cert slope vs 1/eps (alpha=2^-10) |")
    say("|---|---|---|---|")
    for fam in FAMS:
        sel = [r for r in by_fam[fam] if r["cert"] is not None and
               r["eps_log2"] <= -5 and r["triv"] == 0]
        if not sel:
            say(f"| {fam} | n/a | | |")
            continue
        cw = sorted(r["cert"]["W"] * r["eps"] ** 2 for r in sel)
        deep = [int(r["cert"]["E"]) for r in sel if r["eps_log2"] == -13]
        sl = [r for r in sel if r["alpha_log2"] == -10]
        slope = "n/a"
        if len(sl) >= 3:
            m, b, _ = fit_line([-r["eps_log2"] for r in sl],
                               [math.log2(r["cert"]["E"]) for r in sl])
            slope = f"{m:.2f}"
        dp = f"{min(deep)} .. {max(deep)}" if deep else "n/a"
        say(f"| {fam} | {np.median(cw):.3g} [{cw[0]:.3g}, {cw[-1]:.3g}] | "
            f"{dp} | {slope} |")
    say("")

    # ---------- 7. winner tables (coarse specified grid) ----------
    say("## Winner tables (specified coarse grid; P=push, W=WY, "
        "t suffix = trivial cell, number = ratio_to_target)\n")
    ALL = {(r["graph"], r["alpha_log2"], r["eps_log2"]): r for r in rows}
    a_grid = list(range(-2, -15, -2))
    e_grid = list(range(-3, -14, -2))
    for fam in FAMS:
        say(f"### {fam}\n")
        say("| alpha \\ eps | " + " | ".join(f"2^{e}" for e in e_grid) + " |")
        say("|" + "---|" * (len(e_grid) + 1))
        for a in a_grid:
            cells = []
            for e in e_grid:
                r = ALL.get((fam, float(a), float(e)))
                if r is None or r["status"] != "ok":
                    cells.append("skip")
                    continue
                tag = "P" if r["winner"] == "push" else "W"
                if r["cert"] is not None:
                    tag += "/P" if r["W_push"] <= r["cert"]["W"] else "/W"
                if r["triv"]:
                    tag += "t"
                cells.append(f"{tag} {r['ratio_to_target']:.2g}")
            say(f"| 2^{a} | " + " | ".join(cells) + " |")
        say("")

    text = "\n".join(out)
    with open(os.path.join(HERE, "analysis.md"), "w") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    main()
