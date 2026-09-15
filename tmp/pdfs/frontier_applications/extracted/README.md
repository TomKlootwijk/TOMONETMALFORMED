# Perpetuum Mobile / Frontier Applications A1.0

Framework attribution: **Tom Klootwijk / NL200678942**. Prepared with Codex assistance on 15 September 2026.

This companion preserves the preceding assistant reply and expands its 18 applications into proposals with operating mechanisms, conditional models, mappings to PM 1.0, demonstrators, comparison criteria, research gaps and future extensions. Primary research supports components only. No new application hardware or physical experiment is reported.

## Contents

- `apps_01_06.json`, `apps_07_12.json`, `apps_13_18.json`: editable application chapters.
- `original_reply.md`: exact conversation witness; its commit link is the historical PM 1.0 receipt.
- `reply_apps.json`: parsed application text for the printed appendix.
- `assemble_content.py`: assembles chapters, introduction, research plan, original reply and bibliography.
- `content.json`, `Frontier_Applications_A1_0.md`: page source and readable export.
- `references.json`: primary component sources, claims supported and evidence boundaries.
- `assets/frontier_cover.png`, `imagegen_prompt.md`: AI-generated concept image and generation provenance.
- `source_manifest.json`: known expected hashes for the base specification, original reply and cover.
- `build_pdf.py`: ReportLab layout and attachment packaging, with hard failure on page overflow.
- `verify_pdf.py`, `verification_receipt.json`: editorial, text, margin and attachment checks. The receipt is external to the PDF to avoid a self-referential PDF hash.
- `layout_report.json`: measured end position of every intended reading unit.
- `attachment_manifest.json`: exact size and SHA-256 for each embedded artifact except that manifest itself.

The companion embeds the unchanged 38-page `Perpetuum_Mobile_Tom_Klootwijk_V1_0.pdf`, which itself embeds the four original user PDFs and its earlier reference validation package. PM page citations refer to that exact edition.

## Rebuild

On Windows, use Python with `reportlab`, `pypdf`, `pdfplumber` and the installed Calibri/Consolas fonts:

```powershell
python assemble_content.py
python build_pdf.py
python verify_pdf.py
```

Run from this directory or pass absolute script paths. The PDF is written one directory above. Keep the base PM 1.0 PDF in that parent directory. To rebuild an extracted attachment package, put its files together beside the builder; the builder also finds the embedded base PDF and `frontier_cover.png` in that directory.

Render the resulting PDF with Poppler (`pdftoppm -r 100 -png <pdf> <prefix>`) and visually inspect every page. The repository delivery was checked with that render workflow. No rendering or editorial check is evidence that a proposed machine works.

The cover is illustrative concept art, not a photograph or engineering drawing. Process strips are native vector diagrams. Hashes support integrity comparison and are unsigned; they do not authenticate authorship or scientific conclusions.
