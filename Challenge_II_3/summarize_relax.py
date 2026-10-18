"""Challenge II.3: summary table of all Si cell relaxations (direct QE vc-relax and ASE-driven QE)."""
import os
import numpy as np
from ase.io import read
EXP_A = 5.431
EV_A3_TO_KBAR = 1602.1766208
rows = []
for run in ['default', 'tight_shifted']:
    qe_out = f'{run}/cell_relaxation_si_direct.out'
    if os.path.exists(qe_out):
        a = read(qe_out, format='espresso-out', index=-1)
        n_scf = sum(1 for line in open(qe_out) if line.startswith('!'))
        rows.append((f'QE vc-relax ({run})', a, n_scf))
    traj = f'{run}/relaxation.traj'
    if os.path.exists(traj):
        images = read(traj, index=':')
        rows.append((f'ASE-QE BFGS ({run})', images[-1], len(images)))
print(f"{'Run':<30}{'E/eV':>14}{'P/kbar':>9}{'Fmax/eV/A':>11}{'V/A^3':>9}{'a/A':>9}{'Si-Si/A':>9}{'#SCF':>6}")
print('-' * 97)
for name, at, n in rows:
    e = at.get_potential_energy()
    try:
        p = -np.trace(at.get_stress(voigt=False)) / 3 * EV_A3_TO_KBAR
    except Exception:
        p = float('nan')
    fmax = np.abs(at.get_forces()).max()
    v = at.get_volume()
    print(f"{name:<30}{e:14.5f}{p:9.2f}{fmax:11.5f}{v:9.4f}{(4*v)**(1/3):9.4f}{at.get_distance(0, 1, mic=True):9.4f}{n:6d}")
print(f"\nExperimental lattice constant a = {EXP_A} A, Si-Si = {EXP_A*np.sqrt(3)/4:.4f} A")
