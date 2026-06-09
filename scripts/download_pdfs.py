#!/usr/bin/env python3
import re
import time
from pathlib import Path

import requests

bib = Path('references/references.bib').read_text(encoding='utf-8')
out = Path('references/pdfs')
out.mkdir(parents=True, exist_ok=True)

entries = re.findall(r'@\w+\s*\{([^,]+),(.+?)(?=\n@|\Z)', bib, re.S)

for key, body in entries:
    match = re.search(r'eprint\s*=\s*[\{\"]([^\}\