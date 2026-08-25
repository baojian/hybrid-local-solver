"""I5-F E4: tax-free headline table — W(repo) / W(e') / W(oracle) for three
mechanisms x representative families."""
import json, math, sys
import numpy as np
sys.path.insert(0, "/home/claude/work/overnight/lib")
sys.path.insert(0, "/home/claude/work/overnight/i3a_amg")
sys.path.insert(0, "/home/claude/work/overnight/i2f_grid")
import zoo, cert
from amglib import GModel, VecMeter, amg_local, support_stats
import mech

OUT = "/home/claude/work/overnight/i5f/out"
EPS = 1e-6
rows = []


def fit_s(sub):
    xs = np.array([-math.log2(r["alpha"]) for r in sub])
    for key in ("Wr", "We", "Wo"):
        ys = np.array([math.log2(r[key] / r["volS"]) for r in sub])
        yield key, float(np.polyfit(xs, ys, 1)[0])


def cell(mechname, fam, alpha, runs, volS):
    r = dict(mech=mechname, fam=fam, alpha=alpha, volS=volS, **runs)
    rows.append(r)
    print(f"{mechname:9s} {fam:11s} a=2^{int(math.log2(alpha))}: "
          f"W/vol repo {runs['Wr']/volS:8.0f}  e' {runs['We']/volS:8.0f} "
          f"(cert {runs['ecost']/volS:6.1f}, tier{runs.get('tier','?')})  "
          f"oracle {runs['Wo']/volS:8.0f}   tax r/o {runs['Wr']/runs['Wo']:.2f} "
          f"e/o {runs['We']/runs['Wo']:.2f}", flush=True)


def amg_family(fam, gens):
    for alpha, (adj, seed) in gens:
        m = GModel(adj, alpha, seed)
        x0 = m.solve_exact()
        st = support_stats(m, EPS)
        volS = max(st["volS"], 1.0)
        mt = VecMeter(m.d); ra = amg_local(m, EPS, mt, wall_cap=120)
        Wr = mt.total()
        assert ra["status"] != "cert" or m.semantic_err(ra["x"]) <= EPS
        mt = VecMeter(m.d)
        ro = amg_local(m, EPS, mt, oracle=True, x_exact=x0, wall_cap=120)
        Wo = mt.total()
        mt = VecMeter(m.d)
        re = mech.amg_eprime(m, EPS, mt, x_exact=x0, wall_cap=120)
        We = mt.total()
        if re["status"] == "cert":
            e = float(np.max(np.abs(re["x"] - x0) / m.sqd))
            assert e <= EPS, f"e'-stopped AMG err {e} > eps"
        runs = dict(Wr=Wr, We=We, Wo=Wo, ecost=re.get("ecost", 0.0),
                    tier=re.get("tier"),
                    st=(ra["status"], re["status"], ro["status"]))
        cell("AMG", fam, alpha, runs, volS)


def main():
    import run_zoo_helpers as H  # noqa  (not present; inline generators)


if __name__ == "__main__":
    sys.path.insert(0, "/home/claude/work/overnight/i3a_amg")
    from run_zoo import fast_grid

    print("== (a) local AMG ==")
    amg_family("grid2d", [(2**-4, fast_grid(141, 141)),
                          (2**-6, fast_grid(201, 201)),
                          (2**-8, fast_grid(301, 301))])
    amg_family("caterpillar", [(2**-6, zoo.caterpillar(3000, 1)),
                               (2**-8, zoo.caterpillar(3000, 1)),
                               (2**-10, zoo.caterpillar(3000, 1))])
    amg_family("rand_reg3", [(2**-4, zoo.random_regular(20000, 3)),
                             (2**-6, zoo.random_regular(20000, 3)),
                             (2**-8, zoo.random_regular(20000, 3))])

    print("== (c) local elimination ==")
    for fam, gen in (("caterpillar", lambda: zoo.caterpillar(6000, 1)),
                     ("comb", lambda: zoo.caterpillar(2500, 6)),
                     ("spider", lambda: zoo.spider(6, 2500))):
        for alpha in (2**-6, 2**-8, 2**-10, 2**-12):
            adj, seed = gen()
            m = GModel(adj, alpha, seed)
            x0 = m.solve_exact()
            st = support_stats(m, EPS)
            volS = max(st["volS"], 1.0)
            mt = VecMeter(m.d)
            rr = mech.direct3(m, EPS, mt, "repo"); Wr = mt.total()
            mt = VecMeter(m.d)
            ro = mech.direct3(m, EPS, mt, "oracle", x_exact=x0)
            Wo = mt.total()
            mt = VecMeter(m.d)
            re = mech.direct3(m, EPS, mt, "eprime", x_exact=x0)
            We = mt.total()
            if re["status"] == "cert":
                assert float(np.max(np.abs(re["x"] - x0) / m.sqd)) <= EPS
            runs = dict(Wr=Wr, We=We, Wo=Wo, ecost=re.get("ecost", 0.0),
                        tier=1,
                        st=(rr["status"], re["status"], ro["status"]))
            cell("ELIM", fam, alpha, runs, volS)

    print("== (b) lattice MG (i2f) ==")
    import gridlib
    for alpha, w in ((2**-6, 201), (2**-8, 301), (2**-10, 451)):
        m = gridlib.LatticeModel(w, alpha, dim=2)
        x0 = m.solve_exact()
        st = gridlib.support_stats(m, EPS)
        volS = max(st["volS"], 1.0)
        mt = gridlib.VecMeter(m.d)
        rr = gridlib.mg_local(m, EPS, mt); Wr = mt.total()
        mt = gridlib.VecMeter(m.d)
        ro = gridlib.mg_local(m, EPS, mt, x_exact=x0, oracle=True)
        Wo = mt.total()
        mt = gridlib.VecMeter(m.d)
        re = mech.mg3_eprime(m, EPS, mt, gridlib.mg_local, gridlib.ladder, x0)
        We = mt.total()
        if re["status"] == "cert":
            assert float(np.max(np.abs(re["x"] - x0) / m.sqd)) <= EPS
        runs = dict(Wr=Wr, We=We, Wo=Wo, ecost=re.get("ecost", 0.0),
                    tier=1,
                    st=(rr["status"], re["status"], ro["status"]))
        cell("MG-lat", "grid2d", alpha, runs, volS)

    json.dump(rows, open(f"{OUT}/headline.json", "w"))
    print("\n== exponents s of W/vol(S) ~ alpha^-s ==")
    for mn in ("AMG", "ELIM", "MG-lat"):
        for fam in sorted({r["fam"] for r in rows if r["mech"] == mn}):
            sub = [r for r in rows if r["mech"] == mn and r["fam"] == fam]
            if len(sub) >= 2:
                ss = dict(fit_s(sub))
                print(f"{mn:8s} {fam:11s}: s_repo {ss['Wr']:+.2f}  "
                      f"s_e' {ss['We']:+.2f}  s_oracle {ss['Wo']:+.2f}")
    print(f"\ncert soundness checks this run: {cert.SOUND_CHECKS}, "
          f"violations {len(cert.VIOLATIONS)}")
