from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
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
CROSSREF_WORKS_URL = "https://api.crossref.org/works"

ENTRY_START = re.compile(r"^@(\w+)\s*\{\s*([^,]+),")
FIELD_LINE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_-]*)\s*=\s*([{\"])(.*?)([}\"]),?\s*$")


@dataclass
class BibEntry:
    raw: str
    entry_type: str
    key: str
    fields: dict[str, str]


def normalize_title(title: str) -> str:
    title = title.lower()
    title = re.sub(r"[^a-z0-9]+", " ", title)
    return " ".join(title.split())


def similarity(left: str, right: str) -> float:
    return SequenceMatcher(None, normalize_title(left), normalize_title(right)).ratio()


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


def parse_entry(entry: str) -> BibEntry:
    lines = entry.splitlines()
    match = ENTRY_START.match(lines[0])
    if not match:
        return BibEntry(raw=entry, entry_type="unknown", key="unknown", fields={})

    fields = {}
    for line in lines[1:-1]:
        match = FIELD_LINE.match(line)
        if match:
            fields[match.group(1)] = match.group(3).strip()

    return BibEntry(raw=entry, entry_type=match.group(1), key=match.group(2).strip(), fields=fields)


def request_json(url: str, timeout_seconds: int = 20) -> dict:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "genai-software-architecture-challenges/1.0 (mailto:example@example.com)"},
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def query_crossref(title: str, author: str | None, limit: int) -> list[dict]:
    params = {
        "query.title": title,
        "rows": str(limit),
        "select": "DOI,title,author,issued,URL,type,container-title",
    }
    if author:
        params["query.author"] = author
    url = CROSSREF_WORKS_URL + "?" + urllib.parse.urlencode(params)
    data = request_json(url)
    return data.get("message", {}).get("items", [])


def first_author_name(author_field: str | None) -> str | None:
    if not author_field:
        return None
    first_author = author_field.split(" and ")[0]
    first_author = first_author.replace("{", "").replace("}", "")
    parts = [part.strip() for part in first_author.split(",")]
    if len(parts) > 1:
        return parts[0]
    return first_author.split()[-1] if first_author.split() else None


def find_best_doi(entry: BibEntry, min_score: float, limit: int) -> tuple[str | None, float, str | None]:
    title = entry.fields.get("title")
    if not title:
        return None, 0.0, None

    author = first_author_name(entry.fields.get("author"))
    try:
        items = query_crossref(title, author, limit)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        print(f"WARN {entry.key}: Crossref lookup failed: {error}")
        return None, 0.0, None

    best_doi = None
    best_score = 0.0
    best_title = None
    for item in items:
        titles = item.get("title") or []
        candidate_title = titles[0] if titles else ""
        score = similarity(title, candidate_title)
        if score > best_score:
            best_score = score
            best_doi = item.get("DOI")
            best_title = candidate_title

    if best_doi and best_score >= min_score:
        return best_doi, best_score, best_title
    return None, best_score, best_title


def add_or_update_doi(raw_entry: str, doi: str) -> str:
    lines = raw_entry.splitlines()
    for index, line in enumerate(lines):
        if line.strip().lower().startswith("doi") and "=" in line:
            trailing_comma = "," if line.rstrip().endswith(",") else ""
            lines[index] = f"  doi           = {{{doi}}}{trailing_comma}"
            return "\n".join(lines)

    insert_at = len(lines) - 1
    preferred_previous_fields = ["year", "pages", "number", "volume"]
    for field in preferred_previous_fields:
        for index, line in enumerate(lines):
            if line.strip().lower().startswith(field.lower()) and "=" in line:
                insert_at = index + 1
                break
        if insert_at != len(lines) - 1:
            break

    if insert_at > 0 and not lines[insert_at - 1].rstrip().endswith(","):
        lines[insert_at - 1] = lines[insert_at - 1].rstrip() + ","

    lines.insert(insert_at, f"  doi           = {{{doi}}},")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Find missing DOI values for BibTeX entries using Crossref.")
    parser.add_argument("--dry-run", action="store_true", help="Only print matches without changing references.bib.")
    parser.add_argument("--min-score", type=float, default=0.92, help="Minimum title similarity score for accepting a DOI.")
    parser.add_argument("--limit", type=int, default=5, help="Maximum Crossref candidates per entry.")
    parser.add_argument("--sleep", type=float, default=0.2, help="Delay between Crossref requests.")
    args = parser.parse_args()

    text = BIB_PATH.read_text(encoding="utf-8")
    prefix, raw_entries = split_entries(text)
    updated_entries = []
    changed_count = 0

    for raw_entry in raw_entries:
        entry = parse_entry(raw_entry)
        if entry.fields.get("doi"):
            updated_entries.append(raw_entry)
            continue

        doi, score, matched_title = find_best_doi(entry, args.min_score, args.limit)
        if doi:
            changed_count += 1
            print(f"FOUND {entry.key}: {doi} score={score:.3f}")
            if matched_title:
                print(f"  matched: {matched_title}")
            updated_entries.append(add_or_update_doi(raw_entry, doi) if not args.dry_run else raw_entry)
        else:
            print(f"MISS  {entry.key}: best_score={score:.3f}")
            if matched_title:
                print(f"  best: {matched_title}")
            updated_entries.append(raw_entry)

        time.sleep(args.sleep)

    if not args.dry_run and changed_count:
        parts = []
        if prefix:
            parts.append(prefix)
        parts.extend(updated_entries)
        BIB_PATH.write_text("\n\n".join(parts).rstrip() + "\n", encoding="utf-8")

    print(f"Done. DOI values found: {changed_count}")


if __name__ == "__main__":
    main()
