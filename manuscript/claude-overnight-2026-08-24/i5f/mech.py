"""I5-F mechanisms with pluggable stopping: repo (Tier 0) / (e') (Tier 1) /
oracle.  AMG body adapted from i3a_amg/amglib.amg_local (unchanged charging);
elimination adapted from direct_local; lattice MG driven through i2f
gridlib.mg_local as a fixed-region ladder."""
import math, sys, time
import numpy as np
import scipy.sparse.linalg as spla

sys.path.insert(0, "/home/claude/work/overnight/lib")
sys.path.insert(0, "/home/claude/work/overnight/i3a_amg")
import cert
from amglib import Explorer, build_hierarchy, v_cycle


def amg_eprime(model, eps, meter, x_exact=None, nu1=2, nu2=2, max_cycles=40,
               theta=0.25, max_coarse=40, stall=0.6, stall_win=2, warm=True,
               rseed=0, wall_cap=240.0, grow=1.5, ext="sc"):
    """amg_local with the (e') stopping rule.  Policy: each cycle first try
    the free repo rule; once the interior residual is dominated by the
    boundary floor (c_in <= 0.3 c_bd), evaluate (e') once (charged); if it
    fails, grow the region.  Every (e') evaluation is soundness-asserted
    against x_exact when given."""
    alpha = model.alpha
    target = alpha * eps
    rng = np.random.default_rng(rseed)
    ex = Explorer(model, meter)
    Q, sqd, b = model.Q, model.sqd, model.b
    xg = np.zeros(model.n)
    t_start = time.perf_counter()
    R = 0
    volprev = 0.0
    exhausted = False
    tot_cycles = 0
    attempts = 0
    ecost = 0.0
    necert = 0
    Aexp = math.sqrt(alpha)          # expected amplification; adapted online
    while True:
        if time.perf_counter() - t_start > wall_cap:
            return dict(x=xg, status="cap", volOmega=volprev, ecost=ecost,
                        necert=necert, attempts=attempts)
        while True:
            R += 1
            if not ex.grow_to(R + 1):
                exhausted = True
                R = min(R, ex.r)
                break
            if ex.ballvol(R) >= grow * volprev:
                break
        meter.phase("setup")
        S = ex.ball(R)
        if S.size == 0:
            break
        volprev = float(model.d[S].sum())
        bd = np.setdiff1d(ex.ball(R + 1), S, assume_unique=False)
        if bd.size:
            meter.ring_scan(bd)
        meter.scan_idx(S)
        AS = Q[S][:, S].tocsr()
        fS = b[S].copy()
        volS = float(model.d[S].sum())

        def level0_scan(k, _S=S):
            for _ in range(int(round(k))):
                meter.scan_idx(_S)

        levels, linfo = build_hierarchy(AS, sqd[S].copy(), meter, level0_scan,
                                        theta=theta, max_coarse=max_coarse,
                                        rng=rng, smooth=True,
                                        rho0=2.0 / (1.0 + alpha), vol0=volS)
        Xb = Q[bd][:, S].tocsr() if bd.size else None
        meter.phase("solve")
        xS = np.zeros(S.size)
        if warm and xg.any():
            xS[:] = xg[S]
            meter.rec(float(S.size))
        cyc = 0
        best = math.inf
        stall_ct = 0
        prev = None
        tried_e = False
        while cyc < max_cycles:
            v_cycle(levels, 0, xS, fS, meter, level0_scan, nu1, nu2)
            cyc += 1
            tot_cycles += 1
            level0_scan(1)
            rin = fS - AS @ xS
            c_in = float(np.max(np.abs(rin) / sqd[S]))
            if bd.size:
                meter.ring_scan(bd)
                c_bd = float(np.max(np.abs(-(Xb @ xS)) / sqd[bd]))
            else:
                c_bd = 0.0
            meter.rec(float(S.size + bd.size))
            cc = max(c_in, c_bd)
            if cc < target:                       # Tier 0 fires: free stop
                xg[:] = 0.0; xg[S] = xS
                return dict(x=xg, status="cert", tier=0, R=R, cycles=cyc,
                            volOmega=volS, ecost=ecost, necert=necert,
                            attempts=attempts + 1, tot_cycles=tot_cycles)
            # Tier 1: interior converged relative to the boundary floor,
            # AND the gate says certification is plausibly in range
            # (tier0/alpha * Aexp <= 2 eps); Aexp adapts to measured Ahat.
            gate_ok = cc / alpha * Aexp <= 2.0 * eps
            if (not tried_e) and cyc >= 2 and gate_ok and (
                    c_bd == 0.0 or c_in <= 0.3 * c_bd):
                tried_e = True
                xg[:] = 0.0; xg[S] = xS
                o = cert.certify_eprime(model, xg, exterior=ext, meter=meter,
                                        eps_target=eps)
                ecost += o["cost"]["total"]
                necert += 1
                if x_exact is not None:
                    e = float(np.max(np.abs(xg - x_exact) / sqd))
                    assert o["err_bound"] >= e * (1 - 1e-9), \
                        f"(e') VIOLATION in amg_eprime: {o['err_bound']} < {e}"
                Aexp = max(0.7 * o["err_bound"] / (cc / alpha), 1e-6)
                if o["err_bound"] <= eps:
                    return dict(x=xg, status="cert", tier=1, R=R, cycles=cyc,
                                volOmega=volS, ecost=ecost, necert=necert,
                                attempts=attempts + 1, tot_cycles=tot_cycles,
                                ebound=o["err_bound"], Kcert=o["K"],
                                volcert=o["volOmega"])
                if exhausted or S.size >= model.n:
                    tried_e = False    # terminal region: keep cycling, retry
                else:
                    break                          # region too small: grow
            if c_bd >= target and cyc >= 3 and (tried_e or not
                                                (cc / alpha * Aexp
                                                 <= 4.0 * eps)):
                break
            if cc < stall * best:
                best = cc; stall_ct = 0
            else:
                stall_ct += 1
                if stall_ct >= stall_win:
                    if (not tried_e) and cc / alpha * Aexp <= 2.0 * eps:
                        tried_e = True
                        xg[:] = 0.0; xg[S] = xS
                        o = cert.certify_eprime(model, xg, exterior=ext,
                                                meter=meter, eps_target=eps)
                        ecost += o["cost"]["total"]; necert += 1
                        Aexp = max(0.7 * o["err_bound"] / (cc / alpha), 1e-6)
                        if o["err_bound"] <= eps:
                            return dict(x=xg, status="cert", tier=1, R=R,
                                        cycles=cyc, volOmega=volS,
                                        ecost=ecost, necert=necert,
                                        attempts=attempts + 1,
                                        tot_cycles=tot_cycles)
                    break
        attempts += 1
        if warm:
            xg[:] = 0.0; xg[S] = xS
        if exhausted or S.size >= model.n:
            break
    return dict(x=xg, status="maxed", volOmega=volprev, ecost=ecost,
                necert=necert, attempts=attempts)


