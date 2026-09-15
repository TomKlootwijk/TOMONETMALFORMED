# A18 / Wave-and-material computer

Tom Klootwijk / NL200678942

R1.0 / 15 September 2026


## Page 1: A18 / Wave-and-material computer

<b>Definition:</b> an engineered processor in which propagating waves transform input signals, while a programmable material state sets and retains part of the transformation. A separate controller programs, measures and qualifies that physical response.

Input -> encode -> optical core -> coherent I/Q readout -> output. Material retains core settings; digital control programs and verifies them.

The proposed optical implementation takes four coherent input channels and returns four complex output channels. Its first supported tasks are calibrated linear transforms, including the source-specific H4 and scaled pinion. Material memory initially stores settings. An extension with evolving material state can instead process signal history.

<b>The enhancement:</b> make A18 an explicit machine contract: name the inputs and outputs, compile only physically reachable transforms, measure phase as well as amplitude, qualify every configuration, recover from drift, and account for programming and readout costs.

Tom Klootwijk / NL200678942<br/>R1.0 / 15 September 2026 / Prepared with Codex assistance<br/>Focused supplement to Frontier Applications A1.0, A18, pp. 41-42, and Perpetuum Mobile PM 1.0, V02/V04.

This document defines a proposed integration. It includes an executed synthetic numerical example and a hardware experiment plan. It does not report a fabricated A18 processor or measured hardware performance.


## Page 2: What changes when A18 is made precise

| Original direction | Enhanced definition | Useful result |
| --- | --- | --- |
| Waves plus retained material | Frozen optical transfer during each accepted read block; separate programming dynamics | A reproducible computation boundary |
| A programmable transform | Supported operator family and bounded physical compiler | Unsupported requests are identified before use |
| Optical readout | Calibrated complex I/Q receiver with a common phase origin | Signed and complex outputs have defined meaning |
| Write and verify | Programming record, settling, basis probes and held-out verification | The current hardware response supports admission |
| Handle material drift | Pilot checks, gain limits, temperature envelope and invalidation rules | Old configuration records cannot mask new physical errors |
| Future adaptation | Retained settings plus a separate, characterized dynamic memory state | Temporal processing becomes a testable extension |

### Where this proposal adds something specific

Optical computation with retained weights and retained programmable components already exist [R1, R3]. A recent ferroelectric mesh combines retained-capable cells with complex mesh demonstrations performed using volatile control [R4]. A18 proposes source-typed operators, calibrated mappings, execution records, guarded use and resource-aware reconfiguration. Whether these additions improve a real task must be measured.

The most useful enhancement is a processor that reports what transformation it can currently perform and with what error bound. The surrounding machine can then decide whether that capability is suitable for its next sensing or control task.

The document makes no novelty or patent determination. Research claims are attributed; the A18 contracts, integration choices and experiment criteria are proposed here.


## Page 3: A machine with three interacting parts

Input -> encode -> optical core -> coherent I/Q readout -> output. Material retains core settings; digital control programs and verifies them.

| Part | Concrete implementation role |
| --- | --- |
| Wave path | Common optical source; four amplitude/phase encoders; mixing network; controlled attenuation/phase; four coherent receivers. A0 fixes signal scale. |
| Retained settings | Material devices retain calibrated phase, coupling or attenuation settings. A complex weight may need several physical controls; one material state does not imply independent amplitude and phase control. |
| Digital supervision | Driver scheduling, device maps, thermal observations, transfer estimation, limited output correction, trace storage and the external task interface. |
| Resources and access | Write drivers, local oscillator, calibration injection, monitor taps, temperature control and terminated unused channels are part of the instrument. |

### A deliberately bounded first core

```text
S_core(g,theta,T) = D(g,theta,T) * H4
D = diag(d1,d2,d3,d4)
|di| <= 1 in the ideal passive row-weight model
```

A fixed H4 mixer followed by four calibrated complex weight channels supports a restricted matrix family, including the scaled pinion. Real mixer imperfections are measured. A general matrix needs a larger architecture; two programmable unitary meshes around an attenuation stage provide an ideal construction [R2].

