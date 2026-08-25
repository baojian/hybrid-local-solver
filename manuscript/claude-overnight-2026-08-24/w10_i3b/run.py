"""I3-B driver: growing-support APCG with several boundary-reporting
structures observing the SAME trajectory, each with its own meter.

Control flow is driven by the canonical (eager_pull) semantics: at a poll,
whoever violates is admitted.  All structures see identical trajectories and
identical admissions, so their gate meters are directly comparable.
Correctness is asserted exhaustively at every poll against a dense
recomputation of G_j for all j in N(S).
"""
import json
import math
import os
import random
import sys
import time

import numpy as np
import scipy.sparse as sp

sys.path.insert(0, "/home/claude/work/overnight/w3_apcg")
sys.path.insert(0, "/home/claude/work/overnight/lib")
sys.path.insert(0, "/home/claude/work/overnight/w10_i3b")

from solvers import Model, Restricted, exact_support_solver   # noqa: E402
from meter import Meter                                       # noqa: E402
import gate as G                                              # noqa: E402


def boundary_matrix(R):
    """Sparse |B| x |S| matrix of Q_{j i} for exhaustive verification."""
    rows, cols, vals = [], [], []
    for t, row in enumerate(R.Brows):
        for (i, q) in row:
            rows.append(t); cols.append(i); vals.append(q)
    return sp.csr_matrix((vals, (rows, cols)),
                         shape=(len(R.Bnodes), R.n))


