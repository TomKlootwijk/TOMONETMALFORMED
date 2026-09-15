# PPM-SEED-v1 / exact contract and conformance

## B. Proposed SEED definition (new, not inherited)

### B1. Core bytes and normalization

Name: **PPM-SEED-v1**. H means SHA-256, `||` byte concatenation, U16/U64 mean fixed-width unsigned big-endian integers. All field lengths are byte counts. Every shown `\0` is one NUL byte (hex 00), not backslash-plus-zero. Reject overflow; never wrap a counter/length. SHA-256 is specified by NIST FIPS 180-4 [E1]; this custom labeled counter construction is an editorial reproducibility definition, not a standardized DRBG or security claim.

Core seed S is exactly 32 bytes, the big-endian representation of an integer in `[0,2^256)`. Persist as exactly 64 lowercase hex digits. A decimal input adapter accepts ASCII `0|[1-9][0-9]*` only, rejects signs, whitespace, leading zeroes, non-ASCII digits and out-of-range values, then emits U256. Equivalent decimal and fixed hex seeds identify the same S.

Optional explicitly named text adapter: strict UTF-8 of the input Unicode scalar sequence, no Unicode normalization, trimming, newline change or case folding; reject lone surrogates. `S = H(ASCII("PPM/TEXT/v1") || 00 || U64(len(t)) || t)`. Visually equivalent but differently encoded strings can intentionally give different seeds; persist the resulting canonical seed hex and the adapter identifier. Public seeds carry no secrecy promise.

### B2. Manifest C and binding

The canonical manifest is a restricted RFC 8785 JSON subset [E2]: UTF-8 without BOM; no whitespace between tokens; recursively sorted ASCII object keys; preserved array order; JSON null/booleans/strings/arrays/objects only. Keys match `[a-z][a-z0-9_]*`. Values preserve Unicode scalar sequences as-is, reject lone surrogates. Escape quote/backslash, controls 08/09/0a/0c/0d as `\b\t\n\f\r`, other U+0000-001F as lowercase `\u00hh`; leave `/` and remaining Unicode unescaped. Reject duplicate keys, ALL JSON numeric tokens (including -0), NaN/Infinity, invalid UTF-8 and unsupported types. Integers, real constants, units and tolerances use schema-typed strings; no numeric coercion. ASCII-only keys make RFC 8785 UTF-16 sorting identical to byte order. The reference `json.dumps` matches this deliberately restricted subset; it is not a general-purpose RFC 8785 implementation.

Exactly nine root fields are required: `schema`, `family`, `sub_v`, `numeric_mode`, `seed_hex`, `sources`, `assets`, `algorithms`, `parameters`. Schema exactly `ppm-seed-v1`; family/sub_v/numeric_mode are nonempty slash-delimited lower ASCII identifiers with components `[a-z0-9_.-]+`. `sources` and `assets` are arrays of `{id,sha256}`, unique and sorted by ASCII id, hash values exactly 64 lowercase hex digits. `algorithms` and `parameters` are objects; the selected application sub-V defines and validates every required field/typed string. Reject missing/extra root fields. For an actual source-based run, source entries bind the four original file hashes; fixture-only manifests may deliberately have empty reference lists.

Let C be these canonical bytes; then:

`m = H("PPM/MANIFEST/v1\0" || U64(len(C)) || C)`

`K = H("PPM/SEED/v1\0" || S || m)`

The seed appearing in C must equal S. Source/asset hashes refer to their exact byte contents. The manifest fixes profile versions, numerical mode, deterministic algorithm choices, shapes, parameter units/values, initial-state encoding and input/asset identities. Timestamp, host path and observational performance metadata go in a separate receipt unless they are actual mathematical inputs. No manifest may contain its own digest, result digest or a mutable output reference; that would create a binding cycle. Application validators must resolve referenced contents and check their hashes; the lightweight seed module validates reference syntax, not file existence/content or application semantics.

### B3. Random-access stream and range sampling

`B(d,c) = H("PPM/BLOCK/v1\0" || K || U16(len(d)) || ASCII(d) || U64(c))`

Domain d has 1-65,535 ASCII bytes with slash-separated nonempty components `[a-z0-9_.-]+`; counter c is `[0,2^64)`. Algorithms assign explicit stable domains to logical entities and sampling sites, e.g. `geometry/instance/0/position`. Never use worker/thread IDs or wall-clock arrival order. If domains include numeric IDs, the application schema requires canonical decimal strings. A domain plus counter is one identity; distinct APIs/sites must not unintentionally reuse it. Rejection consumption advances only that domain. A raw-byte API returns all 32 bytes of B; the normative u64 sampling API takes only the first eight bytes as big-endian x and discards the other 24. Do not silently substitute platform RNGs or byte order.

