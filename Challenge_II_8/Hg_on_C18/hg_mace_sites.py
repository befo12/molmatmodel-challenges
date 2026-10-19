"""Challenge II.8, Hg on C18 - MACE foundation models vs DFT for the three adsorption sites.
Same structures as the DFT runs (Hg 3.4 A above the top / bridge / hollow site). MACE-MP is trained
on PBE data without dispersion; the DFT runs use PBE + DFT-D3(BJ) (QE dftd3_version = 4), so each
model is also run with D3(BJ) added (mace_mp(dispersion=True), torch-dftd). For each model: single
points on flat graphene, then a full BFGS relaxation (fmax 0.01 eV/A, no atoms fixed).
E_ads = E(Hg@C18) - E(C18, relaxed) - E(Hg atom).
Run in Challenge_II_8/Hg_on_C18:  python -u hg_mace_sites.py > hg_mace_sites.py.log 2>&1
"""
import warnings
warnings.filterwarnings('ignore')
import numpy as np
from ase.io import read
from ase.optimize import BFGS
from ase.neighborlist import neighbor_list
from mace.calculators import mace_mp

flat = read('c18.vasp')
hg = read('hg.vasp')
start = {'top': read('c18_hg.vasp'), 'bridge': read('site_bridge/c18_hg.vasp'),
         'hollow': read('site_hollow/c18_hg.vasp')}


def site_of(a):
    ihg = [i for i, s in enumerate(a.get_chemical_symbols()) if s == 'Hg'][0]
    ic = [i for i, s in enumerate(a.get_chemical_symbols()) if s == 'C']
    d = np.sort(a.get_distances(ihg, ic, mic=True))
    n = int((d < d[0] + 0.05).sum())
    _, _, dcc = neighbor_list('ijd', a[ic], 1.8)
    h = a.positions[ihg, 2] - a.positions[ic, 2].mean()
    return {1: 'top', 2: 'bridge', 6: 'hollow'}.get(n, f'{n} C'), h, dcc.min(), dcc.max()


for model, disp in (('medium', False), ('medium-mpa-0', False), ('medium', True), ('medium-mpa-0', True)):
    calc = mace_mp(model=model, default_dtype='float64', device='cpu', dispersion=disp, damping='bj')
    label = model + (' + D3(BJ)' if disp else '')

    def energy(a):
        a = a.copy(); a.calc = calc
        return a.get_potential_energy()

    def relax(a):
        a = a.copy(); a.calc = calc
        opt = BFGS(a, logfile=None)
        opt.run(fmax=0.01, steps=500)
        return a.get_potential_energy(), a, opt.nsteps

    e_hg = energy(hg)
    e_c_flat = energy(flat)
    e_c, c_rel, _ = relax(flat)
    print(f"\nMACE-MP {label}: E(Hg) = {e_hg:.6f} eV, E(C18 flat) = {e_c_flat:.6f} eV, "
          f"E(C18 relaxed) = {e_c:.6f} eV")
    print(f"{'start':<8}{'E_ads flat/eV':>14}{'E_ads relaxed/eV':>18}{'final':>8}{'h(Hg)/A':>9}"
          f"{'C-C min/max (A)':>17}{'steps':>7}")
    for s, a in start.items():
        ef = energy(a) - e_c_flat - e_hg
        er, ar, n = relax(a)
        site, h, cmin, cmax = site_of(ar)
        print(f"{s:<8}{ef:14.3f}{er - e_c - e_hg:18.3f}{site:>8}{h:9.3f}{cmin:9.3f}/{cmax:.3f}{n:7d}")
print("\nE_ads flat = Hg at 3.4 A over flat graphene (no relaxation); relaxed = full BFGS relaxation")
