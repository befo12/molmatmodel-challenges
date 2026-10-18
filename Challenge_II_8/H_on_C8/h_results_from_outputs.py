"""Challenge II.8 (H on graphene): collect the results of h_adsorption_challenges.py from the
QE outputs in runs/ (the driver was interrupted by a hardware shutdown during the last step,
H@C18, so its own summary table was not printed; all other steps had finished).

E_b = E(slab) + E(H) - E(H@slab)   (positive = bound)
H@C18: last BFGS step of runs/HC18_spin_relax/relax.traj (NOT converged, see readme)."""
import numpy as np
from ase.io import read

E = {}
for t in ['H_atom_nomag', 'C8_unrelaxed', 'HC8_nomag_relax', 'C8_relax', 'H_atom_spin', 'HC8_spin_relax',
          'H_atom_spin_ecut100', 'C8_relax_geom_ecut100', 'HC8_spin_geom_ecut100',
          'H_atom_spin_ecut120', 'C8_relax_geom_ecut120', 'HC8_spin_geom_ecut120', 'C18']:
    E[t] = read(f'runs/{t}/espresso.pwo', format='espresso-out').get_potential_energy()
    print(f"{t:<24} E = {E[t]:16.6f} eV")
tr = read('runs/HC18_spin_relax/relax.traj', index=':')
e18, f18 = tr[-1].get_potential_energy(), np.abs(tr[-1].get_forces()).max()
print(f"{'HC18_spin_relax':<24} E = {e18:16.6f} eV  (BFGS step {len(tr)-1}, fmax = {f18:.3f} eV/A, not converged)")


def geo(h):
    d = h.get_distances(len(h) - 1, range(len(h) - 1), mic=True)
    j = d.argmin()
    zc = [p[2] for k, p in enumerate(h.positions[:-1]) if k != j]
    return d.min(), h[j].position[2] - np.mean(zc)


g0 = geo(read('runs/HC8_nomag_relax/final.vasp'))
g1 = geo(read('runs/HC8_spin_relax/final.vasp'))
rows = [('C8, course protocol', E['C8_unrelaxed'] + E['H_atom_nomag'] - E['HC8_nomag_relax'], *g0),
        ('C8 relaxed slab', E['C8_relax'] + E['H_atom_nomag'] - E['HC8_nomag_relax'], *g0),
        ('C8 relaxed, spin-polarized', E['C8_relax'] + E['H_atom_spin'] - E['HC8_spin_relax'], *g1)]
for ec in (100, 120):
    rows.append((f'C8, spin, ecutwfc {ec} Ry',
                 E[f'C8_relax_geom_ecut{ec}'] + E[f'H_atom_spin_ecut{ec}'] - E[f'HC8_spin_geom_ecut{ec}'], *g1))
rows.append(('C18, spin (not converged)', E['C18'] + E['H_atom_spin'] - e18, *geo(tr[-1])))
print(f"\n{'Model':<30}{'E_b (eV)':>10}{'C-H (A)':>10}{'C pucker (A)':>14}")
print('-' * 64)
for name, eb, dch, dz in rows:
    print(f"{name:<30}{eb:10.3f}{dch:10.3f}{dz:14.3f}")
print("\n'C pucker' = height of the C atom bonded to H above the mean plane of the other C atoms")
print(f"Spin-polarization energy of the isolated H atom: {E['H_atom_nomag'] - E['H_atom_spin']:.3f} eV")
print(f"Energy change on relaxing the clean C8 slab: {1000*(E['C8_relax'] - E['C8_unrelaxed']):.2f} meV")
print(f"Magnetic moment: H atom 1.00 muB, H@C8 1.00 muB (spin-polarized runs), see runs/*/espresso.pwo")
