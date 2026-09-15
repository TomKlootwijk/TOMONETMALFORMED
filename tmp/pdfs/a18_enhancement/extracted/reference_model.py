"""A18 four-input/four-output coherent wave/material numerical reference.

All observations, loss, drift and detector noise below are SYNTHETIC.
This checks mathematics and software only. It is not a hardware experiment,
material characterization, security generator, or performance benchmark.
No RNG is used: every probe, held-out input and noise pattern is explicit.
x is dimensionless, a=A0*x is in sqrt(W), and decoded y=A_phi*x is dimensionless.
Dependencies: Python standard library and NumPy. Run: python reference_model.py
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import sys

import numpy as np

SOURCE_PM_CONTENT_SHA256 = "bc395d17b21434c6bac37374d754828352fed4febf4bd123fb065c9594b86b4b"
PHI = (1.0 + np.sqrt(5.0)) / 2.0
H4 = 0.5 * np.array([[1, 1, 1, 1], [1, -1, 1, -1],
                     [1, 1, -1, -1], [1, -1, -1, 1]], dtype=np.float64)
A_PHI = np.diag([PHI, 1.0 / PHI, 1.0, -1.0]) @ H4
TARGET = A_PHI / PHI
P_REFERENCE_W = 1e-3
PROBE_AMPLITUDE = np.sqrt(P_REFERENCE_W)
STATIC_AMPLITUDE = np.array([0.92, 0.85, 0.90, 0.88])
STATIC_PHASE_RAD = np.array([0.04, -0.06, 0.03, -0.02])
DRIFT_AMPLITUDE_RATIO = np.array([0.995, 0.997, 0.993, 0.998])
DRIFT_PHASE_RAD = np.array([0.012, -0.008, 0.015, -0.010])
CAL_NOISE_RELATIVE = 1e-4
CAL_NOISE_PATTERN = np.array([
    [1+1j, -1+0.5j, 0.5-1j, -0.5-0.5j],
    [-1j, 1, -1+0.25j, 0.5+0.75j],
    [0.25+0.5j, -0.75j, 1-0.5j, -1+1j],
    [-0.5+0.25j, 0.75+1j, -1-0.5j, 0.5-1j],
], dtype=np.complex128)
HOLDOUT_RAW = np.array([
    [1, 1j, -1, -1j],
    [1, -1, 1, -1],
    [1+1j, 2, -1j, 0.5-0.25j],
    [0, 1, 1j, 0],
    [1, -1, 1j, -1j],
    [0.25, 0.5j, -0.75, 1+0.5j],
], dtype=np.complex128)
READ_NOISE_RELATIVE = 5e-5
READ_NOISE_PATTERN = np.array([
    [1+1j, -1j, 0.5, -0.5+0.5j],
    [-0.5j, 0.5+1j, -1, 0.75j],
    [1, -0.5+0.5j, 0.25j, -1-0.25j],
    [-1j, 1, -0.5-0.5j, 0.25+0.75j],
    [0.5+0.25j, -1-0.5j, 0.75j, 1],
    [-0.75+0.5j, 0.25j, 1-1j, -0.5],
], dtype=np.complex128)
POLICY = {"singular_value_floor": 1e-8,
          "minimum_row_factor": 0.1,
          "maximum_decoder_amplitude_gain": 2.5,
          "maximum_relative_row_model_residual": 0.005}


class CalibrationRejected(ValueError):
    pass


def fit_row_calibration(s_hat: np.ndarray) -> dict:
    """Fit S_hat ~= diag(r) TARGET; never silently use a full inverse.

    This narrow decoder is justified only for independent row gain/phase errors.
    Cross-row mixing, input phase errors and changing propagation need a richer
    independently validated model, physical retuning or a rejected configuration.
    """
    s_hat = np.asarray(s_hat, dtype=np.complex128)
    if s_hat.shape != (4, 4) or not np.isfinite(s_hat).all():
        raise CalibrationRejected("invalid_shape_or_nonfinite")
    singular_values = np.linalg.svd(s_hat, compute_uv=False)
    if singular_values[-1] < POLICY["singular_value_floor"]:
        raise CalibrationRejected("singular_or_dark_transfer")
    row_energy = np.sum(np.abs(TARGET) ** 2, axis=1)
    r_hat = np.sum(s_hat * TARGET.conj(), axis=1) / row_energy
    model = r_hat[:, None] * TARGET
    residual = float(np.linalg.norm(s_hat - model) / np.linalg.norm(s_hat))
    if residual > POLICY["maximum_relative_row_model_residual"]:
        raise CalibrationRejected("row_model_mismatch")
    if np.min(np.abs(r_hat)) < POLICY["minimum_row_factor"]:
        raise CalibrationRejected("row_factor_too_small")
    decoder = PHI / r_hat
    if np.max(np.abs(decoder)) > POLICY["maximum_decoder_amplitude_gain"]:
        raise CalibrationRejected("decoder_gain_too_large")
    return {"row_factors": r_hat, "decoder_factors": decoder,
            "relative_model_residual": residual, "singular_values": singular_values,
            "max_decoder_gain": float(np.max(np.abs(decoder)))}


def decode(calibration: dict, output: np.ndarray) -> np.ndarray:
    """Normalize the coherent field by A0 and return dimensionless y."""
    output = np.asarray(output, dtype=np.complex128)
    if output.shape != (4,) or not np.isfinite(output).all():
        raise CalibrationRejected("invalid_readout")
    return calibration["decoder_factors"] * output / PROBE_AMPLITUDE


def synthetic_basis(s: np.ndarray, noise: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Each column is a synthetic read of a known coherent basis input."""
    probe_matrix = PROBE_AMPLITUDE * np.eye(4, dtype=np.complex128)
    observations = s @ probe_matrix + noise
    reconstructed = observations / PROBE_AMPLITUDE
    return observations, reconstructed


