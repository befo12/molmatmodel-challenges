"""Challenge II.8, H on graphene - follow-up with k-point sampling.
The course protocol uses the Gamma point only. Here the spin-polarized binding energy is recomputed
with a k-grid (course settings otherwise: PBE + DFT-D3, 80 Ry, Gaussian 0.01 Ry), relaxing H and all
C atoms with pw.x (calculation = 'relax', forc_conv_thr = 3.9e-4 Ry/bohr = 0.01 eV/A):
  * C8  (2x2 cell): k = 6x6x1  (as in Casolo et al., J. Chem. Phys. 130, 054704 (2009))
  * C18 (3x3 cell): k = 4x4x1  (same k-point density as 6x6x1 for the 2x2 cell)
  * both cells again at the Gamma point with the same relaxation protocol, for comparison
E_b = E(slab) + E(H atom, spin-polarized) - E(H@slab). Relaxations start from the Gamma geometries
in runs/. Run:  python -u h_kpoint_followup.py > h_kpoint_followup.py.log 2>&1  (results in kfollow/)
"""
import os, json, subprocess
import numpy as np
from ase.io import read, write

PW = os.environ.get('PW_COMMAND', 'mpirun -np 4 pw.x')
PSEUDO = os.path.abspath('.')


def pw(atoms, tag, kpts, spin=False, relax=False, magmom_H=1.0):
    d = f'kfollow/{tag}'
    res = f'{d}/result.json'
    if os.path.exists(res):
        return json.load(open(res)), read(f'{d}/final.vasp')
    os.makedirs(d, exist_ok=True)
    a = atoms.copy()
    if spin:
        a.set_initial_magnetic_moments([magmom_H if s == 'H' else 0.0 for s in a.get_chemical_symbols()])
    inp = {'control': {'calculation': 'relax' if relax else 'scf', 'prefix': 'x', 'outdir': './tmp',
                       'pseudo_dir': PSEUDO, 'tprnfor': True, 'etot_conv_thr': 1e-5, 'forc_conv_thr': 3.9e-4},
           'system': {'ecutwfc': 80, 'occupations': 'smearing', 'smearing': 'gauss', 'degauss': 0.01,
                      'vdw_corr': 'DFT-D3', 'dftd3_version': 4, 'nspin': 2 if spin else 1},
           'electrons': {'conv_thr': 1.0e-10, 'mixing_beta': 0.3}}
    if relax:
        inp['ions'] = {'ion_dynamics': 'bfgs'}
    pp = {s: f'{s}.upf' for s in sorted(set(a.get_chemical_symbols()))}
    write(f'{d}/pw.in', a, format='espresso-in', input_data=inp, pseudopotentials=pp, kpts=kpts)
    with open(f'{d}/pw.out', 'w') as f:
        subprocess.run(f'{PW} -in pw.in', shell=True, cwd=d, stdout=f, stderr=subprocess.STDOUT, check=True)
    out = open(f'{d}/pw.out').read()
    assert 'JOB DONE' in out, f'{tag}: pw.x did not finish'
    if relax:
        assert 'bfgs converged' in out, f'{tag}: relaxation not converged'
    fin = read(f'{d}/pw.out', format='espresso-out', index=-1)
    mags = [float(l.split('=')[1].split()[0]) for l in out.splitlines() if 'total magnetization' in l]
    r = {'E': fin.get_potential_energy(), 'mag': mags[-1] if mags else None, 'kpts': list(kpts),
         'nsteps': out.count('!    total energy')}
    write(f'{d}/final.vasp', fin, format='vasp', direct=True)
    json.dump(r, open(res, 'w'))
    return r, fin


def geometry(a):
    """C-H bond length and height of the H-bonded C atom above the mean plane of the other C atoms."""
    h = [i for i, s in enumerate(a.get_chemical_symbols()) if s == 'H'][0]
    c = [i for i, s in enumerate(a.get_chemical_symbols()) if s == 'C']
    d = a.get_distances(h, c, mic=True)
    cb = c[int(np.argmin(d))]
    others = [i for i in c if i != cb]
    return d.min(), a.positions[cb, 2] - a.positions[others, 2].mean()


def last_geometry(run):
    f = f'runs/{run}/final.vasp'
    return read(f) if os.path.exists(f) else read(f'runs/{run}/relax.traj', -1)


h_atom = read('h.vasp')
c8 = read('c.vasp')
c18 = read('c18.vasp' if os.path.exists('c18.vasp') else '../Hg_on_C18/c18.vasp')
start8 = last_geometry('HC8_spin_relax')
start18 = last_geometry('HC18_spin_relax')

rH, _ = pw(h_atom, 'H_atom_spin_G', (1, 1, 1), spin=True)
print(f"H atom (spin, Gamma, 10 A box)   E = {rH['E']:.6f} eV  m = {rH['mag']}", flush=True)
rows = []
for name, slab, start, k in [('C8 (2x2)', c8, start8, (6, 6, 1)), ('C18 (3x3)', c18, start18, (4, 4, 1)),
                             ('C8 (2x2)', c8, start8, (1, 1, 1)), ('C18 (3x3)', c18, start18, (1, 1, 1))]:
    tag = name.split()[0]
    rs, _ = pw(slab, f'{tag}_k{k[0]}', k)
    rc, fin = pw(start, f'H{tag}_spin_relax_k{k[0]}', k, spin=True, relax=True)
    eb = rs['E'] + rH['E'] - rc['E']
    dch, puck = geometry(fin)
    rows.append((name, k, eb, dch, puck, rc['mag'], rc['nsteps']))
    print(f"{name:<10} k={k[0]}x{k[1]}x{k[2]}  E(slab) = {rs['E']:.6f}  E(H@slab) = {rc['E']:.6f}  "
          f"E_b = {eb:.3f} eV  ({rc['nsteps']} SCF steps)", flush=True)

print("\nSpin-polarized binding energy of H on graphene")
print(f"{'cell':<11}{'k-grid':>8}{'E_b/eV':>9}{'C-H/A':>8}{'pucker/A':>10}{'m/muB':>8}   Casolo 2009 (PBE, 6x6x1)")
lit = {'C8 (2x2)': '0.75 eV, 0.36 A', 'C18 (3x3)': '0.77 eV, 0.42 A'}
for name, k, eb, dch, puck, m, n in rows:
    print(f"{name:<11}{k[0]}x{k[1]}x{k[2]:>4}{eb:9.3f}{dch:8.3f}{puck:10.3f}{m:8.2f}   {lit[name]}")
print("\npucker = height of the H-bonded C atom above the mean plane of the other C atoms")
