#!/usr/bin/env python3
"""Exact audits for variable two-port STOPs and a restricted cactus GO.

The cactus ledger below is deliberately a representation-level audit: it
certifies the cost of literal ancestor rescans, not an algorithmic lower
bound.  The transfer test certifies only the fixed, fully active cycle
named-response primitive used by the bounded-live-site cactus result.
"""

from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "manuscript/notes/aesp_cd_l1_rppr/sections/body/06_lem_aesp_cd_kkt_error.tex"


def solve(matrix, rhs):
    """Solve a nonsingular rational system by exact Gauss--Jordan elimination."""
    n = len(rhs)
    if not n:
        return []
    augmented = [list(matrix[i]) + [rhs[i]] for i in range(n)]
    for column in range(n):
        pivot_row = next(i for i in range(column, n) if augmented[i][column])
        augmented[column], augmented[pivot_row] = (
            augmented[pivot_row],
            augmented[column],
        )
        pivot = augmented[column][column]
        augmented[column] = [value / pivot for value in augmented[column]]
        for row in range(n):
            if row == column or not augmented[row][column]:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                value - factor * base
                for value, base in zip(augmented[row], augmented[column])
            ]
    return [row[-1] for row in augmented]


def exact_rppr_direction_stop():
    """Check the literal unweighted theta-core formulas and opposite labels."""
    # Three internally disjoint u1--u2 paths:
    # u1-s-b-u2, u1-a-t-u2, and u1-q-u2.
    u1, s, b_node, u2, a, t, q = range(7)
    edges = [
        (u1, s),
        (s, b_node),
        (b_node, u2),
        (u1, a),
        (a, t),
        (t, u2),
        (u1, q),
        (q, u2),
    ]
    adjacency = [[] for _ in range(7)]
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    degree = [len(row) for row in adjacency]
    assert degree == [3, 2, 2, 3, 2, 2, 2]

    alpha, diagonal_scale, coupling, rho = F(1, 2), F(3, 4), F(1, 4), F(1, 37)
    matrix = [[F(0) for _ in range(7)] for _ in range(7)]
    for i in range(7):
        matrix[i][i] = diagonal_scale * degree[i]
        for j in adjacency[i]:
            matrix[i][j] = -coupling
    load = [-alpha * rho * degree[i] for i in range(7)]

    # Exact elimination without pivoting has positive pivots, independently
    # checking the SPD claim for this concrete Stieltjes matrix.
    factor = [row[:] for row in matrix]
    for k in range(7):
        assert factor[k][k] > 0
        for i in range(k + 1, 7):
            if not factor[i][k]:
                continue
            multiplier = factor[i][k] / factor[k][k]
            for j in range(k + 1, 7):
                factor[i][j] -= multiplier * factor[k][j]

    def conditioned_state(s_value, t_value):
        ports = {s: s_value, t: t_value}
        active_internal = [a, b_node]
        rhs = [
            load[i] - sum(matrix[i][j] * ports[j] for j in ports)
            for i in active_internal
        ]
        values = solve(
            [[matrix[i][j] for j in active_internal] for i in active_internal],
            rhs,
        )
        state = {s: s_value, t: t_value, a: values[0], b_node: values[1]}
        keys = {
            vertex: load[vertex]
            - sum(matrix[vertex][j] * state.get(j, F(0)) for j in range(7))
            for vertex in (u1, u2, q)
        }
        return state, keys

    equal, equal_keys = conditioned_state(5 * rho, 5 * rho)
    forward, forward_keys = conditioned_state(6 * rho, 5 * rho)
    reverse, reverse_keys = conditioned_state(5 * rho, 6 * rho)
    assert equal[a] == equal[b_node] == rho / 6
    assert forward[a] == rho / 6 and forward[b_node] == rho / 3
    assert reverse[a] == rho / 3 and reverse[b_node] == rho / 6
    assert equal_keys == {u1: -5 * rho / 24, u2: -5 * rho / 24, q: -rho}
    assert forward_keys == {u1: rho / 24, u2: -rho / 6, q: -rho}
    assert reverse_keys == {u1: -rho / 6, u2: rho / 24, q: -rho}

    normal_1 = (F(1, 4), F(1, 24))
    normal_2 = (F(1, 24), F(1, 4))
    determinant = normal_1[0] * normal_2[1] - normal_1[1] * normal_2[0]
    assert determinant == F(35, 576)
    # The port sums agree, while the strict positive label is reversed.
    assert 6 * rho + 5 * rho == 5 * rho + 6 * rho
    return determinant


