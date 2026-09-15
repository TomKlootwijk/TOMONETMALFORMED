from pathlib import Path
import json, sys, hashlib, html, tempfile
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, Color, white
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader, PdfWriter

ROOT=Path(__file__).resolve().parent
_build_temp=tempfile.TemporaryDirectory(prefix='ppm_pdf_')
TMP=Path(_build_temp.name)
OUT=ROOT.parent/'Perpetuum_Mobile_Tom_Klootwijk_V1_0.pdf'
for name,file in [('Body','calibri.ttf'),('Bold','calibrib.ttf'),('Italic','calibrii.ttf'),('Mono','consola.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(Path(r'C:\Windows\Fonts')/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')
NAVY=HexColor('#122F40'); TEAL=HexColor('#007C88'); INK=HexColor('#233744'); MUTED=HexColor('#506571'); PALE=HexColor('#EAF2F4'); LINE=HexColor('#C7D7DD')
W,H=A4; WIDTH=W-104
styles={
 'body':ParagraphStyle('body',fontName='Body',fontSize=10.5,leading=14.1,textColor=INK,spaceAfter=8),
 'small':ParagraphStyle('small',fontName='Body',fontSize=9.1,leading=12,textColor=MUTED,spaceAfter=6),
 'title':ParagraphStyle('title',fontName='Bold',fontSize=25,leading=28,textColor=NAVY,spaceAfter=13),
 'subtitle':ParagraphStyle('subtitle',fontName='Body',fontSize=12,leading=16,textColor=MUTED,spaceAfter=16),
 'head':ParagraphStyle('head',fontName='Bold',fontSize=12.4,leading=15.4,textColor=TEAL,spaceBefore=8,spaceAfter=6),
 'eq':ParagraphStyle('eq',fontName='Mono',fontSize=9.1,leading=13.1,textColor=NAVY,spaceAfter=0),
 'cell':ParagraphStyle('cell',fontName='Body',fontSize=9.4,leading=12.2,textColor=INK),
 'th':ParagraphStyle('th',fontName='Bold',fontSize=9.2,leading=11.8,textColor=white),
 'label':ParagraphStyle('label',fontName='Bold',fontSize=9,leading=12,textColor=TEAL,spaceAfter=8),
}
def P(s,sty='body'):
    return Paragraph(s,styles[sty])
def escaped(s):
    return html.escape(s).replace('\n','<br/>')
def box(items,bg=PALE):
    t=Table([[items]],colWidths=[WIDTH])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),('BOX',(0,0),(-1,-1),.45,LINE),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
    return t
class LoopDiagram(Flowable):
    def __init__(self): super().__init__(); self.width=WIDTH; self.height=118
    def draw(self):
        c=self.canv; bw=(WIDTH-30)/4; bh=40
        labels=[('STATE','word + history'),('TRANSITION','typed + guarded'),('DOMAIN','plant or digital'),('READBACK','measured or exact')]
        for i,(a,b) in enumerate(labels):
            x=i*(bw+10); c.setFillColor(NAVY if i<2 else TEAL); c.roundRect(x,52,bw,bh,4,fill=1,stroke=0)
            c.setFillColor(white); c.setFont('Bold',8); c.drawCentredString(x+bw/2,76,a); c.setFont('Body',8); c.drawCentredString(x+bw/2,62,b)
            if i<3:
                c.setStrokeColor(TEAL); c.line(x+bw+1,72,x+bw+9,72)
        c.setStrokeColor(TEAL); c.setLineWidth(1); c.line(WIDTH-bw/2,49,WIDTH-bw/2,25); c.line(WIDTH-bw/2,25,bw/2,25); c.line(bw/2,25,bw/2,48)
        c.setFillColor(TEAL); c.setFont('Body',9); c.drawCentredString(WIDTH/2,9,'next epoch: causal feedback + recorded evidence')

pages=json.loads((ROOT/'content.json').read_text(encoding='utf-8'))
def frame(c,doc):
    n=c.getPageNumber(); c.saveState()
    if n>1:
        c.setStrokeColor(LINE); c.line(52,H-43,W-52,H-43)
        c.setFillColor(NAVY); c.setFont('Bold',8); c.drawString(52,H-34,'PERPETUUM MOBILE')
        c.setFillColor(MUTED); c.setFont('Body',8); c.drawRightString(W-52,H-34,'PM 1.0  /  FORMALIZATION OF FORMALIZATIONS')
    c.setStrokeColor(LINE); c.line(52,43,W-52,43)
    c.setFillColor(MUTED); c.setFont('Body',8); c.drawString(52,29,'Tom Klootwijk  /  NL200678942  /  15 September 2026')
    c.drawRightString(W-52,29,f'{n:02d} / {len(pages):02d}'); c.restoreState()

