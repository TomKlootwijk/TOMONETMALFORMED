from pathlib import Path
root=Path('C:/TOMONETMALFORMED/output/pdf')
src=root/'frontier_applications_source'
dst=root/'a18_wave_material_source'
code=(src/'build_pdf.py').read_text(encoding='utf-8')
code=code.replace('Perpetuum_Mobile_Frontier_Applications_A1_0.pdf','A18_Wave_Material_Computer_Definition_Enhanced_R1_0.pdf')
code=code.replace('Build the application companion from its editable page JSON.','Build the focused A18 technical supplement from editable page JSON.')
start=code.index("    if page.get('cover'):")
end=code.index("    for block in page['blocks']:",start)
code=code[:start]+'''    if page.get('cover'):
        cover_style = ParagraphStyle('cover', parent=styles['title'], fontSize=35, leading=38, spaceAfter=15)
        items.extend([P('PERPETUUM MOBILE / A18 / R1.0', 'label'), Spacer(1, 12),
                      Paragraph('WAVE-AND-MATERIAL<br/>COMPUTER', cover_style),
                      P('Definition and enhanced architecture', 'subtitle')])
    else:
        items.extend([P(page['label'], 'label'), P(html.escape(page['title']), 'title')])
'''+code[end:]
at=code.index('def page_items(page):')
diagram='''class Architecture(Flowable):
    """Native vector drawing: wave path, retained settings and feedback."""
    def __init__(self):
        super().__init__()
        self.width = WIDTH
        self.height = 143
    def draw(self):
        c = self.canv
        gap = 9
        bw = (WIDTH-4*gap)/5
        labels = [('INPUT x','four channels'),('ENCODE','field a'),('OPTICAL CORE','transfer S'),('I/Q READ','field b'),('OUTPUT y','scaled result')]
        for i,(title,sub) in enumerate(labels):
            x=i*(bw+gap)
            c.setFillColor(NAVY if i<3 else TEAL)
            c.roundRect(x,88,bw,38,3,fill=1,stroke=0)
            c.setFillColor(white); c.setFont('Bold',8)
            c.drawCentredString(x+bw/2,111,title)
            c.setFont('Body',8); c.drawCentredString(x+bw/2,98,sub)
            if i<4:
                c.setStrokeColor(TEAL); c.line(x+bw+1,107,x+bw+gap-1,107)
        c.setFillColor(PALE); c.setStrokeColor(LINE)
        c.roundRect(119,40,WIDTH-238,29,3,fill=1,stroke=1)
        c.setFillColor(NAVY); c.setFont('Bold',8.7)
        c.drawCentredString(WIDTH/2,51,'MATERIAL g / retained settings')
        c.setStrokeColor(TEAL); c.line(WIDTH/2,69,WIDTH/2,86)
        c.setFillColor(MUTED); c.setFont('Body',8.5)
        c.drawCentredString(WIDTH/2,14,'DIGITAL CONTROL / program, measure, qualify, monitor')
        c.setStrokeColor(LINE); c.line(28,31,WIDTH-28,31)

'''
code=code[:at]+diagram+code[at:]
code=code.replace("        elif kind == 'pipeline':", "        elif kind == 'architecture':\n            items.append(Architecture())\n        elif kind == 'pipeline':")
code=code.replace('FRONTIER APPLICATIONS / A1.0','A18 / DEFINITION + ENHANCEMENT / R1.0')
code=code.replace('# Perpetuum Mobile / Frontier Applications','# A18 / Wave-and-material computer')
code=code.replace('A1.0 / 15 September 2026','R1.0 / 15 September 2026')
code=code.replace("'Frontier_Applications_A1_0.md'","'A18_Definition_Enhanced_R1_0.md'")
code=code.replace("            elif b['type'] == 'pipeline':", "            elif b['type'] == 'architecture':\n                md.append('Input -> encode -> optical core -> coherent I/Q readout -> output. Material retains core settings; digital control programs and verifies them.\\n')\n            elif b['type'] == 'pipeline':")
start=code.index("    manifest = json.loads((ROOT / 'source_manifest.json')")
end=code.index('    attachment_manifest = []',start)
code=code[:start]+'''    manifest = json.loads((ROOT / 'source_manifest.json').read_text(encoding='utf-8'))
    base = ROOT / manifest['companion']['relative_path']
    if not base.exists():
        base = ROOT / manifest['companion']['filename']
    if hashlib.sha256(base.read_bytes()).hexdigest() != manifest['companion']['sha256']:
        raise ValueError('Companion source hash mismatch')
    result = json.loads((ROOT / 'reference_results.json').read_text(encoding='utf-8'))
    if hashlib.sha256((ROOT / 'reference_model.py').read_bytes()).hexdigest() != result['provenance']['script_sha256']:
        raise ValueError('Numerical model receipt does not match its script')
    md = markdown(pages)
    (ROOT / 'layout_report.json').write_text(json.dumps(layout, indent=2), encoding='utf-8')
    filenames = ['content.json','source_manifest.json','references.json','write_content.py',
                 'prepare_sources.py','numeric_summary.json','reference_model.py','reference_results.json',
                 'build_pdf.py','verify_pdf.py','README.md','layout_report.json']
    attachments = [base, md] + [ROOT / name for name in filenames]
'''+code[end:]
code=code.replace('Perpetuum Mobile | Frontier Applications A1.0','A18 | Wave-and-material computer | R1.0')
code=code.replace('Codex-assisted application expansion','Codex-assisted A18 definition and enhancement')
code=code.replace('18 proposed analog, digital and physical applications with models and experiments','Coherent wave processing, retained material settings, calibrated operation and synthetic reference model')
code=code.replace('futuristic applications','A18, retained photonic computation')
(dst/'build_pdf.py').write_text(code,encoding='utf-8')