def direct3(model, eps, meter, mode, x_exact=None, wall_cap=90.0,
            max_nnz=4e7, ext="sc"):
    """Growing-ball exact elimination with stopping mode in
    {'repo','eprime','oracle'} — direct_local's ladder and charges."""
    alpha = model.alpha
    tgt = alpha * eps
    ex = Explorer(model, meter)
    Q, sqd, b = model.Q, model.sqd, model.b
    xg = np.zeros(model.n)
    t0 = time.perf_counter()
    R = 0; volprev = 0.0; exhausted = False
    ecost = 0.0; necert = 0
    Aexp = math.sqrt(alpha)
    while True:
        if time.perf_counter() - t0 > wall_cap:
            return dict(x=xg, status="cap", volOmega=volprev, ecost=ecost)
        while True:
            R += 1
            if not ex.grow_to(R + 1):
                exhausted = True; R = min(R, ex.r); break
            if ex.ballvol(R) >= 1.5 * volprev:
                break
        S = ex.ball(R)
        if S.size == 0:
            break
        volprev = float(model.d[S].sum())
        bd = np.setdiff1d(ex.ball(R + 1), S)
        if bd.size:
            meter.ring_scan(bd)
        meter.scan_idx(S)
        AS = Q[S][:, S].tocsc()
        lu = spla.splu(AS, permc_spec="MMD_AT_PLUS_A", diag_pivot_thresh=0.0,
                       options=dict(SymmetricMode=True))
        Lm = lu.L.tocsc()
        cnt = np.diff(Lm.indptr).astype(float)
        meter.resp(float(np.sum(cnt ** 2)))
        meter.mat(float(Lm.nnz + lu.U.nnz))
        xS = lu.solve(b[S])
        meter.resp(2.0 * float(Lm.nnz + lu.U.nnz))
        meter.scan_idx(S)
        rin = b[S] - AS @ xS
        c_in = float(np.max(np.abs(rin) / sqd[S]))
        if bd.size:
            meter.ring_scan(bd)
            c_bd = float(np.max(np.abs(-(Q[bd][:, S] @ xS)) / sqd[bd]))
        else:
            c_bd = 0.0
        meter.rec(float(S.size + bd.size))
        cc = max(c_in, c_bd)
        volS = float(model.d[S].sum())
        xg[:] = 0.0; xg[S] = xS
        if mode == "repo":
            ok = cc < tgt
        elif mode == "oracle":
            ok = float(np.max(np.abs(xg - x_exact) / sqd)) <= eps
        else:
            if cc < tgt:
                ok = True
            elif cc / alpha * Aexp > 2.0 * eps:
                ok = False              # gated: certification out of range
            else:
                o = cert.certify_eprime(model, xg, exterior=ext, meter=meter,
                                        eps_target=eps)
                ecost += o["cost"]["total"]; necert += 1
                if x_exact is not None:
                    e = float(np.max(np.abs(xg - x_exact) / sqd))
                    assert o["err_bound"] >= e * (1 - 1e-9), \
                        f"(e') VIOLATION in direct3: {o['err_bound']} < {e}"
                Aexp = max(0.7 * o["err_bound"] / (cc / alpha), 1e-6)
                ok = o["err_bound"] <= eps
        if ok:
            return dict(x=xg, status="cert", R=R, volOmega=volS, ecost=ecost,
                        necert=necert)
        xg[:] = 0.0
        if float(Lm.nnz) > max_nnz or exhausted or S.size >= model.n:
            return dict(x=xg, status="maxed", volOmega=volS, ecost=ecost)


