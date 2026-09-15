# WANTWOMAN

**Tom Klootwijk's unified approximation of multiscale cyclic dynamics,
recursive geometry, and one-bit physical-field encoding.**

Framework attribution: Tom Klootwijk. Identification supplied in the request:
NL200678942; Gregorian birth date 10-07-1990. Edition 1.0, 15 September 2026.
Formalization, mathematical completions, implementation and testing are
AI-assisted. Established physical equations are attributed to their references.

## Start here

Read `WANTWOMAN.pdf`. Its numbered equations define the implementation and its
source-to-formalization ledger identifies conflicts and completions explicitly.
The unmodified uploaded 21-page document is preserved as `original/source.pdf`.

The PDF distinguishes source conventions (S), explicit definitions/completions
(D), proved propositions (P), imported physical equations (E), and executed
checks (T). No biological period or fitted experimental parameter is inferred
from the supplied personal metadata.

## Reproduce the implementation and benchmark

Python 3.10 or later; no third-party Python packages. Executed here with
Python 3.13.5. From this directory:

```sh
python -m unittest discover -s tests -v
python code/reproduce.py
python code/verify_manifest.py
```

The packaged conformance log contains **28 passing tests**. The reproducibility
script generates a 4096-update Q24 oscillator benchmark, P64 node trace,
explicit LUT, two one-bit streams, and a numerical report. Running it under a
different Python version changes the recorded version; floating comparison
results can differ in their last digits. The integer kernel semantics are
specified independently of floating-point math. A manifest check after editing
or regenerating a file appropriately reports a mismatch with the delivered
archive's original contents.

## Build the PDF from its editable source

With `pdflatex` and the TeX packages named in the source installed:

```sh
cd source
pdflatex -interaction=nonstopmode -halt-on-error WANTWOMAN.tex
pdflatex -interaction=nonstopmode -halt-on-error WANTWOMAN.tex
```

The rebuilt PDF appears in `source/`; the delivered copy is at the archive root.
No standalone font files are included.

## P64 contract

P64 is a **64-bit node record**, with a **separate one-bit output**. It does not
contain every scene node, solver array, LUT, clock accumulator or traversal
address. Those are external context. Profile name: `WANTWOMAN-P64-v1`.

| Bits | Field | Interpretation |
|---|---|---|
| 63 | chi | Symbolic label/parity/phase-control bit |
| 62:52 | rho | Unsigned offset log-radius code, 0..2047 |
| 51:41 | theta | Unsigned angular code, 0..2047 |
| 40:30 | z | Signed auxiliary feature, -1024..1023 |
| 29:20 | phi | Unsigned periodic feature, 0..1023 |
| 19:15 | depth | 0..31 |
| 14:10 | phase | 0..31 |
| 9:3 | lut | 0..127 |
| 2 | kappa | Chart-orientation bit |
| 1:0 | cycle | 0 gestation, 1 crop, 2 menses, 3 composite/user |

The default strict0 OTAN2 is the literal left-fold rule:

```text
((rho XOR old_occupancy) << 10) AND 2047
```

It has exactly two possible phase outputs. The separately named `mix` mode is:

```text
(rho XOR (old_occupancy << 10)) AND 2047
```

It has 2048 possible outputs for fixed occupancy. Neither map reconstructs a
geometric angle from radius alone. The kernel additionally stores an angular
feature and applies its stated updates.

The default terminal rule uses a Klein chart seam:
`theta -> (-theta) mod 2048`, `kappa -> kappa XOR 1`, then resets depth.
The source's radial-reflection/half-turn rule is retained separately as
`source_polar_involution`, not silently used as an equivalent quotient seam.

Round to nearest, ties away from zero. The radial and z outputs saturate;
theta and phi wrap. Metadata changes only through declared field writes.
The multiplier coefficients in the pinion stage use Q16 shift-and-add and the
precisely ordered rounding stages in the PDF.

## Minimal kernel call

```python
import sys
sys.path.insert(0, 'code')
from wantwoman import pack, step, unpack

word = pack(rho=1024, theta=0, z=0, phi=0, depth=0, chi=0, cycle=3)
word, occupancy = step(word, previous_occupancy=0, branch=0,
                       phase=0, forcing=31, mode='strict0')
print(f'{word:016X}', occupancy, unpack(word))
```

The first word in the supplied trace is `2A22D3EF039080B3`.

## Data files and what they mean

`data/trace.csv` records 4096 pre-step physical samples and the corresponding
post-update P64 records. Time runs from 0 through 31.9921875 s in increments of
1/128 s. The physical benchmark report also includes the state at 32 s.
`x_q24` and `p_q24` are normalized signed integers; divide by 16777216 to recover
the benchmark's metre and kg m/s values.

`data/polar_occupancy.bin` is the **polar radial-membership output**, using the
explicit demonstration LUT. `data/oscillator_sigma_delta.bin` is the separate
**pulse-density encoding** of the quantized/clipped normalized oscillator
signal `(x+1)/2`. These are not interchangeable observations.

Each stream contains 4096 valid bits / 512 bytes, most-significant-bit first
within each byte. Right zero-padding is specified for a partial final byte,
although the supplied streams need none. `data/stream_metadata.json` records
that contract. The CSV word hex field is an unsigned 16-character value, not
a native-memory byte dump.

`data/polar_lut.csv` specifies all 128 demonstration thresholds.
`data/word_fields.csv` supplies generated masks, widths and shifts.
`results/numerical_report.json` supplies computed numerical errors, convergence
results, constants and data hashes. All benchmark data are synthetic.

## Implementation coverage

Implemented: checked word packing, integer pinion transform, strict0 and mix
OTAN2, terminal seam variants, rational phase clock, LUT membership, exact
rational interval-enclosure/PSI helpers, bit packing, pulse-density encoding,
and a fixed-point symplectic-Euler oscillator.

The physics supplement also specifies mechanics/action, conservation,
diffusion/heat, wave/Maxwell, Schrödinger, relativistic/gravity, and crop-water
adapters. Those other physical solvers are not implemented in this archive.
The PSI helpers require bounds containing all descendants; the default P64
trace does not invent such scene bounds and therefore performs no culling.

## Source and integrity

`REFERENCES.json` records the primary-source URLs and their uses.
`MANIFEST.sha256` covers every delivered file except itself. The original
uploaded PDF is included without modification. Run the manifest verifier on
a freshly extracted archive before making edits.
