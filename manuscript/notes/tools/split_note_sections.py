"""Mechanically extract an inline research-note body into ordered section files.

The splitter preserves every byte from the first top-level ``\\section`` to
``\\end{document}``, changing only where that text is stored. Section and
subsection boundaries are preferred. If one such block exceeds ``--max-lines``,
the tool cuts only immediately before a theorem-like environment so a theorem
and its following proof remain together.

This is an explicit migration tool, not part of normal note builds. It refuses
to overwrite an existing ``sections/body`` directory.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
NOTES_ROOT = REPOSITORY_ROOT / "manuscript" / "notes"
HEADING = re.compile(r"^\\(?:section|subsection)\{")
RESULT = re.compile(
    r"^\\begin\{(?:theorem|lemma|proposition|corollary|definition|problem|remark)\}"
)
LABEL = re.compile(r"\\label\{([^}]+)\}")
TITLE = re.compile(r"^\\(?:section|subsection)\{([^}]*)")


def _slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return slug[:72] or "part"


def _chunk_name(index: int, lines: list[str]) -> str:
    sample = "".join(lines[:30])
    label = LABEL.search(sample)
    if label:
        name = _slug(label.group(1))
    else:
        title = TITLE.match(lines[0])
        name = _slug(title.group(1) if title else "part")
    return f"{index:02d}_{name}.tex"


def _separate_trailing_blank_lines(text: str) -> tuple[str, str]:
    """Keep one final newline in a file and return the remaining separator."""

    trailing_newlines = len(text) - len(text.rstrip("\n"))
    if trailing_newlines <= 1:
        return text, ""
    separator = "\n" * (trailing_newlines - 1)
    return text[: -len(separator)], separator


def _bounded_chunks(
    lines: list[str], start: int, end: int, max_lines: int
) -> list[tuple[int, int]]:
    cuts = [start]
    cursor = start
    result_starts = [index for index in range(start + 1, end) if RESULT.match(lines[index])]
    while end - cursor > max_lines:
        before_limit = [index for index in result_starts if cursor < index <= cursor + max_lines]
        if before_limit:
            next_cut = before_limit[-1]
        else:
            after_limit = [index for index in result_starts if index > cursor]
            if not after_limit:
                break
            next_cut = after_limit[0]
        if next_cut == cursor:
            break
        cuts.append(next_cut)
        cursor = next_cut
    cuts.append(end)
    return list(zip(cuts[:-1], cuts[1:], strict=True))


def split_note(note_id: str, max_lines: int) -> list[Path]:
    """Split one registered note and return the created section paths."""

    note = NOTES_ROOT / note_id
    main = note / "main.tex"
    output = note / "sections" / "body"
    if not main.is_file():
        raise ValueError(f"missing note entrypoint: {main}")
    if output.exists():
        raise ValueError(f"refusing to overwrite existing directory: {output}")

    original = main.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)
    try:
        body_start = next(
            index for index, line in enumerate(lines) if line.startswith(r"\section{")
        )
        document_end = next(
            index
            for index in range(body_start, len(lines))
            if lines[index].startswith(r"\end{document}")
        )
    except StopIteration as error:
        raise ValueError(f"{main}: expected \\section and \\end{{document}}") from error

    headings = [index for index in range(body_start, document_end) if HEADING.match(lines[index])]
    boundaries = [*headings, document_end]
    spans: list[tuple[int, int]] = []
    for start, end in zip(boundaries[:-1], boundaries[1:], strict=True):
        spans.extend(_bounded_chunks(lines, start, end, max_lines))

    output.mkdir(parents=True)
    created: list[Path] = []
    inputs: list[str] = []
    reconstructed: list[str] = []
    for index, (start, end) in enumerate(spans, start=1):
        content_lines = lines[start:end]
        filename = _chunk_name(index, content_lines)
        path = output / filename
        if path.exists():
            raise ValueError(f"refusing to overwrite section: {path}")
        content = "".join(content_lines)
        stored_content, separator = _separate_trailing_blank_lines(content)
        path.write_text(stored_content, encoding="utf-8")
        created.append(path)
        inputs.append(f"\\input{{sections/body/{path.stem}}}\n{separator}")
        reconstructed.append(stored_content + separator)

    if "".join(reconstructed) != "".join(lines[body_start:document_end]):
        raise RuntimeError(f"{note_id}: extracted body does not reconstruct byte-for-byte")

    new_main = "".join([*lines[:body_start], *inputs, *lines[document_end:]])
    main.write_text(new_main, encoding="utf-8")
    return created


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("note", nargs="+", help="registered note id")
    parser.add_argument("--max-lines", type=int, default=900)
    arguments = parser.parse_args()
    if arguments.max_lines < 100:
        parser.error("--max-lines must be at least 100")

    for note_id in arguments.note:
        created = split_note(note_id, arguments.max_lines)
        print(f"{note_id}: extracted {len(created)} body files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
