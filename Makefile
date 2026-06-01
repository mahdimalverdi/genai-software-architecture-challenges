SHELL := /bin/bash

.PHONY: tex pdf clean fix-references check-references

tex:
	python3 scripts/build_tex.py

pdf: tex
	bash scripts/build_pdf.sh

clean:
	python3 scripts/clean.py

fix-references:
	python3 scripts/fix_references.py

check-references:
	python3 scripts/check_references.py
