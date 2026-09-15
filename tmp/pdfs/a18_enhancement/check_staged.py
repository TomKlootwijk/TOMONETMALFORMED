from pathlib import Path
import subprocess,json
root=Path('C:/TOMONETMALFORMED')
paths=subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=root).decode().split('\0')
paths=[p for p in paths if p]
for path in paths:
    assert path=='.gitattributes' or path=='output/pdf/A18_Wave_Material_Computer_Definition_Enhanced_R1_0.pdf' or path.startswith('output/pdf/a18_wave_material_source/')
    assert subprocess.check_output(['git','show',':'+path],cwd=root)==(root/path).read_bytes(),path
print(json.dumps({'staged_files':len(paths),'exact_byte_agreement':True,'scope':'A18 PDF and source only, with byte-preservation attributes'}))
