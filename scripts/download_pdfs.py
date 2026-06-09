#!/usr/bin/env python3
from pathlib import Path
import time
import requests

bib_path = Path('references/references.bib')
out_dir = Path('references/pdfs')
out_dir.mkdir(parents=True, exist_ok=True)

current_key = None
seen = 0
saved = 0

for line in bib_path.read_text(encoding='utf-8').splitlines():
    stripped = line.strip()

    if stripped.startswith('@'):
        marker = stripped.split(',', 1)[0]
        current_key = marker.split