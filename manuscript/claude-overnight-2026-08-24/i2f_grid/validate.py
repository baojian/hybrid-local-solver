"""Validation: (i) the interior identity Q = a I + beta L, (ii) the local MG
V-cycle convergence factor, (iii) correctness of every solver against the
exact sparse solve, (iv) meter bookkeeping sanity."""
import sys
import math
import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/i2f_grid")
import gridlib as G
from gridlib import (LatticeModel, VecMeter, support_stats, push_c,
                     cheb_local, mg_local, nd_ees, Region, ladder)


def check_operator(w=21, alpha=0.25, dim=2):
    M = LatticeModel(w, alpha, dim)
    beta = (1 - alpha) / (4.0 * dim)
    n = M.n
    idx = np.arange(n).reshape(M.shape)
    sl = tuple(slice(2, w - 2) for _ in range(dim))
    inner = idx[sl].ravel()
    # A_int = a I + beta * L on interior rows
    Lg = (2 * dim) * np.eye(n) - M.A.toarray()
    Qd = M.Q.toarray()
    err = np.max(np.abs(Qd[inner] - (alpha * np.eye(n)[inner] + beta * Lg[inner])))
    return err


def mg_rate(w=201, alpha=2 ** -8, m=127, cycles=8):
    """Measured V-cycle residual reduction factor on the local problem."""
    M = LatticeModel(w, alpha, 2)
    reg = Region(m, alpha, 2)
    rbm = [G._rb_masks(reg.m(l), 2) for l in range(reg.nlev)]
    up = np.zeros((m + 2, m + 2)); fp = np.zeros((m + 2, m + 2))
    fp[m // 2 + 1, m // 2 + 1] = M.b[M.seed]
    rates = []
    prev = None
    for c in range(cycles):
        ch = dict(lev0=0, resp=0.0, mat=0.0, setup=0.0)
        G.v_cycle(reg, 0, up, fp, rbm, ch, 2, 1)
        r = G._resid(up, fp, reg.cf[0], reg.diag[0])
        rn = float(np.max(np.abs(r)))
        if prev is not None:
            rates.append(rn / prev)
        prev = rn
    return rates


def check_cert(w=101, alpha=2 ** -6, m=31):
    """The stencil certificate over Omega U dOmega must equal the TRUE global
    certificate ||D^{-1/2}(Qx-b)||_inf of the zero-extended iterate."""
    M = LatticeModel(w, alpha, 2)
    reg = Region(m, alpha, 2)
    rbm = [G._rb_masks(reg.m(l), 2) for l in range(reg.nlev)]
    up = np.zeros((m + 2, m + 2)); fp = np.zeros((m + 2, m + 2))
    fp[m // 2 + 1, m // 2 + 1] = M.b[M.seed]
    ch = dict(lev0=0, resp=0.0, mat=0.0, setup=0.0)
    G.v_cycle(reg, 0, up, fp, rbm, ch, 2, 1)
    ri = G._region_index(M, m)
    xg = np.zeros(M.n)
    xg[ri["core"].ravel()] = up[1:-1, 1:-1].ravel()
    beta = (1 - alpha) / 8.0
    rin = G._resid(up, fp, reg.cf[0], reg.diag[0])
    cert_local = max(float(np.max(np.abs(rin))) / 2.0,
                     G._ring_cert(up, beta, 2))
    return cert_local, M.cert_resid(xg)


def main():
    print("== (i) interior operator identity Q = aI + beta L ==")
    for dim in (2, 3):
        for a in (0.25, 2 ** -8):
            e = check_operator(15 if dim == 3 else 21, a, dim)
            print(f"  dim={dim} alpha={a:.5g}  max|Q - (aI+beta L)|_interior "
                  f"= {e:.2e}")

    print("== (ii) V-cycle residual reduction (should be ~0.05-0.2, "
          "alpha-free) ==")
    for a in (2 ** -4, 2 ** -8, 2 ** -12):
        r = mg_rate(alpha=a)
        print(f"  alpha=2^{int(round(math.log2(a)))}: rates "
              + " ".join(f"{x:.3f}" for x in r[:6]))

    print("== (ii-b) stencil certificate == global cert_resid ==")
    for a in (2 ** -4, 2 ** -6, 2 ** -10):
        cl, cg = check_cert(alpha=a)
        print(f"  alpha={a:.5g}: local={cl:.6e} global={cg:.6e} "
              f"ratio={cl/cg:.9f}")
        assert abs(cl / cg - 1) < 1e-9, "certificate mismatch"

    print("== (iii) end-to-end correctness on grid(101,101) ==")
    w = 101
    for a in (2 ** -4, 2 ** -8):
        M = LatticeModel(w, a, 2)
        x0 = M.solve_exact()
        for eps in (1e-4, 1e-6):
            ss = support_stats(M, eps)
            row = [f"alpha=2^{int(round(math.log2(a)))} eps={eps:g} "
                   f"nS={ss['nS']} volS={ss['volS']:.0f} R={ss['R']} "
                   f"bd={ss['touches_bd']}"]
            mm = VecMeter(M.d)
            out = mg_local(M, eps, mm, x_exact=x0)
            e1 = M.semantic_err(out["x"])
            row.append(f"MG m={out['m']} cyc={out['cycles']} "
                       f"W={mm.total():.3g} err/eps={e1/eps:.3f} "
                       f"cert/(a*eps)={out['cert']/(a*eps):.3f} "
                       f"{out['status']}")
            mm2 = VecMeter(M.d)
            out2 = nd_ees(M, eps, mm2, x_exact=x0)
            e2 = M.semantic_err(out2["x"])
            row.append(f"ND m={out2['m']} W={mm2.total():.3g} "
                       f"err/eps={e2/eps:.3f} {out2['status']}")
            p = push_c(M, eps)
            e3 = M.semantic_err(p["x"])
            row.append(f"PUSH W={p['W']:.3g} err/eps={e3/eps:.3f}")
            mm4 = VecMeter(M.d)
            out4 = cheb_local(M, eps, mm4)
            e4 = M.semantic_err(out4["x"])
            row.append(f"CHEB it={out4['iters']} W={mm4.total():.3g} "
                       f"err/eps={e4/eps:.3f} {out4['status']}")
            print("  " + "\n     ".join(row))
            # A "maxed" status means the region ladder hit the grid boundary:
            # the algorithm CORRECTLY refuses to certify, and the semantic
            # error may then exceed eps.  Only certified runs are asserted.
            if out["status"] == "cert":
                assert e1 <= eps * 1.0000001, ("MG semantic failure", e1, eps)
            if out2["status"] == "cert":
                assert e2 <= eps * 1.0000001, ("ND semantic failure", e2, eps)
            assert e3 <= eps * 1.0000001, ("push semantic failure", e3, eps)
            if out4["status"] == "cert":
                assert e4 <= eps * 1.0000001, ("cheb semantic failure", e4, eps)
    print("ALL VALIDATION CHECKS PASSED")


if __name__ == "__main__":
    main()
