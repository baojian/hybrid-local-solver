import argparse
import time
import numpy as np
from numpy import bool_
from numpy import sqrt
from numpy import int64
from numpy import float64
from numba import njit
from numba import objmode
from numpy.linalg import norm

"""
This module is for symmetric diagonally dominant solvers:

        Qx=b, where

        Q is symmetric diagonally dominant
        Q = I - ((1-alpha)/(1+alpha))*D^{-1/2} A D^{-1/2}
        b = 2*alpha/(1+alpha) D^{-1/2} e_s
"""


@njit(cache=True)
def sdd_get_opt(n, indptr, indices, degree, source, alpha, eps):
    with objmode(start="f8"):
        start = time.perf_counter()
    xt = np.zeros(n, dtype=float64)
    grad = np.zeros(n, dtype=float64)
    const = (1.0 - alpha) / (1.0 + alpha)
    sq_deg = sqrt(degree)
    ind = 0
    while True:
        grad[:] = xt
        for u in np.arange(n):
            val = const * xt[u] / degree[u]
            for v in indices[indptr[u] : indptr[u + 1]]:
                grad[v] -= val
        grad[source] += -(2.0 * alpha) / (1.0 + alpha)
        xt[:] = xt - grad
        err = np.linalg.norm(grad, 1)
        ind += 1
        if err < eps:
            break
    with objmode(run_time="f8"):
        run_time = time.perf_counter() - start
    # separate objmode block with no outputs: nopython mode has no
    # str.format(), and putting the print in the block above would make
    # run_time non-outgoing.
    with objmode():
        print(
            "get true ppv: error={:.6e} iterations={:,} run-time={:.6f}s".format(err, ind, run_time)
        )
    return xt / sq_deg


@njit(cache=True)
def sdd_global_gd(n, indptr, indices, degree, b, alpha, eps, opt_x, l1_err):
    with objmode(start="f8"):
        start = time.perf_counter()

    xt = np.zeros(n, dtype=float64)
    rt = np.zeros(n, dtype=float64)
    tmp = np.zeros(n, dtype=float64)
    sq_deg = sqrt(degree)
    rt[:] = sq_deg * b
    eps_vec = eps * degree
    const = (1.0 - alpha) / (1.0 + alpha)

    errs = []
    opers = []
    op_time = np.float64(0.0)
    while True:
        xt += rt
        tmp[:] = 0.0
        for u in np.arange(n):
            val = const * rt[u] / degree[u]
            for v in indices[indptr[u] : indptr[u + 1]]:
                tmp[v] += val
        rt[:] = tmp

        # ------ debug time ------
        with objmode(debug_start="f8"):
            debug_start = time.perf_counter()
        if opt_x is not None:
            err = norm(xt / sq_deg - opt_x, 1)
            errs.append(err)
        else:
            errs.append(np.inf)
        opers.append(np.sum(degree))
        with objmode(op_time="f8"):
            op_time += time.perf_counter() - debug_start
        # ------------------------

        if np.sum(eps_vec <= np.abs(rt)) <= 0.0 or np.abs(errs[-1]) <= 0.0:
            break
        if l1_err is not None and errs[-1] <= l1_err:
            break
    with objmode(run_time="f8"):
        run_time = time.perf_counter() - start
    return xt / sq_deg, rt, errs, opers, run_time, op_time


