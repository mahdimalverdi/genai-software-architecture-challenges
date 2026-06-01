from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "drafts" / "report"
BUILD_LATEX = ROOT / "build" / "latex"
TEMPLATES = ROOT / "templates"


def convert_markdown_to_latex(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.startswith("# "):
            lines.append(r"\section{" + line[2:].strip() + "}")
        elif line.startswith("## "):
            lines.append(r"\subsection{" + line[3:].strip() + "}")
        elif line.strip() == "":
            lines.append("")
        else:
            lines.append(line)
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
