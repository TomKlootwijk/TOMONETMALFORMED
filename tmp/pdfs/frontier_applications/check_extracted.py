from pathlib import Path
import hashlib, subprocess, sys
from pypdf import PdfReader
root=Path(__file__).resolve().parent
original=Path('C:/TOMONETMALFORMED/output/pdf/Perpetuum_Mobile_Frontier_Applications_A1_0.pdf')
dest=root/'extracted'
dest.mkdir(exist_ok=True)
for name, copies in PdfReader(original).attachments.items():
    assert Path(name).name==name
    (dest/name).write_bytes(copies[0])
for script in ('assemble_content.py','build_pdf.py','verify_pdf.py'):
    subprocess.run([sys.executable,str(dest/script)],check=True)
rebuilt=root/original.name
same=original.read_bytes()==rebuilt.read_bytes()
print('EXTRACTED_REBUILD_IDENTICAL:',same)
assert same
