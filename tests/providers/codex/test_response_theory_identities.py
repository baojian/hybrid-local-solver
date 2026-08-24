import numpy as np

from src.hybrid_solver_codex.evolving_cg import pagerank_matrix, pagerank_rhs
from src.hybrid_solver_codex.response_hybrid import DenseNestedResponse
from src.synthetic_graphs import graph_from_edges


def _schur_complement(
    matrix: np.ndarray,
    eliminated: list[int],
) -> tuple[np.ndarray, np.ndarray]:
    eliminated_array = np.asarray(eliminated, dtype=int)
    survivor_array = np.asarray(
        [vertex for vertex in range(matrix.shape[0]) if vertex not in eliminated],
        dtype=int,
    )
    if eliminated_array.size == 0:
        return survivor_array, matrix.copy()
    eliminated_block = matrix[np.ix_(eliminated_array, eliminated_array)]
    survivor_to_eliminated = matrix[np.ix_(survivor_array, eliminated_array)]
    schur = matrix[np.ix_(survivor_array, survivor_array)] - (
        survivor_to_eliminated @ np.linalg.solve(eliminated_block, survivor_to_eliminated.T)
    )
    return survivor_array, 0.5 * (schur + schur.T)


def _position(vertices: np.ndarray, vertex: int) -> int:
    matches = np.flatnonzero(vertices == vertex)
    assert matches.size == 1
    return int(matches[0])


def _irregular_graph():
    return graph_from_edges(
        "irregular-grounded-test",
        7,
        [
            (0, 1),
            (0, 2),
            (1, 2),
            (1, 3),
            (2, 4),
            (3, 4),
            (3, 5),
            (4, 5),
            (4, 6),
            (5, 6),
        ],
    )


def test_pagerank_operator_is_a_grounded_laplacian_under_diagonal_scaling():
    graph = _irregular_graph()
    alpha = 0.13
    matrix = pagerank_matrix(graph, alpha).toarray()
    degree_matrix = np.diag(graph.degree)
    square_root_degree = np.sqrt(graph.degree)
    grounded = square_root_degree[:, None] * matrix * square_root_degree[None, :]
    expected = (1.0 - alpha) / 2.0 * (
        degree_matrix - graph.adjacency.toarray()
    ) + alpha * degree_matrix
    np.testing.assert_allclose(grounded, expected, rtol=1.0e-13, atol=1.0e-14)

    eliminated = [0, 1, 3]
    survivors, matrix_schur = _schur_complement(matrix, eliminated)
    grounded_survivors, grounded_schur = _schur_complement(grounded, eliminated)
    np.testing.assert_array_equal(grounded_survivors, survivors)
    inverse_square_root = 1.0 / np.sqrt(graph.degree[survivors])
    np.testing.assert_allclose(
        matrix_schur,
        inverse_square_root[:, None] * grounded_schur * inverse_square_root[None, :],
        rtol=1.0e-12,
        atol=1.0e-13,
    )

    rng = np.random.default_rng(19)
    normalized_correction = np.zeros(graph.n)
    normalized_correction[eliminated] = rng.normal(size=len(eliminated))
    symmetric_correction = square_root_degree * normalized_correction
    np.testing.assert_allclose(
        (matrix @ symmetric_correction) / square_root_degree,
        (grounded @ normalized_correction) / graph.degree,
        rtol=1.0e-13,
        atol=1.0e-14,
    )


def test_source_leverage_is_exactly_terminal_schur_diagonal_loss():
    graph = _irregular_graph()
    alpha = 0.09
    matrix = pagerank_matrix(graph, alpha).toarray()
    old_face = [0, 1]
    batch = [2, 3]
    enlarged_face = old_face + batch

    inverse_enlarged = np.linalg.inv(matrix[np.ix_(enlarged_face, enlarged_face)])
    batch_embedding = np.zeros((len(enlarged_face), len(batch)))
    batch_embedding[len(old_face) :, :] = np.eye(len(batch))
    source_green = batch_embedding.T @ inverse_enlarged @ batch_embedding

    old_survivors, old_schur = _schur_complement(matrix, old_face)
    new_survivors, new_schur = _schur_complement(matrix, enlarged_face)
    for vertex in [4, 5, 6]:
        response_row = matrix[vertex, enlarged_face] @ inverse_enlarged @ batch_embedding
        conditional_leverage = float(response_row @ np.linalg.solve(source_green, response_row.T))

        old_vertex = _position(old_survivors, vertex)
        old_batch = [_position(old_survivors, batch_vertex) for batch_vertex in batch]
        old_batch_block = old_schur[np.ix_(old_batch, old_batch)]
        old_cross = old_schur[old_vertex, old_batch]
        schur_update = float(old_cross @ np.linalg.solve(old_batch_block, old_cross.T))
        new_vertex = _position(new_survivors, vertex)
        diagonal_loss = float(old_schur[old_vertex, old_vertex] - new_schur[new_vertex, new_vertex])

        np.testing.assert_allclose(conditional_leverage, schur_update, rtol=1.0e-11)
        np.testing.assert_allclose(conditional_leverage, diagonal_loss, rtol=1.0e-11)