def weighted_direction_stop():
    """Check a grounded weighted diamond with two independent port normals."""
    # Each row is one internal vertex coupled to the two ports.  Unit ground
    # makes the internal diagonal 1+left+right and the full matrix strictly
    # diagonally dominant after giving each port an additional unit ground.
    edge_weights = ((F(1), F(2)), (F(2), F(1)))
    directions = []
    for left, right in edge_weights:
        diagonal = 1 + left + right
        directions.append((left / diagonal, right / diagonal))
    determinant = (
        directions[0][0] * directions[1][1]
        - directions[0][1] * directions[1][0]
    )
    assert directions == [(F(1, 4), F(1, 2)), (F(1, 2), F(1, 4))]
    assert determinant == -F(3, 16)
    return determinant


def cycle_chain(block_count, length):
    """Build a cactus chain whose blocks are cycles of the given length."""
    adjacency = [[] for _ in range(block_count + 1)]
    blocks = []
    owner = {0: 0}
    for block in range(1, block_count + 1):
        left, right = block - 1, block
        edges = [(left, right)]
        previous = left
        for _ in range(length - 2):
            adjacency.append([])
            vertex = len(adjacency) - 1
            owner[vertex] = block
            edges.append((previous, vertex))
            previous = vertex
        edges.append((previous, right))
        owner[right] = block
        for u, v in edges:
            adjacency[u].append(v)
            adjacency[v].append(u)
        blocks.append(edges)
    return adjacency, blocks, owner, list(range(block_count + 1))


def rppr_system(adjacency, alpha, rho):
    n = len(adjacency)
    diagonal_scale = (1 + alpha) / 2
    coupling = (1 - alpha) / 2
    degree = [len(row) for row in adjacency]
    matrix = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        matrix[i][i] = diagonal_scale * degree[i]
        for j in adjacency[i]:
            matrix[i][j] = -coupling
    load = [
        alpha * ((1 if i == 0 else 0) - rho * degree[i]) for i in range(n)
    ]
    return degree, diagonal_scale, coupling, matrix, load


def restricted_solution(matrix, load, active):
    indices = sorted(active)
    values = solve(
        [[matrix[i][j] for j in indices] for i in indices],
        [load[i] for i in indices],
    )
    return dict(zip(indices, values))


def singleton_trace(adjacency, matrix, load, owner, length):
    active = {0}
    naive_rescan_work = 0
    admissions = []
    for _ in range(len(adjacency) + 1):
        value = restricted_solution(matrix, load, active)
        assert all(coordinate > 0 for coordinate in value.values())
        state = [value.get(i, F(0)) for i in range(len(adjacency))]
        frontier = sorted(
            {v for u in active for v in adjacency[u] if v not in active}
        )
        keys = {
            v: load[v]
            - sum(matrix[v][j] * state[j] for j in range(len(adjacency)))
            for v in frontier
        }
        positive = [v for v in frontier if keys[v] > 0]
        if not positive:
            break
        vertex = min(positive, key=lambda candidate: (owner[candidate], candidate))
        assert keys[vertex] > 0
        active.add(vertex)
        admissions.append((vertex, owner[vertex], keys[vertex]))
        # Literal rescan: every ancestor cycle has `length` sites.
        naive_rescan_work += length * owner[vertex]
    else:
        raise AssertionError("singleton trace did not terminate")
    return active, admissions, naive_rescan_work


def schur(matrix, load, ports):
    ports = list(ports)
    port_set = set(ports)
    interior = [i for i in range(len(matrix)) if i not in port_set]
    if not interior:
        return (
            [[matrix[i][j] for j in ports] for i in ports],
            [load[i] for i in ports],
        )
    interior_matrix = [[matrix[i][j] for j in interior] for i in interior]
    inverse_load = solve(interior_matrix, [load[i] for i in interior])
    inverse_columns = [
        solve(interior_matrix, [matrix[i][j] for i in interior]) for j in ports
    ]
    summary = [
        [
            matrix[i][j]
            - sum(
                matrix[i][u] * inverse_columns[column][row]
                for row, u in enumerate(interior)
            )
            for column, j in enumerate(ports)
        ]
        for i in ports
    ]
    summary_load = [
        load[i]
        - sum(
            matrix[i][u] * inverse_load[row]
            for row, u in enumerate(interior)
        )
        for i in ports
    ]
    return summary, summary_load