@njit(cache=True)
def sdd_local_gd(n, indptr, indices, degree, b, alpha, eps, opt_x):
    with objmode(start="f8"):
        start = time.perf_counter()

    xt = np.zeros(n, dtype=float64)
    rt = np.zeros(n, dtype=float64)
    eps_vec = eps * alpha * degree
    sq_deg = sqrt(degree)
    const = (1.0 - alpha) / (1.0 + alpha)

    # queue data structure
    s = np.nonzero(b)[0]
    rt[s[0]] = b[s[0]] * np.sqrt(degree[s[0]])
    queue = np.zeros(n, dtype=int64)
    queue[: len(s)] = s
    q_mark = np.zeros(n, dtype=bool_)
    q_mark[s] = True
    rear = len(s)
    st = np.zeros(n, dtype=int64)
    vl = np.zeros(n, dtype=float64)
    st_len = rear

    errs = []
    opers = []
    op_time = np.float64(0.0)
    while True:
        # updates for current iteration from queue
        if st_len < n / 4:
            st[:st_len] = queue[:st_len]
        else:  # use continuous memory
            st[:st_len] = np.nonzero(q_mark)[0]
        vl[:st_len] = rt[st[:st_len]]
        q_mark[st[:st_len]] = False
        rear = 0

        # --- debug ---
        with objmode(debug_start="f8"):
            debug_start = time.perf_counter()
        with objmode(op_time="f8"):
            op_time += time.perf_counter() - debug_start

        # ------ debug time ------
        with objmode(debug_start="f8"):
            debug_start = time.perf_counter()
        if opt_x is not None:
            errs.append(norm(xt / sq_deg - opt_x, 1))
        else:
            errs.append(np.inf)  # fakes
        opers.append(np.sum(degree[st[:st_len]]))
        with objmode(op_time="f8"):
            op_time += time.perf_counter() - debug_start
        # ------------------------

        xt[st[:st_len]] += vl[:st_len]
        rt[st[:st_len]] -= vl[:st_len]
        for ind in range(st_len):
            u = st[ind]
            val = const * vl[ind] / degree[u]
            for v in indices[indptr[u] : indptr[u + 1]]:
                rt[v] += val
                if not q_mark[v] and eps_vec[v] <= rt[v]:
                    queue[rear] = v
                    q_mark[v] = True
                    rear += 1
        st_len = rear
        # queue is empty now, quit
        if rear == 0:
            break

    with objmode(run_time="f8"):
        run_time = time.perf_counter() - start
    return xt / sq_deg, rt, errs, opers, run_time, op_time


@njit(cache=True)
def sdd_global_sor(n, indptr, indices, degree, b, alpha, eps, omega, opt_x, l1_err):
    with objmode(start="f8"):
        start = time.perf_counter()
    # --- initialization ---
    xt = np.zeros(n, dtype=float64)
    rt = np.zeros(n, dtype=float64)
    sq_deg = sqrt(degree)
    rt[:] = sq_deg * b
    eps_vec = eps * degree
    const = (1.0 - alpha) / (1.0 + alpha)

    # results
    errs = []
    opers = []
    op_time = np.float64(0.0)
    oper = 0.0
    with objmode(debug_start="f8"):
        debug_start = time.perf_counter()
    with objmode(op_time="f8"):
        op_time += time.perf_counter() - debug_start
    while True:
        for u in range(n):
            oper += degree[u]
            delta = omega * rt[u]
            xt[u] += delta
            rt[u] -= delta
            val = const * delta / degree[u]
            for v in indices[indptr[u] : indptr[u + 1]]:
                rt[v] += val

        # ------ debug time ------
        with objmode(debug_start="f8"):
            debug_start = time.perf_counter()
        # minimal l1-err meets
        err = norm(xt / sq_deg - opt_x, 1)
        if opt_x is not None:
            errs.append(err)
        else:
            errs.append(np.inf)  # fakes
        opers.append(oper)
        oper = 0.0
        with objmode(op_time="f8"):
            op_time += time.perf_counter() - debug_start
        # ------------------------

        # all nodes are inactive or get exact solution
        if np.sum(eps_vec <= np.abs(rt)) <= 0.0 or np.abs(errs[-1]) <= 0.0:
            break
        if l1_err is not None and err <= l1_err:
            break

    with objmode(run_time="f8"):
        run_time = time.perf_counter() - start
    return xt / sq_deg, rt, errs, opers, run_time, op_time