There are four logical inputs and four logical outputs. This is a 4x4 forward transfer block, not the complete scattering matrix of a device with only four physical ports.


## Page 4: The input-to-result contract

```text
x in C^4; ||x||2 <= 1; W in C^(4x4)
a = A0*x
b_hat = S(omega;g,theta,T)*a + n_total
S_target = gamma*W/s; s = max(1,||W||2)
y_hat = s*b_hat/(gamma*A0)
```

| Symbol | Meaning and units |
| --- | --- |
| x, W, y_hat | Dimensionless numerical input, requested linear operator and decoded output. dagger denotes conjugate transpose; ||.||2 is the vector or spectral norm. |
| a, b, b_hat, n_total, A0 | Input, actual output and estimated output amplitudes in sqrt(W). n_total aggregates optical noise and calibrated receiver error; A0 is positive. |a_i| squared is channel power. |
| g, theta, T | Device-specific retained state; trim settings with declared units; temperature in kelvin. g may represent phase fraction or polarization through different adapters. |
| omega, gamma, s | Angular frequency in rad/s; positive amplitude headroom no greater than one; numerical scaling at least one. |

The linear model applies over a stated bandwidth, input range and approximately constant configuration during a read block. The notation is a frequency-domain relation; modulated inputs need a characterized baseband transfer and delay. A matrix at one carrier frequency does not establish arbitrary-bandwidth filtering.

The input adapter preserves requested complex values within its calibrated range. It reports clipping, missing phase reference or invalid channels. A task output includes a configuration ID, numerical scale, timestamp, error statement and exact validity status.

A0 is limited by encoder range, receiver saturation, material read disturbance and linearity. gamma provides amplitude margin for loss; choosing it smaller increases the numerical amplification of measurement error.


## Page 5: Material memory has its own dynamics

```text
during program: g_next = F_write(g,u_pulse,T;device) + e_g
during read:    dg/dt = F_relax(g,T,I_read;device)
C_th*dT/dt = P_abs + P_driver - G*(T-Ta)
configuration = (g_estimate, theta, calibration, history)
```

These are model slots, not a universal material law. F_write and F_relax require device-specific measurements. C_th is heat capacity in J/K, G thermal conductance in W/K, and power terms are watts for a declared thermal boundary. State-estimation error e_g and unobserved internal state remain explicit.

| Candidate embodiment | Mechanism supported by research | Required A18 binding |
| --- | --- | --- |
| Phase-change photonics | Electrically programmed material states alter optical response [R3] | Pulse history, absorption, phase/attenuation reachability, settling, drift and endurance |
| Ferroelectric photonics | Retained unit-cell states demonstrated in a programmable-mesh architecture [R4] | Preconditioning, pulse trains, full-mesh addressing and thermal sensitivity |
| Fast trim controls | A separately powered actuator corrects smaller response changes | Range, power, noise, interaction with retained state and reset semantics |

### Timing must name the operation

Propagation delay, volatile switching, retained-state writing, settling, calibration and task service time are different quantities. For example, the fast Pockels switching figure in the 2026 ferroelectric mesh paper is not the latency of an arbitrary retained rewrite and verification cycle [R4].

A stored setting can need no continuous programming bias while the complete instrument still consumes power. Read illumination, control, thermal stabilization and the coherent reference remain in the energy account.


## Page 6: Compile the source transform into passive hardware

```text
phi = (1+sqrt(5))/2
H4 = 0.5*[[1,1,1,1],[1,-1,1,-1],
          [1,1,-1,-1],[1,-1,-1,1]]
A_phi = diag(phi,phi^-1,1,-1)*H4
S_target = gamma*A_phi/phi
```

H4 is orthogonal and has unit singular values. The pinion singular values are phi, 1, 1 and phi^-1. Scaling by phi makes the forward target contractive: its singular values become gamma times 1, phi^-1, phi^-1 and phi^-2. These are the exact PM 1.0 numerical operators, pp. 22-23.

```text
passive, fixed configuration: S^dagger*S <= I
W = U*Sigma*V^dagger
ideal network: V^dagger -> gamma*Sigma/s -> U
```

