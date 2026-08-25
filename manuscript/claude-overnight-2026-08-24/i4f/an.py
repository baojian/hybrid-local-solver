import json, math, numpy as np, sys
OUT="/home/claude/work/overnight/i4f/out"
def fit(xs, ys):
    xs=np.log(np.array(xs)); ys=np.log(np.array(ys))
    if len(xs)<2: return float('nan'), float('nan')
    A=np.vstack([xs, np.ones_like(xs)]).T
    s,i = np.linalg.lstsq(A, ys, rcond=None)[0]
    return float(s), float(math.exp(i))

def sec1():
    rows=json.load(open(f"{OUT}/amp1.json"))
    print("### A_real = (1-c) err/theta  (=1 => repo certificate exactly right; "
          "1/A = over-charge factor).  eps=1e-5")
    kinds=["opt","ball","ista","cheb"]
    fams=sorted(set(r["fam"] for r in rows))
    print("%-12s %-6s | %s" % ("family","kind"," ".join("a=2^%-3d"%int(round(math.log2(a))) for a in [2**-2,2**-4,2**-6,2**-8,2**-10,2**-12])),
          "| slope p in A~alpha^p")
    for f in fams:
        for k in kinds:
            rs=[r for r in rows if r["fam"]==f and r["kind"]==k]
            if not rs: continue
            rs.sort(key=lambda r:-r["alpha"])
            cells=" ".join("%7.4g"%r["A"] for r in rs)
            p,_=fit([r["alpha"] for r in rs],[max(r["A"],1e-16) for r in rs])
            print("%-12s %-6s | %-52s | %.3f"%(f,k,cells,p))
    print()
    bad=[r for r in rows if not r.get("sound",True)]
    print("SOUNDNESS of the sharp bound Ahat(T) >= A_real:  violations = %d / %d"%(len(bad),len(rows)))
    inT=[r for r in rows if "argmax_in_T" in r]
    print("max_i G_i attained inside T (max principle):     %d / %d"%(sum(1 for r in inT if r["argmax_in_T"]),len(inT)))

def sec2():
    rows=json.load(open(f"{OUT}/cert2.json"))
    print("\n### support-conditional sharp constant A_sharp(T) vs realized A_real vs "
          "max-principle A_mp,  xhat = exact solve on S_eps (ring residual)")
    print("%-12s %-7s %-6s %8s %9s %8s %8s %7s"%("family","alpha","nT","A_real","A_sharp","A_mp","A_l1","sqrt(a)"))
    for r in rows:
        print("%-12s 2^%-5.0f %-6d %8.4g %9.4g %8.3f %8.3g %7.4g"%(
            r["fam"],math.log2(r["alpha"]),r["nT"],r["A_real"],r["A_sharp"],r["A_mp"],r["A_l1"],r["sqrt_a"]))
    print("\nmax-principle bound A_mp over all cells: min=%.3f max=%.3f  "
          "(>= 1/2 always => at best a 2x improvement)  CONFIRMS I3-A"%(
        min(r["A_mp"] for r in rows), max(r["A_mp"] for r in rows)))
    print("\n### K-term Neumann (candidate c): Ahat_K, and K needed to reach 2x of A_sharp")
    print("%-12s %-7s %9s %9s | %s"%("family","alpha","A_sharp","A_real"," ".join("K=%-4d"%k for k in [1,4,16,64,256,512])))
    for r in rows:
        nu=r["neumann"]
        cells=" ".join("%6.3g"%nu[str(k)][0] if str(k) in nu else "   -  " for k in [1,4,16,64,256,512])
        print("%-12s 2^%-5.0f %9.4g %9.4g | %s"%(r["fam"],math.log2(r["alpha"]),r["A_sharp"],r["A_real"],cells))

def sec4():
    rows=json.load(open(f"{OUT}/esc4.json"))
    rows=[r for r in rows if r["kind"]=="opt"]
    print("\n### (e) profile localized supersolution: Ahat_e(K) and charged read cost vol(Omega_K)")
    KS=[0,1,2,4,8,16,32,64,128]
    print("%-12s %-7s %8s %8s | %s"%("family","alpha","A_real","1/sqrt(a)"," ".join("K=%-3d"%k for k in KS)))
    for r in rows:
        cv=r["curve"]
        cells=" ".join("%5.3g"%cv[str(k)][0] if str(k) in cv else "  -  " for k in KS)
        print("%-12s 2^%-5.0f %8.4g %8.1f | %s"%(r["fam"],math.log2(r["alpha"]),r["A_real"],1/r["sqrt_a"],cells))
    print("\nK* = smallest K with Ahat_e(K) <= 2*A_real ;  cost = vol(Omega_K*) / vol(S_eps)")
    print("%-12s %-7s %8s %6s %8s %10s"%("family","alpha","A_real","K*","K*sqrt(a)","volOm/volSe"))
    for r in rows:
        cv=r["curve"]; ks=sorted(int(k) for k in cv)
        star=None
        for k in ks:
            if cv[str(k)][0] <= 2*r["A_real"]+1e-12: star=k; break
        if star is None:
            print("%-12s 2^%-5.0f %8.4g %6s %8s %10s"%(r["fam"],math.log2(r["alpha"]),r["A_real"],">%d"%ks[-1],"-","-"))
        else:
            print("%-12s 2^%-5.0f %8.4g %6d %8.2f %10.2f"%(r["fam"],math.log2(r["alpha"]),r["A_real"],
                  star, star*r["sqrt_a"], cv[str(star)][1]/max(r["volSe"],1)))
    bad=[r for r in rows if not r["sound"]]
    print("\nSOUNDNESS of (e) [Ahat_e(K) >= A_real for every K, every cell]: violations = %d / %d"%(len(bad),len(rows)))

def sec3():
    try: rows=json.load(open(f"{OUT}/tax3.json"))
    except Exception as e: print("\n(tax3 not ready)",e); return
    print("\n### CERTIFICATE TAX: region method (exact restricted solve on BFS ball)")
    print("%-11s %-7s %6s %6s %6s | %9s %9s %7s %7s"%("family","alpha","R_cert","R_shrp","R_orcl",
          "vol_cert","vol_orcl","tax","residual tax after (e)"))
    for r in rows:
        print("%-11s 2^%-5.0f %6s %6s %6s | %9.4g %9.4g %7s %7s"%(
            r["fam"],math.log2(r["alpha"]),r["ball_R_cert"],r["ball_R_sharp"],r["ball_R_oracle"],
            r["ball_vol_cert"] or float('nan'), r["ball_vol_oracle"] or float('nan'),
            ("%.2f"%r["ball_tax_vol"]) if r.get("ball_tax_vol") else "-",
            ("%.2f"%(r["ball_vol_sharp"]/r["ball_vol_oracle"])) if (r.get("ball_vol_sharp") and r.get("ball_vol_oracle")) else "-"))

for f in (sec1, sec2, sec4, sec3):
    try: f()
    except Exception as e: print("SECTION FAIL", f.__name__, e)
