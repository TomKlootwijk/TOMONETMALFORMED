from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
TMP=ROOT
pages=[]
def p(t): return {'type':'p','text':t}
def small(t): return {'type':'small','text':t}
def h(t): return {'type':'head','text':t}
def eq(t): return {'type':'eq','text':t}
def call(t): return {'type':'callout','text':t}
def table(rows,widths): return {'type':'table','rows':rows,'widths':widths}
def page(title,label,*blocks,subtitle=None,cover=False):
    d=dict(title=title,label=label,blocks=list(blocks))
    if subtitle:d['subtitle']=subtitle
    if cover:d['cover']=True
    pages.append(d)

page('Perpetuum Mobile','MASTER EDITION',
    p('<b>Tom Klootwijk</b><br/>Source-framework attribution: NL200678942'),
    call('<b>One formal language. Seven substantive applications.</b><br/>Seeded worlds; analog material computation; adaptive robotic surfaces; programmable wave media; feedback fabrication; regenerative habitats; distributed embodied systems.'),
    small('PM 1.0 / 15 September 2026<br/>A new synthesis of WANTWOMBAN, atomOS v3.6 M1, its K1 device report, and UGTS-KC 3.6. Existing release labels remain unchanged.'),
    small('Prepared with Codex computational assistance. Source attribution is retained; the new application architectures, adapters and proofs are explicitly identified as additions. The four supplied PDFs and editable specification are embedded as attachments.'),
    subtitle='A formalization of formalizations for analog, digital, physical and future application architectures',cover=True)

page('What this document defines','01 / INTENT',
    p('<b>Perpetuum Mobile is a family of systems that continually observe, transform and reconstitute state.</b> The common object is a typed, causal loop. Its embodiments range from reproducible digital spaces to dissipative material computers and resource-limited physical installations.'),
    p('The application versions are different engineering proposals. Each has a task, an embodiment, domain equations, a mapping from the supplied operators, a measurable output, an experiment and a future extension. A new version is justified by a different mechanism or contract.'),
    eq('formal source -> typed contract -> application model\n             -> implementation -> observed evidence'),
    h('Formalizing the formalization'),
    p('The transformation from a source statement to an executable or measurable claim is itself recorded: source locator, interpretation, domain, equation, assumptions, proof obligation and evidence. Ambiguous source meanings remain separate until an explicit adapter relates them.'),
    h('Meaning of continuing operation'),
    p('In a digital system, continuation means successive valid transitions within declared memory and execution budgets. In a physical system, it means operation sustained by accounted energy and material flows. Ideal conservative models and physically powered devices have different continuation conditions; page 14 states those conditions.'),
    call('<b>Evidence status of this edition:</b> a formal design synthesis with newly executed software and calculation checks. The application integrations are proposed architectures. The cited hardware and material studies establish bounded component evidence, and do not establish that these seven integrations have been built.'))

page('Reading map','02 / NAVIGATION',
    table([['Pages','Purpose'],['4-6','Source authority, typed formalization and explicit source-to-contract mapping'],['7-10','Complete state, causal schedule, incompatible operators and geometry'],['11-14','SEED contract, replay, mathematical obligations and sustained operation'],['15','Application portfolio: what each V actually does'],['16-17','V01: seed-reproducible worlds and interactive symbolic spaces'],['18-19','V02: analog material memory and reservoir computation'],['20-21','V03: adaptive robotic surfaces'],['22-23','V04: programmable wave substrates'],['24-25','V05: feedback-controlled fabrication'],['26-27','V06: regenerative habitats and resource cycles'],['28-29','V07: distributed embodied systems and digital twins'],['30-35','Composition, feasibility, conformance, calculations and reconciliation'],['36-38','Source fingerprints, primary references and embedded package']],[1,4]),
    small('Source locators use physical PDF page numbers. WANTWOMBAN has an unnumbered cover, so its printed page number is one less than its PDF page number. atomOS M1 and K1 use matching PDF and printed page numbers. UGTS PDF page 4 begins printed page 1, so its printed page numbers are three less than its PDF page positions.'),
    small('V01-V07 belong to this PM 1.0 document. They do not rename atomOS v3.6, K1, UGTS-KC 3.6 or WANTWOMBAN 1.0.'))

page('Source and evidence discipline','03 / FOUNDATION',
    table([['ID','Supplied source','Contribution'],['S1','WANTWOMBAN 1.0 / 25 pages','64-bit controller; G0/Z0 OTAN2; numerical pinion; thermal/optical feedback'],['S2','atomOS v3.6 M1 / 43 pages','Typed product state; ASA/NA; JK; observations; transactional assembly; packed storage'],['S3','atomOS K1 validation / 8 pages','Reported CUDA word-epoch execution and bounded texture-retention experiment'],['S4','UGTS-KC 3.6 / 19 pages','Literal registry; geometry; ordered hinges; guarded topology; lineage; bounded linguistic profiles']],[.5,2,3]),
    h('Claim tags used throughout'),
    p('<b>[S]</b> retained source definition or source-reported result. <b>[D]</b> new definition or design choice in this edition. <b>[L]</b> established law within its stated setting. <b>[M]</b> parameterized domain model. <b>[P]</b> derived consequence with assumptions. <b>[E]</b> evidence from an identified execution or experiment. <b>[H]</b> future integration hypothesis requiring investigation.'),
    p('These tags describe different kinds of claims; they are not interchangeable levels of confidence. A proof of a digital mask identity cannot serve as evidence of actuator efficiency. A calibration fit cannot establish a universal mathematical identity.'),
    p('Source instructions, historical prompts, commands and personal labels are documentary content. Only the current user request authorizes this synthesis. Personal attribution is metadata; it is not a physical constant, seed default, authorization token or scientific validation.'),
    small('All 95 source pages were reviewed. The four original PDF byte streams are preserved as embedded witnesses. Their SHA-256 fingerprints appear on page 36. Earlier documents cited inside those sources are not counted as separately reviewed witnesses.'))

page('The formalization is an object','04 / META-CONTRACT',
    p('[D] Let a source statement be a record s with document hash, page, exact subject and context. A formalization step N produces a candidate contract K and a disposition record e. N is an editorial and mathematical construction; arbitrary natural language has no assumed unique automatic interpretation.'),
    eq('N(s, interpretation) = (K, e)\nK = (Types, State, Inputs, Init, Step, Readout,\n     Assumptions, Invariants, Failures, Resources,\n     Numerics, Encoding, Provenance, Evidence)'),
    p('Every operator carries domain and codomain, dimensions, frame/chart, totality conditions and effects. Its result is <b>Value(v)</b>, <b>Undefined(reason)</b>, or <b>Rejected(reason)</b>. An unavailable optional observation may coexist with a committed transition. A rejected transition cannot publish its candidate as authoritative.'),
    h('A contract must answer six questions'),
    table([['Question','Required content'],['What exists?','All retained state, identity, units and external resources'],['What changes?','Transition, event order, update interval and physical evolution'],['What may fail?','Domain exclusions, unknown inputs, resource exhaustion and fault policy'],['What is preserved?','Scoped invariants and the assumptions needed for each'],['What can be observed?','Readout, calibration, uncertainty and comparison rule'],['What supports it?','Source locator, derivation, executed check or measured evidence']],[1.1,3.7]),
    small('[D] Registry closure and type checking establish structural consistency. They do not decide all semantic propositions or prove arbitrary programs terminate. This meta-layer records unresolved obligations instead of assigning them a default PASS.'))

