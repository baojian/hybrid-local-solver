"""I3-B: the boundary-reporting problem for growing-support local solvers.

TASK (formal).  State: support S, iterate x supported on S, threshold
  thr_j = mult * alpha*rho*sqrt(d_j).
Normalized gate value  G_j(x) = -grad_j f(x) / sqrt(d_j)
   = ( b_j + (1-alpha)/2 * sum_{i~j} x_i/sqrt(d_i d_j) ) / sqrt(d_j).
Violation: G_j > mult*alpha*rho  (=: thr).  The interior solver moves x on S;
grad_j moves only through neighbours of moved coordinates.  A REPORTER must
emit every j in N(S) the first time it violates, by the next poll at the
latest, and must never miss one.

Interior solver = lazy APCG (solvers.apcg_run representation):
      x = p + phi * Mh ,   phi decays geometrically, one coordinate of
      (p, Mh) changes per step.
Hence for a boundary vertex j, with  P_j = sum_{i in S} Q_ji p_i  and
      M_j = sum_{i in S} Q_ji Mh_i ,
      -grad_j(x) = b_j - P_j - phi * M_j            (EXACT, O(1))
and P_j, M_j change only when a neighbour of j is sampled.  This is the
"push" representation; the classical gate instead PULLS (rescans N(j)) and
therefore pays d_j per test.

CHARGING (meter):
  pull test of j            -> rec(d_j)          [scan of j's adjacency]
  push of one interior step -> rec(1) per boundary neighbour  (also counted
                               separately as `piggy` -- these edges are
                               inside the d_i scan the interior solver has
                               already paid for)
  O(1) accumulator test     -> rec(1)
  heap operation            -> resp(ceil(log2(size+2)))
  report                    -> emit(1)
"""
import heapq
import math

import numpy as np


def build_push_index(R):
    """For each local interior index i, the list of (t, q) with t the index of
    a boundary vertex adjacent to i and q = Q_{B[t] i}.  Built from R.Brows,
    which the interior solver's own adjacency scans already expose."""
    idx = [[] for _ in range(R.n)]
    for t, row in enumerate(R.Brows):
        for (i, q) in row:
            idx[i].append((t, q))
    return idx


class GateBase:
    name = "base"

    def __init__(self, R, meter, mult=1.0):
        self.R = R
        self.meter = meter
        self.mult = float(mult)
        self.thr = self.mult * R.arho
        self.nb = len(R.Bnodes)
        self.reported = set()
        self.piggy = 0          # push work that is inside the interior scan
        self.wakeups = 0        # exact recomputes triggered
        self.false_wakeups = 0
        self.sweeps = 0

    # --- interface -------------------------------------------------------
    def note_update(self, i, dp, dMh, phi):
        pass

    def note_flush(self, phi):
        pass

    def poll(self, k, phi, x):
        return []

    def _emit(self, j):
        self.reported.add(j)
        self.meter.emit(1)

    def _heap(self, size):
        self.meter.resp(max(1, int(math.ceil(math.log2(size + 2)))))


class EagerPull(GateBase):
    """(a) baseline: full rescan of N(S), pulling each j's adjacency."""
    name = "eager_pull"

    def poll(self, k, phi, x):
        R = self.R
        self.sweeps += 1
        out = []
        for t, j in enumerate(R.Bnodes):
            g = -R.Bb[t]
            for (i, q) in R.Brows[t]:
                g += q * x[i]
            self.meter.rec(R.Bdeg[t])          # d_j: the pull
            self.wakeups += 1
            if -g / R.Bsqd[t] > self.thr:
                if j not in self.reported:
                    self._emit(j)
                    out.append(j)
        return out


