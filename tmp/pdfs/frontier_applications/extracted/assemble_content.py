from pathlib import Path
import json, html, re
ROOT=Path(__file__).resolve().parent
def safe(s):
    return html.escape(s.replace('\u2011','-').replace('\u2013','-').replace('\u2014',' - '))
def p(t):return {'type':'p','text':t}
def h(t):return {'type':'head','text':t}
def small(t):return {'type':'small','text':t}
def eq(t):return {'type':'eq','text':t}
def call(t):return {'type':'callout','text':t}
def table(rows,widths):return {'type':'table','rows':rows,'widths':widths}
pages=[]
def page(title,label,*blocks,**extra):
    pages.append(dict(title=title,label=label,blocks=list(blocks),**extra))
apps=[]
for name in ('apps_01_06.json','apps_07_12.json','apps_13_18.json'):
    apps.extend(json.loads((ROOT/name).read_text(encoding='utf-8')))
apps.sort(key=lambda a:a['id'])
assert [a['id'] for a in apps]==list(range(1,19))
required={'id','title','short_title','modes','families','scenario','mechanism','source_roles','equation','equation_context','loop','demonstrator','metrics','failure','future','seed_role','references'}
for a in apps:
    assert not (required-set(a)),(a['id'],required-set(a))
    assert len(a['loop'])==4 and len(a['metrics'])==3
    assert len(a['equation'].splitlines())<=5
    assert max(map(len,a['equation'].splitlines()))<=72

page('Frontier Applications','APPLICATION COMPANION',
    p('<b>Tom Klootwijk / NL200678942</b><br/>Framework attribution'),
    p('18 expanded architectures for analog, digital, physical and future systems.'),
    small('A1.0 / 15 September 2026<br/>Companion to Perpetuum Mobile PM 1.0. Prepared with Codex assistance.'),
    small('Cover: AI-generated concept art showing a proposed adaptive workshop. It is not a photograph, engineering drawing or evidence of a built PM machine.'),
    cover=True,subtitle='From a surface that remembers to a habitat that repairs itself')

page('From an idea list to an application book','01 / PURPOSE',
    p('This companion documents and expands the preceding 18-application reply. The original wording is preserved in a printed appendix and an embedded Markdown witness. Each expanded application now has a use scenario, operating mechanism, model, source mapping, demonstrator, comparison criteria and future extension.'),
    p('A01-A18 are application identifiers. V01-V07 refer to the existing families in <b>Perpetuum Mobile PM 1.0</b>. The new numbering does not imply eighteen new physical laws or replace the earlier specification.'),
    h('The central proposition'),
    call('A common formal description could connect digital rules, physical memory, geometric transformations, measured feedback and repair. Its value must appear in the useful result: a better experiment, a more reliable action, lower resource use or a clearer explanation of failure.'),
    h('How to read the expanded designs'),
    p('<b>Proposal:</b> a new integration described here. <b>Component evidence:</b> a cited result supporting one ingredient. <b>Model:</b> a conditional equation requiring parameters and an operating region. <b>Demonstrator:</b> a finite experiment that has not been performed for this book. <b>Future:</b> an extension dependent on unresolved engineering.'),
    p('Equations are compact design contracts. They do not replace a full material model, hardware specification, control proof or qualification process. Numeric acceptance targets are proposed experiment criteria unless a cited source explicitly reports a measured result.'),
    small('The underlying PM 1.0 PDF is embedded unchanged. It contains the four original source PDFs, the exact SEED contract and scoped reference checks. The new book introduces no claim that these eighteen complete systems have been built.'))

for group in (apps[:9],apps[9:]):
    rows=[['Application','Embodiment / PM family','Pages']]
    for a in group:
        start=7+(a['id']-1)*2
        rows.append([f'<b>A{a["id"]:02d}</b> '+safe(a['title']),safe(', '.join(a['modes']))+'<br/>'+safe(', '.join(a['families'])),f'{start}-{start+1}'])
    page('Application atlas / '+('1-9' if group[0]['id']==1 else '10-18'),'02 / READING MAP',table(rows,[2.75,1.75,.55]),
        small('Applications occupy pp. 7-42. Integration and experiment planning follow on pp. 43-48; the original reply is on pp. 49-51. The bibliography and provenance record follow. Internal PDF bookmarks provide direct chapter navigation.'))

