"""Fetch pinned experiment graphs into an explicitly selected directory."""

from __future__ import annotations

import argparse
import hashlib
import os
from collections.abc import Callable
from pathlib import Path
from typing import BinaryIO
from urllib.request import Request, urlopen

from src.graphs import GRAPH_FILES, GRAPH_NAMES, validate_graph_file

DATASET_ID = "baojian-zh/local-pagerank-graphs"
DATASET_REVISION = "a1fcce6153e4c9707c1eb18a91eeebd6bbe7a0ed"
DATASET_SUBDIRECTORY = "localized-sparse-spd-solver/input"
DATASET_BASE_URL = (
    f"https://huggingface.co/datasets/{DATASET_ID}/resolve/"
    f"{DATASET_REVISION}/{DATASET_SUBDIRECTORY}"
)
DEFAULT_TIMEOUT_SECONDS = 60
CHUNK_SIZE = 1024 * 1024

OpenUrl = Callable[..., BinaryIO]


def graph_url(name: str) -> str:
    """Return the revision-pinned source URL for one catalogued graph."""
    if name not in GRAPH_FILES:
        choices = ", ".join(GRAPH_NAMES)
        raise ValueError(f"unknown graph {name!r}; expected one of: {choices}")
    return f"{DATASET_BASE_URL}/{name}/{name}_csr-mat.npz"


def fetch_graph(
    name: str,
    *,
    data_dir: str | os.PathLike[str],
    force: bool = False,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    opener: OpenUrl | None = None,
) -> Path:
    """Fetch and verify one graph, writing only below ``data_dir``."""
    source_url = graph_url(name)
    destination = Path(data_dir).expanduser() / name / f"{name}_csr-mat.npz"

    if destination.exists() and not force:
        try:
            return validate_graph_file(name, destination, check_sha256=True)
        except OSError as error:
            raise OSError(
                f"existing graph file did not match the pinned manifest: {destination}; "
                "pass --force to replace it"
            ) from error

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.{os.getpid()}.part")
    expected_size, expected_sha256 = GRAPH_FILES[name]
    digest = hashlib.sha256()
    downloaded = 0
    request = Request(source_url, headers={"User-Agent": "hybrid-local-solver/0.1"})
    open_url = opener or urlopen

    try:
        with open_url(request, timeout=timeout) as response, temporary.open("wb") as output:
            while chunk := response.read(CHUNK_SIZE):
                output.write(chunk)
                digest.update(chunk)
                downloaded += len(chunk)

        if downloaded != expected_size:
            raise OSError(
                f"size mismatch for {name}: expected {expected_size}, downloaded {downloaded}"
            )
        actual_sha256 = digest.hexdigest()
        if actual_sha256 != expected_sha256:
            raise OSError(
                f"SHA-256 mismatch for {name}: expected {expected_sha256}, "
                f"downloaded {actual_sha256}"
            )
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)

    return destination


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch revision-pinned graph files for full experiments."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        required=True,
        help="destination root; files are written below <data-dir>/<graph>/",
    )
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument(
        "--graph",
        action="append",
        choices=GRAPH_NAMES,
        help="graph to fetch; repeat to select more than one",
    )
    selection.add_argument("--all", action="store_true", help="fetch every catalogued graph")
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace an existing file after downloading and verifying a new copy",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    names = GRAPH_NAMES if args.all else tuple(args.graph)
    for name in names:
        destination = fetch_graph(name, data_dir=args.data_dir, force=args.force)
        print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