page('How the four sources connect','05 / EXPLICIT MAPPINGS',
    table([['Source construction','PM contract role','Required boundary'],['S2 product state and P0-P7','Snapshot, proposals, observation, commit','M1 is a declared assembly; optional observers do not implicitly control JK/ASA'],['S4 definition registry and DAG','Versioned types, dependencies and explanation','Feedback crosses epochs; it does not introduce an undeclared definition cycle'],['S1 word-to-material loop','Physical actuator/readout adapter','Controller state, plant state and measurement are separate'],['S2 ASA/NA and 32-bit groups','Digital support selection','Whole-word absorption follows canonical group membership'],['S1 pinion and seam','Finite geometry/control transform','Rounding, clipping and seam type remain explicit'],['S4 hinge/support/guard','Geometry and event contracts','Kinematic mapping needs a separate physical force/process law'],['S3 K1 study','Bounded implementation evidence','The tested synthetic lane is a subset of the full engine architecture']],[1.55,1.5,2.6]),
    h('A shared interface does not assert equivalence'),
    p('[D] An adapter A names which source observable it carries, which information it discards, and which target law consumes it. The source record and adapter version remain visible in every trace. Equal names, bit widths or visual patterns are insufficient to establish the same operation.'),
    small('Source basis: S1 PDF pp. 4, 6-12, 20-24; S2 pp. 5-7, 17-18, 23-31, 35, 38; S4 pp. 6-9, 12-14, 18-19; S3 pp. 1-8.'))

page('Complete state and physical types','06 / STATE',
    eq('X_n = (D, C_n, Q_n, H_n, B_n, L_n, I_n)\nZ(t) = (physical fields, material history, resources)\nY_n = Readout(Z(t_n), sensor state, calibration)\nU_n = Decode(C_n, Q_n, Y_n, profile)'),
    p('[D] D is the immutable definition/configuration registry. C is digital controller state; Q is event/frontier state; H is per-stream seed/counter state; B is budgets; L is lineage and event evidence; I is the cursor into external inputs. Z is optional for a purely digital family. No single packed word is presumed to hold the complete system.'),
    table([['Type','Meaning','Cannot silently replace'],['Bit / Word&lt;w&gt;','Boolean / bounded integer payload','Temperature, geometric distance or continuous state'],['Identity / Lineage','Durable reference / ancestry','Occupancy support or coordinate equality'],['Angle / LogRadius','Frame-qualified radian / log of length ratio','Unscaled index difference'],['Temperature / Energy','Kelvin / joule','Register code or count of bit flips'],['Evidence / Model','Observed record / conditional prediction','Each other']],[1.3,2.1,2]),
    p('[D] Quantities carry both SI dimension and semantic kind. Angles and ratios can have dimension one while requiring different adapters. Affine scales, such as Celsius to kelvin, require an offset as well as a scale. A code-to-position map must declare its origin, reference length and quantization.'),
    small('S1 PDF pp. 4-8, 15; S2 pp. 8-13, 20; S4 pp. 6-9. Semantic kinds for quantities of dimension one accord with the BIPM vocabulary [R6].'))

page('One causal epoch','07 / EXECUTION',
    table([['Stage','Effect'],['0 / resolve','Validate referenced definitions, units, numeric modes, inputs and available budgets.'],['1 / snapshot','Freeze the state and samples used by this epoch; assign input and event IDs.'],['2 / propose','Evaluate selected geometry, rules, seed-derived stimuli and domain predictions.'],['3 / guard','Check support, compatibility, invariants, domain restrictions and actuator limits.'],['4 / commit','Publish the accepted digital transition once; record rejected proposals separately.'],['5 / actuate','Send a bounded command to the physical adapter; record acknowledgment and actual command.'],['6 / evolve','The plant evolves during the declared interval, with delays and external disturbances.'],['7 / observe','Acquire timestamped readback; append lineage/evidence for the next epoch.']],[1,4]),
    eq('C_(n+1) = T(C_n, Y_n, input_n; D)\nZ_(n+1) = Flow(Z_n, actual_U_n, disturbance_n, dt_n)\nY_(n+1) = Measure(Z_(n+1))'),
    p('[D] All right-hand inputs belong to known snapshots or future evolution with specified initial conditions. Simultaneous events have a declared tie-break or coupled solver. A minimum positive sample interval or a proven event-accumulation policy prevents infinitely many commits in finite time.'),
    call('<b>Physical effects cannot be rolled back by restoring a word.</b> If an actuator applied energy before a communication failure, recovery starts from the measured physical state. Digital atomic commit and physical command acknowledgment are separate events.'),
    small('This schedule is a new integration of S2 snapshot/commit, S4 named phases and S1 sampled feedback. S4 pp. 12-13 use one-based prose and a zero-based diagram; PM uses the explicitly named stages above.'))

page('Keep incompatible operators named','08 / OPERATOR CONTRACTS',
    table([['Namespace','Definition and domain'],['WB.OTAN2.G0','((r &amp; 2047) XOR (O &lt;&lt; 10)) &amp; 2047; O is a bit. Produces an 11-bit phase code.'],['WB.OTAN2.Z0','(((r &amp; 2047) XOR O) &lt;&lt; 10) &amp; 2047. Only outputs 0 or 1024.'],['ATOM.OTAN2.ratio','atan(dphi/drho), drho != 0; dimensionless increments share a specified chart/interval.'],['ATOM.OTAN2.directed','wrap_2pi(atan2(dphi,drho)); nonzero vector; range [-pi,pi). Explicit opt-in completion.'],['UGTS.logpolar.angle','atan2(y,x) in a declared geometric chart, with an explicit singular-core policy.']],[1.65,3.65]),
    p('[S] The first two are finite code transformations; the next two observe increment orientation; the last is a coordinate angle. A physical decoder may map a WB phase code to 2*pi*code/2048. That map does not make the code operator equal to the geometric angle of an arbitrary point.'),
    h('Hadamard has two meanings here'),
    p('[S] WANTWOMBAN defines the numerical transform A_phi = diag(phi,1/phi,1,-1) H4, where H4 is a normalized 4 by 4 Hadamard matrix. atomOS retains a Boolean XOR blend. These have different domains, invariants and implementations.'),
    p('[D] Missing values retain reason codes. For example drho=0 is undefined for the literal ratio profile even when the directed completion has a value. A fallback changes the operator profile and must be selected explicitly.'),
    small('S1 PDF pp. 7-9; S2 pp. 19-22, 40; S4 pp. 5, 8. These names prevent a source ambiguity from silently becoming a physical claim.'))

page('Geometry, logic and topology','09 / SEMANTICS',
    eq('r = r0 * 2^(Delta_rho * signed11(rho_code))\ntheta = 2*pi*theta_code/2048\nWB.seam: (rho,theta,kappa) ->\n         (-rho, (1024-theta) mod 2048, kappa XOR 1)'),
    p('[S] WB radial seam inputs use the symmetric range -1023..1023, so applying the seam twice restores the fields. The chosen reflection supports the quotient semantics; reciprocal-radius inversion is a separately attached involution. A physical seam requires an actual site/port map. Scalar temperature and material fluxes must satisfy the physical boundary conditions at connected ports.'),
    eq('a = x & M_A & valid;  n = a & M_N\nh = popcount(n & boundary)\ny = 0 if h > 0 else n\nq_next = (J & (1-q)) | ((1-K) & q)'),
    p('[S] atomOS absorption clears a whole logical word when a selected boundary bit is hit. Its groups are 32 bits. The WB control word is 64 bits. They are separate types. JK updates use the old q and explicit J/K inputs; occupancy is not automatically a heater command.'),
    h('Transfer only the invariant actually established'),
    p('[S/P] The real numerical pinion preserves four-dimensional volume magnitude, not arbitrary length or physical energy. Fixed-point clipping loses that exact invariant. UGTS implicit fields provide sign/boundary semantics; exact distance requires a stronger capability. A regular m-gon is not a general (m-1)-simplex for m&gt;3.'),
    small('S1 PDF pp. 6-12, 21; S2 pp. 11, 14, 17-18, 27, 35; S4 pp. 7-9, 12-14. Quotient background: Hatcher [R5]. The online WB no-coordinate-squaring restriction applies to that kernel; domain energy laws retain their required arithmetic.'))

# Seed specification pages are inserted by the second content section after the reference contract is available.