For n in `[1,2^64]`, compute L = 2^64 - (2^64 mod n) in arithmetic wide enough to represent 2^64. Repeatedly draw x at c, increment c, reject x >= L, otherwise return x mod n. The terminal next-counter value 2^64 means exhausted; it is never hashed or wrapped. Failure to find an accepted draw before exhaustion produces an explicit exhaustion error (the reference raises ValueError; an application may map it to a named status). Record start counter, consumed count including rejects, n and result. Every residue occurs exactly L/n times among accepted 64-bit words; hence the mapping adds no modulo bias **conditional on uniform input words**. A fixed public seed is deterministic, not a physical random source; this does not prove perfect SHA-256 distribution across finite seed sets.

For a [0,1) binary64 grid sample, use `u = (x >> 11) * 2^-53`, discarding low 11 bits. The retained integer fits exactly in binary64 and the power-of-two scaling is exact; endpoint 1 is excluded. This is a different registered sampling API/domain, not an extra unrecorded draw. Distribution transforms (Gaussian, etc.) require separately pinned algorithms and math/numeric contracts.

### B4. Transcript and replay contract

For exact initial-state bytes X0 under the family schema:

`T0 = H("PPM/TRANSCRIPT/v1\0" || m || U64(len(X0)) || X0)`.

For event i starting at zero, let Ei be its constrained-canonical JSON bytes:

`T(i+1) = H("PPM/EVENT/v1\0" || Ti || U64(i) || U64(len(Ei)) || Ei)`.

Every family defines event schemas with logical tick/index, ordered external input or measurement bytes/content hashes, domain/counter and reject count for draws, state transition/outcome/status, and checkpoint state hash. Physical timestamps, units, sensor calibration and uncertainty are external-input facts, never generated retroactively by a seed. Receipt records terminal event count, final Ti, exact manifest/initial-state/input files, implementation/compiler/math/backend versions and verification result. Replay resolves and hashes all inputs, recomputes each draw and transition, compares each event/counter/status in logical order, and checks terminal count plus checkpoint/final-state hashes; comparing a hash alone is not execution validation. Missing dependencies or divergent first event gives explicit failure/unavailable, not fabricated data.

Terminal count is necessary to detect truncation relative to the expected receipt. Unsigned hashes/chains only support integrity relative to a trusted expected value; they do not authenticate an author and are fully recomputable by an editor. Schedule-independent streams do not automatically make the full program deterministic: event ordering, reductions, state updates and external inputs also need contracts.

### B5. Numerical modes and replay levels

- **u64-mod**: state words represent integers modulo 2^64. Add/multiply reduce modulo 2^64, bitwise operations are on 64 bits, right shift is logical. Shift counts outside 0-63 are rejected unless a family explicitly chooses another named behavior. Words serialize as eight big-endian bytes / 16 lowercase hex digits. Boolean JK/state/reason comparisons exact. This mode alone does not implement floating geometric kernels.
- **fixed-q** (family specialization required): integers plus declared scale 2^-f, widths and units; exact intermediate arithmetic; round to nearest, ties to even only at declared rescaling points; overflow gives a named error unless that family explicitly chooses modular arithmetic. It can promise cross-platform exact replay once each operation is specified.
- **binary64-pinned**: IEEE binary64 round-to-nearest/ties-even, evaluation/reduction order, FMA/contraction, subnormal behavior, signed-zero/NaN/status rules, constant bit patterns, transcendental implementation/version and compiler/backend flags all pinned. Persist actual 64-bit values as 16 lowercase hex digits under the schema. Claim bitwise replay only for the validated environment set; binary64 alone is insufficient. NVIDIA documents the relevance of FMA and operation order [E6].
- **binary64-tolerance**: a separately named comparison policy, e.g. `abs(a-b) <= abs_tol + rel_tol*max(abs(a),abs(b))`, with units, tolerances and NaN/undefined handling fixed before the run. Integer/state/status fields stay exact. Angle comparisons must choose circular or literal differences explicitly. For inherited K1, keep its own published angular/invariant thresholds (2e-11 rad / 1e-10) rather than substituting this example policy. Tolerance agreement is not bitwise replay, and success on outputs cannot hide divergent discrete branches.

Levels: stream-byte identity; exact deterministic state replay; tolerance-conformant numerical replay; statistical/measurement compatibility. Report which is achieved. SEED does not supply an energy source, ensure numerical stability, establish a physical law, or validate real-world autonomous cycles.

## C. Locally executed new reference checks

Files beside this note:

- `seed_reference_v1.py`: minimal Python stdlib reference, not source-PDF code.
- `seed_reference_v1_results.json`: **46 passed checks**, Python 3.13.11, Windows 11 build 26200.
- `seed_reference_v1_crosscheck.ps1`: independently reconstructs the fixed manifest frame, seed frame and three block frames using .NET SHA-256.
- `seed_reference_v1_crosscheck_results.json`: **5 passed comparisons**, PowerShell 7.6.5, .NET 10.0.11, same Windows machine.

