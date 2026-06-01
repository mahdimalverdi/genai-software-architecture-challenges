from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BIB_PATH = ROOT / "references" / "references.bib"

BOOK_ENTRIES = {
    "engineeringAiSystems2025": """@book{engineeringAiSystems2025,
  author    = {Bass, Len and Lu, Qinghua and Weber, Ingo and Zhu, Liming},
  title     = {Engineering AI Systems: Architecture and DevOps Essentials},
  publisher = {Addison-Wesley Professional},
  year      = {2025},
  edition   = {1st},
  isbn      = {978-0138261412},
  url       = {https://books.google.com/books?id=Z4s-EQAAQBAJ},
  note      = {ISBN-10: 0138261415. Publication date: February 11, 2025.}
}""",
    "huyen2025aiEngineering": """@book{huyen2025aiEngineering,
  author    = {Huyen, Chip},
  title     = {AI Engineering: Building Applications with Foundation Models},
  publisher = {O'Reilly Media},
  year      = {2025},
  edition   = {1st},
  isbn      = {978-1098166304},
  url       = {https://www.oreilly.com/library/view/ai-engineering/9781098166298/},
  note      = {ISBN-10: 1098166302. Publication date: January 7, 2025.}
}""",
}


def replace_entry(text: str, key: str, replacement: str) -> tuple[str, bool]:
    pattern = re.compile(r"@book\{" + re.escape(key) + r",\n(?:.*?\n)\}", re.DOTALL)
    if pattern.search(text):
        return pattern.sub(replacement, text, count=1), True
    return text.rstrip() + "\n\n" + replacement + "\n", False


def main() -> None:
    text = BIB_PATH.read_text(encoding="utf-8")
    for key, entry in BOOK_ENTRIES.items():
        text, replaced = replace_entry(text, key, entry)
        action = "UPDATED" if replaced else "ADDED"
        print(f"{action} {key}")
    BIB_PATH.write_text(text.rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
