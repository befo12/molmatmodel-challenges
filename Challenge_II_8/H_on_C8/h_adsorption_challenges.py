"""Challenge II.8 (H on graphene): all challenges with the course settings
(PBE, ecutwfc 80 Ry, Gaussian smearing 0.01 Ry, DFT-D3 (version 4), nspin = 2, Gamma point,
BFGS fmax = 0.01 eV/A; structures c.vasp, h.vasp, ch.vasp and C18 from Hg_on_C18/c18.vasp).

E_b = E(slab) + E(H) - E(H@slab)   (positive = bound)

 1. course protocol (no initial magnetic moment, unrelaxed C8)        -> reproduces the course
 2. challenge: relaxed C8 slab
 3. extra: spin-polarized H atom and H@C8 (starting magnetic moment 1 muB on H). In the course
    runs nspin = 2 but no starting magnetization is given, so QE converges to a NON-magnetic
    H atom (magnetization 0) although an isolated H atom has 1 unpaired electron.
 4. challenge: ecutwfc = 100 and 120 Ry (single points at the 80 Ry geometries, spin-polarized)
 5. challenge: H on a larger C18 slab (3x3), spin-polarized, relaxed
"""
import copy
import json
import os
import sys
from ase import Atom
from ase.io import read, write
from ase.optimize import BFGS
from ase.calculators.espresso import Espresso, EspressoProfile

DRY = '--dry' in sys.argv          # test the workflow with EMT instead of QE
os.environ['OMP_NUM_THREADS'] = '1'
BASE = {
    'control': {'prefix': 'calc', 'outdir': './tmp', 'verbosity': 'low', 'tprnfor': True},
    'system': {'ecutwfc': 80, 'occupations': 'smearing', 'smearing': 'gauss', 'degauss': 0.01,
               'vdw_corr': 'DFT-D3', 'dftd3_version': 4, 'nspin': 2},
    'electrons': {'conv_thr': 1.0e-10},
}
profile = EspressoProfile(command='mpirun -np 4 pw.x', pseudo_dir=os.path.abspath('.'))


def run(atoms, tag, ecut=80, spin=False, relax=False):
    """Run (or resume) one calculation in runs/<tag>; finished results are re-used."""
    d = f'runs/{tag}'
    os.makedirs(d, exist_ok=True)
    if os.path.exists(f'{d}/result.json'):                 # finished in an earlier run
        r = json.load(open(f'{d}/result.json'))
        print(f"   {tag:<24} E = {r['e']:14.6f} eV   magnetization = {r['mag']:6.3f} muB   (re-used)", flush=True)
        return r['e'], read(f'{d}/final.vasp')
    if os.path.exists(f'{d}/final.vasp') and os.path.exists(f'{d}/espresso.pwo'):   # finished before resume support
        a = read(f'{d}/espresso.pwo', format='espresso-out')
        e = a.get_potential_energy()
        try:
            mag = float(a.get_magnetic_moment())
        except Exception:
            mag = float('nan')
        json.dump({'e': e, 'mag': mag}, open(f'{d}/result.json', 'w'))
        print(f"   {tag:<24} E = {e:14.6f} eV   magnetization = {mag:6.3f} muB   (re-used)", flush=True)
        return e, read(f'{d}/final.vasp')
    atoms = atoms.copy()
    if relax and os.path.exists(f'{d}/relax.traj'):        # interrupted relaxation: continue from last geometry
        try:
            atoms.positions = read(f'{d}/relax.traj', index=-1).positions
            print(f"   {tag:<24} continuing interrupted relaxation", flush=True)
        except Exception:                                  # trajectory damaged (e.g. power loss): start again
            os.rename(f'{d}/relax.traj', f'{d}/relax.traj.broken')
    if spin:
        atoms.set_initial_magnetic_moments([1.0 if s == 'H' else 0.0 for s in atoms.get_chemical_symbols()])
    if DRY:
        from ase.calculators.emt import EMT
        atoms.calc = EMT()
    else:
        inp = copy.deepcopy(BASE)
        inp['system']['ecutwfc'] = ecut
        atoms.calc = Espresso(profile=profile, directory=d, input_data=inp,
                              pseudopotentials={'C': 'C.upf', 'H': 'H.upf'}, kpts=(1, 1, 1))
    if relax:
        BFGS(atoms, trajectory=f'{d}/relax.traj', append_trajectory=True,
             logfile=f'{d}/relax.log').run(fmax=0.01, steps=200)
    e = atoms.get_potential_energy()
    try:
        mag = float(atoms.get_magnetic_moment())
    except Exception:
        mag = float('nan')
    write(f'{d}/final.vasp', atoms, format='vasp', direct=False)
    json.dump({'e': e, 'mag': mag}, open(f'{d}/result.json', 'w'))
    print(f"   {tag:<24} E = {e:14.6f} eV   magnetization = {mag:6.3f} muB", flush=True)
    return e, atoms