verify=(src/'verify_pdf.py').read_text(encoding='utf-8')
verify=verify.replace('Perpetuum_Mobile_Frontier_Applications_A1_0.pdf','A18_Wave_Material_Computer_Definition_Enhanced_R1_0.pdf')
start=verify.index('    apps = []')
end=verify.index('    reader = PdfReader(PDF)',start)
verify=verify[:start]+'''    refs = {r['id'] for r in json.loads((ROOT / 'references.json').read_text(encoding='utf-8'))}
    cited = set()
    for page in pages:
        text = json.dumps(page)
        for group in re.findall(r'\\[(R\\d+(?:,\\s*R\\d+)*)\\]',text):
            cited.update(x.strip() for x in group.split(','))
    assert cited <= refs, cited - refs
'''+verify[end:]
start=verify.index("    base_bytes = reader.attachments[")
end=verify.index('    receipt = {',start)
verify=verify[:start]+'''    base_bytes = reader.attachments[sources['companion']['filename']][0]
    assert hashlib.sha256(base_bytes).hexdigest() == sources['companion']['sha256']
    companion = PdfReader(io.BytesIO(base_bytes))
    assert len(companion.pages) == 56 and len(companion.attachments) == 18
    pm_bytes = companion.attachments['Perpetuum_Mobile_Tom_Klootwijk_V1_0.pdf'][0]
    assert hashlib.sha256(pm_bytes).hexdigest() == sources['normative_pm']['sha256']
    pm = PdfReader(io.BytesIO(pm_bytes))
    assert len(pm.pages) == 38 and len(pm.attachments) == 20
    result = json.loads(reader.attachments['reference_results.json'][0])
    assert result['status'] == 'passed'
    assert result['provenance']['script_sha256'] == hashlib.sha256(reader.attachments['reference_model.py'][0]).hexdigest()
    assert result['provenance']['pm_content_json_sha256'] == hashlib.sha256(pm.attachments['content.json'][0]).hexdigest()
    numeric = json.loads(reader.attachments['numeric_summary.json'][0])
    assert numeric['source_receipt_sha256'] == hashlib.sha256(reader.attachments['reference_results.json'][0]).hexdigest()
'''+verify[end:]
verify=verify.replace("'edition': 'Frontier Applications A1.0'", "'edition': 'A18 Definition and Enhanced Architecture R1.0'")
verify=verify.replace("'applications': 18,", "'application': 'A18',")
verify=verify.replace("'base_pdf_pages': 38, 'base_pdf_nested_attachments': 20,", "'companion_pages': 56, 'normative_pm_pages': 38, 'synthetic_model_checks': result['checks_passed'],")
(dst/'verify_pdf.py').write_text(verify,encoding='utf-8')
print('A18 builders created.')
