from pathlib import Path
import subprocess, json
root=Path('C:/TOMONETMALFORMED')
paths=subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=root).decode().split('\0')
paths=[p for p in paths if p]
assert paths
for path in paths:
    assert path=='.gitattributes' or path=='output/pdf/Perpetuum_Mobile_Frontier_Applications_A1_0.pdf' or path.startswith('output/pdf/frontier_applications_source/')
    staged=subprocess.check_output(['git','show',':'+path],cwd=root)
    working=(root/path).read_bytes()
    assert staged==working,path
print(json.dumps({'staged_files':len(paths),'exact_bytes_match':True,'scope_check':'pass'}))