def ch_geometry(slab_atoms, h):
    """C under H rise and C-H bond length."""
    d = h.get_distances(len(h) - 1, range(len(h) - 1), mic=True)
    j = d.argmin()
    zc = [p[2] for k, p in enumerate(h.positions[:-1]) if k != j]
    return d.min(), h[j].position[2] - sum(zc) / len(zc)


h_atom, c8, ch8 = read('h.vasp'), read('c.vasp'), read('ch.vasp')
c18 = read('c18.vasp')
ch18 = c18.copy()
ch18.append(Atom('H', (3.701586008, 2.137111678, 8.7)))   # on top of a C atom, 1.2 A above, as in ch.vasp
res = []

print("1. Course protocol (no starting magnetization, unrelaxed C8)")
eH0, _ = run(h_atom, 'H_atom_nomag')
eC8, _ = run(c8, 'C8_unrelaxed')
eCH0, ch8_0 = run(ch8, 'HC8_nomag_relax', relax=True)
res.append(('C8, course protocol', eC8 + eH0 - eCH0, *ch_geometry(c8, ch8_0)))

print("2. Relaxed C8 slab")
eC8r, c8r = run(c8, 'C8_relax', relax=True)
res.append(('C8 relaxed slab', eC8r + eH0 - eCH0, *ch_geometry(c8, ch8_0)))

print("3. Spin-polarized H atom and H@C8")
eH1, _ = run(h_atom, 'H_atom_spin', spin=True)
eCH1, ch8_1 = run(ch8_0, 'HC8_spin_relax', spin=True, relax=True)
res.append(('C8 relaxed, spin-polarized', eC8r + eH1 - eCH1, *ch_geometry(c8, ch8_1)))

print("4. Higher ecutwfc (single points, spin-polarized)")
for ec in (100, 120):
    eh, _ = run(h_atom, f'H_atom_spin_ecut{ec}', ecut=ec, spin=True)
    ec8, _ = run(c8r, f'C8_relax_geom_ecut{ec}', ecut=ec)
    ech, _ = run(ch8_1, f'HC8_spin_geom_ecut{ec}', ecut=ec, spin=True)
    res.append((f'C8, spin, ecutwfc {ec} Ry', ec8 + eh - ech, *ch_geometry(c8, ch8_1)))

print("5. H on C18 (3x3), spin-polarized")
eC18, _ = run(c18, 'C18')
eCH18, ch18_1 = run(ch18, 'HC18_spin_relax', spin=True, relax=True)
res.append(('C18, spin-polarized', eC18 + eH1 - eCH18, *ch_geometry(c18, ch18_1)))

print(f"\n{'Model':<30}{'E_b (eV)':>10}{'C-H (A)':>10}{'C pucker (A)':>14}")
print('-' * 64)
for name, eb, dch, dz in res:
    print(f"{name:<30}{eb:10.3f}{dch:10.3f}{dz:14.3f}")
print("\nE_b = E(slab) + E(H) - E(H@slab); 'C pucker' = height of the C atom below H above the mean C plane")
print(f"Spin-polarization energy of the isolated H atom: E(H, non-magnetic) - E(H, spin) = {eH0 - eH1:.3f} eV")