The diagonal stage attenuates or diverts light to unused terminated channels. Phase-only control cannot realize every nonunitary matrix. The negative pinion coefficient needs a pi phase relation in a coherent implementation. Numerical decoding by phi/gamma restores scale in the reported number and amplifies error by the same factor.

### The physical compiler is a measured fit

```text
(g*,theta*) = argmin_admissible sum_k w_k *
             ||S_device(omega_k;g,theta,T)-S_target(omega_k)||F^2
```

The admissible set includes reachable settings, failed components, input range, temperature and writing budgets. The ideal factorization gives a design; a calibrated device must still meet the residual bound [R2, R6]. A fixed H4-plus-weights core accepts only its supported subset.


## Page 7: Recover the field, including its phase

```text
I_out = K_I*Re(b*conj(L)) + offset_I + noise_I
Q_out = K_Q*Im(b*conj(L)) + offset_Q + noise_Q
b_hat = CalibrateIQ(I_out,Q_out,L;receiver_profile)
```

L is the complex local-oscillator field with a declared phase origin. In this receiver convention, I_out and Q_out are electrical currents; K terms include responsivity and optical-hybrid factors. The calibrated inverse maps actual readings into sqrt(W). Gains, offsets, quadrature imbalance, reference drift and saturation belong to the receiver profile. Coherent processor research demonstrates quadrature-based complex readout [R7].

### Why intensity alone is insufficient

```text
x1 = [1,0,0,0]^T; x2 = [0,1,0,0]^T
|H4*x1|^2 = |H4*x2|^2 = [1,1,1,1]^T/4
H4*x1 != H4*x2
```

The two outputs have identical channel powers and different signed fields. An intensity detector therefore cannot, by itself, verify this signed transformation. An intensity-based architecture could use another encoding and decoding convention, but that would be a different interface and must be evaluated separately.

### A common reference connects the channels

Each of the four receiver channels must be calibrated against the same reference convention. Unknown channel phases can turn a correct optical calculation into a wrong numerical result. Calibration signals should exercise both quadratures and multiple amplitudes; four basis vectors alone do not characterize receiver nonlinearity.

These equations define the proposed coherent adapter. They do not claim that the intensity-oriented tensor-core experiment [R1] already provides this A18 phase-sensitive interface.


## Page 8: Calibrate the transformation that exists

```text
a_j = A0*e_j; S_hat[:,j] = b_hat_j/A0
d_hat_i = (S_hat[i,:]*conj(S_target[i,:])^T)
          / ||S_target[i,:]||2^2
row_residual = ||S_hat-diag(d_hat)*S_target||F
```

Four phase-referenced basis probes identify a linear 4x4 forward transfer at one frequency and configuration. Repeat probes estimate noise and time variation. Sweep the declared frequency band and test held-out coherent superpositions. Null inputs check offsets; multiple amplitudes check linearity and saturation.

### Use limited correction only when its model fits

If deviations are approximately one stable complex factor per output row, four scalar corrections can remove row gain and phase errors. Require every relevant target row to have nonzero norm, bound each inverse factor, and independently check the row-model residual. Small or dark responses cannot be recovered by unlimited numerical gain.

```text
b_corrected_i = b_hat_i / d_hat_i
y_hat_i = s*b_corrected_i/(gamma*A0)
```

Arbitrary internal mixing errors generally cannot be repaired by those four factors. Reconfigure and remeasure the optical core. A full dense digital correction matrix would add a different computation cost and could perform much of the requested work electronically; it is not hidden inside this baseline.

Measured feedback configuration is supported by programmable-mesh research [R6]. This contract adds explicit scope, gain and holdout requirements. The included reference example uses synthetic basis observations and a declared row-error model only.


## Page 9: Program, verify, then admit a read block

