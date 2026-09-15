# Perpetuum Mobile PM 1.0

This folder holds the editable PDF content and reproducible support checks.

## Rebuild

Requires Python with reportlab and pypdf, and Windows Calibri/Consolas fonts.
Keep all extracted attachments in one folder if rebuilding away from the original workspace. Source PDF hashes are checked. The supplied absolute source paths are used when available; otherwise the builder uses adjacent source PDFs with matching filenames.

1. Edit content.json directly, or edit write_content.py/write_seed_pages.py and run both writers in that order: write_seed_pages.py, then write_content.py.
2. Run python build_pdf.py. The PDF is written to the parent folder.
3. Render and visually inspect any edited PDF before delivery.

## Check support

- python seed_reference_v1.py writes seed_reference_v1_results.json.
- pwsh -File seed_reference_v1_crosscheck.ps1 reads that companion result and independently checks five frames/hashes.
- python formal_checks.py writes formal_checks_results.json.

These are local specification checks, not application-level or physical demonstrations. The reference seed manifest is deliberately a standalone fixture. Real application manifests must bind actual source/assets and a complete family schema.

The four original PDFs are embedded in the final PDF and remain unchanged. SHA-256 manifests provide unsigned integrity records.