@njit(cache=True)
def sdd_local_appr(n, indptr, indices, degree, s, alpha, eps, opt_x=None):
    with objmode(start="f8"):
        start = time.perf_counter()
    # --- initialization ---
    xt = np.zeros(n, dtype=float64)
    rt = np.zeros(n, dtype=float64)
    rt[:] = s
    sq_deg = sqrt(degree)
    eps_vec = eps * degree
    # ----------------------
    # queue data structure
    st = np.nonzero(s)[0]
    front = int64(0)
    # One slot for every vertex, one for the iteration flag, and one spare
    # slot so the circular queue never confuses a full frontier with an empty
    # one.
    queue_capacity = n + 2
    queue = np.zeros(queue_capacity, dtype=int64)
    queue[: len(st)] = st
    q_mark = np.zeros(n + 1, dtype=bool_)
    q_mark[st] = True
    rear = len(st)
    queue[rear] = n  # iteration flag
    q_mark[n] = True
    rear += 1

    # results
    errs = []
    opers = []
    op_time = np.float64(0.0)
    oper = 0.0
    with objmode(debug_start="f8"):
        debug_start = time.perf_counter()
    with objmode(op_time="f8"):
        op_time += time.perf_counter() - debug_start

    while True:
        u = queue[front]
        q_mark[u] = False
        front = (front + 1) % queue_capacity
        if u == n:  # one local iteration
            # ------ debug time ------
            with objmode(debug_start="f8"):
                debug_start = time.perf_counter()
            if opt_x is not None:
                errs.append(norm(xt / sq_deg - opt_x, 1))
            else:
                errs.append(np.inf)  # fakes
            opers.append(oper)
            oper = 0.0
            with objmode(op_time="f8"):
                op_time += time.perf_counter() - debug_start
            # ------------------------

            queue[rear] = n
            rear = (rear + 1) % queue_capacity
            continue

        oper += degree[u]
        delta = 0.5 * (1.0 - alpha) * rt[u]
        xt[u] += alpha * rt[u]
        rt[u] = delta
        # ACL Algorithm 1 requires an active pushed vertex to return to the
        # queue. Without this check the routine can stop with r[u] >= eps*d[u]
        # when none of u's neighbors becomes active.
        if not q_mark[u] and eps_vec[u] <= rt[u]:
            queue[rear] = u
            q_mark[u] = True
            rear = (rear + 1) % queue_capacity
        for v in indices[indptr[u] : indptr[u + 1]]:
            rt[v] += delta / degree[u]
            if not q_mark[v] and eps_vec[v] <= rt[v]:
                queue[rear] = v
                q_mark[v] = True
                rear = (rear + 1) % queue_capacity
        # only iteration flag left, quit
        if (rear - front) % queue_capacity == 1:
            # ------ debug time ------
            with objmode(debug_start="f8"):
                debug_start = time.perf_counter()
            if opt_x is not None:
                errs.append(norm(xt / sq_deg - opt_x, 1))
            else:
                errs.append(np.inf)  # fakes
            opers.append(oper)
            with objmode(op_time="f8"):
                op_time += time.perf_counter() - debug_start
            break
            # ------------------------
    with objmode(run_time="f8"):
        run_time = time.perf_counter() - start
    return xt, rt, errs, opers, run_time, op_time


@njit(cache=True)
def sdd_local_sor(n, indptr, indices, degree, b, alpha, eps, omega, opt_x):
    with objmode(start="f8"):
        start = time.perf_counter()
    # --- initialization ---
    xt = np.zeros(n, dtype=float64)
    rt = np.zeros(n, dtype=float64)
    eps_vec = eps * alpha * degree
    const = (1.0 - alpha) / (1.0 + alpha)
    # ----------------------
    # queue data structure
    s = np.nonzero(b)[0]
    rt[s[0]] = b[s[0]] * np.sqrt(degree[s[0]])
    front = int64(0)
    queue = np.zeros(n + 1, dtype=int64)
    queue[: len(s)] = s
    q_mark = np.zeros(n + 1, dtype=bool_)
    q_mark[s] = True
    rear = len(s)
    queue[rear] = n  # iteration flag
    q_mark[n] = True
    rear += 1

    # results
    errs = []
    opers = []
    op_time = np.float64(0.0)
    oper = np.float64(0.0)
    with objmode(debug_start="f8"):
        debug_start = time.perf_counter()
    with objmode(op_time="f8"):
        op_time += time.perf_counter() - debug_start

    while True:
        u = queue[front]
        q_mark[u] = False
        front = (front + 1) % n
        if u == n:  # one local iteration
            # ------ debug time ------
            with objmode(debug_start="f8"):
                debug_start = time.perf_counter()
            sq_deg = sqrt(degree)
            if opt_x is not None:
                errs.append(norm(xt / sq_deg - opt_x, 1))
            else:
                errs.append(np.inf)  # fakes
            opers.append(oper)
            oper = 0.0
            with objmode(op_time="f8"):
                op_time += time.perf_counter() - debug_start
            # ------------------------

            queue[rear] = n
            rear = (rear + 1) % n
            continue
        oper += degree[u]
        delta = omega * rt[u]
        xt[u] += delta
        rt[u] -= delta
        val = const * delta / degree[u]
        for v in indices[indptr[u] : indptr[u + 1]]:
            rt[v] += val
            if not q_mark[v] and eps_vec[v] <= np.abs(rt[v]):
                queue[rear] = v
                q_mark[v] = True
                rear = (rear + 1) % n
        # only iteration flag left, quit
        if (rear - front) == 1:
            if len(errs) != 0:
                break
            # ------ debug time ------
            with objmode(debug_start="f8"):
                debug_start = time.perf_counter()
            sq_deg = np.sqrt(degree)
            if opt_x is not None:
                errs.append(norm(xt / sq_deg - opt_x, 1))
            else:
                errs.append(np.inf)  # fakes
            opers.append(oper)
            with objmode(op_time="f8"):
                op_time += time.perf_counter() - debug_start
            break
            # ------------------------
    with objmode(run_time="f8"):
        run_time = time.perf_counter() - start
    return xt / sqrt(degree), rt, errs, opers, run_time, op_time


