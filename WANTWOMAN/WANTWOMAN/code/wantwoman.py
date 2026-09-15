"""WANTWOMAN v1.0: P64 integer state kernel and exact reference utilities.

The source PDF's names are retained. New closures and source corrections are
specified in WANTWOMAN.pdf. No third-party runtime dependencies are required.
P64 is a 64-bit node record, not the whole scene or a physical solver state.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Sequence

MASK64 = (1 << 64) - 1
PHI_Q16 = 106039
INV_PHI_Q16 = 40503
GOLDEN11 = 782
GOLDEN10 = 391


@dataclass(frozen=True)
class Field:
    shift: int
    width: int
    signed: bool = False

    @property
    def mask(self) -> int:
        return ((1 << self.width) - 1) << self.shift


FIELDS = {
    "chi": Field(63, 1),
    "rho": Field(52, 11),
    "theta": Field(41, 11),
    "z": Field(30, 11, True),
    "phi": Field(20, 10),
    "depth": Field(15, 5),
    "phase": Field(10, 5),
    "lut": Field(3, 7),
    "kappa": Field(2, 1),
    "cycle": Field(0, 2),
}


def _integer(x: int, name: str = "value") -> int:
    if not isinstance(x, int):
        raise TypeError(f"{name} must be an integer")
    return x


def validate_word(word: int) -> int:
    _integer(word, "word")
    if not 0 <= word <= MASK64:
        raise ValueError("word must be an unsigned 64-bit integer")
    return word


def sign_extend(raw: int, width: int) -> int:
    if width < 1 or not 0 <= raw < (1 << width):
        raise ValueError("invalid raw value or width")
    return raw - (1 << width) if raw & (1 << (width - 1)) else raw


def get_field(word: int, name: str) -> int:
    validate_word(word)
    f = FIELDS[name]
    raw = (word >> f.shift) & ((1 << f.width) - 1)
    return sign_extend(raw, f.width) if f.signed else raw


def set_field(word: int, name: str, value: int) -> int:
    validate_word(word)
    _integer(value)
    f = FIELDS[name]
    lo = -(1 << (f.width - 1)) if f.signed else 0
    hi = (1 << (f.width - (1 if f.signed else 0))) - 1
    if not lo <= value <= hi:
        raise ValueError(f"{name} must be in [{lo}, {hi}]")
    raw = value & ((1 << f.width) - 1)
    return (word & (MASK64 ^ f.mask)) | (raw << f.shift)


def pack(**values: int) -> int:
    word = 0
    for name, value in values.items():
        word = set_field(word, name, value)
    return word


def unpack(word: int) -> dict[str, int]:
    return {name: get_field(word, name) for name in FIELDS}


def clamp(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))


def round_div(numerator: int, denominator: int) -> int:
    """Nearest integer, with exact halfway cases away from zero."""
    if denominator <= 0:
        raise ValueError("denominator must be positive")
    q, r = divmod(abs(numerator), denominator)
    q += int((r << 1) >= denominator)
    return -q if numerator < 0 else q


def mul_shift_add(value: int, constant: int) -> int:
    """Exact signed integer multiplication implemented by additions and shifts."""
    a, b = abs(value), abs(constant)
    result = 0
    while b:
        if b & 1:
            result += a
        a <<= 1
        b >>= 1
    return -result if (value < 0) ^ (constant < 0) else result


def walsh4(v: Sequence[int]) -> tuple[int, int, int, int]:
    """Unnormalized 4 x 4 Sylvester matrix M, so M(M(v)) == 4v."""
    if len(v) != 4:
        raise ValueError("four coordinates required")
    x, y, z, f = v
    return x + y + z + f, x - y + z - f, x + y - z - f, x - y - z + f


def pinion_fixed(v: Sequence[int], contraction_shift: int = 2) -> tuple[int, ...]:
    """Q16 approximation of 2**(-s) diag(phi,1/phi,1,-1) H4 v.

    Rounding stages are part of the definition, not reordered by an optimizer.
    All values are widened Python integers until the caller applies field limits.
    """
    if contraction_shift < 0:
        raise ValueError("contraction_shift cannot be negative")
    h = tuple(round_div(x, 2) for x in walsh4(v))
    a = (round_div(mul_shift_add(h[0], PHI_Q16), 1 << 16),
         round_div(mul_shift_add(h[1], INV_PHI_Q16), 1 << 16), h[2], -h[3])
    return tuple(round_div(x, 1 << contraction_shift) for x in a)


def low_parity(word: int) -> int:
    validate_word(word)
    return (word & 1) ^ ((word >> 1) & 1) ^ ((word >> 2) & 1)


def otan2(rho: int, occupancy: int, mode: str = "strict0") -> int:
    """Source-literal left fold or the separately named full-resolution mixer.

    strict0: ((rho XOR occupancy) << 10) AND 2047 (two possible phases).
    mix:     rho XOR (occupancy << 10) (2048 possible phases for fixed O).
    Neither function recovers a geometric angle from a radius alone.
    """
    if not 0 <= rho < 2048 or occupancy not in (0, 1):
        raise ValueError("rho must be 11-bit unsigned and occupancy one bit")
    if mode == "strict0":
        return ((rho ^ occupancy) << 10) & 2047
    if mode == "mix":
        return (rho ^ (occupancy << 10)) & 2047
    raise ValueError("mode must be 'strict0' or 'mix'")


def effective_theta(word: int) -> int:
    theta = get_field(word, "theta")
    return (-theta) & 2047 if get_field(word, "kappa") else theta


def klein_seam(word: int) -> int:
    """Chart seam (theta,kappa) -> (-theta mod 2048, kappa XOR 1).

    Depth is intentionally untouched: this map is an involution. The separate
    traversal rule resets depth when entering the root again.
    """
    word = set_field(word, "theta", (-get_field(word, "theta")) & 2047)
    return word ^ FIELDS["kappa"].mask


def source_polar_involution(word: int) -> int:
    """Source p.14 radial reflection/half-turn, distinct from a Klein quotient."""
    word = set_field(word, "rho", 2047 - get_field(word, "rho"))
    word = set_field(word, "theta", (get_field(word, "theta") + 1024) & 2047)
    return word ^ FIELDS["kappa"].mask


def default_lut() -> tuple[int, ...]:
    """A fully specified integer-only demonstration boundary, not measured data.

    L[j] = 960 + 3 min(j,128-j); L ranges from 960 through 1152.
    """
    return tuple(960 + mul_shift_add(min(j, 128-j), 3) for j in range(128))


def lookup(word: int, lut: Sequence[int]) -> tuple[int, int]:
    if len(lut) != 128 or any(not isinstance(x, int) or not 0 <= x <= 2047 for x in lut):
        raise ValueError("LUT must contain 128 unsigned 11-bit integer thresholds")
    idx = ((effective_theta(word) >> 4) + get_field(word, "phase")) & 127
    word = set_field(word, "lut", idx)
    return word, int(get_field(word, "rho") <= lut[idx])


def step(word: int, previous_occupancy: int, branch: int, phase: int,
         forcing: int = 0, *, mode: str = "strict0",
         lut: Sequence[int] | None = None) -> tuple[int, int]:
    """Complete P64 node transition, with the order specified in the PDF.

    chi and cycle are preserved. The branch is external traversal input.
    At depth 31 only the seam/root reset happens before phase and LUT updates.
    """
    validate_word(word)
    if previous_occupancy not in (0, 1) or branch not in (0, 1):
        raise ValueError("occupancy and branch must be bits")
    if not 0 <= phase <= 31 or not -31 <= forcing <= 31:
        raise ValueError("phase or forcing out of range")
    if mode not in ("strict0", "mix"):
        raise ValueError("invalid OTAN2 mode")
    f = unpack(word)
    if f["depth"] == 31:
        word = set_field(klein_seam(word), "depth", 0)
    else:
        direction = 1 if (branch ^ low_parity(word) ^ f["chi"]) else -1
        v = (f["rho"] - 1024, f["theta"] - 1024, f["z"], f["phi"] - 512)
        a, b, c, e = pinion_fixed(v)
        signed = lambda value: value if direction > 0 else -value
        r = clamp(1024 + a + signed(8 + abs(forcing)), 0, 2047)
        theta = (1024 + b + signed(GOLDEN11)
                 + otan2(r, previous_occupancy, mode) + (f["chi"] << 10)) & 2047
        z = clamp(c + signed(4), -1024, 1023)
        phi = (512 + e + signed(GOLDEN10)) & 1023
        for name, value in (("rho", r), ("theta", theta), ("z", z),
                            ("phi", phi), ("depth", f["depth"] + 1)):
            word = set_field(word, name, value)
    word = set_field(word, "phase", phase)
    return lookup(word, default_lut() if lut is None else lut)


@dataclass
class PhaseClock:
    """Exact rational clock; stores its accumulator outside the P64 word."""
    period_ticks: int
    counter: int = 0

    def __post_init__(self) -> None:
        if self.period_ticks <= 0 or not 0 <= self.counter < self.period_ticks:
            raise ValueError("invalid phase clock")

    @property
    def phase(self) -> int:
        return (self.counter << 5) // self.period_ticks

    def tick(self) -> int:
        self.counter = (self.counter + 1) % self.period_ticks
        return self.phase


def signed_negate_raw(raw: int, width: int) -> int:
    """Field-local modular two's-complement negation, including minimum code."""
    if width < 1 or not 0 <= raw < (1 << width):
        raise ValueError("invalid raw field")
    return (-raw) & ((1 << width) - 1)