Coverage includes NIST `abc` SHA-256 value [E7], empty SHA-256, seed format/range rejection, decimal/hex equivalence, Unicode preservation/surrogate rejection, canonical key/escape handling, duplicate/numeric/NaN/BOM/UTF-8 rejects, manifest binding and key-order invariance, counter/domain changes, wrap/domain-length rejection, 64-bit rejection boundaries, exhausted stream, binary64 grid endpoints, transcript mutation, and an exhaustive reduced-width 8-bit illustration for all 256 possible ranges. These are finite reference checks, not a formal proof of Python/.NET, a second-platform qualification, a full application replay, or any CUDA/physical rerun.

Fixture canonical manifest is 272 bytes (exact string in results JSON), seed 64 zero hex digits, family digital, sub_v reference-1.0.0, numeric_mode u64-mod; domain `geometry/instance/0/position` is 28 bytes. Empty source/asset lists explicitly mean this is a standalone conformance fixture.

| Field | Exact hexadecimal value |
|---|---|
| Manifest prefix | `50504d2f4d414e49464553542f763100` |
| Seed prefix | `50504d2f534545442f763100` |
| Block prefix | `50504d2f424c4f434b2f763100` |
| Text prefix | `50504d2f544558542f763100` |
| m | `f2d7055b0a5fc0b30c0a5e89e9a449865cc3d32592855b829b634df7a6643b77` |
| K | `32ab7cdd6e624f91afef400f59ac5a8762526ba4d6ef72b40b344c9aba2b9714` |
| B(d,0) | `1bf021f9bb711c5514a3075a26a407c75959e1730dbd5df9e22f2942800b7622` |
| B(d,1) | `d0a14fda9e7fa168805bfb8afb27484ad1a53e23b880a0c09fd9ba36c8796257` |
| B(d,2) | `2a04b004b30040b75087785dfc816ae36799c4c16eb1046abff0abeaa30712e2` |
| T0 for eight 00 state bytes | `dcfbde3d36d39bbf075680548e2b6476cbc371a1c0d6ca46e60d0a22ef17361e` |

First ten range-n=10 outputs: **7, 6, 7, 4, 8, 4, 2, 7, 9, 8**; one block consumed each. The first block input's full bytes and first transcript event/value are included in the JSON receipt. Prefixes, length fields, byte order and full SHA values are essential test-vector inputs; displaying seed and outputs alone would not fix the algorithm.

## D. Verified primary external references (retrieved 15 September 2026)

- **E1, SHA-256 definition/integrity purpose:** NIST, FIPS 180-4, Secure Hash Standard. https://csrc.nist.gov/pubs/fips/180-4/upd1/final . The page notes a planned revision; this contract explicitly pins SHA-256 under FIPS 180-4.
- **E2, canonical JSON:** RFC 8785 sections 3.1, 3.2.2.2, 3.2.3, 3.2.4. https://www.rfc-editor.org/rfc/rfc8785.html . Used for preserved strings, invalid Unicode rejection, string escaping, sorted keys and UTF-8. This is an informational RFC, not an Internet Standards Track specification. The custom profile prohibits numeric tokens and restricts keys.
- **E3, Python API:** official hashlib documentation. https://docs.python.org/3/library/hashlib.html . Supports byte-oriented SHA-256/digest use in the local reference; does not validate this new custom stream.
- **E4, cache metric semantics/cold replay:** NVIDIA Nsight Compute Profiling Guide, hardware model/metrics and cache control. https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html#metrics-reference and https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html#cache-control . A sector is 32 bytes; default replay cache flushing affects kernel-isolation interpretation. This confirms terminology, not the PDF's retained logs.
- **E5, PTX cache hints/asynchronous completion:** NVIDIA PTX ISA 8.7, sections 9.7.9.1 and 9.7.9.25.1-.2. https://docs.nvidia.com/cuda/archive/12.8.1/parallel-thread-execution/index.html . Cache operators are performance hints; asynchronous results need appropriate completion/order handling, including proxy synchronization.
- **E6, floating-point reproducibility:** NVIDIA, Floating Point and IEEE 754. https://docs.nvidia.com/cuda/floating-point/index.html . Supports distinctions among IEEE formats, operation order and fused operations; not a blanket bitwise guarantee for application code.
- **E7, SHA-256 known example:** NIST, Secure Hash Algorithm - Message Digest Length = 256, single-block `abc` example. https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/SHA256.pdf . Expected digest `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`.

Suggested PDF summary: “The source report supplies bounded evidence for its K1 CUDA implementation. The present document adds a precisely serialized SEED extension and local reference checks. Neither evidence category establishes an autonomous physical energy source or universal correctness of every proposed application family.”
