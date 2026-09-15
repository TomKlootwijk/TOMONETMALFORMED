"""Build the application companion from its editable page JSON.

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
OUT = ROOT.parent / 'Perpetuum_Mobile_Frontier_Applications_A1_0.pdf'
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

def page_items(page):
    items = []
    if page.get('cover'):
        cover_style = ParagraphStyle('cover', parent=styles['title'], fontSize=39, leading=41, spaceAfter=10)
        items.extend([P('PERPETUUM MOBILE / APPLICATION COMPANION A1.0', 'label'), Spacer(1, 6),
                      Paragraph('FRONTIER<br/>APPLICATIONS', cover_style),
                      P(page['subtitle'], 'subtitle')])
        art = ROOT / 'assets' / 'frontier_cover.png'
        if not art.exists():
            art = ROOT / 'frontier_cover.png'
        items.extend([Image(str(art), width=WIDTH, height=WIDTH * 2 / 3), Spacer(1, 15)])
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
        c.drawRightString(W - 52, H - 34, 'FRONTIER APPLICATIONS / A1.0')
    c.setStrokeColor(LINE)
    c.line(52, 43, W - 52, 43)
    c.setFillColor(MUTED)
    c.setFont('Body', 8)
    c.drawString(52, 29, 'Tom Klootwijk / NL200678942 / 15 September 2026')
    c.drawRightString(W - 52, 29, f'{number:02d} / {total:02d}')
    c.restoreState()

def markdown(pages):
    md = ['# Perpetuum Mobile / Frontier Applications\n\nTom Klootwijk / NL200678942\n\nA1.0 / 15 September 2026\n']
    for number, page in enumerate(pages, 1):
        md.append(f'\n## Page {number}: {page["title"]}\n')
        if page.get('subtitle'):
            md.append(page['subtitle'] + '\n')
        for b in page['blocks']:
            if b['type'] in ('p', 'small', 'head', 'callout'):
                md.append(('### ' if b['type'] == 'head' else '') + b['text'] + '\n')
            elif b['type'] == 'eq':
                md.append('```text\n' + b['text'] + '\n```\n')
            elif b['type'] == 'pipeline':
                md.append(' → '.join(b['labels']) + '\n')
            elif b['type'] == 'table':
                for i, row in enumerate(b['rows']):
                    md.append('| ' + ' | '.join(row) + ' |')
                    if i == 0:
                        md.append('| ' + ' | '.join('---' for _ in row) + ' |')
                md.append('')
    path = ROOT / 'Frontier_Applications_A1_0.md'
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
    base = ROOT / manifest['base_specification']['relative_path']
    if not base.exists():
        base = ROOT / manifest['base_specification']['filename']
    if hashlib.sha256(base.read_bytes()).hexdigest() != manifest['base_specification']['sha256']:
        raise ValueError('Base specification hash mismatch')
    for key in ('conversation_reply', 'image'):
        item = manifest[key]
        path = ROOT / item['filename']
        if not path.exists():
            path = ROOT / Path(item['filename']).name
        if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            raise ValueError('Source witness hash mismatch: ' + key)
    md = markdown(pages)
    (ROOT / 'layout_report.json').write_text(json.dumps(layout, indent=2), encoding='utf-8')
    filenames = [
        'original_reply.md', 'reply_apps.json', 'source_manifest.json', 'imagegen_prompt.md',
        'apps_01_06.json', 'apps_07_12.json', 'apps_13_18.json', 'content.json', 'references.json',
        'assemble_content.py', 'build_pdf.py', 'verify_pdf.py', 'README.md', 'layout_report.json',
    ]
    attachments = [base, md] + [ROOT / name for name in filenames]
    art = ROOT / 'assets' / 'frontier_cover.png'
    attachments.append(art if art.exists() else ROOT / 'frontier_cover.png')
    attachment_manifest = []
    for path in attachments:
        data = path.read_bytes()
        writer.add_attachment(path.name, data)
        attachment_manifest.append({'name': path.name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    manifest_path = ROOT / 'attachment_manifest.json'
    manifest_path.write_text(json.dumps(attachment_manifest, indent=2), encoding='utf-8')
    writer.add_attachment(manifest_path.name, manifest_path.read_bytes())
    writer.add_metadata({
        '/Title': 'Perpetuum Mobile | Frontier Applications A1.0',
        '/Author': 'Tom Klootwijk (source framework); Codex-assisted application expansion',
        '/Subject': '18 proposed analog, digital and physical applications with models and experiments',
        '/Creator': 'ReportLab and pypdf; Codex-assisted preparation',
        '/Keywords': 'Perpetuum Mobile, Tom Klootwijk, UGTS, atomOS, WANTWOMBAN, SEED, futuristic applications',
    })
    with OUT.open('wb') as f:
        writer.write(f)
    print(json.dumps({'output': str(OUT), 'pages': len(pages), 'attachments': len(attachments) + 1, 'bytes': OUT.stat().st_size}))

if __name__ == '__main__':
    build()
