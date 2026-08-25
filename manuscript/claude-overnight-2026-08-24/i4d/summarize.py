"""Parse run_work.log / run_ridge.log into the I4-D tables (robust to a job
still running: the JSON is only written at the end)."""
import re, sys, math
import numpy as np
OUT = "/home/claude/work/overnight/i4d/out"

hdr = re.compile(r"^\[(E2|E3) ([\w\-]+)\]\s*(.*)$")
row = re.compile(r"^\s{2}(\w+)\s+W=([\d.eE+\-naif]+)\s+W\*eps=([\d.eE+\-naif]+)"
                 r"\s+W/vol=([\d.eE+\-naif]+)\s+err/eps=([\d.eE+\-naif]+)\s+(\S+)")
cells = []
cur = None
for ln in open(f"{OUT}/run_work.log"):
    m = hdr.match(ln)
    if m:
        cur = dict(kind=m.group(1), tag=m.group(2), info=m.group(3).strip(),
                   rows=[])
        cells.append(cur); continue
    m = row.match(ln)
    if m and cur is not None:
        try:
            cur["rows"].append(dict(mech=m.group(1), W=float(m.group(2)),
                                    Weps=float(m.group(3)),
                                    Wvol=float(m.group(4)),
                                    erat=float(m.group(5)), st=m.group(6)))
        except ValueError:
            pass

def volstar(info):
    m = re.search(r"vol\*eps=([\d.]+)", info)
    return float(m.group(1)) if m else float("nan")
def alph(info):
    m = re.search(r"a=2\^(-?[\d.]+)", info)
    return 2.0 ** float(m.group(1)) if m else float("nan")

print("=" * 118)
print("TOTAL CHARGED WORK at each family's OUTPUT-SATURATING cell "
      "(W*eps = 1  <=>  W = 1/eps exactly)")
print("%-16s %-30s %7s | %s" % ("cell", "params", "vol*eps",
      "W*eps per mechanism  (valid runs only; 'x'=err>eps or not certified)"))
print("-" * 118)
for c in cells:
    ok = [r for r in c["rows"] if r["erat"] <= 1.0 and
          not r["st"].startswith("skip") and np.isfinite(r["W"])]
    if not ok: 
        print("%-16s %-30s  (no valid run)" % (c["tag"], c["info"][:30])); continue
    best = min(ok, key=lambda r: r["W"])
    s = "  ".join("%s=%.4g%s" % (r["mech"], r["Weps"],
                  "" if r["st"] == "cert" else "!") for r in ok)
    a = alph(c["info"]); vs = volstar(c["info"])
    fy = 1.0 / math.sqrt(a) if np.isfinite(a) else float("nan")
    print("%-16s %-30s %7.3f | %s\n%18s BEST %s: W*eps=%.4g  =%.3gx output  "
          "=%.3g x (FY22 target/eps=%.4g)"
          % (c["tag"], c["info"][:30], vs, s, "", best["mech"], best["Weps"],
             best["Weps"] / vs if vs > 0 else float("nan"),
             best["Weps"] / fy if np.isfinite(fy) else float("nan"), fy))
print("=" * 118)
try:
    txt = open(f"{OUT}/run_ridge.log").read()
    print("\nRIDGE (output-saturating curve):")
    for ln in txt.splitlines():
        if "best W*eps" in ln or ln.startswith("=="):
            print(" ", ln.strip())
except FileNotFoundError:
    pass