def affine_box(matrix: Sequence[Sequence[Fraction]], shift: Sequence[Fraction],
               box: Sequence[tuple[Fraction, Fraction]]) -> tuple[tuple[Fraction, Fraction], ...]:
    """Exact rational axis-aligned enclosure of A(box)+b; no float rounding."""
    if len(matrix) != len(shift) or any(len(row) != len(box) for row in matrix):
        raise ValueError("incompatible affine dimensions")
    if any(lo > hi for lo, hi in box):
        raise ValueError("invalid interval")
    out = []
    for row, off in zip(matrix, shift):
        lo = hi = Fraction(off)
        for coef, (a, b) in zip(row, box):
            coef, a, b = Fraction(coef), Fraction(a), Fraction(b)
            lo += min(coef*a, coef*b)
            hi += max(coef*a, coef*b)
        out.append((lo, hi))
    return tuple(out)


def hull(*boxes: Sequence[tuple[Fraction, Fraction]]) -> tuple[tuple[Fraction, Fraction], ...]:
    if not boxes or any(len(b) != len(boxes[0]) for b in boxes):
        raise ValueError("nonempty equal-dimensional boxes required")
    return tuple((min(b[i][0] for b in boxes), max(b[i][1] for b in boxes))
                 for i in range(len(boxes[0])))


