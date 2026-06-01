from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BIB_PATH = ROOT / "references" / "references.bib"

ENTRY_START = re.compile(r"^@(\w+)\s*\{\s*([^,]+),")
FIELD_LINE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_-]*)\s*=\s*(.+?)(,?)\s*$")

FIELD_ORDER = [
    "author",
    "title",
    "booktitle",
    "journal",
    "publisher",
    "institution",
    "type",
    "year",
    "volume",
    "number",
    "pages",
    "doi",
    "archivePrefix",
    "eprint",
    "url",
    "note",
]


def split_entries(text: str) -> tuple[list[str], list[str]]:
    header = []
    entries = []
    current = []
    depth = 0
    in_entry = False

    for line in text.splitlines():
        if line.lstrip().startswith("@") and not in_entry:
            in_entry = True
            current = [line.rstrip()]
            depth = line.count("{") - line.count("}")
            if depth == 0:
                entries.append("\n".join(current))
                in_entry = False
            continue

        if in_entry:
            current.append(line.rstrip())
            depth += line.count("{") - line.count("}")
            if depth == 0:
                entries.append("\n".join(current))
                in_entry = False
        elif line.strip():
            header.append(line.rstrip())

    return header, entries


def parse_entry(entry: str) -> tuple[str, str, dict[str, str]]:
    lines = entry.splitlines()
    match = ENTRY_START.match(lines[0])
    if not match:
        return "misc", "unknown", {}

    entry_type = match.group(1)
    key = match.group(2).strip()
    fields = {}

    for line in lines[1:-1]:
        match = FIELD_LINE.match(line)
        if match:
            field_name = match.group(1)
            value = match.group(2).rstrip().rstrip(",")
            fields[field_name] = value

    return entry_type, key, fields


def format_entry(entry: str) -> str:
    entry_type, key, fields = parse_entry(entry)
    ordered_names = [name for name in FIELD_ORDER if name in fields]
    extra_names = sorted(name for name in fields if name not in FIELD_ORDER)
    names = ordered_names + extra_names

    lines = [f"@{entry_type}{{{key},"]
    for index, name in enumerate(names):
        comma = "," if index < len(names) - 1 else ""
        lines.append(f"  {name:<13} = {fields[name]}{comma}")
    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    text = BIB_PATH.read_text(encoding="utf-8")
    header, entries = split_entries(text)
    formatted_entries = [format_entry(entry) for entry in entries]
    formatted_entries.sort(key=lambda item: ENTRY_START.match(item.splitlines()[0]).group(2).lower())

    parts = []
    if header:
        parts.append("\n".join(header))
    parts.extend(formatted_entries)

    BIB_PATH.write_text("\n\n".join(parts).rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