| State | Permitted work | Condition for advancement |
| --- | --- | --- |
| UNQUALIFIED | Resolve target, profile, resource limits and actual device state | Inputs and bounded programming plan are valid |
| PROGRAMMING | Issue identified pulses; retain actual acknowledgments and meter resources | Pulse outcomes are reconciled |
| SETTLING | Observe the material and thermal response | Measured readiness criteria hold |
| VERIFYING | Acquire calibrated probes and held-out observations | Transfer, uncertainty and operating limits pass |
| QUALIFIED | Serve bounded read blocks, labeled with the configuration record | Pilot and envelope checks remain valid |
| INVALIDATED | Hold results for affected blocks; diagnose and remeasure | A newly verified configuration replaces the old one |

The digital commit accepts a command or configuration record. It does not assert that the physical pulse completed. An interrupted write may leave a partially changed material state. Recovery reads that state and replans from it; replaying the pulse blindly can produce a different setting or consume additional device life.

### A configuration record is a claim with a scope

It contains the device and target identities, source/operator hashes, measured transfer, receiver calibration, uncertainty, frequency and temperature envelope, input scale, output scaling, accepted correction factors, probe evidence and validity interval. It is a locally issued evidence record, not an independent certification.

Baseline read blocks contain no programming. Read disturbance and ordinary drift can still change the material. A failed monitor invalidates the interval whose correctness can no longer be bounded.


## Page 10: Enhance service life and useful availability

| Enhancement | Concrete policy | What must be measured |
| --- | --- | --- |
| Retention plus trim | Retain coarse settings; use a separately budgeted fine actuator for bounded drift | Trim range, noise, static cost and interaction with retained state |
| Write-aware target scheduling | Group compatible jobs to amortize rewriting; cap write count and energy per cell | Workload benefit, measured cycling degradation and scheduling delay |
| Reuse verified configurations | Cache targets and configuration evidence; recheck current transfer before reuse | Retention dispersion and verification overhead |
| Reserve paths | Fit around a failed component only if surviving hardware can reach the target | Actual loss, residual, bandwidth and new calibration cost |
| Optional two-bank service | Prepare another physical bank while the active bank reads; verify the selector after handover | Isolation, crosstalk, output phase discontinuity, footprint and full energy |

```text
choose plan minimizing normalized_terms:
fit_error + lambda_E*write_energy + lambda_N*write_count
          + lambda_t*service_delay
subject to error, temperature and device-life limits
```

The weights and normalization are application choices. An energy-saving schedule cannot change a scientific input order that matters to the experiment. A spare path or second bank improves availability only when its additional loss, controls and transitions remain acceptable.

These are proposed engineering improvements. Physical recovery here means restoring a usable measured response by reconfiguration or replacement; it does not imply that the material repairs its own damage.


## Page 11: Attach a usable error bound to the result

```text
S = S_target + E; ||x||2 <= 1
||y_hat-W*x||2 <= (s/gamma)*||E||2*||x||2
                 + s*||n_total||2/(gamma*A0)
```

n_total includes optical noise and calibrated receiver error. This bound excludes unmodeled encoder errors; those require an additional term or end-to-end characterization. With a row-correction matrix C, assess the effective transfer C*S and noise C*n_total. Large correction gains amplify uncertainty, not only the desired signal.

| Error source | Observation and action |
| --- | --- |
| Static transfer mismatch | Held-out complex inputs and a matrix residual; recompile or reject outside tolerance |
| Thermal/material drift | Pilot vectors and temperature records; bound the valid interval or invalidate it |
| Phase-reference changes | Reference monitors and receiver checks; re-establish common phase before accepting output |
| Read noise and quantization | Repeated readings and calibrated receiver model; use absolute as well as relative errors |
| Latency or dropout | Timestamp, block identifier and missing-sample status; never fill unknown data with a valid-looking number |

### Validity between measurements requires an assumption

Pilot agreement at sampled times alone does not bound every intervening input. Set a maximum block duration using a measured drift-rate envelope and uncertainty allowance, or characterize complete blocks through independent evidence. Near a target null, use absolute output error because relative error can diverge.

An active amplifier or frequency-changing modulation needs a different energy and transfer model. The passive fixed-configuration inequality cannot certify those operating modes.


## Page 12: An executed four-channel numerical example

<b>Evidence type: synthetic model.</b> All device observations, perturbations and energy inputs below are declared numerical values. No optical hardware was measured.

