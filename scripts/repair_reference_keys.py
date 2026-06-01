from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BIB_PATH = ROOT / "references" / "references.bib"

ENTRY_START = re.compile(r"^@(?P<type>[A-Za-z]+)\s*\{\s*(?P<key>[^,]*)\s*,?")
FIELD_LINE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_-]*)\s*=\s*[{\"](.+?)[}\"],?\s*$")
STOP_WORDS = {
    "a",
    "an",
    "and",
    "for",
    "in",
    "into",
    "is",
    "of",
    "on",
    "the",
    "to",
    "using",
    "with",
}


def split_entries(text: str) -> tuple[str, list[str]]:
    prefix_lines = []
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
        else:
            prefix_lines.append(line.rstrip())

    return "\n".join(prefix_lines).strip(), entries


def parse_fields(entry: str) -> dict[str, str]:
    fields = {}
    for line in entry.splitlines()[1:-1]:
        match = FIELD_LINE.match(line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


def clean_key(key: str) -> str:
    return key.strip().strip("{}").strip()


def is_valid_key(key: str) -> bool:
    if not key or key in {"unknown", "{"}:
        return False
    if key.startswith("{") or key.endswith("}"):
        return False
    return bool(re.fullmatch(r"[A-Za-z0-9:_./-]+", key))


def family_name(author: str | None) -> str:
    if not author:
        return "ref"
    first_author = author.split(" and ")[0].replace("{", "").replace("}", "")
    if "," in first_author:
        name = first_author.split(",", 1)[0]
    else:
        parts = first_author.split()
        name = parts[-1] if parts else "ref"
    name = re.sub(r"[^A-Za-z0-9]", "", name).lower()
    return name or "ref"


def title_suffix(title: str | None) -> str:
    if not title:
        return "reference"
    words = re.findall(r"[A-Za-z0-9]+", title.lower())
    words = [word for word in words if word not in STOP_WORDS]
    selected = words[:4] or ["reference"]
    return selected[0] + "".join(word.capitalize() for word in selected[1:])


def make_key(fields: dict[str, str]) -> str:
    author_part = family_name(fields.get("author"))
    year_part = re.sub(r"[^0-9]", "", fields.get("year", "")) or "unknown"
    return author_part + year_part + title_suffix(fields.get("title"))


def unique_key(base_key: str, used_keys: set[str]) -> str:
    if base_key not in used_keys:
        used_keys.add(base_key)
        return base_key

    index = 2
    while f"{base_key}{index}" in used_keys:
        index += 1
    key = f"{base_key}{index}"
    used_keys.add(key)
    return key


def repair_entry(entry: str, used_keys: set[str]) -> tuple[str, bool, str, str]:
    lines = entry.splitlines()
    match = ENTRY_START.match(lines[0])
    if not match:
        return entry, False, "unknown", "unknown"

    entry_type = match.group("type")
    current_key = clean_key(match.group("key"))
    fields = parse_fields(entry)

    if is_valid_key(current_key) and current_key not in used_keys:
        used_keys.add(current_key)
        return entry, False, current_key, current_key

    new_key = unique_key(make_key(fields), used_keys)
    lines[0] = f"@{entry_type}{{{new_key},"
    return "\n".join(lines), True, current_key or "<empty>", new_key


def main() -> None:
    text = BIB_PATH.read_text(encoding="utf-8")
    prefix, entries = split_entries(text)
    used_keys = set()
    repaired_entries = []
    repaired_count = 0

    for entry in entries:
        repaired_entry, repaired, old_key, new_key = repair_entry(entry, used_keys)
        repaired_entries.append(repaired_entry)
        if repaired:
            repaired_count += 1
            print(f"REPAIRED {old_key} -> {new_key}")

    parts = []
    if prefix:
        parts.append(prefix)
    parts.extend(repaired_entries)
    BIB_PATH.write_text("\n\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Done. Repaired keys: {repaired_count}")


if __name__ == "__main__":
    main()