def minimum_reuse(setup: Fraction, per_task: Fraction, digital: Fraction):
    """Smallest integer N>=1 satisfying setup+N*per_task < N*digital."""
    if min(setup, per_task, digital) < 0:
        raise ValueError("negative_energy")
    advantage = digital - per_task
    if advantage <= 0:
        return None
    return max(1, int(setup // advantage) + 1)


def encode(value):
    """Result JSON is an ordinary receipt, not a PPM-SEED manifest."""
    if isinstance(value, np.ndarray):
        if np.iscomplexobj(value):
            return {"real": value.real.tolist(), "imag": value.imag.tolist()}
        return value.tolist()
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    if isinstance(value, complex):
        return {"real": value.real, "imag": value.imag}
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    return value


def run_reference(pm_content: Path | None = None) -> dict:
    if pm_content is None:
        pm_content = Path(__file__).resolve().parent.parent / "perpetuum_mobile_source" / "content.json"
    source_bytes = pm_content.read_bytes()
    observed_source_hash = hashlib.sha256(source_bytes).hexdigest()
    if observed_source_hash != SOURCE_PM_CONTENT_SHA256:
        raise ValueError("PM content hash differs from the pinned source; review the source matrices before proceeding")
    checks = []
    def check(name: str, condition: bool):
        if not bool(condition):
            raise AssertionError(name)
        checks.append(name)
    def reject(name: str, value: np.ndarray, expected: str):
        try:
            fit_row_calibration(value)
        except CalibrationRejected as exc:
            check(name, str(exc) == expected)
            return {"case": name, "status": "rejected", "reason": str(exc)}
        raise AssertionError(name + " was accepted")

    check("normalized_h4_orthogonal", np.array_equal(H4.T @ H4, np.eye(4)))
    check("h4_self_inverse", np.array_equal(H4 @ H4, np.eye(4)))
    sv_unscaled = np.linalg.svd(A_PHI, compute_uv=False)
    sv_target = np.linalg.svd(TARGET, compute_uv=False)
    check("unscaled_analytic_singular_values", np.allclose(sv_unscaled, [PHI, 1, 1, 1/PHI], rtol=0, atol=2e-15))
    check("unscaled_not_contractive", sv_unscaled[0] > 1)
    check("target_analytic_singular_values", np.allclose(sv_target, [1, 1/PHI, 1/PHI, 1/PHI**2], rtol=0, atol=2e-15))
    check("target_contractive", sv_target[0] <= 1 + 2e-15)
    witness = H4[0]
    witness_unscaled_power_ratio = float(np.linalg.norm(A_PHI @ witness) ** 2)
    check("pinion_gain_witness", abs(witness_unscaled_power_ratio - PHI**2) < 2e-15)
    check("scaled_witness_no_power_gain", abs(np.linalg.norm(TARGET @ witness) ** 2 - 1) < 2e-15)
    check("unscaled_volume_not_power", abs(abs(np.linalg.det(A_PHI)) - 1) < 2e-15)

    # Illustrative material-state-to-amplitude mapping, NOT a measured law:
    # t(g)=exp(-2g), 0<=g<=1, with a separate fixed pi phase on output 4.
    ideal_amplitudes = np.array([1, 1/PHI**2, 1/PHI, 1/PHI])
    material_g = -0.5 * np.log(ideal_amplitudes)
    fixed_phases = np.array([0, 0, 0, np.pi])
    material_target = np.diag(np.exp(-2*material_g) * np.exp(1j*fixed_phases)) @ H4
    check("illustrative_material_encoding", np.allclose(material_target, TARGET, rtol=0, atol=2e-16))
    check("illustrative_material_state_bounds", np.all((material_g >= 0) & (material_g <= 1)))

    r0 = STATIC_AMPLITUDE * np.exp(1j * STATIC_PHASE_RAD)
    drift = DRIFT_AMPLITUDE_RATIO * np.exp(1j * DRIFT_PHASE_RAD)
    r1 = drift * r0
    s0, s1 = r0[:, None] * TARGET, r1[:, None] * TARGET
    check("both_synthetic_transfers_passive", all(np.linalg.svd(s, compute_uv=False)[0] <= 1 for s in (s0, s1)))
    _, noiseless_hat = synthetic_basis(s0, np.zeros((4,4), dtype=np.complex128))
    check("basis_recovers_noiseless_transfer", np.allclose(noiseless_hat, s0, rtol=0, atol=1e-16))
    clean_cal = fit_row_calibration(s0)
    check("row_fit_recovers_exact_coefficients", np.allclose(clean_cal["row_factors"], r0, rtol=0, atol=2e-16))
    check("exact_decoder_restores_unscaled_target", np.allclose(clean_cal["decoder_factors"][:,None]*s0, A_PHI, rtol=0, atol=3e-16))
    cal_noise0 = PROBE_AMPLITUDE * CAL_NOISE_RELATIVE * CAL_NOISE_PATTERN
    cal_noise1 = PROBE_AMPLITUDE * CAL_NOISE_RELATIVE * (0.75j * CAL_NOISE_PATTERN.T)
    y_basis0, s_hat0 = synthetic_basis(s0, cal_noise0)
    y_basis1, s_hat1 = synthetic_basis(s1, cal_noise1)
    cal0, cal1 = fit_row_calibration(s_hat0), fit_row_calibration(s_hat1)
    check("both_noisy_calibrations_pass_policy", cal0["relative_model_residual"] < POLICY["maximum_relative_row_model_residual"] and cal1["relative_model_residual"] < POLICY["maximum_relative_row_model_residual"])

    inputs = PROBE_AMPLITUDE * HOLDOUT_RAW / np.linalg.norm(HOLDOUT_RAW, axis=1)[:,None]
    check("heldout_input_power_normalization", np.allclose(np.sum(np.abs(inputs)**2, axis=1), P_REFERENCE_W, rtol=0, atol=1e-18))
    row_records = []
    columns = {k: [] for k in ("static_scalar", "static_calibrated", "drift_stale", "drift_refreshed")}
    for i, a in enumerate(inputs):
        n = PROBE_AMPLITUDE * READ_NOISE_RELATIVE * READ_NOISE_PATTERN[i]
        x = a / PROBE_AMPLITUDE
        ideal = A_PHI @ x
        field0, field1 = s0 @ a, s1 @ a
        obs0, obs1 = field0 + n, field1 + n
        estimates = {"static_scalar": PHI * obs0 / PROBE_AMPLITUDE,
                     "static_calibrated": decode(cal0, obs0),
                     "drift_stale": decode(cal0, obs1),
                     "drift_refreshed": decode(cal1, obs1)}
        errors = {k: float(np.linalg.norm(v-ideal) / np.linalg.norm(ideal)) for k,v in estimates.items()}
        for k,v in errors.items():
            columns[k].append(v)
        # Exact operator bound includes calibration error AND detector noise.
        mismatch = np.diag(cal1["decoder_factors"]) @ s1 - A_PHI
        bound = float((np.linalg.norm(mismatch, 2)*np.linalg.norm(a)
                       + cal1["max_decoder_gain"]*np.linalg.norm(n)) / PROBE_AMPLITUDE)
        actual_error = float(np.linalg.norm(estimates["drift_refreshed"]-ideal))
        check(f"decoder_error_bound_input_{i}", actual_error <= bound + 1e-15)
        check(f"physical_transfer_power_input_{i}", float(np.vdot(field1,field1).real) <= P_REFERENCE_W + 1e-18)
        row_records.append({"input_id": i, "x_dimensionless": x, "a_sqrt_w": a,
                            "ideal_unscaled_numerical_output": ideal,
                            "read_noise_sqrt_w": n, "static_readout": obs0, "drifted_readout": obs1,
                            "decoded_outputs": estimates, "relative_l2_errors": errors,
                            "refreshed_error_norm": actual_error, "refreshed_error_bound": bound,
                            "noiseless_static_output_power_w": float(np.vdot(field0,field0).real),
                            "noiseless_drifted_output_power_w": float(np.vdot(field1,field1).real)})
    check("calibration_improves_all_synthetic_holdouts", all(c < n for c,n in zip(columns["static_calibrated"],columns["static_scalar"])))
    check("refresh_improves_all_drifted_holdouts", all(f < s for f,s in zip(columns["drift_refreshed"],columns["drift_stale"])))
    check("refreshed_example_below_0_1_percent", max(columns["drift_refreshed"]) < 0.001)
    check("nonzero_detector_noise_amplified", cal1["max_decoder_gain"] > 1)

    # Basis inputs 1 and 2 produce equal intensities but distinct fields.
    e0, e1 = PROBE_AMPLITUDE*np.eye(4)[0], PROBE_AMPLITUDE*np.eye(4)[1]
    b0, b1 = TARGET @ e0, TARGET @ e1
    check("intensity_ambiguity_equal_powers", np.array_equal(np.abs(b0)**2,np.abs(b1)**2))
    check("intensity_ambiguity_different_fields", np.linalg.norm(b0-b1)>0)

    dark = s0.copy(); dark[1,:] = 0
    high_gain = s0.copy(); high_gain[1,:] = 0.2*TARGET[1,:]
    wrong_model = s0.copy(); wrong_model[0,:] += 0.2*TARGET[1,:]
    nonfinite = s0.copy(); nonfinite[0,0] = np.nan
    rejections = [
        reject("dark_row_rejected",dark,"singular_or_dark_transfer"),
        reject("high_decoder_gain_rejected",high_gain,"decoder_gain_too_large"),
        reject("cross_row_mixing_rejected",wrong_model,"row_model_mismatch"),
        reject("nonfinite_calibration_rejected",nonfinite,"invalid_shape_or_nonfinite"),
    ]

    setup, per_task, digital = Fraction(2,1000), Fraction(3,1_000_000), Fraction(5,1_000_000)
    n_min = minimum_reuse(setup,per_task,digital)
    check("energy_strict_break_even_integer", n_min == 1001)
    check("energy_at_1000_equal", setup+1000*per_task == 1000*digital)
    check("energy_at_1001_better", setup+1001*per_task < 1001*digital)
    check("energy_no_break_even_if_running_cost_not_lower", minimum_reuse(setup,digital,digital) is None)
    blocks = []
    for length in (800,2000):
        blocks.append({"valid_tasks_before_recalibration":length,
                       "hybrid_energy_j":float(setup+length*per_task),
                       "digital_energy_j":float(length*digital),
                       "hybrid_lower":setup+length*per_task < length*digital})
    check("frequent_recalibration_erases_illustrative_advantage", blocks[0]["hybrid_lower"] is False and blocks[1]["hybrid_lower"] is True)

    return encode({
        "schema":"a18-numerical-reference-v2", "status":"passed",
        "scope":"Synthetic four-input/four-output mathematics and software checks only; no hardware measurements.",
        "utc_executed":datetime.now(timezone.utc).isoformat(),
        "environment":{"python":sys.version,"python_executable":sys.executable,
                       "numpy":np.__version__,"platform":platform.platform(),
                       "machine":platform.machine(),"numeric_types":["float64","complex128"],
                       "replay":"Tolerance-based numerical reproduction; exact listed inputs; no RNG.",
                       "linear_algebra":"NumPy SVD; no physical device backend"},
        "provenance":{"pm_edition":"Perpetuum Mobile 1.0", "pm_pages":[22,23],
                      "pm_content_json_sha256":observed_source_hash,
                      "pm_content_expected_sha256":SOURCE_PM_CONTENT_SHA256,
                      "pm_content_path_verified":str(pm_content.resolve()),
                      "pm_content_bytes_verified":len(source_bytes),
                      "pm_content_hash_verification":"matched actual source file during this run",
                      "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        "output_units":{"input_x":"dimensionless; norm(x)<=1; holdouts have norm(x)=1",
                        "physical_input_a":"sqrt(W); a=A0*x",
                        "physical_coherent_readouts_and_noise":"sqrt(W)",
                        "A0":"sqrt(W); sqrt(reference_input_power_w)",
                        "ideal_unscaled_numerical_output":"dimensionless; y=A_phi*x",
                        "decoded_outputs":"dimensionless; y_hat=(phi/r_hat)*readout/A0",
                        "refreshed_error_norm_and_bound":"dimensionless",
                        "decoder_factors":"dimensionless calibration multipliers; normalization by A0 is separate",
                        "optical_output_power":"W; derived only from noiseless physical fields, not decoded y"},
        "checks_passed":len(checks),"checks":checks,
        "matrices":{"phi":PHI,"h4":H4,"unscaled_pinion":A_PHI,"passive_target":TARGET,
                    "singular_values_unscaled":sv_unscaled,"singular_values_target":sv_target,
                    "eigenvalues_target_gram":np.linalg.eigvalsh(TARGET.conj().T@TARGET),
                    "unscaled_abs_determinant":abs(np.linalg.det(A_PHI)),
                    "maximum_power_gain_witness_input":witness,
                    "unscaled_witness_power_ratio":witness_unscaled_power_ratio},
        "illustrative_material_encoding":{"status":"Chosen surrogate, not measured constitutive physics",
                    "formula":"amplitude t(g)=exp(-2*g), 0<=g<=1; fixed fourth-output phase pi",
                    "state_g":material_g,"target_amplitudes":ideal_amplitudes,"fixed_phase_rad":fixed_phases,
                    "no_programming_dynamics_claim":True},
        "parameters":{"reference_input_power_w":P_REFERENCE_W,"basis_probe_amplitude_sqrt_w":PROBE_AMPLITUDE,
                      "static_output_amplitudes":STATIC_AMPLITUDE,"static_phase_errors_rad":STATIC_PHASE_RAD,
                      "drift_amplitude_ratios":DRIFT_AMPLITUDE_RATIO,"drift_phase_errors_rad":DRIFT_PHASE_RAD,
                      "calibration_noise_relative_scale":CAL_NOISE_RELATIVE,
                      "calibration_noise_pattern":CAL_NOISE_PATTERN,
                      "refreshed_noise_pattern_rule":"0.75j * original_pattern.T",
                      "heldout_raw_complex_vectors":HOLDOUT_RAW,"read_noise_relative_scale":READ_NOISE_RELATIVE,
                      "read_noise_pattern":READ_NOISE_PATTERN,"acceptance_policy":POLICY},
        "synthetic_calibration":{"static_transfer":s0,"drifted_transfer":s1,
                      "static_basis_observations_sqrt_w":y_basis0,"drifted_basis_observations_sqrt_w":y_basis1,
                      "static_reconstructed_transfer":s_hat0,"drifted_reconstructed_transfer":s_hat1,
                      "static_calibration":cal0,"refreshed_calibration":cal1,
                      "fit_formula":"r_hat_i=sum_j(S_hat_ij*conj(TARGET_ij))/sum_j(abs(TARGET_ij)^2)",
                      "decode_formula":"dimensionless_output_i=(phi/r_hat_i)*coherent_readout_i/A0",
                      "error_bound":"(||D*S-A_phi||_2*||a||_2 + ||D||_2*||noise||_2)/A0; D=diag(phi/r_hat)",
                      "model_boundary":"Four complex per-output corrections only. Reject cross-row error, severe attenuation and singular transfer.",
                      "decoder_boundary":"Numerical rescaling and complex correction do not create optical energy; they amplify noise and incur computation."},
        "heldout_inputs":row_records,
        "summary_relative_errors":{k:{"minimum":min(v),"mean":float(np.mean(v)),"maximum":max(v)} for k,v in columns.items()},
        "intensity_ambiguity":{"inputs_sqrt_w":[e0,e1],"distinct_fields_sqrt_w":[b0,b1],
                               "identical_output_intensities_w":np.abs(b0)**2,
                               "conclusion":"Power-only readings cannot identify signed/complex output; a common coherent reference is required."},
        "rejected_calibrations":rejections,
        "energy_break_even":{"status":"Illustrative algebra; all energy values are chosen inputs, not measurements",
                            "equations":["E_hybrid=E_setup+N*e_hybrid","E_digital=N*e_digital",
                                         "hybrid lower iff N*(e_digital-e_hybrid)>E_setup"],
                            "setup_energy_j":float(setup),"hybrid_per_task_j":float(per_task),
                            "digital_per_task_j":float(digital),"minimum_integer_reuse":n_min,
                            "recalibration_blocks":blocks,
                            "boundary":"Same useful task/accuracy and full energy boundary required. Recalibration starts a new setup cost. Real values unknown."},
        "limitations":["No hardware, source CUDA, physical calibration, endurance or application-performance experiment was run.",
                       "All loss, drift, material mapping and noise are explicitly chosen synthetic inputs.",
                       "Finite probes and holdouts do not prove universal model adequacy or statistical noise properties.",
                       "Stable common phase reference, narrowband operation and a fixed configuration during each vector are assumed.",
                       "The 4x4 forward transfer is a sub-block; reflections, reverse paths and losses require a complete physical port account.",
                       "No new random generator is used; PPM-SEED remains unchanged and optional for a later stimulus extension."],
        "implementation_references":["https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html",
                                     "https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html"],
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,default=Path(__file__).with_name("reference_results.json"))
    parser.add_argument("--pm-content",type=Path,default=None,
                        help="Original PM content.json to verify; default is the neighboring perpetuum_mobile_source/content.json")
    args = parser.parse_args()
    result = run_reference(args.pm_content)
    args.out.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"checks_passed":result["checks_passed"],
                      "summary_relative_errors":result["summary_relative_errors"],
                      "maximum_decoder_gain":result["synthetic_calibration"]["refreshed_calibration"]["max_decoder_gain"],
                      "minimum_reuse":result["energy_break_even"]["minimum_integer_reuse"],
                      "output":str(args.out)},indent=2))