page('What the common architecture contributes','03 / SHARED OPERATING MODEL',
    table([['Source/family','Concrete contribution','Additional work in an application'],['UGTS / geometry and lineage','Typed objects, ordered hinges, support, compatibility, guarded events','Device/material bindings and valid event certificates'],['atomOS / logic and records','Packed support, explicit JK/ASA/NA profiles, transactional digital state','Actuator decoding and any newly introduced feedback policy'],['WANTWOMBAN / material feedback','Word-command-heat-colour-measurement loop','Calibrated device response, energy boundary and physical state'],['PM SEED / digital replay','Exact input generation and reproducible logical streams','Full descriptor, external-input transcript and numerical rules']],[1.3,1.8,2]),
    eq('descriptor + state + input -> proposal -> guard -> commit\nactual command -> physical evolution -> measured readback'),
    p('The physical plant keeps evolving while software evaluates a proposal. Digital commit cannot reverse deposited material, heat, charge or motion. A command and its acknowledgment must therefore be separate records, followed by reconciliation with the actual state.'),
    p('The full causal loop includes sensor, computation, communication and actuator delay. A future machine needs a stability or bounded-error argument for the resulting system. Reusing the same record format does not prove that two physical components are compatible.'),
    small('Source map: PM 1.0 pp. 4-14 and 34-36. Literal OTAN2, code-mixing OTAN2, geometric atan2, numerical H4 and Boolean XOR retain their separate meanings.'))

page('Three flagship directions','04 / RESEARCH PRIORITIES',
    h('1 / A surface with physical memory'),
    p('Combine A02 material memory with A03 adaptive tooling. Begin by showing that a measured history-dependent signal improves a bounded contact task. Add deformation only after separating the influence of temperature, shape, load and readout drift. This is a compact place to test whether the source-specific composition adds value.'),
    h('2 / A workshop that changes its capabilities'),
    p('Combine the adaptive table, A08 experiment automation and A09 inspected fabrication. A fixture is designed, made, measured and used; its later removal or failure remains in the physical record. The result would be a workshop that configures itself for particular tasks within known machine and material limits.'),
    h('3 / A habitat that commissions repairs'),
    p('Combine A01, A12 and A14: resource monitoring, intermittent-link robots and local maintenance. Begin with an uncrewed installation and a small approved repair catalog. The final ambition is a system that closes inspection, diagnosis, planning, repair and verification while accounting for consumables.'),
    call('These priorities are editorial judgments about useful research structure, not measured rankings of readiness or commercial value. A01 is the broadest integration; A02 and A03 offer smaller experiments that can expose its assumptions.'),
    small('A future photonic or acoustic layer can be added through A04/A18 after its bandwidth, calibration, power and conversion costs are known. Its contribution should be evaluated against the same task performed electronically.'))

for a in apps:
    tag=f'A{a["id"]:02d}'
    page(f'{tag} / '+a['short_title'],'APPLICATION / DESIGN',
        small('<b>'+safe(a['title'])+'</b><br/>'+safe(' + '.join(a['modes']))+' / '+safe(', '.join(a['families']))),
        h('A scene to make the idea concrete'),p(safe(a['scenario'])),
        {'type':'pipeline','labels':a['loop']},
        h('Operating mechanism'),p(safe(a['mechanism'])),
        eq(a['equation']),p(safe(a['equation_context'])),
        h('Where this framework enters'),p(safe(a['source_roles'])))
    rows=[['Measure','Proposed comparison or criterion']]+[[safe(m['measure']),safe(m['criterion'])] for m in a['metrics']]
    page(f'{tag} / Experiment and future','APPLICATION / VALIDATION',
        small('<b>'+safe(a['title'])+'</b>'),
        h('Minimum demonstrator'),p(safe(a['demonstrator'])),
        table(rows,[1.2,3.9]),
        h('The failure that matters'),p(safe(a['failure'])),
        h('How the future extension would differ'),p(safe(a['future'])),
        h('The exact role of SEED'),p(safe(a['seed_role'])),
        small('Component evidence: '+', '.join('['+r['id']+']' for r in a['references'])+'. See the bibliography for the result supported and the boundary of that evidence.'))