The reference preserves PM H4 and the scaled pinion. A synthetic passive core adds output loss and phase offsets; explicit complex basis probes include bounded errors. Four output correction factors are fitted and evaluated on separate finite complex vectors. No random generator or substitute SEED construction is used.

| Check / maximum held-out relative L2 error | Executed result |
| --- | --- |
| Mathematical and software checks | 44 passed |
| Scalar decoding only | 15.976844% |
| Four-factor calibration | 0.063294% |
| Specified drift; old calibration | 1.375459% |
| Specified drift; refreshed calibration | 0.051705% |
| Largest refreshed numerical decoder gain | 1.908980 |
| Held-out complex vectors | 6 |

Calibration improves these six held-out vectors because the chosen perturbations closely match the row-factor model. The drift case demonstrates why retaining an old calibration is insufficient. These percentages are finite synthetic errors, not measured hardware accuracy or a statistical confidence interval.

### Failure cases are part of the example

The script checks intensity ambiguity, a dark output row, excessive inverse gain and unmodeled mixing. It also checks passive scaling and numerical error amplification. The exact inputs, formulas, software environment and results are embedded as reference_model.py and reference_results.json.

A good result on this restricted row-error model does not establish that arbitrary fabrication errors admit row-wise correction. The example validates internal mathematical consistency and the implemented checks only.


## Page 13: When retaining a program could pay off

```text
E_A18(N) = E_setup + N*e_read + E_idle + E_recheck
E_digital(N) = E_digital_setup + N*e_digital
E_setup includes write, settle and initial calibration
```

e_read includes the source, encoders, local oscillator, receivers, conversion, correction and control for one accepted vector. Add failed reads, retries and cooling at the same workload boundary. A passive optical path does not make these terms disappear. A retained setting is most promising when reused many times or when the signal is already optical.

```text
neglecting digital setup, idle and recheck costs:
N > E_setup/(e_digital-e_read)
requires e_digital > e_read
```

Illustration only: setup energy 2 mJ, complete hybrid read cost 3 microjoules per task and digital cost 5 microjoules per task give strict break-even at 1,001 reused tasks. Under these chosen values, requalification every 800 tasks removes the advantage; a 2,000-task interval permits it. Actual values must be measured.

### Energy and service time need separate decisions

The smallest energy total may not meet an interactive deadline. Report throughput at matched error, first-result latency, reconfiguration downtime, block duration, calibration frequency and rejected work. Device propagation delay is only one term in end-to-end latency.

The displayed break-even expression suppresses idle and periodic recheck costs to expose the arithmetic. A real comparison must restore them and the electronic baseline setup cost. No device purchasing or performance forecast follows from the illustrative numbers.


## Page 14: Build a demonstrator that answers a question

| Stage | Hardware work | Evidence produced |
| --- | --- | --- |
| Characterize | One retained phase/weight channel; calibrated optical source and readout | Reachability, write history, read disturbance, drift and usable gain range |
| Mix four channels | H4 mixer, four programmable weight channels and coherent receivers | Measured H4 and scaled pinion over declared inputs and bandwidth |
| Close the verification loop | Bounded controller, calibration injection, temperature monitor and trace storage | Programming, settling, holdouts and correctly invalidated failed blocks |
| Exercise useful service | Repeated sensing or filtering workload with planned reconfiguration | Accuracy, energy, latency, endurance and availability at the task boundary |

### Predeclare the comparison

Compare fixed optical settings, retention without adaptive correction, the enhanced A18 policy and conventional electronics on the same input stream. Count manual calibration and rejected attempts. Hold out complete configurations, input phases and temperature trajectories from model fitting.

### Proposed acceptance contract

Before hardware trials, assign numeric limits to absolute/relative error, usable optical power, bandwidth, drift, settling, inverse gain, cycle count and resource budget. Report uncertainty and trial count. The synthetic limits in the reference example are software fixtures; they are not proposed device specifications.

Inject loss, temperature change, missing references and interrupted write acknowledgments within the characterized bench envelope. Independently observe what the device did. A successful demo includes an honest unsupported-target response as well as an accepted computation.

