from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.parse
import urllib.request

GOOGLE_BOOKS_VOLUME_URL = "https://www.googleapis.com/books/v1/volumes/"


def extract_google_books_id(value: str) -> str:
    parsed = urllib.parse.urlparse(value)
    if parsed.query:
        query = urllib.parse.parse_qs(parsed.query)
        if query.get("id"):
            return query["id"][0]
    return value.strip()


def request_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "genai-software-architecture-challenges/1.0"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def format_authors(authors: list[str]) -> str:
    return " and ".join(authors)


def extract_identifiers(info: dict) -> dict[str, str]:
    identifiers = {}
    for item in info.get("industryIdentifiers", []) or []:
        item_type = item.get("type")
        identifier = item.get("identifier")
        if item_type and identifier:
            identifiers[item_type] = identifier
    return identifiers


def make_key(title: str, year: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", title)
    suffix = words[0].lower() + "".join(word.capitalize() for word in words[1:4]) if words else "book"
    return f"book{year}{suffix}"


def print_bibtex(volume_id: str, info: dict) -> None:
    title = info.get("title", "")
    authors = info.get("authors", []) or []
    publisher = info.get("publisher", "")
    year = (info.get("publishedDate", "") or "")[:4]
    identifiers = extract_identifiers(info)
    isbn = identifiers.get("ISBN_13") or identifiers.get("ISBN_10", "")
    url = f"https://books.google.com/books?id={volume_id}"
    key = make_key(title, year or "unknown")

    print(f"@book{{{key},")
    if authors:
        print(f"  author    = {{{format_authors(authors)}}},")
    if title:
        print(f"  title     = {{{title}}},")
    if publisher:
        print(f"  publisher = {{{publisher}}},")
    if year:
        print(f"  year      = {{{year}}},")
    if isbn:
        print(f"  isbn      = {{{isbn}}},")
    print(f"  url       = {{{url}}},")
    print(f"  note      = {{Google Books ID: {volume_id}. DOI برای این منبع در metadata عمومی Google Books ثبت نشده است.}}")
    print("}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Look up Google Books metadata by volume id or books.google.com URL.")
    parser.add_argument("value", help="Google Books volume id or books.google.com URL")
    args = parser.parse_args()

    volume_id = extract_google_books_id(args.value)
    data = request_json(GOOGLE_BOOKS_VOLUME_URL + urllib.parse.quote(volume_id))
    info = data.get("volumeInfo", {})

    print("metadata:")
    print(f"  id: {volume_id}")
    print(f"  title: {info.get('title', '')}")
    print(f"  authors: {', '.join(info.get('authors', []) or [])}")
    print(f"  publisher: {info.get('publisher', '')}")
    print(f"  publishedDate: {info.get('publishedDate', '')}")
    for key, value in extract_identifiers(info).items():
        print(f"  {key}: {value}")
    print()
    print_bibtex(volume_id, info)


if __name__ == "__main__":
    try:
        main()
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        raise SystemExit(f"Google Books lookup failed: {error}")
