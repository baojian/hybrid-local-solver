"""Fit vol(S_eps) ~ C * alpha^-p * eps^-q per family; report saturation."""
import json, math
import numpy as np
OUT = "/home/claude/work/overnight/i4d/out"
R = json.load(open(f"{OUT}/out_measure.json"))
fams = []
seen = set()
for r in R:
    if r["family"] not in seen:
        seen.add(r["family"]); fams.append(r["family"])
print("%-12s %6s | %-22s | %-9s %-9s | %-9s | %s"
      % ("family", "cells", "vol(S_eps) ~ a^-p eps^-q", "p", "q",
         "max vol*eps", "max volB/volS   (n_S max)"))
print("-" * 118)
out = {}
for f in fams:
    rs = [r for r in R if r["family"] == f and not r["clipped"] and r["nS"] > 2]
    if len(rs) < 6:
        print("%-12s  (too few clean cells: %d)" % (f, len(rs))); continue
    Aa = np.array([[1.0, -math.log(r["alpha"]), -math.log(r["eps"])] for r in rs])
    y = np.array([math.log(r["volS"]) for r in rs])
    coef, res, *_ = np.linalg.lstsq(Aa, y, rcond=None)
    pred = Aa @ coef
    r2 = 1 - np.sum((y - pred) ** 2) / max(np.sum((y - y.mean()) ** 2), 1e-30)
    mv = max(rs, key=lambda r: r["volS_eps"])
    mb = max(rs, key=lambda r: r["volB"] / max(r["volS"], 1))
    out[f] = dict(p=coef[1], q=coef[2], r2=r2, maxvol_eps=mv["volS_eps"],
                  maxvolB_ratio=mb["volB"] / max(mb["volS"], 1))
    print("%-12s %6d | C=%7.3g  R^2=%.3f    | %+8.3f %+8.3f | %9.4f | %8.2f  (%d)"
          % (f, len(rs), math.exp(coef[0]), r2, coef[1], coef[2],
             mv["volS_eps"], mb["volB"] / max(mb["volS"], 1),
             max(r["nS"] for r in rs)))
allr = [r for r in R if r["nS"] > 0 and not r["clipped"]]
print("\nGLOBAL: %d clean cells; max vol(S_eps)*eps = %.4f (%s a=2^%.0f eps=%.0e);"
      % (len(allr), max(r["volS_eps"] for r in allr),
         *[ (lambda b: (b["family"], math.log2(b["alpha"]), b["eps"]))(
             max(allr, key=lambda r: r["volS_eps"]))][0]))
print("        violations of vol(S_eps) < 1/eps :",
      sum(1 for r in allr if r["volS_eps"] >= 1.0))
print("        max |S_eps|*eps                  : %.4f"
      % max(r["nS_eps"] for r in allr))
print("        max vol(dS_eps)*eps              : %.4f  <-- boundary ring is NOT bounded by 1/eps in general"
      % max(r["volB_eps"] for r in allr))
json.dump(out, open(f"{OUT}/fit_out.json", "w"))
