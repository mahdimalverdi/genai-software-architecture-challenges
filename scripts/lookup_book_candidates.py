from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from difflib import SequenceMatcher

CROSSREF_WORKS_URL = "https://api.crossref.org/works"
OPEN_LIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def score(left: str, right: str) -> float:
    return SequenceMatcher(None, normalize(left), normalize(right)).ratio()


def request_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "genai-software-architecture-challenges/1.0"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def first_year(work: dict) -> str:
    for field in ["published-print", "published-online", "published", "issued"]:
        date_parts = work.get(field, {}).get("date-parts")
        if date_parts and date_parts[0]:
            return str(date_parts[0][0])
    return ""


def crossref_candidates(title: str, limit: int) -> list[dict[str, str]]:
    params = {
        "query.title": title,
        "rows": str(limit),
        "select": "DOI,title,author,publisher,issued,published,published-print,published-online,URL,type,ISBN",
    }
    url = CROSSREF_WORKS_URL + "?" + urllib.parse.urlencode(params)
    candidates = []
    try:
        items = request_json(url).get("message", {}).get("items", [])
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        print(f"WARN: Crossref lookup failed: {error}")
        return candidates

    for item in items:
        isbn_values = item.get("ISBN") or []
        candidates.append(
            {
                "source": "crossref",
                "title": (item.get("title") or [""])[0],
                "publisher": item.get("publisher", ""),
                "year": first_year(item),
                "isbn": isbn_values[0] if isbn_values else "",
                "doi": (item.get("DOI") or "").lower(),
                "url": item.get("URL", ""),
                "type": item.get("type", ""),
            }
        )
    return candidates


def open_library_candidates(title: str, limit: int) -> list[dict[str, str]]:
    url = OPEN_LIBRARY_SEARCH_URL + "?" + urllib.parse.urlencode({"title": title, "limit": str(limit)})
    candidates = []
    try:
        docs = request_json(url).get("docs", [])
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        print(f"WARN: Open Library lookup failed: {error}")
        return candidates

    for doc in docs:
        isbn_values = doc.get("isbn") or []
        candidates.append(
            {
                "source": "open-library",
                "title": doc.get("title", ""),
                "publisher": (doc.get("publisher") or [""])[0],
                "year": str(doc.get("first_publish_year") or ""),
                "isbn": isbn_values[0] if isbn_values else "",
                "doi": "",
                "url": "https://openlibrary.org" + doc.get("key", "") if doc.get("key") else "",
                "type": "book",
            }
        )
    return candidates


def main() -> None:
    parser = argparse.ArgumentParser(description="Print book metadata candidates from public sources.")
    parser.add_argument("title", help="Book title to search")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    candidates = crossref_candidates(args.title, args.limit) + open_library_candidates(args.title, args.limit)
    candidates.sort(key=lambda item: score(args.title, item.get("title", "")), reverse=True)

    if not candidates:
        print("No candidates found.")
        return

    for item in candidates:
        print(f"score: {score(args.title, item.get('title', '')):.3f}")
        print(f"source: {item.get('source', '')}")
        print(f"title: {item.get('title', '')}")
        print(f"publisher: {item.get('publisher', '')}")
        print(f"year: {item.get('year', '')}")
        print(f"isbn: {item.get('isbn', '')}")
        print(f"doi: {item.get('doi', '')}")
        print(f"url: {item.get('url', '')}")
        print()


if __name__ == "__main__":
    main()