page('One machine assembled from five ideas','05 / COMPOSITION',
    p('<b>Proposed demonstrator:</b> an adaptive repair workcell. A seeded digital description requests a cradle for a part. A03 reshapes a table; A02 reads history-dependent contact signals; A09 deposits a temporary fixture; A08 schedules the experiment; A04 may later provide a calibrated optical signal path.'),
    table([['Connection','Information crossing the boundary','What must be established'],['Design -> surface','Target pose, load envelope, frame and tolerances','Reachability and measured load support'],['Surface -> memory','Timestamped sensor sequence with calibration','Scaling, read disturbance and history preparation'],['Memory -> decision','Estimated contact/slip state plus uncertainty','A validated decision policy and latency limit'],['Decision -> fabrication','Bounded path, material ID and support requirements','Actual deposition and independent verification'],['All -> next design','Measurements, failures and actual resource use','Versioned inputs; no replacement of evidence by predictions']],[1.1,2,2]),
    eq('total cycle time = sense + decide + move + settle + verify\nnet useful output = accepted result within the task envelope'),
    p('A useful trial compares the complete workcell against conventional fixtures and ordinary feedback on the same part family. Include setup, calibration, rejects, removal and maintenance. A faster inner computation is only one part of the result.'),
    small('The demonstration is a research proposal. It is intentionally smaller than a self-maintaining habitat and can fail in ways that reveal which larger integration is premature.'))

page('A sequence of engineering gates','06 / DEVELOPMENT PATH',
    table([['Gate','Evidence required to proceed','Stop or revise when'],['G0 / specify','Task, units, state, ports, source profile and baseline are explicit','Names conceal missing mechanisms or undefined observables'],['G1 / characterize','Component response, drift, noise and operating bounds are measured','The selected model cannot explain held-out responses'],['G2 / couple','Adjacent components exchange correctly typed signals under load','Delay, crosstalk or conversion cost defeats the intended task'],['G3 / close the loop','The physical loop works over a declared envelope and fault set','Unmodeled events destabilize it or invalidate the guards'],['G4 / compare','A full-system result exceeds a preregistered baseline or meets a new capability','The apparent advantage disappears after overhead and failures'],['G5 / extend','Scale and mission claims are supported by new evidence','A small demonstration is being treated as proof of general deployment']],[1.05,2.05,2]),
    p('These gates specify evidence, not dates. The document does not assign universal development times or technology-readiness scores. Costs, personnel, fabrication access and qualification requirements depend on the selected application and region.'),
    p('A failed gate is useful information. Preserve the observation and update the model or design. Change an acceptance rule prospectively with a new version; do not relabel a failed run as a pass by altering its original criterion.'),
    small('Useful first tests isolate the uncertain physical link. For example, measure whether deformation changes a memory readout before building a full robotic skin around it.'))

page('Experiments that can reject the idea','07 / COMPARISON DESIGN',
    h('Measure the capability the user receives'),
    p('For a fixture, measure accepted load-bearing geometry and setup time. For a reservoir, measure held-out temporal-task error and total energy. For a wave processor, measure complex transfer accuracy over bandwidth and temperature. For repair, measure the repaired property with an independent method.'),
    table([['Control','Purpose'],['Conventional baseline','Shows whether ordinary geometry, sensing and control already solve the task'],['Component removal','Tests whether material memory, source geometry or wave processing adds useful information'],['Matched resource budget','Prevents extra sensors, training data, energy or manual calibration from being hidden advantages'],['Held-out conditions','Tests new inputs and environments rather than memorized calibration trajectories'],['Fault injection','Tests stale measurements, partial actions, device failure and interrupted communication'],['Independent readout','Checks the actual result with an instrument or method not used to approve it']],[1.25,3.85]),
    p('Report trial count, rejected and missing runs, uncertainty, data partitions, parameter changes and the scope of any averaging. A useful success on one task does not establish universal superiority. Keep computational costs and physical resource costs separate until they are converted into a common, justified objective.'),
    small('The criteria in A01-A18 are proposed experiment designs. New application-level measurements are not reported in this companion.'))