def slit_cull(box: Sequence[tuple[Fraction, Fraction]], normal: Sequence[Fraction],
              offset: Fraction = Fraction(0), half_width: Fraction = Fraction(0)) -> bool:
    """Sound PSI test when box encloses every descendant's geometry."""
    if half_width < 0 or len(normal) != len(box):
        raise ValueError("invalid slit")
    ((lo, hi),) = affine_box((normal,), (-offset,), box)
    return lo > half_width or hi < -half_width


def pack_bits(bits: Iterable[int]) -> tuple[bytes, int]:
    """Most-significant-bit first; final byte padded on the right with zeroes."""
    result = bytearray()
    accumulator = count = n = 0
    for bit in bits:
        if bit not in (0, 1):
            raise ValueError("bitstream values must be 0 or 1")
        accumulator = (accumulator << 1) | bit
        count += 1
        n += 1
        if count == 8:
            result.append(accumulator)
            accumulator = count = 0
    if count:
        result.append(accumulator << (8 - count))
    return bytes(result), n


def unpack_bits(data: bytes, valid_bits: int) -> list[int]:
    if not 0 <= valid_bits <= len(data)*8:
        raise ValueError("invalid bit count")
    return [(data[i >> 3] >> (7 - (i & 7))) & 1 for i in range(valid_bits)]


def sigma_delta(values: Iterable[int], scale: int) -> tuple[list[int], int]:
    """First-order one-bit pulse-density encoder of integers in [0,scale]."""
    if scale <= 0:
        raise ValueError("scale must be positive")
    residual = 0
    bits = []
    for value in values:
        if not 0 <= value <= scale:
            raise ValueError("input must be in [0,scale]")
        residual += value
        bit = int(residual >= scale)
        if bit:
            residual -= scale
        bits.append(bit)
    return bits, residual


def oscillator(steps: int, dt_shift: int = 7, qbits: int = 24) -> list[tuple[int, int]]:
    """Integer symplectic Euler: p' = p-h*x; x' = x+h*p'.

    Dimensionless oscillator, x(0)=1, p(0)=0, h=2**(-dt_shift).
    Returned states include the initial state. Solver arrays are external to P64.
    """
    if steps < 0 or dt_shift < 1 or qbits < 1:
        raise ValueError("invalid oscillator configuration")
    scale = 1 << qbits
    denominator = 1 << dt_shift
    x, p = scale, 0
    history = [(x, p)]
    for _ in range(steps):
        p -= round_div(x, denominator)
        x += round_div(p, denominator)
        history.append((x, p))
    return history