def test_response_objects_ignore_degree_preserving_exterior_rewiring():
    exposed_edges = [(0, 1), (0, 2), (1, 3)]
    first_graph = graph_from_edges(
        "exterior-complete-bipartite",
        6,
        exposed_edges + [(2, 4), (2, 5), (3, 4), (3, 5)],
    )
    second_graph = graph_from_edges(
        "exterior-cycle",
        6,
        exposed_edges + [(2, 3), (3, 4), (4, 5), (5, 2)],
    )
    np.testing.assert_array_equal(first_graph.degree, second_graph.degree)

    alpha = 0.11
    first_matrix = pagerank_matrix(first_graph, alpha).toarray()
    second_matrix = pagerank_matrix(second_graph, alpha).toarray()
    face = [0, 1]
    boundary = [2, 3]
    batch_embedding = np.array([[0.0], [1.0]])

    def normalized_response(matrix: np.ndarray) -> np.ndarray:
        inverse_face = np.linalg.inv(matrix[np.ix_(face, face)])
        source_green = batch_embedding.T @ inverse_face @ batch_embedding
        return (
            np.diag(1.0 / np.sqrt(first_graph.degree[boundary]))
            @ matrix[np.ix_(boundary, face)]
            @ inverse_face
            @ batch_embedding
            / np.sqrt(source_green.item())
        )

    np.testing.assert_allclose(
        normalized_response(first_matrix),
        normalized_response(second_matrix),
        rtol=1.0e-13,
        atol=1.0e-14,
    )

    old_face = [0]
    first_old_survivors, first_old_schur = _schur_complement(first_matrix, old_face)
    first_new_survivors, first_new_schur = _schur_complement(first_matrix, face)
    second_old_survivors, second_old_schur = _schur_complement(second_matrix, old_face)
    second_new_survivors, second_new_schur = _schur_complement(second_matrix, face)
    for vertex in boundary:
        first_loss = (
            first_old_schur[
                _position(first_old_survivors, vertex), _position(first_old_survivors, vertex)
            ]
            - first_new_schur[
                _position(first_new_survivors, vertex), _position(first_new_survivors, vertex)
            ]
        )
        second_loss = (
            second_old_schur[
                _position(second_old_survivors, vertex), _position(second_old_survivors, vertex)
            ]
            - second_new_schur[
                _position(second_new_survivors, vertex), _position(second_new_survivors, vertex)
            ]
        )
        np.testing.assert_allclose(first_loss, second_loss, rtol=1.0e-13, atol=1.0e-14)

    assert not np.allclose(first_new_schur, second_new_schur)


def test_transposed_anchor_sketch_recovers_the_exterior_dual_signature():
    graph = _irregular_graph()
    alpha = 0.08
    matrix = pagerank_matrix(graph, alpha).toarray()
    anchor = np.array([0, 1])
    frontier = np.array([2, 3])
    outside_anchor = np.array([2, 3, 4, 5, 6])
    exterior = np.array([4, 5, 6])
    inverse_anchor = np.linalg.inv(matrix[np.ix_(anchor, anchor)])
    rng = np.random.default_rng(37)
    measurement = rng.normal(size=(4, outside_anchor.size))
    inverse_sqrt_degree = np.diag(1.0 / np.sqrt(graph.degree[outside_anchor]))
    harmonic_sketch = (
        inverse_anchor
        @ matrix[np.ix_(anchor, outside_anchor)]
        @ inverse_sqrt_degree
        @ measurement.T
    )

    frontier_vector = rng.normal(size=frontier.size)
    correction = np.zeros(graph.n)
    correction[frontier] = frontier_vector
    correction[anchor] = -(inverse_anchor @ matrix[np.ix_(anchor, frontier)] @ frontier_vector)
    dual_signature = matrix @ correction
    np.testing.assert_allclose(dual_signature[anchor], 0.0, atol=1.0e-13)
    np.testing.assert_allclose(
        measurement @ (dual_signature[outside_anchor] / np.sqrt(graph.degree[outside_anchor])),
        measurement
        @ (
            matrix[np.ix_(outside_anchor, frontier)]
            @ frontier_vector
            / np.sqrt(graph.degree[outside_anchor])
        )
        - harmonic_sketch.T @ (matrix[np.ix_(anchor, frontier)] @ frontier_vector),
        rtol=1.0e-12,
        atol=1.0e-13,
    )

    schur_frontier = matrix[np.ix_(frontier, frontier)] - (
        matrix[np.ix_(frontier, anchor)] @ inverse_anchor @ matrix[np.ix_(anchor, frontier)]
    )
    frontier_source = rng.normal(size=frontier.size)
    exact_frontier = np.linalg.solve(schur_frontier, frontier_source)
    exact_correction = np.zeros(graph.n)
    exact_correction[frontier] = exact_frontier
    exact_correction[anchor] = -(inverse_anchor @ matrix[np.ix_(anchor, frontier)] @ exact_frontier)
    exact_dual = matrix @ exact_correction
    np.testing.assert_allclose(exact_dual[frontier], frontier_source, rtol=1.0e-12)

    frontier_columns = np.array([_position(outside_anchor, vertex) for vertex in frontier])
    exterior_columns = np.array([_position(outside_anchor, vertex) for vertex in exterior])
    complete_measurement = measurement @ (
        exact_dual[outside_anchor] / np.sqrt(graph.degree[outside_anchor])
    )
    np.testing.assert_allclose(
        measurement[:, exterior_columns] @ (exact_dual[exterior] / np.sqrt(graph.degree[exterior])),
        complete_measurement
        - measurement[:, frontier_columns] @ (frontier_source / np.sqrt(graph.degree[frontier])),
        rtol=1.0e-12,
        atol=1.0e-13,
    )