page('Energy, material and irreversible action','08 / PHYSICAL ACCOUNTING',
    eq('Delta E = integral(P_in - P_useful - P_loss) dt\nDelta M = integral(mass_in - mass_out) dt\nrecycling: internal transfers cancel in the total boundary'),
    p('State the boundary before writing a balance. Recovered water enters a usable-water reservoir from a waste/process reservoir; it is not new mass for the whole habitat. Thermal memory consumes or redistributes physical energy. Wave tuning and readout may require significant support electronics.'),
    h('A physical state has a history'),
    p('Applied heat remains after a software rejection. Deposited material remains after a failed inspection. An interrupted motion can end between its intended start and finish. Recovery must begin with the actual state, retaining uncertainty until it is resolved.'),
    table([['Application mechanism','Resources and effects to include'],['Material computation','Driver energy, preparation/reset, readout, drift compensation and cooling'],['Photonic/phononic processing','Source, tuners, transducers, loss, detection, conversion and control'],['Adaptive mechanics','Mechanical work, elastic storage, damping, holding and service life'],['Fabrication/repair','Feedstock, purge, waste, curing, inspection and rework'],['Distributed operation','Communication, local computation, travel, standby and recovery']],[1.35,3.8]),
    p('The name Perpetuum Mobile describes continuing causal operation in this architecture. Useful physical operation still needs a supplied and accounted resource flow. A recurring digital state does not establish unlimited physical endurance.'),
    small('PM 1.0 pp. 14, 26-27 and 30 specify the corresponding continuation and interface conditions.'))

page('SEED, state and experimental memory','09 / REPRODUCIBILITY',
    eq('digital replay = seed + immutable descriptor + initial state\n               + ordered input transcript + numeric rules\nphysical repeatability = prepared state + calibration\n                      + measured disturbances + uncertainty'),
    p('A seed can choose stimuli, procedural geometry, task order, optimization initialization and controlled simulation scenarios. Use stable logical identities for its streams; do not derive them from changing worker IDs or network arrival order.'),
    p('The complete PPM-SEED-v1 construction is retained in the embedded PM 1.0 package. It fixes byte framing, SHA-256 domains, counters, range sampling and transcripts. Its fixture results validate that reference construction on the recorded environments; they do not validate the new machines in this book.'),
    h('A minimum useful experiment record'),
    table([['Record','Contents'],['Configuration','Application ID, source/profile hashes, geometry/material/firmware versions'],['Initial state','Digital state and physical preparation with measured tolerance'],['Inputs','Seed-derived draws and actual external measurements with timestamps'],['Actions','Proposals, guards, actual commands, acknowledgments and partial actions'],['Results','Raw readouts, uncertainty, outcome and independent comparison'],['Receipt','Terminal event count, artifact hashes, code/environment and missing evidence']],[1.1,4]),
    p('This companion adds content, source and rendering verification. Existing seed/calculation receipts remain source evidence with their original scope. No new claim of physical validation follows from the PDF passing editorial or integrity checks.'),
    small('Hash consistency supports comparison with a known expected artifact. Unsigned hashes do not authenticate authorship or establish that a measurement is true.'))

page('A research portfolio with dependencies','10 / SYNTHESIS',
    table([['Research cluster','Applications','Shared bottleneck'],['Embodied surfaces','A02, A03, A06, A11, A15','Calibration under changing load, contact, temperature and shape'],['Wave/material computation','A02, A04, A07, A18','Useful signal processing after conversion, drift and control overhead'],['Fabrication and discovery','A05, A08, A09, A16, A17','Reliable measurement of what was actually made and what property it has'],['Persistent distributed operation','A01, A10, A12, A13, A14','Maintaining trustworthy state under delay, failure, degradation and resource limits']],[1.4,1.6,2.1]),
    p('The main research opportunity is composition. A geometry system can describe a support, a material system can remember a signal, and a controller can act on a measurement. Combining them becomes useful only when the interfaces preserve the meaning, timing and uncertainty required by the task.'),
    p('The broadest future machine would inspect its surroundings, identify a bounded need, synthesize a change, enact it and verify the outcome. The strongest starting point is an experiment where one uncertain interface can be measured independently.'),
    call('A surface that remembers physically, reshapes mechanically, processes signals optically and coordinates repair is a compelling direction. The hypotheses in this book turn that direction into a set of experiments capable of showing where it works, where it fails and whether it earns its complexity.'),
    small('This is a design and research companion. It is not a novelty determination, production certification, procurement recommendation or a report of completed application hardware.'))

