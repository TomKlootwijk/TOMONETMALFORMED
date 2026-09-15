"""Proposed PPM-SEED-v1 reference, authored for Perpetuum Mobile.

This is new specification support, not code extracted from the source PDFs.
Uses Python's standard library only. SHA-256 stream is for reproducibility;
this module makes no DRBG certification, secrecy, or authentication claim.
"""
from __future__ import annotations
import copy
import hashlib
import json
import platform
import re
from pathlib import Path

H = lambda b: hashlib.sha256(b).digest()
KEY = re.compile(r"[a-z][a-z0-9_]*\Z", re.ASCII)
HEX64 = re.compile(r"[0-9a-f]{64}\Z", re.ASCII)
DECIMAL = re.compile(r"(?:0|[1-9][0-9]*)\Z", re.ASCII)
DOMAIN = re.compile(r"[a-z0-9_.-]+(?:/[a-z0-9_.-]+)*\Z", re.ASCII)
REQUIRED = {"schema", "family", "sub_v", "numeric_mode", "seed_hex",
            "sources", "assets", "algorithms", "parameters"}

def ube(n: int, width: int) -> bytes:
    if type(n) is not int or not 0 <= n < 1 << (8 * width):
        raise ValueError("unsigned integer outside field range")
    return n.to_bytes(width, "big")

def seed_decimal(s: str) -> bytes:
    if type(s) is not str or not DECIMAL.fullmatch(s) or len(s) > 78:
        raise ValueError("seed decimal must be canonical ASCII decimal")
    return ube(int(s), 32)

def seed_hex(s: str) -> bytes:
    if type(s) is not str or not HEX64.fullmatch(s):
        raise ValueError("seed hex must be 64 lowercase hexadecimal characters")
    return bytes.fromhex(s)

def seed_text(s: str) -> bytes:
    if type(s) is not str:
        raise ValueError("text seed must be a Unicode scalar string")
    raw = s.encode("utf-8", errors="strict")
    return H(b"PPM/TEXT/v1\0" + ube(len(raw), 8) + raw)

def _value(v):
    if v is None or type(v) is bool:
        return
    if type(v) is str:
        v.encode("utf-8", errors="strict")  # Reject lone surrogates.
        return
    if type(v) is list:
        for x in v:
            _value(x)
        return
    if type(v) is dict:
        for k, x in v.items():
            if type(k) is not str or not KEY.fullmatch(k):
                raise ValueError("keys must be lower ASCII snake_case identifiers")
            _value(x)
        return
    raise ValueError("JSON numeric tokens and non-JSON types are prohibited")

def canonical(v) -> bytes:
    """Restricted RFC 8785 subset; ASCII keys; all numbers are typed strings."""
    _value(v)
    return json.dumps(v, ensure_ascii=False, allow_nan=False,
                      sort_keys=True, separators=(",", ":")).encode("utf-8")

def parse_json(raw: bytes):
    def pairs(ps):
        d = {}
        for k, v in ps:
            if k in d:
                raise ValueError("duplicate object key")
            d[k] = v
        return d
    def no_number(_):
        raise ValueError("JSON numeric tokens are prohibited")
    if not isinstance(raw, bytes) or raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("expected UTF-8 bytes without BOM")
    v = json.loads(raw.decode("utf-8", errors="strict"), object_pairs_hook=pairs,
                   parse_int=no_number, parse_float=no_number,
                   parse_constant=no_number)
    _value(v)
    return v

def manifest_bytes(m: dict) -> bytes:
    if type(m) is not dict or set(m) != REQUIRED:
        raise ValueError("wrong manifest fields")
    if m["schema"] != "ppm-seed-v1":
        raise ValueError("wrong manifest schema")
    for k in ("family", "sub_v", "numeric_mode"):
        if type(m[k]) is not str or not DOMAIN.fullmatch(m[k]):
            raise ValueError("invalid profile identifier")
    seed_hex(m["seed_hex"])
    for k in ("algorithms", "parameters"):
        if type(m[k]) is not dict:
            raise ValueError("expected object")
    for k in ("sources", "assets"):
        entries = m[k]
        if type(entries) is not list:
            raise ValueError("expected list")
        ids = []
        for e in entries:
            if type(e) is not dict or set(e) != {"id", "sha256"}:
                raise ValueError("wrong content reference")
            if type(e["id"]) is not str or not DOMAIN.fullmatch(e["id"]):
                raise ValueError("invalid content id")
            seed_hex(e["sha256"])
            ids.append(e["id"])
        if ids != sorted(ids) or len(set(ids)) != len(ids):
            raise ValueError("references must have unique sorted ids")
    return canonical(m)

def bind_manifest(m: dict) -> tuple[bytes, bytes, bytes]:
    raw = manifest_bytes(m)
    digest = H(b"PPM/MANIFEST/v1\0" + ube(len(raw), 8) + raw)
    key = H(b"PPM/SEED/v1\0" + seed_hex(m["seed_hex"]) + digest)
    return raw, digest, key

