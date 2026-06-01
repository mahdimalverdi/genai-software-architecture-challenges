from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
BIB_PATH = ROOT / "references" / "references.bib"
CROSSREF_WORKS_URL = "https://api.crossref.org/works/"

ENTRY_START = re.compile(r"^@(?P<type>[A-Za-z]+)\s*\{\s*(?P<key>[^,]+)\s*,")
FIELD_LINE = re.compile(r"^\s*(?P<name>[A-Za-z][A-Za-z0-9_-]*)\s*=\s*(?P<value>.+?)(?P<comma>,?)\s*$")

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

PRESERVED_FIELDS = {"archivePrefix", "eprint", "note"}
CONFERENCE_TYPES = {"conference-paper", "proceedings-article"}
JOURNAL_TYPES = {"journal-article", "journal-issue", "journal-volume"}
BOOK_TYPES = {"book", "monograph"}


@dataclass
class BibEntry:
    entry_type: str
    key: str
    fields: dict[str, str]
    raw: str


def strip_bib_value(value: str) -> str:
    value = value.strip().rstrip(",").strip()
    if len(value) >= 2 and value[0] in "{\"" and value[-1] in "}\"":
        return value[1:-1].strip()
    return value


def brace(value: str) -> str:
    return "{" + value.replace("\n", " ").strip() + "}"


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


def parse_entry(raw_entry: str) -> BibEntry | None:
    lines = raw_entry.splitlines()
    if not lines:
        return None

    entry_match = ENTRY_START.match(lines[0])
    if not entry_match:
        return None

    fields = {}
    for line in lines[1:-1]:
        field_match = FIELD_LINE.match(line)
        if not field_match:
            continue
        fields[field_match.group("name")] = strip_bib_value(field_match.group("value"))

    return BibEntry(
        entry_type=entry_match.group("type"),
        key=entry_match.group("key").strip(),
        fields=fields,
        raw=raw_entry,
    )


def request_json(url: str, timeout_seconds: int = 20) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "genai-software-architecture-challenges/1.0"})
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def fetch_crossref_work(doi: str) -> dict | None:
    url = CROSSREF_WORKS_URL + urllib.parse.quote(doi.strip(), safe="")
    try:
        data = request_json(url)
    except urllib.error.HTTPError as error:
        print(f"WARN: DOI lookup failed for {doi}: HTTP {error.code}")
        return None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        print(f"WARN: DOI lookup failed for {doi}: {error}")
        return None

    return data.get("message")


def crossref_entry_type(work: dict, fallback: str) -> str:
    work_type = work.get("type", "")
    if work_type in CONFERENCE_TYPES:
        return "inproceedings"
    if work_type in JOURNAL_TYPES:
        return "article"
    if work_type in BOOK_TYPES:
        return "book"
    if work_type == "book-chapter":
        return "incollection"
    return fallback


def crossref_year(work: dict) -> str | None:
    for field in ["published-print", "published-online", "published", "issued"]:
        date_parts = work.get(field, {}).get("date-parts")
        if date_parts and date_parts[0]:
            return str(date_parts[0][0])
    return None


def first_item(values: list | None) -> str | None:
    if values:
        return " ".join(str(values[0]).split())
    return None


def crossref_author(author: dict) -> str | None:
    family = author.get("family")
    given = author.get("given")
    name = author.get("name")
    if family and given:
        return f"{family}, {given}"
    if family:
        return family
    if name:
        return name
    return None


def crossref_authors(work: dict) -> str | None:
    authors = []
    for author in work.get("author", []):
        formatted = crossref_author(author)
        if formatted:
            authors.append(formatted)
    return " and ".join(authors) if authors else None


