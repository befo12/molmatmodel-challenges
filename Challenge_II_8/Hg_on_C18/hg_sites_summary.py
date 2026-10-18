"""Challenge II.8 (Hg on C18): adsorption energy on the on-top, bridge and hollow sites.

E_ads = E(Hg@C18) - E(C18) - E(Hg)   (negative = bound)
top = course run (this directory); bridge / hollow = course script with the Hg atom moved
laterally (site_bridge/, site_hollow/). E(C18) and E(Hg) from the course single points.
"""
import re
import numpy as np
from ase.io import read

SITES = {'top': ('.', (3.701586008, 2.137111678)),
         'bridge': ('site_bridge', (3.701586008, 2.849482402)),
         'hollow': ('site_hollow', (4.935448011, 2.849482402))}


def grab(fname, pattern):
    return float(re.findall(pattern + r'\s*:?\s*([-\d.]+)', open(fname).read())[-1])


e_c18 = grab('energy_c18.out', 'Total energy')
e_hg = grab('energy_Hg.out', 'Total energy')
print(f"E(C18) = {e_c18:.6f} eV, E(Hg) = {e_hg:.6f} eV\n")
print(f"{'site':<8}{'E(Hg@C18)/eV':>15}{'E_ads/eV':>10}{'E_ads/kJmol':>12}{'h(Hg)/A':>9}{'d(Hg-C)min/A':>14}"
      f"{'lateral shift/A':>16}{'#C within 3.9 A':>17}")
print('-' * 101)
for site, (d, (x0, y0)) in SITES.items():
    e = grab(f'{d}/relaxation_Hg_C18.out', 'Total Energy')
    a = read(f'{d}/final_relaxed_structure.vasp')
    ihg = [i for i, s in enumerate(a.get_chemical_symbols()) if s == 'Hg'][0]
    ic = [i for i, s in enumerate(a.get_chemical_symbols()) if s == 'C']
    dist = a.get_distances(ihg, ic, mic=True)
    h = a[ihg].position[2] - np.mean(a.positions[ic, 2])
    # lateral displacement of Hg relative to the slab (minimum image in the xy plane)
    vec = np.array([a[ihg].position[0] - x0, a[ihg].position[1] - y0, 0.0])
    frac = np.linalg.solve(a.cell.array.T, vec)
    frac[:2] -= np.round(frac[:2])
    lat = np.linalg.norm(a.cell.array.T @ frac)
    eads = e - e_c18 - e_hg
    print(f"{site:<8}{e:15.6f}{eads:10.3f}{eads*96.485:12.1f}{h:9.3f}{dist.min():14.3f}{lat:16.3f}"
          f"{int((dist < 3.9).sum()):17d}")
print("\nh(Hg) = height of Hg above the mean C plane; lateral shift = in-plane distance moved from the initial site")
