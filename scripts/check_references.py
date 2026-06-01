from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BIB_PATH = ROOT / "references" / "references.bib"

ENTRY_START = re.compile(r"^@(\w+)\s*\{\s*([^,]+),")
REQUIRED_FIELDS = {
    "article": {"author", "title", "year"},
    "book": {"author", "title", "publisher", "year"},
    "inproceedings": {"author", "title", "booktitle", "year"},
    "techreport": {"author", "title", "institution", "year"},
    "misc": {"title", "year"},
}


def split_entries(text: str) -> list[str]:
    entries = []
    current = []
    depth = 0
    in_entry = False

    for line in text.splitlines():
        if line.lstrip().startswith("@") and not in_entry:
            in_entry = True
            current = [line.rstrip()]
            depth = line.count("{") - line.count("}")
            continue

        if in_entry:
            current.append(line.rstrip())
            depth += line.count("{") - line.count("}")
            if depth == 0:
                entries.append("\n".join(current))
                in_entry = False

    return entries


def entry_fields(entry: str) -> tuple[str, str, set[str]]:
    lines = entry.splitlines()
    match = ENTRY_START.match(lines[0])
    if not match:
        return "unknown", "unknown", set()

    entry_type = match.group(1).lower()
    key = match.group(2).strip()
    fields = set()
    for line in lines[1:-1]:
        if "=" in line:
            fields.add(line.split("=", 1)[0].strip())
    return entry_type, key, fields


def main() -> None:
    text = BIB_PATH.read_text(encoding="utf-8")
    entries = split_entries(text)
    keys = []
    errors = []

    for entry in entries:
        entry_type, key, fields = entry_fields(entry)
        keys.append(key)
        required = REQUIRED_FIELDS.get(entry_type, {"title", "year"})
        missing = sorted(required - fields)
        if missing:
            errors.append(f"{key}: missing {', '.join(missing)}")
        if not ({"doi", "url", "eprint"} & fields):
            errors.append(f"{key}: missing one of doi/url/eprint")

    duplicate_keys = sorted({key for key in keys if keys.count(key) > 1})
    for key in duplicate_keys:
        errors.append(f"{key}: duplicate key")

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)

    print(f"OK: {len(entries)} references checked.")


if __name__ == "__main__":
    main()