def assert_block_schur_assembly(
    blocks,
    ports,
    alpha,
    rho,
    diagonal_scale,
    coupling,
    global_summary,
    global_load,
):
    """Assemble fixed two-port block summaries and compare to one global Schur."""
    size = len(ports)
    assembled = [[F(0) for _ in range(size)] for _ in range(size)]
    assembled_load = [F(0) for _ in range(size)]
    port_index = {vertex: i for i, vertex in enumerate(ports)}
    for block, edges in enumerate(blocks, 1):
        vertices = sorted({vertex for edge in edges for vertex in edge})
        local_index = {vertex: i for i, vertex in enumerate(vertices)}
        count = len(vertices)
        local_matrix = [[F(0) for _ in range(count)] for _ in range(count)]
        local_load = [F(0) for _ in range(count)]
        for u, v in edges:
            iu, iv = local_index[u], local_index[v]
            local_matrix[iu][iu] += diagonal_scale
            local_matrix[iv][iv] += diagonal_scale
            local_matrix[iu][iv] -= coupling
            local_matrix[iv][iu] -= coupling
            local_load[iu] -= alpha * rho
            local_load[iv] -= alpha * rho
        left, right = block - 1, block
        keep = [local_index[left], local_index[right]]
        summary, summary_load = schur(local_matrix, local_load, keep)
        global_indices = (port_index[left], port_index[right])
        for i, global_i in enumerate(global_indices):
            assembled_load[global_i] += summary_load[i]
            for j, global_j in enumerate(global_indices):
                assembled[global_i][global_j] += summary[i][j]
    assembled_load[0] += alpha
    assert assembled == global_summary
    assert assembled_load == global_load


def graph_radius(adjacency):
    distance = [None] * len(adjacency)
    distance[0] = 0
    queue = [0]
    for u in queue:
        for v in adjacency[u]:
            if distance[v] is None:
                distance[v] = distance[u] + 1
                queue.append(v)
    return max(distance)


def cactus_case(block_count, length):
    adjacency, blocks, owner, ports = cycle_chain(block_count, length)
    alpha = F(1, 5)
    rho = F(1, 10 ** (3 * (block_count + length)))
    degree, diagonal_scale, coupling, matrix, load = rppr_system(
        adjacency, alpha, rho
    )
    active, admissions, naive_work = singleton_trace(
        adjacency, matrix, load, owner, length
    )
    assert active == set(range(len(adjacency)))
    expected = length * (length - 1) * block_count * (block_count + 1) // 2
    assert naive_work == expected
    volume = sum(degree)
    assert volume == 2 * block_count * length
    radius = graph_radius(adjacency)
    assert radius <= block_count + length
    global_summary, global_load = schur(matrix, load, ports)
    assert_block_schur_assembly(
        blocks,
        ports,
        alpha,
        rho,
        diagonal_scale,
        coupling,
        global_summary,
        global_load,
    )
    ratio = F(naive_work, (radius + 1) * volume)
    return len(adjacency), len(admissions), volume, radius, naive_work, ratio


def matrix_multiply(left, right):
    return [
        [sum(left[i][k] * right[k][j] for k in range(3)) for j in range(3)]
        for i in range(3)
    ]


def balanced_transfer_product(matrices):
    """Return M_last ... M_first with balanced parenthesization."""
    if len(matrices) == 1:
        return matrices[0]
    middle = len(matrices) // 2
    left = balanced_transfer_product(matrices[:middle])
    right = balanced_transfer_product(matrices[middle:])
    return matrix_multiply(right, left)