class PushGate(GateBase):
    """Common machinery: exact accumulators P_j, M_j maintained by pushing
    from the interior side."""

    def __init__(self, R, meter, mult=1.0):
        super().__init__(R, meter, mult)
        self.P = [0.0] * self.nb
        self.M = [0.0] * self.nb
        self.push_idx = build_push_index(R)
        self.Bb = list(R.Bb)
        self.Bsqd = list(R.Bsqd)

    def init_state(self, p, Mh, phi):
        """Rebuild P, M from the current interior state.  A true incremental
        implementation carries P, M across an admission and pays only
        O(d_{j0}) per admitted vertex (see findings); this harness rebuilds
        the segment object, so the rebuild is done here and CHARGED at the
        incremental rate by the driver."""
        for t, row in enumerate(self.R.Brows):
            ps = ms = 0.0
            for (i, q) in row:
                ps += q * p[i]
                ms += q * Mh[i]
            self.P[t] = ps
            self.M[t] = ms

    def note_update(self, i, dp, dMh, phi):
        for (t, q) in self.push_idx[i]:
            if dp:
                self.P[t] += q * dp
            if dMh:
                self.M[t] += q * dMh
            self.meter.rec(1)
            self.piggy += 1
        return self.push_idx[i]

    def note_flush(self, phi):
        for t in range(self.nb):
            self.M[t] *= phi
            self.meter.rec(1)

    def gval(self, t, phi):
        """Exact normalized gate value, O(1)."""
        return (self.Bb[t] - self.P[t] - phi * self.M[t]) / self.Bsqd[t]


class EagerPush(PushGate):
    """(a') full sweep, but O(1) per boundary vertex -> |N(S)| per sweep."""
    name = "eager_push"

    def poll(self, k, phi, x):
        self.sweeps += 1
        out = []
        for t, j in enumerate(self.R.Bnodes):
            self.meter.rec(1)
            self.wakeups += 1
            if self.gval(t, phi) > self.thr:
                if j not in self.reported:
                    self._emit(j)
                    out.append(j)
        return out


class EventGate(PushGate):
    """Shared event-queue machinery for (b) and (b').

    Each boundary slot carries a certificate: a value of phi above which it
    provably cannot violate.  phi decreases monotonically, so a max-heap on
    the certificate phi yields the next slot that must be looked at.  A slot
    is re-keyed only when one of its interior neighbours moves."""


class LazyBound(EventGate):
    """(b) sound UPPER BOUND per boundary vertex + heap; exact recompute only
    when the bound crosses the threshold.

    Between touches P_j, M_j are frozen and G_j(phi) = (b_j - P_j -
    phi*M_j)/sqrt(d_j) moves only through phi.  The *generic* drift bound
    (no sign information used) is
        |G_j(phi) - G_j(phi_ref)| <= |M_j| * (phi_ref - phi) / sqrt(d_j)
    so j cannot violate while  phi > phi_ref - (thr - G_j^ref)*sqrt(d_j)/|M_j|.
    Key the max-heap by that "bound-crossing phi"; phi is decreasing, so the
    top of the heap is the next vertex whose CERTIFICATE expires.  A wakeup
    that finds no violation is a FALSE wakeup (charged, re-keyed)."""
    name = "lazy_bound"

    def __init__(self, R, meter, mult=1.0):
        super().__init__(R, meter, mult)
        self.key = [None] * self.nb
        self.heap = []
        self.alive = [True] * self.nb

    def init_state(self, p, Mh, phi):
        super().init_state(p, Mh, phi)
        self.heap = []
        for t in range(self.nb):
            self._rekey(t, phi, charge=False)

    def _rekey(self, t, phi, charge=True):
        pc = self._crossing_phi(t, phi)
        self.key[t] = pc
        if pc > 0.0 or pc == float("inf"):
            heapq.heappush(self.heap, (-pc, t))
            if charge:
                self._heap(len(self.heap))

    def note_update(self, i, dp, dMh, phi):
        touched = super().note_update(i, dp, dMh, phi)
        for (t, _q) in touched:
            if self.alive[t]:
                self._rekey(t, phi)
        return touched

    def note_flush(self, phi):
        super().note_flush(phi)
        for t in range(self.nb):
            if self.alive[t]:
                self._rekey(t, 1.0)

    def poll(self, k, phi, x):
        self.sweeps += 1
        out = []
        while self.heap:
            negp, t = self.heap[0]
            pc = -negp
            if pc != self.key[t]:              # stale entry
                heapq.heappop(self.heap)
                self._heap(len(self.heap) + 1)
                continue
            if pc < phi:                       # certificate still valid
                break
            heapq.heappop(self.heap)
            self._heap(len(self.heap) + 1)
            self.meter.rec(1)                  # exact O(1) recompute
            self.wakeups += 1
            if self.gval(t, phi) > self.thr:
                j = self.R.Bnodes[t]
                self.alive[t] = False
                if j not in self.reported:
                    self._emit(j)
                    out.append(j)
            else:
                self.false_wakeups += 1
                self.key[t] = None
                self._rekey(t, phi)
        return out

    def _crossing_phi(self, t, phi):
        g = self.gval(t, phi)
        slack = self.thr - g
        m = abs(self.M[t])
        if slack <= 0.0:
            return float("inf")
        if m <= 0.0:
            return -1.0                     # frozen strictly below threshold
        return phi - slack * self.Bsqd[t] / m


