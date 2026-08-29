#!/usr/bin/env python3
"""Exact audits for variable two-port STOPs and a restricted cactus GO.

The cactus ledger below is deliberately a representation-level audit: it
certifies the cost of literal ancestor rescans, not an algorithmic lower
bound.  The transfer test certifies only the fixed, fully active cycle
named-response primitive used by the bounded-live-site cactus result.
"""

from fractions import Fraction as F
import math
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "manuscript/notes/aesp_cd_l1_rppr/sections/body/06b_prop_aesp_cd_dynamic_reporters.tex"
PRODUCTIVE_SOURCE = (
    ROOT
    / "manuscript/notes/aesp_cd_l1_rppr/sections/body/06c_prop_aesp_cd_productive_cactus.tex"
)
PROJECTIVE_GUARD_SOURCE = (
    ROOT
    / "manuscript/notes/aesp_cd_l1_rppr/sections/body/06e_cor_aesp_cd_projective_guard.tex"
)


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


def projective_pullback_order_audit():
    """Check the exact normalized two-port pullback and its order sign."""
    translation = (F(2, 7), -F(1, 5))
    matrices = (
        ((F(3), F(1)), (F(1), F(2))),
        ((F(1), F(3)), (F(2), F(1))),
        ((F(1), F(2)), (F(2), F(4))),
    )
    rows = []
    for matrix in matrices:
        p11, p12 = matrix[0]
        p21, p22 = matrix[1]
        determinant = p11 * p22 - p12 * p21
        images = []
        for slope in (F(1, 5), F(2, 3), F(7, 4)):
            intercept = F(3, 11) - slope / 13
            normal = (slope, F(1))
            offset = -intercept
            pulled_normal = (
                p11 * normal[0] + p21 * normal[1],
                p12 * normal[0] + p22 * normal[1],
            )
            pulled_offset = offset - sum(
                normal[i] * translation[i] for i in range(2)
            )
            denominator = p12 * slope + p22
            formula_slope = (p11 * slope + p21) / denominator
            formula_intercept = (
                intercept + slope * translation[0] + translation[1]
            ) / denominator
            assert pulled_normal[1] == denominator > 0
            assert pulled_normal[0] / pulled_normal[1] == formula_slope
            assert -pulled_offset / pulled_normal[1] == formula_intercept
            images.append(formula_slope)
        if determinant > 0:
            assert images == sorted(images)
        elif determinant < 0:
            assert images == sorted(images, reverse=True)
        else:
            assert len(set(images)) == 1
        rows.append((determinant, images))

    def multiply(left, right):
        return tuple(
            tuple(sum(left[i][k] * right[k][j] for k in range(3)) for j in range(3))
            for i in range(3)
        )

    def projective(matrix, shift):
        return (
            (matrix[0][0], F(0), matrix[1][0]),
            (shift[0], F(1), shift[1]),
            (matrix[0][1], F(0), matrix[1][1]),
        )

    p1, p2 = matrices[:2]
    u1, u2 = translation, (F(1, 3), F(2, 9))
    composite_p = tuple(
        tuple(sum(p1[i][k] * p2[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )
    composite_u = tuple(
        sum(p1[i][k] * u2[k] for k in range(2)) + u1[i] for i in range(2)
    )
    assert multiply(projective(p2, u2), projective(p1, u1)) == projective(
        composite_p, composite_u
    )

    interval = (F(1, 5), F(7, 4))
    for matrix, (determinant, images) in zip(matrices, rows, strict=True):
        p11, p12 = matrix[0]
        p21, p22 = matrix[1]
        endpoint_images = tuple(
            (p11 * slope + p21) / (p12 * slope + p22) for slope in interval
        )
        assert (min(images), max(images)) == (
            min(endpoint_images),
            max(endpoint_images),
        )
        if determinant == 0:
            assert endpoint_images[0] == endpoint_images[1]
    return rows


def alternating_meld_facets():
    """Exact alternating-facet STOP for an explicitly merged parent hull."""
    half = 9
    count = 2 * half
    translation = 16 * half * half

    def value(index, x, odd_shift):
        return F(index * x - index * index - (odd_shift if index % 2 else 0))

    winners = []
    shifted_winners = []
    for index in range(1, count + 1):
        x = 2 * index
        values = [value(row, x, 0) for row in range(1, count + 1)]
        assert values[index - 1] == max(values)
        assert values.count(max(values)) == 1
        winners.append(index)

        shifted = [
            value(row, x, translation) for row in range(1, count + 1)
        ]
        shifted_winner = 1 + shifted.index(max(shifted))
        assert shifted_winner % 2 == 0
        shifted_winners.append(shifted_winner)

    assert winners == list(range(1, count + 1))
    assert sum(index % 2 for index in winners) == half
    assert not any(index % 2 for index in shifted_winners)
    return half, winners, shifted_winners


def root_port_forget_stop():
    """Check that excluding both pinned root ports would miss a positive key."""
    matrix = [[F(2), -F(1)], [-F(1), F(2)]]
    load = [F(1), -F(1)]
    pinned_state = [F(0), F(0)]
    keys = [
        load[i] - sum(matrix[i][j] * pinned_state[j] for j in range(2))
        for i in range(2)
    ]
    # A handle containing only rows forgotten strictly below the root is empty
    # on this one-edge decomposition, but the first root-port key is positive.
    forgotten_handle = []
    assert not forgotten_handle
    assert keys == [F(1), -F(1)]
    assert max(keys) > 0
    return keys


def objective_gain_charge_stop():
    """Calibrate a strict K2 admission whose exact Schur gain tends to zero."""
    alpha = F(1, 5)
    diagonal = (1 + alpha) / 2
    coupling = (1 - alpha) / 2
    gains = []
    for epsilon in (F(1, 10), F(1, 100), F(1, 1000)):
        rho = coupling - epsilon
        root_value = alpha * (1 - rho) / diagonal
        key = -alpha * rho + coupling * root_value
        pivot = diagonal - coupling * coupling / diagonal
        gain = key * key / (2 * pivot)
        assert key == alpha * epsilon / diagonal > 0
        assert pivot == alpha / diagonal > 0
        assert gain == alpha * epsilon * epsilon / (2 * diagonal)
        assert gain >= key * key / 2  # Here lambda_max(H)=1.
        gains.append(gain)
    assert gains[0] > gains[1] > gains[2] > 0
    assert gains[1] * 100 == gains[0]
    assert gains[2] * 100 == gains[1]
    return gains


def static_cluster_and_prefix_merge_ledgers():
    """Audit the flat sqrt ledger and online immutable-prefix merge charge."""
    flat_rows = []
    for root in range(2, 33):
        length = root * root
        touched = root
        repeated = length // touched
        phase_work = min(length, touched * repeated)
        phase_events = touched + repeated
        assert phase_work == length
        assert phase_events == 2 * root
        assert 2 * phase_work == root * phase_events
        flat_rows.append((length, phase_events, phase_work))

    # Binary-counter merging of consecutive immutable factors.  A singleton
    # build costs one; merging two equal adjacent chunks costs their total size.
    stack = []
    total_work = 0
    power_rows = []
    for factor_count in range(1, 257):
        chunk = 1
        total_work += 1
        while stack and stack[-1] == chunk:
            stack.pop()
            chunk *= 2
            total_work += chunk
        stack.append(chunk)
        assert sum(stack) == factor_count
        assert len(stack) == factor_count.bit_count()
        assert total_work <= factor_count * (1 + factor_count.bit_length())
        if factor_count & (factor_count - 1) == 0:
            level = factor_count.bit_length() - 1
            assert total_work == factor_count * (1 + level)
            assert stack == [factor_count]
            power_rows.append((factor_count, total_work))

    # A heavy superblock with b structural blocks and maximum cycle length L
    # has S=O(bL); b and L/2 are separately radius-paid.
    for block_count in range(1, 65):
        for longest_cycle in range(1, 65):
            structural_size = block_count * longest_cycle
            radius_lower = max(block_count, longest_cycle // 2)
            assert structural_size <= 4 * (1 + radius_lower) ** 2
    return flat_rows[-1], power_rows[-1]


def balanced_sp_epoch_ledgers():
    """Audit canonical clean covers and sqrt-cap rebuild accounting."""

    def cover_size(size, dirty):
        def visit(left, right):
            has_dirty = any(left <= leaf < right for leaf in dirty)
            if not has_dirty or right - left == 1:
                return 1
            middle = (left + right) // 2
            return visit(left, middle) + visit(middle, right)

        return visit(0, size)

    size = 64
    height = int(math.log2(size))
    cap = math.isqrt(size)
    assert cap * cap == size
    sequences = (
        [5] * 100,
        [0] * 19 + list(range(1, 33)) + [7] * 11,
        [(17 * step + 3) % size for step in range(96)],
    )
    rows = []
    for sequence in sequences:
        dirty = set()
        rebuilds = 0
        query_work = 0
        maximum_cover = 0
        for leaf in sequence:
            dirty.add(leaf)
            if len(dirty) == cap:
                rebuilds += 1
                dirty.clear()
            cover = cover_size(size, dirty)
            maximum_cover = max(maximum_cover, cover)
            assert cover <= 1 + max(1, len(dirty)) * height
            query_work += cover
        actual = size * (1 + rebuilds) + query_work
        declared = size + len(sequence) * cap + (len(sequence) // cap) * size
        productive = size + len(sequence) * min(len(set(sequence)) + 1, cap)
        assert rebuilds <= len(sequence) // cap
        assert actual <= 2 * declared
        assert actual <= height * productive
        rows.append(
            (
                len(sequence),
                len(set(sequence)),
                rebuilds,
                maximum_cover,
                actual,
                productive,
            )
        )
    return rows


def hysteretic_heavy_path_ledgers():
    """Stress the online 2-hysteretic HLD and its atom--node rebuild charge."""

    def one_case(parent, atom_weight):
        count = len(parent)
        children = [[] for _ in range(count)]
        depth = [0] * count
        for vertex in range(1, count):
            children[parent[vertex]].append(vertex)
            depth[vertex] = depth[parent[vertex]] + 1
        radius = max(depth)
        active = [False] * count
        subtree_weight = [0] * count
        heavy = [None] * count
        chosen_weights = [[] for _ in range(count)]
        switch_count = [0] * count
        conservative_rebuild = 0
        largest_light_count = 0

        def is_ancestor(ancestor, vertex):
            while depth[vertex] > depth[ancestor]:
                vertex = parent[vertex]
            return ancestor == vertex

        for inserted in range(count):
            active[inserted] = True
            route = []
            cursor = inserted
            while cursor != -1:
                route.append(cursor)
                subtree_weight[cursor] += atom_weight[inserted]
                cursor = parent[cursor]

            # Descendant weights change before ancestor decisions are tested.
            for node in route:
                live_children = [child for child in children[node] if active[child]]
                if not live_children:
                    continue
                competitor = max(
                    live_children,
                    key=lambda child: (subtree_weight[child], -child),
                )
                old_heavy = heavy[node]
                if old_heavy is None:
                    heavy[node] = competitor
                    chosen_weights[node].append(subtree_weight[competitor])
                elif (
                    competitor != old_heavy
                    and subtree_weight[competitor] > 2 * subtree_weight[old_heavy]
                ):
                    assert subtree_weight[competitor] > 2 * chosen_weights[node][-1]
                    heavy[node] = competitor
                    chosen_weights[node].append(subtree_weight[competitor])
                    switch_count[node] += 1
                    comparable = [
                        atom
                        for atom in range(count)
                        if active[atom]
                        and (is_ancestor(atom, node) or is_ancestor(node, atom))
                    ]
                    conservative_rebuild += sum(atom_weight[atom] for atom in comparable)

            current_weight = subtree_weight[0]
            light_count = sum(
                child != heavy[parent[child]] for child in route[:-1]
            )
            largest_light_count = max(largest_light_count, light_count)
            assert light_count <= 1 + math.ceil(math.log(current_weight, 1.5))
            for child in range(1, inserted + 1):
                if child != heavy[parent[child]]:
                    assert 3 * subtree_weight[child] <= 2 * subtree_weight[parent[child]]

        total_weight = sum(atom_weight)
        switch_cap = 1 + total_weight.bit_length()
        assert all(count_at_node <= switch_cap for count_at_node in switch_count)
        assert conservative_rebuild <= (
            total_weight * (2 * radius + 1) * switch_cap
        )
        return (
            count,
            total_weight,
            radius,
            sum(switch_count),
            largest_light_count,
            conservative_rebuild,
        )

    cases = []
    # A long spine with alternating side growth stresses ancestor updates.
    parent = [-1]
    for vertex in range(1, 96):
        parent.append(max(0, vertex - 2) if vertex % 3 else 0)
    cases.append(one_case(parent, [1 + (vertex % 5) for vertex in range(len(parent))]))

    # Random topological leaf streams cover repeated heavy-child reversals.
    generator = random.Random(20260829)
    for count in (32, 64, 128, 192):
        parent = [-1] + [generator.randrange(vertex) for vertex in range(1, count)]
        weights = [generator.randrange(1, 8) for _ in range(count)]
        cases.append(one_case(parent, weights))
    assert any(row[3] > 0 for row in cases)
    return cases


def productive_site_numeric_key_pressure():
    """Show why dormant runs store homogeneous rows, not numerical keys."""
    # Cut a four-cycle at parent site zero and set its value to one.  Sites
    # 1,2,3 form the interior path.  Attach a child y at site 1 with diagonal
    # 2, coupling -1, and load -1/4.  Its positive key makes the admission
    # legal.  Eliminating y contributes s=1/2 and r=-1/8 at site 1, changing
    # the numerical key at still-dormant site 2 without touching its local
    # aggregate response.
    old_matrix = [
        [F(3), -F(1), F(0)],
        [-F(1), F(3), -F(1)],
        [F(0), -F(1), F(3)],
    ]
    touched_matrix = [
        [F(5, 2), -F(1), F(0)],
        [-F(1), F(3), -F(1)],
        [F(0), -F(1), F(3)],
    ]
    old_value = solve(old_matrix, [F(1), F(0), F(1)])
    child_key = -F(1, 4) + old_value[0]
    touched_value = solve(touched_matrix, [F(7, 8), F(0), F(1)])
    threshold = F(7, 24)
    old_key = old_value[1] - threshold
    touched_key = touched_value[1] - threshold
    assert old_value == [F(3, 7), F(2, 7), F(3, 7)]
    assert child_key == F(5, 28) > 0
    assert touched_value == [F(8, 17), F(41, 136), F(59, 136)]
    assert old_key == -F(1, 168) < 0
    assert touched_key == F(1, 102) > 0
    return child_key, old_key, touched_key


def productive_epoch_integer_ledgers():
    """Check repeated-site and maximal-reset productive epoch charges."""

    def ledger(event_sites, cap):
        touched = set()
        scans = 0
        resets = 0
        for site in event_sites:
            touched.add(site)
            scans += len(touched) + 1
            if len(touched) == cap:
                resets += 1
                touched.clear()
        assert scans <= len(event_sites) * (cap + 1)
        assert resets <= len(event_sites) // cap
        return scans, resets

    event_count, cap = 100, 10
    # Fill an epoch to k-1 distinct sites, then mutate one of them repeatedly:
    # there is no rebuild, but every scan is paid by the J*k term.
    repeated = list(range(cap - 1)) + [0] * (event_count - cap + 1)
    # Touch k distinct sites in every epoch, attaining the reset upper bound.
    reset_heavy = [event % cap for event in range(event_count)]
    repeated_result = ledger(repeated, cap)
    reset_result = ledger(reset_heavy, cap)
    assert repeated_result == (964, 0)
    assert repeated_result[0] <= event_count * (len(set(repeated)) + 1)
    assert reset_result == (650, 10)
    return repeated_result, reset_result


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


def connected_order_small_rho_certificate():
    """Replay an exact core--side--terminal connected order on three triangles."""
    block_count = length = 3
    terminal_count = 9
    adjacency, blocks, owner, _ports = cycle_chain(block_count, length)
    core_count = len(adjacency)
    sites = [sorted({vertex for edge in block for vertex in edge}) for block in blocks]
    branch_site = {}
    side_order = []
    # q=ceil(sqrt(3))-1=1: one side leaf at each exit articulation.
    for block in range(1, block_count + 1):
        exit_site = block
        adjacency.append([exit_site])
        leaf = len(adjacency) - 1
        adjacency[exit_site].append(leaf)
        owner[leaf] = block
        branch_site[leaf] = (block, exit_site)
        side_order.append(leaf)
    terminal_order = []
    for _ in range(terminal_count):
        adjacency.append([block_count])
        leaf = len(adjacency) - 1
        adjacency[block_count].append(leaf)
        owner[leaf] = block_count
        branch_site[leaf] = (block_count, block_count)
        terminal_order.append(leaf)
    order = list(range(1, core_count)) + side_order + terminal_order

    alpha, rho = F(1, 5), F(1, 10**75)
    degree, _p, _c, matrix, load = rppr_system(adjacency, alpha, rho)
    active = {0}
    closed = [False] * (block_count + 1)
    touched = [set() for _ in range(block_count + 1)]
    visits = [0] * (block_count + 1)
    phase_minimum = {"core": None, "side": None, "terminal": None}

    for position, vertex in enumerate(order):
        assert any(neighbor in active for neighbor in adjacency[vertex])
        value = restricted_solution(matrix, load, active)
        assert all(coordinate > 0 for coordinate in value.values())
        state = [value.get(i, F(0)) for i in range(len(adjacency))]
        key = load[vertex] - sum(
            matrix[vertex][j] * state[j] for j in range(len(adjacency))
        )
        assert key > 0
        if position < core_count - 1:
            phase = "core"
        elif position < core_count - 1 + block_count:
            phase = "side"
        else:
            phase = "terminal"
        old_minimum = phase_minimum[phase]
        phase_minimum[phase] = key if old_minimum is None else min(old_minimum, key)

        event_owner = owner[vertex]
        for block in range(1, event_owner + 1):
            if not closed[block]:
                continue
            visits[block] += 1
            if block == event_owner and vertex in branch_site:
                touched[block].add(branch_site[vertex][1])
            elif block < event_owner:
                touched[block].add(block)
        active.add(vertex)
        for block in range(1, block_count + 1):
            if not closed[block] and set(sites[block - 1]) <= active:
                closed[block] = True

    assert active == set(range(len(adjacency)))
    assert F(12, 10_000) < phase_minimum["core"] < F(13, 10_000)
    assert F(31, 100_000) < phase_minimum["side"] < F(32, 100_000)
    assert F(33, 100_000) < phase_minimum["terminal"] < F(34, 100_000)
    productive_counts = tuple(
        len(touched[block]) for block in range(1, block_count + 1)
    )
    visit_counts = tuple(visits[block] for block in range(1, block_count + 1))
    assert productive_counts == (1, 1, 1)
    assert visit_counts == (14, 12, 10)
    assert graph_radius(adjacency) * sum(degree) == 168
    return (
        {phase: float(value) for phase, value in phase_minimum.items()},
        productive_counts,
        visit_counts,
    )


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
    productive_source = PRODUCTIVE_SOURCE.read_text()
    projective_guard_source = PROJECTIVE_GUARD_SOURCE.read_text()
    assert r"\label{cor:aesp-cd-cactus-live-sites}" in source
    assert r"\label{prob:aesp-cd-variable-two-port-reporter}" in source
    assert r"\label{prop:aesp-cd-two-port-direction-stop}" in source
    assert r"\label{lem:aesp-cd-two-port-projective-pullback}" in source
    assert r"\label{cor:aesp-cd-slope-separated-projective-meld}" in source
    assert r"\label{prop:aesp-cd-sp-static-epoch-reporter}" in source
    assert r"\label{prop:aesp-cd-sp-alternating-meld-stop}" in source
    assert r"\label{cor:aesp-cd-projective-separation-guard}" in projective_guard_source
    assert "virtual top forget" in source
    assert r"\label{cor:aesp-cd-cactus-productive-sites}" in productive_source
    assert r"\label{cor:aesp-cd-cactus-productive-epochs}" in productive_source
    assert r"\label{lem:aesp-cd-connected-order-small-rho}" in productive_source
    assert r"\label{prop:aesp-cd-objective-gain-charge-stop}" in productive_source
    assert r"\label{cor:aesp-cd-schur-gain-batch-payment}" in productive_source
    assert r"\label{prop:aesp-cd-cactus-static-cluster-stop}" in productive_source
    assert r"\label{prop:aesp-cd-cactus-offline-hld}" in productive_source
    assert r"\label{thm:aesp-cd-cactus-online-hysteretic-hld}" in productive_source
    assert "binary-counter stack" in productive_source
    assert "not their pulled-back" in productive_source

    rppr_determinant = exact_rppr_direction_stop()
    weighted_determinant = weighted_direction_stop()
    projective_rows = projective_pullback_order_audit()
    alternating_facets = alternating_meld_facets()
    root_keys = root_port_forget_stop()
    objective_gains = objective_gain_charge_stop()
    interface_ledgers = static_cluster_and_prefix_merge_ledgers()
    sp_epoch_ledgers = balanced_sp_epoch_ledgers()
    hysteretic_ledgers = hysteretic_heavy_path_ledgers()
    productive_keys = productive_site_numeric_key_pressure()
    epoch_ledgers = productive_epoch_integer_ledgers()
    connected_order = connected_order_small_rho_certificate()
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
    print("  projective pullback determinants / slope images", projective_rows)
    print("  alternating merged-hull facets", alternating_facets)
    print("  cactus literal-rescan ledgers", cactus_rows)
    print("  fixed two-port Schur assembly and 3x3 named responses PASS")
    print("  virtual top forget catches pinned root-port keys", root_keys)
    print("  K2 strict-admission objective gains", objective_gains)
    print("  flat sqrt / immutable-prefix ledgers", interface_ledgers)
    print("  balanced SP static-epoch ledgers", sp_epoch_ledgers)
    print("  online hysteretic HLD ledgers", hysteretic_ledgers)
    print("  legal productive-site numerical-key pressure", productive_keys)
    print("  productive epoch integer ledgers", epoch_ledgers)
    print("  connected-order small-rho phase minima / p / J", connected_order)
    print("  final exact positive site slopes", slopes)
    print("  scope: representation STOP plus restricted named-response GO only")


if __name__ == "__main__":
    main()
