"""Build the focused A18 technical supplement from editable page JSON.

Windows: requires Calibri/Consolas, ReportLab and pypdf.
Every reading unit is placed in its own frame; overflow is a hard error.
"""
from pathlib import Path
import hashlib
import html
import io
import json
import tempfile

from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Flowable, Frame, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / 'A18_Wave_Material_Computer_Definition_Enhanced_R1_0.pdf'
W, H = A4
WIDTH = W - 104
NAVY = HexColor('#122F40')
TEAL = HexColor('#007C88')
INK = HexColor('#233744')
MUTED = HexColor('#506571')
PALE = HexColor('#EAF2F4')
LINE = HexColor('#C7D7DD')
for name, filename in [('Body', 'calibri.ttf'), ('Bold', 'calibrib.ttf'),
                       ('Italic', 'calibrii.ttf'), ('Mono', 'consola.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(Path('C:/Windows/Fonts') / filename)))
pdfmetrics.registerFontFamily('Body', normal='Body', bold='Bold', italic='Italic', boldItalic='Bold')
styles = {
    'body': ParagraphStyle('body', fontName='Body', fontSize=10.3, leading=13.5, textColor=INK, spaceAfter=7),
    'small': ParagraphStyle('small', fontName='Body', fontSize=9.1, leading=11.8, textColor=MUTED, spaceAfter=6),
    'title': ParagraphStyle('title', fontName='Bold', fontSize=23, leading=25.5, textColor=NAVY, spaceAfter=11),
    'subtitle': ParagraphStyle('subtitle', fontName='Body', fontSize=12.5, leading=16, textColor=MUTED, spaceAfter=12),
    'head': ParagraphStyle('head', fontName='Bold', fontSize=12, leading=14.6, textColor=TEAL, spaceBefore=7, spaceAfter=5),
    'eq': ParagraphStyle('eq', fontName='Mono', fontSize=9, leading=12.6, textColor=NAVY),
    'cell': ParagraphStyle('cell', fontName='Body', fontSize=9.4, leading=12.1, textColor=INK),
    'th': ParagraphStyle('th', fontName='Bold', fontSize=9.2, leading=11.8, textColor=white),
    'label': ParagraphStyle('label', fontName='Bold', fontSize=9, leading=12, textColor=TEAL, spaceAfter=8),
}

def P(text, style='body'):
    return Paragraph(text, styles[style])

def box(items):
    t = Table([[items]], colWidths=[WIDTH])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PALE), ('BOX', (0, 0), (-1, -1), .45, LINE),
        ('LEFTPADDING', (0, 0), (-1, -1), 12), ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 9), ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
    ]))
    return t

class Pipeline(Flowable):
    """Four task-specific steps drawn as editable vector geometry."""
    def __init__(self, labels):
        Flowable.__init__(self)
        self.labels = labels
        self.width = WIDTH
        self.height = 50

    def draw(self):
        c = self.canv
        gap, bh = 12, 30
        bw = (WIDTH - 3 * gap) / 4
        for i, label in enumerate(self.labels):
            x = i * (bw + gap)
            c.setFillColor(NAVY if i < 2 else TEAL)
            c.roundRect(x, 13, bw, bh, 3, fill=1, stroke=0)
            c.setFillColor(white)
            size = min(8.6, (bw - 10) / max(pdfmetrics.stringWidth(label, 'Bold', 1), 1))
            c.setFont('Bold', size)
            c.drawCentredString(x + bw / 2, 24, label)
            if i < 3:
                c.setStrokeColor(TEAL)
                c.setLineWidth(.9)
                c.line(x + bw + 2, 28, x + bw + gap - 2, 28)
                c.line(x + bw + gap - 4, 30, x + bw + gap - 2, 28)
                c.line(x + bw + gap - 4, 26, x + bw + gap - 2, 28)

class Architecture(Flowable):
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

def page_items(page):
    items = []
    if page.get('cover'):
        cover_style = ParagraphStyle('cover', parent=styles['title'], fontSize=35, leading=38, spaceAfter=15)
        items.extend([P('PERPETUUM MOBILE / A18 / R1.0', 'label'), Spacer(1, 12),
                      Paragraph('WAVE-AND-MATERIAL<br/>COMPUTER', cover_style),
                      P('Definition and enhanced architecture', 'subtitle')])
    else:
        items.extend([P(page['label'], 'label'), P(html.escape(page['title']), 'title')])
    for block in page['blocks']:
        kind = block['type']
        if kind in ('p', 'small', 'head'):
            items.append(P(block['text'], {'p': 'body', 'small': 'small', 'head': 'head'}[kind]))
        elif kind == 'eq':
            items.extend([box([P(html.escape(block['text']).replace('\n', '<br/>'), 'eq')]), Spacer(1, 8)])
        elif kind == 'callout':
            items.extend([box([P(block['text'])]), Spacer(1, 9)])
        elif kind == 'architecture':
            items.append(Architecture())
        elif kind == 'pipeline':
            items.append(Pipeline(block['labels']))
        elif kind == 'table':
            rows = [[P(x, 'th' if i == 0 else 'cell') for x in row] for i, row in enumerate(block['rows'])]
            widths = [WIDTH * x / sum(block['widths']) for x in block['widths']]
            t = Table(rows, colWidths=widths, hAlign='LEFT')
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), NAVY),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#F0F5F6')]),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
                ('LINEBELOW', (0, -1), (-1, -1), .4, LINE),
            ]))
            items.extend([t, Spacer(1, 9)])
        elif kind == 'spacer':
            items.append(Spacer(1, block['height']))
        else:
            raise ValueError('Unknown block type: ' + kind)
    return items

