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

ENTRY_START = re.compile(r"^@(?P<type>[A-Za-z]+)\s*\{\s*(?P<key>[^,]+)\s*,")
FIELD_LINE = re.compile(r"^\s*(?P<name>[A-Za-z][A-Za-z0-9_-]*)\s*=\s*(?P<value>.+?)(?P<comma>,?)\s*$")

FIELD_ORDER = [
    "author",
    "title",
    "publisher",
    "year",
    "isbn",
    "url",
    "note",
]

TODO_NOTE_PREFIX = "اطلاعات نویسنده، ناشر، شابک و نشانی رسمی"


@dataclass
class BibEntry:
    entry_type: str
    key: str
    fields: dict[str, str]
    raw: str


def clean_value(value: str) -> str:
    value = value.strip().rstrip(",").strip()
    if len(value) >= 2 and value[0] in "{\"" and value[-1] in "}\"":
        return value[1:-1].strip()
    return value


def brace(value: str) -> str:
    return "{" + " ".join(value.split()) + "}"


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def title_score(left: str, right: str) -> float:
    return SequenceMatcher(None, normalize(left), normalize(right)).ratio()


def request_json(url: str, timeout_seconds: int = 20) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "genai-software-architecture-challenges/1.0"})
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


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


def parse_entry(raw: str) -> BibEntry | None:
    lines = raw.splitlines()
    if not lines:
        return None
    entry_match = ENTRY_START.match(lines[0])
    if not entry_match:
        return None
    fields = {}
    for line in lines[1:-1]:
        field_match = FIELD_LINE.match(line)
        if field_match:
            fields[field_match.group("name")] = clean_value(field_match.group("value"))
    return BibEntry(entry_match.group("type"), entry_match.group("key").strip(), fields, raw)


def format_entry(entry: BibEntry) -> str:
    names = [name for name in FIELD_ORDER if name in entry.fields]
    names.extend(sorted(name for name in entry.fields if name not in FIELD_ORDER))
    lines = [f"@{entry.entry_type}{{{entry.key},"]
    for index, name in enumerate(names):
        comma = "," if index < len(names) - 1 else ""
        lines.append(f"  {name:<9} = {brace(entry.fields[name])}{comma}")
    lines.append("}")
    return "\n".join(lines)


def isbn_from_identifiers(identifiers: list[dict]) -> str | None:
    for identifier in identifiers:
        if identifier.get("type") in {"ISBN_13", "ISBN_10"}:
            return identifier.get("identifier")
    return None


def google_books_candidates(title: str) -> list[dict[str, str]]:
    query = urllib.parse.quote(f'intitle:"{title}"')
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=5"
    candidates = []
    try:
        items = request_json(url).get("items", [])
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        print(f"WARN: Google Books lookup failed for {title}: {error}")
        return candidates
    for item in items:
        info = item.get("volumeInfo", {})
        candidate = {
            "source": "google-books",
            "title": info.get("title", ""),
            "author": " and ".join(info.get("authors", [])),
            "publisher": info.get("publisher", ""),
            "year": (info.get("publishedDate", "") or "")[:4],
            "isbn": isbn_from_identifiers(info.get("industryIdentifiers", [])) or "",
            "url": info.get("canonicalVolumeLink") or info.get("infoLink") or "",
        }
        candidates.append(candidate)
    return candidates


def open_library_candidates(title: str) -> list[dict[str, str]]:
    url = "https://openlibrary.org/search.json?" + urllib.parse.urlencode({"title": title, "limit": "5"})
    candidates = []
    try:
        docs = request_json(url).get("docs", [])
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        print(f"WARN: Open Library lookup failed for {title}: {error}")
        return candidates
    for doc in docs:
        isbn_values = doc.get("isbn") or []
        candidates.append(
            {
                "source": "open-library",
                "title": doc.get("title", ""),
                "author": " and ".join(doc.get("author_name") or []),
                "publisher": (doc.get("publisher") or [""])[0],
                "year": str(doc.get("first_publish_year") or ""),
                "isbn": isbn_values[0] if isbn_values else "",
                "url": "https://openlibrary.org" + doc.get("key", "") if doc.get("key") else "",
            }
        )
    return candidates


