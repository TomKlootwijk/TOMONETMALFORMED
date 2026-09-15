"""Executable conformance and numerical checks for WANTWOMAN v1.0."""
from __future__ import annotations

import math
from pathlib import Path
import random
import sys
import unittest
from fractions import Fraction as F

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
import wantwoman as w


class FieldsTests(unittest.TestCase):
    def test_layout_covers_64_bits_without_overlap(self):
        aggregate = 0
        for f in w.FIELDS.values():
            self.assertEqual(aggregate & f.mask, 0)
            aggregate |= f.mask
        self.assertEqual(aggregate, w.MASK64)
        self.assertEqual(sum(f.width for f in w.FIELDS.values()), 64)

    def test_sign_extension_exhaustive(self):
        for width in (10, 11):
            for raw in range(1 << width):
                value = w.sign_extend(raw, width)
                self.assertTrue(-(1 << (width-1)) <= value < 1 << (width-1))
                self.assertEqual(value & ((1 << width)-1), raw)

    def test_pack_round_trip_random(self):
        rng = random.Random(19900710)
        for _ in range(1500):
            word = rng.getrandbits(64)
            self.assertEqual(w.pack(**w.unpack(word)), word)

    def test_field_isolation(self):
        rng = random.Random(10)
        for name, f in w.FIELDS.items():
            lo = -(1 << (f.width-1)) if f.signed else 0
            hi = (1 << (f.width - int(f.signed))) - 1
            for value in (lo, 0, hi):
                word = rng.getrandbits(64)
                updated = w.set_field(word, name, value)
                self.assertEqual(w.get_field(updated, name), value)
                self.assertEqual((updated ^ word) & (w.MASK64 ^ f.mask), 0)

    def test_range_checks(self):
        with self.assertRaises(ValueError): w.set_field(0, 'rho', 2048)
        with self.assertRaises(ValueError): w.set_field(0, 'z', 1024)
        with self.assertRaises(ValueError): w.get_field(-1, 'rho')
        with self.assertRaises(ValueError): w.step(0, 2, 0, 0)

    def test_modular_negation_exhaustive(self):
        for raw in range(2048):
            self.assertEqual(w.signed_negate_raw(w.signed_negate_raw(raw, 11), 11), raw)
        self.assertEqual(w.signed_negate_raw(1024,11), 1024)
        self.assertNotEqual(w.signed_negate_raw(7,11), 7 ^ 2047)

    def test_source_inversion_expression_is_identity(self):
        for word in (0, w.MASK64, 1 << 63, 0x923456789abcdef0):
            self.assertEqual((word >> 63) & 0x001FFC0000000000, 0)

    def test_toggle_is_not_addition(self):
        word = w.pack(kappa=1, lut=3)
        self.assertEqual(w.get_field(word ^ 4,'lut'),3)
        self.assertNotEqual(w.get_field(word + 4,'lut'),3)


class AlgebraTests(unittest.TestCase):
    def test_walsh_involution(self):
        rng = random.Random(36)
        for _ in range(1000):
            v = tuple(rng.randrange(-1024,1024) for _ in range(4))
            self.assertEqual(w.walsh4(w.walsh4(v)), tuple(4*x for x in v))

    def test_hadamard_norm_preservation_on_exact_rationals(self):
        v = (F(1),F(2),F(-3),F(5))
        h = tuple(F(x,2) for x in w.walsh4(v))
        self.assertEqual(sum(x*x for x in v),sum(x*x for x in h))

    def test_shift_add_product(self):
        for a in range(-23,24):
            for b in (-106039,-40503,-1,0,1,40503,106039):
                self.assertEqual(w.mul_shift_add(a,b),a*b)

    def test_rounding_ties(self):
        for n in range(-30,31):
            exact = F(n,2)
            expected = math.floor(abs(exact) + F(1,2))
            if n < 0: expected = -expected
            self.assertEqual(w.round_div(n,2),expected)

    def test_pinion_fixed_stages_against_fraction_reference(self):
        def rnd(x):
            n = math.floor(abs(x)+F(1,2))
            return -n if x < 0 else n
        rng = random.Random(1618)
        for _ in range(1000):
            v = [rng.randrange(-1024,1024) for _ in range(4)]
            h = [rnd(F(x,2)) for x in w.walsh4(v)]
            a = [rnd(F(h[0]*106039,65536)),rnd(F(h[1]*40503,65536)),h[2],-h[3]]
            expected = tuple(rnd(F(x,4)) for x in a)
            self.assertEqual(w.pinion_fixed(v),expected)

    def test_otan2_strict_has_two_values_exhaustively(self):
        values = set()
        for rho in range(2048):
            for o in (0,1):
                got = w.otan2(rho,o)
                self.assertEqual(got,1024*((rho^o)&1))
                values.add(got)
        self.assertEqual(values,{0,1024})

    def test_otan2_mix_bijection_at_fixed_occupancy(self):
        for o in (0,1):
            self.assertEqual({w.otan2(r,o,'mix') for r in range(2048)},set(range(2048)))

    def test_parity_is_only_three_low_bits(self):
        for bits in range(8):
            self.assertEqual(w.low_parity(bits),bits.bit_count() & 1)
            self.assertEqual(w.low_parity(bits | 0xABCDEFF000000000),w.low_parity(bits))


