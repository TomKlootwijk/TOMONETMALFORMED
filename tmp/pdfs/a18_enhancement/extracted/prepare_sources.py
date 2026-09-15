"""Update compact source records and table data from the executed model receipt."""
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parent
companion=ROOT.parent/'Perpetuum_Mobile_Frontier_Applications_A1_0.pdf'
if not companion.exists(): companion=ROOT/companion.name
expected='8a2506a35bfdc316f6c96827293663b7a964d6932985e89ac659ea4f4f517bca'
assert hashlib.sha256(companion.read_bytes()).hexdigest()==expected
pm_local=ROOT/'pm_content.json'
pm_source=ROOT.parent/'perpetuum_mobile_source'/'content.json'
pm_expected='bc395d17b21434c6bac37374d754828352fed4febf4bd123fb065c9594b86b4b'
pm_bytes=(pm_local if pm_local.exists() else pm_source).read_bytes()
assert hashlib.sha256(pm_bytes).hexdigest()==pm_expected
if not pm_local.exists(): pm_local.write_bytes(pm_bytes)
manifest={'edition':'A18 Definition and Enhanced Architecture R1.0',
    'framework_author':'Tom Klootwijk','author_identifier':'NL200678942',
    'companion':{'filename':companion.name,'relative_path':'../'+companion.name,'pages':56,
        'sha256':expected,'repository_commit':'b2c3fb239bd3572d95080440ad35b843dbc6b6b4'},
    'pm_content':{'filename':'pm_content.json','sha256':pm_expected,'origin':'Exact PM 1.0 content.json'},
    'normative_pm':{'edition':'PM 1.0','pages':38,'location':'Nested attachment in the companion',
        'sha256':'b6532f9638e6cca77d75c2636a54afb5daf587a4e69aceff72102384252a5a55'}}
(ROOT/'source_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
r=json.loads((ROOT/'reference_results.json').read_text(encoding='utf-8'))
assert r['status']=='passed'
assert r['provenance']['script_sha256']==hashlib.sha256((ROOT/'reference_model.py').read_bytes()).hexdigest()
e=r['summary_relative_errors']; energy=r['energy_break_even']
rows=[['Check / maximum held-out relative L2 error','Executed result'],
    ['Mathematical and software checks',str(r['checks_passed'])+' passed'],
    ['Scalar decoding only',f'{100*e["static_scalar"]["maximum"]:.6f}%'],
    ['Four-factor calibration',f'{100*e["static_calibrated"]["maximum"]:.6f}%'],
    ['Specified drift; old calibration',f'{100*e["drift_stale"]["maximum"]:.6f}%'],
    ['Specified drift; refreshed calibration',f'{100*e["drift_refreshed"]["maximum"]:.6f}%'],
    ['Largest refreshed numerical decoder gain',f'{r["synthetic_calibration"]["refreshed_calibration"]["max_decoder_gain"]:.6f}'],
    ['Held-out complex vectors',str(len(r['heldout_inputs']))]]
summary={'rows':rows,
    'interpretation':'Calibration improves these six held-out vectors because the chosen perturbations closely match the row-factor model. The drift case demonstrates why retaining an old calibration is insufficient. These percentages are finite synthetic errors, not measured hardware accuracy or a statistical confidence interval.',
    'energy_text':f'Illustration only: setup energy 2 mJ, complete hybrid read cost 3 microjoules per task and digital cost 5 microjoules per task give strict break-even at {energy["minimum_integer_reuse"]:,} reused tasks. Under these chosen values, requalification every 800 tasks removes the advantage; a 2,000-task interval permits it. Actual values must be measured.',
    'source_receipt_sha256':hashlib.sha256((ROOT/'reference_results.json').read_bytes()).hexdigest()}
(ROOT/'numeric_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print('Source manifest and numeric summary prepared.')
