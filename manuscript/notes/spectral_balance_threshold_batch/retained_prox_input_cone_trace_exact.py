#!/usr/bin/env python3
"""Exact supplied-graph trace of the stopped masked-input-residual chronology.

This is an unregistered companion audit, not a graph-uniform proof.  It runs
the canonical point-source retained-prox loop from the zero lower state in
random-walk degree coordinates.  Every arithmetic operation and every branch
used by the algorithm is evaluated with :class:`fractions.Fraction`.

The script supports two explicitly named product orders.  Both begin with the
input-residual frontier, one gradient product, and uniform safe lowerization.
The ``input-frontier-only`` order then admits one positive exterior batch at
zero state without any residual push, exactly matching
``run_retained_prox(..., input_residual_append=True)`` with its other update
flags left at their defaults.  The ``one-push-maximal`` order instead makes
one active diagonal push and a maximal append-and-push closure:

1. append every exterior row with positive residual at the NAG input;
2. check the active masked input residual and execute one gradient product;
3. apply the uniform safe lowerization and clamp the momentum state;
4. make one simultaneous positive-residual diagonal push on the active face;
5. run the maximal exact-positive exterior diagonal-push closure; and
6. test the fixed-beta width stopping condition (default `beta=1/4`).

The JSON trace records each exact admission and stopping decision.  If the
input cone fails, the script stops before executing that product and emits the
full exact state.  ``rho_scale`` means ``d_source * rho`` and must lie in
``(0,1)``.  A rational retained root ``s`` fixes
``alpha = s^2 / (2-s^2)``.

There is deliberately no finite-precision publication tolerance here.  Every
input-frontier, active-push, and append-closure branch uses the exact strict
test ``residual > 0``; equivalently, the publication floor is exactly zero,
and a zero residual is not admitted or pushed.
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction as F
from pathlib import Path


def fraction(value: str) -> F:
    """Parse a rational CLI value and reject non-rational spellings."""
    try:
        return F(value)
    except (ValueError, ZeroDivisionError) as error:
        raise argparse.ArgumentTypeError(f"expected a rational number, got {value!r}") from error


def load_json_argument(value: str) -> object:
    """Load JSON from a path, or directly from an inline JSON argument."""
    stripped = value.lstrip()
    if stripped.startswith(("[", "{")):
        return json.loads(value)
    return json.loads(Path(value).read_text(encoding="utf-8"))


def build_graph(payload: object, source_override: int | None) -> tuple[list[set[int]], int]:
    """Validate a finite simple connected unit-edge graph JSON payload."""
    if isinstance(payload, list):
        edges_payload = payload
        vertex_count_payload: object | None = None
        source_payload: object = 0
    elif isinstance(payload, dict):
        if "edges" not in payload:
            raise ValueError("graph object must contain an 'edges' list")
        edges_payload = payload["edges"]
        vertex_count_payload = payload.get(
            "vertices",
            payload.get("vertex_count", payload.get("n")),
        )
        source_payload = payload.get("source", 0)
    else:
        raise ValueError("graph JSON must be an edge list or an object containing 'edges'")

    if not isinstance(edges_payload, list) or not edges_payload:
        raise ValueError("edge list must be a nonempty JSON list")
    edges: list[tuple[int, int]] = []
    largest_vertex = -1
    for edge in edges_payload:
        if (
            not isinstance(edge, list | tuple)
            or len(edge) != 2
            or isinstance(edge[0], bool)
            or isinstance(edge[1], bool)
            or not isinstance(edge[0], int)
            or not isinstance(edge[1], int)
        ):
            raise ValueError(f"edge must be a pair of integer vertex ids, got {edge!r}")
        left, right = edge
        if left < 0 or right < 0:
            raise ValueError(f"vertex ids must be nonnegative, got {edge!r}")
        if left == right:
            raise ValueError(f"self-loops are not allowed, got {edge!r}")
        edges.append((min(left, right), max(left, right)))
        largest_vertex = max(largest_vertex, left, right)
    if len(set(edges)) != len(edges):
        raise ValueError("parallel or duplicate edges are not allowed")

    if vertex_count_payload is None:
        vertex_count = largest_vertex + 1
    else:
        if isinstance(vertex_count_payload, bool) or not isinstance(vertex_count_payload, int):
            raise ValueError("'vertices'/'vertex_count'/'n' must be an integer")
        vertex_count = vertex_count_payload
    if vertex_count < 2:
        raise ValueError("graph must have at least two vertices")
    if largest_vertex >= vertex_count:
        raise ValueError("an edge endpoint is outside the declared vertex range")

    neighbors = [set() for _ in range(vertex_count)]
    for left, right in edges:
        neighbors[left].add(right)
        neighbors[right].add(left)
    if not all(neighbors):
        raise ValueError("connected nontrivial graphs cannot contain an isolated vertex")
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in neighbors[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    if len(seen) != vertex_count:
        raise ValueError("graph must be connected")

    source_value = source_payload if source_override is None else source_override
    if isinstance(source_value, bool) or not isinstance(source_value, int):
        raise ValueError("source must be an integer vertex id")
    if not 0 <= source_value < vertex_count:
        raise ValueError("source is outside the graph")
    return neighbors, source_value


def extremum(values: list[F], indices: list[int], *, minimum: bool) -> tuple[int, F] | None:
    """Return the deterministic first minimizer or maximizer on ``indices``."""
    if not indices:
        return None
    best = indices[0]
    for vertex in indices[1:]:
        if (values[vertex] < values[best]) if minimum else (values[vertex] > values[best]):
            best = vertex
    return best, values[best]


def sign_partition(values: list[F], indices: list[int]) -> dict[str, object]:
    """Record an exact ``> 0`` classification using its two boundary witnesses."""
    positive = [vertex for vertex in indices if values[vertex] > 0]
    nonpositive = [vertex for vertex in indices if values[vertex] <= 0]
    return {
        "considered": indices,
        "positive": positive,
        "minimum_positive": extremum(values, positive, minimum=True),
        "maximum_nonpositive": extremum(values, nonpositive, minimum=False),
    }


def serialize(value: object) -> object:
    """Convert exact values recursively to JSON-safe canonical strings."""
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(key): serialize(item) for key, item in value.items()}
    if isinstance(value, tuple | list):
        return [serialize(item) for item in value]
    return value


def trace_retained_prox(
    neighbors: list[set[int]],
    source: int,
    root: F,
    rho_scale: F,
    relative_width: F,
    maximum_phase_products: int,
    maximum_phases: int,
    chronology: str,
    stop_beta: F = F(1, 4),
) -> dict[str, object]:
    """Run the exact canonical zero-start chronology on one supplied graph."""
    if not 0 < root <= 1:
        raise ValueError("root must lie in (0,1]")
    if not 0 < rho_scale < 1:
        raise ValueError("rho_scale=d_source*rho must lie in (0,1)")
    if not 0 < relative_width < 1:
        raise ValueError("relative_width must lie in (0,1)")
    if maximum_phase_products < 1 or maximum_phases < 1:
        raise ValueError("product and phase limits must be positive")
    if not 0 < stop_beta < F(1, 2):
        raise ValueError("stop_beta must lie in (0,1/2)")
    if chronology not in {"input-frontier-only", "one-push-maximal"}:
        raise ValueError(f"unknown chronology {chronology!r}")

    vertex_count = len(neighbors)
    degrees = [len(row) for row in neighbors]
    source_degree = degrees[source]
    alpha = root * root / (2 - root * root)
    sigma = alpha
    original_diagonal = (1 + alpha) / 2
    shifted_diagonal = (1 + 3 * alpha) / 2
    coupling = (1 - alpha) / 2
    lipschitz = 1 + alpha
    shifted_gap = 2 * alpha
    momentum = (1 - root) / (1 + root)
    auxiliary_scale = (1 - root) / root
    rho = rho_scale / source_degree
    zero = F(0)

    def apply_shifted(state: list[F], vertex: int) -> F:
        return shifted_diagonal * state[vertex] - coupling / degrees[vertex] * sum(
            (state[neighbor] for neighbor in neighbors[vertex]),
            zero,
        )

    def residual(load: list[F], state: list[F]) -> list[F]:
        return [load[vertex] - apply_shifted(state, vertex) for vertex in range(vertex_count)]

    original_load = [-alpha * rho for _ in range(vertex_count)]
    original_load[source] += alpha / source_degree
    lower = [zero for _ in range(vertex_count)]
    certified = {source}
    initial_width = F(1, source_degree) - rho
    width = initial_width
    target_width = relative_width * initial_width
    phases: list[dict[str, object]] = []
    total_products = 0
    total_input_admissions = 0
    total_post_admission_batches = 0
    global_minimum: dict[str, object] | None = None
    # The only beta-dependent branches are the post-product stopping tests.
    # A stopped product imposes ratio <= beta, while a continued product
    # imposes beta < ratio.  These exact bounds therefore describe the whole
    # interval of beta values which replay the identical chronology prefix.
    chronology_beta_lower = zero
    chronology_beta_upper = F(1, 2)

    def chronology_beta_cell() -> dict[str, object]:
        return {
            "lower": chronology_beta_lower,
            "lower_inclusive": True,
            "upper": chronology_beta_upper,
            "upper_inclusive": False,
        }

    metadata: dict[str, object] = {
        "warning": "finite Fraction-exact supplied-graph audit, not a theorem",
        "coordinate_system": "random-walk degree coordinates",
        "chronology": chronology,
        "chronology_definition": (
            "input frontier; gradient; uniform lowerization/clamp; one exterior "
            "positive-residual admission batch at zero state; fixed-beta stop; no "
            "active or append residual push"
            if chronology == "input-frontier-only"
            else "input frontier; gradient; uniform lowerization/clamp; one active "
            "positive-residual diagonal push; maximal exterior append-and-push "
            "closure; fixed-beta stop"
        ),
        "publication_rule": {
            "floor": zero,
            "comparison": "exact strict residual > 0",
            "tie_behavior": "zero residual is neither admitted nor pushed",
        },
        "vertices": vertex_count,
        "edges": [
            [left, right]
            for left in range(vertex_count)
            for right in sorted(neighbors[left])
            if left < right
        ],
        "degrees": degrees,
        "source": source,
        "root": root,
        "alpha": alpha,
        "rho_scale": rho_scale,
        "rho": rho,
        "relative_width": relative_width,
        "stop_beta": stop_beta,
        "initial_width": initial_width,
        "target_width": target_width,
        "constants": {
            "sigma": sigma,
            "original_diagonal": original_diagonal,
            "shifted_diagonal": shifted_diagonal,
            "coupling": coupling,
            "lipschitz": lipschitz,
            "shifted_gap": shifted_gap,
            "momentum": momentum,
            "auxiliary_scale": auxiliary_scale,
        },
        "limits": {
            "maximum_phase_products": maximum_phase_products,
            "maximum_phases": maximum_phases,
        },
    }

    while width > target_width:
        if len(phases) >= maximum_phases:
            return {
                **metadata,
                "status": "phase_limit",
                "phases": phases,
                "completed_phases": len(phases),
                "total_products": total_products,
                "total_input_admission_batches": total_input_admissions,
                "total_post_admission_batches": total_post_admission_batches,
                "current_width": width,
                "certified_face": sorted(certified),
                "minimum_active_input_residual": global_minimum,
                "same_chronology_stop_beta_interval": chronology_beta_cell(),
            }

        phase_number = len(phases) + 1
        phase_start_certified = sorted(certified)
        old_lower = lower[:]
        old_width = width
        shifted_load = [
            original_load[vertex] + sigma * old_lower[vertex] for vertex in range(vertex_count)
        ]
        current = old_lower[:]
        previous = old_lower[:]
        auxiliary = old_lower[:]
        product_records: list[dict[str, object]] = []
        phase_stopped = False
        preceding_inner_width: F | None = None
        preceding_stop_margin: F | None = None

        for product_number in range(1, maximum_phase_products + 1):
            # This is exactly the NAG input represented by current/previous.
            input_extrapolate = [zero for _ in range(vertex_count)]
            for vertex in certified:
                input_extrapolate[vertex] = current[vertex] + momentum * (
                    current[vertex] - previous[vertex]
                )
            full_input_residual = residual(shifted_load, input_extrapolate)
            outside = sorted(set(range(vertex_count)) - certified)
            input_frontier = sign_partition(full_input_residual, outside)
            input_batch = list(input_frontier["positive"])
            if input_batch:
                certified.update(input_batch)
                total_input_admissions += 1
            face = sorted(certified)

            # Because all new rows enter at zero state, the same full residual
            # is the masked residual on the enlarged face.
            input_minimum = extremum(full_input_residual, face, minimum=True)
            assert input_minimum is not None
            input_vertex, input_value = input_minimum
            minimum_record = {
                "phase": phase_number,
                "product": product_number,
                "vertex": input_vertex,
                "value": input_value,
            }
            if global_minimum is None or input_value < global_minimum["value"]:
                global_minimum = minimum_record

            record: dict[str, object] = {
                "product": product_number,
                "face_before_input_frontier": sorted(set(face) - set(input_batch)),
                "input_frontier": input_frontier,
                "face_for_product": face,
                "minimum_active_input_residual": (input_vertex, input_value),
            }
            if input_value < 0:
                record["executed"] = False
                product_records.append(record)
                failure = {
                    "phase": phase_number,
                    "product": product_number,
                    "vertex": input_vertex,
                    "value": input_value,
                    "face": face,
                    "input_batch": input_batch,
                    "phase_old_width": old_width,
                    "preceding_inner_width": preceding_inner_width,
                    "preceding_inner_width_over_old_width": (
                        None if preceding_inner_width is None else preceding_inner_width / old_width
                    ),
                    "preceding_stop_margin": preceding_stop_margin,
                    "stop_width_threshold": stop_beta * old_width,
                    # Retained for consumers of the original quarter-only trace.
                    "quarter_width_threshold": old_width / 4,
                    "phase_start_lower": old_lower,
                    "lower": lower,
                    "current": current,
                    "previous": previous,
                    "auxiliary": auxiliary,
                    "input_extrapolate": input_extrapolate,
                    "shifted_load": shifted_load,
                    "active_input_residuals": [
                        [vertex, full_input_residual[vertex]] for vertex in face
                    ],
                }
                phases.append(
                    {
                        "phase": phase_number,
                        "old_width": old_width,
                        "start_face": phase_start_certified,
                        "products": product_records,
                        "stopped": False,
                    }
                )
                return {
                    **metadata,
                    "status": "counterexample",
                    "phases": phases,
                    "completed_phases": phase_number - 1,
                    "total_products": total_products,
                    "total_input_admission_batches": total_input_admissions,
                    "total_post_admission_batches": total_post_admission_batches,
                    "current_width": width,
                    "certified_face": sorted(certified),
                    "minimum_active_input_residual": global_minimum,
                    "same_chronology_stop_beta_interval": chronology_beta_cell(),
                    "first_negative_active_input_residual": failure,
                }

            record["executed"] = True
            following = [zero for _ in range(vertex_count)]
            for vertex in face:
                following[vertex] = (
                    input_extrapolate[vertex] + full_input_residual[vertex] / lipschitz
                )
            previous, current = current, following

            # Uniform degree-coordinate shave.  Its direction is B_AA 1.
            shifts = [zero]
            for vertex in face:
                row_residual = shifted_load[vertex] - apply_shifted(current, vertex)
                direction = (
                    shifted_diagonal
                    - coupling * len(neighbors[vertex] & certified) / degrees[vertex]
                )
                assert direction > 0
                shifts.append(-row_residual / direction)
            shift = max(shifts)
            # Under the checked input cone, (I-B/L) maps the nonnegative
            # input residual to a nonnegative raw-current residual.  Retain
            # this exact equality as a chronology sanity check.
            assert shift == 0
            for vertex in face:
                lower[vertex] = max(lower[vertex], current[vertex] - shift, zero)

            next_auxiliary = [zero for _ in range(vertex_count)]
            if auxiliary_scale:
                for vertex in face:
                    next_auxiliary[vertex] = current[vertex] + auxiliary_scale * (
                        current[vertex] - previous[vertex]
                    )
                    current[vertex] = max(current[vertex], lower[vertex])
                    next_auxiliary[vertex] = max(next_auxiliary[vertex], lower[vertex])
                    previous[vertex] = (
                        current[vertex]
                        - (next_auxiliary[vertex] - current[vertex]) / auxiliary_scale
                    )
            else:
                for vertex in face:
                    current[vertex] = max(current[vertex], lower[vertex])
                    previous[vertex] = current[vertex]
                    next_auxiliary[vertex] = current[vertex]
            auxiliary = next_auxiliary

            # The source-clock search leaves all push flags off.  The separate
            # one-push conjecture performs the simultaneous active push here.
            pre_push_residual = residual(shifted_load, lower)
            assert all(pre_push_residual[vertex] >= 0 for vertex in face)
            active_push_decision = sign_partition(pre_push_residual, face)
            active_push = (
                list(active_push_decision["positive"]) if chronology == "one-push-maximal" else []
            )
            increments = [zero for _ in range(vertex_count)]
            for vertex in active_push:
                increments[vertex] = pre_push_residual[vertex] / shifted_diagonal
            for vertex in active_push:
                lower[vertex] += increments[vertex]
            full_residual = residual(shifted_load, lower)
            if auxiliary_scale:
                for vertex in face:
                    current[vertex] = max(current[vertex], lower[vertex])
                    auxiliary[vertex] = max(auxiliary[vertex], lower[vertex])
                    previous[vertex] = (
                        current[vertex] - (auxiliary[vertex] - current[vertex]) / auxiliary_scale
                    )
            else:
                for vertex in face:
                    current[vertex] = max(current[vertex], lower[vertex])
                    auxiliary[vertex] = current[vertex]
                    previous[vertex] = current[vertex]

            # The frontier-only chronology executes one exterior admission
            # decision and leaves every new row at exact zero state.  The
            # one-push chronology pushes each admitted batch and repeats to
            # maximal closure.
            closure_records: list[dict[str, object]] = []
            while True:
                outside = sorted(set(range(vertex_count)) - certified)
                closure_decision = sign_partition(full_residual, outside)
                batch = list(closure_decision["positive"])
                closure_records.append(
                    {
                        **closure_decision,
                        "admitted": batch,
                        "pushed": chronology == "one-push-maximal" and bool(batch),
                    }
                )
                if not batch:
                    break
                total_post_admission_batches += 1
                if chronology == "input-frontier-only":
                    certified.update(batch)
                    break
                batch_increment = [zero for _ in range(vertex_count)]
                for vertex in batch:
                    batch_increment[vertex] = full_residual[vertex] / shifted_diagonal
                for vertex in batch:
                    lower[vertex] += batch_increment[vertex]
                    current[vertex] = lower[vertex]
                    auxiliary[vertex] = lower[vertex]
                    previous[vertex] = lower[vertex]
                certified.update(batch)
                full_residual = residual(shifted_load, lower)

            assert all(full_residual[vertex] >= 0 for vertex in certified)
            assert all(
                full_residual[vertex] <= 0 for vertex in set(range(vertex_count)) - certified
            )

            total_products += 1
            positive_residual_vertices = [
                vertex for vertex in range(vertex_count) if full_residual[vertex] > 0
            ]
            maximum_positive = extremum(
                full_residual,
                positive_residual_vertices,
                minimum=False,
            )
            if maximum_positive is None:
                maximum_vertex: int | None = None
                maximum_residual = zero
            else:
                maximum_vertex, maximum_residual = maximum_positive
            inner_width = maximum_residual / shifted_gap
            residual_threshold = shifted_gap * old_width * stop_beta
            stop_margin = residual_threshold - maximum_residual
            stop = stop_margin >= 0
            stop_ratio = inner_width / old_width
            if stop:
                chronology_beta_lower = max(chronology_beta_lower, stop_ratio)
            else:
                chronology_beta_upper = min(chronology_beta_upper, stop_ratio)
            assert chronology_beta_lower <= stop_beta < chronology_beta_upper
            record.update(
                {
                    "uniform_shift": shift,
                    "active_push": {
                        **active_push_decision,
                        "enabled": chronology == "one-push-maximal",
                        "pushed": active_push,
                    },
                    "post_product_admissions": closure_records,
                    "face_after_closure": sorted(certified),
                    "stop": {
                        "decision": stop,
                        "maximum_positive_residual_vertex": maximum_vertex,
                        "maximum_positive_residual": maximum_residual,
                        "residual_threshold": residual_threshold,
                        "margin": stop_margin,
                        "inner_width": inner_width,
                        "inner_width_over_old_width": inner_width / old_width,
                    },
                }
            )
            product_records.append(record)
            if stop:
                width = old_width / 2 + inner_width
                phase_stopped = True
                phases.append(
                    {
                        "phase": phase_number,
                        "old_width": old_width,
                        "new_width": width,
                        "start_face": phase_start_certified,
                        "end_face": sorted(certified),
                        "product_count": product_number,
                        "products": product_records,
                        "stopped": True,
                    }
                )
                break
            preceding_inner_width = inner_width
            preceding_stop_margin = stop_margin

        if not phase_stopped:
            phases.append(
                {
                    "phase": phase_number,
                    "old_width": old_width,
                    "start_face": phase_start_certified,
                    "end_face": sorted(certified),
                    "product_count": maximum_phase_products,
                    "products": product_records,
                    "stopped": False,
                }
            )
            return {
                **metadata,
                "status": "product_limit",
                "phases": phases,
                "completed_phases": phase_number - 1,
                "total_products": total_products,
                "total_input_admission_batches": total_input_admissions,
                "total_post_admission_batches": total_post_admission_batches,
                "current_width": width,
                "certified_face": sorted(certified),
                "minimum_active_input_residual": global_minimum,
                "same_chronology_stop_beta_interval": chronology_beta_cell(),
            }

    return {
        **metadata,
        "status": "pass",
        "phases": phases,
        "completed_phases": len(phases),
        "total_products": total_products,
        "total_input_admission_batches": total_input_admissions,
        "total_post_admission_batches": total_post_admission_batches,
        "final_width": width,
        "certified_face": sorted(certified),
        "minimum_active_input_residual": global_minimum,
        "same_chronology_stop_beta_interval": chronology_beta_cell(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fraction-exact canonical zero-start input-cone trace",
        epilog=(
            "Publication uses exact residual > 0 throughout: the publication "
            "floor is exactly zero, and equality is not admitted or pushed."
        ),
    )
    parser.add_argument(
        "--graph-json",
        required=True,
        help="path to, or inline, edge-list JSON; object form may specify vertices/source",
    )
    parser.add_argument("--source", type=int, help="override a source stored in graph JSON")
    parser.add_argument("--root", type=fraction, required=True, help="rational retained root s")
    parser.add_argument(
        "--rho-scale",
        type=fraction,
        required=True,
        help="rational d_source*rho in (0,1)",
    )
    parser.add_argument("--relative-width", type=fraction, default=F(1, 32))
    parser.add_argument(
        "--stop-beta",
        type=fraction,
        default=F(1, 4),
        help="inner-width stopping fraction beta in (0,1/2); default 1/4",
    )
    parser.add_argument("--maximum-phase-products", type=int, default=2000)
    parser.add_argument("--maximum-phases", type=int, default=200)
    parser.add_argument(
        "--chronology",
        choices=("input-frontier-only", "one-push-maximal"),
        required=True,
        help=(
            "input-frontier-only matches default run_retained_prox flags plus "
            "input_residual_append; one-push-maximal is the pushed chronology"
        ),
    )
    parser.add_argument(
        "--print-failure-summary",
        action="store_true",
        help=(
            "on a negative active input residual, print its exact value and the "
            "preceding inner_width/old_width ratio to stderr"
        ),
    )
    parser.add_argument(
        "--output",
        help="optional output JSON path; stdout is used when omitted",
    )
    args = parser.parse_args()

    # Exact long traces can legitimately produce integers with many thousands
    # of decimal digits.  Python 3.11's safety cap is inappropriate for this
    # trusted arithmetic output.
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)

    try:
        neighbors, source = build_graph(load_json_argument(args.graph_json), args.source)
        result = trace_retained_prox(
            neighbors,
            source,
            args.root,
            args.rho_scale,
            args.relative_width,
            args.maximum_phase_products,
            args.maximum_phases,
            args.chronology,
            args.stop_beta,
        )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.error(str(error))
    output = json.dumps(serialize(result), indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    if result["status"] == "counterexample":
        if args.print_failure_summary:
            witness = result["first_negative_active_input_residual"]
            print(
                json.dumps(
                    serialize(
                        {
                            "status": "counterexample",
                            "phase": witness["phase"],
                            "product": witness["product"],
                            "vertex": witness["vertex"],
                            "active_input_residual": witness["value"],
                            "phase_old_width": witness["phase_old_width"],
                            "preceding_inner_width": witness["preceding_inner_width"],
                            "preceding_inner_width_over_old_width": witness[
                                "preceding_inner_width_over_old_width"
                            ],
                            "stop_beta": args.stop_beta,
                            "stop_width_threshold": witness["stop_width_threshold"],
                        }
                    ),
                    sort_keys=True,
                ),
                file=sys.stderr,
            )
        raise SystemExit(1)
    if result["status"] != "pass":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
