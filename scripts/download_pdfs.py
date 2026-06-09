#!/usr/bin/env python3
"""Download freely available arXiv PDFs from references/references.bib."""

from __future__ import annotations

import re
import time
from pathlib import Path
from urllib.parse import quote

import requests

BIB_PATH = Path("references/references.bib")
OUT_DIR = Path("references/pdfs")
TIMEOUT_SECONDS = 30
DELAY_SECONDS = 1.0


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return