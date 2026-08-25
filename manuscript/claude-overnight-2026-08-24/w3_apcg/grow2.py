"""I2-A: extended growing-support APCG machinery for the carry-mode attack.

New vs exp_grow.py (old files untouched):
  * Restricted2: boundary gate with hysteresis multiplier (admit only when
    -grad_j/sqrt(d_j) > gate_mult * alpha*rho), separate boundary-charge
    ledger, exclude set (for batching), strict final sweep support.
  * apcg_grow2: carry/restart, check_mult (stale gate), hysteresis with
    final strict sweep (correctness-preserving), admission batching,
    diagnostic hook computing the estimate-sequence damage per admission:
       Lambda(x,z; S) = F_S(x) - F_S^* + (alpha/2) ||z - x^*_S||_2^2
    (the LLX Lyapunov: (sigma/2)||.||_L^2 with sigma=2a/(1+a), L=c*(1+a)/2
     collapses to (alpha/2)||.||_2^2), and per-admission release
       D_t = F^*_{S_t} - F^*_{S_{t+1}},  slack s_j at x^*_{S_t}.
  * restricted_opt: exact active-set solve of the S-restricted problem.
  * one-step contraction verifier (paper-form step, any (x,z) state).
"""
import math

import numpy as np
import scipy.sparse.linalg as spla

import sys
sys.path.insert(0, "/home/claude/work/overnight/w3_apcg")
sys.path.insert(0, "/home/claude/work/overnight/lib")
from solvers import Restricted, apcg_run       # noqa: E402
from meter import Meter                        # noqa: E402


class Restricted2(Restricted):
    """Restricted problem with gated boundary: hysteresis + exclude set +
    boundary-charge ledger (charges still flow into the meter as before)."""

    def __init__(self, model, rho, S, gate_mult=1.0, bd_ledger=None,
                 exclude=None, **kw):
        super().__init__(model, rho, S, boundary=True, **kw)
        self.gate_mult = float(gate_mult)
        self.bd_ledger = bd_ledger if bd_ledger is not None else [0]
        self.exclude = exclude if exclude is not None else set()

    def _violators(self, x, meter, mult):
        out = []
        for t, j in enumerate(self.Bnodes):
            if j in self.exclude:
                continue
            g = -self.Bb[t]
            for (i, q) in self.Brows[t]:
                g += q * x[i]
            meter.rec(self.Bdeg[t])
            self.bd_ledger[0] += self.Bdeg[t]
            if -g / self.Bsqd[t] - mult * self.arho > 0.0:
                out.append(j)
        return out

    def boundary_violators(self, x, meter):
        return self._violators(x, meter, self.gate_mult)

    def strict_violators(self, x, meter):
        return self._violators(x, meter, 1.0)

    def boundary_grad(self, x, j):
        """Uncharged: exact grad_j f(x) for a boundary node (diagnostics)."""
        t = self.Bnodes.index(j)
        g = -self.Bb[t]
        for (i, q) in self.Brows[t]:
            g += q * x[i]
        return g

    def confirm(self, x, cand, meter, mult=None):
        """Re-test a candidate set at the current x (deferred confirmation).
        Charges d_j per re-test.  Returns the survivors."""
        if mult is None:
            mult = self.gate_mult
        idx = {j: t for t, j in enumerate(self.Bnodes)}
        out = []
        for j in sorted(cand):
            t = idx.get(j)
            if t is None:
                out.append(j)          # no longer on the boundary: keep
                continue
            g = -self.Bb[t]
            for (i, q) in self.Brows[t]:
                g += q * x[i]
            meter.rec(self.Bdeg[t])
            self.bd_ledger[0] += self.Bdeg[t]
            if -g / self.Bsqd[t] - mult * self.arho > 0.0:
                out.append(j)
        return out


def restricted_opt(R):
    """Exact optimum of the S-restricted RPPR problem by active set inside S.
    Returns (xs, Fs) with xs an len(S) vector (diagnostics; uncharged)."""
    n = R.n
    act = {i for i in range(n) if R.bv[i] > R.lamv[i]}
    if not act:
        return np.zeros(n), 0.0
    for _ in range(10000):
        A = sorted(act)
        QAA = R.QSS[A][:, A].tocsc()
        xa = spla.spsolve(QAA, R.bv[A] - R.lamv[A])
        xa = np.atleast_1d(xa)
        if np.min(xa) <= 0:
            act = {g for g, v in zip(A, xa) if v > 0}
            if not act:
                return np.zeros(n), 0.0
            continue
        xs = np.zeros(n)
        xs[A] = xa
        grad = R.QSS @ xs - R.bv
        mask = np.ones(n, bool)
        mask[A] = False
        viol = mask & (grad < -R.lamv - 1e-13)
        if not viol.any():
            Fs = 0.5 * float(xs @ grad) - 0.5 * float(xs @ R.bv) \
                + float(R.lamv @ np.abs(xs))
            return xs, Fs
        act |= {int(j) for j in np.nonzero(viol)[0]}
    raise RuntimeError("restricted active set did not settle")


def lyapunov(R, x, z, xs, Fs, alpha):
    _, _, F = R.eval(np.asarray(x))
    return (F - Fs) + 0.5 * alpha * float(np.sum((np.asarray(z) - xs) ** 2))


def admitted_slacks(R, xs, adm):
    """slack s_j = (-grad_j f(x*_S) - lam_j)_+ for admitted boundary nodes,
    evaluated at the restricted optimum xs (diagnostics; uncharged)."""
    out = {}
    md = R.model
    al = md.alpha
    off = -(1.0 - al) / 2.0
    for j in adm:
        g = -float(md.b[j])
        for h in md.adj[j]:
            if h in R.gl:
                g += off / math.sqrt(md.d[j] * md.d[h]) * xs[R.gl[h]]
        lamj = R.arho * math.sqrt(md.d[j])
        out[j] = max(0.0, -g - lamj)
    return out


def apcg_grow2(mdl, rho, rng, Strue, variant="carry", delta=0.1,
               check_mult=1, gate_mult=1.0, batch_iters=0, recheck=False,
               diag=False, max_total=40_000_000):
    """Growing-support APCG.  Returns run dict; if diag, adds 'events' with
    per-admission (Lam_minus, Lam_plus, D, slacks, iters_at, nS) and
    Lam0/Lam_end."""
    al = mdl.alpha
    lam = al * rho * mdl.sqd
    S = sorted(int(i) for i in np.nonzero(mdl.s)[0] if mdl.b[i] > lam[i])
    meter = Meter(mdl.adj)
    bdl = [0]
    for g in S:
        meter.rec(int(mdl.d[g]))
    smap, xmap = {}, {}
    phi_carry = 1.0
    Strueset = set(Strue)
    n_events = n_admitted = 0
    spurious = []
    tot_iters = 0
    last_rebuild_iters = 0
    pending = set()
    events = []
    cache = {}          # frozenset(S) -> (xs, Fs)
    sweep_events = 0
    n_recheck = 0

    def opt_for(R):
        key = (len(R.S), R.S[0], R.S[-1], hash(tuple(R.S)))
        if key not in cache:
            cache.clear()
            cache[key] = restricted_opt(R)
        return cache[key]

    while True:
        R = Restricted2(mdl, rho, S, gate_mult=gate_mult, bd_ledger=bdl,
                        exclude=pending)
        if variant == "carry":
            p0 = [smap.get(g, (0.0, 0.0))[0] for g in R.S]
            M0 = [smap.get(g, (0.0, 0.0))[1] for g in R.S]
            st = (p0, M0, phi_carry)
            res = apcg_run(R, meter, rng, delta=delta, boundary=True,
                           want_sym=False, state=st,
                           check_every=check_mult * R.n,
                           max_iter=max_total - tot_iters)
        else:
            x0 = [xmap.get(g, 0.0) for g in R.S]
            res = apcg_run(R, meter, rng, delta=delta, boundary=True,
                           want_sym=False, x0=x0,
                           check_every=check_mult * R.n,
                           max_iter=max_total - tot_iters)
        tot_iters += res["iters"]
        adm = None
        if res["status"] == "admit":
            adm = res["admit"]
        elif res["status"] == "ok":
            if pending:
                adm = []            # force rebuild with pending
            elif gate_mult > 1.0:
                x = res["x"]
                sv = R.strict_violators(x, meter)
                if sv:
                    sweep_events += 1
                    pending |= set(sv)      # merged below; adm must be a
                    adm = []                # rebuild trigger, not the list
        if adm is None:
            out = dict(status=res["status"], W=meter.total(),
                       W_boundary=bdl[0], iters=tot_iters, nS=len(S),
                       volS=R.vol, admit_events=n_events,
                       admitted=n_admitted, spurious=len(spurious),
                       spur_vol=int(sum(mdl.d[j] for j in spurious)),
                       spurious_nodes=sorted(spurious)[:50],
                       sweep_events=sweep_events, n_recheck=n_recheck,
                       x=res["x"], S=list(S),
                       missed=len(Strueset - set(S)))
            if diag:
                xs, Fs = opt_for(R)
                # final state lacks z; report the F-gap part (lower bd on Lam)
                out["Lam_end"] = float(R.eval(np.asarray(res["x"]))[2] - Fs)
                out["events"] = events
            return out

        # admission event bookkeeping
        if res["status"] == "admit":
            pending |= set(res["admit"])
        do_rebuild = True
        if batch_iters and res["status"] == "admit":
            if tot_iters - last_rebuild_iters < batch_iters:
                do_rebuild = False
        if not do_rebuild:
            # resume same support with pending excluded from the gate
            if variant == "carry":
                p, Mh, phi_carry = res["state"]
                smap = {g: (p[k], Mh[k]) for k, g in enumerate(R.S)}
            else:
                xmap = {g: float(v) for g, v in zip(R.S, res["x"])}
            continue

        adm = sorted(pending)
        pending = set()
        if recheck and adm:
            # deferred confirmation: the candidate must STILL violate the gate
            # at the current iterate before it is allowed into S.
            if res["status"] == "admit":
                p_, Mh_, phi_ = res["state"]
                xc = np.asarray(p_) + phi_ * np.asarray(Mh_)
            else:
                xc = np.asarray(res["x"])
            adm = R.confirm(xc, adm, meter)
            n_recheck += 1
            if not adm and res["status"] == "ok":
                # converged and every candidate withdrew: final strict sweep
                # over the whole boundary (correctness guard).
                R.exclude = set()
                sv = R.strict_violators(xc, meter)
                if sv:
                    sweep_events += 1
                    adm = sv
                else:
                    return dict(status=res["status"], W=meter.total(),
                                W_boundary=bdl[0], iters=tot_iters,
                                nS=len(S), volS=R.vol,
                                admit_events=n_events, admitted=n_admitted,
                                spurious=len(spurious),
                                spur_vol=int(sum(mdl.d[j]
                                                 for j in spurious)),
                                spurious_nodes=sorted(spurious)[:50],
                                sweep_events=sweep_events,
                                n_recheck=n_recheck, x=res["x"], S=list(S),
                                missed=len(Strueset - set(S)))
            if not adm:
                last_rebuild_iters = tot_iters
                if variant == "carry":
                    p_, Mh_, phi_carry = res["state"]
                    smap = {g: (p_[k], Mh_[k]) for k, g in enumerate(R.S)}
                else:
                    xmap = {g: float(v) for g, v in zip(R.S, xc)}
                continue
        n_events += 1
        n_admitted += len(adm)
        spurious += [j for j in adm if j not in Strueset]
        ev = None
        if diag:
            if res["status"] == "admit":
                p, Mh, phi = res["state"]
                x = np.asarray(p) + phi * np.asarray(Mh)
                z = np.asarray(p) - phi * np.asarray(Mh)
            else:
                x = np.asarray(res["x"])
                z = x.copy()
            xs, Fs = opt_for(R)
            Lm = lyapunov(R, x, z, xs, Fs, al)
            sl = admitted_slacks(R, xs, adm)
            ev = dict(iters=tot_iters, nS=len(S), Fs=Fs, Lam_minus=Lm,
                      slacks={int(j): float(v) for j, v in sl.items()},
                      spur=[int(j) for j in adm if j not in Strueset])
        if variant == "carry":
            if res["status"] == "admit":
                p, Mh, phi_carry = res["state"]
                smap = {g: (p[k], Mh[k]) for k, g in enumerate(R.S)}
            else:
                # converged segment (sweep/batched admission at h-stop):
                # only x is available; continue with z = x (momentum flushed
                # at a near-critical point -- cheap, happens at tiny gap)
                phi_carry = 1.0
                smap = {g: (float(v), 0.0)
                        for g, v in zip(R.S, res["x"])}
        else:
            xmap = {g: float(v) for g, v in zip(R.S, res["x"])}
        for j in adm:
            meter.rec(int(mdl.d[j]))
        S = sorted(set(S) | set(adm))
        last_rebuild_iters = tot_iters
        if diag:
            R2 = Restricted2(mdl, rho, S, gate_mult=gate_mult,
                             bd_ledger=[0])
            xs2, Fs2 = restricted_opt(R2)
            cache.clear()
            key = (len(R2.S), R2.S[0], R2.S[-1], hash(tuple(R2.S)))
            cache[key] = (xs2, Fs2)
            xp = np.zeros(R2.n)
            zp = np.zeros(R2.n)
            gl2 = R2.gl
            for k, g in enumerate(R.S):
                xp[gl2[g]] = x[k]
                zp[gl2[g]] = z[k]
            Lp = lyapunov(R2, xp, zp, xs2, Fs2, al)
            ev["D"] = ev["Fs"] - Fs2
            ev["Lam_plus"] = Lp
            events.append(ev)


