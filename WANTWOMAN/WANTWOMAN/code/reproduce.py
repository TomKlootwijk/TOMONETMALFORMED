"""Regenerate WANTWOMAN's synthetic data, bitstreams and numerical report."""
from __future__ import annotations

import csv
from datetime import date
from decimal import Decimal, localcontext
import hashlib
import json
import math
from pathlib import Path
import platform
import sys

from wantwoman import (FIELDS, GOLDEN10, GOLDEN11, PHI_Q16, INV_PHI_Q16,
    PhaseClock, clamp, default_lut, oscillator, pack, pack_bits,
    round_div, sigma_delta, step, unpack)

ROOT=Path(__file__).resolve().parents[1]


def main() -> None:
    for folder in ('data','results'):
        (ROOT/folder).mkdir(exist_ok=True)
    qbits=24
    scale=1<<qbits
    steps=4096
    shift=7
    h=1/(1<<shift)
    states=oscillator(steps,shift,qbits)
    maximum_x_error=max(abs(x/scale-math.cos(n*h)) for n,(x,p) in enumerate(states))
    maximum_p_error=max(abs(p/scale+math.sin(n*h)) for n,(x,p) in enumerate(states))
    maximum_energy_error=max(abs((x*x+p*p)/(2*scale*scale)-0.5) for x,p in states)
    energy_invariant_error=max(abs((x*x+p*p)/(2*scale*scale)-h*x*p/(2*scale*scale)-0.5)
                               for x,p in states)
    values=[clamp(round_div(x+scale,2),0,scale) for x,p in states[:-1]]
    sigma_bits,residual=sigma_delta(values,scale)
    sigma_data,count=pack_bits(sigma_bits)
    (ROOT/'data'/'oscillator_sigma_delta.bin').write_bytes(sigma_data)
    clock=PhaseClock(804)
    word=pack(rho=1024,theta=0,z=0,phi=0,depth=0,chi=0,cycle=3)
    occupancy=0
    rows=[]
    occupancy_bits=[]
    for n,(x,p) in enumerate(states[:-1]):
        phase=clock.phase
        forcing=clamp(round_div(31*x,scale),-31,31)
        word,occupancy=step(word,occupancy,n&1,phase,forcing)
        fields=unpack(word)
        rows.append({'n':n,'time_s':f'{n*h:.8f}','x_q24':x,'p_q24':p,
                     'reference_x_m':f'{math.cos(n*h):.12f}',
                     'word_hex':f'{word:016X}','occupancy':occupancy,
                     'sigma_delta_bit':sigma_bits[n],**fields})
        occupancy_bits.append(occupancy)
        clock.tick()
    with (ROOT/'data'/'trace.csv').open('w',newline='',encoding='utf-8') as out:
        writer=csv.DictWriter(out,fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    data,_=pack_bits(occupancy_bits)
    (ROOT/'data'/'polar_occupancy.bin').write_bytes(data)
    with (ROOT/'data'/'polar_lut.csv').open('w',newline='',encoding='utf-8') as out:
        writer=csv.writer(out); writer.writerow(['index','log_radius_threshold_code'])
        writer.writerows(enumerate(default_lut()))
    with (ROOT/'data'/'word_fields.csv').open('w',newline='',encoding='utf-8') as out:
        writer=csv.writer(out); writer.writerow(['field','msb','lsb','width','signed','hex_mask'])
        for name,f in FIELDS.items():
            writer.writerow([name,f.shift+f.width-1,f.shift,f.width,f.signed,f'{f.mask:016X}'])
    with localcontext() as ctx:
        ctx.prec=60
        phi=(Decimal(1)+Decimal(5).sqrt())/2
        qphi=Decimal(PHI_Q16)/65536
        qinv=Decimal(INV_PHI_Q16)/65536
        constants={
            'phi':str(phi),
            'phi_q16':str(qphi),
            'inverse_phi_q16':str(qinv),
            'phi_q16_absolute_error':str(abs(qphi-phi)),
            'inverse_phi_q16_absolute_error':str(abs(qinv-1/phi)),
            'pinion_fixed_diagonal_product':str(qphi*qinv),
            'golden_step_11_bits':GOLDEN11,
            'golden_step_10_bits':GOLDEN10,
            'golden_angle_radians':2*math.pi/(float(phi)**2),
            'golden_angle_11bit_radians':GOLDEN11*2*math.pi/2048,
            'golden_angle_11bit_error_radians':abs(GOLDEN11*2*math.pi/2048-2*math.pi/(float(phi)**2)),
        }
    convergence=[]
    for dt_shift in (6,7,8):
        history=oscillator(8*(1<<dt_shift),dt_shift,24)
        error=max(abs(x/scale-math.cos(n/(1<<dt_shift))) for n,(x,p) in enumerate(history))
        convergence.append({'h':1/(1<<dt_shift),'max_abs_x_error_over_8_s':error})
    result={
        'edition':'WANTWOMAN 1.0',
        'data_kind':'synthetic benchmark, not experimental observations',
        'python_version':platform.python_version(),
        'steps':steps,'time_step_s':h,'duration_s':steps*h,'fixed_point_fraction_bits':qbits,
        'oscillator_mass_kg':1,'spring_constant_N_per_m':1,
        'initial_position_m':1,'initial_momentum_kg_m_per_s':0,
        'max_abs_position_error_m':maximum_x_error,
        'max_abs_momentum_error_kg_m_per_s':maximum_p_error,
        'max_abs_energy_error_J':maximum_energy_error,
        'max_modified_energy_error_J':energy_invariant_error,
        'sigma_delta_residual_integer':residual,
        'sigma_delta_mean_error':abs(sum(sigma_bits)/steps-sum(values)/(scale*steps)),
        'sigma_delta_mean_error_bound':1/steps,
        'occupancy_ones':sum(occupancy_bits),'stream_valid_bits':count,
        'bytes_per_stream':len(data),
        'rational_clock_period_s':804*h,
        'physical_oscillator_period_s':2*math.pi,
        'clock_period_relative_error':abs(804*h-2*math.pi)/(2*math.pi),
        'age_on_edition_date':36,
        'civil_days_from_1990_07_10_to_2026_07_10':(date(2026,7,10)-date(1990,7,10)).days,
        'constants':constants,'convergence':convergence,
        'first_word_hex':rows[0]['word_hex'],'last_word_hex':rows[-1]['word_hex'],
        'files_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted((ROOT/'data').iterdir()) if p.is_file()},
    }
    (ROOT/'results'/'numerical_report.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    meta={'format':'raw bits, most-significant bit first, right zero padding',
          'valid_bits':count,'time_step_s':h,'samples_per_second':1/h,
          'polar_occupancy.bin':'P64 log-polar membership stream, strict0 OTAN2',
          'oscillator_sigma_delta.bin':'pulse-density encoding of clipped (x+1)/2',
          'P64_profile':'WANTWOMAN-P64-v1; Klein chart seam; 128-entry triangle LUT',
          'source_of_numbers':'synthetic oscillator and explicit demonstration design constants'}
    (ROOT/'data'/'stream_metadata.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
    result['files_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in sorted((ROOT/'data').iterdir()) if p.is_file()}
    (ROOT/'results'/'numerical_report.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