def block(key: bytes, domain: str, counter: int) -> bytes:
    if type(key) is not bytes or len(key) != 32:
        raise ValueError("key must be 32 bytes")
    if type(domain) is not str or not DOMAIN.fullmatch(domain):
        raise ValueError("invalid domain identifier")
    d = domain.encode("ascii")
    return H(b"PPM/BLOCK/v1\0" + key + ube(len(d), 2) + d + ube(counter, 8))

def range_from_words(n: int, words):
    """A bounded iterable models the remaining counter space for one stream."""
    if type(n) is not int or not 1 <= n <= 1 << 64:
        raise ValueError("range must be in [1, 2^64]")
    limit = (1 << 64) - ((1 << 64) % n)
    for consumed, x in enumerate(words, 1):
        ube(x, 8)
        if x < limit:
            return x % n, consumed
    raise ValueError("stream exhausted without accepted sample")

def sample_range(key: bytes, domain: str, counter: int, n: int):
    ube(counter, 8)
    words = (int.from_bytes(block(key, domain, c)[:8], "big")
             for c in range(counter, 1 << 64))
    value, consumed = range_from_words(n, words)
    # The returned next value may be 2^64: this is a terminal cursor, not a block.
    return value, counter + consumed, consumed

def unit_interval(word: int) -> float:
    """Exact binary64 grid point in [0,1), using the high 53 bits."""
    ube(word, 8)
    return (word >> 11) * (2.0 ** -53)

def transcript_start(manifest_digest: bytes, initial_state: bytes) -> bytes:
    if type(manifest_digest) is not bytes or len(manifest_digest) != 32:
        raise ValueError("manifest digest must be 32 bytes")
    if type(initial_state) is not bytes:
        raise ValueError("initial state must be bytes")
    return H(b"PPM/TRANSCRIPT/v1\0" + manifest_digest
             + ube(len(initial_state), 8) + initial_state)

def transcript_step(previous: bytes, index: int, event: dict) -> bytes:
    if type(previous) is not bytes or len(previous) != 32:
        raise ValueError("previous digest must be 32 bytes")
    if type(event) is not dict:
        raise ValueError("event must be an object")
    raw = canonical(event)
    return H(b"PPM/EVENT/v1\0" + previous + ube(index, 8) + ube(len(raw), 8) + raw)

FIXTURE = {
    "schema": "ppm-seed-v1", "family": "digital", "sub_v": "reference-1.0.0",
    "numeric_mode": "u64-mod", "seed_hex": "0" * 64,
    "sources": [], "assets": [], "algorithms": {"sampler": "sha256-counter-v1"},
    "parameters": {"range_n": "10"},
}

