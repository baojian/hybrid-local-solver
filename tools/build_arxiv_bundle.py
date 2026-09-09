"""Package only the compiled active paper's local dependencies for arXiv.

Run after a successful manuscript build. The TeX recorder supplies the actual
input graph; global TeX-distribution packages and research-note archives are
not copied. A clean extracted-archive build is the independent completeness
check used when preparing a release.
"""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import shutil
import tarfile
from pathlib import Path


MANUSCRIPT = Path(__file__).resolve().parents[1] / "manuscript"
SOURCE_SUFFIXES = {
    ".tex",
    ".sty",
    ".cls",
    ".bst",
    ".bbl",
    ".bib",
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".eps",
}
README = """Accelerated Local Algorithms for Personalized and Regularized PageRank
Baojian Zhou

This archive is a self-contained source copy of the active manuscript.
The main entry point is main.tex. Standard TeX Live packages are required.

Build with:
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

The generated main.bbl is included. To rebuild the bibliography manually:
    pdflatex main.tex
    bibtex main
    pdflatex main.tex
    pdflatex main.tex

The full references.bib is retained for future editing. Research notes,
source-paper PDFs, numerical development archives, and temporary build files
are not needed to compile this article and are not included.
"""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def collect_sources() -> dict[str, bytes]:
    for name in ("main.tex", "main.fls", "main.bbl", "main.pdf", "references.bib"):
        if not (MANUSCRIPT / name).is_file():
            raise RuntimeError(f"Missing {name}; build the manuscript first")
    inputs = {MANUSCRIPT / "main.tex", MANUSCRIPT / "references.bib", MANUSCRIPT / "main.bbl"}
    for line in (MANUSCRIPT / "main.fls").read_text().splitlines():
        if not line.startswith("INPUT "):
            continue
        path = Path(line[6:])
        if not path.is_absolute():
            path = MANUSCRIPT / path
        path = path.resolve()
        if path.is_relative_to(MANUSCRIPT) and path.suffix.lower() in SOURCE_SUFFIXES:
            inputs.add(path)
    members = {}
    for path in sorted(inputs):
        relative = path.relative_to(MANUSCRIPT)
        if relative.parts[0] in {"archive", "notes", "dist"}:
            raise RuntimeError(f"The active paper unexpectedly imports {relative}")
        if not path.is_file():
            raise RuntimeError(f"Missing recorded input: {relative}")
        members[relative.as_posix()] = path.read_bytes()
    members["README.txt"] = README.encode()
    return members


def main() -> None:
    members = collect_sources()
    destination = MANUSCRIPT / "dist"
    destination.mkdir(exist_ok=True)
    archive = destination / "arxiv-source.tar.gz"
    temporary = destination / "arxiv-source.tar.gz.tmp"
    with temporary.open("wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w") as tar:
                for name, data in sorted(members.items()):
                    entry = tarfile.TarInfo(name)
                    entry.size = len(data)
                    entry.mode = 0o644
                    entry.mtime = 0
                    tar.addfile(entry, io.BytesIO(data))
    temporary.replace(archive)
    pdf = destination / "accelerated-local-rppr.pdf"
    shutil.copyfile(MANUSCRIPT / "main.pdf", pdf)
    manifest = {
        "entry_point": "main.tex",
        "archive_sha256": sha256(archive.read_bytes()),
        "pdf_sha256": sha256(pdf.read_bytes()),
        "members": [
            {"path": name, "bytes": len(data), "sha256": sha256(data)}
            for name, data in sorted(members.items())
        ],
    }
    (destination / "arxiv-source-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(
        json.dumps(
            {
                "archive": str(archive),
                "pdf": str(pdf),
                "source_files": len(members),
                "archive_bytes": archive.stat().st_size,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
