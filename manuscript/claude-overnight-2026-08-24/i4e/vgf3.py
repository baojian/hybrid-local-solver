"""I5-B  VGF-SP3: incremental solves across rounds + (e') certificate.

Replaces I4-E vgf_local's per-round FULL re-solve + FULL re-scan with:

  * cached region rows: each admitted row is scanned once (C_adj); every
    re-read (band assembly, residual update) is charged as a repeat via
    scan_idx (R_adj) -- same convention, but now only BAND rows repeat,
    never all of S.
  * a maintained one-signed residual r = b - Q x on S (r >= 0 throughout:
    x is always a subsolution; every solve is a Dirichlet solve on a band
    with frozen complement, which zeroes r on the band and only increases
    it elsewhere).  Between sweeps nothing is rebuilt.
  * BAND solves: the active set {i : r_i/sqd_i >= zeta*alpha*eps} (tracked
    by a dirty set -- no per-round scan of S) is solved exactly with the
    complement frozen.  This subsumes both the old "full solve" and the
    old "extension solve": per-sweep cost is O(vol(touched)), not O(vol(S)).
  * incremental value bounds: ulb lifts are pushed to the ring accumulators
    (kinetic-gate style) edge by edge; acc[y] == sum_{w in S, w~y} ulb[w]
    exactly at all times, so Lo(h) = c_a*acc[h]/d_h is both the admission
    key and a SOUND upper bound on the true ring residual (x/sqd <= ulb).
  * optional (e') early stop (I4-F): when every remaining ring value is
    below c_e*eps, build the profile-localized supersolution on
    Omega_K = B_K(supp psi), K = ceil(4/sqrt(alpha)) (volume-capped), and
    stop if the SOUND error bound max_T Ghat < eps.  All reads charged
    (rows outside S pay first exposure), factorisation charged as LDL.

Soundness carried over from I4-E Lemmas V1-V3 unchanged: ulb <= u always
(frozen Dirichlet data is a lower bound; M-matrix comparison), admitted
region is contained in {v : u_v >= theta*gamma*eps} u {seed}, and the
certificate implies err <= eps (repository implication, or (e') by the
maximum-principle supersolution).
"""
import heapq
import math
import sys
import time

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

sys.path.insert(0, "/home/claude/work/overnight/i3a_amg")
sys.path.insert(0, "/home/claude/work/overnight/i4e")
from amglib import _nbrs  # noqa
from vgf import _region_solve, _lg  # noqa


def _echeck(model, meter, inS, r_int, Sarr, acc, eps, cap_vol, Kmax):
    """(e') profile-localized supersolution certificate (I4-F).
    Returns (err_bound, volO) -- SOUND upper bound on max_i |pi_h-pi|_i/d_i.
    psi >= |rho|/d pointwise: ring from acc (Lo), interior from r (Q-scale
    -> push scale factor 2/(1+a)); rho = 0 outside S u ring.  Charged:
    BFS row reads via scan_idx (outside-S rows pay C_adj), local LDL like
    _region_solve's MMD route."""
    a = model.alpha
    c = (1.0 - a) / (1.0 + a)
    n = model.n
    d, ip, ii = model.d, model.indptr, model.indices
    psi = {}
    for i, ri in zip(Sarr.tolist(), r_int.tolist()):
        v = (2.0 / (1.0 + a)) * abs(ri) / model.sqd[i]
        if v > 0:
            psi[i] = v
    c_a = c
    for y, av in acc.items():
        v = c_a * av / d[y]
        if v > 0:
            psi[y] = max(psi.get(y, 0.0), v)
    if not psi:
        return 0.0, 0.0
    th = max(psi.values())
    T = np.array([k for k, v in psi.items() if v > 1e-14 * th], np.int64)
    meter.rec(float(len(psi)))
    inO = np.zeros(n, bool)
    inO[T] = True
    frontier = T
    volO = float(d[T].sum())
    for _k in range(Kmax):
        if frontier.size == 0:
            break
        meter.scan_idx(frontier)              # BFS layer row reads (charged)
        nb = np.unique(np.concatenate(
            [ii[ip[v]:ip[v + 1]] for v in frontier]))
        nb = nb[~inO[nb]]
        if nb.size == 0:
            break
        if volO + float(d[nb].sum()) > cap_vol:
            break
        inO[nb] = True
        frontier = nb
        volO += float(d[nb].sum())
    O = np.flatnonzero(inO)
    K = (sp.diags(model.d) - c * model.A).tocsr()
    KO = K[O][:, O].tocsc()
    meter.rec(float(KO.nnz))
    # affordability test (charged above): abort on shapes whose local LDL
    # would dwarf the run (high average degree ~ treewidth proxy, or huge O)
    if O.size > 25000 or KO.nnz > 8.0 * O.size:
        return math.inf, volO
    nout = d[O] - np.asarray(model.A[O][:, O].sum(axis=1)).ravel()
    psiO = np.array([psi.get(int(i), 0.0) for i in O.tolist()])
    rhs = d[O] * psiO + c * nout * th / (1.0 - c)
    lu = spla.splu(KO, permc_spec="MMD_AT_PLUS_A", diag_pivot_thresh=0.0,
                   options=dict(SymmetricMode=True))
    Lm = lu.L.tocsc()
    cnt = np.diff(Lm.indptr).astype(float)
    fac = float(np.sum(cnt ** 2))
    if fac > max(2.0e5, 0.5 * meter.total()):
        # fill-estimate triage abort (campaign convention: the colcount
        # estimate is charged O(|O|), the numeric factor is never formed)
        meter.rec(float(O.size))
        return math.inf, volO
    meter.resp(fac)
    nnzLU = float(Lm.nnz + lu.U.nnz)
    meter.mat(nnzLU)
    Gh = lu.solve(rhs)
    meter.resp(2.0 * nnzLU)
    inT = np.isin(O, T)
    return float(Gh[inT].max()), volO


