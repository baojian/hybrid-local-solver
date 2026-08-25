/* Literal C port of lib/model.py:appr_lazy (FIFO lazy ACL push).
 * Semantics identical: pop-left; skip stale (r[u] < eps*d[u], no charge);
 * push: p[u]+=alpha*xi, r[u]=a*xi, r[w]+=a*xi/d[u]; enqueue neighbors that
 * newly cross threshold, then re-enqueue u if still active.
 * Work accounting mirrors Meter.scan: first exposure of u -> W_first += d_u,
 * repeats -> W_rep += d_u.  Charged only on executed pushes (as in lib).
 */
#include <string.h>

long long cpush(int n, const int *indptr, const int *indices,
                double alpha, double eps, int seed,
                double *p, double *r,
                long long *W_first, long long *W_rep,
                unsigned char *seen, unsigned char *inq, int *queue)
{
    double a = (1.0 - alpha) / 2.0;
    long long wf = 0, wr = 0, npush = 0;
    memset(seen, 0, (size_t)n);
    memset(inq, 0, (size_t)n);
    for (int i = 0; i < n; i++) { p[i] = 0.0; r[i] = 0.0; }
    r[seed] = 1.0;
    int cap = n + 1, head = 0, tail = 0;
    queue[tail++] = seed; if (tail == cap) tail = 0;
    inq[seed] = 1;
    while (head != tail) {
        int u = queue[head++]; if (head == cap) head = 0;
        inq[u] = 0;
        int du = indptr[u + 1] - indptr[u];
        if (r[u] < eps * du) continue;
        double xi = r[u];
        if (seen[u]) wr += du; else { seen[u] = 1; wf += du; }
        npush++;
        p[u] += alpha * xi;
        r[u] = a * xi;
        for (int k = indptr[u]; k < indptr[u + 1]; k++) {
            int w = indices[k];
            int dw = indptr[w + 1] - indptr[w];
            r[w] += a * xi / du;
            if (!inq[w] && r[w] >= eps * dw) {
                queue[tail++] = w; if (tail == cap) tail = 0;
                inq[w] = 1;
            }
        }
        if (!inq[u] && r[u] >= eps * du) {
            queue[tail++] = u; if (tail == cap) tail = 0;
            inq[u] = 1;
        }
    }
    *W_first = wf; *W_rep = wr;
    return npush;
}