def furniture(c, number, total):
    c.saveState()
    if number > 1:
        c.setStrokeColor(LINE)
        c.line(52, H - 43, W - 52, H - 43)
        c.setFillColor(NAVY)
        c.setFont('Bold', 8)
        c.drawString(52, H - 34, 'PERPETUUM MOBILE')
        c.setFillColor(MUTED)
        c.setFont('Body', 8)
        c.drawRightString(W - 52, H - 34, 'A18 / DEFINITION + ENHANCEMENT / R1.0')
    c.setStrokeColor(LINE)
    c.line(52, 43, W - 52, 43)
    c.setFillColor(MUTED)
    c.setFont('Body', 8)
    c.drawString(52, 29, 'Tom Klootwijk / NL200678942 / 15 September 2026')
    c.drawRightString(W - 52, 29, f'{number:02d} / {total:02d}')
    c.restoreState()

def markdown(pages):
    md = ['# A18 / Wave-and-material computer\n\nTom Klootwijk / NL200678942\n\nR1.0 / 15 September 2026\n']
    for number, page in enumerate(pages, 1):
        md.append(f'\n## Page {number}: {page["title"]}\n')
        if page.get('subtitle'):
            md.append(page['subtitle'] + '\n')
        for b in page['blocks']:
            if b['type'] in ('p', 'small', 'head', 'callout'):
                md.append(('### ' if b['type'] == 'head' else '') + b['text'] + '\n')
            elif b['type'] == 'eq':
                md.append('```text\n' + b['text'] + '\n```\n')
            elif b['type'] == 'architecture':
                md.append('Input -> encode -> optical core -> coherent I/Q readout -> output. Material retains core settings; digital control programs and verifies them.\n')
            elif b['type'] == 'pipeline':
                md.append(' → '.join(b['labels']) + '\n')
            elif b['type'] == 'table':
                for i, row in enumerate(b['rows']):
                    md.append('| ' + ' | '.join(row) + ' |')
                    if i == 0:
                        md.append('| ' + ' | '.join('---' for _ in row) + ' |')
                md.append('')
    path = ROOT / 'A18_Definition_Enhanced_R1_0.md'
    path.write_text('\n'.join(md), encoding='utf-8')
    return path

def build():
    pages = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
    stream = io.BytesIO()
    c = canvas.Canvas(stream, pagesize=A4, invariant=1, pageCompression=1)
    layout = []
    for number, page in enumerate(pages, 1):
        furniture(c, number, len(pages))
        items = page_items(page)
        frame = Frame(52, 56, WIDTH, H - 63 - 56, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        frame.addFromList(items, c)
        if items:
            leftover = getattr(items[0], 'text', type(items[0]).__name__)
            raise RuntimeError(f'Page {number} overflow ({page["title"]}): {str(leftover)[:180]}')
        layout.append({'page': number, 'title': page['title'], 'bottom_content_y': round(frame._y, 2)})
        c.showPage()
    c.save()
    reader = PdfReader(stream)
    assert len(reader.pages) == len(pages)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    for number, page in enumerate(pages):
        writer.add_outline_item(page['title'], number)
    manifest = json.loads((ROOT / 'source_manifest.json').read_text(encoding='utf-8'))
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
                 'prepare_sources.py','pm_content.json','numeric_summary.json','reference_model.py','reference_results.json',
                 'build_pdf.py','verify_pdf.py','README.md','layout_report.json']
    attachments = [base, md] + [ROOT / name for name in filenames]
    attachment_manifest = []
    for path in attachments:
        data = path.read_bytes()
        writer.add_attachment(path.name, data)
        attachment_manifest.append({'name': path.name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    manifest_path = ROOT / 'attachment_manifest.json'
    manifest_path.write_text(json.dumps(attachment_manifest, indent=2), encoding='utf-8')
    writer.add_attachment(manifest_path.name, manifest_path.read_bytes())
    writer.add_metadata({
        '/Title': 'A18 | Wave-and-material computer | R1.0',
        '/Author': 'Tom Klootwijk (source framework); Codex-assisted A18 definition and enhancement',
        '/Subject': 'Coherent wave processing, retained material settings, calibrated operation and synthetic reference model',
        '/Creator': 'ReportLab and pypdf; Codex-assisted preparation',
        '/Keywords': 'Perpetuum Mobile, Tom Klootwijk, UGTS, atomOS, WANTWOMBAN, SEED, A18, retained photonic computation',
    })
    with OUT.open('wb') as f:
        writer.write(f)
    print(json.dumps({'output': str(OUT), 'pages': len(pages), 'attachments': len(attachments) + 1, 'bytes': OUT.stat().st_size}))

if __name__ == '__main__':
    build()