def mg3_eprime(model, eps, meter, mg_local, ladder, x_exact, ext="sc"):
    """Lattice MG with (e') stopping, emulated as a fixed-region ladder over
    gridlib.mg_local calls (each charged on the same meter).  At each region
    size the interior is converged to the oracle target (then squeezed to
    eps/2, eps/4 if needed) and (e') is evaluated; failure grows the region.
    W is a slight over-charge of a native integration (restart per call)."""
    ecost = 0.0; necert = 0
    Aexp = math.sqrt(model.alpha)
    for m in ladder(model.w - 3, 2):
        for tt in (eps, eps / 2, eps / 4):
            res = mg_local(model, tt, meter, m0=m, mmax=m, x_exact=x_exact,
                           oracle=True)
            xh = res["x"]
            if not np.any(xh):
                break
            t0b = cert.certify_tier0(model, xh)
            if t0b * Aexp > 2.0 * eps:
                if res["status"] != "cert":
                    break
                continue                      # gated: squeeze further first
            o = cert.certify_eprime(model, xh, exterior=ext, meter=meter,
                                    eps_target=eps)
            ecost += o["cost"]["total"]; necert += 1
            e = float(np.max(np.abs(xh - x_exact) / model.sqd))
            assert o["err_bound"] >= e * (1 - 1e-9), \
                f"(e') VIOLATION in mg3: {o['err_bound']} < {e}"
            Aexp = max(0.7 * o["err_bound"] / t0b, 1e-6)
            if o["err_bound"] <= eps:
                return dict(x=xh, status="cert", m=m, ecost=ecost,
                            necert=necert, ebound=o["err_bound"])
            if res["status"] != "cert":
                break        # region cannot even reach the oracle target
    return dict(x=None, status="maxed", ecost=ecost, necert=necert)
