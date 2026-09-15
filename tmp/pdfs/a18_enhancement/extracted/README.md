# A18 / Wave-and-material computer

Technical definition and enhanced architecture, R1.0.

Framework attribution: Tom Klootwijk / NL200678942.

Prepared with Codex assistance from Perpetuum Mobile PM 1.0 and Frontier Applications A1.0. This supplement develops the A18 research proposal; its numerical example checks a synthetic mathematical model, not application hardware.

## What is defined and enhanced

- Four coherent input channels and four output channels, with explicit complex amplitudes, numerical scaling and I/Q readout.
- A bounded H4 plus retained row-weight core, with a general passive matrix decomposition as an extension.
- Separate retained configuration, physical writing and dynamic signal-memory models.
- Measured configuration admission, drift invalidation, restricted calibration corrections and bounded decoder gain.
- Write-aware scheduling, optional fine trim, spare-path and two-bank proposals.
- Complete energy accounting, a physical experiment plan and cross-domain application directions.

All hardware proposals require device-specific characterization. Published component results are distinguished from this A18 integration. In particular, the 2026 BTO paper demonstrates retained individual cells while its complex mesh demonstrations used volatile control.

## Numerical example

`reference_model.py` uses explicit finite inputs, synthetic loss/phase/drift/noise and NumPy linear algebra. It preserves the exact normalized PM H4 and pinion operators. It produces dimensionless numerical outputs from coherent fields in sqrt(W), checks restricted row corrections and rejects unsupported calibration cases. The recorded `reference_results.json` identifies its runtime and verified source hashes. Its 44 checks are mathematics/software evidence only.

The model does not implement a fabricated photonic circuit, generic inverse tuning, a measured material law or an application benchmark. Its illustrated material attenuation curve and energy inputs are chosen surrogates. Exact numerical inputs are listed; no RNG or replacement for PPM-SEED-v1 is introduced.

## Rebuild the recorded PDF

Use Windows Python with `reportlab`, `pypdf`, `pdfplumber`, `numpy`, and the installed Calibri/Consolas fonts. The delivered numerical run used bundled Python 3.12.14 / NumPy 2.3.5. From this directory:

```powershell
python prepare_sources.py
python write_content.py
python build_pdf.py
python verify_pdf.py
```

The builder writes `../A18_Wave_Material_Computer_Definition_Enhanced_R1_0.pdf`. Keep the prior companion PDF in the parent directory. For an extracted attachment package, the builder and preparation script also find it beside themselves. The companion's expected hash is enforced.

The rebuild uses the already recorded model receipt. To independently rerun the numerical model without changing that receipt:

```powershell
python reference_model.py --pm-content pm_content.json --out new_reference_results.json
```

Compare numerical values with the tolerances declared in the model; execution time, runtime and path fields can differ. To publish a new recorded numerical run, replace the receipt intentionally, then regenerate the summary, content and PDF. Never copy a script hash into an old result to make mismatched artifacts appear consistent.

## Source and evidence inventory

- `write_content.py`, `content.json`, `A18_Definition_Enhanced_R1_0.md`: editable document sources.
- `references.json`: seven primary research records and evidence boundaries.
- `source_manifest.json`, `pm_content.json`: exact source identity and PM numeric/page witness.
- `reference_model.py`, `reference_results.json`, `numeric_summary.json`: executable synthetic example, full receipt and displayed table data.
- `prepare_sources.py`, `build_pdf.py`, `verify_pdf.py`: preparation, PDF layout, text and attachment verification.
- `layout_report.json`, `attachment_manifest.json`: intended page geometry and exact embedded-byte hashes.
- `verification_receipt.json`: external verification record, including final PDF hash. It is outside the PDF to avoid a circular hash.

The PDF embeds these sources and the unchanged 56-page Frontier Applications A1.0 PDF. The companion itself embeds the 38-page PM 1.0 specification and its nested four-source package. Third-party research papers are linked, not republished in this new supplement.

Render the delivered PDF using Poppler and visually inspect every page. Native vector diagrams provide architecture views; no custom bitmap image is needed. Document and hash checks do not validate hardware or establish scientific novelty.