If an ordinary volatile optical bench is used initially, label it as a wave-path surrogate. Demonstrating A18 material retention requires actual retained-state components and measured preparation/readback.


## Page 15: Extend it from stored settings to signal memory

```text
z_(n+1) = f(z_n, B*x_n; g,T)
b_n = S(g,z_n,T)*a_n
y_n = W_out*[1; measured_features_n]
```

z is an additional, physically evolving state with calibrated units, time constants and preparation. g retains slower configuration. The readout is trained and evaluated on separate sequences. Dynamic memristors supply component evidence for temporal processing [R5]; their particular device law cannot be assigned to a photonic material without characterization.

### Two enhancements with different physical meaning

| Extension | Mechanism | New obligation |
| --- | --- | --- |
| Material fading memory | Input-dependent material dynamics retain recent excitation before relaxing | Measure relaxation, disturbance, nonlinear response and repeatability |
| Explicit recurrent loop | Route earlier measured outputs into later inputs through a declared delay and controller | Specify loop gain, sampling, latency, saturation and stability |

```text
illustrative discrete recurrence: z_next = f(R*z + B*x)
if f is Lipschitz with L_f and L_f*||R||2 < 1,
then same-input state differences contract each step
```

This is a sufficient condition for a specified discrete model, using its induced norm and operating set. It is not a stability proof for an unknown delayed physical loop. Useful nonlinear behavior, accuracy and memory capacity still need task experiments.

Retaining the last programmed weight is configuration memory. Remembering the order of recent inputs is signal memory. The second is a substantive new capability with different equations and evidence.


## Page 16: Cross-domain embodiments that earn their differences

| Embodiment | What propagates / what persists | Best bounded question |
| --- | --- | --- |
| Coherent photonic core | Optical amplitudes / retained refractive or coupling settings | Can repeated linear transforms meet error and total-cost targets? |
| Photonic material reservoir | Optical excitation / measured transient material states | Do physical features distinguish temporal sequences at matched resources? |
| RF or microwave network | Voltage/current waves with impedance conventions / latched tuning states | Can a retained multi-channel filter help a calibrated sensor or communication task? |
| Acoustic or elastic network | Pressure or displacement / mechanically retained geometry or material state | Can a structure retain a useful transfer while damping and loading vary? |
| Digital reference and twin | Numerical states / versioned configuration and measurement records | Can commands and comparison results be replayed and divergences explained? |

These are application embodiments, not cosmetic revision labels. Each requires its own wave, material, transducer and energy laws. Pressure, displacement and electrical voltage cannot simply inherit the optical sqrt(W) convention. Units and the meaningful observable determine the adapter.

```text
elastic example: M*qddot + D*qdot + K(g)*q = B*f
readout = L*q; geometry and damping are measured
```

Only the optical contract and synthetic example are developed quantitatively here. The other embodiments are research directions linked through explicit interfaces, not demonstrated interchangeable hardware.


## Page 17: Futuristic uses with an actual computation inside

| Application | What A18 would compute | Why material retention could matter |
| --- | --- | --- |
| Adaptive optical sensing surface | Reusable projections of four optical channels; later, temporal contact features | Keep useful sensing modes between task changes; add signal memory only with calibrated dynamics |
| Self-reconfiguring microscope | Complex mixing or mode selection in a coherent measurement instrument | Reuse aligned optical configurations; verify each one as temperature and optics change |
| Robot inspection workcell | Fixed transform features for defect or alignment measurements | Switch among qualified inspection modes and retain the setting used for each result |
| Remote environmental instrument | Selected linear projections of encoded spectral or interferometric channels | Reuse a small task library under finite power and maintenance budgets |
| Adaptive communication front end | Linear channel mixing or equalization over a measured band | Retain slowly changing settings while separately correcting drift |
| Wave-and-material temporal instrument | Nonlinear features of signal history in the dynamic extension | Process temporal structure locally if its memory is repeatable and useful |

A four-channel core is a small processing tile. Large sensors require explicit tiling, time multiplexing or additional channels, each with conversion, synchronization and resource costs. Ordinary image intensities or electrical sensors first need an encoder; that overhead can determine whether an optical implementation is worthwhile.

