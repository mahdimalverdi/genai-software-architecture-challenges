SHELL := /bin/bash

.PHONY: tex pdf clean pdf-deps pdf-clean pdf-build fix-references check-references verify-references fill-dois refresh-references refresh-books repair-reference-keys

tex:
	python3 scripts/build_tex.py

pdf: tex
	bash scripts/build_pdf.sh

pdf-deps:
	sudo apt update
	sudo apt install -y texlive-xetex texlive-lang-arabic texlive-bibtex-extra texlive-fonts-recommended texlive-latex-recommended texlive-latex-extra texlive-binaries fonts-hosny-amiri

pdf-clean:
	rm -rf build/latex build/pdf

pdf-build: pdf-clean pdf

clean:
	python3 scripts/clean.py

fix-references:
	python3 scripts/fix_references.py

check-references:
	python3 scripts/check_references.py

verify-references:
	python3 scripts/verify_references.py

fill-dois:
	python3 scripts/fill_dois.py

refresh-references:
	python3 scripts/update_references_from_doi.py

refresh-books:
	python3 scripts/update_books_metadata.py

repair-reference-keys:
	python3 scripts/repair_reference_keys.py
