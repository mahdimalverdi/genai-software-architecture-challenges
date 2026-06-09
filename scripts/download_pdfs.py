#!/usr/bin/env python3
"""Download freely available PDFs for bibliography entries.

The script reads `references/references.bib`, finds entries with an arXiv
`eprint` field, and downloads the corresponding PDF from arXiv. It does not
bypass paywalls and only uses publicly available URLs.
"""

from __future__ import annotations

import argparse
import re
import time
from pathlib import Path
from urllib.parse import quote

import requests

DEFAULT_BIB_PATH = Path("references/references.bib")
DEFAULT_OUT_DIR = Path("references/pdfs")
DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_DELAY_SECONDS = 1.0


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")[: