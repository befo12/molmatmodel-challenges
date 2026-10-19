"""Helper for the k-point follow-up of Challenge II.8: course QE settings (PBE + DFT-D3, 80 Ry,
Gaussian smearing 0.01 Ry, conv_thr 1e-10) with a selectable k-grid and optional spin."""
import os, json
import numpy as np
from ase.calculators.espresso import Espresso, EspressoProfile

PW = os.environ.get('PW_COMMAND', 'mpirun -np 4 pw.x')


def calc(directory, symbols, kpts, spin=False, pseudo_dir='.'):
    inp = {'control': {'prefix': 'x', 'outdir': './tmp', 'tstress': True, 'tprnfor': True},
           'system': {'ecutwfc': 80, 'occupations': 'smearing', 'smearing': 'gauss', 'degauss': 0.01,
                      'vdw_corr': 'DFT-D3', 'dftd3_version': 4, 'nspin': 2 if spin else 1},
           'electrons': {'conv_thr': 1.0e-10, 'mixing_beta': 0.3}}
    pp = {s: f'{s}.upf' for s in sorted(set(symbols))}
    return Espresso(directory=directory, profile=EspressoProfile(command=PW, pseudo_dir=os.path.abspath(pseudo_dir)),
                    pseudopotentials=pp, input_data=inp, kpts=kpts)


def single_point(atoms, directory, kpts, spin=False, magmoms=None, pseudo_dir='.'):
    """Run (or re-use) one SCF; returns energy (eV) and total magnetization."""
    res = os.path.join(directory, 'result.json')
    if os.path.exists(res):
        return json.load(open(res))
    a = atoms.copy()
    if spin and magmoms is not None:
        a.set_initial_magnetic_moments(magmoms)
    a.calc = calc(directory, a.get_chemical_symbols(), kpts, spin, pseudo_dir)
    e = a.get_potential_energy()
    m = None
    for line in open(os.path.join(directory, 'espresso.pwo')):
        if 'total magnetization' in line:
            m = float(line.split('=')[1].split()[0])
    out = {'E': e, 'mag': m, 'kpts': list(kpts), 'fmax': float(np.linalg.norm(a.get_forces(), axis=1).max())}
    json.dump(out, open(res, 'w'))
    return out