def apcg_segment(R, meter_int, gates, rng, delta=0.1, poll_every=None,
                 max_iter=None, state=None, verify_stride=1, flush_at=1e-120):
    """One fixed-support APCG segment with boundary reporting.
    Returns dict(status, admit, x, iters, state)."""
    n = R.n
    sigma = R.sigma
    a = math.sqrt(sigma) / n
    na = n * a
    r = (1.0 - a) / (1.0 + a)
    cp = 0.5 * (na + 1.0)
    cm = 0.5 * (na - 1.0)
    tstep = 1.0 / (na * R.c)
    if max_iter is None:
        max_iter = int(60.0 * n / math.sqrt(sigma)) + 40 * n
    if poll_every is None:
        poll_every = n
    if state is not None:
        p, Mh, phi = state
    else:
        p, Mh, phi = [0.0] * n, [0.0] * n, 1.0
    b, lam, nbr, c = R.b, R.lam, R.nbr, R.c
    target = delta * R.arho
    QBS = boundary_matrix(R)
    Bb = np.array(R.Bb); Bsqd = np.array(R.Bsqd)
    true_viol = {gs.name: set() for gs in gates}
    k = 0
    status = "cap"
    admit = []
    while k < max_iter:
        i = rng.randrange(n)
        rphi = r * phi
        pi_, mi = p[i], Mh[i]
        yi = pi_ + rphi * mi
        g = c * yi - b[i]
        for (jj, q) in nbr[i]:
            g += q * (p[jj] + rphi * Mh[jj])
        zh = pi_ - rphi * mi
        u = zh - tstep * g
        thr = tstep * lam[i]
        zn = u - thr if u > thr else (u + thr if u < -thr else 0.0)
        dlt = zn - zh
        phi = rphi
        dp = dMh = 0.0
        if dlt != 0.0:
            dp = cp * dlt
            dMh = cm * dlt / phi
            p[i] = pi_ + dp
            Mh[i] = mi + dMh
        meter_int.scan(R.S[i])
        for gs in gates:
            gs.note_update(i, dp, dMh, phi)
        k += 1
        if phi < flush_at:
            for t in range(n):
                Mh[t] *= phi
            for gs in gates:
                gs.note_flush(phi)
            phi = 1.0
            meter_int.rec(n)
        if k % poll_every == 0:
            x = np.asarray(p) + phi * np.asarray(Mh)
            reports = {}
            for gs in gates:
                reports[gs.name] = gs.poll(k, phi, x)
            if (k // poll_every) % verify_stride == 0 or any(reports.values()):
                Gv = (Bb - QBS @ x) / Bsqd
                for gs in gates:
                    now = {R.Bnodes[t]
                           for t in np.nonzero(Gv > gs.thr)[0]}
                    true_viol[gs.name] |= now
                    miss = now - gs.reported
                    assert not miss, (gs.name, "MISSED", sorted(miss)[:5], k)
                    bad = gs.reported - true_viol[gs.name]
                    assert not bad, (gs.name, "FALSE", sorted(bad)[:5], k)
            ctrl = gates[0]
            if ctrl.reported:
                new = sorted(ctrl.reported - set(admit))
                if new:
                    admit = sorted(ctrl.reported)
                    x = np.asarray(p) + phi * np.asarray(Mh)
                    return dict(status="admit", admit=admit, x=x, iters=k,
                                state=(p, Mh, phi))
            if k % n == 0:
                # stop-check on its own (standard) schedule, independent of
                # the gate poll schedule
                meter_int.rec(R.n + R.vol)
                h, sym, F = R.eval(x)
                if h <= target and sym <= target:
                    status = "ok"
                    break
    x = np.asarray(p) + phi * np.asarray(Mh)
    return dict(status=status, admit=[], x=x, iters=k, state=(p, Mh, phi))


def grow_run(model, rho, struct_names, mults=None, poll_every_mode="n",
             delta=0.1, seed=0, verify_stride=1, max_seg=400,
             max_iter_cap=None):
    """Growing-support APCG.  Returns per-structure gate ledgers."""
    rng = random.Random(seed)
    lam = model.alpha * rho * model.sqd
    S = sorted({int(i) for i in np.nonzero(model.s)[0]
                if model.b[i] > lam[i]})
    assert S, "empty seed support"
    mults = mults or {}
    ledgers = {nm: Meter(model.adj) for nm in struct_names}
    meter_int = Meter(model.adj)
    prev_S = set()
    stats = {nm: dict(wakeups=0, false_wakeups=0, piggy=0, sweeps=0)
             for nm in struct_names}
    state = None
    segs = 0
    admissions = 0
    t0 = time.time()
    while segs < max_seg:
        segs += 1
        R = Restricted(model, rho, S, boundary=True)
        R.arho = model.alpha * rho
        gates = []
        for nm in struct_names:
            gs = G.STRUCTURES[nm](R, ledgers[nm], mults.get(nm, 1.0))
            # incremental init charge for push structures: rescan of the
            # NEWLY admitted interior vertices only (d_i each), which the
            # interior solver already pays at admission.
            if isinstance(gs, G.PushGate):
                newv = [v for v in S if v not in prev_S]
                ledgers[nm].rec(sum(int(model.d[v]) for v in newv))
            gates.append(gs)
        prev_S = set(S)
        if state is None:
            st0 = ([0.0] * R.n, [0.0] * R.n, 1.0)
        else:
            st0 = state
        for gs in gates:
            if isinstance(gs, G.PushGate):
                gs.init_state(st0[0], st0[1], st0[2])
        pe = R.n if poll_every_mode == "n" else 1
        mi = max_iter_cap
        for gs in gates:
            gs.reported = set()
        res = apcg_segment(R, meter_int, gates, rng, delta=delta,
                           poll_every=pe, state=state,
                           verify_stride=verify_stride, max_iter=mi)
        for gs in gates:
            st = stats[gs.name]
            st["wakeups"] += gs.wakeups
            st["false_wakeups"] += gs.false_wakeups
            st["piggy"] += gs.piggy
            st["sweeps"] += gs.sweeps
        state = res["state"]
        if res["status"] == "admit":
            adm = res["admit"]
            admissions += len(adm)
            S = sorted(set(S) | set(adm))
            # carry mode: append zeros for the new coordinates
            p, Mh, phi = state
            gl = {g_: kk for kk, g_ in enumerate(R.S)}
            newp, newMh = [], []
            for g_ in S:
                if g_ in gl:
                    newp.append(p[gl[g_]]); newMh.append(Mh[gl[g_]])
                else:
                    newp.append(0.0); newMh.append(0.0)
            state = (newp, newMh, phi)
            continue
        break
    Rf = Restricted(model, rho, S, boundary=True)
    out = dict(S=S, vol_S=Rf.vol, nb=len(Rf.Bnodes),
               vol_B=int(sum(Rf.Bdeg)), segs=segs, admissions=admissions,
               iters_total=None, interior=meter_int.vector(),
               wall=time.time() - t0, status=res["status"])
    out["gates"] = {nm: dict(total=ledgers[nm].total(),
                             vec=ledgers[nm].vector(),
                             **stats[nm])
                    for nm in struct_names}
    return out


# ---------------------------------------------------------------- families

def ring_star(m=60, hub_deg=48):
    edges = [(0, k) for k in range(1, m + 1)]
    nid = m + 1
    hubs = []
    for k in range(1, m + 1):
        hub = nid; nid += 1
        edges.append((k, hub))
        for _ in range(hub_deg - 1):
            edges.append((hub, nid)); nid += 1
        hubs.append(hub)
    adj = {u: set() for u in range(nid)}
    for u, v in edges:
        adj[u].add(v); adj[v].add(u)
    return {u: sorted(adj[u]) for u in range(nid)}, 0, hubs


def tune_rho_ring(adj, seed, alpha, hubs, target_rel=0.95, iters=26):
    """Bisect rho so every hub sits just BELOW activation."""
    mdl = Model(adj, alpha, seed)

    def probe(r):
        xs, S = exact_support_solver(mdl, r)
        grad = mdl.Q @ xs - mdl.b
        lam = alpha * r * mdl.sqd
        rels = [float(-grad[h] / lam[h]) for h in hubs]
        nin = sum(1 for h in hubs if h in set(S))
        return nin == 0, max(rels), len(S)

    lo, hi = 1e-8, 0.5
    ok_hi, _, _ = probe(hi)
    if not ok_hi:
        return hi, probe(hi)[1]
    for _ in range(iters):
        mid = math.sqrt(lo * hi)
        if probe(mid)[0]:
            hi = mid
        else:
            lo = mid
    r = hi
    for _ in range(80):
        ok, rel, _ = probe(r)
        if ok and rel <= target_rel:
            return r, rel
        r *= 1.01
    return r, probe(r)[1]
