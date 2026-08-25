import json, math
import numpy as np
J = json.load(open("out/zoo.json"))
byf = {}
for r in J:
    byf.setdefault(r["tag"].split(" a=")[0], []).append(r)
print("REGION INFLATION:  vol(S_VGF)/vol(S_eps)  and  vol(S_cert)/vol(S_eps)")
print("(the sound gate admits down to gamma*eps, so the region is S_{gamma eps})")
print("%-10s | %-24s | %-24s | %-8s" % ("family", "vol(S_VGF)/vol(S_eps)",
                                        "vol(S_VGFO)/vol(S_eps)", "infl exp"))
allr, allq = [], []
for fam, rs in byf.items():
    rs.sort(key=lambda r: -r["alpha"])
    a = np.log([r["alpha"] for r in rs])
    rv = [r["vgf_vol"] / max(r["volS"], 1) for r in rs]
    ov = [r["vgfO_vol"] / max(r["volS"], 1) for r in rs]
    q = -np.polyfit(a, np.log(rv), 1)[0]
    # work per unit of the region actually solved (pure mechanism, self-cert)
    wq = -np.polyfit(a, np.log([r["vgf"]["W"] / r["vgf_vol"] for r in rs]),
                     1)[0]
    allr.append(q); allq.append(wq)
    print("%-10s | %6.2f %6.2f %6.2f    | %6.2f %6.2f %6.2f    | %+.3f  "
          "W/volReg exp %+.3f" % (fam, rv[0], rv[1], rv[2], ov[0], ov[1],
                                  ov[2], q, wq))
print("MEDIAN region-inflation alpha-exponent : %+.3f" % float(np.median(allr)))
print("MEDIAN W/vol(S_VGF) alpha-exponent     : %+.3f  (max %+.3f)"
      % (float(np.median(allq)), float(np.max(allq))))
print()
print("ROUNDS (alpha-free cycle count?)  R at a=2^-4/-8/-12, and vol(S_VGF)")
for fam, rs in byf.items():
    rs.sort(key=lambda r: -r["alpha"])
    print("  %-10s R=%s  vol=%s" % (fam, "/".join(str(r["vgf_R"]) for r in rs),
                                    "/".join("%.0f" % r["vgf_vol"] for r in rs)))