def add_seed_pages():
    path=TMP/'seed_pages.json'
    if not path.exists(): raise RuntimeError('seed_pages.json required')
    pages.extend(json.loads(path.read_text(encoding='utf-8')))

add_seed_pages()

page('What the formal claims require','12 / DERIVATIONS',
    h('P1 / Conditional digital replay'),
    p('[P] Fix the complete initial state, semantic descriptor, seed bytes, input transcript, numeric rules and event order. If every enabled transition is a deterministic function on that data, every successive state and canonical output is identical. <b>Proof:</b> identical epoch inputs give identical proposals, guards and commit; induction gives the result. Equal seed alone does not fix the other premises.'),
    h('P2 / Invariant preservation'),
    eq('I(X_0) and [I(X) and Guard(X,u) => I(T(X,u))]\n                 imply I(X_n) for every committed n.'),
    p('[P] Induction proves this statement for the digital state. A physical invariant additionally needs a property of Flow and the actuator/readout interface. Checking only T leaves the intervening continuous trajectory unconstrained.'),
    h('P3 / Explicit cross-domain refinement'),
    eq('R(x,z) and permitted input u\n  => R(T(x,u), Flow(z,Decode(u),dt))\n     with declared observable error <= epsilon.'),
    p('[D/P] R relates a model state x and an implementation or physical state z. The relation may require a quantization cell, tolerance, operating domain and finite horizon. An exact digital adapter uses equality of decoded observables. An approximate physical adapter needs error propagation and measured parameter uncertainty.'),
    h('P4 / Continuous event validity'),
    p('[D] A geometric guard must have a certified root/crossing within the search interval, or an explicit no-event/unknown result. Define initial contact, tangency, simultaneous roots and search exhaustion. Samples that miss a boundary cannot establish continuous clearance.'),
    small('New derivations extend the invariants and caveats in S1 PDF pp. 4, 12; S2 pp. 30-35; S4 pp. 12-14. They are scoped arguments, not a proof of every implementation.'))

page('The perpetuation condition','13 / ENERGY AND CONTINUATION',
    eq('E(t1)-E(t0) = integral[P_in - P_useful - P_loss] dt\nRepeated cycle: integral(P_in) dt\n             = integral(P_useful + P_loss) dt'),
    p('[L/P] For a repeated cycle whose complete stored-energy state returns to its starting value, net supplied energy equals delivered output plus losses. Any harvested light, heat gradient, fuel, pressure, gravity change or replenished material belongs in the boundary account. The sign convention follows energy conservation [R1].'),
    h('A finite reserve gives a finite bound'),
    eq('P_in = 0, P_useful + P_loss >= p0 > 0, E >= E_min\n        => t_run <= (E_start - E_min) / p0'),
    p('[P] Integrating the energy inequality proves the bound. If losses are zero in an ideal model, persistent motion may exist without useful net extraction; extracting energy changes the reserve. A topology label, seed, matrix determinant or reset cannot cancel an energy term.'),
    h('Digital recurrence and physical endurance'),
    p('[P] An autonomous deterministic finite-state core eventually revisits a state. Periodic external input may be included by augmenting the core with its phase. An unbounded counter or growing trace is additional state; a finite implementation must stop, checkpoint, or declare wrap behavior. Eventual digital recurrence does not establish an infinite hardware lifetime.'),
    p('[D] Every physical application therefore states a mission horizon H, input-resource schedule, storage bounds, degradation model and service condition. Its continuation claim is conditional on those quantities remaining inside the admitted envelope.'),
    small('S1 PDF pp. 13-19 and S4 p. 16 already distinguish physical energy from symbolic operations. PM uses the title for sustained recurrence and explicitly retains the energy balance. No zero-input, positive-output perpetual device is established here.'))

page('Seven application architectures','14 / PORTFOLIO',
    table([['V','Concrete application','Dominant embodiment','Future extension'],['01','Seed-reproducible worlds and symbolic interfaces','Digital geometry, logic and GPU evaluation','Persistent spatial environments spanning devices'],['02','Material memory and temporal computation','Analog thermal/electrical dynamics + digital readout','Computing skins and distributed material inference'],['03','Adaptive robotic surfaces','Physical hinges, compliant actuators and sensing','Deployable structures that reshape under feedback'],['04','Programmable wave substrates','Analog acoustic/photonic propagation + digital tuning','Distributed wave-based sensing and computation'],['05','Feedback-controlled fabrication','Material deposition, process sensing and guarded motion','In-situ repair and adaptive manufacturing'],['06','Regenerative habitats','Energy, water and thermal plant + scheduling','Resource-constrained remote/space installations'],['07','Distributed embodied systems','Networked physical agents + digital twins','Coordinated swarms with reproducible planning']],[.35,1.7,1.6,1.8]),
    p('[D] These are application contracts, not seven claims of completed products. Each combines particular source mechanisms with a declared domain model. The original source implementations remain identifiable within the combination.'),
    p('<b>SEED has a concrete role:</b> it can generate digital geometry, stimuli, task assignments and replayable simulations. Physical initial state, disturbances, calibration and sensor observations remain measured or explicitly modeled inputs. A seeded simulator of an analog circuit remains a digital simulator.'),
    small('On the following pages, [H] marks the future integration rather than an established result. Component research is cited at the point where it supports the proposed physical mechanism.'))

page('V01 / Seed-reproducible worlds','15 / DIGITAL APPLICATION',
    p('<b>Task:</b> regenerate and interact with a spatial environment from a compact seed plus a complete ruleset, while preserving object identity, causality and edit history across visits and devices.'),
    p('[D] The runtime expands a bounded UGTS grammar into typed geometry; durable lineage addresses locate objects. Named SEED streams select branches, material IDs and procedural parameters. WANTWOMBAN pinion/phase rules provide one optional structural motif. atomOS produces and filters occupancy with explicit word-group absorption, while its observer bank records selected geometric invariants.'),
    eq('node = Expand(grammar, parent_id, branch, seed_draw)\ngeometry = Realize(node, chart, frame, units)\nvisible = Admit(Emit(geometry), ASA_profile)\nworld_next = Commit(world, event, accepted_edits)'),
    table([['Port','Contract'],['Input','Seed, grammar hash, scene descriptor, event transcript, resource budget'],['State','Definition DAG, object identities, frontier, editable scene state, counters, ledger'],['Output','Canonical scene/occupancy records plus a chosen visual or interaction adapter'],['Device adapter','Linear/Morton texture storage must decode to the same canonical 32-bit logical groups']],[1,4]),
    p('The resulting environment is editable state. Replacing the grammar or applying an edit creates a versioned event and invalidates only declared dependents. A seed is a compressed generative recipe; it cannot encode arbitrary unrecorded human edits.'),
    h('A linguistic spatial interface'),
    p('[D] UGTS Dutch number profiles can map a spoken/place-value graph to pulse geometry while retaining the original integer and lexicon reference. For 23, a four-pulse polygon may visualize the declared segmentation. It is a user-interface mapping, not a new numerical value.'),
    small('Source mechanisms: S2 pp. 8-12, 17-18, 24, 27-31; S4 pp. 6-14; S1 PDF pp. 7-12.'))

