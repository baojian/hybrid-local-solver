import sys, json; sys.path.insert(0,'/home/claude/work/overnight/w10_i3b')
import run as RR, exp
from solvers import Model
out=[]
for D in (48,192):
    adj, seed, hubs = RR.ring_star(m=60, hub_deg=D)
    rho, rel = RR.tune_rho_ring(adj, seed, 2**-10, hubs, target_rel=0.95, iters=24)
    mdl = Model(adj, 2**-10, seed)
    for mult in (1.0, 2.9, 8.0):
        o = exp.one(mdl, rho, mult, 'n', seed=1)
        g=o['gates']
        rec=dict(D=D,mult=mult,volS=o['vol_S'],volB=o['vol_B'],adm=o['admissions'],
                 interior=o['interior']['total'],status=o['status'],
                 gates={k:v['total'] for k,v in g.items()},
                 kin_piggy=g['kinetic']['piggy'], kin_wake=g['kinetic']['wakeups'])
        out.append(rec); print(json.dumps(rec), flush=True)
json.dump(out, open('/home/claude/work/overnight/w10_i3b/res_mult.json','w'), indent=1)