The strongest research opportunity is repeated processing of already optical signals, with slowly changing tasks and a measurable reason to retain settings. The question is whether the complete instrument benefits, not whether light propagates quickly.


## Page 18: Bind A18 to the supplied framework

| Source contribution | A18 binding | Boundary preserved |
| --- | --- | --- |
| WANTWOMBAN H4/pinion | Exact numerical targets; powered material/readback pattern | Boolean XOR, optical interference and geometric operators retain different meanings |
| UGTS registry and relations | Typed channels, ordered optical connections, material/receiver profiles and lineage | A compatible graph does not fabricate a coupler or prove reachability |
| atomOS state and admission | Bounded proposals, configuration IDs, actual-command records and dispositions | A logical commit does not establish a completed physical write |
| PM SEED contract | Reproducible target libraries, probe choices and benchmark ordering | Measured phase, temperature and physical write outcomes remain external evidence |

A complete A18 descriptor pins target matrices, channel order, numeric mode, input scale, device and receiver profiles, units, measured operating limits, compiler/correction versions and the evidence policy. Calibration records carry actual observations and exact validity status.

```text
digital replay = descriptor + initial state + input transcript
physical agreement = preparation + calibration + measured inputs
                   + a declared uncertainty comparison
```

Use the exact PPM-SEED-v1 construction in the embedded PM source when randomness is required. The finite numerical example here lists its inputs explicitly and uses no random stream. The absence of a seed in that example is deliberate and reproducible.

Source locators: PM 1.0 pp. 5-8, 11-12, 18-19 and 22-23; Frontier Applications A1.0 pp. 41-42. The original documents remain embedded through the unchanged source package.


## Page 19: What qualifies as an A18 result

| Claim | Required evidence |
| --- | --- |
| Defined computation | Input/output units, target, encoding, scaling, frequency band and validity rules |
| Retained setting | Measured state survives the declared idle interval without continuous programming bias; support power is recorded |
| Correct linear task | End-to-end complex agreement on held-out inputs at declared uncertainty |
| Adaptive enhancement | Better declared task result than the fixed/calibration baseline, including retries and overhead |
| Temporal capability | Held-out sequence benefit from measured dynamic state against memoryless and digital temporal controls |
| Useful efficiency | Matched task accuracy with complete energy/time/resource accounting |
| Reproducible evidence | Source, code, inputs, calibration, actual outcomes and exclusions remain traceable |

### Status of this delivery

Completed: the focused definition, enhanced architecture, conditional equations, bounded compiler design, synthetic numerical checks and a physical experiment plan. The document and embedded source bytes are verified during delivery. Hardware fabrication, material characterization and application trials remain future work.

A18 is now a proposal for a verified, reconfigurable wave processor with retained material settings. Its next decisive step is a measured retained-weight channel, followed by the four-channel H4/pinion experiment.


## Page 20: Research basis / 1

Primary research checked 15 September 2026. Summaries below describe component evidence; the proposed A18 machine contracts are distinct from those demonstrations.

### R1 / Retained photonic computation

Feldmann et al. (2021), Parallel convolutional processing using an integrated photonic tensor core, Nature 589, 52-58. <link href="https://www.nature.com/articles/s41586-020-03070-1" color="#007C88">Source</link>.

Phase-change memory arrays and optical wavelength multiplexing perform specified convolution operations. This supports the combination of optical processing and retained weights.

<b>Boundary:</b> The experiment is not evidence of A18&#x27;s arbitrary coherent complex interface, verification protocol or total-system advantage. No projected speed from this paper is used as an A18 measurement.

### R2 / Interferometer decomposition

Clements et al. (2016), Optimal design for universal multiport interferometers, Optica 3, 1460-1465. <link href="https://doi.org/10.1364/OPTICA.3.001460" color="#007C88">Source</link>.

A constructive mesh decomposition supplies a design basis for unitary optical transformations.

<b>Boundary:</b> Nonunitary targets need additional attenuation, embedding or other machinery. An ideal factorization does not prove a fabricated network can reach a requested error tolerance.

### R3 / Electrically programmed material settings

