SHELL := /bin/bash

.PHONY: tex pdf clean fix-references check-references verify-references fill-dois refresh-references repair-reference-keys

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

verify-references:
	python3 scripts/verify_references.py

fill-dois:
	python3 scripts/fill_dois.py

refresh-references:
	python3 scripts/update_references_from_doi.py

repair-reference-keys:
	python3 scripts/repair_reference_keys.py
