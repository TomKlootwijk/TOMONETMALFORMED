"""Verify document completeness and integrity, not proposed machine performance."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import io
import json
import re
import unicodedata
import pdfplumber
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
PDF = ROOT.parent / 'Perpetuum_Mobile_Frontier_Applications_A1_0.pdf'

class PlainText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, data):
        self.parts.append(data)

def plain(text):
    parser = PlainText()
    parser.feed(text)
    return ''.join(parser.parts)

def norm(text):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', text))

def main():
    pages = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
    apps = []
    for name in ('apps_01_06.json', 'apps_07_12.json', 'apps_13_18.json'):
        apps.extend(json.loads((ROOT / name).read_text(encoding='utf-8')))
    assert [a['id'] for a in apps] == list(range(1, 19))
    refs = {r['id'] for a in apps for r in a['references']}
    cited = set()
    for a in apps:
        for field in ('scenario', 'mechanism', 'source_roles', 'equation_context', 'demonstrator', 'failure', 'future', 'seed_role'):
            assert a[field].strip(), (a['id'], field)
            cited.update(re.findall(r'\[(A\d\dR\d+)\]', a[field]))
    assert cited <= refs, cited - refs
    original = json.loads((ROOT / 'reply_apps.json').read_text(encoding='utf-8'))
    title_norm = lambda s: norm(s).replace('“', '"').replace('”', '"')
    assert all(title_norm(a['title']) == title_norm(b['title']) for a, b in zip(apps, original))
    reader = PdfReader(PDF)
    assert len(reader.pages) == len(pages)
    assert len(reader.outline) == len(pages)
    text_checks = 0
    for i, (actual, expected) in enumerate(zip(reader.pages, pages), 1):
        extracted = norm(actual.extract_text())
        assert norm(f'{i:02d} / {len(pages):02d}') in extracted
        for block in expected['blocks']:
            if block['type'] in ('p', 'small', 'head', 'callout'):
                witnesses = [plain(block['text'])]
            elif block['type'] == 'eq':
                witnesses = block['text'].splitlines()
            elif block['type'] == 'table':
                witnesses = [plain(cell) for row in block['rows'] for cell in row]
            elif block['type'] == 'pipeline':
                witnesses = block['labels']
            else:
                witnesses = []
            for witness in witnesses:
                assert norm(witness) in extracted, (i, witness[:160])
                text_checks += 1
    violations = []
    with pdfplumber.open(PDF) as doc:
        for i, page in enumerate(doc.pages, 1):
            for ch in page.chars:
                if ch['text'].isspace():
                    continue
                if ch['x0'] < 50 or ch['x1'] > page.width - 50:
                    violations.append((i, ch['text'], 'horizontal margin'))
                if ch['top'] < 20 or ch['bottom'] > page.height - 18:
                    violations.append((i, ch['text'], 'page edge'))
                if 44 < ch['top'] < 58 or page.height - 54 < ch['bottom'] < page.height - 40:
                    violations.append((i, ch['text'], 'body margin'))
    assert not violations, violations[:20]
    manifest = json.loads((ROOT / 'attachment_manifest.json').read_text(encoding='utf-8'))
    assert len(reader.attachments) == len(manifest) + 1
    for item in manifest:
        copies = reader.attachments[item['name']]
        assert len(copies) == 1
        data = copies[0]
        assert len(data) == item['bytes']
        assert hashlib.sha256(data).hexdigest() == item['sha256'], item['name']
    assert reader.attachments['attachment_manifest.json'][0] == (ROOT / 'attachment_manifest.json').read_bytes()
    sources = json.loads((ROOT / 'source_manifest.json').read_text(encoding='utf-8'))
    base_bytes = reader.attachments[sources['base_specification']['filename']][0]
    assert hashlib.sha256(base_bytes).hexdigest() == sources['base_specification']['sha256']
    base = PdfReader(io.BytesIO(base_bytes))
    assert len(base.pages) == 38
    assert len(base.attachments) == 20
    receipt = {
        'scope': 'Editorial completeness, PDF structure, glyph margins and embedded-byte integrity only; no new physical application validation.',
        'edition': 'Frontier Applications A1.0', 'pdf': PDF.name,
        'sha256': hashlib.sha256(PDF.read_bytes()).hexdigest(),
        'pages': len(pages), 'applications': 18, 'bookmarks': len(reader.outline),
        'text_witness_checks': text_checks, 'glyph_margin_violations': len(violations),
        'attachments': len(reader.attachments), 'attachment_hash_checks': len(manifest),
        'base_pdf_pages': 38, 'base_pdf_nested_attachments': 20,
        'citation_ids': len(refs), 'cited_ids_resolved': len(cited),
        'result': 'pass',
    }
    (ROOT / 'verification_receipt.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
