"""Proof checks for the September 6 two-stage investigation."""

from datetime import datetime, timezone
import hashlib
from pathlib import Path
import subprocess


def provenance(parameters, output=None):
    """Record a reproducible source snapshot for newly launched audits."""
    package = Path(__file__).resolve().parent
    root = package.parents[2]
    hashes = {}
    snapshot = output.parent / (output.stem + "_source") if output else None
    if snapshot:
        snapshot.mkdir(parents=True, exist_ok=True)
    for path in sorted(package.glob("*.py")):
        content = path.read_bytes()
        hashes[path.name] = hashlib.sha256(content).hexdigest()
        if snapshot:
            (snapshot / path.name).write_bytes(content)
    return {
        "start_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], cwd=root, text=True)
        ),
        "source_sha256": hashes,
        "source_snapshot": str(snapshot) if snapshot else None,
        "random_seed": None,
        "parameters": parameters,
    }
