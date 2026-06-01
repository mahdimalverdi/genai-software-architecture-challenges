SHELL := /bin/bash

.PHONY: tex pdf clean

tex:
	python3 scripts/build_tex.py

pdf: tex
	bash scripts/build_pdf.sh

clean:
	bash scripts/clean.sh