def score_candidate(entry_title: str, entry_year: str | None, candidate: dict[str, str]) -> float:
    score = title_score(entry_title, candidate.get("title", ""))
    if entry_year and candidate.get("year") == entry_year:
        score += 0.05
    if candidate.get("author"):
        score += 0.02
    if candidate.get("publisher"):
        score += 0.02
    if candidate.get("isbn"):
        score += 0.03
    return min(score, 1.0)


def best_candidate(title: str, year: str | None, min_score: float) -> tuple[dict[str, str] | None, float]:
    candidates = google_books_candidates(title) + open_library_candidates(title)
    best = None
    best_score = 0.0
    for candidate in candidates:
        score = score_candidate(title, year, candidate)
        if score > best_score:
            best = candidate
            best_score = score
    if best and best_score >= min_score:
        return best, best_score
    return None, best_score


def update_entry(entry: BibEntry, candidate: dict[str, str], only_missing: bool, remove_todo_note: bool) -> BibEntry:
    fields = dict(entry.fields)
    for name in ["title", "author", "publisher", "year", "isbn", "url"]:
        value = candidate.get(name)
        if not value:
            continue
        if only_missing and fields.get(name):
            continue
        fields[name] = value
    if remove_todo_note and fields.get("note", "").startswith(TODO_NOTE_PREFIX):
        fields.pop("note", None)
    return BibEntry("book", entry.key, fields, entry.raw)


def add_missing_title(entries: list[BibEntry], key: str, title: str, year: str | None) -> list[BibEntry]:
    if any(normalize(entry.fields.get("title", "")) == normalize(title) for entry in entries):
        return entries
    fields = {"title": title}
    if year:
        fields["year"] = year
    fields["note"] = "اطلاعات نویسنده، ناشر، شابک و نشانی رسمی باید پیش از نسخه‌ی نهایی گزارش تکمیل و بازبینی شود."
    entries.append(BibEntry("book", key, fields, ""))
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description="Complete BibTeX book metadata using Google Books and Open Library.")
    parser.add_argument("--title", help="Add this book title if it is not already present.")
    parser.add_argument("--key", default="engineeringAiSystems2025", help="BibTeX key for --title when adding a new book.")
    parser.add_argument("--year", help="Expected publication year for --title.")
    parser.add_argument("--dry-run", action="store_true", help="Print matches without writing references.bib.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing book fields with fetched metadata.")
    parser.add_argument("--remove-todo-note", action="store_true", help="Remove placeholder note when metadata is found.")
    parser.add_argument("--min-score", type=float, default=0.86, help="Minimum match score for accepting metadata.")
    parser.add_argument("--sleep", type=float, default=0.2, help="Delay between book lookups.")
    args = parser.parse_args()

    prefix, raw_entries = split_entries(BIB_PATH.read_text(encoding="utf-8"))
    entries = [entry for raw in raw_entries if (entry := parse_entry(raw)) is not None]

    if args.title:
        entries = add_missing_title(entries, args.key, args.title, args.year)

    updated = []
    update_count = 0
    for entry in entries:
        if entry.entry_type.lower() != "book":
            updated.append(entry)
            continue
        title = entry.fields.get("title")
        if not title:
            updated.append(entry)
            continue
        candidate, score = best_candidate(title, entry.fields.get("year"), args.min_score)
        if not candidate:
            print(f"MISS  {entry.key}: {title} best_score={score:.3f}")
            updated.append(entry)
            continue
        print(f"FOUND {entry.key}: {candidate.get('title')} source={candidate.get('source')} score={score:.3f}")
        updated.append(update_entry(entry, candidate, not args.overwrite, args.remove_todo_note))
        update_count += 1
        time.sleep(args.sleep)

    if not args.dry_run:
        parts = []
        if prefix:
            parts.append(prefix)
        parts.extend(format_entry(entry) for entry in updated)
        BIB_PATH.write_text("\n\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Done. Book references updated: {update_count}")


if __name__ == "__main__":
    main()