def check_suite():
    checks = []
    def ok(name, condition):
        if not condition:
            raise AssertionError(name)
        checks.append(name)
    def rejects(name, f):
        try:
            f()
        except (ValueError, UnicodeError):
            checks.append(name)
        else:
            raise AssertionError("did not reject: " + name)
    ok("nist_sha256_abc", H(b"abc").hex() ==
       "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
    ok("sha256_empty", H(b"").hex() ==
       "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    ok("seed_decimal_hex_equivalence", seed_decimal("42") == seed_hex("0" * 62 + "2a"))
    ok("seed_max", seed_decimal(str((1 << 256) - 1)) == b"\xff" * 32)
    for name, value in [("seed_negative", "-1"), ("seed_overflow", str(1 << 256)),
                        ("seed_whitespace", " 1"), ("seed_leading_zero", "01"),
                        ("seed_unicode_digit", "\u0661")]:
        rejects(name, lambda v=value: seed_decimal(v))
    rejects("seed_uppercase_hex", lambda: seed_hex("A" * 64))
    ok("text_preserves_unicode_sequence", seed_text("\u00e9") != seed_text("e\u0301"))
    rejects("text_lone_surrogate", lambda: seed_text("\ud800"))
    ok("canonical_key_order", canonical({"z":"2", "a":"1"}) == b'{"a":"1","z":"2"}')
    ok("canonical_string_escaping", canonical({"a":"\b\t\n\f\r\x00\"\\/"}) ==
       b'{"a":"\\b\\t\\n\\f\\r\\u0000\\\"\\\\/"}')
    ok("canonical_no_unicode_normalization", canonical({"a":"\u00e9"}) != canonical({"a":"e\u0301"}))
    for name, raw in [("duplicate_keys", b'{"a":"1","a":"2"}'),
                      ("integer_token", b'{"a":1}'), ("float_token", b'{"a":1.0}'),
                      ("negative_zero_token", b'{"a":-0}'), ("nan_token", b'{"a":NaN}'),
                      ("bom", b'\xef\xbb\xbf{}'), ("bad_utf8", b'{"a":"\xff"}'),
                      ("invalid_key", b'{"A":"1"}')]:
        rejects(name, lambda r=raw: parse_json(r))
    raw, md, key = bind_manifest(FIXTURE)
    ok("manifest_parser_roundtrip", canonical(parse_json(raw)) == raw)
    reordered = dict(reversed(list(FIXTURE.items())))
    ok("manifest_key_order_invariant", bind_manifest(reordered) == (raw, md, key))
    edited = copy.deepcopy(FIXTURE)
    edited["parameters"]["range_n"] = "11"
    ok("manifest_change_changes_stream", bind_manifest(edited)[2] != key)
    edited = copy.deepcopy(FIXTURE)
    edited["seed_hex"] = "0" * 63 + "1"
    ok("seed_change_changes_stream", bind_manifest(edited)[2] != key)
    d = "geometry/instance/0/position"
    blocks = [block(key, d, i) for i in range(3)]
    ok("counter_separation", len(set(blocks)) == 3)
    ok("domain_separation", block(key, "geometry/instance/1/position", 0) != blocks[0])
    rejects("counter_wrap", lambda: block(key, d, 1 << 64))
    rejects("empty_domain", lambda: block(key, "", 0))
    rejects("oversized_domain", lambda: block(key, "a" * 65536, 0))
    ok("range_1", range_from_words(1, [(1 << 64) - 1]) == (0, 1))
    ok("range_full_width", range_from_words(1 << 64, [(1 << 64) - 1]) == ((1 << 64) - 1, 1))
    ok("range_rejection_boundary", range_from_words(10, [(1 << 64) - 1, (1 << 64) - 6, 7]) == (7, 3))
    ok("range_last_accepted", range_from_words(10, [(1 << 64) - 7]) == (9, 1))
    rejects("range_zero", lambda: range_from_words(0, [0]))
    rejects("range_too_large", lambda: range_from_words((1 << 64) + 1, [0]))
    rejects("range_exhausted", lambda: range_from_words(10, [(1 << 64) - 1]))
    ok("unit_interval_zero", unit_interval(0) == 0.0)
    ok("unit_interval_upper_endpoint", unit_interval((1 << 64) - 1) == 1.0 - 2.0 ** -53)
    ok("unit_interval_discards_low_11_bits", unit_interval(2047) == 0.0 and unit_interval(2048) == 2.0 ** -53)
    # Exhaustive reduced-width illustration checks equal residue counts for ALL n.
    for n in range(1, 257):
        lim = 256 - 256 % n
        counts = [0] * n
        for x in range(lim):
            counts[x % n] += 1
        if len(set(counts)) != 1:
            raise AssertionError("rejection proof illustration failed")
    ok("exhaustive_8bit_all_256_ranges", True)
    cursor, draws = 0, []
    for _ in range(10):
        value, cursor, used = sample_range(key, d, cursor, 10)
        draws.append({"value": str(value), "next_counter": str(cursor), "consumed": str(used)})
    t0 = transcript_start(md, b"\x00" * 8)
    event = {"counter": "0", "domain": d, "value": draws[0]["value"]}
    t1 = transcript_step(t0, 0, event)
    ok("transcript_replay", transcript_step(t0, 0, event) == t1)
    ok("transcript_event_mutation", transcript_step(t0, 0, {**event, "value":"changed"}) != t1)
    ok("transcript_index_mutation", transcript_step(t0, 1, event) != t1)
    return {
        "status": "passed", "scope": "new PPM-SEED-v1 local reference checks only",
        "python": platform.python_version(), "platform": platform.platform(),
        "checks_passed": len(checks), "checks": checks,
        "fixture": FIXTURE, "canonical_manifest_utf8": raw.decode("utf-8"),
        "manifest_prefix_hex": b"PPM/MANIFEST/v1\0".hex(),
        "seed_prefix_hex": b"PPM/SEED/v1\0".hex(),
        "block_prefix_hex": b"PPM/BLOCK/v1\0".hex(),
        "text_prefix_hex": b"PPM/TEXT/v1\0".hex(),
        "manifest_length": len(raw), "manifest_digest": md.hex(), "key": key.hex(),
        "domain": d, "domain_length": len(d.encode("ascii")),
        "block_0_input_hex": (b"PPM/BLOCK/v1\0" + key + ube(len(d),2) + d.encode("ascii") + ube(0,8)).hex(),
        "blocks_0_1_2": [b.hex() for b in blocks], "range_10_draws": draws,
        "initial_state_hex": (b"\x00" * 8).hex(), "transcript_0": t0.hex(),
        "event_0": event, "transcript_1": t1.hex(),
        "reference_source_sha256": H(Path(__file__).read_bytes()).hex(),
    }

if __name__ == "__main__":
    result = check_suite()
    destination = Path(__file__).with_name("seed_reference_v1_results.json")
    destination.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
