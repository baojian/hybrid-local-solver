"""Validate active assignments and provider-owned path boundaries."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
COORDINATION_ROOT = Path("docs/coordination")
ASSIGNMENTS_FILE = COORDINATION_ROOT / "active_assignments.toml"
OWNERSHIP_FILE = COORDINATION_ROOT / "ownership.toml"
CONTEXT_FILE = COORDINATION_ROOT / "context.toml"
PROVIDERS_FILE = Path("src/solver_providers.toml")
BRANCH_PATTERN = re.compile(r"^agent/(?P<family>[a-z0-9][a-z0-9-]*)/(?P<task>[a-z0-9][a-z0-9-]*)$")
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
ASSIGNMENT_STATES = {"active", "ready_for_review"}
REQUIRED_CONTEXT_EXCLUDES = {
    ".agents/**",
    "papers/**",
    "manuscript/archive/**",
    "manuscript/notes/_shared/coordination/rounds/**",
    "src/hybrid_solver_codex/**",
    "src/hybrid_solver_claude/**",
    "experiments/providers/**",
    "tests/providers/**",
}


@dataclass(frozen=True, slots=True)
class Scope:
    path: str
    is_directory: bool

    def contains(self, candidate: str) -> bool:
        if self.is_directory:
            return candidate == self.path or candidate.startswith(f"{self.path}/")
        return candidate == self.path

    def overlaps(self, other: Scope) -> bool:
        return self.contains(other.path) or other.contains(self.path)


@dataclass(frozen=True, slots=True)
class Assignment:
    id: str
    agent_family: str
    branch: str
    base_commit: str
    role: str
    state: str
    write_scope: tuple[Scope, ...]
    permitted_shared_files: tuple[Scope, ...]


@dataclass(frozen=True, slots=True)
class OwnedScope:
    scope: Scope
    agent_family: str


def _load_toml(repository_root: Path, relative_path: Path) -> dict:
    with (repository_root / relative_path).open("rb") as source:
        return tomllib.load(source)


def _scope(value: object, *, field_name: str, errors: list[str]) -> Scope | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field_name} entries must be nonempty strings")
        return None
    if "\\" in value:
        errors.append(f"{field_name} must use forward slashes: {value!r}")
        return None

    is_directory = value.endswith("/")
    raw_path = value[:-1] if is_directory else value
    candidate = PurePosixPath(raw_path)
    if candidate.is_absolute() or raw_path in {"", "."} or ".." in candidate.parts:
        errors.append(f"{field_name} must be a repository-relative path: {value!r}")
        return None
    normalized = candidate.as_posix()
    if normalized != raw_path:
        errors.append(f"{field_name} must be normalized: {value!r}")
        return None
    return Scope(path=normalized, is_directory=is_directory)


def _string(record: dict, field_name: str, *, label: str, errors: list[str]) -> str:
    value = record.get(field_name)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}.{field_name} must be a nonempty string")
        return ""
    return value


def _scopes(record: dict, field_name: str, *, label: str, errors: list[str]) -> tuple[Scope, ...]:
    values = record.get(field_name)
    if not isinstance(values, list) or not values:
        errors.append(f"{label}.{field_name} must be a nonempty list")
        return ()
    parsed = [_scope(value, field_name=f"{label}.{field_name}", errors=errors) for value in values]
    return tuple(scope for scope in parsed if scope is not None)


def load_assignments(repository_root: Path) -> tuple[list[Assignment], list[str]]:
    errors: list[str] = []
    document = _load_toml(repository_root, ASSIGNMENTS_FILE)
    if document.get("schema_version") != 1:
        errors.append(f"{ASSIGNMENTS_FILE}: schema_version must be 1")

    records = document.get("assignment", [])
    if not isinstance(records, list):
        return [], [*errors, f"{ASSIGNMENTS_FILE}: assignment must be an array of tables"]

    assignments = []
    for index, record in enumerate(records):
        label = f"assignment[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{label} must be a table")
            continue
        assignment_id = _string(record, "id", label=label, errors=errors)
        agent_family = _string(record, "agent_family", label=label, errors=errors)
        branch = _string(record, "branch", label=label, errors=errors)
        base_commit = _string(record, "base_commit", label=label, errors=errors)
        role = _string(record, "role", label=label, errors=errors)
        state = _string(record, "state", label=label, errors=errors)
        write_scope = _scopes(record, "write_scope", label=label, errors=errors)
        shared_scope = _scopes(record, "permitted_shared_files", label=label, errors=errors)

        match = BRANCH_PATTERN.fullmatch(branch)
        if branch and not match:
            errors.append(f"{label}.branch must match agent/<family>/<task>: {branch!r}")
        elif match and match.group("family") != agent_family:
            errors.append(f"{label}.branch family does not match agent_family")
        if base_commit and not COMMIT_PATTERN.fullmatch(base_commit):
            errors.append(f"{label}.base_commit must be a 40-character lowercase commit id")
        if state and state not in ASSIGNMENT_STATES:
            choices = ", ".join(sorted(ASSIGNMENT_STATES))
            errors.append(f"{label}.state must be one of: {choices}")
        for shared in shared_scope:
            if not any(write.contains(shared.path) for write in write_scope):
                errors.append(
                    f"{label}.permitted_shared_files path is outside write_scope: {shared.path}"
                )

        assignments.append(
            Assignment(
                id=assignment_id,
                agent_family=agent_family,
                branch=branch,
                base_commit=base_commit,
                role=role,
                state=state,
                write_scope=write_scope,
                permitted_shared_files=shared_scope,
            )
        )

    ids = [assignment.id for assignment in assignments]
    branches = [assignment.branch for assignment in assignments]
    for duplicate in sorted({value for value in ids if ids.count(value) > 1}):
        errors.append(f"duplicate assignment id: {duplicate}")
    for duplicate in sorted({value for value in branches if branches.count(value) > 1}):
        errors.append(f"duplicate assignment branch: {duplicate}")

    active = [assignment for assignment in assignments if assignment.state == "active"]
    for left_index, left in enumerate(active):
        for right in active[left_index + 1 :]:
            for left_scope in left.write_scope:
                for right_scope in right.write_scope:
                    if left_scope.overlaps(right_scope):
                        errors.append(
                            "active assignment scopes overlap: "
                            f"{left.id}:{left_scope.path} and {right.id}:{right_scope.path}"
                        )
    return assignments, errors


def load_owned_scopes(repository_root: Path) -> tuple[list[OwnedScope], list[str]]:
    errors: list[str] = []
    document = _load_toml(repository_root, OWNERSHIP_FILE)
    if document.get("schema_version") != 1:
        errors.append(f"{OWNERSHIP_FILE}: schema_version must be 1")
    records = document.get("owned_scope", [])
    if not isinstance(records, list) or not records:
        return [], [*errors, f"{OWNERSHIP_FILE}: owned_scope must be a nonempty array"]

    owned_scopes = []
    for index, record in enumerate(records):
        label = f"owned_scope[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{label} must be a table")
            continue
        agent_family = _string(record, "agent_family", label=label, errors=errors)
        scope = _scope(record.get("path"), field_name=f"{label}.path", errors=errors)
        if scope is not None and not scope.is_directory:
            errors.append(f"{label}.path must end with '/'")
        if scope is not None:
            owned_scopes.append(OwnedScope(scope=scope, agent_family=agent_family))

    for left_index, left in enumerate(owned_scopes):
        for right in owned_scopes[left_index + 1 :]:
            if left.scope.overlaps(right.scope):
                errors.append(f"owned scopes overlap: {left.scope.path} and {right.scope.path}")
    return owned_scopes, errors


def context_errors(repository_root: Path) -> list[str]:
    errors: list[str] = []
    document = _load_toml(repository_root, CONTEXT_FILE)
    if document.get("schema_version") != 1:
        errors.append(f"{CONTEXT_FILE}: schema_version must be 1")
    default = document.get("default")
    if not isinstance(default, dict):
        return [*errors, f"{CONTEXT_FILE}: default must be a table"]
    for field_name in ("include", "exclude"):
        values = default.get(field_name)
        if (
            not isinstance(values, list)
            or not values
            or not all(isinstance(v, str) for v in values)
        ):
            errors.append(f"{CONTEXT_FILE}: default.{field_name} must be a nonempty string list")
    excludes = default.get("exclude", [])
    if isinstance(excludes, list):
        missing = REQUIRED_CONTEXT_EXCLUDES.difference(excludes)
        for pattern in sorted(missing):
            errors.append(f"{CONTEXT_FILE}: required default exclusion is missing: {pattern}")
    return errors


def provider_errors(repository_root: Path, owned_scopes: list[OwnedScope]) -> list[str]:
    errors: list[str] = []
    document = _load_toml(repository_root, PROVIDERS_FILE)
    if document.get("schema_version") != 1:
        errors.append(f"{PROVIDERS_FILE}: schema_version must be 1")
    if document.get("contract") != "src.solver_contract.SolverBackend":
        errors.append(f"{PROVIDERS_FILE}: contract must name the shared SolverBackend")
    providers = document.get("provider", [])
    if not isinstance(providers, list) or not providers:
        return [*errors, f"{PROVIDERS_FILE}: provider must be a nonempty array"]

    provider_ids: list[str] = []
    for index, provider in enumerate(providers):
        label = f"provider[{index}]"
        if not isinstance(provider, dict):
            errors.append(f"{label} must be a table")
            continue
        provider_id = _string(provider, "id", label=label, errors=errors)
        package = _string(provider, "package", label=label, errors=errors)
        _string(provider, "state", label=label, errors=errors)
        provider_ids.append(provider_id)
        expected_package = f"src.hybrid_solver_{provider_id}"
        if provider_id and package != expected_package:
            errors.append(f"{label}.package must be {expected_package!r}")

        expected_scopes = (
            f"src/hybrid_solver_{provider_id}",
            f"experiments/providers/{provider_id}",
            f"tests/providers/{provider_id}",
        )
        for expected_scope in expected_scopes:
            matching = [
                owned
                for owned in owned_scopes
                if owned.scope.path == expected_scope and owned.agent_family == provider_id
            ]
            if len(matching) != 1:
                errors.append(f"{label} requires one matching owned scope for {expected_scope}/")

    for duplicate in sorted({value for value in provider_ids if provider_ids.count(value) > 1}):
        errors.append(f"duplicate provider id: {duplicate}")
    return errors


def repository_errors(repository_root: Path = REPOSITORY_ROOT) -> list[str]:
    _, assignment_errors = load_assignments(repository_root)
    owned_scopes, ownership_errors = load_owned_scopes(repository_root)
    return [
        *assignment_errors,
        *ownership_errors,
        *context_errors(repository_root),
        *provider_errors(repository_root, owned_scopes),
    ]


def changed_path_errors(
    changed_paths: list[str],
    *,
    branch: str,
    assignments: list[Assignment],
    owned_scopes: list[OwnedScope],
) -> list[str]:
    errors: list[str] = []
    match = BRANCH_PATTERN.fullmatch(branch)
    if not match:
        return [f"branch must match agent/<family>/<task>: {branch!r}"]
    agent_family = match.group("family")
    matching = [assignment for assignment in assignments if assignment.branch == branch]
    if len(matching) != 1:
        return [f"branch must have exactly one assignment record: {branch!r}"]
    assignment = matching[0]

    for raw_path in changed_paths:
        candidate_scope = _scope(raw_path, field_name="changed path", errors=errors)
        if candidate_scope is None:
            continue
        candidate = candidate_scope.path
        if not any(scope.contains(candidate) for scope in assignment.write_scope):
            errors.append(f"changed path is outside assignment write_scope: {candidate}")
            continue

        owners = [owned for owned in owned_scopes if owned.scope.contains(candidate)]
        if owners:
            owner = owners[0].agent_family
            if owner != agent_family:
                errors.append(f"{candidate} is owned by {owner}, not branch family {agent_family}")
        elif not any(scope.contains(candidate) for scope in assignment.permitted_shared_files):
            errors.append(f"shared changed path is not explicitly permitted: {candidate}")
    return errors


def _git_changed_paths(repository_root: Path, base: str, head: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACDMRTUXB", f"{base}...{head}"],
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def _git_worktree_paths(repository_root: Path) -> list[str]:
    tracked = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACDMRTUXB", "HEAD"],
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
    )
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return sorted({*tracked.stdout.splitlines(), *untracked.stdout.splitlines()})


def _print_result(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(f"coordination error: {error}", file=sys.stderr)
        return 1
    print("coordination records and owned paths are valid")
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("check", help="validate coordination records")
    diff_parser = subparsers.add_parser(
        "check-diff", help="validate changed paths for one assigned branch"
    )
    diff_parser.add_argument("--base", required=True)
    diff_parser.add_argument("--head", required=True)
    diff_parser.add_argument("--branch", required=True)
    worktree_parser = subparsers.add_parser(
        "check-worktree", help="validate tracked and untracked worktree paths"
    )
    worktree_parser.add_argument("--branch", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    assignments, assignment_errors = load_assignments(REPOSITORY_ROOT)
    owned_scopes, ownership_errors = load_owned_scopes(REPOSITORY_ROOT)
    errors = [
        *assignment_errors,
        *ownership_errors,
        *context_errors(REPOSITORY_ROOT),
        *provider_errors(REPOSITORY_ROOT, owned_scopes),
    ]
    if args.command == "check-diff" and not errors:
        changed_paths = _git_changed_paths(REPOSITORY_ROOT, args.base, args.head)
        errors.extend(
            changed_path_errors(
                changed_paths,
                branch=args.branch,
                assignments=assignments,
                owned_scopes=owned_scopes,
            )
        )
    elif args.command == "check-worktree" and not errors:
        changed_paths = _git_worktree_paths(REPOSITORY_ROOT)
        errors.extend(
            changed_path_errors(
                changed_paths,
                branch=args.branch,
                assignments=assignments,
                owned_scopes=owned_scopes,
            )
        )
    return _print_result(errors)


if __name__ == "__main__":
    raise SystemExit(main())