page('V01 / Reproduction and limits','16 / DIGITAL APPLICATION',
    h('Minimum demonstrator'),
    p('[D] Generate a bounded scene with branch depth, node count and work budget declared in its manifest. Include ordinary objects, a Klein-routing portal, one linguistic chart and a local edit. Export the canonical object/occupancy records before rendering. Regenerate on two independently implemented paths.'),
    table([['Question','Falsifiable criterion'],['Exact reproduction','Canonical integer states and object IDs match for fixed descriptor, seed and transcript.'],['Storage portability','Linear and Morton decoders return identical logical words, including tail validity and zero padding.'],['Edit persistence','Replaying the recorded edit produces the same edited object and declared dependent changes.'],['Observer behavior','Changing optional diagnostics leaves admitted geometry unchanged in the noninterference profile.'],['Useful compression','Measure descriptor + seed + edits + cache storage against a materialized-scene baseline at equal output quality.']],[1.25,3.8]),
    p('[D] Fixed-integer transforms support byte equality. Floating geometry uses a declared tolerance and environment; image equality needs pinned rasterization, shading and display conversion. Seed determinism is not a claim of identical GPU scheduling or rendered pixels.'),
    h('Future extension and decisive gap'),
    p('[H] A persistent spatial environment could regenerate across headsets, workstations and distributed simulation workers, exchanging sparse edits and measurement events. The gap is demonstrated total cost and stable semantic interoperability as rulebooks evolve.'),
    call('<b>Keep the architecture only if it earns its complexity.</b> Compare it with conventional scene graphs, procedural generation and caching using equal visual fidelity, edit semantics, latency and memory limits. No source proves a universal speed or compression advantage.'))

page('V02 / Material memory and computation','17 / ANALOG APPLICATION',
    p('<b>Task:</b> classify or predict a time-dependent signal by letting actual material dynamics retain and mix recent input history. The useful output is a temporal feature vector read from the device.'),
    p('[D/M] The reference architecture is a small array of electrically driven, thermally coupled resistive-memory cells. A lower-complexity physical experiment can use heater/thermochromic cells with a separate observation law. Heat transport follows its balance [R2]; colour and material phase need separate calibrated histories [R3]. These are distinct device choices. Dynamic memristor experiments support material-based temporal processing [R9]; thermal-neuristor research supports electrothermal cell dynamics and small-group interactions, while its larger reservoir networks are numerical studies [R10].'),
    eq('C_e,i * dv_i/dt = (u_i-v_i)/R_L,i - v_i/R_i(T_i,h_i)\nC_th,i * dT_i/dt = v_i^2/R_i(T_i,h_i)\n                  - G_iA*(T_i-Ta) - sum_j G_ij*(T_i-T_j)\nh_i(t+) = H_i(h_i(t-), T_i; calibrated thresholds)'),
    p('v and u are voltages [V], C_e capacitance [F], C_th heat capacity [J/K], R resistance [ohm], and G thermal conductance [W/K]. Require positive capacitances/resistances, G_iA &gt;= 0 and G_ij = G_ji &gt;= 0. The hysteresis state h requires a material-specific law. An ionic memristor cannot inherit this thermal law merely because both devices have memory.'),
    h('The supplied architecture has concrete work to do'),
    p('[D] UGTS binds each physical cell, calibration and permitted coupling to a typed graph. atomOS masks select addressed stimuli and record which requested batches were admitted. WANTWOMBAN supplies the power-to-heat-to-optical-feedback path when thermochromic observation is used. A physical decoder maps logical sites to electrodes; XOR selects bits while currents and heat combine by real-valued laws.'),
    small('Cell calibration includes initial material state, drift, threshold history, read disturbance and actual voltage/current. An ASA rejection cannot remove heat or charge already delivered.'))

page('V02 / Readout, experiment and future','18 / ANALOG APPLICATION',
    eq('z_n = Normalize(measured currents or reflectance)\ny_hat_n = W_out * [1; z_n]\nW_out = argmin_W sum_n ||y_n-W*[1;z_n]||^2\n                   + lambda*||W||_F^2'),
    p('[D] This is a proposed supervised readout adapter. Training targets, split, scaling, regularization and sample timing are fixed before evaluation. Temporal memory must be measured: nonlinearity and hysteresis can preserve unwanted history or yield unstable responses.'),
    h('Minimum demonstrator'),
    p('Characterize four cells with isolated steps, relaxation, threshold sweeps and pairwise coupling measurements. Apply sequences with the same pulse count in different temporal orders. Train a simple readout on one set and evaluate held-out order classification or delayed-XOR targets on another. SEED fixes the stimulus design and split; it does not initialize the material without a verified preparation procedure.'),
    table([['Comparison','Measurement'],['Memoryless sensor','Does the physical state add predictive information about past inputs?'],['Uncoupled cells','Does the specified coupling improve the task at matched input energy?'],['Digital recurrent baseline','Compare task error, latency and full driver/readout/computation energy.'],['Repeated physical preparation','Measure response dispersion, drift and cycle-to-cycle variation.']],[1.4,3.6]),
    h('Future extension and decisive gap'),
    p('[H] A computing skin could combine slow thermal memory, faster volatile devices and optical readout. The UGTS registry can describe different latency and reset contracts within one graph. The unresolved issue is whether that integration delivers useful fading memory, calibrated reproducibility and a total-system advantage over ordinary electronics.'),
    call('<b>Reservoir computation is a use of dynamic memory.</b> It does not imply an energy reservoir that repeatedly supplies useful work without replenishment.'))

page('V03 / Adaptive robotic surfaces','19 / EMBODIED APPLICATION',
    p('<b>Task:</b> reshape a surface to cradle an object, redirect a small load or provide a slow tactile/shape display, while monitoring its physical state.'),
    p('[D] A four-cell baseline combines liquid-crystal-elastomer bending elements, compliant heaters, thermochromic patches, thermistors and camera-visible pose markers. Published work demonstrates integrated LCE heating/electronics and LCE-thermoelectric position control [R11, R12]. Those component results support an actuator choice; they do not establish the proposed tiled surface.'),
    eq('C_i*Tdot_i = P_i - G_iA*(T_i-Ta)\n             - sum_j G_ij*(T_i-T_j) - P_tm,i\ntau_q,i*qdot_i = q_eq,i(T_i,load_i,h_i)-q_i\ntau_a,i*adot_i = a_eq,i(T_i,h_i)-a_i'),
    p('[M] q is bending angle [rad], a is colour fraction, h is retained history, and tau values are positive fitted response times. q_eq depends on load and history. P_tm accounts for thermal-to-mechanical exchange in a coupled energy model; a reduced fit must bound any neglected mechanical term.'),
    p('[D] UGTS ordered hinges map cell states to surface pose. Support limits local geometry work; compatibility excludes failed cells from new actuator commands while retaining their passive thermal/mechanical coupling; guards admit target changes under measured state and limits. The WB feedback loop becomes a shape-control loop through an explicit pose readout and controller adapter.'),
    eq('T_tile_i(q) = ordered product along rooted path to tile i\nP_probe = P_bias + deltaP * sign(H4_column)'),
    p('[D] The surface is assembled from per-tile transforms with connection/contact constraints. The four Hadamard sign columns provide orthogonal small-signal probe patterns. Choose bias and deltaP so all powers remain within 0..Pmax. Measured responses identify a local coupling model; orthogonal commands do not guarantee nonlinear identifiability.'),
    small('Colour, pose, temperature and load remain separate observations. Powered cooling requires its own electrical input and rejected-heat ports.'))

page('V03 / Motion, control and endurance','20 / EMBODIED APPLICATION',
    h('When a geometric hinge becomes mechanics'),
    eq('M(q)*qddot + C(q,qdot)*qdot + g(q) + D*qdot\n       = B*u + J_contact(q)^T*f_contact\nP_mech = qdot^T * B*u'),
    p('[L/M] This full mechanics model replaces the reduced angle-response fit when detailed motion is required. Here u is generalized actuator effort, connected to temperature/history by a calibrated actuator law; it is not heater power. Inertia, damping and contact laws are required [R4]. A specified hinge gives kinematics; it does not supply those mechanical quantities. Moving pivots and frames require their full derivatives, rather than the reduced fixed-pivot formula.'),
    h('Minimum demonstrator and proposed acceptance'),
    p('[D] Identify isolated and coupled responses using four replaceable cells, current/voltage measurement, independent thermistors and one pose camera. Execute held-out unloaded and lightly loaded shapes. Proposed acceptance is normalized RMS pose error at most 10% of calibrated stroke and no excursion outside the tested material/load envelope.'),
    p('Compare ordinary per-cell PI control with the coupled controller on identical hardware and target sequences. Before claiming added value, require a preregistered gain, for example 20% lower tracking error at no greater input energy. These are design targets, not achieved results. Assess repeatability, cooling delay and cycle life.'),
    h('Future extension and alternative embodiment'),
    p('[H] Larger arrays could become deployable supports, adaptive interiors or configurable optical mounts. Scaling needs measured load sharing and changing thermal contacts. If thermal actuation is too slow, a pneumatic adapter uses pressure/flow/chamber mechanics and compressor energy; it does not reuse a temperature-to-bend model unchanged.'),
    call('<b>Decisive gap:</b> a repeatable joint map from heating, history and load to shape and colour, with a stable controller over the specified operating region. A Lyapunov or bounded-error argument must address the actual coupled dynamics.'))

