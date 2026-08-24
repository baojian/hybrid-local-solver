"""Reproducible numerical and exact-arithmetic audits for research-note claims."""

from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def note_directory(note_id: str) -> Path:
    """Return the source directory for a registered standalone research note."""

    return REPOSITORY_ROOT / "manuscript" / "notes" / note_id


def note_tex_source(note_id: str) -> str:
    """Read a note's entrypoint and section files as one audit source."""

    directory = note_directory(note_id)
    paths = [directory / "main.tex"]
    sections = directory / "sections"
    if sections.is_dir():
        paths.extend(sorted(sections.rglob("*.tex")))
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)
