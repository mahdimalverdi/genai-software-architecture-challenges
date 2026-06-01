from __future__ import annotations

from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BIB_PATH = ROOT / "references" / "references.bib"

ENTRY_START = re.compile(r"^@(\w+)\s*\{\s*([^,]+),")
FIELD_LINE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_-]*)\s*=\s*[{\"](.+?)[}\"],?\s*$")
ARXIV_API_URL = "https://export.arxiv.org/api/query?id_list="
CROSSREF_API_URL = "https://api.crossref.org/works/"


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


def parse_entry(entry: str) -> tuple[str, str, dict[str, str]]:
    lines = entry.splitlines()
    match = ENTRY_START.match(lines[0])
    if not match:
        return "unknown", "unknown", {}

    entry_type = match.group(1).lower()
    key = match.group(2).strip()
    fields = {}

    for line in lines[1:-1]:
        match = FIELD_LINE.match(line)
        if match:
            fields[match.group(1)] = match.group(2).strip()

    return entry_type, key, fields


def request_url(url: str, timeout_seconds: int = 15) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "genai-software-architecture-challenges/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        return response.read().decode("utf-8", errors="replace")


def verify_arxiv(entry_key: str, fields: dict[str, str]) -> list[str]:
    eprint = fields.get("eprint")
    if not eprint:
        return []

    errors = []
    try:
        body = request_url(ARXIV_API_URL + urllib.parse.quote(eprint))
        root = ET.fromstring(body)
        namespace = {"atom": "http://www.w3.org/2005/Atom"}
        entries = root.findall("atom:entry", namespace)
        if not entries:
            errors.append(f"{entry_key}: arXiv id not found: {eprint}")
            return errors

        arxiv_title = " ".join(entries[0].findtext("atom:title", default="", namespaces=namespace).split())
        local_title = " ".join(fields.get("title", "").split())
        if local_title and arxiv_title and local_title.lower() != arxiv_title.lower():
            errors.append(f"{entry_key}: arXiv title differs from local title")
    except (urllib.error.URLError, TimeoutError, ET.ParseError) as error:
        errors.append(f"{entry_key}: could not verify arXiv id {eprint}: {error}")

    return errors


def verify_doi(entry_key: str, fields: dict[str, str]) -> list[str]:
    doi = fields.get("doi")
    if not doi:
        return []

    errors = []
    url = CROSSREF_API_URL + urllib.parse.quote(doi, safe="")
    try:
        request_url(url)
    except urllib.error.HTTPError as error:
        errors.append(f"{entry_key}: DOI lookup failed for {doi}: HTTP {error.code}")
    except (urllib.error.URLError, TimeoutError) as error:
        errors.append(f"{entry_key}: could not verify DOI {doi}: {error}")

    return errors


def main() -> None:
    entries = split_entries(BIB_PATH.read_text(encoding="utf-8"))
    errors = []
    verified_count = 0

    for entry in entries:
        _, key, fields = parse_entry(entry)
        entry_errors = []
        entry_errors.extend(verify_arxiv(key, fields))
        entry_errors.extend(verify_doi(key, fields))
        errors.extend(entry_errors)
        if fields.get("eprint") or fields.get("doi"):
            verified_count += 1

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)

    print(f"OK: verified {verified_count} references through arXiv and/or Crossref.")


if __name__ == "__main__":
    main()