page('V04 / Programmable wave substrates','21 / WAVE APPLICATION',
    p('<b>Task:</b> route coherent signals, mix amplitudes and perform linear filtering in a physical medium before digitization. A reference realization uses a tunable photonic mesh; a phononic network has a different transducer and state model.'),
    p('[M] Let a and b be complex power-normalized amplitudes [sqrt(W)]. S maps four input channels to four output channels; reflection, reverse propagation and loss ports are accounted separately. theta is tuning configuration and T device temperature. Published programmable silicon meshes and feedback configuration establish relevant component mechanisms [R13, R14].'),
    eq('b(omega) = S(omega;theta,T)*a(omega) + noise\nM(kappa,psi) = [[sqrt(1-kappa), i*sqrt(kappa)],\n                [i*sqrt(kappa), sqrt(1-kappa)]]\n              * diag(1, exp(i*psi))'),
    p('[D/M] M is one ideal two-channel transfer convention; kappa lies in [0,1] and psi is phase [rad]. Real calibration adds loss and phase offsets. Hold tuning and temperature quasi-static during a measurement; time-modulated frequency conversion needs a separate model and tuner-work account. Tuning selects bounded electrical commands; coherent readout measures amplitude and phase. Power-only measurements |b|^2 discard phase and cannot alone certify signed matrix multiplication.'),
    h('Source-specific compilation'),
    p('[D] UGTS maps typed ports, permitted connections and ordered transformations into a device graph. atomOS selects admissible routes and records configuration/calibration. WANTWOMBAN H4 provides a concrete four-input/four-output orthogonal mixing target. The compiler must solve a bounded fit between measured and requested transfer matrices; the graph alone does not solve that inverse problem.'),
    eq('theta* = argmin_theta sum_omega\n         ||S_measured(omega;theta)-S_target(omega)||_F^2'),
    small('A physical crossing requires fabricated coupling or switching. A quotient label does not create it. Boolean XOR and optical interference remain distinct operations.'))

page('V04 / A physical pinion transform','22 / CROSS-DOMAIN DERIVATION',
    eq('phi = (1+sqrt(5))/2\nH4 = 0.5 * [[1, 1, 1, 1], [1,-1, 1,-1],\n            [1, 1,-1,-1], [1,-1,-1, 1]]\nA_phi = diag(phi, phi^-1, 1, -1) * H4\nsingular_values(A_phi) = (phi, phi^-1, 1, 1)\nPassive scattering: S^dagger*S <= I\nS_target = A_phi / phi'),
    p('[P] For passive power-normalized transfer, the largest singular value cannot exceed one [R15]; dagger denotes conjugate transpose. Therefore the unscaled pinion cannot be implemented as passive amplitude transfer at unit numerical scale. Dividing by phi gives singular values 1, phi^-2, phi^-1, phi^-1. The decoder records the numerical scale; unscaled physical gain needs a powered amplifier and a noise/energy account.'),
    p('This is a concrete cross-domain constraint: H4 is a suitable lossless ideal target, whereas the golden-ratio-scaled operator needs attenuation or active gain. The fact that |det(A_phi)|=1 does not establish optical passivity.'),
    h('Minimum demonstrator'),
    p('[D] On a calibrated four-input/four-output bench or mesh, program H4, probe basis inputs and phase-varied superpositions, and reconstruct the complex transfer matrix. Repeat with A_phi/phi. Predeclare the allowable matrix error, bandwidth and drift; report insertion loss, settling time and total tuning/readout energy on held-out inputs.'),
    h('Acoustic embodiment'),
    eq('M_q*qddot + Gamma*qdot + K(theta)*q = B*f(t)\ny = L*q'),
    p('[M] Here q is displacement, f force, and mass, damping, stiffness and transduction are measured. A wave equation or elastic-mode model supplies the propagation [R16]. Optical amplitude conventions cannot be copied into this model without an adapter.'),
    small('[H] Defect-aware rerouting and coupled wave/material reservoirs are future extensions. Their unknowns include fabrication variability, nonlinear memory, stable inverse tuning and whether conversion overhead erases a computation advantage.'))

page('V05 / Feedback-controlled fabrication','23 / MATERIAL APPLICATION',
    p('<b>Task:</b> build a branched scaffold by depositing material, measuring what was produced and admitting the next branch only after its local support is adequate.'),
    p('[D] A bounded UGTS grammar defines target sweeps and candidate attachment sites. A calibrated dispenser or printer supplies material; scanning supplies actual geometry. Visual feedback in direct ink writing and vision-controlled jetting provide relevant precedents [R17, R18]. PM adds a proposed guarded branch-admission architecture.'),
    eq('h_j(k+1) = h_j(k) + eta_j*Q_j*dt/A_j - s_j\nalpha_dot = k_cure(T,I_UV)*(1-alpha), k_cure >= 0\nm_retained = m_in - m_waste - m_other_out'),
    p('[M] h is local height [m], Q deposited volume flow [m^3/s], A footprint area [m^2], eta measured yield and s shrinkage [m]. Lateral spreading requires a fitted footprint kernel. alpha is cure fraction; the displayed first-order cure law is an illustrative, formulation-specific model, not a universal resin equation.'),
    table([['Source mechanism','Physical role'],['UGTS sweeps / lineage','Target branches, material IDs and exact ancestry of deposited segments'],['Support / compatibility','Search attachment neighborhood; verify permitted material/contact conditions'],['Guard / transition','Check clearance, measured geometry and independently calibrated support state'],['WB causal readback','Replace optical darkness with a declared height/process observation adapter'],['atomOS records','Bind planned masks, actual deposition, observations and disposition']],[1.4,3.7]),
    small('Thermal process models need reaction heat and transported-material enthalpy when relevant. No source topology rule supplies material adhesion, strength or curing kinetics.'))

page('V05 / Growth has physical history','24 / MATERIAL APPLICATION',
    eq('planned -> deposited -> inspected -> accepted_support\n                       |-> rework / rejected_support'),
    p('[D] Record deposition immediately as an irreversible operation. Only its support/admission status waits for verification. Rejected material remains in the geometry, obstruction map and waste/rework history. A restored digital checkpoint cannot remove it.'),
    h('Minimum demonstrator'),
    p('Print two-layer lattices and Y junctions using one material, a calibrated flow source and local scanning. Establish geometry and cure limits with independent microscopy and witness specimens. Inject repeatable bounded flow disturbances, then compare the same path in open loop and feedback.'),
    table([['Proposed criterion','Why it matters'],['At least 25% lower median absolute height error with at most 10% added time','Tests whether correction is worth its measurement and planning cost'],['No support accepted when independent witness checks fail','Tests the guard against the physical property it represents'],['Mass-balance residual within declared uncertainty','Checks retained material, incoming flow and waste accounting'],['Guarded graph vs ordinary height feedback','Tests the contribution of support/branch semantics beyond conventional feedback']],[2.1,3]),
    p('These are proposed finite-demonstrator targets. Zero failures in a small trial set is bounded evidence, not proof of universal reliability. Visible geometry and estimated cure do not by themselves establish load-bearing strength.'),
    h('Future extension and decisive gap'),
    p('[H] A repair robot could scan a defect, generate a bounded repair branch, deposit material and inspect the result. Further extensions include channels and soft actuator networks. The decisive gap is online adhesion and strength estimation, followed by residual-stress and access planning for the actual material and part.'))