def crossref_fields(work: dict, existing_fields: dict[str, str]) -> dict[str, str]:
    fields = {}
    work_type = work.get("type", "")

    authors = crossref_authors(work)
    title = first_item(work.get("title"))
    container_title = first_item(work.get("container-title"))
    year = crossref_year(work)

    if authors:
        fields["author"] = authors
    if title:
        fields["title"] = title
    if container_title:
        if work_type in CONFERENCE_TYPES:
            fields["booktitle"] = container_title
        elif work_type in JOURNAL_TYPES:
            fields["journal"] = container_title
        else:
            fields["journal"] = container_title
    if work.get("publisher"):
        fields["publisher"] = work["publisher"]
    if year:
        fields["year"] = year
    if work.get("volume"):
        fields["volume"] = work["volume"]
    if work.get("issue"):
        fields["number"] = work["issue"]
    if work.get("page"):
        fields["pages"] = work["page"]
    if work.get("DOI"):
        fields["doi"] = work["DOI"].lower()
    if work.get("URL"):
        fields["url"] = work["URL"]

    for field in PRESERVED_FIELDS:
        if existing_fields.get(field):
            fields[field] = existing_fields[field]

    return fields


def remove_stale_fields(fields: dict[str, str], entry_type: str, fresh: dict[str, str]) -> dict[str, str]:
    cleaned = dict(fields)
    if entry_type == "inproceedings" or "booktitle" in fresh:
        cleaned.pop("journal", None)
    if entry_type == "article" or "journal" in fresh:
        cleaned.pop("booktitle", None)
    if entry_type not in {"article", "inproceedings"}:
        cleaned.pop("journal", None)
        cleaned.pop("booktitle", None)
    return cleaned


def merge_fields(existing: dict[str, str], fresh: dict[str, str], only_missing: bool, entry_type: str) -> dict[str, str]:
    merged = dict(existing)
    for key, value in fresh.items():
        if only_missing and merged.get(key):
            continue
        merged[key] = value
    return remove_stale_fields(merged, entry_type, fresh)


def format_entry(entry_type: str, key: str, fields: dict[str, str]) -> str:
    ordered_names = [name for name in FIELD_ORDER if name in fields]
    extra_names = sorted(name for name in fields if name not in FIELD_ORDER)
    names = ordered_names + extra_names
    lines = [f"@{entry_type}{{{key},"]
    for index, name in enumerate(names):
        comma = "," if index < len(names) - 1 else ""
        lines.append(f"  {name:<13} = {brace(fields[name])}{comma}")
    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Update BibTeX metadata from DOI using Crossref.")
    parser.add_argument("--dry-run", action="store_true", help="Print updates without writing references.bib.")
    parser.add_argument("--only-missing", action="store_true", help="Only fill empty fields; do not overwrite existing metadata.")
    parser.add_argument("--sleep", type=float, default=0.2, help="Delay between Crossref requests.")
    args = parser.parse_args()

    text = BIB_PATH.read_text(encoding="utf-8")
    prefix, raw_entries = split_entries(text)
    updated_entries = []
    updated_count = 0

    for raw_entry in raw_entries:
        entry = parse_entry(raw_entry)
        if entry is None:
            updated_entries.append(raw_entry)
            continue

        doi = entry.fields.get("doi")
        if not doi:
            updated_entries.append(raw_entry)
            continue

        work = fetch_crossref_work(doi)
        if not work:
            updated_entries.append(raw_entry)
            continue

        entry_type = crossref_entry_type(work, entry.entry_type)
        fresh_fields = crossref_fields(work, entry.fields)
        merged_fields = merge_fields(entry.fields, fresh_fields, args.only_missing, entry_type)
        formatted_entry = format_entry(entry_type, entry.key, merged_fields)
        updated_entries.append(formatted_entry if not args.dry_run else raw_entry)
        updated_count += 1
        title = fresh_fields.get("title", entry.fields.get("title", ""))
        print(f"UPDATED {entry.key}: @{entry.entry_type} -> @{entry_type} :: {doi} :: {title}")
        time.sleep(args.sleep)

    if not args.dry_run:
        parts = []
        if prefix:
            parts.append(prefix)
        parts.extend(updated_entries)
        BIB_PATH.write_text("\n\n".join(parts).rstrip() + "\n", encoding="utf-8")

    print(f"Done. References updated from DOI: {updated_count}")


if __name__ == "__main__":
    main()
