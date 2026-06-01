from pathlib import Path
import re
import textwrap

ROOT = Path(__file__).resolve().parents[1]
BIB_PATH = ROOT / "references" / "references.bib"

ENTRY_START = re.compile(r"^@(\w+)\s*\{\s*([^,]+),")
FIELD_LINE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_-]*)\s*=\s*(.+?)(,?)\s*$")

MAX_LINE_LENGTH = 100
WRAPPED_FIELDS = {
    "author",
    "title",
    "booktitle",
    "journal",
    "publisher",
    "institution",
    "note",
}

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
    "isbn",
    "doi",
    "archivePrefix",
    "eprint",
    "url",
    "note",
]

ARXIV_JOURNAL_RE = re.compile(r"\{?arXiv preprint arXiv:[0-9.]+\}?", re.IGNORECASE)


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


def clean_value(value: str) -> str:
    value = value.strip().rstrip(",").strip()
    if len(value) >= 2 and value[0] in "{\"" and value[-1] in "}\"":
        return value[1:-1].strip()
    return value


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
            fields[field_name] = clean_value(match.group(2))

    return entry_type, key, fields


def normalize_entry(entry_type: str, fields: dict[str, str]) -> tuple[str, dict[str, str]]:
    normalized_fields = dict(fields)
    has_booktitle = bool(normalized_fields.get("booktitle"))
    has_journal = bool(normalized_fields.get("journal"))

    if has_booktitle:
        journal = normalized_fields.get("journal", "")
        if ARXIV_JOURNAL_RE.fullmatch(journal.strip()):
            normalized_fields.pop("journal", None)
        entry_type = "inproceedings"

    if has_journal and not has_booktitle:
        entry_type = "article"

    if entry_type == "inproceedings":
        normalized_fields.pop("journal", None)
    elif entry_type == "article":
        normalized_fields.pop("booktitle", None)

    return entry_type, normalized_fields


def wrap_field(name: str, value: str, comma: str) -> list[str]:
    prefix = f"  {name:<13} = {{"
    suffix = f"}}{comma}"
    single_line = f"{prefix}{value}{suffix}"

    if name not in WRAPPED_FIELDS or len(single_line) <= MAX_LINE_LENGTH:
        return [single_line]

    width = MAX_LINE_LENGTH - len(prefix)
    wrapped = textwrap.wrap(
        value,
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    )

    if len(wrapped) <= 1:
        return [single_line]

    lines = [f"{prefix}{wrapped[0]}"]
    continuation_prefix = " " * len(prefix)
    for part in wrapped[1:-1]:
        lines.append(f"{continuation_prefix}{part}")
    lines.append(f"{continuation_prefix}{wrapped[-1]}{suffix}")
    return lines


def format_entry(entry: str) -> str:
    entry_type, key, fields = parse_entry(entry)
    entry_type, fields = normalize_entry(entry_type, fields)
    ordered_names = [name for name in FIELD_ORDER if name in fields]
    extra_names = sorted(name for name in fields if name not in FIELD_ORDER)
    names = ordered_names + extra_names

    lines = [f"@{entry_type}{{{key},"]
    for index, name in enumerate(names):
        comma = "," if index < len(names) - 1 else ""
        lines.extend(wrap_field(name, fields[name], comma))
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
