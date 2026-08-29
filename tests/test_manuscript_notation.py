from __future__ import annotations

import re
import tomllib
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
MANUSCRIPT = REPOSITORY / "manuscript"
NOTES = MANUSCRIPT / "notes"
SHARED_PROBLEM_INPUT = r"\input{../../tex/shared/source_aligned_problem}"
ACTIVE_SHARED_PROBLEM_INPUT = r"\input{tex/shared/source_aligned_problem}"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _publication_tex_sources() -> list[Path]:
    sources = [MANUSCRIPT / "main.tex", MANUSCRIPT / "appendix.tex"]
    sources.extend(sorted((MANUSCRIPT / "sections").rglob("*.tex")))
    sources.extend(sorted(NOTES.rglob("*.tex")))
    return sources


def test_research_note_registry_matches_standalone_documents() -> None:
    registry = tomllib.loads(_read(NOTES / "registry.toml"))
    records = registry["note"]

    ids = [record["id"] for record in records]
    assert len(ids) == len(set(ids)), "note ids must be unique"

    declared = {Path(record["entrypoint"]) for record in records}
    discovered = {
        path.relative_to(NOTES) for path in NOTES.rglob("*.tex") if r"\documentclass" in _read(path)
    }
    assert declared == discovered
    assert all(path.name == "main.tex" for path in declared)
    for entrypoint in declared:
        note_directory = NOTES / entrypoint.parent
        assert (note_directory / "README.md").is_file()
        makefile = note_directory / "Makefile"
        assert makefile.is_file()
        assert "include ../note.mk" in _read(makefile)


def test_every_note_uses_the_shared_shell_and_problem_model_once() -> None:
    registry = tomllib.loads(_read(NOTES / "registry.toml"))
    for record in registry["note"]:
        entrypoint = NOTES / record["entrypoint"]
        assert r"\input{../../tex/shared/research_note_preamble}" in _read(entrypoint)

        problem_imports = sum(
            _read(path).count(SHARED_PROBLEM_INPUT) for path in entrypoint.parent.rglob("*.tex")
        )
        assert problem_imports == 1, (
            f"{record['id']} must import the common problem model exactly once; "
            f"found {problem_imports} imports"
        )


def test_active_manuscript_uses_the_shared_problem_model_once() -> None:
    sources = [MANUSCRIPT / "main.tex", MANUSCRIPT / "appendix.tex"]
    sources.extend(sorted((MANUSCRIPT / "sections").rglob("*.tex")))
    problem_imports = sum(_read(path).count(ACTIVE_SHARED_PROBLEM_INPUT) for path in sources)
    assert problem_imports == 1
    assert ACTIVE_SHARED_PROBLEM_INPUT in _read(MANUSCRIPT / "sections/problem_formulation.tex")


def test_shared_problem_keeps_author_bold_optimum_notation() -> None:
    shared = _read(MANUSCRIPT / "tex/shared/source_aligned_problem.tex")
    required = {
        r"\bm{A}",
        r"\bm{D}",
        r"\bm{Q}",
        r"\bm{x}",
        r"\bm{s}",
        r"\bm{x}^*",
        r"\bm{x}_0^*",
        r"\bm{x}_\rho^*",
    }
    assert all(symbol in shared for symbol in required)
    assert "plain italic notation" not in shared
    assert r"x^0" not in shared
    assert r"x^\star(\rho)" not in shared


def test_reusable_latex_declarations_are_confined_to_shared_files() -> None:
    declaration = re.compile(
        r"\\(?:newcommand|renewcommand|providecommand|DeclareMathOperator|"
        r"newtheorem|newenvironment|def)\b"
    )
    offenders = [
        path.relative_to(REPOSITORY)
        for path in _publication_tex_sources()
        if declaration.search(_read(path))
    ]
    assert not offenders, f"move reusable declarations to manuscript/tex/shared: {offenders}"


def test_source_aligned_core_definitions_are_not_redeclared() -> None:
    patterns = {
        "PageRank matrix": re.compile(
            r"Q\s*:?=\s*\\frac\{1\+\\alpha\}\{2\}\s*I\s*-\s*"
            r"\\frac\{1-\\alpha\}\{2\}\s*D\^\{-1/2\}AD\^\{-1/2\}",
            re.DOTALL,
        ),
        "smooth PageRank objective": re.compile(
            r"f\(x\)\s*:?=\s*\\frac12\s*x\^\\top\s*Qx\s*-\s*"
            r"\\alpha\s*x\^\\top\s*D\^\{-1/2\}s",
            re.DOTALL,
        ),
        "RPPR regularizer": re.compile(
            r"g_\\rho\(x\)\s*:?=\s*\\alpha\\rho",
            re.DOTALL,
        ),
    }

    offenders: list[str] = []
    for path in _publication_tex_sources():
        text = _read(path)
        for name, pattern in patterns.items():
            if pattern.search(text):
                offenders.append(f"{path.relative_to(REPOSITORY)} ({name})")
    assert not offenders, f"use source_aligned_problem.tex instead: {offenders}"


def test_reserved_seed_and_accuracy_names_do_not_regress() -> None:
    forbidden = {
        "seed vertex written as s": re.compile(r"s\s*\\in\s*(?:V|\\mathcal\{V\}|\\gV|\[n\])"),
        "unit seed e_s": re.compile(r"e_(?:s\b|\{s\})"),
        "ambiguous epsilon glyph": re.compile(r"\\epsilon\b"),
        "ambiguous epsilon macro": re.compile(r"\\eps(?![A-Za-z])"),
    }
    offenders: list[str] = []
    for path in _publication_tex_sources():
        text = _read(path)
        for name, pattern in forbidden.items():
            if pattern.search(text):
                offenders.append(f"{path.relative_to(REPOSITORY)} ({name})")
    assert not offenders, f"reserved notation drift detected: {offenders}"


def test_known_semantic_aliases_do_not_regress() -> None:
    forbidden = {
        "RPPR map must retain alpha and rho": re.compile(r"\\mathcal\s*T_\\rho"),
        "fixed-point residual must retain its namespace": re.compile(r"R_\\rho\b"),
        "AESP ratio must not use FISTA q": re.compile(r"q_(?:A|\{\\(?:rm|mathrm)\s+(?:A|cat)\})"),
        "AESP decay must not reuse RPPR rho": re.compile(r"\\rho_(?:A|\{\\(?:rm|mathrm)\s+A\})"),
        "regularizer must not be called r_rho": re.compile(r"r_\\rho\s*\("),
        "smooth gradient must be nabla f": re.compile(r"g\s*\(x\)\s*:?=\s*\\nabla\s*f"),
        "normalized adjacency must not be W": re.compile(
            r"W\s*:?=\s*D\^\{-1/2\}\s*A\s*D\^\{-1/2\}"
        ),
        "unregularized optimum must be x_0^*": re.compile(
            r"\\bm\{x\}\^\*\s*:?=\s*\\bm\{Q\}\^\{-1\}\\bm\{b\}"
        ),
    }
    offenders: list[str] = []
    for path in _publication_tex_sources():
        text = _read(path)
        for name, pattern in forbidden.items():
            if pattern.search(text):
                offenders.append(f"{path.relative_to(REPOSITORY)} ({name})")
    assert not offenders, f"semantic notation drift detected: {offenders}"