@njit(cache=True)
def sdd_global_heavy_ball(n, indptr, indices, degree, b, alpha, eps, opt_x, l1_err):
    with objmode(start="f8"):
        start = time.perf_counter()
    # ----------------------
    xt_tilde = np.zeros(n, dtype=float64)
    delta_cur = np.zeros(n, dtype=float64)
    delta_pre = np.zeros(n, dtype=float64)
    xt = np.zeros(n, dtype=float64)
    rt = np.zeros(n, dtype=float64)
    sq_deg = sqrt(degree)
    rt[:] = sq_deg * b
    eps_vec = eps * alpha * degree
    const = (1.0 - alpha) / (1.0 + alpha)
    tmp_r = np.zeros_like(rt)
    beta1 = 1.0 + ((1.0 - sqrt(alpha)) / (1.0 + sqrt(alpha))) ** 2.0
    beta2 = ((1.0 - sqrt(alpha)) / (1.0 + sqrt(alpha))) ** 2

    # ----------------------
    errs = []
    opers = []
    op_time = np.float64(0.0)

    while True:
        delta_cur[:] = beta1 * rt + beta2 * xt_tilde
        xt[:] += delta_cur
        tmp_r[:] = 0.0
        for u in np.arange(n):
            val = const * delta_cur[u] / degree[u]
            for v in indices[indptr[u] : indptr[u + 1]]:
                tmp_r[v] += val
        rt[:] += tmp_r - delta_cur
        xt_tilde[:] += delta_cur - delta_pre
        delta_pre[:] = delta_cur

        # ------ debug time ------
        with objmode(debug_start="f8"):
            debug_start = time.perf_counter()
        # minimal l1-err meets
        err = norm(xt / sq_deg - opt_x, 1)
        if opt_x is not None:
            errs.append(err)
        else:
            errs.append(np.inf)  # fakes
        opers.append(np.sum(degree))
        with objmode(op_time="f8"):
            op_time += time.perf_counter() - debug_start
        # ------------------------
        # all nodes are inactive or get exact solution
        if np.sum(eps_vec <= np.abs(rt)) <= 0.0 or np.abs(errs[-1]) <= 0.0:
            break
        if l1_err is not None and err <= l1_err:
            break

    with objmode(run_time="f8"):
        run_time = time.perf_counter() - start
    return xt / sq_deg, rt, errs, opers, run_time, op_time


