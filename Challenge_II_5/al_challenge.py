"""Challenge II.5: Al from the experimental structure -> convergence test -> relaxation (EOS)
-> electronic properties with the relaxed cell and converged parameters.
Experimental structure: fcc Al, Fm-3m, a = 4.0495 A (room temperature; Wyckoff,
Crystal Structures 1963 / COD 9008460). Same pseudopotential (Al.upf) and smearing as the course."""
import os, re, subprocess
import numpy as np
from ase.build import bulk
from ase.eos import EquationOfState
from ase.units import GPa
from ase.calculators.espresso import Espresso, EspressoProfile
os.environ['OMP_NUM_THREADS'] = '1'
A_EXP = 4.0495
TOL = 1.0   # meV/atom between successive steps
profile = EspressoProfile(command='mpirun -np 6 pw.x', pseudo_dir=os.path.abspath('.'))

def energy(a, ecut, k, tag):
    atoms = bulk('Al', 'fcc', a=a)
    atoms.calc = Espresso(profile=profile, directory=f'runs/{tag}', pseudopotentials={'Al': 'Al.upf'},
        input_data={'control': {'calculation': 'scf', 'outdir': './tmp'},
                    'system': {'ecutwfc': ecut, 'occupations': 'smearing', 'smearing': 'gauss', 'degauss': 0.01},
                    'electrons': {'conv_thr': 1e-10}},
        kpts=(k, k, k))
    return atoms.get_potential_energy(), atoms.get_volume()

print(f"1. ecutwfc convergence at k = 12x12x12, a = {A_EXP} A (tolerance {TOL} meV/atom)")
prev, ecut_conv = None, None
for ec in range(20, 105, 5):
    e, _ = energy(A_EXP, ec, 12, f'ecut_{ec}')
    d = None if prev is None else 1000 * (e - prev)
    print(f"   ecutwfc = {ec:3d} Ry  E = {e:.6f} eV" + ("" if d is None else f"  dE = {d:8.3f} meV"), flush=True)
    if d is not None and abs(d) < TOL:
        ecut_conv = ec
        break
    prev = e
ecut_conv = ecut_conv or 100
print(f">>> ecutwfc converged at {ecut_conv} Ry")

print(f"\n2. k-point convergence at ecutwfc = {ecut_conv} Ry")
prev, k_conv = None, None
for k in range(4, 33, 2):
    e, _ = energy(A_EXP, ecut_conv, k, f'k_{k}')
    d = None if prev is None else 1000 * (e - prev)
    print(f"   k = {k:2d}x{k:2d}x{k:2d}  E = {e:.6f} eV" + ("" if d is None else f"  dE = {d:8.3f} meV"), flush=True)
    if d is not None and abs(d) < TOL:
        k_conv = k
        break
    prev = e
k_conv = k_conv or 32
print(f">>> k-points converged at {k_conv}x{k_conv}x{k_conv}")

print(f"\n3. Equation of state around a_exp (ecutwfc = {ecut_conv} Ry, k = {k_conv})")
vols, ens = [], []
for s in np.linspace(0.97, 1.03, 7):
    e, v = energy(A_EXP * s, ecut_conv, k_conv, f'eos_{s:.3f}')
    vols.append(v); ens.append(e)
    print(f"   a = {A_EXP*s:.4f} A  V = {v:.4f} A^3  E = {e:.6f} eV", flush=True)
eos = EquationOfState(vols, ens, eos='birchmurnaghan')
v0, e0, B = eos.fit()
a0 = (4 * v0) ** (1 / 3)
eos.plot('al_eos.png')
print(f">>> relaxed a0 = {a0:.4f} A (exp. {A_EXP} A, {100*(a0-A_EXP)/A_EXP:+.2f} %), "
      f"V0 = {v0:.4f} A^3, B = {B/GPa:.1f} GPa (exp. ~76 GPa)")

os.makedirs('relaxed_electronic', exist_ok=True)
src = open('electronic_properties_al.py').read()
src = src.replace('2.0194648450', f'{a0/2:.10f}')
src = src.replace("'ecutwfc': 65,", f"'ecutwfc': {ecut_conv},")
src = src.replace('scf_kpts = (15,15,15)', f'scf_kpts = ({k_conv},{k_conv},{k_conv})')
src = src.replace('nscf_kpts = (30, 30, 30)', f'nscf_kpts = ({2*k_conv}, {2*k_conv}, {2*k_conv})')
open('relaxed_electronic/electronic_properties_al_relaxed.py', 'w').write(src)
subprocess.run('cp Al.upf relaxed_electronic/ && cd relaxed_electronic && '
               'python electronic_properties_al_relaxed.py > electronic_properties_al_relaxed.out 2>&1',
               shell=True, check=True)
print(f"\n4. Electronic properties with a0 = {a0:.4f} A, ecutwfc = {ecut_conv} Ry, k(SCF) = {k_conv}, k(NSCF) = {2*k_conv}:")
for line in open('relaxed_electronic/electronic_properties_al_relaxed.out'):
    if re.search(r'Fermi level|Integrated|Relative difference', line):
        print('  ' + line.strip())
