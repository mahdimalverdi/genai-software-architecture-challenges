#!/usr/bin/env bash
set -euo pipefail

mkdir -p build/pdf
cd build/latex

if command -v latexmk >/dev/null 2>&1; then
  latexmk -xelatex -interaction=nonstopmode report.tex
else
  xelatex -interaction=nonstopmode report.tex
fi

cp report.pdf ../pdf/report.pdf