@njit(cache=True)
def sdd_local_heavy_ball(n, indptr, indices, degree, b, alpha, eps, opt_x):
    with objmode(start="f8"):
        start = time.perf_counter()
    # ----------------------
    xt_tilde = np.zeros(n, dtype=float64)
    xt = np.zeros(n, dtype=float64)
    rt = np.zeros(n, dtype=float64)
    eps_vec = eps * alpha * degree
    const = (1.0 - alpha) / (1.0 + alpha)
    beta1 = 1.0 + ((1.0 - sqrt(alpha)) / (1.0 + sqrt(alpha))) ** 2.0
    beta2 = ((1.0 - sqrt(alpha)) / (1.0 + sqrt(alpha))) ** 2

    # ----------------------
    # queue data structure
    s = np.nonzero(b)[0]
    rt[s[0]] = b[s[0]] * np.sqrt(degree[s[0]])
    queue = np.zeros(n, dtype=int64)
    queue[: len(s)] = s
    q_mark = np.zeros(n, dtype=bool_)
    q_mark[s] = True
    rear = len(s)
    st1 = np.zeros(n, dtype=int64)
    vl1 = np.zeros(n, dtype=float64)
    st1_len = 0
    st2 = np.zeros(n, dtype=int64)
    vl2 = np.zeros(n, dtype=float64)
    st2_len = rear

    # ----------------------
    errs = []
    opers = []
    op_time = np.float64(0.0)

    while True:
        # updates for current iteration from queue
        if st2_len < n / 4:
            st2[:st2_len] = queue[:st2_len]
        else:  # continuous memory
            st2[:st2_len] = np.nonzero(q_mark)[0]
        # st2[:st2_len] = queue[:st2_len]

        vl2[:st2_len] = beta1 * rt[st2[:st2_len]] + beta2 * xt_tilde[st2[:st2_len]]
        q_mark[st2[:st2_len]] = False

        # --- debug ---
        with objmode(debug_start="f8"):
            debug_start = time.perf_counter()
        sq_deg = sqrt(degree)
        with objmode(op_time="f8"):
            op_time += time.perf_counter() - debug_start
        # -------------

        rear = 0
        xt[st2[:st2_len]] += vl2[:st2_len]
        rt[st2[:st2_len]] -= vl2[:st2_len]
        for ind in range(st2_len):
            u = st2[ind]
            val = const * vl2[ind] / degree[u]
            for v in indices[indptr[u] : indptr[u + 1]]:
                rt[v] += val
                if not q_mark[v] and eps_vec[v] <= np.abs(rt[v]):
                    queue[rear] = v
                    q_mark[v] = True
                    rear += 1
        xt_tilde[st2[:st2_len]] += vl2[:st2_len]
        xt_tilde[st1[:st1_len]] -= vl1[:st1_len]

        st1[:st2_len] = st2[:st2_len]
        vl1[:st2_len] = vl2[:st2_len]
        st1_len = st2_len
        st2_len = rear

        # ------ debug time ------
        with objmode(debug_start="f8"):
            debug_start = time.perf_counter()
        # minimal l1-err meets
        if opt_x is not None:
            err = norm(xt / sq_deg - opt_x, 1)
            errs.append(err)
        else:
            errs.append(np.inf)  # fakes
        opers.append(np.sum(degree[st1[:st1_len]]))
        with objmode(op_time="f8"):
            op_time += time.perf_counter() - debug_start
        # ------------------------
        # queue is empty now, quit
        if rear == 0:
            break

    with objmode(run_time="f8"):
        run_time = time.perf_counter() - start
    return xt / sq_deg, rt, errs, opers, run_time, op_time


@njit(cache=True)
def sdd_global_cheby(n, indptr, indices, degree, b, alpha, eps, opt_x, l1_err):
    with objmode(start="f8"):
        start = time.perf_counter()
    # ----------------------
    xt_tilde = np.zeros(n, dtype=float64)
    delta_cur = np.zeros(n, dtype=float64)
    delta_pre = np.zeros(n, dtype=float64)
    xt = np.zeros(n, dtype=float64)
    rt = np.zeros(n, dtype=float64)
    sq_deg = sqrt(degree)
    rt[:] = sq_deg * b
    xt_tilde[:] = rt
    xt[:] = rt
    delta_pre[:] = rt
    eps_vec = eps * degree
    const = (1.0 - alpha) / (1.0 + alpha)
    delta_t = const

    tmp_r = np.zeros(n, dtype=float64)
    tmp_r[:] = 0.0
    for u in np.arange(n):
        val = const * delta_pre[u] / degree[u]
        for v in indices[indptr[u] : indptr[u + 1]]:
            tmp_r[v] += val
    rt[:] = tmp_r

    # ----------------------
    errs = []
    opers = []
    op_time = np.float64(0.0)

    while True:
        delta_t = 1.0 / (2.0 / const - delta_t)
        beta = 2.0 * delta_t / const

        delta_cur[:] = beta * rt + (beta - 1.0) * xt_tilde
        xt[:] += delta_cur
        tmp_r[:] = 0.0
        for u in np.arange(n):
            val = const * delta_cur[u] / degree[u]
            for v in indices[indptr[u] : indptr[u + 1]]:
                tmp_r[v] += val
        rt[:] += tmp_r - delta_cur
        xt_tilde[:] += delta_cur - delta_pre
        delta_pre[:] = delta_cur

        # ------ debug time ------
        with objmode(debug_start="f8"):
            debug_start = time.perf_counter()
        # minimal l1-err meets
        err = norm(xt / sq_deg - opt_x, 1)
        if opt_x is not None:
            errs.append(err)
        else:
            errs.append(np.inf)  # fakes
        opers.append(np.sum(degree))
        with objmode(op_time="f8"):
            op_time += time.perf_counter() - debug_start
        # ------------------------
        # all nodes are inactive or get exact solution
        if np.sum(eps_vec <= np.abs(rt)) <= 0.0 or np.abs(errs[-1]) <= 0.0:
            break
        if l1_err is not None and err <= l1_err:
            break

    with objmode(run_time="f8"):
        run_time = time.perf_counter() - start
    return xt / sq_deg, rt, errs, opers, run_time, op_time


