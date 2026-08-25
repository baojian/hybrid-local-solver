"""I3-B experiments: gate structures on the adversarial ring and the benign
families, at two poll schedules."""
import json
import math
import sys
import time

import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/w3_apcg")
sys.path.insert(0, "/home/claude/work/overnight/lib")
sys.path.insert(0, "/home/claude/work/overnight/w10_i3b")

import run as RR                                  # noqa: E402
from solvers import Model, Restricted, exact_support_solver   # noqa: E402
import zoo                                        # noqa: E402

NAMES = ["eager_pull", "eager_push", "lazy_bound", "kinetic", "deg_bucket"]


def star_ref(model, rho):
    xs, S = exact_support_solver(model, rho)
    R = Restricted(model, rho, S, boundary=True)
    return dict(vol_S=R.vol, nS=len(S), nB=len(R.Bnodes),
                vol_B=int(sum(R.Bdeg)))


def one(model, rho, mult, poll_mode, seed=1, vstride=1, cap=None):
    mults = {nm: mult for nm in NAMES}
    out = RR.grow_run(model, rho, NAMES, mults=mults,
                      poll_every_mode=poll_mode, seed=seed,
                      verify_stride=vstride, max_iter_cap=cap)
    return out


def ring_experiment(path_out):
    res = []
    for alpha_e in (8, 10, 12):
        alpha = 2.0 ** -alpha_e
        for D in (12, 48, 192, 384):
            t0 = time.time()
            adj, seed, hubs = RR.ring_star(m=60, hub_deg=D)
            rho, rel = RR.tune_rho_ring(adj, seed, alpha, hubs,
                                        target_rel=0.95, iters=24)
            mdl = Model(adj, alpha, seed)
            ref = star_ref(mdl, rho)
            for poll_mode, vs in (("n", 1), ("1", 20)):
                o = one(mdl, rho, 8.0, poll_mode, seed=1, vstride=vs)
                rec = dict(fam="ring", alpha=alpha, alpha_e=alpha_e, D=D,
                           rho=rho, rel=rel, poll=poll_mode, mult=8.0,
                           ref=ref, tune_s=time.time() - t0, **{
                               k: o[k] for k in
                               ("vol_S", "nb", "vol_B", "segs", "admissions",
                                "status", "wall")})
                rec["gates"] = {nm: o["gates"][nm]["total"] for nm in NAMES}
                rec["gvec"] = {nm: o["gates"][nm]["vec"] for nm in NAMES}
                rec["interior"] = o["interior"]["total"]
                res.append(rec)
                print(json.dumps({k: rec[k] for k in
                                  ("alpha_e", "D", "poll", "vol_S", "vol_B",
                                   "admissions", "gates", "interior",
                                   "status")}), flush=True)
            json.dump(res, open(path_out, "w"), indent=1)
    return res


def benign_experiment(path_out):
    fams = {}
    a, s = zoo.path(800); fams["path"] = (a, s, 1.0 / 3200)
    a, s = zoo.caterpillar(300, 1); fams["caterpillar"] = (a, s, 1.0 / 2400)
    a, s = zoo.spider(6, 100); fams["spider"] = (a, s, 1.0 / 2400)
    a, s = zoo.grid(24, 24); fams["grid"] = (a, s, 1.0 / 2400)
    a, s = zoo.binary_tree(9); fams["btree"] = (a, s, 1.0 / 2400)
    res = []
    for alpha_e in (8, 12):
        alpha = 2.0 ** -alpha_e
        for fam, (adj, seed, rho) in fams.items():
            mdl = Model(adj, alpha, seed)
            ref = star_ref(mdl, rho)
            for poll_mode, vs in (("n", 1), ("1", 20)):
                t0 = time.time()
                o = one(mdl, rho, 1.0, poll_mode, seed=1, vstride=vs)
                rec = dict(fam=fam, alpha=alpha, alpha_e=alpha_e, rho=rho,
                           poll=poll_mode, mult=1.0, ref=ref,
                           **{k: o[k] for k in
                              ("vol_S", "nb", "vol_B", "segs", "admissions",
                               "status", "wall")})
                rec["gates"] = {nm: o["gates"][nm]["total"] for nm in NAMES}
                rec["interior"] = o["interior"]["total"]
                res.append(rec)
                print(json.dumps({k: rec[k] for k in
                                  ("fam", "alpha_e", "poll", "vol_S", "vol_B",
                                   "admissions", "gates", "interior",
                                   "status", "wall")}), flush=True)
                json.dump(res, open(path_out, "w"), indent=1)
    return res


if __name__ == "__main__":
    which = sys.argv[1]
    if which == "ring":
        ring_experiment("/home/claude/work/overnight/w10_i3b/res_ring.json")
    elif which == "benign":
        benign_experiment("/home/claude/work/overnight/w10_i3b/res_benign.json")
