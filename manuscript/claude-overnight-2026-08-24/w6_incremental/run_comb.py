"""I2-B step 2: the COMB adversary. (A) (B,alpha) matrix, (B) eps-scaling."""
import sys, json, time
import numpy as np

sys.path.insert(0, '/home/claude/work/overnight/lib')
sys.path.insert(0, '/home/claude/work/overnight/w6_incremental')
from model import Model
import core, i2b

ALPHAS = [2.0 ** -6, 2.0 ** -10, 2.0 ** -14]
out = []
t00 = time.time()


def show(rec):
    for k, v in rec['bk'].items():
        if k.startswith('ORACLE'):
            continue
        print(f"    {k:9s} W/vol={v.get('Wvol', float('nan')):10.2f}"
              f" {'CAPPED@%.2f' % v['frac'] if v.get('capped') else ''}"
              f"{v.get('error', '')}", flush=True)
    s = rec['bk'].get('SEG-LDL', {})
    if 'lev_mean' in s:
        print(f"      SEG levmean={s['lev_mean']:.2f} levmax={s['lev_max']}"
              f" adm/vtx={s['admit_nodes_total']/max(rec['S'],1):.1f}"
              f" qnodes/q={s['query_nodes_total']/max(s['nqueries'],1):.1f}"
              f" paths={s['npaths']} rebuilds={s['rebuilds']}"
              f" rbnodes={s['rebuild_nodes']}", flush=True)
    i = rec['bk'].get('INC-LDL', {})
    if 'nnzL' in i:
        print(f"      INC nnzL={i['nnzL']} nnzL/S={i['nnzL']/max(rec['S'],1):.1f}",
              flush=True)


def one(B, a, cap, tag, want=None, eps_force=None):
    T = max(2, int(round(1.0 / np.sqrt(a))))
    adj, s = i2b.comb(B, T)
    n = len(adj)
    mo = Model(adj, a, s)
    keepQ = False
    if eps_force is None:
        eps, tr = i2b.tune_eps_trace(mo, cap, keep_Q=keepQ)
    else:
        eps = eps_force
        tr = core.grow_trace(mo, eps, keep_Q=keepQ)
    if want is None:
        want = ['COLD-LU', 'INC-LDL', 'TREE-INC', 'SEG-LDL']
    print(f"[{time.time()-t00:6.1f}s] {tag} B={B} T={T} n={n} "
          f"alpha=2^{int(np.log2(a))} eps=2^{int(np.log2(eps))} "
          f"S={len(tr['S'])} vol={tr['rounds'][-1]['volS']}", flush=True)
    rec = i2b.run_all(mo, eps, want, keep_Q=keepQ, tr=tr, verbose=False,
                      inc_cap=(6e6, 8e8))
    rec.update(family='comb', Bbone=B, T=T, tag=tag)
    show(rec)
    out.append(rec)
    json.dump(out, open('/home/claude/work/overnight/w6_incremental/res_comb.json', 'w'))
    return rec


# (A) matrix
for B in [32, 128, 512]:
    for a in ALPHAS:
        one(B, a, 2500, 'MATRIX')

# (B) eps-scaling at B=512 (unclipped reach) and B=32 (clipped reach)
for B in [512, 32]:
    for a in ALPHAS:
        T = max(2, int(round(1.0 / np.sqrt(a))))
        adj, s = i2b.comb(B, T)
        mo = Model(adj, a, s)
        prev = -1
        for k in range(2, 40):
            eps = 2.0 ** -k
            t0 = time.time()
            tr = core.grow_trace(mo, eps, keep_Q=False)
            sz = len(tr['S'])
            if sz == prev:
                continue
            prev = sz
            if sz < 150:
                continue
            if sz > 9000:
                break
            print(f"[{time.time()-t00:6.1f}s] SCALE B={B} a=2^{int(np.log2(a))}"
                  f" eps=2^{-k} S={sz} vol={tr['rounds'][-1]['volS']}", flush=True)
            rec = i2b.run_all(mo, eps, ['COLD-LU', 'INC-LDL', 'TREE-INC',
                                        'SEG-LDL'],
                              keep_Q=False, tr=tr, verbose=False,
                              inc_cap=(6e6, 8e8))
            rec.update(family='comb', Bbone=B, T=T, tag='SCALE')
            show(rec)
            out.append(rec)
            json.dump(out, open('/home/claude/work/overnight/w6_incremental/res_comb.json', 'w'))
            if time.time() - t00 > 900:
                break
        if time.time() - t00 > 900:
            break
print(f"TOTAL {time.time()-t00:.1f}s")