@njit(cache=True)
def sdd_local_cheby(n, indptr, indices, degree, b, alpha, eps, opt_x):
    with objmode(start="f8"):
        start = time.perf_counter()
    # ----------------------
    xt_tilde = np.zeros(n, dtype=float64)
    xt = np.zeros(n, dtype=float64)
    rt = np.zeros(n, dtype=float64)
    # ----------------------
    # queue data structure
    s = np.nonzero(b)[0]
    rt[s[0]] = b[s[0]] * np.sqrt(degree[s[0]])
    xt_tilde[s[0]] = rt[s[0]]
    xt[s[0]] = rt[s[0]]
    queue = np.zeros(n, dtype=int64)
    queue[: len(s)] = s
    q_mark = np.zeros(n, dtype=bool_)
    q_mark[s] = True
    rear = len(s)
    eps_vec = eps * alpha * degree
    const = (1.0 - alpha) / (1.0 + alpha)
    delta_t = const

    st1 = np.zeros(n, dtype=int64)
    vl1 = np.zeros(n, dtype=float64)
    st1_len = rear
    st1[:st1_len] = queue[:st1_len]
    vl1[:st1_len] = rt[st1[:st1_len]]
    q_mark[st1[:st1_len]] = False

    rear = 0
    rt[st1[:st1_len]] = 0.0
    for ind in range(st1_len):
        u = st1[ind]
        val = const * vl1[ind] / degree[u]
        for v in indices[indptr[u] : indptr[u + 1]]:
            rt[v] += val
            if not q_mark[v] and eps_vec[v] <= np.abs(rt[v]):
                queue[rear] = v
                q_mark[v] = True
                rear += 1
    st2 = np.zeros(n, dtype=int64)
    vl2 = np.zeros(n, dtype=float64)
    st2_len = rear
    # ----------------------
    errs = []
    opers = []
    op_time = np.float64(0.0)

    while True:
        delta_t = 1.0 / (2.0 / const - delta_t)
        beta = 2.0 * delta_t / const

        # updates for current iteration from queue
        if st2_len < n / 4:
            st2[:st2_len] = queue[:st2_len]
        else:  # continuous memory
            st2[:st2_len] = np.nonzero(q_mark)[0]
        # st2[:st2_len] = queue[:st2_len]

        vl2[:st2_len] = beta * rt[st2[:st2_len]] + (beta - 1.0) * xt_tilde[st2[:st2_len]]
        q_mark[st2[:st2_len]] = False

        # --- debug ---
        with objmode(debug_start="f8"):
            debug_start = time.perf_counter()
        sq_deg = sqrt(degree)
        with objmode(op_time="f8"):
            op_time += time.perf_counter() - debug_start
        # -------------

        rear = 0
        xt[st2[:st2_len]] += vl2[:st2_len]
        rt[st2[:st2_len]] -= vl2[:st2_len]
        for ind in range(st2_len):
            u = st2[ind]
            val = const * vl2[ind] / degree[u]
            for v in indices[indptr[u] : indptr[u + 1]]:
                rt[v] += val
                if not q_mark[v] and eps_vec[v] <= np.abs(rt[v]):
                    queue[rear] = v
                    q_mark[v] = True
                    rear += 1
        xt_tilde[st2[:st2_len]] += vl2[:st2_len]
        xt_tilde[st1[:st1_len]] -= vl1[:st1_len]

        # ------ debug time ------
        with objmode(debug_start="f8"):
            debug_start = time.perf_counter()
        # minimal l1-err meets
        if opt_x is not None:
            err = norm(xt / sq_deg - opt_x, 1)
            errs.append(err)
        else:
            errs.append(np.inf)  # fakes
        opers.append(np.sum(degree[st1[:st1_len]]))
        with objmode(op_time="f8"):
            op_time += time.perf_counter() - debug_start
        # ------------------------
        st1[:st2_len] = st2[:st2_len]
        vl1[:st2_len] = vl2[:st2_len]
        st1_len = st2_len
        st2_len = rear

        # queue is empty now, quit
        if rear == 0:
            break

    with objmode(run_time="f8"):
        run_time = time.perf_counter() - start
    return xt / sq_deg, rt, errs, opers, run_time, op_time


