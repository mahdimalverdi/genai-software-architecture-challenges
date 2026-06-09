#!/usr/bin/env python3
import re,time
from pathlib import Path
import requests
bib=Path('references/references.bib').read_text()
out=Path('references/pdfs');out.mkdir(parents=True,exist_ok=True)
for k,b in re.findall(r'@(\w+)\{([^,]+),(.+?)(?=\n@|\Z)',bib,re.S):
    m=re.search(r'eprint\s*=\s*[{\"]([^}\"]+)',b)
    if not m: continue
    eid=m.group(1).strip()
    p=out/f'{k}-{eid}.pdf'
    if p.exists(): continue
    r=requests.get(f'https://arxiv.org/pdf/{eid