def cycle_transfer(diagonal, coupling, load, parent_value):
    """Solve a cycle cut at site zero using its fixed 3x3 transfers."""
    count = len(diagonal)
    product = [[F(i == j) for j in range(3)] for i in range(3)]
    matrices = []
    for i in range(1, count - 1):
        transfer = [
            [
                diagonal[i] / coupling[i],
                -coupling[i - 1] / coupling[i],
                -load[i] / coupling[i],
            ],
            [F(1), F(0), F(0)],
            [F(0), F(0), F(1)],
        ]
        matrices.append(transfer)
        product = matrix_multiply(transfer, product)
    assert product == balanced_transfer_product(matrices)

    final_diagonal = diagonal[-1]
    preceding_coupling = coupling[-2]
    wrap_coupling = coupling[-1]
    coefficient_x1 = (
        final_diagonal * product[0][0]
        - preceding_coupling * product[1][0]
    )
    coefficient_parent = (
        final_diagonal * product[0][1]
        - preceding_coupling * product[1][1]
        - wrap_coupling
    )
    constant = (
        final_diagonal * product[0][2]
        - preceding_coupling * product[1][2]
        - load[-1]
    )
    assert coefficient_x1
    x1 = -(coefficient_parent * parent_value + constant) / coefficient_x1
    value = [parent_value, x1]
    for i in range(1, count - 1):
        value.append(
            (
                diagonal[i] * value[i]
                - coupling[i - 1] * value[i - 1]
                - load[i]
            )
            / coupling[i]
        )
    return value


def assert_cycle_named_response_go():
    """Compare transfer responses with exact dense solves after point updates."""
    count = 7
    coupling = [F(i + 2, 2 * i + 5) for i in range(count)]
    diagonal = [
        F(1) + coupling[i - 1] + coupling[i] for i in range(count)
    ]
    load = [F(i - 4, 13) for i in range(count)]
    updates = (None, (3, F(2, 7), F(5, 17)), (6, F(1, 4), -F(2, 9)))
    final_slopes = None
    for update in updates:
        updated_diagonal = diagonal[:]
        updated_load = load[:]
        if update:
            site, diagonal_change, load_change = update
            updated_diagonal[site] += diagonal_change
            updated_load[site] += load_change
        responses = []
        for parent_value in (F(0), F(1), F(3, 5)):
            response = cycle_transfer(
                updated_diagonal, coupling, updated_load, parent_value
            )
            interior = list(range(1, count))
            dense = solve(
                [
                    [
                        updated_diagonal[i]
                        if i == j
                        else (
                            -coupling[min(i, j)] if abs(i - j) == 1 else F(0)
                        )
                        for j in interior
                    ]
                    for i in interior
                ],
                [
                    updated_load[i]
                    + (coupling[0] * parent_value if i == 1 else 0)
                    + (coupling[-1] * parent_value if i == count - 1 else 0)
                    for i in interior
                ],
            )
            assert response[1:] == dense
            responses.append(response)
        # Exact affinity and strict inverse-positivity slopes on a full cycle.
        for coordinate in range(count):
            assert responses[2][coordinate] == (
                responses[0][coordinate]
                + F(3, 5) * (responses[1][coordinate] - responses[0][coordinate])
            )
        final_slopes = [
            responses[1][i] - responses[0][i] for i in range(1, count)
        ]
        assert all(slope > 0 for slope in final_slopes)
    return final_slopes


def main():
    source = SOURCE.read_text()
    assert r"\label{cor:aesp-cd-cactus-live-sites}" in source
    assert r"\label{prob:aesp-cd-variable-two-port-reporter}" in source
    assert r"\label{prop:aesp-cd-two-port-direction-stop}" in source

    rppr_determinant = exact_rppr_direction_stop()
    weighted_determinant = weighted_direction_stop()
    cactus_rows = [
        cactus_case(block_count, length)
        for block_count, length in ((2, 3), (3, 4), (4, 4), (5, 5), (6, 6))
    ]
    assert cactus_rows[-1][-1] > cactus_rows[0][-1]
    slopes = assert_cycle_named_response_go()

    print("PASS variable two-port exact audit:")
    print(
        "  directionality STOP determinants",
        rppr_determinant,
        weighted_determinant,
    )
    print("  cactus literal-rescan ledgers", cactus_rows)
    print("  fixed two-port Schur assembly and 3x3 named responses PASS")
    print("  final exact positive site slopes", slopes)
    print("  scope: representation STOP plus restricted named-response GO only")


if __name__ == "__main__":
    main()