@njit(cache=True)
def sdd_global_cgm(n, indptr, indices, degree, b, alpha, eps, opt_x, l1_err):
    with objmode(start="f8"):
        start = time.perf_counter()
    xt = np.zeros(n, dtype=float64)
    tmp_v = np.zeros(n, dtype=float64)
    rt = np.zeros_like(xt)
    p = np.zeros_like(xt)
    ap = np.zeros_like(p)
    sq_deg = sqrt(degree)

    eps_vec = eps * sq_deg
    rt[:] = b
    rt_pre = np.dot(rt, rt)
    p[:] = rt  # conjugate direction

    # ----------------------
    errs = []
    opers = []
    op_time = np.float64(0.0)
    while True:
        if rt_pre <= 0.0:
            break
        tmp_v *= 0.0
        for u in np.arange(n):
            tmp = p[u] / sq_deg[u]
            for v in indices[indptr[u] : indptr[u + 1]]:
                tmp_v[v] += tmp / sq_deg[v]
        ap[:] = p - ((1.0 - alpha) / (1.0 + alpha)) * tmp_v
        alpha_t = rt_pre / np.dot(p, ap)
        xt[:] = xt + alpha_t * p
        rt[:] = rt - alpha_t * ap
        r_cur = np.dot(rt, rt)
        beta_t = r_cur / rt_pre
        rt_pre = r_cur
        p[:] = rt + beta_t * p

        # ------ debug time ------
        with objmode(debug_start="f8"):
            debug_start = time.perf_counter()
        if opt_x is not None:
            err = norm(xt - opt_x, 1)
        else:
            err = np.inf
        if opt_x is not None:
            errs.append(err)
        else:
            errs.append(np.inf)  # fakes
        opers.append(np.sum(degree))
        with objmode(op_time="f8"):
            op_time += time.perf_counter() - debug_start
        # ------------------------
        # all nodes are inactive or get exact solution
        if np.sum(eps_vec <= np.abs(rt)) <= 0.0 or np.abs(errs[-1]) <= 0.0:
            break
        # minimal l1-err meets
        if l1_err is not None and err <= l1_err:
            break
    with objmode(run_time="f8"):
        run_time = time.perf_counter() - start
    return xt, rt, errs, opers, run_time, op_time


def parse_eps(eps_arg, n):
    """Turn the --eps string into a number.

    Accepts either a plain value ('1e-6', '3.15e-06') or an '<x>/n' expression
    ('1./n', '.1/n', '1e-4/n', or bare '/n' meaning 1/n), where n is the node
    count of the graph actually loaded -- which is why this is resolved here
    rather than by argparse's type=, since n is not known until load time.
    """
    s = str(eps_arg).strip()
    if s.endswith("/n"):
        num = s[:-2].strip()
        eps = (1.0 if num in ("", "+") else float(num)) / n
    else:
        eps = float(s)
    if not eps > 0.0:
        raise ValueError(f"--eps must be positive, got {eps_arg!r} -> {eps}")
    return eps


def opt_omega(alpha):
    """Textbook optimal SOR relaxation: minimizes the GLOBAL iteration matrix's
    spectral radius.  = 2/(1+sqrt(1-c^2)) with c = (1-a)/(1+a)."""
    return 2.0 * (1.0 + alpha) / (1.0 + np.sqrt(alpha)) ** 2.0


def adaptive_omega(alpha, eps, n, slope=0.06, shift=1.5):
    """eps-adaptive SOR relaxation -- the 'adp-sor' rule.

    `opt_omega` is optimal for the GLOBAL graph, but at loose eps the push only
    touches a small, better-conditioned LOCAL subgraph whose optimal omega is
    smaller.  So lower omega below the global optimum by `slope` per decade that
    the gate is looser than ~10^-shift/n, clamped to [1, opt_omega] -- never
    worse than plain Gauss-Seidel, never past the global optimum.

    Depends on eps only through mult = n*eps (graph-size independent).  The
    (slope, shift) = (0.06, 1.5) fit is from com-dblp, alpha=0.05 (see the
    reference README, section Omega); other alpha may want a refit.
    """
    w_opt = opt_omega(alpha)
    w = w_opt - slope * max(0.0, np.log10(n * eps) + shift)
    return min(w_opt, max(1.0, w))