class Kinetic(LazyBound):
    """(b') exact event queue.  Between touches G_j is an exact affine
    function of phi, so the crossing phi is available in closed form:
        G_j(phi) > thr  <=>  phi * M_j < b_j - P_j - thr*sqrt(d_j) =: c_j
    M_j > 0 : crossing at phi < c_j/M_j (phi decreases -> will happen)
    M_j < 0 : crossing at phi > c_j/M_j (phi decreases -> will NOT happen)
    M_j = 0 : violating iff c_j > 0, forever.
    Max-heap on crossing phi; zero false wakeups by construction."""
    name = "kinetic"

    def _crossing_phi(self, t, phi):
        c = self.Bb[t] - self.P[t] - self.thr * self.Bsqd[t]
        m = self.M[t]
        if m == 0.0:
            return float("inf") if c > 0.0 else -1.0
        pc = c / m
        if m > 0.0:
            return pc if pc > 0.0 else -1.0     # crossing when phi drops < pc
        # m < 0: G increases with phi; already-violating iff phi > pc
        return float("inf") if phi > pc else -1.0


class DegreeBucket(GateBase):
    """(c) degree-bucketed PULL gate with a certified schedule.

    No accumulators (pure pull), but exploit that the threshold grows like
    sqrt(d_j) while the per-unit-motion drift of -grad_j falls like
    1/sqrt(d_j): in normalized terms the drift of G_j obeys
        |G_j(x') - G_j(x)| <= (1-alpha)/(2 d_j) * V,
        V := sum_{i in S} |x'_i - x_i| / sqrt(d_i)
    so a bucket of vertices with degree >= D needs re-scanning only after V
    has grown by  2*D*margin_min/(1-alpha), where margin_min is the smallest
    (thr - G_j) recorded in that bucket at its last scan.  V is computed once
    per poll at cost |S| (charged); each bucket is rescanned at cost
    vol(bucket)."""
    name = "deg_bucket"

    def __init__(self, R, meter, mult=1.0):
        super().__init__(R, meter, mult)
        self.buckets = {}
        for t, j in enumerate(R.Bnodes):
            lv = int(math.floor(math.log2(max(1, R.Bdeg[t]))))
            self.buckets.setdefault(lv, []).append(t)
        self.margin = {lv: 0.0 for lv in self.buckets}
        self.Vref = {lv: 0.0 for lv in self.buckets}
        self.xref = None
        self.V = 0.0
        self.al = R.model.alpha
        self.sqdS = np.array(R.sqd)
        self.bucket_scans = {lv: 0 for lv in self.buckets}

    def poll(self, k, phi, x):
        R = self.R
        self.sweeps += 1
        xa = np.asarray(x)
        if self.xref is None:
            self.xref = np.zeros(len(xa))
        self.V = float(np.sum(np.abs(xa - self.xref) / self.sqdS)) + self.V
        self.xref = xa.copy()
        self.meter.rec(R.n)                       # |S| to update V
        out = []
        for lv, ts in self.buckets.items():
            D = 2.0 ** lv
            budget = 2.0 * D * self.margin[lv] / (1.0 - self.al)
            if (self.V - self.Vref[lv]) < budget:
                continue                          # certificate still valid
            self.bucket_scans[lv] += 1
            mm = float("inf")
            for t in ts:
                if R.Bnodes[t] in self.reported:
                    continue
                g = -R.Bb[t]
                for (i, q) in R.Brows[t]:
                    g += q * x[i]
                self.meter.rec(R.Bdeg[t])
                self.wakeups += 1
                gv = -g / R.Bsqd[t]
                if gv > self.thr:
                    self._emit(R.Bnodes[t])
                    out.append(R.Bnodes[t])
                else:
                    mm = min(mm, self.thr - gv)
            self.margin[lv] = 0.0 if mm == float("inf") else mm
            self.Vref[lv] = self.V
        return out


STRUCTURES = {
    "eager_pull": EagerPull,
    "eager_push": EagerPush,
    "lazy_bound": LazyBound,
    "kinetic": Kinetic,
    "deg_bucket": DegreeBucket,
}
