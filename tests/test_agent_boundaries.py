from dataclasses import replace

from tools.agent_boundaries import (
    REPOSITORY_ROOT,
    Scope,
    changed_path_errors,
    load_assignments,
    load_owned_scopes,
    repository_errors,
)


def test_repository_coordination_records_are_valid():
    assert repository_errors(REPOSITORY_ROOT) == []


def test_current_family_can_change_owned_and_permitted_shared_paths():
    assignments, _ = load_assignments(REPOSITORY_ROOT)
    owned_scopes, _ = load_owned_scopes(REPOSITORY_ROOT)

    errors = changed_path_errors(
        ["experiments/providers/codex/explore_evolving_cg.py", "README.md"],
        branch="agent/codex/coordination-and-offline-data",
        assignments=assignments,
        owned_scopes=owned_scopes,
    )

    assert errors == []


def test_foreign_owned_path_is_rejected():
    assignments, _ = load_assignments(REPOSITORY_ROOT)
    owned_scopes, _ = load_owned_scopes(REPOSITORY_ROOT)
    assignment = assignments[0]
    expanded = replace(
        assignment,
        write_scope=(*assignment.write_scope, Scope("src/hybrid_solver_claude", True)),
    )

    errors = changed_path_errors(
        ["src/hybrid_solver_claude/__init__.py"],
        branch=expanded.branch,
        assignments=[expanded],
        owned_scopes=owned_scopes,
    )

    assert errors == [
        "src/hybrid_solver_claude/__init__.py is owned by claude, not branch family codex"
    ]


def test_unlisted_shared_path_is_rejected():
    assignments, _ = load_assignments(REPOSITORY_ROOT)
    owned_scopes, _ = load_owned_scopes(REPOSITORY_ROOT)
    assignment = assignments[0]
    expanded = replace(
        assignment,
        write_scope=(*assignment.write_scope, Scope("unlisted.txt", False)),
    )

    errors = changed_path_errors(
        ["unlisted.txt"],
        branch=expanded.branch,
        assignments=[expanded],
        owned_scopes=owned_scopes,
    )

    assert errors == ["shared changed path is not explicitly permitted: unlisted.txt"]


def test_unassigned_branch_is_rejected():
    assignments, _ = load_assignments(REPOSITORY_ROOT)
    owned_scopes, _ = load_owned_scopes(REPOSITORY_ROOT)

    errors = changed_path_errors(
        ["README.md"],
        branch="feature/unassigned",
        assignments=assignments,
        owned_scopes=owned_scopes,
    )

    assert errors == ["branch must match agent/<family>/<task>: 'feature/unassigned'"]