# ---------------------------------------------------------------- verifier

def onestep_expectation(R, x, z, sigma=None):
    """Exact E_i[Lambda(x+,z+)] over uniform i for one paper-form APCG step
    from an arbitrary state (x, z), plus Lambda(x,z).  Uses the restricted
    exact optimum.  Returns (Lam, ELamp, a)."""
    n = R.n
    if sigma is None:
        sigma = R.sigma
    a = math.sqrt(sigma) / n
    na = n * a
    xs, Fs = restricted_opt(R)
    al = R.model.alpha
    x = np.asarray(x, float)
    z = np.asarray(z, float)
    Lam = lyapunov(R, x, z, xs, Fs, al)
    y = (x + a * z) / (1.0 + a)
    gy = R.QSS @ y - R.bv
    zh = (z + a * x) / (1.0 + a)
    acc = 0.0
    for i in range(n):
        u = zh[i] - gy[i] / (na * R.c)
        thr = R.lam[i] / (na * R.c)
        if u > thr:
            zi = u - thr
        elif u < -thr:
            zi = u + thr
        else:
            zi = 0.0
        zp = zh.copy()
        zp[i] = zi
        xp = y + na * (zp - z) + (sigma / n) * (z - y)
        acc += lyapunov(R, xp, zp, xs, Fs, al)
    return Lam, acc / n, a
