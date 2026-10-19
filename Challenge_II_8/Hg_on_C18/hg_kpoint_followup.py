"""Challenge II.8, Hg on C18 - follow-up: is the bridge / hollow preference real or an artefact of
Gamma-only sampling? Course settings (PBE + DFT-D3, 80 Ry, Gaussian 0.01 Ry) with different k-grids:
flat graphene + Hg 3.4 A above top / bridge / hollow; the Gamma-relaxed (Kekule-distorted) bridge /
hollow structures with and without Hg; flat C18 and the Hg atom as references.
E_ads = E(Hg@C18) - E(C18, flat) - E(Hg); E_dist = E(distorted sheet) - E(flat sheet).
Run:  python -u hg_kpoint_followup.py > hg_kpoint_followup.py.log 2>&1   (results kept in kfollow/)
"""
import sys, os
from ase.io import read
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qe_k import single_point

flat = read('c18.vasp')
hg = read('hg.vasp')
start = {'top': read('c18_hg.vasp'), 'bridge': read('site_bridge/c18_hg.vasp'),
         'hollow': read('site_hollow/c18_hg.vasp')}
relaxed = {s: read(f'site_{s}/relaxation.traj', -1) for s in ('bridge', 'hollow')}
sheet = {}
for s, a in relaxed.items():
    b = a.copy()
    del b[[x.index for x in b if x.symbol == 'Hg']]
    sheet[s] = b
GRIDS = [(1, 1, 1), (3, 3, 1), (6, 6, 1)]


def E(name, atoms, k):
    r = single_point(atoms, f'kfollow/{name}_k{k[0]}', k)
    print(f"   {name:<26} k={k[0]}x{k[1]}x{k[2]}  E = {r['E']:16.6f} eV", flush=True)
    return r['E']


rows = []
for k in GRIDS:
    print(f"k-grid {k[0]}x{k[1]}x{k[2]}", flush=True)
    e_c = E('C18_flat', flat, k)
    e_hg = E('Hg_atom', hg, k)
    r = {'k': k}
    for s in ('top', 'bridge', 'hollow'):
        r[f'ads_flat_{s}'] = E(f'HgC18_{s}_flat', start[s], k) - e_c - e_hg
    for s in ('bridge', 'hollow'):
        r[f'dist_{s}'] = E(f'C18_{s}_distorted', sheet[s], k) - e_c
        r[f'ads_relaxG_{s}'] = E(f'HgC18_{s}_relaxedGamma', relaxed[s], k) - e_c - e_hg
    rows.append(r)

print("\nk-grid   E_ads flat: top / bridge / hollow   E_dist: bridge / hollow   E_ads Gamma-relaxed: bridge / hollow  (eV)")
for r in rows:
    k = r['k']
    print(f"{k[0]}x{k[1]}x{k[2]:<4}{r['ads_flat_top']:9.3f}{r['ads_flat_bridge']:9.3f}{r['ads_flat_hollow']:9.3f}  "
          f"{r['dist_bridge']:9.3f}{r['dist_hollow']:9.3f}  {r['ads_relaxG_bridge']:9.3f}{r['ads_relaxG_hollow']:9.3f}")
