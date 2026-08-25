"""I4-B: the eleven-coordinate charged-work ledger.

Coordinates (project promotion standard):
  C_adj   first-exposure adjacency work        (sum of d_u over first scans)
  R_adj   repeated adjacency scans of vertices in the EXPLORATION/BOUNDARY
          role (re-reading a boundary row, re-discovering a frontier)
  R_int   repeated reads of old ACTIVE rows by the interior solver
          (assembling / re-scanning Q[S,S] rows, level-0 smoother passes)
  C_pre   global preprocessing charged separately from seed-local work
  C_ctl   control: boundary tests, gate accumulator pushes, heap re-keys,
          interval refinements, TRIAGE, certificate verification
  C_rec   coordinate / gradient / splitting / Krylov / propagation ops
  C_resp  factor, elimination, Schur, response, sketch and preconditioner
          updates (incl. teardown write-offs on a mechanism switch)
  M_pers  peak persistent state cells carried between rounds
  M_tmp   peak temporary state cells (factors, hierarchies)
  C_mat   vector materialisation and state writes
  C_emit  output writes

W (charged work) = C_adj+R_adj+R_int+C_pre+C_ctl+C_rec+C_resp+C_mat+C_emit.
M_pers / M_tmp are SPACE and are reported but NOT summed into W.

APPROXIMATIONS, stated explicitly (see findings sec. "ledger honesty"):
 * R_adj vs R_int is a role split of the same physical operation (re-reading
   an adjacency row).  We assign a re-read to R_int iff the vertex is in the
   current active set S at the time of the read, else to R_adj.
 * C_ctl absorbs the kinetic-gate accumulator pushes.  Each pushed edge is
   ALSO counted in `piggy`, because it happens inside an interior row scan
   the solver has already been charged for; both totals are reported and the
   headline W double-counts them (conservative / over-charge).
 * C_pre is 0 for every method measured here: nothing is precomputed
   globally.  The exact reference solve used only for verification is not
   charged to any method.
 * M_pers / M_tmp are counted in cells (one float or one index = 1 cell).
"""
import numpy as np

KEYS = ["C_adj", "R_adj", "R_int", "C_pre", "C_ctl", "C_rec", "C_resp",
        "M_pers", "M_tmp", "C_mat", "C_emit"]
WORK_KEYS = ["C_adj", "R_adj", "R_int", "C_pre", "C_ctl", "C_rec", "C_resp",
             "C_mat", "C_emit"]


class Ledger:
    """Eleven-coordinate meter.  Exposes the VecMeter interface
    (scan_idx / rec / resp / mat / phase) so amglib's hierarchy builder and
    V-cycle can be charged unchanged."""

    def __init__(self, dvec):
        self.dv = np.asarray(dvec, float)
        self.seen = np.zeros(self.dv.shape[0], dtype=bool)
        self.inS = np.zeros(self.dv.shape[0], dtype=bool)
        for k in KEYS:
            setattr(self, k, 0.0)
        # sub-accounts (diagnostics, not extra coordinates)
        self.ctl_triage = 0.0     # cost of the triage test itself
        self.ctl_gate = 0.0       # cost of the boundary gate
        self.ctl_cert = 0.0       # cost of certificate evaluation
        self.resp_switch = 0.0    # write-off charged on a mechanism switch
        self.setup = 0.0
        self.solve = 0.0
        self.piggy = 0.0          # gate pushes inside an interior row scan
        self.agg = 0.0            # amglib aggregation charge (already in C_resp)
        self.agg_seq = 0.0
        self._phase = "solve"

    # -------- VecMeter-compatible interface -------------------------------
    def phase(self, p):
        self._phase = p

    def _ph(self, k):
        if self._phase == "setup":
            self.setup += k
        else:
            self.solve += k

    def scan_idx(self, idx):
        """Charge an adjacency read of every vertex in idx."""
        idx = np.asarray(idx)
        if idx.size == 0:
            return
        new = ~self.seen[idx]
        w_new = float(self.dv[idx[new]].sum())
        self.C_adj += w_new
        old = idx[~new]
        if old.size:
            act = self.inS[old]
            self.R_int += float(self.dv[old[act]].sum())
            self.R_adj += float(self.dv[old[~act]].sum())
        self.seen[idx] = True
        self._ph(w_new + float(self.dv[old].sum()) if old.size else w_new)

    def scan1(self, g):
        """Scalar fast path for scan_idx([g])."""
        d = float(self.dv[g])
        if self.seen[g]:
            if self.inS[g]:
                self.R_int += d
            else:
                self.R_adj += d
        else:
            self.seen[g] = True
            self.C_adj += d
        self._ph(d)

    def rec(self, k=1):
        self.C_rec += k
        self._ph(k)

    def resp(self, k=1):
        self.C_resp += k
        self._ph(k)

    def mat(self, k=1):
        self.C_mat += k
        self._ph(k)

    # -------- I4-B specific -----------------------------------------------
    def ctl(self, k=1, kind="gate"):
        self.C_ctl += k
        self._ph(k)
        if kind == "triage":
            self.ctl_triage += k
        elif kind == "cert":
            self.ctl_cert += k
        else:
            self.ctl_gate += k

    def switch_writeoff(self, cells):
        self.C_resp += cells
        self.resp_switch += cells
        self._ph(cells)

    def emit(self, k=1):
        self.C_emit += k
        self._ph(k)

    def persist(self, cells):
        self.M_pers = max(self.M_pers, float(cells))

    def temp(self, cells):
        self.M_tmp = max(self.M_tmp, float(cells))

    def set_active(self, idx):
        self.inS[np.asarray(idx, dtype=np.int64)] = True

    # -------- reporting ----------------------------------------------------
    def W(self):
        return float(sum(getattr(self, k) for k in WORK_KEYS))

    def vector(self):
        v = {k: float(getattr(self, k)) for k in KEYS}
        v["W"] = self.W()
        v["ctl_triage"] = self.ctl_triage
        v["ctl_gate"] = self.ctl_gate
        v["ctl_cert"] = self.ctl_cert
        v["resp_switch"] = self.resp_switch
        v["setup"] = self.setup
        v["solve"] = self.solve
        v["piggy"] = self.piggy
        return v


def from_vecmeter(v, split_rint=0.0):
    """Map a 6-counter VecMeter vector (I3-A campaign code) onto the eleven
    coordinates.  APPROXIMATE: VecMeter does not separate the boundary role
    from the active role, nor control work from coordinate work, so
      R_int <- split_rint * R_adj  (0 by default: everything left in R_adj),
      C_ctl <- 0 (certificate work is inside C_rec there),
      C_pre <- 0, M_pers/M_tmp <- unmeasured (reported as NaN).
    W is identical to VecMeter.total() in every case."""
    out = {k: 0.0 for k in KEYS}
    out["C_adj"] = v["C_adj"]
    out["R_adj"] = v["R_adj"] * (1.0 - split_rint)
    out["R_int"] = v["R_adj"] * split_rint
    out["C_rec"] = v["C_rec"]
    out["C_resp"] = v["C_resp"]
    out["C_mat"] = v["C_mat"]
    out["M_pers"] = float("nan")
    out["M_tmp"] = float("nan")
    out["W"] = v["total"]
    return out