def vgf3_local(model, eps, meter, growth=3.0, spec_theta=0.1, ecert=False,
               x_exact=None, oracle=False, max_sweeps=400, wall_cap=60.0,
               inner="auto", fill_kappa=25.0, zeta=0.5, ecert_c=1.0,
               ecert_kmult=4.0, verbose=False):
    n = model.n
    d, sqd = model.d, model.sqd
    Q, b = model.Q, model.b
    ip, ii = model.indptr, model.indices
    a = model.alpha
    c_a = (1.0 - a) / (1.0 + a)
    gam = 2.0 * a / (1.0 + a)
    gate = gam * eps
    floor_ = spec_theta * gate
    target = a * eps
    c2 = (1.0 - a) / 2.0                      # -offdiag scale of Q

    inS = np.zeros(n, bool)
    ulb = np.zeros(n)
    x = np.zeros(n)
    r = np.zeros(n)                           # residual b - Qx, valid on S
    Slist = [model.seed]
    inS[model.seed] = True
    meter.scan_idx(np.array([model.seed]))
    volS = float(d[model.seed])
    cert_vol = float(d[model.seed])
    r[model.seed] = b[model.seed]
    dirty = {int(model.seed)}
    acc = {}
    hp = []
    t0 = time.perf_counter()
    sweeps = 0
    nsolve = 0
    band_vol_tot = 0.0
    status = "maxed"
    ework = 0.0
    e_last_W = 0.0
    e_last_nu = math.inf
    e_tries = 0
    stopped_by = "std"

    def admit(v, val):
        nonlocal volS, cert_vol
        meter.scan_idx(np.array([v]))
        inS[v] = True
        Slist.append(v)
        volS += float(d[v])
        ulb[v] = max(ulb[v], val)
        if val >= gate:
            cert_vol += float(d[v])
        # r[v] = b_v - Q[v,:]x = b_v + c2*sum_{w~v,S} x_w/(sqd_v sqd_w)
        nbv = ii[ip[v]:ip[v + 1]]
        meter.rec(float(nbv.size))
        s_in = 0.0
        for y in nbv.tolist():
            if inS[y]:
                s_in += x[y] / sqd[y]
            else:
                if y not in acc:
                    acc[y] = 0.0
                    meter.resp(1.0)           # degree query, new ring vertex
                if ulb[v] > 0:
                    acc[y] += ulb[v]
                    ny = c_a * acc[y] / d[y]
                    if ny >= floor_:
                        heapq.heappush(hp, (-ny, y))
                        meter.resp(_lg(len(hp)))
        r[v] = b[v] + c2 * s_in / sqd[v]
        acc.pop(v, None)
        dirty.add(int(v))

    inband = np.zeros(n, bool)

    def lift():
        """Residual-driven band solves until no r_i/sqd_i >= zeta*target.
        Bands grow GEOMETRICALLY across passes (active set + a BFS margin
        INSIDE S), so a lift costs O(vol(final band) * log) -- the final
        band is the true influence region of the update, never more than S.
        The margin is inside the already-admitted (already-paid) region, so
        output-boundedness is untouched; margin-row re-reads are charged as
        repeats via scan_idx."""
        nonlocal nsolve, band_vol_tot
        passes = 0
        prev_vol = 0.0
        while passes < 200:
            passes += 1
            meter.rec(float(len(dirty)))
            act = [i for i in dirty if r[i] >= zeta * target * sqd[i]]
            dirty.difference_update(
                [i for i in dirty if r[i] < zeta * target * sqd[i]])
            if not act:
                return
            bset = set(act)
            bvol = float(d[np.asarray(act, np.int64)].sum())
            tgt_vol = min(volS, max(2.0 * prev_vol, 2.0 * bvol))
            frontier = list(bset)
            while bvol < tgt_vol and frontier:
                nxt = []
                for v in frontier:
                    nbv = ii[ip[v]:ip[v + 1]]
                    meter.rec(float(nbv.size))
                    for y in nbv.tolist():
                        if inS[y] and y not in bset:
                            bset.add(y)
                            nxt.append(y)
                            bvol += float(d[y])
                    if bvol >= tgt_vol:
                        break
                frontier = nxt
            prev_vol = bvol
            band = np.array(sorted(bset), np.int64)
            meter.scan_idx(band)              # re-read band rows (R_adj)
            QB = Q[band]
            meter.rec(float(QB.nnz))
            QBB = QB[:, band].tocsc()
            rhs = b[band] - QB @ x + QBB @ x[band]
            volB = float(d[band].sum())
            band_vol_tot += volB

            def scan0(k, _B=band):
                for _ in range(int(round(k))):
                    meter.scan_idx(_B)
            xN, _rt, _fl = _region_solve(
                QBB, rhs, meter, fill_kappa, inner in ("auto", "amg"),
                sqd[band], a, target, volB, scan0, root=0)
            nsolve += 1
            xN = np.maximum(xN, x[band])      # monotone (theory: always >=)
            dx = xN - x[band]
            if _rt == "amg":
                rnum = rhs - QBB @ xN
                meter.rec(float(QBB.nnz))
                r[band] = rnum                # SIGNED: psi must cover |r|
            else:
                r[band] = 0.0
            x[band] = xN
            inband[band] = True
            newu = np.maximum(ulb[band], xN / sqd[band])
            du_all = newu - ulb[band]
            ulb[band] = newu
            for idx_l, v in enumerate(band.tolist()):
                dxv = dx[idx_l]
                duv = du_all[idx_l]
                if dxv <= 0.0 and duv <= 0.0:
                    continue
                nbv = ii[ip[v]:ip[v + 1]]
                meter.rec(float(nbv.size))
                for y in nbv.tolist():
                    if inS[y]:
                        if dxv > 0.0 and not inband[y]:
                            r[y] += c2 * dxv / (sqd[v] * sqd[y])
                            dirty.add(y)
                    elif duv > 0.0:
                        if y not in acc:
                            acc[y] = 0.0
                            meter.resp(1.0)
                        acc[y] += duv
                        ny = c_a * acc[y] / d[y]
                        if ny >= floor_:
                            heapq.heappush(hp, (-ny, y))
                            meter.resp(_lg(len(hp)))
            inband[band] = False
            dirty.update(band.tolist())

    def try_ecert(nu_like):
        """Attempt the (e') certificate under the retry guards; returns the
        sound error bound (or inf if the guards say don't attempt)."""
        nonlocal e_last_nu, e_last_W, e_tries, ework
        if e_tries >= 12:
            return math.inf
        if not (e_tries == 0 or meter.total() >= 3.0 * e_last_W):
            return math.inf
        e_last_nu = nu_like
        e_last_W = meter.total()
        e_tries += 1
        W0 = meter.total()
        Kmax = int(math.ceil(ecert_kmult / math.sqrt(a)))
        S_ = np.asarray(Slist, np.int64)
        ringvol = float(sum(d[y] for y in acc))
        meter.rec(float(len(acc)))
        if ringvol > 60.0 * volS:
            # reading even B_1(ring) would dwarf the region: not worth it
            return math.inf
        bound, _volO = _echeck(model, meter, inS, r[S_], S_, acc,
                               eps, 2.0 * (volS + ringvol) + 2000.0, Kmax)
        ework += meter.total() - W0
        return bound

    last = dict(volS=volS, nS=1, rounds=0)
    ecert_stop = False
    while sweeps < max_sweeps:
        if time.perf_counter() - t0 > wall_cap:
            status = "cap"
            break
        sweeps += 1
        budget = growth * volS
        admitted = 0
        # ---- admission + cheap newN micro-solves (one sweep) ------------
        # burst: admit by value; micro-solve: exact Dirichlet solve on the
        # NEW block only (frozen complement, O(vol(new)) -- I4-E's ext
        # solve), which lifts ring bounds enough to keep admission running.
        # The expensive residual-driven lift() runs ONCE, at sweep end.
        while True:
            burst = []
            while hp:
                if volS >= budget and admitted:
                    break
                negLo, v = heapq.heappop(hp)
                meter.resp(_lg(len(hp) + 1))
                if inS[v]:
                    continue
                cur = c_a * acc[v] / d[v]
                if -negLo < cur - 1e-15 * max(cur, 1e-300):
                    continue
                isviol = cur >= gate
                if not isviol:
                    if cur < floor_:
                        break
                    if d[v] > budget - volS:
                        continue
                if (ecert and not oracle and cur < ecert_c * eps
                        and isviol and e_tries < 12
                        and (e_tries == 0
                             or meter.total() >= 3.0 * e_last_W)):
                    # everything left in the heap is sub-semantic: before
                    # paying for it, see whether (e') already certifies.
                    lift()
                    bound = try_ecert(cur)
                    if bound < eps:
                        heapq.heappush(hp, (negLo, v))
                        ecert_stop = True
                        break
                admit(v, cur)
                admitted += 1
                burst.append(v)
            if ecert_stop or not burst:
                break
            # micro extension solve on the new block only
            N = np.asarray(sorted(burst), np.int64)
            meter.scan_idx(N)
            QN = Q[N]
            meter.rec(float(QN.nnz))
            QNN = QN[:, N].tocsc()
            rhsN = b[N] - QN @ x + QNN @ x[N]

            def scanN(k, _N=N):
                for _ in range(int(round(k))):
                    meter.scan_idx(_N)
            xN, _rt, _fl = _region_solve(
                QNN, rhsN, meter, fill_kappa, inner in ("auto", "amg"),
                sqd[N], a, target, float(d[N].sum()), scanN, root=0)
            nsolve += 1
            xN = np.maximum(xN, x[N])
            dxN = xN - x[N]
            if _rt == "amg":
                rnumN = rhsN - QNN @ xN
                meter.rec(float(QNN.nnz))
                rnewN = rnumN                 # SIGNED: psi must cover |r|
            else:
                rnewN = np.zeros(N.size)      # exact route: residual 0
            x[N] = xN
            r[N] = rnewN
            inband[N] = True
            newuN = np.maximum(ulb[N], xN / sqd[N])
            duN = newuN - ulb[N]
            ulb[N] = newuN
            for idx_l, v in enumerate(N.tolist()):
                dxv = dxN[idx_l]
                duv = duN[idx_l]
                if dxv <= 0.0 and duv <= 0.0:
                    continue
                nbv = ii[ip[v]:ip[v + 1]]
                meter.rec(float(nbv.size))
                for y in nbv.tolist():
                    if inS[y]:
                        if dxv > 0.0 and not inband[y]:
                            r[y] += c2 * dxv / (sqd[v] * sqd[y])
                            dirty.add(y)
                    elif duv > 0.0:
                        if y not in acc:
                            acc[y] = 0.0
                            meter.resp(1.0)
                        acc[y] += duv
                        ny = c_a * acc[y] / d[y]
                        if ny >= floor_:
                            heapq.heappush(hp, (-ny, y))
                            meter.resp(_lg(len(hp)))
            inband[N] = False
            dirty.update(N.tolist())
            if volS >= budget:
                break
        lift()
        # ---- certificate ------------------------------------------------
        meter.rec(float(len(acc)))
        nu = 0.0
        for y, av in acc.items():
            v = c_a * av / d[y]
            if v > nu:
                nu = v
        S = np.asarray(Slist, np.int64)
        c_in = zeta * target                  # guaranteed by lift()
        semerr = (float(np.max(np.abs(x - x_exact) / sqd))
                  if x_exact is not None else math.inf)
        last = dict(volS=volS, nS=int(S.size), rounds=sweeps,
                    cert_vol=cert_vol, nsolve=nsolve, bandvol=band_vol_tot,
                    nu_over_gate=nu / gate if gate else math.inf,
                    semerr=semerr, ework=ework, stopped_by=stopped_by,
                    e_tries=e_tries)
        if ecert_stop:
            status = "cert"
            stopped_by = "ecert"
            last["stopped_by"] = "ecert"
            break
        if oracle:
            if semerr <= eps:
                status = "cert"
                break
        elif nu < gate:
            status = "cert"
            break
        elif ecert and nu < ecert_c * eps:
            bound = try_ecert(nu)
            last["ework"] = ework
            last["ebound_over_eps"] = bound / eps
            if bound < eps:
                status = "cert"
                stopped_by = "ecert"
                last["stopped_by"] = "ecert"
                break
        if admitted == 0 and not hp:
            # progress guarantee: force the top violator in
            best, bv = 0.0, -1
            for y, av in acc.items():
                v = c_a * av / d[y]
                if v > best:
                    best, bv = v, y
            meter.rec(float(len(acc)))
            if best < gate:
                status = "stalled" if not oracle else "cert"
                break
            admit(bv, best)
            lift()
        if verbose:
            print(f"  sw={sweeps} |S|={len(Slist)} vol={volS:.0f} "
                  f"nu/gate={nu/gate:.3g} W={meter.total():.4g} "
                  f"sem={semerr:.3g}")
    xg = np.zeros(n)
    S = np.asarray(Slist, np.int64)
    xg[S] = x[S]
    return dict(x=xg, status=status, **last)
