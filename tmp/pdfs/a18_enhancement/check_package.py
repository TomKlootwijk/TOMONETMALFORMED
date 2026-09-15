from pathlib import Path
import json,subprocess,sys
import numpy as np
from pypdf import PdfReader
root=Path(__file__).resolve().parent
original=Path('C:/TOMONETMALFORMED/output/pdf/A18_Wave_Material_Computer_Definition_Enhanced_R1_0.pdf')
dest=root/'extracted'
dest.mkdir(exist_ok=True)
for name,copies in PdfReader(original).attachments.items():
    assert Path(name).name==name
    (dest/name).write_bytes(copies[0])
for script in ('prepare_sources.py','write_content.py','build_pdf.py','verify_pdf.py'):
    subprocess.run([sys.executable,str(dest/script)],check=True)
assert original.read_bytes()==(root/original.name).read_bytes()
subprocess.run([sys.executable,str(dest/'reference_model.py'),'--pm-content',str(dest/'pm_content.json'),'--out',str(dest/'rerun_results.json')],check=True)
old=json.loads((dest/'reference_results.json').read_text())
new=json.loads((dest/'rerun_results.json').read_text())
assert old['checks']==new['checks']
for case,stats in old['summary_relative_errors'].items():
    for field,value in stats.items():
        assert abs(value-new['summary_relative_errors'][case][field])<=1e-12
assert old['energy_break_even']==new['energy_break_even']
print('EXTRACTED_PDF_REBUILD_IDENTICAL: True')
print('EXTRACTED_MODEL_RERUN: 44 checks; summary agreement <=1e-12')