story=[]
for idx,page in enumerate(pages):
    if idx: story.append(PageBreak())
    if page.get('cover'):
        story.extend([Spacer(1,22),P('FORMAL SPECIFICATION  /  MASTER V1.0','label'),Spacer(1,25)])
        coverstyle=ParagraphStyle('cover',parent=styles['title'],fontSize=43,leading=45)
        story.append(Paragraph('PERPETUUM<br/>MOBILE',coverstyle))
        story.append(Spacer(1,14)); story.append(P(page['subtitle'],'subtitle')); story.append(Spacer(1,18))
        story.append(LoopDiagram()); story.append(Spacer(1,22))
    else:
        story.append(P(page.get('label',f'{idx:02d} / SPECIFICATION'),'label'))
        story.append(P(page['title'],'title'))
        if page.get('subtitle'): story.append(P(page['subtitle'],'subtitle'))
    for b in page['blocks']:
        kind=b['type']
        if kind in ('p','small','head'): story.append(P(b['text'],{'p':'body','small':'small','head':'head'}[kind]))
        elif kind=='eq':
            story.append(box([P(escaped(b['text']),'eq')])); story.append(Spacer(1,9))
        elif kind=='callout':
            story.append(box([P(b['text'])])); story.append(Spacer(1,10))
        elif kind=='diagram': story.append(LoopDiagram())
        elif kind=='table':
            rows=[[P(x,'th' if i==0 else 'cell') for x in row] for i,row in enumerate(b['rows'])]
            widths=[WIDTH*x/sum(b['widths']) for x in b['widths']]
            t=Table(rows,colWidths=widths,hAlign='LEFT',repeatRows=1)
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#F0F5F6')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,-1),(-1,-1),.4,LINE)]))
            story.append(t); story.append(Spacer(1,10))
        elif kind=='spacer': story.append(Spacer(1,b['height']))
    # Every planned page is an intentional reading unit. Overflow is an error below.

base=TMP/'layout.pdf'
doc=SimpleDocTemplate(str(base),pagesize=A4,rightMargin=52,leftMargin=52,topMargin=63,bottomMargin=56,title='Perpetuum Mobile - Formalization of Formalizations - PM 1.0',author='Tom Klootwijk (source framework); synthesis prepared with Codex',subject='Typed cross-domain application families, deterministic seed contract, source-specific semantics and evidence')
doc.build(story,onFirstPage=frame,onLaterPages=frame)
r=PdfReader(base)
if len(r.pages)!=len(pages): raise RuntimeError(f'Layout overflow: expected {len(pages)} pages, got {len(r.pages)}')

md=['# PERPETUUM MOBILE\n\nTom Klootwijk / NL200678942\n\nPM 1.0 / 15 September 2026\n']
for i,page in enumerate(pages,1):
    md.append(f'\n## Page {i}: '+page.get('title','Perpetuum Mobile')+'\n')
    if page.get('subtitle'): md.append(page['subtitle']+'\n')
    for b in page['blocks']:
        if b['type'] in ('p','small','head','callout'): md.append(b['text']+'\n')
        elif b['type']=='eq': md.append('```text\n'+b['text']+'\n```\n')
        elif b['type']=='table':
            md.append('\n'.join('| '+' | '.join(row)+' |' for row in b['rows'])+'\n')
source_md=ROOT/'Perpetuum_Mobile_V1_0.md'; source_md.write_text('\n'.join(md),encoding='utf-8')
w=PdfWriter(); w.clone_document_from_reader(r)
for i,page in enumerate(pages):
    w.add_outline_item(page.get('title','Perpetuum Mobile'),i)
manifest=json.loads((ROOT/'source_manifest.json').read_text(encoding='utf-8'))
attachments=[source_md,ROOT/'content.json',ROOT/'build_pdf.py',ROOT/'source_manifest.json']
for item in manifest:
    original=Path(item['path'])
    witness=original if original.exists() else ROOT/original.name
    if not witness.exists(): raise FileNotFoundError('Extract attached source PDF beside this builder: '+original.name)
    if hashlib.sha256(witness.read_bytes()).hexdigest()!=item['sha256']: raise ValueError('Source witness hash mismatch: '+original.name)
    attachments.append(witness)
for name in ('seed_reference_v1.py','seed_reference_v1_results.json','seed_reference_v1_crosscheck.ps1','seed_reference_v1_crosscheck_results.json','PPM_SEED_v1_contract.md','formal_checks.py','formal_checks_results.json','write_content.py','write_seed_pages.py','seed_pages.json','README.md'):
    path=ROOT/name
    if path.exists(): attachments.append(path)
artifact_manifest=[]
for path in attachments:
    data=path.read_bytes(); w.add_attachment(path.name,data)
    artifact_manifest.append({'name':path.name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
package_manifest=ROOT/'attachment_manifest.json'
package_manifest.write_text(json.dumps(artifact_manifest,indent=2),encoding='utf-8')
w.add_attachment(package_manifest.name,package_manifest.read_bytes())
w.add_metadata({'/Title':'Perpetuum Mobile | PM 1.0 | Tom Klootwijk','/Author':'Tom Klootwijk (source framework)','/Subject':'Meta-formalization with V01-V07 application architectures','/Creator':'Codex-assisted synthesis; ReportLab; pypdf','/Keywords':'Perpetuum Mobile, WANTWOMBAN, atomOS, UGTS, deterministic seed, cross-domain, formalization'})
with OUT.open('wb') as f: w.write(f)
print(json.dumps({'output':str(OUT),'pages':len(r.pages),'attachments':len(attachments)+1,'bytes':OUT.stat().st_size}))

_build_temp.cleanup()