Chen et al. (2023), Non-volatile electrically programmable integrated photonics with a 5-bit operation, Nature Communications 14, 3465. <link href="https://www.nature.com/articles/s41467-023-39180-3" color="#007C88">Source</link>.

Sb2S3 photonic devices demonstrate electrically retained multilevel settings and phase-error trimming.

<b>Boundary:</b> Write latency, thermal separation and endurance depend on the actual device and pulse protocol. One headline switching time cannot specify an entire A18 rewrite and verification cycle.

### R4 / Retained-capable programmable mesh

Catala-Lahoz et al. (2026), High-speed non-volatile barium titanate field-programmable photonic gate array, Nature Photonics. <link href="https://www.nature.com/articles/s41566-026-01934-y" color="#007C88">Source</link>.

The integrated ferroelectric architecture demonstrates retained individual cells. Its complex mesh configurations, including routing, filtering and unitary transformations, were characterized using volatile actuation.

<b>Boundary:</b> Automated retained-state addressing of the full mesh remained future work. Fast volatile Pockels switching is not a retained rewrite latency; retained intermediate states use pulse protocols. This source does not establish the complete A18 instrument.


## Page 21: Research basis / 2

Primary research checked 15 September 2026. Summaries below describe component evidence; the proposed A18 machine contracts are distinct from those demonstrations.

### R5 / Dynamic material information processing

Du et al. (2017), Reservoir computing using dynamic memristors for temporal information processing, Nature Communications 8, 2204. <link href="https://www.nature.com/articles/s41467-017-02337-y" color="#007C88">Source</link>.

Short-term dynamics in electronic WOx memristors supply temporal features used by a trained readout.

<b>Boundary:</b> This is electronic device evidence. Its coupling to a photonic processor and the proposed A18 material-history law remain separate research tasks.

### R6 / Measured programmable-mesh configuration

Perez-Lopez et al. (2020), Multipurpose self-configuration of programmable photonic circuits, Nature Communications 11, 6359. <link href="https://www.nature.com/articles/s41467-020-19608-w" color="#007C88">Source</link>.

Experiments and optimization studies support calibrated control curves, automated configuration and routing in programmable photonic circuits.

<b>Boundary:</b> No algorithmic convergence guarantee follows for every requested matrix, damaged circuit or larger mesh. An accepted A18 configuration still requires its own measured residual and holdout evidence.

### R7 / Complex optical readout

Xie et al. (2025), Complex-valued matrix-vector multiplication using a scalable coherent photonic processor. <link href="https://pmc.ncbi.nlm.nih.gov/articles/PMC11970466/" color="#007C88">Source</link>.

A coherent processor uses an optical hybrid and balanced detection to recover both quadratures for complex-valued processing.

<b>Boundary:</b> Its apparatus and calibration do not automatically qualify a different retained-state mesh. A18 must bind its own receiver gains, phase convention, uncertainty and operating range.


## Page 22: Provenance and reproducible package

<b>Framework attribution:</b> Tom Klootwijk / NL200678942.<br/><b>Preparation:</b> Codex-assisted definition and enhancement of A18.<br/><b>Edition:</b> R1.0 / 15 September 2026.

### Preserved source witness

The exact 56-page Frontier Applications A1.0 PDF is embedded unchanged. Its own attachments include PM 1.0, which contains the four original source PDFs. Source instructions were treated as document content; the user request defined the work.

```text
8a2506a35bfdc316f6c96827293663b7
a964d6932985e89ac659ea4f4f517bca
```

### Included editable evidence

The package includes page JSON, editable Markdown, source manifest, primary bibliography, builders, the numerical model and its exact recorded result, the compact table source and an attachment hash manifest. The external verification receipt identifies this final PDF without a self-referential embedded hash.

Rebuild using the supplied Python files, ReportLab, pypdf and the documented font/runtime requirements. The scientific model results use the recorded numerical environment; equivalent results on another environment require the declared comparison tolerance.

Diagrams are native vector architecture drawings. The model uses synthetic values. Unsigned artifact hashes support integrity checks but do not independently authenticate authorship or measurement truth.
