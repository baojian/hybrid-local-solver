import json, math, sys
import numpy as np
J = json.load(open("/home/claude/work/overnight/i4e/out/zoo.json"))
byf = {}
for r in J:
    fam = r["tag"].split(" a=")[0]
    byf.setdefault(fam, []).append(r)
MECH = ("push", "composed", "vgf", "vgfO")
print("%-10s %8s | %-28s | %-28s" % ("family", "volSeps", "W*eps  (a=2^-4/-8/-12)",
                                     "alpha-exponent  p in W ~ a^-p"))
print("-" * 106)
hdr = "%-10s %8s |" % ("", "")
for mm in MECH:
    hdr += " %-22s" % mm
print(hdr)
rows = {}
for fam, rs in byf.items():
    rs.sort(key=lambda r: -r["alpha"])
    line = "%-10s %8.0f |" % (fam, rs[-1]["volS"])
    ex = {}
    for mm in MECH:
        we = [r[mm]["We"] for r in rs]
        al = [r["alpha"] for r in rs]
        good = [(a, w) for a, w in zip(al, we)
                if w == w and w > 0]
        if len(good) >= 2:
            x = np.log([g[0] for g in good])
            y = np.log([g[1] for g in good])
            p = -np.polyfit(x, y, 1)[0]
        else:
            p = float("nan")
        ex[mm] = p
        line += " %6.3g/%6.3g/%6.3g p=%+.2f" % (we[0], we[1], we[2], p)
    rows[fam] = ex
    print(line)
print()
print("W / vol(S_eps)  (charged units per unit of OUTPUT volume)")
print("%-10s |" % "family", " ".join("%-22s" % m for m in MECH))
for fam, rs in byf.items():
    rs.sort(key=lambda r: -r["alpha"])
    line = "%-10s |" % fam
    for mm in MECH:
        line += " " + "/".join("%7.1f" % (r[mm]["W"] / max(r["volS"], 1))
                               for r in rs) + " "
    print(line)
print()
print("MEDIAN alpha-exponent over families:")
for mm in MECH:
    v = [rows[f][mm] for f in rows if rows[f][mm] == rows[f][mm]]
    print("   %-10s median p = %+.3f   max p = %+.3f   (families: %d)"
          % (mm, float(np.median(v)), float(np.max(v)), len(v)))
print()
print("VGF certificate gap (vgf / vgfO)  = the SP1 stopping-rule cost:")
g = [r["vgf"]["W"] / r["vgfO"]["W"] for r in J
     if r["vgfO"]["W"] > 0 and r["vgf"]["W"] == r["vgf"]["W"]]
print("   median %.2f  max %.2f" % (float(np.median(g)), float(np.max(g))))
print()
print("How often is each mechanism the best?  (cells: %d)" % len(J))
cnt = {m: 0 for m in MECH}
for r in J:
    b = min(MECH, key=lambda m: r[m]["We"] if r[m]["We"] == r[m]["We"]
            else 1e300)
    cnt[b] += 1
print("  ", cnt)
print()
print("VGF vs push and vs composed, worst-case ratio over the 45 cells:")
for other in ("push", "composed"):
    rat = [r["vgf"]["We"] / r[other]["We"] for r in J if r[other]["We"] > 0]
    print("   vgf/%-9s median %.2f   max %.2f   min %.4f"
          % (other, float(np.median(rat)), float(np.max(rat)),
             float(np.min(rat))))

print()
print("=" * 100)
print("MECHANISM alpha-exponent: fit  W/vol(S_eps) ~ alpha^-q   (q=0 <=> ALPHA-FREE)")
print("%-10s |" % "family", " ".join("%-9s" % m for m in MECH))
qs = {m: [] for m in MECH}
for fam, rs in byf.items():
    rs.sort(key=lambda r: -r["alpha"])
    line = "%-10s |" % fam
    for mm in MECH:
        x = np.log([r["alpha"] for r in rs])
        y = np.log([r[mm]["W"] / max(r["volS"], 1) for r in rs])
        q = -np.polyfit(x, y, 1)[0]
        qs[mm].append(q)
        line += " %+8.3f" % q
    print(line)
print("%-10s |" % "MEDIAN", " ".join("%+8.3f " % float(np.median(qs[m]))
                                     for m in MECH))
print("%-10s |" % "MAX", " ".join("%+8.3f " % float(np.max(qs[m]))
                                  for m in MECH))