def single_local_sdd_solver(para):
    # para = [alpha, eps, source, graph, algo]
    alpha, eps, source, graph, algo = para
    dataset = graph.name
    n = graph.n
    indptr, indices, degree = graph.indptr, graph.indices, graph.degree
    b = np.zeros(n, dtype=np.float64)
    b[source] = 2.0 * alpha / ((1.0 + alpha) * np.sqrt(degree[source]))
    opt_x = sdd_get_opt(n, indptr, indices, degree, source, alpha, 1e-10)
    # Every local solver returns the same 6-tuple:
    #   (xt, rt, errs, opers, run_time, op_time)
    # algo: gd | appr | sor | opt-sor | adp-sor | hb | cheby
    if algo == "gd":
        result_local = sdd_local_gd(n, indptr, indices, degree, b, alpha, eps, opt_x)
    elif algo == "appr":
        s = np.zeros_like(b)
        s[source] = 1.0
        result_local = sdd_local_appr(n, indptr, indices, degree, s, alpha, eps, opt_x)
    elif algo == "sor":
        omega = 1.0
        result_local = sdd_local_sor(n, indptr, indices, degree, b, alpha, eps, omega, opt_x)
    elif algo == "opt-sor":
        result_local = sdd_local_sor(
            n, indptr, indices, degree, b, alpha, eps, opt_omega(alpha), opt_x
        )
    elif algo == "adp-sor":
        result_local = sdd_local_sor(
            n, indptr, indices, degree, b, alpha, eps, adaptive_omega(alpha, eps, n), opt_x
        )
    elif algo == "hb":
        result_local = sdd_local_heavy_ball(n, indptr, indices, degree, b, alpha, eps, opt_x)
    elif algo == "cheby":
        result_local = sdd_local_cheby(n, indptr, indices, degree, b, alpha, eps, opt_x)
    else:
        # argparse `choices` already blocks this from the CLI; this guards the
        # function when it is called directly.  Raising beats exit(-1) so the
        # failure is catchable and `result_local` can never be unbound below.
        raise ValueError(f"unknown algorithm: {algo!r}")
    errs, opers, run_time = result_local[2], result_local[3], result_local[4]
    # errs is ||xt/sqrt(d) - opt_x||_1 recorded per iteration, so errs[-1] is
    # the l1 error of the returned estimate against the (tight) reference.
    l1_err = errs[-1] if len(errs) else float("nan")
    print(
        "Algorithm: {} on dataset: {}, run-time: {} opers: {} l1-error: {:.6e}".format(
            algo, dataset, run_time, np.sum(opers), l1_err
        )
    )
    return alpha, eps, source, algo, dataset, result_local


def main(args):
    # Imported lazily so the solvers above keep depending on numpy + numba
    # only -- graph loading pulls scipy and is needed only on this CLI path.
    from ..graphs import load_graph

    graph = load_graph(args.dataset, data_dir=args.data_dir)
    eps = parse_eps(args.eps, graph.n)
    res = single_local_sdd_solver([args.alpha, eps, args.source_id, graph, args.algo])
    errs, opers = res[-1][2], np.sum(res[-1][3])
    l1_err = errs[-1] if len(errs) else float("nan")
    print(
        f"source={args.source_id} alpha={args.alpha} eps={eps:.4e} "
        f"operations={opers:,.0f} l1-error={l1_err:.6e}"
    )
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local SDD Solver")
    parser.add_argument(
        "--data-dir",
        type=str,
        required=True,
        help="local graph root created by the explicit data-acquisition command",
    )
    parser.add_argument(
        "--algo",
        type=str,
        default="appr",
        choices=["gd", "appr", "sor", "opt-sor", "adp-sor", "hb", "cheby"],
        required=False,
        help="local solver to run",
    )
    parser.add_argument(
        "--dataset", type=str, default="com-dblp", required=False, help="Dataset name"
    )
    parser.add_argument("--alpha", type=float, default=0.1, required=False, help="Alpha value")
    # str, not float: '1./n' and '.1/n' need n, which is only known after the
    # graph is loaded.  Resolved by parse_eps().
    parser.add_argument(
        "--eps",
        type=str,
        default="1./n",
        required=False,
        help="Eps value: a number ('1e-6') or '<x>/n' ('1./n', '.1/n')",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=17,
        required=False,
        help="Seed for random (reserved: source selection is currently fixed via --source_id)",
    )
    parser.add_argument(
        "--source_id", type=int, default=0, required=False, help="The source node id"
    )
    main(parser.parse_args())