original=json.loads((ROOT/'reply_apps.json').read_text(encoding='utf-8'))
for offset in (0,6,12):
    blocks=[]
    if offset==0:
        blocks += [small('The following is the original assistant application reply preserved as a source witness. Its opening commit receipt refers to ea9941d, the preceding PM 1.0 delivery, not this companion.'),p('These are proposed integrations. My strongest picks for transformative potential are the first three.')]
    for a in original[offset:offset+6]:
        blocks += [h(str(a['id'])+' / '+safe(a['title'])),p(safe(a['text']))]
    if offset==12:
        blocks += [small('<b>The most distinctive combination:</b> a surface that can remember physically, reshape mechanically, process signals optically and coordinate its own repair.'),small('Your framework could provide the common language connecting those capabilities. Improvements in efficiency, reliability or autonomy would still need comparison with conventional implementations.')]
    page(f'Original reply / {offset+1}-{offset+6}','APPENDIX / CONVERSATION WITNESS',*blocks)

# Group repeated primary sources while retaining every in-chapter identifier.
refs={}
for a in apps:
    for r in a['references']:
        key=r['url'].rstrip('/')
        if key not in refs:refs[key]=dict(ids=[],title=r['title'],url=r['url'],support=r['support'],boundary=r['boundary'])
        refs[key]['ids'].append(r['id'])
refs=list(refs.values())
(ROOT/'references.json').write_text(json.dumps(refs,indent=2,ensure_ascii=False),encoding='utf-8')
ref_groups=[refs[offset:offset+5] for offset in range(0,len(refs),5)]
if len(ref_groups)>1 and len(ref_groups[-1])<=2:
    ref_groups[-2].extend(ref_groups.pop())
for group_index,group in enumerate(ref_groups):
    blocks=[small('Primary component sources checked 15 September 2026. Chapter equations and complete PM integrations are proposals unless a specific result is attributed. A component paper does not validate an entire application.')]
    for r in group:
        blocks += [h(' / '.join(r['ids'])),p(safe(r['title'])+f' <link href="{html.escape(r["url"],quote=True)}" color="#007C88">Source</link>.'),small('<b>Supports:</b> '+safe(r['support'])+'<br/><b>Boundary:</b> '+safe(r['boundary']))]
    page(f'Component research / {group_index+1}','REFERENCES',*blocks)

source=json.loads((ROOT/'source_manifest.json').read_text(encoding='utf-8'))
page('Provenance and editable package','PROVENANCE',
    p('<b>Framework attribution:</b> Tom Klootwijk / NL200678942.<br/><b>Edition:</b> Frontier Applications A1.0, 15 September 2026.<br/><b>Preparation:</b> Codex-assisted expansion of the preceding assistant reply, using the supplied framework and primary component research.'),
    h('Normative base specification'),
    p('Perpetuum Mobile PM 1.0 / 38 pages. The exact original is embedded as a source witness, including its nested four-source package. All PM page references in this companion refer to that edition.'),
    eq(source['base_specification']['sha256'][:32]+'\n'+source['base_specification']['sha256'][32:]),
    h('Original reply witness'),
    p('original_reply.md preserves the prior reply including its historical commit link. Its exact SHA-256 is:'),
    eq(source['conversation_reply']['sha256'][:32]+'\n'+source['conversation_reply']['sha256'][32:]),
    h('Package contents'),
    p('Embedded files include this book\'s editable Markdown and JSON, all eighteen structured application chapters, bibliography, builder, original reply, source/attachment manifests, cover image and exact imagegen prompt. The base PM 1.0 PDF is embedded unchanged.'),
    small('The cover was generated with the built-in image_gen tool; its asset and prompt are retained in the repository. Native vector process diagrams are explanatory layouts. Integrity records are unsigned and are not claims of independent authorship verification or scientific validity.'))

(ROOT/'content.json').write_text(json.dumps(pages,indent=2,ensure_ascii=False),encoding='utf-8')
print(f'Assembled {len(pages)} pages, 18 expanded applications, {len(refs)} distinct primary references.')
