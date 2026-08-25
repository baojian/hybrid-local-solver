"""Adversary search: signed-eta gp ops (pushes AND anti-pushes) with r >= 0.
Question: can r_center exceed 1 (which would weaken Step 3's per-op cap)?
Potential argument predicts r_c <= Psi = r_c + c_a*sum(r_leaf), with Psi
invariant under leaf ops and decreasing in Zc; pumping needs center-antis
which look exactly reversible. Search randomly for a violation."""
import random
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'lib'))
from zoo import star
from gpush import GP

best = {}
for alpha in (1/4, 1/16):
    for m in (4, 8):
        adj, seed = star(m)
        ca = (1 - alpha) / (1 + alpha)
        maxrc, maxl1, minZc = 1.0, 1.0, 0.0
        rng = random.Random(42)
        for trial in range(3000):
            st = GP(adj, alpha, seed, center=0)
            for step in range(150):
                kind = rng.randrange(4)
                f = rng.uniform(0.05, 1.0)
                if kind == 0:                      # center push
                    eta = f * st.cap(0)
                    if eta > 1e-15: st.gp(0, eta)
                elif kind == 1:                    # center ANTI-push
                    mn = min(st.r[w] for w in range(1, st.n))
                    cap_anti = 2.0 * m * mn / (1 - alpha)
                    if cap_anti > 1e-15: st.gp(0, -f * cap_anti)
                elif kind == 2:                    # leaf push (max-r leaf)
                    w = max(range(1, st.n), key=lambda v: st.r[v])
                    eta = f * st.cap(w)
                    if eta > 1e-15: st.gp(w, eta)
                else:                              # leaf ANTI-push
                    w = rng.randrange(1, st.n)
                    cap_anti = 2.0 * st.r[0] / (1 - alpha)
                    if cap_anti > 1e-15: st.gp(w, -f * cap_anti)
                assert st.min_r_seen > -1e-10, 'r went negative: bug'
                maxrc = max(maxrc, st.r[0])
                maxl1 = max(maxl1, st.sum_r)   # r>=0 so sum = l1
                minZc = min(minZc, st.Zc)
        best[(alpha, m)] = (maxrc, maxl1, minZc)
        print(f'alpha={alpha:.4f} m={m}: max r_c={maxrc:.12f}  '
              f'max ||r||_1={maxl1:.6f}  min Zc={minZc:.4f}')
print('\nno rollout drove r_c above 1 =>' if all(v[0] <= 1 + 1e-9
      for v in best.values()) else 'VIOLATION FOUND =>',
      'evidence that the Step-3 cap survives signed one-hop ops with r>=0')
