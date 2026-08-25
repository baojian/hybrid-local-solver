import sys, json, time, traceback
import numpy as np
sys.path.insert(0, '/home/claude/work/overnight/lib')
sys.path.insert(0, '/home/claude/work/overnight/w6_incremental')
import zoo
from model import Model
import core

OUT = '/home/claude/work/overnight/w6_incremental'

GRAPHS = {
    'path':        lambda: zoo.path(6000, seed_end=True),
    'caterpillar': lambda: zoo.caterpillar(3000, 1),
    'spider':      lambda: zoo.spider(8, 400),
    'btree':       lambda: zoo.binary_tree(12),
    'decoy_hub':   lambda: zoo.decoy_hub(50, 300),
    'theta':       lambda: zoo.theta_graph(60, 60, 60),
    'grid':        lambda: zoo.grid(70, 70),
}


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    return o


def sweep_main():
    res = []
    for gname, gf in GRAPHS.items():
        adj, seed = gf()
        for alpha in (1e-2, 1e-4):
            mo = Model(adj, alpha, seed)
            for k in range(4, 11):
                eps = 2.0 ** -k
                t0 = time.time()
                try:
                    r = core.run_config(mo, eps)
                    r.update(graph=gname, k=k)
                    res.append(r)
                    tots = {b: int(core.total_of(v)) for b, v in
                            r['backends'].items()}
                    print(f"[main] {gname} a={alpha:g} eps=2^-{k} "
                          f"E={r['E']} |S|={r['S']} vol={r['volS']} "
                          f"meanT={r['meanT']:.1f} {tots} "
                          f"({time.time()-t0:.1f}s)", flush=True)
                except Exception as e:
                    print(f"[main] FAIL {gname} a={alpha} k={k}: {e}",
                          flush=True)
                    traceback.print_exc()
        with open(f'{OUT}/results_main.json', 'w') as f:
            json.dump(jsonable(res), f)
    return res


def sweep_alpha():
    res = []
    eps = 2.0 ** -8
    for gname in ('path', 'btree', 'grid'):
        adj, seed = GRAPHS[gname]()
        for j in (4, 6, 8, 10, 12, 14):
            alpha = 2.0 ** -j
            mo = Model(adj, alpha, seed)
            t0 = time.time()
            try:
                r = core.run_config(mo, eps)
                r.update(graph=gname, k=8, j=j)
                res.append(r)
                tots = {b: int(core.total_of(v)) for b, v in
                        r['backends'].items()}
                iw = r['backends'].get('CG-WARM', {}).get('iters', [])
                ic = r['backends'].get('CG-COLD', {}).get('iters', [])
                print(f"[alpha] {gname} a=2^-{j} E={r['E']} |S|={r['S']} "
                      f"mean_it_warm={np.mean(iw):.1f} "
                      f"mean_it_cold={np.mean(ic):.1f} {tots} "
                      f"({time.time()-t0:.1f}s)", flush=True)
            except Exception as e:
                print(f"[alpha] FAIL {gname} j={j}: {e}", flush=True)
                traceback.print_exc()
        with open(f'{OUT}/results_alpha.json', 'w') as f:
            json.dump(jsonable(res), f)
    return res


def sweep_diag():
    """alpha = eps diagonal: the regime where the 1/eps^2 shape can bite."""
    res = []
    for gname in ('path', 'caterpillar'):
        adj, seed = GRAPHS[gname]()
        for k in (4, 6, 8, 10, 12):
            eps = 2.0 ** -k
            alpha = eps
            mo = Model(adj, alpha, seed)
            t0 = time.time()
            try:
                r = core.run_config(mo, eps)
                r.update(graph=gname, k=k, diag=True)
                res.append(r)
                tots = {b: int(core.total_of(v)) for b, v in
                        r['backends'].items()}
                print(f"[diag] {gname} a=eps=2^-{k} E={r['E']} "
                      f"|S|={r['S']} vol={r['volS']} {tots} "
                      f"({time.time()-t0:.1f}s)", flush=True)
            except Exception as e:
                print(f"[diag] FAIL {gname} k={k}: {e}", flush=True)
                traceback.print_exc()
        with open(f'{OUT}/results_diag.json', 'w') as f:
            json.dump(jsonable(res), f)
    return res


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    t0 = time.time()
    if which in ('all', 'main'):
        sweep_main()
    if which in ('all', 'alpha'):
        sweep_alpha()
    if which in ('all', 'diag'):
        sweep_diag()
    print(f'TOTAL WALL {time.time()-t0:.1f}s', flush=True)
