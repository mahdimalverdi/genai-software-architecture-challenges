#!/usr/bin/env python3

import re
import time
from pathlib import Path

import requests

bib_path = Path("references/references.bib")
out_dir = Path("references/pdfs")
out_dir.mkdir(parents=True, exist_ok=True)

bib = bib_path.read_text(encoding="utf-8")
entries = re.findall(r"@\w+\s*\{([^,]+),(.+?)(?=\n@|\Z)", bib, re.S)

saved = 0
skipped = 0

for key, body in entries:
    match = re.search(r"eprint\s*=\s*[\{\"]([^\}\"]+)", body)
    if not match:
        skipped += 1
        continue

    eprint = match.group(1).strip()
    pdf_url = "https://arxiv.org/pdf/" + eprint
    pdf_path = out_dir / (key + "-" + eprint.replace("/", "-") + ".pdf")

    if pdf_path.exists() and pdf_path.stat().st_size > 0:
        print("skip:", pdf_path)
        continue

    print("download:", pdf_url)
    response = requests.get(pdf_url, timeout=30)

    if response.status_code != 200 or not response.content.startswith(b"%PDF"):
        print("failed:", key, response.status_code)
        continue

    pdf_path.write_bytes(response.content)
    saved += 1
    time.sleep(1)

print("saved:", saved)
print("skipped without arxiv eprint:", skipped)