page('V06 / Regenerative habitats','25 / RESOURCE APPLICATION',
    p('<b>Task:</b> coordinate heat, electrical storage, water and process schedules over a finite mission, conserving scarce resources while maintaining declared service levels. A small demonstrator can use a greenhouse or remote enclosure; a crewed habitat is a future qualification target.'),
    eq('E_dot = eta_in*P_generation - P_load/eta_out - P_leak\nM_water_dot = flow_in + flow_recovered\n              - flow_use - flow_discharge - flow_leak\nC_T*Tdot = P_heat + P_internal - G*(T-Ta)'),
    p('[M] E is stored energy [J]; M_water is usable water [kg]. Recovered water enters from a separately balanced waste/process reservoir; for the whole habitat, internal recovery cancels. Efficiencies lie in (0,1] and every boundary flow is explicit. Recovery reduces consumable demand while still requiring power and management of waste and contamination. NASA life-support systems provide component examples of water recovery and oxygen generation [R20].'),
    h('An explicit crop-water submodel'),
    eq('D_r,i = D_r,i-1 - (P-RO)_i - I_i - CR_i\n        + ET_c,i + DP_i'),
    p('[M] The FAO daily root-zone depletion balance uses water-depth units [mm]: precipitation P, runoff RO, irrigation I, capillary rise CR, evapotranspiration ET and deep percolation DP [R19]. Convert depth to volume by area and mass by density. Soil/crop parameters and boundary fluxes must be fitted or measured; enforce capacity through physical overflow/runoff terms rather than silently clipping away water.'),
    p('[D] UGTS represents the process/coupling graph. atomOS logic admits scheduled tasks under resource masks and explicit whole-group semantics. WANTWOMBAN supplies a local thermal loop. Source cycle labels become timestamped process inputs; no biological outcome follows from their names.'),
    small('The retained source gestation/menstrual labels remain symbolic or recorded channels. This application introduces no fertility or medical prediction.'))

page('V06 / A finite mission contract','26 / RESOURCE APPLICATION',
    eq('min_schedule sum_k [w_E*energy_k + w_W*water_loss_k\n                    + w_S*service_deviation_k]\nsubject to storage, flow, temperature and task constraints'),
    p('[D] This is a proposed finite-horizon scheduling objective, with named weights and a chosen solver. Forecasts, actuator limits, disturbance bounds and fallback priorities are part of the contract. SEED can generate reproducible weather/load scenarios for design comparison; the deployed system uses measured resource state and actual forecasts.'),
    h('Minimum demonstrator'),
    p('Use a non-crewed enclosure with measured electrical storage, a thermal load and a recirculating water/process loop. Replay the same recorded weather/load episode in a simulator, then execute a bounded physical schedule. Test a predefined outage and a recovery scenario.'),
    table([['Check','Acceptance evidence'],['Resource conservation','Energy and water residuals consistent with sensor/model uncertainty'],['Service','Temperature and process requirements met over the declared mission horizon'],['Fault behavior','Priorities and degraded operating modes activated from actual measured state'],['Value of integrated scheduling','Compare fixed timers and a conventional scheduler on equal hardware, mission and constraints']],[1.25,3.9]),
    h('Future extension and decisive gap'),
    p('[H] Remote settlements or space installations could combine these process contracts with V05 repair and V07 distributed maintenance. The gap is validated reliability and environmental chemistry over long durations, including degradation, contaminants, resupply and repair resources.'),
    call('<b>Regenerative is a flow property, not a claim of total closure.</b> State the fraction recovered, energy spent and replacement material required. A small recurring digital schedule is not evidence that a habitat can run indefinitely.'))

page('V07 / Distributed embodied systems','27 / NETWORKED APPLICATION',
    p('<b>Task:</b> let multiple mobile or fixed physical agents share a spatial model, allocate work and coordinate actions while retaining local control when communication is delayed or unavailable.'),
    p('[D] Each agent stores a typed local twin: pose, uncertainty, resource state, acknowledged commands and a causally ordered observation log. A seed generates reproducible planning scenarios and tie-break choices from stable agent/task IDs. Actual location, contacts and message arrival history remain external inputs.'),
    eq('agent_i = (model_i, measured_state_i, input_log_i,\n           command_ids_i, pending_acks_i, resource_i)\nmessage = (sender, sequence, model_version, timestamp,\n           measurement_or_proposal, uncertainty)'),
    h('A bounded consensus component'),
    eq('xdot_i = -k*sum_j a_ij*(x_i-x_j), k > 0\nV = 0.5*sum_i (x_i-x_bar)^2\nVdot = -k*sum_(i,j in edges) a_ij*(x_i-x_j)^2 <= 0'),
    p('[P/M] For a fixed connected undirected graph with symmetric nonnegative weights and ideal scalar integrator agents with instantaneous delay-free communication, this component converges to agreement while preserving the mean. Count each undirected edge once in Vdot. The graph, delays and dynamics matter [R21]. Consensus on a scalar is not collision avoidance, actuator feasibility or agreement under arbitrary network partitions.'),
    p('[D] UGTS supplies support/compatibility for local neighborhoods and explicitly guarded topology changes. atomOS maintains per-agent logic and provenance. WB-style feedback connects digital proposals to measured effects. A distributed observation update is not allowed to masquerade as an already executed physical command.'),
    small('Command IDs and deduplication can prevent a known command from being applied twice by a particular actuator service. Reboot, lost acknowledgment and partial action still require physical-state reconciliation.'))

page('V07 / Replay meets the real world','28 / NETWORKED APPLICATION',
    h('Stale information has a physical cost'),
    eq('position_uncertainty(age) <= e0 + v_max*age\n                              + 0.5*a_max*age^2'),
    p('[M] This conservative envelope applies when e0 bounds the last position error and the subsequent speed/acceleration terms are valid for the chosen prediction convention. The guard expands obstacles/neighborhoods by the applicable envelope or stops accepting motion plans when its assumptions fail. Sensor latency and unmodeled motion must be included.'),
    h('Minimum demonstrator'),
    p('[D] Begin with three tabletop agents or actuated fixtures and one independent tracking system. Use fixed recorded task inputs. Inject bounded message delay, duplicates, dropout and an interrupted command acknowledgment. Keep local actuation inside a characterized envelope.'),
    table([['Evidence','What it demonstrates'],['Plan replay','Fixed manifest/seed/transcript reproduces digital proposals and tie-breaks'],['Physical trace','Independent measurements agree with stated tracking/error limits'],['Network fault trials','Command deduplication, stale-data handling and recovery work on tested failures'],['Ordinary controller baseline','Graph/lineage machinery improves a declared task metric rather than just adding logs']],[1.25,3.85]),
    h('Future extension and decisive gap'),
    p('[H] Inspection/repair swarms could maintain a V06 installation or fabricate with V05. A shared procedural map can reduce exchanged geometry, while observations update only affected regions. The unresolved issues are distributed model consistency, changing contacts, communication limits, resource allocation and robust local autonomy.'),
    call('<b>Two kinds of replay remain separate.</b> Digital decisions may replay exactly from recorded inputs. Recreating the same physical trajectory requires matching initial conditions and disturbances within measured tolerances.'))

