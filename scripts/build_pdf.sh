#!/usr/bin/env bash
set -euo pipefail

mkdir -p build/pdf

if [[ ! -f build/latex/report.tex ]]; then
  echo "Missing build/latex/report.tex. Run: make tex" >&2
  exit 1
fi

if ! command -v xelatex >/dev/null 2>&1; then
  echo "Missing xelatex. Run: make pdf-deps" >&2
  exit 1
fi

cd build/latex

xelatex -interaction=nonstopmode -halt-on-error report.tex

if [[ -f report.aux ]] && grep -q "\\bibdata" report.aux; then
  if command -v bibtex >/dev/null 2>&1; then
    bibtex report || true
  else
    echo "Missing bibtex. Run: make pdf-deps" >&2
    exit 1
  fi
fi

xelatex -interaction=nonstopmode -halt-on-error report.tex
xelatex -interaction=nonstopmode -halt-on-error report.tex

cp report.pdf ../pdf/report.pdf
