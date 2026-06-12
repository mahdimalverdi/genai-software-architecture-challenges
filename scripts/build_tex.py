from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "drafts" / "report"
BUILD_LATEX = ROOT / "build" / "latex"
TEMPLATES = ROOT / "templates"


def convert_inline(text: str) -> str:
    """Convert a small, controlled subset of Markdown inline syntax to LaTeX."""
    text = re.sub(r"`([^`]+)`", r"\\texttt{\1}", text)
    return text


def convert_markdown_to_latex(text: str) -> str:
    lines = []
    in_itemize = False
    in_quote = False

    def close_blocks() -> None:
        nonlocal in_itemize, in_quote
        if in_itemize:
            lines.append(r"\end{itemize}")
            in_itemize = False
        if in_quote:
            lines.append(r"\end{quote}")
            in_quote = False

    for line in text.splitlines():
        stripped = line.strip()

        if stripped.startswith("# "):
            close_blocks()
            lines.append(r"\section{" + convert_inline(stripped[2:]) + "}")
        elif stripped.startswith("## "):
            close_blocks()
            lines.append(r"\subsection{" + convert_inline(stripped[3:]) + "}")
        elif stripped.startswith("### "):
            close_blocks()
            lines.append(r"\subsubsection{" + convert_inline(stripped[4:]) + "}")
        elif stripped.startswith("- "):
            if in_quote:
                lines.append(r"\end{quote}")
                in_quote = False
            if not in_itemize:
                lines.append(r"\begin{itemize}")
                in_itemize = True
            lines.append(r"\item " + convert_inline(stripped[2:]))
        elif stripped.startswith("> "):
            if in_itemize:
                lines.append(r"\end{itemize}")
                in_itemize = False
            if not in_quote:
                lines.append(r"\begin{quote}")
                in_quote = True
            lines.append(convert_inline(stripped[2:]))
        elif stripped == "":
            close_blocks()
            lines.append("")
        else:
            close_blocks()
            lines.append(convert_inline(line))

    close_blocks()
    return "\n".join(lines)


def main() -> None:
    BUILD_LATEX.mkdir(parents=True, exist_ok=True)

    content_parts = []
    for path in sorted(REPORT_DIR.glob("*.md")):
        content_parts.append(convert_markdown_to_latex(path.read_text(encoding="utf-8")))

    content = "\n\n".join(content_parts)
    report_template = (TEMPLATES / "report.tex.j2").read_text(encoding="utf-8")
    preamble_template = (TEMPLATES / "preamble.tex.j2").read_text(encoding="utf-8")

    (BUILD_LATEX / "report.tex").write_text(
        report_template.replace("{{ content }}", content),
        encoding="utf-8",
    )
    (BUILD_LATEX / "preamble.tex").write_text(preamble_template, encoding="utf-8")

    references = ROOT / "references" / "references.bib"
    if references.exists():
        (BUILD_LATEX / "references.bib").write_text(
            references.read_text(encoding="utf-8"),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
