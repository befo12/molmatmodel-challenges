"""Challenge II.8 (Hg on C18): adsorption energy on the on-top, bridge and hollow sites.

E_ads = E(Hg@C18) - E(C18) - E(Hg)   (negative = bound)
top = course run (this directory); bridge / hollow = course script with the Hg atom moved
laterally (site_bridge/, site_hollow/). E(C18) and E(Hg) from the course single points.

The final site is identified from the distances to the nearest C atoms (no atoms are fixed in the
course script, so the whole system may translate during BFGS; absolute coordinates are therefore
not compared). The graphene distortion is shown by the range of C-C bond lengths
(ideal flat graphene: all 1.425 A).
"""
import re
import numpy as np
from ase.io import read
from ase.neighborlist import neighbor_list

SITES = {'top': '.', 'bridge': 'site_bridge', 'hollow': 'site_hollow'}


def grab(fname, pattern):
    return float(re.findall(pattern + r'\s*:?\s*([-\d.]+)', open(fname).read())[-1])


def site_of(dist):
    """top: 1 nearest C; bridge: 2 equidistant; hollow: 6 equidistant (tolerance 0.05 A)."""
    d = np.sort(dist)
    n = int((d < d[0] + 0.05).sum())
    return {1: 'top', 2: 'bridge', 6: 'hollow'}.get(n, f'{n} C')


e_c18 = grab('energy_c18.out', 'Total energy')
e_hg = grab('energy_Hg.out', 'Total energy')
print(f"E(C18) = {e_c18:.6f} eV, E(Hg) = {e_hg:.6f} eV\n")
print(f"{'start':<8}{'E(Hg@C18)/eV':>15}{'E_ads/eV':>10}{'kJ/mol':>8}{'h(Hg)/A':>9}"
      f"{'d(Hg-C)/A':>11}{'final':>8}{'C-C min/max (A)':>17}{'dE relax/eV':>13}{'steps':>7}")
print('-' * 106)
for site, d in SITES.items():
    e = grab(f'{d}/relaxation_Hg_C18.out', 'Total Energy')
    traj = read(f'{d}/relaxation.traj', ':')
    a = traj[-1]
    ihg = [i for i, s in enumerate(a.get_chemical_symbols()) if s == 'Hg'][0]
    ic = [i for i, s in enumerate(a.get_chemical_symbols()) if s == 'C']
    dist = a.get_distances(ihg, ic, mic=True)
    h = a[ihg].position[2] - np.mean(a.positions[ic, 2])
    _, _, dcc = neighbor_list('ijd', a[ic], 1.8)
    de = traj[-1].get_potential_energy() - traj[0].get_potential_energy()
    eads = e - e_c18 - e_hg
    print(f"{site:<8}{e:15.6f}{eads:10.3f}{eads*96.485:8.1f}{h:9.3f}{dist.min():11.3f}{site_of(dist):>8}"
          f"{dcc.min():9.3f}/{dcc.max():.3f}{de:13.3f}{len(traj)-1:7d}")
print("\nh(Hg) = height of Hg above the mean C plane; d(Hg-C) = shortest Hg-C distance;"
      "\nfinal = site from the nearest-C pattern; dE relax = E(last) - E(first BFGS step)")
