"""Charged-work meter — a 6-counter approximation of the repository's
eleven-coordinate resource vector, documented per the shared problem
definition. Every adjacency scan of u costs d_u (first exposure -> C_adj,
repeats -> R_adj). Numerical flops/coordinate ops -> C_rec. Response
construction/application (factor updates, Schur, transfer) -> C_resp.
Materialized cells -> C_mat. Output writes -> C_emit.

All experiment claims should report meter.vector() alongside accuracy.
"""


class Meter:
    def __init__(self, adj):
        self.adj = adj
        self.d = {u: len(adj[u]) for u in adj}
        self.seen = set()
        self.C_adj = 0   # first-exposure adjacency work (sum of degrees)
        self.R_adj = 0   # repeated adjacency scans
        self.C_rec = 0   # numerical recurrence / coordinate ops
        self.C_resp = 0  # response construction/application/query
        self.C_mat = 0   # materialized intermediate cells
        self.C_emit = 0  # output writes

    def scan(self, u):
        if u in self.seen:
            self.R_adj += self.d[u]
        else:
            self.seen.add(u)
            self.C_adj += self.d[u]

    def rec(self, k=1):
        self.C_rec += k

    def resp(self, k=1):
        self.C_resp += k

    def mat(self, k=1):
        self.C_mat += k

    def emit(self, k=1):
        self.C_emit += k

    def total(self):
        return (self.C_adj + self.R_adj + self.C_rec + self.C_resp
                + self.C_mat + self.C_emit)

    def vector(self):
        return dict(C_adj=self.C_adj, R_adj=self.R_adj, C_rec=self.C_rec,
                    C_resp=self.C_resp, C_mat=self.C_mat, C_emit=self.C_emit,
                    total=self.total())

    def __repr__(self):
        return f"Meter({self.vector()})"