class TopologyAndKernelTests(unittest.TestCase):
    def test_klein_chart_seam_involution_exhaustive(self):
        for theta in range(2048):
            for kappa in (0,1):
                word = w.pack(rho=1000,theta=theta,kappa=kappa,depth=31,chi=1,cycle=2)
                seam = w.klein_seam(word)
                self.assertEqual(w.klein_seam(seam),word)
                self.assertEqual(w.effective_theta(seam),w.effective_theta(word))
                self.assertEqual(w.lookup(word,w.default_lut())[1],w.lookup(seam,w.default_lut())[1])

    def test_source_polar_involution(self):
        rng = random.Random(7)
        for _ in range(1000):
            word = rng.getrandbits(64)
            self.assertEqual(w.source_polar_involution(w.source_polar_involution(word)),word)

    def test_terminal_root_reset(self):
        word = w.pack(rho=1000,theta=100,z=-4,phi=99,depth=31,chi=1,cycle=2)
        new, bit = w.step(word,0,1,9)
        self.assertEqual(w.get_field(new,'depth'),0)
        self.assertEqual(w.get_field(new,'theta'),1948)
        self.assertEqual(w.get_field(new,'rho'),1000)
        self.assertEqual(w.get_field(new,'kappa'),1)
        self.assertEqual(w.get_field(new,'phase'),9)
        self.assertIn(bit,(0,1))

    def test_kernel_determinism_and_metadata(self):
        start = w.pack(rho=1024,theta=0,z=0,phi=0,chi=1,cycle=2)
        word, bit = start, 0
        for n in range(4096):
            args = (word,bit,n&1,n&31,(n%63)-31)
            a = w.step(*args)
            self.assertEqual(a,w.step(*args))
            word,bit=a
            self.assertEqual(w.get_field(word,'chi'),1)
            self.assertEqual(w.get_field(word,'cycle'),2)
            self.assertEqual(w.get_field(word,'depth'),(n+1)&31)
            self.assertEqual(w.pack(**w.unpack(word)),word)

    def test_phase_clock_period(self):
        clock = w.PhaseClock(804)
        phases = [clock.tick() for _ in range(804)]
        self.assertEqual(clock.counter,0)
        self.assertEqual(set(phases),set(range(32)))
        self.assertEqual(phases,[clock.tick() for _ in range(804)])

    def test_phase_lut_bit_semantics(self):
        word = w.pack(rho=1000,theta=100,phase=3,cycle=2)
        updated, bit = w.lookup(word,w.default_lut())
        self.assertEqual(w.get_field(updated,'lut'),((100>>4)+3)&127)
        self.assertEqual(w.get_field(updated,'cycle'),2)
        self.assertEqual(bit,int(1000<=w.default_lut()[9]))


class GeometryAndEncodingTests(unittest.TestCase):
    def test_affine_box_exact_corner_enclosure(self):
        A=((F(1,2),F(-1,4)),(F(1,3),F(1,2)))
        b=(F(2),F(-1))
        box=((F(-2),F(3)),(F(-4),F(1)))
        bound=w.affine_box(A,b,box)
        for x in box[0]:
            for y in box[1]:
                point=[A[i][0]*x+A[i][1]*y+b[i] for i in range(2)]
                for i in range(2): self.assertTrue(bound[i][0]<=point[i]<=bound[i][1])

    def test_subtree_hull_pruning_sound(self):
        A=((F(1,2),F(1,4)),(F(-1,4),F(1,2)))
        shifts=((F(-1),F(1,2)),(F(1),F(1,2)))
        primitive=((F(0),F(0)),(F(0),F(0)))
        bound=primitive
        points=[(F(0),F(0))]
        frontier=points[:]
        for _ in range(6):
            bound=w.hull(primitive,*(w.affine_box(A,b,bound) for b in shifts))
            frontier=[tuple(sum(A[i][j]*p[j] for j in range(2))+b[i] for i in range(2))
                      for p in frontier for b in shifts]
            points+=frontier
        for offset in range(-8,9):
            cull=w.slit_cull(bound,(F(1),F(0)),F(offset),F(1,5))
            if cull:
                self.assertTrue(all(abs(p[0]-offset)>F(1,5) for p in points))

    def test_parent_point_is_not_descendant_bound(self):
        parent=(F(2),F(2))
        self.assertTrue(w.slit_cull((parent,),(F(1),)))
        child=(F(0),F(0))
        self.assertFalse(w.slit_cull(w.hull((parent,),(child,)),(F(1),)))

    def test_bitstream_roundtrip_and_padding(self):
        bits=[1,0,1,1,0,0,0,1,1]
        data,n=w.pack_bits(bits)
        self.assertEqual(data,bytes([0b10110001,0b10000000]))
        self.assertEqual(w.unpack_bits(data,n),bits)
        self.assertEqual(w.pack_bits([]),(b'',0))

    def test_sigma_delta_exact_conservation(self):
        rng=random.Random(1990)
        scale=1024
        for length in (1,2,7,128,4096):
            values=[rng.randrange(scale+1) for _ in range(length)]
            bits,residual=w.sigma_delta(values,scale)
            self.assertEqual(sum(values)-scale*sum(bits),residual)
            self.assertTrue(0<=residual<scale)
            self.assertLess(abs(F(sum(bits),length)-F(sum(values),scale*length)),F(1,length))

    def test_oscillator_first_order_convergence(self):
        errors=[]
        for shift in (6,7,8):
            states=w.oscillator(8*(1<<shift),shift,24)
            err=max(abs(x/(1<<24)-math.cos(n/(1<<shift))) for n,(x,p) in enumerate(states))
            errors.append(err)
        self.assertTrue(errors[0]>1.8*errors[1]>0)
        self.assertTrue(errors[1]>1.8*errors[2]>0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