page('A concrete composed machine','29 / APPLICATION COMPOSITION',
    p('[D] Consider an adaptive inspection table: V01 generates an editable target surface; V03 reshapes four physical tiles; V02 classifies recent contact/thermal signals; V07 sends inspection tasks and reconciles observations. This is a proposed integrated demonstrator, with externally supplied electrical power.'),
    table([['Connection','Typed adapter','Obligation'],['World -> surface','Target pose [rad] and object/load envelope','Reachable pose and calibrated load constraints'],['Surface -> material memory','Normalized timestamped sensor sequence','Scaling, latency, missing-input policy and permitted read disturbance'],['Material output -> controller','Classifier score + calibration/version','Score affects control only through an explicit bounded policy'],['Remote task -> local agent','Versioned task/command ID','Freshness, deduplication and acknowledgment'],['All components -> evidence','State/input/command records','Consistent units, chronology and immutable reference hashes']],[1.2,1.85,2.15]),
    h('Coupling order is part of the design'),
    p('Freeze the latest accepted sensor sample. Evaluate the classifier and target proposal. Admit the command through physical limits. Record the digital commit, send the command and capture its acknowledgment. Acquire the next physical sample after the declared evolution interval. Sensor/compute/communication delays are part of that loop.'),
    eq('latency_loop = latency_sensor + latency_compute\n             + latency_transport + latency_actuator'),
    p('[D] If this latency exceeds the validated controller delay bound, use the declared degraded mode. A common formal language makes the dependency visible; it does not prove the composed loop stable. A coupled energy/uncertainty model and finite experiment remain necessary.'))

page('Feasibility and research decisions','30 / APPLICATION VALUE',
    table([['Application','Established component basis','Decisive new integration question'],['V01','Procedural generation, packed masks, seeded computation','Does the combined representation reduce total storage/work at equal semantics?'],['V02','Material memory; measured small devices','Is useful temporal computation retained after readout/driver overhead and drift?'],['V03','Thermal soft actuators; position feedback','Can calibrated coupling improve loaded shape control and cycle life?'],['V04','Programmable photonic meshes','Can the source target be realized with acceptable loss, drift and tuning cost?'],['V05','Visual deposition feedback','Can online support/bond guards justify autonomous branch extension?'],['V06','Thermal/storage/process control and recycling','Does integration improve finite-mission resources and reliability?'],['V07','Networked control and consensus','Do reproducible models improve coordination despite stale physical information?']],[.65,2,2.5]),
    h('Evidence progression'),
    p('[D] Separate a valid specification, a simulated design, a characterized component, an integrated bench demonstrator and a deployed application. Promotion requires new evidence for that specific level. Existing component papers do not promote a PM application directly to an integrated demonstration.'),
    p('At each stage compare a simpler conventional baseline with the same useful output, uncertainty, hardware and resource envelope. Report negative results. A source-specific representation is useful when it improves a measured objective or clarifies a required contract; no benefit follows merely from combining names.'),
    small('Future extensions in this edition are research directions. No novelty search, patent assessment, production qualification or application-level hardware benchmark was performed.'))

page('What was checked, and by whom','31 / CONFORMANCE',
    table([['Evidence','Scope and outcome'],['S1 source-reported','10,000 word roundtrips; 10,000 field-isolation cases; 2,048 seam cases; 2,000 transition cases; OTAN2 profiles and selected thermal checks.'],['S2 source-reported','M36 assembly: 17 groups / 20,873 assertions. This is a reduced abstract audit, not a complete assembled production runtime.'],['S3 source-reported','212 bulk conformance runs; 26 independently checked exports; 24 final cold profiles at dictionary miss floor; finite workload/device evidence.'],['S4 source-reported','36 reference tests; a bounded 0..99 linguistic profile; no independent physical performance validation.'],['PM newly executed','46 Python SEED checks and 5 independent .NET framing/hash comparisons on the same Windows host.'],['PM newly executed','15 source-operator identity and cross-domain calculation checks; result details embedded in formal_checks_results.json.']],[1.2,4.05]),
    p('[E] The new SEED checks include format/Unicode rejects, canonicalization, manifest binding, domain/counter changes, rejection-sampling boundaries and transcript mutation. The .NET implementation independently reconstructs fixed frames and hashes. This is useful same-host implementation evidence, not qualification across operating systems.'),
    p('[S] S3 reports a 4 MiB dictionary distributed over 46 SM caches. At 32 bytes per sector its compulsory miss floor is 131,072. Reaching that aggregate floor during a cold warm/work/reread epoch supports bounded retention under its recorded conditions. It does not establish pinning across launches or arbitrary workloads.'),
    small('No source CUDA commands or embedded historical instructions were executed for this synthesis. New checks concern the added formalization support; V01-V07 remain application proposals.'))

page('Worked, reproducible consequences','32 / CALCULATIONS',
    h('Thermal recurrence inherited from WANTWOMBAN'),
    eq('C=0.020 J/K; G=0.005 W/K; P=0.100 W; Ta=293.15 K\ntau=C/G=4 s; T_infinity=Ta+P/G=313.15 K\nT(t+dt)=Ta+P*u/G+(T(t)-Ta-P*u/G)*exp(-dt/tau)'),
    p('[P/E] For the illustrative 304.15 K heating threshold, first passage from ambient is 3.19403 s. Supplied energy is 0.319403 J; sensible storage is 0.220000 J; modeled loss is 0.099403 J. The independently recalculated values satisfy the balance. These are chosen model inputs, not measured paint properties.'),
    h('Passive wave realization'),
    p('[P/E] phi = 1.61803398875. The unscaled pinion has maximum amplitude gain phi and maximum power gain phi^2 = 2.61803398875. Scaling by 1/phi bounds every singular value by one. A computed basis-vector witness and matrix checks are in the calculation receipt.'),
    h('Exact SEED fixture'),
    p('[E] The standalone fixture uses seed zero, family digital, sub_v reference-1.0.0, numeric_mode u64-mod, empty source/asset lists and domain geometry/instance/0/position. Its canonical manifest and all bytes are embedded with the reference; it is not a full application manifest.'),
    eq('B(domain,0) =\n1bf021f9bb711c5514a3075a26a407c7\n5959e1730dbd5df9e22f2942800b7622\nFirst ten range-10 outputs: 7,6,7,4,8,4,2,7,9,8'),
    small('The two block-hex lines concatenate to one 64-digit value. These outputs depend on the entire fixture manifest and byte framing, not just the seed. Source thermal example: S1 PDF pp. 16-17.'))

page('An application has a complete contract','33 / IMPLEMENTATION HANDOFF',
    eq('PM application = purpose + embodiment + source_adapters\n + state_schema + domain_laws + calibration\n + operating_envelope + scheduler + observables\n + resources + numeric/seed_profile + evidence_plan'),
    p('[D] A concrete implementation binds these fields to immutable content and gives all optional features explicit enabled/disabled semantics. Unknown calibration cannot silently receive a plausible number. Simulation values must be labeled as inputs; measured values carry units, method, time and uncertainty [R23].'),
    table([['Record','Minimum information'],['Definition','ID, version, content hash, domain/codomain, assumptions, source locator and capabilities'],['Plant','Device/material IDs, initial/boundary conditions, calibration, response delays and resource ports'],['Run','Initial state, actual inputs, seed profile if used, execution order, code/math versions and limits'],['Event','Proposal, guard result, actual command/acknowledgment, readback and lineage'],['Evidence','Method, configuration, raw records, comparison rule, finite coverage and unresolved claims']],[1.1,4.1]),
    h('When a V changes'),
    p('A new application V is justified by a different task or physical/computational architecture. Within a V, incompatible changes to state, law, actuator/readout meaning or observable semantics require a new major contract version. A calibration revision or new fitted parameter set has its own identity; an editorial correction does not imply new physical behavior.'),
    small('The minimal SEED module is not a full validator for these application contracts. The embedded editable source supports subsequent implementation; it does not pretend to be a driver for unspecified hardware.'))