def test_two_ledger_response_bound_and_diagonal_loss_telescope():
    graph = graph_from_edges(
        "wheel-fragment",
        7,
        [(0, leaf) for leaf in range(1, 7)] + [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)],
    )
    alpha = 0.07
    matrix = pagerank_matrix(graph, alpha).toarray()
    right_hand_side = np.array([0.0, 0.11, 0.08, 0.13, 0.07, 0.09, 0.05])
    response = DenseNestedResponse(matrix)
    initial_face = [1]
    batches = ([2, 3], [4], [5])
    exterior_vertex = 0

    response.expand(initial_face)
    previous_solution = response.solve_active(right_hand_side)
    initial_survivors, initial_schur = _schur_complement(matrix, initial_face)
    response_rows: list[np.ndarray] = []
    coefficients: list[np.ndarray] = []
    corrections: list[np.ndarray] = []

    for batch in batches:
        basis, _ = response.normalized_frontier_lift(batch)
        response.expand(batch)
        current_solution = response.solve_active(right_hand_side)
        correction = current_solution - previous_solution
        coefficient = basis.T @ matrix @ correction

        np.testing.assert_allclose(basis @ coefficient, correction, rtol=1.0e-11, atol=1.0e-12)
        response_rows.append((matrix[exterior_vertex, :] @ basis) / np.sqrt(graph.degree[0]))
        coefficients.append(coefficient)
        corrections.append(correction)
        previous_solution = current_solution

    leverage_by_epoch = np.asarray([row @ row for row in response_rows])
    energy_by_epoch = np.asarray([coefficient @ coefficient for coefficient in coefficients])
    response_by_epoch = np.asarray(
        [row @ coefficient for row, coefficient in zip(response_rows, coefficients, strict=True)]
    )
    np.testing.assert_array_less(
        np.abs(response_by_epoch),
        np.sqrt(leverage_by_epoch * energy_by_epoch) + 1.0e-13,
    )
    assert np.sum(np.sqrt(leverage_by_epoch * energy_by_epoch)) <= (
        np.sqrt(np.sum(leverage_by_epoch) * np.sum(energy_by_epoch)) + 1.0e-13
    )

    total_correction = np.sum(corrections, axis=0)
    np.testing.assert_allclose(
        total_correction @ matrix @ total_correction,
        np.sum(energy_by_epoch),
        rtol=1.0e-11,
        atol=1.0e-13,
    )

    final_face = initial_face + [vertex for batch in batches for vertex in batch]
    final_survivors, final_schur = _schur_complement(matrix, final_face)
    initial_position = _position(initial_survivors, exterior_vertex)
    final_position = _position(final_survivors, exterior_vertex)
    normalized_diagonal_loss = (
        initial_schur[initial_position, initial_position]
        - final_schur[final_position, final_position]
    ) / graph.degree[exterior_vertex]
    np.testing.assert_allclose(
        np.sum(leverage_by_epoch),
        normalized_diagonal_loss,
        rtol=1.0e-11,
        atol=1.0e-13,
    )

    unit_seed_rhs = pagerank_rhs(graph, alpha, source=1)
    unit_seed_solution = np.linalg.solve(matrix, unit_seed_rhs)
    assert unit_seed_solution @ matrix @ unit_seed_solution <= alpha + 1.0e-13