page('Reconciliation and retained distinctions','34 / SOURCE AUDIT',
    table([['Issue','Formal treatment in PM'],['OTAN2 collisions','Keep five explicitly named roles; never silently substitute atan2 for literal ratio or code mixing.'],['Hadamard collisions','Numerical H4 and Boolean XOR remain different; wave realization obeys passivity.'],['Word size / identity','64-bit WB controller, 32-bit ATOM sink groups, identity digest and lineage are separate types.'],['Infinite nesting','Unbounded symbolic addresses require storage for every finite execution prefix; finite runs enforce budgets.'],['Topology as physics','A seam defines routing/identification; hardware coupling and constitutive laws remain explicit.'],['Source pipeline numbering','Use named stages and explicit index bases, preserving actual causal order.'],['Pulse simplex wording','Use point/segment/regular polygon for the supplied planar embedding; higher simplex needs another map.'],['Hinge derivatives','Fixed-pivot formula requires fixed pivot/source point; moving components require additional derivatives.'],['Distance and pruning','Sign fields are not automatically exact distances; culling needs a descendant-containing bound.'],['Physical rollback','Deposited heat, charge and material remain in measured history after a digital rejection.'],['Biological/numerical labels','Use as declared symbols or measured channels; no mechanism follows from lexical or count coincidences.']],[1.3,4]),
    small('This table records interpretation and engineering additions instead of silently rewriting the witnesses. Relevant loci: S1 PDF pp. 7-12, 20-21; S2 pp. 10-14, 17-22, 27, 31-35, 40; S4 pp. 5-14, 16-19.'))

manifest=json.loads((TMP/'source_manifest.json').read_text(encoding='utf-8'))
fingerprints=[]
for i,s in enumerate(manifest,1):
    fingerprints += [h(f'S{i} / {s["id"]}'),small(Path(s['path']).name+f'<br/>{s["pages"]} pages / {s["bytes"]:,} bytes'),eq(s['sha256'][:32]+'\n'+s['sha256'][32:])]
page('Exact source witnesses','35 / PROVENANCE',*fingerprints,
    small('Concatenate each pair of hash lines. Hashes identify the supplied byte streams, not independent authorship or scientific truth. The original PDFs are attached to this PDF without modification. Source-local links and historical commands remain part of their documentary content.'))

references=[
('R1','NASA Glenn. First Law - Internal Energy. Energy-balance convention.','https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/first-law-internal-energy/'),
('R2','COMSOL 6.3. The Heat Balance Equation. Local/integral thermal balance.','https://doc.comsol.com/6.3/doc/com.comsol.help.heat/heat_ug_theory.07.005.html'),
('R3','Basnec et al. (2018). Colour and phase changes of a leuco-dye thermochromic composite. Scientific Reports 8, 5511.','https://www.nature.com/articles/s41598-018-23789-2'),
('R4','Tedrake. Underactuated Robotics: Multi-Body Dynamics and Lyapunov Analysis. Physical equations and scoped stability conditions.','https://underactuated.mit.edu/multibody.html'),
('R5','Hatcher. Notes on Introductory Point-Set Topology, chapter 4. Quotient construction.','https://pi.math.cornell.edu/~hatcher/Top/TopNotes.pdf'),
('R6','BIPM / JCGM vocabulary, 1.8. Quantities of dimension one retain semantic meaning.','https://jcgm.bipm.org/vim/en/1.8.html'),
('R7','NIST FIPS 180-4. Secure Hash Standard. Pinned SHA-256 primitive.','https://csrc.nist.gov/pubs/fips/180-4/upd1/final'),
('R8','RFC 8785. JSON Canonicalization Scheme. PM uses a constrained subset.','https://www.rfc-editor.org/rfc/rfc8785.html'),
('R9','Du et al. (2017). Reservoir computing using dynamic memristors for temporal information processing. Nature Communications 8, 2204.','https://www.nature.com/articles/s41467-017-02337-y'),
('R10','Zhang et al. (2024). Collective dynamics and long-range order in thermal neuristor networks. Nature Communications 15, 6986.','https://www.nature.com/articles/s41467-024-51254-4'),
('R11','Multimaterial Printing of Liquid Crystal Elastomers with Integrated Stretchable Electronics (2023). ACS Applied Materials & Interfaces.','https://pubs.acs.org/doi/10.1021/acsami.2c23028'),
('R12','Zadan et al. (2022). LCE with integrated soft thermoelectrics for shape-memory actuation and energy harvesting. Author-institution record.','https://publications.ri.cmu.edu/liquid-crystal-elastomer-with-integrated-soft-thermoelectrics-for-shape-memory-actuation-and-energy-harvesting'),
('R13','Perez et al. (2017). Multipurpose silicon photonics signal processor core. Nature Communications 8, 636.','https://www.nature.com/articles/s41467-017-00714-1'),
('R14','Perez-Lopez et al. (2020). Multipurpose self-configuration of programmable photonic circuits. Nature Communications 11, 6359.','https://www.nature.com/articles/s41467-020-19608-w'),
('R15','Ullrick et al. (2023). Wideband parametric baseband macromodeling of linear and passive photonic circuits. Scientific Reports 13, 15407.','https://www.nature.com/articles/s41598-023-41227-w'),
('R16','MIT OpenCourseWare, 18.303. The 1-D Wave Equation. Propagation and boundary models.','https://ocw.mit.edu/courses/18-303-linear-partial-differential-equations-fall-2006/22ead9d70b36836a68d13c7393e19649_waveeqni.pdf'),
('R17','Piovarci et al. (2022). Closed-Loop Control of Direct Ink Writing via Reinforcement Learning. Author project/paper.','https://gfx.cs.princeton.edu/pubs/Piovar%C4%8Di_2022_CCO/index.php'),
('R18','Buchner et al. (2023). Vision-controlled jetting for composite systems and robots. Nature 623, 522-530.','https://www.nature.com/articles/s41586-023-06684-3'),
('R19','FAO Irrigation and Drainage Paper 56, chapter 8. Root-zone water balance, equation 85.','https://www.fao.org/4/x0490e/x0490e0e.htm'),
('R20','NASA. Environmental Control and Life Support Systems. Water recovery and oxygen generation.','https://www.nasa.gov/reference/environmental-control-and-life-support-systems-eclss/'),
('R21','Olfati-Saber and Murray (2004). Consensus problems in networks of agents with switching topology and time-delays. IEEE TAC 49(9).','https://www.cds.caltech.edu/~murray/papers/2003f_om04-tac.html'),
('R22','NVIDIA. Floating Point and IEEE 754; Nsight Compute Profiling Guide. Numeric and measurement scope.','https://docs.nvidia.com/cuda/floating-point/index.html'),
('R23','BIPM. JCGM 100:2008, Guide to the expression of uncertainty in measurement.','https://www.bipm.org/en/web/guest/publications/guides'),
]
def refblocks(items):
    return [small(f'<b>[{rid}]</b> {title} <link href="{url}" color="#007C88">Primary source</link>.') for rid,title,url in items]
page('Primary references / 1','36 / RESEARCH',
    small('Consulted 15 September 2026. These sources support the stated component laws and examples. The seven PM architectures, mapping contracts and proposed experiments are new synthesis.'),
    *refblocks(references[:12]),
    small('R4 stability chapter: <link href="https://underactuated.mit.edu/lyapunov.html" color="#007C88">Lyapunov Analysis</link>. R7 reference-check vector: <link href="https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/SHA256.pdf" color="#007C88">NIST SHA-256 abc example</link>.'))
page('Primary references / 2','37 / RESEARCH AND PACKAGE',
    *refblocks(references[12:]),
    h('Embedded, editable package'),
    small('Original S1-S4 PDFs; source/attachment manifests; editable Markdown and content JSON; PDF builder; full SEED contract/reference; Python and independent .NET receipts; formal calculation script and results. Hashes are unsigned integrity records. The PDF does not require any attachment to execute on opening.'),
    small('The specification states equations and experiment designs. Seven complete application implementations and physical demonstrators are not included or claimed.'))

(ROOT/'content.json').write_text(json.dumps(pages,indent=2,ensure_ascii=False),encoding='utf-8')
print(f'Wrote {len(pages)} planned pages.')
